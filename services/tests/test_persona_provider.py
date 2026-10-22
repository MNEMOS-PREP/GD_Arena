"""The persona model may live on a different vendor from evaluation."""

from services.common.config import settings
from services.llm import get_persona_llm_provider, set_llm_provider
from services.llm.openai_provider import OpenAIProvider


def test_persona_provider_uses_its_own_endpoint_and_key(monkeypatch):
    import services.llm as llm

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
    import asyncio
    from types import SimpleNamespace

    from services.llm import openai_provider

    monkeypatch.setattr(openai_provider, "HEDGE_AFTER_SECONDS", 0.05)
    calls = 0

    async def create(**_):
        nonlocal calls
        calls += 1
        if calls == 1:
            await asyncio.sleep(30)  # the stalled call
        message = SimpleNamespace(content="Fair point.")
        return SimpleNamespace(
            choices=[SimpleNamespace(message=message, finish_reason="stop")],
            usage=None,
            model="m",
        )

    provider = OpenAIProvider(model="m", api_key="k")
    provider._client = SimpleNamespace(
        chat=SimpleNamespace(completions=SimpleNamespace(create=create))
    )
    result = await asyncio.wait_for(provider.complete_text(system="s", prompt="p"), timeout=5)
    assert result.raw_text == "Fair point." and calls == 2
