# Workflow — 自我演化（Self-Evolution）

> **何时用**：**每次会话收尾**都跑；以及周期性审视项目健康、把"信号→经验"固化时。
> **权威源（不在本文件重述设计细节）**：[`docs/self-evolution.md`](../../docs/self-evolution.md)（闭环设计·组成·各阶段）+ `scripts/self_evolve.py` + `data/evolution/*.yaml`。

## 一句话

**引擎负责"随时间观测与排序"，Agent 负责"据此行动与固化经验"**，二者合成跨会话持续进化闭环：
`SENSE 感知 → INTERPRET 解释 → ACT 行动(半自动) → LEARN 学习`。

## 会话收尾标准动作（本 harness 的落点）

1. **跑周期**：`python scripts/self_evolve.py`（干跑，不改内容）｜`make evolve`；已核证 P0 需回填再 `--apply`。
2. **读梯队**：看 `docs/evolution/next_actions.md` 顶部高优先项 + 报告尾"记忆更新提示"。
3. **回写台账**：按编务总则 5 更新 `docs/next-phase-plan.md`。
4. **补记带外动作**：本会话做了未走引擎的"重型/结构性"动作，即时
   `python scripts/self_evolve.py --record <类别> --actor agent --subject ".." --note ".." --outcome applied`。
   - 常用 `category`：`ui_refactor`·`content_integration`·`data_correction`·`cycle_run`·`note`（见 `docs/self-evolution.md` 事件 schema）。
   - `outcome`：`applied`·`declined`·`observed`·`skipped`。
5. **沉淀长期记忆**（`UpdateMemory`）：
   - 进度快照变化 → 更新 `project_introduction`；
   - 新验证失败/台账矛盾/工具受限 → 记 `common_pitfalls_experience`；
   - 重复流程模式 → 更新 `learned_skill_experience` / `task_experience`；
   - 结构性技术选型 → `important_decision_experience`。
6. **本 harness 自身也是进化对象**：新增方法/技能/工具/工作流时按 [`../README.md`](../README.md)〈如何扩展〉登记。

## 台账即"供后续机制读取的接口"

- 权威源 `data/evolution/evolution_log.yaml`（`huayan.evolution.log/v1`，`seq` 单调、**只追加**），人类可读 `docs/evolution/evolution_ledger.md`。
- 其他机制/未来会话按 `category`/`actor`/`outcome` 过滤即可回溯（例：`actor=human AND outcome=applied` 审计人工干预；`category=threshold_tune` 看阈值自适应轨迹）。
- 被**否决**的提议（`outcome: declined`）也留痕，避免重复扰动已刻意保留的判断。

## 边界（不可逾越）

- 引擎**只发现、记录、排序，绝不为消除待办而臆造或篡改研究内容**；内容级修正一律登记进 `next_actions` 待人工/Agent 考证。
- 〔待核〕/〔无法获取〕多为**有意保留的考证边界**，健康度偏低≠错误；是否推进由人判断。
- 进度回填仅动 P0 状态列，且需"管线全绿"佐证 + 人工确认。
