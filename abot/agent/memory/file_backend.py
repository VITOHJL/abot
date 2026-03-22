"""File-based memory backend: MEMORY.md only (no HISTORY.md)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING

from loguru import logger

from abot.agent.memory.backend import MemoryBackend
from abot.utils.helpers import ensure_dir

if TYPE_CHECKING:
    from abot.providers.base import LLMProvider


_SAVE_MEMORY_TOOL = [
    {
        "type": "function",
        "function": {
            "name": "save_memory",
            "description": "Save the memory consolidation result to persistent storage.",
            "parameters": {
                "type": "object",
                "properties": {
                    "memory_update": {
                        "type": "string",
                        "description": "Full updated long-term memory as markdown. Include all existing "
                        "facts plus new ones. Return unchanged if nothing new.",
                    },
                },
                "required": ["memory_update"],
            },
        },
    }
]


def _format_messages_for_prompt(messages: list[dict]) -> str:
    """Format messages for the consolidation prompt."""
    lines = []
    for m in messages:
        if not m.get("content"):
            continue
        tools = ""
        if m.get("tools_used"):
            tools = f" [tools: {', '.join(m['tools_used'])}]"
        elif m.get("tool_calls"):
            names = [
                tc.get("function", {}).get("name", "?")
                for tc in (m["tool_calls"] or [])
            ]
            if names:
                tools = f" [tools: {', '.join(names)}]"
        lines.append(
            f"[{m.get('timestamp', '?')[:16]}] {m['role'].upper()}{tools}: {m['content']}"
        )
    return "\n".join(lines)


class FileMemoryBackend(MemoryBackend):
    """Memory backend that persists only to MEMORY.md."""

    def __init__(self, workspace: Path):
        self.memory_dir = ensure_dir(workspace / "memory")
        self.memory_file = self.memory_dir / "MEMORY.md"

    def read_long_term(self) -> str:
        if self.memory_file.exists():
            return self.memory_file.read_text(encoding="utf-8")
        return ""

    def write_long_term(self, content: str) -> None:
        self.memory_file.write_text(content, encoding="utf-8")

    async def consolidate_and_save(
        self,
        turns: list[list[dict]],
        provider: LLMProvider,
        model: str,
    ) -> bool:
        """Consolidate turns into MEMORY.md via LLM. No HISTORY.md."""
        if not turns:
            return True

        flat_messages: list[dict] = []
        for turn in turns:
            flat_messages.extend(turn)

        if not flat_messages:
            return True

        lines_str = _format_messages_for_prompt(flat_messages)
        current_memory = self.read_long_term()
        prompt = f"""Process this conversation and call the save_memory tool with your consolidation.

## Current Long-term Memory
{current_memory or "(empty)"}

## Conversation to Process
{lines_str}"""

        try:
            response = await provider.chat(
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a memory consolidation agent.\n"
                            "Your job is to update long-term MEMORY.md with stable facts and user preferences as markdown.\n"
                            "Include all existing facts plus new ones from the conversation.\n"
                            "Return unchanged if nothing new to add.\n\n"
                            "Always call the save_memory tool with memory_update."
                        ),
                    },
                    {"role": "user", "content": prompt},
                ],
                tools=_SAVE_MEMORY_TOOL,
                model=model,
            )

            if not response.has_tool_calls:
                logger.warning("Memory consolidation: LLM did not call save_memory, skipping")
                return False

            args = response.tool_calls[0].arguments
            if isinstance(args, str):
                args = json.loads(args)
            if isinstance(args, list):
                if args and isinstance(args[0], dict):
                    args = args[0]
                else:
                    logger.warning("Memory consolidation: unexpected arguments")
                    return False
            if not isinstance(args, dict):
                logger.warning("Memory consolidation: unexpected arguments type {}", type(args).__name__)
                return False

            update = args.get("memory_update")
            if update is not None:
                if not isinstance(update, str):
                    update = json.dumps(update, ensure_ascii=False)
                if update != current_memory:
                    self.write_long_term(update)

            logger.info("Memory consolidation done for {} turns ({} messages)", len(turns), len(flat_messages))
            return True
        except Exception:
            logger.exception("Memory consolidation failed")
            return False
