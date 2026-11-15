#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""R5 灵验叙事：《華嚴經傳記》（唐法藏集，T51n2073）一手回源。

本文是本经自己的接受史：十篇目（部類/隱顯/傳譯/支流/論釋/講解/諷誦/轉讀/書寫/雜述）。
本探针取諷誦、轉讀、書寫三篇的灵验故事，逐条以起止锚切片，lb 可回源。

与既有算子的交叉（只记交叉，不在此判）：
  · 普安「受持華嚴力」北周滅法脱难 —— 与 S3（法难）交叉
  · 法诚「圖畫七處八會之像」 —— 与 R2（图像化）交叉

Usage:
  python scripts/build_r5_lingyan.py
"""
import json
import re
from datetime import date
from pathlib import Path

from build_translation_workshop import Doc, sha256

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "research" / "r5_lingyan.json"

SRC = {
    "zhuanji": ("data/references/cbeta/T51n2073.xml",
                "《華嚴經傳記》，唐法藏集，CBETA T51n2073"),
}

Q = {
    # 諷誦第七
    "q_pj_yi": ("zhuanji", "濟曰。經言世醫所療治", "畢竟不復發。",
                "諷誦·普濟：诵经疗病，引经句自证"),
    "q_bc_xiangdai": ("zhuanji", "乃別護淨。造香函盛經頂戴", "始終如鏡。",
                      "諷誦·辨才：顶戴华严三载，梦普贤指授而忽然成诵"),
    "q_hw_shen": ("zhuanji", "僧曰。貧道夏臘既卑", "理宜尊勝。",
                  "諷誦·慧悟：山神供斋，「受持華嚴」者位尊胜"),
    "q_hw_li": ("zhuanji", "余華嚴經力", "蒙致仙藥。",
                "諷誦·慧悟：自证「華嚴經力」致仙药而凌空远逝"),
    # 轉讀第八
    "q_pa_nan": ("zhuanji", "安曰。今蒙脫難。乃惟受持華嚴力耳", "凡所祈誠",
                 "轉讀·普安：北周滅法避难山中，自证脱难为「受持華嚴力」——与 S3 交叉"),
    # 書寫第九
    "q_dy_guang": ("zhuanji", "纔寫數行。每字皆放光明", "久之方歇。",
                   "書寫·德圓：香汁造纸净写，每字放光照一院"),
    "q_fc_tu": ("zhuanji", "乃潔淨圖畫七處八會之像", "弘文館學士張靜。",
                "書寫·法誠：造华严堂图画七处八会像，请弘文馆学士张静写经——与 R2 交叉"),
    # 講解第六（讲主式接受）
    "q_bt_tou": ("zhuanji", "譙王欲請講華嚴經", "遂講華嚴。數十餘遍。",
                 "講解·求那跋陀羅：未善宋言，礼祈感梦换头，遂能讲华严数十遍"),
    "q_sf_yan": ("zhuanji", "請範冬講。至華嚴六地", "飛來入聽訖講便去。",
                 "講解·僧範：讲至华严六地，雁入堂伏听，讲散方去；雀、鸭继之"),
    "q_ji_zhen": ("zhuanji", "時有雄鷄一頭", "感通之明應也。",
                  "講解·靈裕：齐后染患愿闻华严，雄鸡随众听讲，讲散疾瘳"),
    "q_hg_pan": ("zhuanji", "立頓漸圓三教", "以華嚴為圓教。",
                 "講解·慧光：立顿渐圆三教判群典，以华严为圆教——判教史源头（与 L4 交叉）"),
    "q_hf_bian": ("zhuanji", "正講華嚴。輒有一僧加毀", "特致鞭楚",
                  "講解·僧範：讲华严而遭毁谤者夜受神鞭——毁经有征的叙事形态"),
}


def main() -> int:
    docs, sources = {}, {}
    for key, (rel, edition) in SRC.items():
        p = ROOT / rel
        docs[key] = Doc(key, p)
        sources[key] = {"path": rel, "edition": edition,
                        "bytes": p.stat().st_size,
                        "sha256": sha256(p.read_bytes())}

    quotes = {}
    for qid, (sk, a, b, note) in Q.items():
        q = docs[sk].slice_quote(a, b)
        quotes[qid] = {"source": sk, "lb": q["lb"], "text": q["text"].strip(),
                       "section": note.split("：")[0], "note": note}

    groups = [
        {"kind": "諷誦", "quotes": ["q_pj_yi", "q_bc_xiangdai", "q_hw_shen", "q_hw_li"],
         "what": "以诵经为中心的神异：疗病、感圣助成诵、受持者受尊胜、经力致仙"},
        {"kind": "轉讀", "quotes": ["q_pa_nan"],
         "what": "以转读为中心的神异：灭法中脱难自证经力（与 S3 交叉）"},
        {"kind": "書寫", "quotes": ["q_dy_guang", "q_fc_tu"],
         "what": "以写经为中心的神异：字字放光、净土造纸；并见经变图像（与 R2 交叉）"},
        {"kind": "講解", "quotes": ["q_bt_tou", "q_sf_yan", "q_ji_zhen", "q_hg_pan", "q_hf_bian"],
         "what": "讲主式接受：感梦换头成讲主、禽鸟伏听、讲经疾瘳、判教源头（慧光立圆教，与 L4 交叉）、毁经神谴"},
    ]

    data = {
        "meta": {
            "operator": "R5",
            "title": "灵验叙事：本经自己的接受史（華嚴經傳記）",
            "date": date.today().isoformat(),
            "method": ("逐条以起止锚在源文切片（不手抄），记叶码 lb；源文件记 sha256；"
                       "十二条引文覆盖諷誦/轉讀/書寫/講解四篇；与 S3/R2/L4 的交叉只记不判。"),
            "sources": sources,
            "structure": "十篇目：部類、隱顯、傳譯、支流、論釋、講解、諷誦、轉讀、書寫、雜述",
        },
        "quotes": quotes,
        "groups": groups,
        "boundaries": [
            "《華嚴經傳記》是法藏（本经译主一系）为本经集的传记——采选本身有宗派立场，"
            "灵验故事的取舍是「本经门下的接受史」，不是随机样本。",
            "故事形态是六朝隋唐僧传灵验体的常规母题（顶戴感圣、山神供斋、寫经放光）；"
            "本文只登记「有这类记载」，不判其史实性——判灵验真伪超出文献学范围。",
            "普安条是北周滅法（非會昌）语境，与 §17.21 的會昌法难不同代，只记交叉。",
            "法诚条「圖畫七處八會之像」是 R2（图像化）的一手例证：经变图像不晚于唐初——"
            "但只此一见在库，不能据此立「经变流行」的定量结论。",
            "转引链：本传多引《續高僧傳》与唐初诸记（文中「通師云云」一类），"
            "故事多为二手；引文照录，不改其性质。",
        ],
        "summary": {"quotes": len(quotes), "groups": len(groups)},
    }
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n",
                   encoding="utf-8")
    print(f"quotes {len(quotes)} groups {len(groups)}")
    for qid, q in quotes.items():
        print(f"  {qid} {q['lb']} [{q['section']}] {q['text'][:36]}…")
    print("written", OUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
