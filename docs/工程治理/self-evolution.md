# 自我进化机制 · 设计与使用 (Self-Evolution Mechanism)

> 2026-09-20 落地 | 让项目随时间**自适应**地更新、调整，持续提升适应能力。

## 一、它是什么

一个闭环控制回路，把「项目状态」当作可被周期观测、解释、行动、学习的系统：

```
        ┌──────────────────────── evolution loop ────────────────────────┐
        │                                                                 │
   [SENSE 感知] ──► [INTERPRET 解释] ──► [ACT 行动·半自动] ──► [LEARN 学习] ─┘
   验证关卡/标记     健康度/老化优先级      低风险记账自动做      写进化记忆(时间序列)
   /台账矛盾/文件    /反馈阈值整定/节奏     内容类动作逐项确认    /推算下次复核/记忆提示
   老化
```

- **进化对象**：① 项目数据管线（来源可靠性、待核/存疑积压、进度台账一致性、构建/验证结果、文件老化、可选链接失效）；② Agent 学习闭环（每轮沉淀经验到长期记忆，见第五节）。
- **触发**：手动命令（无外部依赖，标准库 + PyYAML）。
- **自适应深度**：**半自动**——可推导的记账动作自动做；触及内容的动作（进度回填）逐项人工确认。

严格遵守项目「**考证优先 / 严禁假信息 / 边界自知**」原则：引擎只发现、记录、排序，**绝不为消除待办而臆造或篡改研究内容**；无法自动处理者如实登记为 `next_actions`。

## 二、组成

| 文件 | 角色 | 谁写 |
|------|------|------|
| `data/evolution/evolution_config.yaml` | **基因组**（可调参数：阈值/标记词/目标/自适应控制器） | 人工维护（引擎只读） |
| `data/evolution/evolution_state.yaml` | **记忆**（registry 待办台账 + history 时间序列 + adaptive 生效阈值） | 引擎每轮写 |
| `data/evolution/evolution_log.yaml` | **进化台账**（只追加事件流：每一次自动/人工/Agent 动作的显式记录，schema `huayan.evolution.log/v1`） | 引擎每轮追加 |
| `scripts/self_evolve.py` | **引擎**（Sense→Interpret→Act→Learn） | 人工维护 |
| `docs/evolution/health_<date>.md` | 健康度报告（+ `health_latest.md`） | 引擎每轮产出 |
| `docs/evolution/next_actions.md` | 待办梯队（按老化优先级排序） | 引擎每轮产出 |
| `docs/evolution/evolution_ledger.md` | 台账的人类可读滚动视图（由 `evolution_log.yaml` 渲染） | 引擎每轮产出 |

## 三、命令

```bash
python scripts/self_evolve.py                 # 干跑一轮：感知+解释+记账+出报告（不改任何研究内容）
python scripts/self_evolve.py --apply         # 追加：对「进度台账矛盾」逐项 y/N 确认后回填 P0 状态
python scripts/self_evolve.py --check-links   # 追加：链接失效检查（联网；本环境直连不通域已白名单）
python scripts/self_evolve.py --json          # 机器可读摘要
python scripts/self_evolve.py --no-validators # 离线快速预检（跳过子进程验证；此时不触发进度回填）
python scripts/self_evolve.py --reference-date 2026-09-20   # 可复现实验的基准日
python scripts/self_evolve.py --ledger                       # 打印进化台账（最近事件）后退出
python scripts/self_evolve.py --record <类别> --actor <auto|human|agent> --subject ".." --note ".." --outcome <..>  # 带外追加一条进化事件（不跑周期），供人工/Agent 显式记录未走引擎的重型动作
```

等价 Make 目标：`make evolve` / `make evolve-apply` / `make evolve-links` / `make evolve-ledger`。

## 四、各阶段做什么

### SENSE 感知
- **验证关卡**：子进程跑 `test_pipeline.py` / `verify_demo.py` / `verify_sources.py --json`，取通过状态与来源评分（`PYTHONIOENCODING=utf-8` 规避 Windows 控制台 CJK 崩溃）。
- **标记扫描**：遍历 `scan.include`（排除台账/构建产物/引擎自身文件），匹配 `markers` 词表（【待订正】/〔待核〕/〔存疑〕/〔待考〕/〔线索〕/〔待补〕/〔无法获取〕/〔无通行英译〕/TODO/🔴），按 `signature = hash(文件+标记+句)` 建条目（行号漂移不产生重复）。
- **进度台账矛盾**：当管线全绿，却仍有 P0 行标 `🔴 待实施` → 记为陈旧（可回填）。
- **文件老化**：以 `git log` 最后提交时间为准备，超 `file_stale_days` 告警。
- **链接失效**（可选）：抽 URL 做 HEAD/GET 超时探测。

### INTERPRET 解释（**随时间适应的核心**）
- **老化加权优先级**：`priority = severity × (1+gain)^⌊age/escalation_window⌋`（封顶 `max_multiplier`）——同一待办搁置越久，优先级自动爬升。
- **反馈式阈值整定**：高优先积压 > `tolerance_high` → 缩短 `escalation_window`（**收紧**，让问题更快浮出）；< `tolerance_low` → 加长窗口（**放宽**，降噪）。生效值写入 `state.adaptive`，不改基因组文件。
- **健康度**：透明扣分模型（验证失败、来源评分缺口、各级积压）。
- **复核节奏**：据积压与阈值推算 `recommended_cadence_days` 与下次复核日期。

### ACT 行动（半自动）
- **自动（确定性派生）**：registry 刷新（新增/复现/`absent_cycles`）、连续 `grace_cycles` 未再出现的条目自动归档为 `resolved`、写报告与历史。
- **逐项确认（`--apply`）**：仅「进度回填」——把管线核证的 P0 `🔴待实施 → ✅已完成·进化引擎核证<date>`；非交互/EOF 一律保守跳过。内容级修正**永不**自动执行，只登记进 `next_actions` 待人工/Agent 考证。

### LEARN 学习
- 把本轮指标追加进 `history`（时间序列），使「适应能力」可被趋势观测（连续多轮同向收紧＝积压是结构性的，应立专项）。
- 报告尾部给出「记忆更新提示」，供 Agent 沉淀长期经验（见下）。
- **每一次动作落台账**：本轮产生的自动动作（体检总览、登记新增、自动归档、阈值整定、节奏设定、链接失效）与经确认的人工动作（进度回填的执行/否决）均作为一条事件**只追加**写入 `data/evolution/evolution_log.yaml`，并渲染为 `docs/evolution/evolution_ledger.md`。

## 五、进化台账 (Evolution Ledger) —— 供后续机制读取的接口

目的：**每一次进化——无论自动还是人工——都有显式、可回放的记录**，让未来的自我演化机制与其他机制能追溯「何时、由谁、对什么、做了什么、依据什么」。

- **权威源**：`data/evolution/evolution_log.yaml`（`schema: huayan.evolution.log/v1`，`events` 为只追加列表，`seq` 单调递增）。人类可读视图：`docs/evolution/evolution_ledger.md`。
- **事件 schema**（字段稳定，缺省字段不写）：

  | 字段 | 含义 |
  |------|------|
  | `seq` / `ts` / `date` / `cycle` | 序号 / 时间戳 / 日期 / 所属周期 |
  | `actor` | `auto`（引擎）· `human`（人工确认）· `agent`（编码助手带外记录） |
  | `category` | `cycle_run`·`marker_register`·`auto_resolve`·`threshold_tune`·`cadence_set`·`progress_backfill`·`link_check`·`note` |
  | `subject` | 作用对象（文件/阈值/P0 行…） |
  | `before` / `after` / `action` | 变更前后值或动作描述（如 `30 → 27`、`🔴 待实施 → ✅ 已完成`） |
  | `outcome` | `applied`·`declined`·`observed`·`skipped` |
  | `evidence` / `rationale` | 依据（如管线全绿）/ 理由（如积压超带限→收紧） |

- **为何重要**：`history`（`state.yaml`）只有每轮聚合指标；台账保留**动作级明细**，包括被**否决**的提议（`outcome: declined`）——其他机制据此知道哪些判断人已过目并刻意保留，避免重复扰动。
- **他机制如何读**：按 `category` / `actor` / `outcome` 过滤即可（例：取 `category=threshold_tune` 回溯阈值自适应轨迹；取 `actor=human AND outcome=applied` 审计人工干预史）。
- **带外记录**：凡未走引擎但属于「进化」的重型动作（如手工整理某模块、Agent 做出结构性决策），应即时 `--record --actor agent/human` 补记，保持台账完整。

## 六、Agent 学习闭环（进化的另一半）

引擎产出是**信号**；把信号变成**经验**由编码助手在每个工作会话收尾时执行：

1. **跑周期**：任务收尾时 `make evolve`（或 `--apply` 回填已核证进度）。
2. **读梯队**：看 `docs/evolution/next_actions.md` 顶部高优先项与「记忆更新提示」。
3. **沉淀记忆**（UpdateMemory）：
   - 进度快照变化 → 更新 `project_introduction` 类记忆；
   - 新出现的验证失败/台账矛盾/工具受限 → 记入 `common_pitfalls_experience`；
   - 重复出现的流程模式 → 更新 `learned_skill_experience` / `task_experience`。
4. **回写台账**：按编务总则 5「进度留痕」更新 `next-phase-plan.md`。

如此：**引擎负责"随时间观测与排序"，Agent 负责"据此行动与固化经验"**，二者合成跨会话持续进化的闭环。

## 七、边界与免责（边界自知）

- 〔待核〕/〔无法获取〕类多为**有意保留的考证边界**（如派内传承、无独立史料者），健康度因此偏低**不等于错误**，只反映"未闭环考证量"；是否推进由人工判断。
- 进度回填仅动 P0 状态列且需绿管线佐证 + 人工确认；不触碰研究正文。
- 链接检查在本环境部分站点直连不通，已白名单 `84000.co`/`bodhiai.cn`，未列域超时会计为失效，建议偶发使用。
