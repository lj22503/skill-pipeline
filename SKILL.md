---
name: skill-pipeline
description: ［何时使用］当用户需要创建/检查/迭代技能时；当用户说"新技能"、"检查技能"、"迭代技能"、"技能周报"、"skill pipeline"时；当检测到技能生命周期管理相关关键词时
author: ant (CEO 助理)
created: 2026-04-24
version: 1.0.0
skill_type: 核心🔴
allowed-tools: [Bash, Read, Write, Exec]
related_skills: [skill-creator, skill-evolve, skill-optimizer, skill-vetter, skill-designer, find-skills, ljg-skill-map]
tags: [技能管理，工作流，编排，生命周期，自动化]
---

# 技能流水线（Skill Pipeline）v1.0.0

**定位**：元技能，编排 7 个技能管理工具，实现技能全生命周期自动化。

---

## 🎯 核心功能

### 功能 1：新技能创建（完整流程）

**触发**："新技能：XXX"、"创建技能"

**流程**：
```
find-skills（搜索生态）
  ↓ 无匹配
skill-designer（设计方案）
  ↓
skill-creator（创建初版）
  ↓
skill-vetter（安全检查）
  ↓ 通过
skill-optimizer（质量评估）
  ↓ ≥75 分
ljg-skill-map（更新地图）
  ↓
上线使用
```

**执行**：
```bash
# 运行完整流程
python3 scripts/pipeline.py create --name "my-skill" --desc "技能描述"

# 分步执行
python3 scripts/pipeline.py discover --query "关键词"
python3 scripts/pipeline.py design --audience "目标人群" --pain "痛点"
python3 scripts/pipeline.py create --name "my-skill"
python3 scripts/pipeline.py vet --skill "my-skill"
python3 scripts/pipeline.py optimize --skill "my-skill"
```

### 功能 2：技能检查（vet + optimize）

**触发**："检查技能：XXX"、"技能审查"

**流程**：
```
skill-vetter（安全检查）
  ↓ 通过
skill-optimizer（质量评估）
  ↓
生成报告
```

**执行**：
```bash
python3 scripts/pipeline.py check --skill "my-skill"
```

### 功能 3：技能迭代（evolve）

**触发**："迭代技能：XXX"、"优化技能"

**流程**：
```
skill-evolve（观察→总结→改进→验证）
  ↓
skill-optimizer（验证改进效果）
  ↓
更新版本
```

**执行**：
```bash
python3 scripts/pipeline.py evolve --skill "my-skill" --round 1
```

### 功能 4：技能周报（批量审查）

**触发**："技能周报"、"技能审计"

**流程**：
```
ljg-skill-map（扫描全部技能）
  ↓
skill-review-v3（批量审查）
  ↓
生成周报报告
```

**执行**：
```bash
python3 scripts/pipeline.py audit --week 17
```

---

## ⚠️ 常见错误

**错误 1：跳过安全检查**
```
问题：
• 直接安装未 vet 的技能
• 可能存在安全风险

解决：
✓ 所有新技能必须经过 skill-vetter 检查
✓ 检查不通过的技能禁止安装
```

**错误 2：质量评估不达标就上线**
```
问题：
• skill-optimizer 评分 <75 分就上线
• 用户体验差

解决：
✓ 评分 ≥75 分才能上线
✓ <60 分必须重新设计
```

**错误 3：不记录演进日志**
```
问题：
• skill-evolve 改进后不记录 changes.md
• 下次改进从零开始

解决：
✓ 每轮改进必须记录到 evolution-log.md
✓ 遵循 Bootstrap 原则（笔记自举）
```

---

## 🧪 使用示例

**输入**：
```bash
# 创建新技能
python3 scripts/pipeline.py create --name "content-analyzer" --desc "内容分析工具"

# 检查现有技能
python3 scripts/pipeline.py check --skill "investment-framework"

# 迭代改进
python3 scripts/pipeline.py evolve --skill "skill-designer" --round 2

# 生成周报
python3 scripts/pipeline.py audit --week 17
```

**预期输出**：
```
🔧 技能流水线 v1.0.0
==================================================

📋 任务：创建新技能
🎯 技能名称：content-analyzer
📝 描述：内容分析工具

─────────────────────────────────────────
步骤 1/6：搜索生态...
✅ 未找到匹配技能

步骤 2/6：设计方案...
✅ 设计完成（人群评估：4.2/5）

步骤 3/6：创建初版...
✅ 初版创建完成

步骤 4/6：安全检查...
✅ 通过（Safe / Low Risk）

步骤 5/6：质量评估...
✅ 评分：82/100（良好）

步骤 6/6：更新地图...
✅ 地图已更新

🎉 技能上线成功！
路径：~/.agents/skills/content-analyzer
==================================================
```

---

## 🔗 相关资源

- `references/workflow.md` - 工作流详细说明
- `references/checklist.md` - 质量检查清单
- `templates/pipeline-report.md` - 报告模板
- `scripts/pipeline.py` - 主控制器

---

## 🔧 故障排查

| 问题 | 检查项 | 解决方案 |
|------|--------|---------|
| 流程中断 | 上一步是否完成？ | 检查日志，修复后重试 |
| 评分异常 | 标准文件存在吗？ | 检查 skill-optimizer 配置 |
| 安全检查失败 | 有恶意代码吗？ | 联系技能作者或拒绝安装 |
| 演进不收敛 | 测试 prompt 合理吗？ | 重新选择测试用例 |

---

*版本：1.0.0 | 最后更新：2026-04-24*
