# -*- coding: utf-8 -*-
"""
ru_lai_studies.py — 《如来现相品》数据科学层生成器（三视角）

三层分源：经文事实（data/translation/ru_lai_assembly.yaml，逐字回源 T10n0279 卷六）
          → 本条生成器（析构·度量）
          → data/translation/ru_lai_studies.yaml（呈现层所消费）。

三视角：
  L1 语言统计（linguistic-statistical）：字频／Zipf／Shannon 熵／TF-IDF／「海」族词。
  L2 代数·组合（algebraic-combinatorial）：八方之 D8 群作用（Burnside 定轨数）、
      十方之对径胚（antipodal）五对、四十问之「海」特征二分。
  L3 拓扑（topological）：十方名相共字图之连通分量 β0、环数 β1（1-骨架）、
      按共字数阈值之 0 维持久化（合并树）。

约束：零新增依赖（纯 Python）；一切数字自卷六实测或自 assembly 明列数据算出；
      凡不可考者不臆造。L2 之群作用为对「八方方位」之对称性分析，非经文所言。
"""
import sys
import math
import re
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import miaoyan_metrics as mm  # noqa: E402
import yaml  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
ASM = ROOT / "data" / "translation" / "ru_lai_assembly.yaml"
OUT = ROOT / "data" / "translation" / "ru_lai_studies.yaml"

CJK = re.compile(r"[\u3400-\u9fff]")

KEY_TERMS = ["海", "光", "如來", "佛", "智", "蓮華", "莊嚴", "世界", "眾生",
             "菩薩", "雲", "三昧", "解脫", "光明", "微塵", "佛剎", "供養", "十方", "法界"]


def cjk_chars(s):
    return [c for c in s if CJK.match(c)]


def entropy(counter):
    n = sum(counter.values())
    if n == 0:
        return 0.0
    return -sum((v / n) * math.log2(v / n) for v in counter.values())


def ols_slope(xs, ys):
    n = len(xs)
    mx = sum(xs) / n
    my = sum(ys) / n
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den = sum((x - mx) ** 2 for x in xs)
    return num / den


def bigrams(s):
    cs = cjk_chars(s)
    return [cs[i] + cs[i + 1] for i in range(len(cs) - 1)]


# ───────────────────────── L1 语言统计 ─────────────────────────
def verse_groups(vol6, asm):
    """以偈颂起句为锚切出 14 个偈颂群文本（起句→下一锚点），供 TF-IDF。"""
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


def lens_linguistic(vol6, asm):
    chars = cjk_chars(vol6)
    n = len(chars)
    freq = Counter(chars)
    uniq = len(freq)
    h = entropy(freq)
    ranks = sorted(freq.values(), reverse=True)[:200]
    xs = [math.log(r + 1) for r in range(len(ranks))]
    ys = [math.log(f) for f in ranks]
    slope = ols_slope(xs, ys)
    top = [{"char": c, "count": v} for c, v in freq.most_common(15)]

    term_counts = {t: vol6.count(t) for t in KEY_TERMS}

    # 「海」族词：每一「海」前 1-2 个 CJK 字
    seg = []
    for i, c in enumerate(vol6):
        if c == "海":
            pc = "".join(cjk_chars(vol6[max(0, i - 3):i]))
            if pc:
                seg.append((pc[-2:] if len(pc) >= 2 else pc) + "海")
    sea = Counter(seg)

    groups = verse_groups(vol6, asm)
    docs = {gid: Counter(bigrams(txt)) for gid, txt in groups}
    df = Counter()
    for d in docs.values():
        for t in d:
            df[t] += 1
    tfidf = {}
    for gid, cnt in docs.items():
        total = sum(cnt.values()) or 1
        scored = {t: (c / total) * math.log((len(docs) + 1) / (df[t] + 1)) for t, c in cnt.items()}
        scored = {t: s for t, s in scored.items() if cnt[t] >= 2 and df[t] <= 6}
        top_t = sorted(scored.items(), key=lambda kv: (-kv[1], kv[0]))[:5]
        tfidf[gid] = [{"form": t, "tfidf": round(s, 5), "count": cnt[t]} for t, s in top_t]

    return {
        "corpus": {
            "cjk_total": n,
            "unique_chars": uniq,
            "type_token_ratio": round(uniq / n, 4),
            "shannon_entropy_bits": round(h, 4),
            "max_entropy_bits": round(math.log2(uniq), 4),
            "note_zh": "字熵以卷六经文（CJK 表意字）计；ZIPF 斜率取秩 1–200 之 log–log 最小二乘。",
            "note_en": "Character entropy over the CJK characters of juan 6; Zipf slope is the log-log least-squares fit over ranks 1–200.",
        },
        "zipf": {
            "ranks": len(ranks),
            "slope": round(slope, 4),
            "top_chars": [{"char": c, "count": v} for c, v in freq.most_common(15)],
        },
        "term_counts": {t: vol6.count(t) for t in KEY_TERMS},
        "sea_family": {
            "total_sea": vol6.count("海"),
            "distinct_forms": len([k for k in sea if k != "海"]),
            "top": [{"form": k, "count": v} for k, v in sea.most_common(20) if k != "海"],
        },
        "tfidf": tfidf,
    }


# ───────────────────────── L2 代数·组合 ─────────────────────────
def lens_algebra(asm):
    horiz_ids = ["E", "SE", "S", "SW", "W", "NW", "N", "NE"]  # 顺时针 45° 步（E=0°）
    qa = asm["questions"]["group_a"]["items_zh"]
    qb = asm["questions"]["group_b"]["items_zh"]

    # D8 作用：旋转 r_m: k->k+m；反射 s_m: k->m-k（皆 mod 8）；两极 U(8),D(9) 不动
    group = []
    for m in range(8):
        group.append(("r%d" % m, [((k + m) % 8) for k in range(8)] + [8, 9]))
    for m in range(8):
        group.append(("s%d" % m, [((m - k) % 8) for k in range(8)] + [8, 9]))

    fixed_sum = sum(sum(1 for i in range(10) if perm[i] == i) for _, perm in group)
    orbits = fixed_sum / len(group)
    # 显式轨道（对生成元闭包）
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
            "group_a": len(qa),
            "group_b": len(qb),
            "group_a_endswith_sea": sum(1 for t in qa if t.endswith("海")),
            "group_b_endswith_sea": sum(1 for t in qb if t.endswith("海")),
            "readout_zh": "以「海」作词尾之单一特征即完全分判甲、乙二组（甲 0/20，乙 20/20）。",
            "readout_en": "A single lexical feature (terminating in 海) perfectly separates Set A from Set B (A 0/20, B 20/20).",
        },
    }


# ───────────────────────── L3 拓扑 ─────────────────────────
def _rank_gf2(rows, ncols):
    """GF(2) 上矩阵之秩（行阶梯），rows 为 {int 位掩码} 列表。"""
    rows = [r for r in rows if r]
    rank = 0
    for col in range(ncols):
        piv = None
        bit = 1 << col
        for i in range(rank, len(rows)):
            if rows[i] & bit:
                piv = i
                break
        if piv is None:
            continue
        rows[rank], rows[piv] = rows[piv], rows[rank]
        for i in range(len(rows)):
            if i != rank and (rows[i] & bit):
                rows[i] ^= rows[rank]
        rank += 1
    return rank


def lens_topology(asm):
    ids = [d["id"] for d in asm["directions"]]
    fields = {d["id"]: set(cjk_chars("".join([d["world_ocean_zh"], d["land_zh"], d["buddha_zh"], d["bodhisattva_zh"]])))
              for d in asm["directions"]}
    n = len(ids)
    wt = {}
    for i in range(n):
        for j in range(i + 1, n):
            w = len(fields[ids[i]] & fields[ids[j]])
            if w > 0:
                wt[(ids[i], ids[j])] = w

    def graph_at(t):
        adj = {x: set() for x in ids}
        for (a, b), w in wt.items():
            if w >= t:
                adj[a].add(b)
                adj[b].add(a)
        return adj

    def components(adj):
        seen, comps = set(), []
        for x in ids:
            if x in seen:
                continue
            comp, stack = set(), [x]
            while stack:
                u = stack.pop()
                if u in comp:
                    continue
                comp.add(u)
                stack += list(adj[u])
            seen |= comp
            comps.append(comp)
        return comps

    def homology(t):
        """旗复形（clique complex）之 β0、β1（GF(2)）。"""
        adj = graph_at(t)
        edges = [(a, b) for i, a in enumerate(ids) for b in ids[i + 1:] if b in adj[a]]
        eidx = {e: i for i, e in enumerate(edges)}
        comps = components(adj)
        beta0 = len(comps)
        cyc = len(edges) - n + beta0
        tris = [(a, b, c) for i, a in enumerate(ids) for j, b in enumerate(ids[i + 1:], i + 1)
                if b in adj[a] for c in ids[j + 1:] if c in adj[a] and c in adj[b]]
        rows = []
        for (a, b, c) in tris:
            m = 0
            for e in ((a, b), (a, c), (b, c)):
                m |= 1 << eidx[e]
            rows.append(m)
        rank_d2 = _rank_gf2(rows, len(edges)) if tris else 0
        beta1 = cyc - rank_d2
        return {"threshold": t, "edges": len(edges), "beta0": beta0,
                "cyclomatic": cyc, "triangles": len(tris), "rank_d2": rank_d2, "beta1": beta1}

    maxt = max(wt.values()) if wt else 0
    filtration = [homology(t) for t in range(1, maxt + 1)]
    h1 = homology(1)
    adj1 = graph_at(1)
    return {
        "graph": {
            "nodes": n,
            "rule_zh": "两方之「世界海／国土／佛号／上首菩萨」四名相共字 ≥1 则连边；权＝共字数。",
            "rule_en": "Two directions are linked if their four names (ocean/land/buddha/leading bodhisattva) share ≥1 character; weight = shared count.",
            "max_weight": maxt,
            "density_t1": round(2 * h1["edges"] / (n * (n - 1)), 4),
            "degree_t1": {x: len(adj1[x]) for x in ids},
            "components_t1": [sorted(c) for c in components(adj1)],
            "top_edges": [{"a": a, "b": b, "shared": w}
                          for (a, b), w in sorted(wt.items(), key=lambda p: (-p[1], p[0]))[:12]],
            "readout_zh": ("阈值 t＝1 时十方名相两两皆有共字，图退化为完全图 K10 —— 名相用字高度互渗。"
                           "故有意义之结构在**较高阈值之过滤**中显现（见 filtration）。"),
            "readout_en": ("At t=1 every pair of directions shares a character, so the graph is the complete "
                           "graph K10. Structure appears only under higher-threshold filtration (see filtration)."),
        },
        "flag_complex": {
            "note_zh": "β1 取旗复形（clique complex）之整系数模 GF(2) 同调：β1＝(E−V+β0)−rank ∂2。",
            "note_en": "β1 is the GF(2) homology of the flag (clique) complex: β1 = (E − V + β0) − rank(∂2).",
            "at_t1": h1,
        },
        "filtration": {
            "note_zh": "按共字数阈值 t 过滤：阈值越高、保留之边越少，β0(t) 自 1（连通）递增而碎裂；β1 与三角形数同录。",
            "note_en": "Filtration by shared-character threshold t: the higher the threshold, the fewer edges kept, so β0(t) rises from 1 (connected) as components fragment; β1 and triangle counts recorded alongside.",
            "max_threshold": maxt,
            "steps": filtration,
        },
    }


if __name__ == "__main__":
    vol6 = mm.load()[6]
    asm = yaml.safe_load(ASM.read_text(encoding="utf-8"))
    # 回源自检：assembly 之名相须逐字见于卷六
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
                        "Zipf／TF-IDF／群作用／图论诸项皆本站析构。三视角（语言统计·代数组合·拓扑）为观察同一经文之三种窗口。"),
            "note_en": ("This is an analytical (data-science) layer, not a sutra statement. Names and counts come "
                        "from the assembly layer; all statistics are computed here. The three lenses are three windows "
                        "onto one text."),
        },
        "linguistic": lens_linguistic(vol6, asm),
        "algebra": lens_algebra(asm),
        "topology": lens_topology(asm),
    }
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