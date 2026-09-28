# 华严宗部数字化梳理平台 — 架构设计

> 更新: 2026-08-05 | Demo v2.0 重构计划

## 一、系统全景 — 三层知识管理架构

```
┌──────────────────────────────────────────────────────────────┐
│  L1: 权威数据层 (Authoritative Sources)                       │
│  SQLite (data/catalog/huayan.db)                              │
│  ┌──────────┬──────────┬──────────┬──────────┬──────────┐   │
│  │ persons  │  texts   │ glossary │locations │ chapters │   │
│  │cross_refs│trans_units│ FTS5全文检索 │ lineage_edges │   │
│  └──────────┴──────────┴──────────┴──────────┴──────────┘   │
│  权威数据源 — 所有策展/录入直接操作SQLite                      │
├──────────────────────────────────────────────────────────────┤
│  L2: 图验证层 (Graph Validation)                              │
│  Neo4j ← SQLite导出 → Cypher验证查询                          │
│  • 连通性: MATCH (p:Person) WHERE NOT (p)-[]-() RETURN p     │
│  • 完备性: 传承链无断环·关键人物存在                            │
│  • 一致性: 朝代-年份匹配·同名人去重                             │
├──────────────────────────────────────────────────────────────┤
│  L3: 展示层 (Presentation)                                    │
│  YAML/JSON ← SQLite导出脚本 → build.py → 多页面HTML           │
│  ┌──────────────────────────────────────────────────────┐    │
│  │  web/demo/                                          │    │
│  │  ├── index.html (导航主页)                           │    │
│  │  ├── css/common.css (共享样式)                       │    │
│  │  ├── js/common.js  (共享脚本)                        │    │
│  │  └── tabs/                                          │    │
│  │      ├── lineage.html   (Tab1: 法脉传承·布局保留)     │    │
│  │      ├── gap.html       (Tab2: 华严文献·布局重构)     │    │
│  │      ├── jiaoxing.html  (Tab3: 华严教行·布局重构)     │    │
│  │      ├── frontier.html  (Tab4: 前沿对话·布局重构)     │    │
│  │      └── cosmology.html (Tab5: 世主妙严·布局重构)     │    │
│  └──────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────┘
```

**数据流**: SQLite (权威源) → export脚本 → YAML/JSON (中间格式) → build.py → HTML
**验证流**: SQLite → Neo4j加载 → Cypher查询 → 验证报告
**策展流**: 研究/录入 → SQLite INSERT/UPDATE → Git diff 可审计

## 二、核心数据模型

### Person (人物)
```
id, n(name), dy(dynasty), ti(title), li(lineage), multi[secondary lineages]
tp(type: patriarch|translator|scholar|practitioner)
b(birth), d(death), bio, wk(works[])
_isGhost: 多法脉副条目标记
```

### Edge (传承边)
```
s(source), t(target), r(relation: MASTER|INFLUENCE|LINEAGE|CONTEMPORARY), li(lineage)
```

### Location (地点)
```
id, n(name), lat, lng, tp(type: temple|mountain|region), dy(dynasty), ds(description), ps(persons[])
```

### 法系颜色映射
```
华严五祖=#b8863c 华严莲社=#5e8b9e 月霞系=#7a9ec0 贤首宗高原法系=#c46b5d
临济宗=#d48476 高丽华严=#6d9a6e 日本华严=#8b7a9e 李通玄系=#c8893e
慈舟系=#8b7a9e 译师=#a09080 印度源流=#9e8b6e 当代学者=#b0a898
```

## 三、源码模块

### Web源文件 (web/demo/src/)

| 文件 | 职责 | 行数 |
|------|------|------|
| `data.js` | GRAPH/GAP/HEART数据占位 + 全局变量 | 7 |
| `lineage.js` | Tab1: Canvas时间轴/地图/动画/交互/法系 | 1230 |
| `gap.js` | Tab2: 差异总览/原文对读/文本系谱/参考文献 | 479 |
| `jiaoxing.js` | Tab3: 华严教行（原practice.js·重命名） | 948 |
| `frontier.js` | Tab4: 跨界对话/文献综述 | 121 |
| `cosmology.js` | Tab5: 华藏世界海曼荼罗/三界诸天 | 309 |
| `init.js` | 初始化/评论系统/GitHub认证/事件绑定 | 225 |

### 数据文件 (data/)

| 目录 | 格式 | 说明 |
|------|------|------|
| `catalog/schema.sql` | SQL | SQLite完整Schema（权威数据源） |
| `catalog/huayan.db` | SQLite | 运行时数据库 |
| `knowledge_graph/` | JSON→SQLite | 人物·关系·地点（从SQLite导出） |
| `translation/` | YAML→SQLite | 差异矩阵·术语库·gap内容 |
| `practice/` | YAML | 修行体系·禅观法要·讲法资源 |
| `frontier/` | YAML | 跨界对话·文献综述 |
| `cosmology/` | YAML | 华藏世界海·三界诸天·艺术珍品 |
| `events/` | YAML | 历史事件·动画节点·传播故事 |

### 构建脚本

| 文件 | 职责 |
|------|------|
| `web/demo/scripts/build.py` | 主构建：YAML/JSON → 6个HTML+CSS+JS |
| `scripts/export_sqlite_to_json.py` | SQLite → JSON/YAML 导出 |
| `scripts/load_neo4j.py` | SQLite → Neo4j 加载+验证 |
| `scripts/verify_sources.py` | 来源可靠性分级验证 (T1/T2/T3/T0) |
| `scripts/verify_demo.py` | 构建产物18项自动检查 |

## 四、构建流程

```
SQLite (权威源)
    │
    ├── export_sqlite_to_json.py ──→ data/knowledge_graph/*.json
    │                                data/translation/*.yaml
    │
    ├── load_neo4j.py ──→ Neo4j (连通性/完备性/一致性验证)
    │
    ▼
data/**/*.yaml ──────────┐
web/demo/src/*.js ───────┤
web/demo/src/*.css ──────┤
                          ├── build.py ──→ web/demo/
web/demo/src/data.js ────┤                ├── index.html
                          │                ├── css/common.css
                          │                ├── js/common.js
                          │                └── tabs/*.html (5个)
                          │
verify_demo.py ──────────┘ (18项检查)

verify_sources.py (来源可靠性T1-T3-T0评分)
```

## 五、数据库Schema

SQLite数据库 `data/catalog/huayan.db` 包含以下表（完整定义见 `data/catalog/schema.sql`）：

| 表名 | 说明 | 核心字段 |
|------|------|---------|
| `persons` | 人物（祖师/译者/行者/学者） | name_zh, type, birth_year, death_year, dynasty, lineage_branch, source, verified |
| `texts` | 经典/章疏/仪轨/讲记 | title_zh, type, taisho_no, cbeta_id, tohk_no, author_id, translator_id |
| `chapters` | 品目 | sutra_id, title_zh, order_num, in_60/80/40huayan, in_tibetan, content_diff |
| `locations` | 地点 | name_zh, lat, lng, type, dynasty, related_persons |
| `person_locations` | 人物-地点关联 | person_id, location_id, relation (born/died/taught/visited) |
| `cross_refs` | 文献互参 | from_text_id, to_text_id, relation (cites/commentary_on/alternate_trans) |
| `glossary` | 四语术语 | term_sa/bo/zh/en, category, definition_zh/en, alt_translations |
| `translation_units` | 对译单元 | chapter_id, source_text, chinese_draft, english_draft, status |
| `texts_fts` | 全文检索 | FTS5虚拟表，覆盖title/abstract |
| `glossary_fts` | 术语全文检索 | FTS5虚拟表 |

Neo4j图数据库用于验证（非持久存储），加载persons和edges后进行：
- **连通性**: 无孤立人物节点
- **完备性**: 传承链无断环
- **一致性**: 朝代-年份匹配，同名人去重
