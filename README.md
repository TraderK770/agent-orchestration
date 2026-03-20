# 🎯 Agent Orchestration

**Multi-Agent orchestration framework for AI coding assistants.**

Let multiple AI conversations work as a team — Fork tasks, Review results, Merge outputs.

让多个 AI 对话像团队一样分工协作 — 拆分任务、审查结果、合并产出。

---

## ✨ What is this? / 这是什么？

A prompt-based orchestration framework that splits complex tasks across multiple independent AI agents, each working in isolated sandboxes. No API keys, no server — just prompts and a Python launcher.

一套基于提示词的编排框架，将复杂任务拆分给多个独立 AI Agent，每个 Agent 在隔离沙箱中工作。无需 API Key，无需服务器 — 只需提示词和一个 Python 启动器。

### Architecture / 架构

```
                    ┌─────────────┐
                    │ Orchestrator│  (Main Agent)
                    │  拆分/审查   │
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
        ┌──────────┐ ┌──────────┐ ┌──────────┐
        │Executor 1│ │Executor 2│ │Executor 3│
        │ 独立沙箱  │ │ 独立沙箱  │ │ 独立沙箱  │
        └──────────┘ └──────────┘ └──────────┘
              │            │            │
              └────────────┼────────────┘
                           ▼
                    ┌─────────────┐
                    │   Review    │  (Human decides)
                    │  人类决策    │
                    └─────────────┘
```

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
- Any AI coding assistant (e.g., Google Antigravity, Cursor, Windsurf)

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

1. **Orchestrator defines WHAT, not HOW** — Pre-setting methods limits possibilities
2. **Sandbox isolation** — Each executor is a feature branch, free to work independently
3. **Human-in-the-loop** — Merge only after human review and confirmation
4. **Depth over breadth** — Each agent is an expert, not an assembly line worker

---

## 🤝 Compatibility / 兼容性

This framework is **AI-assistant agnostic**. It works with any tool that supports multi-turn conversations:

- ✅ Google Antigravity
- ✅ Cursor
- ✅ Windsurf
- ✅ GitHub Copilot
- ✅ Any LLM chat interface

---

## 📄 License

MIT License — see [LICENSE](LICENSE)

---

## 🌟 Star this repo if you find it useful!

如果觉得有用，请给个 ⭐️！
