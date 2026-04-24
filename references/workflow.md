# 技能流水线工作流详细说明

## 📋 工作流总览

```
发现 → 设计 → 创建 → 安全审查 → 质量评估 → 上线 → 迭代 → 审计
```

---

## 1. 发现阶段（find-skills）

**目标**：搜索生态，避免重复造轮子

**触发**：用户提出新技能需求

**执行**：
```bash
python3 scripts/pipeline.py discover --query "关键词"
```

**输出**：
- 匹配技能列表
- 安装建议

**决策点**：
- ✅ 有匹配 → 安装现有技能
- ❌ 无匹配 → 进入设计阶段

---

## 2. 设计阶段（skill-designer）

**目标**：设计可自运营的场景化 Skill 工具

**触发**：确认需要新技能

**执行**：
```bash
python3 scripts/pipeline.py design --audience "目标人群" --pain "痛点"
```

**输入**：
- 目标人群名称
- 核心痛点描述
- 5 维评分（痛点强度、分享意愿、付费能力、触达难度、任务复杂度）

**输出**：
- JSON 格式的结构化设计方案
- 人群评估、框架绑定、场景设计、价值验证、执行路径

---

## 3. 创建阶段（skill-creator）

**目标**：从 0 到 1 创建技能初版

**触发**：设计方案确认

**执行**：
```bash
python3 scripts/pipeline.py create --name "技能名称" --desc "技能描述"
```

**输出**：
- 技能目录结构
- SKILL.md 初版
- scripts/、references/、templates/ 目录

---

## 4. 安全审查阶段（skill-vetter）

**目标**：防止恶意代码

**触发**：技能创建后

**执行**：
```bash
python3 scripts/pipeline.py vet --skill "技能名称"
```

**检查项**：
- 危险命令（curl/wget/eval/exec/sudo/rm -rf）
- 权限范围
- 模板文件完整性

**决策点**：
- ✅ 通过 → 进入质量评估
- ❌ 失败 → 拒绝安装，联系作者或重新设计

---

## 5. 质量评估阶段（skill-optimizer）

**目标**：基于标准自动评分

**触发**：安全检查通过后

**执行**：
```bash
python3 scripts/pipeline.py optimize --skill "技能名称"
```

**评分维度**：
- 元数据完整（20%）
- 触发清晰度（25%）
- 结构完整（25%）
- 内容质量（20%）
- 规范性（10%）

**决策点**：
- ≥90 分：优秀，直接上线
- ≥75 分：良好，建议优化后上线
- ≥60 分：合格，需要优化
- <60 分：需改进，重新设计

---

## 6. 上线阶段（ljg-skill-map）

**目标**：更新技能地图

**触发**：质量评估通过后

**执行**：
```bash
python3 scripts/pipeline.py map
```

**输出**：
- 更新技能地图
- 记录上线日志

---

## 7. 迭代阶段（skill-evolve）

**目标**：持续改进技能质量

**触发**：使用反馈 / 定期审查

**执行**：
```bash
python3 scripts/pipeline.py evolve --skill "技能名称" --round 1
```

**工作流**：
1. 观察（用真实 prompt 跑 skill）
2. 总结（提炼错误模式）
3. 改进（JIT 原则，每轮只改一件事）
4. 验证（重跑对比）

**收敛标准**：
- 目标模式问题消失
- 连续两轮无新模式
- 用户说"可以了"

---

## 8. 审计阶段（skill-review-v3）

**目标**：批量质量审查

**触发**：每周一

**执行**：
```bash
python3 scripts/pipeline.py audit --week 17
```

**输出**：
- 技能周报
- 质量趋势
- 改进建议

---

## 🔗 技能协作关系

```
skill-pipeline（编排层）
  ├── find-skills（发现）
  ├── skill-designer（设计）
  ├── skill-creator（创建）
  ├── skill-vetter（安全）
  ├── skill-optimizer（质量）
  ├── ljg-skill-map（地图）
  └── skill-evolve（迭代）
```

---

## 📊 质量阈值

| 阶段 | 阈值 | 动作 |
|------|------|------|
| 安全检查 | 100% 通过 | 不通过则拒绝 |
| 质量评估 | ≥75 分 | <60 分重新设计 |
| 演进迭代 | 连续 2 轮收敛 | 不收敛则重新设计 |
| 定期审计 | 无严重问题 | 有问题则优先处理 |

---

*最后更新：2026-04-24*
