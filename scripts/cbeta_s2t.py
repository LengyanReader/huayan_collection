#!/usr/bin/env python3
"""cbeta_s2t.py — 以 CBETA 经文自身反推「简体→繁体」字表，取代通用简繁转换器

缘起（编务原则：原文是什么语言就用什么，简体与英文只作说明性语言）：
中文经卷的「原文」是 CBETA 所录字形，回填须得原字。通用转换器不可靠：
  · opencc s2tw：了→瞭、复次→複次（CBETA 作了、復次）
  · opencc s2t ：众→衆、为→爲（CBETA 作眾、為）
  · zhconv zh-hant：干→幹（乾闼婆遂成幹闥婆）、里→裏
皆非佛典正字，一经误用便把「引文有讹」的冤判加在清白经文上。

办法：转换本该「由经证经」。手上既已有 T279 全文（T279 为繁体），
则对每个待转之简体字，取各转换器所给候选繁体形，逐一回到 T279 中查其是否
真见；独见者即正字，一一对应。多个形皆见者（如干→乾/幹）标为歧义，不臆断，
交由上层按上下文定位或列为待核。所得字表落盘为 JSON，可审计、可复用。

字表格式：{"复": {"form": "復", "count": 4213}, "干": {"forms": ["幹", "乾"], "ambiguous": true}}
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from functools import lru_cache
from pathlib import Path

from opencc import OpenCC
from zhconv import convert as _zh

CJK = re.compile(r"[\u3400-\u9fff\U00020000-\U0002ffff]")

MAP_PATH = Path(__file__).with_name("cbeta_char_map.json")
_cc_tw = OpenCC("s2tw")

# 各转换器候选不全之处，依 T279 实见字形补入候选（仍走「回经中查证」，
# 不直接指定结果）。例：zhconv 对「干」只给 幹/干，而 T279 实见「乾闥婆」。
EXTRA_CANDIDATES = {
    "干": ["乾", "幹", "干"], "只": ["只", "隻", "衹"], "后": ["後", "后"],
    "咸": ["咸", "鹹"], "里": ["裡", "裏", "里"], "复": ["復", "複", "复"],
    "面": ["面", "麵", "麪"], "发": ["發", "髮"], "台": ["臺", "台"],
    "系": ["系", "係", "繫"], "舍": ["舍", "捨"], "划": ["划", "劃"],
    "表": ["表", "錶"], "板": ["板", "闆"],
    # 佛典异体与专名正字（皆经 T279 实见，故列入候选而不径定）：
    "修": ["修", "脩"],          # 阿脩羅之脩，非修行之修
    "疏": ["疏", "踈"],          # 寶葉扶踈
    "骄": ["骄", "憍", "驕"],     # 憍慢
    "踊": ["踊", "踴"],          # 踴躍
    "燄": ["燄", "焰"],          # 妙焰海
    "晖": ["暉", "輝"],          # 含輝發焰
    "脐": ["脐", "臍", "𪗇"],     # 大精進金剛𪗇
    "睹": ["睹", "覩"],          # 皆明覩
    "荡": ["蕩", "蕩"],
    "荫": ["蔭", "荫"],
    "并": ["並", "併", "并"],
    "剩": ["剩", "賸"],
    "弥": ["彌", "弥"],
    "签": ["籤", "簽"],
    "占": ["占", "佔"],
    # 以下六组为《世主妙严品》实证之正字（皆 T279 实见，见 collate 记录）：
    "毗": ["毗", "毘"],          # 毘盧遮那、毘摩質多羅
    "秘": ["秘", "祕"],          # 祕密之境
    "稀": ["稀", "希"],          # 希有
    "绕": ["绕", "遶"],          # 所共圍遶
    "回": ["回", "迴"],          # 周迴間列
    "踊": ["踊", "涌", "踴"],     # 十八相作「涌、遍涌、普遍涌」
}

# 转换器一概不作此转者，依 T279 实见正字直接入表（须有经文实证）：
#   沉 → 沈：T279 作「沈迷惡道受諸苦」，不作「沉迷」（沈沒義，CBETA 通作沈）。
MANUAL = {"沉": "沈"}


def candidate_forms(c: str) -> list[str]:
    """一个简体字可能对应的全部繁体候选（含其本身），顺序即偏好序。"""
    out = []
    for f in (_cc_tw.convert(c), _zh(c, "zh-hant"), _zh(c, "zh-hant-tw"),
              _zh(c, "zh-cn"), c):
        if f and f not in out:
            out.append(f)
    for f in EXTRA_CANDIDATES.get(c, []):
        if f not in out:
            out.append(f)
    return out


class CbetaS2T:
    def __init__(self, sutra: str, map_path: Path = MAP_PATH, verbose: bool = False):
        self.sutra = sutra
        self.map_path = map_path
        self.counts = Counter(sutra)
        self.table: dict[str, dict] = {}
        if map_path.exists():
            self.table = json.loads(map_path.read_text(encoding="utf-8"))
        self.new: dict[str, dict] = {}
        self.verbose = verbose

    def resolve(self, c: str) -> dict:
        if c in self.table:
            return self.table[c]
        if c in MANUAL:
            rec = {"form": MANUAL[c], "count": self.counts.get(MANUAL[c], 0),
                   "note": "依 T279 实见正字入表"}
        else:
            forms = [f for f in candidate_forms(c) if self.counts.get(f, 0) > 0]
            if not forms:
                # 经中不见任何候选形（如「只」）：保留原字，交由上层定位失败后列待核
                rec = {"forms": [c], "ambiguous": True, "note": "T279 无对应正字"}
            elif len(forms) == 1:
                rec = {"form": forms[0], "count": self.counts[forms[0]]}
            else:
                rec = {"forms": forms, "ambiguous": True,
                       "counts": {f: self.counts[f] for f in forms}}
        self.table[c] = rec
        self.new[c] = rec
        return rec

    def convert(self, s: str) -> str:
        out = []
        for ch in s:
            rec = self.resolve(ch)
            out.append(rec["form"] if "form" in rec else ch)
        return "".join(out)

    def save(self) -> int:
        if not self.new:
            return 0
        self.map_path.write_text(
            json.dumps(self.table, ensure_ascii=False, indent=1, sort_keys=True),
            encoding="utf-8")
        return len(self.new)


@lru_cache(maxsize=4)
def get_s2t(sutra: str, map_path: str = str(MAP_PATH)) -> CbetaS2T:
    return CbetaS2T(sutra, Path(map_path))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    xml = Path(sys.argv[1] if len(sys.argv) > 1
               else r"C:\Users\data\AppData\Local\Temp\opencode\t10n0279.xml")
    sutra = re.sub(r"<[^>]+>", "", xml.read_text(encoding="utf-8")).replace("\n", "")
    eng = CbetaS2T(sutra)
    probe = sys.argv[2] if len(sys.argv) > 2 else "了复众为干只后里面发沉复痴咸"
    for ch in probe:
        rec = eng.resolve(ch)
        mark = "歧" if rec.get("ambiguous") else "定"
        shown = rec.get("form") or "/".join(rec["forms"])
        print(f"  {ch} → {shown}  [{mark}]  {rec.get('count', rec.get('counts', ''))}")
    n = eng.save()
    print(f"字表新增 {n} 字 → {eng.map_path.name}")
