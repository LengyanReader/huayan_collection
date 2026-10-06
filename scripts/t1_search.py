# -*- coding: utf-8 -*-
"""T1 祖典检索工具（L.109 立）——可复现之「比勘」之基

用途：海云修行体系研究 §5.1–5.5 需与 T1 祖典逐要素比勘。比勘之第一步
      是**可复现地**定位祖典中之相关段落——不靠一次性 grep，不靠记忆。

底本（本地 txt，均在册）：
  T1733 法藏《华严一乘教义分齐章》（探玄记）
  T1735 澄观《大方广佛华严经随疏演义钞》〔本库命名·待订正〕
  T1736 澄观《大方广佛华严经疏》
  T1739 李通玄《新华严经论》
  X0223 李通玄《华严经合论》
  T1732 智俨《华严一乘教义分齐章》（对照用）

〔体例〕CBETA txt 用**康熙／兼容部首字**（⽣⼤⾨⻄⺠⺒…），NFKC 不覆盖此区，
      故比对与检索**必须 NFKC ＋ RAD 双层归一**（L.107 之方法论要害，勿忘）。

用法：
  python scripts/t1_search.py 解脱門                 # 全部底本检索
  python scripts/t1_search.py 解脱門 --book T1735
  python scripts/t1_search.py 下手處 --ctx 60 --max 20
  python scripts/t1_search.py --list
"""
import argparse
import glob
import io
import os
import re
import sys
import unicodedata

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

ROOT = "data/references/cbeta_txt"
BOOKS = ["T1732", "T1733", "T1735", "T1736", "T1739", "X0223"]
BOOK_NAME = {
    "T1732": "法藏《华严一乘教义分齐章》（搜玄记）",
    "T1733": "法藏《华严一乘教义分齐章》（探玄记）",
    "T1735": "澄观《大方广佛华严经疏》",
    "T1736": "澄观《大方广佛华严经随疏演义钞》",
    "T1739": "李通玄《新华严经论》",
    "X0223": "李通玄《华严经合论》",
}
# 编号依 CBETA 正体：T35n1735《疏》、T36n1736《钞》。
# 〔L109 自纠〕本表初版曾把 T1735／T1736 之名对调（误以「疏」为钞），
# 经核《华严经细读》篇首及本项目诸处引用（皆作「澄观《疏》(`T35n1735`)」
# 「澄观《随疏演义钞》(`T36n1736`)」）而正。**本地文件名是对的，错的是本表。**

# 底本之使用限制（据《华严经细读_第一部_世主妙严品.md》L506 所记〔使用限制〕）
BOOK_LIMIT = {
    "T1735": "**本项目所藏系截断本**（止于入法界品中段，未及毗卢遮那品）"
             "——故凡涉后续诸品之澄观说，须另取完整本方可断言",
}

# 康熙／兼容部首 → 通用部首（续 L.107 之 RAD 字典）
RAD = {
    "⽣": "生", "⼤": "大", "⾨": "面", "⻄": "西", "⺠": "民", "⺒": "貝",
    "⾔": "言", "⾐": "衣", "⾬": "雨", "⾯": "面", "⻌": "辶", "⻏": "阝",
    "⾎": "舟", "⾕": "谷", "⾖": "米", "⾔": "言", "⻑": "長", "⾜": "足",
    "⾜": "足", "⻘": "青", "⾺": "見", "⾻": "貝", "⼝": "口", "⾹": "甘",
    "⾺": "見", "⽵": "爪", "⻚": "頁", "⾲": "卤", "⾳": "音", "⾴": "聿",
    "⾴": "聿", "⽥": "田", "⽹": "网", "⽝": "网", "⻄": "西", "⾕": "谷",
    "⾨": "面", "⾬": "雨", "⻌": "辶", "⻃": "風", "⻝": "食", "⻞": "食",
    "⻠": "馬", "⻢": "馬", "⻤": "鬼", "⻩": "黃", "⻬": "齊", "⻮": "齒",
    "⻰": "龍", "⻳": "龜", "⻲": "亀", "⾊": "色", "⻅": "見",
}


def norm(s):
    s = unicodedata.normalize("NFKC", s)
    for k, v in RAD.items():
        s = s.replace(k, v)
    return s


def find_book(code):
    for p in glob.glob(os.path.join(ROOT, code + "_*.txt")):
        return p
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("term", nargs="?", help="检索词（繁简皆可，脚本自动归一）")
    ap.add_argument("--book", default="", help="限单一底本（如 T1735）")
    ap.add_argument("--ctx", type=int, default=50, help="上下文字数（行内）")
    ap.add_argument("--ctxl", type=int, default=0,
                    help="另取上下 N **行**（CBETA txt 行短，行内不足时用此）")
    ap.add_argument("--max", type=int, default=10, help="每本最多显示条数")
    ap.add_argument("--count-only", action="store_true", help="只计数")
    ap.add_argument("--list", action="store_true", help="列出在册底本")
    args = ap.parse_args()

    if args.list:
        for c in BOOKS:
            p = find_book(c)
            if not p:
                print("%-6s  %s  ——【缺】" % (c, BOOK_NAME[c]))
                continue
            n = sum(1 for _ in io.open(p, encoding="utf-8", errors="replace"))
            print("%-6s  %s  (%s, %d 行)" % (c, BOOK_NAME[c],
                                             os.path.basename(p), n))
            if c in BOOK_LIMIT:
                print("        └〔使用限制〕%s" % BOOK_LIMIT[c])
        return 0

    if not args.term:
        ap.print_help()
        return 2

    needle = norm(args.term)
    books = [args.book] if args.book else BOOKS
    grand = 0
    for code in books:
        if code not in BOOK_NAME:
            print("未知底本：%s" % code)
            return 2
        p = find_book(code)
        if not p:
            print("%-6s  【缺底本】" % code)
            continue
        lines = io.open(p, encoding="utf-8", errors="replace").read().splitlines()
        hits = []
        for i, l in enumerate(lines, 1):
            nl = norm(l)
            if needle in nl:
                hits.append(i)
        grand += len(hits)
        if args.count_only:
            print("%-6s  %3d 见" % (code, len(hits)))
            continue
        shown = hits[:args.max]
        print("%s　%s　%d 见（显示 %d）"
              % (code, BOOK_NAME[code], len(hits), len(shown)))
        for i in shown:
            seg = norm(lines[i - 1])
            j = seg.find(needle)
            if args.ctxl:
                lo_l = max(1, i - args.ctxl)
                hi_l = min(len(lines), i + args.ctxl)
                for k in range(lo_l, hi_l + 1):
                    mark = ">>" if k == i else "  "
                    print("   %s L%-6d %s" % (mark, k, norm(lines[k - 1])))
                print("")
                continue
            lo = max(0, j - args.ctx)
            hi = min(len(seg), j + len(needle) + args.ctx)
            print("   L%-6d …%s…" % (i, seg[lo:hi]))
        if len(hits) > len(shown):
            print("   …（余 %d 见，用 --max 增显）" % (len(hits) - len(shown)))
        print("")
    if not args.count_only:
        print("合计 %d 见" % grand)
    return 0


if __name__ == "__main__":
    sys.exit(main())
