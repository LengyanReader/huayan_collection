#!/usr/bin/env python3
"""Build the T9 末会 probe: how the three 入法界品 divide the same journey.

The 入法界品 is where 善財 visits one teacher after another. Each visit ends with
the same formula — 辭退 — and the next begins with a new teacher named by the
previous one. So the number and position of those 辭退 marks is a segmentation
the text itself provides, with no editorial hand.

Four observations, each answerable from the text alone:

  1. 段数 — how many 辭退 marks does each recension have inside the 入法界品?
     (80 華嚴 品39 / 60 華嚴 品34 / 40 華嚴 whole). Two caveats built in:
     the last visit (普賢) has no mark, and the opening assemblies also
     disperse with 辭退 — so marks are split into 参末 (pre-window names
     善財) and 会众散 (it does not). A count is "departures with the
     formula", not "visits".
  2. 字面锚 — take the 40 characters before each 80-華嚴 mark, find them in
     the other two, and measure how far that lands from their nearest mark.
     A window anchors only when it occurs EXACTLY ONCE in the destination
     (first-hit matching would slam different visits' identical formulae
     onto one spot); windows with several occurrences are counted 复见.
     Same place / nearby / drifted / no anchor. This measures *wording
     affinity* at the boundaries — not visit correspondence: 无锚 only
     means the verbatim window is absent, never that the visit is.
  3. 同名锚 — the departure formula sometimes writes the teacher's name
     outright (善財禮賢勝足). Extract 禮X足 objects in each mark's
     pre-window on both sides, drop a stoplist, and pair marks whose
     extracted names are equal under a monotonic (same-order) matching.
     Proper names and generic titles are counted separately: a proper-name
     pair anchors one visit; a generic pair (王, 夜天…) is only
     order-consistent, not an identification.
  4. 参长剖面 — clean-char length between consecutive marks per recension.

Caveat built in: 「辭退」 marks the *end* of a visit, so the last visit (普賢)
has no mark.

Usage:
  python scripts/build_endgame_probe.py
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from bisect import bisect_left
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_implicit_quotes import Doc  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
CBETA = ROOT / "data" / "references" / "cbeta"
OUT = ROOT / "data" / "research" / "endgame_probe.json"

MARK = "辭退"
ANCHORS = (40, 32, 24, 16)      # 锚窗长度，逐级降
SAME = 60                        # 同一处
NEAR = 300                       # 邻近
CTX = 24                         # 标记上下文（clean 字）
CHAIN_N = 8                      # 链式对齐的字窗
NAME_WIN = 120                   # 参末套语窗口（标记前 clean 字）
SHUCAI_WIN = 200                 # 参末/会众散判定窗（标记前 clean 字）

FILES = {
    "T279": ("T10n0279.xml", 39, "八十華嚴〈入法界品〉"),
    "T278": ("T09n0278.xml", 34, "六十華嚴〈入法界品〉"),
    "T293": ("T10n0293.xml", None, "四十華嚴（全）"),
}
PIN = re.compile(r'<cb:mulu level="1"[^>]*type="品">(\d+) ')

# 参末套语「禮X足」对象：先去掉尾衔，再做同名配对
NAME_RE = re.compile(r"禮([一-鿿]{1,8})足")
STOP = {"佛", "世尊", "如來", "其", "彼", "諸", "已", "足", "雙", "頭",
        "塔", "廟", "舍利", "合掌", "膝", "地"}
# 通名（类称），不算参名可锚
GENERIC = {"王", "長者", "居士", "菩薩", "比丘", "比丘尼", "優婆夷", "優婆塞",
           "婆羅門", "夜天", "夜神", "夜", "童子", "童女", "天女", "船師", "外道",
           "仙人", "神", "地神", "道士"}
TAIL_TITLES = ("比丘尼", "優婆夷", "優婆塞", "婆羅門", "長者", "比丘", "菩薩",
               "夜天", "夜神", "童子", "童女", "天女", "居士", "船師", "外道",
               "仙人", "國王", "王者", "神")


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def scope(doc: Doc, pin: int | None) -> tuple[int, int, str]:
    """返回 (norm 起, norm 止, 起处 lb)。pin=None 取全篇。"""
    if pin is None:
        return 0, len(doc.norm), doc.lb_at(doc.raw_index(0))
    for m in PIN.finditer(doc.raw):
        if int(m.group(1)) == pin:
            raw = m.start()
            start = sum(1 for i in range(len(doc.norm)) if doc.raw_index(i) < raw)
            return start, len(doc.norm), doc.lb_at(raw)
    raise SystemExit(f"品 {pin} not found")


def marks_of(doc: Doc, a: int, b: int) -> list[int]:
    return [i for i in range(a, b) if doc.norm.startswith(MARK, i)]


def anchor_to(src: Doc, pos: int, dst: Doc) -> tuple[int, int] | tuple[str, int] | None:
    """把 src 中 pos 之前的一段文字映射到 dst。

    唯一出现才可锚：返回 (落点, 窗长)。窗在 dst 出现多次 → 套语复见，
    返回 ("multi", 次数)——首见即中会把不同参的相同套语撞到一处。
    各级窗都 0 见 → None。
    """
    for n in ANCHORS:
        if pos < n:
            continue
        w = src.norm[pos - n:pos]
        hits = [m.start() for m in re.finditer(re.escape(w), dst.norm)]
        if len(hits) == 1:
            return hits[0] + n, n
        if len(hits) > 1:
            return "multi", len(hits)
    return None


def classify(dist: int | None) -> str:
    if dist is None:
        return "无锚"
    if dist <= SAME:
        return "同一处"
    if dist <= NEAR:
        return "邻近"
    return "漂移"


def uniq_index(doc: Doc, n: int) -> dict[str, int]:
    """n-gram → 唯一起点；出现一次以上记 -1（不复用首见，避免假锚）。"""
    idx: dict[str, int] = {}
    s = doc.norm
    for i in range(len(s) - n + 1):
        g = s[i:i + n]
        idx[g] = -1 if g in idx else i
    return idx


def chain_of(src: Doc, dst: Doc, n: int) -> list[tuple[int, int]]:
    """src 的 n-gram 唯一命中 dst 者为候选，取两侧位置同增的最长链（LIS）。"""
    idx = uniq_index(dst, n)
    s = src.norm
    cand = []
    for i in range(len(s) - n + 1):
        j = idx.get(s[i:i + n])
        if j is not None and j >= 0:
            cand.append((i, j))
    tails: list[int] = []
    tail_at: list[int] = []
    prev = [-1] * len(cand)
    for k, (_, j) in enumerate(cand):
        p = bisect_left(tails, j)
        if p == len(tails):
            tails.append(j)
            tail_at.append(k)
        else:
            tails[p] = j
            tail_at[p] = k
        prev[k] = tail_at[p - 1] if p else -1
    if not tail_at:
        return []
    out, k = [], tail_at[-1]
    while k >= 0:
        out.append(cand[k])
        k = prev[k]
    out.reverse()
    return out


def map_pos(xs: list[int], ys: list[int], p: int, limit: int) -> int | None:
    """按链分段线性插值；链覆盖范围之外不给位置（不外推）。"""
    if not xs or p < xs[0] or p > xs[-1]:
        return None
    k = bisect_left(xs, p)
    if k < len(xs) and xs[k] == p:
        return max(0, min(limit - 1, ys[k]))
    x0, x1, y0, y1 = xs[k - 1], xs[k], ys[k - 1], ys[k]
    q = y0 + (p - x0) * (y1 - y0) / (x1 - x0)
    return max(0, min(limit - 1, int(round(q))))


def family_marks(doc: Doc, a: int, b: int) -> list[tuple[int, str]]:
    """收束语族：辭退／辭去／而退／「遶（繞、匝）…而去」。

    先取动词性收束语（辭退／辭去／而退）；「匝…而去」只在与前三者
    不重叠时计入——否则「遶…辭退而去」里的 匝 会吞掉真正的 辭退。
    """
    s = doc.norm
    strong: list[tuple[int, int, str]] = []
    for pat in ("辭退", "辭去", "而退"):
        start = a
        while True:
            p = s.find(pat, start, b)
            if p < 0:
                break
            strong.append((p, len(pat), pat))
            start = p + 1
    strong.sort()
    accepted: list[tuple[int, int, str]] = []
    last_end = -1
    for p, ln, kind in strong:
        if p < last_end:
            continue
        accepted.append((p, ln, kind))
        last_end = p + ln
    for m in re.finditer(r"[遶繞匝]", s[a:b]):
        p = a + m.start()
        q = s.find("而去", p + 1, min(b, p + 12))
        if q <= 0:
            continue
        ln = q + 2 - p
        if any(p < st + ln0 and p + ln > st for st, ln0, _ in accepted):
            continue
        accepted.append((p, ln, "匝…而去"))
    accepted.sort()
    return [(p, kind) for p, _, kind in accepted]


def clean_ctx(doc: Doc, pos: int, n: int, before: bool = True) -> str:
    ci = doc.clean_of_norm[pos]
    return (doc.clean[max(0, ci - n):ci] if before
            else doc.clean[ci:ci + n]).replace("\n", "").strip()


def slice_at(doc: Doc, pos: int, before: int = 18, after: int = 6) -> str:
    """以 norm 位置为心取 clean 片段（含标记本身），供引文回源。"""
    ci = doc.clean_of_norm[pos]
    return doc.clean[max(0, ci - before):ci + after].replace("\n", "").strip()


def extract_name(doc: Doc, pos: int) -> tuple[str | None, str]:
    """参末套语「禮X足」对象：标记前 NAME_WIN 字内最后一个可取对象。"""
    win = clean_ctx(doc, pos, NAME_WIN)
    hits = [h for h in NAME_RE.findall(win) if h not in STOP]
    if not hits:
        return None, win[-CTX:]
    raw = hits[-1]
    for t in TAIL_TITLES:                      # 去尾衔：德雲比丘→德雲
        if raw.endswith(t) and len(raw) > len(t):
            raw = raw[: -len(t)]
            break
    if raw in STOP or not raw:
        return None, win[-CTX:]
    return raw, win[-CTX:]


def pair_by_name(seq_a: list[str | None], seq_b: list[str | None],
                 generic: set[str]) -> list[dict]:
    """单调同名配对：LCS 只在名字（含 None 不配）上。返回配对行。"""
    la, lb = len(seq_a), len(seq_b)
    dp = [[0] * (lb + 1) for _ in range(la + 1)]
    for i in range(la - 1, -1, -1):
        for j in range(lb - 1, -1, -1):
            if seq_a[i] and seq_a[i] == seq_b[j]:
                dp[i][j] = dp[i + 1][j + 1] + 1
            else:
                dp[i][j] = max(dp[i + 1][j], dp[i][j + 1])
    pairs, i, j = [], 0, 0
    while i < la and j < lb:
        if seq_a[i] and seq_a[i] == seq_b[j]:
            nm = seq_a[i]
            pairs.append({"a_index": i, "b_index": j, "name": nm,
                          "generic": nm in generic})
            i += 1
            j += 1
        elif dp[i + 1][j] >= dp[i][j + 1]:
            i += 1
        else:
            j += 1
    return pairs


def main() -> int:
    docs = {k: Doc(k, CBETA / f) for k, (f, _, _) in FILES.items()}
    scopes, marks = {}, {}
    for k, (f, pin, label) in FILES.items():
        a, b, lb = scope(docs[k], pin)
        scopes[k] = {"label": label, "pin": pin, "start": a, "end": b,
                     "lb": lb, "chars": sum(1 for i in range(a, b)
                                            if docs[k].norm[i:i + 1].strip())}
        marks[k] = marks_of(docs[k], a, b)

    result = {
        "meta": {
            "date": date.today().isoformat(),
            "mark": MARK,
            "anchor_lengths": list(ANCHORS),
            "same_within": SAME,
            "near_within": NEAR,
            "name_window": NAME_WIN,
            "shucai_window": SHUCAI_WIN,
            "method": (f"①段数：在〈入法界品〉范围内数「{MARK}」——每次参访以「{MARK}」收束，"
                       f"末参（普賢）无此语；又开初会众散退亦用此语，故按标记前 "
                       f"{SHUCAI_WIN} 字内是否出现「善財」分为参末／会众散两计。"
                       f"②字面锚：取八十本每个标记前 {ANCHORS[0]} 字（不足则递减至 "
                       f"{ANCHORS[-1]} 字），在另一本中原样查找，唯该窗在对方**恰出现一次**"
                       f"才可锚（套语多见则记复见，首见即中会把不同参的同套语撞到一处），"
                       f"落点离该本最近标记 ≤{SAME} 字为同一处、≤{NEAR} 邻近、否则漂移——"
                       f"这量的是参界措辞亲缘，无锚只说明原样窗不存在，不证明该参为对方所无。"
                       f"③同名锚：取各标记前 {NAME_WIN} 字内「禮X足」对象（去尾衔、"
                       f"去虚指），两侧同名且次序单调者配对；正名与通名（王、夜天等）分计，"
                       f"通名对只说明次序相合，不作人名认定。④参长：相邻标记间净字数。"
                       f"⑤链式对齐：取 {CHAIN_N}-gram 在对方**恰出现一次**者为候选，"
                       f"以两侧位置同增求最长链（LIS），再按相邻链点分段线性插值定位；"
                       f"链覆盖范围外不推位置（记无链），插值只给位置、不给语义。"
                       f"⑥收束语族：辭退／辭去／而退／「遶（繞、匝）…而去」四种收束语，"
                       f"重叠取先出现者；另记标记前 {SHUCAI_WIN} 字内有无「善財」，"
                       f"无语者即非善財参访（如开初会众散退）。"),
            "sources": {},
        },
        "texts": {},
        "marks_detail": {},
        "pivot": {},
        "reverse": {},
        "name_pairs": {},
        "lengths": {},
        "examples": [],
        "summary": {},
    }
    for k, d in docs.items():
        result["meta"]["sources"][k] = {
            "path": str(d.path.relative_to(ROOT)).replace("\\", "/"),
            "sha256": sha256(d.path.read_bytes()),
        }
        result["texts"][k] = dict(scopes[k], marks=len(marks[k]))

    # --- 标记明细：分类（参末/会众散）、同名对象、参长 ---
    for k, d in docs.items():
        rows, prev = [], scopes[k]["start"]
        for p in marks[k]:
            pre = clean_ctx(d, p, SHUCAI_WIN)
            name, _ = extract_name(d, p)
            rows.append({
                "lb": d.lb_at(d.raw_index(p)),
                "kind": "参末" if "善財" in pre else "会众散",
                "name": name,
                "generic": (name in GENERIC) if name else None,
                "visit_chars": sum(1 for i in range(prev, p)
                                   if d.norm[i:i + 1].strip()),
            })
            prev = p
        result["marks_detail"][k] = rows
        result["lengths"][k] = [r["visit_chars"] for r in rows]

    def ctx(doc: Doc, pos: int) -> str:
        return clean_ctx(doc, pos, CTX)

    # --- ② 以八十本为轴，映到六十、四十（字面锚，唯一出现才可锚） ---
    pivot = {}
    for other in ("T278", "T293"):
        rows = []
        for idx, p in enumerate(marks["T279"]):
            hit = anchor_to(docs["T279"], p, docs[other])
            if hit is None:
                rows.append({"lb": docs["T279"].lb_at(docs["T279"].raw_index(p)),
                             "mapped_lb": None, "dist": None, "cls": "无锚",
                             "anchor": 0, "ctx": ctx(docs["T279"], p)})
                continue
            if hit[0] == "multi":
                rows.append({"lb": docs["T279"].lb_at(docs["T279"].raw_index(p)),
                             "mapped_lb": None, "dist": None, "cls": "复见",
                             "anchor": 0, "occurrences": hit[1],
                             "ctx": ctx(docs["T279"], p)})
                continue
            q, n = hit
            near = min(marks[other], key=lambda x: abs(x - q))
            dist = abs(near - q)
            rows.append({
                "lb": docs["T279"].lb_at(docs["T279"].raw_index(p)),
                "mapped_lb": docs[other].lb_at(docs[other].raw_index(near)),
                "dist": dist,
                "cls": classify(dist),
                "anchor": n,
                "ctx": ctx(docs["T279"], p),
            })
        pivot[other] = rows
    result["pivot"] = pivot

    # --- 反向：四十本的标记映回八十本（无锚≠独有，只报锚定子集） ---
    rev = []
    for p in marks["T293"]:
        hit = anchor_to(docs["T293"], p, docs["T279"])
        if hit is None:
            rev.append({"lb": docs["T293"].lb_at(docs["T293"].raw_index(p)),
                        "mapped_lb": None, "dist": None, "cls": "无锚",
                        "anchor": 0, "ctx": ctx(docs["T293"], p)})
            continue
        if hit[0] == "multi":
            rev.append({"lb": docs["T293"].lb_at(docs["T293"].raw_index(p)),
                        "mapped_lb": None, "dist": None, "cls": "复见",
                        "anchor": 0, "occurrences": hit[1],
                        "ctx": ctx(docs["T293"], p)})
            continue
        q, n = hit
        near = min(marks["T279"], key=lambda x: abs(x - q))
        dist = abs(near - q)
        rev.append({
            "lb": docs["T293"].lb_at(docs["T293"].raw_index(p)),
            "mapped_lb": docs["T279"].lb_at(docs["T279"].raw_index(near)),
            "dist": dist,
            "cls": classify(dist),
            "anchor": n,
            "ctx": ctx(docs["T293"], p),
        })
    result["reverse"] = rev

    # --- ③ 同名锚：八十↔六十、八十↔四十（单调配对） ---
    seq = {k: [r["name"] for r in result["marks_detail"][k]] for k in FILES}
    for other in ("T278", "T293"):
        pairs = pair_by_name(seq["T279"], seq[other], GENERIC)
        for pr in pairs:
            pr["a_lb"] = result["marks_detail"]["T279"][pr["a_index"]]["lb"]
            pr["b_lb"] = result["marks_detail"][other][pr["b_index"]]["lb"]
            pr.pop("a_index"), pr.pop("b_index")
        result["name_pairs"][other] = pairs

    def tally(rows: list[dict]) -> dict:
        out = {}
        for r in rows:
            out[r["cls"]] = out.get(r["cls"], 0) + 1
        return out

    def med(xs: list[int]) -> int:
        xs = sorted(xs)
        return xs[len(xs) // 2]

    # --- ④ 链式对齐：8-gram 唯一锚 → LIS 单调链 → 分段线性插值 ---
    chain = {}
    qmap = {}
    for name, sk, dk in (("to_60", "T279", "T278"), ("to_40", "T279", "T293"),
                         ("rev_40_80", "T293", "T279")):
        src, dst = docs[sk], docs[dk]
        ch = chain_of(src, dst, CHAIN_N)
        xs, ys = [c[0] for c in ch], [c[1] for c in ch]
        rows = []
        qmap[name] = {}
        for p in marks[sk]:
            q = map_pos(xs, ys, p, len(dst.norm))
            base = {"lb": src.lb_at(src.raw_index(p)), "ctx": ctx(src, p),
                    "mark_ctx": slice_at(src, p)}
            if q is None:
                rows.append(dict(base, mapped_lb=None, dist=None, cls="无链"))
                continue
            qmap[name][base["lb"]] = q
            near = min(marks[dk], key=lambda x: abs(x - q))
            dist = abs(near - q)
            rows.append(dict(base, mapped_lb=dst.lb_at(dst.raw_index(near)),
                             mapped_at=dst.lb_at(dst.raw_index(q)),
                             dist=dist, cls=classify(dist)))
        ds = [r["dist"] for r in rows if r["dist"] is not None]
        chain[name] = {"from": sk, "to": dk, "n": CHAIN_N, "anchors": len(ch),
                       "rows": rows, "tally": tally(rows),
                       "median": med(ds) if ds else None,
                       "max": max(ds) if ds else None}
    result["chain"] = chain

    # --- ⑤ 收束语族：辭退／辭去／而退／匝…而去（窄义；逐处记类） ---
    fam = {}
    for k, d in docs.items():
        fm = family_marks(d, scopes[k]["start"], scopes[k]["end"])
        kinds_f, before, not_before = {}, 0, []
        for p, kind in fm:
            kinds_f[kind] = kinds_f.get(kind, 0) + 1
            if "善財" in clean_ctx(d, p, SHUCAI_WIN):
                before += 1
            else:
                not_before.append(d.lb_at(d.raw_index(p)))
        fam[k] = {"total": len(fm), "kinds": kinds_f,
                  "before_shancai": before, "not_before_lb": not_before}
    result["family"] = fam

    # --- ⑥ 离群点举例：链定位处的收束语用词不同（位置由链给，引文按位置截取） ---
    def phrase_near(doc: Doc, pos: int, phrase: str, win: int = 200) -> int:
        a, b = max(0, pos - win), min(len(doc.norm), pos + win)
        idx = [m.start() for m in re.finditer(re.escape(phrase), doc.norm[a:b])]
        if not idx:
            raise SystemExit(f"outlier phrase not found near {pos}: {phrase}")
        return a + min(idx, key=lambda x: abs(a + x - pos))

    out_cases = (
        ("to_60", "0369a14", "辭詣彼城", "八十「辭退而去」／六十「辭詣彼城」"),
        ("to_60", "0417c25", "戀仰辭去", "八十「辭退而去」／六十「戀仰辭去」"),
        ("to_40", "0335a03", "戀慕而去", "八十「辭退而去」／四十「戀慕而去」"),
        ("rev_40_80", "0807a17", "戀仰辭去", "四十「辭退而去」／八十「戀仰辭去」"),
        ("rev_40_80", "0809a17", "戀仰而去", "四十「辭退而去」／八十「戀仰而去」"),
    )
    outs = []
    for name, lb, phrase, why in out_cases:
        v = chain[name]
        row = next((r for r in v["rows"] if r["lb"] == lb), None)
        if row is None or row.get("cls") == "同一处":
            raise SystemExit(f"outlier case lost: {name} {lb}")
        dst = docs[v["to"]]
        tp = phrase_near(dst, qmap[name][lb], phrase)
        outs.append({"dir": name, "lb": lb, "cls": row["cls"],
                     "dist": row["dist"],
                     "a": {"key": v["from"], "lb": lb, "text": row["mark_ctx"]},
                     "b": {"key": v["to"], "lb": dst.lb_at(dst.raw_index(tp)),
                           "text": slice_at(dst, tp, 14, 6)},
                     "why": why})
    result["chain_outliers"] = outs
    result["chain_gap"] = {
        name: [{"lb": r["lb"], "mapped_lb": r["mapped_lb"], "dist": r["dist"]}
               for r in v["rows"] if r["cls"] in ("漂移", "邻近")]
        for name, v in chain.items()}

    p60, p40 = pivot["T278"], pivot["T293"]
    kinds = {k: {kk: sum(1 for r in result["marks_detail"][k]
                         if r["kind"] == kk) for kk in ("参末", "会众散")}
             for k in FILES}
    np60, np40 = result["name_pairs"]["T278"], result["name_pairs"]["T293"]
    result["summary"] = {
        "marks": {k: len(v) for k, v in marks.items()},
        "kinds": kinds,
        "pivot_to_60": tally(p60),
        "pivot_to_40": tally(p40),
        "reverse_40_to_80": tally(rev),
        "reverse_40_unanchored": sum(1 for r in rev if r["cls"] in ("漂移", "无锚")),
        "median_dist_60": sorted(r["dist"] for r in p60 if r["dist"] is not None)[
            len([r for r in p60 if r["dist"] is not None]) // 2] if any(
            r["dist"] is not None for r in p60) else None,
        "median_dist_40": sorted(r["dist"] for r in p40 if r["dist"] is not None)[
            len([r for r in p40 if r["dist"] is not None]) // 2] if any(
            r["dist"] is not None for r in p40) else None,
        "name_pairs_60": {"proper": sum(1 for p in np60 if not p["generic"]),
                          "generic": sum(1 for p in np60 if p["generic"])},
        "name_pairs_40": {"proper": sum(1 for p in np40 if not p["generic"]),
                          "generic": sum(1 for p in np40 if p["generic"])},
        "median_visit_chars": {k: med(v) for k, v in result["lengths"].items()},
        "max_visit": {k: {"chars": max(v), "lb": result["marks_detail"][k][v.index(max(v))]["lb"]}
                      for k, v in result["lengths"].items()},
        "chain": {k: {"tally": v["tally"], "median": v["median"], "max": v["max"],
                      "anchors": v["anchors"]} for k, v in chain.items()},
        "chain_median": {k: v["median"] for k, v in chain.items()},
        "chain_anchors": {k: v["anchors"] for k, v in chain.items()},
        "family": {k: v["total"] for k, v in fam.items()},
        "family_kinds": {k: v["kinds"] for k, v in fam.items()},
        "family_before_shancai": {k: v["before_shancai"] for k, v in fam.items()},
    }

    # --- 示例：各分类各取两条（同一处／邻近／漂移／无锚），带两侧行号 ---
    picks = []
    for label, rows in (("T278", p60), ("T293", p40)):
        for cls in ("同一处", "邻近", "漂移", "复见", "无锚"):
            for r in [x for x in rows if x["cls"] == cls][:2]:
                picks.append({"to": label, "cls": cls, **r})
    result["examples"] = picks

    # --- 名异实例：海雲（同名锚）之后一参，八十／六十作「善住」，四十作「妙住」；梵本旁证 ---
    gv_path = ROOT / "data" / "references" / "sanskrit" / "gandavyuha_vaidya.txt"
    result["variant_example"] = {
        "note": ("海雲参（同名锚 T279 0336b11 ↔ T293 0682b18）之后的下一参，"
                 "八十本指示句作「善住」、六十本参末套语作「善住比丘」，"
                 "四十本参末套语作「妙住」——是否同实，梵本可旁证："
                 "Gaṇḍavyūha 海雲（Sāgaramegha）之后一参作 Supratiṣṭhita 比丘，"
                 "且「于虚空中经行」情节与八十本〈善住比丘〉章相合；"
                 "supra- 兼有善／妙二义，'善住'与'妙住'为同一梵名之两译"
                 "〔本文判断，梵本一手旁证〕。"),
        "quotes": [
            {"key": "T279", "lb": "0336b11", "text": "名曰：善住"},
            {"key": "T278", "lb": "0692c12", "text": "禮善住比丘足"},
            {"key": "T293", "lb": "0684a06", "text": "禮妙住足"},
            {"key": "T279", "lb": "0336b11", "text": "禮海雲足"},
            {"key": "T293", "lb": "0682b18", "text": "禮海雲足"},
        ],
        "sanskrit": {
            "source": "data/references/sanskrit/gandavyuha_vaidya.txt",
            "sha256": sha256(gv_path.read_bytes()),
            "quotes": [
                {"text": "sāgarameghasya bhikṣorantikāt prakrāntaḥ",
                 "zh": "善财自海雲（Sāgaramegha）比丘所去"},
                {"text": "so 'paśyatsupratiṣṭhitaṃ bhikṣuṃ gaganatale caṃkramyamāṇam",
                 "zh": "见 Supratiṣṭhita（善住）比丘于虚空中经行"},
            ],
        },
    }

    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    s = result["summary"]
    print(f"marks {s['marks']}  kinds {s['kinds']}")
    print(f"→60 {s['pivot_to_60']} (med {s['median_dist_60']})  "
          f"→40 {s['pivot_to_40']} (med {s['median_dist_40']})  "
          f"40↔80 {s['reverse_40_to_80']} unanchored {s['reverse_40_unanchored']}")
    print(f"name pairs 60 {s['name_pairs_60']}  40 {s['name_pairs_40']}")
    print(f"chain {[(k, v['tally'], v['median'], v['anchors']) for k, v in s['chain'].items()]}")
    print(f"family {s['family']} kinds {s['family_kinds']} "
          f"before_shancai {s['family_before_shancai']}")
    print(f"median visit chars {s['median_visit_chars']}")
    print("written", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
