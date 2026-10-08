# -*- coding: utf-8 -*-
"""
ru_lai_studies.py — 《如来现相品》数据科学层驱动（四视角）

三层分源：经文事实（data/translation/ru_lai_assembly.yaml，逐字回源 T10n0279 卷六）
          → 本条驱动（析构·度量，算子见 scripts/data_science.py）
          → data/translation/ru_lai_studies.yaml（呈现层所消费）。

视角：
  L1 语言统计：字频／Zipf／Shannon 熵／TF-IDF／「海」族词。
  L2 代数·组合：八方之 D8 群作用（Burnside 定轨数）、十方之对径胚五对、四十问「海」二分。
  L3 拓扑：十方名相共字图之 β0、β1（旗复形）与阈值过滤。
  L4 几何·持久同调：同名相复形之各维持久条形（完整枚举，nv=10）。

约束：零新增依赖；数字自卷六实测或自 assembly 明列数据算出；凡不可考者不臆造。
      L2 之群作用为对方位几何之对称性分析，非经文所言。
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import miaoyan_metrics as mm  # noqa: E402
import data_science as ds  # noqa: E402
import yaml  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
ASM = ROOT / "data" / "translation" / "ru_lai_assembly.yaml"
OUT = ROOT / "data" / "translation" / "ru_lai_studies.yaml"

DIR_ZH = {"E": "東", "SE": "東南", "S": "南", "SW": "西南", "W": "西",
          "NW": "西北", "N": "北", "NE": "東北", "U": "上", "D": "下"}
KEY_TERMS = ["海", "光", "如來", "佛", "智", "蓮華", "莊嚴", "世界", "眾生",
             "菩薩", "雲", "三昧", "解脫", "光明", "微塵", "佛剎", "供養", "十方", "法界"]


# ───────── L1 语言统计（偈组切分 + 引擎） ─────────
def verse_groups(vol6, asm):
    anchors = []
    for v in asm["verses"]["leading"]:
        anchors.append((str(v["id"]), v["incipit_zh"]))
    for v in asm["verses"]["main"]:
        anchors.append((str(v["id"]), v["incipit_zh"]))
    pos = []
    for gid, inc in anchors:
        i = vol6.find(inc)
        if i < 0:
            raise SystemExit("anchor not found: %s %s" % (gid, inc))
        pos.append((i, gid))
    pos.sort()
    out = []
    for idx, (i, gid) in enumerate(pos):
        j = pos[idx + 1][0] if idx + 1 < len(pos) else len(vol6)
        out.append((gid, vol6[i:j]))
    return out


# ───────── L2 代数·组合（ru-lai 专设） ─────────
def lens_algebra(asm):
    horiz_ids = ["E", "SE", "S", "SW", "W", "NW", "N", "NE"]
    qa = asm["questions"]["group_a"]["items_zh"]
    qb = asm["questions"]["group_b"]["items_zh"]
    group = []
    for m in range(8):
        group.append(("r%d" % m, [((k + m) % 8) for k in range(8)] + [8, 9]))
    for m in range(8):
        group.append(("s%d" % m, [((m - k) % 8) for k in range(8)] + [8, 9]))
    fixed_sum = sum(sum(1 for i in range(10) if perm[i] == i) for _, perm in group)
    orbits = fixed_sum / len(group)
    seen, orb_sets = set(), []
    for p in range(10):
        if p in seen:
            continue
        orb, stack = set(), [p]
        while stack:
            x = stack.pop()
            for _, perm in group:
                y = perm[x]
                if y not in orb:
                    orb.add(y)
                    stack.append(y)
        seen |= orb
        orb_sets.append(sorted(orb))
    pairing = [["E", "W"], ["N", "S"], ["NE", "SW"], ["NW", "SE"], ["U", "D"]]
    return {
        "octagon_symmetry": {
            "group": "D8（正八边形对称群）",
            "order": len(group),
            "generators": ["r（旋转 45°）", "s（反射）"],
            "burnside_fixed_sum": fixed_sum,
            "num_orbits": orbits,
            "orbits": orb_sets,
            "readout_zh": "八方为 1 个传递轨道（G·E ＝ 八方全体）；上、下各为不动点；合 3 轨道。",
            "readout_en": "The eight directions form a single transitive orbit; zenith and nadir are each fixed. Total: 3 orbits.",
            "note_zh": "此为对方位几何之对称性分析（数学视角），非经文所说；经文本无「群」之名。",
            "note_en": "A symmetry analysis of the eight directions (a mathematical lens); the sutra itself has no notion of a group.",
        },
        "antipodal": {
            "pairing": pairing,
            "pairs": len(pairing),
            "readout_zh": "十方＝五组对跖（对径）方向；对径映射为无不动点之对合，商得 5 元。",
            "readout_en": "The ten directions pair into five antipodal pairs; the antipodal involution is fixed-point-free, giving a 5-element quotient.",
        },
        "questions_partition": {
            "total": len(qa) + len(qb),
            "group_a": len(qa), "group_b": len(qb),
            "group_a_endswith_sea": sum(1 for t in qa if t.endswith("海")),
            "group_b_endswith_sea": sum(1 for t in qb if t.endswith("海")),
            "readout_zh": "以「海」作词尾之单一特征即完全分判甲、乙二组（甲 0/20，乙 20/20）。",
            "readout_en": "A single lexical feature (terminating in 海) perfectly separates Set A from Set B (A 0/20, B 20/20).",
        },
    }


# ───────── 节点集（十方） ─────────
def direction_nodes(asm):
    nodes = []
    for d in asm["directions"]:
        chars = "".join(d[k] for k in ("world_ocean_zh", "land_zh", "buddha_zh", "bodhisattva_zh"))
        nodes.append({"id": d["id"], "label_zh": DIR_ZH.get(d["id"], d["id"]),
                      "label_en": d.get("id", ""), "chars": chars})
    return nodes


TOPO = dict(
    rule_zh="两方之「世界海／国土／佛号／上首菩萨」四名相共字 ≥1 则连边；权＝共字数。",
    rule_en="Two directions are linked if their four names (ocean/land/buddha/leading bodhisattva) share ≥1 character; weight = shared count.",
    readout_zh=("阈值 t＝1 时十方名相两两皆有共字，图退化为完全图 K10 —— 名相用字高度互渗。"
                "故有意义之结构在**较高阈值之过滤**中显现（见 filtration）。"),
    readout_en=("At t=1 every pair of directions shares a character, so the graph is the complete "
                "graph K10. Structure appears only under higher-threshold filtration (see filtration)."),
)
METHOD_ZH = ("顶点＝十方；λ(σ)＝σ 诸边共字数之最小值（顶点最先出现）；复形 K_t＝{σ : λ(σ) ≥ t}，"
             "t 自 max 降至 1 而自空渐满（增过滤）。以 GF(2) 边界矩阵约化（standard reduction）"
             "得各维配对（birth, death）。与拓扑节之静态 Betti 数互补：静态只问某阈值下有几何环，"
             "持久则问环于何阈值生、何阈值灭。")
METHOD_EN = ("Vertices = ten directions; λ(σ) = min shared-character count over the edges of σ "
             "(vertices first); complex K_t = {σ : λ(σ) ≥ t}, with t from max down to 1 (an increasing "
             "filtration). GF(2) boundary-matrix reduction yields per-dimension (birth, death) pairs. "
             "This complements the static Betti numbers of the topology lens: there we ask how many "
             "cycles at a threshold, here when each cycle is born and dies.")

# ───────── 四视角「分析说明」卡（目的·方法·效果；中英必配）─────────
# 呈现层 web/demo/src/data_science.js 逐视角取用，渲染于该视角读数之前。
# 纪律：只述本数据层确已算出者（数字与本文件产出之 YAML 同源），
#       不引外部基准、不加未经回源之判断；L2 之群作用须标明为数学视角而非经文所说。
LENS_GUIDES = {
    "linguistic": {
        "purpose_zh": ("为本品用字立一份可复核的量化底账——多大篇幅、多少字头、用字集中到什么程度、"
                       "词频如何分布——作为其余三视角的对照背景（同一底本、同一切分）。"),
        "purpose_en": ("To establish a reproducible quantitative baseline for the chapter's wording — size, "
                       "character inventory, concentration and frequency profile — as the background against "
                       "which the other three lenses are read (same source text, same segmentation)."),
        "method_zh": ("只取 T10n0279 卷六之 CJK 表意字；计字次与字头，算型例比 TTR 与香农熵 "
                      "H＝−Σp·log₂p（上限 log₂ 字头数）；Zipf 斜率取秩 1–200 的 log–log 最小二乘；"
                      "TF-IDF 以偈组（前导三颂＋十一组十偈，共 14 组）为文档单位取各组特征词。"),
        "method_en": ("Only CJK characters of juan 6 (T10n0279) are counted. Tokens, types, the type-token "
                       "ratio and Shannon entropy H = −Σp·log₂p (upper bound = log₂ of types) are computed; "
                       "the Zipf slope is a log-log least-squares fit over ranks 1–200; TF-IDF treats each "
                       "verse group (three leading verses plus eleven ten-verse groups, 14 in all) as a "
                       "document."),
        "effect_zh": ("卷六 8,119 字、498 字头（TTR 0.0613），字熵 7.5454 bit，为其上限 8.96 bit 之 84%；"
                      "Zipf 斜率 −0.8517；字频前五为「一」259、「佛」228、「現」183、「切」174、「十」151。"
                      "与本系《世主妙嚴品》（31,953 字／837 字头／熵 7.9521 bit／Zipf −0.8003）对读："
                      "本品字头少、熵亦低，而两品 Zipf 斜率同在 −0.8 上下，词频结构可直接比较。"),
        "effect_en": ("Juan 6 runs to 8,119 characters with 498 types (TTR 0.0613); character entropy is "
                      "7.5454 bits against an upper bound of 8.96 bits (84%), and the Zipf slope is −0.8517. "
                      "The five most frequent characters are 一 (259), 佛 (228), 現 (183), 切 (174) and 十 (151). "
                      "Read against the same corpus family's Lords of the Assembly chapter (31,953 characters, "
                      "837 types, entropy 7.9521 bits, Zipf −0.8003): this chapter has fewer types and lower "
                      "entropy, while both Zipf slopes sit near −0.8, so their frequency structures are "
                      "directly comparable."),
    },
    "algebra": {
        "purpose_zh": ("问：本品十方方位之名相集合究竟有哪些可检验的对称与分划？把「八方—上下」「对跖」"
                       "「四十问两组」这些直观描述，化成可以计数的等价类与二分。"),
        "purpose_en": ("What verifiable symmetries and partitions does the set of ten directions actually admit? "
                       "Intuitive descriptions — eight around, two above/below, antipodal pairs, the two sets of "
                       "forty questions — are turned into countable equivalence classes and bipartitions."),
        "method_zh": ("以 D8（旋转 45° 与反射，阶 16）作用于八方，用 Burnside 引理（各群元不动点数之和 ÷ 群阶）"
                      "定轨道数并直接求轨道；再列十方之对径对合；四十问按「词尾是否为『海』」作二分并统计命中。"),
        "method_en": ("D8 (45° rotations and reflections, order 16) acts on the eight horizontal directions; "
                       "Burnside's lemma (sum of fixed points over the group, divided by the order) gives the "
                       "orbit count, and the orbits are then computed directly. The antipodal involution on the "
                       "ten directions is listed, and the forty questions are bipartitioned by whether they "
                       "terminate in 海, with hit counts per set."),
        "effect_zh": ("Burnside：不动点数和 48 ÷ 阶 16 ＝ 3 轨道——八方为一传递轨道，上、下各为不动点；"
                      "十方＝5 组对跖（东西·南北·东北西南·西北东南·上下）；四十问以「海」词尾之单一特征即完全分判"
                      "两组（甲 0/20、乙 20/20）。此为对方位几何之数学分析，经文本身无「群」之名。"),
        "effect_en": ("Burnside: 48 fixed points summed over 16 group elements gives 3 orbits — the eight "
                       "horizontal directions form one transitive orbit, while zenith and nadir are each fixed. "
                       "The ten directions fall into 5 antipodal pairs (E–W, N–S, NE–SW, NW–SE, up–down). "
                       "A single lexical feature, terminating in 海, separates the forty questions perfectly "
                       "(set A 0/20, set B 20/20). This is a mathematical analysis of directional geometry; "
                       "the sutra itself has no notion of a group."),
    },
    "topology": {
        "purpose_zh": ("把十方名相之间的「共字」关系化为一张加权图，问它在多强的取舍（阈值）下仍连成一片、"
                       "何时开始成环——名相关系由此有了可度量的门槛，而不只是罗列名相。"),
        "purpose_en": ("To recast the shared-character relations among the ten directions as a weighted graph "
                       "and ask how strong a threshold it survives while staying connected, and when cycles "
                       "appear — the names thereby acquire measurable thresholds instead of a mere list."),
        "method_zh": ("顶点＝十方；两方之四名相（世界海／国土／佛号／上首菩萨）共字 ≥1 连边，权＝共字数。"
                      "逐阈值取权 ≥ t 之边，算边数、连通分量数 β₀、以及圈秩经 GF(2) 边界约化后的 β₁ 与三角形数。"),
        "method_en": ("Vertices = the ten directions; two directions are joined when their four names "
                       "(world-ocean, land, buddha, leading bodhisattva) share at least one character; the "
                       "weight is the shared-character count. For each threshold t only edges of weight ≥ t "
                       "are kept, and edge count, connected components β₀, and — after GF(2) boundary "
                       "reduction — β₁ and the triangle count are recorded."),
        "effect_zh": ("t＝1 时 45 条边齐备（密度 1.0），图为完全图 K10，β₀＝1、β₁＝0——十方名相互渗至两两皆有共字，"
                      "故结构反而要到高阈值才显形：t＝13 时仅余西北—上一条边（共字 13），β₀ 升至 9。"
                      "亦即低阈值全连通是常态，分野出现在共字 10 以上的强关系里。"),
        "effect_en": ("At t = 1 all 45 edges are present (density 1.0): the graph is the complete graph K10 "
                      "with β₀ = 1 and β₁ = 0, meaning every pair of directions already shares a character. "
                      "Structure therefore appears only at higher thresholds — at t = 13 a single edge remains "
                      "(northwest–up, 13 shared characters) and β₀ rises to 9. Connectivity at low thresholds "
                      "is the norm; the real divisions sit in the strong relations of ten or more shared "
                      "characters."),
    },
    "geometry": {
        "purpose_zh": ("追踪阈值过滤过程中各维洞（分量／环／腔）的生灭，分辨哪些结构只是某个阈值上的暂时现象、"
                       "哪些从头贯穿到尾；谱几何则从另一面问同一张图的整体连通度与内禀二分方向。"),
        "purpose_en": ("To track the birth and death of holes in each dimension across the filtration, telling "
                       "which structures are transient features of a threshold and which persist end to end; "
                       "spectral geometry answers from another side — overall connectivity and the intrinsic "
                       "direction of bisection."),
        "method_zh": ("λ(σ)＝σ 各边共字数之最小值，K_t＝{σ : λ(σ) ≥ t}，t 自 max 降至 1（增过滤）；以 GF(2) "
                      "边界矩阵约化得各维 (birth, death) 条形，并以 Euler–Poincaré χ＝Σ(−1)ⁱβᵢ 与终复形之"
                      "直接同调交叉校验。nv＝10 ≤ 11，2¹⁰−1＝1023 个单纯形全枚举（max_dim 9，未限维）。"
                      "谱部取加权 Laplacian L＝D−W 之全谱：λ₂ 为代数连通度，Fiedler 向量给二分方向，"
                      "归一化 λ₂ 配 Cheeger 不等式量该二分之边界。"),
        "method_en": ("λ(σ) is the minimum shared-character count over the edges of σ, K_t = {σ : λ(σ) ≥ t}, "
                       "with t from max down to 1 (an increasing filtration). GF(2) boundary-matrix reduction "
                       "yields per-dimension (birth, death) bars, cross-checked against a direct homology "
                       "computation of the final complex via the Euler–Poincaré identity χ = Σ(−1)ⁱβᵢ. With "
                       "nv = 10 ≤ 11 all 2¹⁰ − 1 = 1,023 simplices are enumerated (max_dim 9, uncapped). The "
                       "spectral part takes the full spectrum of the weighted Laplacian L = D − W: λ₂ is the "
                       "algebraic connectivity, the Fiedler vector gives the bisection direction, and the "
                       "normalized λ₂ with Cheeger's inequality measures that cut's boundary."),
        "effect_zh": ("t 自 13 降至 1：β₀ 由 9 合至 1（终复形连通），β₁ 全程为 0；本质类仅 H0 一条，"
                      "H1／H2／H3 皆 0——高维之洞都随阈值升高被填掉，不留下贯穿全程的环与腔。"
                      "谱部：Σλ＝612＝2m，λ₂＝40.62、归一化 λ₂＝0.923，Cheeger 值 0.531（割 5，"
                      "λ₂/2 ≤ h ≤ √(2λ₂) 成立）；Fiedler 二分为北·西南·下（3 名相）／"
                      "东·南·西·东北·东南·西北·上（7 名相）。"),
        "effect_en": ("As t falls from 13 to 1, β₀ contracts from 9 to 1 (the final complex is connected) and "
                      "β₁ stays 0 throughout; only one essential class remains, in H0 — H1, H2 and H3 are all "
                      "0, so holes in higher dimensions are filled in as the threshold rises and no cycle or "
                      "cavity survives the whole filtration. Spectrally: Σλ = 612 = 2m, λ₂ = 40.62, normalized "
                      "λ₂ = 0.923, Cheeger value 0.531 (cut of 5, with λ₂/2 ≤ h ≤ √(2λ₂) satisfied). The "
                      "Fiedler bisection puts north, southwest and down (3 names) against east, south, west, "
                      "northeast, southeast, northwest and up (7 names)."),
    },
}



if __name__ == "__main__":
    vol6 = mm.load()[6]
    asm = yaml.safe_load(ASM.read_text(encoding="utf-8"))
    miss = []
    for d in asm["directions"]:
        for k in ("world_ocean_zh", "land_zh", "buddha_zh", "bodhisattva_zh"):
            if d[k] not in vol6:
                miss.append((d["id"], k, d[k]))
    for v in asm["verses"]["main"]:
        if v["speaker_zh"] not in vol6:
            miss.append(("speaker", v["speaker_zh"]))
    if miss:
        raise SystemExit("assembly 回源断言失败（须逐字见于卷六）：%s" % miss)

    nodes = direction_nodes(asm)
    nv, w, maxt = ds._weights(nodes)
    ids = [nd["id"] for nd in nodes]

    data = {
        "meta": {
            "id": "ru-lai-studies",
            "article": "ru-lai-xian-xiang",
            "title_zh": "《如来现相品》数据科学层",
            "title_en": "The Tathāgata's Manifestation · Data-Science Layer",
            "source_primary": "CBETA T10n0279《大方廣佛華嚴經》卷第六·如來現相品第二",
            "generated_by": "scripts/ru_lai_studies.py",
            "sources": [{"label": "CBETA T10n0279", "url": "https://cbetaonline.dila.edu.tw/zh/T10n0279"}],
            "note_zh": ("体例：本层为数据科学层产物，非经文陈述。名相与数目出 assembly 层；字频／熵／"
                        "Zipf／TF-IDF／群作用／图论诸项皆本站析构。四视角（语言统计·代数组合·拓扑·几何持久同调）"
                        "为观察同一经文之四种窗口。"),
            "note_en": ("This is an analytical (data-science) layer, not a sutra statement. Names and counts come "
                        "from the assembly layer; all statistics are computed here. The four lenses are four windows "
                        "onto one text."),
        },
        "lens_guides": LENS_GUIDES,
        "linguistic": ds.lens_linguistic(
            vol6, KEY_TERMS, doc_groups=verse_groups(vol6, asm), sea_char="海",
            note_zh="字熵以卷六经文（CJK 表意字）计；ZIPF 斜率取秩 1–200 之 log–log 最小二乘。",
            note_en="Character entropy over the CJK characters of juan 6; Zipf slope is the log-log least-squares fit over ranks 1–200."),
        "algebra": lens_algebra(asm),
        "topology": ds.lens_topology(
            nv, w, ids=ids, labels={nd["id"]: nd["label_zh"] for nd in nodes},
            rule_zh="两方之「世界海／国土／佛号／上首菩萨」四名相共字 ≥1 则连边；权＝共字数。",
            rule_en="Two directions are linked if their four names (ocean/land/buddha/leading bodhisattva) share ≥1 character; weight = shared count.",
            readout_zh=("阈值 t＝1 时十方名相两两皆有共字，图退化为完全图 K10 —— 名相用字高度互渗。"
                        "故有意义之结构在**较高阈值之过滤**中显现（见 filtration）。"),
            readout_en=("At t=1 every pair of directions shares a character, so the graph is the complete "
                        "graph K10. Structure appears only under higher-threshold filtration (see filtration).")),
        "geometry": ds.lens_geometry(
            nv, w, method_zh=METHOD_ZH, method_en=METHOD_EN, report_dims=(0, 1, 2, 3),
            readout_zh="t 自 %d 降至 1，复形由疏而满：十顶点启 10 个 H0 类，随边出现而并，终余 1（连通）；"
                       "H1／H2 之类随环而生、随三角形／四面体填充而灭。" % maxt,
            readout_en=("As t drops from %d to 1 the complex densifies: the ten vertices start 10 H0 classes that "
                        "merge as edges appear, leaving 1 (connected); H1/H2 classes are born with cycles and die as "
                        "triangles/tetrahedra fill them.") % maxt),
    }
    data["geometry"]["spectral"] = ds.spectral_geometry(nv, w, ids=ids, labels={nd["id"]: nd["label_zh"] for nd in nodes}, top_k=8)
    OUT.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False, default_flow_style=False), encoding="utf-8")
    print("wrote", OUT)
    print("L1 chars=%d uniq=%d H=%.4f zipf=%.4f" % (
        data["linguistic"]["corpus"]["cjk_total"], data["linguistic"]["corpus"]["unique_chars"],
        data["linguistic"]["corpus"]["shannon_entropy_bits"], data["linguistic"]["zipf"]["slope"]))
    print("L2 orbits=%s fixed_sum=%d" % (data["algebra"]["octagon_symmetry"]["num_orbits"],
                                          data["algebra"]["octagon_symmetry"]["burnside_fixed_sum"]))
    print("L3 V=%d maxW=%d t1: beta0=%d beta1=%d tri=%d" % (
        data["topology"]["graph"]["nodes"], data["topology"]["graph"]["max_weight"],
        data["topology"]["flag_complex"]["at_t1"]["beta0"],
        data["topology"]["flag_complex"]["at_t1"]["beta1"],
        data["topology"]["flag_complex"]["at_t1"]["triangles"]))
    _g = data["geometry"]
    print("L4 simplices=%d maxdim=%d H0=%d H1=%d H2=%d H3=%d essential(H0)=%d" % (
        _g["n_simplices"], _g["max_dim"], len(_g["barcode"]["H0"]), len(_g["barcode"]["H1"]),
        len(_g["barcode"]["H2"]), len(_g["barcode"]["H3"]), len(_g["essential"]["H0"])))
