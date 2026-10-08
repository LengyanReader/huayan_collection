# -*- coding: utf-8 -*-
"""
shizhu_studies.py — 《世主妙嚴品》数据科学层生成器

四视角：
  L1 语言统计（linguistic-statistical）：本品（卷一至卷五）字频／Zipf／Shannon 熵／TF-IDF（按卷）／「海」族词。
  L2 代数·组合（algebraic-combinatorial）：四十类会众之类目普查（所属组／世间／列名员数之分布）。
  L3 拓扑（topological）：四十类名相（类名＋上首名）共字加权图之 β0、β1（旗复形、GF(2)）。
  L4 几何·持久同调（persistent homology）：同名相复形按共字阈值过滤之持久条形
      （节点四十，限维至 3，报 H0–H2）。

三层分源：经文事实（data/translation/miaoyan_assembly.yaml，逐字回源 T10n0279 卷一至卷五）
          → 本条生成器（析构·度量，四视角算子见 scripts/data_science.py）
          → data/translation/shizhu_studies.yaml（呈现层所消费）。

约束：零新增依赖（纯 Python）；数字自底本实测或自 assembly 明列数据算出；凡不可考者不臆造。
"""
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import miaoyan_metrics as mm  # noqa: E402
import data_science as ds  # noqa: E402
import yaml  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
ASM = ROOT / "data" / "translation" / "miaoyan_assembly.yaml"
OUT = ROOT / "data" / "translation" / "shizhu_studies.yaml"

KEY_TERMS = ["佛", "菩薩", "神", "天王", "龍王", "海", "光明", "解脫門", "功德", "莊嚴",
             "眾生", "世界", "微塵", "如來", "三昧", "供養", "神力", "威神", "清淨",
             "智慧", "法界", "眾會", "善根"]

REALM_ZH = {"智正觉世间主": "智正覺世間主", "器世间主": "器世間主",
            "众生世间主": "眾生世間主", "天众": "天眾"}

# ───────── 四视角「分析说明」卡（目的·方法·效果；中英必配）─────────
# 呈现层 web/demo/src/data_science.js 逐视角取用，渲染于该视角读数之前。
# 纪律：只述本数据层确已算出者（数字与本文件产出之 YAML 同源），
#       不引外部基准、不加未经回源之判断；L2 须标明本品无天然对称群故作普查。
LENS_GUIDES = {
    "linguistic": {
        "purpose_zh": ("为本品（卷一至卷五）用字立一份可复核的量化底账——篇幅多少、字头几何、"
                       "用字集中到什么程度、词频如何分布、逐卷各有何特征词——作为其余三视角的对照背景。"),
        "purpose_en": ("To establish a reproducible quantitative baseline for the chapter (juan 1–5) — length, "
                       "character inventory, concentration, frequency profile and the distinctive terms of each "
                       "juan — as the background against which the other three lenses are read."),
        "method_zh": ("只取 T10n0279 卷一至卷五之 CJK 表意字；计字次与字头，算型例比 TTR 与香农熵 "
                      "H＝−Σp·log₂p（上限 log₂ 字头数）；Zipf 斜率取秩 1–200 的 log–log 最小二乘；"
                      "TF-IDF 以五卷为文档单位取各卷特征词。"),
        "method_en": ("Only CJK characters of juan 1–5 (T10n0279) are counted. Tokens, types, the type-token "
                       "ratio and Shannon entropy H = −Σp·log₂p (upper bound = log₂ of types) are computed; "
                       "the Zipf slope is a log-log least-squares fit over ranks 1–200; TF-IDF treats each of "
                       "the five juan as a document and extracts its distinctive terms."),
        "effect_zh": ("本品 31,953 字、837 字头（TTR 0.0262），字熵 7.9521 bit，为其上限 9.7091 bit 之 82%；"
                      "Zipf 斜率 −0.8003；字频前五为「一」673、「神」618、「無」604、「眾」597、「切」551。"
                      "篇幅约为《如来现相品》（8,119 字）之四倍，字头数（837 对 498）与熵"
                      "（7.9521 对 7.5454 bit）亦相应更高，而 Zipf 斜率同在 −0.8 上下。"),
        "effect_en": ("The chapter runs to 31,953 characters with 837 types (TTR 0.0262); character entropy is "
                      "7.9521 bits against an upper bound of 9.7091 bits (82%), and the Zipf slope is −0.8003. "
                      "The five most frequent characters are 一 (673), 神 (618), 無 (604), 眾 (597) and 切 (551). "
                      "At roughly four times the length of the Tathāgata's Manifestation chapter (8,119 "
                      "characters), it has correspondingly more types (837 against 498) and higher entropy "
                      "(7.9521 against 7.5454 bits), while both Zipf slopes sit near −0.8."),
    },
    "algebra": {
        "purpose_zh": ("本品四十类会众无天然之对称群可作用（异于〈如来现相品〉之十方方位），故此视角不问"
                       "「对称」而问「构成」：把会众按所属组、世间摄属、列名员数三面数清，见其结构之数。"),
        "purpose_en": ("The forty classes of this chapter admit no natural symmetry group (unlike the ten "
                       "directions of the Tathāgata's Manifestation), so this lens asks not about symmetry but "
                       "about composition: the assembly counted on three faces — group, realm and listed-member "
                       "count."),
        "method_zh": ("对 assembly 层四十类逐类计数，作三张频数表（所属组／世间摄属／列名员数 n_named），"
                      "并把列名员数之和与 assembly 层 metrics.named_total 对账。"),
        "method_en": ("Every class in the assembly layer is counted, yielding three frequency tables (by group, "
                       "by realm, by listed-member count n_named); the summed listed members are then reconciled "
                       "against metrics.named_total of the assembly layer."),
        "effect_zh": ("四十类＝菩萨 1 ＋ 异生众 39（十九类神 19・八部四王 8・欲界天七众 7・色界天五众 5）；"
                      "列名员数合计 414 名，与 assembly 层对账相合——普查既给出会众之构成，也对经文事实层"
                      "作了一次交叉校验。"),
        "effect_en": ("Forty classes = 1 bodhisattva class + 39 other classes (19 god-classes, 8 legions and "
                       "kings, 7 desire-realm classes, 5 form-realm classes); listed members total 414, "
                       "reconciling exactly with the assembly layer — the census gives the composition of the "
                       "assembly and simultaneously cross-checks the factual layer."),
    },
    "topology": {
        "purpose_zh": ("把四十类名相（类名＋上首之名）的共字关系化为一张加权图，问会众名号在多强的取舍"
                       "（阈值）下仍连成一片、何时开始成环——名号之间的结构由此可以度量。"),
        "purpose_en": ("To recast the shared-character relations among the forty classes (class name plus leading "
                       "member) as a weighted graph, asking how strong a threshold the assembly's names survive "
                       "while staying connected and when cycles appear — the structure among names thereby "
                       "becomes measurable."),
        "method_zh": ("顶点＝四十类；类名与上首之名共字 ≥1 连边，权＝共字数。逐阈值取权 ≥ t 之边，算边数、"
                      "连通分量数 β₀、以及圈秩经 GF(2) 边界约化后的 β₁ 与三角形数。"),
        "method_en": ("Vertices = the forty classes; two classes are joined when class name and leading member "
                       "share at least one character, the weight being the shared-character count. For each "
                       "threshold t only edges of weight ≥ t are kept, and edge count, connected components β₀, "
                       "and — after GF(2) boundary reduction — β₁ and the triangle count are recorded."),
        "effect_zh": ("t＝1 时 391 条边、密度 0.5013，β₀＝1（四十类全连通）而 β₁＝1（环已出现）；最强边为 "
                      "c36–c38（共字 6）。类名多用「神」「天王」等同一后缀，使低阈值之图近乎稠密，"
                      "结构要到更高阈值才分得开：t＝6 时仅余 1 条边、β₀＝39。"),
        "effect_en": ("At t = 1 there are 391 edges (density 0.5013): β₀ = 1, so all forty classes are connected, "
                       "while β₁ = 1, so a cycle has already formed; the strongest edge is c36–c38 with 6 shared "
                       "characters. Because class names reuse the same suffixes (神, 天王 …), the low-threshold "
                       "graph is nearly dense and structure only separates at higher thresholds: at t = 6 a "
                       "single edge remains and β₀ = 39."),
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
                      "直接同调交叉校验。节点四十，为免组合爆炸将单纯形维数限至 3（10,058 个单纯形，"
                      "只报 H0／H1／H2），属「限维旗复形」近似。谱部取加权 Laplacian L＝D−W 之全谱："
                      "λ₂ 为代数连通度，Fiedler 向量给二分方向，归一化 λ₂ 配 Cheeger 不等式量该二分之边界。"),
        "method_en": ("λ(σ) is the minimum shared-character count over the edges of σ, K_t = {σ : λ(σ) ≥ t}, "
                       "with t from max down to 1 (an increasing filtration). GF(2) boundary-matrix reduction "
                       "yields per-dimension (birth, death) bars, cross-checked against a direct homology "
                       "computation of the final complex via the Euler–Poincaré identity χ = Σ(−1)ⁱβᵢ. With "
                       "forty nodes the simplex dimension is capped at 3 — 10,058 simplices, reporting only "
                       "H0/H1/H2 — a dimension-capped flag-complex approximation. The spectral part takes the "
                       "full spectrum of the weighted Laplacian L = D − W: λ₂ is the algebraic connectivity, "
                       "the Fiedler vector gives the bisection direction, and the normalized λ₂ with Cheeger's "
                       "inequality measures that cut's boundary."),
        "effect_zh": ("t 自 6 降至 1：β₀ 由 39 合至 1，t＝1 时 β₁＝1；本质类 H0 一条＋H1 一条——有一个贯穿全程的环，"
                      "与〈如来现相品〉十方图之 H1 本质类为 0 成对照。谱部：Σλ＝1310＝2m，λ₂＝3.400、"
                      "归一化 λ₂＝0.109（十方图为 0.923），Cheeger 值 0.0707（割 20，"
                      "λ₂/2 ≤ h ≤ √(2λ₂) 成立）；Fiedler 二分恰为 c00–c19 与 c20–c39 两域（各 20 类），"
                      "即「菩萨＋十九类神」与「八部四王＋欲界七众＋色界五众」。"),
        "effect_en": ("As t falls from 6 to 1, β₀ contracts from 39 to 1 and at t = 1 we have β₁ = 1; the "
                      "essential classes are one in H0 and one in H1 — a single cycle persists through the whole "
                      "filtration, where the ten-direction graph of the Tathāgata's Manifestation has no "
                      "essential H1. Spectrally: Σλ = 1310 = 2m, λ₂ = 3.400, normalized λ₂ = 0.109 (0.923 for "
                      "the ten-direction graph), Cheeger value 0.0707 (cut of 20, with λ₂/2 ≤ h ≤ √(2λ₂) "
                      "satisfied). The Fiedler bisection falls exactly on c00–c19 against c20–c39 (twenty "
                      "classes each), that is, bodhisattva plus the nineteen god-classes against the eight "
                      "legions and kings, the seven desire-realm and the five form-realm classes."),
    },
}



def lens_algebra_census(asm):
    """四十类会众之类目普查（组合析构；本品无天然对称群，故不设群作用）。"""
    cls = asm["classes"]
    by_group = Counter(c["group_zh"] for c in cls)
    by_realm = Counter(c["realm"] for c in cls)
    by_named = Counter(c["n_named"] for c in cls)
    total_named = sum(c["n_named"] for c in cls)
    census = [
        {"title_zh": "按所属组", "title_en": "By group",
         "rows": [[k, v] for k, v in by_group.most_common()]},
        {"title_zh": "按世间摄属", "title_en": "By realm",
         "rows": [[REALM_ZH.get(k, k), v] for k, v in by_realm.most_common()]},
        {"title_zh": "按列名员数 n_named", "title_en": "By listed-member count",
         "rows": [[("列名 %d 员" % k), v] for k, v in sorted(by_named.items(), reverse=True)]},
    ]
    return {
        "kind": "census",
        "note_zh": ("本品四十类会众无天然之对称群可作用（异于〈如来现相品〉之十方方位），"
                    "故本视角作组合普查：以类目、摄属、列名员数三分，见其构成之数。"),
        "note_en": ("The forty classes here admit no natural symmetry group (unlike the ten directions of the "
                    "Tathāgata's Manifestation); this lens is thus a combinatorial census — by group, realm, and "
                    "listed-member count."),
        "readout_zh": ("四十类＝菩萨 1 ＋ 异生众 39（十九类神 19・八部四王 8・欲界天七众 7·色界天五众 5）；"
                       "列名员数合计 %d 名（n_named 之和），与 assembly.metrics.named_total 相合。" % total_named),
        "readout_en": ("Forty classes = 1 bodhisattva class + 39 other classes (19 god-classes, 8 legions/kings, "
                       "7 desire-realm, 5 form-realm); listed members total %d, matching assembly.metrics.named_total."
                       % total_named),
        "census": census,
        "total_classes": len(cls), "total_named": total_named,
    }


def build_nodes(asm):
    nodes = []
    for i, c in enumerate(asm["classes"]):
        chars = "".join(ch for ch in (c["cat"] + c.get("leader", "")) if "\u4e00" <= ch <= "\u9fff")
        nodes.append({"id": "c%02d" % i, "label_zh": c["cat"], "chars": chars})
    return nodes


if __name__ == "__main__":
    J = mm.load()
    pin = "".join(J[n] for n in range(1, 6))
    asm = yaml.safe_load(ASM.read_text(encoding="utf-8"))

    nodes = build_nodes(asm)
    nv, w, maxt = ds._weights(nodes)
    ids = [nd["id"] for nd in nodes]
    labels = {nd["id"]: nd["label_zh"] for nd in nodes}
    n_edges_t1 = sum(1 for x in w.values() if x >= 1)

    data = {
        "meta": {
            "id": "shizhu-studies",
            "article": "shizhu-miaoyan",
            "title_zh": "《世主妙嚴品》数据科学层",
            "title_en": "The Lords of the Assembly · Data-Science Layer",
            "source_primary": "CBETA T10n0279《大方廣佛華嚴經》卷一至卷五·世主妙嚴品第一",
            "generated_by": "scripts/shizhu_studies.py",
            "sources": [{"label": "CBETA T10n0279", "url": "https://cbetaonline.dila.edu.tw/zh/T10n0279"}],
            "note_zh": ("体例：本层为数据科学层产物，非经文陈述。名相与数目出 assembly 层（40 类／414 名）；"
                        "字频／熵／Zipf／TF-IDF／组合普查／图论诸项皆本站析构。四视角"
                        "（语言统计·代数组合·拓扑·几何持久同调）为观察同一品经文之四种窗口。"),
            "note_en": ("This is an analytical (data-science) layer, not a sutra statement. Names and counts come "
                        "from the assembly layer (40 classes / 414 named); all statistics are computed here. The four "
                        "lenses are four windows onto one chapter."),
        },
        "lens_guides": LENS_GUIDES,
        "linguistic": ds.lens_linguistic(
            pin, KEY_TERMS, doc_groups=[("卷%d" % n, J[n]) for n in range(1, 6)],
            sea_char="海",
            note_zh=("字熵以本品（卷一至卷五）经文（CJK 表意字）计；Zipf 斜率取秩 1–200 之 log–log 最小二乘；"
                     "TF-IDF 以卷为文档单位。"),
            note_en=("Character entropy over the CJK characters of the chapter (juan 1–5); Zipf slope is the log-log "
                     "least-squares fit over ranks 1–200; TF-IDF treats each juan as a document."),
            tfidf_top=8, tfidf_max_df=3),
        "algebra": lens_algebra_census(asm),
        "topology": ds.lens_topology(
            nv, w,
            rule_zh="两「类」（其类名与上首之名）共字 ≥1 则连边；权＝共字数。",
            rule_en="Two classes are linked if their class name and leading name share ≥1 character; weight = shared count.",
            readout_zh=("阈值 t＝1 时四十类名相（类名＋上首）两两共字者达 %d 条边（密度 %.3f）——"
                        "因类名多用同一后缀（如「神」「天王」）而高度互渗，图近乎稠密。"
                        "有意义之结构在较高阈值之过滤中显现（见 filtration）。" % (n_edges_t1, 0.0)),
            readout_en=("At t=1 the forty class-names (class + leading member) share characters on %d edges — the "
                        "heavy reuse of common suffixes (神, 天王 …) makes the graph nearly dense; structure appears "
                        "only under higher-threshold filtration (see filtration)." % n_edges_t1),
            ids=ids, labels=labels, top_n=15),
    }
    # 密度需先算 filled density（readout 内占位 0.0 于后补给）
    dens = round(2 * n_edges_t1 / (nv * (nv - 1)), 4)
    data["topology"]["graph"]["density_t1"] = dens
    data["topology"]["graph"]["readout_zh"] = (
        "阈值 t＝1 时四十类名相（类名＋上首）两两共字者达 %d 条边（密度 %.3f）——"
        "因类名多用同一后缀（如「神」「天王」）而高度互渗，图近乎稠密。"
        "有意义之结构在较高阈值之过滤中显现（见 filtration）。" % (n_edges_t1, dens))

    data["geometry"] = ds.lens_geometry(
        nv, w, max_simplex_dim=3, report_dims=(0, 1, 2),
        method_zh=("顶点＝四十类；λ(σ)＝σ 诸边共字数之最小值（顶点最先出现）；K_t＝{σ:λ(σ)≥t}，"
                   "t 自 max 降至 1（增过滤）。以 GF(2) 边界矩阵约化得各维配对（birth, death）。"
                   "节点四十，为避免组合爆炸，限单纯形维数至 3（故只报 H0／H1／H2 三维持久条形），"
                   "乃『限维旗复形』近似。"),
        method_en=("Vertices = forty classes; λ(σ) = min shared-character count over the edges of σ (vertices "
                   "first); K_t = {σ:λ(σ)≥t}, t from max down to 1 (increasing filtration). GF(2) boundary-matrix "
                   "reduction yields per-dimension (birth, death) pairs. With forty nodes the simplex dimension is "
                   "capped at 3 (a dimension-capped flag-complex approximation) to avoid combinatorial explosion, "
                   "so only H0/H1/H2 bars are reported."),
        readout_zh=("t 自 %d 降至 1，复形由疏而满：四十顶点启 40 个 H0 类，随边出现而并，终余 1（连通）；"
                    "H1／H2 之类随环而生、随三角形／四面体填充而灭。" % maxt),
        readout_en=("As t drops from %d to 1 the complex densifies: the forty vertices start 40 H0 classes that "
                    "merge as edges appear, leaving 1 (connected); H1/H2 classes are born with cycles and die as "
                    "triangles/tetrahedra fill them." % maxt),
    )

    data["geometry"]["spectral"] = ds.spectral_geometry(nv, w, ids=ids, labels=labels, top_k=8)

    OUT.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False, default_flow_style=False), encoding="utf-8")
    print("wrote", OUT)
    c = data["linguistic"]["corpus"]
    print("L1 cjk=%d uniq=%d H=%.4f zipf=%.4f" % (
        c["cjk_total"], c["unique_chars"], c["shannon_entropy_bits"], data["linguistic"]["zipf"]["slope"]))
    print("L2 census classes=%d named=%d" % (len(asm["classes"]), sum(x["n_named"] for x in asm["classes"])))
    g = data["topology"]["graph"]
    print("L3 V=%d maxW=%d t1 edges=%d beta0=%d beta1=%d tri=%d" % (
        g["nodes"], g["max_weight"], n_edges_t1,
        data["topology"]["flag_complex"]["at_t1"]["beta0"],
        data["topology"]["flag_complex"]["at_t1"]["beta1"],
        data["topology"]["flag_complex"]["at_t1"]["triangles"]))
    gg = data["geometry"]
    print("L4 simplices=%d maxdim=%d H0=%d H1=%d H2=%d truncated=%s" % (
        gg["n_simplices"], gg["max_dim"], len(gg["barcode"]["H0"]), len(gg["barcode"]["H1"]),
        len(gg["barcode"]["H2"]), gg["truncated"]))
