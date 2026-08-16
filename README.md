# 华严宗部文献与修行资料数字化梳理

构建以华严宗为核心的佛法文献与修行资料数字化系统。

- **多维知识图谱** — 92位祖师/行者传承谱系 · 96条传承边 · 46处道场 · 175条人物轨迹 · 73处文明疆域
- **多维格义** — 梵-于阗-藏-汉-满-英多语对读 + 藏汉华严品目差异对比 (Toh44 45品 vs 汉文39品) · 50条四语术语
- **教海行云** — 修行体系·禅观法要·杜顺五教止观·华严判教·实修心要·讲法资源
- **前沿对话** — 华严与AI/神经科学/心灵哲学/儒家/道家/基督教等跨传统对话
- **世主妙严** — 华藏世界海曼荼罗 · 三界诸天图 · 艺术珍品 · 梵呗
- **灵性仁本** — 灵性经济学/人本经济学/修行传统与永续/本土知识体系

> m📖 详见 [CLAUDE.md](CLAUDE.md) · [docs/next-phase-plan.md](docs/next-phase-plan.md) · [docs/architecture.md](docs/architecture.md)

---

## Demo

**[web/demo/index.html](web/demo/index.html)** — 导航主页，6个独立Tab页面：

| Tab | 名称                 | 说明                                          |
| --- | -------------------- | --------------------------------------------- |
| 1   | 法脉传承·时空长河   | 交互式时间轴 + 全球文明地图 + 92节点动画      |
| 2   | 华严文献·雅思渊才   | 藏汉品目差异矩阵 + 四语术语 + 文本系谱        |
| 3   | 教海行云·信解行证   | 修行体系 + 禅观法要 + 杜顺五教止观 + 华严判教 |
| 4   | 前沿对话·跨界研究   | AI/神经科学/心灵哲学跨学科对话 + 文献综述     |
| 5   | 世主妙严·华藏世界海 | 二十重世界曼荼罗 + 三界诸天 + 艺术珍品        |
| 6   | 灵性仁本·澄明永续   | 灵性经济学 + 人本经济学 + 本土知识体系        |

---

## 快速开始

```bash
conda activate hy_py312

# 构建 Demo
python web/demo/scripts/build.py

# 本地预览
python -m http.server 8080 -d web/demo
# → http://localhost:8080
```

## 知识管理架构

```
L1: YAML/SQLite (权威数据源) → L2: build.py (构建) → L3: HTML (展示)
```

所有知识性内容先进 `data/` YAML 数据层，再由 build.py 注入 HTML，严禁硬编码在 JS 中。
详见 [docs/knowledge-management.md](docs/knowledge-management.md) · [docs/reference-management.md](docs/reference-management.md)

## 技术栈

- **前端**: 纯 HTML/CSS/JS + Canvas + Leaflet (CDN)
- **数据**: YAML + SQLite + JSON
- **构建**: Python 3.12 (conda: `hy_py312`)
- **部署**: GitHub Pages (main分支 `/docs` 目录)
