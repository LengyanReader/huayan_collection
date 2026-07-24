# 华严宗部数字化梳理平台 — 架构设计 (v0.2)

> **更新**: 2024-07-24 — 新增轻量技术栈方案、Loop/Graph Engineering 工作流、完备资源清单
>
> 配套文档:
> - [技术栈设计](tech-stack.md) — 组件选型与渐进增强
> - [工程工作流](engineering-workflow.md) — 闭环开发验证方法论
> - [翻译规范](translation-guide.md) — 藏汉对译标准

---

## 一、系统全景

```
                        用户界面层
        ┌─────────────────────────────────────┐
        │  CLI (huayan)  │  Observable (Web)   │
        │  文献查询/图谱   │  数据叙事/可视化     │
        └──────────┬──────────────────┬────────┘
                   │                  │
        ┌──────────▼──────────────────▼────────┐
        │          应用服务层 (Python)           │
        │  ┌─────────┐ ┌──────┐ ┌───────────┐ │
        │  │ Catalog │ │Graph │ │Translation│ │
        │  │ Service │ │Service│ │  Service  │ │
        │  └────┬────┘ └──┬───┘ └─────┬─────┘ │
        └───────┼─────────┼───────────┼───────┘
                │         │           │
        ┌───────▼─────────▼───────────▼───────┐
        │           数据存储层                  │
        │  ┌──────┐ ┌───────┐ ┌────────────┐  │
        │  │SQLite│ │ Neo4j │ │  LanceDB   │  │
        │  │目录   │ │ 图谱  │ │  向量检索   │  │
        │  └──────┘ └───────┘ └────────────┘  │
        └─────────────────────────────────────┘
                │
        ┌───────▼─────────────────────────────┐
        │        AI 辅助层 (Ollama 本地)        │
        │  ┌─────────────────┐  ┌───────────┐ │
        │  │ qwen2.5:7b      │  │ dmeta-emb │ │
        │  │ 实体提取/翻译/QA │  │ 文本向量化 │ │
        │  └─────────────────┘  └───────────┘ │
        └─────────────────────────────────────┘
```

## 二、数据模型

详见 [architecture.md (原始版本)](architecture.md) 中的数据模型部分，核心表结构不变。

新增:
- `data/catalog/complete_catalog.yaml` — 60+ 部文献的完整目录，含语境关联标注
- `data/references/resource-inventory.md` — 所有资源清单与完备性追踪

## 三、工程方法论

本项目采用 **Loop Engineering + Graph Engineering** 双轨方法：

- **Loop Engineering**: 数据→图谱→验证→修复→演示 的闭环迭代
- **Graph Engineering**: 以图谱连通性、一致性、完备性为质量度量标准

详见 [engineering-workflow.md](engineering-workflow.md)。

## 四、当前数据资产

| 资产 | 数量 | 完备度 |
|------|------|--------|
| 人物 | 43 人 | ~85% |
| 传承系谱 | 11 条 | ~90% |
| 道场 | 15 处 | ~80% |
| 文献目录 | 60+ 部 | ~95% (目录级) |
| 品目差异 | 45 品 × 39 品 | ~80% (待段落级) |
| 术语库 | 25 条 | ~25% (目标 100+) |
| JSON Schema | 3 个 | 100% |

## 五、目录结构（简表）

```
huayan_collection/
├── README.md
├── CLAUDE.md
├── pyproject.toml
├── Makefile
├── .gitignore
├── data/
│   ├── catalog/
│   │   ├── schema.sql
│   │   └── complete_catalog.yaml          ← 新增: 完整文献目录
│   ├── knowledge_graph/
│   │   ├── personas.json                  ← 扩充: 43人
│   │   ├── lineages.json                  ← 扩充: 11条
│   │   ├── locations.json
│   │   ├── neo4j_import/init.cypher
│   │   └── schemas/
│   ├── translation/
│   │   ├── diff_matrix.yaml
│   │   └── glossary.yaml
│   ├── texts/
│   │   ├── sutras/ commentaries/ rituals/ modern/
│   └── references/
│       ├── ref.md
│       └── resource-inventory.md           ← 新增: 资源清单
├── src/                                    (待实现)
├── web/                                    (待实现)
├── docs/
│   ├── architecture.md
│   ├── tech-stack.md                       ← 新增: 轻量技术栈
│   ├── engineering-workflow.md             ← 新增: 工程工作流
│   └── translation-guide.md
└── scripts/
    ├── neo4j-start.bat
    └── neo4j-setup.sh
```
