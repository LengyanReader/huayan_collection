# CLAUDE.md — 华严宗部文献与修行资料数字化梳理

## 项目概述

构建以华严宗为核心的佛法文献与修行资料数字化系统：
1. **多维知识图谱**：华严宗祖师/行者传承谱系、地理道场、经典关联（**95 人**，30 处地点/道场，**98 条**传承边，24 法系，174 条人物行迹，73 处文明疆域）
2. **多维格义**：梵-于阗-藏-汉-满-英多语对读 + 藏汉华严品目差异比对 (Toh44 45品 vs 汉文39品)
3. **华严宇宙观**：华藏世界海曼荼罗 + 三界诸天图

## Demo

**[web/demo/index.html](web/demo/index.html)** — 导航主页，链接到6个独立Tab页面
- Tab 1: **法脉传承**·时空长河 (Canvas时间轴 + 理论/修行图层 + 主地图 + 全球文明迷你地图 + 95节点动画 + 古地图模式 + 174条人物行迹)
- Tab 2: **华严文献**·汉藏差异 (子导航四页 + 三语对读 + 50条术语 + 文本系谱)
- Tab 3: **华严教行** (子导航四页·修行体系/禅观法要/实修心要/讲法资源 + YouTube集成)
- Tab 4: **前沿对话** (AI/计算现象学/神经科学/心灵哲学 + 文献综述)
- Tab 5: **世主妙严** (华藏世界海曼荼罗 + 三界诸天图 + 艺术珍品 + 梵呗)
- Tab 6: **灵性仁本**·澄明永续 (灵性经济学/人本经济学/修行传统与永续/本土知识体系)

## 知识管理架构（三层数据栈）

```
L1: SQLite (权威数据源)  →  L2: db_reader.py (数据服务层)  →  L3: build.py → HTML
```

- **SQLite** (`data/catalog/huayan.db`): persons, texts, chapters, locations, glossary, lineages, lineage_edges + FTS5全文检索
- **db_reader.py** (`scripts/db_reader.py`): 从SQLite读取，输出graph.json兼容格式，供build.py消费
- **YAML/JSON**: 非图谱数据（修行体系/宇宙观/前沿对话等）仍以YAML为权威源
- **策展**: 直接操作SQLite (`scripts/import_all_to_sqlite.py` 多源合并导入)

数据流: JSON/YAML源文件 → `import_all_to_sqlite.py` → SQLite → `db_reader.py` → `build.py` → HTML

详见 [docs/knowledge-management.md](docs/knowledge-management.md)

## 核心文档索引

| 文档 | 路径 | 说明 |
|------|------|------|
| 后续计划 | [docs/next-phase-plan.md](docs/next-phase-plan.md) | v2.0重构 P0-P4 路线图 |
| 架构设计 | [docs/architecture.md](docs/architecture.md) | 三层数据栈、数据模型、模块职责 |
| 知识管理 | [docs/knowledge-management.md](docs/knowledge-management.md) | SQLite/Neo4j/YAML三层规范 |
| **参考文献管理** | [docs/reference-management.md](docs/reference-management.md) | 文献知识库维护规范 (新增) |
| 工程工作流 | [docs/engineering-workflow.md](docs/engineering-workflow.md) | Loop/Graph Engineering |
| 翻译规范 | [docs/translation-guide.md](docs/translation-guide.md) | 藏汉对译玄奘体规范 |
| 多语对读 | [docs/multilingual-alignment.md](docs/multilingual-alignment.md) | 梵-于阗-藏-汉-满-英对读架构 |
| 校验框架 | [docs/verification-framework.md](docs/verification-framework.md) | 三级来源分级 + 验证状态机 |
| 可视化研究 | [docs/visualization-research.md](docs/visualization-research.md) | 系谱可视化方案分析 |
| 海云体系 | [docs/ref海云继梦法师_佛法修行体系研究.md](docs/ref海云继梦法师_佛法修行体系研究.md) | 外部参考文档（只读） |
| **文殊普贤信仰** | [docs/文殊普贤信仰专题研究.md](docs/文殊普贤信仰专题研究.md) | 二圣信仰专题（梵藏汉英·艺术·修行） |
| **善财五十三参** | [docs/善财五十三参深度研究.md](docs/善财五十三参深度研究.md) | 五十三参版本考·地理考·心地境界·象征结构 |
| **李通玄长者** | [docs/李通玄长者华严专题研究.md](docs/李通玄长者华严专题研究.md) | 长者生平·著作·思想·与五祖关系·历史影响 |
| 华严二祖综合 | [docs/华严宗二祖智俨_综合深度研究.md](docs/华严宗二祖智俨_综合深度研究.md) | 智俨综合研究（合并二祖研究） |

## 技术栈

- **前端 Demo**: 纯 HTML/CSS/JS + Canvas + Leaflet (CDN), 6个独立HTML页面
- **数据库**: SQLite 3 (权威数据源) + Neo4j (图验证)
- **数据交换**: YAML/JSON → build.py 构建内嵌
- **ETL**: Python 3.12 (conda env: `hy_py312`)
- **部署**: 本地双击 → GitHub Pages

## ⚠️ 工程核心原则

1. **知识图谱驱动** — 所有开发、管理、维护以结构化知识图谱（SQLite + YAML）为核心，不依赖手工编码的数据
2. **源头治理** — 问题在数据源头（SQLite/YAML）解决，不下游修补
3. **灵活优先** — 架构设计以可扩展性为第一优先级，新内容 = 新数据行，不改代码
4. **杜绝硬编码** — 数据进 SQLite/YAML → build.py 读取 → 前端渲染，禁止在 JS/HTML/Python 中写死任何内容

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
│   ├── init_db.py              # SQLite初始化
│   ├── import_all_to_sqlite.py # 多源JSON→SQLite合并导入
│   ├── db_reader.py            # SQLite→JSON数据服务层
│   ├── export_sqlite_to_json.py # 导入/导出/验证
│   ├── test_pipeline.py        # 全链路数据一致性测试
│   ├── verify_demo.py          # 构建产物验证
│   ├── verify_sources.py       # 来源可靠性验证
│   └── load_neo4j.py           # Neo4j加载+验证
└── src/                        # Python后端（待实现）
```

## 快速命令

```bash
# 初始化/导入数据
python scripts/init_db.py                    # 初始化空数据库
python scripts/import_all_to_sqlite.py       # 多源JSON→SQLite导入
python scripts/export_sqlite_to_json.py --verify  # 数据完整性验证

# 图验证: SQLite → Neo4j + Cypher检查
python scripts/load_neo4j.py --verify-sqlite  # SQLite直接图验证（无需Neo4j服务器）
python scripts/load_neo4j.py --generate       # 导出Cypher脚本
python scripts/load_neo4j.py --verify         # Neo4j在线验证（需服务器）

# 来源可靠性验证
python scripts/verify_sources.py

# 全链路测试
python scripts/test_pipeline.py              # 数据一致性测试

# 构建Demo (6个HTML + CSS + JS)
python web/demo/scripts/build.py

# 构建产物验证
python scripts/verify_demo.py
```
