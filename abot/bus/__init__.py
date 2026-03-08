"""Message bus module for decoupled channel-agent communication."""

from abot.bus.events import InboundMessage, OutboundMessage
from abot.bus.queue import MessageBus

__all__ = ["MessageBus", "InboundMessage", "OutboundMessage"]

