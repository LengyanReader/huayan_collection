# -*- coding: utf-8 -*-
"""verify_imagery_p39.py — P39 文化资产参证·图像著录一致性校验（三不变量）"""
import io, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8")
DOC = os.path.join(ROOT, "docs", "经学文献", "华严经细读", "第九会_逝多林_证入法界", "华严经细读_第三十九部_入法界品.md")
REG = os.path.join(ROOT, "data", "imagery", "rufajie_imagery.yaml")

def main():
    errs = []
    doc = io.open(DOC, encoding="utf-8").read()
    reg = io.open(REG, encoding="utf-8").read()

    # 登记册条目
    items = {}
    for m in re.finditer(r"- img_no: (\S+)\n((?:  .*\n?)+)", reg):
        no = m.group(1)
        body = m.group(2)
        tm = re.search(r"thumb_url: (\S+)", body)
        bm = re.search(r"boundary: (.+)", body)
        cm = re.search(r"category: (.+)", body)
        items[no] = {"thumb": tm.group(1) if tm else "",
                     "boundary": bm.group(1).strip() if bm else "",
                     "category": cm.group(1).strip() if cm else ""}

    # 文中图
    figs = re.findall(r'<img class="doc-img" src="([^"]+)"[^>]*alt="([^"]*)"[^>]*>\s*<figcaption[^>]*>\s*图 ([\d\-]+)', doc)
    fig_nos = set()
    for src, alt, no in figs:
        fig_nos.add(no)
        if no not in items:
            errs.append("文中图 %s 未登记" % no)
        else:
            if src != items[no]["thumb"]:
                # 允许 thumb 参数差异
                if src.split("?")[0] != items[no]["thumb"].split("?")[0]:
                    errs.append("图 %s src 与登记不符" % no)
            if not items[no]["boundary"]:
                errs.append("图 %s 缺边界" % no)
            if not items[no]["category"]:
                errs.append("图 %s 缺分类" % no)
            if "边界" not in doc.split("图 " + no)[1][:600]:
                errs.append("图 %s 图注无边界声明" % no)
    # 在册必在文
    reg_nos = set(items.keys())
    for no in reg_nos - fig_nos:
        errs.append("登记图 %s 未在文中出现" % no)
    # 分类不拔高：A 类须 evidence
    for no, it in items.items():
        if it["category"].startswith("A") and "待核" not in it["category"] and "证据" not in it["category"]:
            errs.append("A 类图 %s 缺 evidence" % no)

    print("图 %d 张·登记 %d 项" % (len(fig_nos), len(reg_nos)))
    if errs:
        for e in errs:
            print("  ✗", e)
        sys.exit(1)
    print("✅ ALL CHECKS PASSED —— 《入法界品》图像著录门禁全绿")

if __name__ == "__main__":
    main()
