#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
miaoyan_eda.py — 世主妙严品会众名号构词法 EDA 生成器

输入：
  data/translation/miaoyan_assembly.yaml        会众结构（40 类 / 414 名，权威源）
  data/translation/miaoyan_eda_lexicon.yaml     词素表（人工编纂，含 semantic domain）
输出：
  data/translation/miaoyan_eda.yaml             EDA 派生数据（供 db_reader → build → 前端）

设计立场（依「考证优先」「严禁假信息」「杜绝硬编码」）：
  1. **源数据是权威**：类名、成员名、类序、众数表达、上首、集总词、誓愿——全部取自
     miaoyan_assembly.yaml，本脚本不新增、不改写、不臆补任何经文事实。
  2. **词素切分为编辑性分析**：单字切分是本脚本的**方法选择**（非经文原貌），
     故输出一律带 `method` 与 `caveat` 字段，在前端显著标注〔析构·待考〕。
  3. **域归类为人工判读**：domain 取值来自 lexicon.yaml；未入表者不臆补，
     计入 `unsegmented` 并在前端「待补词素」区列出。
  4. **统计可复现**：频次矩阵、组合矩阵、二部图边集皆由数据算出，非人工填写。
  5. **对重复与异体如实报备**：跨类同名（如「可愛樂光明天王」）、CBETA 异体字
     （焰/峯/眾/淨/彌/毘）均单独登记，不静默合并。

用法：
  python scripts/miaoyan_eda.py            # 生成 miaoyan_eda.yaml
  python scripts/miaoyan_eda.py --check    # 只校验（不写文件）
  python scripts/miaoyan_eda.py --print    # 打印统计摘要到 stdout
"""
from __future__ import annotations

import argparse
import collections
import io
import json
import os
import re
import sys
from typing import Any, Dict, List, Tuple

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.stderr.write("需要 PyYAML：conda activate hy_py312\n")
    raise

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSEMBLY = os.path.join(ROOT, "data", "translation", "miaoyan_assembly.yaml")
LEXICON = os.path.join(ROOT, "data", "translation", "miaoyan_eda_lexicon.yaml")
EDA_OUT = os.path.join(ROOT, "data", "translation", "miaoyan_eda.yaml")

# 十七语义域 → 呈现序（与 lexicon.yaml 头部说明一致）
# L.100 新增 dharma（法教类）：「法」自成一义群（法界/法性/法教/法门），
# 既非 nature（物象）亦非 wisdom（心智）亦非 virtue（功德），故立新域而不屈就。
DOMAIN_ORDER = [
    "luminosity", "jewel", "sound", "form", "virtue", "wisdom", "power",
    "motion", "nature", "space", "body", "speech", "time", "number",
    "affix", "dharma", "unassigned",
]
DOMAIN_ZH = {
    "luminosity": "光明类", "jewel": "宝严类", "sound": "音聲类", "form": "形相类",
    "virtue": "功德类", "wisdom": "智慧类", "power": "威势力类", "motion": "動行类",
    "nature": "自然类", "space": "空間类", "body": "身體類", "speech": "言說类",
    "time": "時間类", "number": "數量类", "affix": "冠綴类", "dharma": "法教类",
    "unassigned": "未定",
}
DOMAIN_EN = {
    "luminosity": "luminosity", "jewel": "jewel-adornment", "sound": "sound",
    "form": "form", "virtue": "merit-virtue", "wisdom": "wisdom", "power": "power",
    "motion": "motion", "nature": "nature", "space": "space", "body": "body",
    "speech": "speech", "time": "time", "number": "quantity", "affix": "affix",
    "dharma": "dharma-teaching", "unassigned": "unassigned",
}
DOMAIN_COLOR = {
    "luminosity": "#f2c14e", "jewel": "#c0392b", "sound": "#8e6cbb",
    "form": "#2e86ab", "virtue": "#27ae60", "wisdom": "#16a085",
    "power": "#d35400", "motion": "#7f8c8d", "nature": "#1e8449",
    "space": "#5dade2", "body": "#af7ac5", "speech": "#e67e22",
    "time": "#7d6608", "number": "#5d6d7e", "affix": "#a04000",
    "dharma": "#6c3483", "unassigned": "#b3b3b3",
}
GROUP_ORDER = ["bodhisattva", "deities", "eight", "desire", "form"]
GROUP_ZH = {
    "bodhisattva": "同生众·菩萨",
    "deities": "异生众·十九类神",
    "eight": "异生众·八部",
    "desire": "异生众·欲界天",
    "form": "异生众·色界天",
}
GROUP_EN = {
    "bodhisattva": "bodhisattvas", "deities": "nineteen classes of deities",
    "eight": "eight classes of non-humans", "desire": "desire-realm gods",
    "form": "form-realm gods",
}

# ── 名号类尾（后缀）────────────────────────────────────────────
# 类尾**不再查全局尾表**：改由 class_tail() 依各类成员自身的最长公共后缀逐类派生
# （「主X神」类只剥末字「神」而保留「主X」）。原全局尾表会因「神/王/天子」等短尾
# 先命中而使「執金剛神」「阿脩羅王」等复合尾一次也剥不到——18 条中 13 条落空，
# 致八部与造型神核名残留音译类名、名号字数虚高、伪搭配混入 pair_freq。
# 下列 SUFFIX_FALLBACK 仅作 lexicon.yaml class_tails 段缺失时的兜底，正常路径不走。
SUFFIX_FALLBACK = ["菩薩摩訶薩", "菩薩", "執金剛", "身眾", "足行", "道場",
                   "天子", "神", "王", "天",
                   "阿脩羅", "迦樓羅", "緊那羅", "摩睺羅伽", "夜叉", "龍",
                   "鳩槃荼", "乾闥婆"]

# CBETA 原字形 ↔ 通行正字（仅登记，不改经文字形）
GLYPH_VARIANTS = [
    {"cbeta": "焰", "common": "燄", "n": None},
    {"cbeta": "峯", "common": "峰", "n": None},
    {"cbeta": "眾", "common": "衆", "n": None},
    {"cbeta": "淨", "common": "净", "n": None},
    {"cbeta": "彌", "common": "弥", "n": None},
    {"cbeta": "毘", "common": "毗", "n": None},
    {"cbeta": "莊", "common": "庄", "n": None},
    {"cbeta": "寶", "common": "宝", "n": None},
    {"cbeta": "脩", "common": "修", "n": None},
]


def _load(path: str) -> Any:
    with io.open(path, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def lcs_suffix(names: List[str]) -> str:
    """一组名的最长公共后缀——即该类成员共有的「类尾」。

    各名先去掉句末标点与省文号（经文列名常以「……」收尾，如「大福光智生菩薩摩訶薩……」），
    否则该名会以「……」收尾而使公共后缀落空。
    """
    if not names:
        return ""
    clean = [n.rstrip("。…、， ") for n in names if n.rstrip("。…、， ")]
    if not clean:
        return ""
    s = clean[0]
    for n in clean[1:]:
        k = 0
        while k < len(s) and k < len(n) and s[len(s) - 1 - k] == n[len(n) - 1 - k]:
            k += 1
        s = s[len(s) - k:]
    return s


def class_tail(cat: str, names: List[str], is_zhu: bool) -> str:
    """由该类成员自身逐类派生类尾（数据驱动，不依赖全局尾表）。

    派生规则（顺序即优先）：
      1. 「主X神」类：只剥末字「神」，**保留「主X」**——因「主」为句式标记
         （标示所主），属名之结构成分而非可弃之尾缀。
      2. 其余各类：取成员最长公共后缀。这既命中「執金剛神」「阿脩羅王」全称，
         亦能处理类名本身不是后缀的情形（「諸大龍王」之成员共尾为「龍王」）。
    """
    if is_zhu and names and all(n.endswith("神") for n in names):
        return "神"
    return lcs_suffix(names)


def strip_suffix(name: str, suf: str) -> Tuple[str, str]:
    """去名号类尾 → (核名, 类尾)。核名空则整名返回（整名即类名者，如「天子」）。"""
    s = name.rstrip("。…")
    if suf and s.endswith(suf) and len(s) > len(suf):
        return s[: -len(suf)], suf
    return s, ""


def build_lexicon(raw: Any) -> Dict[str, Dict[str, Any]]:
    """词素表 → {zh: entry}，以首见为准。"""
    out: Dict[str, Dict[str, Any]] = {}
    for m in raw.get("morphemes", []) or []:
        if not m or not m.get("zh"):
            continue
        zh = m["zh"]
        if len(zh) != 1:          # 词素表只收单字
            continue
        out.setdefault(zh, {
            "zh": zh,
            "py": m.get("py", ""),
            "domain": m.get("domain", "unassigned"),
            "gloss": m.get("gloss", ""),
            "gloss_en": m.get("gloss_en", ""),
            "c": m.get("c", "low"),
            "note": m.get("note", ""),
            # L.100：已考订而**不可归域**之罕字标记（如 𪗇／㵎）。
            # 此标记只用于区分「待归域」与「不可归域」，不改变 domain 值，
            # 亦不参与任何计数以外的逻辑——防止后续批次为凑「unassigned→0」
            # 而臆造语义域（违「严禁假信息」）。
            "unresolved_glyph": bool(m.get("unresolved_glyph", False)),
        })
    return out


def build_lexemes(raw: Any) -> List[Dict[str, Any]]:
    """多字词表 → 按长度降序（最长匹配优先）。"""
    lx = []
    for m in raw.get("lexemes", []) or []:
        if m and m.get("zh") and len(m["zh"]) > 1:
            lx.append({
                "zh": m["zh"],
                "domain": m.get("domain", "unassigned"),
                "gloss": m.get("gloss", ""),
                "gloss_en": m.get("gloss_en", ""),
                "c": m.get("c", "low"),
                "note": m.get("note", ""),
            })
    lx.sort(key=lambda m: -len(m["zh"]))
    return lx


def build_tails(raw: Any) -> List[str]:
    """类尾表 → 长度降序的剥离顺序（数据驱动，缺则回退内置表）。"""
    tails = [t["zh"] for t in (raw.get("class_tails") or []) if t.get("zh")]
    if not tails:
        tails = list(SUFFIX_FALLBACK)
    return sorted(set(tails), key=lambda s: -len(s))


def segment(core: str, lex: Dict[str, Dict[str, Any]],
            lexemes: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[str]]:
    """两段切分：先按多字词最长匹配，未命中者再逐字。
    返回 ([seg...], [未入表字])；seg.mode ∈ word|char
    """
    toks: List[Dict[str, Any]] = []
    miss: List[str] = []
    i = 0
    n = len(core)
    while i < n:
        hit = None
        for lx in lexemes:                      # 词级
            w = lx["zh"]
            if core.startswith(w, i):
                hit = lx
                break
        if hit:
            toks.append({"zh": hit["zh"], "domain": hit["domain"], "c": hit["c"],
                         "known": True, "mode": "word"})
            i += len(hit["zh"])
            continue
        ch = core[i]                            # 字级
        e = lex.get(ch)
        if e:
            toks.append({"zh": ch, "domain": e["domain"], "c": e["c"],
                         "known": True, "mode": "char"})
        else:
            toks.append({"zh": ch, "domain": "unassigned", "c": "low",
                         "known": False, "mode": "char"})
            miss.append(ch)
        i += 1
    return toks, miss


def segment_chars_only(core: str, lex: Dict[str, Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[str]]:
    """纯逐字切分（对照法），用于与两段切分互校。"""
    toks, miss = [], []
    for ch in core:
        e = lex.get(ch)
        if e:
            toks.append({"zh": ch, "domain": e["domain"], "c": e["c"], "known": True, "mode": "char"})
        else:
            toks.append({"zh": ch, "domain": "unassigned", "c": "low", "known": False, "mode": "char"})
            miss.append(ch)
    return toks, miss


def _build_group_profiles(order, zh, en, n_by_group, classes_by_group,
                         tok_by_group, dom_by_group, head_by_group, tailch_by_group,
                         wordhit_by_group, lowconf_by_group, medconf_by_group,
                         nchars_by_group, len_by_group, tails_derived, notes, dom_of):
    """群级纵深剖面：定量（脚本算得）+ 定性（取自 lexicon.yaml group_profiles 段）。

    定性描述不写在脚本里（编务总则·杜绝硬编码）：脚本只负责算出可核的量，
    「此群何以如此」的判断由 lexicon.yaml 的 group_profiles 段提供，此处按 key 合并。
    缺该段则对应字段留空，页面显示「〔未录〕」，不以脚本内的先入之见填补。
    """
    out = []
    all_groups = [g for g in order if n_by_group.get(g)]
    for g in all_groups:
        n = n_by_group[g]
        toks = tok_by_group[g]
        tok_sum = sum(toks.values()) or 1        # 分母为词素位数，非成员数
        note = (notes or {}).get(g) or {}
        # 群特有词素：只此群出现（全库别群皆无）
        exclusive = [z for z, c in toks.most_common()
                     if c >= 2 and all(tok_by_group[o].get(z, 0) == 0
                                       for o in all_groups if o != g)]
        # 群内多字词
        words = [{"zh": z, "n": c} for z, c in wordhit_by_group[g].most_common(8)]
        doms = [{"domain": d, "domain_zh": DOMAIN_ZH.get(d, d), "n": c,
                 "pct": round(100.0 * c / tok_sum, 1)}
                for d, c in dom_by_group[g].most_common()]
        tails = sorted({t["tail"] for t in tails_derived if t["group"] == g})
        lens = len_by_group[g]
        out.append({
            "key": g, "zh": zh.get(g, g), "en": en.get(g, g),
            "n_named": n,
            "n_tokens": tok_sum,
            "n_classes": len(classes_by_group.get(g, [])),
            "classes": classes_by_group.get(g, []),
            "n_core_chars": nchars_by_group.get(g, 0),
            "core_len_mean": round(nchars_by_group.get(g, 0) / max(1, n), 2),
            "core_len_min": min(lens) if lens else 0,
            "core_len_max": max(lens) if lens else 0,
            "len_hist": dict(sorted(lens.items())),
            "n_distinct_morph": len(toks),
            "n_word_hits": sum(wordhit_by_group[g].values()),
            "n_lowconf": lowconf_by_group.get(g, 0),
            "lowconf_pct": round(100.0 * lowconf_by_group.get(g, 0) / tok_sum, 1),
            "n_medconf": medconf_by_group.get(g, 0),
            "medconf_pct": round(100.0 * medconf_by_group.get(g, 0) / tok_sum, 1),
            "top_morphs": [{"zh": z, "n": c,
                            "domain_zh": DOMAIN_ZH.get(dom_of.get(z, "unassigned"), "未定")}
                           for z, c in toks.most_common(12)],
            "exclusive_morphs": [{"zh": z, "n": toks[z]} for z in exclusive[:10]],
            "top_heads": [{"zh": z, "n": c} for z, c in head_by_group[g].most_common(6)],
            "top_tailchs": [{"zh": z, "n": c} for z, c in tailch_by_group[g].most_common(6)],
            "word_hits": words,
            "domains": doms,
            "top_domain": doms[0] if doms else {},
            "class_tails": tails,
            # 定性（lexicon.yaml 提供；缺则空字符串，页面显示「〔未录〕」）
            "note": note.get("note", ""),
            "note_en": note.get("note_en", ""),
            "character": note.get("character", ""),
        })

    # ── 群间对比：词素重合度 + 主导域距离 ──
    pairs = []
    for i, a in enumerate(all_groups):
        for b in all_groups[i + 1:]:
            sa, sb = set(tok_by_group[a]), set(tok_by_group[b])
            inter, uni = sa & sb, sa | sb
            shared = sorted(inter, key=lambda z: -(tok_by_group[a][z] + tok_by_group[b][z]))
            da = {d["domain"]: d["pct"] for d in next(
                (p["domains"] for p in out if p["key"] == a), [])}
            db = {d["domain"]: d["pct"] for d in next(
                (p["domains"] for p in out if p["key"] == b), [])}
            dist = sum(abs(da.get(d, 0.0) - db.get(d, 0.0))
                       for d in set(da) | set(db)) / 2.0
            pairs.append({
                "a": a, "b": b,
                "a_zh": zh.get(a, a), "b_zh": zh.get(b, b),
                "shared": len(inter),
                "jaccard": round(len(inter) / max(1, len(uni)), 3),
                "top_shared": [{"zh": z,
                                "n_a": tok_by_group[a][z], "n_b": tok_by_group[b][z]}
                               for z in shared[:8]],
                "domain_dist": round(dist, 1),
            })
    pairs.sort(key=lambda p: (-p["shared"], p["domain_dist"]))
    return out, pairs


def analyse(asm: Any, lexraw: Any) -> Dict[str, Any]:
    lex = build_lexicon(lexraw)
    lexemes = build_lexemes(lexraw)
    classes = asm["classes"]

    # ── 逐类逐名切分 ──
    per_class: List[Dict[str, Any]] = []
    tok_total = collections.Counter()           # 两段切分：词/字位 → 次数
    char_total = collections.Counter()          # 纯逐字对照：字 → 次数
    dom_total = collections.Counter()            # domain → 次数
    dom_by_group: Dict[str, collections.Counter] = {g: collections.Counter() for g in GROUP_ORDER}
    n_by_group: Dict[str, int] = collections.Counter()
    pair_total = collections.Counter()          # 有序二元组 → 次数
    pair_by_group: Dict[str, collections.Counter] = {g: collections.Counter() for g in GROUP_ORDER}
    tail_total = collections.Counter()
    head_total = collections.Counter()           # 核名首字
    tailch_total = collections.Counter()         # 核名末字
    len_by_group: Dict[str, collections.Counter] = {g: collections.Counter() for g in GROUP_ORDER}
    unsegmented = collections.Counter()          # 未入表字 → 出现次数
    lowconf_hits = collections.Counter()         # c == "low" 逐位计（前端须显示〔待考〕者）
    medconf_hits = collections.Counter()         # c == "medium" 单列，不与 low 混计
    word_hits = collections.Counter()            # 多字词命中 → 次数
    # ── 群组纵深所需累加器（群级钻取，见 group_profiles）──
    tok_by_group: Dict[str, collections.Counter] = {g: collections.Counter() for g in GROUP_ORDER}
    head_by_group: Dict[str, collections.Counter] = {g: collections.Counter() for g in GROUP_ORDER}
    tailch_by_group: Dict[str, collections.Counter] = {g: collections.Counter() for g in GROUP_ORDER}
    wordhit_by_group: Dict[str, collections.Counter] = {g: collections.Counter() for g in GROUP_ORDER}
    lowconf_by_group: Dict[str, int] = collections.Counter()
    medconf_by_group: Dict[str, int] = collections.Counter()
    nchars_by_group: Dict[str, int] = collections.Counter()
    classes_by_group: Dict[str, List[str]] = collections.defaultdict(list)
    core_of: Dict[str, str] = {}                 # 整名 → 核名
    core_classes: Dict[str, List[str]] = collections.defaultdict(list)
    # 「〔形容〕主〔所主〕」句式：主X神 类的结构分析
    zhu_formula: List[Dict[str, Any]] = []
    class_tails_derived: List[Dict[str, Any]] = []
    n_no_core = 0                                  # 整名即类名（无核名可析）者

    for c in classes:
        g = c["group"]
        mdom = collections.Counter()
        mtok = collections.Counter()
        mhead = collections.Counter()
        mtailch = collections.Counter()
        mpair = collections.Counter()
        clen = collections.Counter()
        members_out: List[Dict[str, Any]] = []
        is_zhu_class = bool(c["cat"].endswith("神")) and "主" in c["cat"]
        classes_by_group[g].append(c["cat"])       # 每类只记一次（不可置于成员循环内）
        # 类尾由本类成员自身派生（见 class_tail()），非查全局尾表
        ctail = class_tail(c["cat"], list(c["members"]), is_zhu_class)
        leader_core, leader_tail = strip_suffix(c["leader"], ctail)
        n_zhu_hits = 0
        zhu_targets: List[str] = []

        for mi, raw in enumerate(c["members"], 1):
            name = raw.rstrip("。…")
            core, tail = strip_suffix(raw, ctail)
            if not tail:
                n_no_core += 1
            core_of[name] = core
            core_classes[core].append(c["cat"])

            toks, miss = segment(core, lex, lexemes)
            ctoks, cmiss = segment_chars_only(core, lex)
            for t in toks:
                if t["known"]:
                    tok_total[t["zh"]] += 1
                    mtok[t["zh"]] += 1
                    tok_by_group[g][t["zh"]] += 1
                    if t["mode"] == "word":
                        word_hits[t["zh"]] += 1
                        wordhit_by_group[g][t["zh"]] += 1
                    dom_total[t["domain"]] += 1
                    mdom[t["domain"]] += 1
                    dom_by_group[g][t["domain"]] += 1
                    if t["c"] == "low":
                        lowconf_hits[t["zh"]] += 1
                        lowconf_by_group[g] += 1
                    elif t["c"] == "medium":
                        medconf_hits[t["zh"]] += 1
                        medconf_by_group[g] += 1
                else:
                    unsegmented[t["zh"]] += 1
            nchars_by_group[g] += len(core)
            for t in ctoks:
                if t["known"]:
                    char_total[t["zh"]] += 1
            # 有序二元组（相邻词素，词级切分结果）
            for i in range(len(toks) - 1):
                a, b = toks[i]["zh"], toks[i + 1]["zh"]
                pair_total[(a, b)] += 1
                mpair[(a, b)] += 1
                pair_by_group[g][(a, b)] += 1
            if core:
                mhead[core[0]] += 1
                head_total[core[0]] += 1
                head_by_group[g][core[0]] += 1
                mtailch[core[-1]] += 1
                tailch_total[core[-1]] += 1
                tailch_by_group[g][core[-1]] += 1
            clen[len(core)] += 1
            len_by_group[g][len(core)] += 1
            tail_total[tail] += 1
            n_by_group[g] += 1
            # 「主Y」句式检出：核名中「主」之后所接的「所主」
            zhu_obj = ""
            if is_zhu_class and "主" in core:
                k = core.rindex("主")
                zhu_obj = core[k + 1:]
                n_zhu_hits += 1
                zhu_targets.append(zhu_obj)

            members_out.append({
                "i": mi,
                "name": name,
                "core": core,
                "tail": tail,
                "is_leader": 1 if name == leader_core + leader_tail else 0,
                "n_char": len(core),
                "head": core[0] if core else "",
                "tailch": core[-1] if core else "",
                "segs": toks,
                "segs_char_only": ctoks,
                "domains": [t["domain"] for t in toks],
                "n_word": sum(1 for t in toks if t["mode"] == "word"),
                "n_unsegmented": len(miss),
                "n_unsegmented_char_only": len(cmiss),
                "zhu_object": zhu_obj,
            })

        if is_zhu_class:
            zhu_formula.append({
                "cat": c["cat"], "idx": c["idx"], "group": g,
                "n_named": c.get("n_named", len(c["members"])),
                "n_formula": n_zhu_hits,
                "pct": round(100.0 * n_zhu_hits / max(1, len(c["members"])), 1),
                "objects": collections.Counter(zhu_targets).most_common(),
            })

        # 派生类尾入册（可审计：读者据表即可复算核名）
        n_tailed = sum(1 for m in members_out if m["tail"])
        class_tails_derived.append({
            "cat": c["cat"], "idx": c["idx"], "group": g,
            "tail": ctail, "n_members": len(c["members"]),
            "n_tailed": n_tailed, "n_no_core": len(c["members"]) - n_tailed,
            "rule": "zhu-keep" if is_zhu_class else "lcs",
        })

        top_dom = sorted(mdom.items(), key=lambda kv: (-kv[1], kv[0]))
        per_class.append({
            "idx": c["idx"],
            "cat": c["cat"],
            "group": g,
            "group_zh": c.get("group_zh") or GROUP_ZH.get(g, g),
            "realm": c.get("realm", ""),
            "count_expr": c.get("count_expr", ""),
            "leader": c.get("leader", ""),
            "leader_core": leader_core,
            "leader_tail": leader_tail,
            "n_named": c.get("n_named", len(c["members"])),
            "domain_zh": c.get("domain_zh", ""),
            "collective": c.get("collective", ""),
            "collective_pos": c.get("collective_pos", ""),
            "vow_kind": c.get("vow_kind", ""),
            "n_char_total": sum(m["n_char"] for m in members_out),
            "len_hist": {str(k): v for k, v in sorted(clen.items())},
            "head_hist": dict(mhead.most_common()),
            "tailch_hist": dict(mtailch.most_common()),
            "domain_hist": {d: n for d, n in top_dom},
            "domain_top": top_dom[0][0] if top_dom else "",
            "top_morphemes": [{"zh": z, "n": n} for z, n in mtok.most_common(8)],
            "top_pairs": [{"a": a, "b": b, "n": n} for (a, b), n in mpair.most_common(6)],
            "n_word_hits": sum(m["n_word"] for m in members_out),
            "n_unsegmented": sum(m["n_unsegmented"] for m in members_out),
            "members": members_out,
        })

    # ── 跨类同核名 ──
    dup_cores = [
        {"core": k, "classes": sorted(set(v)), "n": len(v)}
        for k, v in core_classes.items() if len(set(v)) > 1
    ]
    dup_cores.sort(key=lambda d: (-d["n"], d["core"]))

    # ── 跨类同赞词（epithet sharing）──
    # 「主X神」之名作「〔赞词〕主〔所主〕神」，核名因所主槽不同而相异，
    # 故 core_duplicates（整核相同）**结构上看不见**共赞词者，须另测：
    # 剥去「主X」槽后比较前半赞词。十九类神之外不适用（无此句式）。
    epi_classes: Dict[str, List[str]] = collections.defaultdict(list)
    epi_detail: Dict[str, List[Dict[str, str]]] = collections.defaultdict(list)
    n_epithet_members = 0
    for c in classes:
        if not (c["cat"].endswith("神") and "主" in c["cat"]):
            continue
        ctail = class_tail(c["cat"], list(c["members"]), True)
        for mi, raw in enumerate(c["members"], 1):
            name = raw.rstrip("。…")
            core_, _ = strip_suffix(name, ctail)
            mo = re.match(r"^(.*)主(.+)$", core_)
            if not mo:
                continue
            epi = mo.group(1)
            n_epithet_members += 1
            epi_classes[epi].append(c["cat"])
            # 只存「类」与「所主槽」：成员原名属经文事实，只在 assembly 一处，
            # 此处不复制（页面上由赞词＋所主槽＋类尾现拼）。
            epi_detail[epi].append({"cat": c["cat"], "domain": mo.group(2)})
    dup_epithets = [
        {"epithet": k, "n": len(v), "classes": sorted(set(v)), "members": epi_detail[k]}
        for k, v in epi_classes.items() if len(set(v)) > 1
    ]
    dup_epithets.sort(key=lambda d: (-d["n"], d["epithet"]))

    # ── 异体字实数（不改字形，仅统计）──
    glyph_stats = []
    all_cores = list(core_of.values())
    for gv in GLYPH_VARIANTS:
        n_cbeta = sum(1 for s in all_cores if gv["cbeta"] in s)
        n_common = sum(1 for s in all_cores if gv["common"] in s)
        if n_cbeta or n_common:
            glyph_stats.append({
                "cbeta": gv["cbeta"], "common": gv["common"],
                "n_cbeta": n_cbeta, "n_common": n_common,
            })

    # ── 语义网络节点/边 ──
    lexnodes = []
    lx_by_zh = {m["zh"]: m for m in lexemes}
    for z, n in tok_total.most_common():
        e = lex.get(z) or lx_by_zh.get(z, {})
        lexnodes.append({
            "id": "m:" + z, "zh": z, "py": e.get("py", ""),
            "domain": e.get("domain", "unassigned"),
            "domain_zh": DOMAIN_ZH.get(e.get("domain", "unassigned"), "未定"),
            "n": n, "c": e.get("c", "low"),
            "mode": "word" if z in lx_by_zh else "char",
            "gloss": e.get("gloss", ""), "gloss_en": e.get("gloss_en", ""),
        })
    lexedges = [
        {"source": "m:" + a, "target": "m:" + b, "n": n}
        for (a, b), n in pair_total.most_common(400) if a in tok_total and b in tok_total
    ]

    # ── 二部图：类 ↔ 成员 ──
    classnodes = [
        {"id": "c:%d" % c["idx"], "cat": c["cat"], "group": c["group"],
         "n_named": c["n_named"], "label": c["cat"]}
        for c in per_class
    ]
    binedges = []
    for c in per_class:
        for m in c["members"]:
            binedges.append({
                "source": "c:%d" % c["idx"],
                "target": "m:%d:%d" % (c["idx"], m["i"]),
                "n": 1,
            })

    # ── 热力图矩阵：group × domain ──
    # 分母须为该群「词素位」总数（tok 数），不可用成员数：一名之核名可含多个同域词素，
    # 以成员数为分母会使 pct 超过 100%（旧法即有此失，如 deities 冠缀类 124.2%）。
    heat = []
    for g in GROUP_ORDER:
        tok_sum = sum(dom_by_group[g].values()) or 1
        row = {"group": g, "group_zh": GROUP_ZH[g], "n": n_by_group[g],
               "n_tokens": sum(dom_by_group[g].values()), "cells": []}
        for d in DOMAIN_ORDER:
            n = dom_by_group[g].get(d, 0)
            row["cells"].append({
                "domain": d, "domain_zh": DOMAIN_ZH[d], "n": n,
                "pct": round(100.0 * n / tok_sum, 2),
            })
        heat.append(row)

    # ── 词素×类群 矩阵（取高频前 40）──
    top40 = [z for z, _ in tok_total.most_common(40)]
    morph_group: Dict[str, Dict[str, int]] = {}
    for c in per_class:
        g = c["group"]
        acc = morph_group.setdefault(g, collections.Counter())
        for m in c["members"]:
            for t in m["segs"]:
                if t["known"]:
                    acc[t["zh"]] += 1
    morph_matrix = [
        {"zh": z,
         "domain": (lex.get(z) or lx_by_zh.get(z, {})).get("domain", "unassigned"),
         "domain_zh": DOMAIN_ZH.get((lex.get(z) or lx_by_zh.get(z, {})).get("domain", "unassigned"), "未定"),
         "mode": "word" if z in lx_by_zh else "char",
         "by_group": {g: morph_group.get(g, {}).get(z, 0) for g in GROUP_ORDER},
         "total": tok_total.get(z, 0)}
        for z in top40
    ]

    n_tok = sum(tok_total.values())
    n_un = sum(unsegmented.values())
    n_char = sum(char_total.values())

    # ── L.100：domain=unassigned 三类拆分（防「为凑 0 而臆造域」）──
    # ① lexeme 型：已注册为多字专名/音译，注册目的即防逐字强析 → **按设计不可析**
    # ② 不可归域型：词素带 unresolved_glyph 标记 → 已考订而字义不可判读
    # ③ 待归域型：其余 → **真正的待办积压**
    unass_total = unass_lex = unass_glyph = 0
    unass_lex_c: collections.Counter = collections.Counter()
    unass_glyph_c: collections.Counter = collections.Counter()
    unass_backlog_c: collections.Counter = collections.Counter()
    for z, n in tok_total.items():
        e = lex.get(z) or lx_by_zh.get(z) or {}
        if e.get("domain", "unassigned") != "unassigned":
            continue
        unass_total += n
        if z in lx_by_zh:
            unass_lex += n
            unass_lex_c[z] += n
        elif e.get("unresolved_glyph"):
            unass_glyph += n
            unass_glyph_c[z] += n
        else:
            unass_backlog_c[z] += n
    unass_backlog = sum(unass_backlog_c.values())

    # ── 群组纵深：群级钻取 + 群间对比 ──
    dom_of = {z: (lex.get(z) or lx_by_zh.get(z, {})).get("domain", "unassigned")
              for z in tok_total}
    group_profiles, group_pairs = _build_group_profiles(
        GROUP_ORDER, GROUP_ZH, GROUP_EN, n_by_group, classes_by_group,
        tok_by_group, dom_by_group, head_by_group, tailch_by_group,
        wordhit_by_group, lowconf_by_group, medconf_by_group, nchars_by_group, len_by_group,
        class_tails_derived, (lexraw.get("group_profiles") or {}), dom_of,
    )

    out: Dict[str, Any] = {
        "article": asm.get("article", "shizhu-miaoyan"),
        "source": asm.get("source", ""),
        "source_url": "https://cbetaonline.dila.edu.tw/zh/T10n0279",
        "generated_by": "scripts/miaoyan_eda.py（源：miaoyan_assembly.yaml + miaoyan_eda_lexicon.yaml）",
        "method": {
            "segmentation": "两段切分：先按多字词（lexemes 段）最长匹配，未命中者再逐字（morphemes 段）",
            "segmentation_alt": "另存纯逐字切分结果于各成员 segs_char_only，供两法互校",
            "caveat": "〔析构·待考〕切分是本工具的**方法选择**，非经文原貌。词级切分以本项目词素表所收词为限，未收之词仍退化为逐字，故覆盖率非绝对上限。",
            "domain_assignment": "语义域取自人工编纂词素表 miaoyan_eda_lexicon.yaml；每词素只归一域，不并列多义，故热力图为**单一判读视角**下的分布，不等于该字在本品中的全部义项。",
            "class_tail": "名号之「类尾」逐类**由该类成员自身派生**（「主X神」类只剥末字「神」，其余取成员最长公共后缀），剥离后得「核名」；「主X神」类**保留「主X」**，因其「主」为句式标记而非可弃之尾缀（见 zhu_formula 段）。逐类派生结果见 class_tails_derived 段，可据以复算。",
            "n_named_caveat": "n_named 为经文明列成员数，**不等于**该类众数（后者经文作「微塵數／無量」）。",
            "unassigned_caveat": "未入表之字计入 unsegmented，前端标〔待补词素〕；**不臆补其义**。梵天／八部音译名（「那羅延」「因陀羅」「毘沙門」「迦樓羅」等）多归 unassigned，非表示无义，而表示不宜逐字强析。",
            "editors_view": "本节全部统计为编辑性分析，**非经文自述**；引用时须连同本 method 一并标注。",
        },
        "domains": [
            {"key": d, "zh": DOMAIN_ZH[d], "en": DOMAIN_EN[d], "color": DOMAIN_COLOR[d],
             "n": dom_total.get(d, 0)}
            for d in DOMAIN_ORDER
        ],
        "groups": [
            {"key": g, "zh": GROUP_ZH[g], "en": GROUP_EN[g], "n": n_by_group.get(g, 0),
             "len_hist": {str(k): v for k, v in sorted(len_by_group[g].items())},
             "top_domains": [{"domain": d, "domain_zh": DOMAIN_ZH[d], "n": n}
                             for d, n in dom_by_group[g].most_common(6)]}
            for g in GROUP_ORDER
        ],
        "metrics": {
            "classes": len(per_class),
            "named_total": sum(c["n_named"] for c in per_class),
            "tokens_total": n_tok,
            "tokens_char_only": n_char,
            "word_hits": sum(word_hits.values()),
            "distinct_tokens": len(tok_total),
            "morphemes_lexicon": len(lex),
            "lexemes_lexicon": len(lexemes),
            "class_tails": len(class_tails_derived),
            "n_no_core": n_no_core,
            "coverage_pct": round(100.0 * n_tok / max(1, n_tok + n_un), 2),
            "unsegmented_chars": n_un,
            "unsegmented_distinct": len(unsegmented),
            "unassigned_segs": unass_total,
            "unassigned_lexeme_segs": unass_lex,
            "unassigned_unresolved_glyph_segs": unass_glyph,
            "unassigned_backlog_segs": unass_backlog,
            "lexicon_unused": len([z for z in lex if z not in char_total]),
            "lowconf_hits": sum(lowconf_hits.values()),
            "medconf_hits": sum(medconf_hits.values()),
            "tail_hist": dict(tail_total.most_common()),
            "pair_edges": len(lexedges),
            "core_duplicates": len(dup_cores),
            "epithet_shared": len(dup_epithets),
            "epithet_members": n_epithet_members,
            "zhu_classes": len(zhu_formula),
            "zhu_members": sum(z["n_formula"] for z in zhu_formula),
        },
        "zhu_formula": {
            "note": "十九类神可分两型：**后十五类「主X神」无一例外**（150/150 名）皆作「〔形容〕主〔所主〕神」——「主」为**句式标记**（非尊称、非语义成分），标示该类众之所主，故其名非自由命名，而是同一模子的填空；前四类（執金剛神·身眾神·足行神·道場神）则不作「主X」式，而为「〔属性〕神」尾缀型。四类造型神与十五类主X神并列，正合「异生众·十九类神」之数。",
            "note_en": "The nineteen deity classes split into two patterns. The last fifteen 「主X神」 classes follow the formula 〔epithet〕主〔domain〕神 without exception (150 of 150 named members) — 主 is a grammatical marker of the governed domain, not a title, so these names are not free naming but fill-in-the-blank of one mould. The first four (執金剛神, 身眾神, 足行神, 道場神) do not take the 主X form but are 〔attribute〕神 suffix types. Four form-deity classes plus fifteen 主X神 classes together make up the nineteen classes of the 異生眾.",
            "classes": zhu_formula,
        },
        "heat_matrix": heat,
        "group_profiles": group_profiles,
        "group_pairs": group_pairs,
        "morph_matrix": morph_matrix,
        "morph_freq": [
            {"zh": z, "n": n,
             "domain": (lex.get(z) or lx_by_zh.get(z, {})).get("domain", "unassigned"),
             "domain_zh": DOMAIN_ZH.get((lex.get(z) or lx_by_zh.get(z, {})).get("domain", "unassigned"), "未定"),
             "c": (lex.get(z) or lx_by_zh.get(z, {})).get("c", "low"),
             "mode": "word" if z in lx_by_zh else "char",
             "n_char_only": char_total.get(z, 0),
             "gloss": (lex.get(z) or lx_by_zh.get(z, {})).get("gloss", ""),
             "gloss_en": (lex.get(z) or lx_by_zh.get(z, {})).get("gloss_en", "")}
            for z, n in tok_total.most_common()
        ],
        "word_hits": [
            {"zh": z, "n": n, "domain": lx_by_zh[z].get("domain", "unassigned"),
             "domain_zh": DOMAIN_ZH.get(lx_by_zh[z].get("domain", "unassigned"), "未定"),
             "gloss": lx_by_zh[z].get("gloss", "")}
            for z, n in word_hits.most_common()
        ],
        "head_freq": [{"zh": z, "n": n} for z, n in head_total.most_common()],
        "tailch_freq": [{"zh": z, "n": n} for z, n in tailch_total.most_common(60)],
        "pair_freq": [
            {"a": a, "b": b, "n": n, "word": a + b,
             "by_group": {g: pair_by_group[g].get((a, b), 0) for g in GROUP_ORDER}}
            for (a, b), n in pair_total.most_common(120)
        ],
        "collocations": lexraw.get("collocations", []) or [],
        "lexemes": lexemes,
        "class_tails": lexraw.get("class_tails", []) or [],
        "class_tails_derived": class_tails_derived,
        "glyph_variants": glyph_stats,
        "core_duplicates": dup_cores,
        "epithet_sharing": {
            "note": "「主X神」之名作「〔赞词〕主〔所主〕神」。核名含所主槽，故**同一赞词配不同所主**者（如「大光普照主火」与「大光普照主風」）核名相异，上一节「跨类重名」按整核比较，**结构上测不到**。故另测此项：剥去「主X」槽后比较前半赞词。凡十九类神之外者不具此句式，不入此项。",
            "note_en": "Names in the 「主X神」 classes take the form 〔epithet〕主〔domain〕神. Because the core retains the domain slot, members sharing an epithet but governing different domains (e.g. 「大光普照主火」 vs 「大光普照主風」) have distinct cores and are structurally invisible to whole-core cross-class comparison. This metric therefore compares the epithet alone, after removing the 主X slot. Members outside the nineteen deity classes lack this pattern and are excluded. Each entry records only the class and the governed domain — member names are sutra fact and are held solely by the assembly.",
            "n_members_parsed": n_epithet_members,
            "groups": dup_epithets,
        },
        "unsegmented": [
            {"zh": z, "n": n, "note": lex.get(z, {}).get("note", "未入词素表〔待补〕")}
            for z, n in unsegmented.most_common()
        ],
        "unassigned_breakdown": {
            "note": "「domain=unassigned」**不是单一性质的积压**，须分三类读（见 metrics 四项计数）："
                    "① **专名／音译型**——已注册为多字 lexeme（如「因陀羅」「那羅延」「普賢」「毘樓博叉」），"
                    "注册目的正是阻止逐字强析，故其 unassigned 是**设计结果而非待办**，强行归域反属臆造；"
                    "② **不可归域型**——底本罕字，字义在现有底本与字书内不可判读（带 unresolved_glyph 标记，"
                    "如「𪗇」「㵎」），已考订而止步于此；"
                    "③ **待归域型**——前两类之外者，方为真正可推进的积压。"
                    "三者皆不得为凑「unassigned→0」而强并。",
            "note_en": "'unassigned' is not a single kind of backlog and must be read in three classes: "
                       "(1) proper names and transliterations registered as multi-character lexemes — their "
                       "unassigned status is by design, since registration exists precisely to prevent "
                       "character-by-character forcing; (2) base-text obscure glyphs whose meaning cannot be "
                       "determined from the available text or dictionaries (flagged unresolved_glyph); "
                       "(3) everything else, the only genuinely actionable backlog. None of the three may be "
                       "collapsed merely to drive 'unassigned' toward zero.",
            "lexeme": [{"zh": z, "n": n} for z, n in unass_lex_c.most_common()],
            "unresolved_glyph": [{"zh": z, "n": n,
                                  "note": (lex.get(z) or {}).get("note", "")}
                                 for z, n in unass_glyph_c.most_common()],
            "backlog": [{"zh": z, "n": n} for z, n in unass_backlog_c.most_common()],
        },
        "lexicon_notes": lexraw.get("notes", []) or [],
        "graph": {
            "lex_nodes": lexnodes,
            "lex_edges": lexedges,
            "class_nodes": classnodes,
            "bipartite_edges": binedges,
        },
        "classes": per_class,
    }
    return out


def dump_yaml(data: Any, path: str) -> int:
    txt = yaml.safe_dump(data, allow_unicode=True, sort_keys=False,
                         default_flow_style=False, width=100)
    with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("# 由 scripts/miaoyan_eda.py 自动生成，勿手改\n")
        fh.write("# 源：data/translation/miaoyan_assembly.yaml ＋ data/translation/miaoyan_eda_lexicon.yaml\n")
        fh.write("# 校验：python scripts/miaoyan_eda.py --check\n")
        fh.write("# ⚠ 本文件含编辑性析构分析（见 method 段），非经文自述数据。\n")
        fh.write(txt)
    return os.path.getsize(path)


def do_check(data: Dict[str, Any]) -> List[str]:
    errs: List[str] = []
    m = data["metrics"]
    asm_total = 414
    if m["classes"] != 40:
        errs.append("类数应为 40，实为 %d" % m["classes"])
    if m["named_total"] != asm_total:
        errs.append("成员总数应为 %d，实为 %d" % (asm_total, m["named_total"]))
    n_sum = sum(len(c["members"]) for c in data["classes"])
    if n_sum != m["named_total"]:
        errs.append("逐类成员数之和 %d ≠ named_total %d" % (n_sum, m["named_total"]))
    for c in data["classes"]:
        if c["n_named"] != len(c["members"]):
            errs.append("类 %s：n_named %d ≠ members %d" % (c["cat"], c["n_named"], len(c["members"])))
        if not c["members"]:
            errs.append("类 %s 无成员" % c["cat"])
        else:
            if sum(c["members"][0]["is_leader"] for _ in [0]) != 1 and c["members"][0]["is_leader"] != 1:
                errs.append("类 %s 上首标记异常" % c["cat"])
    doms = {d["key"] for d in data["domains"]}
    for d in data["heat_matrix"]:
        # 域占比的分母为该群词素位数，故各域 pct 之和须≈100（舍入容差 1.5）
        s = sum(c["pct"] for c in d["cells"])
        if d["n_tokens"] and abs(s - 100.0) > 1.5:
            errs.append("热力图群 %s 各域 pct 合计 %.1f%%（应≈100%%，分母疑用错）" % (d["group"], s))
        for c in d["cells"]:
            if not (0 <= c["pct"] <= 100):
                errs.append("热力图群 %s 域 %s pct=%s 越界" % (d["group"], c["domain"], c["pct"]))
    for gp in data.get("group_profiles") or []:
        if gp["n_classes"] > gp["n_named"]:
            errs.append("群 %s 类数 %d > 明列名数 %d" % (gp["key"], gp["n_classes"], gp["n_named"]))
        s = sum(d["pct"] for d in gp["domains"])
        if gp["n_tokens"] and abs(s - 100.0) > 1.5:
            errs.append("群 %s 各域 pct 合计 %.1f%%（应≈100%%）" % (gp["key"], s))
        if len(gp["classes"]) != gp["n_classes"]:
            errs.append("群 %s classes 列表 %d 条 ≠ n_classes %d"
                        % (gp["key"], len(gp["classes"]), gp["n_classes"]))
    if len(data.get("group_pairs") or []) != 10:
        errs.append("群间对比 %d 对 ≠ C(5,2)=10" % len(data.get("group_pairs") or []))
    if not (0 < m["coverage_pct"] <= 100):
        errs.append("覆盖率异常：%s" % m["coverage_pct"])
    for d in data["domains"]:
        if d["key"] not in DOMAIN_ORDER:
            errs.append("域 %s 不在 DOMAIN_ORDER" % d["key"])
    # ── L.100：unassigned 三类拆分必须自洽（详见 unassigned_breakdown）──
    ub = data.get("unassigned_breakdown") or {}
    n_lx = sum(x["n"] for x in ub.get("lexeme") or [])
    n_ug = sum(x["n"] for x in ub.get("unresolved_glyph") or [])
    n_bl = sum(x["n"] for x in ub.get("backlog") or [])
    if m.get("unassigned_segs") != n_lx + n_ug + n_bl:
        errs.append("unassigned 拆分类 %d+%d+%d ≠ unassigned_segs %s"
                    % (n_lx, n_ug, n_bl, m.get("unassigned_segs")))
    for key, val in (("unassigned_lexeme_segs", n_lx),
                     ("unassigned_unresolved_glyph_segs", n_ug),
                     ("unassigned_backlog_segs", n_bl)):
        if m.get(key) != val:
            errs.append("metrics.%s=%s ≠ 明细之和 %d" % (key, m.get(key), val))
    # 三类不得重叠：同一词素不得同时出现在两类清单中
    zs_lx = {x["zh"] for x in ub.get("lexeme") or []}
    zs_ug = {x["zh"] for x in ub.get("unresolved_glyph") or []}
    zs_bl = {x["zh"] for x in ub.get("backlog") or []}
    if zs_lx & zs_ug or zs_lx & zs_bl or zs_ug & zs_bl:
        errs.append("unassigned 三类清单存在重叠：%s"
                    % (sorted((zs_lx & zs_ug) | (zs_lx & zs_bl) | (zs_ug & zs_bl))))
    # 防臆造护栏：带 unresolved_glyph 标记者不得同时被归入任何语义域
    for x in ub.get("unresolved_glyph") or []:
        e = next((mm for mm in data.get("morph_freq") or []
                  if mm.get("zh") == x["zh"]), None)
        if e and e.get("domain") not in (None, "", "unassigned"):
            errs.append("罕字「%s」已标记 unresolved_glyph，却又归入域 %s——"
                        "属为凑 0 而臆造语义域" % (x["zh"], e.get("domain")))
    # 切分自洽：词级切分会把「金剛」等合并为 1 位，故 tokens_total ≤ tokens_char_only
    if m["tokens_total"] > m["tokens_char_only"]:
        errs.append("两段切分位 %d > 纯逐字位 %d，逻辑矛盾"
                    % (m["tokens_total"], m["tokens_char_only"]))
    if m["unsegmented_chars"] > m["tokens_char_only"]:
        errs.append("待补字次 %d > 纯逐字位 %d，逻辑矛盾"
                    % (m["unsegmented_chars"], m["tokens_char_only"]))
    n_core_chars = sum(c["n_char_total"] for c in data["classes"])
    if m["tokens_char_only"] + m["unsegmented_chars"] != n_core_chars:
        errs.append("纯逐字位 %d + 待补 %d ≠ 核名总字数 %d"
                    % (m["tokens_char_only"], m["unsegmented_chars"], n_core_chars))
    n_word = sum(m["n_word"] for c in data["classes"] for m in c["members"])
    if n_word != m["word_hits"]:
        errs.append("类内多字词命中合计 %d ≠ word_hits %d" % (n_word, m["word_hits"]))
    # 每类上首须恰有一位
    for c in data["classes"]:
        if sum(m["is_leader"] for m in c["members"]) != 1:
            errs.append("类 %s 上首标记数 %d ≠ 1"
                        % (c["cat"], sum(m["is_leader"] for m in c["members"])))
    # 词素频次总量须等于 classes 内统计之和
    s = sum(mt["n"] for mt in data["morph_freq"])
    if s != m["tokens_total"]:
        errs.append("morph_freq 合计 %d ≠ tokens_total %d" % (s, m["tokens_total"]))

    # 置信度三级须互斥且穷尽：low + med ≤ tokens_total，且逐成员统计与之相符。
    # 旧版 lowconf_hits 曾把 low 与 medium 合并计数，与 schema 及页面「low 者须标〔待考〕」
    # 之约不符；故三级分列并加此不变量，令口径失实无处可藏。
    n_low = m.get("lowconf_hits", 0)
    n_med = m.get("medconf_hits", 0)
    if n_low + n_med > m["tokens_total"]:
        errs.append("low %d + med %d > tokens_total %d（三级非互斥？）"
                    % (n_low, n_med, m["tokens_total"]))
    seg_low = seg_med = 0
    for c in data["classes"]:
        for mem in c["members"]:
            for sg in mem.get("segs") or []:
                if sg.get("c") == "low":
                    seg_low += 1
                elif sg.get("c") == "medium":
                    seg_med += 1
    if (seg_low, seg_med) != (n_low, n_med):
        errs.append("逐成员 confidence 统计 low/med = %d/%d ≠ metrics %d/%d"
                    % (seg_low, seg_med, n_low, n_med))
    for gp in data.get("group_profiles") or []:
        gl = gp.get("n_lowconf", 0)
        gm = gp.get("n_medconf")
        if gm is None:
            errs.append("群 %s 缺 n_medconf" % gp.get("key"))
        elif gl + gm > gp.get("n_tokens", 0):
            errs.append("群 %s low %d + med %d > n_tokens %d"
                        % (gp.get("key"), gl, gm, gp.get("n_tokens")))
    if sum(g.get("n_lowconf", 0) for g in data.get("group_profiles") or []) != n_low:
        errs.append("各群 n_lowconf 之和 ≠ metrics.lowconf_hits")
    # 「主X神」两型论断：命中类必为十九类神之后十五类，且各类须 100% 合式。
    # 该论断已写入 zhu_formula.note，故在此加不变量防止改数据时注文与统计脱节。
    zf = data["zhu_formula"]["classes"]
    n_deity = sum(c["n_named"] for c in data["classes"] if c["group"] == "deities")
    if n_deity != 190:
        errs.append("神类成员合计 %d ≠ 190" % n_deity)
    if len(zf) != 15:
        errs.append("「主X神」命中类数 %d ≠ 15" % len(zf))
    for c in zf:
        if c["pct"] != 100.0 or c["n_formula"] != c["n_named"]:
            errs.append("类 %s 「主X神」合式率 %s%%（%d/%d），注文称无一例外"
                        % (c["cat"], c["pct"], c["n_formula"], c["n_named"]))
    if sum(c["n_formula"] for c in zf) != 150:
        errs.append("「主X神」合式名合计 %d ≠ 150" % sum(c["n_formula"] for c in zf))
    # 前四类造型神不得被误判为「主X神」式
    for c in data["classes"]:
        if c["group"] == "deities" and not c["cat"].startswith("主"):
            if c["cat"] in {z["cat"] for z in zf}:
                errs.append("非「主」字类 %s 被计入「主X神」" % c["cat"])
    # 类尾须逐类派生得非空值，且实际剥除率须可解释（少数整名即类名者为 0）
    ctd = data.get("class_tails_derived") or []
    if len(ctd) != len(data["classes"]):
        errs.append("class_tails_derived %d 条 ≠ 类数 %d" % (len(ctd), len(data["classes"])))
    for t in ctd:
        if not t.get("tail"):
            errs.append("类 %s 派生类尾为空" % t["cat"])
        if t["n_tailed"] + t["n_no_core"] != t["n_members"]:
            errs.append("类 %s tailed %d + no_core %d ≠ members %d"
                        % (t["cat"], t["n_tailed"], t["n_no_core"], t["n_members"]))
        if t["rule"] == "zhu-keep" and t["tail"] != "神":
            errs.append("类 %s 标 zhu-keep 却不只剥「神」（tail=%s）" % (t["cat"], t["tail"]))
    if m.get("n_no_core") != sum(t["n_no_core"] for t in ctd):
        errs.append("n_no_core %d ≠ 各类 no_core 之和 %d"
                    % (m.get("n_no_core"), sum(t["n_no_core"] for t in ctd)))

    # 「跨类同赞词」不变量
    ep = data.get("epithet_sharing") or {}
    n_parsed = ep.get("n_members_parsed", 0)
    if n_parsed != 150:
        errs.append("epithet 可析名 %d ≠ 150（十九类神全体）" % n_parsed)
    for g in ep.get("groups") or []:
        if g["n"] != len(g["members"]):
            errs.append("赞词「%s」n=%d ≠ members %d" % (g["epithet"], g["n"], len(g["members"])))
        if len(set(g["classes"])) < 2:
            errs.append("赞词「%s」仅一类，不应列于跨类共用" % g["epithet"])
        if len(set(g["classes"])) != g["n"]:
            errs.append("赞词「%s」跨 %d 类却 n=%d（应一名一类）"
                        % (g["epithet"], len(set(g["classes"])), g["n"]))
    if m.get("epithet_shared") != len(ep.get("groups") or []):
        errs.append("metrics.epithet_shared %s ≠ groups %d"
                    % (m.get("epithet_shared"), len(ep.get("groups") or [])))
    if m.get("epithet_members") != n_parsed:
        errs.append("metrics.epithet_members %s ≠ n_members_parsed %d"
                    % (m.get("epithet_members"), n_parsed))
    return errs


def summary(data: Dict[str, Any]) -> str:
    m = data["metrics"]
    L: List[str] = []
    L.append("═══ 世主妙严品·会众名号构词法 EDA ═══")
    L.append("类 %d ／ 名 %d ／ 词素位 %d（纯逐字对照 %d）"
             % (m["classes"], m["named_total"], m["tokens_total"], m["tokens_char_only"]))
    L.append("入表 %d 种（词素 %d／多字词 %d）　覆盖率 %.1f%%　待补 %d 字次（%d 种）"
             % (m["distinct_tokens"], m["morphemes_lexicon"], m["lexemes_lexicon"],
                m["coverage_pct"], m["unsegmented_chars"], m["unsegmented_distinct"]))
    L.append("类尾剥离：" + "  ".join("%s×%d" % (k or "（无）", v)
                                     for k, v in m["tail_hist"].items()))
    L.append("")
    L.append("── 语义域分布 ──")
    tot = sum(d["n"] for d in data["domains"]) or 1
    for d in data["domains"]:
        if not d["n"]:
            continue
        L.append("  %-11s %-10s %5d  %5.1f%%  %s"
                 % (d["key"], d["zh"], d["n"], 100.0 * d["n"] / tot,
                    "█" * int(round(40.0 * d["n"] / tot))))
    L.append("")
    L.append("── 各类群主导域 ──")
    for g in data["groups"]:
        if not g["n"]:
            continue
        top = "、".join("%s(%d)" % (t["domain_zh"], t["n"]) for t in g["top_domains"][:4])
        L.append("  %-12s n=%3d  %s" % (g["zh"], g["n"], top))
    L.append("")
    L.append("── 「主X神」句式 ──")
    z = data["zhu_formula"]
    L.append("  命中 %d 类 / %d 名（神类 190 名中占 %.1f%%；全 414 名中占 %.1f%%）"
             % (m["zhu_classes"], m["zhu_members"],
                100.0 * m["zhu_members"] / 190.0,
                100.0 * m["zhu_members"] / m["named_total"]))
    for c in z["classes"][:4]:
        L.append("    %-8s %d/%d 名（%s%%）所主：%s"
                 % (c["cat"], c["n_formula"], c["n_named"], c["pct"],
                    "、".join("%s×%d" % (o, n) for o, n in c["objects"][:3])))
    L.append("")
    L.append("── 冠字（核名首字）前 20 ──")
    L.append("  " + "  ".join("%s%d" % (h["zh"], h["n"]) for h in data["head_freq"][:20]))
    L.append("")
    L.append("── 多字词命中前 15 ──")
    L.append("  " + "  ".join("%s×%d" % (w["zh"], w["n"]) for w in data["word_hits"][:15]))
    L.append("")
    L.append("── 高频相邻组前 25 ──")
    L.append("  " + "  ".join("%s×%d" % (p["word"], p["n"]) for p in data["pair_freq"][:25]))
    L.append("")
    L.append("── 跨类同核名 ──")
    if data["core_duplicates"]:
        for d in data["core_duplicates"]:
            L.append("  「%s」 → %s" % (d["core"], "、".join(d["classes"])))
    else:
        L.append("  （无）")
    L.append("")
    L.append("── 跨类同赞词（「主X神」剥所主槽后）──")
    ep = data["epithet_sharing"]
    L.append("  可析 %d 名（十九类神 150 名中占 %.1f%%），跨类共用 %d 组"
             % (ep["n_members_parsed"],
                100.0 * ep["n_members_parsed"] / 150.0,
                len(ep["groups"])))
    for d in ep["groups"]:
        L.append("  「%s」 ×%d → %s" % (d["epithet"], d["n"], "、".join(d["classes"])))
    L.append("")
    L.append("── 异体字（CBETA 原字形保留）──")
    for g in data["glyph_variants"]:
        L.append("  %s(%d) ／ %s(%d)"
                 % (g["cbeta"], g["n_cbeta"], g["common"], g["n_common"]))
    L.append("")
    L.append("── 待补词素（未入表，前 15）──")
    for u in data["unsegmented"][:15]:
        L.append("  %s ×%d" % (u["zh"], u["n"]))
    return "\n".join(L)


def main() -> int:
    ap = argparse.ArgumentParser(description="世主妙严品会众名号构词法 EDA")
    ap.add_argument("--check", action="store_true", help="只校验不写文件")
    ap.add_argument("--print", dest="do_print", action="store_true", help="打印统计摘要")
    a = ap.parse_args()

    if not os.path.exists(ASSEMBLY):
        sys.stderr.write("缺源文件：%s\n" % ASSEMBLY)
        return 2
    if not os.path.exists(LEXICON):
        sys.stderr.write("缺词素表：%s\n" % LEXICON)
        return 2

    asm = _load(ASSEMBLY)
    lexraw = _load(LEXICON)
    data = analyse(asm, lexraw)
    errs = do_check(data)
    if errs:
        print("✗ 校验未过：")
        for e in errs:
            print("   - " + e)
        return 1

    if a.do_print:
        print(summary(data))

    if a.check:
        print("✓ --check 通过：类 %d／名 %d／覆盖率 %.1f%%"
              % (data["metrics"]["classes"], data["metrics"]["named_total"],
                 data["metrics"]["coverage_pct"]))
        return 0

    size = dump_yaml(data, EDA_OUT)
    print("✓ 已生成 %s（%s 字节，%.1f KB）" % (os.path.relpath(EDA_OUT, ROOT), size, size / 1024.0))
    print("  类 %d ／ 名 %d ／ 词素位 %d ／ 覆盖率 %.1f%% ／ 待补字次 %d"
          % (data["metrics"]["classes"], data["metrics"]["named_total"],
             data["metrics"]["tokens_total"], data["metrics"]["coverage_pct"],
             data["metrics"]["unsegmented_chars"]))
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
