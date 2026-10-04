# -*- coding: utf-8 -*-
"""世主妙严品·底本实测口径（唯一权威）。

口径（凡本文所称「T279 实测」皆依此）：
  1. 以 data/references/cbeta/T10n0279.xml 为底本；
  2. 剥离控制符（PDF 抽取伪影）、<note> 校勘记、<app>/<rdg>/<lem> 校勘异文；
  3. 剥离一切空白与全角空格；
  4. 逐卷以 <cb:juan n="NNN" fun="open"> 位置切分；
  5. 「本品」= 卷一至卷五；「全经」= 卷一至卷八十。
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8")

T279 = ROOT / "data/references" / "cbeta" / "T10n0279.xml"


def _clean(s, drop_app=True):
    s = re.sub(r"[\x00-\x08\x0b-\x1f]", "", s)
    s = re.sub(r"<note\b.*?</note>", "", s, flags=re.S)
    if drop_app:
        s = re.sub(r"<app\b.*?</app>", "", s, flags=re.S)
    return re.sub(r"<[^>]+>", "", s)


def _juan_of(xml, drop_app=True):
    opens = [(m.start(), int(m.group(1)))
             for m in re.finditer(r'<cb:juan n="(\d+)" fun="open">', xml)]
    bounds = [p for p, _ in opens] + [len(xml)]
    return {n: re.sub(r"[\s\u3000]", "", _clean(xml[p:bounds[i + 1]], drop_app))
            for i, (p, n) in enumerate(opens)}


def cjk_len(s):
    """本文口径的字数：仅计中日韩表意文字（含扩展 A），不计标点、不计异文。"""
    return sum(1 for ch in s
               if "\u4e00" <= ch <= "\u9fff" or "\u3400" <= ch <= "\u4dbf")


def sentences(s):
    """本文口径的句数：以句号「。」计。"""
    return s.count("。")


def load():
    xml = T279.read_bytes().decode("utf-8")
    J = _juan_of(xml)
    return J


def stats():
    J = load()
    pin = "".join(J[n] for n in range(1, 6))
    quan = "".join(J[n] for n in sorted(J))
    out = {
        "juan_count": len(J),
        "pin_cjk": cjk_len(pin),
        "pin_sent": sentences(pin),
        "quan_cjk": cjk_len(quan),
        "per_juan": {str(n): {"cjk": cjk_len(J[n]), "sent": sentences(J[n])}
                     for n in range(1, 6)},
    }
    keys = ["解脫門", "承佛威力", "承佛威神", "承佛神力", "復承如來威神之力",
            "而說頌言", "即說頌言", "而說頌曰", "爾時", "如是等而為上首"]
    out["pin"] = {k: pin.count(k) for k in keys}
    out["quan"] = {k: quan.count(k) for k in keys}
    out["per_juan_keys"] = {
        str(n): {k: J[n].count(k) for k in
                 ["解脫門", "承佛威力", "承佛威神", "承佛神力",
                  "而說頌言", "即說頌言", "而說頌曰"]}
        for n in range(1, 6)}
    return out


if __name__ == "__main__":
    st = stats()
    print(json.dumps(st, ensure_ascii=False, indent=2))
    # 对账
    pin = st["pin"]
    groups = (pin["承佛威力"] + pin["承佛威神"] + pin["承佛神力"]
              + pin["復承如來威神之力"])
    utter = pin["而說頌言"] + pin["即說頌言"] + pin["而說頌曰"]
    print(f"\n对账：导语式 {groups} ／ 说颂式 {utter} （二者皆应为 52 组）",
          "OK" if groups == utter == 52 else "!! 不平")
    print(f"对账：卷一–五 颂块组数 12+13+14+13 = {12+13+14+13}")
    assert groups == utter, "导语式与说颂式组数不平"