
# Loop Engineering & Graph Engineering 开发验证工作流

## 一、核心理念

传统软件开发流程（需求→设计→实现→测试）不适合此项目。本项目的数据高度结构化（图谱）但领域知识密集（佛学），需要一种**以数据质量为核心、以图谱连通性为验证标准、以持续反馈为驱动**的工程方法。

### 两个 Engineering 的定义

**Loop Engineering**: 以评估验证为驱动的闭环迭代。每个产出物（一篇人物传记、一行翻译）都经过"生成→评估→修正→再验证"的循环。循环的停止条件不是"实现了"，而是"与已有知识体系无矛盾"。

**Graph Engineering**: 以图谱的**连通性、一致性、完备性**为质量度量标准。一条传承链上缺少一个人物，图谱就出现了"断边"。一个道场缺少地理坐标，就无法生成 GIS 图层。图工程的核心是：**图不会说谎——缺失和矛盾会以断开的形式直接呈现**。

---

## 二、闭环开发总流程

```
                    ┌──────────────────────────────┐
                    │     1. DATA LAYER             │
                    │  数据采集 / 结构化 / 入库     │
                    │  CBETA → SQLite, BDRC → YAML  │
                    └──────────────┬───────────────┘
                                   │
                    ┌──────────────▼───────────────┐
                    │     2. GRAPH LAYER            │
                    │  实体链接 / 关系构建 / 写入   │
                    │  SQLite → Neo4j (Cypher)      │
                    └──────────────┬───────────────┘
                                   │
           ┌───────────────────────┼───────────────────────┐
           │                       │                       │
  ┌────────▼────────┐    ┌────────▼────────┐    ┌────────▼────────┐
  │ 3a. 连通性验证   │    │ 3b. 完备性评估   │    │ 3c. 一致性检查   │
  │ 无孤立节点?      │    │ 关键人物缺失?    │    │ 同一人有多个ID?  │
  │ 传承链无断环?    │    │ 道场坐标未填?    │    │ 朝代和年份匹配?  │
  └────────┬────────┘    └────────┬────────┘    └────────┬────────┘
           │                       │                       │
           └───────────────────────┼───────────────────────┘
                                   │
                    ┌──────────────▼───────────────┐
                    │     4. FIX & ITERATE          │
                    │  补充数据 / 修正关系 / 去重   │
                    │  回到步骤 2                    │
                    └──────────────┬───────────────┘
                                   │ (全部通过)
                    ┌──────────────▼───────────────┐
                    │     5. DEMO & REPORT          │
                    │  生成可演示的图谱/报告/可视化  │
                    └──────────────────────────────┘
```

### 循环退出条件

| 层     | 通过标准                                                                         |
| ------ | -------------------------------------------------------------------------------- |
| 连通性 | Neo4j 中`MATCH (p:Person) WHERE NOT (p)-[]-() RETURN p` 返回 0 行              |
| 完备性 | 每条传承链`MATCH path = (a:Person)-[:MASTER_OF*]->(b:Person)` 中无缺失标注节点 |
| 一致性 | 同一`name_zh + birth_year` 下无重复 Person 节点                                |

---

## 三、各环节的具体操作与验证

### 3.1 Data Layer — 文献采集与结构化

**输入**: CBETA TEI/XML, BDRC IIIF API, 手工录入
**输出**: Markdown + YAML frontmatter → SQLite texts/persons/chapters 表

**验证脚本** (每个数据文件入库后自动运行):

```python
# verify_catalog.py
def check_persons():
    """检查: 所有 persons 记录的必填字段不为空"""
    persons = load_json("data/knowledge_graph/personas.json")
    for p in persons:
        assert p.get("name_zh"), f"Missing name_zh for {p['id']}"
        assert p.get("type"), f"Missing type for {p['id']}"
        assert p.get("dynasty"), f"Missing dynasty for {p['id']}"

def check_glossary():
    """检查: 术语至少有 zh + 1 种其他语言"""
    terms = load_yaml("data/translation/glossary.yaml")
    for t in terms:
        assert t.get("zh"), f"Missing zh for term {t.get('id')}"
        has_other = t.get("sa") or t.get("bo_wylie") or t.get("en")
        assert has_other, f"Term {t['zh']} has no cross-language mapping"
```

### 3.2 Graph Layer — 知识图谱构建

**输入**: SQLite tables + JSON 数据文件
**输出**: Neo4j 节点与关系

**加载脚本**:

```python
# graph_loader.py
def load_persons_to_neo4j(driver, persons):
    for p in persons:
        driver.execute_query("""
            MERGE (p:Person {name_zh: $name_zh, birth_year: $birth_year})
            SET p.type = $type, p.dynasty = $dynasty, p.name_sa = $name_sa
        """, p)
        # 关联朝代节点
        driver.execute_query("""
            MATCH (p:Person {name_zh: $name_zh})
            MATCH (d:Dynasty {name: $dynasty})
            MERGE (p)-[:DURING]->(d)
        """, {"name_zh": p["name_zh"], "dynasty": p["dynasty"]})
```

### 3.3 Graph Quality — 验证层（核心创新点）

#### 3.3.1 连通性检查 (Connectivity Check)

```cypher
-- 找出所有孤立人物节点（无任何关系边）
MATCH (p:Person)
WHERE NOT (p)-[]-()
RETURN p.name_zh, p.type, p.dynasty
-- 期望: 0 行。如果有结果 → 需补充关系边或标记为"待关联"

-- 检查华严五祖传承链是否连续
MATCH path = (a:Person {name_zh: '杜顺'})
      -[:MASTER_OF|INFLUENCED*1..10]->
      (b:Person {name_zh: '宗密'})
RETURN length(path) as hops
-- 若 hops < 4（五祖间距至少4跳）→ 传承链有断
```

#### 3.3.2 完备性评估 (Completeness Audit)

```
完备性评分卡:
  ✓ 每位人物: name_zh + type + dynasty + birth_year/death_year 至少有一个
  ✓ 每部经典: title_zh + taisho_no 或 cbeta_id 至少有一个
  ✓ 每条传承边: from + to + relation + note（说明来源）
  ✓ 每个道场: lat + lng 已填充或标注 "待定"
  ✓ 每个品目: 标注 in_80huayan / in_60huayan / in_tibetan 布尔值

评分 = 已完备字段 / 总应有字段
目标: > 90%
```

#### 3.3.3 一致性检查 (Consistency Check)

```cypher
-- 检查: 同一人名是否有多个 Person 节点（重复检测）
MATCH (p:Person)
WITH p.name_zh as name, collect(p) as nodes
WHERE size(nodes) > 1
RETURN name, size(nodes) as duplicates

-- 检查: Person.dynasty 与关联的 Dynasty 节点名是否匹配
MATCH (p:Person)-[:DURING]->(d:Dynasty)
WHERE p.dynasty <> d.name
RETURN p.name_zh, p.dynasty, d.name as dynasty_node

-- 检查: MASTER_OF 关系中，师的生年 < 徒的生年
-- (需要 birth_year 不为 null)
```

### 3.4 Fix & Iterate — 修正循环

发现问题的处理流程:

```
连通性断裂 ──▶ 查找断裂位置 ──▶ 补充人物或关系边 ──▶ 重新加载 ──▶ 再验证
完备性不足 ──▶ 标注 missing 字段 ──▶ 补充数据源 ──▶ 更新 JSON ──▶ 再验证
一致性冲突 ──▶ 查看重复节点 ──▶ MERGE 合并 ──▶ 统一数据源 ──▶ 再验证
```

### 3.5 Demo — 可演示的验证产出

每次迭代后用以下方式展示进展:

#### 图谱快照

```cypher
// 生成传承谱系总览
MATCH path = (a:Person)-[:MASTER_OF|INFLUENCED*1..8]->(b:Person)
WHERE a.lineage_branch IS NOT NULL
RETURN a, b, path
LIMIT 100
// 在 Neo4j Browser 中以力导向图呈现
```

#### 完备性仪表盘

```python
def completeness_dashboard():
    """生成 Markdown 格式的完备性报告"""
    total_persons = count("persons")
    persons_with_full_dates = count("persons WHERE birth_year AND death_year")
    total_edges = count("lineage edges")
    edges_with_source = count("edges WHERE note LIKE '%《%'")
    return f"""
    | 指标 | 完成度 |
    |------|--------|
    | 人物 (至少name+dynasty+type) | {total_persons} |
    | 人物 (含生卒年) | {persons_with_full_dates}/{total_persons} |
    | 传承边 (含出处标注) | {edges_with_source}/{total_edges} |
    """
```

#### 版本差异热力图

```yaml
# 每次数据更新后，生成差异热力图
diff:
  date: "2024-07-24"
  changes:
    persons_added: 23
    persons_updated: 5
    lineages_added: 3
    glossary_terms_added: 10
  completeness_before: 0.65
  completeness_after: 0.82
```

---

## 四、翻译对译的 Loop Engineering

藏汉对译工作流有自己的特殊循环:

```
藏文原文 (Toh 44 某品)
    │
    ├── 1. 术语提取 ──▶ glossary.yaml 查重 ──▶ 缺失则新增
    │
    ├── 2. LLM 初译 ──▶ Ollama (qwen2.5:7b + 自定义提示词)
    │
    ├── 3. 人工审校 ──▶ 对照八十华严对应品(若有) ──▶ 标注差异级别
    │       │
    │       ├── A级: 与汉文完全对应 → 沿用汉译术语
    │       ├── B级: 与汉文部分对应 → 标注差异 + 保留两种表述
    │       └── C级: 藏文独有内容 → 全新翻译 + 保留术语原文
    │
    ├── 4. 术语一致性回溯 ──▶ 检查: 新译术语是否与 glossary.yaml 已有译法一致
    │       │                   不一致 → 选择 (A) 修改译文 或 (B) 拆分术语义项
    │
    └── 5. 定稿 ──▶ translation_units 表 status → final
```

### 翻译质量度量

| 度量       | 方法                                                       | 目标         |
| ---------- | ---------------------------------------------------------- | ------------ |
| 术语一致性 | 遍历译文中所有术语，查 glossary.yaml 确认译法统一          | 100%         |
| 风格符合度 | 抽样检查是否遵循玄奘四言体规范 (docs/translation-guide.md) | > 80%        |
| 可回译性   | 将汉译回译为藏文 (LLM辅助)，检查语义是否偏离               | 核心段落达标 |

---

## 五、持续集成的检查链

```
每次 git commit (data/ 变更) 触发:

  ┌── 1. Schema 验证
  │     JSON/YAML → JSON Schema 校验
  │     失败 → 拒绝提交
  │
  ├── 2. 数据完整性
  │     必填字段检查 / ID 唯一性 / 引用有效性
  │     失败 → 警告但允许提交（标记 fixme）
  │
  ├── 3. 图谱生成 (可选，较大变更时触发)
  │     重新加载 Neo4j → 运行连通性/一致性 Cypher 查询
  │     失败 → 生成报告，人工决策
  │
  └── 4. 完备性趋势报告
        对比上次 commit 的完备性评分
        生成 CHANGELOG.md 条目
```

---

## 六、知识管理规则 (Knowledge Management Rules)

### 6.0 核心原则：先入库，后显示

**所有页面显示的内容必须来源于结构化源文件。严禁在 build.py 或 JS 中硬编码数据。**

任何新增内容（人物/关系/事件/术语/论文）的工作流：

```
① 确定内容类型 → 找到对应源文件 (JSON/YAML)
② 按现有格式追加记录
③ python web/demo/scripts/build.py 构建
④ 验证构建输出 (人数/边数/事件数一致)
⑤ git commit + push
```

违反此规则的典型错误：
- ❌ 在 build.py 中写 `nodes.append({...})` 追加人物
- ❌ 在 lineage.js 中直接修改 ANIM_WAYPOINTS 数组
- ✅ 写入 `personas.json`，由 build.py 自动读取
- ✅ 写入 `events/anim_waypoints.yaml`，由 build.py 注入

### 6.1 全 Tab 数据源映射

| Tab | 内容 | 源文件 | 格式 |
|-----|------|--------|------|
| 法脉传承 | 人物 | `data/knowledge_graph/personas.json` | JSON |
| 法脉传承 | 传承边 | `data/knowledge_graph/lineages.json` | JSON |
| 法脉传承 | 地点 | `data/knowledge_graph/locations.json` | JSON |
| 法脉传承 | 历史事件 | `data/events/key_events.yaml` (待建) | YAML |
| 法脉传承 | 动画节点 | `data/events/anim_waypoints.yaml` (待建) | YAML |
| 法脉传承 | 传播故事 | `data/events/transmission_story.yaml` (待建) | YAML |
| 汉藏文献 | 差异矩阵 | `data/translation/diff_matrix.yaml` | YAML |
| 汉藏文献 | 术语库 | `data/translation/glossary.yaml` | YAML |
| 华严行法 | 修行体系 | `data/practice/` (待建) | YAML |
| 前沿对话 | 文献综述 | `data/frontier/` (待建) | YAML |
| 华严其观 | 宇宙观 | `data/cosmology/` (待建) | YAML |

### 6.2 构建验证输出

每次构建打印验证信息：
```
OK  index.html
    192,497 bytes | 73 persons | 81 edges | 23 locations
```
人数/边数/地点数的变化是数据正确性的第一道防线。

## 七、技术实现要点

### 6.1 不使用 CI 服务器

当前阶段不必引入 GitHub Actions 或 Jenkins。用 **pre-commit hook** + **手动 Make target** 即可:

```bash
# .git/hooks/pre-commit
make verify-data   # 运行所有数据验证脚本
```

```makefile
# Makefile 新增
verify-data:
	$(PYTHON) scripts/verify_schema.py
	$(PYTHON) scripts/verify_completeness.py

verify-graph:
	$(PYTHON) scripts/verify_graph_connectivity.py

report:
	$(PYTHON) scripts/generate_completeness_report.py

demo:
	@echo "=== 华严宗部知识图谱 Demo ==="
	@echo "1. 启动 Neo4j: make neo4j-console"
	@echo "2. 打开浏览器: http://localhost:7474"
	@echo "3. 运行查询: MATCH (p:Person)-[r:MASTER_OF]->(d) RETURN p,r,d"
```

### 6.2 每次迭代的工作流命令

```bash
# 一个完整的 Loop: 修改数据 → 验证 → 入图 → 检查 → 修复

# Step 1: 编辑数据文件
code data/knowledge_graph/personas.json

# Step 2: 验证 Schema + 数据完整性
make verify-data

# Step 3: 重新加载 Neo4j (如果图数据有变更)
make graph-load

# Step 4: 运行图谱质量检查
make verify-graph

# Step 5: 查看完备性报告
make report

# Step 6: 根据报告修复 → 回到 Step 1
# 直到 verify-graph 全部通过
```

---

## 七、演示层的设计

在完成数据-图谱-验证闭环后，演示通过以下三层递进展开:

1. **Neo4j Browser (最底层)**: 直接 Cypher 查询，开发者视角。验证数据正确性
2. **Observable 数据故事 (中层)**: 嵌入式可视化（力导向图、时间轴、GIS 地图），面向学术用户
3. **静态报告 (最顶层)**: Markdown + PNG 截图，面向非技术读者，可分享

每一层都基于同一份数据，从不同视角呈现同一真相。
