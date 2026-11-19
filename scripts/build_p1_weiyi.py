#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P1 补完（第一批）：道教義樞·位業義的五阶体系 × 華嚴十地结构。

§17.13 遗留「位業義全疏的逐句对读未做」——本探针取其对读第一组：
位業義的「證位品：始自發心終乎極道，大有五位」（發心/伏道/知真/出離/…）
× T279 十地品的「從初地乃至第七地…從第八地乃至第十地」二分结构。
mandoku 源剥 ¶ 后切片；判读标〔本文判断〕。
"""
from __future__ import annotations

import hashlib
import json
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_translation_workshop import Doc  # noqa: E402
from build_implicit_quotes import Doc as IDoc  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "research" / "p1_weiyi.json"
TMP = ROOT / ".tmp" / "p1weiyi"


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def main() -> int:
    raw = (ROOT / "data/references/daozang/KR5e0031_001.txt").read_text(encoding="utf-8")
    TMP.mkdir(parents=True, exist_ok=True)
    tmpf = TMP / "KR5e0031_001.txt"
    tmpf.write_text(raw.replace("¶", ""), encoding="utf-8")
    dy = Doc("KR5e0031", tmpf)
    t279 = IDoc("T279", ROOT / "data/references/cbeta/T10n0279.xml")

    def s_cn(key, doc, start, end):
        i = doc.norm.find(start)
        j = doc.norm.find(end, i if i >= 0 else 0)
        if i < 0 or j < 0:
            raise SystemExit(f"{key}: 锚未命中 {start[:12]!r}")
        c0 = doc.clean_of_norm[i]
        c1 = doc.clean_of_norm[min(j + len(end), len(doc.norm) - 1)]
        return {"source": key, "lb": doc.lb_at(doc.raw_index(i)),
                "text": doc.clean[c0:c1 + len(end)].replace("\n", "").strip()}

    def s_mandoku(key, start, end):
        q = dy.slice_quote(start, end)
        return {"source": key, "lb": q.get("lb", ""),
                "text": q["text"].replace("¶", "").strip()}

    pairs = [
        {
            "id": "weiyi_wuwwei",
            "title": "位業義·證位品五阶 × 華嚴十地七地二分",
            "non_buddhist": [s_mandoku("daojiao", "證位品者始自發心終乎極道", "知真四者出離")],
            "buddhist": [s_cn("t279", t279, "菩薩從初地乃至第七地成就智功用分",
                              "無功用行皆悉成就")],
            "analysis": ("位業義證位品立「始自發心、終乎極道」的五阶（發心/伏道/"
                        "知真/出離/…），並記陸先生「起自凡夫積行成道：始化曰仙、"
                        "仙化成真」的阶梯；華嚴十地品以「從初地乃至第七地成就智"
                        "功用分，從第八地乃至第十地無功用行」把十地切成**功用/"
                        "無功用二分**。两者都是「分段化的成道阶梯」，且都立一个"
                        "**转折位**（道教在仙真之化、华严在七地入八地）。"
                        "不在场的那半：道教五阶的终点是仙真品位（位业实有——"
                        "位业义正是为此立章），华严的十地在无功用行处已"
                        "「非位非阶」可言（位位无碍——阶位本身被圆融消解）。"
                        "〔本文判断〕"),
        },
        {
            "id": "weiyi_27pin",
            "title": "位業義·二十七品三清位 × 華嚴阶位清单",
            "non_buddhist": [s_mandoku("daojiao", "凡二十七品爲三清一乘之位", "一乘之位")],
            "buddhist": [s_cn("t279", t279, "菩薩十地", "如實說菩薩十地差別相故")],
            "analysis": ("位業義引「三界四民之位……凡二十七品爲三清一乘之位」——"
                        "道教的阶位**数目化**（27 品三清）；華嚴亦言「令得菩薩十地"
                        "始終、如實說菩薩十地差別相」——同样以**可数的阶位序列**"
                        "安顿修行历程。不在场的那半：道教的 27 品是**死后迁转的"
                        "官阶想象**（三清九宫各有名号），华严的十地是**现生观行"
                        "的证位**（位位有波罗蜜配属）——数目化同、性质异。"
                        "〔本文判断〕"),
        },
    ]

    data = {
        "meta": {
            "date": date.today().isoformat(),
            "title": "P1 补完（第一批）：位業義五阶 × 華嚴十地",
            "method": ("mandoku 源剥 ¶ 后切片；華嚴侧 norm 锚切片；lb/位置可回源。"
                       "「位業義全疏逐句对读」仍为长时程——本批为体系层对读第一批。"),
            "sources": {"daojiao": {"path": "data/references/daozang/KR5e0031_001.txt",
                                    "sha256": sha256((ROOT / "data/references/daozang/KR5e0031_001.txt").read_bytes())},
                        "t279": {"path": "data/references/cbeta/T10n0279.xml",
                                 "sha256": sha256((ROOT / "data/references/cbeta/T10n0279.xml").read_bytes())}},
        },
        "pairs": pairs,
    }
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n",
                   encoding="utf-8")
    for p in pairs:
        print(f"[{p['id']}]")
        for q in p["non_buddhist"] + p["buddhist"]:
            print("   ", q.get("lb", "@"), q["text"][:56])
    print("written", OUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
