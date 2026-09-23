# Sources — 参考来源 · 检索记录 · 扩充待办

> 依〈考证优先 / 引用可点〉：本 harness 引用的外部方法**一律给可点来源**；本项目**尚未落实**者标〔待落地〕，不假装已具备。

## 一、方法论来源（外部·一手）

| 来源 | 链接 | 用于 |
|---|---|---|
| Anthropic — *Effective harnesses for long-running agents*（2025-11-26）| https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents | [`principles.md`](principles.md) §2/§4：initializer+coding agent、`feature_list.json`、一次一特性、净态、自验证、子代理未来向 |
| Anthropic — *Effective context engineering for AI agents*（2025）| https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents | §1 上下文腐坏/注意力预算/最小高信号集、§5 compaction、结构化记笔记、子代理、just-in-time 检索 |
| Anthropic — *Equipping agents for the real world with Agent Skills*（2025-10-16）| https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills | §7 Skills 渐进加载 |
| Anthropic — *Writing effective tools for AI agents*（2025-09-11）| https://www.anthropic.com/engineering/writing-tools-for-agents | §8 工具/MCP 设计（自包含·无歧义·最小工具集）|
| Agent Skills 规范 · Claude Platform Docs | https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview | 技能=目录+SKILL.md+资源 |
| skills.sh（开放技能生态/包管理 `npx skills`）| https://skills.sh/ | [`skills.md`](skills.md) §三 安装/检索 |

**取回留证**：前两篇长文已抓取存档于本机 `…/agent-tools/8400b1ce/9176c70e.txt`、`fb7f1c54.txt`（会话内缓存，非仓库文件）。〔可选〕如需仓库内长期留存，可另存 `harness/refs/` 摘要卡。

## 二、项目内权威源（本 harness 只连接、不重述）

- [`CLAUDE.md`](../CLAUDE.md) — 宪法：概述·进度·工程核心原则·编务总则八条·多语EN七原则·知识管理规则·目录约定。
- [`docs/next-phase-plan.md`](../docs/next-phase-plan.md) — 心跳：L 系列批次滚动登记（进度权威源）。
- [`docs/self-evolution.md`](../docs/self-evolution.md) — 免疫与记忆：闭环设计。
- [`docs/verification-framework.md`](../docs/verification-framework.md) · [`docs/reference-management.md`](../docs/reference-management.md) · [`docs/knowledge-management.md`](../docs/knowledge-management.md) · [`docs/engineering-workflow.md`](../docs/engineering-workflow.md) · [`docs/translation-guide.md`](../docs/translation-guide.md) · [`docs/multilingual-alignment.md`](../docs/multilingual-alignment.md) · [`docs/architecture.md`](../docs/architecture.md) · [`docs/tech-stack.md`](../docs/tech-stack.md)。
- `scripts/verify_*.py` · `test_pipeline.py` · `self_evolve.py` · `web/demo/scripts/build.py` — 验收闸与引擎。

> 上列批次号引用（L.㉝ / L.㊾⑭ 等）出处为 `docs/next-phase-plan.md`，为其**权威源**；本 harness 仅指向，不复述其变更明细。

## 三、检索记录（本轮）

- 2026-09-23：`WebSearch` 命中 Anthropic 工程长文两篇 + Agent Skills 生态 → `WebFetch` 抓取 harnesses / context-engineering 两篇正文（awesome-agent-skills 列表页抓取超时失败，未据以立项，故第三节候选仅列方向、标〔待评估〕未声称已装）。
- `npx skills find`（联网检索具体技能）在本环境**被中断/未成功**，故 `skills.md` §三的"可安装候选"为**方向性建议**，安装命令为**待执行**，非既成事实。
- 2026-09-23（覆盖度复审）：应"double check 是否全面且深入"再审计——比对 `scripts/`（23 脚本）与 `web/demo/src/`（10 JS）实际资产，发现初版遗漏两个工程量最大的面→新增 `workflows/data-pipeline.md`、`workflows/web-ui.md`，并补全 `tools.md` §1b 脚本清单（审计/回填/抓取/OCR）。复审均为**实读代码/脚本名与行号**为据，未臆断。
- 2026-09-23（待核项证据核实）：跟踪 `build_demo.py`——**纠正**初版误写（“产 graph JSON”）：它内联 GRAPH/GAP 写 **旧单页 `web/demo/index.html`**；`graph.json` 实由 `export_sqlite_to_json.py` 生成；`build.py` 才是当前 `index.html`+tabs 的产物源。build_demo.py 全仓无引用→确认遗留，且与 build.py **输出路径碰撞**（误跑覆首页）。

## 四、扩充待办（backlog · 供后续会话逐项推进）

- [ ] 〔待落地〕用 `create-skill` 固化 4 个专属技能：`huayan-multilingual-en` / `huayan-source-audit` / `huayan-item-diff` / `huayan-static-build-verify`（见 `skills.md` §四）。
- [ ] 〔待落地〕`create-subagent` 建"翻译审校代理""来源核查代理"（principles §6）。
- [ ] 〔待评估〕`npx skills find` 实际检索并安装：文档处理(pdf/docx，解析讲记/扫描对照)、l10n QA、BibTeX 导出、data-validation。装前核对安装量/来源/星数。
- [ ] 〔待评估〕是否引入重型 MCP（浏览器自动化 Puppeteer/Playwright 以强化交互实测；Neo4j MCP）。
- [ ] 〔待评估〕项目级技能目录 `.claude/skills/`（随仓库分发），与用户级技能如何分工。
- [x] 〔已完成·工具治理〕`scripts/build_demo.py` = 遗留旧单页 demo 生成器→**已 `git rm` 删除**（写 `web/demo/index.html`与 build.py 碰撞；全仓无引用；graph.json 实由 export_sqlite_to_json.py 产出。可经 git 历史恢复）。
- [x] 〔已完成·工具缺口〕Makefile 新增 `verify-all`（串 test-pipeline+demo-verify+verify-sources）与 `test-pipeline` 目标。
- [x] 〔已完成·部署隐患〕`demo-deploy` 改为暂存整个 `web/demo/`，并加提示：讲法正文 txt 需另提交。
- [x] 〔已完成〕新建 `workflows/deploy.md`（Pages 源=main 根·CRLF/LF·CDN·发布步骤，只连接 next-phase-plan 既定事实）。
- [x] 〔已完成〕抽出 `workflows/verification.md`（三道闸+`make verify-all`+交互实测/CDP 退化+缓存陷阱）。
- [x] 〔已完成·存疑分级〕依编务约定区分：〔待核〕=真待办(verify/sev4)、〔存疑〕=审慎判定(boundary/sev2)；并修 `act_registry` 重见时刷新 kind/severity 以同 config 基因组。
- [ ] 〔新见〕存疑降为 boundary 后，需人工隔目抽检：数据层少数〔存疑〕或实为可补源的待办（现一律计为边界，可忍，因不丢只降噪）。
- [ ] 〔可选〕周期性 `/better-harness` 审视本 harness（重复劳动/资产/会话产出/修复计划）。
- [ ] 〔待落地〕用 `create-skill` 固化 4 个专属技能（详 §一）· `create-subagent` 建翻译审校/来源核查代理·实跑 `npx skills find` 装候选·评估重型 MCP·项目级 `.claude/skills/` 分工。
