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

> 以下为方向性候选；**安装前务必**用 `find-skills` 核对**安装量(≥1K 优先)/来源信誉/GitHub 星数**，勿凭搜索标题就装。安装命令模板：
> ```bash
> npx skills add <owner/repo@skill> -g -y      # -g 用户级；-y 跳过确认
> npx skills find <关键词>                       # 关键词检索
> npx skills check / update                     # 检查/更新已装技能
> ```
> 浏览：https://skills.sh/ · 官方：`anthropics/skills`（文档处理 pdf/docx/xlsx/pptx、frontend-design 等）

| 需求方向 | 候选类型 | 用途（本项目） |
|---|---|---|
| 文档处理 | anthropics 官方 `pdf` / `docx` / `xlsx` | 解析祖师大德讲记 PDF / 扫描版 CBETA 对照，抽取入 YAML |
| 本地化 QA | `l10n` / `i18n` 质量类技能 | 多语对读字段一致性、占位符/术语校验（补充自建 `_markEnBlocks`）|
| 学术引用 | BibTeX / 引用导出类 | 把 `bibliography.yaml` 导出为标准参考文献格式 |
| 数据管道 | `pytest` / data-validation（great_expectations 类）| 强化 `test_pipeline.py` 之外的 schema/期望校验 |

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
