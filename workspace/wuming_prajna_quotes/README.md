# 无明与般若 · 回源工作目录（L.505）

- `verify_quotes.py` —— 引文回源核验器（CBETA TEI/P5；剥标签＋标点无关匹配＋原文回映）。底本路径已改指 `data/references/cbeta/`（canonical 库）。
- `verify_out.txt` —— 最近一次全量核验输出（TOTAL 98·OK 98·MISS 0，对 canonical 件复跑；历史批次记录见 git 历史）。
- `enrich.py` / `enrich2.py` / `integrate3.py` —— 《docs/宗派研究/无明与般若.md》三批增补的锚点式补丁脚本（逐锚断言唯一，可重放审计）。
- XML 底本已按仓库惯例移入 `data/references/cbeta/`（新增 14 部，登记见该目录 `INGEST_log.md` §L.505 与 `README.md` 表；T48n2008 与库内既有件 sha256 相同 `f9d173749307`，径删副本）。
- `part2-4.md` 为拼装中间件，成稿后删除——文章本体即 SSOT，git 历史留痕。
