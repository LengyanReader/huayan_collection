# CLAUDE.md — 华严宗部文献与修行资料数字化梳理

## 项目概述

构建以华严宗为核心的佛法文献与修行资料数字化系统：
1. **多维知识图谱**：华严宗祖师/行者传承谱系、地理道场、经典关联（47 人，18 处地点，34 条传承边）
2. **藏汉华严对译**：藏文《华严经》(Toh 44, 45品) vs 汉文 (39品) 差异比对，A阶段品目级完成，B阶段十地品对读已启动

## Demo

**[web/demo/index.html](web/demo/index.html)** — 78KB 自包含单文件
- Tab 1: 法脉传承·时空长河 (Canvas时间轴 + 双语地图 + 多法脉Ghost + 双人对比 + 动画播放)
- Tab 2: 汉藏华严差异对比 (子导航三页 + 三语对读 + 30条术语 + 84000校勘注)
- Tab 3: 华严行法 (修行蓝图 + 五教止观可折叠 + 技术面/工程面双轨 + 50+著作清单)

## 核心文档索引

| 文档 | 路径 | 说明 |
|------|------|------|
| 后续计划 | [docs/next-phase-plan.md](docs/next-phase-plan.md) | 三方向完整现状 + P0/P1/P2 路线图 |
| 架构设计 | [docs/architecture.md](docs/architecture.md) | 数据模型、模块职责 |
| 工程工作流 | [docs/engineering-workflow.md](docs/engineering-workflow.md) | Loop/Graph Engineering |
| 翻译规范 | [docs/translation-guide.md](docs/translation-guide.md) | 藏汉对译玄奘体规范 |
| 多语对读 | [docs/multilingual-alignment.md](docs/multilingual-alignment.md) | 梵-于阗-藏-汉-满-英对读架构 |
| 校验框架 | [docs/verification-framework.md](docs/verification-framework.md) | 三级来源分级 + 验证状态机 |
| 可视化研究 | [docs/visualization-research.md](docs/visualization-research.md) | 系谱可视化方案分析 |
| 海云体系 | [docs/ref海云继梦法师_佛法修行体系研究.md](docs/ref海云继梦法师_佛法修行体系研究.md) | 外部参考文档（只读） |

## 技术栈

- **前端 Demo**: 纯 HTML/CSS/JS + Canvas + Leaflet (CDN), 单文件 ~78KB
- **数据**: 内嵌 JSON, 零构建步骤, 零 fetch 请求
- **ETL**: Python 3.12 (conda env: hy_py312)
- **部署**: 本地双击 → GitHub Pages

## 开发流程

```bash
# 编辑源码 (web/demo/src/ 下7个文件)
code web/demo/src/lineage.js

# 构建 + 18项验证
make demo

# 本地预览 (localhost:8080)
make demo-serve

# 一键部署
make demo-deploy
```

## 目录约定

```
huayan_collection/
├── web/demo/
│   ├── index.html           # 构建产出
│   ├── src/                 # 7个源文件
│   │   ├── template_top.html/bottom.html
│   │   ├── data.js          # DATA + globals
│   │   ├── lineage.js       # Canvas/Map/Select/Interact/Tabs
│   │   ├── gap.js           # Tab2 汉藏差异
│   │   ├── practice.js      # Tab3 华严行法
│   │   └── init.js          # Init + Events + Bookmarks
│   └── scripts/build.py     # 构建脚本
├── data/                    # 数据文件
│   ├── knowledge_graph/     # JSON + YAML
│   ├── translation/         # YAML
│   ├── catalog/             # SQL + YAML
│   └── references/          # 参考文档
├── docs/                    # 项目文档
├── scripts/                 # 验证/Neo4j脚本
└── src/                     # Python后端(待实现)
```

## 快速命令

```bash
conda activate hy_py312
make demo              # 构建 + 验证
make demo-serve        # 本地预览
make demo-deploy       # 部署到 GitHub Pages
```
