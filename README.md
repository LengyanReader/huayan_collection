# 华严宗部文献与修行资料数字化梳理

[![Status](https://img.shields.io/badge/status-phase%201%20%E2%80%94%20architecture-brightgreen)](#)
[![Version](https://img.shields.io/badge/version-0.1.0-blue)](#)

构建以华严宗为核心的佛法文献与修行资料数字化系统，包含两大核心目标：

1. **多维知识图谱** — 华严宗祖师/行者传承谱系、地理道场、经典关联的可视化知识网络
2. **藏汉华严对译** — 定位藏文《华严经》(Toh 44) 与汉文版本的差异，进行汉英翻译与对比

> 📖 **架构设计文档**: [docs/architecture.md](docs/architecture.md)
>
> 📋 **可行性分析与实施计划**: [C:\Users\data\.claude\plans\fizzy-toasting-steele.md](C:\Users\data\.claude\plans\fizzy-toasting-steele.md)

---

## 项目结构

```
huayan_collection/
├── data/                         # 📦 数据中心
│   ├── catalog/                  #   SQLite 文献目录库
│   │   └── schema.sql           #     数据库结构定义
│   ├── texts/                    #   经典全文 (Markdown + YAML)
│   │   ├── sutras/              #     经文
│   │   ├── commentaries/        #     章疏论著
│   │   ├── rituals/             #     仪轨忏法
│   │   └── modern/              #     近现代讲记
│   ├── knowledge_graph/          #   图谱数据
│   │   ├── personas.json        #     📌 核心人物 (20人)
│   │   ├── lineages.json        #     📌 传承谱系 (6支)
│   │   ├── locations.json       #     📌 道场地点 (15处)
│   │   └── neo4j_import/        #     Neo4j 初始化
│   │       └── init.cypher      #       Schema + 索引 + 朝代节点
│   ├── translation/              #   藏汉对译项目
│   │   ├── diff_matrix.yaml     #     📌 45品 vs 39品差异矩阵
│   │   └── glossary.yaml        #     📌 四语术语库 (25词条)
│   └── references/               #   学术参考
├── src/                          # 🐍 Python 源码 (待实现)
│   ├── cli/                      #   CLI 命令入口
│   ├── catalog/                  #   文献目录服务
│   ├── graph/                    #   图谱服务
│   └── translation/              #   对译服务
├── web/                          # 🌐 前端 (待实现)
├── docs/                         # 📖 文档
│   ├── architecture.md           #   架构设计文档
│   └── translation-guide.md     #   翻译规范指南
├── pyproject.toml                # Python 项目配置
├── Makefile                      # 常用命令
├── CLAUDE.md                     # AI 助手指令
└── README.md
```

📌 = 当前阶段已完成的核心数据文件

---

## 核心数据资产 (Phase 1 产出)

### 文献目录

- **SQLite Schema**: 7 张核心表 (persons, texts, chapters, locations, cross_refs, glossary, translation_units)
- 含全文检索 (FTS5) 和完整索引

### 知识图谱

- **20 位核心人物**: 从华严初祖杜顺 (557 CE) 到当代贤度法师，覆盖 1400+ 年传承链
- **6 支传承系谱**: 华严五祖、李通玄系、高丽华严、月霞系、慈舟系、智光系
- **15 处核心道场**: 从五台山到台北华严莲社，含 GIS 坐标

### 藏汉对译基础设施

- **45 品 vs 39 品差异矩阵**: 逐品标注藏文独有品目（《如来华严品》《普贤宣说品》）和内容参差
- **25 条四语术语**: 梵 (IAST) — 藏 (Wylie + Unicode) — 汉 — 英，含释义和别译

---

## 四大阶段路线图

| 阶段 | 时间 | 核心交付 |
|------|------|---------|
| **Phase 1** 基础构建 | 1-8 月 | 华严宗部文献总目录 + 数据管道 |
| **Phase 2** 知识图谱 | 6-18 月 | 交互式人物关系/时空可视化 |
| **Phase 3** 藏汉对译 | 12-36 月 | 藏译华严特有品目汉英双译本 |
| **Phase 4** 整合发布 | 30-48 月 | 华严云端修学平台 v1.0 |

---

## 技术栈

| 层级 | 技术 |
|------|------|
| 版本控制 | Git + Git LFS |
| 数据管道 | Python 3.11+ (Click, lxml, pandas, spaCy) |
| 关系数据库 | SQLite (含 FTS5 全文检索) |
| 图数据库 | Neo4j Community |
| 前端可视化 | Next.js / Observable Framework + D3.js + Leaflet |
| 部署 | Cloudflare Pages / Vercel |

---

## 快速开始

```bash
# 安装 Python 依赖
pip install -e .

# 初始化文献目录数据库
huayan catalog init

# 启动 Neo4j 图谱 (需要 Docker)
make graph-start

# 初始化图谱 Schema
huayan graph init

# 加载图谱数据
huayan graph load
```

---

## 数据源

- **CBETA** (cbeta.org) — 汉文大藏经数字化全文
- **BDRC/BUDA** (bdrc.io) — 藏文甘珠尔 IIIF API
- **84000** (84000.co) — 藏文华严英译 + 三语术语库
- **义天录** — 新编诸宗教藏总录（文献真伪鉴定基准）

---

## 许可

MIT License
