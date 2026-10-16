# PROVENANCE · 僧传画像 harness

## Derivation record

| step | what | source file(s) | capability used |
|---|---|---|---|
| Route | "需求模糊" hit → `ambition-elevation` | `reference/capability-router.md` | ambition-elevation |
| Refine R0-R4 | Restate → Elevate → Classify → Offer → Confirm | `reference/requirement-refinement.md` | ambition-elevation |
| Feature vector | Classify 8-axis from user's confirmed answers | `reference/derivation-rules.md` §1 | baseline-discipline |
| Module derive | M0-M8 rule table; verifiability=high lever | `reference/derivation-rules.md` §2 | (rules) |
| Capability match | Match `data/capabilities.json` against final vector | `src/harness_factory/data/capabilities.json` | expert-instruments, reproducible-experiments, frontier-standard |
| Override | gate_strictness standard→strict (grounding=required + 宁缺不伪 红线) | Project context (huayan_collection cardinal rule) | source=**mixed** |

## Load order (what was actually read)

1. `harness_factory/SKILL.md` — entry + load-index
2. `reference/capability-router.md` — route to hit row
3. `reference/requirement-refinement.md` — R0-R5 protocol
4. `reference/derivation-rules.md` — feature vocab + rule table + capability map + output contract
5. `src/harness_factory/data/capabilities.json` — when/why per capability
6. `data/knowledge_graph/schemas/persona.schema.json` (target project) — existing dimensions to inherit

## Unverified / marked items

- 僧传十科/门类 **确切名目** → 待回源 T50n2059 目录核定，此处不列具体名称。
- 比丘尼传 = T50n2063 · 宝唱 → 据此前 v2.6 深度检核报告，正式引用前再核 CBETA。
- 居士出处（高僧传·优婆塞 / 广弘明集 / 其他）→ 待回源确认。
- 各样本僧之具体卷/科 → 执行阶段逐人回源。
