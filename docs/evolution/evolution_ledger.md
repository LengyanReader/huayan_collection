# 进化台账 (Evolution Ledger)

> 由 `scripts/self_evolve.py` 自动维护的**只追加**审计流水；权威机读源为 `data/evolution/evolution_log.yaml`。
> 记录每一次进化动作——自动体检/阈值整定/自动归档，与人工确认的进度回填/否决，以及 Agent 带外记录。

共 **42** 条事件。

## 2026-09-24

| seq | 周期 | 触发 | 类别 | 对象 | 动作/变更 | 结果 | 依据/理由 |
|---|---|---|---|---|---|---|---|
| 37 | 8 | 🤖 | cycle_run | 周期 #8 体检总览 | — → health=83.1 open=75 high=29 | 👁观测 | 新增 6·归档 0·台账矛盾 0 |
| 38 | 8 | 🤖 | marker_register | 登记新增待办 6 项 |  | ✅执行 | 扫描 include 文件命中的待核/存疑/待订正标记 |
| 39 | 8 | 🤖 | threshold_tune | escalation_window_days | 9 → 7 | ✅执行 | 高优先积压 29 vs 带限[6,25]→收紧 |
| 40 | 8 | 🤖 | cadence_set | next_review | — → +7d → 2026-10-01 | ✅执行 | 据积压与阈值推算复核节奏 |
| 41 | — | 🧠 | content_expand | chan_authentic_traces +3 researched topi | Derived from docs/禅门文献与研究地图_四域近年.md; inserted by raw-text sp | ✅执行 |  |
| 42 | — | 🧠 | content_expand | 禅门实迹 references: 26→61 条·A/B/C 信度分级+34可回 | references 结构化(label/tier/url/note)+双渲染器(build.py CHAN_TRACE | ✅执行 |  |

## 2026-09-23

| seq | 周期 | 触发 | 类别 | 对象 | 动作/变更 | 结果 | 依据/理由 |
|---|---|---|---|---|---|---|---|
| 16 | — | 🧠 | harness_setup | 新建 harness/ 智能体工作法总纲目录 | 综合 Anthropic《长时程 agent harness》《上下文工程》+ 本项目既有资产，落地 harness/： | ✅执行 |  |
| 17 | — | 🧠 | harness_setup | harness coverage audit: added data-pipel | double-check found initial harness under-covered repo engine | ✅执行 |  |
| 18 | — | 🧠 | harness_setup | verify follow-up backlog: build_demo.py  | graph.json actually produced by export_sqlite_to_json.py; bu | ✅执行 |  |
| 19 | 3 | 🤖 | cycle_run | 周期 #3 体检总览 | — → health=45.2 open=244 high=103 | 👁观测 | 新增 84·归档 0·台账矛盾 0 |
| 20 | 3 | 🤖 | marker_register | 登记新增待办 84 项 |  | ✅执行 | 扫描 include 文件命中的待核/存疑/待订正标记 |
| 21 | 3 | 🤖 | threshold_tune | escalation_window_days | 24 → 21 | ✅执行 | 高优先积压 103 vs 带限[6,25]→收紧 |
| 22 | 3 | 🤖 | cadence_set | next_review | — → +14d → 2026-10-07 | ✅执行 | 据积压与阈值推算复核节奏 |
| 23 | 4 | 🤖 | cycle_run | 周期 #4 体检总览 | — → health=83.5 open=75 high=33 | 👁观测 | 新增 0·归档 0·台账矛盾 0 |
| 24 | 4 | 🤖 | threshold_tune | escalation_window_days | 21 → 18 | ✅执行 | 高优先积压 33 vs 带限[6,25]→收紧 |
| 25 | 4 | 🤖 | cadence_set | next_review | — → +14d → 2026-10-07 | ✅执行 | 据积压与阈值推算复核节奏 |
| 26 | 5 | 🤖 | cycle_run | 周期 #5 体检总览 | — → health=81.1 open=75 high=33 | 👁观测 | 新增 0·归档 0·台账矛盾 0 |
| 27 | 5 | 🤖 | threshold_tune | escalation_window_days | 18 → 15 | ✅执行 | 高优先积压 33 vs 带限[6,25]→收紧 |
| 28 | 5 | 🤖 | cadence_set | next_review | — → +14d → 2026-10-07 | ✅执行 | 据积压与阈值推算复核节奏 |
| 29 | 6 | 🤖 | cycle_run | 周期 #6 体检总览 | — → health=81.1 open=75 high=33 | 👁观测 | 新增 0·归档 0·台账矛盾 0 |
| 30 | 6 | 🤖 | threshold_tune | escalation_window_days | 15 → 12 | ✅执行 | 高优先积压 33 vs 带限[6,25]→收紧 |
| 31 | 6 | 🤖 | cadence_set | next_review | — → +7d → 2026-09-30 | ✅执行 | 据积压与阈值推算复核节奏 |
| 32 | — | 🧠 | tooling | fix self_evolve scan: pathlib trailing / | expand_targets now treats /**-suffixed excludes as subtree p | ✅执行 |  |
| 33 | 7 | 🤖 | cycle_run | 周期 #7 体检总览 | — → health=84.1 open=69 high=27 | 👁观测 | 新增 0·归档 0·台账矛盾 0 |
| 34 | 7 | 🤖 | threshold_tune | escalation_window_days | 12 → 9 | ✅执行 | 高优先积压 27 vs 带限[6,25]→收紧 |
| 35 | 7 | 🤖 | cadence_set | next_review | — → +7d → 2026-09-30 | ✅执行 | 据积压与阈值推算复核节奏 |
| 36 | — | 🧠 | content_verify | chan_authentic_traces 6 items resolved:  | Shenhui dates via pagoda inscription + Zongmi commentary; Sh | ✅执行 |  |

## 2026-09-20

| seq | 周期 | 触发 | 类别 | 对象 | 动作/变更 | 结果 | 依据/理由 |
|---|---|---|---|---|---|---|---|
| 1 | 1 | 🤖 | cycle_run | 周期 #1 体检总览 | — → health=67.1 open=75 high=61 | 👁观测 | 新增 75·归档 0·台账矛盾 0 |
| 2 | 1 | 🤖 | marker_register | 登记新增待办 75 项 |  | ✅执行 | 扫描 include 文件命中的待核/存疑/待订正标记 |
| 3 | 1 | 🤖 | threshold_tune | escalation_window_days | 30 → 27 | ✅执行 | 高优先积压 61 vs 带限[6,25]→收紧 |
| 4 | 1 | 🤖 | cadence_set | next_review | — → +14d → 2026-10-04 | ✅执行 | 据积压与阈值推算复核节奏 |
| 5 | — | 👤 | progress_backfill | next-phase-plan P0 6项(SQLite初始化/JSON→SQL | 管线全绿佐证下回填 🔴待实施→✅已完成·进化引擎核证2026-09-20（台账上线前历史动作，补记） | ✅执行 |  |
| 6 | 2 | 🤖 | cycle_run | 周期 #2 体检总览 | — → health=69.5 open=75 high=61 | 👁观测 | 新增 0·归档 0·台账矛盾 0 |
| 7 | 2 | 🤖 | threshold_tune | escalation_window_days | 27 → 24 | ✅执行 | 高优先积压 61 vs 带限[6,25]→收紧 |
| 8 | 2 | 🤖 | cadence_set | next_review | — → +14d → 2026-10-04 | ✅执行 | 据积压与阈值推算复核节奏 |
| 9 | — | 🧠 | content_edit | 独立文章·新技术与佛教 | 术语统一 模型卡→模型说明卡(首现注 model card)；口语化→书面/学术改写(导言至第十六章约40处) | ✅执行 |  |
| 10 | — | 🧠 | data_correction | teaching_resources.yaml·播客规模 | Apple/Spotify 普贤乘华严宗 scale 2000+集→387集(RSS核验387 items)，关闭 L. | ✅执行 |  |
| 11 | — | 🧠 | content_integration | 海云讲法导航+前沿挂接 | 讲法资源(pv-resources)顶部加海云讲法全库导航(本页跳转+独立页链接+三方向快捷入口)；build.py 令 | ✅执行 |  |
| 12 | — | 🧠 | ui_refactor | 海云讲法页·去#hl-focus重叠块(practice.js+build.py | 删除独立「主要讲法方向·快捷入口」区块(8个一级目录卡片与目录树重复)，3个重点方向内并入总览；移除navigation | ✅执行 |  |
| 13 | — | 🧠 | content_integration | 前沿对话新增「南予其时」tab占位 | navigation.yaml+frontier_dialogue.yaml(section nanyu/anchor  | ✅执行 |  |
| 14 | — | 🧠 | ui_refactor | 南予其时·由frontier内嵌section改为最底部独立页面 | 用户指示：移到tab最底部+打开为独立页面。新建docs/南予其时.md占位+standalone_articles.y | ✅执行 |  |
| 15 | — | 🧠 | ui_refactor | 海云讲法降级为讲法资源子项(侧栏扁平化) | navigation.yaml删除海云讲法顶层group，其入口改为讲法资源sub-link(jxSubNav haiy | ✅执行 |  |

