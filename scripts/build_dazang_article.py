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

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "research" / "dazang_mapping_verification.json"
ENRICH = ROOT / "data" / "research" / "dazang_enrichment.json"
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
    out.append("> 题名、译者、卷数均由 CBETA XML 逐部解析（A）；译者栏用通行简称，全称见 CBETA byline。「角色」「对应簇」为本文判断，校注互见取自 Taishō `docNumber`。")
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


def table_forty(enrich):
    rows = enrich.get("forty", {}).get("batches", [])
    out = ["| 批 | 日期 | 窗 | 主要发现（节录） |", "|---|---|---:|---|"]
    for r in rows:
        out.append(f'| {esc(r["batch"])} | {esc(r["date"])} | {r["windows"]} | {esc(_clip(r["finding"]))} |')
    out.append("")
    out.append(f'> 共 **{enrich.get("forty", {}).get("windows_total", 0)} 个对照窗**；完整发现见 `data/research/huayan_80_40_duikandu_b*.json`。')
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
        "bhumi": table_bhumi(enrich),
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