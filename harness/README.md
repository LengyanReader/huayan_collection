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
| `claude-progress.txt` 进度流水 + git 历史 | [`docs/next-phase-plan.md`](../docs/next-phase-plan.md)（滚动批次登记）+ git | [`principles.md`](principles.md) §2 |
| `feature_list.json`：结构化待办、只改 `passes` 字段 | `data/evolution/evolution_state.yaml`（registry 台账）| [`principles.md`](principles.md) §3 |
| 结构化记笔记 / agentic memory（NOTES.md、to-do、memory 工具） | `data/evolution/evolution_log.yaml`（**只追加**台账）+ 长期记忆库 | [`principles.md`](principles.md) §3 |
| "自验证后才算完成" + 测试工具（浏览器自动化/curl） | `verify_demo.py` / `test_pipeline.py` / `verify_sources.py` + headless Chrome CDP | [`tools.md`](tools.md) §验证关卡 |
| 初始器 agent + 逐特性增量推进（一次只做一件、留净态） | 会话收尾协议（跑 `make evolve`、更新计划、提交前全绿） | [`principles.md`](principles.md) §4 |
| 子代理架构（主 agent 协调、子 agent 返回浓缩结论） | `Agent` 工具（Debug / CodeReview / Browser / Search 子代理）| [`tools.md`](tools.md) §子代理 |
| 压缩（compaction）：接近窗口上限即摘要重启 | 会话续接时的自动 compaction + 本目录作为"外部记忆" | [`principles.md`](principles.md) §5 |

> 一句话：**`CLAUDE.md` 是宪法，`next-phase-plan.md` 是心跳，`self_evolve` 是免疫与记忆，`verify_*` 是验收闸，本 `harness/` 是把它们串成闭环的操作手册。**

---

## 二、目录结构

```
harness/
├── README.md              ← 本文件：总纲·映射·索引·如何扩展
├── principles.md          ← Agentic 工程方法与原则（上下文工程 + 长时程 harness）
├── skills.md              ← 技能目录：已安装 / 可安装 / 安装法 / 任务映射
├── tools.md               ← 工具清单：验证关卡脚本 / 子代理 / MCP / CLI / 环境约束
├── sources.md             ← 参考来源与检索记录 + 待扩充清单（backlog）
└── workflows/             ← 按工作流编排"技能+工具+门禁"的可复用配方
    ├── data-pipeline.md      数据管线/知识图谱策展（SQLite→build→verify 核心循环）
    ├── web-ui.md             前端·数据驱动导航与渲染（navigation.yaml/双源渲染器/双语链）
    ├── translation.md         翻译（多语EN·校对·术语·渲染安全）
    ├── information-assurance.md 信息保证（考证优先·来源分级·待核边界）
    ├── academic-standards.md  学术规范（引用可点·IEEE/脚注·反伪造）
    ├── self-evolution.md      自我演化（感知→解释→行动→学习 闭环）
    ├── verification.md        验证/测试（三道闸 + 交互实测·make verify-all）
    └── deploy.md              部署/仓库治理（GitHub Pages 源=main 根·CRLF/LF·CDN）
```

---

## 三、八条工作流一览（详见 `workflows/`）

> 数据管线/前端为工程量最大的**工程面**；翻译/信息/学术/演化偏**编辑研究质控**；验证/部署为**横切面**。

| 工作流 | 何时用 | 关键技能 | 关键工具/门禁 | 权威原则源 |
|---|---|---|---|---|
| **数据管线/图谱** | 新增/订正人物·边·地点·经·品目·术语，跑 import→build→verify | `research` | `import_all_to_sqlite`·`export_sqlite_to_json`·`db_reader`·`test_pipeline`(95/98/30)·`load_neo4j` | `CLAUDE.md`〈三层数据栈〉〈权威源表〉+ `docs/knowledge-management.md` |
| **前端/导航渲染** | 改侧栏/独立文章/中英渲染/视图切换/可视化 | `frontend-design` | `navigation.yaml`+`render_sidebar`·`standalone_articles`·双源`WIZ_LIB_RENDER`↔`renderWizLibrary`·`node --check`·CDP/dump-dom | memory〈Interactive State Verification〉+ L.㉝/㊾ 系列 |
| **翻译** | 新增/订正任何 `*_en` / 多语对读字段 | `academic-research-writer`、`citation-verification` | `_markEnBlocks`/`.en-line` 渲染、`audit_bilingual`、`verify_demo`、YAML 转义纪律 | `CLAUDE.md`〈多语 EN 翻译原则〉七条 |
| **信息保证** | 任何史实/名号/年代/数字/出处落库前 | `research`（一手源核查）、`citation-verification` | `verify_sources.py`、`backfill_*`、`extract/ocr_hy_refs`、〔待核〕标记扫描 | `CLAUDE.md`〈工程核心原则 0·考证优先〉+〈编务总则 0/3/6〉 |
| **学术规范** | 撰写/审校研究文档、参考文献 | `academic-research-writer`、`citation-verification` | 引用可点 `[text](url)` + `_dynMD`、GB/T 15835 数字、图表编号 | `CLAUDE.md`〈编务总则 7·引用可点〉+ `docs/reference-management.md` |
| **自我演化** | 每次会话收尾 | （本目录即其接口文档）| `make evolve` / `--apply` / `--ledger`、`--record` | `docs/self-evolution.md` |
| **验证/测试** | 任何改动“是否算完成”的裁决 | （内置）| `make verify-all`、headless Chrome `--dump-dom`/CDP、node --check | `harness/workflows/verification.md` + memory〈Interactive State Verification〉 |
| **部署/仓库治理** | 发布产物到 Pages、换行/缓存/分支决策 | （内置）| `make demo` / `demo-deploy`（已修暂存 web/demo/）、线上 dump-dom 核验 | `docs/next-phase-plan.md`〈部署与仓库治理〉既定事实 |

---

## 四、任一会话的标准节拍（Session Protocol）

> 直接对标 Anthropic "getting up to speed"：新会话先用最小上下文找回状态，再增量做**一件事**，收尾留**净态 + 痕迹**。

1. **定向（orient）**：`pwd` → 读本 `README.md` → 读 `CLAUDE.md`〈当前进度·下一步〉→ 读 `docs/next-phase-plan.md` 顶部与 `docs/evolution/next_actions.md` 高优先项 → `git log --oneline -15`。
2. **验基线（baseline check）**：必要时先跑一次构建/验证，确认工作区处于"可合并净态"；若有破损先修，不要带着破损做新功能（zero-risk-first）。
3. **选一件事（one feature）**：从待办台账选**最高优先级的单一事项**（避免一次做太多导致中途中断、把半成品留给下一会话）。
4. **做+自验证（verify before done）**：改数据源（SQLite/YAML）而非下游 → `build` → `verify_demo` + `test_pipeline`（+ 涉内容则 `verify_sources`）→ 交互态用 headless Chrome/CDP 实测。**验证未全绿不得声称完成、不得标 `passes:true`。**
5. **留痕（leave artifacts）**：更新 `docs/next-phase-plan.md`；跑 `make evolve`；必要时 `self_evolve --record --actor agent` 补记带外动作；沉淀可复用经验到长期记忆。
6. **净态提交（clean state）**：如经用户同意，`git commit` 描述性信息（+ 更新进度文件），使下一位"轮值工程师"可无摩擦接续。

---

## 五、如何扩展本 harness

- **新技能**：装好后在 [`skills.md`](skills.md) 追加一张卡（名称 / 触发 / 对应工作流 / 安装命令）。
- **新工具/脚本**：在 [`tools.md`](tools.md) 追加条目；若成为验收闸，同步进〈验证关卡〉与本 README 第三节。
- **新工作流**（如"图谱策展""多语满/藏""部署/CI"）：在 `workflows/` 新建 `<name>.md`，套用现有四段式（何时用 → 步骤配方 → 技能/工具 → 门禁 → 常见坑），并在本 README 第三节加一行。
- **新方法论**：进 [`principles.md`](principles.md)，并在 [`sources.md`](sources.md) 登记出处链接。
- **一致性铁律**：本目录所有文件遵守〈考证优先 / 严禁假信息 / 边界自知〉——引用外部方法一律给可点来源；本项目未落实者标〔待落地〕，不假装已具备。

> 维护者：编码智能体（agent）与人工共同滚动维护；每次新增能力都应让"下一个失忆的会话"仅凭本目录即可上手。
