# PROGRESS — 华严经细读系列（整仓 harness）

**Updated:** 2026-10-17

> Append-only. 记录结果、订正及其来源。

## Session log

- 2026-10-16T23:04:05+00:00 — harness generated (harness-factory 0.1.0). No work yet.
- 2026-10-17 — **harness 落盘并定制**（本仓首套 harness_factory 契约产物）：
  - 依 `harness_factory` 六步协议（R0–R5）先精炼需求，经用户确认三点：阅读=**Elevated（整仓）**；`AGENTS.md`=**薄入口**（`CLAUDE.md`+`harness/` 仍为 SSOT）；优化=**只出提案**（见 `.harness/decisions.md`）。
  - `init` 以显式特征向量落盘 13 文件（`source=flags`）：domain=humanities · horizon=multi_session · verifiability=medium · stakes=high · grounding=required · artifact=document · tool_surface=read_write · collaboration=solo。**模块 M0–M8 全开**，能力 14 项。
  - 定制：`AGENTS.md` 改写为**薄入口**（SSOT 声明 + 入口地图 + 常驻引用 + 五硬规则/本仓铁律 + 门禁指针），**不重复**研究正文；`.harness/gates.md` 登记本仓既有 `verify_*` 为硬门；`.harness/capabilities.local.md` 填能力落地表；`.harness/decisions.md` 记 R4 决策；`.harness/PROVENANCE.md` 补 L0/L1 推导来源；`.harness/ledger.md` 追加。
  - 观察（observe-only，未改动任何仓内文件）：仓根 5 个 tracked 垃圾文件（`_roll_err.txt`·`test.html`·`tj1.txt`·`verify_demo_last.txt`·`verify_demo_run2.txt`）；`CLAUDE.md` 127 KB／最长行 20,493 字符（上下文膨胀）；`numpy`/`networkx` 在 `hy_py312` 实测可用（旧「缺库阻塞 G3」疑过期〔待核〕）。**均仅提案，待授权处置。**

- 2026-10-17 — **(A) 前五品内容修复批·一（引文回源＋结构一致性）**，逐条留痕、本地 commit（未 push）：
  - 自建**经文回源审计**（temp 脚本，观察态）：抽前五品全部 `> **经文**`／`**经文（…）**：` 引文块逐串回源 `T10n0279`；未对齐者再查 `T09n0278` 六十与六部注疏节选。注疏 txt 含**康熙／CJK 部首码位**（NFKC 不覆盖 U+2E80–2EFF），须按 `unicodedata.name()` 建映射归一。扫描**块 119／串 2,612**；逐条定性后**真缺陷 2 例**，其余皆 `**经文（…）**：` 同行疏解误报。
  - **修复 1（第三部·经文）**：`與知一切眾生語言海轉法輪辭辨智` → **`辭辯智`**。据 `T10n0279` 逐字作「辭辯智」；`T09n0278` 卷三亦作「辭辯智」。同段疏解简体 `辞辨智`→`辞辩智`；§6 对读表「八十」列同步订正（合计 3 处）。
  - **修复 2（第五部·疏引）**：§2.13 澄观引文「重頌總有百一偈……餘一百頌所持剎網」→ **「第二重頌總有一百一偈……餘一百偈頌所持剎網」**（据 `T1735` 原文；与本文后文所引正确形式一致）。
  - **`华严经学_三十九品深度研究.md` 内部矛盾订正 6 项**：① §2.2 五周因果表据 `T1735` 回源重订（辨明所信/差别/平等/成行/证入五周之正解；旧表「四位配五周」及品目范围不合疏文）；② §2.1 七处九会表补「忉利天宫」脱字、订第五会场所误填（「他化自在天」属第六会）；③ 各会「品—卷」据 `T10n0279` 卷首品题实检订正（三会卷16—18·四会19—21·五会22—33·六会34—39·七会品27—37/卷40—52·八会品38）；④ 十回向品「共35卷」→**十一卷（卷23—33）**；⑤ 四十华严经号「T1974」→**`T10n0293`**（2 处）；⑥ §2.3 增**藏译独有二品之会归属**（《如来华严品》→**第一会末**；《普贤宣说品》→**第六会末**；据 Toh44 位次＋84000 转述作法义判断，藏文原典本机缺〔待核〕）。文末增**修订志**。
  - 观察（审计局限，须记）：全仓「引文是否见于 CBETA」之**自动判定当前不可行**——第一–四部注疏引文多作简体、第一部块引多为作者体例注（简体），反查简繁表不完整 → 噪声极大（未见于 CBETA 2,485／9,902 串，绝多数係误报）。已列为待办（需补一套完整简→繁表＋区分经文块与编者块）。
  - 临时脚本与中间产物（`audit_quotes*.py`、`pin_juan.py`、`_audit_quotes_out.txt`、`_pin_juan_map.txt`）**均已清理，未入仓**。

## Handoff (latest)

- **Goal:** 按八十华严三十九品次第推进《华严经细读》系列，一品独立成篇；引文回源、可复算、门禁全绿方称完成。
- **Done:** 整仓 harness 落盘并定制（13 文件）；`AGENTS.md` 作薄入口；能力/门禁/决策/推导记录齐备。**前五品内容修复批·一**已办：经文回源审计（块119/串2,612）＋真缺陷 2 例修复（第三部 `辭辯智`、第五部 疏引百一偈）＋`三十九品深度研究.md` 内部矛盾 6 项订正＋藏译二品会归属落 §2.3。
- **Blocked:** 无（harness 侧）。研究线遗留项：梵藏对勘、图像文物（本机无一手材料）；G3 复算〔待核〕；**全仓「引文见于 CBETA」自动判定缺完整简→繁表**〔待建〕。
- **Next:** ① **开第六品《毗卢遮那品》（卷十一，品6）专篇**（总纲 §3.2 待续首项）；② 续 (A) 批·二：体例骨架一致性（第二/三部是否补 §九 台账，先提案）· 标记完备度 · 加粗密度超标（11/11，属报告模式）· 数据层复算核验；③ `系列总纲` §五／§3.2 添藏译指针；④ O1/O2/O6 待逐项授权。
- **Sources:** `harness_factory` SKILL.md / capability-router.md / requirement-refinement.md / derivation-rules.md / core/01·04·05；本仓 `Makefile`（`verify-all` L96）· `CLAUDE.md` · `harness/README.md` · `.harness/manifest.json`；本轮另据 `data/references/cbeta/T10n0279.xml`（品↔卷实检）· `cbeta_txt/T1735_澄观_华严经疏.txt`（五周因果回源）· `cbeta_txt/T09n0278_juan3.txt`。
