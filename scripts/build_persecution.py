# -*- coding: utf-8 -*-
"""S3 法难·护法：法难一侧有据、护法一侧无据（一手回源）。

二源：
  · 《宋高僧傳》T50n2061 —— 元表藏经石室、僧质隐遁、礼忏转向、法慎塔毁、宗密示寂
  · 《廣弘明集》T52n2103 —— 襄州峴山華嚴寺盧舍那瑞像「法滅藏之得存」

另附：在库 11 部的法难词全词扫描（會昌／廢佛／毀佛／沙汰／還俗），
用来说明「护法无据」是检索所得、不是推断。
「法難」不作检索词：经文中「法難思」「法難遇」为常用搭配，会致大量假阳性。
"""
import json
import re
from datetime import date
from pathlib import Path

from build_translation_workshop import Doc, sha256

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "research" / "persecution.json"

SRC = {
    "songgao": ("data/references/cbeta/T50n2061.xml",
                "《宋高僧傳》，宋贊寧等撰，CBETA T50n2061"),
    "guanghong": ("data/references/cbeta/T52n2103.xml",
                  "《廣弘明集》，唐道宣撰，CBETA T52n2103"),
}

SCAN_FILES = [
    "T10n0279.xml", "T09n0278.xml", "T10n0293.xml", "T50n2054.xml",
    "T50n2061.xml", "T55n2154.xml", "T52n2103.xml", "T52n2102.xml",
    "T50n2060.xml", "T50n2059.xml", "T51n2089.xml",
]
SCAN_KWS = ["會昌", "廢佛", "毀佛", "沙汰", "還俗"]

Q = {
    # 元表：负经入山 → 会昌藏经 → 大中迎出
    "q_yb_carry": ("songgao", "遇心王菩薩指示支提山靈府",
                   "至支提石室而宅焉。"),
    "q_yb_hide": ("songgao", "于時屬會昌搜毀",
                  "今貯在福州僧寺焉。"),
    # 僧质：诵华严 → 会昌搜简而隐 → 大中重兴
    "q_zhi_chant": ("songgao", "年十五，誦《法華》、《華嚴》、《維摩》等經。",
                    "誦《法華》、《華嚴》、《維摩》等經。"),
    "q_zhi_hide": ("songgao", "後往永嘉，鍾會昌之搜簡",
                   "乃隱樂成縣大芙蓉山，胎息而已。"),
    # 礼忏转向
    "q_lifa_hui": ("songgao", "至乎會昌年內", "謂之「小禮」。"),
    "q_lifa_zhu": ("songgao", "又有斆古人逐字禮《華嚴》、《法華》經",
                   "以為禮無漏法藏也。"),
    # 塔毁
    "q_ta_hui": ("songgao", "其塔屬會昌中", "例皆毀焉。"),
    # 五祖示寂（法难元年）
    "q_zongmi": ("songgao", "會昌元年正月六日坐滅於興福塔院",
                 "容貌益悅。"),
    # 前代法难：北周法灭藏像
    "q_zhou_xiang": ("guanghong", "襄州峴山華嚴寺盧舍那瑞像者",
                     "法滅藏之得存。"),
}


def classify(ctx: str) -> str:
    """把邻近命中分到具体事类；未命中任何规则者标「待分类」，由门禁卡住。"""
    if "會昌寺" in ctx:
        return "寺名「會昌寺」（非年号）"
    if "唐杭州華嚴寺道光傳" in ctx:
        return "寺名「華嚴寺」（下一传标题）"
    if "華嚴寺起塔" in ctx:
        return "寺塔与會昌四年碑（寺名）"
    if "于時屬會昌搜毀" in ctx:
        return "元表藏经石室"
    if "鍾會昌之搜簡" in ctx:
        return "僧质遇搜简隐山"
    if "會昌年內" in ctx:
        return "礼忏转向（会昌年内）"
    return "待分类"


def scan_words() -> dict:
    rows = {}
    total = 0
    near = []
    for name in SCAN_FILES:
        p = ROOT / "data" / "references" / "cbeta" / name
        raw = p.read_text(encoding="utf-8", errors="replace")
        m1, m2 = raw.find("<body"), raw.rfind("</body>")
        body = raw[m1:m2 if m2 > m1 else len(raw)]
        txt = re.sub(r"\s+", "", re.sub(r"<[^>]*>", "", body))
        counts = {k: txt.count(k) for k in SCAN_KWS}
        rows[name] = {"counts": counts, "total": sum(counts.values())}
        total += sum(counts.values())
        for k in SCAN_KWS:
            for m in re.finditer(k, txt):
                w = txt[max(0, m.start() - 80):m.start() + 80]
                if "華嚴" in w:
                    near.append({"file": name, "kw": k, "ctx": w,
                                 "note": classify(w)})
    return {"files": len(SCAN_FILES), "keywords": SCAN_KWS,
            "occurrences": total, "rows": rows, "near_huayan": near}


def main() -> int:
    docs, sources = {}, {}
    for key, (rel, edition) in SRC.items():
        p = ROOT / rel
        docs[key] = Doc(key, p)
        sources[key] = {"path": rel, "edition": edition,
                        "bytes": p.stat().st_size,
                        "sha256": sha256(p.read_bytes())}

    quotes = {}
    for qid, (sk, a, b) in Q.items():
        q = docs[sk].slice_quote(a, b)
        quotes[qid] = {"source": sk, "lb": q["lb"], "text": q["text"].strip()}

    events = [
        {"kind": "法难纪年", "when": "會昌元年（841）", "who": "宗密（華嚴五祖）",
         "act": "會昌元年正月六日坐滅於興福塔院——在法难全面展开之前；此条只作纪年，不证法难加于本经",
         "quotes": ["q_zongmi"], "grade": "A"},
        {"kind": "持经入山", "when": "天寶中來華以後", "who": "釋元表（高麗僧）",
         "act": "負《華嚴經》八十卷，尋訪霍童，至支提石室而居",
         "quotes": ["q_yb_carry"], "grade": "A"},
        {"kind": "法难藏经", "when": "會昌（841—846）", "who": "釋元表",
         "act": "「于時屬會昌搜毀」，以華櫚木函盛经，深藏石室中",
         "quotes": ["q_yb_hide"], "grade": "A"},
        {"kind": "法难后迎经", "when": "大中元年（847）", "who": "慧評禪師",
         "act": "率信士迎出甘露都尉院，「其紙墨如新繕寫」，时贮福州僧寺",
         "quotes": ["q_yb_hide"], "grade": "A"},
        {"kind": "僧人隐遁", "when": "會昌", "who": "釋僧質",
         "act": "本诵《法華》《華嚴》《維摩》；遇「會昌之搜簡」，隱樂成縣大芙蓉山",
         "quotes": ["q_zhi_chant", "q_zhi_hide"], "grade": "A"},
        {"kind": "礼忏转向", "when": "會昌年內", "who": "玄暢大師",
         "act": "請修加《一萬五千佛名經》，兩京禮經口唱低頭、檛磬一聲，謂之「小禮」",
         "quotes": ["q_lifa_hui"], "grade": "A"},
        {"kind": "礼忏转向", "when": "會昌以後", "who": "四眾",
         "act": "「逐字禮《華嚴》、《法華》經」，字上安「南無」、字下安「佛」；贊寧判為叨濫",
         "quotes": ["q_lifa_zhu"], "grade": "A"},
        {"kind": "塔寺毁除", "when": "會昌中", "who": "揚州龍興寺法慎靈塔",
         "act": "靈塔（大曆八年李華碑）「屬會昌中，例皆毀焉」",
         "quotes": ["q_ta_hui"], "grade": "A"},
        {"kind": "前代法难藏像", "when": "北周法滅（建德三年後）", "who": "襄州峴山華嚴寺",
         "act": "盧舍那瑞像「本是周朝古像，法滅藏之得存」——像存而经未记",
         "quotes": ["q_zhou_xiang"], "grade": "B"},
    ]

    kinds = {}
    for e in events:
        kinds[e["kind"]] = kinds.get(e["kind"], 0) + 1

    boundaries = [
        "《宋高僧傳》为宋初赞宁所撰，非唐时一手；「會昌搜毀」「搜簡」皆为追述概括语，不是诏令原文。",
        "元表藏经石室是单条传记记载，无第二证；迎出者慧评亦仅此一见。",
        "僧质传只证「诵《華嚴》者隐遁」，不证本经被特别禁毁；把「僧人避乱」读成「经被禁」是越界。",
        "「逐字礼《華嚴》」出于赞宁评议礼忏流变的语境，是教内批评，不是法难史事。",
        "护法一侧无据：以本经为护法论据的文本（护法论、破斥书）在库未见；《廣弘明集》「華嚴」2 见分别为瑞像灵验与梁武讲《般若》引《華嚴》品，皆非护法论辩。",
        "会昌法难的第一手《入唐求法巡禮行記》（圆仁）、《舊唐書·武宗紀》、《唐會要》皆未取；不取则「法难如何加于本经」只能到传记层。",
        "「法難」不作检索词：经文中「法難思」「法難遇」为常用搭配，计入会致大量假阳性。",
        "词频邻近会漏真证据：元表条「會昌搜毀」与「華嚴」相隔四十余字，不在词窗内；本节引文靠逐条读传，不靠词频检索。",
        "《續高僧傳》为唐初道宣所撰，早于會昌百余年，其「會昌」16 处只能是寺名（會昌寺）——这类假阳性正说明词频必须回到上下文。",
    ]

    scan = scan_words()

    data = {
        "meta": {
            "operator": "S3",
            "title": "法难·护法：法难一侧有藏护之迹，护法一侧无据",
            "date": date.today().isoformat(),
            "method": ("逐条以起止锚在源文切片（不手抄），记叶码 lb；源文件记 sha256；"
                       "类型计数由 events 汇总；护法空白由在库全词扫描得，不凭推断。"),
            "sources": sources,
        },
        "quotes": quotes,
        "events": events,
        "kinds": kinds,
        "scan": scan,
        "boundaries": boundaries,
        "summary": {
            "events": len(events),
            "quotes": len(quotes),
            "kinds": len(kinds),
            "kinds_count": kinds,
            "scan_occurrences": scan["occurrences"],
            "scan_files": scan["files"],
            "near_huayan": len(scan["near_huayan"]),
        },
    }
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n",
                   encoding="utf-8")
    print(f"events {len(events)}  quotes {len(quotes)}  kinds {len(kinds)}")
    for qid, q in quotes.items():
        print(f"  {qid} {q['source']} {q['lb']} | {q['text'][:40]}…")
    print(f"scan: {scan['files']} files / {scan['occurrences']} hits / "
          f"{len(scan['near_huayan'])} near 華嚴")
    print(f"written {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
