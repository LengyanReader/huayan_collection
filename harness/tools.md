# Tools — 工具·验证关卡·子代理·MCP·环境约束

> 本项目 agent 可用的"手"。原则（principles §8）：工具职责单一、少重叠；**验证关卡是"是否完成"的唯一裁决者**，不靠 agent 自述。

---

## 一、验证关卡（Definition of Done）🚦

任何触碰数据/构建产物的改动，收尾前须按需全绿。**一条命令跑齐三道闸**：`make verify-all`（= `test-pipeline` + `demo-verify` + `verify-sources`）。详见 [`workflows/verification.md`](workflows/verification.md)。

| 关卡 | 命令 | 检查什么 | 何时必跑 |
|---|---|---|---|
| **数据一致性** | `python scripts/test_pipeline.py` | 人数/边数/地点等全链路一致（95人/98边/30地…）| 涉 `data/**`、SQLite、导入导出 |
| **构建产物** | `python scripts/verify_demo.py` | 各 tab/article HTML 生成、数据驱动页、内联 JS 语法（node --check）| 每次 `build.py` 之后 |
| **来源可靠性** | `python scripts/verify_sources.py [--json]` | 来源分级评分、缺源/待核统计 | 涉史实/名号/年代/出处/引文 |
| **图谱验证** | `python scripts/load_neo4j.py --verify-sqlite` | SQLite→图结构（无需服务器）| 涉传承边/关系 |
| **交互/渲染实测** | headless Chrome `--dump-dom` / CDP | 以"真人用户"路径验证展开/切换/显隐等**运行态** | 涉 JS 交互、折叠门、语言开关、渲染修复 |
| **进化体检** | `python scripts/self_evolve.py` | 汇总上述关卡 + 待核积压 + 台账矛盾 → 健康度 | 每次会话收尾 |

> 交互态**必须真点为验**（记忆〈Interactive State Verification Requirement〉）：静态字符串命中 ≠ 功能正常；曾出现"引入 JS 语法错误而 verify_demo 仍 PASSED"，故 verify_demo 已含 node --check 反向验证（见 `docs/next-phase-plan.md` L.㊾⑭）。

**构建/数据主命令**：`init_db.py` · `import_all_to_sqlite.py` · `db_reader.py` · `export_sqlite_to_json.py --verify` · `web/demo/scripts/build.py`（链详见 [`workflows/data-pipeline.md`](workflows/data-pipeline.md)）。

### 1b. 数据摄取 · 补证 · 审计脚本（scripts/，供各工作流复用）

| 脚本 | 用途 | 归属工作流 |
|---|---|---|
| `import_all_to_sqlite.py` / `export_sqlite_to_json.py` / `db_reader.py` | 多源合并导入 / SQLite↔JSON 往返(`--verify`) / 数据服务唯一出口 | data-pipeline |
| `backfill_core_sources.py` · `backfill_secondary_sources.py` · `backfill_location_sources.py` · `backfill_chapters_title_en.py` · `add_works_links.py` | 幂等**来源/链接补证回填** | information-assurance |
| `audit_bilingual.py` · `audit_classify.py` | 中英配对 / 分类**审计** | translation · data-pipeline |
| `fetch_wechat_articles.py` · `fetch_wechat_chain.py` | 网页/微信原文**抓取** | information-assurance |
| `extract_hy_refs.py` · `ocr_hy_refs.py` | `docs/hy_refs` **提取 + OCR 校对**（人工审，非直用）| information-assurance |
| `append_entries.py`(704L) | 台账/条目批量追加 | self-evolution |

> ✅〔工具治理·已处理〕曾并存**两个写 `web/demo/index.html` 的 builder**；`scripts/build_demo.py`（遗留旧单页生成器·全仓无引用）已于 2026-09-23 **删除**（可经 git 历史恢复）。唯一权威 builder = `web/demo/scripts/build.py`。（`graph.json` 由 `export_sqlite_to_json.py` 产出，与 builder 无关。）

---

## 二、自我演化引擎（免疫 + 记忆）🧬

`scripts/self_evolve.py`（详见 [`workflows/self-evolution.md`](workflows/self-evolution.md) 与 `docs/self-evolution.md`）：
- `python scripts/self_evolve.py` 干跑一轮（Sense→Interpret→Act→Learn，不改研究内容）｜`make evolve`
- `--apply` 对已核证 P0 逐项 y/N 回填｜`make evolve-apply`
- `--ledger` 打印只追加台账｜`make evolve-ledger`
- `--record <类别> --actor <auto|human|agent> --subject .. --note .. --outcome <..>` 带外补记重型动作
- `--check-links`（联网，偶发用）· `--json` · `--no-validators`（离线快检）· `--reference-date`（可复现）

---

## 三、子代理（隔离上下文、并行深挖）🤖

通过 `Agent` 工具派生（返回**浓缩结论**，检索噪声不进主会话）：
- **Search / 检索子代理**：跨多文件的"这在哪实现/谁引用了 X"式定位。
- **Debug 子代理**：复现 + 根因运行期缺陷（用户明确要诊断时）。
- **CodeReview 子代理**：显式请求时对某范围做完整性/正确性/影响评审。
- **Browser 子代理**：真实浏览器交互验证（对标 Anthropic 的 Puppeteer MCP 端到端测试）。
- 未来〔待落地〕：`create-subagent` 固化"翻译审校代理""来源核查代理"。

---

## 四、MCP 与外部接口 🔌

- **MCP**（Model Context Protocol）：本环境经共享目录暴露服务器/工具（先读其 JSON schema 再调用）。当前**未默认挂载**重型 MCP；按需评估〔待落地〕。
- **在线翻译 API**：仅作**上量初稿辅助**、可插拔（无 key 回退子代理著写）；**质量门禁与主编审查不因 API 放松**（`CLAUDE.md`〈多语EN·原则6〉+ `docs/engineering-workflow.md`）。
- **一手数据源**：CBETA Online（`cbetaonline.dila.edu.tw/zh/T…`）、84000（`84000.co`，本环境常直连不通→白名单）、大华严寺 `huayen.world`、NTU 佛学图书馆等。
- **技能生态 CLI**：`npx skills find/add/check/update`（见 [`skills.md`](skills.md) §三）。

---

## 五、运行环境约束（Windows / PowerShell）⚙️

> 反复踩过的坑，务必沿用规避（记忆〈CJK Encoding and Subprocess Safety Conventions〉〈Windows Shell Python One-Liner Pitfalls〉）。

- **Shell 是 pwsh 7**：无 `grep`/`head`/`make`（Make 目标用 `py -m` 或直调 python）。检索用 `Grep`/`Glob` 工具，文件读写用专用工具而非 shell。
- **Python 环境**：conda `hy_py312` → `& "$HOME/miniconda3/envs/hy_py312/python.exe" …`。
- **CJK 编码**：子进程/输出前设 `$env:PYTHONIOENCODING="utf-8"`；否则 Windows 控制台 CJK 崩溃或吞 stdin。
- **别用内联 CJK one-liner**：`python -c "…中文…"` 易 SyntaxError/编码坏；**写临时 `.py` 文件**跑，用完删除。
- **PowerShell 吞输出/重编码**：`Out-File -Encoding utf8` 可能让中文计数误显 0——用 **ASCII 标记**（如 `id="fv-x"`）反证渲染，或把校验写进 Python。
- **Chrome**：`C:\Program Files\Google\Chrome\Application\chrome.exe`（headless `--dump-dom`）。
- **长命令**：勿超 ~500 字符；复杂逻辑落脚本文件再执行。

---

## 六、内置能力（IDE 直给，非脚本）🧠

`SearchCodebase`（语义检索）· `SearchMemory`（长期记忆/知识树）· `LSP`（符号级跳转/引用）· `WebSearch`/`WebFetch`（联网一手核实，服务〈考证优先〉）· `TodoWrite`（长任务分解）· `AskUserQuestion`（决策分叉征询）。
> 用法纪律：任务缺上下文时**先并行** `SearchCodebase` + `SearchMemory`；改某模块前先取该模块知识/规范。

> ⚠ **`SearchReplace` 保存时会重写整份 YAML/JSON 文件**：对**双引号 scalar 内含 `\n` 转义**的字段（如 `data/practice/chan_authentic_traces.yaml` 的 `lineage_evolution.mermaid`），会**把转义折成真实换行**，导致解析后的字符串丢失缩进与内部空格。现象：行数自 19→ 38、parsed string 长度变化、`subgraph 中国禅宗 奠基` 内空格被吞。**反验**：任何触及含长串双引号 scalar 的文件的 `SearchReplace`，**事后必**运行一次 `yaml.safe_load` 对比 `git show HEAD:<path>` 解析后的目标字段。若已碎，**一次性临时脚本按 HEAD 的原始 raw bytes 精准回内该段**（不影其余编辑），**且还原后不再使用 `SearchReplace` 碰同一文件**（否则再碎）。已亲身踩到·已恢复（L.㊿续续续、2026-09-23）。
