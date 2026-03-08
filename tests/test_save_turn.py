"""Test session save turn logic."""
import pytest
from datetime import datetime
from abot.agent.context import ContextBuilder
from abot.session.manager import Session


class MockMessageTool:
    def __init__(self):
        self._sent_in_turn = False


class TestSaveTurn:
    """Tests for _save_turn method."""

    def test_save_turn_truncates_long_tool_result(self):
        """Tool results exceeding max chars should be truncated."""
        from abot.agent.loop import AgentLoop
        
        loop = AgentLoop.__new__(AgentLoop)
        loop._TOOL_RESULT_MAX_CHARS = 500
        session = Session(key="test:truncate")
        
        long_content = "x" * 600
        messages = [
            {"role": "tool", "content": long_content, "tool_call_id": "1"},
        ]
        
        loop._save_turn(session, messages, skip=0)
        
        assert session.messages[0]["content"].endswith("... (truncated)")
        assert session.messages[0]["content"].endswith("... (truncated)")

    def test_save_turn_skips_empty_assistant(self):
        """Empty assistant messages without tool_calls should be skipped."""
        from abot.agent.loop import AgentLoop
        
        loop = AgentLoop.__new__(AgentLoop)
        loop._TOOL_RESULT_MAX_CHARS = 500
        session = Session(key="test:empty")
        
        messages = [
            {"role": "assistant", "content": ""},
        ]
        
        loop._save_turn(session, messages, skip=0)
        
        assert len(session.messages) == 0

    def test_save_turn_strips_runtime_context(self):
        """Runtime context prefix should be stripped from user messages."""
        from abot.agent.loop import AgentLoop
        
        loop = AgentLoop.__new__(AgentLoop)
        loop._TOOL_RESULT_MAX_CHARS = 500
        session = Session(key="test:runtime")
        
        runtime = ContextBuilder._RUNTIME_CONTEXT_TAG + "\nCurrent Time: now (UTC)\n\nHello world"
        messages = [
            {"role": "user", "content": runtime},
        ]
        
        loop._save_turn(session, messages, skip=0)
        
        assert session.messages[0]["content"] == "Hello world"

    def test_save_turn_keeps_image_placeholder(self):
        """Base64 images should be replaced with [image] placeholder."""
        from abot.agent.loop import AgentLoop
        
        loop = AgentLoop.__new__(AgentLoop)
        loop._TOOL_RESULT_MAX_CHARS = 500
        session = Session(key="test:image")
        
        messages = [
            {"role": "user", "content": [
                {"type": "text", "text": "What do you see?"},
                {"type": "image_url", "image_url": {"url": "data:image/png;base64,abc123"}},
            ]},
        ]
        
        loop._save_turn(session, messages, skip=0)
        
        assert session.messages[0]["content"][1] == {"type": "text", "text": "[image]"}

