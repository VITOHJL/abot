from typing import Any

import pytest

from abot.bus.events import OutboundMessage
from abot.bus.queue import MessageBus
from abot.channels.qq_onebot import QQOneBotChannel
from abot.config.schema import QQConfig


class _FakeResp:
    def __init__(self, status: int = 200, payload: dict[str, Any] | None = None) -> None:
        self.status = status
        self._payload = payload or {"status": "ok"}

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return None

    async def text(self) -> str:
        return "ok"

    async def json(self) -> dict[str, Any]:
        return self._payload


class _FakeSession:
    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    def post(self, url: str, json: dict[str, Any]):
        self.calls.append({"url": url, "json": json})
        return _FakeResp()


@pytest.mark.asyncio
async def test_on_group_message_routes_to_group_chat_id() -> None:
    channel = QQOneBotChannel(
        QQConfig(api_url="http://localhost:5700", allow_from=["111"], bot_qq=123),
        MessageBus(),
    )

    event = {
        "post_type": "message",
        "message_type": "group",
        "user_id": 111,
        "group_id": 222,
        "message_id": "m1",
        "raw_message": "hello",
        "message": [
            {"type": "at", "data": {"qq": "123"}},
            {"type": "text", "data": {"text": "hello"}},
        ],
    }

    await channel._handle_message_event(event)

    msg = await channel.bus.consume_inbound()
    assert msg.sender_id == "111"
    assert msg.chat_id == "group_222"


@pytest.mark.asyncio
async def test_send_group_message_uses_group_endpoint() -> None:
    channel = QQOneBotChannel(QQConfig(api_url="http://localhost:5700", allow_from=["*"]), MessageBus())
    channel._session = _FakeSession()

    await channel.send(
        OutboundMessage(
            channel="qq",
            chat_id="group_123",
            content="hello",
        )
    )

    assert len(channel._session.calls) == 1
    call = channel._session.calls[0]
    assert call["url"] == "http://localhost:5700/send_group_msg"
    assert call["json"]["group_id"] == 123
    assert call["json"]["message"] == "hello"
