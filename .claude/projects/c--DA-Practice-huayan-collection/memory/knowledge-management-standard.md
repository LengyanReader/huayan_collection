---
name: knowledge-management-standard
description: 全Tab知识管理规范 — 所有内容数据源文件化，禁止硬编码
metadata:
  type: project
---

所有 Tab 显示的所有内容必须来源于结构化源文件（JSON/YAML），绝非硬编码在 JS 中。

## 数据源文件映射

| Tab | 内容 | 源文件 | 格式 |
|-----|------|--------|------|
| 法脉传承 | 人物 | `data/knowledge_graph/personas.json` | JSON |
| 法脉传承 | 传承边 | `data/knowledge_graph/lineages.json` | JSON |
| 法脉传承 | 地点 | `data/knowledge_graph/locations.json` | JSON |
| 法脉传承 | 历史事件 | `data/events/key_events.yaml` | YAML |
| 法脉传承 | 动画节点 | `data/events/anim_waypoints.yaml` | YAML |
| 法脉传承 | 传播故事 | `data/events/transmission_story.yaml` | YAML |
| 法脉传承 | 理论/修行阶段 | `data/events/theory_practice_stages.yaml` | YAML |
| 汉藏文献 | 差异矩阵 | `data/translation/diff_matrix.yaml` | YAML |
| 汉藏文献 | 术语库 | `data/translation/glossary.yaml` | YAML |
| 汉藏文献 | 文献目录 | `data/catalog/complete_catalog.yaml` | YAML |
| 华严行法 | 修行体系内容 | `data/practice/` (待建) | YAML |
| 前沿对话 | 文献综述 | `data/frontier/` (待建) | YAML |
| 华严其观 | 宇宙观数据 | `data/cosmology/` (待建) | YAML |
| 参考 | 外部参考 | `data/references/` | Markdown |

## 核心原则

1. **禁止硬编码**: 不在 build.py 或 JS 文件中直接写人物/边/事件数据
2. **先入库再显示**: 新增任何内容前，先写入对应源文件
3. **构建验证**: 每次构建打印人数/边数/地点数，确保数据完整
4. **源文件即真相**: index.html 只是产出，所有修改从源文件出发

## 新增内容流程

1. 确定内容类型 → 找到对应源文件
2. 按现有格式追加记录
3. 运行 `python web/demo/scripts/build.py` 构建
4. 验证构建输出的人数/边数/事件数一致
5. Git commit + push

**Why:** 用户要求「所有页面的所有内容」都要有后台知识管理，便于开发/维护/恢复/进化。

**How to apply:** 每次添加数据前先确认已入库；新增内容类型时先创建源文件再写入数据；build.py 只做读取+组装，不硬编码。
