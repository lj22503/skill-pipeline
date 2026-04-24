# 技能流水线（Skill Pipeline）v1.0.0

**定位**：元技能，编排 7 个技能管理工具，实现技能全生命周期自动化。

---

## 🎯 核心功能

| 功能 | 命令 | 说明 |
|------|------|------|
| 创建新技能 | `pipeline.py create` | 完整流程：发现→设计→创建→安全→质量→上线 |
| 检查技能 | `pipeline.py check` | 安全检查 + 质量评估 |
| 迭代技能 | `pipeline.py evolve` | 观察→总结→改进→验证 循环 |
| 技能审计 | `pipeline.py audit` | 批量审查，生成周报 |

---

## 📦 依赖技能

| 技能 | 用途 | 状态 |
|------|------|------|
| find-skills | 搜索生态 | ✅ 已安装 |
| skill-designer | 设计方案 | ✅ 已安装 |
| skill-creator | 创建初版 | ✅ 已安装 |
| skill-vetter | 安全检查 | ✅ 已安装 |
| skill-optimizer | 质量评估 | ✅ 已安装 |
| ljg-skill-map | 更新地图 | ✅ 已安装 |
| skill-evolve | 迭代改进 | ✅ 已安装 |

---

## 🚀 快速开始

### 创建新技能
```bash
python3 scripts/pipeline.py create --name "my-skill" --desc "技能描述"
```

### 检查现有技能
```bash
python3 scripts/pipeline.py check --skill "investment-framework"
```

### 迭代改进
```bash
python3 scripts/pipeline.py evolve --skill "skill-designer" --round 2
```

### 生成周报
```bash
python3 scripts/pipeline.py audit --week 17
```

---

## 📁 项目结构

```
skill-pipeline/
├── SKILL.md              ← 技能定义
├── README.md             ← 本文件
├── scripts/
│   └── pipeline.py       ← 主控制器
├── references/
│   ├── workflow.md       ← 工作流说明
│   └── checklist.md      ← 检查清单
├── templates/
│   └── pipeline-report.md ← 报告模板
└── logs/                 ← 运行日志（自动生成）
```

---

## 📊 工作流

```
发现 → 设计 → 创建 → 安全审查 → 质量评估 → 上线 → 迭代 → 审计
```

详细说明见 `references/workflow.md`

---

## ⚠️ 注意事项

1. **安全检查一票否决**：不通过则拒绝安装
2. **质量阈值**：≥75 分才能上线
3. **演进收敛**：连续 2 轮无新模式则停止
4. **日志记录**：所有操作自动记录到 logs/

---

*版本：1.0.0 | 最后更新：2026-04-24*
