#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P4 教学·课仪：法藏《華嚴經傳記》講解第六（T51n2073，一手在库）。

P4 问「是否进入讲经、课诵、僧教育」。讲解第六 = 法藏亲集的讲经传承谱系：
章首列十位讲主（東晉法業→隋靈幹），每位有讲经事迹——「讲解」自梁陈以来
已成为华严接受的制度性单元，法藏为其立传即制度自证。

引文四条锚点切片（lb 回源）；判读标〔本文判断〕。
"""
from __future__ import annotations

import hashlib
import json
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_implicit_quotes import Doc  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "research" / "p4_jiangjie.json"

EXHIBITS = [
    {
        "key": "jj_head",
        "title": "章首讲主谱系（十位讲主名录）",
        "c_anchor": ["講解第六上東晉南林釋法業", "釋靈幹"],
        "analysis": ("法藏集《華嚴經傳記》，於諷誦、轉讀、書寫之外**专立讲解一篇**，"
                    "章首以朝代为序列十位讲主——「讲解」与讽诵、书写并列，"
                    "是《華嚴》接受史上被制度化的接受方式之一；立传本身即"
                    "制度化自证。〔本文判断〕"),
    },
    {
        "key": "faye_shu",
        "title": "東晉法業：敷弘幽旨·数百人伏膺",
        "c_anchor": ["遂敷弘幽旨欝為宗匠", "伏膺北面"],
        "analysis": ("法业亲从佛度跋陀罗笔受晋译《華嚴》，「敷弘幽旨、欝為宗匠」，"
                    "沙門曇斌等数百人北面受学——晋译初成即转入讲席，"
                    "译与讲首尾相接。〔本文判断〕"),
    },
    {
        "key": "gunabhadra_700",
        "title": "宋求那跋陀羅：集义学沙门七百余人",
        "c_anchor": ["集義學沙門七百餘人", "欲請講華嚴經"],
        "analysis": ("求那跋陀罗以大乘学世号摩訶衍，讲宣「莫能酬抗」；诸僧共请出经，"
                     "集义学沙门七百余人——讲席规模达七百人，是国家层面的"
                     "义学讲经建制。〔本文判断〕"),
    },
]


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def main() -> int:
    d = Doc("T2073", ROOT / "data/references/cbeta/T51n2073.xml")
    exhibits = []
    for ex in EXHIBITS:
        a, b = ex["c_anchor"]
        i = d.norm.find(a)
        j = d.norm.find(b, i if i >= 0 else 0)
        if i < 0 or j < 0:
            raise SystemExit(f"anchor not found: {a[:12]}…")
        c0 = d.clean_of_norm[i]
        c1 = d.clean_of_norm[min(j + len(b), len(d.norm) - 1)]
        exhibits.append({
            "key": ex["key"], "title": ex["title"],
            "lb": d.lb_at(d.raw_index(i)),
            "text": d.clean[c0:c1 + len(b)].replace("\n", ""),
            "analysis": ex["analysis"],
        })
        print(f"  [{exhibits[-1]['lb']}] {ex['title']}: {exhibits[-1]['text'][:70]}…")

    # 讲主名录统计（章首一行）
    i0 = d.norm.find("講解第六上")
    i1 = d.norm.find("諷誦第七")
    seg = d.norm[i0:i1]
    data = {
        "meta": {
            "date": date.today().isoformat(),
            "title": "P4 教学·课仪：華嚴經傳記講解第六",
            "method": "引文锚点切片（lb 回源）；源 sha256 入 JSON。讲解篇在库（T51n2073）。",
            "sources": {"t2073": {"path": "data/references/cbeta/T51n2073.xml",
                                  "sha256": sha256((ROOT / "data/references/cbeta/T51n2073.xml").read_bytes()),
                                  "bytes": (ROOT / "data/references/cbeta/T51n2073.xml").stat().st_size}},
        },
        "chapter_span_chars": i1 - i0,
        "exhibits": exhibits,
    }
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n",
                   encoding="utf-8")
    print("written", OUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
