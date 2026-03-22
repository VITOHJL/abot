"""Memory system for persistent agent memory."""

from __future__ import annotations

from abot.agent.memory.backend import MemoryBackend
from abot.agent.memory.db_store import JSONLTurnStore
from abot.agent.memory.embedding import EmbeddingProvider, SentenceTransformerEmbedding, create_embedding_provider
from abot.agent.memory.file_backend import FileMemoryBackend
from abot.agent.memory.rag_store import RagStore
from abot.agent.memory.store import MemoryStore
from abot.agent.memory.turn_store import TurnRecord, TurnStore

__all__ = [
    "EmbeddingProvider",
    "MemoryBackend",
    "FileMemoryBackend",
    "JSONLTurnStore",
    "MemoryStore",
    "RagStore",
    "SentenceTransformerEmbedding",
    "TurnRecord",
    "TurnStore",
    "create_embedding_provider",
]
