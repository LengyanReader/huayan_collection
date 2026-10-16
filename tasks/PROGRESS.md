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

## Handoff (latest)

- **Goal:** 按八十华严三十九品次第推进《华严经细读》系列，一品独立成篇；引文回源、可复算、门禁全绿方称完成。
- **Done:** 整仓 harness 落盘并定制（13 文件）；`AGENTS.md` 作薄入口；能力/门禁/决策/推导记录齐备。
- **Blocked:** 无（harness 侧）。研究线遗留项：梵藏对勘、图像文物（本机无一手材料）；G3 复算〔待核〕。
- **Next:** ① 跑 `python .harness/check.py .` + `make verify-all` 确认基线绿；② 待用户确认后开**第六品《毗卢遮那品》**专篇。
- **Sources:** `harness_factory` SKILL.md / capability-router.md / requirement-refinement.md / derivation-rules.md / core/01·04·05；本仓 `Makefile`（`verify-all` L96）· `CLAUDE.md` · `harness/README.md` · `.harness/manifest.json`。
