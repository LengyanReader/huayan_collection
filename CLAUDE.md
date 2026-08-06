# CLAUDE.md — 华严宗部文献与修行资料数字化梳理

## 项目概述

构建以华严宗为核心的佛法文献与修行资料数字化系统：
1. **多维知识图谱**：华严宗祖师/行者传承谱系、地理道场、经典关联（**92 人**，46 处地点/道场，**96 条**传承边，174 条人物行迹，73 处文明疆域）
2. **藏汉华严对译**：藏文《华严经》(Toh 44, 45品) vs 汉文 (39品) 差异比对
3. **华严宇宙观**：华藏世界海曼荼罗 + 三界诸天图

## Demo

**[web/demo/index.html](web/demo/index.html)** — 导航主页，链接到5个独立Tab页面
- Tab 1: **法脉传承**·时空长河 (Canvas时间轴 + 理论/修行图层 + 主地图 + 西方文明+华严路线双迷你地图 + 92节点动画 + 古地图模式 + 174条人物行迹)
- Tab 2: **华严文献**·汉藏差异 (子导航四页 + 三语对读 + 50条术语 + 文本系谱)
- Tab 3: **华严教行** (子导航四页·修行体系/禅观法要/实修心要/讲法资源 + YouTube集成)
- Tab 4: **前沿对话** (AI/计算现象学/神经科学/心灵哲学 + 文献综述)
- Tab 5: **世主妙严** (华藏世界海曼荼罗 + 三界诸天图 + 艺术珍品 + 梵呗)

## 知识管理架构（三层数据栈）

```
L1: SQLite (权威数据源)  →  L2: Neo4j (图验证引擎)  →  L3: YAML/JSON → HTML
```

- **SQLite** (`data/catalog/huayan.db`): persons, texts, chapters, locations, glossary, translation_units + FTS5全文检索
- **Neo4j**: 连通性/完备性/一致性 Cypher 验证
- **YAML/JSON**: SQLite导出 → build.py读取 → 注入HTML
- **策展**: 直接操作SQLite，Git跟踪schema.sql+seed_data.sql

详见 [docs/knowledge-management.md](docs/knowledge-management.md)

## 核心文档索引

| 文档 | 路径 | 说明 |
|------|------|------|
| 后续计划 | [docs/next-phase-plan.md](docs/next-phase-plan.md) | v2.0重构 P0-P4 路线图 |
| 架构设计 | [docs/architecture.md](docs/architecture.md) | 三层数据栈、数据模型、模块职责 |
| 知识管理 | [docs/knowledge-management.md](docs/knowledge-management.md) | SQLite/Neo4j/YAML三层规范 |
| 工程工作流 | [docs/engineering-workflow.md](docs/engineering-workflow.md) | Loop/Graph Engineering |
| 翻译规范 | [docs/translation-guide.md](docs/translation-guide.md) | 藏汉对译玄奘体规范 |
| 多语对读 | [docs/multilingual-alignment.md](docs/multilingual-alignment.md) | 梵-于阗-藏-汉-满-英对读架构 |
| 校验框架 | [docs/verification-framework.md](docs/verification-framework.md) | 三级来源分级 + 验证状态机 |
| 可视化研究 | [docs/visualization-research.md](docs/visualization-research.md) | 系谱可视化方案分析 |
| 海云体系 | [docs/ref海云继梦法师_佛法修行体系研究.md](docs/ref海云继梦法师_佛法修行体系研究.md) | 外部参考文档（只读） |

## 技术栈

- **前端 Demo**: 纯 HTML/CSS/JS + Canvas + Leaflet (CDN), 6个独立HTML页面
- **数据库**: SQLite 3 (权威数据源) + Neo4j (图验证)
- **数据交换**: YAML/JSON → build.py 构建内嵌
- **ETL**: Python 3.12 (conda env: `hy_py312`)
- **部署**: 本地双击 → GitHub Pages

## ⚠️ 知识管理核心规则

**所有展示内容必须来源于结构化源文件或SQLite数据库，严禁硬编码在 build.py 或 JS 中。**

| Tab | 内容类型 | 权威源 | 交换格式 |
|-----|---------|--------|---------|
| 法脉传承 | 人物/边/地点 | SQLite persons表 | graph.json |
| 法脉传承 | 事件/动画/传播 | `data/events/*.yaml` | graph.json (扩展) |
| 华严文献 | 差异矩阵/术语 | SQLite chapters/glossary表 | gap.json |
| 华严文献 | 案例/观点/方法论 | `data/translation/gap_content.yaml` | gap.json (扩展) |
| 华严教行 | 修行体系 | `data/practice/*.yaml` | practice.json |
| 前沿对话 | 文献/论文 | `data/frontier/*.yaml` | frontier.json |
| 世主妙严 | 宇宙观/艺术 | `data/cosmology/*.yaml` | cosmology.json |

**新增内容流程**: ①SQLite INSERT/UPDATE 或 YAML → ②导出脚本 → ③build.py构建 → ④验证人数/边数 → ⑤提交

## 目录约定

```
huayan_collection/
├── web/demo/
│   ├── index.html              # 导航主页（构建产出）
│   ├── css/common.css          # 共享样式（构建产出）
│   ├── js/common.js            # 共享脚本（构建产出）
│   ├── tabs/                   # Tab页面（构建产出）
│   │   ├── lineage.html        # Tab1 法脉传承
│   │   ├── gap.html            # Tab2 华严文献
│   │   ├── jiaoxing.html       # Tab3 华严教行
│   │   ├── frontier.html       # Tab4 前沿对话
│   │   └── cosmology.html      # Tab5 世主妙严
│   ├── src/                    # 源文件（供build.py组装）
│   │   ├── data.js             # 数据占位 + 全局变量
│   │   ├── lineage.js          # Tab1 Canvas/Map/Select/Interact
│   │   ├── gap.js              # Tab2 汉藏差异
│   │   ├── jiaoxing.js         # Tab3 华严教行
│   │   ├── frontier.js         # Tab4 前沿对话
│   │   ├── cosmology.js        # Tab5 宇宙观
│   │   ├── init.js             # 初始化 + 评论系统 + GitHub认证
│   │   └── common.css/js       # 共享样式/脚本模板
│   ├── data/                   # 构建产出的JSON（build.py写入）
│   └── scripts/build.py        # 构建脚本
├── data/                       # 数据文件
│   ├── catalog/                # SQLite Schema + 种子SQL + huayan.db
│   ├── knowledge_graph/        # JSON（从SQLite导出）
│   ├── translation/            # YAML（差异矩阵·术语库·gap内容）
│   ├── practice/               # YAML（修行体系·禅观法要·讲法资源）
│   ├── frontier/               # YAML（跨界对话·文献综述）
│   ├── cosmology/              # YAML（华藏世界海·三界诸天·艺术珍品）
│   ├── events/                 # YAML（历史事件·动画节点·传播故事）
│   └── references/             # 参考文档
├── docs/                       # 项目文档
├── scripts/                    # 导出/验证/Neo4j脚本
└── src/                        # Python后端（待实现）
```

## 快速命令

```bash
conda activate hy_py312

# 数据导出: SQLite → JSON/YAML
python scripts/export_sqlite_to_json.py

# 图验证: SQLite → Neo4j + Cypher检查
python scripts/load_neo4j.py --verify

# 来源可靠性验证
python scripts/verify_sources.py

# 构建Demo (6个HTML + CSS + JS)
python web/demo/scripts/build.py

# 构建产物验证
python scripts/verify_demo.py
```
