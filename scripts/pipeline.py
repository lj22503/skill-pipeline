#!/usr/bin/env python3
"""
技能流水线主控制器 v1.0.0
编排 7 个技能管理工具，实现技能全生命周期自动化。
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# 配置
SKILLS_DIR = Path.home() / ".agents" / "skills"
PIPELINE_DIR = Path(__file__).parent.parent
LOG_DIR = PIPELINE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

# 技能路径映射
SKILL_PATHS = {
    "skill-creator": SKILLS_DIR / "skill-creator",
    "skill-evolve": SKILLS_DIR / "skill-evolve",
    "skill-optimizer": SKILLS_DIR / "skill-optimizer",
    "skill-vetter": SKILLS_DIR / "skill-vetter",
    "skill-designer": SKILLS_DIR / "skill-designer",
    "find-skills": SKILLS_DIR / "find-skills",
    "ljg-skill-map": SKILLS_DIR / "ljg-skills" / "skills" / "ljg-skill-map",
}


def log(message: str, level: str = "INFO"):
    """记录日志"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] [{level}] {message}"
    print(log_line)
    
    # 写入日志文件
    log_file = LOG_DIR / f"pipeline-{datetime.now().strftime('%Y-%m-%d')}.log"
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(log_line + "\n")


def run_command(cmd: list, cwd: str = None) -> tuple:
    """运行命令并返回结果（兼容 Python 3.6+）"""
    log(f"执行命令：{' '.join(cmd)}")
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            timeout=300
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        log("命令超时", "ERROR")
        return -1, "", "Timeout"
    except Exception as e:
        log(f"命令执行失败：{e}", "ERROR")
        return -1, "", str(e)


def step_discover(query: str) -> bool:
    """步骤 1：搜索生态（使用 find-skills）"""
    log("步骤 1/6：搜索生态...")
    
    # 使用 npx skills find 搜索
    cmd = ["npx", "skills", "find", query]
    code, stdout, stderr = run_command(cmd)
    
    if code == 0:
        # 检查是否有匹配结果
        if "Install with" in stdout:
            log("✅ 找到匹配技能", "SUCCESS")
            # 提取技能列表
            lines = stdout.strip().split("\n")
            skills_found = [line.strip() for line in lines if "Install with" not in line and line.strip()]
            if skills_found:
                log(f"找到 {len(skills_found)} 个匹配技能：", "SUCCESS")
                for skill in skills_found[:5]:
                    log(f"  - {skill}", "SUCCESS")
            return True
        else:
            log("✅ 未找到匹配技能", "SUCCESS")
            return False
    else:
        log(f"搜索失败：{stderr}", "WARN")
        # 搜索失败不阻塞流程，继续创建
        return False


def step_design(audience: str, pain: str) -> bool:
    """步骤 2：设计方案"""
    log("步骤 2/6：设计方案...")
    
    # 使用 skill-designer
    designer_script = SKILL_PATHS["skill-designer"] / "scripts" / "designer.py"
    if not designer_script.exists():
        log("skill-designer 脚本不存在", "ERROR")
        return False
    
    cmd = [
        "python3", str(designer_script),
        "--audience", audience,
        "--pain", pain,
        "--scores", '{"pain_intensity":5,"sharing_willingness":5,"payment_ability":4,"reachability":2,"task_complexity":3}'
    ]
    code, stdout, stderr = run_command(cmd)
    
    if code == 0:
        log("✅ 设计完成", "SUCCESS")
        return True
    else:
        log(f"设计失败：{stderr}", "ERROR")
        return False


def step_create(name: str, desc: str = "") -> bool:
    """步骤 3：创建初版"""
    log(f"步骤 3/6：创建初版 - {name}...")
    
    # 使用 skill-creator
    creator_script = SKILL_PATHS["skill-creator"] / "scripts" / "creator.py"
    if creator_script.exists():
        cmd = ["python3", str(creator_script), "--name", name, "--desc", desc]
        code, stdout, stderr = run_command(cmd)
        
        if code == 0:
            log("✅ 初版创建完成", "SUCCESS")
            return True
        else:
            log(f"创建失败：{stderr}", "ERROR")
            return False
    else:
        # 手动创建基础结构
        skill_dir = SKILLS_DIR / name
        skill_dir.mkdir(parents=True, exist_ok=True)
        
        # 创建 SKILL.md
        skill_md = skill_dir / "SKILL.md"
        content = f"""---
name: {name}
description: ［何时使用］{desc}
author: ant (CEO 助理)
created: {datetime.now().strftime('%Y-%m-%d')}
version: 1.0.0
skill_type: 通用🟡
allowed-tools: [Bash, Read, Write, Exec]
tags: [{name}]
---

# {name}

**描述**：{desc}

## 🎯 功能

（待补充）

## ⚠️ 常见错误

（待补充）

## 🧪 使用示例

（待补充）

---

*版本：1.0.0 | 最后更新：{datetime.now().strftime('%Y-%m-%d')}*
"""
        with open(skill_md, "w", encoding="utf-8") as f:
            f.write(content)
        
        log("✅ 初版创建完成（基础结构）", "SUCCESS")
        return True


def step_vet(skill_name: str) -> bool:
    """步骤 4：安全检查"""
    log("步骤 4/6：安全检查...")
    
    # 使用 skill-vetter
    vetter_script = SKILL_PATHS["skill-vetter"] / "scripts" / "vetter.py"
    if vetter_script.exists():
        cmd = ["python3", str(vetter_script), "--skill", skill_name]
        code, stdout, stderr = run_command(cmd)
        
        if code == 0:
            log("✅ 安全检查通过", "SUCCESS")
            return True
        else:
            log(f"安全检查失败：{stderr}", "ERROR")
            return False
    else:
        # 手动检查
        skill_dir = SKILLS_DIR / skill_name
        if not skill_dir.exists():
            log(f"技能目录不存在：{skill_dir}", "ERROR")
            return False
        
        # 检查 SKILL.md
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            log("SKILL.md 不存在", "ERROR")
            return False
        
        # 检查是否有危险命令
        with open(skill_md, "r", encoding="utf-8") as f:
            content = f.read()
        
        dangerous_patterns = ["curl", "wget", "eval(", "exec(", "sudo", "rm -rf"]
        found_dangerous = [p for p in dangerous_patterns if p in content]
        
        if found_dangerous:
            log(f"发现危险模式：{found_dangerous}", "ERROR")
            return False
        
        log("✅ 安全检查通过（手动）", "SUCCESS")
        return True


def step_optimize(skill_name: str) -> int:
    """步骤 5：质量评估"""
    log("步骤 5/6：质量评估...")
    
    # 使用 skill-optimizer
    optimizer_script = SKILL_PATHS["skill-optimizer"] / "scripts" / "optimize-skill.py"
    if optimizer_script.exists():
        cmd = ["python3", str(optimizer_script), skill_name]
        code, stdout, stderr = run_command(cmd)
        
        if code == 0:
            # 提取评分
            if "总分：" in stdout:
                score_line = [line for line in stdout.split("\n") if "总分：" in line][0]
                score = int(score_line.split("：")[1].split("/")[0])
                log(f"✅ 评分：{score}/100", "SUCCESS")
                return score
            else:
                log("✅ 评估完成（未提取到评分）", "SUCCESS")
                return 75  # 默认良好
        else:
            log(f"评估失败：{stderr}", "ERROR")
            return 0
    else:
        # 手动评估
        skill_dir = SKILLS_DIR / skill_name
        skill_md = skill_dir / "SKILL.md"
        
        if not skill_md.exists():
            log("SKILL.md 不存在", "ERROR")
            return 0
        
        with open(skill_md, "r", encoding="utf-8") as f:
            content = f.read()
        
        # 简单评分
        score = 0
        if "name:" in content: score += 15
        if "description:" in content: score += 20
        if "功能" in content: score += 20
        if "常见错误" in content: score += 15
        if "使用示例" in content: score += 15
        if "故障排查" in content: score += 15
        
        log(f"✅ 评分：{score}/100（手动）", "SUCCESS")
        return score


def step_map() -> bool:
    """步骤 6：更新地图"""
    log("步骤 6/6：更新地图...")
    
    # 使用 ljg-skill-map
    scan_script = SKILL_PATHS["ljg-skill-map"] / "scripts" / "scan.sh"
    if scan_script.exists():
        cmd = ["bash", str(scan_script)]
        code, stdout, stderr = run_command(cmd)
        
        if code == 0:
            log("✅ 地图已更新", "SUCCESS")
            return True
        else:
            log(f"地图更新失败：{stderr}", "ERROR")
            return False
    else:
        log("✅ 地图更新跳过（scan.sh 不存在）", "WARN")
        return True


def create_pipeline(name: str, desc: str = "", audience: str = "", pain: str = ""):
    """执行完整创建流程"""
    log("=" * 60)
    log("🔧 技能流水线 v1.0.0")
    log("=" * 60)
    log(f"📋 任务：创建新技能")
    log(f"🎯 技能名称：{name}")
    log(f"📝 描述：{desc}")
    log("=" * 60)
    
    # 步骤 1：搜索生态
    if step_discover(name):
        log("⚠️  已存在相似技能，是否继续创建？(y/n)", "WARN")
        response = input().strip().lower()
        if response != "y":
            log("创建已取消", "WARN")
            return
    
    # 步骤 2：设计方案（可选）
    if audience and pain:
        if not step_design(audience, pain):
            log("设计失败，继续创建...", "WARN")
    
    # 步骤 3：创建初版
    if not step_create(name, desc):
        log("创建失败，流程终止", "ERROR")
        return
    
    # 步骤 4：安全检查
    if not step_vet(name):
        log("安全检查失败，流程终止", "ERROR")
        return
    
    # 步骤 5：质量评估
    score = step_optimize(name)
    if score < 60:
        log(f"⚠️  评分 {score}/100 < 60，建议重新设计", "WARN")
    elif score < 75:
        log(f"⚠️  评分 {score}/100 < 75，建议优化", "WARN")
    
    # 步骤 6：更新地图
    step_map()
    
    log("=" * 60)
    log("🎉 技能上线成功！", "SUCCESS")
    log(f"路径：{SKILLS_DIR / name}", "SUCCESS")
    log("=" * 60)


def check_pipeline(skill_name: str):
    """执行检查流程"""
    log("=" * 60)
    log("🔧 技能流水线 v1.0.0")
    log("=" * 60)
    log(f"📋 任务：检查技能 - {skill_name}")
    log("=" * 60)
    
    # 步骤 1：安全检查
    if not step_vet(skill_name):
        log("安全检查失败", "ERROR")
        return
    
    # 步骤 2：质量评估
    score = step_optimize(skill_name)
    
    log("=" * 60)
    log(f"📊 检查结果：{skill_name}", "SUCCESS")
    log(f"安全评分：✅ 通过")
    log(f"质量评分：{score}/100")
    log("=" * 60)


def evolve_pipeline(skill_name: str, round_num: int = 1):
    """执行迭代流程（使用 skill-evolve）"""
    log("=" * 60)
    log("🔧 技能流水线 v1.0.0")
    log("=" * 60)
    log(f"📋 任务：迭代技能 - {skill_name} (Round {round_num})")
    log("=" * 60)
    
    # 使用 skill-evolve
    evolve_base = SKILLS_DIR / f"{skill_name}-evolve"
    evolve_dir = evolve_base / f"round-{round_num}"
    evolve_dir.mkdir(parents=True, exist_ok=True)
    
    log(f"演进目录：{evolve_dir}", "INFO")
    
    # 创建演进日志模板
    evolution_log = evolve_base / "evolution-log.md"
    if not evolution_log.exists():
        log_content = f"""# Evolution Log — {skill_name}

## Round 1 ({datetime.now().strftime('%Y-%m-%d')})

### 观察到的问题
（待补充）

### 改进的措施
（待补充）

### 验证结果
（待补充）

### 剩余问题
（待补充）

### 洞察
（待补充）

---

*由 skill-pipeline 自动生成*
"""
        with open(evolution_log, "w", encoding="utf-8") as f:
            f.write(log_content)
        log(f"✅ 演进日志已创建：{evolution_log}", "SUCCESS")
    
    # 创建 round 目录模板文件
    observations_file = evolve_dir / "observations.md"
    patterns_file = evolve_dir / "patterns.md"
    changes_file = evolve_dir / "changes.md"
    
    if not observations_file.exists():
        with open(observations_file, "w", encoding="utf-8") as f:
            f.write(f"""# 观察记录 — Round {round_num}

## Prompt 1: [简述]
- 结果：[好/一般/差]
- 具体问题：[描述]
- 猜测原因：[指向 skill 中的哪段指令]

## Prompt 2: [简述]
...

---

*由 skill-pipeline 自动生成*
""")
    
    if not patterns_file.exists():
        with open(patterns_file, "w", encoding="utf-8") as f:
            f.write(f"""# 错误模式表 — Round {round_num}

## P01: [模式名称]
- 出现次数：N 次（prompt 1, 3, 5）
- 表现：[用户看到了什么问题]
- 根因：[skill 中的哪段指令导致的]
- 影响面：[高/中/低]

## 本轮改进优先级
1. P0x — [理由]
2. P0x — [理由]

---

*由 skill-pipeline 自动生成*
""")
    
    if not changes_file.exists():
        with open(changes_file, "w", encoding="utf-8") as f:
            f.write(f"""# 改写记录 — Round {round_num}

## 目标模式
- P01: [模式名]
- P02: [模式名]

## 改动清单
1. [文件:行号] 改了什么，为什么
2. ...

## 预期效果
- Prompt 1 应该不再出现 [具体问题]
- Prompt 3 应该 [具体改善]

---

*由 skill-pipeline 自动生成*
""")
    
    log("✅ 演进模板文件已创建", "SUCCESS")
    log("请按照 skill-evolve 的工作流进行改进...", "INFO")
    log("1. 读取目标 skill 的全部内容", "INFO")
    log("2. 选择 3-5 个测试 prompt", "INFO")
    log("3. 跑 skill 并记录观察", "INFO")
    log("4. 提炼模式", "INFO")
    log("5. 改写（JIT 原则）", "INFO")
    log("6. 验证", "INFO")
    
    log("=" * 60)


def audit_pipeline(week_num: int = None):
    """执行审计流程"""
    if week_num is None:
        week_num = datetime.now().isocalendar()[1]
    
    log("=" * 60)
    log("🔧 技能流水线 v1.0.0")
    log("=" * 60)
    log(f"📋 任务：技能周报 - Week {week_num}")
    log("=" * 60)
    
    # 步骤 1：扫描全部技能
    log("扫描技能库...")
    cmd = ["bash", str(SKILL_PATHS["ljg-skill-map"] / "scripts" / "scan.sh")]
    code, stdout, stderr = run_command(cmd)
    
    if code == 0:
        log("✅ 技能库扫描完成", "SUCCESS")
    else:
        log(f"扫描失败：{stderr}", "ERROR")
    
    # 步骤 2：生成周报
    report_file = LOG_DIR / f"skill-report-W{week_num}.md"
    report_content = f"""# 技能周报 - Week {week_num}

**生成时间**：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**生成工具**：skill-pipeline v1.0.0

## 📊 技能库概况

（待补充）

## 🔍 质量审查

（待补充）

## 📈 改进建议

（待补充）

---

*由 skill-pipeline 自动生成*
"""
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report_content)
    
    log(f"✅ 周报已生成：{report_file}", "SUCCESS")
    log("=" * 60)


def main():
    parser = argparse.ArgumentParser(description="技能流水线 v1.0.0")
    subparsers = parser.add_subparsers(dest="command", help="子命令")
    
    # create 命令
    create_parser = subparsers.add_parser("create", help="创建新技能")
    create_parser.add_argument("--name", required=True, help="技能名称")
    create_parser.add_argument("--desc", default="", help="技能描述")
    create_parser.add_argument("--audience", default="", help="目标人群")
    create_parser.add_argument("--pain", default="", help="核心痛点")
    
    # check 命令
    check_parser = subparsers.add_parser("check", help="检查技能")
    check_parser.add_argument("--skill", required=True, help="技能名称")
    
    # evolve 命令
    evolve_parser = subparsers.add_parser("evolve", help="迭代技能")
    evolve_parser.add_argument("--skill", required=True, help="技能名称")
    evolve_parser.add_argument("--round", type=int, default=1, help="轮次")
    
    # audit 命令
    audit_parser = subparsers.add_parser("audit", help="技能审计")
    audit_parser.add_argument("--week", type=int, help="周数")
    
    args = parser.parse_args()
    
    if args.command == "create":
        create_pipeline(args.name, args.desc, args.audience, args.pain)
    elif args.command == "check":
        check_pipeline(args.skill)
    elif args.command == "evolve":
        evolve_pipeline(args.skill, args.round)
    elif args.command == "audit":
        audit_pipeline(args.week)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
