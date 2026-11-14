# -*- coding: utf-8 -*-
"""S1 译场·制度：四本《华严》的译场记录（一手回源）。

三源：
  · 《開元釋教錄》T55n2154 —— 六十、八十两本的入藏条目与译者传
  · 《宋高僧傳》T50n2061 —— 四十本的译场名录（蓮華傳）
  · 德格版 Toh 44 卷末题记 —— 藏译的译校者

全部引文按原文切片（不手抄），逐条记叶码 lb，并对源文件记 sha256。
"""
import hashlib
import json
import re
from bisect import bisect_left
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "research" / "translation_workshop.json"

DERGE_GLOB = "derge_kangyur/avatamsaka/038_*.txt"
SRC = {
    "kaiyuan": ("data/references/cbeta/T55n2154.xml",
                "《開元釋教錄》唐·智昇撰，CBETA T55n2154（大正藏第 55 册）"),
    "songgao": ("data/references/cbeta/T50n2061.xml",
                "《宋高僧傳》宋·贊寧等撰，CBETA T50n2061（大正藏第 50 册）"),
}


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def strip_tags(s: str) -> tuple[str, list[int]]:
    out, pos, i = [], [], 0
    for m in re.finditer(r"<[^>]*>", s):
        chunk = s[i:m.start()]
        out.append(chunk)
        pos.extend(range(i, m.start()))
        i = m.end()
    out.append(s[i:])
    pos.extend(range(i, len(s)))
    return "".join(out), pos


class Doc:
    """CBETA XML：clean 字串 + clean→raw 映射 + 叶码表。"""

    def __init__(self, key: str, path: Path):
        self.key = key
        self.path = path
        self.raw = path.read_text(encoding="utf-8")
        m1 = re.search(r"<body\b", self.raw)
        m2 = self.raw.rfind("</body>")
        self.offset = m1.start() if m1 else 0
        body = self.raw[self.offset:(m2 if m2 > 0 else len(self.raw))]
        self.clean, raw_of_clean = strip_tags(body)
        self.raw_of_clean = [self.offset + i for i in raw_of_clean]
        self._flatten()
        self.lbs = [(m.start(), m.group(1)) for m in
                    re.finditer(r'<lb n="([0-9a-z.]+)"', self.raw)]
        self.lb_starts = [p for p, _ in self.lbs]

    def _flatten(self) -> None:
        """去空白（CBETA 于 lb 处断行）：flat → clean 下标表。"""
        chars, idx = [], []
        for i, ch in enumerate(self.clean):
            if ch.isspace():
                continue
            chars.append(ch)
            idx.append(i)
        self.flat = "".join(chars)
        self.clean_of_flat = idx

    def lb_at_raw(self, pos: int) -> str:
        k = bisect_left(self.lb_starts, pos) - 1
        return self.lbs[max(0, k)][1] if self.lbs else "—"

    def slice_quote(self, start: str, end: str) -> dict:
        i = self.flat.find(start)
        if i < 0:
            raise SystemExit(f"{self.key}: 起锚未命中 {start!r}")
        if self.flat.find(start, i + 1) >= 0:
            raise SystemExit(f"{self.key}: 起锚不唯一 {start!r}")
        j = self.flat.find(end, i)
        if j < 0:
            raise SystemExit(f"{self.key}: 止锚未命中 {end!r}")
        raw = self.raw_of_clean[self.clean_of_flat[i]]
        return {"lb": self.lb_at_raw(raw), "text": self.flat[i:j + len(end)]}


class TibDoc:
    """德格 .txt：叶码形如 [362a.6]，无标签。"""

    def __init__(self, key: str, path: Path):
        self.key = key
        self.path = path
        self.raw = path.read_text(encoding="utf-8")
        self.clean = self.raw
        self.lbs = [(m.start(), m.group(1)) for m in
                    re.finditer(r"\[(\d{3}[ab]\.\d)\]", self.raw)]
        self.lb_starts = [p for p, _ in self.lbs]
        # 正文层：去空白、去叶码标记（[362a.6]），记 bare → raw 偏移
        marked = re.compile(r"\[\d{3}[ab]\.\d\]")
        chars, offs, i = [], [], 0
        while i < len(self.raw):
            m = marked.match(self.raw, i)
            if m:
                i = m.end()
                continue
            ch = self.raw[i]
            if not ch.isspace():
                chars.append(ch)
                offs.append(i)
            i += 1
        self.bare = "".join(chars)
        self.raw_of_bare = offs

    def lb_at_raw(self, pos: int) -> str:
        k = bisect_left(self.lb_starts, pos) - 1
        return self.lbs[max(0, k)][1] if self.lbs else "—"

    def slice_quote(self, start: str, end: str) -> dict:
        i = self.bare.find(start)
        if i < 0:
            raise SystemExit(f"{self.key}: 起锚未命中 {start!r}")
        if self.bare.find(start, i + 1) >= 0:
            raise SystemExit(f"{self.key}: 起锚不唯一 {start!r}")
        j = self.bare.find(end, i)
        if j < 0:
            raise SystemExit(f"{self.key}: 止锚未命中 {end!r}")
        return {"lb": self.lb_at_raw(self.raw_of_bare[i]),
                "text": self.bare[i:j + len(end)]}


def main() -> int:
    docs = {}
    sources = {}
    for key, (rel, edition) in SRC.items():
        p = ROOT / rel
        docs[key] = Doc(key, p)
        sources[key] = {"path": rel, "edition": edition,
                        "bytes": p.stat().st_size, "sha256": sha256(p.read_bytes())}
    tp = next((ROOT / "data" / "references" / "tibetan").glob(DERGE_GLOB))
    docs["derge"] = TibDoc("derge", tp)
    sources["derge"] = {"path": tp.relative_to(ROOT).as_posix(),
                        "edition": "德格版《甘珠爾》Toh 44（Buddhāvataṃsaka）卷末譯校題記",
                        "bytes": tp.stat().st_size, "sha256": sha256(tp.read_bytes())}

    Q = {
        # 六十本
        "q60_entry": ("kaiyuan", "大方廣佛華嚴經六十卷初出元五十卷",
                      "見祖祐二錄"),
        "q60_master": ("kaiyuan", "沙門佛陀跋陀羅。晉言覺賢。本姓釋氏",
                       "甘露飯王之苗裔也。"),
        "q60_roster": ("kaiyuan", "乃手執梵文。共沙門法業慧嚴慧義等百有餘人",
                       "故道場寺猶有華嚴堂焉。"),
        # 八十本
        "q80_entry": ("kaiyuan", "大方廣佛華嚴經八十卷第二出",
                      "於佛授記寺功畢"),
        "q80_master": ("kaiyuan", "沙門實叉難陀。唐云喜學。于闐國人",
                       "善大小乘兼異學論。"),
        "q80_patron": ("kaiyuan", "天后明揚佛日敬重大乘。以華嚴舊經處會未備",
                       "於佛授記寺譯。"),
        "q80_roster": ("kaiyuan", "沙門波崙玄軌等筆受",
                       "太子中舍賈膺福監護。"),
        # 四十本
        "q40_entry": ("songgao", "後以《華嚴》後分梵夾附舶來",
                      "十四年二月解座。"),
        # 藏譯
        "qti_colophon": ("derge", "རྒྱ་གར་གྱི་མཁན་པོ་ཛི་ན་མི་ཏྲ",
                         "གཏན་ལ་ཕབ་པའོ།།"),
    }
    quotes = {}
    for qid, (sk, a, b) in Q.items():
        q = docs[sk].slice_quote(a, b)
        quotes[qid] = {"source": sk, "lb": q["lb"], "text": q["text"].strip()}

    versions = {
        "T278": {
            "label": "六十華嚴", "taisho": "T09n0278",
            "title": "大方廣佛華嚴經（六十卷）",
            "translator": "佛陀跋陀羅（覺賢）",
            "date": "義熙十四年三月十日—元熙二年六月十日（418—420）",
            "place": "楊都·道場寺",
            "patron": "沙門支法領從于闐得梵本；僧團自譯，無敕令記載",
            "base": "于闐所得梵本",
            "scale": "法業、慧嚴、慧義等百有餘人；寺有華嚴堂",
            "quotes": ["q60_entry", "q60_master", "q60_roster"],
            "roster": [
                {"role": "譯主", "person": "佛陀跋陀羅", "quote": "q60_master"},
                {"role": "筆受", "person": "法業", "quote": "q60_entry"},
                {"role": "同譯", "person": "慧嚴、慧義", "quote": "q60_roster"},
            ],
        },
        "T279": {
            "label": "八十華嚴", "taisho": "T10n0279",
            "title": "大方廣佛華嚴經（八十卷）",
            "translator": "實叉難陀（喜學）",
            "date": "證聖元年三月十四日—聖曆二年十月八日（695—699）",
            "place": "東都大內大遍空寺→佛授記寺",
            "patron": "武后發使于闐求訪梵本並請譯人；天后親受筆削、親臨法座",
            "base": "于闐所得梵本",
            "scale": "菩提流志、義淨同宣梵本；復禮、法藏等譯",
            "quotes": ["q80_entry", "q80_master", "q80_patron", "q80_roster"],
            "roster": [
                {"role": "譯主", "person": "實叉難陀", "quote": "q80_master"},
                {"role": "宣梵本", "person": "菩提流志、義淨", "quote": "q80_patron"},
                {"role": "筆受", "person": "波崙、玄軌", "quote": "q80_roster"},
                {"role": "綴文", "person": "復禮", "quote": "q80_roster"},
                {"role": "證義", "person": "法寶、弘景", "quote": "q80_roster"},
                {"role": "監護", "person": "賈膺福", "quote": "q80_roster"},
                {"role": "帝王親預", "person": "武后", "quote": "q80_entry"},
            ],
        },
        "T293": {
            "label": "四十華嚴", "taisho": "T10n0293",
            "title": "大方廣佛華嚴經（四十卷）",
            "translator": "般若（罽賓三藏）",
            "date": "貞元十一年—十四年二月（795—798）",
            "place": "長安·崇福寺",
            "patron": "烏荼國王書獻梵夾（一說）；貞元十二年六月詔譯",
            "base": "南天竺烏荼國王所獻〈入不思議解脫境界普賢行願品〉梵夾",
            "scale": "宣梵、譯語、筆受、綴文、潤文、證義、詳定、寫進，八職具備",
            "quotes": ["q40_entry"],
            "roster": [
                {"role": "譯主", "person": "般若", "quote": "q40_entry"},
                {"role": "宣梵本", "person": "般若", "quote": "q40_entry"},
                {"role": "譯語", "person": "廣濟", "quote": "q40_entry"},
                {"role": "筆受", "person": "圓照", "quote": "q40_entry"},
                {"role": "綴文", "person": "智柔、智通", "quote": "q40_entry"},
                {"role": "潤文", "person": "道恒、鑒虛", "quote": "q40_entry"},
                {"role": "證義", "person": "大通", "quote": "q40_entry"},
                {"role": "詳定", "person": "澄觀、靈邃", "quote": "q40_entry"},
                {"role": "寫進", "person": "霍仙鳴、竇文場", "quote": "q40_entry"},
            ],
        },
        "TOH44": {
            "label": "藏譯", "taisho": "Toh 44",
            "title": "བུདྡྷ་ཨ་བ་ཏང་ས་ཀ（大方廣佛華嚴經，德格版）",
            "translator": "Jinamitra、Surendrabodhi、Ye shes sde 等",
            "date": "吐蕃時期（約 9 世紀初）〔待核〕",
            "place": "吐蕃譯場〔待核〕",
            "patron": "無題記可證",
            "base": "印度梵本",
            "scale": "堪布二員＋大校譯師，譯、校、定三序",
            "quotes": ["qti_colophon"],
            "roster": [
                {"role": "堪布", "person": "Jinamitra、Surendrabodhi",
                 "person_bo": "ཛི་ན་མི་ཏྲ་དང་སུ་རེནྡྲ་བོ་དྷི",
                 "quote": "qti_colophon"},
                {"role": "校譯", "person": "Bande Ye shes sde",
                 "person_bo": "བནྡེ་ཡེ་ཤེས་སྡེ",
                 "quote": "qti_colophon"},
            ],
        },
    }

    roles = ["譯主", "宣梵本", "譯語", "筆受", "綴文", "潤文", "證義",
             "詳定", "監護", "寫進", "同譯", "帝王親預", "堪布", "校譯"]
    matrix = {r: [k for k, v in versions.items()
                  if any(x["role"] == r for x in v["roster"])] for r in roles}

    typology = [
        {"kind": "僧团译场", "key": "T278",
         "why": "道场寺自译，百余人同出，无敕令、无监护；经录只记笔受一人",
         "quote": "q60_roster"},
        {"kind": "国家译场", "key": "T279",
         "why": "武后发使求梵本、亲受笔削，译成于内道场而后移佛授记寺，置监护",
         "quote": "q80_entry"},
        {"kind": "使职监译", "key": "T293",
         "why": "诏译之外，功德使、神策军护军「写进」，又置详定——译场嵌入使职系统",
         "quote": "q40_entry"},
        {"kind": "吐蕃译场", "key": "TOH44",
         "why": "堪布与校译师分职，题记只记「译、校、定」，无汉式职衔",
         "quote": "qti_colophon"},
    ]

    boundaries = [
        "经录、僧传是后世二次编纂，非译场原始档案：所记职衔反映编纂者的分类，不等于译场实设职位。",
        "职衔名目跨时代不完全可比（东晋「笔受」与唐「笔受」未必同责）；本节只陈述各本见于记载的分工。",
        "藏译题记只记堪布、校译师与「译校定」，译场地点、年代须另据他证〔待核〕。",
        "帝王亲预译事属译场条件，本节不据此判 S2（王室信仰）；S2 仍为 none。",
        "六十本「无敕令记载」是文献不载，不等于当时无敕令——只能说本文未见，不能据此判其非官方译场。",
    ]

    data = {
        "meta": {
            "operator": "S1",
            "title": "译场·制度：四本《华严》的译场记录",
            "date": date.today().isoformat(),
            "method": ("逐条以起止锚在源文切片（不手抄），记叶码 lb；源文件记 sha256；"
                       "roster 由引文析出，逐条指向 quote id；matrix 由 roster 汇总。"),
            "sources": sources,
        },
        "quotes": quotes,
        "versions": versions,
        "roles": roles,
        "matrix": matrix,
        "typology": typology,
        "boundaries": boundaries,
        "summary": {
            "versions": len(versions),
            "quotes": len(quotes),
            "roles_attested": {r: len(v) for r, v in matrix.items()},
            "roster_total": sum(len(v["roster"]) for v in versions.values()),
        },
    }
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"versions {len(versions)}  quotes {len(quotes)}  "
          f"roster {data['summary']['roster_total']}")
    for qid, q in quotes.items():
        print(f"  {qid} {q['source']} {q['lb']} | {q['text'][:40]}…")
    print(f"written {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())