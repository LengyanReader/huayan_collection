# Gates — Definition of Done · 完成门禁

> Gate strictness: **strict**（verifiability=medium, stakes=high）
> Every criterion starts `false`. It may be set `true` only after the required evidence is attached (M0.3).
> 每条标准初始为 `false`；**有观察到的证据**方可置 `true`。构建者≠评判者（新上下文、无写权限）。

## Hard gates · 硬门（机械可判，必须全过）

> 命令以本仓 `Makefile` 与既有 `verify_*` 为准（`CONDA_PYTHON = ~/miniconda3/envs/hy_py312/python.exe`）。涉内容改动时**逐条**跑；纯工程改动按改动面择要。

- [ ] **harness 自检**：`python .harness/check.py .` → `OK`（manifest 所列文件皆在、无未渲染占位符）。
- [ ] **构建**：`make demo-build`（`cd web/demo && python scripts/build.py`）无错。
- [ ] **管线测试**：`make test-pipeline`（`scripts/test_pipeline.py`）→ ALL PASSED。
- [ ] **站点验证**：`make demo-verify`（`scripts/verify_demo.py`）→ ALL CHECKS PASSED。
- [ ] **来源核对**：`make verify-sources`（`scripts/verify_sources.py --fixme`）；T0（无源）计数须为 0。
- [ ] **专书门禁**（按改动面加跑）：`verify_shizhu.py` · `verify_ru_lai.py` · `verify_imagery.py` 等 —— 全绿。
- [ ] **JS 语法**：改动 `web/demo/src/*.js` 时 `node --check <file>`，0 错。
- [ ] **空白/差异洁净**：`git diff --check` 无报错。
- [ ] **引文回源**：经文引文逐字核对 CBETA `T10n0279`（繁体原字形）；不得以记忆或他品经文冒充。**证据**：回源脚本输出（如 `scripts/_audit_jingwen`）/ 逐条 diff。
- [ ] **无假信息**：每条关键论断可溯（文件:行 / 经号卷页 / URL）；无法溯者标 〔待核〕/`unverified`。
- [ ] **SSOT 未破**：规则未在 `CLAUDE.md`／`harness/`／`AGENTS.md` 三处漂移；登记同步（`standalone_articles.yaml` / 系列总纲 / `next-phase-plan.md`）。

> 一键：`make verify-all`（= `test-pipeline` + `demo-verify` + `verify-sources`，见 `Makefile` L96）。

## Soft gates · 软门（需人类判断，human-gated）

- [ ] 交付物符合目标（一品一专篇；三层疏解／体例齐全）。
- [ ] 学术判断：疏解得当、异说并存、反例／负面证据已列。
- [ ] 文风与体例：引文繁体照底本、疏解用简体；标题后缀「之拼读」等体例一致。
- [ ] 复核者（人）认可。

## Evidence rule · 证据规则

- 证据是一等产物（测试输出、文件、日志行、截图）。**无证据 → 不得通过**。
- 独立评判者（新上下文、无写权限）确认硬门；无法机械判者，标 `uncertain` 或弃权，**不强行二选一**。
- 先定义完成、后动手；门禁未全绿**不得**声称完成、不得 push／发布（M0.3/M0.8）。
