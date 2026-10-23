"""Response generation adapters used by the assistant service."""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

from assistant_core.errors import ProviderError

if TYPE_CHECKING:
    from assistant_core.knowledge import Rule


class Responder(Protocol):
    """Interface implemented by response generation backends."""

    def explain(self, question: str, rule: Rule) -> str:
        """Explain a matched rule in the context of a user's question."""
        ...


class TemplateResponder:
    """Generate a deterministic response without an external provider."""

    def explain(self, question: str, rule: Rule) -> str:
        """Return the rule title and text as a plain, reliable fallback."""
        del question  # The template does not need the original user text.
        return f"{rule.title}: {rule.text}"


class StubLLMResponder:
    """Stand-in for an LLM provider, with an option to simulate an outage."""

    def __init__(self, fail: bool = False) -> None:
        self.fail = fail

    def explain(self, question: str, rule: Rule) -> str:
        """Return a predictable answer or raise the provider's domain error."""
        del question  # The stub deliberately avoids storing or logging user text.
        if self.fail:
            raise ProviderError("stub provider unavailable")
        return f"Based on '{rule.title}': {rule.text}"
