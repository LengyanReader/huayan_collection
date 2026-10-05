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

- **自述优先**：- **调整修订追踪**：重点留意「前面讲的」「后来讲」「以前」「现在讲」「调整」「修订」「修改」等表述，追踪法师对相关内容、说法、用词的**不断调整修订**过程，将其纳入「边修边讲·边体会·边理顺·边走边拼」的过程性考证。
凡论及「摸索」「曲折」「错误」「助缘」「边修边讲」「边体会」「边理顺」「边走边拼」等，必须只收录**法师自述原话**（A类），不得用他人综述替代。
- **过程性重于结论**：「定型」采用审慎用语（「趋于定型」「大体理顺」「基本能走通」），避免「最终完成」「完全定型」绝对化。
- **组织性用语须自述**：「拼图」「贯通」「串起」「打通」等组织性用语，只有**主语明确指向法师思路组织**且语境清晰时，方可视为自述性思路表述（A）。
- **溯源不可省**：每条关键论断需 ile_path:line_range（可先用字符位置，后换算行号），保留上下文（±60–120字）。
- **二手仅线索**：docs/hy_refs/pfhy.md 等二手综述**仅作线索**，采纳前须回溯 docs/huayanhai/ 原文并验证。
- **三分界限**：对「复原／重构／建构」逐要素比勘祖典（T1733/T1735/T1736/X0223/T1739），以**组织强度**（提炼vs重新编排次第）判定，而非仅定义。
