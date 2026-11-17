#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""T6 化用判定：注疏复用经文的「短串」（4–11 字，低于字面引文阈值）。

§17.14 量了 ≥8 字暗引；§17.34 量了稀有二字组骨架。本探针取两者之间：
**己语块内的 4–11 字共享串**——不是引文（≥12 字面被切走）、不止二字组
（词级），是**短语级复用**：留词换框／缩写／易语的「化用」现场。

方法：在 T7 的己语块内，找同时在经文出现、且双侧全程 ≤3 次的 4–8 字串；
块内 ≥2 个不同短串（或一个 ≥6 字串）＝化用候选。机器出候选，
「留词换框／缩写／易语」的分型人工判读〔本文判断〕。

Pairs：A＝T1735×T279；B＝T1733×T278（C＝X234 嵌经体不取，理由同 §17.15）。
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
OUT = ROOT / "data" / "research" / "t6_huayong.json"

LO, HI = 4, 8       # 短串长度域
RARE_MAX = 3        # 双侧稀疏阈值
CTX = 26

PAIRS = {"A": ("T1735", "T279"), "B": ("T1733", "T278")}

# 人工判读定稿（--curate；双侧锚点重切，判读标〔本文判断〕）
CURATED: dict = {
    "t6_a_fushu": {
        "pair": "A", "find": "菩薩十地亦爾",
        "c_anchor": ["菩薩十地亦爾", "彼因果相順故"],
        "s_anchor": ["菩薩十地亦復如是", "差別得名"],
        "sutra_doc": "T279",
        "kind": "复述（留词换框）",
        "analysis": ("经句「菩薩十地亦復如是，同在一切智中差別得名」被疏语压成"
                    "「菩薩十地亦爾，同在一切智，因一切智得名」——亦復如是→亦爾、"
                    "差別得名→因一切智得名，实词全留、句式重整、**无引号**；同段"
                    "引《十地經論》影像分处则明标书名——引与化用在同一行内分用"
                    "两种标记。〔本文判断〕"),
    },
    "t6_b_kemu": {
        "pair": "B", "find": "爾時良醫」下明示法界",
        "c_anchor": ["第四爾時良醫下", "敬歎法器"],
        "s_anchor": ["爾時良醫", "菩提心耶"],
        "sutra_doc": "T278",
        "kind": "牒示式（经语作科判坐标）",
        "analysis": ("法藏以经文四字短语「爾時良醫」作整个科节的导航坐标"
                    "（「爾時良醫下明示法界中二：初敬歎法器」）——经语成为注疏"
                    "自己的目录语言；同块内「爾時良醫下」两见，科判体系整体"
                    "架在经文短语上。〔本文判断〕"),
    },
    "t6_a_kemu": {
        "pair": "A", "find": "如娑婆下類通一切",
        "c_anchor": ["諸佛子如娑婆下類通一切", "舉此例餘十方"],
        "s_anchor": ["諸佛子如娑婆", "盡法界虛空界"],
        "sutra_doc": "T279",
        "kind": "牒示式（经语作科判坐标）",
        "analysis": ("同型于 B 对：澄观以〈四諦品〉开头语「諸佛子如娑婆」作"
                    "「類通一切」科的坐标，并跨品援引（準〈四諦品〉更有舉此"
                    "例餘十方）——经文短语被化为跨章导航节点。〔本文判断〕"),
    },
}
NAMES = {"A": "澄觀《華嚴經疏》×T279", "B": "法藏《探玄記》×T278"}


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def side_text(doc: Doc, norm_i: int, span: int = CTX * 2) -> str:
    ci = doc.clean_of_norm[norm_i]
    return doc.clean[max(0, ci - CTX):ci + span - CTX].replace("\n", "").strip()


def analyse(pid: str, com_name: str, sutra_name: str) -> dict:
    com = Doc(com_name, ROOT / "data/references/cbeta" / pp.FILES[com_name])
    sutra = Doc(sutra_name, ROOT / "data/references/cbeta" / pp.FILES[sutra_name])
    hits12 = pp.hits(com, sutra, 12)

    # 己语块（复用 T7 口径）
    mask = bytearray(len(com.norm))
    for a, b, _, _ in hits12:
        for i in range(a, min(b, len(mask))):
            mask[i] = 1
    wins = []
    i = 0
    while i < len(mask):
        if mask[i]:
            i += 1
            continue
        j = i
        while j < len(mask) and not mask[j]:
            j += 1
        if j - i >= 150:
            wins.append((i, j))
        i = j

    # 双侧字符串计数（4–8 字串级稀疏）
    def counts(norm: str) -> Counter:
        c = Counter()
        for k in range(LO, HI + 1):
            for i in range(len(norm) - k + 1):
                c[norm[i:i + k]] += 1
        return c

    cs, cc = counts(sutra.norm), counts(com.norm)
    rare = {t for t, n in cs.items() if n <= RARE_MAX and cc.get(t, 0) <= RARE_MAX}

    sspans = {n: (s, e) for n, _, s, e in pp.pin_spans(sutra)}

    def sutra_pin(i: int):
        return next((n for n, (s, e) in sspans.items() if s <= i < e), None)

    cands = []
    sset = set()
    for i in range(len(sutra.norm) - LO + 1):
        sset.add(sutra.norm[i:i + LO])
    for i0, i1 in wins:
        wtxt = com.norm[i0:i1]
        found = []
        consumed = [False] * len(wtxt)
        for p in range(len(wtxt) - LO + 1):
            if consumed[p]:
                continue
            seed = wtxt[p:p + LO]
            if seed not in rare or seed not in sset:
                continue
            # 贪心延展为极大共享串
            a, b = p, p + LO
            while b < len(wtxt) and wtxt[a:b + 1] in sutra.norm:
                b += 1
            while a > 0 and wtxt[a - 1:b] in sutra.norm:
                a -= 1
            for k in range(a, b):
                consumed[k] = True
            run = wtxt[a:b]
            if len(run) > HI:
                continue  # ≥12 由 §17.14 计；9–11 记句引级
            si = sutra.norm.find(run)
            # 引号检测：run 在 clean 中的位置是否落在最近的「…」内
            ci = com.clean_of_norm[i0 + a]
            before = com.clean.rfind("「", 0, ci)
            after = com.clean.find("」", ci)
            quoted = (before >= 0 and after >= 0
                      and ci >= before + 1 and ci + len(run) <= after)
            found.append({
                "s": run, "c_pos": i0 + a, "s_norm": si,
                "s_lb": sutra.lb_at(sutra.raw_index(si)),
                "pin": sutra_pin(si), "quoted": quoted,
                "run_ctx": com.clean[max(0, ci - 22):ci + len(run) + 26]
                                     .replace("\n", ""),
            })
        if len(found) >= 2 or any(len(f["s"]) >= 6 for f in found):
            found.sort(key=lambda f: (f["quoted"], -len(f["s"])))
            top = found[:4]
            c0 = com.clean_of_norm[i0]
            cands.append({
                "c_lb": com.lb_at(com.raw_index(i0)),
                "block_chars": i1 - i0,
                "runs": [{"s": f["s"], "s_lb": f["s_lb"], "pin": f["pin"],
                          "quoted": f["quoted"], "run_ctx": f["run_ctx"]}
                         for f in top],
                "com_text": side_text(com, i0, min(200, i1 - i0)),
                "sutra_ctx": side_text(sutra, top[0]["s_norm"]),
            })
    def block_key(c):
        unq = [r for r in c["runs"] if not r["quoted"]]
        return (-len(unq), -max((len(r["s"]) for r in unq), default=0),
                c["block_chars"])
    cands.sort(key=block_key)
    n_quoted = sum(1 for c in cands if c["runs"] and c["runs"][0].get("quoted"))
    return {"com": com_name, "sutra": sutra_name,
            "stats": {"own_windows": len(wins), "huayong_blocks": len(cands)},
            "candidates": cands[:16]}


def main() -> int:
    data = {
        "meta": {
            "date": date.today().isoformat(),
            "title": "T6 化用判定：己语块内的 4–8 字共享串",
            "method": (f"己语块内共享串（{LO}–{HI} 字，双侧全程 ≤{RARE_MAX} 次）；"
                       "块含 ≥2 个短串或一个 ≥6 字串＝化用候选。分型人工判读"
                       "〔本文判断〕。C 对（宋注）嵌经体不取（理由同 §17.15）。"),
            "sources": {name: {"path": "data/references/cbeta/" + fn,
                               "sha256": sha256((ROOT / "data/references/cbeta" / fn).read_bytes())}
                        for name, fn in pp.FILES.items()},
        },
        "pairs": {},
    }
    for pid, (c, s) in PAIRS.items():
        r = analyse(pid, c, s)
        data["pairs"][pid] = r
        st = r["stats"]
        print(f"[{pid}] {NAMES[pid]} 己语块 {st['own_windows']} → 化用候选 {st['huayong_blocks']}")
        for cand in r["candidates"][:10]:
            for rr in cand["runs"][:3]:
                print(f"  {cand['c_lb']} [{rr['s']}] quoted={rr['quoted']}"
                      f" 经={rr['s_lb']}")
                print(f"    ctx: …{rr['run_ctx']}…")
    if "--curate" in sys.argv:
        docs = {}
        for name, fn in pp.FILES.items():
            docs[name] = Doc(name, ROOT / "data/references/cbeta" / fn)

        def slice_norm(doc: Doc, a: str, b: str) -> dict:
            i = doc.norm.find(a)
            j = doc.norm.find(b, i if i >= 0 else 0)
            if i < 0 or j < 0:
                raise SystemExit(f"anchor not found in {doc.name}: {a[:12]}")
            c0 = doc.clean_of_norm[i]
            c1 = doc.clean_of_norm[min(j + len(b), len(doc.norm) - 1)]
            return {"lb": doc.lb_at(doc.raw_index(i)),
                    "text": doc.clean[c0:c1 + len(b)].replace("\n", "")}

        data["exhibits"] = []
        for key, ex in CURATED.items():
            pid = ex["pair"]
            com_name, sutra_name = PAIRS[pid]
            com, sutra = docs[com_name], docs[ex.get("sutra_doc", sutra_name)]
            matches = [c for c in data["pairs"][pid]["candidates"]
                       if any(ex["find"] in r["run_ctx"] for r in c["runs"])]
            if len(matches) != 1:
                raise SystemExit(f"curated {key}: find matched {len(matches)}")
            ex2 = dict(ex)
            ex2.pop("find")
            ex2["key"] = key
            ex2["com_quote"] = slice_norm(com, *ex["c_anchor"])
            ex2["sutra_quote"] = slice_norm(sutra, *ex["s_anchor"])
            data["exhibits"].append(ex2)
        print(f"exhibits: {len(data['exhibits'])}")
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n",
                   encoding="utf-8")
    print("written", OUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
