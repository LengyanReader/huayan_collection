# 知识管理方案

> 2026-08-05 | 基于 Demo v2.0 重构计划 — 增加 SQLite/Neo4j 数据库层

## 一、三层知识管理架构

```
┌─────────────────────────────────────────────────────────┐
│  L1: SQLite 权威数据层                                   │
│  data/catalog/huayan.db                                  │
│  所有策展/录入/修改直接操作SQLite                          │
│  Git跟踪: schema.sql + seed_data.sql (可审计diff)          │
├─────────────────────────────────────────────────────────┤
│  L2: Neo4j 图验证层                                      │
│  每次数据变更后加载到Neo4j                                 │
│  运行连通性/完备性/一致性Cypher查询                         │
│  不通过 → 修复SQLite → 重新验证                            │
├─────────────────────────────────────────────────────────┤
│  L3: YAML/JSON 交换层 → HTML 展示层                       │
│  SQLite → export脚本 → YAML/JSON                          │
│  build.py读取 → 注入HTML                                  │
│  不直接编辑YAML/JSON（从SQLite导出）                        │
└─────────────────────────────────────────────────────────┘
```

## 二、数据库设计

### SQLite (权威数据源)

完整Schema见 `data/catalog/schema.sql`。核心表：

| 表 | 用途 | 对应展示Tab |
|----|------|-----------|
| `persons` | 人物（80+人） | Tab1 法脉传承 |
| `texts` | 经典/章疏/讲记 | Tab2 华严文献 |
| `chapters` | 品目及汉藏差异 | Tab2 华严文献 |
| `locations` | 道场/地理 | Tab1 法脉传承 |
| `person_locations` | 人物-地点关联 | Tab1 法脉传承 |
| `cross_refs` | 文献互参 | Tab2 华严文献 |
| `glossary` | 四语术语（50+条） | Tab2 华严文献 |
| `translation_units` | 藏汉对译 | Tab2 华严文献 |
| `texts_fts` | 全文检索 | 全局 |
| `glossary_fts` | 术语检索 | 全局 |

### Neo4j (图验证引擎)

节点标签: `Person`, `Location`, `Text`
关系类型: `MASTER_OF`, `INFLUENCED`, `LINEAGE`, `CONTEMPORARY`, `LOCATED_AT`, `AUTHORED`, `TRANSLATED`

验证查询示例:
```cypher
// 连通性: 孤立人物
MATCH (p:Person) WHERE NOT (p)-[]-() RETURN p

// 完备性: 华严五祖传承链
MATCH path = (a:Person {name_zh: '杜顺'})-[:MASTER_OF|INFLUENCED*1..10]->(b:Person {name_zh: '宗密'})
RETURN length(path) as hops  // 期望 >= 4

// 一致性: 同名人去重
MATCH (p:Person) WITH p.name_zh as name, collect(p) as nodes
WHERE size(nodes) > 1 RETURN name, size(nodes)
```

## 三、数据分层与Tab映射

### 全Tab数据源映射

| Tab | 内容类型 | SQLite表 | 交换格式 | 展示端 |
|-----|---------|---------|---------|--------|
| 法脉传承 | 人物 | persons | graph.json | lineage.html |
| 法脉传承 | 传承边 | (persons+edges表) | graph.json | lineage.html |
| 法脉传承 | 地点 | locations + person_locations | graph.json | lineage.html |
| 法脉传承 | 历史事件 | — | events/key_events.yaml | lineage.html |
| 法脉传承 | 动画节点 | — | events/anim_waypoints.yaml | lineage.html |
| 法脉传承 | 传播故事 | — | events/transmission_story.yaml | lineage.html |
| 华严文献 | 差异矩阵 | chapters | gap.json | gap.html |
| 华严文献 | 术语库 | glossary | glossary.yaml | gap.html |
| 华严文献 | 案例/观点/方法论 | — | gap_content.yaml | gap.html |
| 华严教行 | 修行体系 | — | practice/*.yaml | jiaoxing.html |
| 华严教行 | 禅观法要 | — | practice/*.yaml | jiaoxing.html |
| 华严教行 | 讲法资源 | — | practice/*.yaml | jiaoxing.html |
| 前沿对话 | 跨界对话 | — | frontier/*.yaml | frontier.html |
| 世主妙严 | 宇宙观 | — | cosmology/*.yaml | cosmology.html |

注: "—" 表示该内容暂以YAML为权威源（尚未建立对应SQLite表），待后续版本迁移入SQLite。

## 四、数据操作规范

### 4.0 核心原则: 先入库，后导出，再显示

```
① 确定内容类型 → 找到对应SQLite表或YAML文件
② 直接编辑SQLite (INSERT/UPDATE) 或 YAML
③ 运行导出: python scripts/export_sqlite_to_json.py
④ 运行验证: python scripts/load_neo4j.py --verify
⑤ 运行构建: python web/demo/scripts/build.py
⑥ 验证展示: 打开HTML确认数据正确
⑦ git commit + push
```

### 4.1 违反规则的典型错误

- ❌ 在 build.py 中写 `nodes.append({...})` 追加人物
- ❌ 在 lineage.js 中直接修改 ANIM_WAYPOINTS 数组
- ❌ 绕过SQLite直接编辑JSON文件（会丢失权威性）
- ✅ SQLite INSERT INTO persons → 导出 → build.py自动读取
- ✅ 写入 `data/events/anim_waypoints.yaml`，由 build.py 注入

### 4.2 当前硬编码残留及清理计划

| 位置 | 硬编码内容 | 量 | 目标 | 优先级 |
|------|-----------|-----|------|--------|
| build.py L68-230 | 人物+边+地点 | ~30人+~30边+~10地 | SQLite persons表 | P0 |
| lineage.js | ANIM_WAYPOINTS等 | ~200条 | events/*.yaml | P0 |
| cosmology.js | COSMO_LAYERS等 | ~60条 | cosmology/*.yaml | P1 |
| gap.js | 术语/案例/观点 | ~120条 | glossary表+ gap_content.yaml | P1 |
| practice.js | 全部修行内容 | ~660行 | practice/*.yaml | P1 |
| frontier.js | 跨界对话全部文本 | ~100行 | frontier/*.yaml | P2 |

### 4.3 构建验证输出

每次构建打印:
```
OK  web/demo/index.html (2,384 bytes)
OK  web/demo/css/common.css (5,120 bytes)
OK  web/demo/js/common.js (8,456 bytes)
OK  web/demo/tabs/lineage.html (94,218 bytes | 85 persons | 81 edges | 23 locations)
OK  web/demo/tabs/gap.html (48,392 bytes | 45 chapters | 30 glossary terms)
OK  web/demo/tabs/jiaoxing.html (72,156 bytes | 4 practice sections)
OK  web/demo/tabs/frontier.html (28,734 bytes | 4 dialogue domains)
OK  web/demo/tabs/cosmology.html (42,890 bytes | 20 cosmo layers)
```

人数/边数/品目数的变化是数据正确性的第一道防线。

## 五、维护命令速查

```bash
conda activate causality-nd

# 数据导出
python scripts/export_sqlite_to_json.py

# 图验证
python scripts/load_neo4j.py --verify

# 来源可靠性验证
python scripts/verify_sources.py
python scripts/verify_sources.py --fixme

# 构建Demo
python web/demo/scripts/build.py

# 构建产物验证
python scripts/verify_demo.py
```
