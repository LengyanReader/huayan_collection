# 华严项目轻量化技术栈设计

## 设计原则

1. **轻量优先**: 能嵌入的不独立部署，能文件的不走服务端。每增加一个组件必须有不可替代的充分理由
2. **完备性**: 覆盖文献管理→实体提取→图谱构建→语义检索→翻译辅助→可视化的全链路
3. **本地化**: 所有组件均可离线运行，无外部 API 依赖
4. **渐进增强**: 从小数据量开始验证，架构支持扩展但不预设大规模

---

## 一、技术选型总表

| 功能层 | 组件 | 类型 | 理由 |
|--------|------|------|------|
| 版本控制 | Git | — | 已有 |
| 数据交换 | Markdown + YAML | 文件 | 人机可读，Git 友好 |
| 关系数据 | SQLite | 嵌入式 | 零运维，单文件，FTS5 全文检索 |
| 图数据 | Neo4j Community | 本地服务 | 图查询语义直观，Cypher 一流。**仅此一项需要独立服务** |
| 向量存储 | LanceDB | 嵌入式 | 比 ChromaDB 更轻量（无服务端），列式存储，零依赖，Python 原生 |
| 嵌入模型 | shaw/dmeta-embedding-zh | Ollama 部署 | 100M 参数，极轻量，中文优化，MTEB 表现优异 |
| 本地 LLM | qwen2.5:1.5b 或 qwen2.5:7b | Ollama 部署 | 中文理解能力强，支持文言/佛典语境。1.5b 测试用，7b 生产用 |
| ETL | Python (lxml, pandas) | 脚本 | 标准数据科学栈 |
| 前端 | Observable Framework | 静态站点 | 数据叙事+交互可视化，Markdown 驱动，比 Next.js 更轻 |
| 可视化 | D3.js + Observable Plot + Leaflet | 前端库 | 图谱力导向 / 时间轴 / 地图 |
| 编辑器 | VS Code + GitLens | — | 已有 |

### 为什么选择这些

#### LanceDB > ChromaDB

| 维度 | LanceDB | ChromaDB |
|------|---------|----------|
| 运行模式 | 纯嵌入式（import lancedb） | 嵌入式但更重（依赖 SQLite + hnswlib 等） |
| 存储格式 | Lance（列式，Apache Arrow 原生） | 自定义（底层 SQLite） |
| 零依赖 | ✅ 纯 Python | ❌ 需要多个 C 扩展 |
| 查询 | SQL 风格 + 向量搜索 | 自定义 API |
| 磁盘占用 | 更小（列式压缩） | 中等 |

#### qwen2.5 > llama3 (中文场景)

- Qwen 2.5 对中文文言文/佛教术语理解显著优于同参数量 LLaMA
- 1.5b 版本可在 4GB 内存机器运行，适合测试
- 7b 版本在 16GB 内存机器即可流畅推理

#### Observable Framework > Next.js (此项目)

- 本项目以数据叙事为主，非 CRUD 应用
- Observable 原生支持 Markdown + 数据可视化
- 静态导出部署，零服务端
- 比 Next.js 少一个 Node.js 运行时依赖

---

## 二、完整架构图

```
┌─────────────────────────────────────────────────────┐
│              用户交互层                               │
│  ┌──────────┐  ┌──────────┐  ┌───────────────────┐  │
│  │ CLI      │  │ VS Code  │  │ Observable (Web)   │  │
│  │ (huayan) │  │          │  │ 数据故事/可视化     │  │
│  └────┬─────┘  └────┬─────┘  └────────┬──────────┘  │
│       │             │                 │              │
├───────┼─────────────┼─────────────────┼──────────────┤
│       │        Python 应用层          │              │
│  ┌────┴──────────────────────────────┴────────────┐  │
│  │  Catalog   │  Graph    │  Translate  │  Search  │  │
│  │  Service   │  Service  │  Service    │  Service │  │
│  └────┬───────┴─────┬─────┴──────┬─────┴────┬─────┘  │
│       │             │            │          │        │
├───────┼─────────────┼────────────┼──────────┼────────┤
│       │        数据存储层         │          │        │
│  ┌────┴────┐ ┌─────┴────┐ ┌─────┴────┐ ┌───┴──────┐ │
│  │ SQLite  │ │  Neo4j   │ │ LanceDB  │ │ Markdown │ │
│  │ 目录/检索│ │  知识图谱 │ │ 语义向量  │ │  文本    │ │
│  └─────────┘ └──────────┘ └──────────┘ └──────────┘ │
│                                                      │
├──────────────────────────────────────────────────────┤
│              AI 辅助层 (Ollama 本地)                   │
│  ┌──────────────────┐  ┌──────────────────────────┐  │
│  │ dmeta-embedding  │  │  qwen2.5:7b              │  │
│  │ 文本向量化        │  │ 实体提取 / 翻译辅助 / 问答 │  │
│  │ (409MB)          │  │ (~4.7GB)                 │  │
│  └──────────────────┘  └──────────────────────────┘  │
└──────────────────────────────────────────────────────┘
```

**启动顺序**: `Neo4j` → `Ollama` → `Python 应用`

---

## 三、各组件配置

### 3.1 Ollama 本地 LLM

```bash
# 安装 (Windows 原生，已有 MSI 安装包)
# 下载: https://ollama.com/download/windows

# 拉取模型
ollama pull shaw/dmeta-embedding-zh  # 中文嵌入 (409MB)
ollama pull qwen2.5:1.5b             # 轻量测试 LLM (~1GB)
ollama pull qwen2.5:7b               # 生产级 LLM (~4.7GB)

# Python 调用
# pip install ollama
# ollama.embeddings(model='shaw/dmeta-embedding-zh', prompt='法界')
# ollama.chat(model='qwen2.5:7b', messages=[...])
```

### 3.2 LanceDB 向量存储

```bash
pip install lancedb
```

```python
import lancedb
db = lancedb.connect("data/vectors")
table = db.create_table("huayan_glossary", [
    {"vector": embedding, "term_zh": "法界", "term_sa": "dharmadhātu"}
])
# 混合查询: 向量相似度 + 元数据过滤
table.search(query_vector).where("category='doctrine'").limit(10).to_list()
```

### 3.3 Neo4j（已配置）

```bash
make neo4j-console
# Bolt: localhost:7687
# HTTP: localhost:7474
# Auth: neo4j / huayan2024
```

### 3.4 资源占用（低配模式）

| 组件 | 内存 | 磁盘 |
|------|------|------|
| Neo4j | ~512MB-1GB | ~200MB (空库) |
| Ollama + qwen2.5:1.5b | ~1.2GB | ~1GB |
| Ollama + dmeta-embedding | ~200MB | ~409MB |
| SQLite + LanceDB | ~50MB | 10-500MB (数据量) |
| Python 运行时 | ~100MB | — |
| **总计（最低）** | **~2GB** | **~2GB** |
| **总计（推荐）** | **~4GB** | **~5GB** |

---

## 四、避免引入的技术（当前阶段）

以下技术在现阶段**不需要**，避免过早复杂化：

| 不引入 | 原因 | 以后可能需要吗 |
|--------|------|-------------|
| Docker Compose | 本地直接运行更简单。仅有 Neo4j 一个服务 | 如果团队协作可能需要 |
| Redis / RabbitMQ | 单用户本地没有消息队列需求 | 不需要 |
| Kubernetes | 天量级过度设计 | 不需要 |
| MySQL / PostgreSQL | SQLite 足够 10万条记录 | 百万级数据时考虑迁移 |
| LangChain / LlamaIndex | 增加复杂度，直接调用 ollama Python SDK 更简单可控 | 如果 RAG 管道变得非常复杂时考虑 |
| Apache Spark | 数据量远未到需要分布式计算 | 不需要 |
| ElasticSearch | SQLite FTS5 已经足够 | 十万级以上文档时考虑 MeiliSearch |
| FastAPI / Flask | 先不做 API 服务，CLI + 静态站点即可 | Phase 4 公开部署时考虑 |

---

## 五、渐进增强路径

```
Phase 1 (当前)  Phase 2          Phase 3          Phase 4
    │              │                │                │
SQLite ────────▶ SQLite+JSON ──▶ SQLite+LanceDB ──▶ SQLite+LanceDB
Neo4j ────────▶ Neo4j+Cypher ──▶ +Ollama+NLP ────▶ +Observable Web
CLI  ─────────▶ CLI+脚本 ──────▶ CLI+Jupyter ─────▶ CLI+Web Dashboard
```

每个阶段只引入经过验证的必要组件，不提前堆砌。
