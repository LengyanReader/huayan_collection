#!/usr/bin/env python3
"""Build the T6 probe: verbatim reuse of sutra text inside commentaries.

Pair A: T1735 (澄觀《華嚴經疏》, on the 80-fascicle sutra) vs T279 (80 華嚴)
Pair B: T1733 (法藏《探玄記》, on the 60-fascicle sutra) vs T278 (60 華嚴)

Method: strip markup and punctuation from both sides, index every N-character
window of the sutra, then scan the commentary for maximal common substrings of
length >= N. Each hit is classified by the 30 characters that precede it in the
commentary: a quotation mark, 云 / 曰, or 《 means 明引 (marked); otherwise 暗引
(unmarked). A hit is  distinctive when its opening N-gram occurs exactly once in
the sutra — that filters out formulaic strings such as 阿耨多羅三藐三菩提.

The output reports a sweep over N so the reader can see how much the numbers
depend on the threshold, and every example carries the nearest CBETA line id
(`lb`) on both sides, so it can be re-checked by hand.

Usage:
  python scripts/build_implicit_quotes.py
"""

from __future__ import annotations

import bisect
import hashlib
import json
import re
import sys
from collections import Counter
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CBETA = ROOT / "data" / "references" / "cbeta"
OUT = ROOT / "data" / "research" / "implicit_quotes.json"

N_MAIN = 12
SWEEP = (8, 10, 12, 16)
CTX = 30
PUNCT = set("，。、；：？！“”‘’「」『』（）〈〉《》…—·,.;:?!()<>[]{}　 \n\r\t¶")


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def strip_tags(raw: str) -> tuple[str, list[int]]:
    out: list[str] = []
    pos: list[int] = []
    i = 0
    for m in re.finditer(r"<[^>]+>", raw):
        seg = raw[i:m.start()]
        out.append(seg)
        pos.extend(range(i, m.start()))
        i = m.end()
    seg = raw[i:]
    out.append(seg)
    pos.extend(range(i, len(raw)))
    return "".join(out), pos


def strip_punct(clean: str) -> tuple[str, list[int]]:
    chars: list[str] = []
    pos: list[int] = []
    for i, ch in enumerate(clean):
        if ch in PUNCT:
            continue
        chars.append(ch)
        pos.append(i)
    return "".join(chars), pos


class Doc:
    def __init__(self, name: str, path: Path):
        self.name = name
        self.path = path
        self.raw = path.read_text(encoding="utf-8")
        m1 = re.search(r"<body\b", self.raw)
        m2 = self.raw.rfind("</body>")
        self.offset = m1.start() if m1 else 0
        body = self.raw[self.offset:(m2 if m2 > 0 else len(self.raw))]
        self.clean, raw_of_clean = strip_tags(body)
        self.raw_of_clean = [self.offset + i for i in raw_of_clean]
        self.norm, self.clean_of_norm = strip_punct(self.clean)
        self.lb = [(m.start(), m.group(1)) for m in
                   re.finditer(r'<lb n="([0-9a-z]+)"', self.raw)]
        self.lb_starts = [p for p, _ in self.lb]

    def raw_index(self, norm_index: int) -> int:
        return self.raw_of_clean[self.clean_of_norm[norm_index]]

    def lb_at(self, raw_index: int) -> str:
        j = bisect.bisect_right(self.lb_starts, raw_index) - 1
        return self.lb[j][1] if j >= 0 else "?"

    def context_before(self, norm_index: int) -> str:
        ci = self.clean_of_norm[norm_index]
        return self.clean[max(0, ci - CTX):ci]


def gram_counts(sutra: Doc, n: int) -> Counter:
    s = sutra.norm
    if len(s) < n:
        return Counter()
    return Counter(s[i:i + n] for i in range(len(s) - n + 1))


def align(com: Doc, sutra: Doc, n: int, counts: Counter) -> list[dict]:
    s = sutra.norm
    index: dict[str, int] = {}
    for i in range(len(s) - n + 1):
        index.setdefault(s[i:i + n], i)

    hits: list[dict] = []
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
        length = a - a0
        if length >= n:
            ctx = com.context_before(a0)
            wide = com.clean[max(0, com.clean_of_norm[a0] - 200):com.clean_of_norm[a0]]
            open_quote = wide.rfind("「") > wide.rfind("」")
            marked = open_quote or any(m in ctx for m in ("「", "『", "云", "曰", "《"))
            text = c[a0:a]
            if re.search(r"品第[一二三四五六七八九十百]+$", text):
                j = a if a > j else j + 1
                continue
            hits.append({
                "text": text,
                "length": length,
                "kind": "明引" if marked else "暗引",
                "distinct": counts.get(c[a0:a0 + n], 0) == 1,
                "ctx": ctx,
                "c_line": com.lb_at(com.raw_index(a0)),
                "s_line": sutra.lb_at(sutra.raw_index(b0)),
            })
        j = a if a > j else j + 1
    return hits


def summarise(hits: list[dict], sutra_len: int) -> dict:
    total = sum(h["length"] for h in hits)
    marked = [h for h in hits if h["kind"] == "明引"]
    unmarked = [h for h in hits if h["kind"] == "暗引"]
    uniq = [h for h in unmarked if h["distinct"]]
    lengths = sorted((h["length"] for h in hits), reverse=True)
    return {
        "hits": len(hits),
        "matched_chars": total,
        "sutra_chars": sutra_len,
        "coverage": round(total / sutra_len, 4) if sutra_len else 0,
        "marked": {"hits": len(marked), "chars": sum(h["length"] for h in marked)},
        "unmarked": {"hits": len(unmarked), "chars": sum(h["length"] for h in unmarked)},
        "unmarked_distinct": {"hits": len(uniq), "chars": sum(h["length"] for h in uniq)},
        "max_length": lengths[0] if lengths else 0,
        "median_length": lengths[len(lengths) // 2] if lengths else 0,
        "ge_40": sum(1 for x in lengths if x >= 40),
    }


def pick(hits: list[dict], n: int, distinct_only: bool) -> list[dict]:
    pool = [h for h in hits if h["kind"] == "暗引" and (h["distinct"] or not distinct_only)]
    # 年號、譯記、干支一類的相同段落是史料共用，不是經文暗引
    pool = [h for h in pool if not re.search(r"[0-9０-９]|歲次|義熙|年歲", h["text"])]
    pool.sort(key=lambda h: -h["length"])
    return [{k: h[k] for k in ("text", "length", "c_line", "s_line", "ctx")} for h in pool[:n]]


def pick_marked(hits: list[dict], n: int) -> list[dict]:
    pool = sorted((h for h in hits if h["kind"] == "明引"), key=lambda h: -h["length"])
    return [{k: h[k] for k in ("text", "length", "c_line", "s_line", "ctx")} for h in pool[:n]]


def main() -> int:
    pairs = [
        ("A", "T1735", "T279", "澄觀《華嚴經疏》 vs 八十華嚴"),
        ("B", "T1733", "T278", "法藏《探玄記》 vs 六十華嚴"),
    ]
    files = {
        "T1735": "T35n1735.xml",
        "T279": "T10n0279.xml",
        "T1733": "T35n1733.xml",
        "T278": "T09n0278.xml",
    }
    docs: dict[str, Doc] = {}
    for _, c, s, _ in pairs:
        for key in (c, s):
            if key not in docs:
                docs[key] = Doc(key, CBETA / files[key])

    result = {
        "meta": {
            "date": date.today().isoformat(),
            "n_main": N_MAIN,
            "sweep": list(SWEEP),
            "ctx": CTX,
            "method": (f"去标记去标点后取 N 字窗索引；注释侧贪心取极大公共子串（≥N 字），"
                       f"按左侧 {CTX} 字内是否有「『云曰《 判明引／暗引；"
                       f"首 N 字在经中只出现一次者记「独见」，用于滤掉套语。"),
            "sources": {},
        },
        "pairs": {},
    }
    for key, d in docs.items():
        result["meta"]["sources"][key] = {
            "path": str(d.path.relative_to(ROOT)).replace("\\", "/"),
            "sha256": sha256(d.path.read_bytes()),
        }

    for pid, c, s, label in pairs:
        com, sutra = docs[c], docs[s]
        counts = {n: gram_counts(sutra, n) for n in SWEEP}
        sweep = {}
        hits_main: list[dict] = []
        for n in SWEEP:
            hits = align(com, sutra, n, counts[n])
            st = summarise(hits, len(sutra.norm))
            sweep[str(n)] = {k: st[k] for k in ("hits", "matched_chars", "coverage",
                                                "marked", "unmarked", "unmarked_distinct",
                                                "ge_40")}
            if n == N_MAIN:
                hits_main = hits
                main_stats = st
        result["pairs"][pid] = {
            "label": label,
            "commentary": c,
            "sutra": s,
            "stats": main_stats,
            "sweep": sweep,
            "examples_marked": pick_marked(hits_main, 3),
            "examples_unmarked": pick(hits_main, 3, distinct_only=True),
            "examples_unmarked_any": pick(hits_main, 2, distinct_only=False),
        }
        print(f"{pid} {label}: N={N_MAIN} hits={main_stats['hits']} "
              f"coverage={main_stats['coverage']:.2%} "
              f"marked={main_stats['marked']['hits']} unmarked={main_stats['unmarked']['hits']} "
              f"distinct={main_stats['unmarked_distinct']['hits']}")
        for n in SWEEP:
            st = sweep[str(n)]
            print(f"   N={n:2d}: hits={st['hits']:5d} cov={st['coverage']:.2%} "
                  f"unmarked_distinct={st['unmarked_distinct']['hits']}")

    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("written", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
