#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""《丹珠尔》华严命中逐条定性——题录层的加深（内容层仍空，如实标注）。

数据源（均一手、已入库）：
  · works 头行：data/references/tibetan/derge_tengyur/（题名＋梵语题记原样截取）
    ——经 build_tanjur_catalog.py 抽取，见 data/research/tanjur_catalog.json
  · dkar chag：data/references/tibetan/derge_tengyur/vol213_dkarchag.txt
    ——目录条目含造者＋译场原样截取（442b.6／443a／443a.2／216b.5 四条）

定性内容：
  · 体裁（经释／再释／序品别释／赞／摄义／广释）——由题名直译得出，标〔本文判读〕；
  · 造者／译场——照录 dkar chag（藏文原文入 JSON，不转译作断言）；
  · 汉译对应——T1522（世親十地经论）、T297（普贤菩萨行愿赞）两条有据（题名＋
    造者互证，B）；其余无汉译（负向如实）。

Usage: python scripts/build_tanjur_qual.py
"""
from __future__ import annotations

import hashlib
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "research" / "tanjur_qual.json"

DC = ROOT / "data/references/tibetan/derge_tengyur/vol213_dkarchag.txt"


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


# 逐条定性（体裁与汉译对应为〔本文判读〕；造者照录 dkar chag 原文）
QUAL = [
    {
        "D": 3993, "vol": 113, "line": "十地",
        "title_zh": "《聖十地經之釋》（འཕགས་པ་ས་བཅུ་པའི་རྣམ་པར་བཤད་པ）",
        "genre": "经释",
        "genre_basis": "题名直译〔本文判读〕",
        "author_dkarchag": ("སློབ་དཔོན་དབྱིག་གཉེན་གྱིས་མཛད་པ（世親造）；"
                            "译场：མཉྫུ་ཤྲཱི་གརྦྷ（妙吉祥藏）、པྲཛྙཱ་ཝརྨ（般若波羅蜜）勘梵，"
                            "ཡེ་ཤེས་སྡེ（智军）、དཔལ་བརྩེགས（吉祥积）译——dkar chag 442b.6"),
        "dkarchag_folio": "442b.6",
        "han_correspond": "T1522《十地經論》（菩提流支等译，世親造）——题名＋造者互证，B",
        "han_level": "B",
    },
    {
        "D": 3998, "vol": 116, "line": "十地",
        "title_zh": "《十地釋之釋》（ས་བཅུའི་རྣམ་པར་བཤད་པའི་རྣམ་པར་བཤད་པ）",
        "genre": "再释（释世親论之疏）",
        "genre_basis": "题名叠构「釋之釋」直译〔本文判读〕",
        "author_dkarchag": ("世親釋之「འགྲེལ་བཤད」、སློབ་དཔོན་ཉི་མ་གྲུབ（日成）造；"
                            "པྲཛྙཱ་ཝརྨ（般若波羅蜜）勘梵、དཔལ་བརྩེགས་རཀྵི་ཏ（吉祥积护）译"
                            "——dkar chag 443a"),
        "dkarchag_folio": "443a",
        "han_correspond": "无汉译（负向）",
        "han_level": "A（负向：目录层面查无）",
    },
    {
        "D": 3999, "vol": 116, "line": "十地",
        "title_zh": "《聖十地經序品之釋》（འཕགས་པ་ས་བཅུའི་མདོ་སྡེའི་གླེང་གཞི་བཤད་པ）",
        "genre": "序品别释（仅释 gleng gzhi 序分）",
        "genre_basis": "题名直译〔本文判读〕；dkar chag 443a.2 作 གླེང་བཞི（异写照录，不统一）",
        "author_dkarchag": "སློབ་དཔོན་ཤཱཀྱའི་བློ（释迦慧）造——dkar chag 443a.2",
        "dkarchag_folio": "443a.2",
        "han_correspond": "无汉译（负向）",
        "han_level": "A（负向：目录层面查无）",
    },
    {
        "D": 4011, "vol": 117, "line": "行愿",
        "title_zh": "《聖普賢行願王大讚》（འཕགས་པ་བཟང་པོ་སྤྱོད་པའི་སྨོན་ལམ་གྱི་རྒྱལ་པོ་ཆེན་པོའི་བཤད་སྦྱར）",
        "genre": "赞（Bhadracarī 藏译）",
        "genre_basis": "题名直译〔本文判读〕",
        "author_dkarchag": "dkar chag 216b.5 行愿条目群（含萨班诸作）原样截取，本品造者无题记",
        "dkarchag_folio": "216b.5",
        "han_correspond": "T297《普賢菩薩行願贊》（不空译）／T293 卷四十末偈——题名互证，B",
        "han_level": "B",
    },
    {
        "D": 4012, "vol": 117, "line": "行愿",
        "title_zh": "《普賢行願義總攝》（ཀུན་དུ་བཟང་པོའི་སྤྱོད་པའི་སྨོན་ལམ་གྱི་དོན་ཀུན་བསྡུས）",
        "genre": "摄义（颂体）",
        "genre_basis": "题名直译〔本文判读〕",
        "author_dkarchag": ("dkar chag 216b.5 行愿条目：「བསྡུས་དོན་ཚིགས་སུ་བཅད་པ་"
                            "ས་པཎ་གྱིས་མཛད」（摄义颂·萨班造）〔条目对应为本文判读〕"),
        "dkarchag_folio": "216b.5",
        "han_correspond": "无汉译（负向）",
        "han_level": "A（负向：目录层面查无）",
    },
    {
        "D": 4013, "vol": 117, "line": "行愿",
        "title_zh": "《聖普賢行願王廣釋》（འཕགས་པ་བཟང་པོ་སྤྱོད་པའི་སྨོན་ལམ་གྱི་རྒྱལ་པོའི་རྒྱ་ཆེར་འགྲེལ་པ）",
        "genre": "广释（རྒྱ་ཆེར་འགྲེལ་པ＝ṭīkā）",
        "genre_basis": "题名直译〔本文判读〕",
        "author_dkarchag": "题记未见造者〔待核〕",
        "dkarchag_folio": "216b.5（条目群）",
        "han_correspond": "无汉译（负向）",
        "han_level": "A（负向：目录层面查无）",
    },
    {
        "D": 4014, "vol": 117, "line": "行愿",
        "title_zh": "《聖普賢行願王廣釋》（同题异本，与 4013 同题）",
        "genre": "广释（同题第二部）",
        "genre_basis": "题名直译〔本文判读〕；与 4013 关系（异译？异本？）未核〔待核〕",
        "author_dkarchag": "题记未见造者〔待核〕",
        "dkarchag_folio": "216b.5（条目群）",
        "han_correspond": "无汉译（负向）",
        "han_level": "A（负向：目录层面查无）",
    },
    {
        "D": 4015, "vol": 117, "line": "行愿",
        "title_zh": "《聖普賢行願之釋》（འཕགས་པ་བཟང་པོ་སྤྱོད་པའི་སྨོན་ལམ་གྱི་འགྲེལ་པ）",
        "genre": "释（无「廣」字，与 4013/4014 体例有别）",
        "genre_basis": "题名直译〔本文判读〕",
        "author_dkarchag": "题记未见造者〔待核〕",
        "dkarchag_folio": "216b.5（条目群）",
        "han_correspond": "无汉译（负向）",
        "han_level": "A（负向：目录层面查无）",
    },
]


def main() -> int:
    data = {
        "meta": {
            "date": date.today().isoformat(),
            "title": "《丹珠尔》华严命中逐条定性（题录层加深）",
            "method": ("体裁＝题名直译〔本文判读〕；造者／译场＝dkar chag 条目原文照录"
                       "（藏文入 JSON，不断言转译）；汉译对应＝题名＋造者互证者判 B，"
                       "查无者判负向。释论全文未读，内容层仍空——如实标注。"),
            "dkarchag": {"path": str(DC.relative_to(ROOT)).replace("\\", "/"),
                         "sha256": sha256(DC.read_bytes()),
                         "bytes": DC.stat().st_size},
            "catalog_ref": "data/research/tanjur_catalog.json",
        },
        "works": QUAL,
        "summary": {"works": len(QUAL),
                    "genres": {"经释": 1, "再释": 1, "序品别释": 1,
                               "赞": 1, "摄义": 1, "广释": 2, "释": 1}},
    }
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n",
                   encoding="utf-8")
    print("written", OUT)
    for w in QUAL:
        print(f"  D{w['D']} vol{w['vol']} [{w['genre']}] {w['title_zh'][:36]}"
              f" ↔ {w['han_correspond'][:40]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
