# CLAUDE.md — 华严宗部文献与修行资料数字化梳理

## 项目概述

构建以华严宗为核心的佛法文献与修行资料数字化系统：
1. **多维知识图谱**：华严宗祖师/行者传承谱系、地理道场、经典关联（**95 人**，30 处地点/道场，**98 条**传承边，24 法系，174 条人物行迹，73 处文明疆域）
2. **多维格义**：梵-于阗-藏-汉-满-英多语对读 + 藏汉华严品目差异比对 (Toh44 45品 vs 汉文39品)
3. **华严宇宙观**：华藏世界海曼荼罗 + 三界诸天图

## Demo

**[web/demo/index.html](web/demo/index.html)** — 导航主页，链接到6个独立Tab页面
- Tab 1: **法脉传承**·时空长河 (Canvas时间轴 + 理论/修行图层 + 主地图 + 全球文明迷你地图 + 95节点动画 + 古地图模式 + 174条人物行迹)
- Tab 2: **华严文献**·汉藏差异 (子导航多页: 华严经学/以经证经/判教互判/华严祖师/专题研究 + 三语对读 + 50条术语 + 文本系谱)
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
| **李通玄长者** | [docs/李通玄长者_综合深度研究.md](docs/李通玄长者_综合深度研究.md) | 长者生平·著作·思想·与五祖关系·历史影响 |
| 华严二祖综合 | [docs/华严宗二祖智俨_综合深度研究.md](docs/华严宗二祖智俨_综合深度研究.md) | 智俨综合研究（合并二祖研究） |
| **梦参长老** | [docs/梦参老和尚_综合深度研究.md](docs/梦参老和尚_综合深度研究.md) | 梦参综合研究（1915-2017·华严/地藏·信源分级+存疑标注） |

## 技术栈

- **前端 Demo**: 纯 HTML/CSS/JS + Canvas + Leaflet (CDN), 6个独立HTML页面
- **数据库**: SQLite 3 (权威数据源) + Neo4j (图验证)
- **数据交换**: YAML/JSON → build.py 构建内嵌
- **ETL**: Python 3.12 (conda env: `hy_py312`)
- **部署**: 本地双击 → GitHub Pages

## ⚠️ 工程核心原则

0. **考证优先（Verification First）** — ⭐内容与信息依据的考证、确认永远是**最前提、最重要**的事，优先于一切功能与进度：一切数据、结论、名号、数字、参次、年代、地点必须先经一手典籍（CBETA/T84000/原始文献）或权威来源对勘；一时无法确认者必须明确标注〔待核〕/〔存疑〕并如实说明，严禁编造、猜测或以"约第XX参"式占位充数。宁可内容少而可靠，不可多而失实。
1. **知识图谱驱动** — 所有开发、管理、维护以结构化知识图谱（SQLite + YAML）为核心，不依赖手工编码的数据

## ⚠️ 内容采集与编务总则（七条，后续所有新增内容必须遵守）

0. **一口优先·还原分级真实性** — 凡采用的信息来源，**尽可能使用第一手材料**（CBETA/T84000/原始文献/一手档案与采访）；无法直取一手者用可靠二手并据实注明。凡**存疑者必须标明〔待核〕/〔存疑〕**；凡**线索性、局部、信息不充分者必须标明〔线索〕/〔待补〕**，如实交代信息边界，严禁把半成品当作定论。
1. **中英必配·多语酌情** — **凡新增内容，一律同时提供中文与英文各一版本**（映照全站 `.en-line` 中英对照机制）；其他语言（梵/藏/于阗/满/日/韩…）视具体情况酌情使用，不勉强、不硬凑。凡暂无把握之译名照「多语 EN 翻译原则」明示标注。
2. **多译本并存·考据成一** — 凡同一内容存在**多个翻译/版本**（如异译、异本、品目卷数分歧、译名异写），尽可能**梳理清楚并存版本、说明取舍依据与考据出处**，不得只取其一而隐去其余、更不得把某一家译法冒充唯一标准；多版本难以裁决时保留并行并注〔并存/待考〕。
3. **严禁假信息** — **千万避免使用假信息**：不编造年代/地点/名号/引文/数字/参次，不虚构出处，不把口耳相传或二手转述冒充原典；凡来源不明或无法核实者，宁可留白并标注，也不以虚构填充（与考证优先原则互证）。
4. **穷尽采集·分层落地** — **尽可能穷尽信息**；当信息量过大时，先**收集与梳理信息来源、登记入后续计划（docs/next-phase-plan.md）**，分批次慢速提取与实现，不因求全而牺牲可靠性，也不因求快而遗漏来源。
5. **进度留痕·计划滚动** — **每完成一个任务，记得更新进度与下一步计划**：在 `docs/next-phase-plan.md`（及必要的 `docs/*.md`/README）如实登记已完成项、构建/校验结果、遗留问题与**下一批待办梯队**，使项目状态可持续交接、不因会话结束而丢失上下文；新登记内容同时遵守 0-4 及各原则。
6. **边界自知·局限留档** — **清楚自己的局限在哪里，主动暴露信息与方法论的边界**：凡**采集不到、采集不全、有待进一步考察、或受工具/语种/一手资料可得性所限无法确认**之处，一律如实登记（标〔待核〕/〔线索〕/〔无法获取〕，并注明**为何受限**：如史料散佚、语种不通、一手文献未见、核对工具缺失等），纳入 `docs/next-phase-plan.md` 的待考梯队；既不夸大已掌握的信息，也不隐瞒盲区——这些记录即为后续**自我完善与进化的路线图**，使后续工作能针对性地补采、补考、补译。

> 注：以上与「考证优先」（工程核心原则 0）及「多语 EN 翻译原则」互证互补；英文传导、译名规范具体仍循「多语 EN 翻译原则」七条执行。
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
| 华严文献 | 经学/对读/祖师/判教 | `data/translation/avatamsaka_studies.yaml` `intertextual_canon.yaml` `huayan_masters.yaml` `panjiao_hupan.yaml` | gap.json (扩展) |
| 华严文献 | 专题研究 (整篇docs/*.md注入) | `data/translation/topic_studies.yaml` + `docs/佛门真伪问题_综合深度研究.md` 等 | gap.json (扩展: topic_studies) |
| 全站 | **独立文章页** (每篇完整文章独立URL) | `data/translation/standalone_articles.yaml` (sources: topic_studies+huayan_masters 自动展开; others 显式登记整篇 docs/*.md) | `articles/<id>.html` (build.py生成, 全Tab页内嵌 `var ARTICLES` 提供入口条) |
| 华严教行 | 修行体系 | `data/practice/*.yaml` | practice.json |
| 前沿对话 | 文献/论文 | `data/frontier/*.yaml` | frontier.json |
| 世主妙严 | 宇宙观/艺术 | `data/cosmology/*.yaml` | cosmology.json |

**新增内容流程**: ①SQLite INSERT/UPDATE 或 YAML → ②导出脚本 → ③build.py构建 → ④验证人数/边数 → ⑤提交

## ⚠️ 多语 EN 翻译原则（与全文校对结合，重实质不逐字）

本项目的 EN 对照（全站 `*_en` 字段）遵循以下原则，作为后续所有翻译批次的统一约束：

0. **翻译与校对结合、不偏废** — 翻译产出必须纳入完整质量门禁：术语表一致性、教理准确性、考证优先（〔待核〕/〔存疑〕标注、严禁编造史实/观点）、结构/引号安全。翻译≠成稿，一律经主编全文审查后再 render/commit。
1. **重实质、不逐字** — 多语言之间的对应，注重的是**实质内容的对应和准确**（义·理·境的对等），不须拘泥于逐字翻译。意译优先于直译，只要名相所指与教理判断不偏离即可；译名仍循全站固定术语表保持一致。
2. **考证与来源分级** — 一切 EN 内容不得超出中文正文范围，不得新增文件里没有的年代/地点/史实/观点；一时无法确认者标〔待核〕。引用文献/语录有英文原文者照用原题原句；祖师/法师语录正文保持中文原文（zh-only），EN 用最精到阐释转述。
3. **固定术语表** — 全站统一译法（五种姓=five lineages/gotras、三性三无性、八识=eight consciousnesses、阿赖耶识=ālayavijñāna、十玄=ten mysterious gates、华严三昧=Huayan samādhi、五教止观=five teachings of calming and contemplation、即身成佛、三密、法界=dharmadhātu……详见会话里程碑）。人名照拼音/梵文通行拼写（玄奘=Xuanzang、法藏=Fazang、杜顺=Dushun、海云继梦=Haiyun Jihong……）。
4. **EN 渲染约定** — EN 块一律 `.en-line` 随全局显隐（默认中英对照）；正文级 EN 块前缀 📖；标题/主题副行 `title_en`、intro 用 `intro_en`、正文用 `en_body`；引用文献英文原文照用。
5. **YAML 转义纪律** — ①单引号串内 `\'` 非法，用 `''`；②单引号串内撇号（Buddha's）会提前闭合——用双引号串或 `''`；③双引号串内嵌双引号须转义；④双引号包裹含中文「」的字符串会被拆坏——用单引号或 `''`；⑤`en_body`/长 EN 一律用 `|` 块标量（4空格 key / 6空格内容），**禁止单引号包裹英文长文本**；`title_en` 含冒号或撇号必须双引号包裹。
6. **翻译 API 仅作辅助** — 以文本质量为优先对象，在线翻译（如 GLM-4-Flash 免费档）仅作上量初稿辅助、可插拔（无 key 自动回退子代理著写），质量门禁与主编审查始终保留、不因接入 API 而放松。详见 `docs/engineering-workflow.md`「多语 EN 翻译管线」。
7. **正式用词·不硬翻·不幻觉·无对应即明示** — EN 名相一律采用**学界与佛界通行的正式用词/固定术语表**（梵文转写优先，如 śamatha、vipaśyanā、cittamātra、dharmadhātu；专名循全站统一译法）。严禁「字面硬翻」与「自造译名」——不得因中文某词没有思路而凭空组合不存在的英译（例如将经名拆字硬拼），也不得在 EN 中臆造文件里没有的年代/地点/史实/观点。凡学界/佛界**无通行对应译名或暂无把握者**，必须明示标注（〔待核〕/〔无通行英译〕＋保留原名或给出带「本文暂译」的说明），而非硬译充数。

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
│   ├── articles/               # 独立文章页（构建产出, 每篇一个URL）
│   │   ├── index.html          # 独立文章目录
│   │   └── <id>.html           # 如 zhenwei / master-fazang / mimi
│   ├── src/                    # 源文件（供build.py组装）
│   │   ├── data.js             # 数据占位 + 全局变量
│   │   ├── lineage.js          # Tab1 Canvas/Map/Select/Interact
│   │   ├── gap.js              # Tab2 汉藏差异
│   │   ├── jiaoxing.js         # Tab3 华严教行
│   │   ├── frontier.js         # Tab4 前沿对话
│   │   ├── cosmology.js        # Tab5 宇宙观
│   │   ├── article.js          # 独立文章页渲染器
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
