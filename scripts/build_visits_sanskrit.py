# -*- coding: utf-8 -*-
"""T9 逐参名·梵本对照：十八组「两本同字、一本独异」名的「同指」判。

§17.22 只判字面：`＝`/`≈`/`≠`。字面异不等于所指异，但要说「所指同」，
须有第三方 witness。梵本《入法界品》（Vaidya 1960，GRETIL 电子转写）在库，
其指授句「gaccha kulaputra … tatra X nāma Y prativasati」与汉本逐参对应，
可作独立锚。

口径（要紧）：§17.22 中字面有异者共 35 组——
  ① 恰有一对同名、第三本独异：18 组（本节所判：80=60≠40 九组 ＋ 80=40≠60 九组）
  ② 三本全异：17 组（未判，名单写入 boundaries 与 stats.remain_all_diff）
  ③ 三本同字：15 组（未核梵）
本节只判①，不得因此读作「字面异者已尽判」。

对位用三重锚，不靠音写猜：
  ① 角色（比丘／長者／優婆夷／夜神…）
  ② 处所（īṣāṇo＝伊沙那、siṃhavijṛmbhitaṃ＝師子頻申、potalaka＝補怛洛迦…）
  ③ 次序（十八组梵本指令序须不降；唯一相等处即正趣空缺位——脚本自检）

输出只作「同指／待核」，不做教义判，也不评音写精当。
"""
import hashlib
import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(r"C:\DA_Practice\huayan_collection")
SRC_REL = "data/references/sanskrit/gandavyuha_vaidya.txt"
SRC = ROOT / SRC_REL
OUT = ROOT / "data" / "research" / "visits_sanskrit.json"
VN = ROOT / "data" / "research" / "visits_names.json"

# 十八组：§17.22 中字面有异者（80=60≠40 九组 ＋ 80=40≠60 九组）
CASES = [
    dict(no=4, probe="supratisthito nāma bhikṣuḥ", skt="supratisthita",
         role="bhikṣuḥ（比丘）", place="sāgaratīraṃ nāma laṅkāpatham（楞伽道·海岸）",
         verdict="同指·义译",
         basis="su-pratiṣṭhita＝善／妙＋住；八十「善住」、四十「妙住」各取一侧"),
    dict(no=8, probe="āśā nāmopāsikā", skt="āśā",
         role="upāsikā（優婆夷）", place="samudravetāḍī；samantavyūhaṃ udyānaṃ（海潮處·普莊嚴園）",
         verdict="待核·对音不合",
         basis="梵本作 āśā（suprabha 王之妻）；八十「休捨」、四十「伊舍那」皆非其直接对音"),
    dict(no=10, probe="jayoṣmāyatano nāma brāhmaṇaḥ", skt="jayoṣmāyatana",
         role="brāhmaṇaḥ（婆羅門）", place="īṣāṇo nāma janapadaḥ（伊沙那聚落）",
         verdict="同指·义译",
         basis="jaya＋uṣma＝勝＋熱，八十／四十「勝熱」即其义译；六十「方便命」与梵名无对音关系",
         flag="六十「方便命」名源待核"),
    dict(no=11, probe="maitrāyaṇī nāma kanyā", skt="maitrāyaṇī",
         role="kanyā（童女，siṃhaketu 王之女）", place="siṃhavijṛmbhitaṃ nāma nagaram（師子頻申城）",
         verdict="同指·音义并存",
         basis="六十「彌多羅尼」为音写、四十「慈行」取 maitrī＝慈，同出一名"),
    dict(no=17, probe="samantanetro nāma gāndhikaḥ", skt="samantanetra",
         role="gāndhikaḥ śreṣṭhī（香師·長者）", place="vetramūlako janapadaḥ；samantamukhaṃ nagaram（藤根國·普門城）",
         verdict="同指·义译",
         basis="samanta-netra＝普眼；六十「普眼妙香」把 gāndhika（香師）也译进名里"),
    dict(no=21, probe="sarvagāmī nāma parivrājakaḥ", skt="sarvagāmin",
         role="parivrājakaḥ（外道）", place="tosalaṃ nāma nagaram（都薩羅城）",
         verdict="同指·义译",
         basis="sarva＋gāmin＝遍＋行（八十／四十「遍行」）；六十「隨順一切眾生」为同一名的散译"),
    dict(no=23, probe="vairo nāma dāśaḥ", skt="vaira",
         role="dāśaḥ（船師）", place="kūṭāgāraṃ nāma nagaram（海岸樓閣大城）",
         verdict="同指·对音",
         basis="八十／四十「婆施羅」为 vaira 的音写；六十「自在」与梵名无对音关系",
         flag="六十「自在」名源待核"),
    dict(no=24, probe="jayottamo nāma śreṣṭhī", skt="jayottama",
         role="śreṣṭhī（長者）", place="nandihāraṃ nāma nagaram（樂瓔珞城）",
         verdict="同指·义译",
         basis="jaya＋uttama＝勝＋無上；八十／六十「無上勝」、四十「最勝」皆其义译，唯词序不同"),
    dict(no=25, probe="siṃhavijṛmbhitā nāma bhikṣuṇī", skt="siṃhavijṛmbhitā",
         role="bhikṣuṇī（比丘尼）", place="kaliṅgavanaṃ nāma nagaram（羯陵迦林）",
         verdict="同指·义译",
         basis="siṃha＋vijṛmbhita＝師子＋頻申／奮迅；八十／四十「頻申」、六十「奮迅」同义异词"),
    dict(no=26, probe="vasumitrā nāma bhāgavatī", skt="vasumitrā",
         role="bhāgavatī（女）", place="ratnavyūhaṃ nāma nagaram（寶莊嚴城）",
         verdict="同指·对音",
         basis="婆須蜜多／伐蘇蜜多皆 vasumitrā 的音写异形（v/b 互换）"),
    dict(no=28, probe="avalokiteśvaro nāma bodhisattvaḥ", skt="avalokiteśvara",
         role="bodhisattvaḥ（菩薩）", place="potalako nāma parvataḥ（補怛洛迦山）",
         verdict="同指·音义并存",
         basis="avalokita＋īśvara＝觀＋自在（八十／四十）；六十「觀世音」为旧译一系"),
    dict(no=29, probe=None, skt=None, role=None, place=None,
         verdict="待核·梵本无对应",
         basis="观自在指授之后直入大天，其间一万五千余字无第三位指授句；四十「正性無異行」亦无梵名可对",
         gap=("avalokiteśvaro nāma bodhisattvaḥ", "mahādevo devaḥ")),
    dict(no=31, probe="sthāvarā nāma", skt="sthāvarā",
         role="pṛthvīdevatā（地神）", place="bodhimaṇḍe（菩提場）",
         verdict="同指·义译",
         basis="sthāvara＝住／不動；八十／六十「安住」、四十「自性不動」皆其义译"),
    dict(no=34, probe="pradakṣiṇena pramuditanayanajagadvirocanā nāma rātridevatā",
         skt="pramuditanayanajagadvirocanā",
         role="rātridevatā（夜神）", place="vairocanabodhimaṇḍa（菩提場右旋）",
         verdict="同指·义译",
         basis="pramudita-nayana＝喜目、jagad-virocana＝觀察／普照眾生；四十多一「一切」正对 jagat"),
    dict(no=40, probe="sutejomaṇḍalaratiśrīrnāma lumbinīvanadevatā",
         skt="sutejomaṇḍalaratiśrī",
         role="lumbinīvanadevatā（林神）", place="lumbinīvana（嵐毘尼園）",
         verdict="同指·义译",
         basis="su-tejo-maṇḍala-rati-śrī；八十「妙德圓滿」、四十「妙威德圓滿愛敬」皆压缩译"),
    dict(no=41, probe="gopā nāma", skt="gopā",
         role="śākyakanyā（釋女）", place="kapilavastu mahānagara（迦毘羅城）",
         verdict="同指·对音",
         basis="瞿波（八十／四十）与瞿夷（六十）皆 gopā 的音写，新旧译用字不同"),
    dict(no=46, probe="bhadrottamā nāmopāsikā", skt="bhadrottamā",
         role="upāsikā（優婆夷）", place="vartanakaṃ nagaram（婆呾那城）",
         verdict="同指·义译",
         basis="bhadra＋uttama＝賢＋勝；八十／六十「賢勝」、四十「最勝賢」唯词序倒置"),
    dict(no=50, probe="śivarāgro nāma brāhmaṇaḥ", skt="śivarāgra",
         role="brāhmaṇaḥ（婆羅門）", place="dharmagrāmaḥ（法聚落）",
         verdict="同指·音义并存",
         basis="śiva＝寂靜／尸毘；八十「最寂靜」取义、六十「尸毘最勝」取音"),
]

# 附见：不在十八组内，但同一次核梵时直接读出、值得单列的发现
BYPRODUCTS = [
    dict(no=51, probe="śrīsaṃbhavo nāma dārakaḥ", also="śrīmatiśca nāma dārikā",
         skt="śrīsaṃbhava＋śrīmatī",
         role="dārakaḥ＋dārikā（童子＋童女）", place="sumanāmukhaṃ nāma nagaram（名聞國）",
         basis="梵本一句并举两名：「śrīsaṃbhavo nāma dārakaḥ prativasati, śrīmatiśca nāma dārikā」；"
               "汉本作「德生·有德」并列一处，是梵本如此，非编者合并"),
]


def normalize(text: str):
    out, idx = [], []
    for i, ch in enumerate(text):
        if ch.isspace():
            if out and out[-1] == " ":
                continue
            out.append(" ")
            idx.append(i)
        else:
            out.append(ch)
            idx.append(i)
    return "".join(out), idx


def main() -> int:
    raw = SRC.read_text(encoding="utf-8", errors="replace")
    t, _ = normalize(raw)

    starts = [m.start() for m in re.finditer(r"gaccha kulaputra", t)]
    pages = [(m.start(), int(m.group(1))) for m in re.finditer(r"\(gv (\d+)\)", t)]

    def gv_at(pos: int):
        best = None
        for p, n in pages:
            if p <= pos:
                best = n
            else:
                break
        return f"gv {best}" if best else None

    def ord_at(pos: int):
        k = 0
        for i, s in enumerate(starts):
            if s <= pos:
                k = i + 1
            else:
                break
        return k or None

    vn = json.loads(VN.read_text(encoding="utf-8"))
    by_no = {r["no"]: r for r in vn["rows"]}

    # §17.22 的三分：恰一对同名（本节所判）／三本全异／三本同字
    tri = {r["no"]: {r["n80"], r["n60"], r["n40"]} for r in vn["rows"]}
    one_eq = sorted(n for n, s in tri.items() if len(s) == 2)
    all_diff = sorted(n for n, s in tri.items() if len(s) == 3)
    all_same = sorted(n for n, s in tri.items() if len(s) == 1)
    if [c["no"] for c in CASES] != one_eq:
        print("!! CASES 与「恰一对同名」的十八组不一致")
        print("   cases:", [c["no"] for c in CASES])
        print("   one_eq:", one_eq)
        return 8

    cases = []
    for c in CASES:
        row = by_no[c["no"]]
        rec = {
            "no": c["no"],
            "n80": row["n80"], "n60": row["n60"], "n40": row["n40"],
            "rel80_60": row["rel80_60"], "rel80_40": row["rel80_40"],
            "skt": c["skt"], "skt_role": c["role"], "skt_place": c["place"],
            "verdict": c["verdict"], "basis": c["basis"],
            "flag": c.get("flag"),
            "probe": c["probe"],
        }
        if c["probe"]:
            hits = [m.start() for m in re.finditer(re.escape(c["probe"]), t)]
            if len(hits) != 1:
                print(f"!! probe not unique ({len(hits)}): {c['probe']}")
                return 2
            pos = hits[0]
            rec["pos"] = pos
            rec["ord"] = ord_at(pos)
            rec["gv"] = gv_at(pos)
        else:
            a = t.find(c["gap"][0])
            b = t.find(c["gap"][1])
            if a < 0 or b < 0 or b < a:
                print("!! gap anchors not found:", c["no"])
                return 3
            inner = [s for s in starts if a < s < b]
            own = max([s for s in starts if s < b], default=None)
            inner = [s for s in inner if s != own]
            if inner:
                print(f"!! gap for 参 {c['no']} is not empty: {len(inner)} instructions")
                return 4
            rec["pos"] = a
            rec["ord"] = ord_at(a)
            rec["gv"] = gv_at(a)
            rec["gv_to"] = gv_at(b)
            rec["gap_chars"] = (own - a) if own else (b - a)
            rec["gap_between"] = list(c["gap"])
        cases.append(rec)

    # 次序自检：参号递增时，梵本指令序不得下降；
    # 唯一允许相等处是「空缺位」（正趣无指授句，沿用前一位之序）
    ords = [c["ord"] for c in cases if c["ord"]]
    if ords != sorted(ords):
        print("!! Sanskrit ordinals decrease:", ords)
        return 5
    dup = sum(1 for a, b in zip(ords, ords[1:]) if a == b)
    gaps = sum(1 for c in cases if not c["probe"])
    if dup != gaps:
        print(f"!! ordinals equal {dup} times but gap cases {gaps}:", ords)
        return 9

    # 附见：一句两名的梵本 witness
    byp = []
    for b in BYPRODUCTS:
        hits = [m.start() for m in re.finditer(re.escape(b["probe"]), t)]
        if len(hits) != 1:
            print(f"!! byproduct probe not unique ({len(hits)}): {b['probe']}")
            return 6
        near = t[hits[0]:hits[0] + 200]
        if b["also"] not in near:
            print(f"!! byproduct second name not adjacent: {b['also']}")
            return 7
        row = by_no[b["no"]]
        byp.append({
            "no": b["no"], "n80": row["n80"], "n60": row["n60"], "n40": row["n40"],
            "skt": b["skt"], "skt_role": b["role"], "skt_place": b["place"],
            "probe": b["probe"], "also": b["also"],
            "pos": hits[0], "ord": ord_at(hits[0]), "gv": gv_at(hits[0]),
            "basis": b["basis"],
        })

    verdicts = {}
    for c in cases:
        verdicts[c["verdict"]] = verdicts.get(c["verdict"], 0) + 1
    stats = {
        "cases": len(cases),
        "same": sum(1 for c in cases if c["verdict"].startswith("同指")),
        "pending": sum(1 for c in cases if c["verdict"].startswith("待核")),
        "by_verdict": verdicts,
        "flagged": [c["no"] for c in cases if c["flag"]],
        "ord_first": min(ords),
        "ord_last": max(ords),
        "remain_all_diff": len(all_diff),
        "remain_all_diff_nos": all_diff,
        "remain_all_same": len(all_same),
        "remain_all_same_nos": all_same,
    }

    diff_names = "、".join(
        f'{by_no[n]["n80"]}／{by_no[n]["n60"]}／{by_no[n]["n40"]}' for n in all_diff)
    same_nos = "、".join(str(n) for n in all_same)

    data = {
        "meta": {
            "operator": "T9",
            "title": "入法界品十八组异名·梵本同指判（两本同字、一本独异）",
            "date": date.today().isoformat(),
            "method": ("取 §17.22 中「恰有一对同名、第三本独异」的十八组，在梵本《入法界品》中定位其指授句"
                       "（gaccha kulaputra … tatra X nāma Y prativasati），以角色＋处所＋次序三锚对位；"
                       "判据为译名与梵名之对音／义译关系，只判同指与否，不判音写精当。"
                       "字面有异者共 35 组，本节只判其中 18 组（见 boundaries）。"),
            "scope": (f'十八组（§17.22 中恰有一对同名者：{one_eq[0]}…{one_eq[-1]}，共 {len(one_eq)} 组，'
                      f'参号列于 cases）。未判：三本全异 {len(all_diff)} 组、三本同字 {len(all_same)} 组，'
                      f'合计 {len(all_diff) + len(all_same)} 组。'),
            "source": {
                "path": SRC_REL,
                "bytes": SRC.stat().st_size,
                "sha256": hashlib.sha256(SRC.read_bytes()).hexdigest(),
                "edition": "P. L. Vaidya, Gaṇḍavyūhasūtram, Darbhanga: Mithila Institute, 1960 (BST 5)",
                "etext": "GRETIL (sa_gaNDavyUhasUtra), 2020-07-31 版转写",
                "pagination": "文中 (gv N) 为 GRETIL 依 Vaidya 书页所加页码标记",
            },
        },
        "cases": cases,
        "byproducts": byp,
        "stats": stats,
        "boundaries": [
            "这是「同指」判，不是译名优劣判：同指只表两本指同一位善知识，不评谁译得准。",
            "单一写本系统：所用为 Vaidya 校本之电子转写，非多本会校；故「Vaidya 本无对应」只能记作该本无，不得推为梵本原无。",
            "对位靠角色＋处所＋次序三锚；次序单调性由脚本自检（十八组梵本指令序不降；唯一相等处即正趣空缺位，沿用观自在之序），处所名逐条附于表内可复检。",
            "音写是否合于梵音、义译是否尽义，皆不在本节判内；只记两本名与该梵名有无可判的关系。",
            (f'未判者三十二组，不得读作已核：三本全异 {len(all_diff)} 组（{diff_names}）与三本同字 '
             f'{len(all_same)} 组（参号 {same_nos}）。字面同可能两本各依不同梵名而偶合，'
             f'字面全异亦可能三本各取一义，皆须全表核梵方可断言。'),
        ],
    }
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f'cases {stats["cases"]}  same {stats["same"]}  pending {stats["pending"]}  '
          f'ord {stats["ord_first"]}..{stats["ord_last"]}')
    for c in cases:
        print(f'{c["no"]:>3} {c["n80"]:<8} {c["n60"]:<8} {c["n40"]:<10} | '
              f'{str(c["skt"]):<32} {str(c["gv"]):>7} | {c["verdict"]}'
              + (f'  [{c["flag"]}]' if c["flag"] else ""))
    print("written", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
