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
