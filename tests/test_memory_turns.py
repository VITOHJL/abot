"""Tests for turn-based memory: split_into_turns, turn store, RAG."""

import pytest
from pathlib import Path

from abot.agent.loop import AgentLoop
from abot.agent.memory import JSONLTurnStore, RagStore
from abot.agent.memory.db_store import _extract_final_result, _extract_user_question
from abot.session.manager import Session


class TestSplitIntoTurns:
    """Test _split_into_turns logic."""

    def test_single_turn(self):
        messages = [
            {"role": "user", "content": "hi"},
            {"role": "assistant", "content": "hello"},
        ]
        turns = AgentLoop._split_into_turns(messages)
        assert len(turns) == 1
        assert len(turns[0][2]) == 2

    def test_two_turns(self):
        messages = [
            {"role": "user", "content": "q1"},
            {"role": "assistant", "content": "a1"},
            {"role": "user", "content": "q2"},
            {"role": "assistant", "content": "a2"},
        ]
        turns = AgentLoop._split_into_turns(messages)
        assert len(turns) == 2
        assert turns[0][2][0]["content"] == "q1"
        assert turns[1][2][0]["content"] == "q2"

    def test_turn_with_tool_calls(self):
        messages = [
            {"role": "user", "content": "run ls"},
            {"role": "assistant", "content": "", "tool_calls": [{"function": {"name": "exec"}}]},
            {"role": "tool", "content": "file1.txt"},
            {"role": "assistant", "content": "Here are the files."},
        ]
        turns = AgentLoop._split_into_turns(messages)
        assert len(turns) == 1
        assert len(turns[0][2]) == 4


class TestExtractUserQuestion:
    def test_simple(self):
        msgs = [{"role": "user", "content": "hello"}]
        assert _extract_user_question(msgs) == "hello"

    def test_no_user(self):
        msgs = [{"role": "assistant", "content": "hi"}]
        assert _extract_user_question(msgs) == ""


class TestExtractFinalResult:
    def test_last_assistant(self):
        msgs = [
            {"role": "user", "content": "q"},
            {"role": "assistant", "content": "final answer"},
        ]
        assert _extract_final_result(msgs) == "final answer"

    def test_skips_tool_only(self):
        msgs = [
            {"role": "user", "content": "q"},
            {"role": "assistant", "content": "", "tool_calls": [{}]},
            {"role": "tool", "content": "result"},
            {"role": "assistant", "content": "Here is the result."},
        ]
        assert _extract_final_result(msgs) == "Here is the result."


class TestJSONLTurnStore:
    def test_save_and_get(self, tmp_path):
        store = JSONLTurnStore(tmp_path)
        turns = [
            [
                {"role": "user", "content": "q1", "timestamp": "2025-01-01T10:00:00"},
                {"role": "assistant", "content": "a1"},
            ],
        ]
        ids = store.save_turns(turns, "cli:direct")
        assert len(ids) == 1
        rec = store.get_turn(ids[0])
        assert rec is not None
        assert rec.user_question == "q1"
        assert rec.final_result == "a1"


class TestRagStore:
    def test_search_empty(self, tmp_path):
        store = RagStore(tmp_path)
        assert store.search("test") == []

    def test_index_and_search(self, tmp_path):
        store = RagStore(tmp_path)
        turns = [
            [
                {"role": "user", "content": "write a python script", "timestamp": "2025-01-01T10:00:00"},
                {"role": "assistant", "content": "Created script.py"},
            ],
        ]
        store.index_turns(turns, "cli:direct", ["abc123"])
        results = store.search("python script")
        assert len(results) == 1
        assert results[0]["turn_id"] == "abc123"
        assert "python" in results[0]["user_question"].lower()
