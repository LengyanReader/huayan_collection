#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""C 面扩样＋D5 补样：瑜伽经／參同契／無上祕要（一手新入库）。

C1/C3 扩样两个新传统：
  · 印度·瑜伽（Pātañjala-yoga-sūtra，GRETIL corpustei 明文）
    ——定义段（1.1–1.2）锚点切片；修行概念词频矩阵。
  · 道教·丹道（《周易參同契分章通真義》，漢魏伯陽本·後蜀彭曉註，Kanripo KR5d0019）
    ——开篇生成论锚点；炉鼎词频矩阵。
判读纪律：非佛藏文本一律类型判；负向计数如实（佛藏锚词应为 0）。

D5 补样：《無上祕要》（北周武帝敕编，Kanripo KR5e0040，存 68/100 卷）
  ——现存卷的主体是斋醮仪典类书（齋×537、醮×16），义理内核章目
  （道性等）不在现存卷（道性 0 次）——D5 第二部道经的内核共享
  取样为**负向**；现存层与《華嚴》可对读的是观行操作层（存思服食
  vs 定观），给一组操作层双侧引文，标类型判。
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_implicit_quotes import Doc  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "research" / "c_expand.json"


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def slice_norm(doc: Doc, a: str, b: str) -> dict:
    i = doc.norm.find(a)
    j = doc.norm.find(b, i if i >= 0 else 0)
    if i < 0 or j < 0:
        raise SystemExit(f"anchor not found in {doc.name}: {a[:14]}")
    c0 = doc.clean_of_norm[i]
    c1 = doc.clean_of_norm[min(j + len(b), len(doc.norm) - 1)]
    return {"lb": doc.lb_at(doc.raw_index(i)),
            "text": doc.clean[c0:c1 + len(b)].replace("\n", "")}


def main() -> int:
    # ---- 參同契（Kanripo txt，去 mandoku 头） ----
    cq_text = ""
    cq_files = {}
    for p in sorted((ROOT / "data/references/daozang_cantongqi").glob("KR5d0019_*.txt")):
        raw = p.read_bytes()
        cq_files[p.name] = {"bytes": len(raw), "sha256": sha256(raw)}
        t = re.sub(r"[#\[\]|<>]", "", p.read_text(encoding="utf-8", errors="replace"))
        t = re.sub(r"\+?[A-Z_]+:.*?\n", "", t)
        cq_text += re.sub(r"\s+", "", t)
    cq_terms = ["乾坤", "坎離", "鼎", "爐", "鉛", "汞", "龍虎", "火候", "周天",
                "性命", "丹", "藥", "虚無", "自然", "五行的行", "法界", "圓融", "涅槃"]
    cq_terms = [t for t in cq_terms if t != "五行的行"]
    cq_matrix = {t: cq_text.count(t) for t in cq_terms}

    # ---- 瑜伽经（GRETIL 明文） ----
    yg_raw = (ROOT / "data/references/sanskrit/yoga_sutra.txt").read_bytes()
    yg_txt = yg_raw.decode("utf-8", errors="replace")
    yg = re.sub(r"[#*\[\]_]", "", yg_txt)
    yg_flat = re.sub(r"\s+", "", yg)
    yg_terms = ["yoga", "citta", "vṛtti", "nirodha", "samādhi", "dhyāna",
                "abhyāsa", "vairāgya", "kaivalya", "puruṣa", "prakṛti",
                "īśvara", "kleśa", "dharma", "mokṣa"]
    yg_matrix = {t: yg_flat.count(t) for t in yg_terms}

    # ---- 錨點切片 ----
    d19 = Doc("KR5d0019", ROOT / "data/references/daozang_cantongqi/KR5d0019_001.txt")
    cq_struct = {
        "generation": slice_norm(d19, "乾坤者易之門户", "坎離匡郭運轂正軸"),
        "note": "开篇章：乾坤门户→坎離匡郭——丹道以易卦框架立炉鼎结构〔本文判读〕",
    }

    class GD(Doc):  # GRETIL 明文没有 lb 行号，用位置
        pass
    yg_struct = {"def_pos": yg_flat.find("athayogānuśāsanam"),
                 "text": ("atha yogānuśāsanam ｜ yogaś citta-vṛtti-nirodhaḥ"),
                 "note": "1.1–1.2 定义段：瑜伽＝心作用之止息〔GRETIL 明文无行号，位置可回源〕"}

    # ---- 無上祕要（D5 补样） ----
    wu_text = ""
    wu_files = {}
    for p in sorted((ROOT / "data/references/daozang_wushang").glob("KR5e0040_*.txt")):
        raw = p.read_bytes()
        wu_files[p.name] = {"bytes": len(raw), "sha256": sha256(raw)}
        t = re.sub(r"[#\[\]|<>]", "", p.read_text(encoding="utf-8", errors="replace"))
        t = re.sub(r"\+?[A-Z_]+:.*?\n", "", t)
        wu_text += re.sub(r"\s+", "", t)
    wu_terms = ["齋", "醮", "觀", "存思", "服食", "道性", "佛性", "法身",
                "眾生", "三界", "大乘"]
    wu_matrix = {t: wu_text.count(t) for t in wu_terms}
    d40 = Doc("KR5e0040", ROOT / "data/references/daozang_wushang/KR5e0040_001.txt")
    # 存思服食操作层引文（全文跨卷，找含「服食青牙」的卷）
    wu_quote = None
    for name in wu_files:
        dtry = Doc("KR5e0040", ROOT / "data/references/daozang_wushang" / name)
        i = dtry.norm.find("服食青牙")
        if i >= 0:
            wu_quote = {"file": name, "pos": i,
                        "text": dtry.norm[max(0, i - 30):i + 50],
                        "note": "五牙服食·存想五方炁入身（操作层，无 CBETA 式行号，卷档+位置可回源）"}
            break
    t279 = Doc("T279", ROOT / "data/references/cbeta/T10n0279.xml")
    t279_quote = slice_norm(t279, "一微塵中入三昧", "於一普現難思剎")

    data = {
        "meta": {
            "date": date.today().isoformat(),
            "title": "C 面扩样（瑜伽经/參同契）＋D5 补样（無上祕要）",
            "method": ("词频矩阵只作量级参考；结构锚点切片可回源；"
                       "非佛藏文本一律类型判；佛藏锚词负向计数如实。"),
            "sources": {
                "cantongqi": {"dir": "data/references/daozang_cantongqi",
                              "files": cq_files},
                "yogasutra": {"path": "data/references/sanskrit/yoga_sutra.txt",
                              "sha256": sha256(yg_raw),
                              "bytes": len(yg_raw)},
                "wushangmiyao": {"dir": "data/references/daozang_wushang",
                                 "files": wu_files},
                "t279": {"path": "data/references/cbeta/T10n0279.xml",
                         "sha256": sha256((ROOT / "data/references/cbeta/T10n0279.xml").read_bytes())},
            },
        },
        "cantongqi": {"matrix": cq_matrix, "struct": cq_struct,
                      "chars": len(cq_text)},
        "yogasutra": {"matrix": yg_matrix, "struct": yg_struct,
                      "chars": len(yg_flat)},
        "wushangmiyao": {"matrix": wu_matrix, "quote": wu_quote,
                         "t279_quote": t279_quote, "chars": len(wu_text)},
    }
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n",
                   encoding="utf-8")
    print("參同契 matrix:", {k: v for k, v in cq_matrix.items() if v})
    print("yoga matrix:", {k: v for k, v in yg_matrix.items() if v})
    print("無上祕要 matrix:", wu_matrix)
    print("wu_quote:", json.dumps(wu_quote, ensure_ascii=False)[:150] if wu_quote else None)
    print("written", OUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
