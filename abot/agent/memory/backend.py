"""Abstract memory backend interface."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from abot.providers.base import LLMProvider


class MemoryBackend(ABC):
    """Abstract interface for memory backends. Implementations handle MEMORY.md and optional storage."""

    @abstractmethod
    def read_long_term(self) -> str:
        """Read the current long-term memory content (e.g. MEMORY.md)."""
        pass

    @abstractmethod
    async def consolidate_and_save(
        self,
        turns: list[list[dict]],
        provider: LLMProvider,
        model: str,
    ) -> bool:
        """
        Consolidate turns via LLM and persist to long-term memory.

        Args:
            turns: List of turns, each turn is a list of message dicts.
            provider: LLM provider for consolidation.
            model: Model name for consolidation.

        Returns:
            True on success, False on failure.
        """
        pass
