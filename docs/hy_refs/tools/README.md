# docs/hy_refs/tools — 字幕/文献处理工具集

本目录存放华严项目 `hy_refs`（参考文献档案）相关的 **可复用处理工具**。
每个工具独立子目录，代码与数据分离（工具通过 `config.json` 中的 `workspace` 指向数据目录）。

## 工具索引

| 目录 | 用途 | 状态 |
|---|---|---|
| [`sub_extract/`](sub_extract/) | YouTube 硬字幕 OCR 重建（路线 D） | ✅ 生产中 |

## 约定

- 每个工具自含：脚本 + config + helper scripts + README
- 数据/产物不入工具目录（由 workspace 指定外部路径）
- 工具代码可版本控制（无大文件）；workspace 数据不入 git
- 新工具请附 README，说明用途、环境要求、使用方式

## 版本控制

本目录已通过 `.gitignore` 例外规则纳入 git：
```
docs/hy_refs/*          ← 排除所有内容
!docs/hy_refs/tools/    ← 但保留 tools/ 入库
```

## 环境依赖

- Python 3.12 (conda `hy_py312`)
- ffmpeg (系统 PATH)
- PaddleOCR 3.7 / PP-OCRv6
- yt-dlp, OpenCV

## 扩展方向（待开发）

- 批量字幕校对工具（三源互证辅助）
- OCR 结果 post-processing（简繁统一、幻灯片段智能分离）
- 音频转写工具线（若有可用 ASR 模型）
