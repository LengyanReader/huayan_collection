# 🧭 Harness — 华严集 · 智能体工作法总纲

> **这是什么**：本目录把「让编码智能体（agent）在**跨会话、长时间**里稳定推进本项目」所需的**方法、技能、原则、工具**集中成一处，作为整个项目的 *harness*（智能体运行的"驾驶舱 / 线束"）。
> **它不是什么**：它**不重复**权威内容——研究正文、编务原则、数据规范仍以 `CLAUDE.md`、`docs/*.md`、`data/**` 为准。本目录只做**命名、连接、调度与扩展**：告诉后续任意一次会话"该用什么、去哪找、按什么门禁验收"。
> **可扩展**：每类能力一个文件；新增方法/技能/工具/工作流时，在对应文件追加一行卡片，并在本 README 索引登记即可（见文末〈如何扩展〉）。

落地日期：2026-09-23 · 依据 Anthropic 两篇工程长文《Effective harnesses for long-running agents》《Effective context engineering for AI agents》与本项目既有资产综合整理（来源见 [`sources.md`](sources.md)）。

---

## 一、核心心智：本项目已经是一个 harness

长时间运行 agent 的根本困难是：**每个新会话开始时"失忆"**，上下文窗口有限且会"上下文腐坏"（context rot）。业界解法与本项目的既有资产几乎一一对应——本 harness 的第一价值，就是**把这层对应显式写出来**，让每次会话都刻意沿用：

| 长时程 agent 通用机制（Anthropic） | 本项目的对应资产（权威源） | harness 内说明 |
|---|---|---|
| 前置入上下文的"项目记忆"（CLAUDE.md 直投） | [`CLAUDE.md`](../CLAUDE.md)：概述·进度·八条编务总则·多语EN七原则·工程核心原则 | [`principles.md`](principles.md) §1 |
| `claude-progress.txt` 进度流水 + git 历史 | [`docs/工程治理/next-phase-plan.md`](../docs/工程治理/next-phase-plan.md)（滚动批次登记）+ git | [`principles.md`](principles.md) §2 |
| `feature_list.json`：结构化待办、只改 `passes` 字段 | `data/evolution/evolution_state.yaml`（registry 台账）| [`principles.md`](principles.md) §3 |
| 结构化记笔记 / agentic memory（NOTES.md、to-do、memory 工具） | `data/evolution/evolution_log.yaml`（**只追加**台账）+ 长期记忆库 | [`principles.md`](principles.md) §3 |
| "自验证后才算完成" + 测试工具（浏览器自动化/curl） | `verify_demo.py` / `test_pipeline.py` / `verify_sources.py` + headless Chrome CDP | [`tools.md`](tools.md) §验证关卡 |
| 初始器 agent + 逐特性增量推进（一次只做一件、留净态） | 会话收尾协议（跑 `make evolve`、更新计划、提交前全绿） | [`principles.md`](principles.md) §4 |
| 子代理架构（主 agent 协调、子 agent 返回浓缩结论） | `Agent` 工具（Debug / CodeReview / Browser / Search 子代理）| [`tools.md`](tools.md) §子代理 |
| 压缩（compaction）：接近窗口上限即摘要重启 | 会话续接时的自动 compaction + 本目录作为"外部记忆" | [`principles.md`](principles.md) §5 |

> 一句话：**`CLAUDE.md` 是宪法，`harness/rules.md` 是规矩总索引，`harness/coverage-map.md` 是“内容×代码·开发×维护”主轴地图，`harness/concerns.md` 是“别漏了哪些面”的七面正交清单，`next-phase-plan.md` 是心跳，`self_evolve` 是免疫与记忆，`verify_*` 是验收闸——本 `harness/` 把它们串成闭环。**（主轴定位看 coverage-map · 守则看 rules · 防漏看 concerns · 权利边界看 compliance）

---

## 二、目录结构

```
harness/
├── README.md              ← 本文件：总纲·映射·索引·如何扩展
├── coverage-map.md        ← 【骨架】内容/代码 × 开发/维护 的 2×2 治理地图 + 缺口登记
├── concerns.md            ← 【正交关注面】元治理·协作·行文·合规·成本·可发现性·语义互操作（七面×四格）
├── compliance.md         ← 【权利登记面】维护者立场·决策·各源许可·残留风险 R1–R8（合规向）
├── rules.md               ← 【规矩单一索引】历次原则/规矩/踩坑硬约束的一屏汇总（连接不重复）
├── principles.md          ← Agentic 工程方法与原则（上下文工程 + 长时程 harness）
├── skills.md              ← 技能目录：已安装 / 可安装 / 安装法 / 任务映射
├── tools.md               ← 工具清单：验证关卡脚本 / 子代理 / MCP / CLI / 环境约束
├── sources.md             ← 参考来源与检索记录 + 待扩充清单（backlog）
└── workflows/             ← 按工作流编排"技能+工具+门禁"的可复用配方（9 条）
    ├── data-pipeline.md      数据管线/知识图谱策展（SQLite→build→verify 核心循环）
    ├── web-ui.md             前端·数据驱动导航与渲染（navigation.yaml/双源渲染器/双语链）
    ├── translation.md         翻译（多语EN·校对·术语·渲染安全）
    ├── information-assurance.md 信息保证（考证优先·来源分级·待核边界）
    ├── academic-standards.md  学术规范（引用可点·IEEE/脚注·反伪造）
    ├── bibliography.md        分级参考文献轨/P 轨（三级标注+CBETA 深链+SIGLA 逐条核证·零伪造）
    ├── self-evolution.md      自我演化（感知→解释→行动→学习 闭环）
    ├── verification.md        验证/测试（三道闸 + 交互实测·make verify-all）
    └── deploy.md              部署/仓库治理（GitHub Pages 源=main 根·CRLF/LF·CDN）
```

---

## 三、八条工作流一览（详见 `workflows/`）

> 数据管线/前端为工程量最大的**工程面**；翻译/信息/学术/演化偏**编辑研究质控**；验证/部署为**横切面**。

| 工作流 | 何时用 | 关键技能 | 关键工具/门禁 | 权威原则源 |
|---|---|---|---|---|
| **数据管线/图谱** | 新增/订正人物·边·地点·经·品目·术语，跑 import→build→verify | `research` | `import_all_to_sqlite`·`export_sqlite_to_json`·`db_reader`·`test_pipeline`(95/98/30)·`load_neo4j` | `CLAUDE.md`〈三层数据栈〉〈权威源表〉+ `docs/工程治理/knowledge-management.md` |
| **前端/导航渲染** | 改侧栏/独立文章/中英渲染/视图切换/可视化 | `frontend-design` | `navigation.yaml`+`render_sidebar`·`standalone_articles`·双源`WIZ_LIB_RENDER`↔`renderWizLibrary`·`node --check`·CDP/dump-dom | memory〈Interactive State Verification〉+ L.㉝/㊾ 系列 |
| **翻译** | 新增/订正任何 `*_en` / 多语对读字段 | `academic-research-writer`、`citation-verification` | `_markEnBlocks`/`.en-line` 渲染、`audit_bilingual`、`verify_demo`、YAML 转义纪律 | `CLAUDE.md`〈多语 EN 翻译原则〉七条 |
| **信息保证** | 任何史实/名号/年代/数字/出处落库前 | `research`（一手源核查）、`citation-verification` | `verify_sources.py`、`backfill_*`、`extract/ocr_hy_refs`、〔待核〕标记扫描 | `CLAUDE.md`〈工程核心原则 0·考证优先〉+〈编务总则 0/3/6〉 |
| **学术规范** | 撰写/审校研究文档、参考文献 | `academic-research-writer`、`citation-verification` | 引用可点 `[text](url)` + `_dynMD`、GB/T 15835 数字、图表编号 | `CLAUDE.md`〈编务总则 7·引用可点〉+ `docs/工程治理/reference-management.md` |
| **分级文献轨/P 轨** | 把某 `docs/*.md` 参考文献规范化为 `[A/B/C]`+CBETA 深链+SIGLA 核证 | `citation-verification`、`research` | CBETA 反查、`verify_demo`、临时 `scripts/*_tmp.py`、`bib(P-track/<X>):` 提交 | `docs/工程治理/分级参考文献_模板.md` + `workflows/bibliography.md` |
| **自我演化** | 每次会话收尾 | （本目录即其接口文档）| `make evolve` / `--apply` / `--ledger`、`--record` | `docs/工程治理/self-evolution.md` |
| **验证/测试** | 任何改动“是否算完成”的裁决 | （内置）| `make verify-all`、headless Chrome `--dump-dom`/CDP、node --check | `harness/workflows/verification.md` + memory〈Interactive State Verification〉 |
| **部署/仓库治理** | 发布产物到 Pages、换行/缓存/分支决策 | （内置）| `make demo` / `demo-deploy`（已修暂存 web/demo/）、线上 dump-dom 核验 | `docs/工程治理/next-phase-plan.md`〈部署与仓库治理〉既定事实 |

---

## 四、任一会话的标准节拍（Session Protocol）

> 直接对标 Anthropic "getting up to speed"：新会话先用最小上下文找回状态，再增量做**一件事**，收尾留**净态 + 痕迹**。

1. **定向（orient）**：`pwd` → 读本 `README.md` → 读 `CLAUDE.md`〈当前进度·下一步〉→ 读 `docs/工程治理/next-phase-plan.md` 顶部与 `docs/evolution/next_actions.md` 高优先项 → `git log --oneline -15`。
2. **验基线（baseline check）**：必要时先跑一次构建/验证，确认工作区处于"可合并净态"；若有破损先修，不要带着破损做新功能（zero-risk-first）。
3. **选一件事（one feature）**：从待办台账选**最高优先级的单一事项**（避免一次做太多导致中途中断、把半成品留给下一会话）。
4. **做+自验证（verify before done）**：改数据源（SQLite/YAML）而非下游 → `build` → `verify_demo` + `test_pipeline`（+ 涉内容则 `verify_sources`）→ 交互态用 headless Chrome/CDP 实测。**验证未全绿不得声称完成、不得标 `passes:true`。**
5. **留痕（leave artifacts）**：更新 `docs/工程治理/next-phase-plan.md`；跑 `make evolve`；必要时 `self_evolve --record --actor agent` 补记带外动作；沉淀可复用经验到长期记忆。
6. **净态提交（clean state）**：如经用户同意，`git commit` 描述性信息（+ 更新进度文件），使下一位"轮值工程师"可无摩擦接续。

---

## 五、如何扩展本 harness

- **新技能**：装好后在 [`skills.md`](skills.md) 追加一张卡（名称 / 触发 / 对应工作流 / 安装命令）。
- **新工具/脚本**：在 [`tools.md`](tools.md) 追加条目；若成为验收闸，同步进〈验证关卡〉与本 README 第三节。
- **新工作流**（如"图谱策展""多语满/藏""部署/CI"）：在 `workflows/` 新建 `<name>.md`，套用现有四段式（何时用 → 步骤配方 → 技能/工具 → 门禁 → 常见坑），并在本 README 第三节加一行。
- **新方法论**：进 [`principles.md`](principles.md)，并在 [`sources.md`](sources.md) 登记出处链接。
- **一致性铁律**：本目录所有文件遵守〈考证优先 / 严禁假信息 / 边界自知〉——引用外部方法一律给可点来源；本项目未落实者标〔待落地〕，不假装已具备。

> 维护者：编码智能体（agent）与人工共同滚动维护；每次新增能力都应让"下一个失忆的会话"仅凭本目录即可上手。

## 深度研究（Deep Research）规范

### 原则（深研四要）
- **全面性（Comprehensive）**：穷尽相关一手与权威二手，涵盖时间轴（源起→发展→定型）、人物脉络、教义脉络、实践脉络，避免片面选取。
- **深入性（Thorough）**：不止列举事实，须梳理脉络、前提、张力、分歧与论证逻辑，追溯到关键论点的最初出处。
- **准确性（Accurate）**：一切断言须有可溯出处（CBETA/T84000/原典/权威著录/一手档案）。无法确认者一律标注〔待核〕/〔存疑〕/〔线索〕。
- **可靠性（Reliable）**：坚持负面证据（反例/相反说）、多源三角验证、版本并存与取舍依据，不编造、不臆补、不把推测升格为结论。

### 源头分级（T0–T3）
- **T0**：原始一手（经论原文、原始讲记手稿/定本、一次性档案、CBETA/T84000 原始段落）。优先级最高。
- **T1**：权威校注/定本注疏（一手诠释的权威定本，如澄观《疏》/法藏《探玄记》/李通玄《合论》等经校勘妥当者）。
- **T2**：严谨学术（二手研究，具出处、方法清晰、能溯源者）。
- **T3**：可靠工具/资料（百科、机构官网、索引）仅作线索，不直接充作关键结论，须回溯一手。

### 深研方法论（七步）
1. **界定问题**：明确研究问题、边界与不研究范围（What/Not What）。
2. **全域检索**：站内（SQLite/YAML/docs/huayanhai/data）+ 外部权威（CBETA/T84000/DILA/BDRC/汉佛典籍/机构官网）并登记清单。
3. **溯源与清洗**：逐条溯至最初出处，去除转述层累，区分「引述」「转述」「评述」。
4. **三角验证**：至少两种不同类型来源相互印证（原典 vs 注疏 vs 讲记/学术），矛盾处如实记录。
5. **结构化梳理**：按时间轴（演进）、脉络（传承）、结构（体系要素）建构框架，先框架后细节。
6. **证据链固化**：每一关键论断附 ile_path:line_range 或具体经号/卷页/URL，建立可复核路径。
7. **质量门禁**：负面证据清单、未核清单〔待核〕、存疑清单〔存疑〕、假信息零容忍复核。

### 不变量（深研铁律）
- **宁可留白，不以未获底本立证**（L.107/L.108 已固化）。
- **〔未竟〕/〔待核〕/〔存疑〕/〔线索〕必须标注，不可省略**。
- **区分事实 vs 判断**：正文事实用〔实测〕，诠释用〔本文判断〕并注明取舍依据。
- **版本并存**：有分歧者列出诸说→取舍依据→结论（不隐去异说）。

## 深度研究（Deep Research）补充：海云体系专项

**本专项已于 L.109 立「实证库 ＋ 双门禁 ＋ 反向验证」之常设工程形态**，下列各条为其实践所得之规范**与已订正之旧说**（凡与旧说冲突者，以本节为准）。

### 一、证据规范

- **自述优先**：凡论及「摸索」「曲折」「错误」「助缘」「边修边讲」「边体会」「边理顺」「边走边拼」等，**只收录法师自述原话**（A 类），不得用他人综述替代。
- **调整修订追踪**：留意「前面讲的」「后来讲」「以前」「现在讲」「调整」「修订」「修改」等表述，追踪法师对说法用词的不断修订过程。
- **过程性重于结论**：「定型」采用审慎用语（「趋于定型」「大体理顺」「基本能走通」），避免「最终完成」「完全定型」。**且此审慎非编辑姿态，而是依其自用判准**——法师自陈定型之标志限于「入口处架构完毕·出口处清楚·已建立标准作业流程」，并随即声明「剩下的，是各位要努力了」。
- **溯源不可省**：每条关键论断须给 `file_path:line`，保留上下文。
- **二手仅线索**：`docs/hy_refs/pfhy.md` 等二手综述仅作线索，采纳前须回溯 `docs/huayanhai/` 原文验证。
- **三分界限**：对「复原／重构／建构」逐要素比勘祖典（T1733/T1735/T1736/T1739/X0223）。

### 二、三条已订正之旧说（**旧说已废，勿再沿用**）

1. **「组织性用语须自述」——此判准已废弃**。原以「拼图／贯通／串起／打通」等词之出现为归入「重构」之判准；实证其泛用率极高（人口会议、念珠释义、气脉打通乃至**他人悼文**皆命中），据词判义必致谬误。**改以法师自陈之动作判准**（见 `§5.0` 七至八项动作表）。
2. **「曲折」不得代拟为「悔过」**。全库检索：法师**未以「犯过错误／走过弯路」自述失手**（N1）；其自陈之失以**自嘲与病名**出之（「这个笨蛋，就那么简单的事也不会」「不是没资料，你不会用那些资料」）。故禁用「悔过」「认错」一类词，改依其原辞。
3. **「助缘」是分析语汇，非法师原词**（N2）。其自用词为「因缘」，且所举皆具名（梦参、钦因、德林、惹扎西牟尼、牟尼吉、三百余同修）。本文以「助缘」行文时**须标明系归纳**。

### 三、检索与清点之方法论（**血泪教训，务须遵循**）

- **词形变体须一并检索**：只检「拼图」会漏「拼盘」——S1 之「法界大拼盘」即因此一度未计。**此类清点须连变体一并检索**，否则计数偏低。
- **否定性记录须登记「否定之根据」**：N1/N2 使本文**不代拟**法师未曾说过之语，与正面证据价值相埒。
- **同源多版只据一版**：同一讲记有多版初稿／听录／初校者，本文**只据一版引之**，其余仅作异文互校并注明，**不合并异文以充一权威文本**（编务总则第 2 条）。
- **同词须分语义域清点**：同一「拼图」在法师口中兼为赞美自陈与警戒（L2 只积材而不定／L4 硬拼乱黏），**不可单取赞美面**。

### 四、常设门禁（L.109 立，已接入 `scripts/verify_demo.py`）

| 门禁 | 作用 | 反向验证 |
|---|---|---|
| `scripts/verify_haiyun_evidence.py` | 实证库逐条回源：行号＋字串双向、信度值域、台账对账、id 唯一连号、T0 限栈 | ✅ 8 项变异 |
| `scripts/verify_haiyun_draft.py` | 草稿↔实证库编号一致、无伪断言回潮、无未入库之引文 | ✅ 3 项变异 |
| `scripts/_verify_haiyun_reverse.py` | 破坏性变异确认上述断言**真能捕获**（11/11） | — |
| `scripts/build_haiyun_appendix.py` | 附录二**自实证库直出**，杜绝手工转录笔误 | — |

**证据库**：`data/research/haiyun_practice_system_evidence.yaml`（`strong`／`medium`／`limit` ＋ `negative_findings` ＋ `meta.counts` 台账）。

**引文体例**：每条 `quote` 必为底本**同一行内连续**字串，跨行省略者**拆为独立条目**；登记为单行者须**精确命中该行**（区间才容差 ±2）。

**首轮盲区六项（已修，记此以勿再犯）**：①行号容差窗使偏移 1–2 行通过；②分组下限过松，删条目仍通过；③信度无取值域，可任意书写；④否定性记录无下限；⑤条目 id 可重号；⑥台账与实数不对账。**门禁自身之缺陷亦须如实修正，不可迁就**（L.106／L.107 之原则，L.109 沿用）。

### 五、T1 比勘门禁（L.109 立·祖典原文级，已接入 `scripts/verify_demo.py`）

| 门禁 | 作用 | 反向验证 |
|---|---|---|
| `scripts/t1_search.py` | T1 六本**行内＋跨行**检索（NFKC＋RAD 双层归一）；`--list` 兼列各书**使用限制** | — |
| `scripts/t1_quote.py --check` | 引文**逐字回源**（按 `底本＋行号＋归一字位`），**不手录** | ✅ 改引文一字／改行号 |
| `scripts/verify_t1_bikan.py` | 台账对账**六项**：total／by_sec 对账、id 连号、字段完备、否定记录**下限 4**、结论**覆盖五节**、引用不悬空 | ✅ 6 项变异 |
| `scripts/_verify_t1_reverse.py` | 破坏性变异确认断言**真能捕获**（8/8） | — |
| `scripts/_t1_gen_quotes.py`／`_t1_build_lib.py` | 证据库构建器（抽取规格存库，可重跑） | — |

**T1 证据库**：`data/research/t1_bikan_evidence.yaml`（**27 条** C01–C27 ＋ **4 条**否定记录 N5–N8 ＋ **5 节**结论）。

**〔分源·铁律〕T0 ＝ 法师原话（`haiyun_practice_system_evidence.yaml`）；T1 ＝ 祖典原文（本库）。二者**分源立册，不可互相顶替**——T1 之引文**不得**充作法师原话。`verify_haiyun_draft.py` 之 G 项即为此设（正文若「—— 法师…」后紧跟 `〔Cxx〕` 即判失败）。

**〔⚠️ 工程陷阱·务必守〕不得以 shell 重定向取 Python 之 stdout 写引文文件。** PowerShell／cmd 会按 locale（cp1252）重编码，中文与繁体逐字成乱码（实测「初列四諦…」→「σê¥σêùσ¢¢…」），而写在 `.py` 源码内之 key／sec 不受影响——于是**半本文件坏、半本完好，肉眼极易漏过**。故 `_t1_gen_quotes.py` **由 Python 自己写文件**（显式 UTF-8＋`newline`），并**写后回读自校**（不一致即失败，且以「四諦／解脫／普賢／威儀」四串探测，不靠肉眼）。构建链恒为：`python scripts/_t1_gen_quotes.py` → `python scripts/_t1_build_lib.py`。

**〔反向验证·须指派门禁〕** T1 两门**职责分离**（quote 只管引文逐字；bikan 只管台账与结构），故反向脚本须**逐项指派「应捕获此变异之门禁」**；若强求「两道皆须失败」，等于把「职责分离」误判为「门禁薄弱」——此为验证脚本自身之缺陷。另：判「捕获」不可用「失配」二字（**「失配 0 条」亦含此字**，恒假命中），当以 `rc≠0` 且输出**无** `ALL CHECKS PASSED` 为准。

**T1 底本之使用限制（比勘之先天边界，写结论时须随之自限）**：
- T1735 系**截断本**（止于入法界品中段）——凡涉后续诸品之澄观说**不可**据本库断言。
- T1732／T1733 为**会本节录**（5,539／22,762 行，远小于全帙）——故「法藏二书『十玄』全 0 见」**可能系底本不全**，须标〔存疑〕。
- X0223 为**无标点**底本（会本式）——其引文**不加标点**；T1732/T1733/T1735/T1736 有句读，其引文含「。」。**此差异如实保留，不代 X0223 补标点（补则失真）**。

### 六、第四层·待校语料门禁（L.111 立·《九九華嚴》OCR 稿，已接入 `scripts/verify_demo.py`）

**〔四层分源·铁律之二〕** 既有 T0（法师原话）／T1（祖典原文）之外，本项目自 L.111 起立**第四层·待校语料**：

| 层 | 是什么 | 可靠性 | 可否充逐字依据 |
|---|---|---|---|
| **T0** | 法师原话（一手栈 `docs/huayanhai/`） | 可回源 | ✅ |
| **T1** | 祖典原文（CBETA 等） | 可回源 | ✅（但**不得**充法师原话） |
| **第四层** | **OCR 重建字幕稿**等**派生·待校**语料 | **不可回源至原件**（原件已遗失） | ❌ **绝对不可** |

`docs/hy_refs/sub_extract/delivery/ep01–ep12.*`（12 集／约 32.7 小时／32.5 万汉字）即属第四层：寺方原始字幕稿**已遗失**，本稿系对第三方视频硬字幕的影像层还原，**时间码 ±1s、快语速可能丢首字、含幻燈片投影文字（实测 2,256 条以「 | 」拼接）**。

| 门禁 | 作用 | 反向验证 |
|---|---|---|
| `scripts/jj_ocr_audit.py` | **实测**：md／srt／html 条数一致性、覆盖率、片头/拼接/拉丁/简繁/短句污染率、跨源命中。内置 **SIMP 自检**（须命中交付者自述之「现在」「国」，否则「简繁混排 N 条」不可信即中止） | — |
| `scripts/_jj_build_lib.py` | 由实测 JSON **生成**立册（**不手录**）；YAML 解析自检 | — |
| `scripts/verify_jj_lectures.py` | **七道**：结构／**实测对账（重跑，不信 tmp JSON）**／出处可点（11 位 video_id，编务总则七）／**校定状态诚实**（`待校定` 被摘除而无 `calibration_evidence` 即失败）／**T0 限栈不含本路径**／否定记录必备字段＋「不可」限定／越界断言／月份自洽 | ✅ **8/8** |
| `scripts/_verify_jj_reverse.py` | 八类破坏性变异（职责分离：异文件执行） | — |

**立册**：`data/research/jj_huayan_lectures.yaml`（实测台账＋逐集 12 条可点出处＋**否定记录 5 条 N-JJ1–N-JJ5**＋限度 8 条＋**使用规则 U1–U5**＋结论 4 条）。

**〔集数自动发现·不可写死〕** 交付者明言讲座**尚未完結**（「後續會持續更新」），故 `discover_eps()` 扫 `epNN.{md,srt,html}` 得之，**三产物须集集齐备、集号须连续，否则中止**；实测、生成、门禁**三处均不写死「12 集」**。功能测试：以最小 `ep13` 注入交付目录 → 门禁如期报「`meta.episodes` 12 ≠ 目录实测 13 集——**台账漏收新集**」等 6 项失败，`audit` 首行随之变为「13 集」；测毕即删、零残留。**若写死集数，新增集次将静默不入册而门禁仍全绿**——此即交付者明言「会持续更新」时最易犯之错。

**〔三条不可越之界〕**
1. **U1**：本路径**不得**入 T0 一手栈（`verify_haiyun_evidence.T0_ROOT`），OCR 稿不得充 A 类逐字依据——此为**门禁 E 项断言**，非文档约定。
2. **N-JJ1**：「与既有语料 0 命中」**不得**表述为「两源一致」或「两源不一致」——比对语料仅 **66 汉字**且属**另一讲题**，此为「**无可互证之对象**」。
3. **N-JJ3**：「 | 」是**幻燈片文字＋口播**拼接，**非**双轨 OCR，**不得**作两路互校之依据（此为一度误判，已撤回）；引用前须剥离投影文字，否则即以投影字冒充法师语。

**〔门禁自身之三次自纠·记此以勿再犯〕**
① `CUE_MD` 正则漏了 **Markdown 行首反引号**（实为 `` `[时间码]` 文字 ``）→ 解析得 0 条而覆盖率全为 `None`；② 以 `r["%s_cues" % k]` **拼字符串**取键，然 T 与 r 之键名并不对应（`lat↔latin`、`head↔head_garbage`）→ 改**显式映射**；③ 累加循环一度被误置于 `for` 之外，**合计＝末集之数**且输出看似合理——**「静默错算」比崩溃更危险**，故所有实测工具必以**内置自检**（如 SIMP 探测）与**逐集全量打印**互相印证。

**〔禁词检查之结构性教训〕** 初版为「单一禁词表 ＋ 40 字语境豁免」，**两处同时失效**：假阴性（豁免窗口过宽，「不得手录」恰落在窗口内，使「已校定」被豁免）＋假阳性（「须回 T1 祖典或已校定之讲记」中对**他种材料**的合法提及被误杀）。根因是**以关键词窗口猜语义**。现改为**按字段性质分层**：`BANNED_HARD`（任何位置皆禁）＋ `BANNED_STATE`（只在**断言字段** `meta.*`／`calibration`／`conclusions[].判` 内裸禁，散文字段合法提及他种材料之状态故豁免）。**分层依据是字段在本册中之角色，可核对可复跑，不依赖自然语言启发式。**

**〔变异器自身失效亦须如实报出〕** 变异若为空操作（正则未命中、或落点在**注释**而非断言字段），须以 `rc=2` 明示「变异未生效」，上层即判测试无意义——**不得**计为通过。本轮三处即因此暴露：`drop_calibration` 未容引号、`soften_neg` 打在 `key` 而非 `判读`、`shout_verified` 落在文件头注释内。
