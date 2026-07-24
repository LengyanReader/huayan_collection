# CLAUDE.md — 华严宗部文献与修行资料数字化梳理

## 项目概述

构建以华严宗为核心的佛法文献与修行资料数字化系统：
1. **多维知识图谱** — 华严宗祖师/行者传承谱系、地理道场、经典关联（36 人，17 处地点，12 法系）
2. **藏汉华严对译** — 藏文《华严经》(Toh 44, 45品) vs 汉文 (39品) 差异比对，A阶段品目级完成

## Demo

**[web/demo/index.html](web/demo/index.html)** — 40KB 自包含单文件，双击即开
- Tab 1: 法脉传承·时空长河 (分层时间轴 + 双语地图 + 多地时空联动)
- Tab 2: 汉藏华严差异对比 (版本对照 + 差异分布 + 逐品详情 + 学界观点 + 参考文献)

## 核心文档索引

| 文档 | 路径 | 说明 |
|------|------|------|
| 架构设计 | [docs/architecture.md](docs/architecture.md) | 数据模型、模块职责、接口契约 |
| 后续计划 | [docs/next-phase-plan.md](docs/next-phase-plan.md) | 两方向8周路线图 |
| 技术栈 | [docs/tech-stack.md](docs/tech-stack.md) | 轻量化技术选型 |
| 可视化研究 | [docs/visualization-research.md](docs/visualization-research.md) | 系谱可视化方案分析 |
| 工程工作流 | [docs/engineering-workflow.md](docs/engineering-workflow.md) | Loop/Graph Engineering |
| 翻译规范 | [docs/translation-guide.md](docs/translation-guide.md) | 藏汉对译玄奘体规范 |
| 多语对读 | [docs/multilingual-alignment.md](docs/multilingual-alignment.md) | 梵-于阗-藏-汉-满-英对读架构 |
| 校验框架 | [docs/verification-framework.md](docs/verification-framework.md) | 三级来源分级 + 验证状态机 |
| 资源清单 | [data/references/resource-inventory.md](data/references/resource-inventory.md) | 数据源/工具/文献全覆盖 |
| 文献目录 | [data/catalog/complete_catalog.yaml](data/catalog/complete_catalog.yaml) | 60+ 部经典 + 语境警告 |
| 品目差异 | [data/translation/diff_matrix.yaml](data/translation/diff_matrix.yaml) | 藏汉45×39品差异矩阵 |
| 差异总览 | [data/translation/gap_analysis.md](data/translation/gap_analysis.md) | A阶段差异框架 + 学界观点 |

## 技术栈 (轻量化原则)

- **前端 Demo**: 纯 HTML/CSS/JS + Canvas + Leaflet (CDN), 单文件 46KB
- **数据**: 内嵌 JSON, 零构建步骤, 零 fetch 请求
- **数据存储**: SQLite + Neo4j Community (后端规划)
- **AI 层**: Ollama + qwen2.5:7b + dmeta-embedding-zh (规划中)
- **ETL**: Python 3.12 (conda env: hy_py312)
- **部署**: 本地文件双击 → 未来 Cloudflare Pages

## 目录约定

```
huayan_collection/
├── data/
│   ├── catalog/              SQLite 数据库 + 完整目录 YAML
│   ├── knowledge_graph/      人物/传承/地点 JSON + Neo4j Cypher + Schemas
│   ├── translation/          品目差异矩阵 + 四语术语库 + 翻译草稿
│   ├── texts/                经典全文 (Markdown + YAML)
│   └── references/           研究参考 + 资源清单
├── src/                      Python 源码 (待实现)
│   ├── cli/                  CLI 入口
│   ├── catalog/              文献目录服务
│   ├── graph/                图谱服务
│   └── translation/          对译服务
├── web/                      前端 (待实现)
├── docs/                     架构/技术栈/工作流/翻译规范
└── scripts/                  Neo4j 启动/设置脚本
```

## 核心数据原则

1. **语境关联**: 别译本、眷属经的标注必须基于整体内容判断，不可望文生义
2. **置信度标注**: 所有人物/文献实体的 source 字段必须标注出处，verified 字段区分"传统记载"和"学术确认"
3. **渐进完备**: 每个数据文件有明确的可度量完备度百分比
4. **Loop Engineering**: 每个变更经过 Data→Graph→Verify→Fix→Demo 闭环

## 快速命令

```bash
conda activate hy_py312                  # 激活环境
make neo4j-console                       # 启动 Neo4j
make verify-data                         # 数据验证
make verify-graph                        # 图谱质量检查
make report                              # 完备性报告
make env-info                            # 环境信息
```
