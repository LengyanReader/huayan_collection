# Gates · 僧传画像

## Hard gates (non-negotiable · strict per grounding=required)

| gate | description | verify |
|---|---|---|
| **回源门** | Every load-bearing claim (科名, 卷次, 人物 data) has `source:` filled (CBETA / print ref + access date), OR is marked `〔待核〕` | `check.py --source` mode (future) |
| **占位符门** | No unrendered template variables or `TODO_unresolved` markers remain in emitted files | `check.py` (now) |
| **结构完备门** | PLAN.md sections (Goal / DoD / First move) all present | `check.py` (now) |
| **宁缺不伪** | A missing value is preferred over an unverified one; do NOT fill gaps from memory | human review + agent discipline |
| **irreversible-OK** | Push, delete, publish → require explicit user confirmation before execution | agent protocol |

## Soft gates (preferences · adjustable per iteration)

| gate | note |
|---|---|
| demo 版面美学 | 设计良好, 但 MVP 阶段重结构不重像素 |
| 维度穷举充分性 | 尽量覆盖僧传体裁, 但"宁欠勿凑"——维度多到空转不如精简 |
| 取样人数 | "各大宗派一位", 可扩展或精简 |
