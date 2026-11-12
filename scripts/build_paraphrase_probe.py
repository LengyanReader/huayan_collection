#!/usr/bin/env python3
"""Build the T7 probe: how a commentary handles the sutra text it does NOT quote.

Pair A: T1735 (澄觀《華嚴經疏》) vs T279 (80 華嚴)
Pair B: T1733 (法藏《探玄記》) vs T278 (60 華嚴)

T7 asks whether a commentary restates or condenses the sutra in its own words.
This probe measures three things, each with its own limit:

  1. 长度比 — per 品, commentary characters / sutra characters. A ratio above 1
     means the commentary is longer than the text it comments on, so "condensed
     the sutra" cannot be the whole story.
  2. 逐品引用率 — every maximal common substring of >= 12 characters is assigned
     to the 品 it quotes (by its position in the *sutra*), then summed per 品.
     This bounds how much of each 品 is reproduced verbatim.
  3. 锚点链 — greedy alignment at 6 characters, merging neighbouring anchors when
     the sutra gap is <= 40 and the commentary gap <= 20. The span of a chain is
     how far the commentary walks *through* the sutra; no chain spanning 120
     characters means the commentary never follows a long run of text.
  4. 节略标记 — fixed phrases by which a commentator says outright that he is
     skipping something (準前 / 例知 / 文略 …), counted with CBETA line ids.

Usage:
  python scripts/build_paraphrase_probe.py
"""

from __future__ import annotations

import bisect
import hashlib
import json
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_implicit_quotes import Doc  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
CBETA = ROOT / "data" / "references" / "cbeta"
OUT = ROOT / "data" / "research" / "paraphrase_probe.json"

HIT_N = 12                     # 逐品引用率所用最短公共串
CHAIN_N = 6                    # 锚点长度
CHAIN_SGAP = 40                # 锚点间经文最大间隔
CHAIN_CGAP = 20                # 锚点间注疏最大间隔
CTX = 20                       # 标记上下文

# 三类用语。单字「略」义太泛；「不具」「故略」「文略」「此略」经抽样多为他义
# （不具足／故＋略／文字简略），一律不收——宁可少算，不可混算。
MARKERS = [
    ("略不X", r"略不[釋頌明說牒引及載出]"),   # 下略不釋／餘略不頌
    ("準前", r"[準准]前"),                    # 準前思之／準前可知
    ("例類知", r"[例類]知"),                  # 餘可例知／餘可類知
]

FILES = {
    "T1735": "T35n1735.xml",
    "T279": "T10n0279.xml",
    "T1733": "T35n1733.xml",
    "T278": "T09n0278.xml",
}

PIN_RE = re.compile(r'<cb:mulu level="1"[^>]*type="品">([^<]+)</cb:mulu>')


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def pin_spans(doc: Doc) -> list[tuple[int, str, int, int]]:
    """(品号, 标题, raw 起, raw 止)；若首品无标记，则卷首至次品标记算首品。"""
    hits = []
    for m in PIN_RE.finditer(doc.raw):
        num = int(re.match(r"(\d+)", m.group(1)).group(1))
        hits.append((num, m.group(1).strip(), m.start()))
    spans = []
    for i, (num, title, start) in enumerate(hits):
        end = hits[i + 1][2] if i + 1 < len(hits) else len(doc.raw)
        spans.append((num, title, start, end))
    if spans and spans[0][0] > 1:
        spans.insert(0, (1, "（卷首）", doc.offset, spans[0][2]))
    return spans


def raw_to_norm(doc: Doc) -> list[int]:
    return [doc.raw_index(i) for i in range(len(doc.norm))]


def hits(com: Doc, sutra: Doc, n: int) -> list[tuple[int, int, int, int]]:
    """注释侧贪心取极大公共子串（≥n）：(注疏起, 注疏止, 经文起, 经文止)，norm 座标。"""
    s = sutra.norm
    index: dict[str, int] = {}
    for i in range(len(s) - n + 1):
        index.setdefault(s[i:i + n], i)
    res = []
    c = com.norm
    j = 0
    while j <= len(c) - n:
        k = index.get(c[j:j + n])
        if k is None:
            j += 1
            continue
        a, b = j, k
        while a < len(c) and b < len(s) and c[a] == s[b]:
            a += 1
            b += 1
        a0, b0 = j, k
        while a0 > 0 and b0 > 0 and c[a0 - 1] == s[b0 - 1]:
            a0 -= 1
            b0 -= 1
        res.append((a0, a, b0, b))
        j = a if a > j else j + 1
    return res


def chains(anc: list[tuple[int, int, int, int]]) -> list[dict]:
    """把相邻锚点并为链：经文间隔 ≤40、注疏间隔 ≤20 才继续。"""
    out = []
    i = 0
    while i < len(anc):
        j = i
        while j + 1 < len(anc):
            _, a1, _, b1 = anc[j]
            c0, _, d0, _ = anc[j + 1]
            if 1 <= d0 - b1 <= CHAIN_SGAP and 0 <= c0 - a1 <= CHAIN_CGAP:
                j += 1
            else:
                break
        if j > i:
            span = anc[j][3] - anc[i][2]
            hit = sum(x[1] - x[0] for x in anc[i:j + 1])
            out.append({
                "links": j - i + 1,
                "span": span,
                "hit": hit,
                "ratio": round(hit / span, 3) if span else 0.0,
                "c_lb": anc[i][0],
                "s_lb": anc[i][2],
            })
        i = j + 1
    return out


def markers(doc: Doc, norm_start: int, norm_end: int) -> list[dict]:
    out = []
    text = doc.norm
    for label, pat in MARKERS:
        for m in re.finditer(pat, text[norm_start:norm_end]):
            i = norm_start + m.start()
            raw = doc.raw_index(i)
            ci = doc.clean_of_norm[i]
            out.append({
                "type": label,
                "lb": doc.lb_at(raw),
                "ctx": doc.clean[max(0, ci - CTX):ci + m.end() - m.start() + CTX].replace("\n", " ").strip(),
                "before": doc.clean[max(0, ci - 10):ci],
            })
    out.sort(key=lambda x: x["lb"])
    return out


def pick_examples(mk: list[dict], n: int) -> list[dict]:
    """优先取「餘…」一类（指「其余从略」），再按行号补齐。"""
    scored = sorted(mk, key=lambda m: (0 if "餘" in m["before"] else 1, m["lb"]))
    out, seen = [], set()
    for m in scored:
        if m["lb"] in seen:
            continue
        seen.add(m["lb"])
        out.append({"type": m["type"], "lb": m["lb"], "ctx": m["ctx"]})
        if len(out) == n:
            break
    return out


def main() -> int:
    pairs = [
        ("A", "T1735", "T279", "澄觀《華嚴經疏》 vs 八十華嚴"),
        ("B", "T1733", "T278", "法藏《探玄記》 vs 六十華嚴"),
    ]
    docs = {k: Doc(k, CBETA / f) for k, f in FILES.items()}
    nbounds = {k: raw_to_norm(d) for k, d in docs.items()}
    spins = {k: pin_spans(d) for k, d in docs.items()}

    result = {
        "meta": {
            "date": date.today().isoformat(),
            "hit_n": HIT_N,
            "chain": {"n": CHAIN_N, "sgap": CHAIN_SGAP, "cgap": CHAIN_CGAP},
            "markers": [label for label, _ in MARKERS],
            "method": (f"①长度比：按品对齐，注疏字数÷经文字数；②逐品引用率："
                       f"取 ≥{HIT_N} 字极大公共串，按其在经文中的位置归品后累加；"
                       f"③锚点链：{CHAIN_N} 字锚点，经文间隔≤{CHAIN_SGAP}、注疏间隔≤{CHAIN_CGAP} 者并链记跨度；"
                       f"④节略标记：{len(MARKERS)} 类用语计数并附行号；只收「略不釋／頌」「準前」「例類知」，"
                       f"多义的「不具」「故略」「文略」「此略」不收。"),
            "sources": {},
        },
        "pairs": {},
    }
    for k, d in docs.items():
        result["meta"]["sources"][k] = {
            "path": str(d.path.relative_to(ROOT)).replace("\\", "/"),
            "sha256": sha256(d.path.read_bytes()),
        }

    for pid, ck, sk, label in pairs:
        com, sutra = docs[ck], docs[sk]
        cs, ss = spins[ck], spins[sk]
        cn, sn = nbounds[ck], nbounds[sk]
        cmap = {num: (title, a, b) for num, title, a, b in cs}
        smap = {num: (title, a, b) for num, title, a, b in ss}

        hs = hits(com, sutra, HIT_N)   # 每条按其经文起点归品

        rows = []
        for num in sorted(set(cmap) & set(smap)):
            ctitle, cra, crb = cmap[num]
            stitle, sra, srb = smap[num]
            c0 = bisect.bisect_left(cn, cra)
            c1 = bisect.bisect_left(cn, crb)
            s0 = bisect.bisect_left(sn, sra)
            s1 = bisect.bisect_left(sn, srb)
            quoted = sum(a1 - a0 for a0, a1, b0, b1 in hs if s0 <= b0 < s1)
            n_hits = sum(1 for a0, a1, b0, b1 in hs if s0 <= b0 < s1)
            mk = markers(com, c0, c1)
            rows.append({
                "no": num,
                "title": stitle,
                "sutra_chars": s1 - s0,
                "com_chars": c1 - c0,
                "ratio": round((c1 - c0) / (s1 - s0), 3) if s1 > s0 else 0.0,
                "quoted_chars": quoted,
                "quoted_hits": n_hits,
                "quoted_share": round(quoted / (s1 - s0), 5) if s1 > s0 else 0.0,
                "marked": len(mk),
            })

        all_mk = markers(com, 0, len(com.norm))
        by_type: dict[str, int] = {}
        for m in all_mk:
            by_type[m["type"]] = by_type.get(m["type"], 0) + 1

        ch = chains(hits(com, sutra, CHAIN_N))
        spans = sorted((x["span"] for x in ch), reverse=True)

        shares = sorted(r["quoted_share"] for r in rows)
        med = shares[len(shares) // 2] if shares else 0.0
        s_chars = sum(r["sutra_chars"] for r in rows)
        c_chars = sum(r["com_chars"] for r in rows)
        q_chars = sum(r["quoted_chars"] for r in rows)
        longest = max(hs, key=lambda x: x[1] - x[0]) if hs else (0, 0, 0, 0)

        result["pairs"][pid] = {
            "label": label,
            "commentary": ck,
            "sutra": sk,
            "stats": {
                "pins": len(rows),
                "sutra_chars": s_chars,
                "com_chars": c_chars,
                "length_ratio": round(c_chars / s_chars, 3) if s_chars else 0.0,
                "quoted_chars": q_chars,
                "quoted_share": round(q_chars / s_chars, 5) if s_chars else 0.0,
                "quoted_share_median": round(med, 5),
                "quoted_share_max": round(shares[-1], 5) if shares else 0.0,
                "hits": len(hs),
                "max_hit": longest[1] - longest[0],
                "max_hit_c_lb": com.lb_at(com.raw_index(longest[0])) if hs else "",
                "max_hit_s_lb": sutra.lb_at(sutra.raw_index(longest[2])) if hs else "",
                "max_hit_head": com.clean[com.clean_of_norm[longest[0]]:com.clean_of_norm[longest[1]]][:60].replace("\n", "") if hs else "",
                "markers_total": len(all_mk),
                "markers_by_type": by_type,
                "chains": len(ch),
                "chain_max_span": spans[0] if spans else 0,
                "chain_spans_ge_60": sum(1 for x in spans if x >= 60),
                "chain_spans_ge_120": sum(1 for x in spans if x >= 120),
            },
            "pins": rows,
            "top": sorted(rows, key=lambda r: -r["quoted_share"])[:5],
            "bottom": sorted(rows, key=lambda r: r["quoted_share"])[:5],
            "examples": pick_examples(all_mk, 3),
        }
        st = result["pairs"][pid]["stats"]
        print(f"{pid} {label}: pins={st['pins']} 引文率={st['quoted_share']:.3%} "
              f"(中位 {st['quoted_share_median']:.3%}) 长比={st['length_ratio']} "
              f"标记={st['markers_total']} 链={st['chains']} 链最长={st['chain_max_span']} "
              f"单条最长={st['max_hit']}")

    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("written", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
