#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P2 仪轨化＋P3 陀罗尼化：两晚唐单行本（T19n1020／T19n1021，一手新入库）。

P2 问「经文是否被编入斋醮、礼忏仪轨」——直证：
  T19n1020《大方廣佛花嚴經入法界品頓證毘盧遮那法身字輪瑜伽儀軌》（唐不空譯）
  ——〈入法界品〉善知眾藝童子章四十二字门被编入字轮观想瑜伽程序：
  字轮安置→字义观→持诵→顿证毘卢遮那法身，是「经文段被改写成仪轨程序」的
  第一手标本。

P3 问「是否以咒语、陀罗尼形式流通」——直证：
  T19n1021《華嚴經心陀羅尼》（普賢如來說，于闐三藏實叉難陀譯）
  ——八十二字总持；别本经云「若人诵此一遍，准诵龙藏中华严经
  上、中、下三本一遍」——一咒当全经三遍，是把整部经压缩为持诵
  单元的浓缩等式。

引文锚点切片（lb 回源）；判读标〔本文判断〕。
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
OUT = ROOT / "data" / "research" / "p2p3_ritual.json"

EXHIBITS = [
    {
        "key": "p2_open",
        "doc": "T19n1020",
        "facet": "P2",
        "title": "字輪瑜伽儀軌·入仪条件（P2 直证）",
        "c_anchor": ["夫欲頓入一乘修習毘盧遮那如來法身觀者", "則能悟入文殊師利大智慧海"],
        "analysis": ("开篇即把〈入法界品〉的普贤行愿与文殊智慧接进三密"
                    "瑜伽程序：先发普贤微妙行愿、再以三密加持身心——"
                    "经文义理被改写为仪轨的入修条件。〔本文判断〕"),
    },
    {
        "key": "p2_zilun",
        "doc": "T19n1020",
        "facet": "P2",
        "title": "字輪瑜伽儀軌·月轮布字（P2 直证）",
        "c_anchor": ["復應觀察自心諸眾生心及諸佛心本無有異", "放大光明照徹十方"],
        "analysis": ("观自心与佛心平等一相成大月轮，于月轮内右旋布列四十二"
                    "梵字——〈入法界品〉字门章的经文被转写为可操作的观想"
                    "次第，是「经文编入仪轨」的直接标本。〔本文判断〕"),
    },
    {
        "key": "p3_mantra",
        "doc": "T19n1021",
        "facet": "P3",
        "title": "華嚴經心陀羅尼·咒体（P3 直证）",
        "c_anchor": ["唵枳那枳那", "上元縣高公寺摩訶衍和尚授"],
        "analysis": ("普贤如来说、实叉难陀（八十华严主译者）译，咒文归整为"
                    "音译字；末行「上元縣高公寺摩訶衍和尚授」记师授来源——"
                    "陀罗尼以师授方式流通的痕迹。〔本文判断〕"),
    },
    {
        "key": "p3_equiv",
        "doc": "T19n1021",
        "facet": "P3",
        "title": "華嚴經心陀羅尼·一咒当全经三遍（浓缩等式）",
        "c_anchor": ["準誦龍藏中華嚴經", "其人敏悟"],
        "analysis": ("别本经云「若人誦此一遍，準誦龍藏中華嚴經上中下三本"
                     "一遍」——陀罗尼被明文等价为整部经的持诵当量；"
                     "把一部经压缩成一遍咒语，是陀罗尼化的核心机制。"
                     "〔本文判断〕"),
    },
]


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def main() -> int:
    docs = {
        "T19n1020": Doc("T19n1020", ROOT / "data/references/cbeta/T19n1020.xml"),
        "T19n1021": Doc("T19n1021", ROOT / "data/references/cbeta/T19n1021.xml"),
    }
    exhibits = []
    for ex in EXHIBITS:
        d = docs[ex["doc"]]
        a, b = ex["c_anchor"]
        i = d.norm.find(a)
        j = d.norm.find(b, i if i >= 0 else 0)
        if i < 0 or j < 0:
            # 宽容：只取始锚前后窗
            i2 = d.norm.find(a[:6])
            if i2 < 0:
                raise SystemExit(f"anchor not found in {ex['doc']}: {a[:12]}…")
            i = i2
            j = min(i + 40, len(d.norm) - 1)
            c0 = d.clean_of_norm[i]
            c1 = d.clean_of_norm[j]
        else:
            c0 = d.clean_of_norm[i]
            c1 = d.clean_of_norm[min(j + len(b), len(d.norm) - 1)]
        exhibits.append({
            "key": ex["key"], "doc": ex["doc"], "facet": ex["facet"],
            "title": ex["title"],
            "lb": d.lb_at(d.raw_index(i)),
            "text": d.clean[c0:c1 + len(b)].replace("\n", ""),
            "analysis": ex["analysis"],
        })
        print(f"  [{ex['facet']}] {ex['key']} {exhibits[-1]['lb']}: "
              f"{exhibits[-1]['text'][:70]}…")

    data = {
        "meta": {
            "date": date.today().isoformat(),
            "title": "P2 仪轨化＋P3 陀罗尼化：两晚唐单行本",
            "method": ("T19n1020（不空字轮仪轨）＝P2 直证；T19n1021（实叉难陀心陀罗尼）"
                       "＝P3 直证。引文锚点切片（lb 回源）。判读标〔本文判断〕。"),
            "sources": {k: {"path": f"data/references/cbeta/{k}.xml",
                            "sha256": sha256((ROOT / f"data/references/cbeta/{k}.xml").read_bytes()),
                            "bytes": (ROOT / f"data/references/cbeta/{k}.xml").stat().st_size}
                        for k in ("T19n1020", "T19n1021")},
        },
        "exhibits": exhibits,
    }
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n",
                   encoding="utf-8")
    print("written", OUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
