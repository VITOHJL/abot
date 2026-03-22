"""JSONL-based turn storage (lightweight, no SQLite dependency)."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from abot.agent.memory.turn_store import TurnRecord, TurnStore
from abot.utils.helpers import ensure_dir


def _extract_user_question(messages: list[dict]) -> str:
    """Extract the first user message content from a turn."""
    for m in messages:
        if m.get("role") == "user":
            content = m.get("content", "")
            if isinstance(content, str):
                return content
            if isinstance(content, list):
                for part in content:
                    if isinstance(part, dict) and part.get("type") == "text":
                        return part.get("text", "")
                return ""
    return ""


def _extract_final_result(messages: list[dict]) -> str:
    """Extract the last assistant message with content (the final answer)."""
    result = ""
    for m in reversed(messages):
        if m.get("role") == "assistant":
            content = m.get("content", "")
            if content and not m.get("tool_calls"):
                if isinstance(content, str):
                    return content
                if isinstance(content, list):
                    for part in content:
                        if isinstance(part, dict) and part.get("type") == "text":
                            return part.get("text", "")
                    return ""
            elif content:
                result = content if isinstance(content, str) else ""
    return result


def _make_turn_id(session_key: str, ts: str, user_question: str) -> str:
    """Generate a deterministic turn_id from session, timestamp, and user question."""
    raw = f"{session_key}:{ts}:{user_question[:200]}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


class JSONLTurnStore(TurnStore):
    """Store turns in JSONL files under memory/turns/."""

    def __init__(self, workspace: Path):
        self.turns_dir = ensure_dir(workspace / "memory" / "turns")
        self._index: dict[str, str] = {}  # turn_id -> file path
        self._load_index()

    def _load_index(self) -> None:
        """Load turn_id -> path index from turns/index.json if it exists."""
        idx_path = self.turns_dir / "index.json"
        if idx_path.exists():
            try:
                data = json.loads(idx_path.read_text(encoding="utf-8"))
                self._index = data.get("turns", {})
            except Exception:
                self._index = {}

    def _save_index(self) -> None:
        """Persist the index."""
        idx_path = self.turns_dir / "index.json"
        idx_path.write_text(
            json.dumps({"turns": self._index}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def save_turns(
        self,
        turns: list[list[dict]],
        session_key: str,
    ) -> list[str]:
        turn_ids: list[str] = []
        for turn_msgs in turns:
            if not turn_msgs:
                continue
            user_q = _extract_user_question(turn_msgs)
            final_a = _extract_final_result(turn_msgs)
            ts = ""
            for m in turn_msgs:
                if m.get("timestamp"):
                    ts = str(m.get("timestamp", ""))[:19]
                    break
            turn_id = _make_turn_id(session_key, ts, user_q)
            record = {
                "turn_id": turn_id,
                "session_key": session_key,
                "ts": ts,
                "user_question": user_q,
                "final_result": final_a,
                "messages": turn_msgs,
            }
            path = self.turns_dir / f"{session_key.replace(':', '_')}.jsonl"
            with open(path, "a", encoding="utf-8") as f:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
            self._index[turn_id] = str(path)
            turn_ids.append(turn_id)
        if turn_ids:
            self._save_index()
        return turn_ids

    def get_turn(self, turn_id: str) -> TurnRecord | None:
        path_str = self._index.get(turn_id)
        if not path_str:
            return self._scan_for_turn(turn_id)
        path = Path(path_str)
        if not path.exists():
            return None
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    if data.get("turn_id") == turn_id:
                        return TurnRecord(
                            turn_id=data["turn_id"],
                            session_key=data.get("session_key", ""),
                            ts=data.get("ts", ""),
                            user_question=data.get("user_question", ""),
                            final_result=data.get("final_result", ""),
                            messages=data.get("messages", []),
                        )
                except json.JSONDecodeError:
                    continue
        return None

    def _scan_for_turn(self, turn_id: str) -> TurnRecord | None:
        """Fallback: scan all jsonl files for the turn."""
        for path in self.turns_dir.glob("*.jsonl"):
            with open(path, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        data = json.loads(line)
                        if data.get("turn_id") == turn_id:
                            self._index[turn_id] = str(path)
                            self._save_index()
                            return TurnRecord(
                                turn_id=data["turn_id"],
                                session_key=data.get("session_key", ""),
                                ts=data.get("ts", ""),
                                user_question=data.get("user_question", ""),
                                final_result=data.get("final_result", ""),
                                messages=data.get("messages", []),
                            )
                    except json.JSONDecodeError:
                        continue
        return None

    def get_turns_with_context(
        self,
        turn_id: str,
        context_turns: int = 0,
    ) -> list[TurnRecord]:
        center = self.get_turn(turn_id)
        if not center:
            return []
        if context_turns <= 0:
            return [center]
        path_str = self._index.get(turn_id)
        if not path_str:
            return [center]
        path = Path(path_str)
        all_records: list[TurnRecord] = []
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    all_records.append(
                        TurnRecord(
                            turn_id=data["turn_id"],
                            session_key=data.get("session_key", ""),
                            ts=data.get("ts", ""),
                            user_question=data.get("user_question", ""),
                            final_result=data.get("final_result", ""),
                            messages=data.get("messages", []),
                        )
                    )
                except json.JSONDecodeError:
                    continue
        all_records.sort(key=lambda r: r.ts)
        idx = next((i for i, r in enumerate(all_records) if r.turn_id == turn_id), -1)
        if idx < 0:
            return [center]
        start = max(0, idx - context_turns)
        end = min(len(all_records), idx + context_turns + 1)
        return all_records[start:end]
