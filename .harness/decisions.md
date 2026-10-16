# Decisions

> Collaboration: **solo**· stakes: **high**. Resolve conflicts by the M0 priority chain; log the decision and its rationale here (append-only).

| # | decision | options considered | rationale | date |
|---|---|---|---|---|
| 1 | 阅读取 **Elevated（整仓长期集）** | MVP（只第六品）· Elevated（整仓）· Exploratory（+工厂回流与流水线脚本化） | 用户确认：harness 服务整个 39 品长期系列，非单篇 | 2026-10-17 |
| 2 | `AGENTS.md` 作**薄入口**；`CLAUDE.md` + `harness/` 仍为 SSOT | 薄入口 · AGENTS.md 成新主手册 · 不落 AGENTS.md | 保 SSOT、避免规则三处漂移（M0.5）；OpenCode 读 `AGENTS.md`、Claude Code 读 `CLAUDE.md`，两入口并存 | 2026-10-17 |
| 3 | 优化复盘**只出提案**，不改文件 | 只出提案 · 提案+授权修小项 · 暂不优化 | 用户确认：改动属变更，须逐项授权（M0.8） | 2026-10-17 |
| 4 | 人工修正特征向量：domain `data-science`→**humanities**、grounding `preferred`→**required**、artifact `dataset`→**document** | 接受 rules 派生值 · 人工修正 | rules 因「数据」中文信号误判；本仓实为文献学·回源必须·专篇文档。CLI 显式 flag 覆盖（`source=flags`） | 2026-10-17 |
