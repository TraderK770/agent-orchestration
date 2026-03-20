# 🎯 Agent Orchestration

**Multi-Agent orchestration framework built for [Google Antigravity](https://antigravity.google).**

让多个 AI 对话像团队一样分工协作 — 拆分任务、审查结果、合并产出。

---

> [!IMPORTANT]
> **本项目专为 Google Antigravity 环境设计。**
> 
> Antigravity 与 Claude Code / Cursor 等工具有本质区别：
> 
> | | Antigravity | Claude Code / Cursor |
> |---|---|---|
> | **定位** | Agent-first IDE，AI 自主执行 | Copilot 辅助，人类主导 |
> | **对话模型** | 每个对话是独立 Agent，互相隔离 | 单一对话，上下文共享 |
> | **多任务** | 需要人类手动开多个对话 | 无原生多 Agent 能力 |
> | **上下文** | 每个对话有独立上下文窗口，不互通 | 单窗口，无隔离 |
> 
> **这带来一个核心问题：** 当任务复杂到需要多个专业方向协作时，单个 Agent 的上下文窗口放不下所有工作。强行塞入会导致目标漂移、质量下降、重要信息被遗忘。
> 
> **本框架的解决方案：** 把多个独立对话组织成一个协作团队。每个对话（Executor）在自己的沙箱里深度工作，由一个主对话（Orchestrator）统一拆分任务、分发指令、审查合并。就像 Git 的 branch 模型 — Fork 出去干活，Review 后再 Merge。

---

## ✨ Core Features / 核心特性

- **🧠 Orchestrator + Executor 架构** — 主 Agent 拆分任务，Executor Agent 深度执行
- **📦 沙箱隔离** — 每个 Executor 有独立工作目录，互不干扰
- **🔍 六维审查体系** — 使命吻合度、深度指数、可操作性、指令遵循、创新性、格式规范
- **🤝 Human-in-the-loop** — 合并前必须人类确认，防止不可逆错误
- **🐍 Python 自动化** — 机械操作交给脚本，AI 只做需要推理的事

---

## 🚀 Two Strategies / 两种策略

| Strategy | When to use | How it works |
|----------|------------|---------------|
| **Linear** | Task can be split into distinct domains | Different agents handle different directions, merge results |
| **Parallel** | Path is uncertain, need diverse outputs | Same task given to all agents, each explores independently |

| 策略 | 适用场景 | 工作方式 |
|------|----------|----------|
| **线性策略** | 任务可按专业方向拆分 | 不同 Agent 负责不同方向，合并产出 |
| **并行策略** | 路径不确定，需多样化产出 | 同一任务独立探索，人类择优/综合 |

---

## 📦 Quick Start / 快速开始

### Prerequisites
- Python 3.6+
- Google Antigravity (or any AI coding assistant with multi-conversation support)

### Step 1: Load the Orchestrator

In your main AI conversation:
```
Please read orchestrator_prompt.md and enter "Orchestrator Mode".
My goal is: [describe your goal]
```

### Step 2: Set up workspace
```bash
python launcher.py setup "./my_project" "Your mission statement" 3
```

### Step 3: Launch Executors
Open a **new conversation** for each executor, paste the contents of `START_HERE.txt`.

### Step 4: Review
```bash
python launcher.py check "./my_project"
```

---

## 📁 Project Structure / 文件结构

| File | Purpose |
|------|---------|
| `orchestrator_prompt.md` | Orchestrator role definition & workflow |
| `executor_prompt.md` | Executor role definition with few-shot examples |
| `DESIGN_RATIONALE.md` | Design philosophy & decision rationale |
| `launcher.py` | Python automation (workspace setup, status check) |
| `SKILL.md` | Quick reference card |
| `CHANGELOG.md` | Version history |

---

## 🎯 Key Design Principles / 核心设计原则

1. **Orchestrator defines WHAT, not HOW** — 只说做什么，不预设怎么做
2. **Sandbox isolation** — 每个 Executor 就是一个 feature branch
3. **Human-in-the-loop** — 合并前必须人类审查确认
4. **Depth over breadth** — 每个 Agent 是专家，不是流水线工人

---

## 🤝 Compatibility / 兼容性

本框架 **不依赖任何特定 API**，纯提示词 + Python 脚本，适用于任何支持多轮对话的 AI 工具：

- ✅ Google Antigravity（原生最佳）
- ✅ Cursor
- ✅ Windsurf
- ✅ Any LLM chat interface

---

## 📄 License

MIT License — see [LICENSE](LICENSE)

---

## 🌟 Star this repo if you find it useful!

如果觉得有用，请给个 ⭐️！
