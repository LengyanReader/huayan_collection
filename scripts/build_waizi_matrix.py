#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""诸子百家·儒家·道家·印度诸典：统一采集＋对应矩阵探针。

范围（全部一手，Kanripo/GRETIL）：
  道家    老子（道德真經 KR5c0045）、莊子（郭象注 KR5c0138）
  儒家    論語（正文 KR1h0004）、孟子（KR1h0002）、大學（KR1h0015，已入库）、
          中庸（大學中庸集說啟蒙 KR1h0041 内）
  诸子    荀子（KR3a0002）、淮南鴻烈解（KR3j0010）
  印度    薄伽梵歌（GRETIL bhagvg_u）、Īśā Upaniṣad（GRETIL isup___u）

矩阵两层（只到类型判，不判谱系）：
  · C3 语汇层：修行-本体概念词频矩阵（每典 × 概念）
  · C1 结构层：每典取 1–2 条代表性「阶梯/本体」原文，起止锚切片，lb/位置可回源

判读纪律：非佛藏文本一律类型判；负向计数如实登记；不判史实接触。

Usage:
  python scripts/build_waizi_matrix.py
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "research" / "waizi_matrix.json"
BASE = "https://raw.githubusercontent.com/kanripo"
GRE = "https://gretil.sub.uni-goettingen.de/gretil"

CORPORA = {
    # id: (dir, edition, repo, nfiles, url)
    "laozi": ("daojia_laozi", "《道德真經》，戰國老子，Kanripo KR5c0045", "KR5c0045", 3, f"{BASE}/KR5c0045/master"),
    "zhuangzi": ("daojia_zhuangzi", "《莊子》郭象注，晉郭象，Kanripo KR5c0138", "KR5c0138", 11, f"{BASE}/KR5c0138/master"),
    "lunyu": ("rujia_lunyu", "《論語》正文，Kanripo KR1h0004", "KR1h0004", 20, f"{BASE}/KR1h0004/master"),
    "mengzi": ("rujia_mengzi", "《孟子》，漢趙岐注本，Kanripo KR1h0002", "KR1h0002", 15, f"{BASE}/KR1h0002/master"),
    "zhongyong": ("rujia_zhongyong", "《中庸》（大學中庸集說啟蒙内），元景星，Kanripo KR1h0041", "KR1h0041", 3, f"{BASE}/KR1h0041/master"),
    "xunzi": ("zhuzi_xunzi", "《荀子》，周荀况，Kanripo KR3a0002", "KR3a0002", 23, f"{BASE}/KR3a0002/master"),
    "huainanzi": ("zhuzi_huainanzi", "《淮南鴻烈解》，漢高誘注，Kanripo KR3j0010", "KR3j0010", 22, f"{BASE}/KR3j0010/master"),
}

GRETEX = {
    "bhagavadgita": ("yindu_bhagavadgita", "《薄伽梵歌》，Mahābhārata 北本，GRETIL bhagvg_u（Unicode）",
                     f"{GRE}/1_sanskr/2_epic/mbh/ext/bhagvg_u.htm"),
    "ishaupanisad": ("yindu_ishaupanisad", "《Īśā Upaniṣad》，GRETIL isup___u（Unicode）",
                     f"{GRE}/1_sanskr/1_veda/4_upa/isup___u.htm"),
}

# 语汇矩阵：修行-本体概念（C3 共享语汇层）
CONCEPTS = ["道", "德", "聖人", "心", "性", "命", "天", "氣", "神", "靜",
            "虛", "自然", "誠", "聖", "智", "仁", "義", "禮"]
BUDDHIST_ANCHORS = ["法界", "華嚴", "圓融", "涅槃"]

# 结构层：代表性阶梯/本体原文（起止锚，逐条回源；锚为库内实测形态）
STRUCT = {
    "laozi": [
        ("道生一一生二二生三三生萬物", "本体生成序列（四十二章）"),
        ("人法地地法天天法道道法自然", "终极依止序列（二十五章）"),
    ],
    "zhuangzi": [
        ("至人無已", "三无境界之一（逍遥游，郭象注本作「已」）"),
        ("天地與我並生而萬物與我為一", "齐物一元（齐物论）"),
    ],
    "lunyu": [
        ("三十而立，四十而不惑，五十而知天命，六十而耳順",
         "自述生命阶梯（为政）"),
    ],
    "mengzi": [
        ("充實之謂美充實而有光輝之謂大大而化之之謂聖聖而不可知之謂神",
         "六阶人格序列（尽心下）"),
    ],
    "zhongyong": [
        ("天命之謂性率性之謂道修道之謂教", "开篇三句（性→道→教）"),
        ("誠者天之道思誠者人之道", "诚为本体-功夫两轮"),
    ],
    "xunzi": [
        ("其數則始乎誦經終乎讀禮", "为学之数（劝学）"),
        ("其義則始乎爲士終乎爲聖人", "为学之义：士→圣人阶梯"),
    ],
    "huainanzi": [
        ("聖人内修其本而不外飾其末", "内本外末（原道训，作「内」）"),
    ],
    "bhagavadgita": [
        ("kūrmo", "收摄诸根如龟（2.58，龟喻）"),
        ("sthitaprajñasya", "立ち于智慧安定者之问（2.54 章首）"),
    ],
    "ishaupanisad": [
        ("ātman", "梵我关键词（全文 18 颂）"),
    ],
}


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "huayan-fetch/1.0"})
    with urllib.request.urlopen(req, timeout=180) as r:
        return r.read()


def strip_markers(t: str) -> str:
    t = re.sub(r"<pb:[^>]*>", "", t)
    t = re.sub(r"<[^>]+>", "", t)
    t = t.replace("¶", "")
    return t


def main() -> int:
    corpora = {}
    hits_all = {}
    for cid, (slug, edition, repo, nfiles, urlbase) in CORPORA.items():
        d = ROOT / "data" / "references" / slug
        d.mkdir(parents=True, exist_ok=True)
        files, failed = {}, []
        for n in range(nfiles):
            name = f"{repo}_{n:03d}.txt"
            p = d / name
            if not p.exists():
                try:
                    p.write_bytes(fetch(f"{urlbase}/{name}"))
                except Exception as e:  # noqa: BLE001
                    failed.append({"file": name, "err": str(e)[:80]})
                    continue
            raw = p.read_bytes()
            files[name] = {"bytes": len(raw), "sha256": sha256(raw)}
        text = "".join(strip_markers((d / f"{repo}_{n:03d}.txt").read_text(
            encoding="utf-8", errors="replace")) for n in range(nfiles)
            if (d / f"{repo}_{n:03d}.txt").exists())
        flat = re.sub(r"\s+", "", text)
        matrix = {k: flat.count(k) for k in CONCEPTS + BUDDHIST_ANCHORS}
        struct = []
        for a, note in STRUCT.get(cid, []):
            aa = re.sub(r"\s+", "", a)
            idx = flat.find(aa)
            if idx >= 0:
                struct.append({"quote": a, "note": note, "pos": idx,
                               "verbatim": True})
            else:
                struct.append({"quote": a, "note": note, "verbatim": False,
                               "pos_found": flat.find(aa[:10])})
        corpora[cid] = {"slug": slug, "edition": edition, "dir": str(d.relative_to(ROOT)),
                        "files": files, "flat_chars": len(flat),
                        "matrix": matrix, "struct": struct}
        hits_all[cid] = matrix
        print(f"  · {cid}: {len(flat):,} chars, matrix done, "
              f"struct {sum(1 for s in struct if s.get('verbatim'))}/{len(struct)}")

    grex = {}
    for cid, (slug, edition, url) in GRETEX.items():
        d = ROOT / "data" / "references" / slug
        d.mkdir(parents=True, exist_ok=True)
        p = d / (cid + ".txt")
        if not p.exists():
            p.write_bytes(fetch(url))
        raw = p.read_text(encoding="utf-8", errors="replace")
        # 去 HTML 标签与头部
        raw = re.sub(r"<[^>]+>", "", raw)
        raw = re.sub(r"\{[^}]*\}", "", raw)
        text = strip_markers(raw)
        flat = re.sub(r"\s+", "", text)
        matrix = {k: flat.count(k) for k in
                  ["ātman", "brahman", "dharma", "yoga", "mokṣa", "karma",
                   "jñāna", "bhakti", "dhyāna", "tapas"]}
        struct = []
        for a, note in STRUCT.get(cid, []):
            aa = re.sub(r"\s+", "", a)
            idx = flat.find(aa)
            struct.append({"quote": a, "note": note, "verbatim": idx >= 0,
                           "pos": idx})
        grex[cid] = {"slug": slug, "edition": edition, "dir": str(d.relative_to(ROOT)),
                     "flat_chars": len(flat), "matrix": matrix, "struct": struct}
        print(f"  · {cid}: {len(flat):,} chars")

    data = {
        "meta": {
            "date": date.today().isoformat(),
            "purpose": "诸子百家·儒家·道家·印度诸典：C3 语汇矩阵＋C1 结构层（类型判专用）",
            "method": "全文本去标记后做概念词频矩阵（只作量级参考）；结构层取代表性原文，"
                      "起止锚逐字回源（verbatim=true 才算实据）；佛藏锚词（法界/華嚴/圓融/涅槃）"
                      "计入以显接触面之有无。",
            "concepts": CONCEPTS + BUDDHIST_ANCHORS,
            "discipline": "非佛藏文本一律类型判；负向计数如实；不判历史接触。",
        },
        "corpora": corpora,
        "gretil": grex,
        "summary": {"corpora": len(corpora) + len(grex)},
    }
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("written", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
