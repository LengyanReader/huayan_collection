# 高僧画像 · 分析就绪数据模型草案 v0.1

> 目标：把画像页的 19 层内容规范成**可入库、可查询、可跑网络/时空/文本分析**的结构化字段，
> 打通 `SQLite(+FTS5) → JSON → Neo4j` 既有管道（复用 `scripts/import_all_to_sqlite.py`、
> `export_sqlite_to_json.py`、`load_neo4j.py`）。本件是**草案/提案**，不含建库与写入。

## 0. 设计原则（三条硬约束）

1. **扩展而非另立**：以现有 `person_*` 主干（见 `data/knowledge_graph/personas.json`
   · `schemas/persona.schema.json`）为实体锚点，画像新增的是**字段级信度层**，不重造人物 ID。
   现存 `verified: 0|1` 二值过粗，画像以 `grade`(甲乙丙丁戊) + `verdict`(确疑阙孤冲突) 取代。
2. **量化不替考证**：数值/坐标/边只是把已有考证结论**变成可计算的元数据**；每个值仍须带
   `source_siglum` + `page_ref`，可逐字回源。空值记 `NULL`（=待填），不以零/默认值冒充。
3. **圣传与史实分离**：母题/瑞应（H·S 层，戊级）单独成表，分析时作**可过滤的标签**，
   不得与史实字段同权重计入网络或时空度量。

## 1. 实体主键

| 表 | 主键 | 说明 |
| --- | --- | --- |
| `person` | `person_id` | 沿用 `person_\d{3}`（法藏=`person_0xx`，须先与 personas.json 对齐去重） |
| `place` | `place_id` | 古今地名规范化，带经纬；同 `geo_features.yaml` 口径 |
| `work` | `work_id` | 著述/文献，存 Taishō/续藏 短号 |
| `source_ring` | `ring_id` | R1–R6 文献环归属 |

## 2. 画像字段层（核心新增）

### 2.1 `person`（主干 + 画像扩展列）
沿用现有列（`name_zh/bo/sa/en`、`alt_names`、`type`、`dynasty`、`lineage_branch`、
`lineage_order`、`title`、`biography`、`key_works`），**新增**：

| 列 | 类型 | 例(法藏) | 约束 |
| --- | --- | --- | --- |
| `birth_year` | INT NULL | 643 | 允许 NULL=待核 |
| `birth_year_grade` | ENUM(甲乙丙丁戊) | 乙 | 崔传「贞观十七年」有载 |
| `birth_year_verdict` | ENUM(确疑阙孤冲突) | 确 | |
| `death_year` / `death_*_grade` / `*_verdict` | 同上 | 712 / 乙 / 冲突 | 712/710 二说→`冲突` |
| `clan` / `clan_grade` | TEXT/ENUM | 康氏 / 丙 | |
| `native_place_id` | FK→place | 康国/长安 | 族属与徙居分记 |
| `sect_tradition` | TEXT | 华严宗 | |
| `lineage_position` | INT | 3 | 三祖 |
| `main_bio_siglum` | TEXT | T50n2061 卷5 | 入手节点 |
| `completeness_pct` | INT | 58 | 展示态，非事实 |

### 2.2 `place`（古今地名 · 时空可算）
| 列 | 类型 | 例 |
| --- | --- | --- |
| `ancient_name` | TEXT | 大荐福寺 |
| `modern_name` | TEXT NULL | 今西安·寺址待考 |
| `lat` / `lng` | REAL NULL | 34.3 / 108.9 |
| `coord_source` | TEXT | geo_features.yaml / 实测 |
| `confidence` | ENUM(确待核待考) | 待考 |

### 2.3 `person_place`（行迹轨迹 = 时空边）
`person_id` · `place_id` · `event_type`(生/居/讲/译/卒/葬/朝礼) · `year_start` · `year_end` ·
`grade` · `source_siglum`。→ 支撑 GIS 轨迹、迁徙距离×速度、双京结构分析。

### 2.4 `relationship`（分谊边 → Neo4j 关系；双向 + 流评）
| 列 | 说明 |
| --- | --- |
| `person_a`,`person_b` | 端点（a=焦点僧） |
| `rel_type` | 亲教师/嗣法弟子/同期法友/译场合作/帝王护法/私淑远承/并行学者 |
| `is_bidirectional` | BOOL：`分谊` 双向名分 |
| `flow_eval` | TEXT：`流评`（法脉后效+后世评断），可空 |
| `grade` / `verdict` / `source_siglum` / `page_ref` | 逐条回源 |

### 2.5 `claim_evidence`（逐句考据 · N 层 · 信度计量之本）
`person_id` · `layer`(A–U) · `field` · `value` · `source_siglum` · `page_ref` ·
`quote`（僧传原文）· `ur_source`（赞宁取材自）· `grade` · `verdict`。
→ 支撑「可信度随去古远近衰减曲线」「史源采用率」等计量。

### 2.6 `work`（著述 · 引用网络节点）
`work_id` · `title` · `siglum`(T/X/JB…) · `attributed_person_id` · `attribution_grade` ·
`attribution_verdict`(确/疑/冲突，如《金师子章》作者权) · `extant`(存/佚/残) · `ring`(R1..)。

### 2.7 `source_ring`（文献全景 R1–R6 · 已采/未采）
`person_id` · `ring`(R1–R6) · `source_siglum` · `title` · `relation_type`(亲笔/旁证/征引/研究) ·
`used_by_main_bio`(BOOL，赞宁是否采用) · `extant`。→ 支撑史源覆盖率与接受史。

### 2.8 `motif`（文学母题 · 圣传层 · 分析须过滤）
`person_id` · `motif_type`(烧指/神灯/瑞应/预言/地震…) · `layer`(H/S) · `grade`(多戊) · `note`。

### 2.9 `media`（形象媒介考）
`person_id` · `category`(①顶相②形貌③追造④塑像⑤现代⑥变相⑦敕写真仪) ·
`contemporary`(BOOL) · `status`(存/佚/不存在判定) · `source_siglum`。

## 3. 受控词表（枚举）

- `grade`：甲 / 乙 / 丙 / 丁 / 戊（史料层级）
- `verdict`：确 / 疑 / 阙 / 孤 / 冲突（判断）
- `rel_type`：见 2.4
- Neo4j 关系映射：`亲教师→STUDIED_UNDER`、`嗣法弟子→DHARMA_HEIR_OF`、
  `同期法友→CONTEMPORARY_OF`、`译场合作→TRANSLATED_WITH`、`帝王护法→PATRONIZED_BY`、
  `私淑远承→INFLUENCED`（对齐 lineages.json 现有 `MASTER_OF`/`INFLUENCED`）
- 节点：`Person`、`Place`、`Work`、`Source`

## 4. 管道落地（复用既有脚本）

1. `portrait` YAML/JSON → `import_all_to_sqlite.py` 扩列（或新建 `portrait.db`）。
2. `export_sqlite_to_json.py` → 生成 `personas.json`/`lineages.json`/`locations.json` 的画像超集。
3. `load_neo4j.py` → 建 `(:Person)-[:STUDIED_UNDER {grade,verdict,source}]->(:Person)` 等属性边。
4. 导出 `graph.json` → Gephi/networkx/igraph 跑中心度·社群·小世界。
5. `place.lat/lng` → QGIS / Leaflet 叠 `geo_features.yaml`。

## 5. 分析可行度（前置数据门槛）

| 分析 | 就绪条件 | 现状 |
| --- | --- | --- |
| 师承/交游网络中心度 | `relationship` 边填充 | 法藏 7 边已有；余 9 人 0 |
| 时空轨迹/GIS | `place` 经纬 + `person_place` | 法藏今地已建；坐标待精校 |
| 引用网络/接受史 | `source_ring` + `work` | 法藏 R1–R6 半 |
| 信度衰减曲线 | `claim_evidence` 逐句 | 法藏 N1–N7 开例 |
| 母题类型学 | `motif` 跨人 | 待逐人标 |
| 文体计量(作者归属) | `work` 全文语料 | 依赖 CBETA 语料接入 |

**结论**：管道与字段可即刻定义；分析真正跑动的前提是把 9 人 `relationship/place/work`
填到可计量的最小样本（甲任务）。小样本上中心度/社群结论须标注为示意而非统计显著。

## 6. 待用户定夺

- 主干 ID 是否并入 personas.json 现有 80+ 人，还是画像独立命名空间再合并。
- `claim_evidence` 是否需要页码级 `page_ref` 全量（工作量大）。
- 母题/圣传层是否单库隔离（推荐），以免误入量化。
