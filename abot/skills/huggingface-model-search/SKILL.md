---
name: huggingface-model-search
description: 使用 huggingface_model_search 稳定查询 Hugging Face 模型列表，确认正确的模型仓库名（避免 web_fetch 抓网页超时）。
---

## 目标

当你需要确认 Hugging Face 上**正确的模型仓库名**（例如要填写到 `deploy.json` 的 `hf_model.model`）时，必须先调用工具 `huggingface_model_search` 获取候选列表，而不是凭经验猜测或用 `web_fetch` 抓取 Hugging Face 网页。

## 重要说明（避免混淆）

- `huggingface_model_search` 返回的 `results[].id` 是 **Hugging Face 仓库名**（例如 `"bczhou/tiny-llava-v1-hf"`）。
- 它 **只**用于填充 `deploy.json` 中 `hf_model` step 的 `model` 字段。
- 它 **不用于** `deploy.json` 顶层 `id` / `name`（平台卡片标识与展示名应按平台命名体系，例如 `tinyllava` / `TinyLLaVA`，不要直接复用 HF 仓库名或加 `_hf` 后缀）。

## 可用工具

### `huggingface_model_search`

- **用途**：在 Hugging Face 上搜索模型并返回候选列表（结构化 JSON）。
- **入参**：
  - **`query`**（必选）：搜索关键词，例如 `"tinyllava"`、`"whisper"`、`"llava 1.5"`。
  - **`task`**（可选）：pipeline tag / 任务类型，例如 `"text-generation"`、`"image-text-to-text"`。
  - **`limit`**（可选）：返回数量（1–30），建议 5–20。
- **出参**：JSON 字符串，包含：
  - `status`: `"ok"` 或 `"error"`
  - `results`: 候选模型数组，每项包含 `id`（最关键）、`task`、`downloads`、`likes`、`library`、`tags`、`last_modified`

## 使用流程（强制）

1. **先查询**
   - 调用 `huggingface_model_search(query=..., task=..., limit=...)`
2. **再选择**
   - 从返回的 `results[].id` 中选择最合适的模型
   - 常用选择规则（按优先级）：
     - **任务匹配**：`task` 与需求一致（如多模态常见 `"image-text-to-text"`）
     - **热度/稳定性**：`downloads` 更高通常更稳（但也要看任务与 tags）
     - **生态兼容**：`library == "transformers"` / tags 包含 transformers 更常见
3. **再落盘**
   - 将选中的 `id` 原样写入配置：
     - `deploy.json` → `hf_model.model`
     - `usage.yaml`（如需要）→ 模型名引用

## 错误处理（必须遵守）

- 如果返回 `status == "error"`：
  - **不要**改用 `web_fetch` 去抓 Hugging Face 网页（容易超时/不稳定）
  - 请在回复中明确告知：当前环境缺依赖或网络访问 Hugging Face 失败，并给出下一步：
    - 若提示缺少 `huggingface_hub`：建议用户在当前运行环境安装/升级 `huggingface_hub`
    - 若网络失败：建议用户检查网络/代理后重试该工具调用

## 禁止事项（硬规则）

- **禁止**：用 `web_fetch` 抓取 `huggingface.co/models?search=...` 等 HTML 页面来解析模型名。
- **禁止**：在未调用 `huggingface_model_search` 的情况下编造/猜测模型仓库名。
- **禁止**：把 `results[].id` 当作 `deploy.json` 顶层 `id` / `name`。

