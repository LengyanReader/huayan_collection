# -*- coding: utf-8 -*-
"""S2 王室·国家祭祀：诏令一侧有据、祀典一侧无据（一手回源）。

四源：
  · 《大周新譯大方廣佛華嚴經序》T10n0279 卷首（武后御制）
  · 《唐大薦福寺故寺主翻經大德法藏和尚傳》T50n2054（崔致遠）
  · 《開元釋教錄》T55n2154 —— 「天后製新翻聖教序令標經首」
  · 《宋高僧傳》T50n2061 —— 澄觀傳（德宗詔譯四十卷）

另附：在库 11 部的「祭祀／宗廟／社稷／郊祀／封禪／祀典／太廟」全词扫描，
用来说明「祀典无据」是检索所得，不是推断。
"""
import json
import re
from datetime import date
from pathlib import Path

from build_translation_workshop import Doc, sha256

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "research" / "royal_patronage.json"

SRC = {
    "huayan80": ("data/references/cbeta/T10n0279.xml",
                 "《大方廣佛華嚴經》八十卷，CBETA T10n0279；卷首《大周新譯大方廣佛華嚴經序》，天冊金輪聖神皇帝（武后）製"),
    "fazang": ("data/references/cbeta/T50n2054.xml",
               "《唐大薦福寺故寺主翻經大德法藏和尚傳》，新羅崔致遠撰，CBETA T50n2054"),
    "kaiyuan": ("data/references/cbeta/T55n2154.xml",
                "《開元釋教錄》，唐智昇撰，CBETA T55n2154"),
    "songgao": ("data/references/cbeta/T50n2061.xml",
                "《宋高僧傳》，宋贊寧等撰，CBETA T50n2061"),
}

# 祀典词全库扫描：文件 → (说明)
SCAN_FILES = [
    "T10n0279.xml", "T09n0278.xml", "T10n0293.xml", "T50n2054.xml",
    "T50n2061.xml", "T55n2154.xml", "T52n2103.xml", "T52n2102.xml",
    "T50n2060.xml", "T50n2059.xml", "T51n2089.xml",
]
SCAN_KWS = ["祭祀", "宗廟", "社稷", "郊祀", "封禪", "祀典", "太廟"]

Q = {
    # 御序
    "q_pf_title": ("huayan80", "大周新譯大方廣佛華嚴經序", "天冊金輪聖神皇帝製"),
    "q_pf_body": ("huayan80", "朕聞其梵本", "繕寫畢功；"),
    "q80_byline": ("huayan80", "大方廣佛華嚴經卷第一于闐國三藏實叉難陀奉制譯", "奉制譯"),
    # 開元錄：御序制度化
    "q_pf_rule": ("kaiyuan", "天后製新翻聖教序令標經首", "令標經首"),
    # 法藏傳
    "q_fz_edict80": ("fazang", "證聖年中奉勅", "於林光殿譯大寶積經。"),
    "q_fz_precept": ("fazang", "爰降綸旨為菩薩戒師", "亦受菩薩戒。"),
    "q_fz_precept2": ("fazang", "由是中宗睿宗皆請為菩薩戒師", "萬乘歸心。"),
    "q_fz_temples": ("fazang", "因奏於兩都及吳越清涼山五處起寺", "諸家章疏貯之。"),
    "q_fz_rain1": ("fazang", "垂拱三載雲漢之詩作矣。詔藏於西明寺立壇祈之", "未七日雨沾洽。"),
    "q_fz_rain2": ("fazang", "景龍二年中夏憫雨", "未一旬而獲應。"),
    # 澄觀傳：詔譯四十
    "q_cg_edict40": ("songgao", "德宗降中使李輔光宣詔入都", "請明年入。勅允。"),
}


def scan_ritual() -> dict:
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
                    near.append({"file": name, "kw": k, "ctx": w})
    return {"files": len(SCAN_FILES), "keywords": SCAN_KWS,
            "occurrences": total, "rows": rows,
            "near_huayan": near}


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
        {"kind": "御制序", "when": "聖曆二年（699）", "sovereign": "武則天",
         "act": "自撰《大周新譯大方廣佛華嚴經序》，述遣使于闐迎梵本、證聖元年大遍空寺親受筆削、聖曆二年繕寫畢功",
         "quotes": ["q_pf_title", "q_pf_body"], "grade": "A"},
        {"kind": "御制序·制度", "when": "八十本譯成後", "sovereign": "武則天",
         "act": "御序「令標經首」——帝王文字冠於經首，成後世新譯經的定式",
         "quotes": ["q_pf_rule"], "grade": "A"},
        {"kind": "制譯署名", "when": "八十本卷首", "sovereign": "武則天",
         "act": "譯者署「奉制譯」——譯事由制命啟動，署名即制度標記",
         "quotes": ["q80_byline"], "grade": "A"},
        {"kind": "敕譯", "when": "證聖元年—聖曆二年（695—699）", "sovereign": "武則天",
         "act": "奉敕與實叉難陀譯《華嚴》；神龍中又於林光殿譯《大寶積經》",
         "quotes": ["q_fz_edict80"], "grade": "A"},
        {"kind": "敕譯", "when": "貞元十二年（796）", "sovereign": "唐德宗",
         "act": "降中使宣詔入都，與般若譯烏荼國王所進《華嚴》後分四十卷",
         "quotes": ["q_cg_edict40"], "grade": "A"},
        {"kind": "帝受戒", "when": "神龍以後〔待核〕", "sovereign": "唐中宗（「太上皇」所指待核）",
         "act": "降綸旨請法藏為菩薩戒師；太上皇亦受菩薩戒",
         "quotes": ["q_fz_precept"], "grade": "A"},
        {"kind": "帝受戒", "when": "中宗、睿宗朝", "sovereign": "唐中宗、唐睿宗",
         "act": "中宗、睿宗皆請法藏為菩薩戒師——帝王以譯主為戒師",
         "quotes": ["q_fz_precept2"], "grade": "A"},
        {"kind": "敕建寺牓經名", "when": "法藏奏請後", "sovereign": "唐中宗、唐睿宗〔待核〕",
         "act": "奏於兩都及吳越清涼山五處起寺，「均牓華嚴之號」——經名成為寺額",
         "quotes": ["q_fz_temples"], "grade": "A"},
        {"kind": "敕祈雨·立壇", "when": "垂拱三載（687）", "sovereign": "武則天",
         "act": "詔法藏於西明寺立壇祈雨，「每夕齋戒」，未七日雨洽",
         "quotes": ["q_fz_rain1"], "grade": "A"},
        {"kind": "敕祈雨·百座", "when": "景龍二年（708）", "sovereign": "唐中宗",
         "act": "命法藏集百法師於薦福寺以法禱雨；詔批「敷百座以祈恩，未一旬而獲應」",
         "quotes": ["q_fz_rain2"], "grade": "A"},
    ]

    # 类型计数：由 events 汇总，手改无效
    kinds = {}
    for e in events:
        kinds[e["kind"]] = kinds.get(e["kind"], 0) + 1

    boundaries = [
        "《法藏傳》為後世碑傳（新羅崔致遠撰），贊頌體；其中「詔」「勅」是轉述，不是詔書原文——引文照錄，不改其為轉述的性質。",
        "御序是此組唯一帝王親筆文本；其「親受筆削」屬譯場條件（見 §17.19 S1），不等於本經入祀典。",
        "「太上皇」所指與受戒年份，傳文未系年，記〔待核〕；不強指為某一帝。",
        "祈雨兩事是「敕立壇／集百法師」的國家祈禳，儀出法藏與僧團，非本經儀軌——只能證「國家與僧人合作」，不能證「本經入國家祭祀」。",
        "祀典檢索只就本文在庫 11 部而言，未及史部（《舊唐書》《唐會要》《唐大詔令集》）與金石；「無據」不等於「無此事」。",
    ]

    scan = scan_ritual()

    data = {
        "meta": {
            "operator": "S2",
            "title": "王室·国家祭祀：八类诏敕可证，祀典无据",
            "date": date.today().isoformat(),
            "method": ("逐条以起止锚在源文切片（不手抄），记叶码 lb；源文件记 sha256；"
                       "类型计数由 events 汇总；祀典空白由在库全词扫描得，不凭推断。"),
            "sources": sources,
        },
        "quotes": quotes,
        "events": events,
        "kinds": kinds,
        "ritual_scan": scan,
        "boundaries": boundaries,
        "summary": {
            "events": len(events),
            "quotes": len(quotes),
            "kinds": len(kinds),
            "kinds_count": kinds,
            "ritual_occurrences": scan["occurrences"],
            "ritual_files": scan["files"],
            "near_huayan": len(scan["near_huayan"]),
        },
    }
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n",
                   encoding="utf-8")
    print(f"events {len(events)}  quotes {len(quotes)}  kinds {len(kinds)}")
    for qid, q in quotes.items():
        print(f"  {qid} {q['source']} {q['lb']} | {q['text'][:36]}…")
    print(f"ritual scan: {scan['files']} files / {scan['occurrences']} hits / "
          f"{len(scan['near_huayan'])} near 華嚴")
    print(f"written {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())