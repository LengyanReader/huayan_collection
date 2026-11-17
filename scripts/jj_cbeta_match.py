# -*- coding: utf-8 -*-
"""《九九華嚴》OCR 稿 × CBETA `T10n0279` **逐字命中探针**（程序切片·非手抄）

用途：给定某集 OCR 稿（delivery/epNN.md），把每条 cue 归一化为纯汉字，
在 T10n0279 去 note/app/标签并压平后的正文里做**精确 n-gram 命中**，
再向两侧扩展到最长公共串。命中的片段连同 卷/品 元数据一并输出，
供校订稿 §四「CBETA 回源」直接消费——**杜绝手抄转写漂移**。

用法：
  python scripts/jj_cbeta_match.py --ep 15 --json .tmp/ep15_cbeta.json
  python scripts/jj_cbeta_match.py --md docs/hy_refs/sub_extract/delivery/ep16.md --json .tmp/ep16_cbeta.json
  python scripts/jj_cbeta_match.py --ep 15 --text      # 人读摘要

判定口径（保守·宁缺毋造）：
  - 只认**连续汉字**完全相等（标点/空白/拉丁不计），不认近形、不认通假；
  - 单次命中长度 ≥ `--min-len`（默认 12 字）才收录；
  - 命中仅证明「此串见于底本」，**不等于**讲者已逐字引经；引用仍须标〔CBETA 对勘〕。
"""
import argparse
import io
import json
import os
import re
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

CBETA = "data/references/cbeta/T10n0279.xml"
HAN = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")
CUE_MD = re.compile(r"^`\[(\d\d):(\d\d):(\d\d)[\u2013\u2014-]"
                    r"(\d\d):(\d\d):(\d\d)\]`\s*(.+)$")
JUAN_OPEN = re.compile(r'<cb:juan n="(\d+)" fun="open"')
PIN_OPEN = re.compile(r'<cb:mulu level="1" n="(\d+)" type="品">([^<]+)')


def load_cbeta(path=CBETA):
    raw = io.open(path, encoding="utf-8").read()
    # 去校勘注与异文块（可嵌套·重复剥至稳定）
    for _ in range(4):
        prev = raw
        raw = re.sub(r"<note\b[^>]*>.*?</note>", "", raw, flags=re.S)
        raw = re.sub(r"<app\b[^>]*>.*?</app>", "", raw, flags=re.S)
        if raw == prev:
            break
    juan = pin = None
    chars, jus, pins = [], [], []
    for ln in raw.splitlines():
        m = JUAN_OPEN.search(ln)
        if m:
            juan = int(m.group(1))
        m = PIN_OPEN.search(ln)
        if m:
            pin = (int(m.group(1)), re.sub(r"^\d+\s*", "", m.group(2).strip()))
        txt = re.sub(r"<[^>]+>", "", ln)
        for ch in txt:
            if HAN.match(ch):
                chars.append(ch)
                jus.append(juan)
                pins.append(pin)
    # 品×卷 连续区间（供切片时钳制，不跨品/跨卷）
    spans = []
    start = 0
    for i in range(1, len(pins) + 1):
        if i == len(pins) or pins[i] != pins[i - 1] or jus[i] != jus[i - 1]:
            p = pins[i - 1]
            if p is not None:
                spans.append({
                    "pin_no": p[0], "pin": p[1], "juan": jus[i - 1],
                    "start": start, "end": i,
                })
            start = i
    return "".join(chars), jus, pins, spans


def build_grams(cb, n=10):
    d = {}
    for i in range(len(cb) - n + 1):
        d.setdefault(cb[i:i + n], []).append(i)
    return d


def extend(cb, q, ci, qi):
    """以 (ci,qi) 为锚向两侧扩到最长相等串，返回 cb 起止、q 起止。"""
    a, b = ci, qi
    while a > 0 and b > 0 and cb[a - 1] == q[b - 1]:
        a -= 1
        b -= 1
    c, d = ci, qi
    while c + 1 < len(cb) and d + 1 < len(q) and cb[c + 1] == q[d + 1]:
        c += 1
        d += 1
    return a, c + 1, b, d + 1


def match_cue(q, grams, cb, n, min_len):
    if len(q) < min_len:
        return []
    found = {}
    for qi in range(len(q) - n + 1):
        g = q[qi:qi + n]
        for ci in grams.get(g, ()):  # 同一 gram 可能多处出现
            a, c, b, d = extend(cb, q, ci, qi)
            if c - a >= min_len:
                key = (a, c)
                # 取该 cb 区间内最长的 q 对应
                if key not in found or (d - b) > (found[key][2] - found[key][1]):
                    found[key] = (a, b, d)
    # 去掉被更长命中覆盖的短命中
    out = []
    for (a, c), (_a, b, d) in sorted(found.items()):
        if out and a < out[-1][1]:
            if c <= out[-1][1]:
                continue
        out.append((a, c, b, d))
    return out


def parse_cues(path):
    cues = []
    for ln in io.open(path, encoding="utf-8"):
        m = CUE_MD.match(ln.rstrip("\n"))
        if not m:
            continue
        t = "%s:%s:%s" % (m.group(1), m.group(2), m.group(3))
        q = "".join(HAN.findall(m.group(7)))
        cues.append({"t": t, "raw": m.group(7).strip(), "q": q})
    return cues


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ep", type=int, default=0)
    ap.add_argument("--md", default="")
    ap.add_argument("--json", default="")
    ap.add_argument("--min-len", type=int, default=12)
    ap.add_argument("--text", action="store_true")
    a = ap.parse_args()
    md = a.md or ("docs/hy_refs/sub_extract/delivery/ep%02d.md" % a.ep)
    if not os.path.exists(md):
        print("【缺稿】%s" % md)
        return 1
    cb, jus, pins, spans = load_cbeta()
    grams = build_grams(cb, 10)
    cues = parse_cues(md)
    hits = []
    for i, c in enumerate(cues):
        for (s, e, qs, qe) in match_cue(c["q"], grams, cb, 10, a.min_len):
            pin = pins[s] or (None, None)
            sp = next((x for x in spans if x["start"] <= s < x["end"]), None)
            hits.append({
                "cue": i,
                "t": c["t"],
                "len": e - s,
                "text": cb[s:e],
                "juan": jus[s],
                "pin_no": pin[0],
                "pin": pin[1],
                "pos": s,
                "span_start": sp["start"] if sp else s,
                "span_end": sp["end"] if sp else e,
                "before": cb[max(sp["start"] if sp else 0, s - 40):s],
                "after": cb[e:min(sp["end"] if sp else len(cb), e + 40)],
                "cue_raw": c["raw"],
            })
    # 按底本位置去重（同一底本文段被多条 cue 命中时保留最长）
    uniq = {}
    for h in hits:
        k = (h["pos"], h["len"])
        if k not in uniq or h["len"] > uniq[k]["len"]:
            uniq[k] = h
    hits = sorted(uniq.values(), key=lambda x: x["pos"])

    print("【CBETA 命中】%s · cues=%d · 命中段=%d · min_len=%d"
          % (md, len(cues), len(hits), a.min_len))
    for h in hits[:60]:
        print("  %s §%s %s @%d len=%d :: %s"
              % (h["t"], h["pin_no"], h["pin"], h["pos"], h["len"],
                 h["text"][:48] + ("…" if h["len"] > 48 else "")))
    if len(hits) > 60:
        print("  … 余 %d 段（见 JSON）" % (len(hits) - 60))

    if a.json:
        out = {
            "md": md,
            "min_len": a.min_len,
            "cues": len(cues),
            "cbeta_han": len(cb),
            "pin_spans": spans,
            "hits": hits,
        }
        io.open(a.json, "w", encoding="utf-8", newline="\n").write(
            json.dumps(out, ensure_ascii=False, indent=1))
        print("已写 %s" % a.json)
    return 0


if __name__ == "__main__":
    sys.exit(main())