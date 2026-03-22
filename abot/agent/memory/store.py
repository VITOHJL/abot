"""MemoryStore: backward-compatible wrapper around MemoryBackend."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from abot.agent.memory.backend import MemoryBackend
from abot.agent.memory.file_backend import FileMemoryBackend

if TYPE_CHECKING:
    from abot.providers.base import LLMProvider


class MemoryStore:
    """
    Memory store wrapping a MemoryBackend.

    Provides get_memory_context and consolidate_chunk for backward compatibility.
    Uses FileMemoryBackend by default (MEMORY.md only, no HISTORY.md).
    """

    def __init__(self, workspace: Path, backend: MemoryBackend | None = None):
        self._backend = backend or FileMemoryBackend(workspace)

    def read_long_term(self) -> str:
        return self._backend.read_long_term()

    def get_memory_context(self) -> str:
        long_term = self.read_long_term()
        return f"## Long-term Memory\n{long_term}" if long_term else ""

    async def consolidate_chunk(
        self,
        messages: list[dict],
        provider: LLMProvider,
        model: str,
    ) -> tuple[bool, str | None]:
        """
        Consolidate messages into long-term memory via backend.

        Converts flat messages to turns (by splitting on user boundaries) for the backend.
        Returns (success, None).
        """
        if not messages:
            return True, None

        turns = self._split_into_turns(messages)
        success = await self._backend.consolidate_and_save(turns, provider, model)
        return success, None

    @staticmethod
    def _split_into_turns(messages: list[dict]) -> list[list[dict]]:
        """Split flat messages into turns (user -> next user exclusive)."""
        turns: list[list[dict]] = []
        i = 0
        while i < len(messages):
            if messages[i].get("role") != "user":
                i += 1
                continue
            turn: list[dict] = []
            while i < len(messages):
                turn.append(messages[i])
                i += 1
                if i < len(messages) and messages[i].get("role") == "user":
                    break
            turns.append(turn)
        return turns
