#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""D1 复跑：阿含/般若 × 華嚴 共享名目——从「登记 B」升「实测 A」。

§7 承诺的复跑。四阿含＋大品般若（T08n0223，本批入库）全部在库，
三十七道品系名目逐词计数（含异形：覺支/七菩提分），另给三组双侧引文：
  ① 杂阿含·七觉支退不退机制 × T279「如來所轉妙法輪一切皆是菩提分」
     ——同一清单，阿含用为准禅法（起/退机制），华严并入法性悟入；
  ② 中阿含·四念处「觀身如身」 × T279 四念處段；
  ③ 大品般若·六波罗蜜化佛说 × T279 十地檀波罗蜜增上段
     ——般若的六度在華嚴扩成十度（同一名相的扩容）。
计数只作量级参考；引文起止锚切片可回源。
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_implicit_quotes import Doc  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "research" / "d1_agama.json"

FILES = {
    "t279": "data/references/cbeta/T10n0279.xml",
    "chang": "data/references/cbeta/T01n0001.xml",
    "zhong": "data/references/cbeta/T01n0026.xml",
    "za": "data/references/cbeta/T02n0099.xml",
    "zengyi": "data/references/cbeta/T02n0125.xml",
    "dapin": "data/references/cbeta/T08n0223.xml",
}
NAMES = {"t279": "八十華嚴", "chang": "長阿含", "zhong": "中阿含",
         "za": "雜阿含", "zengyi": "增壹阿含", "dapin": "大品般若"}
TERMS = ["四念處", "四正勤", "四如意足", "五根", "五力",
         "覺支", "七菩提分", "八正道", "四聖諦", "十八空", "六波羅蜜"]


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def main() -> int:
    docs = {k: Doc(k, ROOT / rel) for k, rel in FILES.items()}
    matrix = {}
    for tkw in TERMS:
        row = {}
        for k, d in docs.items():
            row[k] = d.norm.count(tkw)
        matrix[tkw] = row

    def s(key, start, end):
        d = docs[key]
        i = d.norm.find(start)
        j = d.norm.find(end, i if i >= 0 else 0)
        if i < 0 or j < 0:
            raise SystemExit(f"{key}: 起锚未命中 {start[:14]!r}" if i < 0 else f"{key}: 止锚未命中 {end[:14]!r}")
        c0 = d.clean_of_norm[i]
        c1 = d.clean_of_norm[min(j + len(end), len(d.norm) - 1)]
        return {"source": key, "lb": d.lb_at(d.raw_index(i)),
                "text": d.clean[c0:c1 + len(end)].replace("\n", "").strip()}

    pairs = [
        {
            "id": "qijuezhi",
            "title": "七觉支：禅法机制 × 法性悟入",
            "non_buddhist_side": "za",
            "non_buddhist": [s("za", "未起念覺支不起", "捨覺支則退")],
            "buddhist": [s("t279", "如來所轉妙法輪一切皆是菩提分", "如是之人常見佛")],
            "analysis": ("同一套觉支名目（念→擇法→精進→猗→喜→定→捨），雜阿含把它"
                        "编入**起灭机制**（未起不起、已起则退——对治五盖的操作手册）；"
                        "華嚴說「如來所轉妙法輪，一切皆是菩提分，若能聞已悟法性」——"
                        "菩提分从禅修清单升为**法性论断**（闻即悟性）。共享清单、"
                        "功能重置：这是 D1「共享清单」判的最干净标本。"),
        },
        {
            "id": "nianchu",
            "title": "四念处：观身如身 × 华严念处段",
            "non_buddhist_side": "zhong",
            "non_buddhist": [s("zhong", "我本為汝說四念處觀身如身", "觀覺心法如法")],
            "buddhist": [s("t279", "四念處", "四念處")],
            "analysis": ("中阿含的四念处是**身受心法的如实观**（觀身如身的重复强调）；"
                        "華嚴中「四念處」出现两次，被纳入菩萨行门清单——名目保留、"
                        "位置改变：从出世道的核心操作变成无尽行门之一。"),
        },
        {
            "id": "liudu_shidu",
            "title": "六波罗蜜 → 十波罗蜜：名相扩容",
            "non_buddhist_side": "dapin",
            "non_buddhist": [s("dapin", "結跏趺坐說六波羅蜜", "必得阿耨多羅三藐三菩提")],
            "buddhist": [s("t279", "十波羅蜜中檀波羅蜜增上", "但隨力隨分")],
            "analysis": ("大品般若以六波罗蜜为纲（化佛宣说）；華嚴十地位中扩为"
                        "**十波罗蜜**且逐地配属（檀增上→余随力随分）——同一 "
                        "波罗蜜清单的**扩容与配位**：般若给了清单，华严给了"
                        "位次分配表。这是 D1 里「继承并扩容」而非仅「共享」的一例。"),
        },
    ]

    data = {
        "meta": {
            "date": date.today().isoformat(),
            "title": "D1 复跑：阿含/般若 × 華嚴 共享名目（实测 A）",
            "method": ("四阿含＋大品般若全部在库逐词计数（含异形覺支/七菩提分）；"
                       "三组双侧引文锚点切片。§7 的「登记 B」由此升「实测 A」。"),
            "sources": {k: {"path": rel,
                            "sha256": sha256((ROOT / rel).read_bytes()),
                            "bytes": (ROOT / rel).stat().st_size}
                        for k, rel in FILES.items()},
        },
        "matrix": matrix,
        "pairs": pairs,
    }
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n",
                   encoding="utf-8")
    print(f"{'词':<8}" + "".join(f"{NAMES[k]:>10}" for k in FILES))
    for tkw, row in matrix.items():
        print(f"{tkw:<8}" + "".join(f"{row[k]:>10}" for k in FILES))
    for p in pairs:
        print(f"  [{p['id']}] {p['non_buddhist'][0]['lb']} ↔ {p['buddhist'][0]['lb']}")
    print("written", OUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
