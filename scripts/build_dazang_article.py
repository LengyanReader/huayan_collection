#!/usr/bin/env python3
"""Generate data-driven tables and SVG figures for the canon-mapping article.

Usage:
  python scripts/build_dazang_article.py

It reads data/research/dazang_mapping_verification.json and replaces
<!--GEN:...--> placeholders in docs/经学文献/华严经与大藏经对应研究.md.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from build_dazang_graph import build_graph, render_citations, render_radial, render_spine
from build_conflation_probe import EXTRA_TITLES

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "research" / "dazang_mapping_verification.json"
ENRICH = ROOT / "data" / "research" / "dazang_enrichment.json"
REGISTRY = ROOT / "data" / "research" / "canon_registry.json"
ONTOLOGY = ROOT / "data" / "research" / "relation_ontology.json"
PROBES = ROOT / "data" / "research" / "cross_canon_probes.json"
IMPLICIT = ROOT / "data" / "research" / "implicit_quotes.json"
PARAPHRASE = ROOT / "data" / "research" / "paraphrase_probe.json"
CONFLATION = ROOT / "data" / "research" / "conflation_probe.json"
ENDGAME = ROOT / "data" / "research" / "endgame_probe.json"
PAIR60 = ROOT / "data" / "research" / "huayan_80_60_pairwise.json"
PAIR40 = ROOT / "data" / "research" / "huayan_80_40_pairwise.json"
ARTICLE = ROOT / "docs" / "经学文献" / "华严经与大藏经对应研究.md"

INK = "#2b2b2b"
MUTED = "#666666"
LINE = "#d8d0c0"
PAPER = "#fbf8f1"
BROWN = "#8b5e34"
RED = "#b03a2e"
BLUE = "#2f5d7c"
GREEN = "#4f6f52"
GOLD = "#a87900"
LIGHT = "#efe9dc"

ROLE_MAIN = {"T09n0278", "T10n0279", "T10n0293"}
CLUSTER = {
    "T10n0280": "名号·光明觉", "T10n0281": "净行／十住", "T10n0282": "净行",
    "T10n0283": "十住", "T10n0284": "十住", "T10n0285": "十地", "T10n0286": "十地",
    "T10n0287": "十地", "T10n0288": "十定", "T10n0289": "寿量", "T10n0290": "寿量",
    "T10n0291": "如来出现", "T10n0292": "离世间", "T10n0293": "入法界",
    "T10n0294": "入法界", "T10n0295": "入法界", "T10n0296": "普贤行愿",
    "T10n0297": "普贤行愿", "T10n0298": "普贤宣说（藏32）", "T10n0299": "十住／贤首（总持）",
    "T10n0300": "佛不思议", "T10n0301": "佛不思议", "T10n0302": "如来出现",
    "T10n0303": "如来出现", "T10n0304": "如来出现", "T10n0305": "信力入印",
    "T10n0306": "修慈", "T10n0307": "十地", "T10n0308": "十地", "T10n0309": "十住〔待核〕",
}

SHORT = {
    "T10n0280": "支娄迦谶", "T10n0281": "支谦", "T10n0282": "聂道真", "T10n0283": "竺法护",
    "T10n0284": "祇多蜜", "T10n0285": "竺法护", "T10n0286": "鸠摩罗什", "T10n0287": "尸罗达摩",
    "T10n0288": "竺法护", "T10n0289": "玄奘", "T10n0290": "法贤", "T10n0291": "竺法护",
    "T10n0292": "竺法护", "T10n0293": "般若", "T10n0294": "圣坚", "T10n0295": "地婆诃罗",
    "T10n0296": "佛陀跋陀罗", "T10n0297": "不空", "T10n0298": "实叉难陀", "T10n0299": "法天",
    "T10n0300": "提云般若", "T10n0301": "实叉难陀", "T10n0302": "失译", "T10n0303": "阇那崛多",
    "T10n0304": "实叉难陀", "T10n0305": "昙摩流支", "T10n0306": "提云般若", "T10n0307": "鸠摩罗什",
    "T10n0308": "吉迦夜", "T10n0309": "竺佛念",
}

CLUSTERS = [
    ("名号·光明觉", "7、9", "12、14", "T280；T281 序品", "A"),
    ("净行", "11", "16", "T282；T281 愿行品", "A"),
    ("十住", "15", "20", "T283、T284；T281 第三章", "A"),
    ("十地", "26", "31", "T285、T286、T287", "A"),
    ("十定", "27", "33", "T288", "A"),
    ("寿量", "31", "37", "T289、T290", "A"),
    ("佛不思议", "33", "39", "汉无；Toh 187", "A（藏）／C（汉）"),
    ("普贤行愿", "36、40 卷末", "42、45 末", "T293 卷40、T296、T297", "A"),
    ("如来出现", "37", "43", "T291", "A"),
    ("离世间", "38", "44", "T292", "A"),
    ("入法界", "39", "45", "T293、T294、T295", "A"),
    ("其余 27 品", "1–6、8、10、12–14、16–25、28–30、32、34、35", "见 §2.3", "无单独汉译", "A"),
]

DASHABHUMIKA = [
    ("T285 渐备一切智德经", "竺法护", 5, 52999, "离群", "0.11–0.12"),
    ("T286 十住经", "鸠摩罗什", 4, 47188, "与 T278 一簇", "0.69"),
    ("T278 六十·品22", "佛陀跋陀罗", 60, 42390, "与 T286 一簇", "0.69"),
    ("T279 八十·品26", "实叉难陀", 80, 43413, "与 T287 一簇", "0.43"),
    ("T287 佛说十地经", "尸罗达摩", 9, 54427, "与 T279 一簇", "0.43"),
]

ASSEMBLIES = [
    ("初会", "菩提场", "1–6", "1–11", 11),
    ("二会", "普光明殿", "7–12", "12–15", 4),
    ("三会", "忉利天", "13–18", "16–18", 3),
    ("四会", "夜摩天", "19–22", "19–21", 3),
    ("五会", "兜率天", "23–25", "22–33", 12),
    ("六会", "他化自在天", "26", "34–39", 6),
    ("七会", "重会普光明殿", "27–37", "40–52", 13),
    ("八会", "三会普光明殿", "38", "53–59", 7),
    ("九会", "逝多林", "39", "60–80", 21),
]

RANGE_DEPTH = {
    "1": "义理", "152": "线索", "220": "文本", "262": "义理", "278": "核实",
    "310": "线索", "374": "引文", "397": "未做", "425": "引文", "848": "核实",
    "1421": "引文", "1505": "核实", "1536": "引文", "1564": "引文", "1579": "引文",
    "1628": "引文", "1693": "核实", "1804": "未做", "1816": "线索", "1851": "核实",
    "2026": "核实", "2121": "未做", "2137": "线索", "2145": "核实",
    "2185": "线索", "2701": "线索", "2732": "线索", "2865": "线索",
}
DEPTH_COLOR = {"核实": GREEN, "文本": BLUE, "引文": "#7a6a9a", "义理": GOLD, "线索": "#b08a6a", "未做": "#bbb"}


def esc(s: str) -> str:
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace("|", "／"))


def txt(x, y, s, size=12, fill=INK, anchor="start", weight="normal", family="'Noto Serif SC','Songti SC',serif"):
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" '
            f'font-weight="{weight}" font-family="{family}">{esc(s)}</text>')


def rect(x, y, w, h, fill="none", stroke=LINE, rx=4, sw=1, op=1):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="{sw}" opacity="{op}"/>')


def line(x1, y1, x2, y2, stroke=LINE, sw=1, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}"{d}/>'


def svg(w, h, title, desc, body):
    return (f'<svg viewBox="0 0 {w} {h}" width="100%" role="img" aria-labelledby="t" '
            f'xmlns="http://www.w3.org/2000/svg" style="max-width:{w}px;margin:1.2rem auto;display:block">'
            f'<title>{esc(title)}</title><desc>{esc(desc)}</desc>'
            f'<rect width="{w}" height="{h}" fill="{PAPER}" rx="8"/>' + body + "</svg>")


def fig_layers():
    b = []
    layers = [
        ("一 同经异本", "T278 / T279 / T293 / Toh 44 / 梵本残存", 24),
        ("二 别生经", "T280–T297 单行异译", 52),
        ("三 论释与注疏", "T1521 / T1522 / T1731–T1742 / X221", 80),
        ("四 义理层", "判教 · 阶位 · 年代 · 影响", 108),
        ("五 版本与检索", "九种汉文藏 · 德格 · CBETA / SAT / 84000", 136),
    ]
    for i, (name, sub, y) in enumerate(layers):
        b.append(rect(40 + i * 14, 36 + i * 46, 680 - i * 28, 74, fill="#fff", stroke=BROWN, sw=1.2))
        b.append(txt(60 + i * 14, 62 + i * 46, name, 15, BROWN, weight="bold"))
        b.append(txt(60 + i * 14, 86 + i * 46, sub, 12, MUTED))
    b.append(txt(720, 60, "由外而内：", 11, MUTED, anchor="end"))
    b.append(txt(720, 76, "越内层越需判断", 11, MUTED, anchor="end"))
    return svg(760, 320, "图1　对应的五层", "由同经异本到版本检索的五层嵌套结构", "".join(b))


def fig_catalog(data):
    b = []
    groups = [("大本", 3, BROWN), ("别生经", 17, BLUE), ("眷属经", 12, GREEN)]
    x = 60
    for name, n, color in groups:
        b.append(rect(x, 60, 190, 70, fill="#fff", stroke=color, sw=1.4))
        b.append(txt(x + 14, 88, name, 15, color, weight="bold"))
        b.append(txt(x + 14, 114, f"{n} 部", 22, INK, weight="bold"))
        x += 220
    b.append(txt(60, 160, "T278–T309 · 32 部 = 3 大本 + 17 别生经 + 12 眷属经", 12, MUTED))
    for i in range(32):
        col = i % 16
        row = i // 16
        fill = BROWN if i < 3 else (BLUE if i < 20 else GREEN)
        b.append(rect(60 + col * 40, 190 + row * 40, 32, 28, fill=fill, stroke=fill, op=0.85))
    b.append(txt(60, 306, "■ 大本（278/279/293）　■ 别生经（280–292、294–297）　■ 眷属经（298–309）", 11, MUTED))
    return svg(760, 330, "图2　华严部 32 部构成", "三十二部按大本、别生经、眷属经分类", "".join(b))


def fig_evolution(data):
    b = []
    base_y, max_h = 270, 180
    vals = [("晋译 T278", 34, "34 品 · 60 卷"), ("唐译 T279", 39, "39 品 · 80 卷"), ("藏译 Toh 44", 45, "45 章 · 115 包")]
    for i, (name, n, sub) in enumerate(vals):
        h = int(max_h * n / 45)
        x = 110 + i * 220
        b.append(rect(x, base_y - h, 90, h, fill=[BROWN, BLUE, GREEN][i], stroke="none", op=0.85))
        b.append(txt(x + 45, base_y - h - 12, str(n), 22, INK, anchor="middle", weight="bold"))
        b.append(txt(x + 45, base_y + 20, name, 13, INK, anchor="middle"))
        b.append(txt(x + 45, base_y + 38, sub, 11, MUTED, anchor="middle"))
    b.append(line(60, base_y, 700, base_y, INK, 1))
    b.append(txt(320, 44, "+4 品（卢舍那佛品分为 2–6）＋1 品（十定）＝ +5", 11, BLUE, anchor="middle"))
    b.append(txt(540, 76, "+4 章（华藏世界分为 5–9）＋2 章（藏11、藏32）＝ +6", 11, GREEN, anchor="middle"))
    return svg(760, 320, "图3　章数演化", "晋译三十四品、唐译三十九品、藏译四十五章的增减算术", "".join(b))


def fig_assemblies():
    b = []
    total = sum(a[4] for a in ASSEMBLIES)
    x0, width = 40, 820
    y = 70
    for i, (hui, place, pin, juan, n) in enumerate(ASSEMBLIES):
        w = width * n / total
        color = [BROWN, BLUE, GREEN, GOLD, "#7a6a9a", RED, "#4a7a8c", "#6b8e6b", "#8c6a4a"][i]
        b.append(rect(x0, y, max(w - 3, 18), 58, fill=color, stroke="none", op=0.9))
        b.append(txt(x0 + 6, y + 20, hui, 11, "#fff", weight="bold"))
        b.append(txt(x0 + 6, y + 36, pin, 10, "#fff"))
        b.append(txt(x0 + 6, y + 50, juan, 10, "#fff"))
        x0 += w
    b.append(txt(40, 46, "七处九会 × 品 × 卷（八十华严）", 14, INK, weight="bold"))
    b.append(txt(40, 158, "初会菩提场 1–6 品（卷1–11）→ 二会普光明殿 7–12（12–15）→ 三会忉利 13–18（16–18）→ 四会夜摩 19–22（19–21）", 10, MUTED))
    b.append(txt(40, 176, "→ 五会兜率 23–25（22–33）→ 六会他化 26（34–39）→ 七会重会 27–37（40–52）→ 八会 38（53–59）→ 九会逝多林 39（60–80）", 10, MUTED))
    return svg(900, 200, "图5　七处九会带状图", "九会按卷次比例展开，标注品次与卷次", "".join(b))


def fig_alignment(rows):
    b = []
    top, rh = 58, 16
    b.append(txt(40, 30, "八十（左）↔ 六十（右）逐品对照", 14, INK, weight="bold"))
    b.append(txt(40, 46, "五行合一：八十品2–6 合为六十品2（卢舍那佛品）；十定品无六十对应；十明＝十通", 10, MUTED))
    for i in range(1, 6):
        y = top + i * rh
        b.append(rect(300, y + 1, 300, rh - 2, fill="#f3e6d8", stroke="none", op=0.6))
    for i, r in enumerate(rows):
        y = top + i * rh
        p80, p60 = r["p80"], r["p60"]
        b.append(txt(300, y + 10, p80.replace("品", ""), 10, INK, anchor="end"))
        b.append(txt(600, y + 10, (p60 or "—").replace("品", ""), 10, MUTED if p60 else RED))
        if p60:
            b.append(line(304, y + 6, 596, y + 6, LINE, 0.8))
        else:
            b.append(line(304, y + 6, 596, y + 6, RED, 0.8, dash="3 3"))
    b.append(line(300, top - 6, 300, top + 39 * rh, BROWN, 1))
    b.append(line(600, top - 6, 600, top + 39 * rh, BROWN, 1))
    return svg(900, top + 39 * rh + 20, "图4　六十／八十逐品对照", "三十九行逐品连线，标出合并段与缺品", "".join(b))


def fig_clusters():
    b = []
    b.append(txt(40, 28, "十二簇：汉品 × 藏章 × 汉别译", 14, INK, weight="bold"))
    b.append(txt(40, 46, "粗线为同簇对应；藏章号依 84000 与本地 TOC，逐品内容仍多属〔待核〕", 10, MUTED))
    for i, (name, pin, tib, zh, grade) in enumerate(CLUSTERS):
        y = 66 + i * 30
        b.append(txt(40, y, name, 11, INK, weight="bold"))
        b.append(rect(150, y - 10, 210, 16, fill="#fff", stroke=LINE))
        b.append(txt(156, y + 2, pin, 9, BLUE))
        b.append(rect(390, y - 10, 150, 16, fill="#fff", stroke=LINE))
        b.append(txt(396, y + 2, tib, 9, GREEN))
        b.append(rect(570, y - 10, 250, 16, fill="#fff", stroke=LINE))
        b.append(txt(576, y + 2, zh, 9, BROWN))
        b.append(txt(830, y + 2, grade, 9, MUTED))
    return svg(900, 66 + 12 * 30, "图6　十二簇三线对齐", "品、藏章、汉别译三列对齐", "".join(b))


def fig_dashabhumika():
    b = []
    b.append(txt(30, 28, "十地五译：两簇一离群", 14, INK, weight="bold"))
    pos = [(80, 90), (240, 90), (160, 190), (390, 150), (520, 240)]
    for (name, tr, juan, cjkv, cluster, sim), (x, y) in zip(DASHABHUMIKA, pos):
        r = 14 + cjkv / 4000
        b.append(f'<circle cx="{x}" cy="{y}" r="{r:.1f}" fill="{BLUE}" opacity="0.82"/>')
        b.append(txt(x, y + 4, str(juan), 10, "#fff", anchor="middle", weight="bold"))
        b.append(txt(x, y + r + 14, name.split(" ")[0], 10, INK, anchor="middle"))
        b.append(txt(x, y + r + 28, f"{cjkv:,} 字", 9, MUTED, anchor="middle"))
    for (x1, y1), (x2, y2), s in [(pos[0], pos[1], "0.69"), (pos[1], pos[2], "0.69"), (pos[2], pos[3], "0.43"), (pos[3], pos[4], "0.43")]:
        b.append(line(x1, y1, x2, y2, BROWN, 1.4))
        b.append(txt((x1 + x2) / 2, (y1 + y2) / 2 - 4, s, 10, RED, anchor="middle"))
    b.append(txt(30, 300, "数字为种子报告的平均对齐相似度（B，未在本仓复算）；圆面积按 CBETA 实测 CJK 字数。", 10, MUTED))
    return svg(700, 320, "图10　十地五译亲缘", "五译的卷数、体量与两簇一离群结构", "".join(b))


def fig_sanskrit():
    b = []
    b.append(txt(40, 30, "梵本存佚：全经佚，四部单品存", 14, INK, weight="bold"))
    items = ["Daśabhūmika\n十地", "Gaṇḍavyūha\n入法界", "Bhadracaryā\n行愿", "Anantabuddha...\n寿量"]
    for i, s in enumerate(items):
        x = 60 + i * 175
        b.append(rect(x, 70, 150, 90, fill="#fff", stroke=GREEN, sw=1.4))
        for j, part in enumerate(s.split("\n")):
            b.append(txt(x + 75, 100 + j * 20, part, 11, GREEN if j == 0 else INK, anchor="middle", weight="bold" if j == 0 else "normal"))
        b.append(txt(x + 75, 148, "存", 12, GREEN, anchor="middle"))
    b.append(rect(60, 190, 660, 46, fill="#f3e6d8", stroke=RED, sw=1))
    b.append(txt(390, 218, "其余全经：梵本无存 · 仅存汉藏译本与中亚残片", 12, RED, anchor="middle"))
    return svg(780, 270, "图11　梵本存佚", "全经梵本已佚，仅四部单品存世", "".join(b))


def fig_citations():
    b = []
    b.append(txt(40, 28, "四部注疏的书名号引用（种子报告·B）", 14, INK, weight="bold"))
    vals = [("智俨·搜玄记", 95), ("法藏·探玄记", 1580), ("澄观·疏", 1667), ("澄观·钞", 4363)]
    mx = 4363
    for i, (n, v) in enumerate(vals):
        y = 60 + i * 34
        w = 420 * v / mx
        b.append(txt(40, y + 4, n, 11, INK))
        b.append(rect(180, y - 10, w, 16, fill=BLUE, stroke="none", op=0.85))
        b.append(txt(186 + w, y + 4, f"{v:,}", 10, MUTED))
    b.append(txt(40, 220, "被引最多（次）：瑜伽 669 · 涅槃 585 · 大智度 538 · 成唯识 507 · 摄论 371", 10, MUTED))
    b.append(txt(40, 240, "合计 7,705 次，已映射 87%。配套 CSV 未入仓，本图仅为种子数据复述，不冒充复算。", 10, RED))
    return svg(700, 260, "图12　注疏引文量级", "四部注疏书名号引用量与被引最多的五部", "".join(b))


def fig_matrix(ranges):
    b = []
    b.append(txt(30, 26, "二十八部类 × 关系深度", 14, INK, weight="bold"))
    rh = 19
    for i, r in enumerate(ranges):
        y = 50 + i * rh
        depth = RANGE_DEPTH.get(r["start"], "未做")
        color = DEPTH_COLOR.get(depth, "#bbb")
        b.append(txt(30, y + 4, f'{r["start"]}–{r["end"]}', 9, MUTED))
        b.append(txt(110, y + 4, r["label"][:34], 9, INK))
        b.append(rect(330, y - 8, {"核实": 300, "文本": 240, "引文": 180, "义理": 120, "线索": 60, "未做": 24}.get(depth, 24), 13, fill=color, stroke="none", op=0.85))
        b.append(txt(640, y + 4, depth, 9, color))
    lx = 690
    for k, c in DEPTH_COLOR.items():
        b.append(rect(lx, 46, 10, 10, fill=c, stroke="none"))
        b.append(txt(lx + 14, 55, k, 9, MUTED))
        lx += 42
    return svg(900, 50 + len(ranges) * rh + 16, "图13　部类关系深度", "二十八部类与华严的关系深度", "".join(b))


def table_versions(data):
    t278 = data["versions"]["T09n0278"]
    t279 = data["versions"]["T10n0279"]
    tib = data["versions"]["Tibetan"]["structural_facts"]
    rows = [
        ("晋译", "T278", "佛陀跋陀罗", "约 418–420", f'{t278["juan_count"]} 卷 · {t278["pin_count"]} 品', f'{t278.get("cjk_body", t278["cjk"]):,}', "七处八会"),
        ("唐译", "T279", "实叉难陀", "695–699", f'{t279["juan_count"]} 卷 · {t279["pin_count"]} 品', f'{t279.get("cjk_body", t279["cjk"]):,}', "七处九会"),
        ("唐译", "T293", "般若", "796–798", "40 卷 · 入法界品", f'{next(x for x in data["catalog_32"] if x["taisho"]=="T10n0293")["cjk_body"]:,}', "单品全本"),
        ("藏译", "Toh 44", "Jinamitra 等", "约 800–836〔存疑〕", f'{tib["tibetan_chapters"]} 章 · {tib["bam_po_total"]} 包', "—", "四函"),
        ("梵本", "—", "—", "—", "全经佚；存四部单品", "—", "—"),
    ]
    out = ["| 本 | 编号 | 译者 | 年代 | 规模 | 实测 CJK | 结构 |", "|---|---|---|---|---|---|---|"]
    for r in rows:
        out.append("| " + " | ".join(r) + " |")
    return "\n".join(out)


def table_mapping(rows):
    out = ["| # | 八十华严 | 六十华严 | 会 | 汉别译／异译 |", "|---|---|---|---|---|"]
    for i, r in enumerate(rows, 1):
        out.append(f'| {i} | {esc(r["p80"])} | {esc(r["p60"] or "—")} | {esc(r["assembly"])} | {esc(r["branch"])} |')
    return "\n".join(out)


def table_catalog(data, name_by_pin):
    out = ["| T | 题名（CBETA） | 译者 | 卷 | 品 | 实测 CJK | 角色 | 对应簇 | 校注互见（T279 品） |", "|---|---|---|---|---|---|---|---|---|"]
    for x in data["catalog_32"]:
        t = x["taisho"]
        role = "大本" if t in ROLE_MAIN else ("别生" if int(t[-3:]) <= 297 else "眷属")
        pins = x["xref"].get("T279") or []
        xref = "、".join(f"{p} {name_by_pin.get(p, '')}" for p in pins) or "—"
        pin = {"T09n0278": 34, "T10n0279": 39, "T10n0293": 1}.get(t, x["pin_count"] or "—")
        out.append(f'| {t.replace("T10n0", "T")} | {esc(x["title_cbeta"])} | {esc(SHORT.get(t, x["translator_cbeta"]))} | {x["juan_cbeta"]} | {pin} | {x.get("cjk_body", x["cjk"]):,} | {role} | {CLUSTER.get(t, "—")} | {esc(xref)} |')
    out.append("")
    out.append("> 题名、译者、卷数、品数、CJK 均由 CBETA XML 逐部解析（`✓`，30/30）；译者栏用通行简称，全称见 CBETA byline。「角色」「对应簇」为本文判断，「校注互见」取自 Taishō `docNumber`。")
    return "\n".join(out)


def table_clusters():
    out = ["| 簇 | 八十品 | 藏章 | 汉别译／异译 | 级 |", "|---|---|---|---|---|"]
    for r in CLUSTERS:
        out.append("| " + " | ".join(esc(x) for x in r) + " |")
    return "\n".join(out)


def table_ranges(ranges):
    out = ["| T 号 | 部类 | 与华严的关系深度 |", "|---|---|---|"]
    for r in ranges:
        depth = RANGE_DEPTH.get(r["start"], "未做")
        out.append(f'| {r["start"]}–{r["end"]} | {esc(r["label"][:40])} | {depth} |')
    return "\n".join(out)


def table_dashabhumika():
    out = ["| 译本 | 译者 | 卷 | 实测 CJK | 亲缘 | 种子相似度（B） |", "|---|---|---|---|---|---|"]
    for r in DASHABHUMIKA:
        out.append("| " + " | ".join(esc(x) for x in r) + " |")
    return "\n".join(out)


def table_claims(data):
    out = ["| id | 主张 | 值 | 判定 |", "|---|---|---|---|"]
    for c in data["claims"]:
        out.append(f'| {c["id"]} | {esc(c["claim"])} | {esc(str(c["value"])[:100])} | {c["status"]} |')
    return "\n".join(out)


def _clip(s, n=76):
    s = str(s)
    return s if len(s) <= n else s[:n] + "…"


def table_canon_registry(reg):
    """Cross-canon carrier registry (§17.3). Rows are data; nothing is inferred."""
    rows = reg.get("rows", [])
    out = ["| 域 | 典藏 | 形制 | 编排 | 本仓见证 | 可做层 | 级 |",
           "|---|---|---|---|---|---|---|"]
    for r in rows:
        out.append("| {d} | {c} | {car} | {o} | {w} | {l} | {g} |".format(
            d=esc(r["domain"]),
            c=esc(r["canon"]),
            car=esc(r["carrier"]),
            o=esc(r["organization"]),
            w=esc(r["witness_local"]),
            l="／".join(r["layers"]),
            g=esc(r["grade"]),
        ))
    out.append("")
    out.append("其中多层登记项只表示「该层在方法上可做」，不表示已做。逐条备注见 `data/research/canon_registry.json`。")
    return "\n".join(out)


STATUS_ZH = {"done": "已做", "partial": "部分", "none": "未做"}
FACET_ZH = {"M": "物质载体", "T": "文本", "D": "义理", "P": "修行",
            "S": "社会史", "R": "接受传播", "C": "比较类型"}


def table_operators(ont):
    """§17.3 — all operators, grouped by facet, straight from the ontology."""
    out = ["| 算子 | 面 | 问法 | 判 | 最低证据 | 越界禁令 | 本文 | 出处 |",
           "|---|---|---|---|---|---|---|---|"]
    for o in ont["operators"]:
        refs = o.get("refs") or "—"
        out.append("| {i} {z} | {f} | {a} | {v} | {e} | {x} | {s} | {r} |".format(
            i=esc(o["id"]), z=esc(o["zh"]), f=esc(o["facet"]),
            a=esc(o["ask"]), v=esc(o["verdict"]), e=esc(o["min_evidence"]),
            x=esc(o["forbidden"]), s=STATUS_ZH.get(o["status"], o["status"]), r=esc(refs)))
    out.append("")
    out.append("「本文」栏是**覆盖状态**，不是价值判断：`未做` 的格子显式留白，比含糊带过可信。")
    return "\n".join(out)


def table_audit(ont):
    """§17.4 — coverage matrix; counts are computed, never typed by hand."""
    ops = ont["operators"]
    out = ["| 面 | 面名 | 算子 | 已做 | 部分 | 未做 | 覆盖率 | 未满算子（部分／未做） |",
           "|---|---|---:|---:|---:|---:|---:|---|"]
    tot = {"done": 0, "partial": 0, "none": 0}
    for f in ont["facets"]:
        mine = [o for o in ops if o["facet"] == f["id"]]
        c = {k: sum(1 for o in mine if o["status"] == k) for k in tot}
        for k in tot:
            tot[k] += c[k]
        score = c["done"] + 0.5 * c["partial"]
        gaps = [f'{o["id"]} {o["zh"]}' for o in mine if o["status"] != "done"]
        out.append(f'| {f["id"]} | {esc(f["name"])} | {len(mine)} | {c["done"]} | {c["partial"]} | {c["none"]} '
                   f'| {score / len(mine) * 100:.0f}% | {esc("、".join(gaps)) if gaps else "—"} |')
    score = tot["done"] + 0.5 * tot["partial"]
    out.append(f'| **合** | — | **{len(ops)}** | **{tot["done"]}** | **{tot["partial"]}** | **{tot["none"]}** '
               f'| **{score / len(ops) * 100:.0f}%** | — |')
    out.append("")
    out.append("口径：`已做`=1、`部分`=0.5、`未做`=0；覆盖率＝加权和÷该面算子数。"
               f"全书加权覆盖 {score:g}/{len(ops)}＝{score / len(ops) * 100:.1f}%。"
               "此表由 `data/research/relation_ontology.json` 直接生成，手改无效。")
    return "\n".join(out)


def table_edges(ont):
    """§4.5 — graph edge types with the facet each one belongs to."""
    ge = ont.get("graph_edges", {})
    order = ["contains", "contains_60", "parallel", "translation", "related", "belongs",
             "unique", "survives", "cites", "cites_class", "sums_to", "contains_part"]
    out = ["| 边型 | 方向 | 含义 | 线型 | 面 | 级 |", "|---|---|---|---|---|---|"]
    for k in order:
        v = ge[k]
        out.append(f'| `{k}` | {esc(v["dir"])} | {esc(v["meaning"])} | {esc(v["line"])} '
                   f'| {v["facet"]} | {esc(v["grade"])} |')
    out.append("")
    out.append(f'> **边型共 {len(ge)} 类**（上表 11 行，其中 `cites`／`cites_class` 为两类）。'
               "「面」按 §17.1 的七面标注：M 物质载体、T 文本、D 义理、P 修行、S 社会史、R 接受传播、C 比较类型。"
               "`sums_to` 与 `contains_part` 只在数据层出现。")
    return "\n".join(out)


def table_t9(probes):
    p = probes["t9"]
    out = [f"共 {len(p['cases'])} 品，逐品对照；引文逐条在底本中做过子串校验。"]
    for case in p["cases"]:
        out.append("")
        out.append(f"**{esc(case['pin'])}**")
        out.append("")
        out.append("| 项 | 澄觀《疏》T1735 | 法藏《探玄記》T1733 |")
        out.append("|---|---|---|")
        for item, a, b in case["rows"]:
            out.append(f"| {esc(item)} | {esc(a)} | {esc(b)} |")
        out.append("")
        for q in case["quotes"]:
            out.append(f'- `{q["src"]}` {q["id"]}：「{esc(q["text"])}」')
        out.append("")
        out.append(f'**判断**：{esc(case["finding"])}')
        out.append("")
        out.append(f'**边界**：{esc(case["limits"])}')
    return "\n".join(out)


def table_d5(probes):
    p = probes["d5"]
    out = ["| 命题 | 《華嚴》T279 | 《度人經》DZ0001 | 判定 | 说明 |",
           "|---|---|---|---|---|"]
    for prop, h, d, note, verdict in p["rows"]:
        out.append(f"| {esc(prop)} | {esc(h)} | {esc(d)} | {esc(verdict)} | {esc(note)} |")
    out.append("")
    c = p["counts"]
    out.append("| 关键词 | T279 | DZ0001 |")
    out.append("|---|---:|---:|")
    for k, v in c.items():
        out.append(f"| {esc(k)} | {v['T279']:,} | {v['DZ0001']:,} |")
    out.append("")
    out.append("计数为去标记后的子串出现次数，只作量级参考。")
    out.append("")
    for q in p["quotes"]:
        out.append(f'- `{q["src"]}` {q["id"]}：「{esc(q["text"])}」')
    out.append("")
    out.append(f'**判断**：{esc(p["finding"])}')
    out.append("")
    out.append(f'**边界**：{esc(p["limits"])}')
    return "\n".join(out)


def table_p1(probes):
    p = probes["p1"]
    out = ["| 位次 | 十住（T279 品15） | 十地（T279 品26） |", "|---:|---|---|"]
    for rank, a, b in p["rows"]:
        out.append(f"| {rank} | {esc(a)} | {esc(b)} |")
    out.append("")
    out.append(f'> 两组名称交集：{len(p["name_overlap"])} 个。')
    out.append("")
    for q in p["quotes"]:
        out.append(f'- `{q["src"]}` {q["id"]}：「{esc(q["text"])}」')
    out.append("")
    out.append(f'**判断**：{esc(p["finding"])}')
    out.append("")
    out.append(f'**边界**：{esc(p["limits"])}')
    return "\n".join(out)


def table_t6(implicit):
    pairs = implicit["pairs"]
    order = ["A", "B", "C"]
    out = ["| 对 | 注释 | 所注经 | 12 字长句 | 明引 | 暗引 | 暗引独见 | 最长 | ≥40 字 | 长句字／经文 |",
           "|---|---|---|---:|---:|---:|---:|---:|---:|---:|"]
    for pid in order:
        p = pairs[pid]
        st = p["stats"]
        out.append(
            f"| {pid} | {esc(p['commentary'])} | {esc(p['sutra'])} | {st['hits']} | "
            f"{st['marked']['hits']} | {st['unmarked']['hits']} | {st['unmarked_distinct']['hits']} | "
            f"{st['max_length']} | {st['ge_40']} | {st['matched_chars']:,}／{st['sutra_chars']:,}"
            f"（{st['coverage']:.2%}） |"
        )
    out.append("")
    out.append("门槛敏感度（同一方法，只改 N）：")
    out.append("")
    sweep_pids = [p for p in order if "sweep" in pairs[p]]
    head = "| N |" + "".join(f" {p} 长句 | {p} 覆盖 |" for p in sweep_pids)
    out.append(head)
    out.append("|---:|" + "---:|---:|" * len(sweep_pids))
    for n in implicit["meta"]["sweep"]:
        cells = [str(n)]
        for p in sweep_pids:
            s = pairs[p]["sweep"][str(n)]
            cells += [str(s["hits"]), f"{s['coverage']:.2%}"]
        out.append("| " + " | ".join(cells) + " |")
    out.append("")
    out.append("暗引示例（两侧行号均为 CBETA `lb`，可回源核对；两本同收的卷首序不算注经复用，示例不取序区）：")
    out.append("")
    for pid in order:
        p = pairs[pid]
        for e in p["examples_unmarked"]:
            out.append(
                f"- {pid} `{p['commentary']}` {e['c_line']} ↔ `{p['sutra']}` {e['s_line']}"
                f"（{e['length']} 字）：「{esc(e['text'])}」"
            )
    out.append("")
    out.append("**判断**：唐疏（A）与唐钞（B）对自宗经的长句复用都是点状的，且以明引为主；"
               "暗引是少数，成因多为「已标品名、句下省引号」。宋注（C）是另一种体例——"
               "疏注合体把经文嵌进注层，长句复用近十倍于唐疏，且九成无引号："
               "注经体的「引」不标明引，是格式的不同，不是袭用的证据。")
    return "\n".join(out)


def table_t7(probe):
    pairs = probe["pairs"]
    order = ["A", "B", "C"]
    out = ["| 对 | 注释 | 所注经 | 品数 | 经文字 | 注疏字 | 长比 | 引文字 | 引用率（中位／最高） | 单条最长 | 链最长 |",
           "|---|---|---|---:|---:|---:|---:|---:|---|---:|---:|"]
    for pid in order:
        p = pairs[pid]
        st = p["stats"]
        out.append(
            f"| {pid} | {esc(p['commentary'])} | {esc(p['sutra'])} | {st['pins']} | "
            f"{st['sutra_chars']:,} | {st['com_chars']:,} | {st['length_ratio']:.3f} | "
            f"{st['quoted_chars']:,} | {st['quoted_share_median']:.2%}／{st['quoted_share_max']:.2%} | "
            f"{st['max_hit']} 字（`{st['max_hit_c_lb']}`） | {st['chain_max_span']} 字 |"
        )
    for pid in order:
        st = pairs[pid]["stats"]
        out.append("")
        out.append(f"最长单条引文（{pid}）：`{st['max_hit_c_lb']}`（{st['max_hit']} 字）：「{esc(st['max_hit_head'])}…」")
    out.append("")
    out.append("明标节略的用语（同一底本内计数；多义的「不具」「故略」「文略」「此略」已剔除）：")
    out.append("")
    out.append("| 用语 | " + " | ".join(order) + " |")
    out.append("|---|" + "---:|" * len(order))
    for label in probe["meta"]["markers"]:
        cells = [str(pairs[pid]["stats"]["markers_by_type"].get(label, 0)) for pid in order]
        out.append(f"| {esc(label)} | " + " | ".join(cells) + " |")
    out.append("| **合** | " + " | ".join(f"**{pairs[pid]['stats']['markers_total']}**" for pid in order) + " |")
    out.append("")
    out.append("引用率最高的品（各取前三）：")
    out.append("")
    out.append("| 对 | 品 | 经文字 | 注疏字 | 长比 | 引用率 |")
    out.append("|---|---|---:|---:|---:|---:|")
    for pid in order:
        for r in pairs[pid]["top"][:3]:
            out.append(f"| {pid} | {esc(r['title'])} | {r['sutra_chars']:,} | {r['com_chars']:,} | "
                       f"{r['ratio']:.2f} | {r['quoted_share']:.2%} |")
    out.append("")
    out.append("注疏反而短于经文的品（长比最低者；这些才是字面意义上的「节略」）：")
    out.append("")
    out.append("| 对 | 品 | 经文字 | 注疏字 | 长比 | 引用率 |")
    out.append("|---|---|---:|---:|---:|---:|")
    for pid in order:
        low = sorted(pairs[pid]["pins"], key=lambda r: r["ratio"])[:3]
        for r in low:
            out.append(f"| {pid} | {esc(r['title'])} | {r['sutra_chars']:,} | {r['com_chars']:,} | "
                       f"{r['ratio']:.2f} | {r['quoted_share']:.2%} |")
    out.append("")
    out.append("明标节略例（`lb` 为 CBETA 行号，可回源核对）：")
    out.append("")
    for pid in order:
        p = pairs[pid]
        for e in p["examples"]:
            out.append(f"- {pid} `{p['commentary']}` {e['lb']}〔{esc(e['type'])}〕：…{esc(e['ctx'])}…")
    out.append("")
    a, b, c = pairs["A"]["stats"], pairs["B"]["stats"], pairs["C"]["stats"]
    out.append(
        f"**判断**：唐疏唐钞对经文既不压缩也不逐句转述——注疏比经文长 {(a['length_ratio'] - 1) * 100:.1f}%（A）"
        f"与 {(b['length_ratio'] - 1) * 100:.1f}%（B），逐品引用率中位 {a['quoted_share_median']:.2%}／"
        f"{b['quoted_share_median']:.2%}，引文点状；多锚点链最长 {a['chain_max_span']}／"
        f"{b['chain_max_span']} 字，无一跨 120 字，注释从不沿经文连续推进。"
        f"可复验的「节略」只有明标的那 {a['markers_total']}／{b['markers_total']} 处"
        f"（略不釋／頌、準前、例類知）——是点状声明，不是整体行为。"
        f"宋注（C，仅 18 品）是另一种体例：长比 {c['length_ratio']:.2f}、引用率中位 "
        f"{c['quoted_share_median']:.2%}、链最长 {c['chain_max_span']} 字——"
        "链沿经推进的是嵌进注层的经文正文，不是注释转述；T7 的「转述／节略」问题对它不成立，"
        "它是 §17.16 之六「逐段嵌入」的另一面。"
    )
    return "\n".join(out)


def _pair_cells(blk, s1, s2):
    return (f"{blk[s1]:.1%}／{blk[s2]:.1%}")


def table_source_map(data, enrich):
    """§4.6 来源拼图总表：39 品 × {六十·藏章·单品别译·梵本·增长痕迹}。

    数据源：mapping_60_80.rows（品名/六十/别译 branch）、tib45（藏章反查）、
    catalog_32 xref（单品反查校验用）；梵本存佚与增长痕迹取自 §6.1 与 84000
    导言（已分别在正文落格，此处仅收拢）。
    """
    # 梵本单品存世（§6.1 表，A/B 级）；增长痕迹（§2.5 藏译拆章、§5.7 参访数）
    SANSKRIT = {
        26: "Daśabhūmika 存",
        31: "寿量梵本存（新发现·B）",
        36: "Bhadracaryā 存（品末偈）",
        39: "Gaṇḍavyūha 存",
    }
    GROWTH = {
        5: "藏译拆为章 5–9（＋新料）",
        39: "聖堅本 25 参→彌勒自数 110",
    }
    tib_by_pin: dict[str, list[int]] = {}
    for r in enrich.get("tib45", []):
        tib_by_pin.setdefault(str(r["pin"]), []).append(r["no"])

    rows = data["mapping_60_80"]["rows"]
    out = []
    out.append("| 品 | 品名（八十） | 六十 | 藏章 | 单品别译（异译） | 梵本 | 增长痕迹 |")
    out.append("|---:|---|---|---|---|---|---|")
    for i, r in enumerate(rows, 1):
        p80 = r["p80"]
        p60 = r["p60"] if r["p60"] and r["p60"] != p80 else "同"
        chapters = tib_by_pin.get(str(i))
        tib = "、".join(str(n) for n in chapters) if chapters else "—"
        branch = r["branch"].strip() if r["branch"] else "—"
        sans = SANSKRIT.get(i, "佚")
        growth = GROWTH.get(i, "—")
        out.append(f"| {i} | {esc(p80)} | {esc(p60)} | {esc(tib)} | "
                   f"{esc(branch)} | {esc(sans)} | {esc(growth)} |")
    out.append("")
    n_branch = sum(1 for r in rows if r["branch"].strip())
    tib_rows = enrich.get("tib45", [])
    hanwu = [r["no"] for r in tib_rows if str(r["pin"]) == "汉无"]
    covered = {str(r["pin"]) for r in tib_rows if str(r["pin"]).isdigit()}
    out.append(f"**拼图完成度**：39 品中 {n_branch} 品有单品别译（§3.2 全表）；"
               f"藏 45 章覆盖 {len(covered)} 品，另有 {len(hanwu)} 章汉无"
               f"（章 {'、'.join(str(n) for n in hanwu)}）；"
               f"梵本单品存 {len(SANSKRIT)} 种（§6.1）；增长痕迹有记者 {len(GROWTH)} 品。"
               "空格＝「无据」，不等于「无来源」。")
    out.append("")
    out.append("**空白登记**（拼图未完处，见 §17.18）：各品的印度前身谱系"
               "（Nattier 原始华严层：兜沙／本业一类最早译）未判；丹珠尔论典"
               "（印度论师怎么读华严）题录全空；东亚传播（新罗·日本）零题录。")
    return "\n".join(out)


def table_growth():
    """§2.8 演变专节：译本时间轴（四貌＝四个时间切片）。

    年代与规模：§2.1/§2.2 已核（CBETA byline、84000 导言 i.11–i.25）；
    聖堅本 25 参、行愿偈 44→62、乌荼王本：84000 Toh 44-45 导言（A，访问 2026-11-13）。
    """
    rows = [
        ("聖堅〈入法界〉单品", "388–408 间", "25 参", "最早的华严汉译是单品；先九参与三十四参后皆缺"),
        ("佛馱跋陀羅 全经", "420", "34 品·60 卷", "全经首次整体着陆；入法界为末品；行愿偈 44 颂"),
        ("實叉難陀 全经", "695–699", "39 品·80 卷", "盧舍那品拆为品 2–6、增十定品（+5）"),
        ("般若〈入法界〉新本", "798", "40 卷", "乌荼王本（795 献唐）；本会前增文；行愿偈 62 颂"),
        ("藏译全经", "约 800–836〔存疑〕", "45 章·115 包", "華藏拆章 5–9、增藏 11/32（+6）；章题定 Gaṇḍavyūha"),
    ]
    out = ["| 译本 | 年代 | 规模 | 相对前貌的增长点 |", "|---|---|---|---|"]
    for a, b, c, d in rows:
        out.append(f"| {esc(a)} | {esc(b)} | {esc(c)} | {esc(d)} |")
    out.append("")
    out.append("（单品先行的时间线见下文；结构算术的拆分定位见 §2.2；参访计数见 §5.7。）")
    return "\n".join(out)


def table_tanjur():
    """§6.3 丹珠尔题录：《行願讚》注释线（Toh 4011–4015）＋十地释线。

    题名/作者/译者逐字取自 dkar chag（Esukhia eTengyur vol.213，situ dkar chag
    443b）；Toh 号取自 eTengyur 卷内 {D} 标记（vol117 完整标记 4010–4015），
    与 dkar chag 目录序互证——双源一致。门禁按「去 folio 标记后子串」回源。
    """
    rows = [
        ("Toh 4011", "འཕགས་པ་བཟང་པོ་སྤྱོད་པའི་སྨོན་ལམ་གྱི་རྒྱལ་པོ་ཆེན་པོའི་བཤད་སྦྱར",
         "ཀླུ་སྒྲུབ（龍樹）", "ཐིག་ལེ་བུམ་པ・བློ་ལྡན་ཤེས་རབ"),
        ("Toh 4012", "ཀུན་དུ་བཟང་པོའི་སྤྱོད་པའི་སྨོན་ལམ་གྱི་དོན་ཀུན་བསྡུས",
         "ཕྱོགས་ཀྱི་གླང་པོ（陳那）", "—"),
        ("Toh 4013", "འཕགས་པ་བཟང་པོ་སྤྱོད་པའི་སྨོན་ལམ་གྱི་རྒྱལ་པོའི་རྒྱ་ཆེར་འགྲེལ་པ",
         "ཤཱཀྱའི་བཤེས་གཉེན", "ཤཱཀྱ་སིངྷ・དཔལ་བརྩེགས"),
        ("Toh 4014", "འཕགས་པ་བཟང་པོ་སྤྱོད་པའི་སྨོན་ལམ་གྱི་རྒྱལ་པོའི་རྒྱ་ཆེར་འགྲེལ་པ",
         "རྒྱན་བཟང་པོ", "ཛྙཱ་ན་གརྦྷ・སྐ་བ་དཔལ་བརྩེགས"),
        ("Toh 4015", "འཕགས་པ་བཟང་པོ་སྤྱོད་པའི་སྨོན་ལམ་གྱི་འགྲེལ་པ",
         "དབྱིག་གཉེན（世親）", "ཨཱ་ནནྡ・བྷ་དྲ་པཱ་ལ"),
    ]
    out = ["| Toh | 题名（藏文原录） | 造者 | 译者 | 目录页 |", "|---|---|---|---|---|"]
    for no, t, a, tr in rows:
        out.append(f"| {no} | {esc(t)} | {esc(a)} | {esc(tr)} | 443b |")
    out.append("")
    out.append("**十地释线**（同名检索另见三部，题名录下、内容对读待下批）：")
    out.append("")
    out.append("| Toh | 题名（藏文原录） | 卷 |")
    out.append("|---|---|---|")
    for no, t, v in (("Toh 3993", "འཕགས་པ་ས་བཅུ་པའི་རྣམ་པར་བཤད་པ", "113"),
                     ("Toh 3998", "ས་བཅུའི་རྣམ་པར་བཤད་པའི་རྣམ་པར་བཤད་པ", "116"),
                     ("Toh 3999", "འཕགས་པ་ས་བཅུའི་མདོ་སྡེའི་གླེང་གཞི", "116")):
        out.append(f"| {no} | {esc(t)} | {v} |")
    return "\n".join(out)


def table_influence():
    """§17.18 影响面开题：四条通道的骨架清单（在库资产与缺口）。"""
    rows = [
        ("宗派传承", "中国五祖→高丽→日本→华严莲社的祖脉谱系",
         "《华严宗脉》专篇（shanhe）＋谱系数据在库", "A（本仓专篇）", "会通到本文的五层坐标待做"),
        ("注疏传统", "智俨→法藏→澄观→净源→德清的释经史（华严塑造中国佛教）",
         "T1732/1733/1735/1736/1739＋X223/234/240 在库；T6/T7 三对已量", "A/B", "后出二线的逐品对读进行中"),
        ("西藏接受", "行願讚释 Toh 4011–4015、十地释 Toh 3993/3998/3999",
         "§6.3/§6.6 题录（eTengyur＋dkar chag 双源）", "B（题录级）", "全文未入库，未对读"),
        ("图像文物", "婆罗浮屠善财浮雕、五台山图、造像、缂丝曼荼罗",
         "文化资产线并行推进中（本仓另线，已入库多件 A 级见证）", "跨线", "R 面与本文的 L3/L4 接口待立"),
        ("儒道论衡", "护教／判教中华严对儒道的指认（宗密《原人论》一类）",
         "未取一手", "C", "待取文本"),
    ]
    out = ["| 通道 | 载体 | 在库资产 | 级 | 缺口 |", "|---|---|---|---|---|"]
    for a, b, c, d, e in rows:
        out.append(f"| {esc(a)} | {esc(b)} | {esc(c)} | {esc(d)} | {esc(e)} |")
    return "\n".join(out)


def table_t4(probe):
    meta = probe["meta"]
    thr = meta["thresholds"]
    pos = probe["controls"]["positive"]
    out = []
    out.append(f"**一、筛查**：库内 {len(probe['screen'])} 部文本（{len(probe['screen']) - 2} 部華嚴部 + 2 部注疏）整篇对测。"
               f"两列是「本文去标点后的不同 {meta['gram']} 字串，有多少也见于该本」。"
               "合本至少要贴住一个源；贴不住的，先出局。")
    out.append("")
    out.append("| 编号 | 题名 | 卷 | 字 | 与 T278 | 与 T279 | 分块检验 |")
    out.append("|---|---|---:|---:|---:|---:|:--:|")
    for r in probe["screen"]:
        out.append(f"| {esc(r['id'])} | {esc(r['title'])} | {r['juan']} | {r['chars']:,} | "
                   f"{r['cov']['T278']:.2%} | {r['cov']['T279']:.2%} | "
                   f"{'受检' if r['tier2'] else '—'} |")
    out.append("")
    out.append(f"（分块检验须 ≥{meta['tier2_min_chars']:,} 字：短经切不出两段，只过筛查。）")
    out.append("")
    out.append("**二、什么算「像」**：同一把尺子量已知关系，排成阶梯：")
    out.append("")
    out.append("| 关系 | 甲 | 乙 | 甲文字数 | 甲 12 字串见于乙 |")
    out.append("|---|---|---|---:|---:|")
    for r in sorted(probe["baselines"], key=lambda x: -x["coverage"]):
        out.append(f"| {esc(r['label'])} | {esc(r['a'])} | {esc(r['b'])} | "
                   f"{r['chars_a']:,} | {r['coverage']:.2%} |")
    out.append("")
    out.append("**三、分块切分**：先植入一部真正的合本当正控，再测库内候选。")
    out.append(f"一个切分点须同时满足：两侧各≥{thr['min_side_share']:.0%}篇幅、"
               f"各自≥{thr['side_coverage']:.0%}覆盖、且压过交叉配对≥{thr['separation']:.0%}，才算通过。")
    out.append("")
    out.append("| 候选 | 源一 | 源二 | 块数 | 单块≥30%（源一／源二） | 左均 源一／源二 | 右均 源一／源二 | 分离度 | 判 |")
    out.append("|---|---|---|---:|---|---|---|---:|---|")
    pr = pos["result"]
    out.append(f"| 正控（植入） | {pos['sources'][0]} | {pos['sources'][1]} | {pos['blocks']} | "
               f"— | {_pair_cells(pr['left'], *pos['sources'])} | "
               f"{_pair_cells(pr['right'], *pos['sources'])} | {pr['separation']:+.1%} | "
               f"{'通过' if pos['pass'] else '未通过'} |")
    for r in probe["partition"]:
        bs, st = r["best_split"], r["block_stats"]
        s1, s2 = r["sources"]
        cells = [r["id"], s1, s2, str(r["blocks"]),
                 f"{st[s1]['blocks_ge_30']}／{st[s2]['blocks_ge_30']}"]
        if bs["split_char"] is None:
            cells += ["—", "—", "—", "不通过"]
        else:
            cells += [_pair_cells(bs["left"], s1, s2), _pair_cells(bs["right"], s1, s2),
                      f"{bs['separation']:+.1%}", "通过" if r["pass"] else "不通过"]
        out.append("| " + " | ".join(cells) + " |")
    out.append("")
    out.append(f"正控是「八十華嚴前半＋六十華嚴後半」的拼接本（{pos['recipe']['first_chars']:,} ＋ "
               f"{pos['recipe']['second_chars']:,} 字）。切点实际落在一块之内："
               f"误差 {pos['result']['recovered_error']} 字，左段对八十 {pos['result']['left'][pos['sources'][0]]:.1%}、"
               f"右段对六十 {pos['result']['right'][pos['sources'][1]]:.1%}，分离度 "
               f"{pos['result']['separation']:+.1%}。检验能看见接缝。")
    out.append("")
    out.append("**四、最佳块**（首块含经题、不计；覆盖率=该 1,000 字块中见于所标源的 12 字串比例）：")
    out.append("")
    out.append("| 候选 | 源 | 块 `lb` | 覆盖率 | 起首 |")
    out.append("|---|---|---|---:|---|")
    for r in probe["partition"]:
        b = r["best_block"]
        if not b:
            continue
        out.append(f"| {r['id']} | {b['source']} | `{b['lb']}` | {b['coverage']:.1%} | "
                   f"{esc(b['head'])}… |")
    out.append("")
    tg = {r["label"]: r for r in probe["targeted"]}
    out.append("**五、定点**：四十華嚴末卷（`%s`，%s 字）与《普賢菩薩行願讚》只有 %.2f%% 相同，"
               "不是从讚文拼入；同本卷 1–39 与八十〈入法界品〉为 %.2f%%。"
               % (probe["targeted"][0]["lb"], f"{probe['targeted'][0]['chars_a']:,}",
                  probe["targeted"][0]["coverage"] * 100, probe["targeted"][1]["coverage"] * 100))
    out.append("")
    # 六、经文合编（卍续藏库外档 X223／X240a／X240b）
    hls = [r for r in probe["partition"] if r["id"] in ("X223", "X240a", "X240b")]
    out.append("**六、经文合编**（卍续藏库外档）：志寧把经文「釐入」李通玄《合論》，"
               "德清《綱要》把经文与澄观疏义合编。两例都不是本节问的「两段拼合」——"
               "块级分类（1,000 字块）见出第三种形态：")
    out.append("")
    out.append("| 候选 | 合编 | 块数 | 经块 | 义块 | 双高 | 交错 | 最长同型 | 整体覆盖 →经／→义源 | 分离度 |")
    out.append("|---|---|---:|---:|---:|---:|---:|---:|---|---:|")
    for r in hls:
        hl = r["helun"]
        s1, s2 = r["sources"]
        out.append(f"| {r['id']} | {esc(EXTRA_TITLES[r['id']])} | {r['blocks']} | "
                   f"{hl['labels']['经块']} | {hl['labels']['义块']} | {hl['labels']['双高']} | "
                   f"{hl['transitions']} | {hl['longest_run']} | "
                   f"{hl['cov_overall'][s1]:.1%}／{hl['cov_overall'][s2]:.1%} | "
                   f"{r['best_split']['separation']:+.1%} |")
    out.append("")
    out.append(f"经论**交错 {hls[0]['helun']['transitions']} 次**（合論；最长同型段 {hls[0]['helun']['longest_run']} 块＝卷首论正文），"
               f"綱要两档交错 {hls[1]['helun']['transitions']}／{hls[2]['helun']['transitions']} 次——"
               "经文按章段厘入，经块与义块高频交替。逐段嵌入下不存在「两侧各贴一个源」的切点，"
               "与通篇近文的 T286 同属不可分离，但成因不同：T286 是一个源到底，合編是两个源编织。"
               "「两本合成一书」在藏内确有其例，形态为**章段级逐段嵌入**，而非「两经各取半部」的拼合本。")
    out.append("")
    v = probe["verdict"]
    out.append(f"**判断**：{v['screen_texts']} 部受检于筛查、{v['candidates']} 部进入分块检验，"
               f"通过 {len(v['passed'])} 部——**{v['statement']}**")
    out.append("")
    t286 = next(r for r in probe["partition"] if r["id"] == "T286")
    out.append("两种「像」必须分开：**通篇对齐一个源**是近文異譯或抄出"
               f"（T286《十住經》{t286['block_stats']['T278']['blocks_ge_30']}/{t286['blocks']} 个块对六十本都≥30%，"
               "但切到哪一侧都一样高，分离度为负）；**两侧分别对齐两个源**才是拼合（正控即如此）。"
               f"库内 {len(probe['partition'])} 部候选全属前者或无对齐，无一部属后者。")
    return "\n".join(out)


def table_endgame(probe):
    s = probe["summary"]
    tx = probe["texts"]
    lbl = {"T279": "八十〈入法界品〉品39", "T278": "六十〈入法界品〉品34",
           "T293": "四十華嚴（全篇）"}
    out = []
    out.append("**一、辭退刻度**：每次参访以「辭退」收束，末参（普賢）无此语；开初会众散去亦用此语。"
               "按标记前 200 字内是否出现「善財」分为参末／会众散——这是机械规则，译文详略会让同一叙述点"
               "分到两边（如八十 0345a20 记参末、四十 0697a23 记会众散），逐处 `lb` 见 JSON。"
               "与 §5.7 的 50／52／53 诸说不同口径：那是「参」的计数，这里是「有辞退语的参末」。")
    out.append("")
    out.append("| 本 | 起 `lb` | 净字 | 辭退 | 参末 | 会众散 | 参长中位 | 最长参 |")
    out.append("|---|---|---:|---:|---:|---:|---:|---|")
    for k in ("T279", "T278", "T293"):
        t, kd = tx[k], s["kinds"][k]
        mv = s["max_visit"][k]
        out.append(f"| {lbl[k]} | `{t['lb']}` | {t['chars']:,} | {t['marks']} | "
                   f"{kd['参末']} | {kd['会众散']} | {s['median_visit_chars'][k]:,} | "
                   f"`{mv['lb']}`（{mv['chars']:,} 字） |")
    out.append("")
    out.append("**二、字面锚（唯一出现才可锚）**：取八十本每个标记前 40 字（不足递减至 16），"
               "在对方原样查找——窗在对方**恰出现一次**才可锚，多见记复见"
               "（首见即中会把不同参的相同套语撞到一处）。")
    out.append("")
    out.append("| 方向 | 标记 | 同一处 | 邻近 | 漂移 | 复见 | 无锚 | 中位距 |")
    out.append("|---|---:|---:|---:|---:|---:|---:|---:|")
    for name, rows_, tally, med in (
            ("八十→六十", probe["pivot"]["T278"], s["pivot_to_60"], s["median_dist_60"]),
            ("八十→四十", probe["pivot"]["T293"], s["pivot_to_40"], s["median_dist_40"]),
            ("四十→八十", probe["reverse"], s["reverse_40_to_80"], None)):
        out.append(f"| {name} | {len(rows_)} | {tally.get('同一处', 0)} | {tally.get('邻近', 0)} | "
                   f"{tally.get('漂移', 0)} | {tally.get('复见', 0)} | {tally.get('无锚', 0)} | "
                   f"{med if med is not None else '—'} |")
    out.append("")
    out.append("**三、锚定子集**：全部同一处／邻近对——"
               "无锚只说明原样窗不存在，不证明该参为对方所无：")
    out.append("")
    out.append("| 方向 | 甲 `lb` | 乙 `lb` | 距 | 窗 | 甲标记前文 |")
    out.append("|---|---|---|---:|---:|---|")
    for direction, rows_ in (("八十→六十", probe["pivot"]["T278"]),
                             ("八十→四十", probe["pivot"]["T293"]),
                             ("四十→八十", probe["reverse"])):
        for r in rows_:
            if r["cls"] in ("同一处", "邻近"):
                out.append(f"| {direction} | `{r['lb']}` | `{r['mapped_lb']}` | {r['dist']} | "
                           f"{r['anchor']} | {esc(r['ctx'][-18:])} |")
    out.append("")
    out.append("**四、链式对齐（8-gram 唯一锚 → 最长单调链 → 分段插值）**："
               "字面锚要求整段 40 字原样重现，跨异译几乎必然落空；改取 8 字窗，"
               "在对方**恰出现一次**者为候选，再取两侧位置同增的最长链（LIS），"
               "相邻链点之间线性插值定位。这量的是**位置对应**，不是字面对应——"
               "插值只给位置，不给语义；链未覆盖处记「无链」，不外推。")
    out.append("")
    out.append("| 方向 | 标记 | 同一处 | 邻近 | 漂移 | 无链 | 中位距 | 链点 |")
    out.append("|---|---:|---:|---:|---:|---:|---:|---:|")
    for name, key in (("八十→六十（链）", "to_60"), ("八十→四十（链）", "to_40"),
                      ("四十→八十（链）", "rev_40_80")):
        c = s["chain"][key]
        t = c["tally"]
        out.append(f"| {name} | {len(probe['chain'][key]['rows'])} | {t.get('同一处', 0)} | "
                   f"{t.get('邻近', 0)} | {t.get('漂移', 0)} | {t.get('无链', 0)} | "
                   f"{c['median'] if c['median'] is not None else '—'} | "
                   f"{c['anchors']:,} |")
    out.append("")
    out.append("链点相邻窗重叠，故数目稠密（是覆盖密度，不是独立锚数）。")
    out.append("")
    out.append("**五、离群点：差异在收束语**：下列各处的链落点与对方最近标记相隔百余至千余字，"
               "「距」即链落点与该本最近标记的距离，乙 `lb` 为收束语所在行。"
               "逐条读两侧原文，可指认的差异都在**收束语的用词**（不涉及参访增减；"
               "师名异写另见七、八两节）：")
    out.append("")
    out.append("| 方向 | 甲 `lb`（标记） | 乙 `lb`（收束语） | 距 | 甲处（收束语） | 乙处（收束语） |")
    out.append("|---|---|---|---:|---|---|")
    dirlbl = {"to_60": "八十→六十（链）", "to_40": "八十→四十（链）",
              "rev_40_80": "四十→八十（链）"}
    for o in probe["chain_outliers"]:
        out.append(f"| {dirlbl[o['dir']]} | `{o['a']['lb']}` | `{o['b']['lb']}` | "
                   f"{o['dist']:,} | …{esc(o['a']['text'][-13:])} | …{esc(o['b']['text'][-13:])} |")
    out.append("")
    gap = next(g for g in probe["chain_gap"]["to_60"] if g["dist"] > 3000)
    out.append(f"另有一处不入表：八十 `{gap['lb']}` 的链落点距六十最近标记 "
               f"{gap['dist']:,} 字——六十本这一段没有对应标记，是分段详略不同，"
               "不是收束语问题。")
    out.append("")
    fam = probe["family"]
    out.append("**六、收束语族（窄义）**：把「辭退」放宽到同义收束语"
               "（辭退／辭去／而退／遶（繞、匝）…而去），三本计 53／51／54。"
               "但**数目不等于参数**：")
    out.append("")
    out.append("| 本 | 辭退 | 辭去 | 而退 | 匝…而去 | 合计 | 其中非善財 | 非善財处 `lb` |")
    out.append("|---|---:|---:|---:|---:|---:|---:|---|")
    for key, nm in (("T279", "八十"), ("T278", "六十"), ("T293", "四十")):
        f = fam[key]
        k = f["kinds"]
        out.append(f"| {nm} | {k.get('辭退', 0)} | {k.get('辭去', 0)} | {k.get('而退', 0)} | "
                   f"{k.get('匝…而去', 0)} | {f['total']} | "
                   f"{f['total'] - f['before_shancai']} | "
                   f"{esc('、'.join('`' + x + '`' for x in f['not_before_lb']))} |")
    out.append("")
    out.append("八十的 53 里，文殊、舍利弗二处的会众散退，以及本生故事中太子「辭退還宮」，"
               "都不是善財参访——**53 不可用作「五十三参」的证成**。"
               "这是本节最该记住的一条：数目对上了，也不能当证据。")
    out.append("")
    np60, np40 = s["name_pairs_60"], s["name_pairs_40"]
    p60n = [p["name"] for p in probe["name_pairs"]["T278"] if not p["generic"]]
    p40n = [p["name"] for p in probe["name_pairs"]["T293"] if not p["generic"]]
    g40n = [p["name"] for p in probe["name_pairs"]["T293"] if p["generic"]]
    out.append("**七、同名锚**：参末套语直书师名（禮X足，去尾衔、去虚指），两侧同名且次序单调者配对。"
               "正名对可锚一参；通名对（王、夜）只说明次序相合，不作人名认定。")
    out.append("")
    out.append("| 对 | 正名对 | 通名对 | 正名 |")
    out.append("|---|---:|---:|---|")
    out.append(f"| 八十↔六十 | {np60['proper']} | {np60['generic']} | {esc('、'.join(p60n))} |")
    out.append(f"| 八十↔四十 | {np40['proper']} | {np40['generic']} | "
               f"{esc('、'.join(p40n))}（通名：{esc('、'.join(g40n))}） |")
    out.append("")
    out.append("同名锚之外还有序位证据：海雲参（同名锚 `0336b11`↔`0682b18`）之后的下一参，"
               "八十本指示句作「善住」、六十本参末套语作「善住比丘」、四十本作「妙住」。"
               "是否同实，梵本可旁证：Gaṇḍavyūha（GRETIL 电子文本，Vaidya 1960 底本）"
               "海雲（Sāgaramegha）之后一参作 **Supratiṣṭhita** 比丘——"
               "「见其于虚空中经行」，情节与八十本〈善住比丘〉章相合；supra- 兼有善／妙二义，"
               "**「善住」与「妙住」为同一梵名之两译**〔本文判断，梵本一手旁证〕。")
    out.append("")
    p60 = json.loads(PAIR60.read_text(encoding="utf-8"))
    p40 = json.loads(PAIR40.read_text(encoding="utf-8"))
    nc = p60["stats"]["name_counter"]
    out.append("**八、师名谱系（五十参逐参比对）**：以参末套语直书的师名逐参比对，"
               "判「全同／义近／基同增衔／异」（`huayan_80_60_pairwise.json`）：")
    out.append("")
    out.append("| 对 | 逐参 | 全同 | 义近 | 基同增衔 | 异 |")
    out.append("|---|---:|---:|---:|---:|---:|")
    out.append(f"| 八十↔六十 | {p60['stats']['total']} | {nc.get('全同', 0)} | "
               f"{nc.get('义近', 0)} | {nc.get('基同增衔', 0)} | {nc.get('异', 0)} |")
    out.append("")
    out.append(f"八十↔四十 的全同为 {p40['stats']['name_same']}/{p40['stats']['total']}，"
               "其余分散在义近、增衔、异名各类，不逐类罗列。"
               "异名不等于异参——如善住／妙住为同一梵名之两译（上表）；"
               "故师名只作谱系刻度，不作「参访增减」的证据。")
    out.append("")
    p60n = p60["stats"]["name_same"] if "name_same" in p60["stats"] else nc.get("全同", 0)
    out.append(f"**判断**：①三本的辭退刻度接近（{s['marks']['T279']}／{s['marks']['T278']}／"
               f"{s['marks']['T293']}；参末 {s['kinds']['T279']['参末']}／"
               f"{s['kinds']['T278']['参末']}／{s['kinds']['T293']['参末']}），"
               "同一段旅程被切成大体相同数目的参——分段是文本自带的刻度，不是编者后加。"
               "②但「字面锚」是弱仪器：八十→六十 48 处仅 2 处可锚，不足以判「六十本措辞独立重译」；"
               "链式对齐 44／48 落在 60 字内（中位 10 字），说明两本的分段几乎逐参对应，"
               "可指认的漂移多在收束语用词（六十「戀仰辭去」「辭詣彼城」）。"
               "③四十本在参界大量沿用八十本文字（字面锚 8 处、链式 46／48），"
               "但收束语也各有着笔（八十作「戀仰而去」处，四十作「辭退而去」）——"
               "同源分叙，不是逐字互抄。"
               f"④收束语族 {fam['T279']['total']}／{fam['T278']['total']}／{fam['T293']['total']} "
               "不能反推参数：八十的 53 中 3 处非善財参访（文殊、舍利弗、本生太子）。"
               f"⑤师名：八十↔六十 {p60['stats']['total']} 参中全同 {p60n}、义近 "
               f"{nc.get('义近', 0)}、基同增衔 {nc.get('基同增衔', 0)}、异 {nc.get('异', 0)}——"
               "师名可作谱系刻度，异名不等于异参。")
    out.append("")
    out.append("**限度**：链式对齐给的是位置，不是语义——插值落点只说明「这一段大致对应到那一段」，"
               "不证明字句相袭；「无链」只说明链未覆盖，不证明该参为对方所无；"
               "收束语族是窄义计数（四种收束语），不等于「参」的数目。")
    return "\n".join(out)


def table_forty(enrich):
    rows = enrich.get("forty", {}).get("batches", [])
    out = ["| 批 | 日期 | 窗 | 主要发现（节录） |", "|---|---|---:|---|"]
    alt = []
    for r in rows:
        w = r.get("windows") or 0
        cell = str(w) if w else f'—（{esc(r.get("kind", "其他记录"))}）'
        if not w:
            alt.append(f'{esc(r["batch"])}（{esc(r.get("kind", "其他记录"))}）')
        out.append(f'| {esc(r["batch"])} | {esc(r["date"])} | {cell} | {esc(_clip(r["finding"]))} |')
    out.append("")
    out.append(f'> 共 **{enrich.get("forty", {}).get("windows_total", 0)} 个对照窗**；完整发现见 `data/research/huayan_80_40_duikandu_b*.json`。'
               + (f'批六、批十三等项目不以「窗口」记录（{"、".join(alt)}），故窗数计「—」，不计入 92 之数。' if alt else ""))
    return "\n".join(out)


def table_bhumi(enrich):
    out = ["| 地 | 梵 | T285 竺法护 | T286 罗什 | T278 六十 | T279 八十 | T287 尸罗达摩 |", "|---|---|---|---|---|---|---|"]
    for r in enrich.get("bhumi", []):
        out.append(f'| {esc(r["name"])} | {esc(r["sa"])} | {esc(r["T285"])} | {esc(r["T286"])} | {esc(r["T278"])} | {esc(r["T279"])} | {esc(r["T287"])} |')
    out.append("")
    out.append("> T285 的十地名单见其卷首「初菩薩住名曰悅豫…第十菩薩住名曰法雨」；它用「十住／道地」语汇，不用标准「十地」名。")
    return "\n".join(out)


def table_tib45(enrich, name_by_pin):
    out = ["| 藏章 | 函 | 起始叶 | 汉品 | 状态 |", "|---:|---|---|---|---|"]
    for r in enrich.get("tib45", []):
        pin = r["pin"]
        label = f"品{pin} {name_by_pin[int(pin)]}" if str(pin).isdigit() and int(pin) in name_by_pin else pin
        out.append(f'| {r["no"]} | {esc(r["vol"])} | {esc(r["folio"])} | {esc(label)} | {esc(r["status"])} |')
    return "\n".join(out)


def table_mentions(enrich):
    out = ["| 名称 | 匹配串 | T1732 | T1733 | T1735 | T1736 | 合计 |", "|---|---|---:|---:|---:|---:|---:|"]
    for r in enrich.get("mentions", {}).get("rows", []):
        out.append(f'| {esc(r["label"])} | {esc("/".join(r["variants"]))} | {r["T1732"]} | {r["T1733"]} | {r["T1735"]} | {r["T1736"]} | {r["total"]} |')
    out.append("")
    out.append("> 这是**名称提及**的字符串匹配，不是书名号引文计数；用于观察四部注疏的相对关注面，不能替代 §8.1 的种子 7,705 条。")
    return "\n".join(out)


def table_p0(data):
    p = data.get("p0", {})
    rows = [
        ("T300 ↔ 八十品33", f'{p.get("T300_vs_C80_33", "—")} 个 12 字共享', "非字面别译", "T300 与 T301 共享 86 个 12 段"),
        ("T301 ↔ 八十品33", f'{p.get("T301_vs_C80_33", "—")} 个 12 字共享', "非字面别译", "同上"),
        ("T300 ↔ T301", f'{p.get("T300_vs_T301", "—")} 个 12 字共享', "同一异译组", "二者互证，非品33 别译"),
        ("T298 ↔ 八十品36", f'{p.get("T298_vs_C80_36", "—")} 个 12 字共享', "非品36 别译", "84000 章题：The Teaching of Samantabhadra（藏32）"),
        ("T309 ↔ 八十品15", f'{p.get("T309_vs_C80_15", "—")} 个 12 字共享', "非十住别译", "与法藏「非十住品亦非十地品」判语一致"),
        ("T281 品3 ↔ 品15／品26", f'{p.get("T281_p3_vs_C80_15", "—")}／{p.get("T281_p3_vs_C80_26", "—")}', "题名与内容错位", "品题作「十地品」，内容起忉利天；校注仍挂 279(15)"),
        ("84000 Toh 44-32", p.get("toh44_32_title") or "未取到", "章题核对", "藏32 = 普贤宣说"),
        ("84000 Toh 187", p.get("toh187_title") or "未取到", "义理对应", "非字面别译"),
    ]
    out = ["| 检查 | 实测 | 判定 | 说明 |", "|---|---|---|---|"]
    for r in rows:
        out.append("| " + " | ".join(esc(x) for x in r) + " |")
    out.append("")
    out.append("> 12 字共享 = 两段去标点后连续 12 个汉字的交集数；0–4 表示无字面平行，86 表示高度同文。此项为本文新增，直接由脚本计算。")
    return "\n".join(out)


def main():

    data = json.loads(DATA.read_text(encoding="utf-8"))
    rows = data["mapping_60_80"]["rows"]
    name_by_pin = {}
    for i, r in enumerate(rows, 1):
        name_by_pin[i] = r["p80"]

    text = ARTICLE.read_text(encoding="utf-8")
    graph = build_graph()
    enrich = json.loads(ENRICH.read_text(encoding="utf-8")) if ENRICH.exists() else {}
    registry = json.loads(REGISTRY.read_text(encoding="utf-8")) if REGISTRY.exists() else {"rows": []}
    ontology = json.loads(ONTOLOGY.read_text(encoding="utf-8"))
    probes = json.loads(PROBES.read_text(encoding="utf-8")) if PROBES.exists() else {}
    implicit = json.loads(IMPLICIT.read_text(encoding="utf-8"))
    paraphrase = json.loads(PARAPHRASE.read_text(encoding="utf-8"))
    conflation = json.loads(CONFLATION.read_text(encoding="utf-8"))
    endgame = json.loads(ENDGAME.read_text(encoding="utf-8"))
    blocks = {
        "graph_spine": render_spine(graph),
        "graph_radial": render_radial(graph),
        "graph_citations": render_citations(),
        "versions": table_versions(data),
        "mapping": table_mapping(rows),
        "catalog": table_catalog(data, name_by_pin),
        "clusters": table_clusters(),
        "ranges": table_ranges(data["section_ranges"]),
        "dashabhumika": table_dashabhumika(),
        "claims": table_claims(data),
        "p0": table_p0(data),
        "forty": table_forty(enrich),
        "canon_registry": table_canon_registry(registry),
        "operators": table_operators(ontology),
        "audit": table_audit(ontology),
        "edge_types": table_edges(ontology),
        "t9": table_t9(probes),
        "d5": table_d5(probes),
        "p1": table_p1(probes),
        "t6": table_t6(implicit),
        "t7": table_t7(paraphrase),
        "t4": table_t4(conflation),
        "endgame": table_endgame(endgame),
        "bhumi": table_bhumi(enrich),
        "source_map": table_source_map(data, enrich),
        "growth": table_growth(),
        "tanjur": table_tanjur(),
        "influence": table_influence(),
        "tib45": table_tib45(enrich, name_by_pin),
        "mentions": table_mentions(enrich),
        "fig_layers": fig_layers(),
        "fig_catalog": fig_catalog(data),
        "fig_evolution": fig_evolution(data),
        "fig_assemblies": fig_assemblies(),
        "fig_alignment": fig_alignment(rows),
        "fig_clusters": fig_clusters(),
        "fig_dashabhumika": fig_dashabhumika(),
        "fig_sanskrit": fig_sanskrit(),
        "fig_citations": fig_citations(),
        "fig_matrix": fig_matrix(data["section_ranges"]),
    }
    n = 0
    for key, val in blocks.items():
        pat = f"<!--GEN:{key}-->"
        start = f"<!--GEN:start:{key}-->"
        end = f"<!--GEN:end:{key}-->"
        block = start + "\n" + val + "\n" + end
        if pat in text:
            text = text.replace(pat, block)
            n += 1
        elif start in text and end in text:
            text = re.sub(re.escape(start) + r".*?" + re.escape(end), block, text, flags=re.S)
            n += 1
    ARTICLE.write_text(text, encoding="utf-8")
    print(f"injected {n}/{len(blocks)} blocks into {ARTICLE}")
    print(f"article chars: {len(text):,}")


if __name__ == "__main__":
    main()