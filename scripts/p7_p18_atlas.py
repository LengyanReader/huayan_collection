# -*- coding: utf-8 -*-
"""P7–P18 atlas layer generator.

Inserts/replaces a standardized front-matter block for every 第二会 / 第三会
article:

    〇之零  导读指南
    〇之二  本品内容地图 (2 SVG figures + 特色矩阵 + 五种读法 + 数与位之谱)

Idempotent: the generated region is wrapped in <!-- ATLAS:BEGIN Pn --> /
<!-- ATLAS:END Pn --> and is fully replaced on re-run.

Usage:  python scripts/p7_p18_atlas.py [P7 P8 ...]
"""
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

BASE = os.path.join("docs", "经学文献", "华严经细读")
DIR2 = os.path.join(BASE, "第二会_普光明殿_差别因果周")
DIR3 = os.path.join(BASE, "第三会_忉利天宫_差别因果周")

GOLD = "#b8863c"
BROWN = "#7a5a28"
INK = "#5a5147"
MUTE = "#8a7a5e"
BG = "#f6efe1"


def b(s):
    """figcaption is HTML: markdown **bold** must become <b>."""
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)


def svgfix(s):
    """SVG text nodes are not markdown: **bold** -> <tspan font-weight="bold">."""
    s = re.sub(r"\*\*([^*<]+?)\*\*", r'<tspan font-weight="bold">\1</tspan>', s)
    return s.replace("**", "")


def build(d):
    L = []
    a = L.append
    tag = d["tag"]
    a(f"<!-- ATLAS:BEGIN {tag} -->")
    a("### 〇之零、导读指南（阅读路径与方法）")
    a("")
    a(f"**定位：** 考证型细读（philological close reading），以「可复核性」为第一优先。{d['dingwei']}")
    a(f"**本品一句：** {d['yiju']}")
    a("**路径：** 〇之二（二图四表）→ 一（品题与脉络）→ 二（全文逐段）→ 四（义理与名相）→ 五（诸家会读）→ 七（数据层）→ 附录按需查阅。")
    a("**方法：** 先经文后诠释；〔实测〕／〔本文判断〕／〔存疑待核〕三分；负面证据同样入账；结构覆盖 100%，个体择要。")
    a(f"**读前三问：** {d['sanwen']}")
    a("")
    a("## 〇之二、本品内容地图（未入其门，先观其海）")
    a("")
    a("> **本节体例。** 图与表之数据，一律取自本文已回源核定之 §二逐段表与 §7.1／§7.5 实测数；**凡属推断者标〔本文判断〕，不入图**。图各看一事，勿求一图而尽本品。")
    a("")
    a("### 〇之二.0 提要")
    a("")
    a(d["tiyao"])
    a("")
    a("| 图 | 画什么 | 一句话 |")
    a("|---|---|---|")
    for f in d["figs"]:
        a(f"| **图 〇-{f['n']}　{f['title']}** | {f['what']} | {f['one']} |")
    a("")
    a(f"**〔读法之序〕**　{d['xufa']}")
    a("")
    a(f"> **EN corresponding · Map of the Chapter.** {d['en_map']}")
    a("")
    for f in d["figs"]:
        a(f"### 〇之二.{f['n']} 图 〇-{f['n']}　{f['title']}")
        a("")
        a("<figure>")
        a(svgfix(f["svg"].strip()))
        a(f"<figcaption><b>图 〇-{f['n']}　{f['title']}。</b>{b(f['cap'])}<div class=\"en-line\">Fig. 0-{f['n']}. {f['en']}</div></figcaption>")
        a("</figure>")
        a("")
        a("**读法三事。**")
        a("")
        for i, item in enumerate(f["dufa"], 1):
            a(f"{i}. {item}")
        a("")
    k = len(d["figs"]) + 1
    a(f"### 〇之二.{k} 本品在{d['hui']}之坐标")
    a("")
    a(d["weici_note"])
    a("")
    a("| 品 | 卷 | 位／科 | 一句提撕 | 与本品之关系 |")
    a("|---|---|---|---|---|")
    for r in d["weici"]:
        a("| " + " | ".join(r) + " |")
    a("")
    a(f"### 〇之二.{k+1} 本品形式特征（与邻品对看）")
    a("")
    a(d["teshe_note"])
    a("")
    a("| 特征 | 本品表现〔实测〕 | 邻品之对照 | 读法上的后果 |")
    a("|---|---|---|---|")
    for r in d["teshe"]:
        a("| " + " | ".join(r) + " |")
    a("")
    a(f"### 〇之二.{k+2} 五种读法（导览）")
    a("")
    a("| 读法 | 路径 | 适合谁 | 得什么 |")
    a("|---|---|---|---|")
    for r in d["dufa5"]:
        a("| " + " | ".join(r) + " |")
    a("")
    a(f"### 〇之二.{k+3} 数与位之谱：本品之数，四等分录")
    a("")
    a("华严之数非计数之数。本品所涉之数，来源不一，性质亦不一；**先分其等，后论其义**，则不为数目所惑。")
    a("")
    a("| 等第 | 数 | 出处 | 性质 |")
    a("|---|---|---|---|")
    for r in d["shu"]:
        a("| " + " | ".join(r) + " |")
    a("")
    a(d["shu_note"])
    a("")
    a(f"<!-- ATLAS:END {tag} -->")
    return "\n".join(L)


def apply(d):
    path = d["path"]
    with io.open(path, encoding="utf-8") as fh:
        t = fh.read()
    nl = "\r\n" if "\r\n" in t else "\n"
    new = build(d)
    if nl != "\n":
        new = new.replace("\n", nl)

    tag = d["tag"]
    # 1) drop an old generated block
    t = re.sub(r"<!-- ATLAS:BEGIN " + tag + r" -->.*?<!-- ATLAS:END " + tag + r" -->\s*", "", t, flags=re.S)
    # 2) drop old 〇之零 if any
    t = re.sub(r"^### 〇之零.*?(?=^## )", "", t, flags=re.S | re.M)
    # 3) drop old 〇之二 block (### or ##), up to next top-level ##
    t = re.sub(r"^#{2,3} 〇之二.*?(?=^## )", "", t, flags=re.S | re.M)
    # 4) drop the stray "---" separators that some old blocks left behind
    t = re.sub(r"(?:\r?\n){3,}", "\n\n", t.replace("\r\n", "\n"))
    if nl != "\n":
        t = t.replace("\n", nl)
        new = new.replace("\n", nl)

    # 5) insert before "## 一"
    m = re.search(r"^## 一[、　]", t, flags=re.M)
    if not m:
        raise SystemExit("anchor '## 一' not found in " + path)
    t = t[: m.start()] + new + nl + nl + t[m.start():]
    with io.open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(t)
    print("ok", tag, os.path.basename(path), len(t), "chars")


# ----------------------------------------------------------------------------
# 第七部　如来名号品
# ----------------------------------------------------------------------------
P7 = {
    "tag": "P7",
    "path": os.path.join(DIR2, "华严经细读_第七部_如来名号品.md"),
    "hui": "第二会（普光明殿·说十信）",
    "dingwei": "本品为第二会之首，一味以「名号」为法，故读法以**数为纲、以名为纬**：二百一十一条名号，一条不可略，而一条亦不可执实。",
    "yiju": "**二百一十一条名号，只是一佛随物立称**——唱名而遍法界，即令信者信「自心是佛」。",
    "sanwen": "① 211 条名号如何由 10 而 100 而 101 层层开出？② 何以名号品居第二会之首、次品却是四圣谛？③ 「或名」二字与「如來於彼」二十见，是何语法、是何法义？",
    "tiyao": "本品占卷第十二全篇，**剥校勘 CJK 3,226 字**（含品题；正文净 3,219），而所举名号 **211 条**——字少而名多，是华严全经中「名相密度」最高之品。结构为三科：**序分**（标主时处·叹佛德十句·叹众德）→**请分**（念请·四十问）→**说分**（现通云集·文殊叹德·四天下中 10 名·四天下十方 100 名·娑婆百亿总标·娑婆十方 101 名·类通一切释差别所由）。若逐名读去，必困于名；先立二图，则见其「由一而多、多而不异」之骨。",
    "xufa": "先观图 〇-1 以得其数（10→100→101→211），次观图 〇-2 以得其方（十一列各十名，而西北独十一），次读〇之二.3 之坐标、〇之二.6 之数等，然后入 §二逐段。**数既明，名始不滥。**",
    "en_map": "Book Twelve holds 3,226 CJK characters but 211 names — the densest name-cluster in the whole sūtra. The chapter opens with the assembly's forty questions and answers them not with doctrines but with names: ten in this four-continental world, a hundred across its ten directions, a bare total for the hundred billion four-continental worlds of Sahā, and a hundred and one across Sahā's neighbouring ten directions. Fig. 0-1 counts the cascade 10 → 100 → 101 = 211; Fig. 0-2 maps the eleven columns and marks the one textual anomaly (the north-west world yields eleven names, not ten).",
    "figs": [
        {
            "n": 1,
            "title": "名号四重遍周图",
            "what": "数从何来",
            "one": "10 → 100 → 101，两段相合为 211；条条皆「或名」",
            "svg": """<svg viewBox="0 0 1000 540" width="100%" style="max-width:1000px;height:auto" xmlns="http://www.w3.org/2000/svg" font-family="serif">
<text x="500" y="26" text-anchor="middle" font-size="14.5" font-weight="bold" fill="#7a5a28">名号四重：由一四天下而百亿四天下，由百亿而尽法界</text>
<text x="500" y="48" text-anchor="middle" font-size="12" fill="#8a7a5e">条长按名数比例（1 名＝4px）；右列为两段合计</text>

<text x="30" y="96" font-size="13" font-weight="bold" fill="#7a5a28">① 此四天下中</text>
<text x="30" y="114" font-size="11" fill="#8a7a5e">一列 · 释迦名号</text>
<rect x="250" y="80" width="40" height="26" fill="#e6dbc5" stroke="#c9b98f"/>
<text x="304" y="99" font-size="12" fill="#5a5147">10 名（一切義成 · 圓滿月 · 師子吼 · 釋迦牟尼 · 第七仙 · 毘盧遮那 · 瞿曇氏 · 大沙門 · 最勝 · 導師）</text>

<text x="30" y="176" font-size="13" font-weight="bold" fill="#7a5a28">② 此四天下十方</text>
<text x="30" y="194" font-size="11" fill="#8a7a5e">十列 · 各十名</text>
<rect x="250" y="160" width="400" height="26" fill="#e6dbc5" stroke="#c9b98f"/>
<text x="664" y="179" font-size="12" fill="#5a5147">10×10＝100 名</text>

<line x1="250" y1="204" x2="650" y2="204" stroke="#c9b98f"/>
<text x="660" y="224" font-size="12" font-weight="bold" fill="#b8863c">四天下段 110（11 列×10）</text>

<text x="30" y="286" font-size="13" font-weight="bold" fill="#7a5a28">③ 娑婆百亿四天下</text>
<text x="30" y="304" font-size="11" fill="#8a7a5e">总标 · 不列名</text>
<rect x="250" y="270" width="400" height="26" fill="none" stroke="#c9b98f" stroke-dasharray="5 4"/>
<text x="664" y="289" font-size="12" fill="#5a5147">「有百億萬種種名號」</text>

<text x="30" y="376" font-size="13" font-weight="bold" fill="#7a5a28">④ 娑婆邻近十方</text>
<text x="30" y="394" font-size="11" fill="#8a7a5e">十列 · 西北独十一</text>
<rect x="250" y="360" width="400" height="26" fill="#e6dbc5" stroke="#c9b98f"/>
<rect x="650" y="360" width="4" height="26" fill="#b8863c"/>
<text x="664" y="379" font-size="12" fill="#5a5147">10×10＋1＝101 名</text>

<line x1="250" y1="404" x2="650" y2="404" stroke="#c9b98f"/>
<text x="660" y="424" font-size="12" font-weight="bold" fill="#b8863c">娑婆段 101（10 列·西北 11）</text>

<rect x="250" y="452" width="700" height="1" fill="#d3c7ae"/>
<text x="30" y="486" font-size="14" font-weight="bold" fill="#b8863c">合计 211 名</text>
<text x="150" y="486" font-size="12" fill="#5a5147">「或名」211 见　·　「如來於彼」20 见　·　「如是等」21 见（§7.2 实测）</text>
<text x="30" y="512" font-size="11.5" fill="#8a7a5e">※ ④段之「＋1」即西北方「歡喜」世界十一名的溢出；澄观已校「西北方名有十一者」，见 §6.1 校勘与图 〇-2。</text>
</svg>""",
            "cap": "四层条长，各按名数比例。**前两层为「四天下段」（中一列＋十方十列，凡 110 名）；后两层为「娑婆段」（百亿总标＋邻近十方，凡 101 名）；两段相合 211。** 图中可见一事：经文明明说「有百億萬種種名號」，却只举 101 名——**举少以摄多，是本品之法，非经文之略**。〔本文判断〕",
            "en": "Four bars, scaled to the number of names. The first two make the four-continental register (one central column plus ten directional columns, 110 names); the last two make the Sahā register (a bare total for the hundred billion worlds plus 101 names in the neighbouring ten directions). The text says there are hundreds of billions of names and then lists 101 — naming few in order to hold many.",
            "dufa": [
                "**两段各有其「总标」。** 四天下段以「其數十千」结，娑婆段以「百億萬種種名號」结；**所举之 211 是样本，不是全部**。凡读数目，先问「这是所举还是所有」。",
                "**101 之「1」不是笔误，是校勘事件。** 西北方「歡喜」世界列十一名，澄观已注「西北方名有十一者」，与密训「唯九」相对（§6.1）。**异文各照底本，不统一**，故图中留此一竖。",
                "**名数递增而句式不变。** 四层皆用「或名：X」同一句式，唯所被之境由一洲而十方、而百亿、而法界——**变者境，不变者名之语法**。此即下品「四圣谛」四十名之所本。",
            ],
        },
        {
            "n": 2,
            "title": "十一列名号矩阵（四天下段）",
            "what": "名从何方",
            "one": "中 1 列＋十方 10 列，每列十名；西北独十一",
            "svg": """<svg viewBox="0 0 1000 520" width="100%" style="max-width:1000px;height:auto" xmlns="http://www.w3.org/2000/svg" font-family="serif">
<text x="500" y="24" text-anchor="middle" font-size="14.5" font-weight="bold" fill="#7a5a28">「此四天下」之十一列：一洲居中，十界环列</text>
<text x="500" y="45" text-anchor="middle" font-size="12" fill="#8a7a5e">每格上一字为方，下二字为世界名，末注名数；悉依 T10n0279 卷十二逐字回源（§2.7–2.8）</text>

<rect x="330" y="70" width="340" height="54" rx="4" fill="#f3ecdf" stroke="#c9b98f"/>
<text x="500" y="92" text-anchor="middle" font-size="12.5" font-weight="bold" fill="#7a5a28">中 · 此四天下</text>
<text x="500" y="112" text-anchor="middle" font-size="11.5" fill="#5a5147">10 名（釋迦牟尼等）</text>

<g font-size="12">
<rect x="40" y="150" width="170" height="52" rx="4" fill="#fff" stroke="#c9b98f"/>
<text x="125" y="170" text-anchor="middle" font-size="11" fill="#8a7a5e">東</text>
<text x="125" y="188" text-anchor="middle" font-weight="bold" fill="#5a5147">善護</text>
<text x="125" y="202" text-anchor="middle" font-size="10.5" fill="#8a7a5e">10 名</text>

<rect x="228" y="150" width="170" height="52" rx="4" fill="#fff" stroke="#c9b98f"/>
<text x="313" y="170" text-anchor="middle" font-size="11" fill="#8a7a5e">南</text>
<text x="313" y="188" text-anchor="middle" font-weight="bold" fill="#5a5147">難忍</text>
<text x="313" y="202" text-anchor="middle" font-size="10.5" fill="#8a7a5e">10 名</text>

<rect x="416" y="150" width="170" height="52" rx="4" fill="#fff" stroke="#c9b98f"/>
<text x="501" y="170" text-anchor="middle" font-size="11" fill="#8a7a5e">西</text>
<text x="501" y="188" text-anchor="middle" font-weight="bold" fill="#5a5147">親慧</text>
<text x="501" y="202" text-anchor="middle" font-size="10.5" fill="#8a7a5e">10 名</text>

<rect x="604" y="150" width="170" height="52" rx="4" fill="#fff" stroke="#c9b98f"/>
<text x="689" y="170" text-anchor="middle" font-size="11" fill="#8a7a5e">北</text>
<text x="689" y="188" text-anchor="middle" font-weight="bold" fill="#5a5147">有師子</text>
<text x="689" y="202" text-anchor="middle" font-size="10.5" fill="#8a7a5e">10 名</text>

<rect x="792" y="150" width="170" height="52" rx="4" fill="#fff" stroke="#c9b98f"/>
<text x="877" y="170" text-anchor="middle" font-size="11" fill="#8a7a5e">東北</text>
<text x="877" y="188" text-anchor="middle" font-weight="bold" fill="#5a5147">妙觀察</text>
<text x="877" y="202" text-anchor="middle" font-size="10.5" fill="#8a7a5e">10 名</text>

<rect x="40" y="228" width="170" height="52" rx="4" fill="#fff" stroke="#c9b98f"/>
<text x="125" y="248" text-anchor="middle" font-size="11" fill="#8a7a5e">東南</text>
<text x="125" y="266" text-anchor="middle" font-weight="bold" fill="#5a5147">喜樂</text>
<text x="125" y="280" text-anchor="middle" font-size="10.5" fill="#8a7a5e">10 名</text>

<rect x="228" y="228" width="170" height="52" rx="4" fill="#fff" stroke="#c9b98f"/>
<text x="313" y="248" text-anchor="middle" font-size="11" fill="#8a7a5e">西南</text>
<text x="313" y="266" text-anchor="middle" font-weight="bold" fill="#5a5147">甚堅牢</text>
<text x="313" y="280" text-anchor="middle" font-size="10.5" fill="#8a7a5e">10 名</text>

<rect x="416" y="228" width="170" height="52" rx="4" fill="#f7ecd2" stroke="#b8863c" stroke-width="1.6"/>
<text x="501" y="248" text-anchor="middle" font-size="11" fill="#b8863c">西北</text>
<text x="501" y="266" text-anchor="middle" font-weight="bold" fill="#7a5a28">妙地</text>
<text x="501" y="280" text-anchor="middle" font-size="10.5" fill="#b8863c">10 名</text>

<rect x="604" y="228" width="170" height="52" rx="4" fill="#fff" stroke="#c9b98f"/>
<text x="689" y="248" text-anchor="middle" font-size="11" fill="#8a7a5e">下</text>
<text x="689" y="266" text-anchor="middle" font-weight="bold" fill="#5a5147">焰慧</text>
<text x="689" y="280" text-anchor="middle" font-size="10.5" fill="#8a7a5e">10 名</text>

<rect x="792" y="228" width="170" height="52" rx="4" fill="#fff" stroke="#c9b98f"/>
<text x="877" y="248" text-anchor="middle" font-size="11" fill="#8a7a5e">上</text>
<text x="877" y="266" text-anchor="middle" font-weight="bold" fill="#5a5147">持地</text>
<text x="877" y="280" text-anchor="middle" font-size="10.5" fill="#8a7a5e">10 名</text>
</g>

<rect x="330" y="312" width="340" height="52" rx="4" fill="none" stroke="#c9b98f" stroke-dasharray="5 4"/>
<text x="500" y="332" text-anchor="middle" font-size="12.5" fill="#7a5a28">此娑婆世界 · 百億四天下</text>
<text x="500" y="352" text-anchor="middle" font-size="11.5" fill="#5a5147">「有百億萬種種名號」——总标，不列名</text>

<line x1="40" y1="392" x2="960" y2="392" stroke="#e0d6c2"/>
<text x="40" y="418" font-size="12" font-weight="bold" fill="#7a5a28">下段·娑婆邻近十方（另 10 列 101 名，见 §2.10）</text>
<text x="40" y="440" font-size="11.5" fill="#5a5147">密訓 10 · 豐溢 10 · 離垢 10 · 豐樂 10 · 攝取 10 · 饒益 10 · 鮮少 10 · <tspan fill="#b8863c" font-weight="bold">歡喜 11</tspan> · 關𨷲 10 · 振音 10</text>
<text x="40" y="470" font-size="11.5" fill="#8a7a5e">澄观：「密訓唯九者……乃是新本脫漏」「西北方名有十一者」——两处溢出，一缺一溢，各照底本（§6.1）。</text>
<text x="40" y="494" font-size="11.5" fill="#8a7a5e">※ 上段十一列之「中」列即释迦本名，故四天下段＝11 列×10＝110 名。</text>
</svg>""",
            "cap": "上段十界环一洲，凡十一列；下段为娑婆邻近十方，另十列。**二段合观，方见「名号遍周」不是一句空话，而是「一洲为心、十方为环、百亿为海」的三重扩张**。图中金色一格（西北妙地写「妙地」，下段西北为「歡喜」11 名）——**同为西北，上段十名、下段十一名，正是澄观校记所指**。",
            "en": "Eleven columns around one continent: the centre plus the ten directions, ten names each. Below, Sahā's own ten neighbouring worlds, ten columns more. Two registers, one design — a continent at the centre, ten directions as a ring, a hundred billion worlds as the sea. The gold cell marks the one overflow: the north-west world yields eleven names.",
            "dufa": [
                "**「此四天下」不是「此世界」。** 上段之境是一洲（四天下），下段之境才是娑婆；**一洲已具十方十界，则一佛之名已遍十方**——此为本品由小入大之第一转。",
                "**名号之「或」字是用法，不是疑辞。** 「或名」者，随方随机而立此称，非谓佛有此名彼无名。**故读名号，当读其「随」，不当读其「异」。**",
                "**两处校勘，一缺一溢，皆不裁改。** 密训「唯九」、西北「十一」，澄观断为新本脱漏与溢出；本文照底本录，异文存于 §6.1，**不以己意补一名、删一名**。",
            ],
        },
    ],
    "weici_note": "本品为第二会之首。第二会六品，依诸家共判，前三品明如来三业（所信之果），后三品明十信之解行德（能信之行）——**本品居其首，以「身业遍应」立信之体**。",
    "weici": [
        ["**7 如来名号**（本品）", "卷12", "十信·所信果·**身业**", "名号遍周，令信自心是佛", "—（本品）"],
        ["8 四圣谛", "卷12", "十信·所信果·**口业**", "四谛四千名，随众生心悉令调伏", "承本品之「名」，转而为「法」"],
        ["9 光明觉", "卷13", "十信·所信果·**意业**", "足轮放光，十段遍照", "三业至此而毕"],
        ["10 菩萨问明", "卷13", "十信·**解**", "九首递问，文殊总酬", "由果转因，解门开"],
        ["11 净行", "卷14", "十信·**行**", "一百四十一誓，遇事发愿", "解而后行"],
        ["12 贤首", "卷14–15", "十信·**德**", "信为道元功德母", "行而后德，十信满心"],
    ],
    "teshe_note": "本品之「特色」不在义理之深，而在**形式之偏**：它以近三千三百字容纳二百一十一条名号，是全部三十九品中「名相密度」最高之品。读它若用读义理品之法，必失；须用读「陀罗尼品」之法——**以名摄义，以数见遍**。",
    "teshe": [
        ["名相密度", "3,226 字 / 211 名（约每 15 字一名）", "第八品 3,262 字 / 440 名，密度更高而篇幅相若", "两品对读，可见第二会「以名说法」之极致"],
        ["句式重复", "「或名」211 见、「如來於彼」20 见、「如是等」21 见", "第八品作「或名」440 见", "重复是结构，不是贫乏；句式为经之骨"],
        ["问而不答于文", "四十问在前，说分不以义答，而以名答", "第十品以偈酬问，逐问作答", "本品之「答」是示现，非言说"],
        ["一多关系", "一洲十名 → 十方百名 → 百亿总标 → 尽法界", "第九品以光之远近表一多", "名之遍与光之遍，同一法界"],
        ["校勘事件", "密训唯九、西北十一（澄观已校）", "第八品十方世界名与旧图不符者已订正", "凡异文，各照底本、不统一"],
    ],
    "dufa5": [
        ["**数读**", "〇之二 → §7.3 名号分布 → §2.7–2.10 各表", "初读本篇者", "先得 10／100／101／211 之骨"],
        ["**方读**", "只读十方世界名与各方首名", "欲见「随方立名」者", "得十一列之矩阵（图 〇-2）"],
        ["**名读**", "取一洲十名，逐名核澄观释（§2.7）", "好名相训释者", "见「一名一德」之训释法"],
        ["**校读**", "§6.1 六十对读＋§6.4 校勘记", "欲核异文者", "得密训九名、西北十一名之实"],
        ["**承读**", "本品 §2.11 → 第八品 §2.2", "欲见两会脉络者", "见「名」如何转而为「谛」"],
    ],
    "shu": [
        ["**T0 经文明文**", "「其數十千」（各列结句）", "`T10n0279` 卷十二", "喻限数，非计数"],
        ["**T0 经文明文**", "「有百億萬種種名號」", "同上 §2.9", "总标，不列名"],
        ["**T0 本文实测**", "**211 名**（110＋101）", "§7.3 逐名点数", "计数（本文自测）"],
        ["**T0 本文实测**", "3,226 字（CJK 剥校勘）", "§7.1 脚本", "计数（本文自测）"],
        ["**T1 澄观《疏》**", "「密訓唯九」「西北方名有十一」", "`T1735` 卷十二末", "注疏校记"],
        ["**T1 澄观《疏》**", "「名號依身而立」", "`T1733`（法藏）·`T1735` 引", "三业分判之据"],
        ["**T2 转述**", "「名号品答四十问中之佛号问」", "诸家科文，非经文明文", "判摄语，须注家"],
    ],
    "shu_note": "> **〔读法〕** 上表七行，惟「211」「3,226」二数为本文自测，其余皆出经文或注疏。**凡本文自测之数，皆附脚本于 §7.4，可覆算**；凡注疏之数，皆注经号卷次，可回源。二者不相混，是全篇「数」之纪律。",
}

# ----------------------------------------------------------------------------
# 第八部　四圣谛品
# ----------------------------------------------------------------------------
P8 = {
    "tag": "P8",
    "path": os.path.join(DIR2, "华严经细读_第八部_四圣谛品.md"),
    "hui": "第二会（普光明殿·说十信）",
    "dingwei": "本品一味以「四谛」为法，读法当以**谛为经、名为纬**：苦集灭道四行，行各十名，十方各四十——**名四百四十，谛则四而已**。",
    "yiju": "**苦集灭道，各随方立十名；名异而谛同，故曰「随众生心，悉令调伏」。**",
    "sanwen": "① 四谛何以各立十名，十名之间是何次第？② 娑婆 40、十方 400、通计 440，而经文又说「四百亿十千」，四数如何并存？③ 四谛品何以次名号品而起？",
    "tiyao": "本品占卷第十二末段，**剥校勘 CJK 3,262 字**（含品题），句末标点 116，独字 427；所举名号 **440**（娑婆四谛各十名＝40，十方十界各四十＝400）。其结构为全部三十九品中最简者之一：**序分只「文殊師利菩薩告諸菩薩言」一句，无独立请分**，直承前品续说；说分十一——娑婆（40）→十方十界（400）→类通一切·释差别所由。**结构之简，正是其义之密**：一切铺排皆在名号，不在科段。",
    "xufa": "先观图 〇-1 得四谛十名之实（娑婆四十名，逐字照录），次观图 〇-2 辨「所举」与「实有」之别，次读〇之二.3 之坐标，然后入 §二逐段。**四数既分，名始不混。**",
    "en_map": "The shortest-structured chapter in the sūtra: one sentence of introduction, no separate request section, and then names and names. Four truths, ten names each, in this world (40); ten neighbouring worlds, forty each (400); 440 named in all — while the text says each world has four hundred billion ten-thousand names. Fig. 0-1 gives the forty names of Sahā verbatim; Fig. 0-2 separates what is *listed* from what is *said to exist*.",
    "figs": [
        {
            "n": 1,
            "title": "娑婆四谛四十名矩阵",
            "what": "名如何成谛",
            "one": "苦集灭道四行，行各十名；十名同谛而异其侧显",
            "svg": """<svg viewBox="0 0 1000 470" width="100%" style="max-width:1000px;height:auto" xmlns="http://www.w3.org/2000/svg" font-family="serif">
<text x="500" y="24" text-anchor="middle" font-size="14.5" font-weight="bold" fill="#7a5a28">娑婆世界四圣谛：四行 × 十名</text>
<text x="500" y="44" text-anchor="middle" font-size="12" fill="#8a7a5e">逐字照录 T10n0279 卷十二（§2.2）；十名皆「或名」，同谛而各侧显一义</text>

<g font-size="11" fill="#8a7a5e" text-anchor="middle">
<text x="143" y="74">一</text><text x="228" y="74">二</text><text x="313" y="74">三</text><text x="398" y="74">四</text><text x="483" y="74">五</text><text x="568" y="74">六</text><text x="653" y="74">七</text><text x="738" y="74">八</text><text x="823" y="74">九</text><text x="908" y="74">十</text>
</g>

<rect x="18" y="84" width="964" height="72" fill="#f8f3ea" stroke="#e0d6c2"/>
<text x="28" y="108" font-size="12.5" font-weight="bold" fill="#7a5a28">苦聖諦</text>
<text x="28" y="128" font-size="10.5" fill="#8a7a5e">10 名</text>
<g font-size="11.5" fill="#5a5147" text-anchor="middle">
<text x="143" y="122">罪</text><text x="228" y="122">逼迫</text><text x="313" y="122">變異</text><text x="398" y="122">攀緣</text><text x="483" y="122">聚</text><text x="568" y="122">刺</text><text x="653" y="122">依根</text><text x="738" y="122">虛誑</text><text x="823" y="122">癰瘡處</text><text x="908" y="122">愚夫行</text>
</g>

<rect x="18" y="164" width="964" height="72" fill="#f3ecdf" stroke="#e0d6c2"/>
<text x="28" y="188" font-size="12.5" font-weight="bold" fill="#7a5a28">苦集聖諦</text>
<text x="28" y="208" font-size="10.5" fill="#8a7a5e">10 名</text>
<g font-size="11.5" fill="#5a5147" text-anchor="middle">
<text x="143" y="202">繫縛</text><text x="228" y="202">滅壞</text><text x="313" y="202">愛著義</text><text x="398" y="202">妄覺念</text><text x="483" y="202">趣入</text><text x="568" y="202">決定</text><text x="653" y="202">網</text><text x="738" y="202">戲論</text><text x="823" y="202">隨行</text><text x="908" y="202">顛倒根</text>
</g>

<rect x="18" y="244" width="964" height="72" fill="#f8f3ea" stroke="#e0d6c2"/>
<text x="28" y="268" font-size="12.5" font-weight="bold" fill="#7a5a28">苦滅聖諦</text>
<text x="28" y="288" font-size="10.5" fill="#8a7a5e">10 名</text>
<g font-size="11.5" fill="#5a5147" text-anchor="middle">
<text x="143" y="282">無諍</text><text x="228" y="282">離塵</text><text x="313" y="282">寂靜</text><text x="398" y="282">無相</text><text x="483" y="282">無沒</text><text x="568" y="282">無自性</text><text x="653" y="282">無障礙</text><text x="738" y="282">滅</text><text x="823" y="282">體真實</text><text x="908" y="282">住自性</text>
</g>

<rect x="18" y="324" width="964" height="72" fill="#f3ecdf" stroke="#e0d6c2"/>
<text x="28" y="348" font-size="12.5" font-weight="bold" fill="#7a5a28">苦滅道聖諦</text>
<text x="28" y="368" font-size="10.5" fill="#8a7a5e">10 名</text>
<g font-size="11.5" fill="#5a5147" text-anchor="middle">
<text x="143" y="362">一乘</text><text x="228" y="362">趣寂</text><text x="313" y="362">導引</text><text x="398" y="362">究竟無分別</text><text x="483" y="362">平等</text><text x="568" y="362">捨擔</text><text x="653" y="362">無所趣</text><text x="738" y="362">隨聖意</text><text x="823" y="362">仙人行</text><text x="908" y="362">十藏</text>
</g>

<text x="18" y="428" font-size="12" fill="#7a5a28">四行各十名＝<tspan font-weight="bold">40 名</tspan>（娑婆一界所举）</text>
<text x="18" y="450" font-size="11.5" fill="#8a7a5e">※ 十名非「同义反复」：如苦谛十名，自「罪」（业）而「逼迫」（受）而「變異」（无常）而「聚」（蕴）而「愚夫行」（人）——<tspan fill="#7a5a28">五蕴·三受·无常，皆苦之一面</tspan>。〔本文判断〕</text>
</svg>""",
            "cap": "四行十列，四十名逐字照录。**十名不是同义语之堆叠，而是同一谛从不同面切入**：苦谛十名，自业（罪）而受（逼迫）而行（愚夫行）；灭谛十名，自「無諍」而「無自性」而「住自性」——**前九破，后一立**。〔本文判断〕读此图，当横看（同一谛之十面），不当竖看（四谛之次第）。",
            "en": "Four rows, ten columns, the forty names of Sahā given verbatim. The ten names are not synonyms but facets: suffering seen as deed, as feeling, as the way of the fool; cessation seen as nine negations closing on one affirmation, 「住自性」.",
            "dufa": [
                "**横看十名，竖看四谛。** 横看则知一谛之十面，竖看则知四谛之次第；**两读不可同时**，同时则乱。",
                "**灭谛之十名，九破一立。** 「無諍·離塵·寂靜·無相·無沒·無自性·無障礙·滅·體真實·住自性」——前九皆遮，末一「住自性」独显。**遮至无可遮处，方说「住」。**",
                "**道谛以「一乘」为首。** 十名之中，「一乘」居首而「十藏」居末——**自一而十，自乘而藏**，正是华严「一即一切」之名相语法。",
            ],
        },
        {
            "n": 2,
            "title": "所举与实有：四数并存图",
            "what": "数何以不矛盾",
            "one": "40／400／440 是所举，四百亿十千是每界实有",
            "svg": """<svg viewBox="0 0 1000 480" width="100%" style="max-width:1000px;height:auto" xmlns="http://www.w3.org/2000/svg" font-family="serif">
<text x="500" y="24" text-anchor="middle" font-size="14.5" font-weight="bold" fill="#7a5a28">四数并存：所举者样本，实有者法界</text>
<text x="500" y="44" text-anchor="middle" font-size="12" fill="#8a7a5e">实线＝经中所举；虚线＝经中所说之实有</text>

<rect x="60" y="70" width="880" height="310" rx="6" fill="none" stroke="#c9b98f" stroke-dasharray="7 6"/>
<text x="76" y="94" font-size="12.5" font-weight="bold" fill="#b8863c">尽法界·虚空界·诸世界</text>
<text x="76" y="113" font-size="11" fill="#8a7a5e">一一世界，四谛各有「四百億十千名」——实有</text>

<rect x="110" y="132" width="780" height="228" rx="5" fill="#f8f3ea" stroke="#c9b98f"/>
<text x="126" y="156" font-size="12.5" font-weight="bold" fill="#7a5a28">十方十世界</text>
<text x="126" y="175" font-size="11" fill="#8a7a5e">密訓·最勝·離垢·豐溢·攝取·饒益·鮮少·歡喜·關𨷲·振音　各 4×10＝40 名 → 合 400 名（所举）</text>

<rect x="170" y="196" width="300" height="120" rx="5" fill="#f3ecdf" stroke="#c9b98f"/>
<text x="186" y="220" font-size="12.5" font-weight="bold" fill="#7a5a28">娑婆世界</text>
<text x="186" y="240" font-size="11" fill="#5a5147">苦·集·滅·道 各十名</text>
<text x="186" y="260" font-size="11" fill="#5a5147">＝ 40 名（所举）</text>
<text x="186" y="286" font-size="11" fill="#8a7a5e">此即图 〇-1 之四十名</text>

<g font-size="12" fill="#7a5a28">
<text x="500" y="222" font-weight="bold">40</text><text x="500" y="240" font-size="11" fill="#8a7a5e">娑婆所举</text>
<text x="600" y="222" font-weight="bold">400</text><text x="600" y="240" font-size="11" fill="#8a7a5e">十方所举</text>
<text x="700" y="222" font-weight="bold" fill="#b8863c">440</text><text x="700" y="240" font-size="11" fill="#8a7a5e">通计所举</text>
</g>
<text x="500" y="286" font-size="11.5" fill="#8a7a5e">440 是「经中所举之全部」，非「法界之全部」</text>

<text x="60" y="420" font-size="12" fill="#7a5a28">品末结句：「此娑婆世界說四聖諦，有如是等四百億十千名；<tspan font-weight="bold">隨眾生心，悉令調伏</tspan>。」</text>
<text x="60" y="446" font-size="11.5" fill="#8a7a5e">→ 名之多寡，随众生心；佛不以一名应一切机。故名有量而法无量。</text>
</svg>""",
            "cap": "三层套叠：内为娑婆所举四十，中为十方所举四百，外为尽法界每一世界之「四百亿十千」。**四数（40／400／440／四百亿十千）非互相矛盾，而是三种「所举」加一种「实有」**。凡读数目，须先问此数是「举」还是「有」；混之则疑经，分之则见法。",
            "en": "Three nested frames: the forty names listed for Sahā, the four hundred listed for the ten neighbouring worlds, and — outermost, in dotted line — the four hundred billion ten-thousand names that every single world is said to possess. 40 / 400 / 440 are what the text *lists*; the last is what the text says *exists*. Confusing the two breeds phantom contradictions.",
            "dufa": [
                "**「所举」与「实有」必须分书。** 本法界观不以数为限：**举四十以摄四百亿十千，是方便；说四百亿十千，是实相**。",
                "**「随众生心，悉令调伏」是立名之由，也是全品之结。** 四谛之名所以千差，只因机有千差；**名从机立，法不随机而异**。",
                "**与第七品对读，可见两品之分工。** 名号品以「一佛多名」显遍，四谛品以「一法多名」显遍——**所遍同，所依异：一依身，一依法**。",
            ],
        },
    ],
    "weici_note": "本品为第二会之次品。**前品明身业，本品明口业**——法藏「四諦品明佛口業普周」、澄观《演义钞》「身語既彰，意業將顯」；故本品之位置，正在三业之第二。",
    "weici": [
        ["7 如来名号（前）", "卷12", "所信果·**身业**·名遍", "211 名，一佛多名", "名者召体；本品承其名而言谛"],
        ["**8 四圣谛（本品）**", "卷12", "所信果·**口业**·法遍", "440 名，一法多名", "—"],
        ["9 光明觉（后）", "卷13", "所信果·**意业**·光遍", "十段遍照，穷法界", "三业毕，所信之境全彰"],
        ["10–12 问明·净行·贤首", "卷13–15", "十信之**解·行·德**", "由果转因", "本品为「果」之末二品，下三品入「因」"],
    ],
    "teshe_note": "本品之特色在**「结构最简而名相最密」**：序分仅一句，无请分，全品几无叙事，唯列名而已。以此读之，则知华严之「说」，有时不以义说而以名说。",
    "teshe": [
        ["名相密度（全经最高）", "3,262 字／440 名（约 7.4 字一名）", "第七品 3,226 字／211 名（约 15 字一名）", "两品合看，是第二会「以名说法」之两极"],
        ["结构负荷最轻", "序分一句、无请分、无偈颂", "第七品序分三段＋请分四十问", "品之轻重不在字数，在结构负荷"],
        ["四×十矩阵", "苦集灭道四行，行各十名，四方同构", "第九品十段为线性倍增", "一为矩阵，一为链；矩阵宜横读"],
        ["名与义之张力", "十名皆同一谛之侧显", "第七品十名乃一佛之异称", "同用「或名」，一显法、一显人"],
        ["校勘", "旧图八方界名系初稿遗留，已订正", "第七品密训九名、西北十一名", "图与经不合者，改图不改经"],
    ],
    "dufa5": [
        ["**谛读**", "只取四谛各首名（罪·繫縛·無諍·一乘）", "初读本篇者", "四谛之纲顷刻而得"],
        ["**名读**", "逐行读十名，比其侧显", "好名相者", "见「一名一义」之训释法"],
        ["**方读**", "只读十方世界名与「各四十名」", "欲见遍周者", "得 400 之量级"],
        ["**数读**", "图 〇-2 ＋ §7.3 对看", "欲辨所举与实有者", "四数不复相碍"],
        ["**承读**", "§2.6 → 第九品 §2.1（足轮放光）", "欲见三业之转者", "见口业如何让位于意业"],
    ],
    "shu": [
        ["**T0 经文明文**", "「四百億十千名」", "`T10n0279` 卷十二·娑婆段结句", "每一世界之实有"],
        ["**T0 经文明文**", "「隨眾生心，悉令調伏」", "同上·品末", "立名之由（非数目）"],
        ["**T0 本文实测**", "**440 名**（40＋400）", "§7.3「或名」计数", "计数（本文自测）"],
        ["**T0 本文实测**", "3,262 字・句末 116・独字 427", "§7.1 脚本", "计数（本文自测）"],
        ["**T1 澄观《疏》**", "「約一界一諦即有十千。娑婆四諦有四百億十千名」", "`T1735` 本品段", "注疏所定之数"],
        ["**T1 法藏《探玄记》**", "「四諦品明佛口業普周」", "`T1733`", "三业分判之据"],
        ["**T2 旧图**", "八方界名（親慧·有師子·妙觀察·喜樂·甚堅牢·妙地·焰慧·持地）", "初稿遗留·与 §2.5 实界名不合", "负面证据，已订正不采用"],
    ],
    "shu_note": "> **〔读法〕** 四数之辨，是本篇第一道关：**40 与 400 是「列名之数」，440 是「通计列名之数」，四百亿十千是「每界实有之数」**。前三是采样，后一是法界。读佛经数目，最忌以采样当法界、以法界疑采样。",
}

# ----------------------------------------------------------------------------
# 第九部　光明觉品
# ----------------------------------------------------------------------------
P9 = {
    "tag": "P9",
    "path": os.path.join(DIR2, "华严经细读_第九部_光明觉品.md"),
    "hui": "第二会（普光明殿·说十信）",
    "dingwei": "本品以「光」为法，读法当**循光而读**：光之所至即法之所至，段段倍增而偈偈不同；**读光即读位，读偈即读义**。",
    "yiju": "**一光放出，十段遍照；界增十倍而光未尝动**——此品无问而说，以现量境代言说。",
    "sanwen": "① 十段之数（十·百·千……）是渐次照还是同时顿照？② 十段各一偈，偈义何以配段？③ 何以此品全无当机请问者？",
    "tiyao": "全品**剥校勘 CJK 4,358 字**（含品题），含标点 5,198，句末 **151**，独字 492。结构三科：**序分**（足轮放光·照此三千大千·别显所照二十目·本会现相＋佛神力召十大菩萨）→**正宗分十段**（T1–T10，每段「长行现境＋一偈赞述」二拍，偈前公式全品一律）→**结分**（第十重穷尽法界，更无结经语，直接过渡问明品）。**全品无当机请问者**，是纯粹的「现相—颂述」结构，与次品《问明》之「设难—酬解」恰成对照。",
    "xufa": "先观图 〇-1 得十段之数与「一放顿照」之别，次观图 〇-2 得十偈义趣之三分，次读〇之二.3 之坐标，然后入 §二逐段。**数与义分看，则光不徒为瑞。**",
    "en_map": "Light from the soles of the Buddha's feet fills three thousand great thousand-worlds; then the same light is said to pass to ten Buddha-lands, a hundred, a thousand … up to a hundred billion nayutas, until it exhausts the dharma-realm. Ten stages, ten verses, one formula. Fig. 0-1 plots the tenfold cascade on a logarithmic scale; Fig. 0-2 divides the ten verses into five on awakening, one on majestic power, four on dharma-nature.",
    "figs": [
        {
            "n": 1,
            "title": "十段遍照倍增图（对数刻度）",
            "what": "光至何处",
            "one": "T1 此界 → T10 百億那由他·穷法界；界增十倍，光不动",
            "svg": """<svg viewBox="0 0 1000 520" width="100%" style="max-width:1000px;height:auto" xmlns="http://www.w3.org/2000/svg" font-family="serif">
<text x="500" y="24" text-anchor="middle" font-size="14.5" font-weight="bold" fill="#7a5a28">十段遍照：界增十倍，而光未尝动</text>
<text x="500" y="44" text-anchor="middle" font-size="12" fill="#8a7a5e">条长按 log₁₀ 比例（1→10⁹ 压缩为等距递增），故「十倍」在图中恒为一格</text>

<line x1="250" y1="470" x2="250" y2="66" stroke="#e0d6c2"/>
<text x="18" y="80" font-size="11.5" fill="#8a7a5e">段·偈</text>

<g font-size="12" fill="#5a5147">
<text x="18" y="96">T1</text><rect x="250" y="84" width="26" height="18" fill="#e6dbc5" stroke="#c9b98f"/><text x="288" y="98" font-size="11.5">此三千大千世界（一界）</text>
<text x="18" y="136">T2</text><rect x="250" y="124" width="44" height="18" fill="#e6dbc5" stroke="#c9b98f"/><text x="306" y="138" font-size="11.5">東方十佛國土 · 10</text>
<text x="18" y="176">T3</text><rect x="250" y="164" width="62" height="18" fill="#e6dbc5" stroke="#c9b98f"/><text x="324" y="178" font-size="11.5">百 · 100</text>
<text x="18" y="216">T4</text><rect x="250" y="204" width="80" height="18" fill="#e6dbc5" stroke="#c9b98f"/><text x="342" y="218" font-size="11.5">千 · 1,000</text>
<text x="18" y="256">T5</text><rect x="250" y="244" width="98" height="18" fill="#e6dbc5" stroke="#c9b98f"/><text x="360" y="258" font-size="11.5">十千 · 10,000</text>
<text x="18" y="296">T6</text><rect x="250" y="284" width="116" height="18" fill="#e6dbc5" stroke="#c9b98f"/><text x="378" y="298" font-size="11.5">百千 · 100,000</text>
<text x="18" y="336">T7</text><rect x="250" y="324" width="134" height="18" fill="#e6dbc5" stroke="#c9b98f"/><text x="396" y="338" font-size="11.5">百萬 · 10⁶</text>
<text x="18" y="376">T8</text><rect x="250" y="364" width="152" height="18" fill="#e6dbc5" stroke="#c9b98f"/><text x="414" y="378" font-size="11.5">一億 · 10⁸</text>
<text x="18" y="416">T9</text><rect x="250" y="404" width="170" height="18" fill="#e6dbc5" stroke="#c9b98f"/><text x="432" y="418" font-size="11.5">十億 · 10⁹</text>
<text x="18" y="456">T10</text><rect x="250" y="444" width="200" height="18" fill="#f7ecd2" stroke="#b8863c" stroke-width="1.4"/><text x="462" y="458" font-size="11.5" font-weight="bold" fill="#7a5a28">百億那由他 → 穷法界（无量）</text>
</g>

<line x1="470" y1="66" x2="470" y2="470" stroke="#e0d6c2" stroke-dasharray="4 5"/>
<text x="486" y="96" font-size="11.5" fill="#8a7a5e">每段皆「長行現境＋一偈贊述」二拍</text>
<text x="486" y="136" font-size="11.5" fill="#8a7a5e">偈前公式全品一律：</text>
<text x="486" y="156" font-size="11.5" fill="#5a5147">「爾時，一切處文殊師利菩薩，</text>
<text x="486" y="176" font-size="11.5" fill="#5a5147">各於佛所，同時發聲，說此頌言」×10</text>
<text x="486" y="216" font-size="11.5" fill="#8a7a5e">※ 「過此世界」而非「次第行至」——</text>
<text x="486" y="236" font-size="11.5" fill="#8a7a5e">光不动，境界自尔增广。〔本文判断〕</text>
<text x="486" y="276" font-size="11.5" fill="#8a7a5e">※ 十段无问而说，故无「云何」句；</text>
<text x="486" y="296" font-size="11.5" fill="#8a7a5e">问号 ×0（与次品问明之十问相反）。</text>
<text x="486" y="336" font-size="11.5" fill="#8a7a5e">※ 李通玄以「光位」表「位次」：</text>
<text x="486" y="356" font-size="11.5" fill="#8a7a5e">足轮放光→成信位；十住足指端放光。</text>
<text x="486" y="396" font-size="11.5" fill="#8a7a5e">※ 第十重「穷尽法界」而无结经语，</text>
<text x="486" y="416" font-size="11.5" fill="#8a7a5e">直接过渡问明品——三业段至此毕。</text>
</svg>""",
            "cap": "十段以对数刻度并列，故「十倍」恒为一格，读者可一眼见其**等比而非等差**。**T1 是「照此三千大千世界」，T2 起是「光明過此世界，遍照東方十佛國土」——「过」字非「行至」，乃「不复局此」**；光未尝移，而所照之境自尔开广。〔本文判断〕图右四注，即读此品之四把钥匙。",
            "en": "Ten stages on a logarithmic axis, so that each tenfold leap occupies one equal step: the cascade is geometric, not arithmetic. T1 lights this world; from T2 the light is said to *pass beyond* — not to travel, but to be no longer confined. The light does not move; the field it discloses widens.",
            "dufa": [
                "**「过」不是「行」。** 若读作光从此界行至彼界，则十段成行程；读作「不复局此」，则十段成开显。**一读成渐，一读成顿**，此本品第一大关。",
                "**十段之数，是「所照之境」之数，非「光」之数。** 光一，境十；**以一光摄十境，正是华严「一即一切」之现量版**。",
                "**无问而说，故无「云何」。** 本品问号 ×0，次品问明「云何」×20——**同一会中，一以境示、一以言诘**，读者当知此二体之分。",
            ],
        },
        {
            "n": 2,
            "title": "十偈义趣配段图",
            "what": "偈说什么",
            "one": "初五菩提 · 次一威德 · 后四法性（依澄观科）",
            "svg": """<svg viewBox="0 0 1000 420" width="100%" style="max-width:1000px;height:auto" xmlns="http://www.w3.org/2000/svg" font-family="serif">
<text x="500" y="26" text-anchor="middle" font-size="14.5" font-weight="bold" fill="#7a5a28">十偈三科：五菩提 · 一威德 · 四法性</text>
<text x="500" y="48" text-anchor="middle" font-size="12" fill="#8a7a5e">依澄观《疏》科（`T1735`@151418 起·§5.1）；段号与图 〇-1 同一坐标</text>

<rect x="40" y="90" width="450" height="60" fill="#f3ecdf" stroke="#c9b98f"/>
<text x="265" y="116" text-anchor="middle" font-size="13" font-weight="bold" fill="#7a5a28">初五偈 · 菩提</text>
<text x="265" y="138" text-anchor="middle" font-size="11.5" fill="#5a5147">超情 · 因果 · 八相 · 体性 · 业用</text>

<rect x="500" y="90" width="90" height="60" fill="#f7ecd2" stroke="#b8863c"/>
<text x="545" y="116" text-anchor="middle" font-size="12.5" font-weight="bold" fill="#7a5a28">次一</text>
<text x="545" y="138" text-anchor="middle" font-size="11" fill="#5a5147">威德</text>

<rect x="600" y="90" width="360" height="60" fill="#ede4d2" stroke="#c9b98f"/>
<text x="780" y="116" text-anchor="middle" font-size="13" font-weight="bold" fill="#7a5a28">后四偈 · 法性</text>
<text x="780" y="138" text-anchor="middle" font-size="11.5" fill="#5a5147">离相 · 一多 · 方便 · 圆遍</text>

<g font-size="11.5" fill="#5a5147" text-anchor="middle">
<text x="90" y="186">T1</text><text x="180" y="186">T2</text><text x="270" y="186">T3</text><text x="360" y="186">T4</text><text x="450" y="186">T5</text><text x="545" y="186">T6</text><text x="650" y="186">T7</text><text x="737" y="186">T8</text><text x="824" y="186">T9</text><text x="911" y="186">T10</text>
</g>
<g stroke="#c9b98f">
<line x1="90" y1="196" x2="90" y2="230"/><line x1="180" y1="196" x2="180" y2="230"/><line x1="270" y1="196" x2="270" y2="230"/><line x1="360" y1="196" x2="360" y2="230"/><line x1="450" y1="196" x2="450" y2="230"/><line x1="545" y1="196" x2="545" y2="230"/><line x1="650" y1="196" x2="650" y2="230"/><line x1="737" y1="196" x2="737" y2="230"/><line x1="824" y1="196" x2="824" y2="230"/><line x1="911" y1="196" x2="911" y2="230"/>
</g>
<g font-size="11" fill="#8a7a5e" text-anchor="middle">
<text x="90" y="250">超情</text><text x="180" y="250">因果</text><text x="270" y="250">八相</text><text x="360" y="250">体性</text><text x="450" y="250">业用</text><text x="545" y="250">威德智身</text><text x="650" y="250">内外包摄</text><text x="737" y="250">方便权实</text><text x="824" y="250">大悲救摄</text><text x="911" y="250">因果圆遍</text>
</g>

<line x1="40" y1="290" x2="960" y2="290" stroke="#e0d6c2"/>
<text x="40" y="316" font-size="12" fill="#7a5a28">义脉：<tspan font-weight="bold">由「超情」而入「因果」，由「体性」而出「业用」；末四偈再由「离相」而「一多」而「方便」而「圆遍」——两度自内而外。</tspan></text>
<text x="40" y="344" font-size="11.5" fill="#8a7a5e">※ 「初五·次一·后四」是澄观科，非经文自标；本文照录其科，不代为改并。</text>
<text x="40" y="368" font-size="11.5" fill="#8a7a5e">※ 十偈皆五言（每偈四句），与第七、八品之纯长行判然；此第二会文体之第一次转换。</text>
<text x="40" y="392" font-size="11.5" fill="#8a7a5e">※ 偈随段出：段增则境广，境广则偈之义亦由「佛身」而「法性」——<tspan fill="#7a5a28">文随境转，非境随文设</tspan>。〔本文判断〕</text>
</svg>""",
            "cap": "十偈三段：初五明菩提（超情·因果·八相·体性·业用），次一明威德智身，后四明法性（离相·一多·方便·圆遍）。**两度自内而外**：先由体出用，再由相入遍。此科出澄观《疏》，本文照录不改；**图只示其次第，不断其优劣**。",
            "en": "Ten verses in three sections: five on awakening (beyond concepts, causality, the eight phases, essence, function), one on majestic wisdom-body, four on dharma-nature (beyond marks, one-and-many, skilful means, universal reach). Twice the movement runs from within outward. The division is Chengguan's, reproduced, not adjudicated.",
            "dufa": [
                "**偈不是长行的复述。** 长行说「光照何处」，偈说「何以为光」；**一为事，一为理**，合之乃全。",
                "**「初五次一后四」是注疏之科，当与经文分书。** 图中标「依澄观科」，即不许以科文冒充经文——此全篇之通例。",
                "**十偈同式而不同义，正示「一法多门」。** 同一光明，或说为菩提，或说为威德，或说为法性；**非光有三，说者有三**。",
            ],
        },
    ],
    "weici_note": "本品为第二会第三品，**三业之末**：名号明身业、四谛明口业、本品明意业。澄观判「上來三品，答初十句所依果問竟」——**所信之果至此而毕，下三品转入能信之行**。",
    "weici": [
        ["7 名号（前二）", "卷12", "所信果·身业", "211 名，名遍", "同属「果」段"],
        ["8 四圣谛（前一）", "卷12", "所信果·口业", "440 名，法遍", "同属「果」段"],
        ["**9 光明觉（本品）**", "卷13", "所信果·**意业**", "十段遍照，光遍", "三业之毕，果境之终"],
        ["10 问明（次）", "卷13", "十信之**解**", "九首递问", "由果转因之枢"],
        ["11–12 净行·贤首", "卷14–15", "十信之**行·德**", "141 誓／717 颂行", "解→行→德"],
    ],
    "teshe_note": "本品之特色在**「无问而说」**：全品无当机者，佛以身光现境，文殊以智光赞述。此在三十九品中不多见，读法亦当随之而变——**不当求其「答何问」，只当观其「现何境」**。",
    "teshe": [
        ["无当机请问", "问号 ×0；全品「现相—颂述」", "第十品「云何」×20，纯问答体", "一以境示，一以言诘"],
        ["文体转折", "长行＋偈（十段各一偈，五言）", "第七、八品纯长行，无偈", "第二会文体之第一次转换"],
        ["等比之数", "十·百·千·十千·百千·百萬·億·十億·百億那由他", "第八品为 4×10 矩阵（等差之列）", "一为链，一为阵"],
        ["公式复沓", "偈前公式 ×10，一字不易", "第七品「或名」×211", "复沓即结构"],
        ["界标风险", "「光明覺品第九」全档唯一见；旧导出有多余见，系目录泄漏", "第十品品题唯一见 @115815", "定界须防「征引串」，见 §7.4"],
    ],
    "dufa5": [
        ["**光读**", "只读十段长行，不读偈", "初读本篇者", "得「一放顿照」之现量"],
        ["**偈读**", "只读十偈，参图 〇-2 之三科", "欲见义趣者", "得「由体出用」之义脉"],
        ["**数读**", "图 〇-1 ＋ §7.3 数法链", "好结构者", "见等比与等差之别"],
        ["**校读**", "§7.4 界标鉴别 ＋ §6.1 六十对读", "欲核文本者", "得唯一见与泄漏见之辨"],
        ["**承读**", "本品 §2.12 → 第十品 §2.1", "欲见三业转因者", "见「现相」如何让位于「设难」"],
    ],
    "shu": [
        ["**T0 经文明文**", "「百億光明」「百億閻浮提……百億色究竟天」", "`T10n0279` 卷十三·序分", "喻限数"],
        ["**T0 经文明文**", "「遍照東方十佛國土」等九段", "同上·T2–T10", "所照之境（等比）"],
        ["**T0 本文实测**", "4,358 字・句末 151・独字 492", "§7.4 脚本", "计数（本文自测）"],
        ["**T0 本文实测**", "十段・偈 ×10・偈前公式 ×10", "§7.4 实测", "计数（本文自测）"],
        ["**T1 澄观《疏》**", "「上來三品，答初十句所依果問竟」", "`T1735` 卷十三末", "判教定位"],
        ["**T1 慧苑**", "「初光明覺品來，明所依所信之境」", "`X0221`@48636", "与澄观同判"],
        ["**T1 李通玄**", "以光位表位次（足轮→成信位）", "`T1739`", "一家之判，非经证"],
    ],
    "shu_note": "> **〔读法〕** 本品之数，惟「十段」「十偈」为结构之数（可数），「百億」「那由他」为喻限之数（不可数）。**结构之数用以定段，喻限之数用以显遍**；二者混读，则十段与百亿相讥而两失。",
}

# ----------------------------------------------------------------------------
# 第十部　菩萨问明品
# ----------------------------------------------------------------------------
P10 = {
    "tag": "P10",
    "path": os.path.join(DIR2, "华严经细读_第十部_菩萨问明品.md"),
    "hui": "第二会（普光明殿·说十信）",
    "dingwei": "本品为十信之**解**门，读法当**以问为纲**：九首递问、文殊总酬，一问一答各成一义，而诸义同出一宗——「各各不相知」。",
    "yiju": "**心性差别，各各不相知；而一能应多，差别在机**——此十四字，为本品立宗，亦为下二品（行·德）之基。",
    "sanwen": "① 九首何以各问一义，其次第是随意的还是有骨的？② 「各各不相知」何以能成立「一能应多」？③ 本品何故无三昧、无普贤、无放光，与前后品判然两体？",
    "tiyao": "本品**剥校勘 CJK 3,133 字**（含标点 3,839），六十侧 3,088 字。全品为**十一「爾時」段**：九段文殊别问九首菩萨（各以偈答）、一段诸菩萨反问文殊（文殊以偈答）、一段佛神力遍照结归。偈颂「頌」×10（九酬＋文殊一酬），答式一律作「以頌答曰」。**问答体、无三昧名、无普贤**——与光明觉之「叙述—颂」二声部不同，本品是纯粹的「设难—酬解」结构。",
    "xufa": "先观图 〇-1 得十一「爾時」段之骨架，次观图 〇-2 得九问归一宗之义脉，次读〇之二.3 之坐标，然后入 §二逐段。**先见其骨，再味其偈。**",
    "en_map": "Eleven 「爾時」 units: nine bodhisattvas questioned by Mañjuśrī, each answering in verse; then the assembly questions Mañjuśrī, who answers in verse; then a closing line of Buddha-power. Ten verse-answers, no samādhi, no Samantabhadra, no light — a pure structure of challenge and reply. Fig. 0-1 lays out the eleven units; Fig. 0-2 traces the nine questions back to their single thesis: minds differ and none knows another.",
    "figs": [
        {
            "n": 1,
            "title": "十一「爾時」段骨架图",
            "what": "问如何成篇",
            "one": "九问九答 → 一反问一总答 → 一结归；十颂而止",
            "svg": """<svg viewBox="0 0 1000 470" width="100%" style="max-width:1000px;height:auto" xmlns="http://www.w3.org/2000/svg" font-family="serif">
<text x="500" y="24" text-anchor="middle" font-size="14.5" font-weight="bold" fill="#7a5a28">十一「爾時」段：九酬 · 一总酬 · 一结归</text>
<text x="500" y="44" text-anchor="middle" font-size="12" fill="#8a7a5e">答式一律「以頌答曰」×10（§7.4 实测）；无三昧名、无普贤、无放光</text>

<rect x="30" y="70" width="120" height="330" rx="5" fill="#f3ecdf" stroke="#c9b98f"/>
<text x="90" y="96" text-anchor="middle" font-size="12.5" font-weight="bold" fill="#7a5a28">文殊師利</text>
<text x="90" y="116" text-anchor="middle" font-size="11" fill="#8a7a5e">能问之主</text>
<text x="90" y="220" text-anchor="middle" font-size="11" fill="#5a5147">九问皆自此出</text>
<text x="90" y="300" text-anchor="middle" font-size="11" fill="#5a5147">末为诸菩萨</text>
<text x="90" y="318" text-anchor="middle" font-size="11" fill="#5a5147">所反问，而自答</text>

<g font-size="11.5" fill="#5a5147">
<rect x="190" y="74" width="300" height="30" fill="#fff" stroke="#d9cdb8"/><text x="200" y="94">一 · 覺首 — 心性差別·各各不相知</text>
<rect x="190" y="108" width="300" height="30" fill="#faf7f0" stroke="#d9cdb8"/><text x="200" y="128">二 · 財首 — 眾生非眾生·隨緣而化</text>
<rect x="190" y="142" width="300" height="30" fill="#fff" stroke="#d9cdb8"/><text x="200" y="162">三 · 寶首 — 四大無我·業性九喻</text>
<rect x="190" y="176" width="300" height="30" fill="#faf7f0" stroke="#d9cdb8"/><text x="200" y="196">四 · 德首 — 一法而無量·地火海風</text>
<rect x="190" y="210" width="300" height="30" fill="#fff" stroke="#d9cdb8"/><text x="200" y="230">五 · 目首 — 福田一等·果報差別</text>
<rect x="190" y="244" width="300" height="30" fill="#faf7f0" stroke="#d9cdb8"/><text x="200" y="264">六 · 勤首 — 一教何以不即斷結</text>
<rect x="190" y="278" width="300" height="30" fill="#fff" stroke="#d9cdb8"/><text x="200" y="298">七 · 法首 — 受持正法而不斷煩惱</text>
<rect x="190" y="312" width="300" height="30" fill="#faf7f0" stroke="#d9cdb8"/><text x="200" y="332">八 · 智首 — 智為上首·六度隨病</text>
<rect x="190" y="346" width="300" height="30" fill="#fff" stroke="#d9cdb8"/><text x="200" y="366">九 · 賢首 — 一道出離·佛土萬殊</text>
</g>

<g stroke="#c9b98f">
<line x1="150" y1="89" x2="190" y2="89"/><line x1="150" y1="123" x2="190" y2="123"/><line x1="150" y1="157" x2="190" y2="157"/><line x1="150" y1="191" x2="190" y2="191"/><line x1="150" y1="225" x2="190" y2="225"/><line x1="150" y1="259" x2="190" y2="259"/><line x1="150" y1="293" x2="190" y2="293"/><line x1="150" y1="327" x2="190" y2="327"/><line x1="150" y1="361" x2="190" y2="361"/>
</g>

<text x="510" y="96" font-size="11.5" fill="#8a7a5e">每段皆「爾時，文殊師利菩薩問 X 菩薩言」</text>
<text x="510" y="116" font-size="11.5" fill="#8a7a5e">→「時，X 菩薩以頌答曰」</text>
<text x="510" y="146" font-size="11.5" fill="#8a7a5e">※ 九首之名皆以「首」结：</text>
<text x="510" y="166" font-size="11.5" fill="#5a5147">覺·財·寶·德·目·勤·法·智·賢</text>
<text x="510" y="186" font-size="11.5" fill="#8a7a5e">——名即所答之法，非随便安立。〔本文判断〕</text>

<rect x="510" y="214" width="440" height="60" rx="4" fill="#f7ecd2" stroke="#b8863c"/>
<text x="524" y="236" font-size="12" font-weight="bold" fill="#7a5a28">段十 · 诸菩萨反问文殊</text>
<text x="524" y="258" font-size="11.5" fill="#5a5147">「佛境界」十一问 → 文殊以颂总答</text>

<rect x="510" y="286" width="440" height="46" rx="4" fill="#ede4d2" stroke="#c9b98f"/>
<text x="524" y="306" font-size="12" font-weight="bold" fill="#7a5a28">段十一 · 长行结归</text>
<text x="524" y="324" font-size="11.5" fill="#5a5147">佛神力遍照 · 十方世界六种震动</text>

<text x="510" y="372" font-size="11.5" fill="#8a7a5e">※ 十颂而止：九酬＋一总酬。「頌」×10 整齐，</text>
<text x="510" y="392" font-size="11.5" fill="#8a7a5e">初稿记「×7 不齐」系 XML 换行空白假象（§6.1）。</text>
<text x="510" y="418" font-size="11.5" fill="#8a7a5e">※ 无三昧、无普贤、无放光——本品之「无」，</text>
<text x="510" y="438" font-size="11.5" fill="#8a7a5e">正是其「有」：一切让位于问答。</text>
</svg>""",
            "cap": "十一「爾時」段：九段一问一答，第十段反转为「诸菩萨问、文殊答」，第十一段以长行结归。**结构之妙在第十段之反转**——问者变为被问者，九首之义遂总摄于文殊一答。**九首之名皆以「首」结，名即所答之法**（觉·财·宝·德·目·勤·法·智·贤）〔本文判断〕。",
            "en": "Eleven units: nine questions with nine verse-answers, then a reversal in which the assembly questions Mañjuśrī, then a prose close. The reversal is the structural pivot — the questioner becomes the respondent, and the nine answers gather into one. Each questioner's name ends in 首, \"chief\", and names the dharma he answers with.",
            "dufa": [
                "**九段是「平面」的，第十段才是「立体」的。** 前九段并列而不相属，第十段一出，九义始有总摄；**故读本品，当先读第十段，再回读前九段**。",
                "**名即法：九首之名不可滑过。** 觉首答「觉」，勤首答「勤」，法首答「法」——**华严之命名，非标识而是表法**。",
                "**「无」亦是结构。** 无三昧、无普贤、无放光，非经之缺，乃体之择：**问明之体，唯在言说**。",
            ],
        },
        {
            "n": 2,
            "title": "九问归一宗图",
            "what": "义归何处",
            "one": "九义同出「各各不相知」，终归「佛境界」",
            "svg": """<svg viewBox="0 0 1000 500" width="100%" style="max-width:1000px;height:auto" xmlns="http://www.w3.org/2000/svg" font-family="serif">
<text x="500" y="24" text-anchor="middle" font-size="14.5" font-weight="bold" fill="#7a5a28">九问归一宗：各各不相知 → 一能应多 → 佛境界</text>
<text x="500" y="46" text-anchor="middle" font-size="12" fill="#8a7a5e">中列为九段所答之义，左为所破之执，右为所显之宗（〔本文判断〕据 §4.1–4.5 归纳）</text>

<rect x="330" y="66" width="340" height="56" rx="5" fill="#f7ecd2" stroke="#b8863c" stroke-width="1.4"/>
<text x="500" y="90" text-anchor="middle" font-size="13" font-weight="bold" fill="#7a5a28">宗：心性差別 · 各各不相知</text>
<text x="500" y="110" text-anchor="middle" font-size="11.5" fill="#5a5147">段一 · 覺首（本品立宗）</text>

<g font-size="11.5" fill="#5a5147">
<rect x="40" y="146" width="260" height="40" fill="#f8f3ea" stroke="#d9cdb8"/><text x="52" y="171">破「众生实有」→ 段二 財首</text>
<rect x="40" y="196" width="260" height="40" fill="#f8f3ea" stroke="#d9cdb8"/><text x="52" y="221">破「四大是我」→ 段三 寶首</text>
<rect x="40" y="246" width="260" height="40" fill="#f8f3ea" stroke="#d9cdb8"/><text x="52" y="271">破「一法是一」→ 段四 德首</text>
<rect x="40" y="296" width="260" height="40" fill="#f8f3ea" stroke="#d9cdb8"/><text x="52" y="321">破「福田不平等」→ 段五 目首</text>
</g>

<g font-size="11.5" fill="#5a5147">
<rect x="700" y="146" width="260" height="40" fill="#ede4d2" stroke="#c9b98f"/><text x="712" y="171">显「随缘而化」</text>
<rect x="700" y="196" width="260" height="40" fill="#ede4d2" stroke="#c9b98f"/><text x="712" y="221">显「业性如幻」</text>
<rect x="700" y="246" width="260" height="40" fill="#ede4d2" stroke="#c9b98f"/><text x="712" y="271">显「一法无量」</text>
<rect x="700" y="296" width="260" height="40" fill="#ede4d2" stroke="#c9b98f"/><text x="712" y="321">显「果报在机」</text>
</g>

<line x1="300" y1="166" x2="700" y2="166" stroke="#e0d6c2"/><line x1="300" y1="216" x2="700" y2="216" stroke="#e0d6c2"/><line x1="300" y1="266" x2="700" y2="266" stroke="#e0d6c2"/><line x1="300" y1="316" x2="700" y2="316" stroke="#e0d6c2"/>

<g font-size="11.5" fill="#5a5147">
<rect x="40" y="346" width="260" height="40" fill="#f8f3ea" stroke="#d9cdb8"/><text x="52" y="371">破「闻教即断」→ 段六 勤首</text>
<rect x="40" y="396" width="260" height="40" fill="#f8f3ea" stroke="#d9cdb8"/><text x="52" y="421">破「受持即证」→ 段七 法首</text>
<rect x="40" y="446" width="260" height="40" fill="#f8f3ea" stroke="#d9cdb8"/><text x="52" y="471">破「一法独尊」→ 段八 智首</text>
</g>
<g font-size="11.5" fill="#5a5147">
<rect x="700" y="346" width="260" height="40" fill="#ede4d2" stroke="#c9b98f"/><text x="712" y="371">显「功在积渐」</text>
<rect x="700" y="396" width="260" height="40" fill="#ede4d2" stroke="#c9b98f"/><text x="712" y="421">显「解须起行」</text>
<rect x="700" y="446" width="260" height="40" fill="#ede4d2" stroke="#c9b98f"/><text x="712" y="471">显「智为上首·随病设药」</text>
</g>
<line x1="300" y1="366" x2="700" y2="366" stroke="#e0d6c2"/><line x1="300" y1="416" x2="700" y2="416" stroke="#e0d6c2"/><line x1="300" y1="466" x2="700" y2="466" stroke="#e0d6c2"/>

<rect x="330" y="146" width="340" height="300" fill="none" stroke="#b8863c" stroke-dasharray="6 5"/>
<text x="500" y="180" text-anchor="middle" font-size="12" fill="#b8863c">段九 · 賢首：一道出離而佛土萬殊</text>
<text x="500" y="210" text-anchor="middle" font-size="11.5" fill="#8a7a5e">——「各各不相知」之极致：</text>
<text x="500" y="230" text-anchor="middle" font-size="11.5" fill="#8a7a5e">道一而土万，佛一而机万</text>
<text x="500" y="262" text-anchor="middle" font-size="11.5" fill="#8a7a5e">八义既立，终以「佛境界」</text>
<text x="500" y="282" text-anchor="middle" font-size="11.5" fill="#8a7a5e">十一问收之（段十）</text>
<text x="500" y="314" text-anchor="middle" font-size="11.5" fill="#8a7a5e">→ 佛神力遍照（段十一）</text>
<text x="500" y="352" text-anchor="middle" font-size="11.5" fill="#8a7a5e">※ 九义非九个道理，</text>
<text x="500" y="372" text-anchor="middle" font-size="11.5" fill="#8a7a5e">乃一理之九面：</text>
<text x="500" y="392" text-anchor="middle" font-size="11.5" fill="#7a5a28">所破者「同」，所显者「异」；</text>
<text x="500" y="412" text-anchor="middle" font-size="11.5" fill="#7a5a28">异而不碍同，故终归佛境。</text>
</svg>""",
            "cap": "左破右显，中为九段所答之义，末以「佛境界」收。**九义不是九个道理，而是一理之九面**：所破者「同」（众生实有、四大是我、一法是一、福田平等……），所显者「异」（随缘、如幻、无量、在机）。**异而不碍同，故终归佛境**〔本文判断〕。此图之义，可与 §4.1–4.5 互证。",
            "en": "Nine answers, one thesis. What is broken on the left is sameness — that beings are solid, that the four elements are self, that one dharma is one, that the field is equal; what is shown on the right is difference — arising by conditions, illusory karmic nature, the one dharma as measureless, fruit according to capacity. Difference without obstructing sameness: hence the close in Buddha-realm.",
            "dufa": [
                "**「各各不相知」不是断灭，是「不混」。** 心心有自有之相，故不相知；**不相知故能相即而不相乱**——此为下品「解」之根。",
                "**九问之次第，由境而心而教而智。** 前五问「法」，六七问「教」，八九问「行」与「智」——**次第非随意，乃自外而内、自解而行**。",
                "**终以「佛境界」十一问收者，示「解」之限。** 九义可解，佛境不可解；**故以问终，不以答终**。",
            ],
        },
    ],
    "weici_note": "本品为第二会第四品，**十信三品（解·行·德）之首**。前三品明所信之果（三业），本品以下转入能信之行——法藏「信中解行及德，明難辨解，居初故來」。",
    "weici": [
        ["7–9 名号·四谛·光明觉", "卷12–13", "所信果·三业", "身·口·意遍", "果境已毕"],
        ["**10 菩萨问明（本品）**", "卷13", "十信·**解**", "九首递问，文殊总酬", "解为行德之本，故居首"],
        ["11 净行", "卷14", "十信·**行**", "141 誓，遇事发愿", "解而后行"],
        ["12 贤首", "卷14–15", "十信·**德**", "信为道元功德母", "行而后德"],
    ],
    "teshe_note": "本品之特色在**「纯问答体」**：无三昧、无放光、无普贤、无动地，一切唯是言说。**在全部三十九品中，以如此纯粹的「设难—酬解」构成一整品者，唯此一品**〔本文判断·据本文所核诸品结构〕。",
    "teshe": [
        ["纯问答体", "十一「爾時」段，九问九答＋一反问一总答＋一结", "第九品无问而说，问号 ×0", "一以言诘，一以境示"],
        ["答式统一", "「以頌答曰」×10（剥空白口径整齐）", "第十二品问号 ×0，以偈问", "同是偈，一为答，一为问"],
        ["无三昧·无普贤", "全品三昧名 ×0，普贤 ×0", "第十五品法慧入无量方便定", "定在此品让位于慧"],
        ["立宗分明", "「各各不相知」一处立宗，九段分疏", "第十一品以「善用其心」一句总持", "一以理立，一以行立"],
        ["校勘", "「頌」×10 整齐；初稿「×7 不齐」系 XML 空白假象", "第九品界标有目录泄漏见", "文本现象须先辨器，后断经"],
    ],
    "dufa5": [
        ["**问读**", "只读九问之问句，不读答", "初读本篇者", "见九问之次第与所破"],
        ["**答读**", "只读九答之偈，参图 〇-2", "欲见义者", "见九义之一宗"],
        ["**喻读**", "取段三·段四·段五之喻，比较其喻法", "好文学者", "见「一法多喻」之巧"],
        ["**校读**", "§6.1 六十对读 ＋ §7.4 实测", "欲核文本者", "得「頌×10」之实"],
        ["**承读**", "本品 §4.1 → 第十一品 §2.2（善用其心）", "欲见解行相即者", "见「解」如何落地为「行」"],
    ],
    "shu": [
        ["**T0 经文明文**", "「以頌答曰」×10", "`T10n0279` 卷十三", "答式（结构标志）"],
        ["**T0 经文明文**", "「各各不相知」", "同上·段一", "本品立宗之句"],
        ["**T0 本文实测**", "3,133 字（含标点 3,839）", "§7.4 脚本", "计数（本文自测）"],
        ["**T0 本文实测**", "十一「爾時」段・頌 ×10", "§7.4 实测", "计数（本文自测）"],
        ["**T1 澄观《疏》**", "「三品明信有解行德。解為二本，此品先来」", "`T1735`@167350", "三品分判之据"],
        ["**T1 法藏《探玄记》**", "「明難辨解，居初故來」", "`T1733`@116220", "与澄观同判"],
        ["**T1 慧苑**", "本品无专段（存疑直证）", "`X0221`", "负面证据，如实记"],
    ],
    "shu_note": "> **〔读法〕** 本品之数最简：十一（段）、十（颂）、九（首）。**三段之数皆有对验**：段以「爾時」为界，颂以「以頌答曰」为界，首以名数为界——三界皆可复算，故 §7.4 之脚本能自证。",
}

# ----------------------------------------------------------------------------
# 第十一部　净行品
# ----------------------------------------------------------------------------
P11 = {
    "tag": "P11",
    "path": os.path.join(DIR2, "华严经细读_第十一部_净行品.md"),
    "hui": "第二会（普光明殿·说十信）",
    "dingwei": "本品为十信之**行**门，读法当**随事而读**：一百四十一誓，遇一事发一愿，自晨起盥漱至夜寐始寤，一日之历即全部修行。",
    "yiju": "**善用其心**四字，是全品之总持；一百四十一誓，只是此四字在日用中的一百四十一次落地。",
    "sanwen": "① 一百四十一誓何以分为十段，十段之次第依何而立？② 八十作 141、六十作 140，此一誓之差当如何处置？③ 全品无偈颂、纯长行问答，与问明品之偈答判然——何以故？",
    "tiyao": "本品八十侧**净身 CJK 2,968 字**（含标点 raw 3,719），六十侧《净行品第七》2,895 字。**全品为纯长行问答**：智首菩萨「二十云何」总问，文殊「一百四十一誓」别答，末以「如是用心，所不能动」结叹。实测**颂 ×0、偈 ×0**——与问明之「以颂答曰」偈颂酬答体判然不同。誓式一律作「……，當願眾生：……，……。」（八十侧「當願眾生」后全用冒号「：」·141 见；六十侧全用逗号「，」·140 见），**两译标点体式 0 交叉**。",
    "xufa": "先观图 〇-1 得十段之量与次第，次观图 〇-2 辨两译一誓之差，次读〇之二.3 之坐标，然后入 §二逐段。**数既定，然后味其愿。**",
    "en_map": "A chapter of pure prose: Zhi Shou asks twenty questions, Mañjuśrī answers with 141 vows, each triggered by an everyday act — waking, washing, walking, eating, sleeping. Not one verse in the whole chapter. The eighty-fascicle text has 141 vows, the sixty-fascicle text 140, and the punctuation of the vow-formula never crosses over between the two. Fig. 0-1 weighs the ten sections; Fig. 0-2 sets the one-vow difference side by side.",
    "figs": [
        {
            "n": 1,
            "title": "一百四十一誓十段量图",
            "what": "愿有多少",
            "one": "11·15·7·6·7·55·22·5·10·3＝141，段段与澄观疏家数全合",
            "svg": """<svg viewBox="0 0 1000 520" width="100%" style="max-width:1000px;height:auto" xmlns="http://www.w3.org/2000/svg" font-family="serif">
<text x="500" y="24" text-anchor="middle" font-size="14.5" font-weight="bold" fill="#7a5a28">一百四十一誓：十段之量（1 誓＝8px）</text>
<text x="500" y="44" text-anchor="middle" font-size="12" fill="#8a7a5e">实测数与澄观疏家数逐段全合（§7.4）；段名依澄观「長分為十」之科</text>

<g font-size="11.5" fill="#5a5147">
<text x="24" y="86">一 · 在家</text><rect x="150" y="70" width="88" height="22" fill="#e6dbc5" stroke="#c9b98f"/><text x="248" y="86" fill="#7a5a28">11</text>
<text x="24" y="122">二 · 出家受戒</text><rect x="150" y="106" width="120" height="22" fill="#e6dbc5" stroke="#c9b98f"/><text x="280" y="122" fill="#7a5a28">15</text>
<text x="24" y="158">三 · 坐禅观</text><rect x="150" y="142" width="56" height="22" fill="#e6dbc5" stroke="#c9b98f"/><text x="216" y="158" fill="#7a5a28">7</text>
<text x="24" y="194">四 · 披挂三衣</text><rect x="150" y="178" width="48" height="22" fill="#e6dbc5" stroke="#c9b98f"/><text x="208" y="194" fill="#7a5a28">6</text>
<text x="24" y="230">五 · 澡漱盥洗</text><rect x="150" y="214" width="56" height="22" fill="#e6dbc5" stroke="#c9b98f"/><text x="216" y="230" fill="#7a5a28">7</text>
<text x="24" y="266">六 · 乞食道行</text><rect x="150" y="250" width="440" height="22" fill="#f7ecd2" stroke="#b8863c" stroke-width="1.4"/><text x="600" y="266" font-weight="bold" fill="#7a5a28">55</text>
<text x="24" y="302">七 · 到城乞食</text><rect x="150" y="286" width="176" height="22" fill="#e6dbc5" stroke="#c9b98f"/><text x="336" y="302" fill="#7a5a28">22</text>
<text x="24" y="338">八 · 还归洗浴</text><rect x="150" y="322" width="40" height="22" fill="#e6dbc5" stroke="#c9b98f"/><text x="200" y="338" fill="#7a5a28">5</text>
<text x="24" y="374">九 · 讽诵旋礼</text><rect x="150" y="358" width="80" height="22" fill="#e6dbc5" stroke="#c9b98f"/><text x="240" y="374" fill="#7a5a28">10</text>
<text x="24" y="410">十 · 寤寐安息</text><rect x="150" y="394" width="24" height="22" fill="#e6dbc5" stroke="#c9b98f"/><text x="184" y="410" fill="#7a5a28">3</text>
</g>

<line x1="150" y1="430" x2="950" y2="430" stroke="#d3c7ae"/>
<text x="24" y="456" font-size="12.5" font-weight="bold" fill="#b8863c">合计 141</text>
<text x="120" y="456" font-size="12" fill="#5a5147">「當願眾生」×141（八十侧·实计）　·　问段「云何」×20（另答端起首 ×1，全品 ×21）</text>
<text x="24" y="482" font-size="11.5" fill="#8a7a5e">※ 段六独得 55 誓，占全品四成——「乞食道行」历时最久、触境最多，故愿亦最多。愿数随事，非随义。</text>
<text x="24" y="504" font-size="11.5" fill="#8a7a5e">※ 十段之次第即一日之次第：晨起→出家→坐禅→披衣→盥洗→入城→乞食→还归→诵礼→寝息。<tspan fill="#7a5a28">经之结构，即生活之结构</tspan>。</text>
</svg>""",
            "cap": "十条之量，一望而知：**段六「乞食道行」55 誓，独居其四成**；而首尾二段（在家 11、寤寐 3）皆短。愿数之多寡，随历时之久暂、触境之疏密，**非按义理分配**。十段之次第，即一日之次第——**经的结构就是生活的结构**〔本文判断〕。",
            "en": "Ten sections by weight. The sixth — begging and walking the road — holds fifty-five of the 141 vows, four tenths of the chapter; the first and last are short. The vows are distributed by how long an activity lasts and how many things it meets, not by doctrinal importance. The order of the ten sections is the order of a single day.",
            "dufa": [
                "**愿数随事，不随义。** 若以为 55 誓必关最胜之义，则误；**乞食道行历时最久、所见最多，故愿最多**——此华严「即事而真」之最朴素的证明。",
                "**一日即一生。** 十段自晨起至寝息，**循环一次即一日，循环一生即一生**；故读此品，不当作「举例」读，当作「日程」读。",
                "**誓式一律，而所对之境无一重复。** 141 次「當願眾生」，141 个不同情境——**同式而不同境，正是「善用其心」之法**。",
            ],
        },
        {
            "n": 2,
            "title": "两译一誓之差·体式对勘图",
            "what": "异译何别",
            "one": "八十 141／冒号；六十 140／逗号；0 交叉",
            "svg": """<svg viewBox="0 0 1000 440" width="100%" style="max-width:1000px;height:auto" xmlns="http://www.w3.org/2000/svg" font-family="serif">
<text x="500" y="24" text-anchor="middle" font-size="14.5" font-weight="bold" fill="#7a5a28">一誓之差与一体之异：八十 141／六十 140</text>
<text x="500" y="44" text-anchor="middle" font-size="12" fill="#8a7a5e">两译「當願眾生」计数与标点体式，实测 0 交叉（§6.1）</text>

<rect x="60" y="72" width="400" height="180" rx="5" fill="#f8f3ea" stroke="#c9b98f"/>
<text x="80" y="96" font-size="13" font-weight="bold" fill="#7a5a28">八十华严 · `T10n0279` 卷十四</text>
<text x="80" y="118" font-size="11.5" fill="#8a7a5e">实叉难陀译 · 本品为「淨行品第十一」</text>
<text x="80" y="152" font-size="12" fill="#5a5147">「當願眾生」</text>
<text x="212" y="152" font-size="13" font-weight="bold" fill="#b8863c">141</text>
<rect x="80" y="164" width="352" height="14" fill="#e6dbc5" stroke="#c9b98f"/><rect x="80" y="164" width="352" height="14" fill="#d9c9a4"/>
<text x="80" y="204" font-size="12" fill="#5a5147">式：<tspan font-family="monospace">「……，當願眾生：……，……。」</tspan></text>
<text x="80" y="226" font-size="11.5" fill="#8a7a5e">冒号「：」141 见　·　逗号「，」0 见</text>

<rect x="540" y="72" width="400" height="180" rx="5" fill="#f3ecdf" stroke="#c9b98f"/>
<text x="560" y="96" font-size="13" font-weight="bold" fill="#7a5a28">六十华严 · `T09n0278` 卷六</text>
<text x="560" y="118" font-size="11.5" fill="#8a7a5e">佛驮跋陀罗译 · 本品为「淨行品第七」</text>
<text x="560" y="152" font-size="12" fill="#5a5147">「當願眾生」</text>
<text x="692" y="152" font-size="13" font-weight="bold" fill="#b8863c">140</text>
<rect x="560" y="164" width="350" height="14" fill="#e6dbc5" stroke="#c9b98f"/>
<rect x="910" y="164" width="10" height="14" fill="none" stroke="#b8863c" stroke-dasharray="2 2"/>
<text x="560" y="204" font-size="12" fill="#5a5147">式：<tspan font-family="monospace">「……，當願眾生，……，……。」</tspan></text>
<text x="560" y="226" font-size="11.5" fill="#8a7a5e">逗号「，」140 见　·　冒号「：」0 见</text>

<line x1="60" y1="276" x2="960" y2="276" stroke="#e0d6c2"/>
<text x="60" y="302" font-size="12" fill="#7a5a28">一誓之差：六十少一誓（虚线处）。<tspan font-weight="bold">两译各照底本，不互补、不裁改、不统一。</tspan></text>
<text x="60" y="328" font-size="11.5" fill="#8a7a5e">旧说「一百四十一」出于疏家料简语（`T1736`@30159）与讲记，本篇不取旧说为准，而以底本逐誓实计——八十坐实 141，六十得 140。</text>
<text x="60" y="354" font-size="11.5" fill="#8a7a5e">※ 标点体式 0 交叉，是两译「译者之笔」最清晰的指纹：<tspan fill="#7a5a28">同为一事，一用冒号领起，一用逗号连读</tspan>。</text>
<text x="60" y="380" font-size="11.5" fill="#8a7a5e">※ 全品颂 ×0、偈 ×0（实测）；与问明「以頌答曰」×10、贤首偈颂为主，恰成第二会文体之三极。</text>
<text x="60" y="406" font-size="11.5" fill="#8a7a5e">※ 数之差须记，义之同须辨：<tspan fill="#7a5a28">一誓之失，不碍十段之同；十段之同，不掩一誓之失</tspan>。〔本文判断〕</text>
</svg>""",
            "cap": "两译并列，一誓之差以虚线标出。**八十 141（冒号）、六十 140（逗号），体式 0 交叉**——这不是谁对谁错，而是两支译笔各自的指纹。**故本篇不取旧说「一百四十一」为准，而以底本逐誓实计**：八十坐实 141，六十得 140。**异文各照底本，不互补、不裁改、不统一**——此为全篇铁律。",
            "en": "Two translations side by side, the single missing vow marked in dotted line. Eighty: 141 vows, colon after 「當願眾生」. Sixty: 140 vows, comma throughout. The punctuation never crosses over — a fingerprint of two translator-hands, not an error to be corrected. The rule: each witness stands as it stands; no filling in, no harmonising.",
            "dufa": [
                "**「少一誓」是文本事实，不是义理缺陷。** 记录它、标明它、不修补它——**负面的文本证据与正面的同样重要**。",
                "**标点亦是证据。** 冒号／逗号 0 交叉，说明两支译笔对「誓」的句法理解不同：一为「领起」，一为「连读」。**此非小节，乃译本之体质**。",
                "**与贤首品对看，见第二会文体之三极。** 净行纯长行（颂 0）、问明偈答（颂 10）、贤首偈颂为主（颂 1 而偈 3）——**同一会中，三品三体**。",
            ],
        },
    ],
    "weici_note": "本品为第二会第五品，**十信三品（解·行·德）之「行」**。李通玄判「又說光明覺品、菩薩問明品、淨行品、賢首品，成就十信之門」；澄观判净行「收前行願，成信德用」——**解而后行，行而后德**。",
    "weici": [
        ["9 光明觉", "卷13", "所信果·意业", "十段遍照", "果境之毕"],
        ["10 问明", "卷13", "十信·**解**", "九首递问", "解为行本"],
        ["**11 净行（本品）**", "卷14", "十信·**行**", "141 誓，遇事发愿", "解而后行"],
        ["12 贤首", "卷14–15", "十信·**德**", "信为道元功德母", "行而后德，十信满心"],
    ],
    "teshe_note": "本品之特色在**「纯长行而无偈」**：全部三十九品中，以一百四十一条同式誓愿构成一品、且不出一偈者，唯此一品〔本文判断·据本文所核诸品文体〕。其「行」不在玄谈，而在**漱口、着衣、见山、见河、入城、乞食、洗足、睡眠**。",
    "teshe": [
        ["纯长行", "颂 ×0、偈 ×0（实测）", "问明「以頌答曰」×10；贤首偈颂为主", "第二会文体之三极"],
        ["同式复沓", "「當願眾生」×141，式无二致", "第七品「或名」×211（名号复沓）", "一以愿复沓，一以名复沓"],
        ["数有异文", "八十 141／六十 140；冒号／逗号 0 交叉", "第八品名号 440 两译大体同", "异文处置之范例"],
        ["即事为道", "所对之境：家·戒·禅·衣·漱·道·食·归·塔·寝", "问明所对之境：心·法·业·福田", "一在境上修，一在理上解"],
        ["日用收束", "以「睡眠始寤，當願眾生：一切智覺，周顧十方」终", "贤首以「信为道元」总摄", "一以一日终，一以一信始"],
    ],
    "dufa5": [
        ["**段读**", "只读十段之首誓与末誓", "初读本篇者", "得一日之次第"],
        ["**愿读**", "逐愿读，遇己身所历之事即止", "欲起行者", "愿愿可落于今日"],
        ["**式读**", "只读 141 个「當願眾生」之后半句", "好文法者", "见「转事成愿」之句法"],
        ["**校读**", "§6.1 六十对读＋图 〇-2", "欲核异文者", "得 141／140 之实与体式之别"],
        ["**承读**", "本品 §2.4 → 第十二品 §2.2", "欲见行德相成者", "见「行」如何成「德」"],
    ],
    "shu": [
        ["**T0 经文明文**", "「當願眾生」×141（八十）", "`T10n0279` 卷十四", "誓数（本文实计，坐实旧说）"],
        ["**T0 经文明文**", "「云何」×20（问段）", "同上·问端", "问事数"],
        ["**T0 本文实测**", "2,968 字（CJK 净身）", "§7.4 脚本", "计数（本文自测）"],
        ["**T0 本文实测**", "十段 11·15·7·6·7·55·22·5·10·3", "§7.4 实测", "计数（本文自测）"],
        ["**T1 澄观《疏》**", "「淨行品百四十一願」「長分為十」", "`T1735`@193301；`T1736`@30159", "注疏之数，与实测全合"],
        ["**T1 法藏《探玄记》**", "「始終隨事發願無空過」", "`T1733`@134720", "释「即事」之旨"],
        ["**T2 讲记**", "承「一百四十一」之说", "海云继梦讲记", "转述，与底本实计合"],
    ],
    "shu_note": "> **〔读法〕** 本品之数有一特殊：**旧说（141）与实测（141）相合，而六十本（140）不合**。故本篇之立场为——**不因旧说而信，不因旧说而疑；以底本实计为准，两译各记其数**。此为「数须对验」之最典型一例。",
}

# ----------------------------------------------------------------------------
# 第十二部　贤首品
# ----------------------------------------------------------------------------
P12 = {
    "tag": "P12",
    "path": os.path.join(DIR2, "华严经细读_第十二部_贤首品.md"),
    "hui": "第二会（普光明殿·说十信）",
    "dingwei": "本品为第二会之**收官**，以偈颂为体，读法当**以颂为行、以链为脉**：七百一十七颂行，其骨在「信為道元功德母」一句，其肉在「若……則……」顶针一链。",
    "yiju": "**信為道元功德母，長養一切諸善法**——此十四字是全品宗眼；其后七百余颂，只是此一句的展转引申。",
    "sanwen": "① 全品偈颂为主，而疏家所计之颂数（359 半／357 半／715 半）何以三源分歧？② 「若……則……」顶针链何以能长达数十环而不乱？③ 本品为十信之「德」，与净行之「行」、问明之「解」，三品之分界安在？",
    "tiyao": "本品跨**卷第十四末至卷第十五**（起锚「賢首品第十二」首见 @124463，止锚「昇須彌山頂品第十三」@137665）。八十侧**净身 CJK 10,228 字**（剥空白 raw 11,694；之一 4,577＋之二 7,117），六十侧《賢首菩薩品第八》**10,159 字**（raw 11,633·跨 `juan6`／`juan7` 二拼接）——**两译仅差 69 字**，为全经两译篇幅最接近之品。全品**偈颂为主**：实测「頌」×**1**、「偈」×**3**，颂行 **717** 行（14 字行 ×716、13 字行 ×1），÷2＝**358.5 颂**；**问号 ×0**——文殊之问以偈托（「以偈問賢首菩薩曰」），不设「云何」句式。",
    "xufa": "先观图 〇-1 得颂行之量与三源口径之别，次观图 〇-2 得顶针一链之骨，次读〇之二.3 之坐标，然后入 §二逐段。**量既明，链既见，然后可读其颂。**",
    "en_map": "The closing chapter of the second assembly, and almost entirely verse: 717 verse-lines (716 of fourteen characters, one of thirteen), that is 358.5 ślokas — against Chengguan's 359.5, Huiyuan's 357.5, and Zhiyan's 715.5 counted by line in the sixty-fascicle recension. Three figures, one text: a difference of counting, not of length. The eighty- and sixty-fascicle versions differ by only 69 characters. Fig. 0-1 plots the verse-lines and the three reckonings; Fig. 0-2 follows the chain of 「若…則…」 from faith in the Buddhas to a body filling space.",
    "figs": [
        {
            "n": 1,
            "title": "颂行与两译计量图",
            "what": "量如何计",
            "one": "717 行 ÷2＝358.5 颂；三源 359.5／357.5／715.5；两译差 69 字",
            "svg": """<svg viewBox="0 0 1000 560" width="100%" style="max-width:1000px;height:auto" xmlns="http://www.w3.org/2000/svg" font-family="serif">
<text x="500" y="24" text-anchor="middle" font-size="14.5" font-weight="bold" fill="#7a5a28">七百一十七颂行：一行二句、二行一颂、三源三数</text>
<text x="500" y="44" text-anchor="middle" font-size="12" fill="#8a7a5e">数据源 `_e12_lines.py`（3 lg／717 l）＋§7.5；条长按 CJK 字数比例（1 字＝0.058px）</text>

<text x="30" y="80" font-size="13" font-weight="bold" fill="#7a5a28">① 颂行之形</text>
<rect x="150" y="64" width="416" height="22" fill="#e6dbc5" stroke="#c9b98f"/>
<text x="576" y="80" font-size="12" fill="#5a5147">14 字行 ×716（10,024 字）</text>
<rect x="150" y="90" width="1" height="22" fill="#b8863c"/>
<text x="160" y="106" font-size="12" fill="#5a5147">13 字行 ×1（L219「𢔌樂色者皆從道」·非 BMP 原字形照录）</text>
<text x="30" y="134" font-size="11.5" fill="#8a7a5e">颂行 CJK 10,037 ＋ 散文题头 191 ＝ 10,228（§7.4 全体守恒）</text>

<text x="30" y="176" font-size="13" font-weight="bold" fill="#7a5a28">② 三源口径</text>
<text x="30" y="196" font-size="11.5" fill="#8a7a5e">同一底本，三种计法；差在「颂／行」之口径，不在文本之多寡</text>
<g font-size="12" fill="#5a5147">
<text x="30" y="228">本文实测</text><rect x="150" y="214" width="358" height="20" fill="#f7ecd2" stroke="#b8863c" stroke-width="1.4"/><text x="518" y="229" font-weight="bold" fill="#7a5a28">358.5 颂（717 行 ÷2）</text>
<text x="30" y="258">澄观《疏》</text><rect x="150" y="244" width="359" height="20" fill="#e6dbc5" stroke="#c9b98f"/><text x="519" y="259">359.5 颂（差 +1）</text>
<text x="30" y="288">慧苑《刊定记》</text><rect x="150" y="274" width="357" height="20" fill="#e6dbc5" stroke="#c9b98f"/><text x="517" y="289">357.5 颂（差 −1）</text>
<text x="30" y="318">智俨《搜玄记》</text><rect x="150" y="304" width="715" height="20" fill="#ede4d2" stroke="#c9b98f"/><text x="875" y="319">715.5 偈（按行计·六十本）</text>
</g>
<text x="30" y="344" font-size="11.5" fill="#8a7a5e">※ 智俨之数近本文之二倍，非经文多寡，乃「一颂＝二行」与「一行＝一偈」之别。古数不裁。</text>

<text x="30" y="386" font-size="13" font-weight="bold" fill="#7a5a28">③ 两译对</text>
<g font-size="12" fill="#5a5147">
<text x="30" y="414">八十 `T10n0279`</text><rect x="170" y="400" width="593" height="20" fill="#e6dbc5" stroke="#c9b98f"/><text x="773" y="415" font-weight="bold" fill="#7a5a28">10,228</text>
<text x="30" y="444">六十 `T09n0278`</text><rect x="170" y="430" width="589" height="20" fill="#ede4d2" stroke="#c9b98f"/><text x="769" y="445" font-weight="bold" fill="#b8863c">10,159</text>
</g>
<text x="30" y="468" font-size="11.5" fill="#8a7a5e">※ 差 69 字——全经两译篇幅最接近之品。然用字之偏则大异：三昧 33／68、光明 94／57、菩提心 3／6。</text>

<line x1="30" y1="490" x2="970" y2="490" stroke="#d3c7ae"/>
<text x="30" y="516" font-size="12" fill="#7a5a28">体式：颂 ×1 · 偈 ×3 · 问号 ×0（「。」312·「，」1,001·「：」7·「；」112·「！」20）</text>
<text x="30" y="540" font-size="11.5" fill="#8a7a5e">※ 问号 0 而实有问：文殊「以偈問賢首菩薩曰」——问在偈中，不在句式。〔本文判断〕</text>
</svg>""",
            "cap": "三层：上为颂行之形（717 行、14 字为主），中为三源口径（358.5／359.5／357.5／715.5），下为两译总量（10,228／10,159）。**三源之差在「颂」与「行」之口径，不在文本之多寡**：澄观、慧苑按颂计（约 358），智俨按行计（约 716），恰为二倍。此图所要说明者唯一事——**数目之不合，先问口径，再问文本**。",
            "en": "Three layers: the shape of the verse (717 lines, almost all fourteen characters); the three reckonings (358.5 by the present count, 359.5 Chengguan, 357.5 Huiyuan, 715.5 Zhiyan); and the totals of the two translations (10,228 / 10,159). The three figures differ by a factor of two because one counts ślokas and the others count lines. Ask about the measure before doubting the text.",
            "dufa": [
                "**「三百五十九颂半」不是文本，是口径。** 澄观所见即是今本；其数与本文实测仅差一颂，**差在「半颂」之断句处**。凡遇古德之数，先复原其计法。",
                "**智俨之 715.5 恰为本文之倍。** 一行一偈、二行一颂——**同一文本，两套度量衡**。不知此，则疑经文有增减。",
                "**两译差 69 字而用字之偏极大。** 三昧 33／68、光明 94／57——**总量近等而重心迥异**，此正是两译「译者之择」最清楚的证据。〔本文判断〕",
            ],
        },
        {
            "n": 2,
            "title": "十信相续功德链·顶针图",
            "what": "链如何行",
            "one": "「若得 X，則 Y」而 Y 复为下句之 X：由信奉諸佛至身遍虚空",
            "svg": """<svg viewBox="0 0 1000 580" width="100%" style="max-width:1000px;height:auto" xmlns="http://www.w3.org/2000/svg" font-family="serif">
<text x="500" y="24" text-anchor="middle" font-size="14.5" font-weight="bold" fill="#7a5a28">十信相续功德链：一环扣一环，末环即首环之果</text>
<text x="500" y="44" text-anchor="middle" font-size="12" fill="#8a7a5e">取 §2.3 长段之要节为十三环（原链实有数十环）；箭头＝「則」字</text>

<g font-size="12" fill="#5a5147">
<rect x="60" y="64" width="330" height="30" rx="4" fill="#f7ecd2" stroke="#b8863c" stroke-width="1.3"/><text x="74" y="84">① 信奉諸佛</text><text x="330" y="84" font-size="10.5" fill="#8a7a5e">链首</text>
<line x1="225" y1="94" x2="225" y2="104" stroke="#c9b98f"/><text x="232" y="104" font-size="10" fill="#b8863c">則</text>
<rect x="60" y="104" width="330" height="30" rx="4" fill="#f8f3ea" stroke="#d9cdb8"/><text x="74" y="124">② 持戒修學處</text>
<line x1="225" y1="134" x2="225" y2="144" stroke="#c9b98f"/><text x="232" y="144" font-size="10" fill="#b8863c">則</text>
<rect x="60" y="144" width="330" height="30" rx="4" fill="#f8f3ea" stroke="#d9cdb8"/><text x="74" y="164">③ 具足諸功德</text>
<line x1="225" y1="174" x2="225" y2="184" stroke="#c9b98f"/><text x="232" y="184" font-size="10" fill="#b8863c">則</text>
<rect x="60" y="184" width="330" height="30" rx="4" fill="#f8f3ea" stroke="#d9cdb8"/><text x="74" y="204">④ 遠離惡知識 · 親近善知識</text>
<line x1="225" y1="214" x2="225" y2="224" stroke="#c9b98f"/><text x="232" y="224" font-size="10" fill="#b8863c">則</text>
<rect x="60" y="224" width="330" height="30" rx="4" fill="#f8f3ea" stroke="#d9cdb8"/><text x="74" y="244">⑤ 發起菩提心</text>
<line x1="225" y1="254" x2="225" y2="264" stroke="#c9b98f"/><text x="232" y="264" font-size="10" fill="#b8863c">則</text>
<rect x="60" y="264" width="330" height="30" rx="4" fill="#f8f3ea" stroke="#d9cdb8"/><text x="74" y="284">⑥ 勤修佛功德 · 習波羅蜜</text>
<line x1="225" y1="294" x2="225" y2="304" stroke="#c9b98f"/><text x="232" y="304" font-size="10" fill="#b8863c">則</text>
<rect x="60" y="304" width="330" height="30" rx="4" fill="#f8f3ea" stroke="#d9cdb8"/><text x="74" y="324">⑦ 常覩見無量佛 · 得辯才</text>
</g>

<path d="M 225 334 L 225 356 Q 225 366 235 366 L 765 366 Q 775 366 775 356 L 775 336" fill="none" stroke="#c9b98f" stroke-dasharray="5 4"/>
<text x="500" y="384" text-anchor="middle" font-size="10.5" fill="#b8863c">越卷而下（卷十四 → 卷十五）</text>

<g font-size="12" fill="#5a5147">
<rect x="610" y="336" width="330" height="30" rx="4" fill="#f8f3ea" stroke="#d9cdb8"/><text x="624" y="356">⑧ 得堅固大悲心 · 慈愍度生</text>
<line x1="775" y1="294" x2="775" y2="284" stroke="#c9b98f"/>
<rect x="610" y="264" width="330" height="30" rx="4" fill="#f8f3ea" stroke="#d9cdb8"/><text x="624" y="284">⑨ 摧殄諸魔力 · 超四魔境</text>
<line x1="775" y1="254" x2="775" y2="244" stroke="#c9b98f"/>
<rect x="610" y="224" width="330" height="30" rx="4" fill="#f8f3ea" stroke="#d9cdb8"/><text x="624" y="244">⑩ 至於不退地</text>
<line x1="775" y1="214" x2="775" y2="204" stroke="#c9b98f"/>
<rect x="610" y="184" width="330" height="30" rx="4" fill="#f8f3ea" stroke="#d9cdb8"/><text x="624" y="204">⑪ 得無生深法忍 · 蒙授記</text>
<line x1="775" y1="174" x2="775" y2="164" stroke="#c9b98f"/>
<rect x="610" y="144" width="330" height="30" rx="4" fill="#f8f3ea" stroke="#d9cdb8"/><text x="624" y="164">⑫ 甘露灌頂</text>
<line x1="775" y1="134" x2="775" y2="124" stroke="#c9b98f"/><text x="782" y="124" font-size="10" fill="#b8863c">則</text>
<rect x="610" y="94" width="330" height="40" rx="4" fill="#f7ecd2" stroke="#b8863c" stroke-width="1.4"/><text x="624" y="112">⑬ 身充遍如虛空</text><text x="624" y="128" font-size="10.5" fill="#8a7a5e">安住不動，滿十方</text>
</g>

<line x1="60" y1="404" x2="940" y2="404" stroke="#d3c7ae"/>
<text x="60" y="430" font-size="12" fill="#7a5a28">链法：「若得／若能 X，則 Y」；而 Y 即下句之 X——故数十环实为一环之展转。</text>
<text x="60" y="456" font-size="11.5" fill="#8a7a5e">※ 链首「信奉諸佛」出于「信」；链尾「身充遍如虛空」即「信」之满量。始终一信，中历万行。〔本文判断〕</text>
<text x="60" y="482" font-size="11.5" fill="#8a7a5e">※ 慧苑七科之「四若常信奉下所具行位」（`X0221`@145024）即指此链；澄观判为「摄前行愿，成信德用」。</text>
<text x="60" y="508" font-size="11.5" fill="#8a7a5e">※ 末环「甘露灌頂」正当十信满心、邻十住灌顶位——故本品之终即第三会之始，两会在位次上无缝。</text>
<text x="60" y="534" font-size="11.5" fill="#8a7a5e">※ 望月轮／明月轮·如幻·如梦等譬喻在链后另起（§2.6 智自在况喻链），不在本图之列。</text>
<text x="60" y="560" font-size="11.5" fill="#7a5a28">→ 读法：顺读见行位，逆读见一信。</text>
</svg>""",
            "cap": "十三环取长段之要节（原链实有数十环），箭头即「則」字。**读法有二：顺读则见十信之行位层层增上，逆读则见始终只是一「信」**——链尾之「身充遍如虛空」，正是链首「信奉諸佛」之满量。末环「甘露灌頂」当十信满心、邻十住灌顶位，**故此品之终即第三会之始**，两会在位次上无缝相接。",
            "en": "Thirteen nodes out of a much longer chain, the arrows being the word 則, \\\"then\\\". Read forward, the chain is a ladder of stations from faith to a body filling space; read backward, it is one faith unfolding. The last node, ambrosial consecration, is the very threshold of the ten abidings — so this chapter's end is the third assembly's beginning.",
            "dufa": [
                "**顶针不是修辞，是位次。** 「則 Y」之 Y 即下句之「若 X」——**法位相续，故句法相衔**；若视为文字游戏，则失其骨。",
                "**链可顺读亦可逆读，所得不同。** 顺读得「行位」，逆读得「一信」；**两读并存，方是华严「行布不碍圆融」之实例**〔本文判断〕。",
                "**链终即会终。** 甘露灌顶→身遍虚空，已越十信而抵十住之门；**故读本品末，须即读第十三品《升须弥山顶》**，不可断在两处。",
            ],
        },
    ],
    "weici_note": "本品为第二会**第六品、亦收官之品**。第二会六品：前三（名号·四谛·光明觉）明所信之果（三业），后三（问明·净行·贤首）明能信之行（解·行·德）。**本品居末，以「德」结，以「信為道元」一句总摄前五品**。",
    "weici": [
        ["10 问明", "卷13", "十信·**解**", "九首递问，文殊总酬", "解为行德之本"],
        ["11 净行", "卷14", "十信·**行**", "141 誓，遇事发愿", "解而后行"],
        ["**12 贤首（本品）**", "卷14–15", "十信·**德**·满心", "717 颂行，信為道元", "行而后德，十信满心"],
        ["13 升须弥山顶", "卷16", "第三会·十住·**发起**", "偈赞佛德，不起而升", "本品末之灌顶即彼会之门"],
        ["14 须弥顶上偈赞", "卷16", "第三会·十住·**方便发起**", "十菩萨各说一颂", "由信入住之第一声"],
        ["15–18 十住·梵行·初发心·明法", "卷16–18", "第三会·十住·**正位·满足**", "十住阶位", "本品所望之全体"],
    ],
    "teshe_note": "本品之特色在**「偈颂为主而问号为零」**：全品以偈构成，文殊之问亦托于偈（「以偈問賢首菩薩曰」），故不设「云何」句式。**在三十九品中，以偈颂叹德、以顶针成链、而纯以「信」之一字立宗者，唯此一品**〔本文判断·据本文所核诸品文体〕。",
    "teshe": [
        ["偈颂为主", "颂行 717／颂 ×1／偈 ×3（实测）", "净行品颂 ×0·偈 ×0（纯长行）", "第二会文体之两极：一纯长行，一纯偈颂"],
        ["问号 ×0", "「。」312·「？」**0**", "净行「云何」×20·问号 21", "问在偈中，不在句式"],
        ["顶针长链", "「若……則……」数十环，一气贯通", "问明九段并列而不相衔", "一为链，一为阵"],
        ["十门三昧", "澄观「略辨十門三昧業用」：海印·華嚴·因陀羅網·手出廣供·現諸法門·四攝·俯同世間·毛光·主伴·寂用", "他品无此十门之科", "本品之「德」以三昧业用显，非以言说显"],
        ["两译近等", "八十 10,228／六十 10,159，差 69 字", "净行 141／140 誓；名号 211 两译同", "总量近等而用字偏异（三昧 33／68）"],
        ["颂数三源", "澄观 359.5／慧苑 357.5／智俨 715.5", "净行誓数疏家与实测全合", "一为口径之别，一为文本之实"],
    ],
    "dufa5": [
        ["**链读**", "只读 §2.3 顶针一链，余皆暂置", "初读本篇者", "得十信行位之一气"],
        ["**宗读**", "只读「信為道元功德母」四句，反复", "欲把捉宗旨者", "得全品之宗眼"],
        ["**门读**", "依 §7.5 十门行链，逐门读三昧业用", "好结构者", "见「德」如何以业用显"],
        ["**数读**", "图 〇-1 ＋ §7.5 L2 口径对验", "欲核文本者", "三源之数不复相碍"],
        ["**承读**", "本品末 → 第十三品 §2.1", "欲见会际衔接者", "见灌顶如何接「不起而升」"],
    ],
    "shu": [
        ["**T0 经文明文**", "「信為道元功德母，長養一切諸善法」", "`T10n0279` 卷十四", "全品宗眼（两译各唯一见）"],
        ["**T0 经文明文**", "「以偈問賢首菩薩曰」", "同上", "问托于偈（故问号 0）"],
        ["**T0 本文实测**", "**717 颂行／358.5 颂／10,228 字**", "§7.5 `_e12_lines.py`", "计数（本文自测）"],
        ["**T0 本文实测**", "之一 4,577＋之二 7,117＝11,694（raw）", "§6.1／§7.1", "计数（本文自测）"],
        ["**T1 澄观《疏》**", "「第二正顯偈詞。有三百五十九頌半」", "`T1735`@195841", "注疏之数（差 +1）"],
        ["**T1 慧苑**", "「總即三百五十七頌半」", "`X0221`@145024", "注疏之数（差 −1）"],
        ["**T1 智俨**", "「此品有七百一十五偈半」", "`T1732`@29947（依六十·按行计）", "口径之别，非文本之差"],
        ["**T2 转述**", "「贤首品明十信之德」", "诸家科文", "判摄语，须注家"],
    ],
    "shu_note": "> **〔读法〕** 本品之「数」有一特殊难处：**三家所计皆与本文实测差 ±1 颂，而智俨之数恰为二倍**。故本篇之立场为——**不裁古数，不疑底本，先复原其计法**。凡数之不合，先问「一行还是一颂」，再问「谁所见本」；二者既明，则三源各安其位。",
}

# ----------------------------------------------------------------------------
# 第十三部　升须弥山顶品
# ----------------------------------------------------------------------------
P13 = {
    "tag": "P13",
    "path": os.path.join(DIR3, "华严经细读_第十三部_升须弥山顶品.md"),
    "hui": "第三会（忉利天宫·说十住）",
    "dingwei": "本品为第三会之**会首**，纯是「由致」——不动一处而遍十方。读法当**以处为纲、以时为纬**：处不变而现处变，时不言而十佛自陈。",
    "yiju": "**不離菩提樹而昇須彌山頂**——八字是全品之骨；处未曾移，而十方各见，此为华严「即体即用」之第一次以「动作」说出。",
    "sanwen": "① 「不離」与「而昇」何以能并存？② 全品仅 654 字，何以为一会之首？③ 十佛颂何以由近而远逆序铺陈？",
    "tiyao": "本品为**全经最短诸品之一**：品界 **CJK 654**（含品题九字·正文净 645），品题＋**六个正文单元**（80-01 齐现 51・02 不離齐升 21・03 严殿 158・05 入殿乐止 60・06 十佛颂 280・07 殿广博 75）。文体为**长行五段＋偈颂一段**，颂即**十佛各一颂、每颂四句**。六十侧〈佛昇須彌頂品第九〉26 段・正文 630。澄观判第三会六品「**分為二分。初二品方便發起，後四品當會正說**」——本品居其首，**唯是由致**（纯为发起）。",
    "xufa": "先观图 〇-1 得「一处而十方」之空间结构，次观图 〇-2 得十佛逆序之时间轴，次读〇之二.3 之坐标，然后入 §二逐段。**处与时既明，六段之短乃见其不短。**",
    "en_map": "The shortest of the assembly-opening chapters: 654 characters, six prose units and one block of ten verses. Its whole content is a single sentence — not leaving the foot of the bodhi tree, the Buddha ascends to the summit of Mount Sumeru — and its whole proof is a chain of ten past Buddhas who each once entered this same hall. Fig. 0-1 draws the spatial paradox; Fig. 0-2 sets the ten Buddhas on a reverse-chronological axis.",
    "figs": [
        {
            "n": 1,
            "title": "不起而升·一处十方图",
            "what": "处如何不动而遍",
            "one": "此不动（菩提树下）·彼现起（须弥山顶）·十方各见",
            "svg": """<svg viewBox="0 0 1000 500" width="100%" style="max-width:1000px;height:auto" xmlns="http://www.w3.org/2000/svg" font-family="serif">
<text x="500" y="24" text-anchor="middle" font-size="14.5" font-weight="bold" fill="#7a5a28">不離菩提樹而昇須彌山頂：一处不动，十方齐见</text>
<text x="500" y="44" text-anchor="middle" font-size="12" fill="#8a7a5e">六单元之 CJK 附于段名后（§1.3 实测）；箭头所标为经文语，非本文增字</text>

<rect x="60" y="62" width="880" height="48" rx="5" fill="#f8f3ea" stroke="#d9cdb8"/>
<text x="500" y="82" text-anchor="middle" font-size="12" fill="#5a5147">十方一切世界 · 一一四天下 · 閻浮提中，悉見如來坐於樹下</text>
<text x="500" y="100" text-anchor="middle" font-size="11" fill="#8a7a5e">80-01 本會齊現（51 字）——不是「此界见」，是「十方一切世界皆见」</text>

<rect x="90" y="136" width="340" height="86" rx="5" fill="#f3ecdf" stroke="#c9b98f"/>
<text x="260" y="160" text-anchor="middle" font-size="12.5" font-weight="bold" fill="#7a5a28">此 · 菩提樹下</text>
<text x="260" y="180" text-anchor="middle" font-size="11.5" fill="#5a5147">摩竭提國阿蘭若法菩提場</text>
<text x="260" y="200" text-anchor="middle" font-size="11.5" fill="#5a5147">本會說法處（體·不動）</text>
<text x="260" y="216" text-anchor="middle" font-size="10.5" fill="#8a7a5e">80-02（21 字）</text>

<line x1="440" y1="179" x2="552" y2="179" stroke="#b8863c" stroke-width="1.4"/>
<path d="M 552 179 L 542 173 L 542 185 Z" fill="#b8863c"/>
<text x="496" y="168" text-anchor="middle" font-size="13" font-weight="bold" fill="#b8863c">不離</text>
<text x="496" y="198" text-anchor="middle" font-size="13" font-weight="bold" fill="#b8863c">而昇</text>

<rect x="570" y="136" width="340" height="86" rx="5" fill="#f7ecd2" stroke="#b8863c" stroke-width="1.4"/>
<text x="740" y="160" text-anchor="middle" font-size="12.5" font-weight="bold" fill="#7a5a28">彼 · 須彌山頂</text>
<text x="740" y="180" text-anchor="middle" font-size="11.5" fill="#5a5147">帝釋妙勝殿·忉利天宮</text>
<text x="740" y="200" text-anchor="middle" font-size="11.5" fill="#5a5147">第三會說法處（用·現起）</text>
<text x="740" y="216" text-anchor="middle" font-size="10.5" fill="#8a7a5e">一处不动，一处现起——两处同时</text>

<text x="60" y="252" font-size="11.5" fill="#7a5a28">〔本文判断〕「不離」与「而昇」不是二事之折衷，而是**一事之两面**：若离而去，则成行；若不昇，则无用。**体不动故能遍，用现起故成位。**</text>

<rect x="60" y="270" width="880" height="72" rx="5" fill="#ffffff" stroke="#e0d6c2"/>
<text x="76" y="292" font-size="12" font-weight="bold" fill="#7a5a28">80-03 各見佛來·各嚴殿座（158 字）</text>
<g font-size="11" fill="#8a7a5e">
<text x="76" y="314">「十千」层级 ×10：十千層級 · 十千欄楯 · 十千寶網 · 十千瓔珞 …… （对六十作「萬種／萬寶／一萬」）</text>
</g>
<g fill="#c9b98f">
<rect x="76" y="322" width="10" height="10"/><rect x="92" y="322" width="10" height="10"/><rect x="108" y="322" width="10" height="10"/><rect x="124" y="322" width="10" height="10"/><rect x="140" y="322" width="10" height="10"/><rect x="156" y="322" width="10" height="10"/><rect x="172" y="322" width="10" height="10"/><rect x="188" y="322" width="10" height="10"/><rect x="204" y="322" width="10" height="10"/><rect x="220" y="322" width="10" height="10"/>
</g>
<text x="244" y="331" font-size="10.5" fill="#8a7a5e">十</text>
<text x="500" y="331" font-size="10.5" fill="#8a7a5e">「善來」×3——一处请佛三称，非重出（§6.4 辨幻影单元 80-04）</text>

<text x="60" y="368" font-size="12" font-weight="bold" fill="#7a5a28">余三段（顺次而下）</text>
<g font-size="11.5" fill="#5a5147">
<rect x="60" y="378" width="200" height="46" rx="4" fill="#f8f3ea" stroke="#d9cdb8"/><text x="160" y="398" text-anchor="middle">80-05 入殿·樂音止</text><text x="160" y="416" text-anchor="middle" font-size="10.5" fill="#8a7a5e">60 字</text>
<rect x="280" y="378" width="200" height="46" rx="4" fill="#f8f3ea" stroke="#d9cdb8"/><text x="380" y="398" text-anchor="middle">80-06 十佛偈頌</text><text x="380" y="416" text-anchor="middle" font-size="10.5" fill="#8a7a5e">280 字（占全品四成三）</text>
<rect x="500" y="378" width="200" height="46" rx="4" fill="#f8f3ea" stroke="#d9cdb8"/><text x="600" y="398" text-anchor="middle">80-07 殿廣博·結通</text><text x="600" y="416" text-anchor="middle" font-size="10.5" fill="#8a7a5e">75 字</text>
<rect x="720" y="378" width="220" height="46" rx="4" fill="none" stroke="#c9b98f" stroke-dasharray="5 4"/><text x="830" y="398" text-anchor="middle">→ 第十四品·重頌</text><text x="830" y="416" text-anchor="middle" font-size="10.5" fill="#8a7a5e">本品之颂，彼品再申</text>
</g>

<text x="60" y="452" font-size="11.5" fill="#8a7a5e">※ 全品问号 ×0、无当机请问者——「由致」之体，本不待问。与第二会光明觉品之「无问而说」，同一手法而更简。</text>
<text x="60" y="476" font-size="11.5" fill="#8a7a5e">※ 645 字而成一会之首：<tspan fill="#7a5a28">品之轻重不在字数，在其所开之局</tspan>。此品所开者，十住三十四品之局也。〔本文判断〕</text>
</svg>""",
            "cap": "一处不动而十方齐见，两处同时现起，是全品之骨。**「不離」与「而昇」不是折衷，是一事两面**：体不动故能遍，用现起故成位〔本文判断〕。下三段顺次而下，独 80-06 十佛颂占 280 字、全品四成三——**短品之中，最长的一段是偈**。",
            "en": "One place unmoved, ten directions seeing at once. Not leaving the bodhi tree and ascending Mount Sumeru are not a compromise but two faces of one act: the essence unmoved is what allows it to reach everywhere; the function arising is what makes a stage. Six prose units, one verse block — and the verse takes 43% of a 645-character chapter.",
            "dufa": [
                "**先读「不離」，再读「而昇」。** 若先读「昇」，「不離」成矛盾；先立「不離」之体，则「昇」只是其用。**次序即义次。**",
                "**「十方一切世界悉见」是第一句，不是修辞。** 本品开篇即不许读者局于一处——**故此后「此殿」云云，皆当读作「一切处」**。",
                "**短品不可略过。** 645 字开十住三十四品之局；**会首之品，其职在「开」，不在「说」**。",
            ],
        },
        {
            "n": 2,
            "title": "十佛颂·逆时序图",
            "what": "时如何铺陈",
            "one": "迦葉→拘那牟尼→…→然燈：由近而远，十佛各一颂",
            "svg": """<svg viewBox="0 0 1000 470" width="100%" style="max-width:1000px;height:auto" xmlns="http://www.w3.org/2000/svg" font-family="serif">
<text x="500" y="24" text-anchor="middle" font-size="14.5" font-weight="bold" fill="#7a5a28">十佛曾入此殿：由近而远，逆时序铺陈</text>
<text x="500" y="44" text-anchor="middle" font-size="12" fill="#8a7a5e">八十 80-06·十佛各一颂四句（CJK 280）；颂名次第悉照 `T10n0279` 卷十六</text>

<line x1="70" y1="120" x2="930" y2="120" stroke="#c9b98f"/>
<path d="M 70 120 L 80 115 L 80 125 Z" fill="#c9b98f"/>
<text x="70" y="104" font-size="11" fill="#8a7a5e">近（现在贤劫）</text>
<text x="930" y="104" text-anchor="end" font-size="11" fill="#8a7a5e">远（过去久远）</text>

<g font-size="11.5" text-anchor="middle">
<g fill="#5a5147">
<circle cx="100" cy="120" r="5" fill="#b8863c"/><text x="100" y="146">迦葉</text>
<circle cx="190" cy="120" r="5" fill="#b8863c"/><text x="190" y="146">拘那牟尼</text>
<circle cx="280" cy="120" r="5" fill="#b8863c"/><text x="280" y="146">迦羅鳩馱</text>
<circle cx="370" cy="120" r="5" fill="#c9b98f"/><text x="370" y="146">毘舍浮</text>
<circle cx="460" cy="120" r="5" fill="#c9b98f"/><text x="460" y="146">尸棄</text>
<circle cx="550" cy="120" r="5" fill="#c9b98f"/><text x="550" y="146">毘婆尸</text>
<circle cx="640" cy="120" r="5" fill="#c9b98f"/><text x="640" y="146">弗沙</text>
<circle cx="730" cy="120" r="5" fill="#c9b98f"/><text x="730" y="146">提舍</text>
<circle cx="820" cy="120" r="5" fill="#c9b98f"/><text x="820" y="146">波頭摩</text>
<circle cx="910" cy="120" r="5" fill="#c9b98f"/><text x="910" y="146">然燈</text>
</g>
<g font-size="10" fill="#8a7a5e">
<text x="100" y="166">一颂</text><text x="190" y="166">一颂</text><text x="280" y="166">一颂</text><text x="370" y="166">一颂</text><text x="460" y="166">一颂</text><text x="550" y="166">一颂</text><text x="640" y="166">一颂</text><text x="730" y="166">一颂</text><text x="820" y="166">一颂</text><text x="910" y="166">一颂</text>
</g>
</g>

<rect x="60" y="186" width="880" height="46" rx="4" fill="#f7ecd2" stroke="#b8863c"/>
<text x="500" y="206" text-anchor="middle" font-size="12.5" font-weight="bold" fill="#7a5a28">「是故此處最吉祥」×10——一一颂皆以此句结</text>
<text x="500" y="224" text-anchor="middle" font-size="11" fill="#8a7a5e">六十字侧作「是故此地最吉祥」×10：两译结句同构，唯「此處／此地」一字之异</text>

<text x="60" y="268" font-size="12" font-weight="bold" fill="#7a5a28">读此轴之三事</text>
<text x="60" y="292" font-size="11.5" fill="#5a5147">① **金色三佛（迦葉·拘那牟尼·迦羅鳩馱）属现在贤劫**，灰色七佛属过去——**颂由近起，逆溯至然燈**。</text>
<text x="60" y="316" font-size="11.5" fill="#5a5147">② 逆序非随意：**愈近者愈可征，愈远者愈显其久**；以「曾入此殿」为线，则时间长短皆摄于一处。</text>
<text x="60" y="340" font-size="11.5" fill="#5a5147">③ 「此處最吉祥」之「此」，在颂中指殿；至 80-07 殿忽广博，**「此」遂结通十方**——空间由点而面，时间由近而远，两者同收于末段。</text>

<line x1="60" y1="360" x2="940" y2="360" stroke="#d3c7ae"/>
<text x="60" y="386" font-size="11.5" fill="#8a7a5e">※ 十佛之名与次第，依底本照录；「过去七佛」之常序（毘婆尸→尸棄→毘舍浮→拘孫→拘那含→迦葉）在此**全部倒转**，非本文改次。〔本文判断·据常序比对〕</text>
<text x="60" y="410" font-size="11.5" fill="#8a7a5e">※ 颂句「最無上」×10（次句），与结句「最吉祥」×10 成双复沓——**十颂之同构，正是「十住」同构之先声**。</text>
<text x="60" y="434" font-size="11.5" fill="#7a5a28">※ 「十千」×10 表庄严，「十」表佛数：<tspan>本品以「十」为数之骨，下一品即以「十菩萨×十颂」承之。</tspan></text>
<text x="60" y="458" font-size="11.5" fill="#8a7a5e">※ 六十侧「善來」仅 ×1（八十 ×3），「萬」代「十千」——两译简繁之别，各照底本。</text>
</svg>""",
            "cap": "十佛沿一条由近及远的轴排列：**金色三佛属现在贤劫，灰色七佛属过去**，而十颂皆以「是故此處最吉祥」结。**逆序不是随意**：以「曾入此殿」为线，愈远者愈显其久，而时间长短皆摄于一处〔本文判断〕。至 80-07 殿忽广博，「此」遂结通十方——空间由点而面，时间由近而远，两者同收于末段。",
            "en": "Ten Buddhas on an axis running from near to far: three of the present kalpa in gold, seven of the past in grey, each verse closing on the same line. The reversal is not arbitrary — with \"once entered this hall\" as the thread, the further back one goes the longer the span, and all of it is gathered into one place. Then the hall suddenly widens, and \"this\" opens out to the ten directions.",
            "dufa": [
                "**十佛不是「举例」，是「证成」。** 一一皆「曾入此殿」，故今日之入非创举，乃**旧事之重演**——此为本品以时间证空间之法。",
                "**结句复沓十次，是全品最重之句。** 「是故此處最吉祥」——**「吉祥」不在远处，即在此处**；此句一立，十住之位始有落处。",
                "**末段「殿皆广博」须与首段「十方齐见」合看。** 首以十方摄一处，末以一处摄十方——**一开一合，全品之呼吸**。",
            ],
        },
    ],
    "weici_note": "本品为第三会**六品之首**。澄观判第三会「**分為二分：初二品方便發起，後四品當會正說**」；本品与次品（偈赞）共为发起，而**本品「唯是由致」，偈赞一品则「義有兩兼」**。",
    "weici": [
        ["12 贤首（前）", "卷14–15", "第二会·十信·德", "717 颂行，信为道元", "信满而入住，故有第三会"],
        ["**13 升须弥山顶（本品）**", "卷16", "第三会·十住·**发起**", "不離而昇，十佛曾入", "—"],
        ["14 须弥顶上偈赞", "卷16", "第三会·十住·**方便发起**", "十菩萨各十颂", "本品之颂，彼品再申"],
        ["15 十住", "卷16", "第三会·十住·**正说**", "十住阶位，百颂", "本会之正说自此始"],
        ["16 梵行", "卷17", "第三会·十住·**胜进**", "十法推徵，离相梵行", "位中通行"],
        ["17–18 初发心·明法", "卷17–18", "第三会·**满足行相**", "校量功德·十法矩阵", "一会之终"],
    ],
    "teshe_note": "本品之特色在**「极短而极重」**：645 字而成一会之首，全品无问、无答、无因缘铺陈，只有一事（不離而昇）与一证（十佛曾入）。**在三十九品中，以如此短幅开一会者，唯此一品**〔本文判断·据本文所核诸品篇幅〕。",
    "teshe": [
        ["篇幅", "CJK 654／正文 645（全经最短诸品之一）", "第十四品 2,510；第十七品 8,207", "同会之中，繁简相去十三倍"],
        ["文体", "长行五段＋偈一段（十佛颂）", "第十四品纯颂群（10 lg）；第十六品纯长行", "一会六品，文体三变"],
        ["无问无答", "问号 ×0；无当机者", "第十六品有正念天子问；第十八品有精进慧问", "发起之品，不待问"],
        ["空间结构", "一处不动·十方齐见·末段结通", "第十四品以「三列名数」表十方", "一以动作表，一以名数表"],
        ["时间结构", "十佛逆序（近→远）", "第十四品无时间轴（唯「承佛威神」）", "本品以过去证现在，独擅其法"],
        ["文本幻影", "平文器 80-04 为 80-03 嵌套节点重计（24 字）", "第十五品有 5 字短 p", "读数据层须先辨器"],
    ],
    "dufa5": [
        ["**处读**", "只读 80-01·02·07 三段", "初读本篇者", "得「一处十方」之骨"],
        ["**佛读**", "只读十佛颂，参图 〇-2 之时间轴", "欲见「证成」之法者", "见过去佛如何证现在"],
        ["**严读**", "只读 80-03 庄严段之「十千」×10", "好名数者", "见「十千」为满数之例"],
        ["**校读**", "§6.4 幻影单元辨 ＋ §6.1′ 六十全本", "欲核文本者", "得 645 之实与 80-04 之伪"],
        ["**承读**", "本品 §2.7 → 第十四品 §2.0", "欲见一会之起者", "见长行如何转成全颂"],
    ],
    "shu": [
        ["**T0 经文明文**", "「不離菩提樹而昇須彌山頂」", "`T10n0279` 卷十六·80-02", "全品之骨"],
        ["**T0 经文明文**", "「是故此處最吉祥」×10", "同上·80-06", "十颂结句（复沓）"],
        ["**T0 本文实测**", "**654 字／645 净／6 单元**", "§7.1／§7.4 脚本", "计数（本文自测）"],
        ["**T0 本文实测**", "十千 ×10・最無上 ×10・善來 ×3", "§7.5 L2", "计数（本文自测）"],
        ["**T1 澄观《疏》**", "「分為二分。初二品方便發起。後四品當會正說」", "`T1735` 卷十六", "一会之科判"],
        ["**T1 澄观《疏》**", "「今初一品長分十段」", "同上", "十段科（本文八段与之相应）"],
        ["**T2 六十**", "26 段・正文 630・「善來」×1・「萬」代「十千」", "`T09n0278` 卷七", "对读（简繁之别）"],
    ],
    "shu_note": "> **〔读法〕** 本品之数极简：654（字）・6（单元）・10（佛）・10（十千）。**四数皆可复算，且四数各有其性质**：字数是量，单元是构，十佛是举，十千是满数之例。**最忌以「十千」为数实**——六十作「萬」，可见其为「取满」而非「计实」。",
}

# ----------------------------------------------------------------------------
# 第十四部　须弥顶上偈赞品
# ----------------------------------------------------------------------------
P14 = {
    "tag": "P14",
    "path": os.path.join(DIR3, "华严经细读_第十四部_须弥顶上偈赞品.md"),
    "hui": "第三会（忉利天宫·说十住）",
    "dingwei": "本品为**纯颂之品**：无叙事、无问答，唯十菩萨各出十颂。读法当**以阵为纲**——三列名数（慧·华·月）为经，十颂递引为纬。",
    "yiju": "**十菩萨皆名「慧」，十世界皆名「华」，十佛皆号「月」**——三列同构，即「行德·感果·智凉」之三翻表法。",
    "sanwen": "① 何以此品全用重颂，而无一句长行正说？② 三列名数（慧·华·月）各十，是巧合还是定位？③ 十菩萨之颂既有递引链，何以七环而缺二？",
    "tiyao": "本品为**长颂之品**（较前品长行反为巨）：品界 **CJK 2,510**（含品题十字·净 2,500），**二十二单元＝1 head＋11 p＋10 lg**。集会长行 80-01（314 字）＋十组「起式 p（18–19 字）＋颂群 lg」——**每 lg 恰 CJK 200・四十句五言・十颂**，十菩萨 × 十颂＝**百颂·四百句·CJK 2,000**。前品 645 字，本品 2,510 字——**重颂品反倍长于行品，为华严文体之一大反差**。",
    "xufa": "先观图 〇-1 得百颂之阵（10×10，格格二百字），次观图 〇-2 得三列名数之配位，次读〇之二.3 之坐标，然后入 §二逐段。**阵既定，颂始不乱。**",
    "en_map": "A chapter of pure verse: 2,510 characters, of which 2,000 are ten bodhisattvas' ten verses each — one hundred ślokas, four hundred five-character lines, every verse-block exactly 200 characters. Its signature is a three-column matrix: all ten bodhisattvas are named 慧 (wisdom), all ten worlds 華 (flower), all ten Buddhas 月 (moon). Fig. 0-1 is the 10×10 grid; Fig. 0-2 the three columns and the chain of cross-references.",
    "figs": [
        {
            "n": 1,
            "title": "十菩萨×十颂·百颂矩阵",
            "what": "颂如何成阵",
            "one": "10 行 ×10 颂＝100 颂；每行恰 CJK 200・40 句五言",
            "svg": """<svg viewBox="0 0 1000 520" width="100%" style="max-width:1000px;height:auto" xmlns="http://www.w3.org/2000/svg" font-family="serif">
<text x="500" y="24" text-anchor="middle" font-size="14.5" font-weight="bold" fill="#7a5a28">百颂之阵：十菩萨各十颂，格格二百字</text>
<text x="500" y="44" text-anchor="middle" font-size="12" fill="#8a7a5e">每格＝一颂（四句五言）；每行＝一 lg，实测恰 CJK 200（§7.1 逐 lg 验）</text>

<g font-size="10" fill="#8a7a5e" text-anchor="middle">
<text x="285" y="74">一</text><text x="342" y="74">二</text><text x="399" y="74">三</text><text x="456" y="74">四</text><text x="513" y="74">五</text><text x="570" y="74">六</text><text x="627" y="74">七</text><text x="684" y="74">八</text><text x="741" y="74">九</text><text x="798" y="74">十</text>
</g>

<g font-size="11.5" fill="#5a5147">
<text x="70" y="96">法慧</text><text x="150" y="96" font-size="10" fill="#8a7a5e">80-03</text>
<text x="70" y="130">一切慧</text><text x="150" y="130" font-size="10" fill="#8a7a5e">80-05</text>
<text x="70" y="164">勝慧</text><text x="150" y="164" font-size="10" fill="#8a7a5e">80-07</text>
<text x="70" y="198">功德慧</text><text x="150" y="198" font-size="10" fill="#8a7a5e">80-09</text>
<text x="70" y="232">精進慧</text><text x="150" y="232" font-size="10" fill="#8a7a5e">80-11</text>
<text x="70" y="266">善慧</text><text x="150" y="266" font-size="10" fill="#8a7a5e">80-13</text>
<text x="70" y="300">智慧</text><text x="150" y="300" font-size="10" fill="#8a7a5e">80-15</text>
<text x="70" y="334">真實慧</text><text x="150" y="334" font-size="10" fill="#8a7a5e">80-17</text>
<text x="70" y="368">無上慧</text><text x="150" y="368" font-size="10" fill="#8a7a5e">80-19</text>
<text x="70" y="402">堅固慧</text><text x="150" y="402" font-size="10" fill="#8a7a5e">80-21</text>
</g>

<g fill="#e6dbc5" stroke="#c9b98f">
<rect x="262" y="80" width="50" height="18"/><rect x="319" y="80" width="50" height="18"/><rect x="376" y="80" width="50" height="18"/><rect x="433" y="80" width="50" height="18"/><rect x="490" y="80" width="50" height="18"/><rect x="547" y="80" width="50" height="18"/><rect x="604" y="80" width="50" height="18"/><rect x="661" y="80" width="50" height="18"/><rect x="718" y="80" width="50" height="18"/><rect x="775" y="80" width="50" height="18"/>
<rect x="262" y="114" width="50" height="18"/><rect x="319" y="114" width="50" height="18"/><rect x="376" y="114" width="50" height="18"/><rect x="433" y="114" width="50" height="18"/><rect x="490" y="114" width="50" height="18"/><rect x="547" y="114" width="50" height="18"/><rect x="604" y="114" width="50" height="18"/><rect x="661" y="114" width="50" height="18"/><rect x="718" y="114" width="50" height="18"/><rect x="775" y="114" width="50" height="18"/>
<rect x="262" y="148" width="50" height="18"/><rect x="319" y="148" width="50" height="18"/><rect x="376" y="148" width="50" height="18"/><rect x="433" y="148" width="50" height="18"/><rect x="490" y="148" width="50" height="18"/><rect x="547" y="148" width="50" height="18"/><rect x="604" y="148" width="50" height="18"/><rect x="661" y="148" width="50" height="18"/><rect x="718" y="148" width="50" height="18"/><rect x="775" y="148" width="50" height="18"/>
<rect x="262" y="182" width="50" height="18"/><rect x="319" y="182" width="50" height="18"/><rect x="376" y="182" width="50" height="18"/><rect x="433" y="182" width="50" height="18"/><rect x="490" y="182" width="50" height="18"/><rect x="547" y="182" width="50" height="18"/><rect x="604" y="182" width="50" height="18"/><rect x="661" y="182" width="50" height="18"/><rect x="718" y="182" width="50" height="18"/><rect x="775" y="182" width="50" height="18"/>
<rect x="262" y="216" width="50" height="18"/><rect x="319" y="216" width="50" height="18"/><rect x="376" y="216" width="50" height="18"/><rect x="433" y="216" width="50" height="18"/><rect x="490" y="216" width="50" height="18"/><rect x="547" y="216" width="50" height="18"/><rect x="604" y="216" width="50" height="18"/><rect x="661" y="216" width="50" height="18"/><rect x="718" y="216" width="50" height="18"/><rect x="775" y="216" width="50" height="18"/>
<rect x="262" y="250" width="50" height="18"/><rect x="319" y="250" width="50" height="18"/><rect x="376" y="250" width="50" height="18"/><rect x="433" y="250" width="50" height="18"/><rect x="490" y="250" width="50" height="18"/><rect x="547" y="250" width="50" height="18"/><rect x="604" y="250" width="50" height="18"/><rect x="661" y="250" width="50" height="18"/><rect x="718" y="250" width="50" height="18"/><rect x="775" y="250" width="50" height="18"/>
<rect x="262" y="284" width="50" height="18"/><rect x="319" y="284" width="50" height="18"/><rect x="376" y="284" width="50" height="18"/><rect x="433" y="284" width="50" height="18"/><rect x="490" y="284" width="50" height="18"/><rect x="547" y="284" width="50" height="18"/><rect x="604" y="284" width="50" height="18"/><rect x="661" y="284" width="50" height="18"/><rect x="718" y="284" width="50" height="18"/><rect x="775" y="284" width="50" height="18"/>
<rect x="262" y="318" width="50" height="18"/><rect x="319" y="318" width="50" height="18"/><rect x="376" y="318" width="50" height="18"/><rect x="433" y="318" width="50" height="18"/><rect x="490" y="318" width="50" height="18"/><rect x="547" y="318" width="50" height="18"/><rect x="604" y="318" width="50" height="18"/><rect x="661" y="318" width="50" height="18"/><rect x="718" y="318" width="50" height="18"/><rect x="775" y="318" width="50" height="18"/>
<rect x="262" y="352" width="50" height="18"/><rect x="319" y="352" width="50" height="18"/><rect x="376" y="352" width="50" height="18"/><rect x="433" y="352" width="50" height="18"/><rect x="490" y="352" width="50" height="18"/><rect x="547" y="352" width="50" height="18"/><rect x="604" y="352" width="50" height="18"/><rect x="661" y="352" width="50" height="18"/><rect x="718" y="352" width="50" height="18"/><rect x="775" y="352" width="50" height="18"/>
<rect x="262" y="386" width="50" height="18"/><rect x="319" y="386" width="50" height="18"/><rect x="376" y="386" width="50" height="18"/><rect x="433" y="386" width="50" height="18"/><rect x="490" y="386" width="50" height="18"/><rect x="547" y="386" width="50" height="18"/><rect x="604" y="386" width="50" height="18"/><rect x="661" y="386" width="50" height="18"/><rect x="718" y="386" width="50" height="18"/><rect x="775" y="386" width="50" height="18"/>
</g>

<text x="850" y="96" font-size="11" fill="#7a5a28">×10 行</text>
<text x="850" y="116" font-size="10.5" fill="#8a7a5e">＝100 颂</text>
<text x="850" y="140" font-size="10.5" fill="#8a7a5e">400 句</text>
<text x="850" y="160" font-size="10.5" fill="#8a7a5e">CJK 2,000</text>

<line x1="262" y1="418" x2="825" y2="418" stroke="#b8863c"/>
<text x="262" y="438" font-size="11.5" fill="#7a5a28">每行（lg）恰 200 字——十行皆同，无一例外。十行之和 2,000＋集会长行 314＋起式 10×18/19＋品题 10＝2,510。</text>

<text x="70" y="466" font-size="11.5" fill="#8a7a5e">※ 一一格皆「十颂」之单位，非颂句；格内不复细分——**由图见阵，不由图读颂**。</text>
<text x="70" y="488" font-size="11.5" fill="#8a7a5e">※ 十菩萨之次第即起式之次第（80-02→80-20 为起式 p，80-03→80-21 为颂群 lg），一一严配，无错简。</text>
<text x="70" y="510" font-size="11.5" fill="#7a5a28">※ 前品 645 字，本品 2,510——<tspan>重颂品倍长于行品</tspan>，华严文体之最大反差之一。</text>
</svg>""",
            "cap": "十行十列，格格一颂。**每行恰 CJK 200 字，十行皆同，无一例外**——这个「整数」不是巧合，是重颂体例的签名：先定颂数，后以字就之。集会长行 314＋起式 10×18/19＋品题 10＋颂 2,000＝2,510，**全品守恒**。此图所示唯一事：**本品是一个「阵」，不是一个「叙」**。",
            "en": "Ten by ten, each cell one śloka. Every row is exactly 200 characters — ten times over, without exception. That integer is not accident but the signature of the versified form: the number of verses is fixed first, and the characters are made to fit. The chapter is a matrix, not a narrative.",
            "dufa": [
                "**先数行，后读颂。** 十行既齐，则知此品之设计是「十×十」；**若逐颂读去而不见阵，则失其体**。",
                "**「每 lg 恰 200」是文本事实，可作为定界之据。** 凡校重颂之品，字数整齐处即编者分段处。〔本文判断〕",
                "**颂多而长行极少，是本品的「礼」：** 前品已立事，此品唯赞德；**事可言简，德须颂广**。",
            ],
        },
        {
            "n": 2,
            "title": "三列名数矩阵（慧·华·月）",
            "what": "名如何表法",
            "one": "菩萨皆慧·世界皆华·佛皆月；三列各十，一一配位",
            "svg": """<svg viewBox="0 0 1000 520" width="100%" style="max-width:1000px;height:auto" xmlns="http://www.w3.org/2000/svg" font-family="serif">
<text x="500" y="24" text-anchor="middle" font-size="14.5" font-weight="bold" fill="#7a5a28">三列名数：菩萨同「慧」· 世界同「华」· 佛同「月」</text>
<text x="500" y="44" text-anchor="middle" font-size="12" fill="#8a7a5e">八十名号悉照 `T10n0279` 卷十六（§4.2 表）；右栏为澄观表法语</text>

<g font-size="10.5" fill="#8a7a5e">
<text x="40" y="72">次</text><text x="72" y="72">菩萨</text><text x="160" y="72">世界</text><text x="300" y="72">佛号</text><text x="420" y="72">澄观表法（节录）</text>
</g>
<line x1="34" y1="78" x2="966" y2="78" stroke="#c9b98f"/>

<g font-size="11" fill="#5a5147">
<text x="40" y="100">1</text><text x="72" y="100" font-weight="bold">法慧</text><text x="160" y="100">因陀羅華</text><text x="300" y="100">殊特月</text><text x="420" y="100" fill="#8a7a5e">十難得法，可謂殊特（發心住·東）</text>
<text x="40" y="124">2</text><text x="72" y="124" font-weight="bold">一切慧</text><text x="160" y="124">波頭摩華</text><text x="300" y="124">無盡月</text><text x="420" y="124" fill="#8a7a5e">發十大心，不可窮盡（治地住·南）</text>
<text x="40" y="148">3</text><text x="72" y="148" font-weight="bold">勝慧</text><text x="160" y="148">寶華</text><text x="300" y="148">不動月</text><text x="420" y="148" fill="#8a7a5e">觀於空等，不可傾動（修行住·西）</text>
<text x="40" y="172">4</text><text x="72" y="172" font-weight="bold">功德慧</text><text x="160" y="172">優鉢羅華</text><text x="300" y="172">風月</text><text x="420" y="172" fill="#8a7a5e">生死涅槃如風不住（生貴住·北）</text>
<text x="40" y="196">5</text><text x="72" y="196" font-weight="bold">精進慧</text><text x="160" y="196">金剛華</text><text x="300" y="196">水月</text><text x="420" y="196" fill="#8a7a5e">饒益安樂如水普潤（方便住·東北）</text>
<text x="40" y="220">6</text><text x="72" y="220" font-weight="bold">善慧</text><text x="160" y="220">妙香華</text><text x="300" y="220">解脫月</text><text x="420" y="220" fill="#8a7a5e">聞十種法心定不動（正心住·東南）</text>
<text x="40" y="244">7</text><text x="72" y="244" font-weight="bold">智慧</text><text x="160" y="244">悅意華</text><text x="300" y="244">無上月</text><text x="420" y="244" fill="#8a7a5e">聞十不退，可謂無上（不退住·西南）</text>
<text x="40" y="268">8</text><text x="72" y="268" font-weight="bold">真實慧</text><text x="160" y="268">阿盧那華</text><text x="300" y="268">星宿月</text><text x="420" y="268" fill="#8a7a5e">三業無失如星明淨（童真住·西北）</text>
<text x="40" y="292">9</text><text x="72" y="292" font-weight="bold">無上慧</text><text x="160" y="292">那羅陀華</text><text x="300" y="292">清淨月</text><text x="420" y="292" fill="#8a7a5e">善知煩惱習氣故清淨（王子住·下）</text>
<text x="40" y="316">10</text><text x="72" y="316" font-weight="bold">堅固慧</text><text x="160" y="316">虛空華</text><text x="300" y="316">明了月</text><text x="420" y="316" fill="#8a7a5e">餘不能知，唯自明了（灌頂住·上）</text>
</g>
<line x1="34" y1="328" x2="966" y2="328" stroke="#c9b98f"/>

<g font-size="11.5" fill="#7a5a28">
<text x="40" y="352">列义</text>
<text x="72" y="352">行德（十解之慧）</text>
<text x="160" y="352">感果（位相創開無著）</text>
<text x="300" y="352">智凉（智明·闇息·恩益）</text>
<text x="420" y="352" fill="#8a7a5e">三列各十，一一配位，无漏无重</text>
</g>

<rect x="34" y="372" width="932" height="52" rx="4" fill="#f7ecd2" stroke="#b8863c"/>
<text x="48" y="392" font-size="11.5" font-weight="bold" fill="#7a5a28">递引链七环（缺二）：先已說×2 · 先說×1 · 如德慧所說×1 · 精進慧大士×1 · 如是實慧說×1 · 勝慧等菩薩×1</text>
<text x="48" y="412" font-size="11" fill="#8a7a5e">十颂之中，后颂引前颂之说——**行列互引，是矩阵之第二维**；缺二处照底本存，不补。</text>

<text x="34" y="452" font-size="11.5" fill="#8a7a5e">※ 「慧·华·月」三字非偶然同名：慧为能见，华为所感，月为果智之凉——<tspan fill="#7a5a28">名身即表法，是华严命名的通例</tspan>。〔本文判断〕</text>
<text x="34" y="476" font-size="11.5" fill="#8a7a5e">※ 方位十字（东·南·西·北·东北·东南·西南·西北·下·上）与「十方各有一大菩萨」相应，八方上下具足。</text>
<text x="34" y="500" font-size="11.5" fill="#8a7a5e">※ 六十侧世界数级作「百佛世界微塵數剎，一一方各十世界」，与八十同量级而句式异——两译各照底本。</text>
</svg>""",
            "cap": "三列各十，一一配位：**菩萨皆「慧」、世界皆「华」、佛皆「月」**。此非偶然同名，而是「行德·感果·智凉」之三翻表法〔本文判断〕。下端递引链七环缺二——**后颂引前颂之说，是矩阵的第二维（行与行相引）；缺二处照底本存，不补**。读此图，当知本品之名号不是装饰，是「以名表位」的完备系统。",
            "en": "Three columns, ten each: all bodhisattvas 慧, all worlds 華, all Buddhas 月 — deed, fruition, and the cool clarity of gnosis, respectively. Below, the chain by which later verses cite earlier ones: seven links, two missing, left as the text has them. The names are not ornament but a complete system of positional notation.",
            "dufa": [
                "**三列同名，是「表法」不是「雷同」。** 十菩萨共一字，则其别在「所证之位」而不在「名」；**读名即读位**。",
                "**澄观之表法语，当与经文分书。** 表中右栏标「澄观表法」，即不许以疏义冒充经文——**此全篇之通例**。",
                "**递引链缺二，是负面证据，须记。** 若以「应有十环」为说而补之，则失校勘之守；**缺处存缺，是文献诚实**。",
            ],
        },
    ],
    "weici_note": "本品为第三会第二品，**与第十三品共为「方便发起」**。澄观判「初二品方便发起，後四品當會正說」；又谓本品「**義有兩兼**」——兼「发起」与「所依」二义，故其体为纯颂，而其用在「赞德以启正说」。",
    "weici": [
        ["13 升须弥山顶（前）", "卷16", "第三会·发起", "645 字·长行为主·十佛颂", "立事"],
        ["**14 须弥顶上偈赞（本品）**", "卷16", "第三会·**方便发起·兼所依**", "2,510 字·纯颂·百颂", "赞德"],
        ["15 十住", "卷16", "第三会·**正说**", "5,589 字·长行＋百颂", "正说十住"],
        ["16 梵行", "卷17", "第三会·胜进", "923 字·纯长行", "位中通行"],
        ["17 初发心功德", "卷17–18", "第三会·满足行相", "8,207 字·十一喻", "校量功德"],
        ["18 明法", "卷18", "第三会·收束", "5,529 字·十法矩阵", "一会之终"],
    ],
    "teshe_note": "本品之特色在**「纯颂而成阵」**：全品无一句正说长行，唯集会长行一段（314 字）与十组起式（18–19 字），余皆颂。**每 lg 恰 200 字、十行无差**，是华严全部重颂品中「整齐度」最高者〔本文判断·据本文所核诸品颂段〕。",
    "teshe": [
        ["纯颂之品", "颂 2,000／全品 2,510（79.7%）", "第十三品颂 280／654（42.8%）", "一会两品，颂之比近二倍"],
        ["颂段整齐", "每 lg 恰 CJK 200，十行无差", "第十五品 lg 2,800（百颂一整块）", "一以十段分，一以整块收"],
        ["三列名数", "菩萨慧×10·世界华×10·佛月×10", "第十三品「十千」×10（庄严名数）", "一以名表位，一以数表严"],
        ["起式公式", "「菩薩承佛」×10·「普觀十方」×9＋「觀察十方」×1", "第十三品「善來」×3", "公式化程度极高，唯三变量轮替"],
        ["递引链", "七环缺二（§2.12）", "他品无此行间互引", "矩阵之第二维"],
        ["篇幅反差", "2,510（前品 645）", "第十三品为全经最短诸品之一", "重颂品反倍长于行品"],
    ],
    "dufa5": [
        ["**阵读**", "只观图 〇-1，不读颂文", "初读本篇者", "得百颂之阵与 200 字之齐"],
        ["**列读**", "只读三列名数表（§4.2）", "欲见以名表位者", "得慧·华·月之三翻"],
        ["**一颂读**", "取法慧首颂与坚固慧末颂对读", "欲见首尾者", "见「初发心」与「灌顶」之照应"],
        ["**引读**", "只读递引链七环", "好文本肌理者", "见颂与颂之互引"],
        ["**承读**", "本品末 → 第十五品 §2.2（总标十住）", "欲见颂如何转长行者", "见「赞德」让位于「列位」"],
    ],
    "shu": [
        ["**T0 经文明文**", "「十方各有一大菩薩……而來詣佛」", "`T10n0279` 卷十六·80-01", "集会长行（314 字）"],
        ["**T0 经文明文**", "菩萨名皆「慧」·世界名皆「華」·佛号皆「月」", "同上·十段起式", "三列名数之实"],
        ["**T0 本文实测**", "**2,510 字／22 单元／100 颂**", "§7.1 逐 lg 验", "计数（本文自测）"],
        ["**T0 本文实测**", "每 lg 恰 CJK 200（十行无差）", "§7.1 逐 lg 验", "计数（本文自测）"],
        ["**T1 澄观《疏》**", "「文有十同義兼三異」「重疊無礙無不互見為一法界圓明大會」", "`T1735` 卷十六", "十同三异之判"],
        ["**T1 澄观《疏》**", "三列表法（發心主導世間／淨治心地如蓮開／智明闇息恩益清涼）", "同上", "以名表位之据"],
        ["**T2 六十**", "109 段·1,421 字（卷七存段）", "`T09n0278`", "对读（存段）"],
    ],
    "shu_note": "> **〔读法〕** 本品之数最整齐：2,510／2,000／100／40／200。**五数相生**：200×10＝2,000（颂），2,000÷20＝100（颂数），100×4＝400（句）。凡整齐至此者，非偶然，是**重颂体例之必然**——颂有定数，字遂有定量。",
}

# ----------------------------------------------------------------------------
# 第十五部　十住品
# ----------------------------------------------------------------------------
P15 = {
    "tag": "P15",
    "path": os.path.join(DIR3, "华严经细读_第十五部_十住品.md"),
    "hui": "第三会（忉利天宫·说十住）",
    "dingwei": "本品为第三会之**正说**，也是全经第一次以「位」为品。读法当**以位为纲、以双十为纬**：十住各有一「所观十法」与一「劝学十法」，同一模板十次实例化。",
    "yiju": "**十住者，从初发心到灌顶，十位各以十法为所缘，而皆结以「不由他悟」**——位是阶梯，悟是自证。",
    "sanwen": "① 十住之次第，是「功德之增」还是「所见之深」？② 每住皆「云何為菩薩…應勸學十法」，何以两列十法而非一列？③ 「不由他悟」十住皆结，此语与第十七品「不由他悟」何以同辞？",
    "tiyao": "本品为第三会**正说之首**，亦第三会篇幅次长之品。品界 **CJK 5,589**（含品题 6·尾重题译由 34），**经文净 5,549**——长行 **2,749** ＋ 重颂 **2,800**。**十九单元**＝1 head＋15 p＋1 lg＋1 byline＋1 短 p（「法慧菩薩言」五字）。长行十住各一 p（CJK 143–286），**颂为一整块 lg，恰 2,800 字＝100 颂 ×28 字**（七言四句·整除无零头）。六十对读〈菩薩十住品第十一〉卷八全本·正文 5,659・220 段。",
    "xufa": "先观图 〇-1 得十住之量与次第，次观图 〇-2 得双十模板之解剖，次读〇之二.3 之坐标，然后入 §二逐段。**模板既识，十住之变乃见。**",
    "en_map": "The first chapter in the sūtra to be built on a *stage*. 5,589 characters: 2,749 of prose and a single verse-block of exactly 2,800 — one hundred ślokas of seven-character lines, divisible with no remainder. Ten abidings, each defined by a set of ten things contemplated and a set of ten things to be practised, each closing on the same phrase: not awakened through another. Fig. 0-1 weighs the ten; Fig. 0-2 dissects the template.",
    "figs": [
        {
            "n": 1,
            "title": "十住阶位与体量梯",
            "what": "位如何成阶",
            "one": "十住各一段长行（143–286 字），末以百颂一整块收",
            "svg": """<svg viewBox="0 0 1000 560" width="100%" style="max-width:1000px;height:auto" xmlns="http://www.w3.org/2000/svg" font-family="serif">
<text x="500" y="24" text-anchor="middle" font-size="14.5" font-weight="bold" fill="#7a5a28">十住之阶：位次为经，字数为纬</text>
<text x="500" y="44" text-anchor="middle" font-size="12" fill="#8a7a5e">条长按各住长行 CJK 比例（1 字＝0.9px）；八十单元 80-005…80-014 逐住实测（§7.5 L2 表）</text>

<g font-size="11.5" fill="#5a5147">
<text x="26" y="76">1 發心住</text><rect x="132" y="62" width="233" height="20" fill="#f7ecd2" stroke="#b8863c" stroke-width="1.3"/><text x="373" y="77" font-weight="bold" fill="#7a5a28">259</text><text x="410" y="77" font-size="10.5" fill="#8a7a5e">十種難得法（十智境）</text>
<text x="26" y="106">2 治地住</text><rect x="132" y="92" width="129" height="20" fill="#e6dbc5" stroke="#c9b98f"/><text x="269" y="107" fill="#7a5a28">143</text><text x="306" y="107" font-size="10.5" fill="#8a7a5e">於諸眾生發十種心</text>
<text x="26" y="136">3 修行住</text><rect x="132" y="122" width="136" height="20" fill="#e6dbc5" stroke="#c9b98f"/><text x="276" y="137" fill="#7a5a28">151</text><text x="313" y="137" font-size="10.5" fill="#8a7a5e">以十種行觀一切法</text>
<text x="26" y="166">4 生貴住</text><rect x="132" y="152" width="136" height="20" fill="#e6dbc5" stroke="#c9b98f"/><text x="276" y="167" fill="#7a5a28">151</text><text x="313" y="167" font-size="10.5" fill="#8a7a5e">從聖教中生成就十法</text>
<text x="26" y="196">5 具足方便住</text><rect x="132" y="182" width="176" height="20" fill="#e6dbc5" stroke="#c9b98f"/><text x="316" y="197" fill="#7a5a28">195</text><text x="353" y="197" font-size="10.5" fill="#8a7a5e">所修善根皆為救護眾生</text>
<text x="26" y="226">6 正心住</text><rect x="132" y="212" width="257" height="20" fill="#e6dbc5" stroke="#c9b98f"/><text x="397" y="227" fill="#7a5a28">286</text><text x="434" y="227" font-size="10.5" fill="#8a7a5e">聞十種法·心定不動</text>
<text x="26" y="256">7 不退住</text><rect x="132" y="242" width="254" height="20" fill="#e6dbc5" stroke="#c9b98f"/><text x="394" y="257" fill="#7a5a28">282</text><text x="431" y="257" font-size="10.5" fill="#8a7a5e">聞十種法·堅固不退</text>
<text x="26" y="286">8 童真住</text><rect x="132" y="272" width="167" height="20" fill="#e6dbc5" stroke="#c9b98f"/><text x="307" y="287" fill="#7a5a28">185</text><text x="344" y="287" font-size="10.5" fill="#8a7a5e">住十種業</text>
<text x="26" y="316">9 王子住</text><rect x="132" y="302" width="158" height="20" fill="#e6dbc5" stroke="#c9b98f"/><text x="298" y="317" fill="#7a5a28">176</text><text x="335" y="317" font-size="10.5" fill="#8a7a5e">善知十種法</text>
<text x="26" y="346">10 灌頂住</text><rect x="132" y="332" width="211" height="20" fill="#e6dbc5" stroke="#c9b98f"/><text x="351" y="347" fill="#7a5a28">234</text><text x="388" y="347" font-size="10.5" fill="#8a7a5e">得成就十種智</text>
</g>

<line x1="132" y1="364" x2="900" y2="364" stroke="#d3c7ae"/>
<text x="26" y="388" font-size="11.5" fill="#5a5147">长行十住合计 <tspan font-weight="bold" fill="#7a5a28">2,062</tspan>　·　序四段＋瑞应＋颂发起＋百颂：其余 3,487</text>
<rect x="132" y="398" width="700" height="26" fill="#d9c9a4" stroke="#c9b98f"/>
<text x="140" y="416" font-size="11.5" fill="#5a5147">重颂 lg ×1　<b>2,800</b>＝100 颂 ×28（七言四句·整除无零头）</text>
<text x="26" y="446" font-size="11.5" fill="#8a7a5e">※ 百颂一整块，不与十住段对齐——**颂不别出其义**（§4.1）：长行已尽，颂唯重述。</text>

<text x="26" y="480" font-size="11.5" fill="#7a5a28">※ 最长为正心（286）与不退（282），最短为治地（143）——**长者皆「闻十种法」，短者皆「发心／观法」**。</text>
<text x="26" y="504" font-size="11.5" fill="#7a5a28">〔本文判断〕体量之分布不随位次递增：**中间二住（6·7）独重**，首尾反轻，非「后后胜前前」之线性。</text>
<text x="26" y="528" font-size="11.5" fill="#8a7a5e">※ 颂段 2,800＝28×100，与第十九品以下诸品之 lg 计量口径同；此数为定界之要据。</text>
<text x="26" y="452" font-size="0" fill="#000">.</text>
</svg>""",
            "cap": "十条之量，长短立见：**最长为正心（286）与不退（282），最短为治地（143）**——长者皆「闻十种法」，短者皆「发心／观法」。**体量不随位次递增**，中间二住独重，首尾反轻〔本文判断〕：此非「后后胜前前」的线性，而是「闻法不动」处说得最详。末段百颂 2,800 字为一整块，不与十住段对齐——**颂不别出其义**。",
            "en": "Ten bars by length, and the pattern is not a ladder: the two middle abidings, steadfastness of mind and non-retrogression, are longest, and both are the ones that say \"hearing ten dharmas, the mind does not move\". The first and last are shorter. Bulk does not increase with stage; the text expands where the test is sharpest. The hundred ślokas at the end form one block of exactly 2,800 characters.",
            "dufa": [
                "**先看长短，再看位次。** 若以为愈高愈详，则与实测相反；**详略随「难处」而不随「高位」**。",
                "**百颂不与十住段对齐，是体例不是错简。** 长行已尽义，颂唯重述——**故不可强以颂配住**，强配则支离。",
                "**「不由他悟」十住皆结，是全品之骨。** 十位虽阶次，而结语同一；**阶次是教，自证是宗**。",
            ],
        },
        {
            "n": 2,
            "title": "双十模板解剖图",
            "what": "住如何构成",
            "one": "所观十法＋劝学十法＋「不由他悟」：同一模板十次实例化",
            "svg": """<svg viewBox="0 0 1000 500" width="100%" style="max-width:1000px;height:auto" xmlns="http://www.w3.org/2000/svg" font-family="serif">
<text x="500" y="24" text-anchor="middle" font-size="14.5" font-weight="bold" fill="#7a5a28">一住之解剖：所观十法 · 劝学十法 · 不由他悟</text>
<text x="500" y="44" text-anchor="middle" font-size="12" fill="#8a7a5e">以「正心住」（80-010·CJK 286）为例；模板十住共用，唯位名与所缘三变量轮替</text>

<rect x="60" y="66" width="880" height="44" rx="5" fill="#f3ecdf" stroke="#c9b98f"/>
<text x="500" y="84" text-anchor="middle" font-size="12" fill="#5a5147">「此菩薩……（所依之行）」</text>
<text x="500" y="101" text-anchor="middle" font-size="10.5" fill="#8a7a5e">位名与所依，十住各异——此处为变量</text>

<rect x="60" y="124" width="420" height="120" rx="5" fill="#f8f3ea" stroke="#d9cdb8"/>
<text x="270" y="146" text-anchor="middle" font-size="12.5" font-weight="bold" fill="#7a5a28">① 所观十法</text>
<text x="270" y="168" text-anchor="middle" font-size="11" fill="#5a5147">「聞十種法，心定不動。何者為十？」</text>
<text x="270" y="192" text-anchor="middle" font-size="10.5" fill="#8a7a5e">列十法——此住所缘之境</text>
<text x="270" y="214" text-anchor="middle" font-size="10.5" fill="#8a7a5e">十住皆一列，无缺无溢</text>
<text x="270" y="234" text-anchor="middle" font-size="10.5" fill="#b8863c">「何者為十」×19（全品）</text>

<rect x="520" y="124" width="420" height="120" rx="5" fill="#f7ecd2" stroke="#b8863c" stroke-width="1.3"/>
<text x="730" y="146" text-anchor="middle" font-size="12.5" font-weight="bold" fill="#7a5a28">② 劝学十法</text>
<text x="730" y="168" text-anchor="middle" font-size="11" fill="#5a5147">「應勸學十法。何等為十？」</text>
<text x="730" y="192" text-anchor="middle" font-size="10.5" fill="#8a7a5e">列十法——此住所修之行</text>
<text x="730" y="214" text-anchor="middle" font-size="10.5" fill="#8a7a5e">「應勸學」×10（十住各一）</text>
<text x="730" y="234" text-anchor="middle" font-size="10.5" fill="#b8863c">「是為十」×9（一列省文·§7.2）</text>

<line x1="480" y1="184" x2="520" y2="184" stroke="#c9b98f"/>
<text x="500" y="176" text-anchor="middle" font-size="10" fill="#8a7a5e">→</text>

<rect x="300" y="262" width="400" height="52" rx="5" fill="#ede4d2" stroke="#c9b98f"/>
<text x="500" y="284" text-anchor="middle" font-size="12.5" font-weight="bold" fill="#7a5a28">③ 「不由他悟」</text>
<text x="500" y="303" text-anchor="middle" font-size="10.5" fill="#8a7a5e">十住皆以此结——同一定式，无一住异</text>

<line x1="270" y1="244" x2="400" y2="262" stroke="#c9b98f"/>
<line x1="730" y1="244" x2="600" y2="262" stroke="#c9b98f"/>

<text x="60" y="344" font-size="12" font-weight="bold" fill="#7a5a28">模板之十次实例化（唯三变量轮替）</text>
<text x="60" y="368" font-size="11.5" fill="#5a5147">变量一：位名（發心→治地→…→灌頂）　变量二：所依之行（见／发心／观法／圣教生…）　变量三：所缘之十法（各异）</text>
<text x="60" y="392" font-size="11.5" fill="#8a7a5e">不变者：「云何為菩薩」×10　·　「應勸學」×10　·　「何者為十／何等為十」×19　·　「不由他悟」结</text>

<line x1="60" y1="410" x2="940" y2="410" stroke="#d3c7ae"/>
<text x="60" y="436" font-size="11.5" fill="#7a5a28">〔本文判断〕此模板之效：**同构十次，则十住之异只在「所缘」，不在「能缘」**——能缘之智是一，所缘之境有十。</text>
<text x="60" y="460" font-size="11.5" fill="#8a7a5e">※ 「何者為十」19 见而「是為十」仅 9 见：一列省文，非缺一法。此计数之差，正是「模板实例化」的文本痕迹。</text>
<text x="60" y="484" font-size="11.5" fill="#8a7a5e">※ 第三会六品之中，本品为唯一以「位」为骨者；余五品或发起（13–14）、或胜进（16）、或校量（17–18）。</text>
</svg>""",
            "cap": "一住之解剖：**①所观十法（所缘之境）→②劝学十法（所修之行）→③「不由他悟」（同一定式）**。此模板十住共用，唯位名、所依之行、所缘十法三变量轮替〔本文判断〕。**同构十次，则十住之异只在所缘，不在能缘**——能缘之智是一，所缘之境有十。「何者為十」19 见而「是為十」仅 9 见，一列省文，正是模板实例化的文本痕迹。",
            "en": "One abiding dissected: ten things contemplated, ten things to be practised, and the same closing phrase, not awakened through another. The template is instantiated ten times with only three variables changing — the name of the stage, the conduct it rests on, and the ten items. The knower is one; the known are ten. Twenty occurrences of \\\"what are the ten\\\" against nine of \\\"this is the ten\\\" mark the template's trace in the text.",
            "dufa": [
                "**双十不是重复，是「境」与「行」的分列。** 所观是所缘，劝学是所修——**一为所见，一为所行**；合之方成一住。",
                "**「不由他悟」须与第十七品同名之语对读。** 同辞而异位：此在十住之结，彼在初发心之极；**同一句话，两处落点**。",
                "**模板之价值在「可预期」。** 读者既识其式，则读第二住时已知其骨；**所当留心者，唯其变处**。",
            ],
        },
    ],
    "weici_note": "本品为第三会**正说之首**。澄观判第三会六品「初二品方便发起，後四品當會正說」；此四品之中，**本品列十住之位，第十六品明位中之行，第十七品校量初发心之德，第十八品以十法收束**——四品成一「位·行·德·法」之全。",
    "weici": [
        ["13–14 升须弥·偈赞", "卷16", "第三会·**方便发起**", "不起而升·百颂赞德", "发起已毕"],
        ["**15 十住（本品）**", "卷16", "第三会·**正说·位**", "十住双十，百颂", "—"],
        ["16 梵行", "卷17", "第三会·正说·**行**", "十法推徵，离相梵行", "位必有行"],
        ["17 初发心功德", "卷17–18", "第三会·**胜进·德**", "十一喻校量", "行必有德"],
        ["18 明法", "卷18", "第三会·**收束·法**", "十法矩阵", "德归诸法，一会终"],
    ],
    "teshe_note": "本品之特色在**「模板之极」**：十住各以同一句式（云何為菩薩…應勸學十法…何者為十…是為十…不由他悟）十次实例化，**在三十九品中，同构程度无出其右者**〔本文判断·据本文所核诸品句式〕。其可读性不在辞，而在「变处」。",
    "teshe": [
        ["模板十次", "「云何為菩薩」×10・「應勸學」×10", "第十四品起式 ×10（菩萨／世界／佛三列）", "一以句式同构，一以名数同构"],
        ["双十并列", "所观十法＋劝学十法（每住二十法）", "第十六品十法推徵＋修十法（双十）", "两品皆「双十」，然一列一破"],
        ["颂段整块", "lg 2,800＝100 颂，不与十住段对齐", "第十四品 lg×10 各 200", "一为整块，一为十段"],
        ["体量非递进", "正心 286・不退 282 最长；治地 143 最短", "第十七品以十一喻递进（后后胜前前）", "一随难处，一随校量"],
        ["「不由他悟」", "十住皆结此语", "第十七品亦有同语（初发心处）", "同辞异位，须对读"],
        ["文本现象", "短 p「法慧菩薩言」五字单独成段", "第十三品有幻影单元 80-04", "两端皆须辨器"],
    ],
    "dufa5": [
        ["**位读**", "只读十住之名与总标（80-004）", "初读本篇者", "得十住之次第"],
        ["**双十读**", "每住只读两列十法之首尾", "欲见模板者", "见境行之分列"],
        ["**变读**", "只比较十住之「所依之行」一句", "好结构者", "见十次实例化之变处"],
        ["**颂读**", "只读百颂，参 §4.1「颂不别出义」", "欲见重颂之体者", "知颂为长行之重述"],
        ["**承读**", "本品 §2.12（灌顶）→ 第十六品 §2.1", "欲见位行之转者", "见「位满」如何转「行净」"],
    ],
    "shu": [
        ["**T0 经文明文**", "「云何為菩薩」×10・「應勸學」×10", "`T10n0279` 卷十六", "模板之句式（结构标志）"],
        ["**T0 经文明文**", "十住名（發心·治地·修行·生貴·具足方便·正心·不退·童真·王子·灌頂）", "同上·80-004", "位名之实"],
        ["**T0 本文实测**", "**5,589 字／净 5,549／长行 2,749＋颂 2,800**", "§7.1 `_e15_stats.py`", "计数（本文自测）"],
        ["**T0 本文实测**", "100 颂＝2,800÷28（整除无零头）", "§7.1 颂验", "计数（本文自测）"],
        ["**T1 澄观《疏》**", "第三会六品「初二品方便發起，後四品當會正說」", "`T1735` 卷十六", "一会之科判"],
        ["**T1 慧苑**", "七分科（甲三昧＋加持→起分→本分→说分→瑞应→证成）", "`X0221` 卷十二", "与澄观科互参"],
        ["**T2 六十**", "〈菩薩十住品第十一〉卷八全本・5,659・220 段", "`T09n0278`", "对读（差 70 字）"],
    ],
    "shu_note": "> **〔读法〕** 本品之数，惟「100 颂＝2,800÷28」一项最为要紧：**整除无零头**，故知 lg 为编者按颂数所定，非自然段落。凡遇此类整数，即是定界之锚。**十住之数（10×2×10＝200 法）亦整，然为义数，不可与字数混。**",
}

# ----------------------------------------------------------------------------
# 第十六部　梵行品
# ----------------------------------------------------------------------------
P16 = {
    "tag": "P16",
    "path": os.path.join(DIR3, "华严经细读_第十六部_梵行品.md"),
    "hui": "第三会（忉利天宫·说十住）",
    "dingwei": "本品为第三会**最短之品**，纯以「推徵」为法：一一问「是梵行耶」，一一答「非」，遮至无所遮，方说「修十种法」。读法当**以遮为纲**。",
    "yiju": "**身非梵行、语非梵行、意非梵行，乃至戒非梵行**——十法俱遣，然后「梵行」之名始立。",
    "sanwen": "① 十法（身·身业·语·语业·意·意业·佛·法·僧·戒）何以恰是此十？② 全品 923 字，何以为十住之「行」？③ 遮遣既尽，何以又须「修十种法」？",
    "tiyao": "本品为**第三会最短、亦全经最短诸品之一**：品界 **CJK 923**（含品题 6·正文 917），**五单元＝1 head＋4 p**，**纯长行·无偈颂**（lg 0·颂 0·偈 0）。四段之量：问端 **50**・过渡 **5**・**推徵核心 669**（占 72.5%）・修十法 **193**（20.9%）。六十对读〈梵行品第十二〉卷八・正文 **993**（比八十多 70 字·核心段反少 133）。",
    "xufa": "先观图 〇-1 得十法遮遣之遍，次观图 〇-2 得「遮后更修」之转折，次读〇之二.3 之坐标，然后入 §二逐段。**遮处既尽，立处自明。**",
    "en_map": "923 characters — the shortest chapter of the third assembly. One question, ten items (body, bodily action, speech, verbal action, mind, mental action, Buddha, dharma, saṅgha, precepts), each answered \"is this the pure practice?\" with a negation, until nothing is left to negate; then, and only then, ten things to be cultivated. Fig. 0-1 shows the sweep of negation; Fig. 0-2 the turn from negation to practice.",
    "figs": [
        {
            "n": 1,
            "title": "十法推徵遮遣图",
            "what": "遮如何遍",
            "one": "身·身業·語·語業·意·意業·佛·法·僧·戒——一一「是梵行耶？」一一非",
            "svg": """<svg viewBox="0 0 1000 500" width="100%" style="max-width:1000px;height:auto" xmlns="http://www.w3.org/2000/svg" font-family="serif">
<text x="500" y="24" text-anchor="middle" font-size="14.5" font-weight="bold" fill="#7a5a28">十法推徵：一一問「是梵行耶」，一一答「非」</text>
<text x="500" y="44" text-anchor="middle" font-size="12" fill="#8a7a5e">十法悉照 `T10n0279` 卷十七（§2.2）；三业各二（身·身業·語·語業·意·意業）＋三宝（佛·法·僧）＋戒</text>

<g font-size="12" fill="#5a5147">
<rect x="40" y="66" width="130" height="28" fill="#f8f3ea" stroke="#d9cdb8"/><text x="105" y="85" text-anchor="middle">身</text>
<rect x="178" y="66" width="130" height="28" fill="#f8f3ea" stroke="#d9cdb8"/><text x="243" y="85" text-anchor="middle">身業</text>
<rect x="316" y="66" width="130" height="28" fill="#f8f3ea" stroke="#d9cdb8"/><text x="381" y="85" text-anchor="middle">語</text>
<rect x="454" y="66" width="130" height="28" fill="#f8f3ea" stroke="#d9cdb8"/><text x="519" y="85" text-anchor="middle">語業</text>
<rect x="592" y="66" width="130" height="28" fill="#f8f3ea" stroke="#d9cdb8"/><text x="657" y="85" text-anchor="middle">意</text>
<rect x="730" y="66" width="130" height="28" fill="#f8f3ea" stroke="#d9cdb8"/><text x="795" y="85" text-anchor="middle">意業</text>
<rect x="40" y="102" width="130" height="28" fill="#f3ecdf" stroke="#c9b98f"/><text x="105" y="121" text-anchor="middle">佛</text>
<rect x="178" y="102" width="130" height="28" fill="#f3ecdf" stroke="#c9b98f"/><text x="243" y="121" text-anchor="middle">法</text>
<rect x="316" y="102" width="130" height="28" fill="#f3ecdf" stroke="#c9b98f"/><text x="381" y="121" text-anchor="middle">僧</text>
<rect x="454" y="102" width="130" height="28" fill="#f7ecd2" stroke="#b8863c" stroke-width="1.3"/><text x="519" y="121" text-anchor="middle">戒</text>
</g>
<text x="600" y="121" font-size="10.5" fill="#8a7a5e">（三宝＋戒·四法列第二行）</text>

<line x1="40" y1="148" x2="960" y2="148" stroke="#c9b98f"/>
<text x="40" y="172" font-size="12" font-weight="bold" fill="#b8863c">「為身是梵行耶？……乃至戒是梵行耶？」——一問遍十法</text>

<text x="40" y="204" font-size="12" font-weight="bold" fill="#7a5a28">答：一一非。理由三式（§2.2）</text>
<g font-size="11.5" fill="#5a5147">
<rect x="40" y="216" width="290" height="72" rx="4" fill="#ffffff" stroke="#e0d6c2"/>
<text x="60" y="238" font-weight="bold">① 九喻非圣</text>
<text x="60" y="258" font-size="10.5" fill="#8a7a5e">如幻·如夢·如影·如響·如化·如空</text>
<text x="60" y="276" font-size="10.5" fill="#8a7a5e">无实体故，不可名为梵行</text>

<rect x="350" y="216" width="290" height="72" rx="4" fill="#ffffff" stroke="#e0d6c2"/>
<text x="370" y="238" font-weight="bold">② 離諸相</text>
<text x="370" y="258" font-size="10.5" fill="#8a7a5e">梵行者，非有相·非无相</text>
<text x="370" y="276" font-size="10.5" fill="#8a7a5e">取相即非，离相亦不可得</text>

<rect x="660" y="216" width="300" height="72" rx="4" fill="#ffffff" stroke="#e0d6c2"/>
<text x="680" y="238" font-weight="bold">③ 無所得</text>
<text x="680" y="258" font-size="10.5" fill="#8a7a5e">若言「是梵行」，即有所得</text>
<text x="680" y="276" font-size="10.5" fill="#8a7a5e">无所得故，乃名梵行</text>
</g>

<text x="40" y="320" font-size="12" font-weight="bold" fill="#7a5a28">遮遣之结构：不是「否定十法」，是「否定『十法即梵行』之命题」</text>
<text x="40" y="344" font-size="11.5" fill="#5a5147">十法本身不破（身·语·意·佛·法·僧·戒皆在），所破者**以之为梵行**之执——**法不破，执法破**。〔本文判断〕</text>

<line x1="40" y1="362" x2="960" y2="362" stroke="#d3c7ae"/>
<text x="40" y="388" font-size="11.5" fill="#8a7a5e">※ 十法之选，非随意：**三业各开体用（身／身業·語／語業·意／意業）成六，加三宝与戒成十**——</text>
<text x="40" y="410" font-size="11.5" fill="#8a7a5e">　 六为「所修之器」，三宝为「所依之境」，戒为「所守之律」；十法盖尽修行之全域。</text>
<text x="40" y="436" font-size="11.5" fill="#7a5a28">※ 本品推徵占 669 字（72.5%）——**全品之重，尽在遮门**；立门（修十法）仅 193 字。</text>
<text x="40" y="460" font-size="11.5" fill="#8a7a5e">※ 问端仅 50 字：「正念天子问·云何而得梵行清净」——**一问到底，无第二问**。</text>
<text x="40" y="484" font-size="11.5" fill="#8a7a5e">※ 六十侧核心段 536 字（比八十少 133），而问端多 19——两译详略互易，各照底本。</text>
</svg>""",
            "cap": "十法一一受问：「为身是梵行耶？……乃至戒是梵行耶？」而一一答非。**所破者不是十法，是以十法为梵行之执**——法不破，执法破〔本文判断〕。三式理由（九喻非圣·离诸相·无所得）层层收窄，至「无所得」而无处可立。**本品 72.5% 的字数用于此遮门**；立门（修十法）仅 193 字。",
            "en": "Ten items, each asked whether it is the pure practice, each answered no. What is negated is not the ten but the proposition that they *are* the practice: the dharmas stand, the grasping does not. Three grounds narrow successively — the nine similes, the absence of marks, the unattainability — until nothing is left to stand on. Nearly three quarters of the chapter is spent here; the positive half takes 193 characters.",
            "dufa": [
                "**遮不是虚无，是「不许以偏为全」。** 十法各是修行之一端，执一端为全体，则非；**故遮其执，不遮其法**。",
                "**「無所得」是遮门之极，也是立门之枢。** 无所立而后可修——**若先有所得，则修成执**。",
                "**十法之数当作「全域」读。** 三业开六、三宝加戒——**十非列举，是穷尽**。〔本文判断〕",
            ],
        },
        {
            "n": 2,
            "title": "遮后更修·五段体量转折图",
            "what": "遮后何立",
            "one": "问端 50→过渡 5→推徵 669→修十法 193；遮尽而立",
            "svg": """<svg viewBox="0 0 1000 470" width="100%" style="max-width:1000px;height:auto" xmlns="http://www.w3.org/2000/svg" font-family="serif">
<text x="500" y="24" text-anchor="middle" font-size="14.5" font-weight="bold" fill="#7a5a28">九百二十三字之分配：遮门七成二，立门二成</text>
<text x="500" y="44" text-anchor="middle" font-size="12" fill="#8a7a5e">条长按 CJK 比例（1 字＝1.1px）；五单元＝1 head＋4 p（§7.5.2）</text>

<g font-size="12" fill="#5a5147">
<text x="30" y="82">品题</text><rect x="150" y="68" width="7" height="20" fill="#d9cdb8" stroke="#c9b98f"/><text x="166" y="83" font-size="11" fill="#8a7a5e">6</text>
<text x="30" y="112">80-001 問端</text><rect x="150" y="98" width="55" height="20" fill="#e6dbc5" stroke="#c9b98f"/><text x="214" y="113" font-size="11" fill="#8a7a5e">50　正念天子問「云何而得梵行清净」</text>
<text x="30" y="142">80-002 過渡</text><rect x="150" y="128" width="6" height="20" fill="#e6dbc5" stroke="#c9b98f"/><text x="165" y="143" font-size="11" fill="#8a7a5e">5　「法慧菩薩言」</text>
<text x="30" y="172">80-003 推徵</text><rect x="150" y="158" width="736" height="20" fill="#f7ecd2" stroke="#b8863c" stroke-width="1.4"/><text x="894" y="173" font-size="11.5" font-weight="bold" fill="#7a5a28">669</text>
<text x="30" y="202">80-004 修十法</text><rect x="150" y="188" width="212" height="20" fill="#e6dbc5" stroke="#c9b98f"/><text x="370" y="203" font-size="11" fill="#8a7a5e">193　十力·大慈悲·如幻如梦</text>
</g>
<text x="150" y="228" font-size="11" fill="#b8863c">↑ 推徵占 72.5%</text>
<text x="150" y="248" font-size="11" fill="#8a7a5e">↑ 立门占 20.9%　·　问端与过渡共 6%</text>

<line x1="30" y1="266" x2="970" y2="266" stroke="#c9b98f"/>
<text x="30" y="292" font-size="12.5" font-weight="bold" fill="#7a5a28">转折之枢：遮尽而立——末段 193 字全品之归宿</text>
<text x="30" y="316" font-size="11.5" fill="#5a5147">「復應修習十種法。何者為十？所謂：處非處智、過現未來業報智、諸禪解脫三昧智、諸根勝劣智、</text>
<text x="30" y="336" font-size="11.5" fill="#5a5147">種種解智、種種界智、一切至處道智、天眼無礙智、宿命無礙智、永斷習氣智。」——即如来十力之智境</text>

<rect x="30" y="352" width="940" height="52" rx="4" fill="#f7ecd2" stroke="#b8863c"/>
<text x="46" y="372" font-size="11.5" font-weight="bold" fill="#7a5a28">末句：「初發心時即得阿耨多羅三藐三菩提，知一切法即心自性，成就慧身，不由他悟。」</text>
<text x="46" y="392" font-size="11" fill="#8a7a5e">此句直贯第十七品——**遮尽而立，立处即是初心**；故本品虽短，为全会之枢。</text>

<text x="30" y="432" font-size="11.5" fill="#8a7a5e">※ 五段之量：6＋50＋5＋669＋193＝923，与品界 CJK 全合（§7.5.2 守恒）。</text>
<text x="30" y="456" font-size="11.5" fill="#7a5a28">※ 六十侧 993 字（多 70）：其核心段反少 133，而问端多 19——<tspan>两译之详略互易，非一详一略</tspan>。</text>
</svg>""",
            "cap": "九百二十三字之分配：**推徵 669（72.5%）、修十法 193（20.9%）、问端与过渡共 55（6%）**。全品之重尽在遮门，而立门只 193 字——**遮尽而立，立处即初心**。末句「初发心时即得阿耨多罗三藐三菩提，知一切法即心自性，成就慧身，不由他悟」直贯第十七品，**故本品虽为全会最短，实为全会之枢**。",
            "en": "923 characters: 669 of negation, 193 of practice, 55 of question and transition. The weight lies almost wholly in the sweeping-away; what is then established is ten forms of the Tathāgata's knowledge, and the chapter closes on the line that the first arousal of the mind itself attains awakening, knowing all dharmas as the mind's own nature — a body of wisdom, not awakened through another. Shortest in the assembly, and its hinge.",
            "dufa": [
                "**先读末段，回读遮门。** 知其所立，则遮门之每一「非」皆有着落；**否则九百字尽是空言**。",
                "**「不由他悟」两品同辞，当合看。** 此在梵行之末，彼在初发心之极——**一行一德，同证一悟**。",
                "**两译详略互易，最宜细辨。** 八十核心多 133 而问端少 19；**若以为「详者必后出」，则误**。",
            ],
        },
    ],
    "weici_note": "本品为第三会第四品（正说四品之二），**十住之「行」**：前品列位，本品明「位中所有之行」。澄观判此品「**以離相為梵行**」，与第十五品之「以十法为位」恰成体用。",
    "weici": [
        ["15 十住（前）", "卷16", "第三会·正说·**位**", "十住双十，百颂", "位已列"],
        ["**16 梵行（本品）**", "卷17", "第三会·正说·**行**", "十法推徵，离相梵行", "位中必有行"],
        ["17 初发心功德", "卷17–18", "第三会·**胜进·德**", "十一喻校量，121 颂", "行成而德显"],
        ["18 明法", "卷18", "第三会·**收束**", "十法矩阵", "德归诸法"],
    ],
    "teshe_note": "本品之特色在**「以遮为宗而极短」**：923 字，五单元，纯长行，无偈颂，**全品四分之三用于否定**。在三十九品中，**以如此短的篇幅、如此高的遮遣比例而成一品者，唯此一品**〔本文判断·据本文所核诸品〕。",
    "teshe": [
        ["篇幅", "CJK 923（第三会最短）", "第十七品 8,207（第三会最长）", "同会之中，相去近九倍"],
        ["文体", "纯长行・lg 0・颂 0・偈 0", "第十五品长行＋百颂；第十七品长行＋121 颂", "一会六品，唯此品全无偈"],
        ["遮遣比例", "推徵 669／923＝72.5%", "第十八品以「立」为主（十法矩阵）", "一遮一立，恰成对照"],
        ["篇幅与译", "八十 923／六十 993（差 +70）", "第十二品两译差仅 69", "两译之差，未必同向"],
        ["单元", "5（1 head＋4 p）", "第十七品 27；第十八品 32", "单元少而字密"],
        ["枢机语", "「初發心時即得…不由他悟」", "第十七品全品即此句之展开", "短品为长品之纲"],
    ],
    "dufa5": [
        ["**遮读**", "只读十法之「是梵行耶」与「非」", "初读本篇者", "得遮门之遍"],
        ["**立读**", "只读 80-004 修十法一段", "欲见归宿者", "得十力之智境"],
        ["**枢读**", "只读末句「不由他悟」", "欲见全会脉络者", "见短品之重"],
        ["**校读**", "§7.5.3 两译对读表", "欲核文本者", "得详略互易之实"],
        ["**承读**", "本品末句 → 第十七品 §2.0", "欲见展开者", "见一句如何成八品之最"],
    ],
    "shu": [
        ["**T0 经文明文**", "「為身是梵行耶？……乃至戒是梵行耶？」", "`T10n0279` 卷十七·80-003", "十法推徵之问"],
        ["**T0 经文明文**", "「初發心時即得阿耨多羅三藐三菩提……不由他悟」", "同上·80-004 末", "全品枢机"],
        ["**T0 本文实测**", "**923 字／正文 917／5 单元**", "§7.5.2", "计数（本文自测）"],
        ["**T0 本文实测**", "推徵 669・修十法 193・问端 50・过渡 5", "§7.5.2", "计数（本文自测）"],
        ["**T1 澄观《疏》**", "以離相為梵行", "`T1735` 卷十七", "释名之据"],
        ["**T1 法藏《探玄记》**", "「梵行品第十二」（六十品次）", "`T1733` 卷十一", "品次对照"],
        ["**T2 六十**", "正文 993・核心段 536・问端 69", "`T09n0278` 卷八", "对读（详略互易）"],
    ],
    "shu_note": "> **〔读法〕** 本品之数最简：923・669・193・50・5。**五数之要，在「669 与 193 之比」**——遮与立近于 3.5:1。凡读此类以遮为宗之品，**比例即是教法**：遮不厌详，立不厌简。若倒转其比例，则成「以理废行」；若执其简而立，则成「执药成病」。",
}

# ----------------------------------------------------------------------------
# 第十七部　初发心功德品
# ----------------------------------------------------------------------------
P17 = {
    "tag": "P17",
    "path": os.path.join(DIR3, "华严经细读_第十七部_初发心功德品.md"),
    "hui": "第三会（忉利天宫·说十住）",
    "dingwei": "本品为第三会**最长之品**，全品只是一件事：**以无分限之法，校有分限之喻**。读法当**以喻为纲**——十一喻层层转胜，而至末仍曰「不可说」。",
    "yiju": "**初发心功德，无有能得知其际者**——十一喻皆可数，而所校之法不可数；喻有尽，法无尽。",
    "sanwen": "① 十一喻何以必须「后后过于前前」而不能并列举？② 发心功德既「不可说」，何故又说八千余字？③ 本品与第十六品末句「不由他悟」是何关系？",
    "tiyao": "本品为**第三会最长品**：品界 **CJK 8,207**——长行 **4,785**（58.3%）＋ 重颂 **3,388**（41.3%）＋ 品题译场 21。**二十七单元**＝1 head＋25 p＋1 lg＋1 byline。重颂为七言，**净句段 484・均长 7.0 言**，通 **121 颂**。品题「初發心功德品第十七」，译场「于闐國三藏實叉難陀奉　制譯」。全品结构：天王请说→叹深难说（十难）→**约喻校量（十一喻）**→就法略示→动地兴供→他方证成（万佛同名）→以偈重颂。",
    "xufa": "先观图 〇-1 得十一喻之次第与「转胜」之法，次观图 〇-2 得「喻有分限·法无限」之数理，次读〇之二.3 之坐标，然后入 §二逐段。**喻既尽，方知不可尽。**",
    "en_map": "The longest chapter of the third assembly: 8,207 characters, 4,785 of prose and 3,388 of verse (121 ślokas of seven-character lines). It says one thing only — that the merit of the first arousal of the mind cannot be measured — and it says it by eleven similes, each surpassing the last, each with four parts and ten layers within, until the similes run out and the point stands: what is measured is finite, the measuring is not.",
    "figs": [
        {
            "n": 1,
            "title": "十一大喻·层层转胜图",
            "what": "喻如何转",
            "one": "后后过于前前，故皆捨置前前、更举后后——十一级而上",
            "svg": """<svg viewBox="0 0 1000 600" width="100%" style="max-width:1000px;height:auto" xmlns="http://www.w3.org/2000/svg" font-family="serif">
<text x="500" y="24" text-anchor="middle" font-size="14.5" font-weight="bold" fill="#7a5a28">十一大喻：后后过于前前，捨置前前更举后后</text>
<text x="500" y="44" text-anchor="middle" font-size="12" fill="#8a7a5e">喻名与单元依澄观科（`T1735`·§7.5.2）；每喻具「举喻·征问·领答·校量」四句，一一喻内皆有十重</text>

<g font-size="11.5" fill="#5a5147">
<text x="26" y="78">1</text><rect x="56" y="64" width="30" height="18" fill="#e6dbc5" stroke="#c9b98f"/><text x="96" y="78">利樂眾生喻</text><text x="230" y="78" font-size="10.5" fill="#8a7a5e">供養樂具·持戒修善</text><text x="470" y="78" font-size="10.5" fill="#8a7a5e">80-004–008</text>
<text x="26" y="110">2</text><rect x="56" y="96" width="46" height="18" fill="#e6dbc5" stroke="#c9b98f"/><text x="112" y="110">速疾步剎喻</text><text x="230" y="110" font-size="10.5" fill="#8a7a5e">一念過剎·展轉至十</text><text x="470" y="110" font-size="10.5" fill="#8a7a5e">80-009</text>
<text x="26" y="142">3</text><rect x="56" y="128" width="62" height="18" fill="#e6dbc5" stroke="#c9b98f"/><text x="128" y="142">知劫成壞喻</text><text x="230" y="142" font-size="10.5" fill="#8a7a5e">知世界成壞劫數</text><text x="470" y="142" font-size="10.5" fill="#8a7a5e">80-010</text>
<text x="26" y="174">4</text><rect x="56" y="160" width="78" height="18" fill="#e6dbc5" stroke="#c9b98f"/><text x="144" y="174">善知勝解喻</text><text x="230" y="174" font-size="10.5" fill="#8a7a5e">知眾生種種差別解</text><text x="470" y="174" font-size="10.5" fill="#8a7a5e">80-011</text>
<text x="26" y="206">5</text><rect x="56" y="192" width="94" height="18" fill="#e6dbc5" stroke="#c9b98f"/><text x="160" y="206">善知諸根喻</text><text x="230" y="206" font-size="10.5" fill="#8a7a5e">知眾生諸根差別</text><text x="470" y="206" font-size="10.5" fill="#8a7a5e">80-012</text>
<text x="26" y="238">6</text><rect x="56" y="224" width="110" height="18" fill="#e6dbc5" stroke="#c9b98f"/><text x="176" y="238">善知欲樂喻</text><text x="300" y="238" font-size="10.5" fill="#8a7a5e">知眾生種種欲樂</text><text x="470" y="238" font-size="10.5" fill="#8a7a5e">80-013</text>
<text x="26" y="270">7</text><rect x="56" y="256" width="126" height="18" fill="#e6dbc5" stroke="#c9b98f"/><text x="192" y="270">善知方便喻</text><text x="300" y="270" font-size="10.5" fill="#8a7a5e">知眾生種種方便</text><text x="470" y="270" font-size="10.5" fill="#8a7a5e">80-014</text>
<text x="26" y="302">8</text><rect x="56" y="288" width="142" height="18" fill="#e6dbc5" stroke="#c9b98f"/><text x="208" y="302">善知他心喻</text><text x="300" y="302" font-size="10.5" fill="#8a7a5e">知眾生種種差別心</text><text x="470" y="302" font-size="10.5" fill="#8a7a5e">80-015</text>
<text x="26" y="334">9</text><rect x="56" y="320" width="158" height="18" fill="#e6dbc5" stroke="#c9b98f"/><text x="224" y="334">善知業相喻</text><text x="300" y="334" font-size="10.5" fill="#8a7a5e">知眾生種種差別業</text><text x="470" y="334" font-size="10.5" fill="#8a7a5e">80-016</text>
<text x="26" y="366">10</text><rect x="56" y="352" width="174" height="18" fill="#e6dbc5" stroke="#c9b98f"/><text x="240" y="366">善知煩惱喻</text><text x="300" y="366" font-size="10.5" fill="#8a7a5e">知眾生種種煩惱</text><text x="470" y="366" font-size="10.5" fill="#8a7a5e">80-017</text>
<text x="26" y="398">11</text><rect x="56" y="384" width="196" height="18" fill="#f7ecd2" stroke="#b8863c" stroke-width="1.4"/><text x="262" y="398" font-weight="bold" fill="#7a5a28">供佛及生喻</text><text x="360" y="398" font-size="10.5" fill="#8a7a5e">供養無邊諸佛及眾生</text><text x="540" y="398" font-size="10.5" fill="#8a7a5e">80-018–020</text>
</g>

<line x1="56" y1="412" x2="252" y2="412" stroke="#b8863c"/>
<path d="M 56 412 L 66 407 L 66 417 Z" fill="#b8863c"/>
<text x="60" y="432" font-size="10.5" fill="#b8863c">渐次转胜</text>

<text x="600" y="78" font-size="11.5" fill="#7a5a28">读此阶之三事</text>
<text x="600" y="104" font-size="11.5" fill="#5a5147">① **不可并列**：若十一喻并列，则读者择一而足；</text>
<text x="600" y="124" font-size="11.5" fill="#5a5147">　 必「捨前举后」，乃显「无有一喻能尽」。</text>
<text x="600" y="150" font-size="11.5" fill="#5a5147">② **后后胜前前**：所校之数愈后愈大，</text>
<text x="600" y="170" font-size="11.5" fill="#5a5147">　 而所校之法（发心功德）始终不动。</text>
<text x="600" y="196" font-size="11.5" fill="#5a5147">③ **四句十重**：每喻皆「举喻·征问·领答·校量」，</text>
<text x="600" y="216" font-size="11.5" fill="#5a5147">　 一一喻内「皆有十重」——**结构之密在全经之首**。</text>

<rect x="600" y="240" width="370" height="130" rx="5" fill="#f8f3ea" stroke="#d9cdb8"/>
<text x="616" y="262" font-size="11.5" font-weight="bold" fill="#7a5a28">第十一喻之结：喻尽而法不尽</text>
<text x="616" y="284" font-size="10.5" fill="#5a5147">「設有供養無邊諸佛及眾生，</text>
<text x="616" y="302" font-size="10.5" fill="#5a5147">　 其心廣大，猶如虛空……」</text>
<text x="616" y="324" font-size="10.5" fill="#5a5147">校量至此而止：**所校者愈大，愈见其不及**。</text>
<text x="616" y="346" font-size="10.5" fill="#b8863c">→ 喻有分限，法无限（图 〇-2）</text>

<text x="26" y="470" font-size="11.5" fill="#8a7a5e">※ 十一喻之名，本文悉依澄观科；喻内之次序与单元，据 §7.5.2 表与 §2.3–2.6 逐段核定。</text>
<text x="26" y="494" font-size="11.5" fill="#8a7a5e">※ 第一喻独占五单元（80-004–008），余十喻各一至三单元——**首喻立式，余喻效之**。</text>
<text x="26" y="518" font-size="11.5" fill="#7a5a28">※ 本品之「校量」非算术，是**归谬**：设一极大之数，证其犹不及，则所证者非数所能及。〔本文判断〕</text>
<text x="26" y="542" font-size="11.5" fill="#8a7a5e">※ 重颂 121 颂（3,388 字）为长行之重述，不与十一喻一一对应；颂以七言，净句段 484·均长 7.0。</text>
<text x="26" y="566" font-size="11.5" fill="#8a7a5e">※ 他方证成段「万佛同名」——以他方之证，证此方之说；与第十三品「十佛曾入」同一手法。</text>
</svg>""",
            "cap": "十一喻自「利乐众生」升至「供佛及生」，一级一级捨前举后。**不可并列，是此法之要**：若十一喻并列，读者择一而足；必捨前举后，乃显「无有一喻能尽」〔本文判断〕。每喻具四句、内含十重，**结构之密为全经之首**。至第十一喻而止，所校者愈大，愈见其不及——**喻有分限，法无限**。",
            "en": "Eleven similes rising from benefiting beings to honouring Buddhas beyond count, each discarding the last. They cannot be laid side by side: if they were, a reader could take one and be satisfied. Each has four parts and ten layers within — the densest structure in the whole sūtra. At the eleventh the similes stop, and the larger the measure, the more plainly it falls short.",
            "dufa": [
                "**读一喻，须读其「捨」字。** 「捨置前前，更举后后」——**捨是此法的一半**；不读捨，则十一喻成十一例。",
                "**校量不是算数，是归谬。** 设极大之数而证其不及，则所证者非数所能及——**故终以「不可说」收**。",
                "**四句十重，宜取一喻细读。** 十一喻全读则疲；**取第一喻（80-004–008）读透，余十喻之式自明**。",
            ],
        },
        {
            "n": 2,
            "title": "喻有分限·法无限图",
            "what": "数如何穷",
            "one": "长行 4,785／重颂 3,388；阿僧祇 21・无量 46・不可说不可说 4",
            "svg": """<svg viewBox="0 0 1000 560" width="100%" style="max-width:1000px;height:auto" xmlns="http://www.w3.org/2000/svg" font-family="serif">
<text x="500" y="24" text-anchor="middle" font-size="14.5" font-weight="bold" fill="#7a5a28">八千二百字，只证一句「不可说」</text>
<text x="500" y="44" text-anchor="middle" font-size="12" fill="#8a7a5e">左：体量分配；右：校量数词频（body80 CJK-only 实测·§7.5.1）</text>

<text x="30" y="80" font-size="12.5" font-weight="bold" fill="#7a5a28">体量</text>
<rect x="30" y="92" width="300" height="230" fill="#f8f3ea" stroke="#d9cdb8"/>
<rect x="46" y="106" width="268" height="126" fill="#e6dbc5" stroke="#c9b98f"/>
<text x="180" y="160" text-anchor="middle" font-size="13" font-weight="bold" fill="#7a5a28">長行 4,785</text>
<text x="180" y="180" text-anchor="middle" font-size="11" fill="#5a5147">25 p　·　58.3%</text>
<text x="180" y="210" text-anchor="middle" font-size="10.5" fill="#8a7a5e">十一喻皆在此</text>
<rect x="46" y="238" width="190" height="74" fill="#d9c9a4" stroke="#c9b98f"/>
<text x="141" y="272" text-anchor="middle" font-size="12.5" font-weight="bold" fill="#7a5a28">重頌 3,388</text>
<text x="141" y="292" text-anchor="middle" font-size="10.5" fill="#5a5147">1 lg　·　41.3%　·　121 頌</text>
<text x="30" y="342" font-size="10.5" fill="#8a7a5e">品题＋译场 21（0.3%）</text>
<text x="30" y="364" font-size="10.5" fill="#7a5a28">合计 8,207＝第三会最长品</text>

<text x="380" y="80" font-size="12.5" font-weight="bold" fill="#7a5a28">校量数词频（1 次＝6px）</text>
<g font-size="11" fill="#5a5147">
<text x="380" y="110">無量</text><rect x="470" y="98" width="276" height="16" fill="#d9c9a4" stroke="#c9b98f"/><text x="754" y="111" fill="#7a5a28">46</text>
<text x="380" y="136">佛子</text><rect x="470" y="124" width="228" height="16" fill="#e6dbc5" stroke="#c9b98f"/><text x="706" y="137">38</text>
<text x="380" y="162">十方</text><rect x="470" y="150" width="228" height="16" fill="#e6dbc5" stroke="#c9b98f"/><text x="706" y="163">38</text>
<text x="380" y="188">阿耨多羅三藐三菩提心</text><rect x="470" y="176" width="186" height="16" fill="#e6dbc5" stroke="#c9b98f"/><text x="664" y="189">31</text>
<text x="380" y="214">阿僧祇</text><rect x="470" y="202" width="126" height="16" fill="#f7ecd2" stroke="#b8863c" stroke-width="1.3"/><text x="604" y="215" font-weight="bold" fill="#7a5a28">21</text>
<text x="380" y="240">初發心</text><rect x="470" y="228" width="66" height="16" fill="#e6dbc5" stroke="#c9b98f"/><text x="544" y="241">11</text>
<text x="380" y="266">那由他</text><rect x="470" y="254" width="48" height="16" fill="#e6dbc5" stroke="#c9b98f"/><text x="526" y="267">8</text>
<text x="380" y="292">微塵數</text><rect x="470" y="280" width="30" height="16" fill="#e6dbc5" stroke="#c9b98f"/><text x="508" y="293">5</text>
<text x="380" y="318">優波尼沙陀</text><rect x="470" y="306" width="24" height="16" fill="#e6dbc5" stroke="#c9b98f"/><text x="502" y="319">4</text>
<text x="380" y="344">不可說不可說</text><rect x="470" y="332" width="24" height="16" fill="#e6dbc5" stroke="#c9b98f"/><text x="502" y="345">4</text>
</g>

<line x1="30" y1="382" x2="970" y2="382" stroke="#c9b98f"/>
<text x="30" y="408" font-size="12.5" font-weight="bold" fill="#b8863c">数之梯：阿僧祇 → 那由他 → 不可說不可說 → 喻 → 法</text>
<text x="30" y="432" font-size="11.5" fill="#5a5147">前四者皆是「有分限之极」：阿僧祇（无数）·那由他（千万亿）·不可说不可说（言语道断）——**而皆不足以校发心功德**。</text>
<text x="30" y="456" font-size="11.5" fill="#5a5147">故第十一喻后,不说「更多」，而说「無有能得知其際者」——**从「量」跳到「无量」,不是加法,是换轴**。〔本文判断〕</text>

<rect x="30" y="476" width="940" height="56" rx="4" fill="#f7ecd2" stroke="#b8863c"/>
<text x="46" y="496" font-size="11.5" font-weight="bold" fill="#7a5a28">〔数理之眼〕凡校量之文，其效不在末数之大，而在「捨」之次数：十一捨而后不可说，则读者自弃其计量之习。</text>
<text x="46" y="516" font-size="11" fill="#8a7a5e">此与第十四品「以十为量、以无尽为归」同法，而此品以「捨」行之，彼品以「引」行之。</text>
</svg>""",
            "cap": "左为体量（长行 4,785・重颂 3,388），右为校量数词频。**关键不在「无量」46 见之多，而在数梯之顶**：阿僧祇→那由他→不可说不可说，皆是「有分限之极」，而皆不足以校发心功德。**故末不说「更多」，而说「无有能得知其际者」——从「量」跳到「无量」，不是加法，是换轴**〔本文判断〕。",
            "en": "Left, the body: 4,785 of prose, 3,388 of verse. Right, the frequency of measuring words. What matters is not that \\\"measureless\\\" occurs 46 times but where the ladder ends: asaṃkhya, nayuta, \\\"unutterable upon unutterable\\\" — each an extremity of the finite, and none sufficient. So the close is not \\\"more\\\" but \\\"no one can know its limit\\\": not addition but a change of axis.",
            "dufa": [
                "**数词之频，不作「重点」读。** 「无量」46 见只证其反复；**要者在「捨」之结构**，不在词频之高低。",
                "**「不可说」不是修辞上的放弃，是方法论上的转身。** 说不可说，仍说八千字——**所说者为「何以不可说」，非「不可说者为何」**。",
                "**与第十四品对看，见两种「无尽」。** 彼以「引」至无尽（递引链），此以「捨」至无尽（十一喻）——**一纵一横，同归无尽**。",
            ],
        },
    ],
    "weici_note": "本品为第三会第五品，**十住之「德」**：前二品（15–16）立位与行，此品校量「初发心」之功德——**位行之极，归于初心**。澄观判此品为「**勝進**」：十住自分已毕，此明趣入十行之胜进功德。",
    "weici": [
        ["15 十住", "卷16", "第三会·正说·位", "十住双十，百颂", "位立"],
        ["16 梵行", "卷17", "第三会·正说·行", "十法推徵，离相梵行", "行净"],
        ["**17 初发心功德（本品）**", "卷17–18", "第三会·**胜进·德**", "十一喻校量，121 颂", "德显"],
        ["18 明法", "卷18", "第三会·**收束·法**", "十法矩阵，双颂", "德归诸法"],
        ["19 昇夜摩天宮", "卷19", "第四会·十行·发起", "不起而升（重演）", "第三会竟，四会启"],
    ],
    "teshe_note": "本品之特色在**「以校量为全部内容」**：八千余字，不出「发心功德不可量」一事，而层层设喻以证之。**在三十九品中，以如此长的篇幅、只作一件事（校量）者，唯此一品**〔本文判断·据本文所核诸品〕。",
    "teshe": [
        ["篇幅", "CJK 8,207（第三会最长）", "第十六品 923（第三会最短）", "同会之中，相去近九倍"],
        ["内容单一", "全品只「校量发心功德」一事", "第十八品十五组十法，条目繁多", "一以深，一以广"],
        ["校量结构", "十一喻，后后胜前前，皆捨置前前", "第八品四十名并列（矩阵，不转胜）", "一为链，一为阵"],
        ["数与语", "阿僧祇 21・无量 46・不可说不可说 4", "第十八品阿僧祇仅 1", "一会之内，数语之偏至此"],
        ["重颂", "121 颂・3,388 字（41.3%）", "第十八品双颂仅 588（10.6%）", "一以颂重述，一以颂点缀"],
        ["证成", "他方万佛同名证成", "第十三品十佛曾入证成", "两品同以「他证」立信"],
    ],
    "dufa5": [
        ["**喻读**", "只读十一喻之「举喻」一句", "初读本篇者", "得十一喻之次第"],
        ["**一喻读**", "取第一喻（80-004–008）读透", "欲见四句十重者", "得校量之全式"],
        ["**数读**", "只观图 〇-2 与 §7.5.1 词频", "好数量级者", "见「换轴」之法"],
        ["**颂读**", "读 §2.7 重颂，比其与长行之异同", "欲见重颂体者", "知颂为长行之重述"],
        ["**承读**", "本品 §2.4 → 第十八品 §2.1", "欲见会终者", "见「德」如何收为「法」"],
    ],
    "shu": [
        ["**T0 经文明文**", "「無有能得知其際者」", "`T10n0279` 卷十七–十八", "校量之结语"],
        ["**T0 经文明文**", "十一喻之「举喻」句", "同上·80-004–020", "喻体之实"],
        ["**T0 本文实测**", "**8,207 字／长行 4,785＋颂 3,388**", "§7.1 `_e17_stats.py`", "计数（本文自测）"],
        ["**T0 本文实测**", "27 单元・121 颂・净句段 484（均 7.0 言）", "§7.1／§7.5.3", "计数（本文自测）"],
        ["**T1 澄观《疏》**", "「此十一喻，後後過於前前，故皆捨置前前更舉後後，巧顯深勝」", "`T1735` 本品段", "十一喻之科判"],
        ["**T1 澄观《疏》**", "「一一喻中皆有十重」", "同上", "四句十重之据"],
        ["**T2 六十**", "〈發心菩薩功德品第十三〉", "`T09n0278`", "品次对照"],
    ],
    "shu_note": "> **〔读法〕** 本品之数有两层：**体量之数**（8,207・4,785・3,388・121）与**校量之数**（阿僧祇・那由他・不可说不可说）。**两层不可混**：前者是本文实测，后者是经文所设之喻限。若以喻限当实测，则疑经；若以实测当喻限，则失旨。",
}

# ----------------------------------------------------------------------------
# 第十八部　明法品
# ----------------------------------------------------------------------------
P18 = {
    "tag": "P18",
    "path": os.path.join(DIR3, "华严经细读_第十八部_明法品.md"),
    "hui": "第三会（忉利天宫·说十住）",
    "dingwei": "本品为第三会**收束之品**，以「十问十答」为骨：问有十句，答即十段，段段以十法应之。读法当**以问为纲、以组为目**——问定其纲，组尽其目。",
    "yiju": "**於佛教中云何修習**——一问十句，答以十段十法；第三会之终，即十行之始。",
    "sanwen": "① 十问何以恰为十句，其自利利他之配当如何？② 「十法矩阵」与前十住之「双十」有何不同？③ 本品为第三会收束，何以不结会而启下？",
    "tiyao": "本品为第三会**收束品**：品界 **CJK 5,529**——长行 **4,921** ＋ 重颂 **588**（两段 lg：问端 **308**・答末 **280**・七言）。**三十二单元**＝1 head＋28 p＋2 lg＋1 byline。结构依澄观三分：**请说分**（精进慧两番问＋问端颂）→**正说分**（赞问许说＋答前十问十段＋十度＋绍三宝＋十庄严＋行成德用＋自在力）→**结说分**（如来欢喜・大众奉行）。",
    "xufa": "先观图 〇-1 得十问十答之配，次观图 〇-2 得本品与第十七品之「数语反衬」，次读〇之二.3 之坐标，然后入 §二逐段。**问既定，则十五组皆有着落。**",
    "en_map": "The closing chapter of the third assembly: 5,529 characters, ten questions asked in a single sentence and answered in ten sections of ten items each, then ten perfections, the continuation of the three jewels, ten adornments, and a double block of verse (308 + 280 characters). Its signature is a matrix, not a measure: where the previous chapter said \\\"unmeasurable\\\" twenty-one times, this one says it once. Fig. 0-1 pairs the ten questions with their answers; Fig. 0-2 sets the two chapters' vocabularies against each other.",
    "figs": [
        {
            "n": 1,
            "title": "十问十答·十法矩阵配组图",
            "what": "问如何成答",
            "one": "一问十句 → 十段十法；澄观「答前十問，即為十段」",
            "svg": """<svg viewBox="0 0 1000 580" width="100%" style="max-width:1000px;height:auto" xmlns="http://www.w3.org/2000/svg" font-family="serif">
<text x="500" y="24" text-anchor="middle" font-size="14.5" font-weight="bold" fill="#7a5a28">十问十答：一问十句，答即十段</text>
<text x="500" y="44" text-anchor="middle" font-size="12" fill="#8a7a5e">左列为经文原句（§2.1·照 `T10n0279` 卷十八逐字）；右列为答段单元（§7.5.2）</text>

<g font-size="11" fill="#8a7a5e">
<text x="30" y="72">问（一問十句·80-003）</text><text x="470" y="72">答（十段·80-009–019）</text>
</g>
<line x1="30" y1="78" x2="970" y2="78" stroke="#c9b98f"/>

<g font-size="11.5" fill="#5a5147">
<text x="30" y="102">① 令諸如來皆生歡喜</text><text x="470" y="102">十不放逸（80-009）· 十令佛喜（80-011/012）</text>
<text x="30" y="130">② 入諸菩薩所住之處</text><text x="470" y="130">十種清淨（80-010）</text>
<text x="30" y="158">③ 一切大行皆得清淨</text><text x="470" y="158">十速入諸地（80-013）· 住地十觀察（80-014）</text>
<text x="30" y="186">④ 所有大願悉使滿足</text><text x="470" y="186">十行清淨（80-015）· 十增勝法（80-016）</text>
<text x="30" y="214">⑤ 獲諸菩薩廣大之藏</text><text x="470" y="214">十清淨願（80-017）· 十法滿願（80-018）</text>
<text x="30" y="242">⑥ 隨所應化常為說法</text><text x="470" y="242">十無盡藏（80-019）· 隨宜說法（80-020）</text>
<text x="30" y="270">⑦ 而恒不捨波羅蜜行</text><text x="470" y="270">十波羅蜜（80-021–022·CJK 695 最长段）</text>
<text x="30" y="298">⑧ 所念眾生咸令得度</text><text x="470" y="298">紹三寶種（80-023）· 教發心／開法藏／善持教法</text>
<text x="30" y="326">⑨ 紹三寶種使不斷絕</text><text x="470" y="326">十莊嚴（80-024）· 身語心佛剎光明眾會神通…</text>
<text x="30" y="354">⑩ 善根方便皆悉不虛</text><text x="470" y="354">莊嚴不空（80-024 末）· 行成德用・自在力</text>
</g>

<line x1="30" y1="372" x2="970" y2="372" stroke="#d3c7ae"/>
<text x="30" y="396" font-size="11.5" fill="#7a5a28">〔本文判断〕十问之配当：**前五「自利兼他」（顺佛喜・顺法入位・顺行・顺愿・顺德成藏），后四「利他兼自」（说法・度生・弘三宝），末一「总结二利不虚」**——此澄观「十句為三」之科。</text>
<text x="30" y="420" font-size="11.5" fill="#8a7a5e">※ 「云何修習」一语总贯十句（澄观：「其修習言亦總亦別」）——**故十问非十事，是一事之十面**。</text>

<rect x="30" y="440" width="940" height="60" rx="4" fill="#f7ecd2" stroke="#b8863c"/>
<text x="46" y="462" font-size="11.5" font-weight="bold" fill="#7a5a28">数科口径之辨：澄观「答前十問，即為十段」，初段五十句（前二十答修習・後三十答令佛歡喜）；</text>
<text x="46" y="482" font-size="11.5" fill="#7a5a28">而本文 §7.5.2 按平文器单元细列十五组。**段以义分，组以单元分，二口径并存**〔本文判断·段界细则待核〕。</text>

<text x="30" y="524" font-size="11.5" fill="#8a7a5e">※ 十度一段（80-021）CJK 695，为全品最长段——**「不捨波羅蜜行」一句，答文最详**。</text>
<text x="30" y="548" font-size="11.5" fill="#8a7a5e">※ 双颂两段（问端 308・答末 280），一在问后、一在答末——**首尾各一颂，中为长行**，与第十七品之「一颂到底」判然。</text>
<text x="30" y="572" font-size="11.5" fill="#7a5a28">※ 澄观「前明十住自分行之勝德，今辨十住趣（十行）之行」——<tspan>本品之终即十行之始</tspan>，故第三会不结而结。</text>
</svg>""",
            "cap": "十问一氣而下，答即十段。**十问非十事，是一事之十面**——「云何修习」一语总贯十句（澄观：「其修習言亦總亦別」）。前五自利兼他，后四利他兼自，末一总结二利不虚。**数科有二口径**：澄观以义分十段，本文以单元细列十五组——**段以义分，组以单元分，并存不裁**〔本文判断〕。",
            "en": "Ten questions in one breath, ten sections in answer. They are not ten matters but ten faces of one: how to practise within the Buddha's teaching — the phrase governs all ten. Five are self-benefit with other-benefit, four the reverse, one closes both. Two reckonings coexist: Chengguan counts ten sections by meaning, this article fifteen groups by textual unit.",
            "dufa": [
                "**先读问，且只读问。** 十句问文是全品之纲；**答之十五组，不过逐句敷演**。问不明则答乱。",
                "**「云何修習」是一句而非十句。** 澄观明言「亦總亦別」——**总则贯十，别则十各一义**；此读本品之钥。",
                "**段与组之两口径，须分书。** 若强以十五组配十段，则生穿凿；**两存则各得其用**。",
            ],
        },
        {
            "n": 2,
            "title": "两品反衬：校量之海与十法之阵",
            "what": "数语如何反转",
            "one": "第十七品阿僧祇 21・无量 46；本品阿僧祇 1・十種 15",
            "svg": """<svg viewBox="0 0 1000 540" width="100%" style="max-width:1000px;height:auto" xmlns="http://www.w3.org/2000/svg" font-family="serif">
<text x="500" y="24" text-anchor="middle" font-size="14.5" font-weight="bold" fill="#7a5a28">一会之两极端：八千字的校量，与五千字的条目</text>
<text x="500" y="44" text-anchor="middle" font-size="12" fill="#8a7a5e">左：第十七品（CJK 8,207）；右：第十八品（CJK 5,529）——同会相邻，而语汇几乎不相犯</text>

<rect x="30" y="66" width="440" height="300" rx="5" fill="#f8f3ea" stroke="#d9cdb8"/>
<text x="46" y="90" font-size="12.5" font-weight="bold" fill="#7a5a28">第十七品 · 初发心功德</text>
<text x="46" y="110" font-size="10.5" fill="#8a7a5e">校量之海：以喻推极，终归「不可说」</text>
<g font-size="11" fill="#5a5147">
<text x="46" y="136">阿僧祇</text><rect x="180" y="124" width="210" height="15" fill="#d9c9a4" stroke="#c9b98f"/><text x="398" y="136" fill="#7a5a28">21</text>
<text x="46" y="164">無量</text><rect x="180" y="152" width="280" height="15" fill="#d9c9a4" stroke="#c9b98f"/><text x="468" y="164" fill="#7a5a28">46</text>
<text x="46" y="192">不可說不可說</text><rect x="180" y="180" width="40" height="15" fill="#e6dbc5" stroke="#c9b98f"/><text x="228" y="192">4</text>
<text x="46" y="220">那由他</text><rect x="180" y="208" width="80" height="15" fill="#e6dbc5" stroke="#c9b98f"/><text x="268" y="220">8</text>
<text x="46" y="248">初發心</text><rect x="180" y="236" width="110" height="15" fill="#e6dbc5" stroke="#c9b98f"/><text x="298" y="248">11</text>
</g>
<text x="46" y="282" font-size="11" fill="#8a7a5e">重颂 121 颂（3,388 字·41.3%）</text>
<text x="46" y="304" font-size="11" fill="#8a7a5e">篇幅 8,207　·　单元 27　·　最长品</text>
<text x="46" y="330" font-size="11" fill="#b8863c">→ 以「捨」尽，以「不可说」收</text>
<text x="46" y="352" font-size="10.5" fill="#8a7a5e">数在此品，是校量之器</text>

<rect x="530" y="66" width="440" height="300" rx="5" fill="#f3ecdf" stroke="#c9b98f"/>
<text x="546" y="90" font-size="12.5" font-weight="bold" fill="#7a5a28">第十八品 · 明法</text>
<text x="546" y="110" font-size="10.5" fill="#8a7a5e">十法之阵：以组尽其目，终归「奉行」</text>
<g font-size="11" fill="#5a5147">
<text x="546" y="136">十種</text><rect x="680" y="124" width="105" height="15" fill="#e6dbc5" stroke="#c9b98f"/><text x="793" y="136">15</text>
<text x="546" y="164">波羅蜜</text><rect x="680" y="152" width="161" height="15" fill="#e6dbc5" stroke="#c9b98f"/><text x="849" y="164">23</text>
<text x="546" y="192">莊嚴</text><rect x="680" y="180" width="182" height="15" fill="#e6dbc5" stroke="#c9b98f"/><text x="870" y="192">26</text>
<text x="546" y="220">無盡藏</text><rect x="680" y="208" width="84" height="15" fill="#e6dbc5" stroke="#c9b98f"/><text x="772" y="220">12</text>
<text x="546" y="248">阿僧祇</text><rect x="680" y="236" width="7" height="15" fill="#b8863c"/><text x="695" y="248" font-weight="bold" fill="#7a5a28">1</text>
</g>
<text x="546" y="282" font-size="11" fill="#8a7a5e">双颂 588（308＋280·10.6%）</text>
<text x="546" y="304" font-size="11" fill="#8a7a5e">篇幅 5,529　·　单元 32　·　收束品</text>
<text x="546" y="330" font-size="11" fill="#b8863c">→ 以「组」尽，以「奉行」收</text>
<text x="546" y="352" font-size="10.5" fill="#8a7a5e">数在此品，是条目之目</text>

<line x1="30" y1="386" x2="970" y2="386" stroke="#c9b98f"/>
<text x="30" y="412" font-size="12.5" font-weight="bold" fill="#7a5a28">反衬之最：阿僧祇 21 ↔ 1</text>
<text x="30" y="436" font-size="11.5" fill="#5a5147">同会相邻两品，一以「无数」为常用语，一几乎不用——**非作者忽变其辞，乃法门忽换其轴**：</text>
<text x="30" y="458" font-size="11.5" fill="#5a5147">十七品之轴是「量」（故数愈多愈见其不足）；十八品之轴是「目」（故数愈整愈见其全）。〔本文判断〕</text>

<text x="30" y="490" font-size="11.5" fill="#8a7a5e">※ 十八品之十法组，自十不放逸至十无尽藏，凡十一组，加随宜说法・十波罗蜜・绍三宝・十庄严四段，共十五组。</text>
<text x="30" y="512" font-size="11.5" fill="#8a7a5e">※ 十七品之十一喻，前喻必捨后喻；十八品之十五组，组组并立而不相捨——**一纵一横，正相对**。</text>
</svg>""",
            "cap": "同会相邻两品，语汇几乎不相犯：**第十七品「阿僧祇」21 见、「无量」46 见；第十八品「阿僧祇」仅 1 见**。非作者忽变其辞，乃法门忽换其轴——**十七品之轴是「量」，数愈多愈见其不足；十八品之轴是「目」，数愈整愈见其全**〔本文判断〕。十七喻必捨前，十五组并立而不相捨：一纵一横，正相对。",
            "en": "Two adjacent chapters in one assembly, almost no vocabulary in common: asaṃkhya twenty-one times against once. The author has not changed his diction; the dharma-gate has changed its axis — one measures, the other enumerates. The eleven similes each discard the last; the fifteen groups stand side by side and discard nothing. One runs vertically, one horizontally.",
            "dufa": [
                "**两品须合读，方见一会之全。** 只读十七品，则谓佛法唯在不可说；只读十八品，则谓佛法尽是条目。**合之则知：说不可说，正为立条目；立条目，正为显不可说**。",
                "**「阿僧祇 21↔1」是一处极小的文本证据，而所证极大。** 词频之变，常是法门转换最灵敏的指针。〔本文判断〕",
                "**双颂首尾各一，是收束之体。** 问后有颂（308），答末有颂（280）——**以颂包长行，与十七品之「一颂到底」异**。",
            ],
        },
    ],
    "weici_note": "本品为第三会**第六品、亦收束之品**。澄观判「**前明十住自分行之勝德，今辨十住趣（十行）之行**」——故本品虽结第三会，实启第四会之十行；**会终而不结，是华严「位位相即」之常法**。",
    "weici": [
        ["16 梵行", "卷17", "第三会·正说·行", "十法推徵，923 字", "行净"],
        ["17 初发心功德", "卷17–18", "第三会·胜进·德", "十一喻，8,207 字", "德显"],
        ["**18 明法（本品）**", "卷18", "第三会·**收束·法**", "十法矩阵，双颂", "第三会竟"],
        ["19 昇夜摩天宮", "卷19", "第四会·十行·发起", "不起而升（重演第十三品）", "四会即启"],
        ["20 夜摩天宮偈贊", "卷19", "第四会·十行·方便发起", "十菩萨各十颂（重演第十四品）", "一会之式，会会皆然"],
    ],
    "teshe_note": "本品之特色在**「以条目尽法」**：十问十答，十五组十法，凡一百五十余条，**几无一句校量之辞**。与第十七品之八千字校量恰成一会之两极——**在三十九品中，以如此密的条目矩阵收一会的，唯此一品**〔本文判断·据本文所核诸品〕。",
    "teshe": [
        ["以组为体", "十五组十法（自十不放逸至十庄严）", "第十七品十一喻（校量）", "一以目尽，一以量极"],
        ["数语反转", "阿僧祇 1（对十七品 21）", "第十七品无量 46", "同会之内，语汇几乎不相犯"],
        ["双颂包长行", "问端 308＋答末 280＝588（10.6%）", "第十七品 121 颂（41.3%）", "一以颂点缀，一以颂重述"],
        ["最长段", "十波罗蜜 80-021（CJK 695）", "第十七品以喻为段，无单段之最", "条目之品，详于一类"],
        ["收而不结", "末段「如來歡喜，大眾奉行」17 字", "第十六品以「不由他悟」收", "一以事收，一以理收"],
        ["单元最多", "32 单元（第三会最多）", "第十六品 5 单元（最少）", "同会之中，单元相去六倍"],
    ],
    "dufa5": [
        ["**问读**", "只读 80-003 十问之句", "初读本篇者", "得全品之纲"],
        ["**组读**", "只读十五组之名与首尾句（§7.5.2）", "欲见矩阵者", "得十法之目"],
        ["**一度读**", "只读十波罗蜜一段（80-021·695 字）", "欲见详处者", "见「不捨波罗蜜」之实"],
        ["**衬读**", "本品 ＋ 第十七品词频对看（图 〇-2）", "好文本肌理者", "见一会之两轴"],
        ["**承读**", "本品 §2.9 → 第十九品 §2.1", "欲见会际者", "见「收而不结」之法"],
    ],
    "shu": [
        ["**T0 经文明文**", "「彼諸菩薩於佛教中云何修習……善根方便皆悉不虛」", "`T10n0279` 卷十八·80-003", "十问之原文"],
        ["**T0 经文明文**", "「如來歡喜，大眾奉行」", "同上·80-030", "结说分（17 字）"],
        ["**T0 本文实测**", "**5,529 字／长行 4,921＋双颂 588**", "§7.1 `_e18_stats.py`", "计数（本文自测）"],
        ["**T0 本文实测**", "32 单元・十波罗蜜段 695（最长）", "§7.1／§7.5", "计数（本文自测）"],
        ["**T1 澄观《疏》**", "「答前十問。即為十段。今初段中有五十句」", "`T1735` 本品段", "十段之科"],
        ["**T1 澄观《疏》**", "「前明十住自分行之勝德，今辨十住趣（十行）之行」", "同上", "收束与开启之判"],
        ["**T2 六十**", "〈明法品第十四〉", "`T09n0278`", "品次对照"],
    ],
    "shu_note": "> **〔读法〕** 本品之数与第十七品恰相反：**十七品之数愈大愈显其不足，十八品之数愈整愈显其全**。故读十七品当问「何以犹不及」，读十八品当问「何以恰为十」。**同一「十」字，一为校量之起点，一为条目之定数**，不可混看。",
}

ALL = [P7, P8, P9, P10, P11, P12, P13, P14, P15, P16, P17, P18]

if __name__ == "__main__":
    want = set(sys.argv[1:])
    for d in ALL:
        if want and d["tag"] not in want:
            continue
        apply(d)
