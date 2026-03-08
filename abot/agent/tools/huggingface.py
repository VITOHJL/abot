"""Tools for querying Hugging Face models."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from abot.agent.tools.base import Tool


@dataclass
class _HFModelView:
    """Lightweight projection of a Hugging Face model card."""

    id: str
    task: str | None = None
    likes: int | None = None
    downloads: int | None = None
    library: str | None = None
    tags: list[str] | None = None
    last_modified: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "task": self.task,
            "likes": self.likes,
            "downloads": self.downloads,
            "library": self.library,
            "tags": self.tags or [],
            "last_modified": self.last_modified,
        }


class HuggingFaceModelSearchTool(Tool):
    """Search models on Hugging Face with a stable API (no HTML scraping)."""

    name = "huggingface_model_search"
    description = (
        "Search models on Hugging Face and return a concise JSON list of candidates "
        "(id, task, downloads, likes, library, tags, last_modified). "
        "Always use this to confirm the exact model id before filling hf_model.model."
    )
    parameters: dict[str, Any] = {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Keyword to search for, e.g. 'tinyllava', 'whisper', 'llava 1.5'.",
                "minLength": 1,
            },
            "task": {
                "type": "string",
                "description": "Optional pipeline tag / task, e.g. 'text-generation', 'image-text-to-text'.",
            },
            "limit": {
                "type": "integer",
                "description": "Maximum number of models to return (1-30).",
                "minimum": 1,
                "maximum": 30,
            },
        },
        "required": ["query"],
    }

    def __init__(self, cache_dir: Path | None = None, default_limit: int = 10):
        self.cache_dir = cache_dir or (Path.home() / ".abot" / "hf_cache")
        self.default_limit = default_limit
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    async def execute(self, query: str, task: str | None = None, limit: int | None = None, **_: Any) -> str:
        """Execute the search. Returns a JSON string."""
        try:
            try:
                from huggingface_hub import HfApi
            except Exception as e:  # pragma: no cover - import error path
                return json.dumps(
                    {
                        "status": "error",
                        "error": (
                            "Python package 'huggingface_hub' is not installed or failed to import. "
                            "Please install it in the current environment, for example:\n\n"
                            "pip install --upgrade huggingface_hub"
                        ),
                        "detail": str(e),
                    },
                    ensure_ascii=False,
                )

            n = limit or self.default_limit
            n = max(1, min(int(n), 30))

            api = HfApi()

            # We use synchronous API under the hood; network latency dominates anyway.
            models: Iterable[Any] = api.list_models(
                search=query,
                pipeline_tag=task or None,
                sort="downloads",
                direction=-1,
                limit=n,
            )

            results: list[_HFModelView] = []
            for m in models:
                mid = getattr(m, "id", None) or getattr(m, "modelId", None)
                if not mid:
                    continue
                results.append(
                    _HFModelView(
                        id=mid,
                        task=(getattr(m, "pipeline_tag", None) or None),
                        likes=getattr(m, "likes", None),
                        downloads=getattr(m, "downloads", None),
                        library=(getattr(m, "library_name", None) or None),
                        tags=list(getattr(m, "tags", []) or []),
                        last_modified=(getattr(m, "lastModified", None) or None),
                    )
                )

            payload = {
                "status": "ok",
                "query": query,
                "task": task,
                "limit": n,
                "count": len(results),
                "results": [r.to_dict() for r in results],
            }
            return json.dumps(payload, ensure_ascii=False)
        except Exception as e:
            return json.dumps(
                {
                    "status": "error",
                    "error": "Failed to query Hugging Face models.",
                    "detail": str(e),
                },
                ensure_ascii=False,
            )


