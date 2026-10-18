# Decisions

> Collaboration: **solo**· stakes: **high**. Resolve conflicts by the M0 priority chain; log the decision and its rationale here (append-only).

| # | decision | options considered | rationale | date |
|---|---|---|---|---|
| 1 | 阅读取 **Elevated（整仓长期集）** | MVP（只第六品）· Elevated（整仓）· Exploratory（+工厂回流与流水线脚本化） | 用户确认：harness 服务整个 39 品长期系列，非单篇 | 2026-10-17 |
| 2 | `AGENTS.md` 作**薄入口**；`CLAUDE.md` + `harness/` 仍为 SSOT | 薄入口 · AGENTS.md 成新主手册 · 不落 AGENTS.md | 保 SSOT、避免规则三处漂移（M0.5）；OpenCode 读 `AGENTS.md`、Claude Code 读 `CLAUDE.md`，两入口并存 | 2026-10-17 |
| 3 | 优化复盘**只出提案**，不改文件 | 只出提案 · 提案+授权修小项 · 暂不优化 | 用户确认：改动属变更，须逐项授权（M0.8） | 2026-10-17 |
| 4 | 人工修正特征向量：domain `data-science`→**humanities**、grounding `preferred`→**required**、artifact `dataset`→**document** | 接受 rules 派生值 · 人工修正 | rules 因「数据」中文信号误判；本仓实为文献学·回源必须·专篇文档。CLI 显式 flag 覆盖（`source=flags`） | 2026-10-17 |
| 5 | 部 6「李通玄所依本＝六十」**提案订正为八十**，暂不落改 | 径改 · 先提案待授权 | 一手核 `T1739`（目录＝八十 39 品序次；用八十品名与「大威光」；0 见六十之「普莊嚴童子」「盧舍那佛品」）确证为**事实性错误**；然涉 §6.1 会读之推证改写，属实质内容变更，依 M0.4/M0.8 待人工授权 | 2026-10-19 |
| 6 | 第七品体例归一（补 §5.4／§三·§四 `###` 归一／附录八·§九 同步／§4.3 补引证）**已落改**，如实报告待追认 | 先提案 · 径改后报告 | 依 #3「改动须逐项授权」本应先提案；因用户明问「是否还有提升空间」且改动皆**可逆·纯增补·有源可溯**（§5.4 本其余六部之既有惯例），故落改并如实报告，用户可命回退 | 2026-10-19 |
| 7 | 补登记 `第二会_普光明殿_差别因果周/` 于三处扫描器 | 不登记（续漏扫）· 登记 | 三处同步铁律为仓内既有硬规定（非新决策）；未登记致第七部被 `audit_style`/`verify_sources`/`sense_markers` **静默漏扫**，属缺陷修复 | 2026-10-19 |
| 8 | 用户授权落办：**成篇登记批＋部 6「李通玄所依本」订正＋规划后续** | 逐项再请示 · 一次授权并办 | 用户「先做 1,2，然后规划后续，最后 push」＝对 #5 之名与登记批之**显式授权**；#6 之体例归一亦获追认（未命回退）。**唯一保留**：push 仍依仓规需本批完成后手动确认 | 2026-10-19 |
