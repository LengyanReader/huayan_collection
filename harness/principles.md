# Principles — Agentic 工程方法与原则

> 本文件提炼"如何让 agent 在有限上下文、跨会话条件下稳定工作"的通用方法，并逐条落到本项目的具体机制。
> 来源：Anthropic《Effective context engineering for AI agents》《Effective harnesses for long-running agents》《Equipping agents for the real world with Agent Skills》（链接见 [`sources.md`](sources.md)）。凡本项目尚未落实者标〔待落地〕。

---

## §1 上下文工程（Context Engineering）

**核心命题**：上下文是**有限资源**，存在"注意力预算"与**上下文腐坏**（context rot：token 越多，召回越差，n² 注意力被稀释）。目标 = **找出能完整表达预期行为的最小高信号 token 集合**（最小 ≠ 短，而是不冗余、不掺无关）。

落地到本项目的做法：
1. **直投 vs 即时检索（hybrid / just-in-time）**：`CLAUDE.md` 作为"naively dropped into context"的项目记忆前置加载；海量数据（`data/**`、`docs/**`）**不预载**，而用 `Glob`/`Grep`/`SearchCodebase` 按需寻址——这正是 Claude Code 的混合检索策略。
2. **命名即元数据**：本项目严格的目录/文件命名（`data/<域>/<主题>.yaml`、`articles/<id>.html`、`pv-<view>`、`hl-*` 锚点）本身就是"渐进披露"的信号，让 agent 据名字判断该不该读，省去全文扫描。
3. **分层结构**：把指令按小节组织（`CLAUDE.md` 的〈工程核心原则〉〈编务总则八条〉〈多语EN七原则〉），避免"一长墙"式提示。
4. **少而权威**：一个事实只有一个权威源（SQLite/YAML），杜绝在 JS/build.py 里硬编码副本——既是工程原则也是"控制上下文熵"。

**反模式（须避免）**：把整份数据塞进上下文；工具/脚本职责重叠导致"不知该用哪个"；一次性堆砌边缘案例当 few-shot。→ 应**策展一组多样化、典范性示例**。

---

## §2 进度记忆：把"心跳"外置

长时间运行 agent 会"失忆"，必须把状态**写在上下文窗口之外**并周期性回读。

| 机制 | 本项目实现 | 使用要点 |
|---|---|---|
| 进度流水（`claude-progress.txt`）| [`docs/next-phase-plan.md`](../docs/next-phase-plan.md) 的 L 系列批次登记 | **每完成一任务即更新**（编务总则 5·进度留痕）；写清"已完成项 / 校验结果 / 遗留 / 下一批梯队" |
| git 历史 | 描述性 commit（一次净态一提交）| 坏改动可 `git revert`、找回工作态 |
| 待办台账（`feature_list.json`）| `data/evolution/evolution_state.yaml` `registry` | 结构化、可排序；老化加权自动抬升长期搁置项优先级 |

> Anthropic 关键经验：待办用 **JSON/YAML 等结构化**而非 Markdown——模型更不易"顺手改写/删除"结构化文件；对决定完成的项，措辞要强硬（"删除/篡改测试是不可接受的"）。本项目据此把"是否真完成"交给**验证关卡**（§4），而非 agent 自述。

---

## §3 结构化记笔记（Agentic Memory）

**做法**：agent 定期把要点写成窗口外的笔记，之后再拉回上下文。等价于"维护一个 NOTES.md / to-do / memory 工具"。

本项目实现：
- **只追加台账**：`data/evolution/evolution_log.yaml`（每一次 auto/human/agent 动作一行、`seq` 单调递增、含 `before/after/evidence`）+ 人类可读 `docs/evolution/evolution_ledger.md`。
- **长期记忆库**：跨会话经验沉淀（`development_spec`、`learned_skill_experience`、`common_pitfalls_experience`、`important_decision_experience` 等类），任务开始/受阻时检索。
- **会话续接摘要**：长会话自动 compaction 时，本 `harness/` + `CLAUDE.md`〈当前进度〉充当"最小可续接外部记忆"，降低压缩失真导致的跑偏。

**铁律**：笔记/台账**只追加、不改写历史**（被否决的提议 `outcome: declined` 也要留痕，避免后人重复扰动）。

---

## §4 增量推进 + 自验证（一次一件事）

Anthropic 观察到的两大失败：①**一次想做太多**→中途耗尽上下文、留半成品；②**看到些进展就宣布完工**。对策：

1. **One feature at a time**：从 §2 待办台账选**单一最高优先项**做完做透。
2. **Leave clean state**：会话结束前留"可合并净态"（无重大 bug、有序、有文档），并 commit + 更新进度。
3. **Verify before "done"**：不得凭代码/自述判定完成——本项目用**三道闸 + 交互实测**（详见 [`tools.md`](tools.md)）：
   - `test_pipeline.py`（数据一致性）、`verify_demo.py`（构建产物）、`verify_sources.py`（来源可靠性）；
   - 交互/渲染态用 **headless Chrome `--dump-dom` / CDP** 以"真人用户"路径实测（对标文中"用浏览器自动化端到端验证"）。
4. **Zero-risk first**：先修复破损再做新功能；问题在**数据源头**解决，不在下游打补丁。

---

## §5 压缩（Compaction）

接近窗口上限时，**摘要会话内容并以摘要重启新窗口**，保留"架构决策 / 未解 bug / 实现要点"，丢弃冗余工具输出。本项目配合点：
- 优先"清理深层历史里的原始工具输出"（最安全的轻量压缩）；
- 把不可丢的决策/待核/边界**及时外置**到 `next-phase-plan.md` / `evolution_log.yaml` / 长期记忆，而非只留在对话里；
- compaction 调参先**最大化召回**再**提升精度**去冗余。

---

## §6 子代理架构（Sub-agents）

主 agent 持高层计划、**子 agent 用干净窗口做聚焦深活**，只回传浓缩结论（常 1–2k token），把大量检索上下文隔离在子代理内。本项目可用：
- `Agent` 工具派生 **Search / Debug / CodeReview / Browser** 等子代理（如"全面审计某文档""复现某渲染 bug"）；
- 主会话仅综合结论，避免自身上下文被检索噪声污染。
> Anthropic 指出这是"未来方向"（测试代理/QA代理/清理代理）——本项目〔待落地〕：可考虑固化"翻译审校子代理""来源核查子代理"专用 prompt。

---

## §7 Skills：把"程序性知识"打包成可加载能力

**Agent Skills** = 目录 + `SKILL.md`（指令 + 元数据 + 可选脚本/资源），按需**渐进加载**，不常驻上下文。这是本 harness 用 [`skills.md`](skills.md) 索引、并可用 `create-skill`/`skill-creator` 持续扩充的原因。原则：
- 技能承载**可复用的工作流知识**（怎么做翻译审校、怎么做引证核查），项目**事实**仍归 `data/`（各司其职，勿把数据塞进技能）。
- 优先复用官方/高安装量/来源可信的技能；低星/未知来源谨慎（见 [`skills.md`](skills.md) 质量判据）。

---

## §8 工具/MCP 设计（面向 agent 的接口）

工具是 agent 与其信息/动作空间之间的契约。原则（《Writing effective tools for agents》）：
- **自包含、抗错、用途单一明确**；输入参数描述性、无歧义。
- **最小可用工具集**：若人类工程师都无法判断某情境该用哪个工具，agent 更不能——避免功能重叠的"臃肿工具集"。
- 本项目既有良好范例：`db_reader.py`（唯一数据服务出口）、`build.py`（唯一渲染出口）、`verify_*`（唯一验收闸）——职责清晰、少重叠。

---

## §9 贯穿性元原则（与本项目宪法互证）

以上工程方法在本项目一律**服从** `CLAUDE.md`〈考证优先 / 严禁假信息 / 边界自知·局限留档 / 引用可点·出处可溯〉。即：**harness 提升的是"效率与连续性"，绝不用以牺牲"真实性与可溯源"为代价**；任何自动机制只发现、记录、排序，**绝不为消除待办而臆造或篡改研究内容**。
