# -*- coding: utf-8 -*-
"""《九九華嚴》單集 **K3d-v1 機械校訂稿** 生成器（程序化·可复跑）

定位：在 K2 证据层之上，完成**文本校訂**可機械化的部分：
  · 講章分段（15 分钟目标 + 最近停顿/转折词；首句提取式标题，非科判）
  · 言說段（按停顿/字数/长度切段），段末〔校〕只标**可观察事实**：
      CBETA 對勘 / slide 剝離 / OCR 重複 / OCR noise / 問答 / 品名 garble
  · slide 短標題剝離（另行列出，不删原文；長 slide 經文不強剝，標候選）
  · 連續重複 cue 折叠（保留首條時間，計數）
  · 品名/術語變體表（OCR 異形 vs CBETA 用字；不擅改正文）
  · CBETA anchor 切片（品×卷钳制·逐命中加粗）
  · 信息無損對賬（speech + slide + dup + noise = total 漢字）

**不做**（不得代寫）：
  · 義理按語 / 判攝 / 讲章科判定名
  · 術語義理定形（只給候選與底本有無）
  · 三源互證（讲义/录音不在仓内）
  · podcast 內容逐句比對

用法：
  python scripts/build_jj_k3d_doc.py --ep 16 --pins 7,8,9
  python scripts/build_jj_k3d_doc.py --ep 17 --pins 7,8,9,10
  python scripts/build_jj_k3d_doc.py --ep 18 --pins 11
"""
import argparse
import importlib.util
import io
import json
import os
import re
import sys

import yaml

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

CUE = re.compile(r"^`\[(\d\d):(\d\d):(\d\d)[\u2013\u2014-]"
                 r"(\d\d):(\d\d):(\d\d)\]`\s*(.+)$")
HAN = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")
LATIN = re.compile(r"[A-Za-z]")
TRANS = re.compile(r"^(好|那|那麼|接下來|下面|現在|我們|這個|第一個|第二個|"
                   r"第三個|最後|所以|也就是說|換句話說|講到這裡|回到|總結|"
                   r"另外|還有|比如說|譬如|首先|其次|再者|第四個|第五個)")

PIN_NAMES = {
    1: "世主妙嚴品", 2: "如來現相品", 3: "普賢三昧品", 4: "世界成就品",
    5: "華藏世界品", 6: "毘盧遮那品", 7: "如來名號品", 8: "四聖諦品",
    9: "光明覺品", 10: "菩薩問明品", 11: "淨行品", 12: "賢首品",
    13: "昇須彌山頂品", 14: "須彌頂上偈讚品", 15: "十住品", 16: "梵行品",
    17: "初發心功德品", 18: "明法品",
}
PIN_JUAN = {1: 1, 2: 6, 3: 7, 4: 7, 5: 8, 6: 11, 7: 12, 8: 12, 9: 13,
            10: 13, 11: 14, 12: 14, 13: 16, 14: 16, 15: 16, 16: 17,
            17: 17, 18: 18}
PIN_DOC = {
    7: "docs/经学文献/华严经细读/第二会_普光明殿_差别因果周/华严经细读_第七部_如来名号品.md",
    8: "docs/经学文献/华严经细读/第二会_普光明殿_差别因果周/华严经细读_第八部_四圣谛品.md",
    9: "docs/经学文献/华严经细读/第二会_普光明殿_差别因果周/华严经细读_第九部_光明觉品.md",
    10: "docs/经学文献/华严经细读/第二会_普光明殿_差别因果周/华严经细读_第十部_菩萨问明品.md",
    11: "docs/经学文献/华严经细读/第二会_普光明殿_差别因果周/华严经细读_第十一部_净行品.md",
    12: "docs/经学文献/华严经细读/第二会_普光明殿_差别因果周/华严经细读_第十二部_贤首品.md",
    3: "docs/经学文献/华严经细读/第一会_菩提场_所信因果周/华严经细读_第三部_普贤三昧品.md",
    4: "docs/经学文献/华严经细读/第一会_菩提场_所信因果周/华严经细读_第四部_世界成就品.md",
    5: "docs/经学文献/华严经细读/第一会_菩提场_所信因果周/华严经细读_第五部_华藏世界品.md",
    6: "docs/经学文献/华严经细读/第一会_菩提场_所信因果周/华严经细读_第六部_毗卢遮那品.md",
}

TERMS = [
    "法身", "法界", "如來", "菩薩", "眾生", "修行", "三昧", "菩提",
    "名號", "四聖諦", "光明", "世界", "微塵", "壽命", "十方", "三世",
    "道場", "樓閣", "莊嚴", "國土", "自在", "清淨", "無明", "煩惱",
    "解脫", "涅槃", "佛剎", "方便", "神通", "放光", "法門", "行願",
    "願海", "業力", "因果", "信解", "證得", "佛身", "法性", "真如",
    "實相", "空相", "心性", "本性", "覺性", "覺力", "智慧", "慈悲",
    "功德", "福報", "因緣", "境界", "世間", "生死", "輪迴", "成佛",
    "普賢", "文殊", "毘盧遮那", "華藏", "娑婆", "極樂", "淨土",
    "禪定", "般若", "波羅蜜", "阿僧祇", "微塵數", "本元界", "本體界",
    "轉靜", "靜慮", "含金量", "人格性", "社會年齡", "普賢乘",
    "華嚴禪觀", "法界三觀", "如來藏", "法身佛", "報身佛", "化身佛",
    "三身", "五蘊",
]

GA_GROUPS = {
    "毘盧遮那": ["毘盧遮那", "毗盧遮那", "毘廬遮那", "昆盧遮那", "昆廬遮那",
                "昆廣遮邦", "毘廬遮邦", "昆盧遮邦", "毗廬遮那", "民燃",
                "尼脑", "比照温力", "星险", "毘遮", "昆赢", "毘盧遮", "昆盧遮"],
    "華藏": ["華藏", "华藏", "華廠", "华厂"],
    "淨行": ["淨行", "净行"],
    "賢首": ["賢首", "贤首"],
    "如來名號": ["如來名號", "如来名号"],
    "四聖諦": ["四聖諦", "四圣谛"],
    "光明覺": ["光明覺", "光明觉"],
    "菩薩問明": ["菩薩問明", "菩萨问明"],
    "普賢": ["普賢", "普贤"],
    "文殊師利": ["文殊師利", "文殊师利"],
    "智首": ["智首"],
}

VAR_PAIRS = [
    ("毘盧遮那", ["毘盧遮那", "毗盧遮那"]),
    ("恆河", ["恆河", "恒河"]),
    ("華蕊燄輪", ["華蕊燄輪", "華蕊焰輪"]),
    ("遶佛", ["遶佛", "繞佛"]),
    ("須彌", ["須彌", "须弥"]),
    ("眾生", ["眾生", "众生"]),
    ("菩薩", ["菩薩", "菩萨"]),
    ("如來", ["如來", "如来"]),
    ("國土", ["國土", "国土"]),
    ("莊嚴", ["莊嚴", "庄严"]),
    ("清淨", ["清淨", "清净"]),
    ("無明", ["無明", "无明"]),
    ("煩惱", ["煩惱", "烦恼"]),
    ("解脫", ["解脫", "解脱"]),
    ("因緣", ["因緣", "因缘"]),
    ("世間", ["世間", "世间"]),
    ("輪迴", ["輪迴", "轮回"]),
    ("壽命", ["壽命", "寿命"]),
    ("微塵", ["微塵", "微尘"]),
    ("道場", ["道場", "道场"]),
    ("樓閣", ["樓閣", "楼阁"]),
    ("淨行", ["淨行", "净行"]),
    ("賢首", ["賢首", "贤首"]),
    ("般若", ["般若", "波若"]),
    ("波羅蜜", ["波羅蜜", "波罗蜜"]),
    ("涅槃", ["涅槃", "涅盤"]),
    ("阿僧祇", ["阿僧祇", "阿僧祗"]),
]

GLYPH_PAIRS = [("焰", "燄"), ("恆", "恒"), ("遶", "繞"),
               ("祇", "祗"), ("槃", "盤"), ("毗", "毘")]

QA_MARKERS = ["有沒有問題", "有問題嗎", "有問題的", "提問", "提問單", "現場提問",
              "發問", "問答", "問答時間", "舉手", "麥克風", "我們先休息",
              "休息一下", "下半場", "後半段", "後面的時間", "今天到這裡",
              "我們先講到這裡", "下一節"]


def sec(h, m, s):
    return int(h) * 3600 + int(m) * 60 + int(s)


def ts(x):
    if x is None:
        return "—"
    x = int(x)
    return "%02d:%02d:%02d" % (x // 3600, (x % 3600) // 60, x % 60)


def hm(x):
    x = int(x)
    return "%02d:%02d" % (x // 60, x % 60)


def norm(s):
    s = re.sub(r"[\s，。、！？；：,.!?;:~\-—「」『』\"'()（）【】|]", "", s)
    return s


def load_cb():
    spec = importlib.util.spec_from_file_location(
        "jj_cbeta_match", "scripts/jj_cbeta_match.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m.load_cbeta()


def parse_cues(path):
    out = []
    for ln in io.open(path, encoding="utf-8"):
        m = CUE.match(ln.rstrip("\n"))
        if not m:
            continue
        s = sec(m.group(1), m.group(2), m.group(3))
        e = sec(m.group(4), m.group(5), m.group(6))
        t = m.group(7).strip()
        out.append({"s": s, "e": e, "text": t, "han": len(HAN.findall(t)),
                    "pipe": "|" in t, "latin": bool(LATIN.search(t)),
                    "noise": False, "dup": False, "slide_only": False,
                    "speech": t, "slide": [], "slide_long": False,
                    "dup_n": 0, "orig_i": len(out)})
    return out


def is_slide_title(s):
    if not s:
        return False
    if len(s) <= 6 and not HAN.search(s):
        return True
    if len(s) > 14:
        return False
    if re.search(r"第.{1,4}品|卷.{1,3}|四十一位|三十九|十信|十住|十行|"
                 r"十迴向|十地|等覺|妙覺|華嚴經|九九華嚴", s):
        return True
    return any(n.replace("品", "") in s for n in PIN_NAMES.values())


def classify(cues, cb):
    prev = ""
    for c in cues:
        if c["s"] < 40 and c["han"] < 20:
            c["noise"] = True
            c["head"] = True
            continue
        if c["han"] <= 1 and not c["pipe"]:
            c["noise"] = True
            continue
        if c["pipe"]:
            segs = [x.strip() for x in c["text"].split("|") if x.strip()]
            sp, sl, long_slide = [], [], False
            for x in segs:
                if is_slide_title(x):
                    sl.append(x)
                else:
                    sp.append(x)
                    if len(x) > 14 and cb and x in cb:
                        long_slide = True
            c["slide"] = sl
            c["speech"] = " ".join(sp)
            c["slide_long"] = long_slide
            if not sp and sl:
                c["slide_only"] = True
        n = norm(c["speech"])
        if n and n == prev:
            c["dup"] = True
        if n:
            prev = n


def segment_sections(cues, target=1200, window=300):
    last = cues[-1]["e"]
    bounds, prev = [], 0
    for t in range(target, last, target):
        lo, hi = t - window, t + window
        cand = [i for i in range(prev + 1, len(cues))
                if lo <= cues[i]["s"] <= hi]
        if not cand:
            continue

        def score(i):
            gap = max(0, cues[i]["s"] - cues[i - 1]["e"])
            tr = 40 if TRANS.match(cues[i]["speech"] or cues[i]["text"]) else 0
            return gap * 12 + tr

        best = max(cand, key=score)
        if best > prev:
            bounds.append(best)
            prev = best
    starts = [0] + bounds
    ends = bounds + [len(cues)]
    return [(starts[i], ends[i]) for i in range(len(starts))]


def build_paragraphs(cues, a0, b0, qa_idx):
    paras, cur, cur_han = [], [], 0
    for i in range(a0, b0):
        cues[i]["dup_n"] = 0

    def flush():
        nonlocal cur, cur_han
        if not cur:
            return
        si, ei = cur[0], cur[-1]
        text = " ".join(cues[i]["speech"] for i in cur if cues[i]["speech"])
        paras.append({"a": si, "b": ei, "text": text,
                      "han": sum(cues[i]["han"] for i in cur),
                      "sh": sum(cues[i]["han"] for i in cur if cues[i]["speech"]),
                      "slide": [x for i in cur for x in cues[i]["slide"]],
                      "dup": sum(cues[i]["dup_n"] for i in cur),
                      "long": any(cues[i]["slide_long"] for i in cur),
                      "qa": qa_idx is not None and si >= qa_idx})
        cur, cur_han = [], 0

    for i in range(a0, b0):
        c = cues[i]
        if c["noise"] or c["slide_only"]:
            continue
        if c["dup"]:
            c["dup_n"] = 1
            if cur:
                cues[cur[-1]]["dup_n"] += 1
            continue
        if cur and (c["s"] - cues[cur[-1]]["e"] >= 6 or cur_han + c["han"] > 400
                    or len(cur) >= 20):
            flush()
        cur.append(i)
        cur_han += c["han"]
    flush()
    # 碎段并入后段
    merged = []
    for p in paras:
        if merged and p["sh"] < 20:
            merged[-1]["text"] += " " + p["text"]
            merged[-1]["b"] = p["b"]
            merged[-1]["han"] += p["han"]
            merged[-1]["sh"] += p["sh"]
            merged[-1]["slide"] += p["slide"]
            merged[-1]["dup"] += p["dup"]
            merged[-1]["long"] = merged[-1]["long"] or p["long"]
        else:
            merged.append(p)
    return merged


def detect_qa(cues, declared):
    floor = int((declared or cues[-1]["s"]) * 0.55)
    for i, c in enumerate(cues):
        if c["s"] < floor:
            continue
        for m in QA_MARKERS:
            if m in c["text"]:
                return i, m
    return None, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ep", type=int, required=True)
    ap.add_argument("--pins", default="")
    ap.add_argument("--out", default="")
    ap.add_argument("--cbeta-json", default="")
    a = ap.parse_args()
    ep = a.ep
    md_in = "docs/hy_refs/sub_extract/delivery/ep%02d.md" % ep
    if not os.path.exists(md_in):
        print("【缺 OCR 稿】%s" % md_in)
        return 1
    out = a.out or ("docs/经学文献/海云讲记_九九华严/episodes/ep%02d.md" % ep)
    cues = parse_cues(md_in)

    M = yaml.safe_load(io.open("data/research/jj_huayan_lectures.yaml",
                               encoding="utf-8").read())
    det = next((x for x in (M.get("episodes_detail") or []) if x["ep"] == ep), {})
    C = yaml.safe_load(io.open("data/research/jj_huayan_collation.yaml",
                               encoding="utf-8").read())
    cm = next((x for x in (C.get("episodes") or []) if x["ep"] == ep), {})
    vid = det.get("video_id") or ""
    info = {}
    ip = "docs/hy_refs/sub_extract/%s.info.json" % vid if vid else ""
    if ip and os.path.exists(ip):
        info = json.load(io.open(ip, encoding="utf-8"))
    title = info.get("title") or det.get("title") or ("第 %d 集" % ep)
    month = re.search(r"#(\d+)月", title)
    month_s = ("2026 年 %s 月" % month.group(1)) if month else "2026 年〔待核〕"
    cj = a.cbeta_json or (".tmp_ep%02d_cbeta.json" % ep)
    cbeta = json.load(io.open(cj, encoding="utf-8")) if os.path.exists(cj) else {}
    hits = cbeta.get("hits") or []
    spans = cbeta.get("pin_spans") or []
    cb, _j, _p, _sp = load_cb()

    pins = [int(x) for x in a.pins.split(",") if x.strip()] if a.pins else []
    qa_idx, qa_mark = detect_qa(cues, det.get("declared_sec") or 0)

    classify(cues, cb)
    total_han = sum(c["han"] for c in cues)
    noise = [c for c in cues if c["noise"]]
    dups = [c for c in cues if c["dup"]]
    slide_only = [c for c in cues if c["slide_only"]]
    noise_han = sum(c["han"] for c in noise)
    dup_han = sum(c["han"] for c in dups)
    slide_han = sum(len(HAN.findall(x)) for c in cues if not c["dup"] for x in c["slide"])
    speech_cues = [c for c in cues if not c["noise"] and not c["dup"]
                   and not c["slide_only"]]
    speech_han = sum(len(HAN.findall(c["speech"])) for c in speech_cues)
    accounted = speech_han + slide_han + dup_han + noise_han
    diff = total_han - accounted

    secs = segment_sections(cues)
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    pin_hits = {}
    for h in hits:
        pin_hits.setdefault(h.get("pin_no"), []).append(h)
    hit_by_cue = {}
    for h in hits:
        hit_by_cue.setdefault(h["cue"], []).append(h)

    total_paras = 0
    for (a0, b0) in secs:
        total_paras += len(build_paragraphs(cues, a0, b0, qa_idx))

    pod = cm.get("podcast") or {}
    L = []
    L.append("# Ep %d · 《華嚴教海·%s（正行＋會後問答·台北國際會議中心）》 · 校订稿（K3d-v1 机械校·待听核）\n"
             % (ep, cm.get("topic_zh") or ("·".join(PIN_NAMES[p] for p in pins) or "品目待核")))
    L.append("> **狀態**：待校 · K3d-v1 机械校（講章分段／段末〔校〕／slide 剝離／重複折叠／術語變體／CBETA 切片）；"
             "**未作義理按語·未三源互證**，不得稱定稿。\n")
    L.append("> **依賴實測**：`jj_huayan_lectures.yaml` ep %d（%s cues · %s 漢字 · 覆蓋 %.2f%% · %s sec ≈ %d 小時 %d 分）\n"
             % (ep, det.get("cues", len(cues)), "{:,}".format(det.get("han_chars", total_han)),
                100 * (det.get("coverage") or 0), det.get("declared_sec", 0),
                (det.get("declared_sec", 0)) // 3600, (det.get("declared_sec", 0) % 3600) // 60))
    L.append("> **視頻**：[%s](https://www.youtube.com/watch?v=%s) · %s\n"
             % (vid or "〔待核〕", vid, month_s))
    if pod.get("url"):
        L.append("> **播客**：[%s](%s)" % (pod.get("label", "正行"), pod["url"]))
        if pod.get("url_qa"):
            L.append(" · [會後問答](%s)" % pod["url_qa"])
        L.append(" · 置信 `%s`\n" % pod.get("confidence", ""))
    L.append("> **底本**：`%s` · CBETA `T10n0279`（§四 程序切片·非手抄）\n" % md_in)
    L.append("\n---\n")

    L.append("## 〇 · 凡例（K3d-v1 机械校·未精校）\n\n")
    L.append("1. **本稿完成**：OCR 全文可讀化 → 講章分段 → 言說段 → 段末〔校〕（CBETA／slide／重複／noise／問答／garble）→ 術語變體 → CBETA anchor 切片 → 信息無損對賬。\n")
    L.append("2. **講章＝程序候選**：%d 分鐘目標＋最近停頓/轉折詞；標題為時間＋程序主題詞（提取式），首句另列於節首，**非科判**；邊界〔待校〕。\n" % 20)
    L.append("3. **段末〔校〕只標可觀察事實**，不作義理判斷；**義理按語 / 判攝 / 科判定名未作**（不得代寫）。\n")
    L.append("4. **正文照 OCR 原字**；slide 短標題剝離後另行列出，長 slide 經文不強剝（標候選）；異體各照底本，不統一。\n")
    L.append("5. **重複折叠**：連續同文 cue 保留首條時間、計數；noise（≤1 漢字且非 slide）剔除並計數。\n")
    L.append("6. **三源互證未作**：讲义/錄音不在仓内；播客僅月份+時長映射，內容未逐句比對。\n")
    L.append("\n---\n")

    L.append("## 一 · 本集概要（程序實測）\n\n")
    L.append("- **總量**：%d cues · %s 漢字 · noise %d／%d 漢字 · 重複 %d／%d 漢字 · slide 短標題 %d 段／%d 漢字 · 正文 cues %d／%d 漢字。\n"
             % (len(cues), "{:,}".format(total_han), len(noise), noise_han,
                len(dups), dup_han, sum(len(c["slide"]) for c in cues), slide_han,
                len(speech_cues), speech_han))
    L.append("- **信息無損對賬**：正文 %d + slide %d + 重複 %d + noise %d = %d；總漢字 %d；差 %+d %s\n"
             % (speech_han, slide_han, dup_han, noise_han, accounted, total_han, diff,
                "✓" if abs(diff) <= 2 else "〔待核〕"))
    L.append("- **品目時間軸**（字面首現＋CBETA 首命中；程序證據）：\n\n")
    L.append("| 品 | 卷 | 字面首現 | CBETA 首命中 | 去重語串 |\n|---|---|---|---|---|\n")
    for no in pins:
        hs = pin_hits.get(no, [])
        first = next((c["s"] for c in cues
                      if PIN_NAMES[no].replace("品", "") in c["text"]), None)
        L.append("| §%d %s | %d | %s | %s | %d |\n"
                 % (no, PIN_NAMES[no], PIN_JUAN.get(no, 0), ts(first),
                    min((h["t"] for h in hs), default="—"), len(hs)))
    L.append("\n- **問答邊界候選**：%s\n"
             % (("`%s` 觸發「%s」〔待听核〕" % (ts(cues[qa_idx]["s"]), qa_mark))
                if qa_idx is not None else "未檢出明確標記〔待核〕"))
    L.append("- **結構**：%d 講章 · %d 言說段。\n" % (len(secs), total_paras))
    L.append("\n---\n")

    L.append("## 二 · %d 講章 · %d 言說段 校訂\n\n" % (len(secs), total_paras))
    L.append("> 講章標題為時間＋程序主題詞（提取式）；段末〔校〕只標可觀察事實。\n\n")
    pidx = 0
    for si, (a0, b0) in enumerate(secs):
        paras = build_paragraphs(cues, a0, b0, qa_idx)
        first = next((c["speech"] or c["text"] for c in cues[a0:b0]
                      if not c["noise"] and not c["slide_only"]
                      and len(HAN.findall(c["speech"] or c["text"])) >= 8), "")
        first = re.sub(r"\s+", "", first)[:40]
        tcount = [(t, sum(1 for c in cues[a0:b0] if t in c["text"])) for t in TERMS]
        top = [t for t, n in sorted(tcount, key=lambda x: -x[1]) if n > 0][:3]
        L.append("### §%s · %s–%s · 程序主題：%s（%dP）\n\n"
                 % (letters[si], hm(cues[a0]["s"]), hm(cues[b0 - 1]["e"]),
                    "／".join(top) or "—", len(paras)))
        sh = sum(p["sh"] for p in paras)
        L.append("> 首句（照錄）：“%s”；本節正文 %d 漢字 · slide %d 段 · CBETA 命中 %d 段。\n\n"
                 % (first or "—", sh,
                    sum(len(p["slide"]) for p in paras),
                    sum(1 for c in cues[a0:b0] if c["orig_i"] in hit_by_cue)))
        for p in paras:
            pidx += 1
            ann = []
            hs = [h for c in cues[p["a"]:p["b"] + 1] for h in hit_by_cue.get(c["orig_i"], [])]
            if hs:
                seen = []
                for h in hs:
                    k = (h.get("pin_no"), h.get("juan"))
                    if k not in seen:
                        seen.append(k)
                ann.append("〔CBETA 對勘·%s〕" % "、".join(
                    "§%s %s·卷%s" % (x[0], PIN_NAMES.get(x[0], ""), x[1]) for x in seen))
            if p["slide"]:
                ann.append("〔slide 剝離 %d 段〕" % len(p["slide"]))
            if p["dup"]:
                ann.append("〔OCR 重複 %d〕" % p["dup"])
            if p["long"]:
                ann.append("〔OCR 待校·slide 長句未剝離〕")
            if any(cues[i]["latin"] for i in range(p["a"], p["b"] + 1)):
                ann.append("〔OCR 待校·拉丁/英文串〕")
            if p["qa"]:
                ann.append("〔問答〕")
            # 品名 garble
            gfound = []
            for canon, vs in GA_GROUPS.items():
                for v in vs:
                    if v == canon or v in cb:
                        continue
                    n = p["text"].count(v)
                    if n:
                        gfound.append("%s×%d" % (v, n))
            if gfound:
                ann.append("〔OCR 待校·品名 garble：%s〕" % "、".join(gfound))
            L.append("**%s%02d** `[%s–%s]`（%d 漢字%s）\n\n"
                     % (letters[si], pidx, ts(cues[p["a"]]["s"]),
                        ts(cues[p["b"]]["e"]), p["sh"],
                        " · " + str(len(p["slide"])) + " slide" if p["slide"] else ""))
            L.append(p["text"] + "\n\n")
            if p["slide"]:
                L.append("> 〔slide 原字〕%s\n\n" % " ｜ ".join(p["slide"]))
            if ann:
                L.append("".join(ann) + "\n\n")
        L.append("---\n")

    L.append("## 三 · 術語／品名變體（K3d-v1 · 待定形）\n\n")
    L.append("### 3.1 品名／garble 群\n\n")
    L.append("| 正形（CBETA） | 異形（OCR） | 次數 | 首現 | 底本有無 | 處理 |\n|---|---|---|---|---|---|\n")
    ga_n = 0
    for canon, vs in GA_GROUPS.items():
        for v in vs:
            if v == canon:
                continue
            if v in canon or canon in v:
                continue
            n = sum(c["text"].count(v) for c in cues)
            if n == 0:
                continue
            ga_n += 1
            ft = next((c["s"] for c in cues if v in c["text"]), None)
            present = v in cb
            L.append("| %s | %s | %d | %s | %s | %s |\n"
                     % (canon, v, n, ts(ft), "見" if present else "未見",
                        "合法異形·照底本" if present else "**garble 候選**·不擅改"))
    if not ga_n:
        L.append("| — | 未檢出 | 0 | — | — | 本集無 garble 候選 |\n")
    L.append("\n### 3.2 術語變體\n\n")
    L.append("| 正形 | 異形 | 正形次數 | 異形次數 | 底本 | 處理 |\n|---|---|---|---|---|---|\n")
    var_n = 0
    for canon, vs in VAR_PAIRS:
        for v in vs[1:]:
            n0 = sum(c["text"].count(canon) for c in cues)
            n1 = sum(c["text"].count(v) for c in cues)
            if n1 == 0:
                continue
            var_n += 1
            L.append("| %s | %s | %d | %d | 正%s／異%s | %s |\n"
                     % (canon, v, n0, n1, "見" if canon in cb else "未見",
                        "見" if v in cb else "未見",
                        "各照底本·不統一" if (canon in cb and v in cb) else "候選定形〔待定〕"))
    if not var_n:
        L.append("| — | 未檢出 | 0 | 0 | — | 本集無變體候選 |\n")
    L.append("\n### 3.2b 單字異形（字面·含複合詞）\n\n")
    L.append("| A | B | A次 | B次 | 底本 | 處理 |\n|---|---|---|---|---|---|\n")
    gl_n = 0
    for x, y in GLYPH_PAIRS:
        nx = sum(c["text"].count(x) for c in cues)
        ny = sum(c["text"].count(y) for c in cues)
        if nx + ny == 0:
            continue
        gl_n += 1
        L.append("| %s | %s | %d | %d | %s／%s | %s |\n"
                 % (x, y, nx, ny, "見" if x in cb else "未見",
                    "見" if y in cb else "未見",
                    "各照底本·不統一" if (x in cb and y in cb) else "候選〔待定〕"))
    if not gl_n:
        L.append("| — | — | 0 | 0 | — | 本集無單字異形 |\n")
    L.append("\n> 單字統計含複合詞，僅供候選；不作字義定形。\n")
    L.append("\n### 3.3 高頻術語（字面計數·含 slide）\n\n")
    L.append("| 術語 | 次數 | 首現 | 底本 | 判讀 |\n|---|---|---|---|---|\n")
    rows = []
    for t in TERMS:
        n = sum(c["text"].count(t) for c in cues)
        if n:
            rows.append((n, t, next((c["s"] for c in cues if t in c["text"]), None)))
    for n, t, ft in sorted(rows, reverse=True)[:25]:
        present = t in cb
        L.append("| %s | %d | %s | %s | %s |\n"
                 % (t, n, ts(ft), "見" if present else "未見",
                    "底本見" if present else "**底本未見**·不擅等同"))
    L.append("\n> 變體/garble 只作候選；正文照 OCR 原字，未改經。\n\n---\n")

    L.append("## 四 · CBETA 回源（程序切片·非手抄）\n\n")
    if not hits:
        L.append("本輪無 ≥12 字精確命中；不得據此稱「無經文引文」〔待听核〕。\n\n")
    else:
        L.append("### 4.1 Anchor 切片（品×卷鉗制·逐命中加粗）\n\n")
        sn = 0
        for no in pins:
            hs = pin_hits.get(no, [])
            if not hs:
                continue
            hs = sorted(hs, key=lambda x: x["pos"])
            groups, cur = [], [hs[0]]
            for h in hs[1:]:
                if h["pos"] - (cur[-1]["pos"] + cur[-1]["len"]) <= 150:
                    cur.append(h)
                else:
                    groups.append(cur)
                    cur = [h]
            groups.append(cur)
            for g in groups:
                sn += 1
                s0 = max(g[0]["span_start"], min(h["pos"] for h in g) - 40)
                e0 = min(g[0]["span_end"], max(h["pos"] + h["len"] for h in g) + 40)
                parts, cu = [], s0
                for h in g:
                    hp, hq = h["pos"], h["pos"] + h["len"]
                    parts.append(cb[cu:hp])
                    parts.append("**" + cb[hp:hq] + "**")
                    cu = hq
                parts.append(cb[cu:e0])
                L.append("#### 4.1.%d §%d %s（卷 %d）· @%d–%d · OCR %s–%s（%d 命中）\n\n"
                         % (sn, no, PIN_NAMES[no], PIN_JUAN.get(no, 0), s0, e0,
                            min(h["t"] for h in g), max(h["t"] for h in g), len(g)))
                L.append("> %s%s%s\n\n"
                         % ("…" if s0 > g[0]["span_start"] else "",
                            "".join(parts),
                            "…" if e0 < g[0]["span_end"] else ""))
        L.append("> 加粗＝逐字命中；前後為底本上下文，未證講者已誦。訪問 2026-11-21。\n\n")
        L.append("### 4.2 命中清單\n\n")
        for no in pins:
            hs = pin_hits.get(no, [])
            if not hs:
                continue
            L.append("#### §%d %s（卷 %d）· %d 條\n\n"
                     % (no, PIN_NAMES[no], PIN_JUAN.get(no, 0), len(hs)))
            for h in hs[:60]:
                L.append("- `[OCR %s]` @%d · **%s**\n" % (h["t"], h["pos"], h["text"]))
            L.append("\n")
    L.append("---\n")

    L.append("## 五 · 與《华严经细读》之會讀\n\n")
    for no in pins:
        doc = PIN_DOC.get(no)
        L.append("- §%d %s → `%s`%s\n"
                 % (no, PIN_NAMES[no], doc or "〔未竟〕",
                    "" if doc and os.path.exists(doc) else "〔未竟·待后续批〕"))
    L.append("\n---\n")

    L.append("## 六 · 存疑 · 待听核清單\n\n")
    L.append("- 講章边界／标题：程序候选，非科判〔待校〕。\n")
    L.append("- 品目归属／問答边界：程序候选〔待听核〕。\n")
    L.append("- noise %d 条、重複 %d 条、slide-only %d 条：已折叠/剔除，原文见 delivery。\n"
             % (len(noise), len(dups), len(slide_only)))
    L.append("- 長 slide 經文未強剝（%d 条候選）〔待听核〕。\n"
             % sum(1 for c in cues if c["slide_long"]))
    L.append("- 品名 garble／術語變體：見 §三；不擅改經。\n")
    L.append("- **義理按語、判攝、科判定名未作**；三源互證缺讲义/錄音。\n")
    L.append("\n---\n")

    L.append("## 七 · 三源互證狀態\n\n")
    L.append("| 源 | 狀態 | 證據／缺口 |\n|---|---|---|\n")
    L.append("| 影像硬字幕（OCR） | 已得 | 720p · %d cues · 覆蓋 %.2f%% |\n"
             % (len(cues), 100 * (det.get("coverage") or 0)))
    L.append("| CBETA `T10n0279` | 已程序对勘 | §四 精確命中 %d 段 |\n" % len(hits))
    L.append("| 寺方字幕原稿 | 未得 | 原稿遺失；僅影像層還原 |\n")
    L.append("| 讲义／錄音 | 未得 | 缺 → 語詞級校定/丟首字復核未完成 |\n")
    L.append("| 官方播客 | %s | %s；內容未逐句比對 |\n"
             % ("已映射" if pod.get("url") else "未映射",
                pod.get("label", "待核")))
    L.append("\n> 結論：**影像＋CBETA 兩源可核；三源互證尚缺讲义/錄音**。本稿可作索引/時間錨點/經文候選，不作逐字引證。\n\n")

    L.append("## 八 · 完成度／缺口（K3d-v1 自評）\n\n")
    L.append("| 項 | 狀態 | 說明 |\n|---|---|---|\n")
    L.append("| OCR 全文 | 已 | %d cues／%s 漢字 |\n" % (len(cues), "{:,}".format(total_han)))
    L.append("| 講章分段 | 程序候選 | %d 章；時間＋主題詞；非科判 |\n" % len(secs))
    L.append("| 言說段 | 已 | %d 段；段末〔校〕 |\n" % total_paras)
    L.append("| slide/重複/noise | 已計數 | slide %d／重複 %d／noise %d |\n"
             % (slide_han, dup_han, noise_han))
    L.append("| 信息無損 | %s | 正文+slide+重複+noise=%d vs 總 %d（差 %+d） |\n"
             % ("✓" if abs(diff) <= 2 else "〔待核〕", accounted, total_han, diff))
    L.append("| 術語變體 | 候選 | 未義理定形 |\n")
    L.append("| CBETA 切片 | 已 | %d 段命中 |\n" % len(hits))
    L.append("| 義理按語 | 未 | 不代寫 |\n")
    L.append("| 三源互證 | 未 | 缺讲义/錄音 |\n")
    L.append("| podcast 內容比對 | 未 | 僅月份+時長 |\n")

    txt = "".join(L)
    io.open(out, "w", encoding="utf-8", newline="\n").write(txt)
    print("已生成 %s · %d bytes · %d 講章 · %d 段 · 正文 %d 漢字 · slide %d 漢字 · 重複 %d · noise %d · diff %+d · CBETA %d"
          % (out, len(txt.encode("utf-8")), len(secs), total_paras, speech_han,
             slide_han, dup_han, noise_han, diff, len(hits)))
    return 0


if __name__ == "__main__":
    sys.exit(main())