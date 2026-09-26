# Skills — 技能目录（已装 / 可装 / 造 / 用）

> Agent Skill = 一个含 `SKILL.md` 的目录，按需**渐进加载**的"程序性知识 + 可选脚本"。本目录只装**与本项目相关**的技能，并给出"何时用哪张"。
> 本机技能目录：`C:\Users\data\.agents\skills\`（用户级）。项目级技能可放仓库 `.claude/skills/`〔待落地，若要随仓库分发〕。

---

## 一、已安装 · 与本项目直接相关 ✅

| 技能 | 何时用 | 支撑工作流 | 备注 |
|---|---|---|---|
| **academic-research-writer** | 写研究文档/文献综述/专题，需同行评审来源 + IEEE 标准参考文献 | 学术规范·翻译 | 强制核实来源可信度——与〈考证优先〉一致 |
| **citation-verification** | 引证核查最佳实践、防伪造引用、常见错误模式 | 信息保证·学术规范 | 与 `verify_sources.py` 互补（人/规约层） |
| **research** | 就某问题对照一手高信源调研，并把结论落成仓库内 Markdown | 信息保证·学术规范 | 契合"分派背景调研给子代理"模式（见 principles §6）|
| **frontend-design** | 建/改 UI 时做有意图的视觉与排版决策 | （Demo 前端）| 本项目纯 HTML/CSS/JS + Canvas + Leaflet |
| **create-skill** / **skill-creator** | 把本项目反复出现的工作流（如"多语EN审校""品目差异对勘"）固化为**自定义技能** | 自我演化·扩展 | 造新能力的入口；见第四节 |
| **create-plugin** | 把 SKILL.md / 市场技能 / 现有文件夹打包成可分发 Qoder 插件 | 扩展 | 若要团队内复用某能力 |
| **create-subagent** | 建聚焦子代理（翻译审校代理、来源核查代理、清理代理）| 扩展 | 落地 principles §6〔待落地〕|
| **find-skills** | 需要新能力时，检索开放技能生态并评估质量后再装 | 扩展 | 装前先查安装量/来源/星数（第三节）|
| **vercel-deploy** | （可选）自动化部署 Web 项目 | 部署 | 本项目当前走 GitHub Pages，按需〔待评估〕|

## 二、已安装 · 与本项目当前无关（暂不使用）⏸️

`ai-image-generation` · `ai-music` · `ai-video-generation` · `image-to-video` · `video-edit` · `brandkit` · `remotion-best-practices` · `huashu-nuwa` · `canvas` · `better-harness`
> 保留不动（用户级共享）；若日后需要为 Demo 生成配图/梵呗音频，再启用相应技能。**不因其存在而引入无关上下文**（上下文工程：最小高信号集）。
> 例外：`better-harness` 可**用于周期性审视本 harness 本身**（生命周期/重复劳动/资产/会话产出/修复计划），按需 `/better-harness` 触发〔待评估〕。

---

## 三、生态里"值得考虑安装"的候选 📥（尚未在本机 · 〔待评估〕）

> **本轮 (2026-09-26) 已实跑** `WebFetch https://skills.sh/`（榜单位 · 全部为 **verified install counts**）+ 若干 `WebSearch`；下表列 **install 数与来源均为实测事实**，未安装者仍标〔待评估〕，遵〈未装者不声称已具备〉。
> 安装命令模板（用户级、跳过确认）：
> ```bash
> npx skills add <owner/repo@skill> -g -y
> npx skills find <关键词>          # 若需再检索细分
> npx skills check / update
> ```

### 3.1 直接对齐本项目现有工作流的高价值候选 ⭐

| 面向工作流 | 技能 (owner/repo@skill) | Install | 一举补哪一块 |
|---|---|---:|---|
| 验证关卡·DoD 门禁 | `obra/superpowers@verification-before-completion` | 221K | 把 `principles.md §4`「未验不声称完成」打包成可加载技能；补 `verify_demo/test_pipeline` 之上的**流程判据层** |
| 数据管线 TDD | `obra/superpowers@test-driven-development` | 236K | 为 `scripts/*.py` + `build.py` 建立红-绿-重构节律，补强 `test_pipeline.py` |
| 子代理深潜 | `obra/superpowers@subagent-driven-development` | 214K | 落地 `principles.md §6`「主 agent 计划·子 agent 浓缩结论」 |
| 并行分派 | `obra/superpowers@dispatching-parallel-agents` | 199K | P 轨多文档批量核验 / 多稿审计 |
| 系统化调试 | `obra/superpowers@systematic-debugging` | 271K | 渲染/构建破损时（曾 L.㊾⑭ 类问题） |
| 交互实测 | `vercel-labs/agent-browser` | 944K | **替代现用 headless Chrome 手搓 CDP**；tools.md §一「真点为验」标准化 |
| 文档解析（讲记/扫描件）| `anthropics/skills@pdf` | 201K | 支撑 `extract_hy_refs.py`/`ocr_hy_refs.py` 上游 PDF 拆分 |
| 报告出稿 | `anthropics/skills@pptx` | 226K | 研究结论转讲义/弘法幻灯片 |
| 造 / 打磨技能 | `anthropics/skills@skill-creator` | 391K | 落地 §四 4 个专属技能（`huayan-multilingual-en` 等） |
| 前端视觉决策 | `anthropics/skills@frontend-design` | 923K | 已装；若重设计 tabs 复用 |

### 3.2 学术/研究工作流（本项目〈考证优先〉的上游）

| 需求 | 技能 | Install | 用途 |
|---|---|---:|---|
| 读论文/背景一次到位 | `lllllllama/rigorpilot-skills@paper-context-resolver` | 451K | 识与心灵二篇 意识科学/心理学 参考文献 [B] 层的**批量一手反查** |
| 项目结构勘察 | `lllllllama/rigorpilot-skills@analyze-project` | 311K | 新会话上手时的定向（对齐 README §四 Session Protocol 步 1）|
| 复现他人研究 | `lllllllama/rigorpilot-skills@ai-research-reproduction` | 311K | 佛学 x 意识科学 x 心理学跨学科论文的对照复现 |
| 仓库接入规划 | `lllllllama/rigorpilot-skills@repo-intake-and-plan` | 450K | 若要并入外部语料/新子库 |

### 3.3 写作·编辑（研究正文的成形）

| 需求 | 技能 | Install | 用途 |
|---|---|---:|---|
| 文章级打磨 | `mattpocock/skills@edit-article` | 198K | 综合深度研究.md 定稿前 |
| 结构塑形 | `mattpocock/skills@writing-shape` | 384K | 论证骨架（配合 `nature-writing`）|
| 素材切片 | `mattpocock/skills@writing-fragments` | 383K | 从笔记→段落 |
| 面向 agent 的写 | `mattpocock/skills@writing-for-agents` | 318K | **写本 harness / SKILL.md 本身** |
| 造技能的文风 | `mattpocock/skills@writing-great-skills` | 324K | §四 造技能时的风格基线 |
| 领域建模 | `mattpocock/skills@domain-modeling` | 700K | 图谱 schema / YAML 域的边界打磨 |
| 代码库设计 | `mattpocock/skills@codebase-design` | 678K | `src/etl/graph/translation` 分层复审 |

### 3.4 知识管理 · 长期笔记生态

| 需求 | 技能 | Install | 用途 |
|---|---|---:|---|
| Obsidian 库联动 | `mattpocock/skills@obsidian-vault` | 202K | `docs/huayanhai/My Notes/`（28 文件）已接近 Obsidian 兼容；接入后可双链/图谱与 `data/knowledge_graph/` 联动 |
| 教学/讲授 | `mattpocock/skills@teach` | 712K | 讲记→讲义→课程的转换（配合 haiyun_* 资源）|

### 3.5 数据采集 / 来源抓取

| 需求 | 技能 | Install | 用途 |
|---|---|---:|---|
| 结构化抓取 | `scrapegraphai/just-scrape` | 245K | 替代/补强 `fetch_wechat_articles.py`/`fetch_wechat_chain.py`，抗站点改版 |

### 3.6 明确**不建议**装的（避免上下文熵）⛔

- `microsoft/azure-skills`、`supabase/agent-skills`、`prisma/skills`、`heygen-com/hyperframes`、`genmedia-labs/*`、`prime-skills/runcomfy-agent-skills`、`flowkit-labs/reddit-automation`、`coreyhaines31/marketingskills`、`leonxlnx/taste-skill` — 与本项目（本地 SQLite + 静态 HTML + 佛学数字人文）无关，装了只污染工具选择的清晰度（`principles.md §8` 最小工具集）。

### 3.7 生态外的**一手数据源**优化（配合工具层，见 [`tools.md`](tools.md) §四）

- **CBETA 离线全文**：`https://cbeta.org/en/downloads`（官方**下载 TEI-XML 全库**）——把 P 轨/`verify_sources` 的 CBETA 反查**从在线复制粘贴升为本地 grep/XML 解析**，同时缓解"84000 常直连不通"。
- **c-text 开放数据**：`https://ctext.org/digital-humanities`（bulk 下载结构化 XML）——先秦两汉/魏晋思潮对照源。
- **84000 Reading Room**：`https://84000.co/reading-room`（多语对照·可离线包）——藏传/梵文对勘。

> ⚠️ 依〈考证优先/严禁假信息〉：**未实际安装并验证的技能，不在本项目文档里声称"已具备"**——本表全部标〔待评估〕即为遵此。

---

## 四、为本项目"造"专属技能 🔧（最高杠杆的扩展路径）

反复出现的编务，适合沉淀成**项目专属技能**（用 `create-skill` / `skill-creator`），把 `CLAUDE.md` 的原则变成可一键加载、带脚本校验的操作手册。候选（〔待落地〕，按价值排序）：

1. **`huayan-multilingual-en`** — 多语 EN 著录与审校：注入〈多语EN七原则〉+ 固定术语表 + YAML 转义纪律 + `.en-line`/`_markEnBlocks` 渲染约定 + "重实质不逐字/无对应即明示〔待核〕"门禁清单。
2. **`huayan-source-audit`** — 来源考证：一手源（CBETA/84000/原典）对勘流程 + 三级来源分级 + `verify_sources.py` 调用 + 〔待核〕/〔存疑〕/〔线索〕标注规范 + "引用可点 `[text](url)`→`_dynMD`"。
3. **`huayan-item-diff`** — 品目/译本差异对勘：Toh44 45 品 vs 汉文 39 品、四种译本对照行的既有范式复用。
4. **`huayan-static-build-verify`** — 数据源→`build.py`→`verify_demo`/`test_pipeline`→headless CDP 实测的收尾闭环脚本化。

> 造技能的度规（承接 principles §7/§8）：**技能装"怎么做"（流程+脚本+判据），不装"是什么"（研究事实留在 `data/`）**；一个技能职责单一、触发描述清晰，避免与既有技能重叠。

---

## 五、技能 × 工作流 × 记忆 的协同

- **技能**给"标准动作"；**记忆库**（`development_spec`/`learned_skill_experience`/`common_pitfalls`）给"本项目特有约束与踩坑"；**`harness/workflows/*`** 把两者与**工具/门禁**编排成端到端配方。
- 典型：做翻译批次 → 加载 `academic-research-writer` +（未来的 `huayan-multilingual-en`）→ 检索记忆〈CJK 编码与子进程安全约定〉〈多语EN翻译原则〉→ 按 `workflows/translation.md` 步骤 → 过 `verify_demo` 闸 → `make evolve` + 更新 `next-phase-plan.md`。
