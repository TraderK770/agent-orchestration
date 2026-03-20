"""
多Agent编排模式 — 自动化启动器
功能：处理所有机械性操作，让AI只专注于需要推理的部分
"""
import os
import shutil
import json
import sys
from datetime import datetime


# 本脚本所在目录（用于定位 executor_prompt.md 等模板文件）
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def create_workspace(base_dir, executor_count):
    """阶段2自动化：创建工作区文件夹结构"""
    os.makedirs(base_dir, exist_ok=True)

    for i in range(1, executor_count + 1):
        executor_dir = os.path.join(base_dir, f"executor_{i:02d}")
        workspace_dir = os.path.join(executor_dir, "workspace")
        os.makedirs(workspace_dir, exist_ok=True)
        print(f"[✓] 创建 executor_{i:02d}/workspace/")

    print(f"[✓] 工作区创建完成：{base_dir}")
    return base_dir


def write_mission(base_dir, mission_text, success_criteria=None, constraints=None):
    """写入 mission.md — 使命声明"""
    content = f"""# 使命声明

## 目标
{mission_text}

## 成功标准
{success_criteria or '（待主Agent补充）'}

## 约束
{constraints or '（待主Agent补充）'}

## 创建时间
{datetime.now().strftime('%Y-%m-%d %H:%M')}
"""
    path = os.path.join(base_dir, "mission.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[✓] mission.md 已写入")
    return path


def copy_resources(base_dir, executor_id, source_paths):
    """将资源文件复制到指定 executor 的 workspace"""
    target_dir = os.path.join(base_dir, f"executor_{executor_id:02d}", "workspace")
    copied = []

    for src in source_paths:
        if not os.path.exists(src):
            print(f"[!] 跳过不存在的文件：{src}")
            continue

        if os.path.isdir(src):
            dirname = os.path.basename(src)
            dst = os.path.join(target_dir, dirname)
            shutil.copytree(src, dst, dirs_exist_ok=True)
            print(f"[✓] 复制目录 {dirname} → executor_{executor_id:02d}/workspace/")
        else:
            dst = os.path.join(target_dir, os.path.basename(src))
            shutil.copy2(src, dst)
            print(f"[✓] 复制文件 {os.path.basename(src)} → executor_{executor_id:02d}/workspace/")
        copied.append(dst)

    return copied


def write_task_template(base_dir, executor_id, mission_text):
    """生成 task.md 骨架（AI只需填写内容部分）"""
    content = f"""# 执行任务

## 使命锚点（不可修改）
{mission_text}

## 背景知识摘要（由Orchestrator预生成）
**项目背景**：（由主Agent填写——2-3句话描述项目）
**已完成的工作**：（由主Agent填写——前序executor的要点摘要，如有）
**关键约束**：（由主Agent填写——不可违反的限制）
**资源说明**：（由主Agent填写——workspace/中文件的简要说明）

## 你的任务
（由主Agent填写——只说做什么，不说怎么做，路径和方法由你自主设计）

## 为什么要深度做
（由主Agent填写）

## 你的工作区
所有工作在 `workspace/` 目录下进行：
- 你需要的资源已经复制到这里
- 你的所有产出物放在这里
- 你不能修改这个目录以外的任何文件

## 预期产出
（由主Agent填写）

## 完成后
将结果写入 `result.md`（与 task.md 同目录）
"""
    path = os.path.join(base_dir, f"executor_{executor_id:02d}", "task.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[✓] executor_{executor_id:02d}/task.md 骨架已生成")
    return path


def write_result_template(base_dir, executor_id):
    """生成 result.md 骨架（执行Agent填写）"""
    content = f"""# 结果：executor_{executor_id:02d}

status: pending
summary: （待填写）

## 方案选择
（待填写）

## 执行过程
（待填写）

## 产出清单
（待填写）

## 质量验证
（待填写）

## 遇到的问题
（待填写）

## 建议
（待填写）
"""
    path = os.path.join(base_dir, f"executor_{executor_id:02d}", "result.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path


def inject_prompt_to_executors(base_dir, executor_count):
    """将 executor_prompt.md 复制到每个 executor 目录，实现自包含"""
    prompt_src = os.path.join(SCRIPT_DIR, "executor_prompt.md")
    if not os.path.exists(prompt_src):
        print(f"[!] 警告：找不到 executor_prompt.md，跳过注入")
        return

    for i in range(1, executor_count + 1):
        dst = os.path.join(base_dir, f"executor_{i:02d}", "executor_prompt.md")
        shutil.copy2(prompt_src, dst)
        print(f"[✓] executor_prompt.md → executor_{i:02d}/")


def generate_start_prompt(base_dir, executor_id):
    """为每个executor生成 START_HERE.txt 一键启动提示词，减少人类操作步骤"""
    executor_dir = os.path.join(base_dir, f"executor_{executor_id:02d}")
    content = f"""请按以下步骤启动执行：
1. 先读取本目录下的 executor_prompt.md（了解你的身份和规则）
2. 再读取本目录下的 task.md（了解你的任务和背景）
3. 扫描 workspace/ 目录下有哪些资源文件
4. 向用户复述理解（使命、任务、资源），确认后开始执行

工作区绝对路径：{executor_dir}
"""
    path = os.path.join(executor_dir, "START_HERE.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[✓] executor_{executor_id:02d}/START_HERE.txt 已生成")
    return path


def create_shared_notes(base_dir):
    """创建 shared_notes.md：executor间单向通信文件（仅追加）"""
    content = """# 共享笔记（Shared Notes）

> 规则：executor 只能**追加**内容，不能修改已有内容。
> 每条笔记附带时间戳和executor编号。
> Orchestrator 可在第二轮任务中将此文件分发给新executor。

---
"""
    path = os.path.join(base_dir, "shared_notes.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[✓] shared_notes.md 已创建")
    return path


def write_executor_rules(base_dir, executor_id):
    """为每个executor生成rules.md（轻量指引，不重复 executor_prompt.md 内容）"""
    executor_dir = os.path.join(base_dir, f"executor_{executor_id:02d}")
    content = f"""# 工作区规则

详细角色定义和工作模式请读 `executor_prompt.md`。
本文件只包含工作边界的快速参考。

## 工作边界（铁律）
- ✅ 可以自由操作 `workspace/` 下的文件
- ✅ 可以写入 `result.md`
- ❌ 不可修改本目录（{os.path.basename(executor_dir)}/）以外的任何文件
- ❌ 不可修改 `task.md`、`executor_prompt.md`、`rules.md`
- ❌ 不可修改 `mission.md`、`plan.md`（即使在沙箱外）
"""
    path = os.path.join(executor_dir, "rules.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[✓] executor_{executor_id:02d}/rules.md 已生成")


def check_results(base_dir):
    """检查所有 executor 的执行状态（供主Agent审查阶段使用）"""
    results = {}
    for item in sorted(os.listdir(base_dir)):
        result_path = os.path.join(base_dir, item, "result.md")
        if os.path.isdir(os.path.join(base_dir, item)) and item.startswith("executor_"):
            if os.path.exists(result_path):
                with open(result_path, "r", encoding="utf-8") as f:
                    content = f.read()
                status = "unknown"
                for line in content.split("\n"):
                    if line.strip().startswith("status:"):
                        status = line.split(":", 1)[1].strip()
                        break
                results[item] = {"status": status, "path": result_path}
            else:
                results[item] = {"status": "no_result_file", "path": result_path}

    return results


def list_workspace_files(base_dir, executor_id):
    """列出指定 executor workspace 下的所有文件"""
    workspace = os.path.join(base_dir, f"executor_{executor_id:02d}", "workspace")
    if not os.path.exists(workspace):
        return []
    files = []
    for root, dirs, filenames in os.walk(workspace):
        for f in filenames:
            full = os.path.join(root, f)
            rel = os.path.relpath(full, workspace)
            size = os.path.getsize(full)
            files.append({"path": rel, "size_bytes": size})
    return files


def generate_startup_summary(base_dir):
    """生成启动摘要，供主Agent读取（替代大量文件注入）"""
    summary = {"工作目录": base_dir, "创建时间": datetime.now().isoformat(), "executors": {}}

    mission_path = os.path.join(base_dir, "mission.md")
    if os.path.exists(mission_path):
        with open(mission_path, "r", encoding="utf-8") as f:
            summary["mission"] = f.read()

    for item in sorted(os.listdir(base_dir)):
        item_path = os.path.join(base_dir, item)
        if os.path.isdir(item_path) and item.startswith("executor_"):
            executor_id = int(item.split("_")[1])
            files = list_workspace_files(base_dir, executor_id)
            summary["executors"][item] = {
                "workspace_files": [f["path"] for f in files],
                "file_count": len(files),
                "has_task": os.path.exists(os.path.join(item_path, "task.md")),
                "has_result": os.path.exists(os.path.join(item_path, "result.md")),
            }

    summary_path = os.path.join(base_dir, "startup_summary.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print(f"[✓] 启动摘要已生成：startup_summary.json")
    return summary_path


# ==================== 主流程 ====================

def full_setup(base_dir, mission_text, executor_count, resource_map=None):
    """
    一键搭建完整工作区

    参数:
        base_dir: 工作目录路径
        mission_text: 使命声明文本
        executor_count: executor 数量
        resource_map: {executor_id: [文件路径列表]} 可选，资源分配

    示例:
        full_setup(
            base_dir="./my_project",
            mission_text="从60分钟教学视频中制作3个高质量短视频",
            executor_count=3,
            resource_map={
                1: ["./videos/lesson01.mp4", "./videos/lesson01.srt"],
                2: ["./videos/lesson01.mp4"],
                3: ["./videos/lesson01.srt"],
            }
        )
    """
    print(f"\n{'='*50}")
    print(f"多Agent编排模式 — 自动搭建")
    print(f"{'='*50}\n")

    create_workspace(base_dir, executor_count)
    write_mission(base_dir, mission_text)

    if resource_map:
        for eid, paths in resource_map.items():
            copy_resources(base_dir, eid, paths)

    for i in range(1, executor_count + 1):
        write_task_template(base_dir, i, mission_text)
        write_result_template(base_dir, i)

    inject_prompt_to_executors(base_dir, executor_count)

    for i in range(1, executor_count + 1):
        write_executor_rules(base_dir, i)

    # plan.md 和 review.md 不由脚本自动生成
    # plan.md 由 AI 在阶段1手动写入（需要推理）
    # review.md 由 AI 在阶段4审查时手动创建（需要推理）

    for i in range(1, executor_count + 1):
        generate_start_prompt(base_dir, i)

    create_shared_notes(base_dir)
    generate_startup_summary(base_dir)

    print(f"\n{'='*50}")
    print(f"搭建完成！每个 executor 目录都是自包含的独立工作区。")
    print(f"")
    print(f"下一步：")
    print(f"1. 主Agent填写每个 task.md 中的（由主Agent填写）部分")
    print(f"2. 人类为每个 executor 新开对话，复制 START_HERE.txt 内容即可启动：")
    for i in range(1, executor_count + 1):
        edir = os.path.join(base_dir, f"executor_{i:02d}")
        print(f"   executor_{i:02d} → {edir}/START_HERE.txt")
    print(f"{'='*50}\n")


if __name__ == "__main__":
    print("用法：在主Agent对话中调用此脚本")
    print("")
    print("示例命令：")
    print('python launcher.py setup "./my_project" "目标描述" 3')
    print('python launcher.py check "./my_project"')
    print("")

    if len(sys.argv) >= 2:
        cmd = sys.argv[1]

        if cmd == "setup" and len(sys.argv) >= 5:
            base = sys.argv[2]
            mission = sys.argv[3]
            count = int(sys.argv[4])
            full_setup(base, mission, count)

        elif cmd == "check" and len(sys.argv) >= 3:
            base = sys.argv[2]
            results = check_results(base)
            print("\n执行状态：")
            for name, info in results.items():
                print(f"  {name}: {info['status']}")

        elif cmd == "summary" and len(sys.argv) >= 3:
            base = sys.argv[2]
            generate_startup_summary(base)
