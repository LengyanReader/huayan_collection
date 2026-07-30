# 知识管理方案

> 2026-07-31 | 基于 Demo v0.9 数据审计

## 一、数据分层架构

```
data/
├── knowledge_graph/           ← 人物·关系·地点 (JSON/YAML)
│   ├── personas.json          ← 73人物 (已入库44, 待迁移~25)
│   ├── lineages.json          ← 81传承边 (已入库47, 待迁移~34)
│   ├── locations.json         ← 23地点 (已入库)
│   └── schemas/               ← JSON Schema 校验
├── translation/               ← 汉藏对译 (YAML)
│   ├── diff_matrix.yaml       ← 品目差异矩阵
│   └── glossary.yaml          ← 术语库
├── catalog/                   ← 文献目录 (SQL+YAML)
│   ├── complete_catalog.yaml
│   └── schema.sql
├── references/                ← 参考文档 (Markdown·只读)
│   └── ref海云继梦法师_佛法修行体系研究.md
└── events/                    ← 待建: 历史事件/动画数据
    ├── key_events.yaml        ← 待建: 36条KEY_EVENTS
    ├── anim_waypoints.yaml    ← 待建: 42+动画节点
    └── transmission_story.yaml← 待建: 传播故事

web/demo/scripts/build.py      ← 构建脚本 (应只读取数据, 不硬编码)
web/demo/src/*.js              ← 前端代码 (数据通过GRAPH/GAP注入)
```

## 二、当前硬编码残留

### A. build.py 中（须迁移至 JSON）

| 类别 | 数量 | 目标文件 |
|------|------|---------|
| 补充人物(思元慧三/体化性果/良弁~观贤7人) | ~9人 | personas.json |
| 日本华严 + 学者 + 法身源头 + 元晓·慧苑·续法 + 义湘·慧光等 | ~15人 | personas.json |
| 各类边(日本/华严/求法僧/跨宗派) | ~30边 | lineages.json |
| 补充地点(东大寺/大华严寺/福慧寺/龟兹等) | ~5处 | locations.json |

### B. lineage.js 中（须迁移至 YAML/JSON）

| 数据 | 数量 | 目标文件 |
|------|------|---------|
| ANIM_WAYPOINTS（动画节点） | ~48条 | events/anim_waypoints.yaml |
| KEY_EVENTS（历史事件） | ~36条 | events/key_events.yaml |
| TRANS_STORY（传播故事） | ~20条 | events/transmission_story.yaml |
| THEORY_STAGES | 6条 | events/theory_stages.yaml |
| PRACTICE_STAGES | 6条 | events/practice_stages.yaml |

### C. cosmology.js 中

| 数据 | 数量 | 目标文件 |
|------|------|---------|
| COSMO_LAYERS（20层世界） | 20条 | events/cosmo_layers.yaml |
| COSMO_WINDS（10重风轮） | 10条 | 同上 |

## 三、迁移优先级

| 优先级 | 内容 | 工作量 | 收益 |
|--------|------|--------|------|
| P0 | build.py 硬编码人物→personas.json | 中 | 消除双重数据源 |
| P0 | build.py 硬编码边→lineages.json | 中 | 同上 |
| P1 | KEY_EVENTS→events/key_events.yaml | 中 | 事件可独立维护 |
| P1 | ANIM_WAYPOINTS→events/anim_waypoints.yaml | 中 | 动画数据可单独更新 |
| P2 | TRANS_STORY→events/transmission_story.yaml | 小 | 传播路线独立管理 |
| P2 | THEORY/PRACTICE/COSMO数据 | 小 | 内容数据独立 |

## 四、维护规范

1. **新增人物**: 写入 `personas.json`，通过 `build.py` 自动构建
2. **新增边**: 写入 `lineages.json`
3. **新增地点**: 写入 `locations.json`
4. **新增事件**: 写入 `events/key_events.yaml`
5. **修改内容**: 只改源文件，不直接改 `index.html`
6. **构建验证**: `python web/demo/scripts/build.py` 后检查人数/边数
7. **备份恢复**: Git 版本控制 + JSON 结构化 → 可直接重建
