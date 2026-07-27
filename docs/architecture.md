# 华严宗部数字化梳理平台 — 架构设计

> 更新: 2026-07-27 | Demo v0.7

## 一、系统全景

```
                        用户界面层
        ┌─────────────────────────────────────┐
        │  web/demo/index.html (78KB 单文件)   │
        │  Tab1: 法脉传承 │ Tab2: 汉藏差异      │
        │  Tab3: 华严行法                       │
        └──────────┬──────────────────────────┘
                   │
        ┌──────────▼──────────────────────────┐
        │          数据层 (内嵌JSON)           │
        │  GRAPH: 47人/34边/18地点             │
        │  GAP:   版本对照/差异矩阵/术语库       │
        └──────────┬──────────────────────────┘
                   │
        ┌──────────▼──────────────────────────┐
        │        数据文件层 (data/)            │
        │  knowledge_graph/ + translation/     │
        │  + catalog/ + references/            │
        └─────────────────────────────────────┘
```

## 二、核心数据模型

### Person (人物)
```
id, n(name), dy(dynasty), ti(title), li(lineage), multi[secondary lineages]
tp(type: patriarch|translator|scholar|practitioner)
b(birth), d(death), bio, wk(works[])
_isGhost: 多法脉副条目标记
```

### Edge (传承边)
```
s(source), t(target), r(relation: MASTER|INFLUENCE|LINEAGE|CONTEMPORARY), li(lineage)
```

### Location (地点)
```
id, n(name), lat, lng, tp(type: temple|mountain|region), dy(dynasty), ds(description), ps(persons[])
```

### 法系颜色映射
```
华严五祖=#b8863c 华严莲社=#5e8b9e 月霞系=#7a9ec0 贤首宗高原法系=#c46b5d
临济宗=#d48476 高丽华严=#6d9a6e 日本华严=#8b7a9e 李通玄系=#c8893e
慈舟系=#8b7a9e 译师=#a09080 印度源流=#9e8b6e 当代学者=#b0a898
```

## 三、源码模块（web/demo/src/）

| 文件 | 职责 | 行数 |
|------|------|------|
| `template_top.html` | HTML骨架 + CSS + 控件 | 110 |
| `template_bottom.html` | 闭合标签 | 3 |
| `data.js` | GRAPH+GAP数据占位 + 全局变量 | 10 |
| `lineage.js` | buildTimelineRows/drawTL/initMap/selectPerson/showInfo/onWheel等 | 270 |
| `gap.js` | renderGap/switchGapView/loadParallelChapter | 250 |
| `practice.js` | renderPractice | 130 |
| `init.js` | 初始化 + 事件绑定 + 书签 + 动画 | 50 |

## 四、构建与验证

```
data/knowledge_graph/*.json ──┐
data/translation/*.yaml ─────┤
                              ├── build.py ──→ index.html (78KB)
web/demo/src/*.js ────────────┤
web/demo/src/*.html ──────────┘

verify_demo.py: 18项自动检查
  1. <!DOCTYPE html> 开头
  2. </html> 结尾
  3. <script> 在 </html> 之前
  4. 无 </script> 出现在JS内容中
  5. 无 fetch() 调用
  6. 括号平衡
  7. 文件大小 (25-80KB)
  8-12. 关键函数存在
  13. 关键人物数据存在
  14-15. 事件监听器存在
  16. 无未转义引号
  17-18. 3个Tab存在
