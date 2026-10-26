"""The persona model: its own vendor if asked, a hedged plain-text line, and a
first reply written while the student is still being heard out (abhinav's
arena-fast, on the panel)."""

import asyncio
from types import SimpleNamespace

import pytest
from httpx import AsyncClient

import services.llm as llm
from services.common.config import settings
from services.llm import QuotaExhausted, get_persona_llm_provider, openai_provider, set_llm_provider
from services.llm.openai_provider import OpenAIProvider
from services.practice import engine
from services.practice.engine import Line
from services.speech.stt import StubSTT, set_stt_provider
from services.speech.tts import StubTTS, set_tts_provider

from .test_practice import _live_practice, _room


def _reply(text: str):
    message = SimpleNamespace(content=text)
    return SimpleNamespace(
        choices=[SimpleNamespace(message=message, finish_reason="stop")], usage=None, model="m"
    )


def _provider(create) -> OpenAIProvider:
    provider = OpenAIProvider(model="m", api_key="k")
    provider._slots = None  # whatever LLM_MAX_CONCURRENCY the local .env says
    provider._client = SimpleNamespace(
        chat=SimpleNamespace(completions=SimpleNamespace(create=create))
    )
    return provider


def test_persona_provider_uses_its_own_endpoint_and_key(monkeypatch):
    monkeypatch.setattr(llm, "_persona_provider", None)
    monkeypatch.setattr(settings, "persona_llm_model", "llama-3.1-8b-instant")
    monkeypatch.setattr(settings, "persona_llm_base_url", "https://api.groq.com/openai/v1")
    monkeypatch.setattr(settings, "persona_llm_api_key", "groq-key")
    set_llm_provider(OpenAIProvider(model="gemini-3.5-flash-lite", api_key="gem-key"))
    try:
        persona = get_persona_llm_provider()
        assert persona.model == "llama-3.1-8b-instant"
        assert persona._base_url == "https://api.groq.com/openai/v1"
        assert persona._api_key == "groq-key"
    finally:
        set_llm_provider(None)
        monkeypatch.setattr(llm, "_persona_provider", None)


def test_persona_provider_defaults_to_the_main_one(monkeypatch):
    monkeypatch.setattr(settings, "persona_llm_model", "")
    main = OpenAIProvider(model="gemini-3.5-flash-lite", api_key="k")
    set_llm_provider(main)
    try:
        assert get_persona_llm_provider() is main
    finally:
        set_llm_provider(None)


async def test_complete_text_hedges_a_stalled_call(monkeypatch):
    monkeypatch.setattr(openai_provider, "HEDGE_AFTER_SECONDS", 0.05)
    calls = 0

    async def create(**_):
        nonlocal calls
        calls += 1
        if calls == 1:
            await asyncio.sleep(30)  # the stalled call
        return _reply("Fair point.")

    result = await asyncio.wait_for(
        _provider(create).complete_text(system="s", prompt="p", max_tokens=400), timeout=5
    )
    assert result.raw_text == "Fair point." and calls == 2
    assert result.metadata["hedged"] is True


async def test_out_of_allowance_is_said_as_it_is_not_as_a_failed_call():
    """The room tells the student the panel is out of allowance (0b0a348): a
    hedge must not turn that into an ordinary failure."""

    async def create(**_):
        raise QuotaExhausted(3600.0)

    with pytest.raises(QuotaExhausted):
        await _provider(create).complete_text(system="s", prompt="p", max_tokens=400)


async def test_a_cancelled_line_cancels_its_requests(monkeypatch):
    """A line nobody waits for any more (the student carried on) must not keep
    its requests running: they spend the per-minute tokens the next line needs."""
    monkeypatch.setattr(openai_provider, "HEDGE_AFTER_SECONDS", 0.01)
    started, cancelled = 0, 0

    async def create(**_):
        nonlocal started, cancelled
        started += 1
        try:
            await asyncio.sleep(30)
        except asyncio.CancelledError:
            cancelled += 1
            raise

    line = asyncio.create_task(
        _provider(create).complete_text(system="s", prompt="p", max_tokens=400)
    )
    await asyncio.sleep(0.1)  # the first call and its hedge are both in flight
    line.cancel()
    with pytest.raises(asyncio.CancelledError):
        await line
    await asyncio.sleep(0.05)
    assert started == 2 and cancelled == 2


async def test_the_first_reply_is_written_while_the_student_is_heard_out(
    client: AsyncClient, candidate_auth: dict, session_factory, monkeypatch
):
    set_stt_provider(StubSTT())
    set_tts_provider(StubTTS())
    monkeypatch.setattr(engine, "CHAIN_PROBABILITY", 0.0)  # one persona answers
    session = await _live_practice(client, candidate_auth)
    room, sent = _room(session_factory, session["id"])
    await room.load()
    written = []

    async def generate(persona, when, cue=None, target="", repeated=""):
        written.append((persona["label"], room.user_active))
        return Line(speak=True, text="I see it differently.", is_conclusion=False)

    monkeypatch.setattr(room, "_generate", generate)
    await room._burst(hold=0.3)
    # Written once, at the start of the listen pause; that line is the one said.
    assert len(written) == 1
    said = [f["payload"]["text"] for f in sent if f.get("type") == "PERSONA_AUDIO_START"]
    assert said == ["I see it differently."]
    await room.close()


async def test_a_burst_dropped_before_it_spoke_still_owes_the_turn(
    client: AsyncClient, candidate_auth: dict, session_factory, monkeypatch
):
    """The first turn is chosen before the student has finished; if they carry
    on, a raised hand or a redirect it took is owed again, not lost."""
    set_stt_provider(StubSTT())
    set_tts_provider(StubTTS())
    monkeypatch.setattr(engine, "LISTEN_WAIT_LIMIT_SECONDS", 0.2)
    session = await _live_practice(client, candidate_auth)
    room, sent = _room(session_factory, session["id"])
    await room.load()
    owed = (next(iter(room.personas)), "hand", "")
    room.forced = owed
    room.user_active = True  # still talking: the burst gives up
    await room._burst(hold=0.0)
    assert room.forced == owed
    assert not any(f.get("type") == "PERSONA_AUDIO_START" for f in sent)
    await room.close()
