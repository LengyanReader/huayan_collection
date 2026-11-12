#!/usr/bin/env python3
"""Build the T4 probe: is any text in this corpus a conflation (合本) of two books?

T4 asks a narrow question: can the candidate be cut into two (or more) blocks,
each of which reproduces a *different* source closely enough that the seam is
visible? "Looks long" is not evidence; "cannot be separated" is the answer we
expect everywhere except a real compilation.

Three parts, each with a job:

  1. 筛查 — every 華嚴部 text in the catalog is measured whole against the two
     complete Chinese translations (T278 六十, T279 八十). A conflation must at
     least be *close* to one of its sources, so a near-zero number retires a
     candidate without any further work.
  2. 分块切分 — for candidates large enough to cut (>= 20k chars), split into
     1,000-character blocks, score each block's 12-gram coverage against both
     sources, and search every split point. A candidate passes only if
       (a) both sides hold >= 20% of the text,
       (b) each side reaches >= 30% coverage against its own source,
       (c) the pairing beats the crossed pairing by >= 15 points.
     Condition (b) is calibrated on a *planted* conflation, not on taste: 30%
     is where copying lives, and no translation in this corpus reaches it.
  3. 对照 — a planted positive (T279 前半 + T278 后半) proves the detector can
     see a seam; two 注疏 negatives (T1735 vs 經, T1736 vs 疏) show what the
     real library looks like when someone *does* bind two books together.

Usage:
  python scripts/build_conflation_probe.py
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import date
from itertools import groupby
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_implicit_quotes import Doc  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
CBETA = ROOT / "data" / "references" / "cbeta"
CATALOG = ROOT / "data" / "research" / "dazang_mapping_verification.json"
OUT = ROOT / "data" / "research" / "conflation_probe.json"

GRAM = 12
BLOCK = 1000
MIN_BLOCK = 200
TIER2_MIN_CHARS = 20000
MIN_SIDE_SHARE = 0.20
SIDE_COVERAGE = 0.30
SEPARATION = 0.15
HEAD = 40

FILES = {
    "T278": "T09n0278.xml",
    "T279": "T10n0279.xml",
    "T293": "T10n0293.xml",
    "T297": "T10n0297.xml",
    "T300": "T10n0300.xml",
    "T302": "T10n0302.xml",
    "T1735": "T35n1735.xml",
    "T1736": "T36n1736.xml",
    "T1739": "T36n1739.xml",
}
for n in range(280, 310):
    FILES[f"T{n}"] = f"T10n{n:04d}.xml"

# 卍續藏庫外檔（§17.8 入庫，路徑不同）
XFILES = {
    "X223": "data/references/cbeta_x/X04n0223.xml",
    "X240a": "data/references/cbeta_x/X08n0240.xml",
    "X240b": "data/references/cbeta_x/X09n0240.xml",
}

# 两个注疏候选＝负控：若「经疏合刊／疏钞合刊」真的存在，它们最像。
# X223＝库外第一试金石：志寧「釐經合論」——经文被逐段厘入李通玄论。
# X240a/b＝第二实例：德清《綱要》——经文与疏义是否逐段合编。
PARTITION_EXTRA = [
    ("T1735", ["T279", "T278"], "經疏合刊：疏文里是否整段插入經文"),
    ("T1736", ["T1735", "T279"], "疏钞合刊：钞文里是否整段重刊疏文"),
    ("X223", ["T279", "T1739"], "经论合编：志寧釐經入論，是逐段嵌入还是两段拼合"),
    ("X240a", ["T279", "T1735"], "经疏合编：德清綱要 卷1–44，经文与疏义是否逐段合编"),
    ("X240b", ["T279", "T1735"], "经疏合编：德清綱要 卷45–80，经文与疏义是否逐段合编"),
]
EXTRA_TITLES = {
    "T1735": "大方廣佛華嚴經疏",
    "T1736": "大方廣佛華嚴經隨疏演義鈔",
    "X223": "華嚴經合論（李通玄造論・志寧釐經合論）",
    "X240a": "華嚴綱要 卷1–44（澄觀疏義・德清提挈）",
    "X240b": "華嚴綱要 卷45–80（澄觀疏義・德清提挈）",
}
TARGETED = [
    ("T293", "T297", "四十華嚴卷40（普賢行願品）是否取自《普賢菩薩行願讚》"),
]
BASELINES = [
    ("T295", "T278", "逐字重合：一卷《入法界品》↔ 六十華嚴"),
    ("T286", "T278", "近文：〈十地品〉異譯《十住經》↔ 六十華嚴"),
    ("T293", "T279", "近文：四十華嚴 ↔ 八十〈入法界品〉"),
    ("T287", "T279", "近文：《十地經》↔ 八十〈十地品〉"),
    ("T279", "T278", "同本異譯：八十 ↔ 六十（全本）"),
    ("T1736", "T1735", "疏—鈔：隨疏演義鈔 ↔ 疏"),
    ("T1735", "T279", "經—疏：澄觀疏 ↔ 八十華嚴"),
    ("T309", "T279", "無關文本：《十住除垢斷結經》↔ 八十華嚴"),
]


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def short_id(taisho: str) -> str:
    """T10n0280 → T280；T35n1735 → T1735。"""
    m = re.match(r"T\d+n0*(\d+)", taisho)
    return f"T{m.group(1)}" if m else taisho


def grams(s: str, n: int = GRAM) -> set[str]:
    return {s[i:i + n] for i in range(len(s) - n + 1)}


def coverage(a: str, gb: set[str]) -> float:
    ga = grams(a)
    return len(ga & gb) / len(ga) if ga else 0.0


def blocks_of(s: str) -> list[tuple[int, str]]:
    out = []
    for i in range(0, len(s), BLOCK):
        b = s[i:i + BLOCK]
        if len(b) >= MIN_BLOCK:
            out.append((i, b))
    return out


def profile(s: str, src: dict[str, set[str]]) -> list[dict]:
    rows = []
    for i, b in blocks_of(s):
        g = grams(b)
        rows.append({
            "start": i,
            "chars": len(b),
            "cov": {k: (len(g & v) / len(g) if g else 0.0) for k, v in src.items()},
        })
    return rows


def best_split(rows: list[dict], s1: str, s2: str) -> dict:
    total = sum(r["chars"] for r in rows)
    best = {"split_block": None, "split_char": None, "left_share": 0.0,
            "left": {s1: 0.0, s2: 0.0}, "right": {s1: 0.0, s2: 0.0},
            "min_side": 0.0, "separation": 0.0, "pass": False}
    if len(rows) < 3 or total == 0:
        return best
    for k in range(1, len(rows)):
        lc = sum(r["chars"] for r in rows[:k])
        rc = total - lc
        if lc < MIN_SIDE_SHARE * total or rc < MIN_SIDE_SHARE * total:
            continue
        left = {s: sum(r["chars"] * r["cov"][s] for r in rows[:k]) / lc for s in (s1, s2)}
        right = {s: sum(r["chars"] * r["cov"][s] for r in rows[k:]) / rc for s in (s1, s2)}
        m = min(left[s1], right[s2])
        sep = m - max(left[s2], right[s1])
        if m > best["min_side"] or (m == best["min_side"] and sep > best["separation"]):
            best = {
                "split_block": k, "split_char": rows[k]["start"],
                "left_share": round(lc / total, 3),
                "left": {s1: round(left[s1], 4), s2: round(left[s2], 4)},
                "right": {s1: round(right[s1], 4), s2: round(right[s2], 4)},
                "min_side": round(m, 4), "separation": round(sep, 4),
                "pass": False,
            }
    best["pass"] = bool(best["min_side"] >= SIDE_COVERAGE and best["separation"] >= SEPARATION)
    return best


def block_stats(rows: list[dict], src: list[str]) -> dict:
    out = {}
    for s in src:
        vals = sorted(r["cov"][s] for r in rows)
        out[s] = {
            "median": round(vals[len(vals) // 2], 4) if vals else 0.0,
            "max": round(vals[-1], 4) if vals else 0.0,
            "blocks_ge_30": sum(1 for v in vals if v >= SIDE_COVERAGE),
        }
    return out


def verified_head(doc: Doc, start: int, block: str, src_norm: str) -> tuple[int, str] | None:
    """在块内找一段确实同见于两本的连续文字（40／32／24 字逐级降），返回 (偏移, clean 起首)。"""
    for length in (HEAD, 32, 24):
        if len(block) <= length:
            continue
        for j in range(0, len(block) - length + 1):
            if block[j:j + length] in src_norm:
                ci = doc.clean_of_norm[start + j]
                raw = doc.clean[ci:ci + length].replace("\n", "")
                return start + j, raw
    return None


def best_block(doc: Doc, rows: list[dict], s1: str, s2: str,
               src_doc: dict[str, Doc]) -> dict | None:
    if len(rows) < 2:
        return None
    # 首块含经题／译者，会虚高，不计入示例
    body = rows[1:]
    s = s1 if max(r["cov"][s1] for r in body) >= max(r["cov"][s2] for r in body) else s2
    top = max(body, key=lambda r: r["cov"][s])
    if top["cov"][s] < 0.05:
        return None
    block = doc.norm[top["start"]:top["start"] + top["chars"]]
    hit = verified_head(doc, top["start"], block, src_doc[s].norm)
    if hit is None:
        return None
    pos, head = hit
    return {
        "source": s,
        "lb": doc.lb_at(doc.raw_index(pos)),
        "chars": top["chars"],
        "coverage": round(top["cov"][s], 4),
        "head": head,
    }


def main() -> int:
    cat = json.loads(CATALOG.read_text(encoding="utf-8"))
    meta = {short_id(r["taisho"]): r for r in cat["catalog_32"]}

    docs: dict[str, Doc] = {}
    gsets: dict[str, set[str]] = {}

    def doc_of(k: str) -> Doc:
        if k not in docs:
            p = (ROOT / XFILES[k]) if k in XFILES else (CBETA / FILES[k])
            docs[k] = Doc(k, p)
        return docs[k]

    def gs_of(k: str) -> set[str]:
        if k not in gsets:
            gsets[k] = grams(doc_of(k).norm)
        return gsets[k]

    result = {
        "meta": {
            "date": date.today().isoformat(),
            "gram": GRAM,
            "block_chars": BLOCK,
            "min_block": MIN_BLOCK,
            "tier2_min_chars": TIER2_MIN_CHARS,
            "thresholds": {
                "min_side_share": MIN_SIDE_SHARE,
                "side_coverage": SIDE_COVERAGE,
                "separation": SEPARATION,
            },
            "method": (
                f"①筛查：全文去标点后取不同 {GRAM} 字串，量其见于 T278／T279 的比例；"
                f"②分块切分：按 {BLOCK} 字切块（末块≥{MIN_BLOCK} 字才计），逐块量两源覆盖率，"
                f"遍历切分点，要求两侧各≥{MIN_SIDE_SHARE:.0%}篇幅、各自达 {SIDE_COVERAGE:.0%}、"
                f"交叉配对低 {SEPARATION:.0%} 以上；③对照：植入正控（T279 前半＋T278 后半）"
                f"与两个注疏负控（T1735/T1736）。"
            ),
            "sources": {},
        },
        "controls": {"positive": {}, "negative": []},
        "screen": [],
        "partition": [],
        "baselines": [],
        "targeted": [],
        "verdict": {},
    }

    needed = ["T278", "T279", "T293", "T297", "T300", "T302", "T1735", "T1736", "T1739"]
    needed += [f"T{n}" for n in range(280, 310)]
    needed += list(XFILES)
    for k in sorted(set(needed)):
        d = doc_of(k)
        result["meta"]["sources"][k] = {
            "path": str(d.path.relative_to(ROOT)).replace("\\", "/"),
            "sha256": sha256(d.path.read_bytes()),
            "chars": len(d.norm),
        }

    g278, g279 = gs_of("T278"), gs_of("T279")

    # --- ③ 正控：植入一个真正的合本，检验探测器能不能看见接缝 ---
    a, b = doc_of("T279").norm, doc_of("T278").norm
    h1, h2 = len(a) // 2, len(b) // 2
    planted = a[:h1] + b[-h2:]
    src = {"T279": g279, "T278": g278}
    prows = profile(planted, src)
    pbest = best_split(prows, "T279", "T278")
    pbest["recovered_error"] = abs(pbest["split_char"] - h1) if pbest["split_char"] is not None else None
    result["controls"]["positive"] = {
        "label": "植入正控：八十華嚴前半 ＋ 六十華嚴後半",
        "recipe": {"first": "T279", "first_chars": h1, "second": "T278", "second_chars": h2},
        "expected_split_char": h1,
        "blocks": len(prows),
        "result": pbest,
        "sources": ["T279", "T278"],
        "pass": bool(pbest["pass"] and pbest["recovered_error"] is not None
                     and pbest["recovered_error"] <= BLOCK),
    }
    print(f"正控: min_side={pbest['min_side']:.3f} sep={pbest['separation']:.3f} "
          f"切点误差={pbest['recovered_error']} → {'PASS' if result['controls']['positive']['pass'] else 'FAIL'}")

    # --- ① 筛查：30 部华严部文本 + 2 部注疏 ---
    screen_ids = [short_id(r["taisho"]) for r in cat["catalog_32"]]
    for k in screen_ids:
        d = doc_of(k)
        c278 = coverage(d.norm, g278)
        c279 = coverage(d.norm, g279)
        m = meta[k]
        result["screen"].append({
            "id": k,
            "title": m["title_cbeta"],
            "juan": m["juan_cbeta"],
            "chars": len(d.norm),
            "xref": m.get("xref") or {},
            "cov": {"T278": round(c278, 4), "T279": round(c279, 4)},
            "tier2": len(d.norm) >= TIER2_MIN_CHARS,
        })
    for k, srcs, note in PARTITION_EXTRA:
        d = doc_of(k)
        result["screen"].append({
            "id": k,
            "title": EXTRA_TITLES[k],
            "juan": len(re.findall(r'<milestone n="\d+" unit="juan"/>', d.raw)),
            "chars": len(d.norm),
            "xref": {},
            "cov": {"T278": round(coverage(d.norm, g278), 4),
                    "T279": round(coverage(d.norm, g279), 4)},
            "tier2": True,
            "note": note,
        })

    # --- ② 分块切分：大体量候选 ---
    part_ids = [(r["id"], ["T278", "T279"]) for r in result["screen"]
                if r["tier2"] and not r.get("note")]
    part_ids += [(k, srcs) for k, srcs, _ in PARTITION_EXTRA]
    for k, srcs in part_ids:
        d = doc_of(k)
        sets = {s: gs_of(s) for s in srcs}
        rows = profile(d.norm, sets)
        best = best_split(rows, srcs[0], srcs[1])
        row = meta.get(k, {})
        result["partition"].append({
            "id": k,
            "title": row.get("title_cbeta") or EXTRA_TITLES.get(k, k),
            "chars": len(d.norm),
            "sources": srcs,
            "blocks": len(rows),
            "block_stats": block_stats(rows, srcs),
            "best_split": best,
            "best_block": best_block(d, rows, srcs[0], srcs[1], docs),
            "pass": best["pass"],
        })
        print(f"{k} blocks={len(rows)} min_side={best['min_side']:.3f} "
              f"sep={best['separation']:.3f} → {'PASS' if best['pass'] else 'no'}")

    # --- 负控记录（取自 partition 中同 id 的结果）---
    for k in ("T1735", "T1736"):
        row = next(r for r in result["partition"] if r["id"] == k)
        result["controls"]["negative"].append({
            "id": k,
            "title": row["title"],
            "sources": row["sources"],
            "min_side": row["best_split"]["min_side"],
            "separation": row["best_split"]["separation"],
            "pass": row["pass"],
        })

    # --- 合编档逐段嵌入检验：块级分类与两源交错次数（X223 / X240a / X240b） ---
    # 逐段嵌入的签名是高频交错；两段拼合的签名是两个长 run。
    HELUN_IDS = ("X223", "X240a", "X240b")
    for hid in HELUN_IDS:
        hrow = next(r for r in result["partition"] if r["id"] == hid)
        s1, s2 = hrow["sources"]
        dh = doc_of(hid)
        sets_h = {s: gs_of(s) for s in (s1, s2)}
        hrows = profile(dh.norm, sets_h)
        labels = []
        for r in hrows:
            c1, c2 = r["cov"][s1], r["cov"][s2]
            if c1 >= SIDE_COVERAGE and c2 >= SIDE_COVERAGE:
                lab = "双高"
            elif c1 >= SIDE_COVERAGE:
                lab = "经块"
            elif c2 >= SIDE_COVERAGE:
                lab = "义块"
            elif max(c1, c2) >= 0.10:
                lab = "双低"
            else:
                lab = "无涉"
            labels.append(lab)
        runs = [(k, sum(1 for _ in g)) for k, g in groupby(labels)]
        hrow["helun"] = {
            "labels": {k: labels.count(k) for k in ("经块", "义块", "双高", "双低", "无涉")},
            "runs": len(runs),
            "transitions": len(runs) - 1,
            "longest_run": max(n for _, n in runs),
            "cov_overall": {s: round(coverage(dh.norm, gs_of(s)), 4) for s in (s1, s2)},
            "runs_head": [list(x) for x in runs[:24]],
        }
        print(f"{hid} helun: labels={hrow['helun']['labels']} runs={len(runs)} "
              f"transitions={len(runs)-1} longest={hrow['helun']['longest_run']}")

    # --- 基线：什么才算「像」 ---
    for x, y, label in BASELINES:
        result["baselines"].append({
            "a": x, "b": y, "label": label,
            "chars_a": len(doc_of(x).norm),
            "coverage": round(coverage(doc_of(x).norm, gs_of(y)), 4),
        })

    # --- 定点：四十華嚴末卷是否取自《普賢菩薩行願讚》 ---
    d293 = doc_of("T293")
    jm = [m.start() for m in re.finditer(r'<milestone n="\d+" unit="juan"/>', d293.raw)]
    j40 = sum(1 for i in range(len(d293.norm)) if d293.raw_index(i) < jm[-1])
    for x, y, label in TARGETED:
        tail, gy = doc_of(x).norm[j40:], gs_of(y)
        result["targeted"].append({
            "a": x, "b": y, "label": label,
            "chars_a": len(tail),
            "lb": d293.lb_at(jm[-1]),
            "coverage": round(coverage(tail, gy), 4),
        })
    result["targeted"].append({
        "a": "T293", "b": "T279", "label": "四十華嚴卷1–39 → 八十華嚴（對照）",
        "chars_a": j40, "lb": "001a01", "coverage": round(coverage(d293.norm[:j40], g279), 4),
    })

    passed = [r["id"] for r in result["partition"] if r["pass"]]
    hl_rows = [r for r in result["partition"] if r["id"] in ("X223", "X240a", "X240b")]
    forms = []
    for r in hl_rows:
        hl = r["helun"]
        if hl["transitions"] >= 6:
            forms.append(f"{r['id']} 交错 {hl['transitions']} 次（逐段嵌入）")
        else:
            forms.append(f"{r['id']} 交错仅 {hl['transitions']} 次（偏两段拼合）")
    result["verdict"] = {
        "candidates": len(result["partition"]),
        "passed": passed,
        "screen_texts": len(result["screen"]),
        "statement": (f"大正藏 32 部无合本候选：无一部可通过分块来源分离检验；"
                      f"卍续藏给出两个经文合编实例，形态：{'；'.join(forms)}。" if not passed
                      else f"通过者：{passed}；合编形态：{'；'.join(forms)}"),
    }

    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("written", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
