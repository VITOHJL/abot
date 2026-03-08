"""QQ channel implementation using OneBot protocol.

OneBot is a unified chatbot protocol that provides more flexibility than the
official QQ bot API.

Recommended adapters:
- Lagrange.onebot
- NapCat
- go-cqhttp (legacy)
"""

import asyncio
import json
from collections import deque
from typing import Any
from urllib.parse import urlparse

import aiohttp
from aiohttp import web
from loguru import logger

from abot.bus.events import OutboundMessage
from abot.bus.queue import MessageBus
from abot.channels.base import BaseChannel
from abot.config.schema import QQConfig


class QQOneBotChannel(BaseChannel):
    """QQ channel using OneBot protocol."""

    name = "qq"

    def __init__(self, config: QQConfig, bus: MessageBus):
        super().__init__(config, bus)
        self.config: QQConfig = config
        self._session: aiohttp.ClientSession | None = None
        self._ws_clients: set[aiohttp.web.WebSocketResponse] = set()
        self._ws_server: web.Application | None = None
        self._ws_runner: web.AppRunner | None = None
        self._ws_site: web.TCPSite | None = None
        self._processed_ids: deque = deque(maxlen=1000)
        self._bot_qq: int | None = config.bot_qq

    async def start(self) -> None:
        """Start the OneBot channel."""
        if not self.config.api_url:
            logger.error("QQ OneBot API URL not configured")
            return

        self._running = True

        headers = {}
        if self.config.access_token:
            headers["Authorization"] = f"Bearer {self.config.access_token}"

        self._session = aiohttp.ClientSession(
            headers=headers,
            timeout=aiohttp.ClientTimeout(total=30),
        )

        # Start reverse WebSocket server (adapter connects to us).
        if self.config.ws_reverse_url:
            parsed = urlparse(self.config.ws_reverse_url)
            ws_host = parsed.hostname or "127.0.0.1"
            ws_port = parsed.port or 8080
            ws_path = parsed.path or "/ws/reverse"

            logger.info(
                "Starting OneBot WebSocket reverse server on ws://{}:{}{}",
                ws_host,
                ws_port,
                ws_path,
            )
            await self._start_websocket_server(ws_host, ws_port, ws_path)
        elif self.config.http_reverse_url:
            logger.info("Using OneBot HTTP reverse: {}", self.config.http_reverse_url)
            await self._start_long_polling()
        else:
            logger.info("Using OneBot HTTP API only: {}", self.config.api_url)
            logger.warning(
                "No reverse connection configured. Bot can send messages but won't receive them. "
                "Configure ws_reverse_url to start WebSocket server for adapter events."
            )

    async def _start_websocket_server(self, host: str, port: int, path: str) -> None:
        """Start WebSocket server for OneBot reverse connections."""
        app = web.Application()

        async def websocket_handler(request: web.Request) -> web.WebSocketResponse:
            ws = web.WebSocketResponse()
            await ws.prepare(request)

            self._ws_clients.add(ws)
            logger.info("OneBot WebSocket client connected from {}", request.remote)

            try:
                async for msg in ws:
                    if msg.type == aiohttp.WSMsgType.TEXT:
                        try:
                            data = json.loads(msg.data)
                            await self._handle_onebot_event(data)
                        except Exception as e:
                            logger.error("Error processing OneBot event: {}", e)
                    elif msg.type == aiohttp.WSMsgType.ERROR:
                        logger.error("WebSocket error: {}", ws.exception())
                        break
                    elif msg.type == aiohttp.WSMsgType.CLOSE:
                        logger.info("WebSocket closed")
                        break
            finally:
                self._ws_clients.discard(ws)
                logger.info("OneBot WebSocket client disconnected")

            return ws

        app.router.add_get(path, websocket_handler)

        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, host, port)
        await site.start()

        self._ws_server = app
        self._ws_runner = runner
        self._ws_site = site

        logger.info("OneBot WebSocket reverse server started on ws://{}:{}{}", host, port, path)

    async def _start_long_polling(self) -> None:
        """Start HTTP long polling for events (placeholder)."""
        logger.warning("HTTP long polling is not fully implemented. Use WebSocket reverse instead.")

    async def _handle_onebot_event(self, event: dict[str, Any]) -> None:
        """Handle incoming OneBot event."""
        post_type = event.get("post_type")

        if post_type == "message":
            await self._handle_message_event(event)
        elif post_type == "notice":
            await self._handle_notice_event(event)
        elif post_type == "request":
            await self._handle_request_event(event)

    async def _handle_message_event(self, event: dict[str, Any]) -> None:
        """Handle OneBot message event."""
        message_type = event.get("message_type")
        user_id = event.get("user_id")
        message_id = event.get("message_id")
        raw_message = event.get("raw_message", "")

        # Skip self messages.
        if self._bot_qq and user_id == self._bot_qq:
            return

        # Deduplicate.
        if message_id and message_id in self._processed_ids:
            return
        if message_id:
            self._processed_ids.append(message_id)

        # Extract text content (OneBot messages may be complex segments).
        content = self._extract_text_from_message(event.get("message", []))
        if not content:
            return

        if message_type == "private":
            await self._handle_message(
                sender_id=str(user_id),
                chat_id=str(user_id),
                content=content,
                metadata={
                    "message_id": message_id,
                    "message_type": "private",
                    "raw_message": raw_message,
                },
            )
        elif message_type == "group":
            group_id = event.get("group_id")
            is_at = self._is_bot_mentioned(event.get("message", []), self._bot_qq)

            if is_at or not self._bot_qq:
                await self._handle_message(
                    sender_id=str(user_id),
                    chat_id=f"group_{group_id}",
                    content=content,
                    metadata={
                        "message_id": message_id,
                        "message_type": "group",
                        "group_id": group_id,
                        "raw_message": raw_message,
                        "is_at": is_at,
                    },
                )

    def _extract_text_from_message(self, message: list[dict[str, Any]] | str) -> str:
        """Extract text content from OneBot message array."""
        if isinstance(message, str):
            return message

        if not isinstance(message, list):
            return ""

        texts = []
        for segment in message:
            if isinstance(segment, dict):
                msg_type = segment.get("type")
                if msg_type == "text":
                    texts.append(segment.get("data", {}).get("text", ""))
                elif msg_type == "at":
                    qq = segment.get("data", {}).get("qq", "")
                    texts.append(f"@user{qq} ")
            elif isinstance(segment, str):
                texts.append(segment)

        return "".join(texts).strip()

    def _is_bot_mentioned(self, message: list[dict[str, Any]], bot_qq: int | None) -> bool:
        """Check if bot is mentioned in a message."""
        if not bot_qq or not isinstance(message, list):
            return False

        for segment in message:
            if isinstance(segment, dict) and segment.get("type") == "at":
                qq = segment.get("data", {}).get("qq")
                if str(qq) == str(bot_qq):
                    return True

        return False

    async def _handle_notice_event(self, event: dict[str, Any]) -> None:
        """Handle OneBot notice event."""
        notice_type = event.get("notice_type")
        logger.debug("OneBot notice event: {}", notice_type)

    async def _handle_request_event(self, event: dict[str, Any]) -> None:
        """Handle OneBot request event."""
        request_type = event.get("request_type")
        logger.debug("OneBot request event: {}", request_type)

    async def stop(self) -> None:
        """Stop the OneBot channel."""
        self._running = False

        for ws in list(self._ws_clients):
            await ws.close()
        self._ws_clients.clear()

        if self._ws_site:
            await self._ws_site.stop()
            self._ws_site = None

        if self._ws_runner:
            await self._ws_runner.cleanup()
            self._ws_runner = None

        if self._session:
            await self._session.close()
            self._session = None

        logger.info("QQ OneBot channel stopped")

    async def send(self, msg: OutboundMessage) -> None:
        """Send a message through OneBot API."""
        if not self._session:
            logger.warning("QQ OneBot session not initialized")
            return

        try:
            if msg.chat_id.startswith("group_"):
                group_id = int(msg.chat_id.replace("group_", "", 1))
                await self._send_group_message(group_id, msg.content)
            else:
                user_id = int(msg.chat_id)
                await self._send_private_message(user_id, msg.content)
        except Exception as e:
            logger.error("Error sending QQ OneBot message: {}", e)

    async def _send_private_message(self, user_id: int, content: str) -> None:
        """Send private message via OneBot API."""
        api_endpoint = f"{self.config.api_url}/send_private_msg"

        payload = {
            "user_id": user_id,
            "message": content,
        }

        async with self._session.post(api_endpoint, json=payload) as resp:
            if resp.status != 200:
                text = await resp.text()
                logger.error("OneBot API error: {} - {}", resp.status, text)
                return

            result = await resp.json()
            if result.get("status") != "ok":
                logger.error("OneBot API returned error: {}", result.get("wording"))

    async def _send_group_message(self, group_id: int, content: str) -> None:
        """Send group message via OneBot API."""
        api_endpoint = f"{self.config.api_url}/send_group_msg"

        payload = {
            "group_id": group_id,
            "message": content,
        }

        async with self._session.post(api_endpoint, json=payload) as resp:
            if resp.status != 200:
                text = await resp.text()
                logger.error("OneBot API error: {} - {}", resp.status, text)
                return

            result = await resp.json()
            if result.get("status") != "ok":
                logger.error("OneBot API returned error: {}", result.get("wording"))
