#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""T7「以己语重述」语义比对探针——注疏不用引文时怎样追随经文。

既有 §17.15 量的是引用率/锚点链/明标节略；本探针回答剩下的问题：
注疏里**没有字面引文**的长段（己语块），是否仍在**追随**经文内容？

方法（机器只做候选，判读标〔本文判断〕）：
  1. 己语块：注疏侧去掉一切 ≥12 字字面引文命中后的极大无命中段（≥150 字）。
  2. 稀有实词对齐：取「经文全程 ≤3 次、且注疏全程 ≤3 次」的二字组——
     排除波罗蜜/阿僧祇一类高频术语后，剩下的就是两文共有的稀有实词。
  3. 追随判定：己语块内出现 ≥2 个不同稀有实词、且这些词落在**同品经文**里
     ＝该块以经文的稀有词汇为骨架重述——转述候选。
  4. 候选打印双侧文本，人工判读（同义改写／引申转述／仅术语同源）后
     以 CURATED 定稿 exhibits。

Pairs：A＝T1735《華嚴經疏》（澄觀）× T279；B＝T1733《探玄記》（法藏）× T278。
复用 build_paraphrase_probe 的 Doc/pin_spans/hits 机件，口径一致。

Usage: python scripts/build_t7_paraphrase.py [--curate]
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from collections import Counter
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_paraphrase_probe as pp  # noqa: E402
from build_implicit_quotes import Doc  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "research" / "t7_paraphrase.json"

WIN_MIN = 150     # 己语块最短（字）
SUB_LEN = 140     # 块内滑窗长度
SUB_STEP = 40     # 滑窗步长
SUB_MIN = 3       # 滑窗追随判定所需不同稀有词数
RARE_MAX = 3      # 双侧稀有阈值（全程出现次数）
TERMS_MIN = 2     # 块级追随判定所需不同稀有词数
CTX = 24          # 双侧引文上下文

PAIRS = {"A": ("T1735", "T279"), "B": ("T1733", "T278")}

# 人工判读定稿（--curate 阶段消费；key = pair:c_lb）。
# 判读纪律：机器只出「稀有实词簇」候选；同义改写／框架重整／书证式重述之判
# 为人工为之，行文标〔本文判断〕；双侧引文一律锚点重切（不手抄）。
CURATED: dict[str, dict] = {
    "A:0675c09": {
        "find": "種子不淨",
        "pair": "A",
        "title": "澄觀疏·不淨觀：论纲植入",
        "c_anchor": ["言不淨之法者", "意含究竟不淨"],
        "s_quotes": [["於母人腹中", "髮白面皺"]],
        "kind": "同义改写（纲目化）",
        "analysis": ("经文四句直叙入胎不淨（於母人腹中…畢竟至於髮白面皺），"
                    "澄觀逐句贴上不淨觀的名相标签：從婬欲生＝種子不淨、母人腹中＝"
                    "住處不淨、成垢穢身＝自相自性、髮白＝究竟不淨——实词全保留、"
                    "句式全重整，经文的叙述被重铸为纲目。〔本文判断〕"),
    },
    "A:0594b15": {
        "find": "苦名我所成者",
        "pair": "A",
        "title": "澄觀疏·四諦异名：随文释义",
        "c_anchor": ["九下方關𨷲世界", "能入滅諦第一義故"],
        "s_quotes": [["彼關𨷲世界中", "或名我所成"]],
        "kind": "释义补足（训诂式）",
        "analysis": ("经只列此世界四諦的异名清单（苦或名我所成……），不释义；"
                    "澄觀逐一判属并释所以：我所成者「我見有故」、我心「即我見愛」、"
                    "覺分「所覺處故」、入義「能入滅諦第一義故」——字面零引文，"
                    "义理全承，是「以己语重述」的纯净形态。〔本文判断〕"),
    },
    "A:0576c22": {
        "find": "三維八隅",
        "pair": "A",
        "title": "澄觀疏·世界海形相：喻名训释",
        "c_anchor": ["非圓方者", "對上方圓等故"],
        "s_quotes": [["世界海有種種差別形相", "山焰形"]],
        "kind": "释义补足（训诂式）",
        "analysis": ("经立喻名（或非圓方、或如山焰形），疏释喻相：三維八隅皆非"
                    "圓方、山焰＝如山似焰皆取上尖、對上方圓等故——喻名是经的，"
                    "释语全是疏的。〔本文判断〕"),
    },
    "B:0186b03": {
        "find": "創出家時願",
        "pair": "B",
        "title": "法藏《探玄記》·淨行願序：三学框架重整",
        "c_anchor": ["初明菩薩在家時願", "三學是其正所修故"],
        "s_quotes": [["菩薩在家", "入空法中"], ["若敷床座", "見真實相"]],
        "kind": "框架重整（时序化）",
        "analysis": ("净行品百余愿在经中是平行愿列；法藏以戒定慧三学次第把它"
                    "重整为修行时序（在家時願→創出家時願→受禁戒時願→修定慧行"
                    "時願），并给出归类理由（出家人三學是其正所修故）——引文只取"
                    "愿文四字头，框架语全为己语。〔本文判断〕"),
    },
    "B:0257b25": {
        "find": "金翅鳥心",
        "pair": "B",
        "title": "法藏《探玄記》·摩尼珠喻：书证式重述",
        "c_anchor": ["此珠力故", "變作摩尼珠"],
        "s_quotes": [["又復於彼大海中", "雨渧如車軸"], ["猶如龍雷震", "雨渧無分別"]],
        "kind": "书证式重述",
        "analysis": ("经以「一一雨渧如車軸」状摩尼珠雨、以「雨渧無分別」喻"
                    "佛法；法藏把意象补成形相（雨渧如車軸、蓋覆一由旬、遮此大雨"
                    "不令下過），并引《觀佛三昧經》（金翅鳥心）、《智論》（佛舍利"
                    "所变）双出其源——重述带书证，是「以己语重述」的最强形态："
                    "字面少经文、内容承经喻、出处标他典。〔本文判断〕"),
    },
}


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def own_windows(com: Doc, hits_list: list[tuple[int, int, int, int]]) -> list[dict]:
    """注疏侧极大无命中段（norm 座标）。"""
    mask = bytearray(len(com.norm))
    for a, b, _, _ in hits_list:
        for i in range(a, min(b, len(mask))):
            mask[i] = 1
    out = []
    i = 0
    while i < len(mask):
        if mask[i]:
            i += 1
            continue
        j = i
        while j < len(mask) and not mask[j]:
            j += 1
        if j - i >= WIN_MIN:
            out.append({"i0": i, "i1": j})
        i = j
    return out


def rare_terms(sutra: Doc, com: Doc) -> set[str]:
    cs = Counter(sutra.norm[i:i + 2] for i in range(len(sutra.norm) - 1))
    cc = Counter(com.norm[i:i + 2] for i in range(len(com.norm) - 1))
    return {t for t, n in cs.items() if n <= RARE_MAX and cc.get(t, 0) <= RARE_MAX}


def lb_of(com: Doc, norm_i: int) -> str:
    return com.lb_at(com.raw_index(norm_i))


def side_text(doc: Doc, norm_i: int, span: int = CTX * 2) -> str:
    ci = doc.clean_of_norm[norm_i]
    return doc.clean[max(0, ci - CTX):ci + span - CTX].replace("\n", "").strip()


def analyse(pair_id: str, com_name: str, sutra_name: str) -> dict:
    com = Doc(com_name, ROOT / "data/references/cbeta" / pp.FILES[com_name])
    if com_name == "X234":
        com = Doc(com_name, ROOT / pp.XFILES["X234"])
    sutra = Doc(sutra_name, ROOT / "data/references/cbeta" / pp.FILES[sutra_name])
    hits12 = pp.hits(com, sutra, 12)
    wins = own_windows(com, hits12)
    rare = rare_terms(sutra, com)
    sspans = {n: (s, e) for n, _, s, e in pp.pin_spans(sutra)}

    def sutra_pin(norm_i: int) -> int | None:
        return next((n for n, (s, e) in sspans.items() if s <= norm_i < e), None)

    tracked, clusters, total_chars = 0, 0, 0
    cands = []
    for w in wins:
        total_chars += w["i1"] - w["i0"]
        win_text = com.norm[w["i0"]:w["i1"]]
        terms = []
        seen = set()
        for k in range(len(win_text) - 1):
            t = win_text[k:k + 2]
            if t in rare and t in sutra.norm and t not in seen:
                seen.add(t)
                si = sutra.norm.find(t)
                terms.append({
                    "t": t,
                    "w_pos": w["i0"] + k,
                    "s_norm": si,
                    "s_lb": sutra.lb_at(sutra.raw_index(si)),
                })
        if len(terms) < TERMS_MIN:
            continue
        tracked += 1
        # 滑窗取簇：块内稀有词最密的小窗（可读 exhibit）
        best_sub = None
        for k in range(0, max(1, len(win_text) - SUB_LEN), SUB_STEP):
            seg = win_text[k:k + SUB_LEN]
            hit = sorted({t["t"] for t in terms if t["t"] in seg},
                         key=lambda t: seg.find(t))
            if len(hit) >= SUB_MIN and (best_sub is None
                                        or len(hit) > best_sub[0]):
                best_sub = (len(hit), k)
        if best_sub is None:
            continue
        clusters += 1
        _, k = best_sub
        sub0 = w["i0"] + k
        sub_terms = [t for t in terms if t["t"] in
                     com.norm[sub0:sub0 + SUB_LEN]]
        # 经文侧：覆盖全部命中词首现位置的区间
        ss = min(t["s_norm"] for t in sub_terms)
        se = max(t["s_norm"] for t in sub_terms)
        s_lo, s_hi = max(0, ss - 8), min(len(sutra.norm), se + 22)
        c0 = sutra.clean_of_norm[s_lo]
        c1 = sutra.clean_of_norm[s_hi - 1]
        cands.append({
            "pin": sutra_pin(sub_terms[0]["s_norm"]),
            "c_lb": lb_of(com, sub0),
            "chars": min(SUB_LEN, w["i1"] - sub0),
            "block_chars": w["i1"] - w["i0"],
            "sub0": sub0,
            "terms": sub_terms,
            "com_text": side_text(com, sub0, SUB_LEN + CTX),
            "sutra_ctx": side_text(sutra, sub_terms[0]["s_norm"]),
            "sutra_span": {"lb": sutra.lb_at(sutra.raw_index(s_lo)),
                           "text": sutra.clean[c0:c1 + 1].replace("\n", "")},
            "key": f"{pair_id}:{lb_of(com, sub0)}",
        })
    cands.sort(key=lambda c: (-len(c["terms"]), c["chars"]))
    return {
        "com": com_name, "sutra": sutra_name,
        "stats": {"own_windows": len(wins), "own_chars": total_chars,
                  "tracked": tracked, "clusters": clusters,
                  "cluster_share": round(clusters / len(wins), 4) if wins else 0},
        "candidates": cands,
    }


def main() -> int:
    curate = "--curate" in sys.argv
    data = {
        "meta": {
            "date": date.today().isoformat(),
            "title": "T7「以己语重述」语义比对：稀有实词骨架对齐",
            "method": ("己语块＝去 ≥12 字引文命中后的极大无命中段（≥150 字）；"
                       f"稀有实词＝双侧全程出现 ≤{RARE_MAX} 次的二字组（排除高频术语）；"
                       f"追随判定＝块内 ≥{TERMS_MIN} 个不同稀有词且落在同品经文。"
                       "机器只出候选；同义改写／引申转述之判读人工为之，标〔本文判断〕。"),
            "params": {"WIN_MIN": WIN_MIN, "RARE_MAX": RARE_MAX,
                       "TERMS_MIN": TERMS_MIN, "SUB_LEN": SUB_LEN,
                       "SUB_STEP": SUB_STEP, "SUB_MIN": SUB_MIN},
            "sources": {
                name: {"path": ("data/references/cbeta_x/" + Path(p).name
                                if name.startswith("X") else "data/references/cbeta/" + Path(p).name),
                       "sha256": sha256((ROOT / ("data/references/cbeta_x/" + Path(p).name
                                                 if name.startswith("X") else "data/references/cbeta/" + Path(p).name)).read_bytes())}
                for name, p in {**pp.FILES, **pp.XFILES}.items()
            },
        },
        "pairs": {},
    }
    for pid, (c, s) in PAIRS.items():
        r = analyse(pid, c, s)
        data["pairs"][pid] = r
        st = r["stats"]
        print(f"[{pid}] {c}×{s} 己语块 {st['own_windows']}（{st['own_chars']:,} 字）"
              f"→ 含稀有实词 {st['tracked']}（弱）｜成簇 {st['clusters']}"
              f"（{st['cluster_share']:.1%}，滑窗 ≥{SUB_MIN} 词）")
        for cand in r["candidates"][:8]:
            pin = cand['pin'] if cand['pin'] is not None else '?'
            print(f"  品{pin} {cand['c_lb']} {cand['chars']}字 "
                  f"terms={[t['t'] for t in cand['terms']][:8]}")
    if curate:
        docs: dict[str, Doc] = {}
        for name, fn in {**pp.FILES, **pp.XFILES}.items():
            path = (ROOT / pp.XFILES[name] if name.startswith("X")
                    else ROOT / "data/references/cbeta" / fn)
            docs[name] = Doc(name, path)

        def slice_norm(doc: Doc, a: str, b: str) -> dict:
            i = doc.norm.find(a)
            j = doc.norm.find(b, i if i >= 0 else 0)
            if i < 0 or j < 0:
                raise SystemExit(f"anchor not found: {a[:12]}…/{b[:12]}… in {doc.name}")
            c0 = doc.clean_of_norm[i]
            c1 = doc.clean_of_norm[min(j + len(b), len(doc.norm) - 1)]
            return {"lb": doc.lb_at(doc.raw_index(i)),
                    "text": doc.clean[c0:c1 + len(b)].replace("\n", "")}

        # exhibits 独立锚点切取（不依赖候选窗；首批探针头部候选的人工定稿）
        # terms 重算：稀有二字组中同时出现在注引与经引两侧者
        data["exhibits"] = []
        for key, ex in CURATED.items():
            pid = key.split(":")[0]
            com = docs[data["pairs"][pid]["com"]]
            sutra = docs[data["pairs"][pid]["sutra"]]
            # exhibit 侧低频共现阈值（≤8）：比簇选的 ≤3 宽，专为短引文对
            cs = Counter(sutra.norm[i:i + 2] for i in range(len(sutra.norm) - 1))
            cc = Counter(com.norm[i:i + 2] for i in range(len(com.norm) - 1))
            lowfreq = {t for t, n in cs.items() if n <= 8 and cc.get(t, 0) <= 8}
            ex = dict(ex)
            ex["key"] = key
            def norm_slice(doc: Doc, a: str, b: str) -> str:
                i = doc.norm.find(a)
                j = doc.norm.find(b, i if i >= 0 else 0)
                return doc.norm[i:j + len(b)]
            cq = slice_norm(com, *ex["c_anchor"])
            sqs = [slice_norm(sutra, a, b) for a, b in ex["s_quotes"]]
            snorm = "".join(norm_slice(sutra, a, b) for a, b in ex["s_quotes"])
            cnorm = norm_slice(com, *ex["c_anchor"])
            terms = sorted({cnorm[k:k + 2] for k in range(len(cnorm) - 1)}
                           & set(lowfreq)
                           & {snorm[k:k + 2] for k in range(len(snorm) - 1)})
            ex["com_quote"] = cq
            ex["sutra_quotes"] = sqs
            ex["terms"] = terms
            if len(terms) < 2:
                raise SystemExit(f"curated {key}: only {len(terms)} rare terms")
            data["exhibits"].append(ex)
        print(f"exhibits: {len(data['exhibits'])}")
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n",
                   encoding="utf-8")
    print("written", OUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
