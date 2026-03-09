---
name: model-deploy-config-generator
description: 生成 deploy.json（部署步骤、运行环境与模型下载），用于将模型在目标平台可重复、可自动化地部署。
---

# Skill: model-deploy-config-generator

## 目标

这个 Skill 专门负责为“模型卡片”生成 **部署配置文件 `deploy.json`**，用于描述：

- 代码拉取与目录初始化
- 系统依赖安装
- Python/Conda 环境准备
- 模型权重下载与落盘路径

你是“模型部署专家”，重点保证输出配置 **可执行、可复现、可维护**。

## 何时使用

在以下场景调用本 Skill：

- 已确认某个模型要接入平台，需要标准化部署流程
- 需要把 README / Model Card 中分散的安装步骤固化为结构化 JSON
- 暂不处理前端展示文案（这属于 `model-usage-config-generator`）

## 优先工具

生成前应尽量使用以下工具收集事实：

1. GitHub 查询工具
- 读取 README / INSTALL / examples，提取真实依赖与启动命令

2. HuggingFace 查询工具
- 确认权重仓库名、任务类型、license、推荐推理方式

3. 经验库查询工具
- 复用同类模型的稳定部署经验，规避已知坑

4. 经验库登记工具
- 部署验证后把新经验回写到经验库

## 输出协议

必须严格按以下结构输出：

```text
===DEPLOY_JSON===
<严格 JSON 对象，不包含注释或额外解释>
===END===
```

生成后建议立刻调用：

- `validate_deploy_json(content="<DEPLOY_JSON 原文>")`

若校验失败，修复后重新输出。

## 输入信息清单

生成前尽量明确以下输入（缺失时在 `tip` 中提示用户补充）：

- 模型标识
- `id`：平台短 ID（例如 `tinyllava`）
- `name`：展示名（例如 `TinyLLaVA`）
- `version`：语义化版本
- 代码来源（可选）
- `repo_url`：源码仓库地址
- `repo_dir_name`：仓库目录名（若与 `id` 不同，仍建议统一落到 `{id}`）
- 权重来源（可选）
- `hf_model_ids`：一个或多个 HF 仓库名（用于 `hf_model` steps）
- 目标平台
- `platforms`：`mac` / `linux` / `windows`（至少一个）

## deploy.json 结构规范

### 1. 顶层结构

顶层必须包含：

- `id`
- `name`
- `version`
- `platforms`

说明：

- `id` / `name` 不应直接复用 Hugging Face 仓库名（例如 `owner/repo`）
- `id` 应稳定、简短，用于路径与平台内标识

### 2. 目录约定（强约束）

统一目录规则：

- 根目录：`$HOME/.modelhunt`
- 工作目录：`$HOME/.modelhunt/{deploy.id}`
- 所有涉及 `cd` 的命令统一进入该目录

如果需要 clone 仓库，建议直接 clone 到 `{deploy.id}` 目录，避免后续路径漂移。

### 3. platforms / steps

`platforms[platform].steps` 是按顺序执行的步骤数组。

每个 step 必须包含：

- `action`
- `tip.zh`
- `tip.en`

常见 `action`：

1. `bash`
- 字段：`commands`（string 数组）
- 规范：`commands` 只保留 1 条命令，复杂逻辑用 `&&` / 子 shell 组合
- 规范：命令末尾附加 `&& echo "Successful" || echo "Failed"`

2. `conda`
- 字段：`conda`、`pythonVersion`
- 规范：环境名必须以 `_aa` 结尾（例如 `{id}_aa`）

3. `brew`
- 字段：`install`

4. `hf_model`
- 字段：`model`、`localPath`
- 规范：`model` 必须来自工具查询结果（如 `huggingface_model_search`）
- 规范：`localPath` 必须位于 `~/.modelhunt/{deploy.id}/...`

## 强一致性自检（必须通过）

输出前在内部完成以下检查：

- 顶层 `id/name/version/platforms` 齐全
- 至少一个平台，且每个平台都有非空 `steps`
- 每个平台至少包含一个 `conda` step
- 每个 step 都有 `action` 与 `tip.zh/tip.en`
- 所有路径指向 `$HOME/.modelhunt/{deploy.id}` 体系
- 所有 `bash.commands[0]` 都以成功/失败回显结尾
- `hf_model.localPath` 位于约定目录下

修复规则：

- 若 schema 报 `conda` 相关错误，只能修复该 step 字段，不允许删除整个 `conda` step

## 依赖稳定性建议（默认执行）

部署失败最常见原因是依赖漂移，而非“缺少某个包”。生成 `bash` 安装命令时建议：

1. 使用 `python -m pip`，不要直接用 `pip`
2. 在安装 requirements 前先固定构建工具
- `pip<25`
- `setuptools<58`
- `wheel<0.40`
3. 若项目未严格锁版本，优先补 `constraints.txt`
4. 安装后执行
- `python -m pip check`
- `python -m pip freeze > .abot_deps_freeze.txt`

推荐单条命令模板（无 constraints）：

```bash
(cd $HOME/.modelhunt/{deploy.id} && python -m pip install --upgrade "pip<25" && python -m pip install --upgrade "setuptools<58" "wheel<0.40" && python -m pip install -r requirements.txt && python -m pip check && python -m pip freeze > .abot_deps_freeze.txt) && echo "Successful" || echo "Failed"
```

## 输出质量要求

- 不编造不存在的参数、路径或仓库名
- 信息不足时给出保守可落地方案，并在 `tip` 明确补充点
- 优先保证可执行性，其次再追求“看起来完整”
