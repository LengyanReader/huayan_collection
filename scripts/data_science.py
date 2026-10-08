# -*- coding: utf-8 -*-
"""
data_science.py — 数据科学层·通用引擎（语言统计／代数组合／拓扑／几何持久同调）

各品细读之「数据科学层」共用此引擎。各品以薄驱动（见 ru_lai_studies.py /
shizhu_studies.py）提供「底本文字」与「节点集」，本引擎据以计算，写出
data/translation/<article>_studies.yaml（呈现层所消费）。

四视角（零新增依赖之纯 Python；数字自底本实测或自 assembly 明列数据算出）：
  L1 语言统计 lens_linguistic：字频／Zipf／Shannon 熵／TF-IDF／某字族词。
  L2 代数·组合：各品结构不同（方位之 D8 群作用、会众之类目普查），故由驱动各自
      提供，本引擎不强套一式。
  L3 拓扑 lens_topology：节点名相共字加权图之连通分量 β0、环数 β1（旗复形、GF(2)）。
  L4 几何 lens_geometry：同名相复形按共字阈值过滤之各维持久条形（birth, death）。

规模自适应：节点数小者（≤ FULL_SIMPLEX_LIMIT）枚举全体单纯形（完整持久同调）；
节点数大者限定 max_simplex_dim（仅枚举至该维之团），以免组合爆炸。
"""
import math
import re
from collections import Counter
from itertools import combinations

CJK = re.compile(r"[\u3400-\u9fff]")

# 完整单纯形枚举之上限（nv ≤ 此值则全枚举，得完整持久同调）
FULL_SIMPLEX_LIMIT = 11


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
def lens_linguistic(text, key_terms, *, doc_groups=None, sea_char=None,
                    note_zh="", note_en="", top_chars=15, tfidf_top=5,
                    tfidf_min_count=2, tfidf_max_df=6):
    """通用语言统计。

    text       : 底本文字。
    key_terms  : 关键词频词表。
    doc_groups : [(gid, group_text)]，供 TF-IDF；None 则不算。
    sea_char   : 若给定（如「海」），统计「〈前 1–2 字〉＋sea_char」之构词。
    """
    chars = cjk_chars(text)
    n = len(chars)
    freq = Counter(chars)
    uniq = len(freq)
    h = entropy(freq)
    ranks = sorted(freq.values(), reverse=True)[:200]
    xs = [math.log(r + 1) for r in range(len(ranks))]
    ys = [math.log(f) for f in ranks]
    slope = ols_slope(xs, ys)
    top = [{"char": c, "count": v} for c, v in freq.most_common(top_chars)]

    out = {
        "corpus": {
            "cjk_total": n,
            "unique_chars": uniq,
            "type_token_ratio": round(uniq / n, 4) if n else 0,
            "shannon_entropy_bits": round(h, 4),
            "max_entropy_bits": round(math.log2(uniq), 4) if uniq else 0,
            "note_zh": note_zh,
            "note_en": note_en,
        },
        "zipf": {"slope": round(slope, 4), "top_chars": top},
        "term_counts": {t: text.count(t) for t in key_terms},
    }

    if sea_char:
        seg = []
        for i, c in enumerate(text):
            if c == sea_char:
                pc = "".join(cjk_chars(text[max(0, i - 3):i]))
                seg.append(pc[-2:] + sea_char if pc else sea_char)
        fam = Counter(s for s in seg if s != sea_char)
        out["sea_family"] = {
            "char": sea_char,
            "total_sea": text.count(sea_char),
            "distinct_forms": len(fam),
            "top": [{"form": k, "count": v} for k, v in fam.most_common(20)],
        }

    if doc_groups:
        docs = [(gid, Counter(bigrams(t))) for gid, t in doc_groups]
        df = Counter()
        for _, b in docs:
            for k in b:
                df[k] += 1
        ndoc = len(docs)
        tfidf = {}
        for gid, b in docs:
            tot = sum(b.values()) or 1
            scored = {t: (c / tot) * math.log((ndoc + 1) / (df[t] + 1))
                      for t, c in b.items() if c >= tfidf_min_count and df[t] <= tfidf_max_df}
            keys = sorted(scored, key=lambda k: (-scored[k], k))[:tfidf_top]
            tfidf[gid] = [{"form": k, "tfidf": round(scored[k], 5), "count": b[k]} for k in keys]
        out["tfidf"] = tfidf

    return out


# ───────────────────────── 图论 · GF(2) 线性代数 ─────────────────────────
def rank_gf2(rows, ncols):
    """GF(2) 之秩。rows 为「列向量」之整数位掩码（位＝行下标），ncols＝行数。"""
    rows = list(rows)
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


def _weights(nodes):
    nv = len(nodes)
    chars = [set(nd["chars"]) for nd in nodes]
    w = {}
    for i, j in combinations(range(nv), 2):
        w[(i, j)] = len(chars[i] & chars[j])
    return nv, w, (max(w.values()) if w else 0)


def _components(nv, w, t):
    adj = [set() for _ in range(nv)]
    for (i, j), x in w.items():
        if x >= t:
            adj[i].add(j)
            adj[j].add(i)
    seen = set()
    comps = []
    for s in range(nv):
        if s in seen:
            continue
        stack = [s]
        comp = []
        while stack:
            x = stack.pop()
            if x in seen:
                continue
            seen.add(x)
            comp.append(x)
            stack.extend(adj[x] - seen)
        comps.append(sorted(comp))
    return comps


def _cliques(nv, w, t, max_size):
    """阈值 t 下之团（全边权重 ≥ t），按规模归集；规模 1 即全体顶点。"""
    adj = [set() for _ in range(nv)]
    for (i, j), x in w.items():
        if x >= t:
            adj[i].add(j)
            adj[j].add(i)
    out = {1: [(i,) for i in range(nv)]}
    prev = set((i,) for i in range(nv))
    for size in range(2, max_size + 1):
        cur = set()
        for c in prev:
            last = c[-1]
            for nx in adj[last]:
                if nx > last and all(v in adj[nx] for v in c):
                    cur.add(c + (nx,))
        if not cur:
            break
        out[size] = sorted(cur)
        prev = cur
    return out


# ───────────────────────── L3 拓扑 ─────────────────────────
def lens_topology(nv, w, *, rule_zh, rule_en, readout_zh, readout_en, top_n=12,
                    labels=None, ids=None):
    """返回 L3 拓扑之呈现数据（图统计＋旗复形 at_t1＋过滤表；过滤自 t=1 升序）。"""
    maxt = max(w.values()) if w else 0
    ids = ids or [str(i) for i in range(nv)]

    def homology(t):
        edges = [(i, j) for i, j in combinations(range(nv), 2) if w[(i, j)] >= t]
        eidx = {e: k for k, e in enumerate(edges)}
        tris = [c for c in combinations(range(nv), 3)
                if all(w[tuple(sorted(e))] >= t for e in combinations(c, 2))]
        r2 = rank_gf2([sum(1 << eidx[tuple(sorted((c[a], c[b])))] for a, b in combinations(range(3), 2))
                       for c in tris], len(edges)) if tris else 0
        comp = _components(nv, w, t)
        beta0 = len(comp)
        cyclomatic = len(edges) - nv + beta0
        return {"threshold": t, "edges": len(edges), "beta0": beta0,
                "cyclomatic": cyclomatic, "triangles": len(tris), "rank_d2": r2,
                "beta1": cyclomatic - r2}

    filt = [homology(t) for t in range(1, maxt + 1)]
    t1 = homology(1)
    comp1 = _components(nv, w, 1)
    deg1 = {}
    for i in range(nv):
        deg1[ids[i]] = sum(1 for j in range(nv) if j != i and w[tuple(sorted((i, j)))] >= 1)
    top_edges = [{"a": ids[i], "b": ids[j], "shared": x}
                 for (i, j), x in sorted(w.items(), key=lambda kv: (-kv[1], kv[0]))[:top_n]]
    return {
        "graph": {
            "nodes": nv, "rule_zh": rule_zh, "rule_en": rule_en, "max_weight": maxt,
            "density_t1": round(2 * t1["edges"] / (nv * (nv - 1)), 4) if nv > 1 else 0,
            "degree_t1": deg1,
            "components_t1": [[ids[k] for k in c] for c in comp1],
            "top_edges": top_edges,
            "labels": labels or {},
            "readout_zh": readout_zh, "readout_en": readout_en,
        },
        "flag_complex": {
            "note_zh": "β1 取旗复形（clique complex）之整系数模 GF(2) 同调：β1＝(E−V+β0)−rank ∂2。",
            "note_en": "β1 is the GF(2) homology of the flag (clique) complex: β1 = (E − V + β0) − rank(∂2).",
            "at_t1": t1,
        },
        "filtration": {
            "note_zh": "按共字数阈值 t 过滤：阈值越高、保留之边越少，β0(t) 自 1（连通）递增而碎裂；β1 与三角形数同录。",
            "note_en": ("Filtration by shared-character threshold t: the higher the threshold, the fewer edges kept, "
                        "so β0(t) rises from 1 (connected) as components fragment; β1 and triangle counts recorded."),
            "max_threshold": maxt,
            "steps": filt,
        },
    }


# ───────────────────────── L4 几何 · 持久同调 ─────────────────────────
def lens_geometry(nv, w, *, method_zh, method_en, report_dims,
                        readout_zh="", readout_en="", max_simplex_dim=None, budget=400000):
    """持久同调。

    max_simplex_dim=None（且 nv 小）→ 全单纯形枚举（含高维），得完整持久同调；
    否则仅枚举至 max_simplex_dim 维之团，report_dims ⊆ 0..max_simplex_dim-1。
    """
    maxt = max(w.values()) if w else 0
    if max_simplex_dim is None:
        top_size = nv
    else:
        top_size = min(nv, max_simplex_dim + 1)

    simplices = []
    truncated = False
    for size in range(1, top_size + 1):
        for c in combinations(range(nv), size):
            if size == 1:
                b = maxt + 1
            else:
                b = min(w[tuple(sorted(e))] for e in combinations(c, 2))
                if b < 1:
                    continue
            simplices.append((c, b))
            if len(simplices) > budget:
                truncated = True
                break
        if truncated:
            break
    simplices.sort(key=lambda sc: (-sc[1], len(sc[0]), sc[0]))
    pos = {sc[0]: i for i, sc in enumerate(simplices)}
    nsim = len(simplices)

    reduced = [0] * nsim
    low_to_col = {}
    pairs = []
    creators = []
    for j in range(nsim):
        c = simplices[j][0]
        col = 0
        if len(c) > 1:
            for r in range(len(c)):
                col ^= (1 << pos[c[:r] + c[r + 1:]])
        while col:
            low = col.bit_length() - 1
            if low in low_to_col:
                col ^= reduced[low_to_col[low]]
            else:
                break
        reduced[j] = col
        if col:
            low = col.bit_length() - 1
            low_to_col[low] = j
            pairs.append((len(simplices[low][0]) - 1, low, j))
        else:
            creators.append(j)
    death_lows = set(low_to_col.keys())
    essential = [j for j in creators if j not in death_lows]

    def bars(dim):
        out = [{"birth": simplices[bi][1], "death": simplices[di][1]}
               for d, bi, di in pairs if d == dim]
        out.sort(key=lambda p: (-p["birth"], p["death"]))
        return out

    def ess(dim):
        return [{"birth": simplices[j][1], "death": None}
                for j in essential if len(simplices[j][0]) - 1 == dim]

    def betti_at(t, maxdim):
        cl = _cliques(nv, w, t, maxdim + 2)

        def rk(colsize, facesize):
            cols = cl.get(colsize, [])
            faces = cl.get(facesize, [])
            if not cols or not faces:
                return 0
            fidx = {c: i for i, c in enumerate(faces)}
            rows = [sum(1 << fidx[c[:r] + c[r + 1:]] for r in range(len(c))) for c in cols]
            return rank_gf2(rows, len(faces))

        ranks = {d: rk(d + 1, d) for d in range(1, maxdim + 2)}
        out = {"t": t, "n1": len(cl.get(2, [])), "n2": len(cl.get(3, [])), "n3": len(cl.get(4, []))}
        for d in range(maxdim + 1):
            out["beta%d" % d] = len(cl.get(d + 1, [])) - ranks.get(d, 0) - ranks.get(d + 1, 0)
        return out

    max_report = max(report_dims)
    curve = [betti_at(t, max_report) for t in range(maxt, 0, -1)]

    # ── 独立之直接同调（对最终复形＝全部已列单纯形，GF(2) 边界约化）──
    #    与持久条形互为交叉校验：Euler–Poincaré 恒等式 χ = Σ(−1)^i β_i。
    _pos = {sc[0]: i for i, sc in enumerate(simplices)}
    _red = [0] * nsim
    _low = {}
    _rank = Counter()
    for _j, (_c, _b) in enumerate(simplices):
        _col = 0
        if len(_c) > 1:
            for _r in range(len(_c)):
                _col ^= 1 << _pos[_c[:_r] + _c[_r + 1:]]
        while _col:
            _l = _col.bit_length() - 1
            if _l in _low:
                _col ^= _red[_low[_l]]
            else:
                break
        _red[_j] = _col
        if _col:
            _low[_col.bit_length() - 1] = _j
            _rank[len(_c) - 1] += 1
    _fdim = Counter(len(sc[0]) - 1 for sc in simplices)
    _maxd = max(_fdim)
    betti_final = {d: _fdim.get(d, 0) - _rank.get(d, 0) - _rank.get(d + 1, 0)
                   for d in range(_maxd + 1)}
    euler_char = sum(((-1) ** d) * _fdim.get(d, 0) for d in range(_maxd + 1))
    euler_from_betti = sum(((-1) ** d) * betti_final[d] for d in range(_maxd + 1))

    if not readout_zh:
        readout_zh = ("t 自 %d 降至 1，复形由疏而满：%d 顶点启 %d 个 H0 类，随边出现而并，终余 1（连通）；"
                      "H1／H2 之类随环而生、随三角形／四面体填充而灭。") % (maxt, nv, nv)
    if not readout_en:
        readout_en = ("As t drops from %d to 1 the complex densifies: the %d vertices start %d H0 classes that "
                      "merge as edges appear, leaving 1 (connected); H1/H2 classes are born with cycles and die as "
                      "triangles/tetrahedra fill them.") % (maxt, nv, nv)

    return {
        "method_zh": method_zh, "method_en": method_en,
        "n_simplices": nsim,
        "max_dim": (nv - 1) if max_simplex_dim is None else max_simplex_dim,
        "truncated": truncated,
        "betti_curve": curve,
        "barcode": {"H%d" % d: bars(d) for d in report_dims},
        "essential": {"H%d" % d: ess(d) for d in report_dims},
        "betti_final": {"H%d" % d: betti_final.get(d, 0) for d in range(_maxd + 1)},
        "euler_char": euler_char,
        "euler_from_betti": euler_from_betti,
        "euler_ok": euler_char == euler_from_betti,
        "readout_zh": readout_zh, "readout_en": readout_en,
    }


# ───────────────────────── L4b 几何 · 谱几何（加权图 Laplacian） ─────────────────────────
def jacobi_eigen(a, sweeps=100, tol=1e-13):
    """对称矩阵之 Jacobi 全谱（返回 (特征值, 特征向量矩阵列)）。a 不被改写。纯 Python。"""
    n = len(a)
    m = [row[:] for row in a]
    v = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for _ in range(sweeps):
        off = sum(m[i][j] ** 2 for i in range(n) for j in range(i + 1, n))
        if off < tol:
            break
        for p in range(n - 1):
            for q in range(p + 1, n):
                if abs(m[p][q]) < 1e-15:
                    continue
                theta = (m[q][q] - m[p][p]) / (2.0 * m[p][q])
                t = (1.0 if theta >= 0 else -1.0) / (abs(theta) + math.sqrt(theta * theta + 1.0))
                c = 1.0 / math.sqrt(t * t + 1.0)
                s = t * c
                for k in range(n):
                    m[k][p], m[k][q] = c * m[k][p] - s * m[k][q], s * m[k][p] + c * m[k][q]
                for k in range(n):
                    m[p][k], m[q][k] = c * m[p][k] - s * m[q][k], s * m[p][k] + c * m[q][k]
                for k in range(n):
                    v[k][p], v[k][q] = c * v[k][p] - s * v[k][q], s * v[k][p] + c * v[k][q]
    return [m[i][i] for i in range(n)], v


def spectral_geometry(nv, w, *, ids=None, labels=None, top_k=8, t=1):
    """加权图 Laplacian L = D − W（W＝共字边权，仅取 ≥ t 之边）之谱几何。

    返回：全谱（升序）、代数连通度 λ₂（Fiedler 值）、谱半径、零特征值数（＝连通分量数）、
    Fiedler 向量（重心方向）及其「重心分域」二分（正／负号之两域）。
    """
    import math as _m
    ids = ids or [str(i) for i in range(nv)]
    A = [[0.0] * nv for _ in range(nv)]
    for (i, j), x in w.items():
        if x >= t:
            A[i][j] = A[j][i] = float(x)
    deg = [sum(A[i]) for i in range(nv)]
    L = [[(deg[i] if i == j else 0.0) - A[i][j] for j in range(nv)] for i in range(nv)]
    eig, V = jacobi_eigen(L)
    order = sorted(range(nv), key=lambda k: eig[k])
    evals = [round(eig[k], 6) for k in order]
    # Fiedler 向量＝对 λ₂（升序第二小）之特征向量
    fidx = order[1] if nv > 1 else order[0]
    fvec = [V[i][fidx] for i in range(nv)]
    # 符号重心分域：正号域 / 负号域（零附近归正）
    pos = [ids[i] for i in range(nv) if fvec[i] >= 0]
    neg = [ids[i] for i in range(nv) if fvec[i] < 0]
    zero_count = sum(1 for e in evals if e < 1e-6)

    # ── 归一化 Laplacian（Cheeger 不等式之正确配对；用于同「归一化」之 conductance）──
    dsqrt = [(_m.sqrt(deg[i]) if deg[i] > 0 else 0.0) for i in range(nv)]
    Ln = [[0.0] * nv for _ in range(nv)]
    for i in range(nv):
        for j in range(nv):
            if i == j:
                Ln[i][j] = 0.0 if deg[i] == 0 else 1.0
            elif dsqrt[i] > 0 and dsqrt[j] > 0:
                Ln[i][j] = -A[i][j] / (dsqrt[i] * dsqrt[j])
    neig, _ = jacobi_eigen(Ln)
    norm_lambda2 = round(sorted(neig)[1], 6) if nv > 1 else 0.0

    # ── Isoperimetric（Cheeger）扫掠切：沿 Fiedler 方向之最小 conductance ──
    total_vol = sum(deg)
    sweep = sorted(range(nv), key=lambda i: fvec[i])
    in_S = [False] * nv
    vol_S = 0.0
    cut = 0.0
    best_h = None
    best_k = 0
    for k in range(1, nv):
        v = sweep[k - 1]
        to_in = sum(A[v][u] for u in range(nv) if in_S[u])
        to_out = sum(A[v][u] for u in range(nv) if not in_S[u])
        cut += to_out - to_in
        vol_S += deg[v]
        in_S[v] = True
        other = total_vol - vol_S
        if vol_S <= 0 or other <= 0:
            continue
        h = cut / min(vol_S, other)
        if best_h is None or h < best_h:
            best_h, best_k = h, k
    lo = max(0.0, norm_lambda2) / 2.0
    hi = _m.sqrt(2.0 * max(0.0, norm_lambda2))
    cheeger = {
        "value": round(best_h if best_h is not None else 0.0, 6),
        "cut_size": best_k,
        "bound_lo": round(lo, 6),
        "bound_hi": round(hi, 6),
        "inequality_ok": (best_h is None) or (lo - 1e-9 <= best_h + 1e-9 and best_h <= hi + 1e-9),
    }

    return {
        "t": t,
        "n_nodes": nv,
        "n_edges_weighted": sum(x for x in w.values() if x >= t),
        "spectrum": evals,
        "top_k": max(1, min(top_k, nv)),
        "algebraic_connectivity": evals[1] if nv > 1 else 0.0,
        "spectral_radius": evals[-1] if evals else 0.0,
        "n_zero_eigen": zero_count,
        "sum_eigen_equals_2m": round(sum(evals), 4),
        "two_edges": 2.0 * sum(x for x in w.values() if x >= t),
        "normalized_algebraic_connectivity": norm_lambda2,
        "cheeger": cheeger,
        "fiedler": {
            "index1": 0,
            "id_neg": neg,
            "id_pos": pos,
            "labels": labels or {},
            "vec": [round(fvec[i], 6) for i in range(nv)],
        },
        "note_zh": ("以加权图 Laplacian L＝D−W（W＝共字边权）之谱为「几何」之不变量："
                    "其最小非零特征值 λ₂ 为代数连通度（Fiedler 值），其对应之 Fiedler 向量"
                    "给出将名相图二分之内在「重心方向」——沿此方向正负号即二分域。"
                    "另以归一化 Laplacian 之 λ₂ 配 Cheeger 不等式，量该二分之内禀边界"
                    "（isoperimetric／conductance），并作 Fiedler 扫掠切以求最小割比。"
                    "此与 L4 之持久同调互补：同调看「洞之生灭」，谱看「图之伸张」。"),
        "note_en": ("Spectral geometry of the weighted graph Laplacian L = D − W (W = shared-character "
                    "edge weights): the smallest non-zero eigenvalue λ₂ is the algebraic connectivity "
                    "(Fiedler value); its Fiedler vector gives an intrinsic bipartition of the name-graph "
                    "(sign of the vector = the two domains). Complementary to L4's persistent homology: "
                    "homology sees the birth/death of holes, the spectrum sees the stretch of the graph."),
    }
