# Coverage Map — 内容 / 代码 × 开发 / 维护 的全方位治理骨架

> **这是什么**：把 harness 提升为**整个项目"开发 + 维护"的单一治理框架**——不管对象是**内容**（研究语料 / 数据 / 文献 / 翻译 / 图谱）还是**代码**（ETL / build / web / scripts），都用同一张 2×2 地图说明"该用什么工作流、受哪些规矩、过哪些门禁、还欠什么"。
> **它不是什么**：不重复权威——规矩正文以 [`CLAUDE.md`](../CLAUDE.md) 为准（汇总索引见 [`rules.md`](rules.md)），工作流步骤以 [`workflows/`](workflows/) 为准。本图只做**坐标定位 + 缺口暴露**。
> **怎么用**：任意会话拿到任务，先在下面四格里定位它落在 `(域 × 生命周期)` 的哪一格，按该格的"资产→门禁→缺口"执行并留痕。

---

## 〇、两域四格总览

| | **开发（Creation）** | **维护（Maintenance）** |
|---|---|---|
| **内容域 Content** | **C-D** 采集→考证→著录→分级→多语→入架 | **C-M** 随时间保持正确·一致·无回退·积压可控 |
| **代码域 Code** | **K-D** 新脚本·新渲染器·新数据摄取·扩展构建 | **K-M** 防腐烂·依赖卫生·技术债·文档漂移·回归防护 |

> **横切两层**（服务全部四格）：**验证关卡**（[`workflows/verification.md`](workflows/verification.md)）+ **自我演化**（[`workflows/self-evolution.md`](workflows/self-evolution.md)）+ **部署/仓库治理**（[`workflows/deploy.md`](workflows/deploy.md)）。规矩总纲见 [`rules.md`](rules.md)。
> **正交关注面**：四格只答“操作对象×生命周期”；元治理/协作/行文/合规/成本/可发现性/语义互操作等**与四格正交的维度**见 [`concerns.md`](concerns.md)——定位完主格再扫一遍它，防“只见树木不见森林”。

---

## C-D · 内容域 × 开发 —— *项目的心脏*

**目标**：把佛学内容**经一手考证后**结构化落库（SQLite/YAML），可点溯源、中英（多语）必配、宁缺不伪。

| 维度 | 现状资产 |
|---|---|
| 工作流 | [`translation`](workflows/translation.md) · [`information-assurance`](workflows/information-assurance.md)（最前提）· [`academic-standards`](workflows/academic-standards.md) · [`bibliography`](workflows/bibliography.md)（P 轨）· [`data-pipeline`](workflows/data-pipeline.md)（摄取侧） |
| 规矩 | 编务总则八条 · 多语 EN 七原则 · 考证优先（详见 [`rules.md`](rules.md) §C/§E/§A） |
| 技能 | `academic-research-writer` · `citation-verification` · `research` ·（未来 `huayan-multilingual-en`/`huayan-source-audit`） |
| 门禁 | `verify_sources.py`（来源分级）· `test_pipeline.py`（人数/边数/地点一致）· `audit_bilingual.py` |

**〔缺口〕**
- [ ] P 轨仅覆盖 4/44 篇文档，其余 40+ 篇参考文献待规范化（见 backlog）。
- [ ] 讲记/扫描件 PDF → YAML 的摄取管线未固化（候选 `anthropics/skills@pdf`）。
- [ ] CBETA SIGLA 反查仍靠在线复制粘贴（→ 一手源离线化，见 [`tools.md`](tools.md) §四）。

## C-M · 内容域 × 维护 —— *让内容历久弥真*

**目标**：内容随时间保持**正确、跨文一致、无静默回退、待核积压可控**。

| 维度 | 现状资产 |
|---|---|
| 工作流 | [`information-assurance`](workflows/information-assurance.md)（复审）· [`bibliography`](workflows/bibliography.md) · [`self-evolution`](workflows/self-evolution.md) |
| 工具 | `self_evolve.py`（〔待核〕〔存疑〕标记扫描 + 老化加权优先级 + 只追加台账）· `verify_sources.py` · `--check-links` · [`docs/文献待核_backlog.md`](../docs/文献待核_backlog.md) |
| 规矩 | 边界自知·局限留档 · 进度留痕·计划滚动（[`rules.md`](rules.md) §C） |

**〔缺口〕**
- [ ] **跨文档一致性**：同一史实/名号在多篇 `docs/*.md` + 多处 YAML 出现，改一处易漏其余——无机械比对。候选：新建 `scripts/audit_consistency.py`（对关键断言跨文件比对）。
- [ ] **来源链接巡检**：CBETA/出版社 URL 偶发失效——`--check-links` 仅按需、未纳入周期闸。
- [ ] **存疑隔目抽检**：存疑降 boundary 后少数实为可补源待办（backlog §四已挂）。
- [ ] **P 轨覆盖率仪表盘**：把"已规范化文档/总数"作可量化指标入 `evolution_state`。

## K-D · 代码域 × 开发 —— *当前文档最薄的一格*

**目标**：新增/扩展 ETL、build、web 渲染器时，**源头治理、杜绝硬编码、可扩展优先**。

| 维度 | 现状资产 |
|---|---|
| 工作流 | [`data-pipeline`](workflows/data-pipeline.md) · [`web-ui`](workflows/web-ui.md) |
| 规矩 | 工程核心原则 1–4（知识图谱驱动 / 源头治理 / 灵活优先 / 杜绝硬编码）· 知识管理核心规则（Tab 权威源表 + 新增内容流程，[`rules.md`](rules.md) §B/§D） |
| 门禁 | `verify_demo.py`（产物 + `node --check` 内联 JS）· `test_pipeline.py` |

**〔缺口〕**
- [ ] **无编码规范文档**：Python（脚本命名/幂等/CLI 约定）与 JS（`*_RENDER` 扩展模式、`.en-line` 渲染约定、双写同步纪律）散落在代码注释与批次记录里，未成文。→ 拟建 [`workflows/code-conventions.md`](workflows/code-conventions.md)〔待落地〕。
- [ ] **测试策略单薄**：仅集成级（`test_pipeline`/`verify_demo`），缺对 `db_reader`/`import_*`/`build.py` 的**单元/回归测试**。候选 `obra/superpowers@test-driven-development`。
- [ ] **build.py 扩展配方**：`GAP_TOPICS_RENDER`/`WIZ_LIB_RENDER` 等"加新数据驱动页"的改法只在 next-phase-plan 的 L 批次里可考，无独立 recipe。

## K-M · 代码域 × 维护 —— *防腐与诚实*

**目标**：代码与**文档随代码同步**、依赖健康、技术债可追踪、不静默破损。

| 维度 | 现状资产 |
|---|---|
| 工作流 | [`verification`](workflows/verification.md) · [`deploy`](workflows/deploy.md) · [`self-evolution`](workflows/self-evolution.md) |
| 工具 | `self_evolve.py`（git 文件老化 + validator 汇总）· 工具治理留痕（如删遗留 `build_demo.py`） |

**〔缺口〕**
- [ ] **文档漂移（P1）**：[`docs/tech-stack.md`](../docs/tech-stack.md) + [`pyproject.toml`](../pyproject.toml) 声明 `sentence-transformers`/LanceDB/Ollama/Observable/SQLite-FTS5，但 `scripts/`+`src/` **0 实现**（neo4j 仅 `load_neo4j.py` 校验用）。要么落地、要么标"愿景·未建"、要么剔未用重依赖。
- [ ] **依赖卫生**：`pyproject` 里 `sentence-transformers` 属未用重依赖，徒增安装体积。
- [ ] **死文件巡检**：`index_single_page_backup.html`、`test.html` 等遗留物无定期清检（曾致 builder 输出路径碰撞）。
- [ ] **回归防护补强**：历史上"引入 JS 语法错误而 verify 仍 PASSED"已补 `node --check`；数据层等价盲区（导入非幂等）宜纳入 `test_pipeline`。

---

## 三、任务 → 格子 的快速路由

- "写一篇新研究 / 补一段翻译" → **C-D**
- "这篇文献的 CBETA 号对不对 / 存疑怎么处理" → **C-D**（著录）↔ **C-M**（复审）
- "把某篇 docs 注册成独立文章 / 加一个 Tab 视图" → **K-D**（+ C-D 供数据）
- "改完站点哪里坏了 / tech-stack 和代码不一致" → **K-M**
- "同一史实两篇文档打架" → **C-M**（跨文一致性·缺口，暂手动）
- "每次会话收尾" → **横切·自我演化**（`make evolve`）

## 四、如何扩展本骨架

- 新增能力先问"落在哪一格"，在对应格补一行资产；发现重复劳动/盲区即在缺格加一条 `〔缺口〕`，并视价值升格为 `workflows/*` 或 `scripts/*`。
- 四格的**开发**面偏"工作流 + 技能"，**维护**面偏"self_evolve + 门禁 + 台账"；任何新工具都应在 [`tools.md`](tools.md) 登记、新规矩在 [`rules.md`](rules.md) 登记。
- 一致性铁律不变：本目录一切服从 [`CLAUDE.md`](../CLAUDE.md)〈考证优先 / 严禁假信息 / 边界自知〉；自动机制只发现、记录、排序，**绝不为消除待办而臆造或篡改**。
