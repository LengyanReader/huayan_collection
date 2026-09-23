# Workflow — 数据管线 / 知识图谱策展（Data Pipeline & KG Curation）

> **何时用**：新增/订正**人物·传承边·地点·经典·品目·术语**等结构化数据，或跑整条 import→export→build→verify 链时。
> **这是本项目最核心的循环**——一切展示的底层。权威细节不在本文件重述：见 `CLAUDE.md`〈知识管理架构·三层数据栈〉〈知识管理核心规则·权威源表〉+ [`docs/knowledge-management.md`](../../docs/knowledge-management.md) + [`docs/architecture.md`](../../docs/architecture.md)。

## 三层数据栈（L1 权威 → L3 呈现）

```
L1 SQLite(data/catalog/huayan.db)  ──►  L2 scripts/db_reader.py(数据服务)  ──►  L3 web/demo/scripts/build.py → HTML
   persons/texts/chapters/locations/glossary/lineages/lineage_edges + FTS5
非图谱数据(修行/宇宙观/前沿/事件) 仍以 data/**/*.yaml 为权威源 → build.py 读取
```

- **图谱数据**（人物/边/地点/经/品目/术语）权威在 **SQLite**；其余在 **YAML**。二者都是唯一权威源，**严禁在 build.py/JS 硬编码副本**。
- 数据流：`JSON/YAML 源` → `import_all_to_sqlite.py`(多源合并导入) → `SQLite` → `db_reader.py` → `build.py` → HTML；`export_sqlite_to_json.py` 负责 SQLite↔JSON 往返与 `--verify`。

## 标准「新增内容」流程（CLAUDE.md 五步）

1. **入库**：`init_db.py`（建库）→ 直接操作 SQLite 或用 `import_all_to_sqlite.py` 合并导入多源；或改对应 `data/**/*.yaml`。
2. **导出**：`export_sqlite_to_json.py`（+ `--verify`）刷新 `data/knowledge_graph/*.json`（personas/lineages/locations）与 graph.json/gap.json。
3. **构建**：`python web/demo/scripts/build.py`（6 tab + articles + css/js + index）。
4. **验证**：`test_pipeline.py` 核对人数/边数/地点（当前基线 **95 人 / 98 边 / 30 地**）→ `verify_demo.py` →（涉史实）`verify_sources.py`。
5. **提交**（经用户同意）+ 更新 `docs/next-phase-plan.md` + `make evolve`。

## 图验证（Neo4j）

- 离线：`python scripts/load_neo4j.py --verify-sqlite`（无需服务器，直接 SQLite 图验证）。
- 生成/在线：`--generate`（导出 Cypher）/ `--verify`（需 Neo4j 服务器）。

## 脚本清单（scripts/，按用途）

| 用途 | 脚本 |
|---|---|
| 建库/导入/导出/服务 | `init_db.py` · `import_all_to_sqlite.py`(945L, 多源合并) · `export_sqlite_to_json.py` · `db_reader.py`(498L) |
| 验证 | `test_pipeline.py` · `verify_sources.py` · `load_neo4j.py`(892L) |
| **来源补证(幂等回填)** | `backfill_core_sources.py` · `backfill_secondary_sources.py` · `backfill_location_sources.py` · `backfill_chapters_title_en.py` · `add_works_links.py` |
| **审校/审计** | `audit_bilingual.py`（中英配对）· `audit_classify.py`（分类）|
| 摄取(原始→数据) | 见 [`information-assurance.md`](information-assurance.md) 与下方「摄取链」|

> ✅〔工具治理·已处理〕曾并存**两个写 `web/demo/index.html` 的 builder**；遗留的 `scripts/build_demo.py`（旧单页生成器·无引用）已于 2026-09-23 删除（git 历史可恢复）。唯一权威 = `web/demo/scripts/build.py`。→ `web/demo/graph.json` 由 **`export_sqlite_to_json.py`** 生成。三道闸一键跑：`make verify-all`。

## 常见坑（考证优先 + 幂等）

- **非幂等 INSERT**：重导入会翻倍/报错 → 用 `INSERT OR REPLACE`（`import_chapters` 已如此修，L.㉖）。
- **源头持久化三步**：某字段（如 locations.source）要活过重建，须同时补 `graph.json` + `import_*.py` 读取 + `db_reader` 导出，缺一即在建库链中丢失（L.㉟）。
- **改数据非改产物**：修复只在 SQLite/YAML 做，绝不在生成的 HTML 或 JS 里改（下游必被重建覆盖）。
- **YAML 1.1 三坑**：`no:`→False、未引号日期→date 不可序列化、内嵌冒号/双引号非法（L.㊻⑤）。
- **计数即回归信号**：test_pipeline 的 95/98/30 变了要么是有意的数据增补、要么是导入丢数据——必须解释差异，不可默默放行。

## 门禁（Definition of Done）

`test_pipeline.py` ✅（人数/边/地一致）＋ `verify_demo.py` ✅ ＋（涉内容）`verify_sources.py` T0=0/评分不降 ＋ `docs/next-phase-plan.md` 已登记 ＋ `make evolve`。
