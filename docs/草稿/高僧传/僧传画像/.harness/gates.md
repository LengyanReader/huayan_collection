# Gates · 僧传画像

## Hard gates (non-negotiable · strict per grounding=required)

| gate | description | verify |
|---|---|---|
| **回源门** | Every load-bearing claim (科名, 卷次, 人物 data) has `source:` filled (CBETA / print ref + access date), OR is marked `〔待核〕` | `check.py --source` mode (future) |
| **占位符门** | No unrendered template variables or `TODO_unresolved` markers remain in emitted files | `check.py` (now) |
| **结构完备门** | PLAN.md sections (Goal / DoD / First move) all present | `check.py` (now) |
| **构建一致门** (v4) | 目录即 demo 根：分册（`portraits/*.html`）为真相源，`monolith.html` 必须是其 `merge` 产物——文字级一致、凡例单一、每页恰一人物面板 | `python build.py check` |
| **链接落盘门** (v4) | 一切相对 href/src 必须解到盘上存在之文件（静态站点根无兼容层） | `python .harness/_linkcheck.py` |
| **标签配平门** (v4) | index / monolith / 各分册逐页 section·div·table·tr·td·svg 等开闭配平 | `python .harness/_tagcheck.py` |
| **外壳幂等门** (v4) | 分册外壳（页头·导航·页脚）必须等于当前模板渲染结果；`sync-shell` 重跑应零写入（面板正文逐字节保留） | `python build.py check` 第 4 项 |
| **宁缺不伪** | A missing value is preferred over an unverified one; do NOT fill gaps from memory | human review + agent discipline |
| **探源四问门** (v5) | 每条承重断言除出处外尚须能回答：①是否存在 ②在哪里（藏地·馆·**架号**）③是否可用 ④如何取用。**「不可用」与「不存在」不得混写**；只知有藏而无架号者不得标甲A | 《tasks/语料通道与文献缺口台账》§六 Q1–Q14 + 逐人谱 §七 |
| **分级不得越级** (v5) | 缺口按 L0（已在库可逐字）/L1（通道明确待入库）/L2（须他库·影印实物）/L3（**未出版或未录入**）登记；未刊未录入者页上固定标 `〔L3·未刊/未录入〕`，**禁止用今人转述伪充一手** | 同上 §三；人工复核 |
| **受限信息不得先行入库** (v5.1) | 需权限·申请·付费·馆内·非公开之材料（台账 §九 O1–O4）**不得先行入库或上页**，一律先登记为待办（§九 T1–T6 / §十 T7–T9）；**申请、发函、接触寺方与未公开考古材料须用户逐次同意**（接 irreversible-OK） | 台账 §九；人工复核 |
| **传闻门** (v5.1) | 无公开路径而有人在说者（寺内口传·学界未刊·内部资料·私藏·赝品伪史·亡者之手，台账 §十 A–F）只记**「谁在说·何时何地说」**，**不得当作事实写进页面**；肉身·舍利·圣迹·伪图类**不判真伪**，双栏并存 | 台账 §十 10.1/10.2 |
| **irreversible-OK** | Push, delete, publish → require explicit user confirmation before execution | agent protocol |

## Soft gates (preferences · adjustable per iteration)

| gate | note |
|---|---|
| demo 版面美学 | 设计良好, 但 MVP 阶段重结构不重像素 |
| **单文件分享件定位** (v4) | monolith.html 只作外发/离线携带件，内容等同分册；**回收触发条件**：人物 > 12 或单文件 > 400 KB（阈值写入 `build.py`）→ 删除根上常驻件，改按需 `python build.py merge dist/monolith.html`；merge 超阈会自动提醒 |
| 维度穷举充分性 | 尽量覆盖僧传体裁, 但"宁欠勿凑"——维度多到空转不如精简 |
| 取样人数 | "各大宗派一位", 可扩展或精简 |
| **取数时间窗** (v5) | CBETA Online API 约 2026-12-01 起需 API Key；待取文本应在此之前完成（GitHub `cbeta-org/xml-p5` blob 端点不受此限，但单书 >1 MB 需分卷源） |
| **版本戳一致** (v4.1) | `build.py` 的 `FOOT` 版本与 `index.html` 页脚版本应同一；改后跑 `sync-shell`+`merge`（当前均为 v0.4） |
| **开放度分档登记** (v5.1) | 每条通道记 O0–O4 档（台账 §9.1）；页面上依档写「可直引 / 已注册可阅览 / 待机构通道 / 待预算 / 待授权」。**档别本身就是信息，不得笼统写「查不到」**；「不可用」与「不存在」仍分开 |
