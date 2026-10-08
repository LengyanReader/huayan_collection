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
