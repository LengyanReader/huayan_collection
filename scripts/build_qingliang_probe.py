#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""R3/R4 一手取证：清凉传三书（古 T2098／廣 T2099／續 T2100）。

R4 仪式半边：五台山华严法会与转读行道的一手记载——
  古清涼傳：靈辨「轉誦華嚴經三七行道」（造论缘起，儀式性轉讀）；
  廣清涼傳：顯慶皇家設齋供一萬菩薩、每歲首大備齋會、尼誦華嚴結庵。
R3 文学半边：續清涼傳卷末附張商英《清涼山賦》并詩、總詩——文人文学接受一手。

统计层：三书术语计数（華嚴/齋/誦/禮/詩/賦/偈/像/寺）只作量级参考。
引文层：六条锚点切片，lb 可回源；判读标〔本文判断〕。

Usage: python scripts/build_qingliang_probe.py
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
OUT = ROOT / "data" / "research" / "qingliang_probe.json"

FILES = {"T2098": "T51n2098.xml", "T2099": "T51n2099.xml",
         "T2100": "T51n2100.xml"}
TERMS = ["華嚴", "文殊", "齋", "誦", "禮", "詩", "賦", "偈", "像", "寺"]

EXHIBITS = [
    {
        "key": "lingbian_zhuanjing",
        "doc": "T2098",
        "title": "古清涼傳·靈辨轉誦行道（R4 转读仪式）",
        "c_anchor": ["轉誦華嚴經三七行道", "還復根形"],
        "kind": "R4",
        "analysis": ("靈辨「頂戴此經（華嚴）、轉誦前行」——以身体仪式（頂戴）＋"
                    "定课转诵（三七日行道）为造论缘起；转读在此是行仪而非义解。"
                    "〔本文判断〕"),
    },
    {
        "key": "xianqing_zhai",
        "doc": "T2099",
        "title": "廣清涼傳·顯慶皇家设斋（R4 国家层面的华严法会）",
        "c_anchor": ["遣內侍黃門金守珍", "巡禮僧數盈一萬"],
        "kind": "R4",
        "analysis": ("显庆年间皇家遣内侍就山供养、设斋供一万菩萨——五台山"
                    "华严法会进入国家祀典层面，且当日巡礼僧数盈万，"
                    "朝台已成制度性流动。〔本文判断〕"),
    },
    {
        "key": "annual_zhaihui",
        "doc": "T2099",
        "title": "廣清涼傳·每岁首斋会（R4 年度斋会制度）",
        "c_anchor": ["每歲首之月大備齋會", "聖凡混同"],
        "kind": "R4",
        "analysis": ("「每歲首之月大備齋會、遐邇無間、聖凡混同」——年度化、"
                     "开放性的斋会制度；下文贫女遇斋即此会的故事化。"
                     "〔本文判断〕"),
    },
    {
        "key": "nun_songjing",
        "doc": "T2099",
        "title": "廣清涼傳·尼誦華嚴結庵（R4 个人课诵）",
        "c_anchor": ["每誦華嚴涅槃二部", "戒律清潔"],
        "kind": "R4",
        "analysis": ("西京万善寺尼于此结庵「每誦華嚴涅槃二部」——華嚴与涅槃"
                    "并列为日常课诵单元；个人课诵层面的一手记。〔本文判断〕"),
    },
    {
        "key": "zsy_fu",
        "doc": "T2100",
        "title": "續清涼傳·張商英《清涼山賦》并詩（R3 文人文学）",
        "c_anchor": ["又述清涼山賦并詩", "山名紫府"],
        "kind": "R3",
        "analysis": ("张商英自述「述清涼山賦并詩附之卷末」——宰辅文人以赋、诗"
                     "两种文体写清凉山；本传自附其文，文学接受的一手自证。"
                     "〔本文判断〕"),
    },
    {
        "key": "zong_shi",
        "doc": "T2100",
        "title": "續清涼傳·總詩（R3 僧人诗颂）",
        "c_anchor": ["五頂嵯峨接太虛", "猛虎巖前客路疎"],
        "kind": "R3",
        "analysis": ("「總詩」（作者题作「總」）以七绝写五顶——卷末诗颂群"
                     "（赋、律诗、绝句并存）显示清凉山写作已成文类。〔本文判断〕"),
    },
]


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def main() -> int:
    docs = {name: Doc(name, ROOT / "data/references/cbeta" / fn)
            for name, fn in FILES.items()}
    stats = {}
    for name, d in docs.items():
        stats[name] = {"chars": len(d.norm),
                       "terms": {t: d.norm.count(t) for t in TERMS}}

    exhibits = []
    for ex in EXHIBITS:
        d = docs[ex["doc"]]
        a, b = ex["c_anchor"]
        i = d.norm.find(a)
        j = d.norm.find(b, i if i >= 0 else 0)
        if i < 0 or j < 0:
            raise SystemExit(f"anchor not found in {ex['doc']}: {a[:10]}…")
        c0 = d.clean_of_norm[i]
        c1 = d.clean_of_norm[min(j + len(b), len(d.norm) - 1)]
        exhibits.append({
            "key": ex["key"], "doc": ex["doc"], "title": ex["title"],
            "kind": ex["kind"],
            "lb": d.lb_at(d.raw_index(i)),
            "text": d.clean[c0:c1 + len(b)].replace("\n", ""),
            "analysis": ex["analysis"],
        })
        print(f"  [{ex['kind']}] {ex['key']} {exhibits[-1]['lb']} "
              f"{exhibits[-1]['text'][:60]}…")

    data = {
        "meta": {
            "date": date.today().isoformat(),
            "title": "R3/R4 一手取证：清凉传三书",
            "method": ("统计层＝术语计数（量级参考）；引文层＝锚点切片（lb 回源）。"
                       "R4 仪式半边＝斋会/转读/行道/课诵；R3 文学半边＝卷末附赋诗。"
                       "音乐化半边（唱腔/梵呗谱）三书无载，仍缺。"),
            "sources": {name: {"path": f"data/references/cbeta/{fn}",
                               "sha256": sha256((ROOT / "data/references/cbeta" / fn).read_bytes()),
                               "bytes": (ROOT / "data/references/cbeta" / fn).stat().st_size}
                        for name, fn in FILES.items()},
        },
        "stats": stats,
        "exhibits": exhibits,
    }
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n",
                   encoding="utf-8")
    for name, s in stats.items():
        print(name, {k: v for k, v in s["terms"].items() if k in
                     ("華嚴", "齋", "誦", "詩", "賦")})
    print("written", OUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
