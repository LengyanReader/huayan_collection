# 华严宗部文献与修行资料数字化梳理

构建以华严宗为核心的佛法文献与修行资料数字化系统。

- **多维知识图谱** — 92位祖师/行者传承谱系 · 96条传承边 · 46处道场 · 175条人物轨迹 · 73处文明疆域
- **藏汉华严对译** — 藏文《华严经》(Toh 44, 45品) vs 汉文 (39品) 差异对比 · 50条四语术语
- **教海行云** — 修行体系·禅观法要·实修心要·讲法资源
- **前沿对话** — 华严与AI/神经科学/心灵哲学/儒家/道家/基督教等跨传统对话
- **世主妙严** — 华藏世界海曼荼罗 · 三界诸天图 · 艺术珍品 · 梵呗

> 📖 详见 [CLAUDE.md](CLAUDE.md) · [docs/next-phase-plan.md](docs/next-phase-plan.md) · [docs/architecture.md](docs/architecture.md)

---

## Demo

**[web/demo/index.html](web/demo/index.html)** — 导航主页，5个独立Tab页面：

| Tab | 名称 | 说明 |
|-----|------|------|
| 🌊 | **法脉传承**·时空长河 | Canvas时间轴 + 大地图 + 7区域迷你地图 + 85节点动画 + 古地图模式 |
| 📜 | **华严文献**·雅思渊才 | 版本对照 · 差异矩阵 · 术语库 · 三语对读 · 文本系谱 |
| 🧘 | **教海行云**·信解行证 | 修行体系 · 禅观法要(含实修心要) · 讲法资源 |
| 🔬 | **前沿对话**·跨界研究 | 与华严/汉传/佛教/其他宗教行门的对话 + 文献综述 |
| 🪷 | **世主妙严**·华藏世界海 | 二十重世界曼荼罗 · 三界诸天 · 艺术珍品 · 梵呗 |

---

## 知识管理架构

```
L1: SQLite (权威数据源)  →  L2: Neo4j (图验证引擎)  →  L3: YAML/JSON → HTML
```

**⚠️ 知识管理核心纪律：所有展示内容必须来源于 `data/` 目录下的结构化数据文件（SQLite / YAML / JSON），严禁在任何构建脚本或前端代码中硬编码数据。** 新增内容必须先写入权威数据源 → 导出 → 构建 → 验证，详见 [docs/knowledge-management.md](docs/knowledge-management.md) 与 [CLAUDE.md](CLAUDE.md)

---

## 数据规模

| 类别 | 数量 | 存储 |
|------|------|------|
| 图谱人物 | 92人 | SQLite persons表 + graph.json |
| 人物轨迹 | 175条 | data/events/person_trajectories.yaml |
| 传承关系边 | 96条 | graph.json |
| 代表道场 | 46座 | data/locations/temple_directory.yaml |
| 四语术语 | 50条 | glossary.yaml + SQLite glossary表 |
| 华严批注 | 57人物+18事件 | data/events/huayan_annotations.yaml |
| 历史事件 | 44条 | data/events/key_events.yaml |
| 文明疆域 | 73处(中国23+世界50) | data/events/world_civilizations.yaml |
| 区域时间线 | 45条西方+中东中亚北非35+撒哈拉以南非洲10+/美洲/大洋洲/儒道各15+ | data/events/*_timeline.yaml |
| 实修心要文章 | 11篇 | docs/hy_refs/wechat/ |

---

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | 纯 HTML/CSS/JS + Canvas + Leaflet (CDN), 6个独立页面 |
| 构建 | Python 3.12 (conda env: `hy_py312`) + build.py |
| 数据库 | SQLite 3 (权威数据源) + Neo4j (图验证) |
| 数据交换 | YAML/JSON → build.py 构建内嵌 |
| 部署 | 本地双击 → GitHub Pages |

---

## 快速命令

```bash
conda activate hy_py312

# 数据导出: SQLite → JSON/YAML
python scripts/export_sqlite_to_json.py

# 图验证: SQLite → Neo4j + Cypher检查
python scripts/load_neo4j.py --verify

# 来源可靠性验证
python scripts/verify_sources.py

# 构建Demo (6个HTML + CSS + JS)
python web/demo/scripts/build.py

# 构建产物验证
python scripts/verify_demo.py
```

---

## 项目结构

```
huayan_collection/
├── web/demo/
│   ├── index.html              # 导航主页
│   ├── css/common.css          # 共享样式
│   ├── js/common.js            # 共享脚本(评论系统/GitHub认证)
│   ├── tabs/
│   │   ├── lineage.html        # 法脉传承
│   │   ├── gap.html            # 华严文献
│   │   ├── jiaoxing.html       # 教海行云
│   │   ├── frontier.html       # 前沿对话
│   │   └── cosmology.html      # 世主妙严
│   ├── src/                    # 源文件(供build.py组装)
│   └── scripts/build.py        # 构建脚本
├── data/
│   ├── catalog/                # SQLite Schema + huayan.db
│   ├── knowledge_graph/        # 人物·关系·地点 JSON
│   ├── translation/            # 差异矩阵·术语库 YAML
│   ├── practice/               # 修行体系 YAML
│   ├── frontier/               # 跨界对话 YAML
│   ├── cosmology/              # 宇宙观 YAML
│   ├── events/                 # 事件·动画·时间线 YAML
│   └── locations/              # 道场名录 YAML
├── docs/                       # 项目文档
├── scripts/                    # 导出/验证/Neo4j脚本
└── CLAUDE.md                   # AI助手指令
```

## 数据源

- **CBETA** (cbetaonline.dila.edu.tw) — 汉文大藏经
- **BDRC** (bdrc.io) — 藏文甘珠尔
- **84000 Project** (84000.co) — 藏文华严英译+术语库
- **大华严寺官网** (huayenworld.org) — 修行体系·法脉资料
- **高僧传·灯录·正史** — 人物传记文献依据

## 许可

MIT License
