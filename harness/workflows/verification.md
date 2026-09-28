# Workflow — 验证 / 测试（Verification Gates）

> **何时用**：任何触碰数据/构建产物/前端的改动，收尾前"是否算完成"的裁决流程。
> 本文件是"怎么跑、怎么解读"的配方；脚本清单见 [`../tools.md`](../tools.md) §一，原则见 [`../principles.md`](../principles.md) §4。

## 三道闸（数据/产物/来源）

| 闸 | 命令 | 通过标志 | 何时必跑 |
|---|---|---|---|
| 数据一致性 | `python scripts/test_pipeline.py` | `ALL TESTS PASSED` | 涉 `data/**`、SQLite、导入导出（基线 95人/98边/30地）|
| 构建产物 | `python scripts/verify_demo.py` | `ALL CHECKS PASSED` | 每次 `build.py` 之后（含 `node --check` 内联 JS 语法）|
| 来源可靠性 | `python scripts/verify_sources.py --json` | 评分不降、T0=0 | 涉史实/名号/年代/出处/引文 |

**一条命令跑齐**：`make verify-all`（= `test-pipeline` + `demo-verify` + `verify-sources`）。

## 基建闸（2026-09-27 R1 事故后新增·阻塞级）

| 闸 | 命令 | 验什么 |
|---|---|---|
| 静态质量 | `make lint` | ruff 两层：src/ 严格·scripts/ 仅 F,E9 错级 |
| 工具自证 | `python -m pytest -q`（现 23 例） | 备份回环/live 护栏墓碑/搜索两层/drift 三态/CLI——**防“验收工具自己烂掉”** |
| 备份可用 | `python scripts/db_backup.py --verify` | 快照↔live 逐表 sha256 指纹 + FTS 冒烟（改过 DB 必跑·§F10） |

## 报告闸（非阻塞·只报警不删改）

- `audit_consistency.py`：〔待核〕台账 + CBETA 号格式/配对候选（首跑已抓到候选冲突·处置=内容轨）
- `check_drift.py`：docs 镜像 ↔ web/demo 全站点面 11 对（现 10 漂移·处置待维护者定）
- 两者已入 `make verify-data` 与 CI；退码非 0 也不拦闸——发现≠裁决（§I10 同款姿态）。

## CI（2026-09-27 首推）

`.github/workflows/verify.yml` = 上述全序自动化（重建链→快照回环→lint→测试→报告层·drift 只 `::warning`）；push 后首跑绿才算“已验证”，本地跑通≠Actions 环境跑通。

## 第四关：交互/渲染实测（静态 ≠ 交互）🔴

数据闸全绿 ≠ 功能正常。**渲染/交互改动必须以"真人用户"路径实测**（memory〈Interactive State Verification Requirement〉）：

1. **headless Chrome `--dump-dom`（首选，最稳）**：
   `& "C:\Program Files\Google\Chrome\Application\chrome.exe" --headless --disable-gpu --dump-dom "file:///.../web/demo/tabs/<tab>.html"`
   → 量产物（CSS/DOM 节点、`data-count`、`id="..."` 锚点、`.en-line`/`en-block` 计数、**ASCII 标记反证**）。
2. **CDP 交互**（点击/切页/取运行态）——本机常 `10053` 断连、**不稳定**；退化方案：注入脚本 + `--dump-dom` 断言 `body` 属性/类（L.㊾⑭）。
3. **Browser 子代理**：需真实浏览器端到端时派生。

> 铁律：浏览器自动化失败**必须显式报告并给替代方案**，不得以静态字符串命中冒充"功能已验证"；曾出现"引入 JS 语法错误而 verify_demo 仍 PASSED"，故 verify_demo 已内置 node --check 反向自证。

## 缓存陷阱（改了没生效？）

`file://` 下 `page.reload(ignoreCache=True)` **不刷新 src/js**（memory〈Three-layer cached JavaScript〉）。用 query-string 绕缓存或经 HTTP（`make demo-serve` → localhost:8080）。

## 环境注意（Windows/pwsh）

conda `hy_py312`；子进程前设 `$env:PYTHONIOENCODING="utf-8"`；PowerShell `Out-File` 重编码可能让中文计数误显 0 → 用 ASCII 标记或把校验写进 Python。详见 [`../tools.md`](../tools.md) §5。

## 解读与留痕

- 计数与基线**有差异必须解释**（有意增补 or 丢数据），不可默默放行。
- 全绿后：更新 `docs/工程治理/next-phase-plan.md` → `make evolve`（进化引擎顺带跑三道闸并刷新 health/next_actions）。任一闸未绿不得声称完成、不得标 `passes:true`。
