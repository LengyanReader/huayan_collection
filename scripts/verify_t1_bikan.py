# -*- coding: utf-8 -*-
"""T1 比勘证据库门禁（L.109 立）——在 t1_quote.py 逐字回源之上加「台账对账」

t1_quote.py --check 只管「引文是否逐字」，本脚本管**其余六道**：
  A meta.counts 与实际条数、分节计数对账
  B id 唯一且连号（C01…C27）
  C 每条必有 code/src_line/key/sec，sec ∈ 5.1–5.5
  D 否定性记录必有 id/key/probe/result/判读；且 **N 条不得少于 4**
    （比勘须双向：只记正面则易生「凡所立论皆有祖典支持」之错觉）
  E conclusions 必覆盖 5.1–5.5 **五节无缺**，且每节必依（依: 非空）
  F 所引 C/N 号必实际存在（防悬空引用，如依: [C99]）

用法：python scripts/verify_t1_bikan.py
"""
import io
import os
import re
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

LIB = "data/research/t1_bikan_evidence.yaml"
SECS = ["5.1", "5.2", "5.3", "5.4", "5.5"]


def die(msg, fails):
    fails.append(msg)
    print("  FAIL  " + msg)


def main():
    if not os.path.exists(LIB):
        print("【缺库】%s" % LIB)
        return 1
    txt = io.open(LIB, encoding="utf-8").read()
    fails = []

    # 段切分
    i_neg = txt.find("negative_findings:")
    i_con = txt.find("conclusions:")
    if i_neg < 0 or i_con < 0:
        print("【缺段】negative_findings / conclusions 未见")
        return 1
    head, neg, con = txt[:i_neg], txt[i_neg:i_con], txt[i_con:]

    qblocks = re.split(r"\n  - id: ", head)[1:]
    nblocks = re.split(r"\n  - id: ", neg)[1:]
    cblocks = re.split(r"\n  - id: ", con.split("\nconclusions:", 1)[-1])
    cblocks = [b for b in cblocks if b.startswith("C") or " sec:" in b]

    ids = [b.split("\n", 1)[0].strip() for b in qblocks]
    nids = [b.split("\n", 1)[0].strip() for b in nblocks]

    print("A 台账对账")
    m = re.search(r"^    total: (\d+)$", txt, re.M)
    if not m or int(m.group(1)) != len(qblocks):
        die("meta.counts.total 与实际条数不符（记 %s／实 %d）"
            % (m.group(1) if m else "无", len(qblocks)), fails)
    bysec = re.search(r"^    by_sec:\n((?:      \"?[\d.]+\"?: \d+\n)+)", txt, re.M)
    if not bysec:
        die("meta.counts.by_sec 缺失", fails)
    else:
        declared = dict(
            (k.strip().strip('"'), int(v))
            for k, v in re.findall(r"\"?([\d.]+)\"?: (\d+)", bysec.group(1)))
        actual = {}
        for b in qblocks:
            s = re.search(r'^    sec: "([\d.]+)"$', b, re.M)
            if s:
                actual[s.group(1)] = actual.get(s.group(1), 0) + 1
        if declared != actual:
            die("by_sec 与实际不符：记 %s／实 %s" % (declared, actual), fails)
        else:
            print("  OK    by_sec %s（合计 %d）"
                  % (actual, sum(actual.values())))

    print("B id 连号")
    exp = ["C%02d" % (i + 1) for i in range(len(qblocks))]
    if ids != exp:
        die("id 非唯一连号：%s" % ids, fails)
    else:
        print("  OK    C01…C%02d 连续无缺无重" % len(qblocks))

    print("C 字段完备")
    for b in qblocks:
        bid = b.split("\n", 1)[0].strip()
        for f in ("code", "src_line", "key", "sec", "quote"):
            if not re.search(r"^    %s: .+$" % f, b, re.M):
                die("%s 缺字段 %s" % (bid, f), fails)
        s = re.search(r'^    sec: "([\d.]+)"$', b, re.M)
        if s and s.group(1) not in SECS:
            die("%s sec 越界：%s" % (bid, s.group(1)), fails)

    print("D 否定性记录（比勘须双向）")
    if len(nids) < 4:
        die("否定性记录仅 %d 条，不足 4——比勘须双向记录" % len(nids), fails)
    for b in nblocks:
        bid = b.split("\n", 1)[0].strip()
        for f in ("key", "probe", "result", "判读"):
            if not re.search(r"^    %s: .+$" % f, b, re.M):
                die("%s 缺字段 %s" % (bid, f), fails)

    print("E 结论覆盖五节")
    seen = {}
    for b in re.split(r"\n  - sec: ", con):
        if not b.strip() or not b.startswith('"'):
            continue
        s = b[:b.index('"', 1)].strip('"')
        seen[s] = True
        if not re.search(r"^    依: \[.+\]$", b, re.M):
            die("sec %s 无「依」字段（结论不得凭空）" % s, fails)
    for s in SECS:
        if s not in seen:
            die("conclusions 缺 sec %s" % s, fails)

    print("F 引用不悬空")
    # 〔L.113·防重犯〕否定记录之 ID 前缀已由 N# 改为 T1N#（以与 T0 库之
    # N# 相区别，见「命名空间」段）。**若此处仍用 `ref.startswith("N")`，
    # 则 T1N# 一律不以其首字母开头 → 此断言整条成为死码**，
    # 「结论引用悬空」之变异将**不被捕获而反向验证假绿**（本轮实测果然如此：
    # 改名后 `_verify_t1_reverse.py` 由 8/8 退为 6/8 而无人察觉）。
    # 故此处**不用前缀判断，改用正则**，新旧两式皆纳：
    #   ^(?:T1)?N\d+$  —— 旧号 N# 与新号 T1N# 皆可，且**不误纳** C 引文。
    NEGID = re.compile(r"^(?:T1)?N\d+$")
    for b in re.split(r"\n  - sec: ", con):
        m = re.search(r"^    依: \[(.+)\]$", b, re.M)
        if not m:
            continue
        for ref in [x.strip() for x in m.group(1).split(",")]:
            if ref.startswith("C") and ref not in ids:
                die("结论引用不存在的引文 %s" % ref, fails)
            if NEGID.match(ref) and ref not in nids:
                die("结论引用不存在的否定记录 %s" % ref, fails)

    print("\n引文 %d／否定记录 %d／结论 %d 节"
          % (len(qblocks), len(nids), len(seen)))
    if fails:
        print("FAIL（%d 项）" % len(fails))
        return 1
    print("ALL CHECKS PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())