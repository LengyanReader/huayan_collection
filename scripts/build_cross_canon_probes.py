#!/usr/bin/env python3
"""Build the three §17 probes: T9 科判, D5 内核共享, P1 阶位.

Every quoted string is asserted to be a substring of the normalized source text
before it is written. If a source changes, this script fails instead of
silently shipping a quote that is no longer there.

Usage:
  python scripts/build_cross_canon_probes.py
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "research" / "cross_canon_probes.json"

SRC = {
    "T1735": ROOT / "data" / "references" / "cbeta" / "T35n1735.xml",
    "T1733": ROOT / "data" / "references" / "cbeta" / "T35n1733.xml",
    "T279": ROOT / "data" / "references" / "cbeta" / "T10n0279.xml",
    "DZ0001": ROOT / "data" / "references" / "daozang",
}


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def cbeta_plain(text: str) -> str:
    text = re.sub(r"<lb[^>]*/>", "", text)
    text = re.sub(r"<pb[^>]*/>", "", text)
    text = re.sub(r"<anchor[^>]*/>", "", text)
    return re.sub(r"<[^>]+>", "", text)


def daozang_plain() -> str:
    parts = []
    for p in sorted(SRC["DZ0001"].glob("KR5a0001_*.txt")):
        t = p.read_text(encoding="utf-8")
        t = re.sub(r"<pb:[^>]*>", "", t)
        t = t.replace("¶", "")
        parts.append(t)
    return "".join(parts)


def load() -> dict[str, str]:
    texts = {}
    for key in ("T1735", "T1733", "T279"):
        texts[key] = cbeta_plain(SRC[key].read_text(encoding="utf-8"))
    texts["DZ0001"] = daozang_plain()
    return texts


def need(texts: dict[str, str], src: str, quote: str) -> str:
    flat = re.sub(r"\s+", "", texts[src])
    q = re.sub(r"\s+", "", quote)
    if q not in flat:
        raise SystemExit(f"quote not found in {src}: {quote[:40]}…")
    return quote


def extract_shizhu(texts: dict[str, str]) -> list[str]:
    flat = re.sub(r"\s+", "", texts["T279"])
    m = re.search(r"所謂：([^。]*?灌頂住)。", flat)
    if not m:
        raise SystemExit("十住 name list not found")
    return m.group(1).split("、")


def extract_shidi(texts: dict[str, str]) -> list[str]:
    flat = re.sub(r"\s+", "", texts["T279"])
    m = re.search(r"何等為十？(一者歡喜地.*?十者法雲地)。", flat)
    if not m:
        raise SystemExit("十地 name list not found")
    names = re.findall(r"[一二三四五六七八九十]者([^，。]+?地)", m.group(1))
    if len(names) != 10:
        raise SystemExit(f"十地 names parsed {len(names)} != 10")
    return names


def main() -> int:
    texts = load()

    # ---------------- T9: 科判 ----------------
    t9_quotes = [
        ("T1735", "C1", "一品分二：初長行散說、後偈頌總攝。"),
        ("T1735", "C2", "初長行中二：先正說十地、後「爾時復以」下菩薩證成。"),
        ("T1735", "C3", "或為三分，為序、正、流通。"),
        ("T1733", "C4", "或為六者，隨行以分，初至起分是起化之由為生物信"),
        ("T1733", "C5", "或為七者，從初至請即為六分，說分通十總為第七。"),
        ("T1733", "C6", "或為四十八者，初地第十各八分、二地二分"),
        ("T1733", "C7", "十種地內總有四百八十分可知。"),
    ]
    t9b_quotes = [
        ("T1735", "E1", "文為七分：一加分、二本分、三請分、四說分、五顯名受持分、六表瑞證成分、七偈頌總攝分。"),
        ("T1735", "E2", "平等出現為宗，融差別果為趣。"),
        ("T1735", "E3", "是以晉經名性起"),
        ("T1733", "E4", "此品長分為七：一加分、二本分、三請分、四說分、五顯名受持分、六表瑞證成分、七偈頌總攝分。"),
        ("T1733", "E5", "前品明能發之因，今辨所顯之果，故次來也。"),
        ("T1733", "E6", "明性起法門，即以為宗。"),
    ]
    t9c_quotes = [
        ("T1735", "F1", "一品大分為二：初明本會、二「爾時文殊師利從善住樓閣出」下明末會。"),
        ("T1735", "F2", "就本會中，長科十分：一序分、二請分、三三昧現相分、四遠集新眾分、五舉失顯得分、六偈頌讚德分、七普賢開發分、八毫光示益分、九文殊述德分"),
        ("T1735", "F3", "大文第十「爾時彼諸」下無涯大用分。"),
        ("T1733", "F4", "此一品中大分有二：初明本會；二「爾時文殊從善住樓閣出已」下明末會。"),
        ("T1733", "F5", "就前本會中長分有十：一序分、二請分、三三昧分、四現淨土分、五集新眾分、六舉劣顯勝分、七偈頌讚德分、八普賢開發分、九毫光示益分、十文殊述德分。"),
    ]
    for src, _, q in t9_quotes + t9b_quotes + t9c_quotes:
        need(texts, src, q)

    t9 = {
        "title": "T9 科判：澄觀《疏》與法藏《探玄記》",
        "cases": [
            {
                "pin": "〈十地品〉（八十 品26／六十 品22）",
                "rows": [
                    ("所释品次", "八十华严 品26（T1735 卷31–34）", "六十华严 品22（T1733 卷9–14）"),
                    ("分科锚点", "文便：先分长行／偈颂", "行相：先分序至地利益"),
                    ("基准科数", "2（长行、偈颂）", "6（序、本分、请分、说分、影像、利益）"),
                    ("可选科数", "1／2／3（教三、证三）／4", "2／3／4／5／6／7／8／9／10"),
                    ("地内细科", "本段只列品级分科", "48 分／地，总 480 分"),
                    ("依据", "疏文自述", "《地论》科文四例"),
                ],
                "quotes": [{"src": s, "id": i, "text": q} for s, i, q in t9_quotes],
                "finding": "同释一品，两家都以「多种分科并存」为方法，但锚点不同：澄观先依文便切长行／偈颂，再逐层二分；法藏先依行相切六分，再展为十，并以四十八分细分地内。科判差异不构成文本差异。",
                "limits": "两家品次不同（26／22）是六十与八十的编次差，不是内容差。",
            },
            {
                "pin": "〈如來出現品〉（八十 品37／六十 品32 性起品）",
                "rows": [
                    ("所释品次", "八十华严 品37（经卷50–52；疏卷49–50）", "六十华严 品32（T1733 卷16–17）"),
                    ("分科锚点", "七分：加→本→请→说→显名受持→表瑞证成→偈颂", "七分：同名同序"),
                    ("基准科数", "7", "7"),
                    ("可选科数", "本段未见另说", "本段未见另说"),
                    ("品名取舍", "晋译作「性起」，此本作「出现」", "「性起」为本名，别译作秘密藏、兴显"),
                    ("依据", "疏文自述", "记文自述"),
                ],
                "quotes": [{"src": s, "id": i, "text": q} for s, i, q in t9b_quotes],
                "finding": "这一品两家完全同科：七分同名同序，措辞几乎逐字相同。与〈十地品〉的 2 对 6 恰成反照——科判的异同取决于所承的注释传统，不是经文本身的属性。",
                "limits": "只核名目与次序，未逐段核对七分在两本的实际落点；同科不等于证明袭用（无直接引用语）。",
            },
            {
                "pin": "〈入法界品〉（八十 品39／六十 品34）",
                "rows": [
                    ("所释品次", "八十华严 品39（经卷60–80；疏卷54起）", "六十华严 品34（T1733 卷18起）"),
                    ("分科锚点", "本会／末会二分 → 本会长科十分", "同：本会／末会二分 → 本会长分十"),
                    ("基准科数", "2；本会 10", "2；本会 10"),
                    ("分合差异", "「现净土」并入「三昧现相」；末另立「无涯大用」", "「现净土」独立为第四；「文殊述德」收尾"),
                    ("依据", "疏文自述", "记文自述"),
                ],
                "quotes": [{"src": s, "id": i, "text": q} for s, i, q in t9c_quotes],
                "finding": "科数同为 2 与 10，但分合不同：澄观把「现净土」并入三昧现相，又在末尾另立「无涯大用」，故十名中两处错位；法藏以「现净土」独立、以「文殊述德」收尾。与〈出现品〉的全同、〈十地品〉的 2 对 6 合看，科判至少有三种关系：全同、同数异分合、异数。",
                "limits": "只核本会十分；末会（五十三参）两家的分段未做。品次 39／34 为编次差，不是内容差。",
            },
        ],
    }


    # ---------------- D5: 内核共享 ----------------
    d5_quotes = [
        ("T279", "H1", "若人欲了知，三世一切佛，應觀法界性，一切唯心造。"),
        ("T279", "H2", "心如工畫師，能畫諸世間，五蘊悉從生，無法而不造。"),
        ("T279", "H3", "於一微塵中，悉見諸世界"),
        ("T279", "H4", "雖勤度一切眾生，而離眾生想"),
        ("DZ0001", "D1", "混元無名非濁非清分爲兩半素玄肇平"),
        ("DZ0001", "D2", "太極一氣分化判爲三辰離爲八景"),
        ("DZ0001", "D3", "一炁既闢萬化通流離合隂陽"),
        ("DZ0001", "D4", "度人无量爲萬道之宗"),
    ]
    for src, _, q in d5_quotes:
        need(texts, src, q)
    counts = {
        "微塵": {"T279": texts["T279"].count("微塵"), "DZ0001": texts["DZ0001"].count("微塵")},
        "法界": {"T279": texts["T279"].count("法界"), "DZ0001": texts["DZ0001"].count("法界")},
        "混元": {"T279": texts["T279"].count("混元"), "DZ0001": texts["DZ0001"].count("混元")},
    }
    d5 = {
        "title": "內核命題對位：《華嚴》T279 與《度人經》DZ0001",
        "rows": [
            ("本源（萬法所依）", "應觀法界性，一切唯心造", "混元無名非濁非清分爲兩半素玄肇平",
             "功能同位，術語不共享（法界／心 vs 混元）", "类型"),
            ("生成（世間成立）", "心如工畫師，能畫諸世間", "太極一氣分化判爲三辰離爲八景",
             "同為生成論，主動因不同（心 vs 氣）", "类型"),
            ("相即（一多／微塵）", "於一微塵中，悉見諸世界", "無對應（「微塵」0 見）",
             "不成立：道經無一多相即命題", "不成立"),
            ("救度（拔苦）", "雖勤度一切眾生，而離眾生想", "度人无量爲萬道之宗",
             "功能類比：皆以「度」為宗，但不構成本文依賴", "类型"),
        ],
        "counts": counts,
        "quotes": [{"src": s, "id": i, "text": q} for s, i, q in d5_quotes],
        "finding": "四項中三項只有功能位同構，一項（一多相即）在《度人經》完全無對應。故「內核共享」只到類型層，且限於本源／生成／救度三個功能位；不足以稱同源。",
        "limits": "道藏只取《度人經》一部；未取《道教義樞》《無上秘要》等教義書，故不能代表整個道教。",
    }

    # ---------------- P1: 阶位 ----------------
    shizhu = extract_shizhu(texts)
    shidi = extract_shidi(texts)
    if len(shizhu) != 10:
        raise SystemExit(f"十住 names parsed {len(shizhu)} != 10")
    p1_quotes = [
        ("T1735", "P1", "有別行譯本名十住經，住是地中一義故。"),
        ("T1733", "P2", "三更別譯一本名十住經"),
    ]
    for src, _, q in p1_quotes:
        need(texts, src, q)
    p1 = {
        "title": "十住與十地：同一階位還是兩套階位",
        "rows": [(i + 1, shizhu[i], shidi[i]) for i in range(10)],
        "name_overlap": sorted(set(shizhu) & set(shidi)),
        "quotes": [{"src": s, "id": i, "text": q} for s, i, q in p1_quotes],
        "finding": "十住十名與十地十名無一重合；兩套階位各自成組。但《疏》《記》都指出別行譯本題作《十住經》，理由是「住是地中一義」——題名重疊來自義訓，不來自同一階位。",
        "limits": "只做佛教內部（華嚴自宗）兩套階位；道教階次無一手文本，跨傳統一半仍缺。",
    }
    if p1["name_overlap"]:
        raise SystemExit(f"十住/十地 name overlap unexpected: {p1['name_overlap']}")

    sources = {}
    for k in SRC:
        if k == "DZ0001":
            raw = b"".join(p.read_bytes() for p in sorted(SRC[k].glob("KR5a0001_*.txt")))
        else:
            raw = SRC[k].read_bytes()
        sources[k] = {
            "path": str(SRC[k].relative_to(ROOT)).replace("\\", "/"),
            "sha256": sha256(raw),
        }

    data = {
        "meta": {
            "date": date.today().isoformat(),
            "method": "逐條引文在正規化底本中做子字串校驗；名稱表由 T279 原文正則抽取。",
            "sources": sources,
        },
        "t9": t9,
        "d5": d5,
        "p1": p1,
    }
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"written {OUT}")
    nq = sum(len(c["quotes"]) for c in t9["cases"])
    print(f"  T9 cases {len(t9['cases'])} ({nq} quotes); D5 rows {len(d5['rows'])}; P1 rows {len(p1['rows'])}")
    print(f"  counts: {counts}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
