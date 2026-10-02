#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""世主妙严品·卷一列名段结构抽取器（权威生成器）

把 `T10n0279` 卷一「列名段」解析为结构化会众数据，生成
`data/translation/miaoyan_assembly.yaml`。**YAML 由本脚本生成，勿手改。**

一、为何需要本脚本
    卷一的句式不是「列一名而曰上首」，而是**先列成员名号，而以其上首**：

        復有佛世界微塵數執金剛神，所謂：妙色那羅延執金剛神、日輪速疾幢執金剛神
        ……蓮華光摩尼髻執金剛神……。如是等而為上首，有佛世界微塵數，
        皆於往昔無量劫中恒發大願，願常親近供養諸佛；……一切如來所住之處，
        常勤守護。復有佛世界微塵數身眾神，所謂：……

    故「类」与「名」须分别计：异生三十九类通例各实列十名（上首一＋同类九），
    十一名之孤例四类（日天子、三十三天王、化乐天王、遍净天王），菩萨轨实列二十名，
    卷一共列名 414 名。**把「类数四十」当作「名数四十」，是本项目此前统计的基底性错误。**

二、段落的确定（不靠猜，全文计数互证）
    分段锚点为「如是等而為上首，」，卷一恰四十次，与解析所得四十类互证。
    记 40 个锚点位置为 pos[0..39]，切为 41 段：
        segs[0]            = 首个锚点之前            → 菩萨轨成员
        segs[k]  (1≤k≤39)  = 锚点 k-1 之后 ~ 锚点 k  → 「上类数词＋上类结句。」
                                                  「復有＋本类数词＋本类名，所謂：成员……。」
        segs[40]           = 末锚点之后              → 末类（大自在天王）之数词＋结句

三、两类易错处（本脚本已逐条对源订正，勿回退）
    1. **数词混入结句**：数词有「復有佛世界微塵數」「其數無量」「不可思議數」
       「不思議數」「有無量數」「不可稱數」「有十佛世界微塵數」等十余种。
       早期版本以固定数词表剥离，遇未登记者即把数词留在结句开头
       （主林神、主河神、迦楼罗王、兜率陀天王四类曾如此），并致集总词漏检。
       **现改为不设数词表**：以「復有」与「所謂」两个结构性锚点定位，
       二者之间即该类的「数词＋类名」，`count_expr` 按原文逐字存留，类名取其余部分。
    2. **集总词不皆在句首**：如主药神作「性皆离垢，仁慈祐物」、主空神作「心皆离垢，广大明洁」，
       集总词「皆」在第二字。早期版本以「结句是否以集总词起首」判有无，致此二类及
       数词混入之四类共六类误记为无集总词。现改为**检索词在结句中的位置**，
       并记 `collective_pos`（起首／句中），以备属性矩阵之用。
       实测全四十类中**确无集总词者仅主水神、主方神二类**（与澄观系「十九类神十七类用总词」之说相合）。

四、语义纪律（写入 DDL 注释，勿混用）
    · `n_named` 是**经文明列之成员数**，≠ 该类众数（后者经文但作「微尘数／无量」，不确指）。
    · `vow` 逐块锚定，长誓愿不得跨类溢出（执金刚神 128 字，为四十类之最）。
    · `vow_kind` 区分「誓愿」（三十九类之集总誓语）与「成就」（菩萨轨之成就赞叹），
      二者语法不同，统计时不可合并。

用法：
    python scripts/miaoyan_assembly.py            # 生成 YAML
    python scripts/miaoyan_assembly.py --check    # 只校验既有 YAML 与本脚本解析一致（回归用）
"""
import argparse
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CBETA = ROOT / "data" / "references" / "cbeta" / "T10n0279.xml"
OUT = ROOT / "data" / "translation" / "miaoyan_assembly.yaml"

ARTICLE = "shizhu-miaoyan"
MARK = "如是等而為上首，"          # 分段锚点，卷一恰四十次
ZHI = "所謂"                     # 类内成员之引入语；其后为「：」或「；」（异文，见 punct_variant）
DOTS = "……"                     # 卷一每类成员列举之省略记号

# 集总词，按长者在前（同一位置取最长者）
COLLECTIVES = ["莫不皆得", "莫不皆以", "莫不勤力", "莫不皆", "莫不", "悉已", "悉以",
               "咸皆", "皆", "俱", "咸", "並", "并", "悉"]

# 组别 → (组别中文, 所主)
GROUP_META = {
    "bodhisattva": ("同生众·菩萨", "智正觉世间主"),
    "deities":     ("异生众·十九类神", "器世间主"),
    "eight":       ("异生众·八部四王", "众生世间主"),
    "desire":      ("异生众·欲界天七众", "天众"),
    "form":        ("异生众·色界天五众", "天众"),
}

# 十九类神之所主（八部、天众不「主」器世间，故无此项）
DOMAIN = {
    "執金剛神": "总持护法", "身眾神": "如来全身", "足行神": "亲近随逐", "道場神": "道场庄严",
    "主城神": "城郭宫殿", "主地神": "大地", "主山神": "山岳", "主林神": "林树",
    "主藥神": "药草", "主稼神": "稼穑", "主河神": "河渠", "主海神": "大海",
    "主水神": "水泉", "主火神": "火", "主風神": "风", "主空神": "虚空",
    "主方神": "四方", "主夜神": "夜", "主晝神": "昼",
}

# CBETA 异文与字形异文：据实登记，不擅改经文。
# 「所謂」引入语之三种写法，卷一列名段实测：36 作「所謂：」、1 作「所謂；」（足行神）、
# 2 作「所謂」无标点（月天子、日天子），合计 39，与三十九类之数合。
# 注：「所謂；」全经 8 见（卷一 1、卷四十七 1、卷五十七 6），惟卷一足行神一处系会众
# 列名之引入语；余七处皆「何等為十？所謂；……」之列举引导语，非此段异文。
VARIANTS = {
    "足行神": {"punct_variant": "所謂；"},
    "月天子": {"punct_variant": "所謂"},
    "日天子": {"punct_variant": "所謂"},
    "主山神": {"glyph_variant": "首名「寶峯開華主山神」之「峯」为异体（他处作「峰」）",
               "punct_variant": "「所謂：寶峯開華主山神，華林妙髻主山神」之首二名用「，」分隔"
                                "（卷一唯此一处；余三十九类之首二名均用「、」）"},
}

# 组别归属（依卷一次第，非由字面推断）
GROUP_ORDER = (["bodhisattva"] + ["deities"] * 19 + ["eight"] * 8
               + ["desire"] * 7 + ["form"] * 5)

# 卷一列名之四十类（依 CBETA 字形与卷一次第，已逐条对源核）。
# 此表为**受控词表**：解析时用以切分数词与类名，并以断言校验解析所得与之全等——
# 若底本有异文或次第有变，脚本即报错中止，而非默默产出「看起来对」的数据。
CLASS_NAMES = [
    "菩薩摩訶薩", "執金剛神", "身眾神", "足行神", "道場神", "主城神", "主地神", "主山神",
    "主林神", "主藥神", "主稼神", "主河神", "主海神", "主水神", "主火神", "主風神",
    "主空神", "主方神", "主夜神", "主晝神",
    "阿脩羅王", "迦樓羅王", "緊那羅王", "摩睺羅伽王", "夜叉王", "諸大龍王", "鳩槃荼王",
    "乾闥婆王",
    "月天子", "日天子", "三十三天王", "須夜摩天王", "兜率陀天王", "化樂天王", "他化自在天王",
    "大梵天王", "光音天王", "遍淨天王", "廣果天王", "大自在天王",
]


def plain_text(path=CBETA):
    """取 CBETA 正文纯文本（去标签、去空白）。"""
    raw = Path(path).read_text(encoding="utf-8")
    return re.sub(r"\s+", "", re.sub(r"<[^>]+>", "", raw))


def vol1(txt=None):
    """取卷一（至卷二卷题之前）。"""
    txt = txt if txt is not None else plain_text()
    starts = [m.start() for m in re.finditer(r"大方廣佛華嚴經卷第[一二三四五]", txt)]
    if len(starts) < 5:
        raise SystemExit("卷次锚点不足，无法定位卷一")
    return txt[:starts[1]]


def split_count_vow(chunk):
    """<数词><界标><结句> → (数词, 结句)。界标取最先出现之「，。、」。"""
    best = min((chunk.find(d) for d in "，。、" if chunk.find(d) >= 0), default=-1)
    if best < 0:
        return "", chunk
    return chunk[:best], chunk[best + 1:]


def find_collective(vow):
    """检索集总词 → (词, 位置)；无则 (None, None)。取最靠前者，同位置取最长者。"""
    hit = None
    for tok in COLLECTIVES:
        i = vow.find(tok)
        if i >= 0 and (hit is None or i < hit[0] or (i == hit[0] and len(tok) > len(hit[1]))):
            hit = (i, tok)
    if hit is None:
        return None, None
    return hit[1], ("起首" if hit[0] == 0 else "句中")


def parse(txt=None):
    """解析卷一列名段 → 40 类之 dict 列表。"""
    v1 = vol1(txt)
    seg_start = v1.find("普賢菩薩摩訶薩")
    if seg_start < 0:
        raise SystemExit("未找到卷一列名段起点")
    s = v1[seg_start:]

    pos = [m.start() for m in re.finditer(re.escape(MARK), s)]
    if len(pos) != 40:
        raise SystemExit(f"「{MARK}」实测 {len(pos)} 次，与四十类之数不合，抽取中止")

    segs = [s[:pos[0]]]
    for k in range(1, 40):
        segs.append(s[pos[k - 1] + len(MARK):pos[k]])
    segs.append(s[pos[40 - 1] + len(MARK):])

    classes = []
    specs = []          # (类名, 数词, 成员列表)

    def add(cat, count_expr, members, vow):
        members = ([x for x in members if x.strip()] if isinstance(members, list)
                   else [x for x in re.split(r"[、，]", members or "") if x.strip()])
        coll, coll_pos = find_collective(vow)
        g = GROUP_ORDER[len(classes)]
        gzh, realm = GROUP_META[g]
        c = {
            "idx": len(classes),
            "cat": cat,
            "group": g,
            "group_zh": gzh,
            "realm": realm,
            "count_expr": count_expr,
            "leader": members[0] if members else None,
            "n_named": len(members),
        }
        if cat in DOMAIN:
            c["domain"] = DOMAIN[cat]
        if coll:
            c["collective"] = coll
            c["collective_pos"] = coll_pos
        c["vow_kind"] = "誓愿" if len(classes) else "成就"
        c["vow"] = vow
        c["members"] = members
        c.update(VARIANTS.get(cat, {}))
        classes.append(c)

    def strip_dots(m):
        for suf in ("。" + DOTS + "。", "。" + DOTS, DOTS + "。", DOTS):
            if m.endswith(suf):
                return m[: -len(suf)]
        return m

    # ── 先取各类之「数词＋类名＋成员」 ──
    # 类 0：成员在首锚点之前；其数词在 segs[1] 前段（经文于首类用「有X」，非「復有X」）。
    f1 = segs[1].find("復有")
    cnt0, _ = split_count_vow(segs[1][:f1].rstrip("。"))
    specs.append((CLASS_NAMES[0], cnt0, [x for x in segs[0].rstrip("。").split("、") if x]))

    # 类 1..39：在 segs[c] 的「復有」之后
    for c in range(1, 40):
        seg = segs[c]
        f = seg.find("復有")
        if f < 0:
            raise SystemExit(f"第 {c} 类未找到「復有」，抽取中止")
        hdr = seg[f + 2:]
        z = hdr.find("，" + ZHI)
        if z < 0:
            raise SystemExit(f"第 {c} 类未找到「，{ZHI}」，抽取中止")
        prefix = hdr[:z]                          # = <數詞><類名>
        members = strip_dots(hdr[z + 1 + len(ZHI) + 1:])   # 跳過「，所謂：」或「，所謂；」
        want = CLASS_NAMES[c]
        if not prefix.endswith(want):
            raise SystemExit(
                f"第 {c} 类名不合：底本作「{prefix}」，受控词表作「{want}」。"
                "若系底本异文或次第有变，请核源后更新 CLASS_NAMES 与 GROUP_ORDER。")
        # 数词＝「復有」＋前缀中类名之前的部分，按原文逐字存留，不设数词表
        specs.append((want, "復有" + prefix[: len(prefix) - len(want)],
                      [x for x in re.split(r"[、，]", members) if x]))

    # ── 再取四十条结句。注意：类 c 之结句在 segs[c+1] 的前段（不在 segs[c]）——
    #    segs[c] 的前段装的是**上一类**（c-1）的结句。此处极易差一位，故显式注明。
    vows = []
    for c in range(0, 39):
        nxt = segs[c + 1]
        f = nxt.find("復有")
        if f < 0:
            raise SystemExit(f"取第 {c} 类结句时，segs[{c + 1}] 未找到「復有」，抽取中止")
        _, vow = split_count_vow(nxt[:f].rstrip("。"))
        vows.append(vow)
    vows.append(split_count_vow(segs[40].rstrip("。"))[1])

    for (cat, count_expr, members), vow in zip(specs, vows):
        add(cat, count_expr, members, vow)
    return classes

    # 末类（大自在天王）之结句已在 vows 中处理（segs[40]）
    return classes


def build():
    classes = parse()
    return {
        "article": ARTICLE,
        "source": "T10n0279 卷一（列名段）",
        "source_note": ("「而為上首」卷一恰四十次，与四十类之数互证。"
                        "各类先列成员名号而以其上首：异生三十九类通例各实列十名，"
                        "日天子、三十三天王、化樂天王、遍淨天王各实列十一，菩萨轨实列二十，"
                        "卷一实列名共 414 名。与袖珍版编者按 20/190/80/71/51=412 之关系："
                        "四项全合，惟欲界天编者按 71、本表实测 73，差二〔存疑待考〕。"),
        "metrics": {
            "classes": len(classes),
            "named_total": sum(c["n_named"] for c in classes),
            "per_class_nominal": 10,
            "classes_of_11": [c["cat"] for c in classes if c["n_named"] == 11],
            "no_collective": [c["cat"] for c in classes if not c.get("collective")],
        },
        "classes": classes,
    }


# ---------------------------------------------------------------- 回归校验
def check(data, verbose=True):
    """断言式校验。任一不过即抛错——此为数据可信度之闸门。"""
    cs = data["classes"]
    errs = []

    def want(cond, msg):
        if not cond:
            errs.append(msg)

    want(len(cs) == 40, f"类数 {len(cs)} ≠ 40")
    want([c["cat"] for c in cs] == CLASS_NAMES,
         "解析所得之类名/次第与受控词表 CLASS_NAMES 不全等")
    want(data["metrics"]["named_total"] == 414,
         f"实列名总数 {data['metrics']['named_total']} ≠ 414")
    want(sum(c["n_named"] for c in cs) == 414, "各类 n_named 之和不等于 414")
    for c in cs:
        want(len(c["members"]) == c["n_named"],
             f"{c['cat']}：成员 {len(c['members'])} 与 n_named {c['n_named']} 不符")
        want(bool(c.get("vow")), f"{c['cat']}：结句为空")
        want(bool(c.get("leader")) and c["leader"] == (c["members"][0] if c["members"] else None),
             f"{c['cat']}：上首与首名不符")
        # 数词不得混入结句
        want(not re.match(r"^(其數|不可思議數|不思議數|有無量數|不可稱數|有?佛世界微塵數|有十佛世界微塵數|無量數|其數無量)",
                          c.get("vow") or ""),
             f"{c['cat']}：结句开头混入数词 —— 「{c.get('vow', '')[:12]}」")
        want(c.get("group") in GROUP_META, f"{c['cat']}：group 非法")

    eleven = [c["cat"] for c in cs if c["n_named"] == 11]
    want(eleven == ["日天子", "三十三天王", "化樂天王", "遍淨天王"],
         f"十一名之四类为 {eleven}，与实测不合")
    # 月天子与光音天王皆十名（旧稿误记为十一之孤例）
    for cat in ("月天子", "光音天王"):
        got = next((c["n_named"] for c in cs if c["cat"] == cat), None)
        want(got == 10, f"{cat} 实列 {got} 名，应为 10")
    # 执金刚神长誓愿不得被截断
    zh = next(c for c in cs if c["cat"] == "執金剛神")
    want(len(zh["vow"]) == 128, f"執金剛神结句 {len(zh['vow'])} 字，应为 128（勿截断）")
    want(zh["vow"].startswith("皆於往昔無量劫中恒發大願"), "執金剛神结句起首失准")
    # 确无集总词者仅主水神、主方神
    want(data["metrics"]["no_collective"] == ["主水神", "主方神"],
         f"无集总词者为 {data['metrics']['no_collective']}，应为 [主水神, 主方神]")
    # 句中之集总词（早期以「起首」判有无，致此二类误记）
    mid = [c["cat"] for c in cs if c.get("collective_pos") == "句中"]
    want("主藥神" in mid and "主空神" in mid,
         f"句中集总词未识别：{mid}")
    # 菩萨轨：结句为「成就」而非「誓愿」，且冠「普」者十一位
    want(cs[0]["vow_kind"] == "成就" and all(c["vow_kind"] == "誓愿" for c in cs[1:]),
         "vow_kind 分配有误")
    # 冠「普」之菩萨十一位，且「首十连缀」——普智雲日幢列第十六位
    pu = [m for m in cs[0]["members"] if m.startswith("普")]
    want(len(pu) == 11, f"冠「普」之菩萨 {len(pu)} 位，应为 11")
    want(pu[10] == "普智雲日幢菩薩摩訶薩", "第十一位冠普者非普智雲日幢（首十连缀之说）")
    # 主山神首二名用「，」分隔（卷一唯此一处）——若漏此规则，该类会由 10 名误作 9 名
    ms = next(c for c in cs if c["cat"] == "主山神")
    want(ms["n_named"] == 10, f"主山神实列 {ms['n_named']} 名，应为 10（「，」分隔首二名）")
    want(ms["members"][0] == "寶峯開華主山神" and ms["members"][1] == "華林妙髻主山神",
         "主山神首二名失准")

    if verbose:
        print("  类数 %d｜实列名 %d｜十一名 %d 类｜冠普菩萨 %d 位"
              % (len(cs), data["metrics"]["named_total"], len(eleven), len(pu)))
        print("  无集总词：%s｜句中集总词：%s"
              % ("、".join(data["metrics"]["no_collective"]), "、".join(mid)))
        print("  执金刚神结句 %d 字（四十类之最）" % len(zh["vow"]))
    if errs:
        print("\n!! 校验不过：")
        for e in errs:
            print("   -", e)
        raise SystemExit(1)
    return True


def dump(data):
    head = ("# 世主妙严品·卷一列名段会众结构（自动生成，勿手改）\n"
            "# 生成器 scripts/miaoyan_assembly.py ｜ 源 CBETA T10n0279 卷一\n"
            "# 校验 python scripts/miaoyan_assembly.py --check\n"
            "#\n"
            "# 【语义】n_named = 经文明列之成员数，≠ 该类众数（后者经文但作「微塵數／無量」）。\n"
            "# 【语义】vow 逐块锚定；vow_kind 分「誓愿」（三十九类）与「成就」（菩萨轨）。\n"
            "# 【语义】collective_pos 分「起首」／「句中」——主藥神、主空神之集总词在第二字。\n")
    body = yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=10 ** 6,
                          default_flow_style=False)
    return head + body


def main():
    ap = argparse.ArgumentParser(description="世主妙严品·卷一列名段抽取器")
    ap.add_argument("--check", action="store_true",
                    help="只校验既有 YAML 与本脚本解析结果一致（回归用），不写文件")
    a = ap.parse_args()

    data = build()
    print("[parse] T10n0279 卷一列名段：%d 类" % len(data["classes"]))
    check(data)

    if a.check:
        if not OUT.exists():
            raise SystemExit("!! %s 不存在，无法比对" % OUT)
        old = yaml.safe_load(OUT.read_text(encoding="utf-8"))
        if old == data:
            print("[check] 既有 YAML 与本脚本解析结果一致 ✅")
        else:
            diff = [k for k in set(old) | set(data) if old.get(k) != data.get(k)]
            print("!! [check] 既有 YAML 与本脚本解析结果不一致，顶层差异：%s" % diff)
            for i, (o, n) in enumerate(zip(old.get("classes", []), data["classes"])):
                if o != n:
                    ks = [k for k in set(o) | set(n) if o.get(k) != n.get(k)]
                    print("   类 %d (%s)：差异字段 %s" % (i, n.get("cat"), ks))
                    for k in ks:
                        print("      旧 %r" % (o.get(k),))
                        print("      新 %r" % (n.get(k),))
            raise SystemExit(1)
        return

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(dump(data), encoding="utf-8")
    print("[write] %s（%d 字节）" % (OUT, len(OUT.read_text(encoding="utf-8"))))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
