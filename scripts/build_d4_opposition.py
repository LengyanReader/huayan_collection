#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""D4 教义对立：法藏《華嚴一乘教義分齊章》（T45n1866，一手新入库）。

D4 问「两方在哪一点上互相否定」。分齊章是华严宗自己写的对立文档——它把
「别教一乘」与「三乘」的对立逐条展开（十说），并同时引三乘教证（法華/
解深密/瑜伽诸论）与一乘教证（華嚴）。对立点不在「有无佛性」而在
**教说位阶**：三乘是临门权引，一乘是界外实授；一乘教内不见说三乘。

引文四条＋经侧一条（T279 海印三昧），锚点切片；判读标〔本文判断〕。
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
OUT = ROOT / "data" / "research" / "d4_opposition.json"

EXHIBITS = [
    {
        "key": "d4_fenxiang",
        "doc": "T45n1866",
        "title": "分相門：別教一乘別於三乘（三车/牛车二分）",
        "c_anchor": ["分相門者此則別教一乘別於三乘", "界外露地所授牛車是一乘教也"],
        "analysis": ("全章最直接的二分：门外三车＝三乘教（诱引），界外露地牛车＝"
                     "一乘教（实授）——对立点被明确安放在**教说的位阶**上，"
                     "不是教义内容的真伪。〔本文判断〕"),
    },
    {
        "key": "d4_quan",
        "doc": "T45n1866",
        "title": "權實差別：臨門三車俱是開方便門",
        "c_anchor": ["以三中牛車亦同羊鹿權引諸子", "臨門三車俱是開方便門"],
        "analysis": ("十说之首（權實差別）：三车与羊鹿同为权引、俱是方便门——"
                     "三乘教法被定性为**权**，这是否定式判断的核心：不否认其"
                     "有效，否定其为究竟。〔本文判断〕"),
    },
    {
        "key": "d4_bujian",
        "doc": "T45n1866",
        "title": "一乘教中不見說三乘",
        "c_anchor": ["海印定中自在演說無盡具足主伴無窮", "本末不見說三乘小乘等法"],
        "analysis": ("互斥的明文：别教一乘（海印定中所演）本末不见说三乘小乘"
                     "等法——两方在「教内有无对方」这一点上互斥：一乘不见"
                     "三乘，三乘亦不见一乘（分相门之意）。〔本文判断〕"),
    },
    {
        "key": "d4_xinghai",
        "doc": "T45n1866",
        "title": "对立的根据：性海果分不可说",
        "c_anchor": ["一別教二同教初中二一性海果分是不可說義", "不與教相應故"],
        "analysis": ("章首即立「性海果分不可说、不与教相应」——别教一乘的"
                     "终极位分在教法之外，三乘之「权」与一乘之「不可说」"
                     "构成对立的两极。〔本文判断〕"),
    },
    {
        "key": "d4_haiyin_sutra",
        "doc": "T279",
        "title": "经侧对应：海印三昧威神力（T279 品3）",
        "c_anchor": ["海印三昧威神力", "放大光明無有邊"],
        "analysis": ("章言「海印定中自在演說」——判教所立的教主说法位，"
                     "在经文中有原文对应（〈普賢三昧品〉）；对立的"
                     "一极有经本，另一极（三乘）由章内引法華/解深密等"
                     "他经立证——对立双方各有文本，法藏是立判者。〔本文判断〕"),
    },
]


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def main() -> int:
    docs = {
        "T45n1866": Doc("T45n1866", ROOT / "data/references/cbeta/T45n1866.xml"),
        "T279": Doc("T279", ROOT / "data/references/cbeta/T10n0279.xml"),
    }
    exhibits = []
    for ex in EXHIBITS:
        d = docs[ex["doc"]]
        a, b = ex["c_anchor"]
        i = d.norm.find(a)
        j = d.norm.find(b, i if i >= 0 else 0)
        if i < 0 or j < 0:
            raise SystemExit(f"anchor not found in {ex['doc']}: {a[:14]}…")
        c0 = d.clean_of_norm[i]
        c1 = d.clean_of_norm[min(j + len(b), len(d.norm) - 1)]
        exhibits.append({
            "key": ex["key"], "doc": ex["doc"], "title": ex["title"],
            "lb": d.lb_at(d.raw_index(i)),
            "text": d.clean[c0:c1 + len(b)].replace("\n", ""),
            "analysis": ex["analysis"],
        })
        print(f"  {ex['key']} {exhibits[-1]['lb']}: {exhibits[-1]['text'][:64]}…")

    data = {
        "meta": {
            "date": date.today().isoformat(),
            "title": "D4 教义对立：一乘与三乘的分齐",
            "method": ("T45n1866《華嚴一乘教義分齊章》为华严宗自书的对立文档；"
                       "引文锚点切片（lb 回源）。对立点＝教说位阶（权/实、"
                       "门内/门外、可见/不可见），非内容真伪。判读标〔本文判断〕。"),
            "sources": {
                "T45n1866": {"path": "data/references/cbeta/T45n1866.xml",
                             "sha256": sha256((ROOT / "data/references/cbeta/T45n1866.xml").read_bytes()),
                             "bytes": (ROOT / "data/references/cbeta/T45n1866.xml").stat().st_size},
                "T279": {"path": "data/references/cbeta/T10n0279.xml",
                         "sha256": sha256((ROOT / "data/references/cbeta/T10n0279.xml").read_bytes()),
                         "bytes": (ROOT / "data/references/cbeta/T10n0279.xml").stat().st_size},
            },
        },
        "exhibits": exhibits,
    }
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n",
                   encoding="utf-8")
    print("written", OUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
