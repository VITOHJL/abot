"""RAG store for semantic/keyword search over turns. Supports hybrid (keyword + vector) when embedding enabled."""

from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING, Any

from abot.utils.helpers import ensure_dir

if TYPE_CHECKING:
    from abot.agent.memory.embedding import EmbeddingProvider


class RagStore:
    """
    Searchable index over turns. Uses keyword search; when embedding_provider is set,
    adds vector search over user_question only (hybrid recall).
    """

    _HYBRID_ALPHA = 0.3  # keyword_weight; vector_weight = 1 - alpha

    def __init__(
        self,
        workspace: Path,
        embedding_provider: EmbeddingProvider | None = None,
    ):
        self.workspace = workspace
        self.embedding_provider = embedding_provider
        self.index_dir = ensure_dir(workspace / "memory" / "rag")
        self.index_file = self.index_dir / "index.jsonl"
        self._chroma_collection = None

    def _get_chroma_collection(self):
        if self._chroma_collection is None:
            import chromadb

            chroma_path = self.index_dir / "chroma"
            ensure_dir(chroma_path)
            client = chromadb.PersistentClient(path=str(chroma_path))
            self._chroma_collection = client.get_or_create_collection(
                name="turns",
                metadata={"hnsw:space": "cosine"},
            )
        return self._chroma_collection

    def index_turns(
        self,
        turns: list[list[dict]],
        session_key: str,
        turn_ids: list[str],
    ) -> None:
        """
        Index turns for search. Call after TurnStore.save_turns.
        - Keyword: writes to index.jsonl (user_q + final_result).
        - Vector: if embedding_provider set, embeds user_q only, writes to ChromaDB.
        """
        from abot.agent.memory.db_store import _extract_final_result, _extract_user_question

        user_questions: list[str] = []
        records: list[dict] = []

        for turn_msgs, turn_id in zip(turns, turn_ids):
            if not turn_msgs or not turn_id:
                continue
            user_q = _extract_user_question(turn_msgs)
            final_a = _extract_final_result(turn_msgs)
            ts = ""
            for m in turn_msgs:
                if m.get("timestamp"):
                    ts = str(m.get("timestamp", ""))[:19]
                    break
            record = {
                "turn_id": turn_id,
                "session_key": session_key,
                "ts": ts,
                "user_question": user_q,
                "final_result": final_a,
            }
            records.append(record)
            user_questions.append(user_q or " ")

        # Keyword index (always)
        with open(self.index_file, "a", encoding="utf-8") as f:
            for rec in records:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")

        # Vector index (embed user_q only)
        if self.embedding_provider and user_questions:
            embeddings = self.embedding_provider.embed(user_questions)
            coll = self._get_chroma_collection()
            # ChromaDB metadata: strings only, truncate long values if needed
            metadatas = []
            for rec in records:
                m = {
                    "turn_id": rec["turn_id"],
                    "session_key": rec["session_key"],
                    "ts": rec["ts"],
                    "user_question": (rec["user_question"] or "")[:2000],
                    "final_result": (rec["final_result"] or "")[:4000],
                }
                metadatas.append(m)
            coll.add(
                ids=[r["turn_id"] for r in records],
                embeddings=embeddings,
                metadatas=metadatas,
            )

    def _keyword_search(
        self,
        query: str,
        top_k: int,
        session_key: str | None,
    ) -> list[tuple[float, dict]]:
        """Returns list of (score, record). score is normalized [0,1], higher better."""
        if not self.index_file.exists():
            return []
        query_lower = query.lower().strip()
        if not query_lower:
            return []
        query_terms = [t for t in query_lower.split() if len(t) > 1]
        if not query_terms:
            query_terms = [query_lower]

        results: list[tuple[int, dict]] = []
        with open(self.index_file, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    if session_key and data.get("session_key") != session_key:
                        continue
                    text = (
                        (data.get("user_question", "") or "")
                        + " "
                        + (data.get("final_result", "") or "")
                    ).lower()
                    score = sum(1 for t in query_terms if t in text)
                    if score > 0:
                        rec = {
                            "turn_id": data.get("turn_id", ""),
                            "ts": data.get("ts", ""),
                            "user_question": data.get("user_question", ""),
                            "final_result": data.get("final_result", ""),
                        }
                        results.append((-score, rec))
                except json.JSONDecodeError:
                    continue
        results.sort(key=lambda x: x[0])
        # Normalize: max_score = len(query_terms), min 1 -> 0-1
        out: list[tuple[float, dict]] = []
        for neg_score, rec in results[: top_k * 2]:
            raw = -neg_score
            norm = min(1.0, raw / max(1, len(query_terms)))
            out.append((norm, rec))
        return out[:top_k]

    def _vector_search(
        self,
        query: str,
        top_k: int,
        session_key: str | None,
    ) -> list[tuple[float, dict]]:
        """Returns list of (similarity, record). similarity in [0,1], higher better."""
        if not self.embedding_provider:
            return []
        q_emb = self.embedding_provider.embed([query])
        if not q_emb:
            return []
        coll = self._get_chroma_collection()
        where = {"session_key": session_key} if session_key else None
        n = min(top_k * 2, coll.count() or 1)
        if n < 1:
            return []
        res = coll.query(
            query_embeddings=q_emb,
            n_results=n,
            where=where,
            include=["metadatas", "distances"],
        )
        ids = res["ids"][0] if res["ids"] else []
        distances = res["distances"][0] if res.get("distances") else []
        metadatas = res["metadatas"][0] if res.get("metadatas") else []
        out: list[tuple[float, dict]] = []
        for i, (tid, dist, meta) in enumerate(zip(ids, distances, metadatas)):
            if i >= top_k:
                break
            meta = meta or {}
            sim = 1.0 - dist if dist is not None else 0.0
            rec = {
                "turn_id": meta.get("turn_id", tid),
                "ts": meta.get("ts", ""),
                "user_question": meta.get("user_question", ""),
                "final_result": meta.get("final_result", ""),
            }
            out.append((sim, rec))
        return out

    def search(
        self,
        query: str,
        top_k: int = 5,
        session_key: str | None = None,
    ) -> list[dict[str, Any]]:
        """
        Search. If embedding_provider set: hybrid (keyword + vector) merge.
        Otherwise: keyword only.
        Returns list of {turn_id, ts, user_question, final_result} sorted by score.
        """
        if not query or not query.strip():
            return []

        if self.embedding_provider:
            kw_results = self._keyword_search(query, top_k * 2, session_key)
            vec_results = self._vector_search(query, top_k * 2, session_key)
            seen: set[str] = set()
            combined: list[tuple[float, dict]] = []
            alpha = self._HYBRID_ALPHA
            for score, rec in kw_results:
                tid = rec.get("turn_id", "")
                if tid not in seen:
                    seen.add(tid)
                    combined.append((alpha * score, rec))
            for score, rec in vec_results:
                tid = rec.get("turn_id", "")
                if tid not in seen:
                    seen.add(tid)
                    combined.append(((1 - alpha) * score, rec))
                else:
                    idx = next(i for i, (_, r) in enumerate(combined) if r.get("turn_id") == tid)
                    old_s, old_r = combined[idx]
                    combined[idx] = (old_s + (1 - alpha) * score, old_r)
            combined.sort(key=lambda x: -x[0])
            return [r for _, r in combined[:top_k]]
        else:
            return [r for _, r in self._keyword_search(query, top_k, session_key)]
