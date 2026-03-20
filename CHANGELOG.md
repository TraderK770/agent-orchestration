# Orchestration 变更日志

## v2.0.1 — 2026-03-20（外部审计修复）

修复13个审计问题（严重1+中等8+轻微4）：

| 优先级 | ID | 修复 | 涉及文件 |
|:------:|:--:|------|----------|
| P0 | A-1/C-1 | 方案C明确为"A+B混合"，不是独立第三模式 | orchestrator_prompt.md |
| P1 | T-1/T-2 | "专精者"→"执行者"，"领域"→"任务执行" | executor_prompt.md |
| P1 | R-1 | shared_notes.md使用规则写入executor_prompt | executor_prompt.md |
| P1 | R-3 | rules.md重构为轻量引导（不再重复executor_prompt） | launcher.py |
| P1 | R-5 | rules.md铁律补全mission.md/plan.md | launcher.py |
| P2 | S-1 | DESIGN_RATIONALE标题去模式A偏见 | DESIGN_RATIONALE.md |
| P2 | S-2 | 六维审查表增加并行策略评分指引 | orchestrator_prompt.md |
| P2 | R-2 | plan.md/review.md不自动生成的原因加注释 | launcher.py |
| P2 | R-4 | 同R-2 | launcher.py |
| P3 | U-1 | 示例命令增加PowerShell注意事项 | SKILL.md |
| P3 | U-2 | START_HERE.txt增加相对路径 | launcher.py |

---

## v2.0.0 — 2026-03-20（架构简化：三模式→二模式）

### 破坏性变更

将三种模式（专精分工/竞争探索/视角发散）简化为两种：

| 新模式 | 原模式 | 说明 |
|--------|--------|------|
| **A 线性策略** | 原模式A | 不同Agent不同方向，合并 |
| **B 并行策略** | 原模式B+C合并 | 同一任务独立探索，不预设路径，合并/竞争由人类决定 |

### 设计原则强化

- 编排者只定义"做什么"，不预设"怎么做"
- 并行策略中Agent互不知情，没有上帝视角
- 择优/综合/混合是人类在审查时的决定，不是编排者预设

### 变更文件

| 文件 | 操作 |
|------|------|
| `orchestrator_prompt.md` | 重写 |
| `DESIGN_RATIONALE.md` | 重写 |
| `SKILL.md` | 更新模式表 |
| `executor_prompt.md` | 简化身份描述 |
| `launcher.py` | task.md模板移除"专精领域"字段 |

---

## v1.3.1 — 2026-03-20（全面一致性审查）

6个文件交叉审查，修复11处不一致。

---

## v1.3.0 — 2026-03-20（设计哲学修正）

**编排者不应预设框架/方法，预设=在起点限制可能性。**

---

## v1.2.1 — 2026-03-20（审查修复）

修复7处描述不一致。

---

## v1.2.0 — 2026-03-20

新增**模式C：视角发散**——同一任务+同一样本，注入不同分析框架/视角，综合洞察而非择优。

---

## v1.1.0 — 2026-03-20

基于本地技能库和 Anthropic 官方 multi-agent 架构对比分析，执行P0/P1优化。

新增六维审查表、背景摘要模板、shared_notes、START_HERE.txt、DESIGN_RATIONALE.md。

---

## v1.0.0 — 初始版本

原始 Fork-Review-Merge 编排系统。
