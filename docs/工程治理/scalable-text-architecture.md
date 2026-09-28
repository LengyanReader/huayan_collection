# 大规模经文对比·可扩展架构方案

> 2026-07-30 | 应对94KB单文件增长至数百KB的架构升级

## 问题

当前 `index.html` 94KB，所有数据（47人物/30术语/文本系谱/前沿对话）内嵌在单文件中。随着后续加入：
- 十地品全文段落（~50KB汉字）
- 入法界品全文段落（~100KB+）
- 藏文独有2品内容
- 更多校勘注

单文件将迅速突破 200KB+，加载性能不可接受。

## 方案：分层加载 + 数据外置

### 架构图

```
index.html (核心框架 ~15KB)
  ├── data/graph.json       (~15KB)  — 法脉人物/传承/地点数据
  ├── data/gap.json         (~5KB)   — 汉藏差异矩阵/术语库
  ├── data/practice.json    (~3KB)   — 华严行法内容模板
  ├── data/frontier.json    (~5KB)   — 前沿对话内容
  └── data/texts/           (按需加载)
        ├── ch31-ten-bhumis.json     — 十地品对读段落
        ├── ch45-ganvyuha.json       — 入法界品段落
        ├── ch11-tathagata.json      — 如来华严品(待)
        └── ch40-transcending.json   — 离世间品段落
```

### 加载策略

| 层级 | 内容 | 加载时机 | 大小 |
|------|------|---------|------|
| **核心层** | HTML骨架+Canvas+Map+Tab切换 | 首次加载 | ~15KB |
| **数据层** | GRAPH+GAP+Practice+Frontier | 首次加载(并行fetch) | ~30KB |
| **文本层** | 经文对读段落 | 用户点击品目时按需加载 | 每品5-50KB |

### 优势

1. **首次加载速度**：核心框架 15KB + 数据 30KB = ~45KB 首屏
2. **按需加载**：用户不查看的经文不加载
3. **独立缓存**：每个JSON文件可被浏览器独立缓存
4. **并行加载**：多个fetch同时发起（`Promise.all`）
5. **渐进增强**：当前94KB单文件可直接拆分，无需重写逻辑

### 实现步骤

| Step | 内容 | 影响 |
|------|------|------|
| 1 | 将 GRAPH/GAP 数据从内联JS提取为独立JSON文件 | 主HTML缩小至~50KB |
| 2 | 将 renderPractice/renderGap/renderFrontier 的内容模板提取为JSON | 进一步缩小至~20KB |
| 3 | 修改数据赋值逻辑：`var GRAPH = __GRAPH__` → `fetch('data/graph.json').then(...)` | 增加异步加载逻辑 |
| 4 | 按需加载经文段落（用户选择品目时fetch对应JSON） | 文本层独立 |
| 5 | 加入loading状态/骨架屏 | 用户体验 |

### 兼容性

- 本地文件打开（`file://`）：fetch不支持 → 需用内联fallback或localStorage
- GitHub Pages（`https://`）：fetch完全支持
- 离线模式：可使用Service Worker缓存JSON

### 与当前构建流程的整合

```
当前:  build.py → index.html (94KB单文件)
未来:  build.py → index.html (15KB) + data/*.json (79KB)
       deploy → 推送所有文件至GitHub Pages
```
