# -*- coding: utf-8 -*-
"""verify_imagery_gen.py — 图像著录一致性校验（参数化·三不变量）"""
import io, os, re, sys, argparse
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--doc", required=True, help="文章 md 相对仓根路径")
    ap.add_argument("--reg", required=True, help="登记册 yaml 相对仓根路径")
    a = ap.parse_args()
    doc = io.open(os.path.join(ROOT, a.doc), encoding="utf-8").read()
    reg = io.open(os.path.join(ROOT, a.reg), encoding="utf-8").read()

    errs = []
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

    figs = re.findall(r'<img class="doc-img" src="([^"]+)"[^>]*alt="([^"]*)"[^>]*>\s*<figcaption[^>]*>\s*图 ([\d\-]+)', doc)
    fig_nos = set()
    for src, alt, no in figs:
        fig_nos.add(no)
        if no not in items:
            errs.append("文中图 %s 未登记" % no)
        else:
            if src.split("?")[0] != items[no]["thumb"].split("?")[0]:
                errs.append("图 %s src 与登记不符" % no)
            if not items[no]["boundary"]:
                errs.append("图 %s 缺边界" % no)
            if not items[no]["category"]:
                errs.append("图 %s 缺分类" % no)
            after = doc.split("图 " + no)[1][:600] if ("图 " + no) in doc else ""
            if "边界" not in after:
                errs.append("图 %s 图注无边界声明" % no)
    for no in set(items.keys()) - fig_nos:
        errs.append("登记图 %s 未在文中出现" % no)
    for no, it in items.items():
        if it["category"].startswith("A") and "待核" not in it["category"]:
            errs.append("A 类图 %s 缺 evidence" % no)

    print("图 %d 张·登记 %d 项" % (len(fig_nos), len(items)))
    if errs:
        for e in errs:
            print("  ✗", e)
        sys.exit(1)
    print("✅ ALL CHECKS PASSED —— 图像著录门禁全绿")

if __name__ == "__main__":
    main()
