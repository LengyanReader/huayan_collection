#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""丹珠尔内容层·第一步：同论异译的开篇对读。

内容层不再停留于抽样——取两部「汉藏同源」文本做**开篇对读**：
  ① D4011《聖普賢行願王大讚》（བཤད་སྦྱར 注释本）× T297《普賢菩薩行願讚》（不空译）
     ——同一 Bhadracarī 的两种译态：藏译自带归敬＋「义略摄为十」解经框架，
     汉译纯颂无框架。
  ② D3993 世親《十地經釋》× T1522《十地經論》（菩提流支等译）
     ——同一部论的两种开篇：藏译归敬文殊＋传承缘起偈（谁说/谁使说/谁受），
     汉译以北魏侍中崔光所制朝廷序开篇——译场形态（经院传承 vs 国家工程）
     在文本结构上直接可见，呼应 §17.19 S1 与 §17.20 S2。

藏文侧以卷号＋字符位置回源（无 CBETA 式 lb）；汉文侧 lb 回源。
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
OUT = ROOT / "data" / "research" / "tanjur_content.json"


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def tib_open(vol: str, D: int, start_kw: str, n: int = 260) -> dict:
    t = Path(f"data/references/tibetan/derge_tengyur/{vol}.txt") \
        .read_text(encoding="utf-8-sig", errors="replace")
    m = re.search(r"\{D" + str(D) + r"\}", t)
    seg = t[m.start():m.start() + 1600]
    clean = re.sub(r"\[[0-9a-z.\]]+\]", "", seg).replace("\n", " ")
    clean = re.sub(r"#", "", clean)
    clean = re.sub(r"\s+", " ", clean).strip()
    i = clean.find(start_kw)
    pos = m.start()
    return {"vol": vol, "pos": pos, "text": clean[i:i + n] if i >= 0
            else clean[:n]}


def main() -> int:
    d297 = Doc("T297", ROOT / "data/references/cbeta/T10n0297.xml")
    d1522 = Doc("T1522", ROOT / "data/references/cbeta/T26n1522.xml")

    def cn(doc, start, end):
        i = doc.norm.find(start)
        j = doc.norm.find(end, i if i >= 0 else 0)
        if i < 0 or j < 0:
            raise SystemExit(f"{doc.key}: 锚未命中 {start[:12]!r}")
        c0 = doc.clean_of_norm[i]
        c1 = doc.clean_of_norm[min(j + len(end), len(doc.norm) - 1)]
        return {"lb": doc.lb_at(doc.raw_index(i)),
                "text": doc.clean[c0:c1 + len(end)].replace("\n", "").strip()}

    d4013 = tib_open("vol117", 4013, "འཇམ་དཔལ་གཞོན་ནུར")
    d4014 = tib_open("vol117", 4014, "སངས་རྒྱས་དང་བྱང་ཆུབ")
    pairs = [
        {
            "id": "twin_tikas",
            "title": "同题两部《行願王廣釋》（D4013/D4014）的归敬分辨",
            "non_buddhist": [d4013, d4014],
            "buddhist": [],
            "analysis": ("两部同题《行願王廣釋》（རྒྱ་ཆེར་འགྲེལ་པ）的归敬**对象不同**："
                        "D4013 归敬**文殊**（འཇམ་དཔལ་གཞོན་ནུར），D4014 归敬**一切佛"
                        "菩萨**（སངས་རྒྱས་དང་བྱང་ཆུབ་སེམས་དཔའ་ཐམས་ཅད་ལ）——"
                        "开篇第一句即证两者为**不同作者的两部独立注疏**"
                        "（题记记 D4013 释迦狮子造、D4014 智藏造），非同本异抄。"
                        "开篇形态作为「第四列题录」的又一应用：分辨同题作品。"
                        "〔本文判读〕"),
        },
        {
            "id": "bhadracari",
            "title": "行願讚同源异译：藏译解经框架 × 汉译纯颂",
            "non_buddhist": [tib_open("vol117", 4011, "ཀུན་དུ་བཟང་པོ་ལ་ཕྱག")],
            "buddhist": [cn(d297, "所有十方世界中", "以此普賢行願力")],
            "analysis": ("同一 Bhadracarī 的两种译态：D4011（བཤད་སྦྱར 注释本）先归敬"
                        "「顶礼普贤」，再立**「义略摄为十」**的解经框架（礼敬/供养/"
                        "忏悔……十支总纲），然后才入正文；T297（不空译）无归敬、"
                        "无框架，直接以「所有十方世界中」入颂——十支结构在汉译里"
                        "**藏在颂文次第中**，在藏译里被**显式提为纲目**。同源文本"
                        "的解经包装差异，是两系传承各自文本形态的第一手证据。"
                        "〔本文判读〕"),
        },
        {
            "id": "dashabhumika_open",
            "title": "十地经论同论异译：归敬文殊＋传承偈 × 朝廷序",
            "non_buddhist": [tib_open("vol113", 3993, "འཇམ་དཔལ་གཞོན་ནུར་གྱུར་པ་ལ་ཕྱག")],
            "buddhist": [cn(d1522, "十地經論序侍中崔光製", "莫不網羅於其中矣"),
                         cn(d1522, "如是我聞一時婆伽婆成道未久", "從他方佛世界俱來集會")],
            "analysis": ("同一部论（世親造十地经释）的两种开篇：D3993 藏译以"
                        "**归敬文殊**＋造论缘起偈开篇——偈文「此法门谁说、谁使说、"
                        "谁示义、谁从彼受、为我分别」把**传承链写进正文**；T1522 "
                        "汉译以北魏侍中**崔光所制朝廷序**开篇（「神覺之玄苑、靈慧之"
                        "妙宅」），继以经文如是我闻——译场形态（经院传承 vs 国家"
                        "工程）在开篇结构上直接可见，与 §17.19 S1（译场）、"
                        "§17.20 S2（王室）互证。〔本文判读〕"),
        },
    ]

    data = {
        "meta": {
            "date": date.today().isoformat(),
            "title": "丹珠尔内容层·第一步：同论异译开篇对读",
            "method": ("藏文侧以卷号＋字符位置回源（无 CBETA 式 lb）；汉文侧 lb 回源。"
                       "内容层从这里开始——仍是开篇对读，非逐部通读〔如实标注〕。"),
            "sources": {
                "t297": {"path": "data/references/cbeta/T10n0297.xml",
                         "sha256": sha256((ROOT / "data/references/cbeta/T10n0297.xml").read_bytes())},
                "t1522": {"path": "data/references/cbeta/T26n1522.xml",
                          "sha256": sha256((ROOT / "data/references/cbeta/T26n1522.xml").read_bytes())},
                "vol113": {"path": "data/references/tibetan/derge_tengyur/vol113.txt"},
                "vol117": {"path": "data/references/tibetan/derge_tengyur/vol117.txt"},
            },
        },
        "pairs": pairs,
    }
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n",
                   encoding="utf-8")
    for p in pairs:
        print(f"[{p['id']}]")
        for q in p["non_buddhist"] + p["buddhist"]:
            print("   ", q.get("lb", q.get("vol", "?")), q["text"][:60])
    print("written", OUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
