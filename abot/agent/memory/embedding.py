"""Embedding provider for vector search. Optional: requires sentence-transformers."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


class EmbeddingProvider(ABC):
    """Abstract embedding provider. embed() returns vectors for given texts."""

    @abstractmethod
    def embed(self, texts: list[str]) -> list[list[float]]:
        """Embed texts to vectors. Returns list of same length as input."""
        ...


class SentenceTransformerEmbedding(EmbeddingProvider):
    """Embedding via sentence-transformers. Lazy-loads model on first use."""

    def __init__(self, model_name: str):
        self._model_name = model_name
        self._model = None

    def _get_model(self):
        if self._model is None:
            from sentence_transformers import SentenceTransformer

            self._model = SentenceTransformer(self._model_name)
        return self._model

    def embed(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        texts = [t if t.strip() else " " for t in texts]
        model = self._get_model()
        vectors = model.encode(texts, convert_to_numpy=True)
        return [v.tolist() for v in vectors]


def create_embedding_provider(model_name: str) -> EmbeddingProvider | None:
    """
    Create embedding provider if model_name is non-empty and deps are available.
    Returns None to fall back to keyword-only search.
    """
    if not model_name or not model_name.strip():
        return None
    try:
        from sentence_transformers import SentenceTransformer  # noqa: F401
    except ImportError:
        return None
    return SentenceTransformerEmbedding(model_name.strip())
