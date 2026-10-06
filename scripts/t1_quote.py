# -*- coding: utf-8 -*-
"""T1 比勘引文抽取（L.109 立）——引文**一律程序抽取**，杜绝手录失真

比勘之第一义是「引文可信」。故本脚本不让人手抄任何 T1 句子：
给定 (底本, 行号, 起字, 止字) 即输出该行之对应子串，写入
`t1_bikan_evidence.yaml` 的 quote 字段。抽错则门禁报错。

用法：
  python scripts/t1_quote.py T1735 7206 1 20
  python scripts/t1_quote.py --check data/research/t1_bikan_evidence.yaml
"""
import argparse
import glob
import io
import os
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

ROOT = "data/references/cbeta_txt"

# 康熙／兼容部首 → 通用。NFKC 已覆盖 U+2F00–U+2FDF（康熙部首），
# 但**不覆盖** U+2E80–U+2EF3（部首补充），故须 RAD 双层（L.107 之要害）。
# 下表之 ⻄／⺠／⺒ 皆属部首补充区，NFKC 无效，非加此表则回源必误报。
RAD = {"⻄": "西", "⺠": "民", "⺒": "貝", "⻅": "見", "⻢": "馬",
       "⻤": "鬼", "⻩": "黃", "⻬": "齊", "⻮": "齒", "⻰": "龍"}


def normalize(s):
    import unicodedata
    s = unicodedata.normalize("NFKC", s)
    for k, v in RAD.items():
        s = s.replace(k, v)
    return s


def load(code):
    hits = glob.glob(os.path.join(ROOT, code + "_*.txt"))
    if not hits:
        raise SystemExit("【缺底本】%s" % code)
    return io.open(hits[0], encoding="utf-8", errors="replace").read().splitlines()


def cut(code, line, a, b=None):
    """取第 line 行自第 a 字至第 b 字（含端点，1-based；b=None 取至行末）。

    〔L109·体例〕**先归一后取字**：底本用康熙／兼容部首字（⾏⾨⽞…），
    若按原字位取则正文将带兼容部首字，故此处以 NFKC＋RAD 归一之行为准。
    """
    lines = load(code)
    if not (1 <= line <= len(lines)):
        raise SystemExit("【行号越界】%s 仅 %d 行" % (code, len(lines)))
    s = normalize(lines[line - 1])
    b = len(s) if b is None else b
    if not (1 <= a <= b <= len(s)):
        raise SystemExit("【字位越界】L%d 归一后长 %d，取 %d–%d"
                         % (line, len(s), a, b))
    return s[a - 1:b]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("code", nargs="?")
    ap.add_argument("line", nargs="?", type=int)
    ap.add_argument("a", nargs="?", type=int)
    ap.add_argument("b", nargs="?", type=int)
    ap.add_argument("--check", default="", help="校验 YAML 之 quote 逐字回源")
    args = ap.parse_args()

    if args.check:
        return check(args.check)
    if not args.code:
        ap.print_help()
        return 2
    print(cut(args.code, args.line, args.a, args.b))
    return 0


def check(path):
    """校验 YAML：引文条目之 quote 必为所记 src_line 该行之逐字子串。

    〔L109·设计〕**只校引文条目**（有 code+src_line+quote 三者齐备者）。
    否定性记录（N 条）与结论（conclusions）本无 quote，**不得**因此报缺字段——
    早版因「凡 - id: 皆须三字段」而误报，此为门禁自身之缺陷，不可迁就。
    """
    import re
    txt = io.open(path, encoding="utf-8").read()
    blocks = re.split(r"\n  - id: ", txt)[1:]
    bad = 0
    n = 0
    skipped = 0
    for blk in blocks:
        bid = blk.split("\n", 1)[0].strip()
        mq = re.search(r'^    quote: "?(.*?)"?$', blk, re.M)
        mc = re.search(r"^    code: (\S+)$", blk, re.M)
        ml = re.search(r"^    src_line: (\d+)$", blk, re.M)
        if not (mq and mc and ml):
            skipped += 1
            continue
        q = mq.group(1)
        code, ln = mc.group(1), int(ml.group(1))
        n += 1
        try:
            line = normalize(load(code)[ln - 1])
        except SystemExit as e:
            print("【%s】%s" % (bid, e))
            bad += 1
            continue
        if q in line:
            print("  OK  %-4s %s:%d  (%d 字)" % (bid, code, ln, len(q)))
        else:
            print("【%s 失配】%s:%d 未逐字命中" % (bid, code, ln))
            bad += 1
    print("\n引文 %d 条校讫；非引文条目（否定性记录／结论等）%d 条略过"
          % (n, skipped))
    print("失配 %d 条" % bad)
    if bad or not n:
        print("FAIL")
        return 1
    print("ALL CHECKS PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
