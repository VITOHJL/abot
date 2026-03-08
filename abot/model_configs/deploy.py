"""Pydantic schema for deploy.json (model deployment config)."""

from __future__ import annotations

import re
from typing import Annotated, Literal, Union

from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator, model_validator

_BASH_SUCCESS_SUFFIX = '&& echo "Successful" || echo "Failed"'


class _StrictBase(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Tip(_StrictBase):
    zh: str = Field(min_length=1)
    en: str = Field(min_length=1)


class StepBase(_StrictBase):
    action: str
    tip: Tip


class BashStep(StepBase):
    action: Literal["bash"]
    commands: list[str] = Field(min_length=1)

    @field_validator("commands")
    @classmethod
    def _validate_commands(cls, v: list[str]) -> list[str]:
        if len(v) != 1:
            raise ValueError("bash.commands must contain exactly 1 command string")
        cmd = v[0].strip()
        if not cmd:
            raise ValueError("bash.commands[0] must be non-empty")
        if not cmd.endswith(_BASH_SUCCESS_SUFFIX):
            raise ValueError(f'bash.commands[0] must end with `{_BASH_SUCCESS_SUFFIX}`')
        return v


class CondaStep(StepBase):
    action: Literal["conda"]
    conda: str = Field(min_length=1)
    pythonVersion: str = Field(min_length=1)

    @field_validator("conda")
    @classmethod
    def _validate_env_name(cls, v: str) -> str:
        if not v.endswith("_aa"):
            # 提醒模型：请保留该步骤，只修改环境名达到要求，而不是删除整个 conda 步骤。
            raise ValueError(
                "conda environment name must end with `_aa` "
                "(DO NOT remove this step; only rename the environment, e.g. '{id}_aa')."
            )
        return v


class BrewStep(StepBase):
    action: Literal["brew"]
    install: str = Field(min_length=1)


class HFModelStep(StepBase):
    action: Literal["hf_model"]
    model: str = Field(min_length=1)
    localPath: str = Field(min_length=1)


DeployStep = Annotated[
    Union[BashStep, CondaStep, BrewStep, HFModelStep],
    Field(discriminator="action"),
]


class PlatformSpec(_StrictBase):
    steps: list[DeployStep] = Field(min_length=1)


class DeployConfig(_StrictBase):
    id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    version: str = Field(min_length=1)
    platforms: dict[str, PlatformSpec] = Field(min_length=1)

    @field_validator("id")
    @classmethod
    def _validate_id(cls, v: str) -> str:
        if not re.fullmatch(r"[a-z0-9_]+", v):
            raise ValueError("id must match ^[a-z0-9_]+$")
        return v

    @model_validator(mode="after")
    def _validate_hf_paths_and_conda(self) -> "DeployConfig":
        prefix = f"~/.modelhunt/{self.id}/"
        for platform, spec in self.platforms.items():
            # 每个平台必须至少有一个 conda 步骤，防止模型“删掉 conda 来通过校验”
            has_conda = any(isinstance(step, CondaStep) for step in spec.steps)
            if not has_conda:
                raise ValueError(
                    f"platforms.{platform}.steps must contain at least one 'conda' step "
                    "(you must keep the conda step; fix its fields instead of deleting it)."
                )
            for idx, step in enumerate(spec.steps):
                if isinstance(step, HFModelStep):
                    if not step.localPath.startswith(prefix):
                        raise ValueError(
                            f"platforms.{platform}.steps[{idx}].localPath must start with {prefix!r}"
                        )
        return self


def validate_deploy_json(data: object) -> tuple[bool, str]:
    """Validate arbitrary decoded JSON data as DeployConfig. Returns (ok, message)."""
    try:
        DeployConfig.model_validate(data)
        return True, "OK"
    except ValidationError as e:
        return False, e.__str__()
    except Exception as e:
        return False, str(e)

