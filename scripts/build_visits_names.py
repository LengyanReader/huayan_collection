# -*- coding: utf-8 -*-
"""T9：入法界品逐参名三本字面对照（八十／六十／四十）。

数据来源：
  · 八十 T279：指授句「善男子！…名曰：X。汝(可)往/詣彼問」——取句中最后一个「名：X」为下一参名，
    同名连出（诗偈里的「觀自在」）去重；特例：摩耶（「有佛母摩耶」）、正趣（「名曰：正趣」）。
  · 六十 T278：名取自既有 60/40 逐参判总表（L.455），本脚本在 T278 入法界品内重新定位并记 lb。
  · 四十 T293：名与参界取自 rufajie_53_dataset.json，lb 由 span 起点换算。

只判字面：同／基同（一方为另一方子串）／异。所指是否同一，须语义与梵本判，本表不越界。
"""
import json
import hashlib
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, r"C:\DA_Practice\huayan_collection\scripts")
from build_translation_workshop import Doc  # noqa: E402

ROOT = Path(r"C:\DA_Practice\huayan_collection")
OUT = ROOT / "data" / "research" / "visits_names.json"

SUFFIX = ("比丘尼", "比丘", "長者", "居士", "優婆夷", "優婆塞", "童子師", "童子", "童女",
          "夜神", "天女", "菩薩", "婆羅門", "仙人", "船師", "外道", "地神", "林神",
          "釋女", "佛母", "王", "女", "天")
VERB = re.compile(r"汝(?:可|當|應)?(?:往|詣)(?:彼|於彼)?(?:問|而問)|汝可問之")
NAMEP = re.compile(r"(?:名之為|名[曰為]?|號[曰為]?)[：:]?([一-鿿]{2,14})")


def clean(name: str) -> str:
    n = re.sub(r"（[^）]*）|〔[^〕]*〕|\([^)]*\)", "", name)
    for s in SUFFIX:
        if n.endswith(s) and len(n) > len(s) + 1:
            n = n[:-len(s)]
            break
    return n.strip()


def first_part(name: str) -> str:
    return name.split("·")[0].strip()


def rel(a: str, b: str) -> str:
    if a == b:
        return "全同"
    if a and b and (a in b or b in a):
        return "基同"
    return "异"


def main() -> int:
    d80 = Doc("80", ROOT / "data/references/cbeta/T10n0279.xml")
    d60 = Doc("60", ROOT / "data/references/cbeta/T09n0278.xml")
    d40 = Doc("40", ROOT / "data/references/cbeta/T10n0293.xml")
    t80, t60, t40 = d80.flat, d60.flat, d40.flat

    s80 = t80.find("入法界品第三十九之一")
    s60 = t60.find("入法界品第三十四")
    seg80 = t80[s80:]

    # ---- 八十：指授句 → 下一参名 ----
    marks = []
    for m in VERB.finditer(seg80):
        w = seg80[max(0, m.start() - 420):m.start()]
        if "善男子" not in w[-320:]:
            continue
        nm = None
        if "有佛母摩耶" in w[-120:]:
            nm = "摩耶"
        elif "名曰：德生" in w[-160:] and "名為：有德" in w[-100:]:
            nm = "德生·有德"
        else:
            hits = list(NAMEP.finditer(w))
            if hits:
                nm = hits[-1].group(1)
        if not nm:
            continue
        pos = s80 + m.start()
        lb = d80.lb_at_raw(d80.raw_of_clean[d80.clean_of_flat[pos]])
        nm = clean(nm)
        if marks and marks[-1]["name"] == nm and pos - marks[-1]["pos"] < 3000:
            continue  # 诗偈里的同名假命中
        marks.append({"name": nm, "lb": lb, "pos": pos})

    # 只取前 50 个（卡 2–51；彌勒以下三卡为摄归，不在指授网内）
    marks = marks[:50]

    pair = json.loads((ROOT / "data/research/huayan_60_40_pairwise.json").read_text(encoding="utf-8"))
    rows_p = pair["rows"]
    if len(rows_p) != 50 or len(marks) != 50:
        print("!! rows", len(rows_p), "marks", len(marks))
        return 2

    # 六十：在 T278 内定位，按顺序单调就近取唯一命中
    seg60 = t60[s60:]
    prev60 = -1
    out_rows = []
    for mk, pr in zip(marks, rows_p):
        n60 = pr["n60"]
        probe = n60.split("·")[0]
        cand = [m.start() for m in re.finditer(re.escape(probe), seg60)]
        after = [c for c in cand if c > prev60]
        pick = after[0] if after else (cand[0] if cand else None)
        if pick is None:
            print("!! 60 name not found:", n60)
            return 3
        prev60 = pick
        lb60 = d60.lb_at_raw(d60.raw_of_clean[d60.clean_of_flat[s60 + pick]])
        out_rows.append({"no": pr["no"], "n80": mk["name"], "lb80": mk["lb"],
                         "pos80": mk["pos"],
                         "n60": n60, "lb60": lb60, "pos60": s60 + pick,
                         "n40raw": pr["n40"]})

    # 四十：在 T293 内按序就近定位（名取 60/40 判总表的 n40，字面在源文重切）
    prev40 = -1
    for r in out_rows:
        c = clean(r["n40raw"])
        probe = first_part(c)
        hits = [m.start() for m in re.finditer(re.escape(probe), t40)]
        after = [h for h in hits if h > prev40]
        if not after:
            print("!! 40 name not found:", r["n40raw"])
            return 4
        pick = after[0]
        prev40 = pick
        r["n40"] = c
        r["n40probe"] = probe
        r["lb40"] = d40.lb_at_raw(d40.raw_of_clean[d40.clean_of_flat[pick]])
        r["pos40"] = pick

    for r in out_rows:
        r["rel80_40"] = rel(r["n80"], r["n40"])
        r["rel80_60"] = rel(r["n80"], r["n60"])
        r["rel60_40"] = rel(r["n60"], r["n40"])

    def cnt(field, val):
        return sum(1 for r in out_rows if r[field] == val)

    stats = {
        "rows": len(out_rows),
        "rel80_40": {"全同": cnt("rel80_40", "全同"), "基同": cnt("rel80_40", "基同"),
                     "异": cnt("rel80_40", "异")},
        "rel80_60": {"全同": cnt("rel80_60", "全同"), "基同": cnt("rel80_60", "基同"),
                     "异": cnt("rel80_60", "异")},
        "rel60_40": {"全同": cnt("rel60_40", "全同"), "基同": cnt("rel60_40", "基同"),
                     "异": cnt("rel60_40", "异")},
        "all_same": sum(1 for r in out_rows if r["n80"] == r["n60"] == r["n40"]),
        "80eq60_ne40": sum(1 for r in out_rows if r["n80"] == r["n60"] != r["n40"]),
        "80eq40_ne60": sum(1 for r in out_rows if r["n80"] == r["n40"] != r["n60"]),
        "all_diff": sum(1 for r in out_rows if len({r["n80"], r["n60"], r["n40"]}) == 3),
    }

    sources = {}
    for key, p in (("80", "data/references/cbeta/T10n0279.xml"),
                   ("60", "data/references/cbeta/T09n0278.xml"),
                   ("40", "data/references/cbeta/T10n0293.xml")):
        fp = ROOT / p
        sources[key] = {"path": p, "bytes": fp.stat().st_size,
                        "sha256": hashlib.sha256(fp.read_bytes()).hexdigest()}

    data = {
        "meta": {
            "operator": "T9",
            "title": "入法界品逐参名：三本字面对照（卡 2–51）",
            "date": date.today().isoformat(),
            "method": ("八十名取指授句『善男子！…名曰：X。汝(可)往／詣彼問』中的 X 并记 lb；"
                       "六十名取既有 60/40 判总表（L.455），本脚本在 T278 内重新定位记 lb；"
                       "四十名取 rufajie_53_dataset.json 的 teacher_t40，lb 由参界 span 起点换算。"
                       "判定只就字面：全同／基同（子串）／异；所指同一性须语义与梵本判，本表不判。"),
            "scope": "卡 2–51（五十参）；卡 52–53 为文殊遥指·普賢摄归，不在指授网内。",
            "sources": sources,
        },
        "rows": out_rows,
        "stats": stats,
        "boundaries": [
            "这是字面判，不是所指判：『異』只说明两个字面不同，不等于两位善知识不同；反之『全同』也只证译名同字。",
            "八十本的指授句有动词异文（汝可往問／汝往彼問／汝詣彼問／汝可問之），本表以同一规则收句，仍可能漏收或多收；漏收处按序对位，须逐参复核。",
            "六十名的字面来自既有的 60/40 判总表（L.455），本表只补定位，不重判；两表冲突时以源文重切为准。",
            "四十本的诸参名多经般若新译改写（如善住→妙住、毘目瞿沙→大威猛聲），本表只记字面异同，不判孰为梵本正译。",
            "梵本《入法界品》未逐参对勘；Supratiṣṭhita 一名两译（善住／妙住）是既有旁证，其余诸参的梵名对应仍待核。",
        ],
    }
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"rows {len(out_rows)}  stats {stats}")
    for r in out_rows:
        print(f'{r["no"]:>2} {r["n80"]:<10} {r["lb80"]} | {r["n60"]:<10} {r["lb60"]} | '
              f'{r["n40"]:<12} {r["lb40"]} | {r["rel80_60"]}/{r["rel80_40"]}')
    print("written", OUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
