#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""R4 仪式·课诵：《四十二字觀門》（唐不空譯，T19n1019）一手回源。

本文是〈入法界品〉善知眾藝童子章的四十二字母观行仪轨本——
「华严字母」课诵的源头文献。与 T279（实叉难陀八十本）同章两译：
仪轨本（不空，奉诏译）与 canonical 本（实叉难陀）互证。

Usage:
  python scripts/build_r4_liturgical.py
"""
import json
from datetime import date
from pathlib import Path

from build_translation_workshop import Doc, sha256

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "research" / "r4_liturgical.json"

SRC = {
    "t1019": ("data/references/cbeta/T19n1019.xml",
              "《大方廣佛華嚴經入法界品四十二字觀門》，唐不空奉詔譯，CBETA T19n1019"),
    "t279": ("data/references/cbeta/T10n0279.xml",
             "《大方廣佛華嚴經》八十本，唐實叉難陀譯，CBETA T10n0279（同章 canonical 本对照）"),
}

Q = {
    # 仪轨本（不空）
    "q_frame": ("t1019", "爾時善財童子從天宮下", "至善知眾藝童子所",
                "仪轨以〈入法界品〉善知眾藝章为剧场——课诵文本内嵌经的叙事框架"),
    "q_hengchi": ("t1019", "我恒稱持入此解脫根本之字", "我恒稱持入此解脫根本之字",
                  "「恒稱持」——常课诵持，仪式化的明文"),
    "q_a_zi": ("t1019", "阿上字時，名由菩薩威德入無差別境界般若波羅蜜門", "悟一切法本不生故。",
               "首字门：「阿」字——每字一枚般若波羅蜜門＋一悟"),
    "q_42": ("t1019", "此四十二般若波羅蜜為首", "入無量無數般若波羅蜜門。",
             "四十二字为首，展开无量门——课诵的教义量级"),
    "q_gongde": ("t1019", "若菩薩摩訶薩能聽如是入諸字門", "得二十種殊勝功德。",
                 "受持读诵得二十种殊胜功德——课诵功德清单"),
    # canonical 本对照（实叉难陀 T279 同章）
    "q_t279": ("t279", "善知眾藝，學菩薩字智", "善知眾藝，學菩薩字智",
               "T279 同章：「善知眾藝，學菩薩字智」——同章两译的 canonical 侧锚点"),
}

GROUPS = [
    {"kind": "仪轨框架", "quotes": ["q_frame", "q_hengchi"],
     "what": "课诵文本内嵌经的叙事框架；「恒稱持」为常课明文"},
    {"kind": "字门结构", "quotes": ["q_a_zi", "q_42"],
     "what": "四十二字，字字一门；为首展开无量门"},
    {"kind": "功德清单", "quotes": ["q_gongde"],
     "what": "受持读诵得二十种殊胜功德"},
    {"kind": "同章对照", "quotes": ["q_t279"],
     "what": "与 T279 同章两译互证（canonical 侧）"},
]


def main() -> int:
    docs, sources = {}, {}
    for key, (rel, edition) in SRC.items():
        p = ROOT / rel
        docs[key] = Doc(key, p)
        sources[key] = {"path": rel, "edition": edition,
                        "bytes": p.stat().st_size,
                        "sha256": sha256(p.read_bytes())}

    quotes = {}
    for qid, (sk, a, b, note) in Q.items():
        q = docs[sk].slice_quote(a, b)
        quotes[qid] = {"source": sk, "lb": q["lb"], "text": q["text"].strip(),
                       "note": note}

    data = {
        "meta": {
            "operator": "R4",
            "title": "仪式·课诵：四十二字觀門（華嚴字母课诵的源头文献）",
            "date": date.today().isoformat(),
            "method": ("逐条以起止锚在源文切片（不手抄），记叶码 lb；源文件记 sha256；"
                       "六条引文（仪轨本五＋canonical 对照一）。"),
            "sources": sources,
            "note": "全文仅 2,203 字符的短仪轨；后世「华严字母」唱诵（华严字母赞）"
                    "承此四十二字门，其明清以降的唱仪文献未取，故 R4 仍 partial。",
        },
        "quotes": quotes,
        "groups": GROUPS,
        "boundaries": [
            "T1019 与 T279 同章而译文独立（不空 vs 實叉難陀）：字门章有两译流传，"
            "本身即是「此章被独立行用」的证据——但两译的字义配属略有出入，"
            "逐字对勘未做。",
            "「华严字母」的明清唱诵仪（如《華嚴字母贊》及丛林唱仪）未取一手；"
            "R4 的「音乐化」半边（唱腔、曲谱）完全未取——本批只到「观门课诵」。",
            "二十种功德清单是经典的「劝持」套式（般若系同款见诸经），"
            "登记其存在，不据以判华严字门的独特性。",
        ],
        "summary": {"quotes": len(quotes), "groups": len(GROUPS)},
    }
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n",
                   encoding="utf-8")
    print(f"quotes {len(quotes)} groups {len(GROUPS)}")
    for qid, q in quotes.items():
        print(f"  {qid} {q['source']} {q['lb']} | {q['text'][:36]}…")
    print("written", OUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
