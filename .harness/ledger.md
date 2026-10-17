# Ledger (append-only)

> Memory depth: **durable**. Never overwrite history; corrections are new rows.

| time | actor | action | basis | result |
|---|---|---|---|---|
| 2026-10-16T23:04:05+00:00 | harness-factory | init | task intake | scaffold generated (13 files) |
| 2026-10-17 | agent | 定制 AGENTS.md 为薄入口（SSOT 声明+入口地图+五硬规则+本仓铁律） | R4 确认：薄入口 | done |
| 2026-10-17 | agent | 登记本仓既有 `verify_*` 为 `.harness/gates.md` 硬门 | `Makefile` L96 `verify-all` | done |
| 2026-10-17 | agent | 填 `capabilities.local.md` 落地表；记 `.harness/decisions.md` R4 决策；补 `PROVENANCE.md` 推导来源 | M0.4/M0.5 | done |
| 2026-10-17 | agent | (A) 批·一：经文回源审计（块119/串2,612）→ 修复真缺陷 2 例（第三部 `辭辨智`→`辭辯智`；第五部 疏引「百一偈」据 `T1735` 订正） | T10n0279／T09n0278／T1735 逐字回源 | done（本地 commit，未 push） |
| 2026-10-17 | agent | `华严经学_三十九品深度研究.md` 内部矛盾订正 6 项（五周因果表回源·七处九会表·各会品—卷实检·十回向品卷数·四十华严经号·藏译二品会归属）＋文末修订志 | T1735 五周因果原文；T10n0279 卷首品题实检；Toh44 位次＋84000 | done |
| 2026-10-17 | agent | 观察：全仓「引文见于 CBETA」自动判定缺完整简→繁表，噪声极大（2,485/9,902 多为误报）→ 记为待办，不据此改文 | 自建审计 v1–v5（temp，已清理） | recorded |
| 2026-10-17 | agent | 第六品《毗盧遮那品》专篇成篇（§〇–§九·1,315 行；卷11·offset 309864–332004；实测 4,939 字／73 颂／四佛 2,426·1,082·479·131） | 用户裁示「按计划开写」＋`T10n0279` 卷十一回源 | done（本地 commit，未 push） |
| 2026-10-17 | agent | 第六品注疏三家会读（澄观 `T1735` 品6科判／法藏 `T1733` 二光二遍／李通玄 `T1739` 十五条）；新得「大威光＝毗盧遮那」补文（`T1735` L5089–5091）与「经来未尽」「所信因果会竟」两判 | T1735/T1733/T1739 逐字回源 | done |
| 2026-10-17 | agent | 用户裁示③「六十卷四约20名对勘」本批交付：**第五部 §6.9 新立**，逐名对勘八十中央世界种二十重；订正原图（对「中央二十重」非「十海首名」）；附录四#8〔待核〕→✅已办 | `T09n0278` 卷四原文＋`T10n0279` 卷八中央二十重 | done |
| 2026-10-17 | agent | 第六品登记发布（`standalone_articles.yaml` 新增 `piluzhena`；系列总纲同步；`next-phase-plan.md` 增 L.133）；新脚本 `scripts/pilu_shena_studies.py` | 系列体例 | done |
| 2026-10-17 | agent | 门禁全绿：`build` 42 files｜28,365,369 B；`verify_demo` ✅ ALL CHECKS PASSED；`test_pipeline` ✅；`verify_sources` EXIT=0；`git diff --check` 净 | verify_* 五关 | done（真机渲染未确认） |
| 2026-10-17 | agent | 观察：`docs/草稿/高僧传/僧传画像/*.html` 有他会话在途改动（13→20 层）；`docs/祖师人物/不空三藏…md` 未跟踪——**本批未触碰、未纳入提交** | `git status` | recorded |
| 2026-10-17 | agent | SSOT 漂移订正：`系列总纲` §二 品6「⬜待开」→「✅已成篇」（与 §三.1 自相矛盾）；`CLAUDE.md` 当前进度补登 L.133（第六品） | 自我 commit 遗漏＋门禁重跑全绿 | done（本地 commit `a2576e2`，未 push） |
| 2026-10-17 | agent | 评估：按七处九会，**第一会（品1–6·卷1–11·所信因果周）六品皆已成篇＝完整**；附记 `三十九品研究` §2.1「第一会 场所＝世间净眼普严殿」于 `T10n0279` 无此组合〔待核〕 | `三十九品研究` §2.1/§2.2（据 `T1735`）＋澄观「所信因果會竟」（`T1735` L5090） | recorded |
| 2026-10-17 | agent | L.135 第一会部 2–6 补 `### 5.2′`（智俨 `T1732`）／`### 5.2″`（慧苑 `X0221`）；部 1 附录八补 `### 八.9`／`### 八.10`（共 12 处插入） | 用户「先落实第 2、3 项」＋二帙部首归一后逐字回源 | done（本地 commit，未 push） |
| 2026-10-17 | agent | 结构判定并落实：**`T1732` 依六十本**（其〈盧舍那佛品第二〉统摄八十品 2–6）→ 部 3–6 之 5.2′ 只引其品 2 通判并明此理；**`X0221` 依八十本** → 逐品直引 | `T1732` L170/L422–454；`X0221` 品 2–6 | done |
| 2026-10-17 | agent | §5 体例订正（(A) 批·二之体例骨架一致性·部分）：部 3/4/5/6 计数标题及台账行改「诸家」；部 4/5 体例「取古今四家——」（仅列 3 家·旧稿误计）→「三家」 | 现有对照表实列 3 家（澄观/法藏/李通玄） | done |
| 2026-10-17 | agent | 新增门禁 `scripts/verify_round_h2.py`：6 部新增节 `> 「…」` 引文按底本归一逐片段子串校 → **34 片段／0 失配**；**揪出并订正 3 处误引**（部 6「無異」→底本「無失」；部 5 梵名删夹注小字 `(入呼)(上呼)` 致不连续；部 1 十门·部 2 科判之撮录当逐字引） | `T1732`/`X0221` 归一比对 | done |
| 2026-10-17 | agent | 门禁全绿：`.harness/check.py` ✅；`verify_sources` 系列 7 篇仍入覆盖（存疑各 +2：部1 231·部2 49·部3 39·部4 38·部5 41·部6 40）；`t1_quote --check` ✅（31 条/0 失配）；`verify_t1_bikan` ✅；`build` 42 files｜28,399,096 B；EOL 保持（部1 CRLF 4475/0；部2 仍 16 裸 LF 未增；部3–6 纯 LF） | verify_* 诸关 | done（本地 commit，未 push） |
| 2026-10-17 | agent | 观察（勿提交）：工作树含他会话在途件（`docs/草稿/高僧传/僧传画像/**`·`docs/祖师人物/不空三藏/玄奘_全方位文献综述.md`·CBETA ingest `T50n*.xml`/`INGEST_log.md`·`data/references/cbeta/README.md`·**已 staged 之** `scripts/cbeta_extract.py`/`fetch_cbeta_history.py`）——本批未触碰、以显式路径提交 | `git status` | recorded |
