---
name: 多Agent编排模式
description: Fork-Review-Merge 多对话协作框架，将复杂任务拆分给多个独立Agent并行执行
---

# 多Agent编排模式（Orchestration Mode）

一套多对话协作模板，让多个AI对话像团队一样分工。

## 文件说明

| 文件 | 用途 |
|------|------|
| `orchestrator_prompt.md` | 主Agent（编排者）的角色定义和工作流程 |
| `DESIGN_RATIONALE.md` | 设计理念说明（两种模式、拆分原则、不预设路径的原则） |
| `executor_prompt.md` | 执行Agent的角色定义和工作规范（含Few-shot示例） |
| `launcher.py` | Python 自动化脚本（创建工作区、检查状态） |

## 两种模式

| 模式 | 适用场景 | 说明 |
|------|----------|------|
| **A 线性策略** | 能拆成不同专业方向 | 不同Agent做不同方向，合并产出 |
| **B 并行策略** | 路径不确定，需多样化产出 | 同一任务多个Agent独立探索，人类决定择优/综合 |

## 使用方式

### 方式1：通过 Workflow 触发
在对话中使用 `/orchestration` 触发完整编排流程。

### 方式2：手动使用

**第1步：主Agent进入编排者模式**
```
请阅读以下文件，进入"编排者模式"：
orchestrator_prompt.md

我的目标是：[描述你的目标]
```

**第2步：用 launcher.py 搭建工作区**
```bash
python launcher.py setup "工作目录路径" "一句话使命" 3
```

> **PowerShell注意**：如路径含空格，请用单引号包裹或将 `\` 替换为 `/`。

**第3步：启动执行Agent（新对话）**
每个 executor 目录下有 `START_HERE.txt`，新开对话后复制其内容粘贴即可启动。

**第4步：检查状态**
```bash
python launcher.py check "工作目录路径"
```

## 职责分工：Python vs AI

| 操作 | 谁做 |
|------|------|
| 创建文件夹/复制资源/生成模板 | **Python** |
| 理解目标/拆分任务/审查结果 | **AI** |

> 原则：**能用代码确定性完成的，绝不交给大模型**。
