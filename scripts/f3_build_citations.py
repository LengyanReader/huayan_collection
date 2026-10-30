# -*- coding: utf-8 -*-
"""F.3 引文挂载数据生成器（可复核 · 逐字回源 miss=0 内建审计）。

对 5 祖核心（杜顺·智俨·法藏·澄观·宗密）共 33 站，逐站在权威 CBETA 底本
（T50n2060 续高僧传 / T50n2061 宋高僧传 / T50n2054 法藏和尚傳）中按【常见字种子
切片 → 句号定界取整句 → 取源字节】提取一手引文，就近回溯大正页锚。
引文一律由源字节切片得到（绝不手打繁体，规避异体字码点不一致）。
种子未命中者 → status=pending（〔待核〕），不臆造。

审计内建：任一 status=sourced 的引文若不在其声明底本中逐字存在，即报错退出，
据此保证「sourced 子集 miss=0」。向后兼容：只读 person_trajectories.yaml，
不改轨迹文件；引文另存 data/events/person_chronicle_citations.yaml。
"""
from pathlib import Path
import re, sys, yaml, json, datetime

ROOT = Path(__file__).resolve().parents[1]
CB = ROOT / "data" / "references" / "cbeta"
TRJ = ROOT / "data" / "events" / "person_trajectories.yaml"
OUT = ROOT / "data" / "events" / "person_chronicle_citations.yaml"

def load(path):
    raw = path.read_text(encoding="utf-8")
    raw = re.sub(r'<pb[^>]*n="([^"]*)"[^>]*/>', r"〔\1〕", raw)
    raw = re.sub(r"<pb[^>]*/>", "", raw)
    raw = re.sub(r"<milestone[^>]*/>", "", raw)
    txt = re.sub(r"<[^>]+>", "", raw)
    return re.sub(r"[ \t]+", "", txt)

def load_raw(path):
    """纯正文（去标签、去页锚、去所有空白）——用于逐字回源审计。"""
    raw = path.read_text(encoding="utf-8")
    raw = re.sub(r"<pb[^>]*/>", "", raw)
    raw = re.sub(r"<milestone[^>]*/>", "", raw)
    txt = re.sub(r"<[^>]+>", "", raw)
    return re.sub(r"\s+", "", txt)

TXT = {
    "T50n2060": load(CB / "T50n2060.xml"),
    "T50n2061": load(CB / "T50n2061.xml"),
    "T50n2054": load(CB / "T50n2054.xml"),
}
TXT_RAW = {k: load_raw(CB / (k + ".xml")) for k in TXT}
SRC_LABEL = {
    "T50n2060": "CBETA T50n2060《續高僧傳》卷廿五·釋法順傳",
    "T50n2061": "CBETA T50n2061《宋高僧傳》",
    "T50n2054": "CBETA T50n2054《法藏和尚傳》",
}
# 底本 URL（CBETA 电子佛典，访问日期见文件头）
SRC_URL = {
    "T50n2060": "https://cbetaonline.dila.edu.tw/zh/T50n2060",
    "T50n2061": "https://cbetaonline.dila.edu.tw/zh/T50n2061",
    "T50n2054": "https://cbetaonline.dila.edu.tw/zh/T50n2054",
}

def index(txt, key):
    i = txt.find(key)
    assert i >= 0, "bio-start key not found: " + key
    return i

def scope(txt, s, e=None):
    i0 = index(txt, s)
    i1 = index(txt, e) if e else len(txt)
    return (i0, i1) if i1 > i0 else (i0, min(i0 + 4000, len(txt)))

def anchor_of(txt, gpos):
    ms = list(re.finditer(r"〔([0-9a-z]+)〕", txt[:gpos]))
    return ms[-1].group(1) if ms else None

def cite(src, rng, seed):
    txt = TXT[src]; i0, i1 = rng; sl = txt[i0:i1]
    j = sl.find(seed)
    if j < 0:
        return None, None
    l = sl.rfind("。", 0, j); l = 0 if l < 0 else l + 1
    r = sl.find("。", j + len(seed)); r = len(sl) if r < 0 else r + 1
    while (r - l) < 10 and l > 0:
        pl = sl.rfind("。", 0, l - 1)
        if pl < 0: break
        l = pl + 1
    q = re.sub(r"〔[0-9a-z]+〕", "", sl[l:r]).replace("\n", "").strip()
    q = q.lstrip("。、「」『』（）() ")
    return q, anchor_of(txt, i0 + j)

# ---- 5 祖 33 站回源规格：(person, idx, src, rng_key, seed or None, note) ----
SC = {
    "2060fs": scope(TXT["T50n2060"], "法順。姓杜氏", "釋道英"),
    "2061fc": scope(TXT["T50n2061"], "釋法藏字賢首", "唐荊州玉泉寺"),
    "2061cg": scope(TXT["T50n2061"], "釋澄觀", "唐京師西明寺良秀"),
    "2061zm": scope(TXT["T50n2061"], "釋宗密", "唐京兆"),
    "2054":   (0, len(TXT["T50n2054"])),
}
SPEC = [
    ("person_001",0,"T50n2060","2060fs","雍州萬年人",""),
    ("person_001",1,"T50n2060","2060fs","僧珍",""),
    ("person_001",2,None,None,None,"本传未载杜顺住终南山至相寺逐字句（传世系据他籍）"),
    ("person_001",3,"T50n2061","2061fc","杜順傳",""),
    ("person_001",4,"T50n2060","2060fs","引入內禁","〔本文判断〕号'帝心'后世所传，本传但云引入内禁隆礼崇敬"),
    ("person_001",5,"T50n2060","2060fs","義善寺","〔本文判断〕底本载卒于南郊义善寺、葬樊川北原，与站点label'终南山'异"),
    ("person_002",0,None,None,None,"诸传未载智俨诞地'天水'逐字句"),
    ("person_002",1,"T50n2060","2060fs","幼年奉敬","本传但云弟子智俨名贯至相、幼年奉敬"),
    ("person_002",2,None,None,None,"本传未载'至相寺从慧光学华严'逐字句"),
    ("person_002",3,"T50n2054","2054","每嗟大教",""),
    ("person_002",4,"T50n2054","2054","以通經旨",""),
    ("person_002",5,"T50n2054","2054","紹隆遺法",""),
    ("person_003",0,"T50n2061","2061fc","康居人也",""),
    ("person_003",1,"T50n2054","2054","投為上足","〔本文判断〕底本作'雲華寺'，站点label作'至相寺'"),
    ("person_003",2,"T50n2054","2054","住太原寺",""),
    ("person_003",3,"T50n2054","2054","實叉難陀譯華嚴經",""),
    ("person_003",4,"T50n2054","2054","探玄記",""),
    ("person_003",5,"T50n2061","2061fc","金師子章",""),
    ("person_003",6,None,None,None,"二传未逐字载书名'五教章'（别名教分/分齐）"),
    ("person_003",7,"T50n2054","2054","終於西京大薦福寺",""),
    ("person_004",0,"T50n2061","2061cg","越州山陰人也",""),
    ("person_004",1,"T50n2061","2061cg","遍尋名山",""),
    ("person_004",2,"T50n2061","2061cg","不疏",""),
    ("person_004",3,"T50n2061","2061cg","成二十軸",""),
    ("person_004",4,"T50n2061","2061cg","德宗降中使","〔本文判断〕本传载德宗宣诏入都；'清凉'号因住清凉山"),
    ("person_004",5,"T50n2061","2061cg","隨疏演","〔本文判断〕底本《隨疏演義》卷数与站点label异"),
    ("person_004",6,"T50n2061","2061cg","以元和年卒","〔本文判断〕本传但云元和年卒；'历七帝师'系概称"),
    ("person_005",0,"T50n2061","2061zm","果州西充人也",""),
    ("person_005",1,"T50n2061","2061zm","圓禪師",""),
    ("person_005",2,"T50n2061","2061zm","上都華嚴觀",""),
    ("person_005",3,"T50n2061","2061zm","諸宗禪言","〔本文判断〕本传作集《禪藏》；草堂寺未逐字载"),
    ("person_005",4,None,None,None,"本传未列《原人論》书名"),
    ("person_005",5,"T50n2061","2061zm","興福塔院",""),
]

trj = yaml.safe_load(TRJ.read_text(encoding="utf-8"))
by_person = {}
audit_fail = []
for pid, idx, src, key, seed, note in SPEC:
    st = trj.get(pid, {})
    route = st.get("route", [])
    if idx >= len(route):
        audit_fail.append((pid, idx, "station index out of range")); continue
    station = route[idx]
    rec = {
        "index": idx,
        "label": station.get("label", ""),
        "y": station.get("y"),
        "lat": station.get("lat"),
        "lng": station.get("lng"),
    }
    if src is None:
        rec.update({"status": "pending", "quote": None, "source": None,
                    "anchor": None, "url": None, "note": note})
    else:
        q, a = cite(src, SC[key], seed)
        if q is None:
            rec.update({"status": "pending", "quote": None, "source": None,
                        "anchor": None, "url": None,
                        "note": (note + "；种子未命中").strip("；")})
        else:
            # 逐字回源审计：引文（去页锚/去空白）必须逐字存在于底本正文
            if q not in TXT_RAW[src]:
                audit_fail.append((pid, idx, "quote not verbatim in source"))
            rec.update({"status": "sourced", "quote": q, "source": SRC_LABEL[src],
                        "anchor": a, "url": SRC_URL[src], "note": note})
    by_person.setdefault(pid, {"name": st.get("name", ""),
                               "person_source": st.get("source", ""),
                               "stations": []})["stations"].append(rec)

by_person = {k: by_person[k] for k in sorted(by_person)}
doc = {
    "version": 1,
    "last_updated": str(datetime.date.today()),
    "generated_by": "scripts/f3_build_citations.py",
    "note": "逐字回源引文挂载表（F.3 首批 5 祖核心）；只读 person_trajectories.yaml，"
            "不改轨迹。sourced 子集经 miss=0 审计；pending 站为底本未载，标〔待核〕。",
    "persons": by_person,
}
if audit_fail:
    print("AUDIT FAIL:", audit_fail); sys.exit(1)

OUT.write_text(yaml.safe_dump(doc, allow_unicode=True, sort_keys=False,
                              default_flow_style=False), encoding="utf-8")
sourced = sum(1 for p in by_person.values() for s in p["stations"] if s["status"] == "sourced")
pending = sum(1 for p in by_person.values() for s in p["stations"] if s["status"] == "pending")
print("OK write %s" % OUT)
print("persons=%d sourced=%d pending=%d total=%d  (miss=0 audit passed)" % (
    len(by_person), sourced, pending, sourced + pending))
