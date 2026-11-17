# data/references · 一手文本层安置规则（SSOT）

> 本文件说明「什么进 git、什么不进、按什么路径放」。新增语料前先读此页。
> 实测基线（2026-11-17）：已入库 **1,246 档 / 68 MB**；未入库影像 8.3 GB（`tibetan/bdrc/**/*.jpg`，已 ignore）。

## 一、三层分流

| 层 | 入 git？ | 示例 | 判据 |
|---|---|---|---|
| **一手文本底本**（UTF-8 的 XML / TXT / YAML / JSON） | **是** | `cbeta/T10n0279.xml`、`cbeta_x/X04n0223.xml`、`daozang/KR5e0031_*.txt`、`shiji/*`、`jinshi/*`、`rujia/*`、`sanskrit/*`、`tibetan/derge_tengyur/*` | 可逐字回源、纯文本、体积小（单档 ≲3 MB） |
| **影像 / 扫描 / 原始下载件**（jpg / png / pdf / zip / 原始 HTML） | **否**（`.gitignore` 挡） | `tibetan/bdrc/**/*.jpg`（8.3 GB）、`huayan_daodu/**/*_pdf/`、`**/宣化淺釋_html/` | 可再由脚本按需取；入库存哈希即可 |
| **派生物 / 研究产物** | **是** | `data/research/*.json`、`data/alignment/*.json`、`web/demo/articles/*.html` | 可复现（有生成脚本）；体积小 |

## 二、目录约定（按藏／语种分层，一藏一目录）

```
data/references/
  cbeta/         大正藏 XML（T 号）           cbeta_x/   卍续藏 XML（X 号）
  cbeta_txt/     注疏线纯文本提取本           daozang/   道藏（Kanripo KR5*）
  shiji/         史部五书（KR2a/m/f）         jinshi/    金石（KR2n，注意：不在 shiji/ 下）
  rujia/         儒家（KR1h）                 sanskrit/  梵文（GRETIL）
  pali/          巴利（SuttaCentral）         tibetan/   藏文（甘珠尔/丹珠尔；影像不入库）
  huayan_daodu/  华严导读线提取本
```

- **一藏一目录**，不按批次另开目录；新藏先在此表登记再落盘。
- `jinshi/` 与 `shiji/` 并列（金石不归史部五书），生成脚本 `build_s2_sidian.py` 已按此分流。

## 三、入库必带三件

1. **出处**：`url`（或 Kanripo repo + 档名）＋底本说明；
2. **哈希**：`sha256`＋`bytes`，登记在 `data/references/external_manifest.json`
   （体量大、逐档登记不现实者，登记在对应研究 JSON 的 `meta` 里，如 `tanjur_catalog.json`、`s2_sidian.json`）；
3. **校验**：入 manifest 的档由 `scripts/verify_dazang_article.py` §17.8 组逐档验哈希；缺档即 FAIL。

## 四、不入库的东西（`.gitignore` 已挡，别硬塞）

- `data/references/tibetan/**/*.jpg`、`**/*.zip`（L.200 藏文线：只入文本）
- `data/references/huayan_daodu/hgs_baihua_pdf/`、`**/宣化淺釋_html/`（L.479：只入清洗后 UTF-8 提取本）
- `.tmp_*`（临时探针/中间件）、`web/demo/_vis/`（可视化截图）
- `docs/hy_refs/*`（原始语料；`docs/hy_refs/tools/` 例外）

## 五、体积红线与升级路径

- 单档 >5 MB 或单目录 >100 MB 的**文本**：先问「能否只入题录＋哈希、正文脚本按需取」；不能则用 Git LFS（本仓尚未启用）。
- 影像/PDF 一律不入库；确需本地保存者放 `_bdrc_pdfs/`、`docs/hy_refs/` 等已 ignore 目录。
- 当前 `.git` 打包体积 ~279 MB（含 8 个宗教传统文本＋全部研究产物），仍属可控。

## 六、新增语料的检查单

```bash
# 1) 落盘到对应藏目录
# 2) 若为外部下载：跑 fetcher（幂等、自动登记 manifest）
python scripts/fetch_missing_corpora.py --only <ID>
# 3) 或手写登记进对应研究 JSON 的 meta.sources（url+sha256+edition）
# 4) 全文章节门禁
python scripts/verify_dazang_article.py
```
