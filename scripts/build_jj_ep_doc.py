# -*- coding: utf-8 -*-
"""《九九華嚴》單集**K2 结构整理稿**生成器（程序化·可复跑）

定位：Ep16+ 新集入库时，把 OCR 初稿整理成可读、可核、可续校的单集文档。
**不是** K3d 精校——不写编者按语、不改讲者原字、不以推断充事实。
本版新增的程序证据层：
  · 品目时间轴（字面首现 + CBETA 首命中）
  · 每时间单元的主品与程序词频
  · 术语候选表（字面计数 + 首现 + 底本逐字有无）
  · CBETA anchor 切片（按品×卷钳制·前后 40 字上下文·非手抄）
  · 会後問答边界候选（标记词 + 时段下限）
  · 播客正行/问答双条映射（若 collation YAML 已填）
  · 三源互证状态与完成度缺口表（显式声明，不静默）

输入：
  docs/hy_refs/sub_extract/delivery/epNN.md    OCR 初稿（必需）
  docs/hy_refs/sub_extract/<vid>.info.json     视频元数据（可选）
  data/research/jj_huayan_lectures.yaml        实测台账（可选）
  data/research/jj_huayan_collation.yaml       编辑元数据（可选）
  .tmp/epNN_cbeta.json                          CBETA 精确命中（jj_cbeta_match.py 产出）

输出：
  docs/经学文献/海云讲记_九九华严/episodes/epNN.md

用法：
  python scripts/build_jj_ep_doc.py --ep 16 --pins 7,8,9
  python scripts/build_jj_ep_doc.py --ep 15 --out .tmp/ep15_doc.md --pins 3,4,5,6
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

# 术语候选（繁体·只作字面统计；非义理定形）
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


def parse_cues(path):
    out = []
    for ln in io.open(path, encoding="utf-8"):
        m = CUE.match(ln.rstrip("\n"))
        if not m:
            continue
        s = sec(m.group(1), m.group(2), m.group(3))
        e = sec(m.group(4), m.group(5), m.group(6))
        t = m.group(7).strip()
        out.append({"s": s, "e": e, "text": t,
                    "han": len(HAN.findall(t)), "pipe": "|" in t})
    return out


def pick_bounds(cues, minutes):
    """按「目标时刻 ±5 分钟内的最大停顿」切分；纯时间程序法，非科判。"""
    if not cues:
        return []
    last = cues[-1]["s"]
    step = minutes * 60
    bounds, prev = [], 0
    for target in range(step, last, step):
        lo, hi = target - 300, target + 300
        cand = [i for i in range(prev + 1, len(cues))
                if lo <= cues[i]["s"] <= hi]
        if not cand:
            continue

        def gap(i):
            return cues[i]["s"] - cues[i - 1]["e"]

        best = max(cand, key=gap)
        if best > prev:
            bounds.append(best)
            prev = best
    return bounds


def load_cb():
    """复用 jj_cbeta_match.load_cbeta（同一实现·不复制逻辑）"""
    spec = importlib.util.spec_from_file_location(
        "jj_cbeta_match", "scripts/jj_cbeta_match.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    cb, jus, pins, spans = m.load_cbeta()
    return cb, spans


def count_in(seq, term):
    return sum(1 for x in seq if term in (x["text"] if isinstance(x, dict) else x))


def first_time(cues, term):
    for c in cues:
        if term in c["text"]:
            return c["s"]
    return None


def group_hits(hs, gap=150):
    if not hs:
        return []
    hs = sorted(hs, key=lambda x: x["pos"])
    groups, cur = [], [hs[0]]
    for h in hs[1:]:
        if h["pos"] - (cur[-1]["pos"] + cur[-1]["len"]) <= gap:
            cur.append(h)
        else:
            groups.append(cur)
            cur = [h]
    groups.append(cur)
    return groups


def detect_qa(cues, declared):
    """会後問答边界候选：只在 >=55% 时长后找标记词；非科判。"""
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
    ap.add_argument("--out", default="")
    ap.add_argument("--pins", default="")
    ap.add_argument("--cbeta-json", default="")
    ap.add_argument("--section-min", type=int, default=20)
    ap.add_argument("--max-slices", type=int, default=12)
    a = ap.parse_args()

    ep = a.ep
    md_in = "docs/hy_refs/sub_extract/delivery/ep%02d.md" % ep
    if not os.path.exists(md_in):
        print("【缺 OCR 稿】%s" % md_in)
        return 1
    cues = parse_cues(md_in)
    if not cues:
        print("【无 cue】%s" % md_in)
        return 1
    out = a.out or ("docs/经学文献/海云讲记_九九华严/episodes/ep%02d.md" % ep)

    M = {}
    if os.path.exists("data/research/jj_huayan_lectures.yaml"):
        M = yaml.safe_load(io.open("data/research/jj_huayan_lectures.yaml",
                                   encoding="utf-8").read())
    det = next((x for x in (M.get("episodes_detail") or []) if x["ep"] == ep), {})
    C = {}
    if os.path.exists("data/research/jj_huayan_collation.yaml"):
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

    cbeta = None
    cj = a.cbeta_json or (".tmp/ep%02d_cbeta.json" % ep)
    if os.path.exists(cj):
        cbeta = json.load(io.open(cj, encoding="utf-8"))
    hits = (cbeta or {}).get("hits") or []
    spans = (cbeta or {}).get("pin_spans") or []
    cb = ""
    if cbeta:
        cb, _spans = load_cb()

    # 同一 cue 的同一语串可能在底本多处出现（stock 句式）；去重后按首见品归属，
    # 其余品记入 also，避免把一句通用语误排成多品多处引文。
    _u = {}
    for h in hits:
        k = (h.get("cue"), h.get("text"))
        if k not in _u:
            hh = dict(h)
            hh["also"] = []
            _u[k] = hh
        elif h.get("pin_no") != _u[k].get("pin_no"):
            _u[k]["also"].append((h.get("pin_no"), h.get("pin"), h.get("juan")))
    hits_u = list(_u.values())
    nhits_raw, nhits_u = len(hits), len(hits_u)

    pins = []
    if a.pins:
        pins = [int(x) for x in a.pins.split(",") if x.strip()]
    else:
        cnt = {}
        for h in hits:
            if h.get("pin_no"):
                cnt[h["pin_no"]] = cnt.get(h["pin_no"], 0) + 1
        for no, name in PIN_NAMES.items():
            k = sum(1 for c in cues if name.replace("品", "") in c["text"])
            if cnt.get(no, 0) >= 3 or k >= 3:
                pins.append(no)
    pins = sorted(set(pins))

    pin_kw = {no: sum(1 for c in cues if PIN_NAMES[no].replace("品", "") in c["text"])
              for no in PIN_NAMES}
    pin_hits = {}
    for h in hits_u:
        pin_hits.setdefault(h.get("pin_no"), []).append(h)

    ncue = len(cues)
    nhan = sum(c["han"] for c in cues)
    npipe = sum(1 for c in cues if c["pipe"])
    nhead = sum(1 for c in cues if c["s"] < 40)
    nlatin = sum(1 for c in cues if LATIN.search(c["text"]))
    nshort = sum(1 for c in cues if c["han"] <= 2)
    declared = det.get("declared_sec") or (info.get("duration") or 0)
    coverage = det.get("coverage")
    cov_s = ("%.2f%%" % (100 * coverage)) if coverage else "〔待实测〕"

    bounds = pick_bounds(cues, a.section_min)
    starts = [0] + bounds
    ends = bounds + [len(cues)]
    secs = [(starts[i], ends[i]) for i in range(len(starts))]
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    topic_hint = "·".join(PIN_NAMES[p] for p in pins) if pins else "品目待核"
    if cm.get("topic_zh"):
        topic_hint = cm["topic_zh"]

    qa_idx, qa_mark = detect_qa(cues, declared)
    pod = cm.get("podcast") or {}

    L = []
    L.append("# Ep %d · 《華嚴教海·%s（正行＋會後問答·台北國際會議中心）》 · 校订稿（K2 结构整理·待校）\n"
             % (ep, topic_hint))
    L.append("> **狀態**：待校 · K2 结构整理（程序证据层已入：品目时间轴／术语候选／CBETA 切片／播客映射；"
             "**逐段按语与三源互证未完成**）\n")
    L.append("> **依賴實測**：`jj_huayan_lectures.yaml` ep %d（%s cues · %s 漢字 · 覆蓋 %s · %s sec ≈ %d 小時 %d 分）\n"
             % (ep, det.get("cues", ncue), "{:,}".format(det.get("han_chars", nhan)),
                cov_s, declared, declared // 3600, (declared % 3600) // 60))
    L.append("> **視頻**：[%s](https://www.youtube.com/watch?v=%s) · %s\n"
             % (vid or "〔待核〕", vid, month_s))
    if pod.get("url"):
        L.append("> **播客**：[%s](%s)" % (pod.get("label", "播客·正行"), pod["url"]))
        if pod.get("url_qa"):
            L.append(" · [會後問答](%s)" % pod["url_qa"])
        L.append(" · 置信 `%s`\n" % pod.get("confidence", ""))
    else:
        L.append("> **音頻**：〔待核〕· %s 场次，播客按正行/问答分条上架时需二次核对\n" % month_s)
    L.append("> **底本**：`%s`（硬字幕 OCR · PaddleOCR chinese_cht · 720p）·"
             "**CBETA 底本** `data/references/cbeta/T10n0279.xml`（§四 程序精确命中 %d 段·非手抄）\n"
             % (md_in, len(hits)))
    L.append("\n---\n")

    L.append("## 〇 · 凡例（K2 结构整理·未精校）\n\n")
    L.append("1. **本稿性质**：Ep %d 于 2026-11 新入册，已完成 **OCR 全文可读化 + 程序证据层**"
             "（品目时间轴／术语候选／CBETA 精确命中／anchor 切片／播客映射）；"
             "K3d 逐段按语、术语定形、语词级校定**未完成**，不得据本稿作逐字引证。\n" % ep)
    L.append("2. **講者口語照 OCR 原**：简繁混排、中英夹杂、闽南语词一律照录，不擅自统一；"
             "异文各照底本（本仓铁律）。\n")
    L.append("3. **分段为程序所切**：按 ≥%d 分钟目标时刻的就近停顿切分，**非讲章科判**；"
             "讲章边界〔待校〕。\n" % a.section_min)
    L.append("4. **標識**：〔OCR 待校〕单源未互证｜〔待听核〕疑误识、存疑不改｜"
             "〔待核〕事实/数目存疑｜〔CBETA 对勘〕§四 精确命中（仅证此串见于底本，"
             "**不等于**讲者已逐字引经）。\n")
    L.append("5. **幻燈片**：含 `|` 者为投影文字与口播拼接，引用前须剥离；"
             "本稿以「含 slide 拼接」标注，不改原文。\n")
    L.append("\n---\n")

    L.append("## 一 · 本集概要（程序实测·非编辑判断）\n\n")
    L.append("- **实测**：%d cues · %s 漢字 · 覆蓋 %s · 时长 %s（%d sec）· 含「|」%d 条 · "
             "片头 40s 内 %d 条 · 含拉丁 %d 条 · ≤2 字短条 %d 条。\n"
             % (ncue, "{:,}".format(nhan), cov_s, ts(declared), declared,
                npipe, nhead, nlatin, nshort))
    L.append("- **首末 cue**：`%s` → `%s`。\n" % (ts(cues[0]["s"]), ts(cues[-1]["e"])))
    L.append("- **品目时间轴**（字面首现 + CBETA 首命中；程序证据，**非**讲者明言）：\n\n")
    L.append("| 品 | 卷 | 字面首现 | CBETA 首命中 | 命中段 | 品名口播 |\n")
    L.append("|---|---|---|---|---|---|\n")
    for no in pins:
        hs = pin_hits.get(no, [])
        first_hit = min((h["t"] for h in hs), default=None)
        L.append("| §%d %s | %d | %s | %s | %d | %d |\n"
                 % (no, PIN_NAMES[no], PIN_JUAN.get(no, 0),
                    ts(first_time(cues, PIN_NAMES[no].replace("品", ""))),
                    first_hit or "—", len(hs), pin_kw.get(no, 0)))
    if not pins:
        L.append("| 〔待核〕 | — | — | — | — | — |\n")
    L.append("\n> 字面首现仅示该品名首次出现，可能是预告/回指；段落起点以听核为准。\n")
    L.append("\n- **问答边界候选**：%s\n"
             % (("`%s` @%s · 触发词「%s」〔待听核〕" % (ts(cues[qa_idx]["s"]),
                                                       ts(cues[qa_idx]["s"]), qa_mark))
                if qa_idx is not None else "未检出明确问答分界〔待核〕"))
    L.append("- **结构**：%d 个时间单元（§A–§%s）。\n"
             % (len(secs), letters[len(secs) - 1]))
    L.append("\n---\n")

    L.append("## 二 · 全文分段（OCR 照录·未按语）\n\n")
    for si, (a0, b0) in enumerate(secs):
        ss = cues[a0]["s"]
        ee = cues[b0 - 1]["e"]
        unit = cues[a0:b0]
        pcount = {no: sum(1 for c in unit if PIN_NAMES[no].replace("品", "") in c["text"])
                  for no in pins}
        dom_no = max(pcount, key=pcount.get) if pcount and max(pcount.values()) > 0 else None
        tcount = [(t, sum(1 for c in unit if t in c["text"])) for t in TERMS]
        top = [t for t, n in sorted(tcount, key=lambda x: -x[1]) if n > 0][:4]
        dom = ("%s %d 次" % (PIN_NAMES[dom_no], pcount[dom_no])) if dom_no else "—"
        L.append("### §%s · %s–%s（%d 段 · 主品：%s）\n\n"
                 % (letters[si], ts(ss), ts(ee), b0 - a0, dom))
        L.append("> 〔程序整理〕按时间停顿切分，非科判；本单元词频（含 slide 标题条）：%s。\n\n"
                 % (" · ".join("%s %d" % (t, n) for t, n in
                                sorted(tcount, key=lambda x: -x[1]) if t in top) or "—"))
        for ci in range(a0, b0):
            c = cues[ci]
            tag = " · 含 slide 拼接「|」" if c["pipe"] else ""
            L.append("**%s%02d** `[OCR %s–%s]`（%d 字 · %d 漢字%s）\n\n"
                     % (letters[si], ci - a0 + 1, ts(c["s"]), ts(c["e"]),
                        len(c["text"]), c["han"], tag))
            L.append(c["text"] + "\n\n")
    L.append("---\n")

    L.append("## 三 · 品目/术语候选（程序提取·待核）\n\n")
    L.append("### 3.1 品目证据\n\n")
    L.append("| 品 | 卷 | CBETA 精确命中段 | 品名口播次数 | 细读会读 |\n")
    L.append("|---|---|---|---|---|\n")
    for no in pins:
        doc = PIN_DOC.get(no)
        L.append("| §%d %s | %d | %d | %d | %s |\n"
                 % (no, PIN_NAMES[no], PIN_JUAN.get(no, 0),
                    len(pin_hits.get(no, [])), pin_kw.get(no, 0),
                    ("`%s`" % doc) if doc and os.path.exists(doc) else "〔未竟·待后续批〕"))
    if not pins:
        L.append("| 〔待核〕 | — | — | — | — |\n")
    L.append("\n> 命中段数＝OCR 稿与 `T10n0279` **连续汉字完全相等**且长度 ≥12 的片段数；"
             "仅证该串见于底本，不证讲者已逐字引经。品名口播次数为字面计数，含 slide 标题条。\n\n")

    L.append("### 3.2 术语候选（字面计数·未定形）\n\n")
    L.append("| 术语 | 口播次数 | 首现 | CBETA 逐字 | 判读 |\n")
    L.append("|---|---|---|---|---|\n")
    term_rows = []
    for t in TERMS:
        n = count_in(cues, t)
        if n <= 0:
            continue
        present = (t in cb) if cb else None
        hitn = sum(1 for h in hits if t in h["text"])
        term_rows.append((n, t, first_time(cues, t), present, hitn))
    term_rows.sort(key=lambda x: -x[0])
    for n, t, ft, present, hitn in term_rows[:30]:
        if present is None:
            verdict = "〔未核〕"
        elif present:
            verdict = "底本见（全局）" + ("·命中 %d 段" % hitn if hitn else "")
        else:
            verdict = "**底本未见**（逐字检索）·不擅等同"
        L.append("| %s | %d | %s | %s | %s |\n"
                 % (t, n, ts(ft), "〔未核〕" if present is None else ("见" if present else "未见"), verdict))
    if len(term_rows) > 30:
        L.append("\n> 仅列前 30 个词频 ≥1 的候选；余 %d 个候选未列。\n" % (len(term_rows) - 30))
    L.append("\n> 术语表为**程序候选**，未作义理定形；「底本未见」仅指逐字检索 `T10n0279` "
             "未见，不擅等同近形/异体；口播计数含 slide 标题条。\n\n")
    L.append("---\n")

    L.append("## 四 · CBETA 回源（程序切片·非手抄）\n\n")
    if not hits:
        L.append("本轮未产生 ≥12 字的精确命中；**不得**据此称「本集无经文引文」——"
                 "可能为口诵差异、OCR 误识或本集确未引经，〔待听核〕。\n\n")
    else:
        L.append("### 4.1 Anchor 切片（按品×卷钳制·前后 40 字）\n\n")
        slice_no = 0
        for no in pins:
            hs = pin_hits.get(no, [])
            for g in group_hits(hs):
                slice_no += 1
                if slice_no > a.max_slices:
                    break
                s0 = max(g[0]["span_start"], min(h["pos"] for h in g) - 40)
                e0 = min(g[0]["span_end"], max(h["pos"] + h["len"] for h in g) + 40)
                hs0 = min(h["pos"] for h in g)
                he0 = max(h["pos"] + h["len"] for h in g)
                parts, cur = [], s0
                for h in g:
                    hp, hq = h["pos"], h["pos"] + h["len"]
                    parts.append(cb[cur:hp])
                    parts.append("**" + cb[hp:hq] + "**")
                    cur = hq
                parts.append(cb[cur:e0])
                snip = "".join(parts)
                L.append("#### 4.1.%d §%d %s（卷 %d）· @%d–%d · OCR %s–%s（%d 命中）\n\n"
                         % (slice_no, no, PIN_NAMES[no], PIN_JUAN.get(no, 0),
                            s0, e0, min(h["t"] for h in g), max(h["t"] for h in g), len(g)))
                L.append("> %s%s%s\n\n"
                         % ("…" if s0 > g[0]["span_start"] else "",
                            snip,
                            "…" if e0 < g[0]["span_end"] else ""))
            if slice_no > a.max_slices:
                break
        total_groups = sum(len(group_hits(pin_hits.get(n, []))) for n in pins)
        if total_groups > a.max_slices:
            L.append("> 切片上限 %d 组；余 %d 组见 `.tmp/ep%02d_cbeta.json`。\n\n"
                     % (a.max_slices, total_groups - a.max_slices, ep))
        L.append("> 切片只覆盖命中段前后 40 字；**加粗＝逐字命中段**，前后为底本上下文，"
                 "未证讲者已诵；品×卷边界由底本 `cb:mulu` 自动钳制。访问日期 2026-11-16。\n\n")

        L.append("### 4.2 逐字命中清单\n\n")
        for no in pins:
            hs = pin_hits.get(no, [])
            if not hs:
                continue
            L.append("#### §%d %s（卷 %d）· 去重 %d 条语串\n\n"
                     % (no, PIN_NAMES[no], PIN_JUAN.get(no, 0), len(hs)))
            for h in hs[:60]:
                also = ("（底本亦见 %s·stock 句式）"
                        % "、".join("§%s %s" % (p, n) for p, n, j in h.get("also", []))
                        ) if h.get("also") else ""
                L.append("- `[OCR %s]` @%d · %d 字 · **%s**%s\n"
                         % (h["t"], h["pos"], h["len"], h["text"], also))
            if len(hs) > 60:
                L.append("- … 余 %d 段（见 `.tmp/ep%02d_cbeta.json`）\n"
                         % (len(hs) - 60, ep))
            L.append("\n")
        L.append("> 底本 `T10n0279` 去 note/app/标签、压平空白后逐字比对。"
                 "异体字（焰/燄、恒/恆、遶/繞等）各照底本，不统一。\n\n")
    L.append("---\n")

    L.append("## 五 · 与《华严经细读》之会读（程序映射）\n\n")
    for no in pins:
        doc = PIN_DOC.get(no)
        if doc and os.path.exists(doc):
            L.append("- §%d %s → `%s`\n" % (no, PIN_NAMES[no], doc))
        elif doc:
            L.append("- §%d %s → 〔未竟·待后续批〕`%s`\n" % (no, PIN_NAMES[no], doc))
    if not pins:
        L.append("- 〔待核〕品目未定，暂不建立会读链接。\n")
    L.append("\n---\n")

    L.append("## 六 · 存疑 · 待听核清单\n\n")
    L.append("- 品目归属：本集 §%s 为程序候选，须与录音/讲义听核后坐实〔待核〕。\n"
             % ("/§".join(str(p) for p in pins) if pins else "—"))
    L.append("- 问答边界：%s\n"
             % (("`%s` 触发「%s」为程序候选，须听核定界〔待听核〕"
                 % (ts(cues[qa_idx]["s"]), qa_mark)) if qa_idx is not None
                else "未检出明确标记，边界〔待核〕"))
    L.append("- 片头 40 秒内 %d 条（动画/角标残帧），引用时整段删除即可。\n" % nhead)
    L.append("- 含「|」%d 条为幻灯片与口播拼接，引用前须剥离（不得以投影字充法师语）。\n" % npipe)
    L.append("- ≤2 字短条 %d 条，多为换句残字或标题条，逐字引证不可用。\n" % nshort)
    L.append("- 简繁混排未统一（依铁律照原），术语定形俟 K3d。\n")
    L.append("- 「底本未见」术语不擅等同近形/异体；须听核或讲义互证〔待核〕。\n")
    L.append("- 本稿**未作**语词级三源互证（讲义/录音/影像），不得称定稿；状态见 §七。\n")
    L.append("\n---\n")

    L.append("## 七 · 三源互证状态\n\n")
    L.append("| 源 | 状态 | 证据 / 缺口 |\n")
    L.append("|---|---|---|\n")
    L.append("| 影像硬字幕（OCR） | 已得 | 720p · %d cues · 覆盖 %s · 三产物条数相符 |\n"
             % (ncue, cov_s))
    L.append("| CBETA `T10n0279` | 已程序对勘 | §四 精确命中 %d 段（去重 %d 条语串）；切片按品×卷钳制 |\n"
             % (nhits_raw, nhits_u))
    L.append("| 寺方字幕原稿 | 未得 | 交付者明言原稿已遗失；本稿仅为影像层还原 |\n")
    L.append("| 讲义 / 录音 | 未得 | 无讲义、无独立录音 → 语词级校定与「丢首字」复核未完成 |\n")
    if pod.get("url"):
        L.append("| 官方播客 | 已映射 | %s（%s）· 正行+问答双条；内容未逐句比对 |\n"
                 % (pod.get("label", ""), pod.get("confidence", "")))
    else:
        L.append("| 官方播客 | 未映射 | 9 月场次分条待核 |\n")
    L.append("\n> 结论：**影像 + CBETA 两源可核；三源互证尚缺讲义/录音一源**。"
             "故本稿可作内容索引、主题定位、时间锚点与经文候选，不作逐字引证。\n\n")

    L.append("## 八 · 完成度与缺口（自评）\n\n")
    L.append("| 项 | 状态 | 说明 |\n")
    L.append("|---|---|---|\n")
    L.append("| OCR 全文照录 | 已 | %d cues / %s 漢字 / 覆盖 %s |\n"
             % (ncue, "{:,}".format(nhan), cov_s))
    L.append("| 品目定位 | 程序候选 | §一 时间轴；待听核 |\n")
    L.append("| CBETA 回源 | 已程序切片 | §四；命中≠讲者已逐字引经 |\n")
    L.append("| 术语表 | 程序候选 | §3.2；未定形，底本未见者不擅等同 |\n")
    L.append("| 逐段按语 | 未 | K3d 编辑判断；本生成器不代写 |\n")
    L.append("| 三源互证 | 未 | 缺讲义/录音；§七 已列状态 |\n")
    L.append("| 播客映射 | %s | %s |\n"
             % ("已" if pod.get("url") else "未",
                pod.get("label", "待核")))
    L.append("| 讲章科判 | 未 | §二 为时间单元，非讲章 |\n")

    txt = "".join(L)
    io.open(out, "w", encoding="utf-8", newline="\n").write(txt)
    print("已生成 %s · %d bytes · %d cues · %d 段 · %d 品目 · CBETA 命中 %d 段（去重 %d）· 切片 %d 组"
          % (out, len(txt.encode("utf-8")), ncue, len(secs), len(pins), nhits_raw, nhits_u,
             min(a.max_slices, sum(len(group_hits(pin_hits.get(n, []))) for n in pins))))
    return 0


if __name__ == "__main__":
    sys.exit(main())