# Capability ledger (task-local) · 任务本地能力台账

> **Task-specific. Lives here, in this task/project — never flows out on its own.**
> The *concretize* half of the bidirectional capability flow. See the harness-factory's
> `reference/capability-flow.md` (or `harness skill capability-flow`).
> 本文件是**任务本地**的能力台账：记录这次任务用到的能力**在这里如何具体落地**。它只属于本任务，
> 不会自行回流；只有「通用化」的模式才以**提案**形式回流到 harness-factory 并交人类审批。

**Task:** 华严经细读系列（huayan_collection）整仓指导性 harness · **Domain:** humanities · **By:** harness-factory 0.1.0 on 2026-10-16T23:04:05+00:00

---

## Capabilities that fired · 本次触发的能力

| capability | rationale (generic) |
|---|---|
| baseline-discipline | Every task needs load-bearing invariants, curated context, and change governance. |
| verification-gate | Define done before work and verify with observed evidence (M0.3). |
| resumable-memory | Work that spans a session must externalize state and resume from it. |
| traceable-sources | Cited material demands every claim trace to a primary source (M0.1). |
| self-improving-loop | Multi-session work benefits from an explicit signal→audit→mutation→journal loop (M0.10). |
| tool-use | A task that touches the world needs a minimal, progressive toolset. |
| human-review-gate | Others are involved or stakes are high: escalate irreversible decisions (M0.8). |
| high-stakes-guardrails | When stakes are high, strengthen gates and lower autonomy. |
| long-horizon-autonomy-control | A long, high-stakes run needs durable memory, hard gates, and low autonomy. |
| sandboxed-execution | Anything that executes code or reaches the world declares an execution backend and a least-privilege posture. |
| portable-skills | Skills emitted in the Agent Skills (SKILL.md) open format load in any compatible harness. |
| ambition-elevation | Restate → elevate → classify → offer MVP/Elevated/Exploratory → confirm before working. |
| expert-instruments | Use the instruments the field actually uses and an outside judge — not self-grading. |
| bidirectional-capability-flow | Concretize locally; distil only as human-gated proposals. |

## Concretization table · 具体化（由 agent 维护，append-only）

> `local realisation` ＝ 该能力**在本仓**的具体落地；`evidence` ＝ 证明其在位的文件/命令；`gap` ＝ 仍缺什么与最省的下一步。

| capability | local realisation · 本地落地 | evidence · 证据 | gap · 缺口 | generalisable? |
|---|---|---|---|---|
| baseline-discipline | `CLAUDE.md`（宪法）+ `harness/rules.md`（规矩索引）+ `AGENTS.md`（薄入口）分层，规则不出二源 | `CLAUDE.md`·`harness/README.md`·`AGENTS.md` | `CLAUDE.md` 已 127 KB（膨胀，见提案 O2） | maybe |
| verification-gate | 本仓 `verify_*` 全登记为 `.harness/gates.md` 硬门；`make verify-all` 一键 | `.harness/gates.md`·`Makefile` L96 | 门禁耗时（verify_demo 3–5 min）需长 timeout | maybe |
| resumable-memory | `docs/工程治理/next-phase-plan.md`（滚动批次）+ `data/evolution/evolution_log.yaml`（只追加）+ `.harness/ledger.md` | `docs/工程治理/next-phase-plan.md` | 收尾依赖人记；宜脚本化「交接摘要」 | maybe |
| traceable-sources | 引文逐字回源 `T10n0279`（繁体）；注疏回源 `cbeta_txt/`（`T1735`/`T1733`/`T1739`/`X0223`）；`verify_sources.py` 分 T0–T3 | `data/references/cbeta/T10n0279.xml`·`scripts/verify_sources.py` | 梵藏对勘缺一手本 | maybe |
| self-improving-loop | `scripts/self_evolve.py`（`make evolve` / `--apply` / `--ledger`）+ `data/evolution/*` | `Makefile` L120–131 | `make evolve` 是否每会话必跑未强制 | maybe |
| tool-use | conda `hy_py312`：`build.py`·`verify_*`·`import_all_to_sqlite`·`node --check`；harness_factory CLI（`check`/`gate`/`doctor`） | `Makefile`·`.harness/check.py` | 无 | no |
| human-review-gate | 不可逆动作（push/发布/删）须显式授权；R4 三问即此闸 | `.harness/decisions.md` | 无 | no |
| high-stakes-guardrails | 伪造经文事故后立「逐字回源 + 存疑标」铁律；门禁 strict | `AGENTS.md`〈本仓铁律〉·`.harness/gates.md` | 无 | maybe |
| long-horizon-autonomy-control | 门禁硬、autonomy=low；每品收尾留净态 | `tasks/PLAN.md`·`.harness/gates.md` | 无 | no |
| sandboxed-execution | 全部本地执行；无出站；push 前须探代理端口 7890 | `CLAUDE.md`（发布规矩） | 无 | no |
| portable-skills | 已产出 `.harness/skills/harness-humanities/SKILL.md`（Agent Skills 格式） | `.harness/skills/harness-humanities/SKILL.md` | 未按本仓细化 trigger | maybe |
| ambition-elevation | 本次 R0–R5 已实跑（三问确认 Elevated/薄入口/只提案） | `tasks/PLAN.md`〈Confirmed reading〉·`.harness/decisions.md` | 无 | **maybe** |
| expert-instruments | 真器械＝conda 环境 + 既有 `verify_*` + CBETA TEI 原文（非摘要）；评判≠自评 | `.harness/gates.md`〈Evidence rule〉 | 缺独立评判者会话（CI 仅 3 闸） | maybe |
| bidirectional-capability-flow | 本文件（concretize 半边）；distil 半边见下「待回流候选」 | `.harness/capabilities.local.md` | 尚未跑 `learn`/`evolve` 回流 | maybe |

## Distillation candidates · 待回流候选

> 标 `maybe` 者，在 ≥2 个独立任务中出现后，经 `harness learn` + `harness evolve` 转**提案**（observe-only，人工把关）。绝不直接改工厂目录。

| candidate | evidence (≥2 tasks?) | proposed change | status |
|---|---|---|---|
| 「**逐字回源**」类门禁：引文必须回源底本 + 存疑标记，可机械抽检 | 本仓（华严细读 5 品）≥2 | new capability `verbatim-source-gate`（M3,M4） | needs-evidence |
| 「**规则不出二源**」：入口文件只索引不复制正文 | 本仓 `AGENTS.md` 薄入口 | doc note in `core/05` 或 `core/08`（SSOT 落地范式） | proposed |
| domain 分类对「数据」信号误判（data-science vs humanities/reading） | 本仓 1（待第 2 例） | 给 `domains.json` 的 humanities/reading 增中文信号权重 | needs-evidence |

## Derivation trace · 推导依据

| M0 | Meta-principles / 元原则 | Truth and traceability outrank speed; automate only observe/record/rank | always: load-bearing invariants (M0); capability: baseline-discipline, ambition-elevation, bidirectional-capability-flow |
| M1 | Context engineering / 上下文工程 | Context is a finite, scarce resource - curate, don't dump | always: context is consumed by every step (M0.6); capability: baseline-discipline |
| M2 | Long-running agents / 长时程 agent | Externalize memory; advance incrementally; make every run resumable | horizon=multi_session >= session; capability: resumable-memory, long-horizon-autonomy-control |
| M3 | Verification & gates / 验证与门禁 | Define done before work; verify the verifier; hard vs soft gates | always: verify before done (M0.3); strictness from verifiability=medium, stakes=high; capability: verification-gate, high-stakes-guardrails, long-horizon-autonomy-control, sandboxed-execution, ambition-elevation, expert-instruments |
| M4 | Provenance & integrity / 来源与完整性 | Every fact traceable to a primary source; uncertain means uncertain | grounding=required, artifact=document; capability: traceable-sources, expert-instruments |
| M5 | Self-evolution / 自演化 | signal -> audit -> mutation -> journal, human-gated | horizon=multi_session >= multi_session; capability: self-improving-loop, bidirectional-capability-flow |
| M6 | Tools & skills / 工具与技能 | Minimal toolset; biased errors; skills load progressively | tool_surface=read_write; capability: tool-use, sandboxed-execution, portable-skills, expert-instruments |
| M7 | Change governance / 变更治理 | Single source of truth; reviewable diffs; no unsolicited destructive acts | always: single source of truth + reviewable diffs (M0.5/M0.9); capability: baseline-discipline, sandboxed-execution, bidirectional-capability-flow |
| M8 | Collaboration & sessions / 协作与会话 | Explicit contracts; escalate decisions; hand off with state | collaboration=solo, stakes=high; capability: human-review-gate, high-stakes-guardrails, long-horizon-autonomy-control, ambition-elevation |

Files in this harness: - `.harness/PROVENANCE.md`
- `.harness/capabilities.local.md`
- `.harness/check.py`
- `.harness/decisions.md`
- `.harness/gates.md`
- `.harness/ledger.md`
- `.harness/manifest.json`
- `.harness/pointer.json`
- `.harness/skills/README.md`
- `.harness/skills/harness-humanities/SKILL.md`
- `AGENTS.md`
- `tasks/PLAN.md`
- `tasks/PROGRESS.md`

## Boundaries · 边界

- **Direction 1 (concretize):** this file stays here; enrich it as the task runs (append-only).
- **Direction 2 (distill):** generalisable patterns go out **only** as proposals in `updates/` — a human reviews them before anything reaches `data/`, `core/`, `domains/`, or `templates/` (M0.4/M0.8).
- **Path convention:** `SKILL.md`, `reference/*.md`, `core/*.md`, `data/*`, `updates/` above refer to the
  **harness-factory that generated this harness** — not this project.

## 2026-11-24 · L.536 人物线（楼宇烈纪念综述）— 本次触发与落地

| capability | 本次落地（concretisation） | evidence |
|---|---|---|
| source-criticism（史源批判） | 追忆文事实分层：官方讣告/机构官网=A、权威媒体通讯=B、有名回忆=C、孤证网文=D；两说并存 5 组如实登记；网络讹传（连襟说/票友说/「12 年劳改」说）判误留痕不采 | 文档附录 C 24 条＋附录 D 来源表 18 条带链接 |
| traceable-sources | 承重引文两路后台调研＋主笔逐字回源（周口日报楼氏自述、国务院参事室欧阳中石口述均 curl 实测命中）；全文引语标媒体＋日期 | `.tmp/lou_research/` 原文存档（不入库） |
| verification-gate | 完成=门禁实测：build/verify_demo/test_pipeline/node --check ＋ **Playwright 真机渲染 16/16**（补历批「浏览器实测缺位」之账） | `tasks/PROGRESS.md` L.536 |
| cross-language | EN 逐节全译依「重实质不逐字」＋固定人名表（Lou Yulie/Feng Youlan/…）；9 块 `> **EN对应**` 全部经 `_markEnBlocks` 打标、zh-only 实测隐藏 | 渲染实测 en-block=9/hidden=9 |
| expression-design | 追忆体谋篇：生平/人格/师道/艺道/著作/身后/结语＋附录四件；趣事（拆表/朱砂/粉蝶儿）不害考证体例 | 文档 §一–§七 |
