# Workflow — 部署 / 仓库治理（Deploy & Repo Governance）

> **何时用**：把构建产物发布到 GitHub Pages、或处理仓库/换行/缓存相关决策时。
> **权威既定事实**在 [`docs/next-phase-plan.md`](../../docs/next-phase-plan.md)〈部署与仓库治理·既定事实（勿再误判）〉——本文件只编排"怎么发"，不复述结论。

## 关键事实（务必先内化，否则易误判）

- **线上 Pages 源 = `main` 根目录**：根 `index.html`（105 B meta-refresh）→ `web/demo/index.html`；`/huayan_collection/` 即根部署。**`gh-pages` 分支不参与线上服务**（历史遗留，勿再往它推）。
- **海云讲法正文**读取路径 `../../../docs/huayanhai/<cat>/<title>.txt` → 解析到 `main/docs/huayanhai/…`，故**正文 txt 必须随 main 提交**（`.gitignore` 仅忽略其 `**/*.html` 原件）。
- **换行**：工作区 CRLF＝提交对象 LF（Git 自动归一）。比对线上字节以 `git cat-file -s <blob>`（对象大小）为准，**勿用本地磁盘文件大小**（差值即 LF↔CRLF 计数）。
- **CDN 缓存**约 1–2 分钟，push 后需等待刷新再核验。

## 发布步骤

1. **构建 + 本地验证**：`make demo`（= `demo-build` + `demo-verify`）；数据有变先 `make verify-all`。
2. **提交产物**：`make demo-deploy` 已修正为暂存整个 `web/demo/`（tabs/articles/css/js/index）。
   - ⚠️ `demo-deploy` **不含 `docs/huayanhai/` 正文**——若本轮改过讲法 txt，须**另行提交**：`git add docs/huayanhai/ && git commit`。
   - 常规开发提交用 `git add -A`（含 data/scripts/docs），不要只加 index.html。
3. **推送**：`git push origin main`。
4. **线上核验**（等 ~2min CDN）：headless Chrome `--dump-dom` 打线上 URL，确认关键锚点存在（如 `jiaoxing.html` 含 `id="hl-topics"`）、正文抽样 200（基线与命令见 next-phase-plan 同节）。

## 常见坑

- **误推 gh-pages / 误把构建产物当源**：源永远是 `data/**`+`docs/**`+`src/**`，产物随源走；改数据不改 HTML（见 [`data-pipeline.md`](data-pipeline.md) / [`web-ui.md`](web-ui.md)）。
- **只提交了 index、漏了 tabs/articles** → 线上半更新。用第 2 步的 `git add web/demo/` 与 `git add -A` 规避。
- **字节对不上以为丢了东西** → 先 `git cat-file -s` 按对象比，排除 CRLF/LF 假差异。

## 门禁

发布属重型动作，**须用户明确同意再 `git push`**；发后必做线上 `--dump-dom` 核验并登记 `docs/next-phase-plan.md` + `make evolve`。
