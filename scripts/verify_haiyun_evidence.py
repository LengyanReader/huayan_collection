# -*- coding: utf-8 -*-
"""海云修行体系实证库·回源校验器

门禁目的：防止 data/research/haiyun_practice_system_evidence.yaml 之内引原话
发生「引用漂移」——即文内所引与底本逐字不符、行号错位、或文件缺失。

五道校验：
  A  结构：分组名与必备字段齐备
  B  存在：src 所指文件俱存在，且在 docs/huayanhai/ 之内（禁逸出 T0 一手栈）
  C  逐字回源：quote 经 NFKC+RAD 双层归一后，须见于所指行 ±window 行
  D  行号：命中所引行须落在 line（或 line 起止区间）之内，防「行号张冠李戴」
  E  存疑诚实：信度字段若含「待核」，须同时带 status 说明；否定性记录须自述检索范围

反向验证（须如期失败，防门禁自身失效）：
  python scripts/verify_haiyun_evidence.py --mutate falsify_quote
  python scripts/verify_haiyun_evidence.py --mutate shift_line
  python scripts/verify_haiyun_evidence.py --mutate drop_section
  python scripts/verify_haiyun_evidence.py --mutate escape_t0
"""
import argparse
import os
import re
import sys
import unicodedata

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

import yaml  # noqa: E402

YAML_PATH = os.environ.get("HAI_EVIDENCE",
                           "data/research/haiyun_practice_system_evidence.yaml")
T0_ROOT = "docs/huayanhai"

# 康熙/兼容部首 → 通用部首（CBETA txt 用字，NFKC 不覆盖此区，故须 RAD 双层）
RAD = {
    "⽣": "生", "⼤": "大", "⾨": "面", "⻄": "西", "⺠": "民",
    "⺒": "貝", "⾔": "言", "⾐": "衣", "⾬": "雨", "⾯": "面",
    "⻌": "辶", "⻏": "阝", "⾎": "舟", "⾐": "衣",
}

REQUIRED = {
    "strong": ["id", "key", "quote", "src", "line", "信度", "status"],
    "medium": ["id", "key", "quote", "src", "line", "判读", "信度", "status"],
    "limit": ["id", "key", "quote", "src", "line", "判读", "信度", "status"],
}

# ── 各分组之最少条数（防止「整组删空」）
MIN_COUNT = {"strong": 8, "medium": 5, "limit": 3}
MIN_NEGATIVE = 3
# 台账等值对账（L109：只设下限时，删一条仍通过，故增 meta.counts 对账）
LEDGER = "counts"

# 信度取值域（防止任意书写）
# 「A（史实待核）」者：引文本身确系法师原话（A），然其中所含历史论断待外证
# 「B（已比勘）」者〔L.114 增〕：原以「B（待比勘）」登记，所待者为 T1 六帙之比勘；
#   既已检得系属（见 S25），若仍书「待比勘」则与实况相违，故增此一值——
#   **值域缺一种状态而强留旧标，即门禁自身之失真**，与「信度取值域」防任意书写之初衷无违。
CONF_ALLOWED = ("A", "B", "A（部分）", "A（史实待核）", "B（待比勘）",
                "B（已比勘）", "待核", "存疑")

# 反向验证：期望的断言标签（须与实际抛出者一致，否则 harness 自身失准）
MUT_EXPECT = {
    "falsify_quote": "C",
    "shift_line": "C",       # 收紧为「单行须精确命中」后，行号偏移亦由 C 抓出
    "drop_section": "A",
    "escape_t0": "B",
    "falsify_conf": "E",
    "drop_item": "Y",
}


def norm(s):
    """NFKC + RAD 双层归一（照 L.107 之方法论要害）。"""
    s = unicodedata.normalize("NFKC", s)
    for k, v in RAD.items():
        s = s.replace(k, v)
    return re.sub(r"[\s，。、；：！？「」『』（）()\-—…·\.]+", "", s)


def norm_radical_only(s):
    return re.sub(r"[\s]+", "", s)


def parse_line(v):
    if isinstance(v, int):
        return v, v
    m = re.match(r"^\s*(\d+)\s*[-–—]\s*(\d+)\s*$", str(v))
    if m:
        return int(m.group(1)), int(m.group(2))
    return int(str(v).strip()), int(str(v).strip())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mutate", default="", help="反向验证：故意破坏数据，验门禁会失败")
    args = ap.parse_args()

    if not os.path.exists(YAML_PATH):
        print("FAIL 实证库不存在：%s" % YAML_PATH)
        return 1
    with open(YAML_PATH, "r", encoding="utf-8") as f:
        doc = yaml.safe_load(f)
    if not isinstance(doc, dict):
        print("FAIL 实证库顶层非映射")
        return 1

    text = yaml.safe_dump(doc, allow_unicode=True)
    if args.mutate == "falsify_quote":
        # 改 strong 首条引文末字：应被 C 逐字回源抓出
        doc["strong"][0]["quote"] = doc["strong"][0]["quote"][:-4] + "已完美圆融无缺。"
        text = yaml.safe_dump(doc, allow_unicode=True)
    elif args.mutate == "shift_line":
        # 行号 +500：应被 C 行号校验抓出
        doc["strong"][0]["line"] = parse_line(doc["strong"][0]["line"])[0] + 500
        text = yaml.safe_dump(doc, allow_unicode=True)
    elif args.mutate == "drop_section":
        doc.pop("limit", None)
        text = yaml.safe_dump(doc, allow_unicode=True)
    elif args.mutate == "escape_t0":
        doc["strong"][0]["src"] = "docs/随笔参考/ref海云继梦法师_佛法修行体系研究.md"
        text = yaml.safe_dump(doc, allow_unicode=True)
    elif args.mutate == "falsify_conf":
        # 把 A 类逐字原话标为 C 类：应被 E 信度一致性抓出
        doc["limit"][0]["信度"] = "C"
        text = yaml.safe_dump(doc, allow_unicode=True)
    elif args.mutate == "drop_item":
        # 删去一条 limit 条目：应被 Y 最少条数抓出
        doc["limit"] = doc["limit"][1:]
        text = yaml.safe_dump(doc, allow_unicode=True)

    doc = yaml.safe_load(text)

    fails = []
    notes = []
    n_items = 0

    # ── Y 台账对账（meta.counts 须与实际条数相等）────────────────
    ledger = ((doc.get("meta") or {}).get(LEDGER) or {})
    actual = {
        "strong": len(doc.get("strong") or []),
        "medium": len(doc.get("medium") or []),
        "limit": len(doc.get("limit") or []),
        "negative_findings": len(doc.get("negative_findings") or []),
    }
    for k, v in actual.items():
        if k not in ledger:
            fails.append("Y meta.%s 缺 %s 之条数台账（新增／删除条目须同步）"
                         % (LEDGER, k))
        elif ledger[k] != v:
            fails.append("Y 条数台账对账不平：%s 台账 %s、实际 %s"
                         % (k, ledger[k], v))

    # ── A 结构 ────────────────────────────────────────────────────
    for sec, req in REQUIRED.items():
        if sec not in doc:
            fails.append("A 缺分组：%s" % sec)
            continue
        got = len(doc[sec] or [])
        if got < MIN_COUNT[sec]:
            fails.append("Y 分组 %s 仅 %d 条，少于下限 %d 条"
                         % (sec, got, MIN_COUNT[sec]))
        for it in doc[sec]:
            n_items += 1
            for k in req:
                if not it.get(k):
                    fails.append("A %s 缺字段 %s" % (it.get("id", "?"), k))

    # ── Y 条目 id 唯一且连号无缺 ──────────────────────────────────
    # 反向验证 L109 补立：id 重号会使「附录二按 id 直出」与「草稿按 id 引用」两处
    # 静默指向同一条，故须验唯一性。
    seen = {}
    for sec in ("strong", "medium", "limit"):
        for it in doc.get(sec) or []:
            iid = it.get("id")
            if iid in seen:
                fails.append("Y 条目 id 重号：%s（%s 与 %s）"
                             % (iid, seen[iid], sec))
            seen[iid] = sec
    for pre, hi in (("S", "S"), ("M", "M"), ("L", "L")):
        got = sorted(int(i[1:]) for i in seen
                     if isinstance(i, str) and re.fullmatch(pre + r"\d+", i))
        if got and got != list(range(1, max(got) + 1)):
            fails.append("Y %s 组编号不连号（须自 1 起连续）：%s" % (pre, got))

    # ── E 存疑诚实 ────────────────────────────────────────────────
    for sec in ("strong", "medium", "limit"):
        for it in doc.get(sec) or []:
            iid = it.get("id", "?")
            conf = str(it.get("信度", ""))
            if conf not in CONF_ALLOWED:
                fails.append("E %s 信度取值非法：「%s」（允许：%s）"
                             % (iid, conf, "／".join(CONF_ALLOWED)))
            # **A 类必为 A 信度**：strong 分组者系最强自述，标 B/C/D 即自相矛盾
            if sec == "strong" and conf not in ("A",):
                fails.append("E %s 属 strong 分组，信度却作「%s」——strong 必为 A"
                             % (iid, conf))
            if "待核" in conf and "status" not in it:
                fails.append("E %s 信度含待核而无 status" % iid)
            if "待核" in conf and not it.get("判读"):
                notes.append("E %s 待核项须正文显式说明" % iid)

    # ── C/D 回源 ──────────────────────────────────────────────────
    # 【L109 自纠·盲区】原设 win=2 之容差窗，本为容纳跨行引文；然此容差使
    # 「行号偏移 1–2 行」亦通过（反向验证 shift_line+1 未被抓出，即此盲区）。
    # 故改为：**登记为单行者须精确命中该行**；仅登记为区间者（`a-b`）才容差。
    win = 2
    for sec in ("strong", "medium", "limit"):
        for it in doc.get(sec) or []:
            iid = it.get("id", "?")
            src = it.get("src") or ""
            # B 存在 + 限 T0
            if not src.startswith(T0_ROOT + "/"):
                fails.append("B %s src 逸出一手栈 T0：%s" % (iid, src))
                continue
            if not os.path.exists(src):
                fails.append("B %s 文件不存在：%s" % (iid, src))
                continue
            with open(src, "r", encoding="utf-8", errors="replace") as f:
                lines = f.read().splitlines()
            lo, hi = parse_line(it.get("line"))
            if lo < 1 or hi > len(lines):
                fails.append("D %s 行号越界 %d-%d（文件共 %d 行）"
                             % (iid, lo, hi, len(lines)))
                continue
            is_range = hi > lo
            if is_range:
                win_txt = "\n".join(lines[max(0, lo - 1 - win): hi + win])
                tag = "区间容差±%d" % win
            else:
                win_txt = lines[lo - 1]
                tag = "单行精确"
            # C 逐字回源
            if norm(it["quote"]) not in norm(win_txt):
                # 再试宽松：仅去空白标点（RAD 归一已含）
                if norm_radical_only(it["quote"]) not in norm_radical_only(win_txt):
                    fails.append("C %s 引文未见底本（%s:%d-%d，%s）"
                                 % (iid, os.path.basename(src), lo, hi, tag))

    # ── E 否定性记录 ──────────────────────────────────────────────
    n_neg = len(doc.get("negative_findings") or [])
    if n_neg < MIN_NEGATIVE:
        fails.append("Y 否定性记录仅 %d 条，少于下限 %d 条" % (n_neg, MIN_NEGATIVE))
    for nf in doc.get("negative_findings") or []:
        for k in ("项", "状态", "检索范围", "实际命中", "结论"):
            if not nf.get(k):
                fails.append("E 否定性记录缺字段 %s：%s" % (k, nf.get("id", "?")))
        if nf.get("状态") not in ("查无", "未查", "已查（部分）", "查无（部分）"):
            fails.append("E 否定性状态取值非法（须查无／未查／已查（部分）"
                         "／查无（部分））：%s" % nf.get("状态"))
    # 否定性记录之 id 须与证据条目不重号（防「否定」冒充「证据」）
    ev_ids = set()
    for sec in ("strong", "medium", "limit"):
        for it in doc.get(sec) or []:
            ev_ids.add(it.get("id"))
    for nf in doc.get("negative_findings") or []:
        if nf.get("id") in ev_ids:
            fails.append("Y 否定性记录 id 与证据条目重号：%s" % nf.get("id"))

    # ── 报告 ─────────────────────────────────────────────────────
    print("实证库：%s" % YAML_PATH)
    print("条目：%d 条（strong %d／medium %d／limit %d）"
          % (n_items, len(doc.get("strong") or []), len(doc.get("medium") or []),
             len(doc.get("limit") or [])))
    print("否定性记录：%d 条" % len(doc.get("negative_findings") or []))
    for n in notes:
        print("  提示 %s" % n)
    if args.mutate:
        print("【反向验证模式 mutate=%s】" % args.mutate)
    if fails:
        print("FAIL %d 项：" % len(fails))
        for f in fails:
            print("  - %s" % f)
        return 1
    if args.mutate:
        exp = MUT_EXPECT.get(args.mutate, "")
        got = "".join(f for f in fails if f.startswith(exp)) if exp else ""
        if not got:
            print("【反向验证不符】期望标签 %s 未出现在失败项中" % exp)
            return 1
    print("ALL CHECKS PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
