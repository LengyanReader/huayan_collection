# Concerns — 正交关注面 · 让 harness 覆盖"方方面面"

> **定位**：[`coverage-map.md`](coverage-map.md) 的 2×2（内容/代码 × 开发/维护）是**主轴**——回答"操作对象 × 生命周期"。但项目实际遇到的治理维度是**正交**于此的：元治理、协作、行文、合规、成本、可发现性、语义互操作……本文件把它们**逐条登记为卡片**，每卡片回答：**这是什么 · 落于哪几格 · 现有资产 · 〔缺口〕**。
> **用法**：拿到任务先在 coverage-map 定位主格，再回到本表扫一遍相关关注面——避免只见树木不见森林。任何新维度即在此加卡片，勿另起文件。
> **连接不重复**：规矩总纲见 [`rules.md`](rules.md)，工具/技能/来源分别见对应文档；本表只做**坐标 + 缺口**。

---

## §1 元治理 · Harness 自身如何演化 (Governance-of-Governance)

**是什么**：harness 自己也是被治理对象——需要节律地回顾、修订、扩展，否则会与项目实际漂移。

| 落于 | 现有资产 | 〔缺口〕 |
|---|---|---|
| 全部格 | `principles.md` §9 元原则·`sources.md` §四 backlog·`docs/next-phase-plan.md` 心跳·`/better-harness` 技能可用 | [ ] 未建立**周期性 harness 审计节奏**（如每 N 批次或每季跑一次 `/better-harness`）<br>[ ] coverage-map 的〔缺口〕登记**无老化加权**（自身也应纳入 self_evolve 视野）<br>[ ] rules.md 与 CLAUDE.md 若漂移，无自动检测 |

**建议路径**：把"扫描 harness/ 文件的 git 年龄 + 检查 rules.md 引用是否仍指到存在的文件"作为 `self_evolve` 的一条子传感器。

---

## §2 协作 · 会话与用户接口 (Collaboration & Session)

**是什么**：agent 与用户（及其未来的其它 agent/合作者）之间的**协议**——沟通节奏、决策升级、偏好、边界、提交/推送规则。

| 落于 | 现有资产 | 〔缺口〕 |
|---|---|---|
| 四格通用 | `README.md` §四 Session Protocol·`principles.md` §4 增量+自验证·长期记忆〈NEVER auto-push〉〈提交可自动推送仅在明确指示时〉·`AskUserQuestion` 决策分叉工具 | [ ] **用户偏好档案**未成文（语言/风格/详略/主动性偏好）——目前全散在长期记忆里<br>[ ] **决策升级阶梯**未定义：什么情况下直接办、什么情况下问、什么情况下拒办<br>[ ] **多 agent 交接协议**空缺（若日后引入子 agent 或人类协作者）<br>[ ] **冲突解决**：CLAUDE.md vs 用户当轮指令 vs 长期记忆 的优先级规则仅隐含，未明文 |

**建议路径**：新建 `harness/collaboration.md`（若此 concern 被激活）：定义"直接办/询问/拒办"三档判据 + 偏好卡片 + 冲突解决顺位。当前用户偏好主要靠记忆系统承载，可暂维持。

---

## §3 认知质量 · 行文与文体 (Cognitive Quality & Voice)

**是什么**：产出**内容**在语言、结构、思维严谨度上的品质；反 AI 腔、反套话、保持学者手感。

| 落于 | 现有资产 | 〔缺口〕 |
|---|---|---|
| 主 C-D | L.㊽ **文体凡例八条**（章节落事实不收格言、加粗只留表格、段落参差、不用"首先/其次/最后"套话）· L.㊾ 语域学术化 + 文言残留归零 · 观点溯源七类标注（推论/评估/论证/主张/预测/立场/总结 + 逐条注依据）· `zh-academic-register` 技能 · GB/T 15835 数字规范 · 加粗密度指标（曾 10.97→9.50 每千字）· `citation-verification` · 论断强度校准（"决定"→"自然体现"） | [ ] **未纳入 rules.md**——文体凡例是 L.㊽ 具体批次的经验，尚未升格为常设规矩<br>[ ] **无自动检查**：套话/加粗密度/文言残留/CJK-in-EN 泄漏——全靠人工回看<br>[ ] **EN 端文体规范**缺（中文有凡例，英文无）<br>[ ] 反幻觉的"不表演式坦白/不虚构细节"仅散在批次记录 |

**建议路径**：①把文体凡例八条 + 观点溯源七类 + 论断强度校准并入 `rules.md §I 行文与文体`；②建 `scripts/audit_style.py` 扫描套话/加粗密度/文言残留；③用 `zh-academic-register` 技能承接改写工作。

---

## §4 合规 · 版权 · 伦理 (Compliance · Copyright · Ethics)

**是什么**：本项目大量使用祖师讲记、今人译著、CBETA/84000 数字化文本、YouTube/Bilibili 链接、微信文章抓取——**版权归属、引用合理范围、宗教内容的表述伦理**都需要边界。

| 落于 | 现有资产 | 〔缺口〕 |
|---|---|---|
| 主 C-D/C-M | `LICENSE` 文件（顶层）· 编务总则 C7 引用可点·出处可溯 · 〔无法获取〕受限标注 · 一手 vs 二手分级 · 祖师语录正文保中文、EN 转述（E4 惯例，避免二次翻译失真） | [ ] **LICENSE 与各引用条款的一致性**未审计（本项目 LICENSE 是什么？与 CBETA/84000 使用条款兼容否？）<br>[ ] **海云继梦讲记/梦参開示等现代法师语录**的转载授权边界未明确<br>[ ] **YouTube/Bilibili 播放列表外链**若失效或视频下架，无处置规约<br>[ ] **微信文章抓取**（`fetch_wechat_articles.py`）的 robots/授权现状未评估<br>[ ] **宗派立场表述伦理**：涉"佛门真伪""判教"等议题，如何避免贬抑他宗？现仅靠〈多译本并存·考据成一〉隐式承担 |

**建议路径**：新建 `harness/compliance.md`（或升为 `workflows/compliance.md`）——列引用条款表 + 各外部资源许可快照 + 敏感议题表述准则。当前 concern 处于**空白**，属高优先待补。

---

## §5 资源 · 性能 · 成本 (Resource · Performance · Cost)

**是什么**：上下文窗口是**有限预算**；构建脚本耗时/依赖大小；外部 API 配额与不可达；静态站产物体积。

| 落于 | 现有资产 | 〔缺口〕 |
|---|---|---|
| 全格横切 | `principles.md` §1 上下文腐坏/注意力预算 · §5 compaction · `tools.md` §五 Windows/pwsh 约束 · 单一 builder 治理 · `self_evolve --no-validators` 离线快检 | [ ] **构建时长/产物大小无监控**（build 现 ~23 MB / 34 files，无增长趋势线）<br>[ ] **每会话 token 消耗**未记录，无法据以决定何时主动 compaction<br>[ ] **外部 API 不可达时的降级策略**仅 84000 一条经验，未成文<br>[ ] `pyproject.toml` **依赖体积**——含未用的 sentence-transformers 等重依赖（见 coverage-map K-M）<br>[ ] **headless Chrome 冷启动**/CDP 偶发 10053 不稳（L.㊻ 曾提"绕 CDP 用 dump-dom"）——经验未升为规程 |

**建议路径**：把"build 产物字节 + 时长"、"self_evolve 健康度"作为可追踪时间序列入 `evolution_state.yaml`；建立"外部源不可达时的绕行清单"文档。

---

## §6 可发现性 · 影响力 · 体验 (Discoverability · Impact · UX)

**是什么**：内容做得再好，读者找不到/看不懂/进不去=影响力打折。覆盖：站内导航、搜索、SEO、社交分享、无障碍、移动适配、多语读者。

| 落于 | 现有资产 | 〔缺口〕 |
|---|---|---|
| 主 C-M · 亦 K-D | `web-ui` 工作流 · `navigation.yaml` 数据驱动侧栏 · `articleChip` 视图入口 · 双语链 `.en-line`+`_markEnBlocks` · 🔗 分享地址按钮（L.㊷） · 6 Tab + 独立文章 URL · GitHub Pages | [ ] **无全局搜索**（P1·见 coverage-map；SQLite FTS5 已声明未 surface）<br>[ ] **文档间交叉引用无索引页**——44 篇 docs + 25 篇文章之间的引用关系不可视<br>[ ] **SEO**：无 sitemap.xml、无 meta description 规范、无 OG 卡片<br>[ ] **无障碍 (a111) 未评估**（键盘导航/屏幕阅读器/色盲友好）<br>[ ] **移动视口**未审<br>[ ] **社交/学术可引用性**：无 DOI/无引用导出（BibTeX/CSL）<br>[ ] **首次访客引导**：无 landing 导览、无"从哪读起"路径 |

**建议路径**：短期把全局搜索（coverage-map 已列 P1）+ sitemap + meta 三件事做掉；中期引 reader-first 的 landing 路径与跨文引用可视化。

---

## §7 数据 · 元数据 · 语义互操作 (Data · Metadata · Semantic Interop)

**是什么**：知识图谱的 schema 演化、实体标识的稳定性、与外部标准的对齐（CIDOC-CRM / Bibliographic / TEI / IIIF）——决定本项目能否与更大的数字人文生态握手。

| 落于 | 现有资产 | 〔缺口〕 |
|---|---|---|
| 主 C-D · 深度影响 K-D | `data/knowledge_graph/schemas/` · SQLite 表结构（persons/texts/chapters/locations/glossary/lineages/lineage_edges）· Neo4j 校验层 · CBETA TxxnXXXX SIGLA 作外部锚点 · `graph.json` 导出 | [ ] **实体 ID 稳定性策略**未成文（曾出现 `person_050` 锚点错位 L.㉘）<br>[ ] **schema 版本化**：字段增删无迁移脚本/无 semver<br>[ ] **与外部标准对齐**：BDRC/CIDOC-CRM/TEI header 是否引入？暂无<br>[ ] **IIIF** 图像互操作（涉艺术珍品/古籍扫描时）未评估<br>[ ] **权威名称档**（Authority Files）：人名/地名/书名的规范形式无中央登记（`bilingual_glossary.yaml`/`search_aliases.yaml` 只是片段）<br>[ ] **多语术语的可重用发布**：术语表未导出为 SKOS/RDF |

**建议路径**：把 schema 演进纳入 `docs/architecture.md`；建 `data/authority/*.yaml`（人/地/书/术语规范化档）；关注 BDRC/VTGS、Numata Center 等近期动向。

---

## 五、七面 × 四格 的矩阵视图（备览）

| Concern | C-D | C-M | K-D | K-M |
|---|:-:|:-:|:-:|:-:|
| §1 元治理 | △ | ● | ● | ● |
| §2 协作 | ● | ● | ● | ● |
| §3 行文 | ● | ● | ○ | ○ |
| §4 合规 | ● | ● | ○ | △ |
| §5 成本 | ● | △ | ● | ● |
| §6 可发现 | ○ | ● | ● | △ |
| §7 语义互操 | ● | △ | ● | △ |

●=该格直接受影响 · △=轻度 · ○=较少

---

## 六、如何扩展本 concern 集

- **新增关注面**（若日后涌现，如"跨站点联合"、"协作翻译社区"、"AI 生成内容合规"等）：在此加一节即可，勿另起文件。
- **升格路径**：某 concern 若已积累足够资产与配方，可拆出成 `workflows/<concern>.md` 或独立 `harness/<concern>.md`；本表保留一行摘要与链接。
- **降级路径**：concern 若被证伪或合并，标 `〔已并入 §X〕` 保留历史，不删卡（承台账只追加原则）。
- **纪律**：本表每卡的〔缺口〕即 backlog 种子——但**不声称已具备**（承 `rules.md §H3`）。

---

> **一句话**：coverage-map 管"打哪一格"，rules 管"守什么规矩"，**concerns 管"别看漏了哪些面"**。三者合一，harness 才真正配得上"全方位赋能开发维护"这个定位。
