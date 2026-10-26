"""LLM layer: one interface, swappable providers (design §54)."""

import logging

from services.common.config import settings
from services.llm.base import LLMError, LLMProvider, LLMResult, QuotaExhausted
from services.llm.stub_provider import StubLLM

logger = logging.getLogger(__name__)

__all__ = [
    "LLMError",
    "LLMProvider",
    "LLMResult",
    "QuotaExhausted",
    "StubLLM",
    "allowance_back_in",
    "get_llm_provider",
    "get_persona_llm_provider",
    "set_llm_provider",
]

_provider: LLMProvider | None = None


def get_llm_provider() -> LLMProvider:
    """Process-wide provider chosen from settings.

    Defaults to the stub so a fresh clone runs the whole pipeline offline. Set
    `LLM_PROVIDER` to `anthropic` or `openai` (plus `LLM_API_KEY` and a matching
    `LLM_MODEL`) for real evaluation.
    """
    global _provider
    if _provider is None:
        choice = settings.llm_provider.lower()
        if choice == "anthropic":
            from services.llm.anthropic_provider import AnthropicProvider

            _provider = AnthropicProvider()
        elif choice == "openai":
            from services.llm.openai_provider import OpenAIProvider

            _provider = OpenAIProvider()
        else:
            _provider = StubLLM()
        logger.info(
            "llm provider selected",
            extra={"provider": _provider.name, "model": _provider.model},
        )
    return _provider



def allowance_back_in() -> float | None:
    """Seconds until GD's models have allowance again, when every one of them is
    out past a busy minute (a daily cap); None while any has headroom, and for a
    provider with no published caps."""
    if settings.llm_provider.lower() != "openai":
        return None
    from services.llm import openai_provider

    fallbacks = [m.strip() for m in settings.llm_fallback_models.split(",") if m.strip()]
    models = [m for m in (settings.llm_model, settings.persona_llm_model.strip(), *fallbacks) if m]
    return openai_provider.allowance_back_in(list(dict.fromkeys(models)))


_persona_provider: LLMProvider | None = None


def get_persona_llm_provider() -> LLMProvider:
    """The model that voices the practice personas.

    A small fast model is plenty for a one-sentence spoken line, and latency is
    what the student feels. Falls back to the main provider when no persona model
    is configured, or when the main provider is not a real vendor (stub, tests).
    """
    global _persona_provider
    base = get_llm_provider()
    model = settings.persona_llm_model.strip()
    url = settings.persona_llm_base_url.strip()
    if not model or base.name not in {"openai", "anthropic"}:
        return base
    if base.model == model and not url:
        return base
    if _persona_provider is None or _persona_provider.model != model:
        if base.name == "openai":
            from services.llm.openai_provider import OpenAIProvider

            # A persona vendor of its own when a base URL is set (abhinav, arena-fast);
            # otherwise the main endpoint and key.
            _persona_provider = OpenAIProvider(
                model=model,
                api_key=settings.persona_llm_api_key.strip() or None,
                base_url=url or None,
            )
        else:
            from services.llm.anthropic_provider import AnthropicProvider

            _persona_provider = AnthropicProvider(model=model)
    return _persona_provider


def set_llm_provider(provider: LLMProvider | None) -> None:
    """Override the provider. Used by tests and by the evaluation worker."""
    global _provider
    _provider = provider
