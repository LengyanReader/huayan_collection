# CLAUDE.md — 华严宗部文献与修行资料数字化梳理

## 项目概述

构建以华严宗为核心的佛法文献与修行资料数字化系统：
1. **多维知识图谱**：华严宗祖师/行者传承谱系、地理道场、经典关联（**65 人**，18 处地点，**53 条**传承边）
2. **藏汉华严对译**：藏文《华严经》(Toh 44, 45品) vs 汉文 (39品) 差异比对
3. **华严宇宙观**：华藏世界海曼荼罗 + 三界诸天图

## Demo

**[web/demo/index.html](web/demo/index.html)** — **~184KB** 自包含单文件
- Tab 1: 法脉传承·时空长河 (Canvas时间轴 + 理论/修行图层 + 主地图+缩略图 + 42节点动画播放 + 古地图模式)
- Tab 2: 汉藏华严差异对比 (子导航四页 + 三语对读 + 30条术语 + 文本系谱)
- Tab 3: 华严行法 (子导航三页·修行体系/禅观法要/讲法资源 + YouTube集成)
- **Tab 4: 前沿对话** (AI/计算现象学/神经科学/心灵哲学 + 文献综述)
- **Tab 5: 华严其观** (华藏世界海曼荼罗 + 三界诸天图)

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

- **前端 Demo**: 纯 HTML/CSS/JS + Canvas + Leaflet (CDN), 单文件 ~192KB
- **数据**: 结构化 JSON/YAML 源文件 → build.py 构建内嵌
- **ETL**: Python 3.12 (conda env: hy_py312)
- **部署**: 本地双击 → GitHub Pages

## ⚠️ 知识管理核心规则

**所有内容必须来源于结构化源文件，严禁硬编码在 build.py 或 JS 中。**

| Tab | 内容类型 | 源文件 |
|-----|---------|--------|
| 法脉传承 | 人物/边/地点 | `data/knowledge_graph/*.json` |
| 法脉传承 | 事件/动画/传播 | `data/events/*.yaml` (待建) |
| 汉藏文献 | 差异矩阵/术语 | `data/translation/*.yaml` |
| 华严行法 | 修行体系 | `data/practice/` (待建) |
| 前沿对话 | 文献/论文 | `data/frontier/` (待建) |
| 华严其观 | 宇宙观 | `data/cosmology/` (待建) |

**新增内容流程**: ①写入源文件 → ②`build.py`构建 → ③验证人数/边数 → ④提交

详见 [docs/knowledge-management.md](docs/knowledge-management.md)

## 开发流程

```bash
# 编辑源数据 (JSON/YAML) 或源码 (web/demo/src/)
code data/knowledge_graph/personas.json
code web/demo/src/lineage.js

# 构建
C:/Users/data/miniconda3/envs/hy_py312/python.exe web/demo/scripts/build.py

# 本地预览 (打开 web/demo/index.html)
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
