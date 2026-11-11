#!/usr/bin/env python3
"""Build enrichment data for the canon-mapping article.

Sources:
  - data/research/huayan_80_40_duikandu_b1..b10.json (品39 vs T293 segmental reading)
  - CBETA T285/T286/T278/T279/T287 (ten bhūmi names, each text's own list)
  - data/alignment/tibetan-derge-toc.json (45 chapters: vol/folio/status)
  - four commentary OCR texts (name mentions, NOT book-title citations)
  - data/research/rufajie_53_dataset.json (53-visit counts)

Output: data/research/dazang_enrichment.json
"""

from __future__ import annotations

import glob
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "research" / "dazang_enrichment.json"

TEXTS = {
    "T1732": "data/references/cbeta_txt/T1732_智俨_搜玄记.txt",
    "T1733": "data/references/cbeta_txt/T1733_法藏_探玄记.txt",
    "T1735": "data/references/cbeta_txt/T1735_澄观_华严经疏.txt",
    "T1736": "data/references/cbeta_txt/T1736_澄观_随疏演义钞.txt",
}

# Ten bhūmis exactly as each text lists them. T285 uses 十住/道地 vocabulary.
BHUMI = [
    ("初地 欢喜", "Pramuditā", "悅豫（初發意悅豫住）", "歡喜地", "歡喜地", "歡喜地", "極喜地"),
    ("二地 离垢", "Vimalā", "離垢", "離垢地", "離垢地", "離垢地", "離垢地"),
    ("三地 发光", "Prabhākarī", "興光", "明地", "明地", "發光地", "發光地"),
    ("四地 焰慧", "Arciṣmatī", "暉曜", "焰地", "焰地", "焰慧地", "焰慧地"),
    ("五地 难胜", "Sudurjayā", "難勝", "難勝地", "難勝地", "難勝地", "難勝地"),
    ("六地 现前", "Abhimukhī", "目見", "現前地", "現前地", "現前地", "現前地"),
    ("七地 远行", "Dūraṃgamā", "玄妙", "遠行地", "遠行地", "遠行地", "遠行地"),
    ("八地 不动", "Acalā", "不動", "不動地", "不動地", "不動地", "不動地"),
    ("九地 善慧", "Sādhumati", "善哉意", "善慧地", "善慧地", "善慧地", "善慧地"),
    ("十地 法云", "Dharmameghā", "法雨", "法雲地", "法雲地", "法雲地", "法雲地"),
]

MENTION_KEYS = [
    ("瑜伽論", ["瑜伽論", "瑜伽師地"]),
    ("涅槃經", ["涅槃經"]),
    ("智度論", ["智度論"]),
    ("成唯識論", ["成唯識論", "唯識論"]),
    ("攝大乘論", ["攝大乘論", "攝論"]),
    ("瓔珞經", ["瓔珞"]),
    ("寶性論", ["寶性論"]),
]


def tib_pin(n: int) -> str:
    """Map a Derge chapter (Toh 44) to the 80-fascicle pin number.

    Anchored on each chapter's own colophon in
    data/references/tibetan/derge_kangyur/avatamsaka/035-038_*.txt:
      1-4   -> 1-4    (1:1)
      5-9   -> 5      (Hua-zang world split into five chapters)
      10    -> 6      (རྣམ་པར་སྣང་མཛད་ཀྱི་ལེའུ, Vairocana)
      11    -> none   (དེ་བཞིན་གཤེགས་པ་རྨད་ག་ཅད, no Chinese counterpart)
      12-31 -> 7-26   (31 = ས་བཅུའི་ལེའུ, Ten Bhumis)
      32    -> none   (ཀུན་ཏུ་བཟང་པོས་བསྟན་པ, T298 is its Chinese witness)
      33-45 -> 27-39  (33 = ཏིང་ངེ་འཛིན་བཅུ, Ten Samadhis)
    """
    if 1 <= n <= 4:
        return str(n)
    if 5 <= n <= 9:
        return "5"
    if n == 10:
        return "6"
    if n in (11, 32):
        return "汉无"
    if 12 <= n <= 31:
        return str(n - 5)
    return str(n - 6)


def main() -> int:
    payload = {}
    rows = []
    for p in sorted(glob.glob(str(ROOT / "data/research/huayan_80_40_duikandu_b*.json")),
                    key=lambda x: int(re.search(r"_b(\d+)\.json$", x).group(1))):
        d = json.loads(Path(p).read_text(encoding="utf-8"))
        # Some batches record comparison items under other keys than "windows"
        # (e.g. b6 speaker_table, b13 gate_name_40/gate_pairs): keep the shape so
        # the table can say so instead of printing a misleading 0.
        if d.get("windows"):
            kind = "windows"
        elif d.get("speaker_table"):
            kind = "说主对照表"
        elif d.get("gate_pairs") or d.get("gate_name_40"):
            kind = "门名／门对"
        else:
            kind = "其他记录"
        rows.append({
            "batch": d.get("batch", ""),
            "date": d.get("date", ""),
            "kind": kind,
            "windows": len(d.get("windows", [])),
            "finding": d.get("finding", ""),
        })
    payload["forty"] = {
        "batches": rows,
        "windows_total": sum(r["windows"] for r in rows),
        "structure": {
            "T293": "40 卷 · 1 品（入法界）· 卷40 普贤行愿",
            "T279": "80 卷 · 品39（入法界）占卷60–80",
            "note": "T293 为单品全本，具完整序分；T279 品39 为全经末品，无新序",
        },
    }

    payload["bhumi"] = [
        {"name": n, "sa": sa, "T285": t285, "T286": t286, "T278": t278, "T279": t279, "T287": t287}
        for n, sa, t285, t286, t278, t279, t287 in BHUMI
    ]

    toc = json.loads((ROOT / "data/alignment/tibetan-derge-toc.json").read_text(encoding="utf-8"))
    payload["tib45"] = [
        {
            "no": c["no"], "vol": c.get("vol", ""), "folio": c.get("start_folio", ""),
            "pin": tib_pin(c["no"]), "status": c.get("alignment_status", ""),
        }
        for c in toc.get("toc", [])
    ]

    mentions = []
    for label, variants in MENTION_KEYS:
        row = {"label": label, "variants": variants}
        total = 0
        for t, path in TEXTS.items():
            body = (ROOT / path).read_text(encoding="utf-8")
            n = sum(body.count(v) for v in variants)
            row[t] = n
            total += n
        row["total"] = total
        mentions.append(row)
    payload["mentions"] = {
        "note": "OCR 文本中的名称提及次数（字符串匹配），不是书名号引文；只能作代理指标。",
        "rows": mentions,
    }

    d53 = json.loads((ROOT / "data/research/rufajie_53_dataset.json").read_text(encoding="utf-8"))
    payload["rufajie53"] = {"meta": d53.get("meta", {}), "stats": d53.get("stats", {}), "visits": len(d53.get("visits", []))}

    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({
        "forty_batches": len(rows), "forty_windows": payload["forty"]["windows_total"],
        "bhumi_rows": len(payload["bhumi"]), "tib_chapters": len(payload["tib45"]),
        "mention_rows": len(mentions), "visits": payload["rufajie53"]["visits"],
    }, ensure_ascii=False, indent=2))
    print(f"written {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())