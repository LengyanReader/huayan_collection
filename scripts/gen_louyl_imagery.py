# -*- coding: utf-8 -*-
"""gen_louyl_imagery.py — 楼宇烈纪念综述图像块生成器（登记源生成·幂等）

SSOT = data/imagery/lou_yulie_imagery.yaml。
文档（docs/人物与学人/不苟为唯贵当_楼宇烈先生纪念综述.md）内：
  - 图位标记 `<!--IMG:<img_no>--> … <!--/IMG:<img_no>-->`（生成器就地重写其间内容）
  - 著录总表 `<!--IMGTBL--> … <!--/IMGTBL-->`（生成器整段重写）
凡正文图块、图注、图源署名、著录总表皆由此生成，杜绝手工转录 URL 与著录笔误。
不变量由 scripts/verify_imagery_gen.py --doc … --reg … 校验（1:1 对账·边界·分类）。

用法： python -X utf8 scripts/gen_louyl_imagery.py
"""
import io, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8")

DOC = os.path.join(ROOT, "docs", "人物与学人", "不苟为唯贵当_楼宇烈先生纪念综述.md")
REG = os.path.join(ROOT, "data", "imagery", "lou_yulie_imagery.yaml")

import yaml


def esc(s):
    return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def fig_block(it):
    no = it["img_no"]
    alt = esc(it.get("alt") or it["title_zh"])
    mw = f' style="max-width:{it["max_width"]}px"' if it.get("max_width") else ""
    en = (f'<div class="en-line" style="font-size:.95em">EN — {it["title_en"]} — {it["desc_en"]} '
          f'Boundary: {it["boundary_en"]}</div>') if it.get("title_en") else ""
    return f'''<figure class="doc-fig" style="margin:18px auto;max-width:820px;text-align:center">
<img class="doc-img" src="{it["thumb_url"]}" alt="{alt}" loading="lazy"{mw}>
<figcaption style="font-size:.78em;color:var(--text2);line-height:1.85;max-width:760px;margin:6px auto 0">
图 {no}　【{it["category"]}】{it["title_zh"]}——{it["desc_zh"]}{it.get("era_zh") and "·" + str(it["era_zh"]) or ""}{it.get("location_zh") and "·" + str(it["location_zh"]) or ""}。**边界**：{it["boundary"]}<br>
{en}
图源：Wikimedia Commons（{it["license_zh"]}，作者：{it.get("author_zh") or "〔待核〕"}）；详目与著录见文末〔▲图像登记〕「{it["id"]}」。
</figcaption>
</figure>'''


def table_block(items):
    rows = "\n".join(
        f'| {it["img_no"]} | 【{it["category"]}】{it["title_zh"]} | {it.get("era_zh","")} | {it.get("location_zh","")} | {it["license_zh"]}（作者：{it.get("author_zh") or "〔待核〕"}） | [{it["id"]}]({it["source_page"]}) |'
        for it in items)
    return (f'| 图号 | 名称 | 年代 | 现址／场合 | 授权（作者） | 登记号 |\n'
            f'| --- | --- | --- | --- | --- | --- |\n{rows}')


def main():
    Y = yaml.safe_load(io.open(REG, encoding="utf-8"))
    items = Y["imagery"]
    doc = io.open(DOC, encoding="utf-8").read()
    orig = doc

    for it in items:
        no = it["img_no"]
        pat = re.compile(r"(<!--IMG:" + re.escape(no) + r"-->)(.*?)(<!--/IMG:" + re.escape(no) + r"-->)", re.S)
        if not pat.search(doc):
            print(f"  ✗ 文档缺图位 <!--IMG:{no}-->")
            sys.exit(1)
        doc = pat.sub(lambda m: m.group(1) + "\n" + fig_block(it) + "\n" + m.group(3), doc)

    doc = re.sub(r"(<!--IMGTBL-->)(.*?)(<!--/IMGTBL-->)",
                 lambda m: m.group(1) + "\n" + table_block(items) + "\n" + m.group(3), doc, flags=re.S)

    if doc == orig:
        print("文档无变化（幂等）")
    else:
        io.open(DOC, "w", encoding="utf-8", newline="\n").write(doc)
        print(f"已生成/更新 {len(items)} 个图块＋著录总表")


if __name__ == "__main__":
    main()
