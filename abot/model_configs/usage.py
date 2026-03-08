"""Pydantic schema for usage.yaml (model usage config)."""

from __future__ import annotations

import re
from typing import Annotated, Any, Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator, model_validator


class _StrictBase(BaseModel):
    model_config = ConfigDict(extra="forbid")


class LanguageConfig(_StrictBase):
    greeting: str = Field(min_length=1)
    suggested_queries: list[str] = Field(min_length=1)


class InterfaceConfig(_StrictBase):
    default_language: str = Field(min_length=1)
    languages: dict[str, LanguageConfig] = Field(min_length=1)

    @model_validator(mode="after")
    def _validate_default_language(self) -> "InterfaceConfig":
        if self.default_language not in self.languages:
            raise ValueError("interface.default_language must exist in interface.languages")
        return self


class GlobalExecution(_StrictBase):
    type: str = Field(min_length=1)
    env_name: str = Field(min_length=1)
    working_directory: str = Field(min_length=1)


class ArgumentProperty(_StrictBase):
    type: Literal["string", "integer", "number", "boolean"]
    description: str | None = None
    default: Any | None = None
    enum: list[Any] | None = None
    minimum: float | None = None
    maximum: float | None = None

    @model_validator(mode="after")
    def _validate_default_type(self) -> "ArgumentProperty":
        if self.default is None:
            return self

        t = self.type
        if t == "string" and not isinstance(self.default, str):
            raise ValueError("default must be a string")
        if t == "boolean" and not isinstance(self.default, bool):
            raise ValueError("default must be a boolean")
        if t == "integer" and not (isinstance(self.default, int) and not isinstance(self.default, bool)):
            raise ValueError("default must be an integer")
        if t == "number" and not (isinstance(self.default, (int, float)) and not isinstance(self.default, bool)):
            raise ValueError("default must be a number")

        if t in ("integer", "number"):
            v = float(self.default)
            if self.minimum is not None and v < float(self.minimum):
                raise ValueError("default must be >= minimum")
            if self.maximum is not None and v > float(self.maximum):
                raise ValueError("default must be <= maximum")
        return self


class ArgumentsSchema(_StrictBase):
    type: Literal["object"] = "object"
    required: list[str] = Field(default_factory=list)
    properties: dict[str, ArgumentProperty] = Field(min_length=1)

    @model_validator(mode="after")
    def _validate_required_keys(self) -> "ArgumentsSchema":
        missing = [k for k in self.required if k not in self.properties]
        if missing:
            raise ValueError(f"arguments.required contains keys not in properties: {missing}")
        return self


class SkillConfig(_StrictBase):
    name: str = Field(min_length=1)
    description: str = Field(min_length=1)
    command_template: str = Field(min_length=1)
    arguments: ArgumentsSchema

    @field_validator("command_template")
    @classmethod
    def _validate_command_template(cls, v: str) -> str:
        # Platform parsers often fail on multiline templates; keep it single-line.
        if "\n" in v or "\r" in v:
            raise ValueError("command_template must be a single-line string (no newlines)")
        return v

    @model_validator(mode="after")
    def _validate_placeholders(self) -> "SkillConfig":
        # Only allow placeholders like {prompt}. Disallow any other braces to prevent
        # conflicts with templaters / f-strings (e.g. {i}).
        tmpl = self.command_template
        placeholder_re = re.compile(r"\{([A-Za-z_][A-Za-z0-9_]*)\}")
        names = placeholder_re.findall(tmpl)

        # Remove all valid placeholders, then ensure no raw braces remain.
        stripped = placeholder_re.sub("", tmpl)
        if "{" in stripped or "}" in stripped:
            raise ValueError("command_template contains '{' or '}' not part of a valid placeholder like {name}")

        props = set(self.arguments.properties.keys())
        unknown = sorted({n for n in names if n not in props})
        if unknown:
            raise ValueError(f"command_template uses placeholders not defined in arguments.properties: {unknown}")

        # Ensure required args appear in template (otherwise calling interface is confusing).
        missing_required = sorted([k for k in self.arguments.required if k not in names])
        if missing_required:
            raise ValueError(f"arguments.required keys must appear in command_template placeholders: {missing_required}")

        return self


UsageSkill = Annotated[SkillConfig, Field()]


class UsageConfig(_StrictBase):
    id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    description: str = Field(min_length=1)
    version: str = Field(min_length=1)
    interface: InterfaceConfig
    global_execution: GlobalExecution
    skills: list[UsageSkill] = Field(min_length=1)

    @field_validator("id")
    @classmethod
    def _validate_id(cls, v: str) -> str:
        if not re.fullmatch(r"[a-z0-9_]+", v):
            raise ValueError("id must match ^[a-z0-9_]+$")
        return v

    @model_validator(mode="after")
    def _validate_exec_alignment(self) -> "UsageConfig":
        # Align with deploy.json conventions
        expected_env = f"{self.id}_aa"
        if self.global_execution.env_name != expected_env:
            raise ValueError(f"global_execution.env_name must be {expected_env!r}")

        expected_wd = f"~/.modelhunt/{self.id}"
        if self.global_execution.working_directory != expected_wd:
            raise ValueError(f"global_execution.working_directory must be {expected_wd!r}")

        # Prevent HF repo-style ids being used as display name
        if "/" in self.name:
            raise ValueError("name must be a human-friendly display name, not an owner/repo string")
        return self


def validate_usage_yaml(data: object) -> tuple[bool, str]:
    """Validate arbitrary decoded YAML data as UsageConfig. Returns (ok, message)."""
    try:
        UsageConfig.model_validate(data)
        return True, "OK"
    except ValidationError as e:
        return False, e.__str__()
    except Exception as e:
        return False, str(e)

