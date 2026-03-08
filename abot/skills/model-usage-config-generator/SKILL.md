---
name: model-usage-config-generator
description: 生成 usage.yaml（展示与调用配置），让已经部署好的模型在平台中被友好、稳定地使用。
---

# Skill: model-usage-config-generator

## 概要

这个 Skill 专门负责为“模型卡片”生成 **使用配置文件 `usage.yaml`**：

- 描述模型在平台中的展示信息（名称、简介、版本）
- 提供多语言的欢迎文案与推荐问题
- 定义全局执行方式（运行环境、工作目录）
- 定义可供前端/调用方使用的技能列表（命令模板 + 参数 schema）

你是 **“模型使用专家”**，需要根据：

- 模型的能力类型（chat / TTS / 图像生成 / embedding / 代码助手等）
- GitHub / HuggingFace 提供的使用示例
- 平台已有模型的 usage 配置惯例

生成 **结构清晰、对调用方友好的使用配置**。

---

## 调用时机

在以下场景下使用本 Skill：

- 已经有了一个可用的部署（本地可以正常跑推理），需要把它“包装成可用的 App/模型卡片”
- 需要为某个模型设计/更新界面文案、推荐提问、命令行调用入口和技能列表
- 对应的 `deploy.json` 已经存在，或由其他流程生成，这里 **只负责 usage 部分**

---

## 工具依赖

在生成 `usage.yaml` 前，你 **应尽量调用** 以下工具（如果可用）：

1. **GitHub 查询工具**
   - 用途：
     - 查看 README 中的“Usage / Examples”
     - 获取推荐的命令行参数组合或 API 调用方式

2. **HuggingFace 查询工具**
   - 用途：
     - 查看 model card 中的“intended use / examples”
     - 判断 pipeline 类型和典型输入输出格式

3. **经验库查询工具**
   - 用途：
     - 检索该模型类型在平台上已有的 usage 设计（比如 TTS/图像生成的常用参数）
     - 避免复用那些已知效果不好的交互方式

4. **经验库登记工具**
   - 用途：
     - 在管理员或用户测试后，把更好的提示文案或参数建议记录进去

---

## 输出协议

每次生成使用配置时，你 **必须** 严格按照下面的协议输出：

1. 可以先用一小段 markdown 说明你会做什么（可选，最多几句话）。
2. 然后按顺序输出两段：

```text
===USAGE_YAML===
<这里是严格的 YAML，没有多余文本，没有 JSON，没有注释>
===END===
```

- `USAGE_YAML` 段：
  - 必须是合法 YAML
  - 可被 `yaml.safe_load()` 直接解析

---

## 结构规范：usage.yaml

### 1. 顶层结构

`usage.yaml` 的目标：为前端 / 调用方提供“如何使用此模型”的完整描述，包括欢迎文案、推荐问题、技能接口等。它描述的是**“怎么用已经部署好的模型”**，而不是“怎么部署模型”。

顶层必须包含（并与对应的 `deploy.json` 保持强一致）：

- `id`：平台短 ID，例如 `"spark_tts"`、`"tinyllava"`。
  - **必须与 `deploy.json.id` 完全一致**，用于在平台内标识同一个模型卡片。
  - 它不是 Hugging Face 的仓库名，禁止写成 `"bczhou/tiny-llava-v1-hf"` 或 `"tinyllava_v1_hf"`。
- `name`：展示名，例如 `"Spark-TTS Complete Toolkit"`、`"TinyLLaVA"`。
  - 面向用户的人类可读名称，禁止直接写成 `"bczhou/tiny-llava-v1-hf"` 这种 HF 仓库名。
- `description`：一句话或一小段整体描述。
- `version`：语义化版本号。
- `interface`：界面与提示文案配置。
- `global_execution`：全局运行环境/入口配置。
- `skills`：技能列表。

### 2. interface 结构

```yaml
interface:
  default_language: "zh"
  languages:
    zh:
      greeting: |
        👋 你好！我是 **Spark-TTS 本地语音助手**。
        ...
      suggested_queries:
        - "用刘德华的声音唱：给我一杯忘情水"
        - "用特朗普的声音说：Make AI Great Again"
    en:
      greeting: |
        👋 Hello! I am your **Spark-TTS Local Assistant**.
        ...
      suggested_queries:
        - "Speak like Trump: Make AI Great Again."
        - "Use Jack Ma's voice to say: I love money."
```

- `default_language`: 默认语言代码，如 `"zh"` 或 `"en"`
- `languages[code].greeting`: 多行 greeting 文案，支持 markdown
- `languages[code].suggested_queries`: 推荐问题/指令列表

### 3. global_execution 结构（必须与 deploy.json 对齐）

```yaml
global_execution:
  type: "conda_cli"
  env_name: "spark_tts_aa"
  working_directory: "~/.modelhunt/spark_tts"
```

- `type`: 执行方式标识，例如 `"conda_cli"`、`"docker"` 等
- `env_name`: 如果使用 conda，则为环境名。**推荐与 `deploy.json` 中的 conda 环境名保持一致**，通常为 `{deploy.id}_aa`（例如 `spark_tts_aa`、`tinyllava_aa`）。
- `working_directory`: 默认工作目录，所有命令在此目录下执行。**必须与 `deploy.json` 中约定的工作目录一致**，通常为 `~/.modelhunt/{deploy.id}`。

> 换句话说：`usage.yaml` 不负责决定模型从哪里下载（这是 `deploy.json` 的职责），只负责在正确的工作目录和环境下调用已经部署好的代码与权重。

### 4. skills 列表结构

`skills` 是一个数组，每个元素描述一个“可调用技能/子工具”：

```yaml
skills:
  - name: "basic_tts"
    description: "Convert text to speech using standard preset voices (Male/Female)."
    command_template: >
      python -m cli.inference
      --text "{text}"
      --save_dir "{save_dir}"
      --model_dir "pretrained_models/Spark-TTS-0.5B"
      --gender "{gender}"
      --speed "{speed}"
      --pitch "{pitch}"
    arguments:
      type: "object"
      required: ["text"]
      properties:
        text:
          type: "string"
          description: "The text content."
        gender:
          type: "string"
          enum: ["male", "female"]
          default: "female"
        speed:
          type: "string"
          enum: ["very_low", "low", "moderate", "high", "very_high"]
          default: "moderate"
        pitch:
          type: "string"
          enum: ["very_low", "low", "moderate", "high", "very_high"]
          default: "moderate"
        save_dir:
          type: "string"
          default: "./results"

  - name: "preset_character_tts"
    description: "Generate speech using built-in celebrity or character voices."
    command_template: >
      python -m cli.inference
      --text "{text}"
      --save_dir "{save_dir}"
      --model_dir "pretrained_models/Spark-TTS-0.5B"
      --prompt_speech_path "{character_path}"
      --speed "{speed}"
      --pitch "{pitch}"
    arguments:
      type: "object"
      required: ["text", "character_path"]
      properties:
        text:
          type: "string"
          description: "The text content."
        character_path:
          type: "string"
          description: "Select the character voice model."
          enum:
            - "src/demos/trump/trump_en.wav"
            - "src/demos/zhongli/zhongli_en.wav"
            - "src/demos/哪吒/nezha_zh.wav"
            - "src/demos/李靖/lijing_zh.wav"
            - "src/demos/杨澜/yanglan_zh.wav"
            - "src/demos/马云/mayun_zh.wav"
            - "src/demos/鲁豫/luyu_zh.wav"
            - "src/demos/余承东/yuchengdong_zh.wav"
            - "src/demos/刘德华/dehua_zh.wav"
            - "src/demos/徐志胜/zhisheng_zh.wav"
        speed:
          type: "string"
          enum: ["very_low", "low", "moderate", "high", "very_high"]
          default: "moderate"
        pitch:
          type: "string"
          enum: ["very_low", "low", "moderate", "high", "very_high"]
          default: "moderate"
        save_dir:
          type: "string"
          default: "./results"

  - name: "voice_cloning"
    description: "Clone a CUSTOM voice from a user-uploaded audio file."
    command_template: >
      python -m cli.inference
      --text "{text}"
      --save_dir "{save_dir}"
      --model_dir "pretrained_models/Spark-TTS-0.5B"
      --prompt_speech_path "{prompt_speech_path}"
      --speed "{speed}"
      --pitch "{pitch}"
    arguments:
      type: "object"
      required: ["text", "prompt_speech_path"]
      properties:
        text:
          type: "string"
        prompt_speech_path:
          type: "string"
          description: "Absolute path to the user's uploaded reference audio file."
        save_dir:
          type: "string"
          default: "./results"
        speed:
          type: "string"
          default: "moderate"
        pitch:
          type: "string"
          default: "moderate"
          default: "moderate"

---

## 结构与安全约束（必须遵守）

为避免 `usage.yaml` 被平台错误解析或在编辑器中报错，你在生成时必须遵守以下硬约束：

### 1. command_template 约束

- **必须是一条可在 shell 中直接执行的命令**，推荐写成单行（可以用 `\` 或 `&&` 连接），**不要在其中内嵌多行 Python 脚本**。
  - 错误示例（禁止）：在 `command_template` 里写 `python -c " ... 多行 import/推理代码 ... "`。
  - 正确示例：把复杂逻辑放到仓库里的 `inference_*.py` / `cli.py` 中，这里只调用入口脚本，例如：
    - `python inference_qwen.py --prompt "{prompt}" --output_dir "{output_dir}" --nfe {nfe}`
- **只能使用 `{参数名}` 占位符**，且这些占位符必须全部出现在 `arguments.properties` 中：
  - 禁止出现未在 `arguments.properties` 中定义的 `{xxx}`。
  - 禁止在命令中使用除占位符外的裸 `{` / `}`（避免与模板引擎或 YAML 解析冲突）。
- 关于模型路径：
  - `command_template` 中涉及模型/权重路径时，应与对应 `deploy.json` 中的下载路径保持一致。
  - 推荐做法：在 `deploy.json` 的 `hf_model.localPath` 下预先下载权重，然后在这里使用**相对于 `global_execution.working_directory` 的相对路径**，例如：
    - `--model_dir "pretrained_models/Spark-TTS-0.5B"`
    - 或 `--model_path "{model_path}"`，同时在 `arguments.properties.model_path.default` 中给出合理默认值（例如：`"models/ymyy307--ArcFlow"`，前提是该目录确实存在于 `~/.modelhunt/{id}/` 下）。

### 2. arguments 约束

- `arguments.type` 必须是 `"object"`。
- `arguments.required` 中的字段名必须全部出现在 `arguments.properties` 中。
- 每个 `properties.*.type` 只能是以下几种之一：
  - `"string"`、`"integer"`、`"number"`、`"boolean"`。
- `default` 的类型必须与 `type` 一致：
  - 若 `type: "integer"`，`default` 必须是整数（不能写成字符串）。
  - 若有 `minimum` / `maximum`，`default` 必须在范围内。


---

## 使用建议

- 每次生成前，优先查看 GitHub / HuggingFace / 经验库，尽可能基于真实使用示例来设计技能与参数。
- 推荐问题要贴近真实使用场景，帮助用户快速上手，而不是展示性很强但不实用的例子。
- 如果某些参数对用户来说太复杂，可以隐藏到 `command_template` 中，使用合理的默认值。

