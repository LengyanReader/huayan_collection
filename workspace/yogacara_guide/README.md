# 瑜伽师地论导读 · 回源工作目录（L.506）

- `fetch.py` —— 稳健下载器（断点续传＋`</TEI>` 完整性校验）。
- `parse_structure.py` —— 结构实测器：五分卷界、`<head>` 标题、卷号映射。
- `probe_quotes.py` —— 义理锚点探测器（初轮，24 组）。
- `verify_quotes.py` / `verify_out.txt` —— 手写 needle 抽检（75 条子串／2 部；底本指 `data/references/cbeta/`）。**注意：needle 与正文脱钩，只能证「这些子串在底本里」，不能证「正文引文都对」。**
- `verify_inline.py` —— **正文抽取式回源核验**：从 md 抽取 blockquote 引文（严格项）与行内「…」（提示项），按省略号分段、只留汉字比对，输出命中卷次；严格项不命中即退出码 1。2026-11-19 首跑抓出「摄释嗢拕南」脱「節、廣、開七門」。
- `figures.py` —— 8 幅信息图生成器（五分卷界、十七地、摄抉择分、四持、九住心×六力×四作意、八证、五法/三自性/三无性、十三住×十地）。按 md 中「图 N｜」定位、原位替换 `<figure>`；数字全部来自 `T30n1579` 实测解析。改图后需重跑 `python web/demo/scripts/build.py`。
- `review_2026-11-19.md` —— 审读报告（缺陷清单＋施工记录＋门禁结果）。
- `part2-4.md` —— 拼装中间件（成稿后不再更新，正文即 SSOT）。
- 底本：`T30n1579`、`T30n1580` 已入 canonical 库（登记见该目录 `INGEST_log.md` §L.505b）；`T42n1828`（遁伦记）下载后仅作卷次参考、未逐字引用，未入库、已删。

## 常用命令

```bash
python workspace/yogacara_guide/verify_quotes.py    # 手写 needle 抽检
python workspace/yogacara_guide/verify_inline.py    # 正文抽取式回源（推荐）
python workspace/yogacara_guide/figures.py          # 重建 8 幅信息图
python web/demo/scripts/build.py                    # 渲染站点
```
