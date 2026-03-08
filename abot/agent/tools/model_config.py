"""Tools for validating model config outputs (deploy.json / usage.yaml)."""

from __future__ import annotations

import json
from typing import Any

from abot.agent.tools.base import Tool
from abot.model_configs.deploy import validate_deploy_json, DeployConfig
from abot.model_configs.usage import UsageConfig, validate_usage_yaml


class ValidateDeployJSONTool(Tool):
    @property
    def name(self) -> str:
        return "validate_deploy_json"

    @property
    def description(self) -> str:
        return "Validate a deploy.json string against the built-in deploy schema. Returns OK or errors."

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "content": {
                    "type": "string",
                    "description": "Raw deploy.json content (must be a JSON object).",
                },
                "return_schema": {
                    "type": "boolean",
                    "description": "If true, returns the JSON Schema for deploy.json instead of validating.",
                    "default": False,
                },
            },
            "required": [],
        }

    async def execute(self, **kwargs: Any) -> str:
        if kwargs.get("return_schema"):
            schema = DeployConfig.model_json_schema()
            return json.dumps(schema, ensure_ascii=False, indent=2)

        content = kwargs.get("content")
        if not isinstance(content, str) or not content.strip():
            return "Error: missing required parameter: content"

        try:
            data = json.loads(content)
        except Exception as e:
            return f"Error: invalid JSON: {e}"

        ok, msg = validate_deploy_json(data)
        return "OK" if ok else f"Error: invalid deploy.json:\n{msg}"


class ValidateUsageYAMLTool(Tool):
    @property
    def name(self) -> str:
        return "validate_usage_yaml"

    @property
    def description(self) -> str:
        return "Validate a usage.yaml string against the built-in usage schema. Returns OK or errors."

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "content": {
                    "type": "string",
                    "description": "Raw usage.yaml content (must be a YAML mapping).",
                },
                "return_schema": {
                    "type": "boolean",
                    "description": "If true, returns the JSON Schema for usage.yaml instead of validating.",
                    "default": False,
                },
            },
            "required": [],
        }

    async def execute(self, **kwargs: Any) -> str:
        if kwargs.get("return_schema"):
            schema = UsageConfig.model_json_schema()
            return json.dumps(schema, ensure_ascii=False, indent=2)

        content = kwargs.get("content")
        if not isinstance(content, str) or not content.strip():
            return "Error: missing required parameter: content"

        try:
            import yaml  # type: ignore
        except Exception as e:
            return (
                "Error: PyYAML is required to validate usage.yaml. Install it in the current environment:\n\n"
                "pip install --upgrade pyyaml\n\n"
                f"Detail: {e}"
            )

        try:
            data = yaml.safe_load(content)
        except Exception as e:
            return f"Error: invalid YAML: {e}"

        ok, msg = validate_usage_yaml(data)
        return "OK" if ok else f"Error: invalid usage.yaml:\n{msg}"


