---
name: harness-humanities
description: Derived agent workflow for "华严经细读系列（huayan_collection）：依八十华严三十九品次第，逐品独立成篇（三层疏解＋注疏对读＋数据层）" (domain humanities; modules M0, M1, M2, M3, M4, M5, M6, M7, M8). Load when resuming this project's agent work to apply its context, memory, verification, and governance rules.
---

# harness-humanities — task harness skill

> Portable [Agent Skills](https://agentskills.io) skill emitted by **harness-factory**.
> Load it whenever you resume this project's agent work: it carries the derived invariants,
> gates, and the load-on-trigger index.

**Derived for:** 华严经细读系列（huayan_collection）：依八十华严三十九品次第，逐品独立成篇（三层疏解＋注疏对读＋数据层），经文引文逐字回源 CBETA 繁体底本
**Domain:** Humanities (`humanities`) · **Modules:** M0, M1, M2, M3, M4, M5, M6, M7, M8
**Capabilities:** baseline-discipline, verification-gate, resumable-memory, traceable-sources, self-improving-loop, tool-use, human-review-gate, high-stakes-guardrails, long-horizon-autonomy-control, sandboxed-execution, portable-skills, ambition-elevation, expert-instruments, bidirectional-capability-flow

## What this skill enforces

| M0 | Meta-principles / 元原则 | Truth and traceability outrank speed; automate only observe/record/rank |
| M1 | Context engineering / 上下文工程 | Context is a finite, scarce resource - curate, don't dump |
| M2 | Long-running agents / 长时程 agent | Externalize memory; advance incrementally; make every run resumable |
| M3 | Verification & gates / 验证与门禁 | Define done before work; verify the verifier; hard vs soft gates |
| M4 | Provenance & integrity / 来源与完整性 | Every fact traceable to a primary source; uncertain means uncertain |
| M5 | Self-evolution / 自演化 | signal -> audit -> mutation -> journal, human-gated |
| M6 | Tools & skills / 工具与技能 | Minimal toolset; biased errors; skills load progressively |
| M7 | Change governance / 变更治理 | Single source of truth; reviewable diffs; no unsolicited destructive acts |
| M8 | Collaboration & sessions / 协作与会话 | Explicit contracts; escalate decisions; hand off with state |

## How to use it

1. Read `AGENTS.md` at the project root — it holds the load-bearing invariants (M0).
2. Keep durable state in `tasks/PROGRESS.md` (and `.harness/ledger.md` when present); resume from it (M2).
3. Obey the gates in `.harness/gates.md`; run `python .harness/check.py` before declaring done (M3).
4. Load only the module you need (progressive disclosure — M1/M6); do not dump every doc into context.
5. Log irreversible decisions in `.harness/decisions.md` when present (M8).

## Gates

Authoritative gate list: `.harness/gates.md`. Summary (strict):

- [ ] `python .harness/check.py .` → OK.
- [ ] `make verify-all`（`test-pipeline` + `demo-verify` + `verify-sources`）全绿。
- [ ] 专书门禁按改动面加跑（`verify_shizhu` / `verify_ru_lai` / `verify_imagery` 等）。
- [ ] `node --check`（改 JS 时） · `git diff --check` 洁净。
- [ ] 引文逐字回源 CBETA `T10n0279`；无法溯者标〔待核〕/`unverified`。
- [ ] Deliverable matches the stated goal; 复核者（人）认可。

## Index

The load-on-trigger index lives in `.harness/skills/README.md`.
