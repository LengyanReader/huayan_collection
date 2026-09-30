# 硬字幕 OCR 提取工具 (sub_extract)

从 YouTube 烧录字幕（hardsub）视频中通过 OCR 重建带时间码的字幕文本。

**所属**：`docs/hy_refs/tools/` · 华严项目路线 D（寺方字幕档案恢复）  
**产物性质**：OCR 重建稿 · 待校定（非寺方定稿，需三源互证另行校定）

---

## 快速使用

```powershell
cd docs/hy_refs/tools/sub_extract

# 全流程（含下载 + 报告）
python batch.py <vid1> <vid2> ...

# 多 Lane 并行（3 路推荐）
pwsh -File launch.ps1 -Lane a -Vids "vid1,vid2"
pwsh -File launch.ps1 -Lane b -Vids "vid3,vid4"
pwsh -File launch.ps1 -Lane c -Vids "vid5,vid6"

# 查看进度
pwsh -File monitor.ps1
```

---

## 架构

```
tools/sub_extract/              ← 本目录（纯代码，可版本控制）
├── pipeline.py                 # 核心四阶段：extract / dedup / ocr / merge
├── batch.py                    # 批量驱动：download→…→report，阶段跳过+增量续跑
├── report.py                   # 自包含 HTML 交付报告（base64 嵌图）
├── config.json                 # 版式参数 + workspace 路径
├── launch.ps1                  # Lane 启动器（PATH + encoding + 隔离）
├── monitor.ps1                 # 进度一览（扫描 workspace 中 vid 目录）
├── det_test.py                 # 确定性验证（证明线程数不影响 OCR 结果）
└── README.md                   # 本文件

<workspace>/                    ← config.json.workspace 指定的数据目录
├── <vid>.mp4                   # 下载视频
├── <vid>.info.json             # 元数据
├── batch_status_{lane}.log     # Lane 状态日志
├── lane_{lane}.out             # Lane stdout/stderr
└── <vid>/                      # 每片产物（完全隔离）
    ├── frames/                 # 抽帧 (frame_NNNNNN.jpg)
    ├── reps/                   # 去重代表帧
    ├── runs.tsv                # run 索引
    ├── ocr_out.tsv             # OCR 结果（增量 append）
    ├── <vid>.srt / <vid>.md    # 最终字幕
    └── 字幕重建報告_*.html     # 交付报告
```

**设计原则**：代码与数据分离。`workspace` 路径在 `config.json` 中配置，
换目录只需改此一项；数据可清理/归档，代码永久保留。

---

## 处理流水线

| # | 阶段 | 命令 | 工具 | 输入→输出 |
|---|---|---|---|---|
| 1 | Download | `batch.py <vid>` (自动) | yt-dlp | URL → `<vid>.mp4` (720p) |
| 2 | Extract | `pipeline.py extract <vid>` | ffmpeg | mp4 → frames/ (1fps crop) |
| 3 | Dedup | `pipeline.py dedup <vid>` | OpenCV | frames/ → reps/ + runs.tsv |
| 4 | OCR | `pipeline.py ocr <vid>` | PaddleOCR | reps/ → ocr_out.tsv |
| 5 | Merge | `pipeline.py merge <vid>` | Python | runs.tsv + ocr_out.tsv → .srt/.md |
| 6 | Report | `report.py <vid>` | Python | .md + reps/ + info.json → .html |

### 字幕带裁剪区域（config.json）

画面中央 64% 宽 × 底部 15.5% 高 —— 覆盖白字/黄字字幕带，
避开右侧竖排标题（"九九華嚴講座 NN"）和左下幻灯片页脚。

---

## 配置参数 (`config.json`)

| 参数 | 默认 | 说明 |
|---|---|---|
| `workspace` | (当前绝对路径) | 数据目录，所有 IO 基于此 |
| `fps` | 1 | 抽帧频率 |
| `crop_x/y/w/h` | 0.18/0.845/0.64/0.155 | 字幕带裁剪比例 |
| `mask_iou` | 0.82 | 相邻帧 IoU ≥ 此值 → 同一字幕 |
| `ink_min` | 0.0035 | 文字像素占比 < 此值 → 无字幕 |
| `white_v` | 200 | 白色像素灰度阈值 |
| `ocr_lang` | chinese_cht | PaddleOCR 语言模型 |
| `ocr_threads` | 1 | 每 lane 线程钉定数（保证确定性+避免超订） |
| `box_cx_min/max` | 0.2/0.8 | OCR 结果水平位置过滤范围 |

---

## 并行质量保障

**核心结论**：线程数不影响 OCR 识别结果（已由 `det_test.py` 实证：40 帧仅 1 帧差异为行尾空格）。

| 风险 | 对策 |
|---|---|
| 线程超订 → 吞吐倒退 | `OMP/MKL/OPENBLAS/FLAGS_num_threads=1` + `paddle.base.core.set_num_threads(1)` |
| 多 Lane 写同一文件 | 按 vid 分目录（零共享）；`batch_status_{LANE}.log` 隔离 |
| OCR 崩溃丢帧 | ocr_out.tsv 逐行 append+flush；resume 跳过已完成帧 |
| paddle↔torch DLL 冲突 (WinError 127) | 导入顺序：paddleocr → paddle |
| cp1252 中文崩溃 | `sys.stdout.reconfigure(encoding="utf-8")` + `PYTHONIOENCODING=utf-8` |
| PaddleOCR oneDNN PIR crash | `enable_mkldnn=False` |
| 片头/侧边污染 | 文本框水平位置过滤 + merge 去重 |

---

## 环境要求

| 组件 | 要求 |
|---|---|
| Python | 3.12 · conda env `hy_py312` |
| PaddleOCR | 3.7 · PP-OCRv6 (chinese_cht) |
| ffmpeg | 系统 PATH 可用 |
| yt-dlp | pip in hy_py312 |
| OpenCV | opencv-python |
| RAM | ~1 GB per OCR lane（3 lanes ≈ 3 GB） |
| CPU | 每 lane ~3 核（钉定后），3 lanes ≈ 9/16 核 |

模型缓存（首次自动下载）：`~/.paddlex/official_models/PP-OCRv6_medium_{det,rec}`

---

## 性能（实测）

- OCR 吞吐：**~20 帧/min/lane**（单线程钉定）
- 单片（~3600 reps）OCR 耗时：**~3-5 h**
- 3 Lane 并行处理 12 集（~30h 视频）：**~15-16 h** wall time
- 每 lane 内存占用：~724 MB

---

## 目标频道

**@huayen-world** · 播放列表 `PL8Dfz9i9H18MhK8kX4NHOY8jsxz80Tt4G` · 《九九華嚴》讲座 12 集

| 集 | Video ID |
|---|---|
| 1 | `aNIhhEfXSUE` |
| 2 | `Z5QNzrCi990` |
| 3 | `h5gOAne5G24` |
| 4 | `jVkDHV483iQ` |
| 5 | `HjrdWNvah4w` |
| 6 | `yU7pjzNCc98` |
| 7 | `wmKHsCmaYVc` |
| 8 | `JCOA1fCQsi0` |
| 9 | `Q310uDRGfk0` |
| 10 | `e6_1t2-3TF8` |
| 11 | `47GWFvcytws` |
| 12 | `PNKB2nHp-IE` |

---

## 已知瑕疵（校定时留意）

1. 片头 0-40s 动画帧产生乱码（"每 | BIRA"等）——可整段丢弃
2. 幻灯片多行文字以 ` | ` 拼接——非纯口播字幕
3. 时间码精度 ±1s（1fps 采样）
4. 繁体为主，偶见简繁混排

---

## 迁移/扩展

- **换视频源**：改 `config.json` 的 `workspace` 指向新数据目录；如频道版式不同需调整 `crop_*` 参数
- **换语言**：改 `ocr_lang`（支持 "chinese_cht"/"chinese"/"japan"/"korean" 等）
- **加入新项目**：在 `tools/` 下新建同级目录即可
