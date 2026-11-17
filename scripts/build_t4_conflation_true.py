#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""T4 真拼合实例：《合部金光明經》（T16n0664，隋寶貴合）品级多源合成探针。

库内第一个「真拼合」实例：寶貴开皇十七年（597）以曇無讖四卷本（T16n0663）为基，
取闍那崛多五卷本补阙、真諦四品增新，合为八卷二十四品。拼合单位＝品——
比《合論》的逐段嵌入粗、比「两经各取半部」的卷级拼合细：T4 算子的第三种粒度。

证据三层（分层标注，不混层）：
  A 正文层：卷头／品题下的译者 byline（CBETA 结构化元素，`byline cb:type="Translator"`）
    ＋序自述（「并前先出合二十四品」）。品级 provenance 规则：有 byline＝本品来源；
    无 byline＝继承当前卷卷头译者（卷头重置基准）。
  B 校本层：随文注「下崛多譯補」「自下五行丹本無」（所承校本之注，标 splice 点）
    ——传统自身对拼合的标记，非隋正文。
  C 计量层：以曇無讖本（T16n0663）为参照，逐品 10-gram 重合率（argmax 落点到 663 品）
    ——讖本品应高、真諦品应≈0；壽量品按校本注 splice 点切分前后段分计。

解析：直接在 XML 结构层取 `<cb:juan fun="open">`／`<cb:div type="pin">`／byline，
不经 clean 空间正则，页眉噪声天然隔离。

Usage: python scripts/build_t4_conflation_true.py
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
OUT = ROOT / "data" / "research" / "t4_conflation_true.json"
TMP = ROOT / ".tmp" / "t4_conflation"

N = 10          # 重合率 n-gram
CN = "一二三四五六七八九十"
CN2 = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5,
       "六": 6, "七": 7, "八": 8, "九": 9, "十": 10}

JUAN_RE = re.compile(r'<cb:juan n="(\d+)" fun="open">')
PIN_RE = re.compile(r'<cb:div type="pin">')
BY_RE = re.compile(r'<byline cb:type="Translator">(.*?)</byline>', re.S)
MULU_RE = re.compile(r'<cb:mulu[^>]*>([^<]*)</cb:mulu>')


def cn2int(s: str) -> int:
    if "十" not in s:
        return CN2.get(s, 0)
    a, _, b = s.partition("十")
    return CN2.get(a, 1) * 10 + CN2.get(b, 0)


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def clean_doc(path: Path, name: str) -> tuple[Doc, str, list[tuple[int, str]]]:
    """Doc from note-stripped XML；返回 (Doc, stripped_raw, 原raw随文注清单)。
    解析坐标一律用 stripped_raw（与 Doc/inv 同系）；随文注 lb 回源用原 raw。"""
    raw = path.read_text(encoding="utf-8")
    notes = [(m.start(), m.group(1)) for m in
             re.finditer(r'<note place="inline">([^<]{2,20})</note>', raw)]
    stripped = re.sub(r'<note place="inline">[^<]{2,20}</note>', "", raw)
    TMP.mkdir(parents=True, exist_ok=True)
    tmpf = TMP / path.name
    tmpf.write_text(stripped, encoding="utf-8")
    return Doc(name, tmpf), stripped, notes


def norm_of_clean(doc: Doc) -> list[int]:
    """clean 索引 → norm 索引。"""
    inv = [-1] * (len(doc.clean) + 1)
    j = 0
    for i, c in enumerate(doc.clean_of_norm):
        while j <= c:
            inv[j] = i - 1 if j < c else i
            j += 1
    while j < len(inv):
        inv[j] = len(doc.norm) - 1
        j += 1
    return inv


def raw2norm(doc: Doc, inv: list[int], r: int) -> int:
    ci = bisect.bisect_right(doc.raw_of_clean, r) - 1
    if ci < 0:
        return 0
    return max(0, inv[min(ci, len(inv) - 1)])


def byline_text(seg: str) -> str | None:
    m = BY_RE.search(seg)
    if not m:
        return None
    return re.sub(r"\s+", "", re.sub(r"<[^>]+>", "", m.group(1))) or None


def norm_src(tr_raw: str | None) -> str:
    if not tr_raw:
        return "?"
    if "曇無讖" in tr_raw:
        return "曇無讖"
    if "真諦" in tr_raw:
        return "真諦"
    if "崛多" in tr_raw:
        return "崛多"
    return "?"


def parse_structure(doc: Doc, raw: str, inv: list[int]) -> tuple[list[dict], list[dict]]:
    """事件流解析：juan open（基准重置）与 pin div（本体）。"""
    events = []
    for m in JUAN_RE.finditer(raw):
        events.append((m.start(), "juan", int(m.group(1))))
    for m in PIN_RE.finditer(raw):
        events.append((m.start(), "pin", len(events)))
    events.sort(key=lambda x: x[0])

    juans, pins = [], []
    base = None
    for idx, (pos, kind, num) in enumerate(events):
        nxt = events[idx + 1][0] if idx + 1 < len(events) else len(raw)
        seg_head = raw[pos:pos + 1600]
        if kind == "juan":
            b = byline_text(seg_head)
            if b:
                base = b
            mulu = MULU_RE.search(seg_head)
            juans.append({"n": num, "raw": pos, "byline": b, "base": base,
                          "mulu": mulu.group(1) if mulu else "?"})
        else:
            # head 区：div 起到首个内容段（<p/<lg）；byline 位于 head 与内容段之间
            pm = re.search(r"<(?:p|lg)\b", raw[pos:pos + 3000])
            head = raw[pos:pos + (pm.start() if pm else 1200)]
            own = byline_text(head)
            mulu = MULU_RE.search(head)
            pins.append({"raw": pos, "raw_end": nxt, "own": own,
                         "byline": own or base,
                         "mulu": mulu.group(1) if mulu else "?"})
    # 品号与 body 边界（norm；body 从首个内容段起，排除 mulu/head/byline）
    for i, p in enumerate(pins):
        mulu = p["mulu"]
        mm = re.match(r"\s*(\d+)\s*([一-龥]+品)", mulu)
        p["no"] = int(mm.group(1)) if mm else i + 1
        p["title"] = mm.group(2) if mm else mulu
        pm = re.search(r"<(?:p|lg)\b", raw[p["raw"]:p["raw"] + 3000])
        body_raw0 = p["raw"] + (pm.start() if pm else 0)
        n0 = raw2norm(doc, inv, body_raw0)
        nxt_pin = pins[i + 1]["raw"] if i + 1 < len(pins) else len(raw)
        nxt_juan = min((j["raw"] for j in juans if j["raw"] > p["raw"]),
                       default=len(raw))
        n1 = raw2norm(doc, inv, min(nxt_pin, nxt_juan))
        p["n_body0"], p["n_body1"] = n0, max(n0, n1)
    return juans, pins


def main() -> int:
    d664, raw664, notes664 = clean_doc(
        ROOT / "data/references/cbeta/T16n0664.xml", "T16n0664")
    d663, raw663, _ = clean_doc(
        ROOT / "data/references/cbeta/T16n0663.xml", "T16n0663")
    inv4 = norm_of_clean(d664)
    inv3 = norm_of_clean(d663)
    juans4, pins4 = parse_structure(d664, raw664, inv4)
    juans3, pins3 = parse_structure(d663, raw663, inv3)
    print(f"0664：卷 {len(juans4)} 品 {len(pins4)}；0663：卷 {len(juans3)} 品 {len(pins3)}")
    for j in juans4:
        print(f"  卷{j['n']} 基准[{norm_src(j['base'])}] byline={j['byline']}")

    ref = set(d663.norm[i:i + N] for i in range(len(d663.norm) - N + 1))
    spans3 = [(p["no"], p["title"], p["n_body0"], p["n_body1"]) for p in pins3]

    def argmax_landing(body: str) -> tuple[str | None, float]:
        grams = [body[i:i + N] for i in range(len(body) - N + 1)]
        if not grams:
            return None, 0.0
        best, best_cov = None, 0.0
        for no, title, s, e in spans3:
            sub = set(d663.norm[i:i + N] for i in range(s, max(s, e - N + 1)))
            hits = sum(1 for g in grams if g in sub)
            cov = hits / len(grams)
            if cov > best_cov:
                best, best_cov = f"{no} {title}", cov
        return best, best_cov

    rows = []
    for p in pins4:
        body = d664.norm[p["n_body0"]:p["n_body1"]]
        g = [body[i:i + N] for i in range(len(body) - N + 1)]
        cov = (sum(1 for x in g if x in ref) / len(g)) if g else 0.0
        where, pin_cov = argmax_landing(body)
        rows.append({
            "no": p["no"], "title": p["title"],
            "src": norm_src(p["byline"]), "byline": p["byline"],
            "own_byline": p["own"] is not None,
            "chars": len(body), "cov": round(cov, 4),
            "argmax_pin": where, "argmax_cov": round(pin_cov, 4),
        })

    # B 层：校本随文注（splice 标记），lb 回源
    marks = []
    for raw_pos, text in notes664:
        if text in ("下崛多譯補", "自下五行丹本無") or text.endswith("譯補"):
            lb = "?"
            for lbm in re.finditer(r'<lb n="([0-9a-z]+)"', raw664[:raw_pos]):
                lb = lbm.group(1)
            marks.append({"lb": lb, "text": text})

    # A 层序文引文（norm 锚 → clean 切片）
    def slice_norm(doc: Doc, a: str, b: str) -> dict:
        i = doc.norm.find(a)
        j = doc.norm.find(b, i if i >= 0 else 0)
        if i < 0 or j < 0:
            return {"ok": False}
        c0 = doc.clean_of_norm[i]
        c1 = doc.clean_of_norm[min(j + len(b), len(doc.norm) - 1)]
        return {"ok": True, "lb": doc.lb_at(doc.raw_index(i)),
                "text": doc.clean[c0:c1 + len(b)].replace("\n", "")}

    preface = slice_norm(d664, "而金光明見有三本", "并前先出合二十四品")

    # 品2 壽量品 splice 切分（校本注 0360c21「下崛多譯補」）
    sp = {"ok": False}
    anchor = d664.norm.find("時四如來忽然不現")
    pin2 = next((p for p in pins4 if p["no"] == 2), None)
    if pin2 and anchor >= 0:
        pre = d664.norm[pin2["n_body0"]:anchor + 9]
        post = d664.norm[anchor + 9:pin2["n_body1"]]
        gp = [pre[i:i + N] for i in range(len(pre) - N + 1)]
        gq = [post[i:i + N] for i in range(len(post) - N + 1)]
        sp = {"ok": True,
              "anchor_lb": d664.lb_at(d664.raw_index(anchor)),
              "pre_chars": len(pre), "post_chars": len(post),
              "pre_cov": round(sum(1 for x in gp if x in ref) / len(gp), 4) if gp else None,
              "post_cov": round(sum(1 for x in gq if x in ref) / len(gq), 4) if gq else None}

    by_src: dict[str, list[float]] = {}
    for r in rows:
        by_src.setdefault(r["src"], []).append(r["cov"])
    med = lambda v: sorted(v)[len(v) // 2] if v else None  # noqa: E731
    stats = {
        "pins664": len(rows), "pins663": len(pins3), "juans664": len(juans4),
        "by_src_counts": {k: len(v) for k, v in by_src.items()},
        "cov_median": {k: round(med(v), 4) for k, v in by_src.items()},
        "cov_min_di": min((r["cov"] for r in rows if r["src"] == "曇無讖"), default=None),
        "cov_max_zhendi": max((r["cov"] for r in rows if r["src"] == "真諦"), default=None),
        "splice_marks": len(marks),
        "preface_lb": preface.get("lb"),
    }
    data = {
        "meta": {
            "date": date.today().isoformat(),
            "title": "T4 真拼合实例：《合部金光明經》品级多源合成",
            "method": ("A 正文层＝卷头/品题译者 byline（CBETA 结构化元素；无 byline 品继承"
                       "当前卷卷头基准，卷头重置）＋序自述；B 校本层＝随文注 splice 标记"
                       f"（传统自身的拼合标记，非隋正文）；C 计量层＝逐品 {N}-gram 重合率"
                       "（对曇無讖本 T16n0663，argmax 落点）。三层分标，不互证混用。"
                       "壽量品按校本注 splice 点切分前后段分计。"),
            "n": N,
            "sources": {
                "t663": {"path": "data/references/cbeta/T16n0663.xml",
                         "sha256": sha256((ROOT / "data/references/cbeta/T16n0663.xml").read_bytes()),
                         "bytes": (ROOT / "data/references/cbeta/T16n0663.xml").stat().st_size},
                "t664": {"path": "data/references/cbeta/T16n0664.xml",
                         "sha256": sha256((ROOT / "data/references/cbeta/T16n0664.xml").read_bytes()),
                         "bytes": (ROOT / "data/references/cbeta/T16n0664.xml").stat().st_size},
            },
        },
        "juan_bases": [{"juan": j["n"], "base": norm_src(j["base"]),
                        "byline": j["byline"]} for j in juans4],
        "preface_quote": preface,
        "splice_split_pin2": sp,
        "splice_marks": marks,
        "pins": rows,
        "stats": stats,
    }
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n",
                   encoding="utf-8")
    print("序引文:", json.dumps(preface, ensure_ascii=False)[:200])
    print("品2切分:", json.dumps(sp, ensure_ascii=False))
    print("校本注:", marks)
    print("stats:", json.dumps(stats, ensure_ascii=False))
    for r in rows:
        print(f"  品{r['no']:>2} {r['title']:<10} [{r['src']}]"
              f"{'(own)' if r['own_byline'] else '     '} "
              f"cov={r['cov']:.3f} chars={r['chars']:>6} "
              f"argmax={r['argmax_pin']}@{r['argmax_cov']:.3f}")
    print("written", OUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
