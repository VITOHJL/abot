"""Turn storage abstraction for compressed conversation turns."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class TurnRecord:
    """A single turn record for storage/retrieval."""

    def __init__(
        self,
        turn_id: str,
        session_key: str,
        ts: str,
        user_question: str,
        final_result: str,
        messages: list[dict[str, Any]],
    ):
        self.turn_id = turn_id
        self.session_key = session_key
        self.ts = ts
        self.user_question = user_question
        self.final_result = final_result
        self.messages = messages


class TurnStore(ABC):
    """Abstract interface for storing and retrieving turn records."""

    @abstractmethod
    def save_turns(
        self,
        turns: list[list[dict]],
        session_key: str,
    ) -> list[str]:
        """
        Save turns and return list of turn_ids.

        Args:
            turns: List of turns, each turn is a list of message dicts.
            session_key: Session identifier (e.g. cli:direct).

        Returns:
            List of turn_id for each saved turn.
        """
        pass

    @abstractmethod
    def get_turn(self, turn_id: str) -> TurnRecord | None:
        """Get a single turn by turn_id."""
        pass

    @abstractmethod
    def get_turns_with_context(
        self,
        turn_id: str,
        context_turns: int = 0,
    ) -> list[TurnRecord]:
        """
        Get a turn and optionally surrounding turns.

        Args:
            turn_id: The center turn.
            context_turns: Number of turns before and after to include (0 = only the turn).

        Returns:
            List of TurnRecords, ordered by time.
        """
        pass
