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
    "KR5e0031": ROOT / "data" / "references" / "daozang",
    "KR1h0015": ROOT / "data" / "references" / "rujia",
    "yogasutra": ROOT / "data" / "references" / "sanskrit" / "yogasutra_with_bhashya.txt",
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
    parts = []
    for p in sorted(SRC["KR5e0031"].glob("KR5e0031_*.txt")):
        t = p.read_text(encoding="utf-8")
        t = re.sub(r"<pb:[^>]*>", "", t)
        t = t.replace("¶", "")
        parts.append(t)
    texts["KR5e0031"] = "".join(parts)
    dx = SRC["KR1h0015"]
    parts = []
    for p2 in sorted(dx.glob("KR1h0015_*.txt")):
        t2 = p2.read_text(encoding="utf-8")
        t2 = re.sub(r"<pb:[^>]*>", "", t2)
        t2 = t2.replace("¶", "")
        parts.append(t2)
    texts["KR1h0015"] = "".join(parts)
    texts["yogasutra"] = SRC["yogasutra"].read_text(encoding="utf-8")
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

    # ---------------- T9 逐品科判（§17.30 起） ----------------
    t9p_quotes = [
        ("T1735", "P1", "今有三十九品，初會有六品；彼經唯三十四，由初會中唯有二品：一〈世間淨眼品〉，即今〈世主品〉；二〈盧舍那品〉，即今〈現相〉已下五品。"),
        ("T1735", "P2", "就第一舉果分中，或科為十：一教起因緣分，即初一品；二大眾同請分、三面光集眾分、四毫光示法分、五眉間出眾分，已上在第二品內；六普賢三昧分、七諸佛同加分、八法主起定分、九大眾重請分，已上在第三品內；十正陳法海分，在後三品內。"),
        ("T1735", "P3", "若以義從文，且分為三：一教起因緣分、二〈現相〉下說法儀式分、三〈世界成就〉下正陳所說分。"),
        ("T1735", "P4", "就初分中亦分為十：一總顯已聞、二「一時」下標主時處、三「始成正覺」別明時分、四「其地」下別顯處嚴、五「爾時世尊」下教主難思、六「有十佛世界」下眾海雲集、七從「爾時如來道場」下稱揚讚德、八「爾時如來師子座」下座內眾流、九「爾時華藏」下天地徵祥、十「如此世界」下結通無盡。"),
        ("T1735", "P5", "序中，就文分二：初此土序、二結通十方無盡世界序。初中復二：初證信序、後「爾時如來道場」下發起序。"),
        ("T1733", "P6", "於中有三十四品：初一品是序分，〈盧舍那品〉下明正宗。"),
        ("T1733", "P7", "今更尋下文，總長分為五：初品是教起因緣分；二〈舍那品〉中一周問答，名舉果勸樂生信分；三從第二會至第六會來一周問答，名修因契果生解分；四第七會中一周問答，名託法進修成行分；五第八會中一周問答，名依人入證成德分。"),
        ("T1733", "P8", "就初序分之中，分為二：初明此土中序分、二明十方無盡世界中序分。初中有三：初有四字，唯是證信；二「一時」下，通二序；三「動地」下，唯是發起。"),
        ("T1733", "P9", "又依《佛地論》分為五：一總顯已聞、二教起時、三顯教主、四教起處、五教所被機。依《法華論》等，有六成就："),
        ("T1733", "P10", "上來三段總明器世間圓滿竟。自下第三明智正覺世間圓滿。於中略作五門料簡：一定佛身、二明融攝、三顯差別、四表示法、五釋本文。"),
        ("T1733", "P11", "大段第二明眾生世間圓滿。於中先總料簡、後釋本文。初中略作十門分別：一明眾數、二新舊、三定器、四世出世、五界趣、六諸乘、七權實、八位地、九表法、十因果。"),
        ("T1733", "P12", "發起序，於中有二：初動地、二興供。"),
        ("T1733", "P13", "明結通十方，以一會即一切會，顯教圓滿，攝主伴故。"),
    ]
    for src, _, q in t9p_quotes:
        need(texts, src, q)
    t9_pin = {
        "title": "T9 科判逐品：八十品1〈世主妙嚴品〉／六十品1〈世間淨眼品〉",
        "cases": [
            {
                "pin": "〈世主妙嚴品〉（八十 品1／六十 品1 世間淨眼品）",
                "rows": [
                    ("所释品次", "八十华严 品1（疏卷4–8 释文；卷1–3 通论）", "六十华严 品1（T1733 卷2，尽世间净眼品）"),
                    ("会级五分", "五周因果：初会六品共为一周（所信因果）；品1 是其中十科之首「教起因缘分」", "教起→举果→修因→託法→依人：初品自成一分「教起因缘分」"),
                    ("品级科数", "10（总显已闻→结通无尽，自述）", "无品级定数；自述序分二、此土序三、佛地论五、六成就"),
                    ("序分切法", "序分二（此土序／十方序）；此土序复二（证信序／发起序）", "序分二（此土序／十方序）；此土序三（证信／通二序／发起）"),
                    ("品内主段", "十分以「如是」起、「如此世界」结", "序分→器世间（三段）→智正觉世间（五门）→众生世间（十门）→发起序→结通"),
                    ("依据", "十例科判、五分、三分并存（疏文自述）", "五分、三分、佛地论五事、法华论六成就（记文自述）"),
                ],
                "quotes": [{"src": s, "id": i, "text": q} for s, i, q in t9p_quotes],
                "finding": "同释初会首品，两家都把它判在「序分」位，且都承认「多种分科并存」；但「五分」同名而异实：澄观以五周因果切，初会六品共为一周，品1 只是其中十科之首「教起因缘分」；法藏以教起—举果—修因—託法—依人五门切，品1 自成一分。落到品级，澄观给品1 一个整齐的十分（总显已闻→结通无尽），法藏不给品级定数，只在品内按序分（此土／十方）→器世间→智正觉世间→众生世间→发起序→结通分段。差异在切法层级，不在经文；科判异同不得写成文本异同。",
                "limits": "两家所据本不同（八十／六十），品次同为 1，起讫亦相当：六十品1 终「结通十方」，八十品1 终「悉亦如是」。但「十分」与「诸段」不可互推——科数不同不等于经文有增减。本表只对品级分科；品内子科（如四十众逐一列名、器世间三段十门）未逐条对照。法藏文中「大段第二」「自下第三」的自计数不在本表判内。",
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
    # ---- D5 扩展：道教義樞·法身義 的三身/四德（佛教内核的结构性借用） ----
    dj_d5_quotes = [
        ("KR5e0031", "D5",
         "三稱者一者道身二者真身三者報身一道身者太平經云道無不導道無不生度人經云唯道爲身"),
        ("KR5e0031", "D5",
         "跡三名者一者應身二者分身三者化身一應身者應是應接謂隨機顯跡應接群生"),
        ("KR5e0031", "D5",
         "何謂四一者常存二者快樂三者自在四者清淨常存者謂湛然安住不遷不動不爲無常無常所動"),
    ]
    for src, _, q in dj_d5_quotes:
        need(texts, src, q)
    d5_daojiao = {
        "source": "道教義樞·法身義第二（唐孟安排，KR5e0031 卷一）",
        "kernel": {
            "三身（本三稱）": ["道身", "真身", "報身"],
            "三身（跡三名）": ["應身", "分身", "化身"],
            "四德": ["常存", "快樂", "自在", "清淨"],
        },
        "quotes": [{"src": s, "id": i, "text": q} for s, i, q in dj_d5_quotes],
        "kernel_overlap": ["三身结构（道身/真身/報身 + 應/分/化）",
                           "四德（常樂我淨的道教对应：常存/快樂/自在/清淨）"],
        "finding": "《道教義樞·法身義》的本跡三身与四德框架与佛教法身说结构性同构——"
                   "且以《本際經》《度人經》《太平經》为典据，是唐初道教义学对佛教内核的"
                   "系统吸收（孟安排书成于武周-开元间）。这是 D5 迄今最强的一组内核同构："
                   "不是孤立词 shared，而是整套范畴框架被移植。",
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
        "limits": "道藏取《度人經》一部＋《道教義樞》法身義（見 daojiao 塊）；《無上秘要》等仍未取。",
        "daojiao": d5_daojiao,
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

    # ---- 道教半边：《道教義樞·位業義》（KR5e0031 卷一，一手文本） ----
    dj_quotes = [
        ("KR5e0031", "P1",
         "位業者登仙學道階業不同證果成真高卑有别三乘七號從此可明十轉九宫因兹用辯"),
        ("KR5e0031", "P1",
         "名乃有七位乃有三一者仙位二者真位三者聖位神道賢靈更無别位名號雖異猶附三階"),
        ("KR5e0031", "P1",
         "證位品者始自發心終乎極道大有五位一者發心二者伏道三者知真四者出離五者無上道"),
        ("KR5e0031", "P1",
         "太清仙九品上清真九品玉清聖九品三九二十七品同脩平等俱入一乘"),
    ]
    for src, _, q in dj_quotes:
        need(texts, src, q)
    dj_stage_names = ["神人", "真人", "仙人", "道人", "聖人", "賢人", "靈人"]
    dj_overlap = sorted(set(dj_stage_names) & (set(shizhu) | set(shidi)))
    p1_daogiao = {
        "source": "道教義樞·位業義第四（唐孟安排，KR5e0031 卷一，Kanripo）",
        "stage_system": {
            "七号": dj_stage_names,
            "三阶": ["仙位", "真位", "聖位"],
            "五心": ["發心", "伏道", "知真", "出離", "無上道"],
            "四位": ["十轉位", "九宫位", "三清位", "極果位"],
            "九宫": ["地仙三品（下三宫）", "天仙三品（中三宫）", "飛仙三品（上三宫）"],
            "三清二十七品": "太清仙九品・上清真九品・玉清聖九品（三九同用上高大神仙玄真天靈至九名）",
            "禀生位": "界内三十二品（三界四民）＋界外二十七品（三清一乘）",
        },
        "quotes": [{"src": s, "id": i, "text": q} for s, i, q in dj_quotes],
        "name_overlap_with_buddhist": dj_overlap,
    }

    # ---- 跨传统扩读：儒家八条目（大學）＋瑜伽八支 ----
    kx_quotes = [
        ("KR1h0015", "P1", "欲治其國者先齊其家欲齊其家者先脩其身"),
        ("KR1h0015", "P1", "致知在格物"),
        ("yogasutra", "P1",
         "yogāṅgāny avadhāryante --- yamaniyamāsanaprāṇāyāmapratyāhāradhāraṇādhyānasamādhayo 'ṣṭāv aṅgāni"),
        ("yogasutra", "P1", "śaucasaṃtoṣatapaḥsvādhyāyeśvarapraṇidhānāni niyamāḥ"),
    ]
    for src, _, q in kx_quotes:
        need(texts, src, q)
    p1_kuax = {
        "source_rujia": "大學（宋朱熹章句，KR1h0015，Kanripo）",
        "source_yoga": "Patañjali Yogasūtra with Bhāṣya（GRETIL，Maas 校订本）",
        "badia": ["格物", "致知", "誠意", "正心", "脩身", "齊家", "治國", "平天下"],
        "bazhi": ["yama", "niyama", "āsana", "prāṇāyāma", "pratyāhāra",
                  "dhāraṇā", "dhyāna", "samādhi"],
        "quotes": [{"src": s, "id": i, "text": q} for s, i, q in kx_quotes],
        "name_overlap_with_buddhist": [],
        "finding": "四地階梯（佛教十住十地／道教三阶七号五心／儒家八条目／瑜伽八支）皆以序列升进为形，"
                   "名目互不重合；唯佛道两地以「發心」为入阶之首。是 C1 同构（皆设升进之阶、皆以终极位为归），"
                   "不是同源。",
    }

    p1 = {
        "title": "十住與十地：同一階位還是兩套階位",
        "rows": [(i + 1, shizhu[i], shidi[i]) for i in range(10)],
        "name_overlap": sorted(set(shizhu) & set(shidi)),
        "quotes": [{"src": s, "id": i, "text": q} for s, i, q in p1_quotes],
        "daojiao": p1_daogiao,
        "kuax": p1_kuax,
        "finding": "十住十名與十地十名無一重合；兩套階位各自成組。但《疏》《記》都指出別行譯本題作《十住經》，理由是「住是地中一義」——題名重疊來自義訓，不來自同一階位。",
        "limits": "道教半邊已得一手（《道教義樞·位業義》）：三阶七号、五心四位、十轉九宫、三清二十七品皆可回源；與十住十地名目交集唯「發心」一節（兩地皆以發心爲入階之首）。位業義全文義疏未逐句對讀。",
    }
    if p1["name_overlap"]:
        raise SystemExit(f"十住/十地 name overlap unexpected: {p1['name_overlap']}")

    sources = {}
    for k in SRC:
        if k == "DZ0001":
            raw = b"".join(p.read_bytes() for p in sorted(SRC[k].glob("KR5a0001_*.txt")))
        elif k == "KR5e0031":
            raw = b"".join(p.read_bytes() for p in sorted(SRC[k].glob("KR5e0031_*.txt")))
        elif k == "KR1h0015":
            raw = b"".join(p.read_bytes() for p in sorted(SRC[k].glob("KR1h0015_*.txt")))
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
        "t9_pin": t9_pin,
        "d5": d5,
        "p1": p1,
    }
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"written {OUT}")
    nq = sum(len(c["quotes"]) for c in t9["cases"])
    print(f"  T9 cases {len(t9['cases'])} ({nq} quotes); D5 rows {len(d5['rows'])}; P1 rows {len(p1['rows'])}")
    nqp = sum(len(c["quotes"]) for c in t9_pin["cases"])
    print(f"  T9 逐品 cases {len(t9_pin['cases'])} ({nqp} quotes)")
    print(f"  counts: {counts}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
