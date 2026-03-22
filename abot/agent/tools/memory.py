"""Memory tools: search_memory and get_turn_detail."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from abot.agent.tools.base import Tool

if TYPE_CHECKING:
    from abot.agent.memory.rag_store import RagStore
    from abot.agent.memory.turn_store import TurnStore


class SearchMemoryTool(Tool):
    """Search past conversations by semantic/keyword. Returns top_k summaries."""

    def __init__(self, turn_store: TurnStore, rag_store: RagStore):
        self._turn_store = turn_store
        self._rag_store = rag_store

    @property
    def name(self) -> str:
        return "search_memory"

    @property
    def description(self) -> str:
        return (
            "Search past conversations for relevant context. "
            "Use when you need to recall what the user asked before or what was implemented. "
            "Returns summaries (time, user question, result). Use get_turn_detail to fetch full implementation."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query (keywords or natural language)",
                },
                "top_k": {
                    "type": "integer",
                    "description": "Maximum number of results to return",
                    "default": 5,
                },
                "session_key": {
                    "type": "string",
                    "description": "Optional: filter by session (e.g. cli:direct). Omit to search all.",
                },
            },
            "required": ["query"],
        }

    async def execute(
        self,
        query: str,
        top_k: int = 5,
        session_key: str | None = None,
        **kwargs: Any,
    ) -> str:
        if not query or not query.strip():
            return "Error: query cannot be empty."
        top_k = max(1, min(20, int(top_k)))
        results = self._rag_store.search(
            query=query.strip(),
            top_k=top_k,
            session_key=session_key,
        )
        if not results:
            return "No matching past conversations found."
        lines = []
        for i, r in enumerate(results, 1):
            turn_id = r.get("turn_id", "")
            ts = r.get("ts", "")[:16] if r.get("ts") else ""
            uq = (r.get("user_question") or "")[:200]
            fr = (r.get("final_result") or "")[:300]
            if len((r.get("final_result") or "")) > 300:
                fr += "..."
            lines.append(
                f"[{i}] turn_id: {turn_id} | {ts}\n"
                f"    用户问：{uq}\n"
                f"    结果：{fr}"
            )
        return "\n\n".join(lines)


class GetTurnDetailTool(Tool):
    """Fetch full conversation for a turn (and optional surrounding context)."""

    def __init__(self, turn_store: TurnStore):
        self._turn_store = turn_store

    @property
    def name(self) -> str:
        return "get_turn_detail"

    @property
    def description(self) -> str:
        return (
            "Fetch the full conversation for a turn. Use after search_memory when you need "
            "implementation details, tool calls, or surrounding context."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "turn_id": {
                    "type": "string",
                    "description": "Turn ID from search_memory results",
                },
                "context_turns": {
                    "type": "integer",
                    "description": "Number of turns before and after to include (0 = only this turn)",
                    "default": 0,
                },
            },
            "required": ["turn_id"],
        }

    async def execute(
        self,
        turn_id: str,
        context_turns: int = 0,
        **kwargs: Any,
    ) -> str:
        if not turn_id or not turn_id.strip():
            return "Error: turn_id cannot be empty."
        context_turns = max(0, min(5, int(context_turns)))
        records = self._turn_store.get_turns_with_context(
            turn_id.strip(),
            context_turns=context_turns,
        )
        if not records:
            return f"Error: Turn '{turn_id}' not found."
        lines = []
        for rec in records:
            lines.append(f"--- Turn {rec.turn_id} | {rec.ts} ---")
            for m in rec.messages:
                role = m.get("role", "?")
                content = m.get("content", "")
                if isinstance(content, list):
                    content = " ".join(
                        p.get("text", "") for p in content if isinstance(p, dict) and p.get("type") == "text"
                    )
                if m.get("tool_calls"):
                    names = [tc.get("function", {}).get("name", "?") for tc in (m["tool_calls"] or [])]
                    lines.append(f"[{role}] (tools: {', '.join(names)})")
                else:
                    preview = (content or "")[:500]
                    if len(content or "") > 500:
                        preview += "..."
                    lines.append(f"[{role}] {preview}")
            lines.append("")
        return "\n".join(lines).strip()
