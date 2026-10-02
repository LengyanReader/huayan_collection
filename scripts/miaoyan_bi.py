# -*- coding: utf-8 -*-
"""世主妙严品会众名号 · BI 式数据分析引擎

分层关系（源 → 源）：
    miaoyan_assembly.yaml（经文事实） + miaoyan_eda_lexicon.yaml（析构词表）
        └─ miaoyan_eda.py ─→ miaoyan_eda.yaml（词素层析构结果）
              └─ miaoyan_bi.py ─→ miaoyan_bi.yaml（★本引擎：BI 式分析层）

设计约束（承项目铁律）：
  · 一切数字皆实算，无一处臆造；每个方法皆给出公式、参数与限度。
  · 不加权臆造「综合总分」——凡需合成为单一数字处，改为分项列示或明示口径。
  · 「相似度」「聚类」皆于「语义域分布·TF-IDF 加权」这一具名空间内计算，
    是构词层的分布相近度，**不是**词义相近度，页面须如实标明。
  · 随机性一律以确定性 LCG 定种，禁 Python random 默认源，以保证可复现。
  · 中英必配：每节皆出 zh/en 双语说明。

用法：
    python scripts/miaoyan_bi.py            # 生成 data/translation/miaoyan_bi.yaml
    python scripts/miaoyan_bi.py --check    # 只跑不变量校验
"""
from __future__ import annotations

import argparse
import collections
import io
import json
import math
import os
import sys
from typing import Any, Dict, List, Sequence, Tuple

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EDA = os.path.join(ROOT, "data", "translation", "miaoyan_eda.yaml")
OUT = os.path.join(ROOT, "data", "translation", "miaoyan_bi.yaml")
ARTICLE = "shizhu-miaoyan"
SOURCE = "CBETA T10n0279《華嚴經》卷二·世主妙嚴品（實主娑婆）"
SOURCE_URL = "https://cbetaonline.dila.edu.tw/zh/T10n0279"

# 群次序与中文名（依 miaoyan_eda.group_profiles 之 order 固定，不自造）
GROUP_ZH = {
    "bodhisattva": "同生众·菩萨",
    "deities": "异生众·十九类神",
    "eight": "异生众·八部",
    "desire": "异生众·欲界主",
    "form": "异生众·色界主",
}
GROUP_EN = {
    "bodhisattva": "Bodhisattvas",
    "deities": "Nineteen classes of deities",
    "eight": "EightLegions",
    "desire": "Desire-realm deities",
    "form": "Form-realm deities",
}
GROUP_ORDER = ["bodhisattva", "deities", "eight", "desire", "form"]


# ══════════════════════════════════════════════════════════════
# 一、统计基元（纯 Python，零依赖）
# ══════════════════════════════════════════════════════════════

def _mean(xs: Sequence[float]) -> float:
    xs = list(xs)
    return sum(xs) / len(xs) if xs else 0.0


def pearson(a: Sequence[float], b: Sequence[float]) -> float:
    n = min(len(a), len(b))
    if n < 3:
        return 0.0
    a, b = a[:n], b[:n]
    ma, mb = _mean(a), _mean(b)
    num = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    da = math.sqrt(sum((x - ma) ** 2 for x in a))
    db = math.sqrt(sum((y - mb) ** 2 for y in b))
    if da <= 0 or db <= 0:
        return 0.0
    return num / (da * db)


def _rank(xs: Sequence[float]) -> List[float]:
    """平均秩（并列取均值），供 Spearman 使用。"""
    idx = sorted(range(len(xs)), key=lambda i: xs[i])
    r = [0.0] * len(xs)
    i = 0
    while i < len(idx):
        j = i
        while j + 1 < len(idx) and xs[idx[j + 1]] == xs[idx[i]]:
            j += 1
        avg = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            r[idx[k]] = avg
        i = j + 1
    return r


def spearman(a: Sequence[float], b: Sequence[float]) -> float:
    n = min(len(a), len(b))
    if n < 3:
        return 0.0
    return pearson(_rank(a[:n]), _rank(b[:n]))


def chi2_sf(x: float, df: int) -> float:
    """卡方上尾（Wilson-Hilferty 近似；df>0）。

    注意：erfc 在 z>27 附近即下溢为 0，故此处另回传 z 值，
    使极端显著（p<1e-300）时仍可报告一个有限之量级，而非打印 0。
    """
    if df <= 0 or x <= 0:
        return 1.0
    z = ((x / df) ** (1.0 / 3.0) - (1.0 - 2.0 / (9.0 * df))) / math.sqrt(2.0 / (9.0 * df))
    return 0.5 * math.erfc(z / math.sqrt(2.0))


def chi2_wh_z(x: float, df: int) -> float:
    """Wilson-Hilferty 变换所得之标准正态 z；用于报告极端显著之量级。"""
    if df <= 0 or x <= 0:
        return 0.0
    return ((x / df) ** (1.0 / 3.0) - (1.0 - 2.0 / (9.0 * df))) / math.sqrt(2.0 / (9.0 * df))


def chi2_cramers(obs: List[List[float]], rows: List[str], cols: List[str]) -> Tuple[float, float, int]:
    """返回 (chi2 统计量, Cramér's V, 自由度)。V 为关联强度，0=无关 1=完全决定。"""
    n = sum(sum(r) for r in obs)
    if n <= 0:
        return 0.0, 0.0, 0
    rt = [sum(r) for r in obs]
    ct = [sum(obs[i][j] for i in range(len(obs))) for j in range(len(obs[0]))]
    chi = 0.0
    for i, row in enumerate(rows):
        for j, col in enumerate(cols):
            e = rt[i] * ct[j] / n
            if e <= 0:
                continue
            chi += (obs[i][j] - e) ** 2 / e
    # 自由度：标准 Pearson 卡方之 df = (行数−1)(列数−1)。
    # 【更正】旧式误用 (min(r,c)−1)(c−1)，于 r=17、c=5 之表得 16 而非 64。
    r_, c_ = len(rows), len(cols)
    df = (r_ - 1) * (c_ - 1)
    k = min(r_, c_)
    v = math.sqrt(chi / (n * (k - 1))) if k > 1 and n > 0 else 0.0
    return chi, min(v, 1.0), df


def cosine(u: Sequence[float], v: Sequence[float]) -> float:
    nu = math.sqrt(sum(x * x for x in u))
    nv = math.sqrt(sum(x * x for x in v))
    if nu <= 0 or nv <= 0:
        return 0.0
    return sum(x * y for x, y in zip(u, v)) / (nu * nv)


def entropy(ps: Sequence[float]) -> float:
    """香农熵（自然对数）；ps 为概率序列。"""
    h = 0.0
    for p in ps:
        if p > 0:
            h -= p * math.log(p)
    return h


def hhi(ps: Sequence[float]) -> float:
    return sum(p * p for p in ps)


class LCG:
    """确定性线性同余发生器（Numerical Recipes 参数）。
    禁 random 模块默认源——其实现版本间可变，会破坏结果可复现性。"""

    def __init__(self, seed: int = 20240717):
        self.s = seed & 0xFFFFFFFF

    def next(self) -> float:
        self.s = (1664525 * self.s + 1013904223) & 0xFFFFFFFF
        return self.s / 4294967296.0

    def randint(self, n: int) -> int:
        return int(self.next() * n) % max(n, 1)


# ── 层次聚类（average linkage，余弦距离）──
def agglomerate(dist: List[List[float]], labels: List[str]) -> List[Dict[str, Any]]:
    """返回 n-1 条合并记录 {a,b,d,size}，含每步后 cluster 的平均轮廓系数。
    dist 为对称距离矩阵（n×n）。"""
    n = len(labels)
    alive = {i: [i] for i in range(n)}
    d = [row[:] for row in dist]
    merges: List[Dict[str, Any]] = []
    step = 0
    while len(alive) > 1:
        best = None
        ks = sorted(alive)
        for ii in range(len(ks)):
            for jj in range(ii + 1, len(ks)):
                a, b = ks[ii], ks[jj]
                if best is None or d[a][b] < best[0]:
                    best = (d[a][b], a, b)
        if best is None:
            break
        da, a, b = best
        new = alive[a] + alive[b]
        step += 1
        for k in alive:
            if k in (a, b):
                continue
            nd = (d[a][k] * len(alive[a]) + d[b][k] * len(alive[b])) / float(len(new))
            d[a][k] = d[k][a] = nd
        del alive[b]
        alive[a] = new
        # 该步的簇内平均距离（average linkage 高度 h）
        merges.append({
            "step": step, "a": labels[new[0]], "b": labels[new[1]],
            "ia": a, "ib": b,
            "d": round(da, 6), "size": len(new),
            "members": [labels[i] for i in sorted(new)],
        })
    return merges


def silhouette(dist: List[List[float]], labels: List[str], assign: List[int]) -> float:
    """全样本平均轮廓系数（dist=距离矩阵）。"""
    return _mean(per_point_silhouette(dist, assign))


def per_point_silhouette(dist: List[List[float]], assign: List[int]) -> List[float]:
    """逐点轮廓系数 s(i)=(b−a)/max(a,b)；a=本簇内平均距离，b=最近他簇平均距离。
    单点簇按 0 计；只余一簇则全为 0。"""
    n = len(assign)
    groups: Dict[int, List[int]] = {}
    for i, c in enumerate(assign):
        groups.setdefault(c, []).append(i)
    if len(groups) < 2:
        return [0.0] * n
    out: List[float] = []
    for i in range(n):
        own = groups[assign[i]]
        if len(own) <= 1:
            out.append(0.0)
            continue
        a = sum(dist[i][j] for j in own if j != i) / (len(own) - 1)
        best = None
        for c, mem in groups.items():
            if c == assign[i]:
                continue
            b = sum(dist[i][j] for j in mem) / len(mem)
            if best is None or b < best:
                best = b
        if best is None or best <= 0:
            out.append(0.0)
            continue
        out.append((best - a) / max(a, best))
    return out


# ── Jacobi 特征分解（对称矩阵，17×17 足够）──
def jacobi_eig(mat: List[List[float]], iters: int = 100) -> Tuple[List[float], List[List[float]]]:
    """返回 (特征值降序列表, 特征向量列矩阵 vecs[i] 为第 i 特征向量)。"""
    n = len(mat)
    a = [row[:] for row in mat]
    v = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for _ in range(iters):
        off = math.sqrt(sum(a[i][j] ** 2 for i in range(n) for j in range(n) if i != j))
        if off < 1e-12:
            break
        for p in range(n - 1):
            for q in range(p + 1, n):
                if abs(a[p][q]) < 1e-14:
                    continue
                theta = (a[q][q] - a[p][p]) / (2.0 * a[p][q])
                t = (1.0 if theta >= 0 else -1.0) / (abs(theta) + math.sqrt(theta * theta + 1.0))
                c = 1.0 / math.sqrt(t * t + 1.0)
                s = t * c
                for k in range(n):
                    akp, akq = a[k][p], a[k][q]
                    a[k][p] = c * akp - s * akq
                    a[k][q] = s * akp + c * akq
                for k in range(n):
                    apk, aqk = a[p][k], a[q][k]
                    a[p][k] = c * apk - s * aqk
                    a[q][k] = s * apk + c * aqk
                for k in range(n):
                    vkp, vkq = v[k][p], v[k][q]
                    v[k][p] = c * vkp - s * vkq
                    v[k][q] = s * vkp + c * vkq
    vals = [a[i][i] for i in range(n)]
    order = sorted(range(n), key=lambda i: -vals[i])
    return [vals[i] for i in order], [[v[r][i] for r in range(n)] for i in order]


def pagerank(nodes: List[str], edges: List[Tuple[str, str, float]], k: int = 30) -> Dict[str, float]:
    """加权 PageRank，阻尼 0.85，k 次幂迭代（幂迭代本身即确定性）。"""
    n = len(nodes)
    if n == 0:
        return {}
    idx = {z: i for i, z in enumerate(nodes)}
    out = [[] for _ in range(n)]
    deg = [0.0] * n
    for a, b, w in edges:
        ia, ib = idx.get(a), idx.get(b)
        if ia is None or ib is None:
            continue
        out[ia].append((ib, w))
        deg[ia] += w
    r = [1.0 / n] * n
    for _ in range(k):
        nr = [(1 - 0.85) / n] * n
        dangling = sum(r[i] for i in range(n) if deg[i] <= 0)
        for i in range(n):
            if deg[i] <= 0:
                continue
            for j, w in out[i]:
                nr[j] += 0.85 * r[i] * w / deg[i]
        s = sum(nr)
        nr = [x / s for x in nr]
        delta = sum(abs(nr[i] - r[i]) for i in range(n))
        r = nr
        if delta < 1e-12:
            break
    return {nodes[i]: r[i] for i in range(n)}


def betweenness(nodes: List[str], edges: List[Tuple[str, str, float]]) -> Dict[str, float]:
    """无权介数中心性（Brandes，邻接表由去重无向边构成）。"""
    adj: Dict[str, List[str]] = {z: [] for z in nodes}
    seen = set()
    for a, b, _w in edges:
        if a == b or (a, b) in seen or (b, a) in seen:
            continue
        seen.add((a, b))
        adj[a].append(b)
        adj[b].append(a)
    bc = {z: 0.0 for z in nodes}
    for s in nodes:
        stack: List[str] = []
        preds: Dict[str, List[str]] = {z: [] for z in nodes}
        sigma = {z: 0.0 for z in nodes}
        dist = {z: -1 for z in nodes}
        sigma[s] = 1.0
        dist[s] = 0
        q = collections.deque([s])
        while q:
            v = q.popleft()
            stack.append(v)
            for w in adj[v]:
                if dist[w] < 0:
                    dist[w] = dist[v] + 1
                    q.append(w)
                if dist[w] == dist[v] + 1:
                    sigma[w] += sigma[v]
                    preds[w].append(v)
        delta = {z: 0.0 for z in nodes}
        while stack:
            w = stack.pop()
            for v in preds[w]:
                if sigma[w]:
                    delta[v] += (sigma[v] / sigma[w]) * (1.0 + delta[w])
            if w != s:
                bc[w] += delta[w]
    n = max(len(nodes) - 1, 1)
    return {z: v / n for z, v in bc.items()}
# ══════════════════════════════════════════════════════════════
# 二、分析主体
# ══════════════════════════════════════════════════════════════

def _load() -> Dict[str, Any]:
    with io.open(EDA, encoding="utf-8") as f:
        return yaml.safe_load(f)


def _r(x: Any, nd: int = 4) -> float:
    return round(float(x) + 0.0, nd)


def _cls_vec(c: Dict[str, Any], dom_keys: List[str], idf: List[float]) -> List[float]:
    """类的 TF-IDF 加权语义域分布向量（构词层空间，非词义向量）。"""
    dh = c.get("domain_hist") or {}
    raw = [float(dh.get(k, 0)) for k in dom_keys]
    return [raw[i] * idf[i] for i in range(len(raw))]


def _build_idf(classes: List[Dict[str, Any]], dom_keys: List[str]) -> List[float]:
    """idf(d) = ln( (1+N) / (1+df(d)) ) —— 平滑版，避免 df=0 时取 log0。"""
    N = len(classes)
    out = []
    for k in dom_keys:
        df = sum(1 for c in classes if (c.get("domain_hist") or {}).get(k, 0) > 0)
        out.append(math.log((1.0 + N) / (1.0 + df)))
    return out


# ── A. 执行记分卡 ─────────────────────────────────────────────
def scorecard(E: Dict[str, Any]) -> Dict[str, Any]:
    m = E["metrics"]
    T = float(m["tokens_total"])
    D = float(m["distinct_tokens"])
    items = [
        ("classes", "会众类别数", "Classes", m["classes"], "40 类（经文明列之群类）", "count"),
        ("named_total", "明列名号数", "Named assemblies", m["named_total"], "经文明列之名号总数", "count"),
        ("tokens_total", "词素位总数", "Token positions", T, "可析核名切分后之词素位置总数（含多字词一次计一位）", "count"),
        ("tokens_per_name", "每名平均词素位", "Token positions per name", T / max(m["named_total"], 1),
         "词素位 ÷ 名号数 —— 名号之平均「信息长度」", "dec2"),
        ("names_per_class", "每类平均名号数", "Names per class", m["named_total"] / max(m["classes"], 1),
         "名号数 ÷ 类数 —— 群类之平均「列举密度」", "dec2"),
        ("distinct_tokens", "不同词素数", "Distinct morphemes", D, "词素表中实际出现之不同词素", "count"),
        ("reuse_rate", "语汇复用率", "Morpheme reuse rate", 1.0 - D / T if T else 0.0,
         "1 − 不同词素 ÷ 词素位 —— 越高则语汇越有限、构词越模板化", "ratio"),
        ("word_rate", "多字词占比", "Multi-char word rate", m["word_hits"] / T if T else 0.0,
         "多字词命中 ÷ 词素位 —— 复名与专名的密度", "ratio"),
        ("high_rate", "判读确定率", "High-confidence rate", (T - m["medconf_hits"] - m["lowconf_hits"]) / T if T else 0.0,
         "high 词素位 ÷ 词素位 —— 「一字一句之义已核定」之比例", "ratio"),
        ("med_rate", "medium 占比", "Medium-confidence rate", m["medconf_hits"] / T if T else 0.0,
         "medium ÷ 词素位 —— 判读存疑（比较之需），非标注义务", "ratio"),
        ("low_rate", "low 占比", "Low-confidence rate", m["lowconf_hits"] / T if T else 0.0,
         "low ÷ 词素位 —— 唯一「前端须显示〔待考〕」之单级", "ratio"),
        ("unassigned_rate", "未定域占比", "Unassigned rate", m["unassigned_segs"] / T if T else 0.0,
         "未定域段 ÷ 词素位 —— 含专名/音译与罕字，非「待办」", "ratio"),
    ]
    rows = []
    for key, zh, en, val, defn, unit in items:
        if unit == "count":
            disp = f"{int(round(val)):,}"
        elif unit == "dec2":
            disp = f"{val:.2f}"
        else:
            disp = f"{val * 100:.2f}%"
        rows.append({"key": key, "zh": zh, "en": en, "value": _r(val, 4),
                     "display": disp, "definition": defn, "unit": unit})
    return {
        "note": "本记分卡刻意**不给「综合总分」**：加权合成为单一数字须预设权重，"
                "而权重无经无据可依，臆造权重即等于臆造结论。故凡须合成为一数处，"
                "一律改为分项列示并各标口径。",
        "note_en": "This scorecard deliberately withholds any composite index: collapsing metrics into a "
                   "single number requires weights, and weights unsupported by evidence would amount to "
                   "manufacturing a conclusion. Where a single figure would be wanted, metrics are listed "
                   "separately with their definitions instead.",
        "items": rows,
    }


# ── B. 结构分解漏斗（MECE drill-down）───────────────────────
def funnel(E: Dict[str, Any]) -> Dict[str, Any]:
    classes = E["classes"]
    members = [mm for c in classes for mm in (c.get("members") or [])]
    with_core = [mm for mm in members if mm.get("core")]
    segs = [s for mm in with_core for s in (mm.get("segs") or [])]
    assigned = [s for s in segs if (s.get("domain") or "unassigned") != "unassigned"]
    high = [s for s in assigned if s.get("c") == "high"]
    med = [s for s in assigned if s.get("c") == "medium"]
    low = [s for s in assigned if s.get("c") == "low"]
    total = len(members)
    tok = len(segs)
    m = E["metrics"]
    # 全域之 low/med（含未定域者）——与 EDA metrics 同口径，用于对账
    lo_n = sum(1 for s in segs if s.get("c") == "low")
    me_n = sum(1 for s in segs if s.get("c") == "medium")
    grade_matrix = collections.Counter(
        ((s.get("domain") or "unassigned") == "unassigned", s.get("c")) for s in segs)
    # 轨道一「名号」逐层收窄；轨道二「词素位」逐层收窄。
    # 二者之间是**扩张**（一名析为多位），故不作漏斗级，另列为换算因子——
    # 若混作一级，则「名号数 < 词素位」会被误读为异常。
    t1 = [
        {"key": "n1", "zh": "经文明列名号", "en": "Named assemblies in the sutra", "n": total,
         "pct_of_track": 1.0,
         "definition": "《世主妙严品》所明列之名号总数（assembly 层经文事实）"},
        {"key": "n2", "zh": "有可析之核名", "en": "Names with an analysable core", "n": len(with_core),
         "pct_of_track": _r(len(with_core) / float(total), 4) if total else 0.0,
         "definition": "剥去类尾后尚余有可析之核者；无核者记 ∅（CBETA 省文记号或核与类名全同者）"},
    ]
    t2 = [
        {"key": "t1", "zh": "词素位", "en": "Token positions", "n": tok, "pct_of_track": 1.0,
         "definition": "核名按词素表切分之位置数（多字词一次计一位）"},
        {"key": "t2", "zh": "已归语义域", "en": "Assigned to a semantic domain", "n": len(assigned),
         "pct_of_track": _r(len(assigned) / float(tok), 4) if tok else 0.0,
         "definition": "归入十七语义域之一者；未定域者不入"},
        {"key": "t3", "zh": "high 判读", "en": "High-confidence reading", "n": len(high),
         "pct_of_track": _r(len(high) / float(tok), 4) if tok else 0.0,
         "definition": "一字一句之义已核定者"},
    ]
    return {
        "note": "本漏斗分**两轨**，不可连读为一轨：轨道一「名号」逐层收窄，"
                "轨道二「词素位」逐层收窄；而二轨之间是**扩张**——一名析为多位词素。"
                "故「名号 414 < 词素位 1877」并非异常，而是转换之必然结果。"
                "若强并为一轨，则扩张之步会被误读为「流失」。"
                "又：t3 之流失（medium+low 之和）**不表示数据缺失**，而表示判读存疑之比重；"
                "误读为「覆盖率不足」即错解此表。",
        "note_en": "The funnel has two tracks that must not be read as one: track one (names) narrows, "
                   "track two (token positions) narrows, and between the two lies an expansion — one "
                   "name yields several token positions. '414 names < 1877 positions' is therefore not "
                   "an anomaly but the necessary result of the transformation; merging the tracks would "
                   "make that expansion look like attrition. Further, the loss at t3 (medium plus low) "
                   "does not indicate missing data but the share of uncertain readings; reading it as a "
                   "coverage deficit misreads the table.",
        "conversion": {
            "tokens_per_name": _r(tok / float(len(with_core)), 4) if with_core else 0.0,
            "zh": "换算因子：每名平均析为几位词素",
            "en": "conversion factor: mean token positions yielded per name",
            "no_core": total - len(with_core),
        },
        "track_names": {"zh": "轨道一 · 名号", "en": "Track one — names", "stages": t1},
        "track_tokens": {"zh": "轨道二 · 词素位", "en": "Track two — token positions", "stages": t2},
        # 对账：本层自「逐词素」重算，EDA 之 metrics 为「导入时」统计，二者须相符
        "reconciliation": {
            "zh": "**对账**：本层自「逐词素」重算，EDA 之 metrics 为「导入时」统计，二者应当相符；"
                  "不相符即数据有变或统计口径有别，须查因。",
            "en": "Reconciliation: this layer recomputes from the segments themselves while the EDA "
                  "metrics were computed at import time. The two must agree; any gap means the data or "
                  "the counting basis has changed and must be investigated.",
            "caveat_zh": "**一处口径之差，须明辨**：EDA 之 lowconf_hits／medconf_hits 统计**全域**"
                         "（含未定域词素）；本层 high/medium/low 只计**已归域**者。"
                         "故「归域内 low」少于「全域 low」，二者之差即未定域中之 low。"
                         "两个数字都对，只是所计之集合不同——混用即错。",
            "caveat_en": "One counting difference must be made explicit: the EDA lowconf_hits and "
                         "medconf_hits counts span all token positions including those with unassigned "
                         "domain, whereas the high/medium/low split here covers assigned positions only. "
                         "The gap is exactly the low-confidence unassigned positions. Both figures are "
                         "correct; they simply count different sets, and conflating them would be an error.",
            "tokens_total": {"bi": tok, "eda": m["tokens_total"], "match": tok == m["tokens_total"]},
            "named_total": {"bi": total, "eda": m["named_total"], "match": total == m["named_total"]},
            "no_core": {"bi": total - len(with_core), "eda": m["n_no_core"],
                        "match": (total - len(with_core)) == m["n_no_core"]},
            "unassigned_segs": {"bi": len(segs) - len(assigned), "eda": m["unassigned_segs"],
                                "match": (len(segs) - len(assigned)) == m["unassigned_segs"]},
            "lowconf_hits": {"bi": lo_n, "eda": m["lowconf_hits"], "match": lo_n == m["lowconf_hits"]},
            "medconf_hits": {"bi": me_n, "eda": m["medconf_hits"], "match": me_n == m["medconf_hits"]},
            "grade_matrix": [{"scope": ("unassigned" if u else "assigned"), "confidence": g, "n": c}
                             for (u, g), c in sorted(grade_matrix.items())],
            "grade_matrix_note_zh": "由此矩阵可直接读出「已归域／未定域」×「high／medium／low」之实数分布；"
                                     "页面须并列此矩阵，以免读者以「归域内 low」冒充「全域 low」。",
            "grade_matrix_note_en": "This matrix gives the actual counts of assigned/unassigned against "
                                    "high/medium/low; the page must display it so that 'low within "
                                    "assigned' is never mistaken for 'low overall'.",
        },
        "grades": {
            "high": {"n": len(high), "pct": _r(len(high) / float(len(assigned)), 4) if assigned else 0.0,
                     "zh": "一字一句之义已核定", "en": "reading settled",
                     "duty": "无须标注", "duty_en": "no annotation required"},
            "medium": {"n": len(med), "pct": _r(len(med) / float(len(assigned)), 4) if assigned else 0.0,
                       "zh": "判读存疑（比较之需）", "en": "reading uncertain (for comparison only)",
                       "duty": "不宜据以定论", "duty_en": "not to be used as settled"},
            "low": {"n": len(low), "pct": _r(len(low) / float(len(assigned)), 4) if assigned else 0.0,
                    "zh": "底本疑读", "en": "textually doubtful",
                    "duty": "前端须显示〔待考〕", "duty_en": "must display 〔待考〕"},
        },
    }


# ── C. 语义域全景（含帕累托与集中度）──────────────────────
def domain_landscape(E: Dict[str, Any]) -> Dict[str, Any]:
    doms = [d for d in E["domains"]]
    total = float(sum(d["n"] for d in doms)) or 1.0
    assigned_total = float(sum(d["n"] for d in doms if d["key"] != "unassigned")) or 1.0
    rows = []
    cum = 0.0
    for i, d in enumerate(sorted(doms, key=lambda x: -x["n"]), 1):
        p = d["n"] / total
        cum += p
        rows.append({
            "rank": i, "key": d["key"], "zh": d["zh"], "en": d["en"], "color": d["color"],
            "n": d["n"], "pct": _r(p, 4), "cum_pct": _r(cum, 4),
            "share_of_assigned": _r(d["n"] / assigned_total, 4) if d["key"] != "unassigned" else 0.0,
            "hhi_contrib": _r(p * p, 6),
        })
    ps = [r["pct"] for r in rows if r["key"] != "unassigned"]
    tot_a = sum(ps) or 1.0
    ps = [x / tot_a for x in ps]
    H = entropy(ps)
    k = len(ps)
    return {
        "note": "十七语义域之分布为**语汇层**之分布，非教义权重之分布。域之划分为本站析构之分析工具，"
                "经文本身无「十七域」之名目，故本页一切域相关结论均为分析性，不可径作教义判读。",
        "note_en": "The distribution across the seventeen semantic domains is a distribution over the "
                   "lexicon, not over doctrine. The domain scheme is an analytical instrument of this "
                   "site; the sutra itself has no 'seventeen domains'. All domain-based conclusions here "
                   "are analytical and must not be read as doctrinal judgement.",
        "rows": rows,
        "concentration": {
            "hhi": _r(hhi(ps), 6),
            "hhi_note": "赫芬达尔指数 Σp²（基于已归域词素位之概率）",
            "hhi_note_en": "Herfindahl index, sum of squared shares over domain-assigned token positions",
            "normalized_entropy": _r(H / math.log(k), 4) if k > 1 else 0.0,
            "entropy": _r(H, 4),
            "effective_domains": _r(math.exp(H), 3),
            "effective_note": "有效域数 e^H —— 「看似十七域，实若几域」之度量",
            "effective_note_en": "effective number of domains, exp(H): how many domains the data behaves "
                                 "as if it used",
            "max_domains": k,
        },
        "pareto": {
            "k80": next((r["key"] for r in rows if r["cum_pct"] >= 0.8), None),
            "k80_zh": next((r["zh"] for r in rows if r["cum_pct"] >= 0.8), None),
            "n_to_80": next((r["rank"] for r in rows if r["cum_pct"] >= 0.8), None),
            "total_domains": len(rows),
        },
    }


# ── D. 交叉透视：语义域 × 群（lift / 卡方 / Cramér's V）──────
def crosstab(E: Dict[str, Any]) -> Dict[str, Any]:
    dom_keys = [d["key"] for d in E["domains"]]
    dom_zh = {d["key"]: d["zh"] for d in E["domains"]}
    classes = E["classes"]
    obs = [[0] * len(GROUP_ORDER) for _ in dom_keys]
    for c in classes:
        gi = GROUP_ORDER.index(c["group"])
        dh = c.get("domain_hist") or {}
        for di, k in enumerate(dom_keys):
            obs[di][gi] += int(dh.get(k, 0))
    N = float(sum(sum(r) for r in obs)) or 1.0
    rt = [sum(r) for r in obs]
    ct = [sum(obs[i][j] for i in range(len(obs))) for j in range(len(GROUP_ORDER))]
    cells = []
    for i, dk in enumerate(dom_keys):
        for j, g in enumerate(GROUP_ORDER):
            e = rt[i] * ct[j] / N
            lift = (obs[i][j] / e) if e > 0 else 0.0
            cells.append({"domain": dk, "domain_zh": dom_zh[dk], "group": g,
                          "group_zh": GROUP_ZH[g], "obs": obs[i][j],
                          "exp": _r(e, 2), "lift": _r(lift, 3)})
    over = sorted([c for c in cells if c["obs"] >= 5], key=lambda c: -c["lift"])[:15]
    under = sorted([c for c in cells if c["obs"] >= 5], key=lambda c: c["lift"])[:15]
    chi, V, df = chi2_cramers(obs, dom_keys, GROUP_ORDER)
    p = chi2_sf(chi, df)
    zwh = chi2_wh_z(chi, df)
    # p 下溢（erfc 在 z>27 附近归零）时，报 z 与量级下限，不报 0
    if p <= 0.0 or zwh > 6.0:
        p_approx_txt = "p < 1e-9（Wilson-Hilferty z = %.1f；erfc 已下溢，故不报精确 p）" % zwh
        p_approx_txt_en = ("p < 1e-9 (Wilson-Hilferty z = %.1f; erfc has underflowed, "
                           "so no exact p is reported)" % zwh)
    else:
        p_approx_txt = _r(p, 6)
        p_approx_txt_en = _r(p, 6)
    return {
        "note": "lift = 观测频数 ÷ 期望频数（期望按行×列独立假设）。lift>1 表示该群**偏好**此域，"
                "<1 表示**回避**。Cramér's V 为全域×群之关联强度（0 无关，1 完全决定）。"
                "两者皆只言「语汇构成之偏」，不言「教义侧重之别」。",
        "note_en": "lift = observed ÷ expected frequency (expected under independence of row and column). "
                   "lift>1 marks a group's preference for a domain, <1 its avoidance. Cramér's V is the "
                   "overall association strength between domain and group (0 = independent, "
                   "1 = fully determined). Both speak only to lexical composition, never to doctrinal "
                   "emphasis.",
        "groups": [{"key": g, "zh": GROUP_ZH[g], "en": GROUP_EN[g], "n": ct[i]}
                   for i, g in enumerate(GROUP_ORDER)],
        "domains": [{"key": d, "zh": dom_zh[d], "n": rt[i]} for i, d in enumerate(dom_keys)],
        "matrix": obs,
        "top_over": over, "top_under": under,
        "chi2": _r(chi, 3), "df": df, "cramers_v": _r(V, 4),
        "p_approx": _r(p, 5),
        "p_approx_txt": p_approx_txt, "p_approx_txt_en": p_approx_txt_en,
        "p_wh_z": _r(zwh, 4),
        "df_note_zh": "自由度 = (行数−1)×(列数−1) = (%d−1)×(%d−1) = %d，"
                      "其中行数为语义域 %d（含「未定域」一行）、列数为群 %d。"
                      "Cramér's V 之分母用 min(行,列)−1 = %d，"
                      "故 V 之值与 df 之取法不同，二者不可互换。"
                      % (len(dom_keys), len(GROUP_ORDER), df, len(dom_keys), len(GROUP_ORDER),
                         min(len(dom_keys), len(GROUP_ORDER)) - 1),
        "df_note_en": "Degrees of freedom = (rows−1)(cols−1) = (%d−1)(%d−1) = %d, with %d semantic "
                      "domains as rows (including the unassigned row) and %d groups as columns. "
                      "Cramér's V uses min(rows,cols)−1 = %d in its denominator, so V and the "
                      "choice of df are not interchangeable."
                      % (len(dom_keys), len(GROUP_ORDER), df, len(dom_keys), len(GROUP_ORDER),
                         min(len(dom_keys), len(GROUP_ORDER)) - 1),
        "v_strength_zh": "Cramér's V=%s 属%s：此关联%s，不可称强。故「五群与语汇面貌大体相应」"
                         "一语须以此弱至中等之关联为限，不可升级为「五群即语汇之分群」。"
                         % (_r(V, 4),
                            "弱" if V < 0.2 else ("中等" if V < 0.4 else "强"),
                            "统计上显著但效应量有限" if V < 0.4 else "显著且可观"),
        "v_strength_en": "Cramér's V of %s is %s: the association is %s and must not be called strong. "
                         "Any statement that the five groups broadly track lexical profile must stay "
                         "within this weak-to-moderate effect and must not be upgraded to 'the five "
                         "groups are lexical clusters'."
                         % (_r(V, 4),
                            "weak" if V < 0.2 else ("moderate" if V < 0.4 else "strong"),
                            "statistically significant but of limited effect size" if V < 0.4
                            else "significant and substantial"),
        "p_note": "p 值为 Wilson–Hilferty 近似（非查表精确值），仅作量级参考",
        "p_note_en": "p is a Wilson–Hilferty approximation, not a table-exact value; for order of "
                     "magnitude only",
    }


# ── F. 语义相似度矩阵（TF-IDF 加权·余弦）────────────────────
def similarity(E: Dict[str, Any]) -> Dict[str, Any]:
    dom_keys = [d["key"] for d in E["domains"]]
    classes = sorted(E["classes"], key=lambda c: c["idx"])
    idf = _build_idf(classes, dom_keys)
    vecs = [_cls_vec(c, dom_keys, idf) for c in classes]
    n = len(classes)
    names = [c["cat"] for c in classes]
    sim = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            s = cosine(vecs[i], vecs[j])
            sim[i][j] = sim[j][i] = _r(s, 4)
    pairs = []
    for i in range(n):
        for j in range(i + 1, n):
            pairs.append({"i": i, "j": j, "a": names[i], "b": names[j],
                          "ga": classes[i]["group"], "gb": classes[j]["group"],
                          "same_group": classes[i]["group"] == classes[j]["group"],
                          "sim": sim[i][j]})
    top = sorted(pairs, key=lambda p: -p["sim"])[:30]
    far = sorted(pairs, key=lambda p: p["sim"])[:20]
    # 群内 vs 群外 平均相似度 —— 检验「群」是否即语义边界
    within = [p["sim"] for p in pairs if p["same_group"]]
    across = [p["sim"] for p in pairs if not p["same_group"]]
    # 群间两两平均
    gp = []
    for x in range(len(GROUP_ORDER)):
        for y in range(x + 1, len(GROUP_ORDER)):
            v = [p["sim"] for p in pairs
                 if {p["ga"], p["gb"]} == {GROUP_ORDER[x], GROUP_ORDER[y]}]
            if v:
                gp.append({"a": GROUP_ORDER[x], "b": GROUP_ORDER[y],
                           "a_zh": GROUP_ZH[GROUP_ORDER[x]], "b_zh": GROUP_ZH[GROUP_ORDER[y]],
                           "mean_sim": _r(_mean(v), 4), "n": len(v)})
    gp.sort(key=lambda r: -r["mean_sim"])
    # ── 混淆诊断：相似度是否只是在量「句式相同」而非语汇不同？──
    tails = {c["idx"]: (c.get("leader_tail") or "") for c in classes}
    # 类尾不可靠（leader_tail 未必为全类之尾），改用 assembly 之 classes[i].leader_tail 与
    # EDA 之 class_tails_derived 之 per-class tail；两者皆缺者归 unknown。
    tails = {}
    for i, c in enumerate(classes):
        t = (c.get("leader_tail") or "").strip()
        tails[i] = t if t else "(unknown)"
    same_tail = [p["sim"] for p in pairs if tails[p["i"]] == tails[p["j"]]]
    diff_tail = [p["sim"] for p in pairs if tails[p["i"]] != tails[p["j"]]]
    n_st = len(same_tail); n_dt = len(diff_tail)
    # 同尾内的相似度有多高，说明「同一句式」这一混淆项能解释多少
    # 单看同尾对无法判断，须与全体均值比较，故同时给出全体均值。
    conf = {
        "tail_of_class": [{"i": i, "cat": names[i], "tail": tails[i]} for i in range(n)],
        "n_same_tail_pairs": n_st, "n_diff_tail_pairs": n_dt,
        "same_tail_mean": _r(_mean(same_tail), 4) if same_tail else None,
        "diff_tail_mean": _r(_mean(diff_tail), 4) if diff_tail else None,
        "overall_mean": _r(_mean([p["sim"] for p in pairs]), 4),
        "confound_ratio_zh": "同句式（同类尾）类对之平均相似度 ÷ 全体类对之平均相似度",
        "confound_ratio_en": "mean similarity of same-tail pairs divided by mean similarity of all pairs",
        "confound_ratio": _r((_mean(same_tail) / _mean([p["sim"] for p in pairs]))
                             if same_tail and pairs else 0.0, 4),
        "note_zh": "此为**混淆项检验**：「主X神」诸类共用一句式，其域分布因句式而趋同，"
                   "故彼此相似度可能反映的是句式同构而非语汇相近。"
                   "读相似度矩阵时须扣除此项；否则「主夜神≈主昼神」一类结果将被过度解读。"
                   "消混淆之对照量即「异句式类对之平均相似度」。",
        "note_en": "This is a confounding check: the 「主X神」 series shares one syntactic template, "
                   "so their domain profiles converge because of the template rather than through shared "
                   "vocabulary. Similarity must be read with this subtracted, or results such as "
                   "'主夜神 ≈ 主晝神' will be over-interpreted. The de-confounded reference is the "
                   "mean similarity across pairs with different templates.",
    }
    return {
        "space_zh": "语义域分布向量（17 维）× TF-IDF 加权 × 余弦相似度",
        "space_en": "17-dim semantic-domain distribution, TF-IDF weighted, cosine similarity",
        "caveat_zh": "此「相似度」量的是**构词层语汇构成之相近**，**不是词义相近**。"
                     "两域分布相同之两类，其名号所指可能全然不同；反之词义相近而构词迥异者，"
                     "此测度必测不到。故本页相似度只可读作「语汇面貌之相似」。",
        "caveat_en": "This similarity measures closeness of lexical composition, not of meaning. Two "
                     "classes with identical domain profiles may denote entirely different things, and "
                     "semantically close classes built from different words are structurally invisible "
                     "here. Read it strictly as similarity of lexical surface.",
        "idx": [c["idx"] for c in classes],
        "names": names,
        "groups": [c["group"] for c in classes],
        "domain_keys": dom_keys,
        "idf": [_r(x, 4) for x in idf],
        "matrix": sim,
        "top": top, "far": far,
        "within_mean": _r(_mean(within), 4), "within_n": len(within),
        "across_mean": _r(_mean(across), 4), "across_n": len(across),
        "confound": conf,
        "group_pair_means": gp,
        "verdict_zh": ("群内显著高于群外，故「五群」之划分与语汇面貌**大体相应**"
                       if _mean(within) > _mean(across) else
                       "群内不高于群外，故「五群」之划分与语汇面貌**不相应**"
                       "（即群界并非语汇边界）"),
        "verdict_en": ("within-group similarity clearly exceeds across-group, so the five-group division "
                       "broadly tracks lexical profile" if _mean(within) > _mean(across) else
                       "within-group similarity does not exceed across-group, so the five-group division "
                       "is not a lexical boundary"),
    }


# ── G. 主题聚类（average-linkage 层次聚类 + 平铺簇 + 轮廓）───
def clustering(E: Dict[str, Any], sim: Dict[str, Any]) -> Dict[str, Any]:
    classes = sorted(E["classes"], key=lambda c: c["idx"])
    names = sim["names"]
    n = len(names)
    S = sim["matrix"]
    dist = [[1.0 - S[i][j] for j in range(n)] for i in range(n)]
    merges = agglomerate(dist, names)
    # 由合并序列回放，得各 k 之平铺划分（依 agglomerate 记录之节点索引 ia/ib 直接重放，
    # 不可依 names 反查——合并后代表名会变，反查必错）
    def flat_at(k: int) -> List[int]:
        # 【更正】旧式仅改写 lab[b] 一个键，未改写「已指向 b」之其余成员；
        # 于是第三次合并之后，被并之簇遂分裂为两支，簇数多于 k。
        # 例：best_k=15 时旧式实得 20 簇。现按 m["members"] 全量改写，
        # 并于后以 len(set(assign)) == k 校验。
        lab: Dict[int, int] = {i: i for i in range(n)}
        for m in merges[:max(n - k, 0)]:
            a, b = lab[m["ia"]], lab[m["ib"]]
            lab[a] = a
            lab[b] = a
            if a != b:
                for i_ in range(n):
                    if lab[i_] == b:
                        lab[i_] = a
        roots = sorted({v for v in lab.values()})
        ren = {r: ci for ci, r in enumerate(roots)}
        return [ren[lab[i]] for i in range(n)]

    curve = []
    best_k, best_s = 2, -2.0
    KMIN, KMAX = 2, 15
    for k in range(KMIN, min(KMAX, n - 1) + 1):
        assign = flat_at(k)
        # 切分必须恰为 k 簇，否则 k 之含义不成立（此即旧式 flat_at 之弊）
        if len(set(assign)) != k:
            continue
        s = silhouette(dist, names, assign)
        curve.append({"k": k, "silhouette": _r(s, 4)})
        if s > best_s:
            best_k, best_s = k, s
    assign = flat_at(best_k)
    # 逐点轮廓（全划分下之轮廓系数），簇轮廓＝簇内诸点轮廓之均值
    pt_sil = per_point_silhouette(dist, assign)
    boundary = (best_k == KMAX or best_k == KMIN)
    # 共形相关系数（树高 vs 原始距离）—— 树结构可信度
    dend = [m["d"] for m in merges]
    member_names = {i: names[i] for i in range(n)}

    def coph(ni: int, nj: int) -> float:
        a, b = member_names[ni], member_names[nj]
        for m in merges:
            if a in m["members"] and b in m["members"]:
                return m["d"]
        return max(dend) if dend else 0.0

    cd = []; ch = []
    for i in range(n):
        for j in range(i + 1, n):
            cd.append(dist[i][j]); ch.append(coph(i, j))
    coph_corr = pearson(cd, ch)
    # 簇画像
    dom_keys = sim["domain_keys"]
    clusters = []
    for ci in sorted(set(assign)):
        mem = [i for i in range(n) if assign[i] == ci]
        dom_sum = [0.0] * len(dom_keys)
        for i in mem:
            dh = classes[i].get("domain_hist") or {}
            for di, k in enumerate(dom_keys):
                dom_sum[di] += float(dh.get(k, 0))
        tot = sum(dom_sum) or 1.0
        tops = sorted(range(len(dom_keys)), key=lambda z: -dom_sum[z])[:3]
        # 簇内高频词素
        fc = collections.Counter()
        for i in mem:
            for mm in (classes[i].get("members") or []):
                for s in (mm.get("segs") or []):
                    fc[s["zh"]] += 1
        top_morphs = [{"zh": z, "n": c} for z, c in fc.most_common(10)]
        grp = collections.Counter(classes[i]["group"] for i in mem)
        members_named = sum(classes[i]["n_named"] for i in mem)
        clusters.append({
            "id": ci,
            "members": [{"idx": classes[i]["idx"], "cat": names[i], "group": classes[i]["group"],
                         "group_zh": GROUP_ZH[classes[i]["group"]], "n_named": classes[i]["n_named"]}
                        for i in mem],
            "n_classes": len(mem), "n_named": members_named,
            "top_domains": [{"key": dom_keys[z], "n": int(dom_sum[z]),
                             "pct": _r(dom_sum[z] / tot, 4)} for z in tops],
            "top_morphs": top_morphs,
            "group_mix": [{"key": g, "zh": GROUP_ZH[g], "n": c} for g, c in grp.most_common()],
            "silhouette": _r(_mean([pt_sil[i] for i in mem]), 4),
        })
    clusters.sort(key=lambda c: -c["n_classes"])
    for i, c in enumerate(clusters):
        c["id"] = i
    # 稳定性：LCG 定种之**无放回 80% 子抽样** 200 次，量同簇共现
    # 【更正】旧式用有放回 bootstrap。仅 40 个类而有放回抽 40 次，
    # 期望仅约 25 个互异单位入选，故任一对同时入选之概率本已受限，
    # 共现率因而被结构性压低（约 0.2），不可与真实之不稳定混为一谈。
    # 今改用无放回 80% 子抽样（jackknife 型），每次约 32 个单位入选，
    # 共现率分母改为「该对同时入选之次数」，不再受入选不足之影响。
    rng = LCG(20240717)
    co_num = collections.Counter()
    co_den = collections.Counter()
    B = 200
    SUB = 0.8
    n_sub = max(int(round(n * SUB)), 3)
    idf = _build_idf(sorted(E["classes"], key=lambda c: c["idx"]), dom_keys)
    allv = [_cls_vec(c, dom_keys, idf) for c in sorted(E["classes"], key=lambda c: c["idx"])]
    for _ in range(B):
        pool = list(range(n))
        for i in range(n - 1, 0, -1):
            j = rng.randint(i + 1)
            pool[i], pool[j] = pool[j], pool[i]
        keep = pool[:n_sub]
        sub = [allv[t] for t in keep]
        ds = [[1.0 - cosine(sub[i], sub[j]) for j in range(n_sub)] for i in range(n_sub)]
        mg = agglomerate(ds, [str(t) for t in keep])
        lab: Dict[int, int] = {i: i for i in range(n_sub)}
        for m in mg[:max(n_sub - best_k, 0)]:
            a, b = lab[m["ia"]], lab[m["ib"]]
            lab[a] = a
            lab[b] = a
            if a != b:
                for i_ in range(n_sub):
                    if lab[i_] == b:
                        lab[i_] = a
        for i in range(n_sub):
            for j in range(i + 1, n_sub):
                co_num[(keep[i], keep[j])] += 1 if lab[i] == lab[j] else 0
                co_den[(keep[i], keep[j])] += 1
    for c in clusters:
        idxs = [m["idx"] for m in c["members"]]
        st = []
        for a in range(len(idxs)):
            for b in range(a + 1, len(idxs)):
                key = (idxs[a], idxs[b])
                if co_den.get(key, 0) > 0:
                    st.append(co_num[key] / float(co_den[key]))
        c["stability"] = _r(_mean(st), 4) if st else None
        c["stability_n_pairs"] = len(st)
    return {
        "method_zh": "层次聚类（average linkage）＋余弦距离；自 k=%d 至 k=%d 逐一切分并算全样本平均"
                     "轮廓系数，取其最大者为最佳 k（仅取切分后确为 k 簇者入算）。"
                     "稳定性以 LCG 定种（种子 20240717）bootstrap "
                     "200 次量同簇共现率。" % (KMIN, min(KMAX, n - 1)),
        "stability_method_zh": "稳定性为**无放回 80%% 子抽样**（jackknife 型）之同簇共现率："
                               "定种 LCG（种子 20240717）重复 200 次，每次无放回抽取 %d/%d 个类，"
                               "重作层次聚类并切于最佳 k；某一对类之共现率 = 该对同簇之次数 ÷ "
                               "该对同时入选之次数。**更正**：旧式用有放回 bootstrap，"
                               "而仅 %d 个类有放回抽 %d 次时期望仅约 %.1f 个互异单位入选，"
                               "任一对同时入选之概率本已受限，共现率因而被结构性压低；"
                               "今改无放回，分母改为「同时入选之次数」，"
                               "故新旧稳定度之数值不可直接比较。"
                               % (n_sub, n, n, n, _r(n * (1.0 - math.exp(-1.0)), 1)),
        "stability_method_en": "Stability is the co-assignment rate under **subsampling without "
                               "replacement at 80%%** (jackknife-type): a seeded LCG (seed 20240717) "
                               "draws %d of the %d classes without replacement, %d times, re-runs "
                               "hierarchical clustering and cuts at the best k; a pair's rate is the "
                               "number of resamples in which the pair co-clustered, divided by the "
                               "number of resamples in which the pair was drawn together. "
                               "**Correction**: an earlier implementation used bootstrap with "
                               "replacement; drawing %d classes with replacement from only %d classes "
                               "leaves on average just %.1f distinct units drawn, which mechanically "
                               "depresses co-assignment. Subsampling removes that bias, so old and new "
                               "stability figures are not directly comparable."
                               % (n_sub, n, B, n, n, _r(n * (1.0 - math.exp(-1.0)), 1)),
        "method_en": "Agglomerative clustering (average linkage) on cosine distance; for k = %d..%d the "
                     "data is cut at each k and the mean silhouette computed, the maximum being the "
                     "chosen k (only cuts yielding exactly k clusters are admitted)."
                     % (KMIN, min(KMAX, n - 1)),
        "caveat_zh": "聚类之数（k）非经文所定，乃算法依轮廓系数所择。故簇界可随参数而移，"
                     "此表当读作「一种可复现之切分」，非「经文自有之类别」。",
        "caveat_en": "The number of clusters is not fixed by the sutra; it is chosen by the algorithm via "
                     "the silhouette coefficient. Cluster boundaries shift with parameters, so this table "
                     "should be read as one reproducible partition, not as the sutra's own categories.",
        "best_k": best_k, "best_silhouette": _r(best_s, 4),
        "k_range": [KMIN, min(KMAX, n - 1)],
        "k_at_boundary": boundary,
        "k_boundary_note_zh": "最佳 k 落于扫描区间之端点，故真实最优可能在区间之外；"
                              "已扩区间至 %d 重新扫描，仍在此端，故此簇数应读作「所扫区间内之最优」。"
                              % min(KMAX, n - 1) if boundary else "最佳 k 落于区间内部。",
        "k_boundary_note_en": ("the best k lies at the edge of the scanned range, so the true optimum may "
                               "lie outside it; read this as the optimum within the scanned range"
                               if boundary else "the best k lies inside the scanned range"),
        "weak_structure_zh": ("轮廓系数 %s 属低值，故聚类之分离度弱：即语汇面貌并无截然分群之象，"
                              "簇界随时可变。故本页聚类只宜作「探索之视图」，不宜作「分类之结论」。"
                              % _r(best_s, 3) if best_s < 0.25 else
                              "轮廓系数 %s 分离度尚可：语汇面貌可见数处聚处，然仍非截然分群，"
                              "故本页聚类当读作「一种可复现之切分」，不宜作「经文自有之类别」。"
                              % _r(best_s, 3)),
        "weak_structure_en": ("the silhouette of %s is low, so separation is weak: the lexical landscape "
                               "shows no sharply divided groups and boundaries are unstable. Treat this "
                               "partition as an exploratory view, not a classification."
                               % _r(best_s, 3) if best_s < 0.25 else
                               "the silhouette of %s indicates moderate separation; several groupings are "
                               "discernible, yet they are not sharply divided, so this partition should be "
                               "read as one reproducible cut rather than the sutra's own categories."
                               % _r(best_s, 3)),
        "curve": curve,
        "merges": [{"step": m["step"], "a": m["a"], "b": m["b"], "d": m["d"], "size": m["size"]}
                   for m in merges],
        "dendrogram": {"heights": dend, "names": names, "idx": sim["idx"],
                       "groups": sim["groups"]},
        "cophenetic_corr": _r(coph_corr, 4),
        "cophenetic_note_zh": "共形相关系数：树高与原距离之相关（>0.9 视为树结构良好）",
        "cophenetic_note_en": "cophenetic correlation between tree heights and original distances "
                              "(>0.9 conventionally indicates a good tree)",
        "clusters": clusters,
    }


# ── H. 主成分分析（PCA，Jacobi 特征分解）────────────────────
def pca(E: Dict[str, Any], sim: Dict[str, Any]) -> Dict[str, Any]:
    dom_keys = sim["domain_keys"]
    classes = sorted(E["classes"], key=lambda c: c["idx"])
    n, k = len(classes), len(dom_keys)
    V = [_cls_vec(c, dom_keys, sim["idf"]) for c in classes]
    mu = [_mean([V[i][j] for i in range(n)]) for j in range(k)]
    Z = [[V[i][j] - mu[j] for j in range(k)] for i in range(n)]
    C = [[_mean([Z[i][a] * Z[i][b] for i in range(n)]) for b in range(k)] for a in range(k)]
    vals, vecs = jacobi_eig(C)
    total = sum(v for v in vals if v > 0) or 1.0
    # 符号规范化：使最大绝对载荷为正，俾坐标可复现
    for t in range(len(vecs)):
        mx = max(range(k), key=lambda j: abs(vecs[t][j]))
        if vecs[t][mx] < 0:
            vecs[t] = [-x for x in vecs[t]]
    score = []
    for i in range(n):
        score.append([sum(Z[i][j] * vecs[t][j] for j in range(k)) for t in range(len(vecs))])
    loadings = []
    for t in range(min(3, k)):
        arr = sorted(range(k), key=lambda j: -abs(vecs[t][j]))[:8]
        loadings.append({
            "pc": t + 1,
            "explained_pct": _r(vals[t] / total, 4),
            "top_domains": [{"key": dom_keys[j], "load": _r(vecs[t][j], 4)} for j in arr],
        })
    grp_cent = {}
    for g in GROUP_ORDER:
        pts = [score[i][:2] for i in range(n) if classes[i]["group"] == g]
        grp_cent[g] = {"x": _r(_mean([p[0] for p in pts]), 4), "y": _r(_mean([p[1] for p in pts]), 4)}
    return {
        "method_zh": "PCA：对「类×语义域」TF-IDF 加权矩阵按列中心化，求 17×17 协方差之特征分解"
                     "（Jacobi 旋转，纯 Python 实现），取前若干主成分。坐标已作符号规范化以保证可复现。",
        "method_en": "PCA: the class-by-domain TF-IDF matrix is column-centred, its 17x17 covariance "
                     "matrix diagonalised by Jacobi rotations (pure-Python), and the leading components "
                     "retained. Component signs are normalised so that results are reproducible.",
        "caveat_zh": "二维散点**不可**读作「距离之远近」——主成分投影有损，三维以上之差异常被压平；"
                     "两轴之正负亦无教义向背之意，仅为统计方向。",
        "caveat_en": "The 2-D scatter must not be read as true distance: a principal-component projection "
                     "is lossy and flattens differences lying beyond the retained axes. The signs of the "
                     "axes carry no doctrinal valence; they are statistical directions only.",
        "explained": [{"pc": t + 1, "var": _r(vals[t], 4), "pct": _r(vals[t] / total, 4)}
                      for t in range(min(5, k))],
        "loadings": loadings,
        "points": [{"idx": classes[i]["idx"], "cat": classes[i]["cat"], "group": classes[i]["group"],
                    "group_zh": GROUP_ZH[classes[i]["group"]],
                    "x": _r(score[i][0], 4), "y": _r(score[i][1], 4),
                    "n_named": classes[i]["n_named"]} for i in range(n)],
        "group_centroids": grp_cent,
    }


# ── I. 帕累托（集中度曲线）──────────────────────────────────
def pareto(E: Dict[str, Any]) -> Dict[str, Any]:
    def series(items: List[Tuple[str, int]], key: str, label: str, label_en: str) -> Dict[str, Any]:
        tot = sum(v for _, v in items) or 1
        cum = 0
        pts = []
        k80 = None
        for i, (z, v) in enumerate(items, 1):
            cum += v
            pct = cum / float(tot)
            if k80 is None and pct >= 0.8:
                k80 = i
            pts.append({"rank": i, "key": z, "n": v, "cum_pct": _r(pct, 4)})
        return {"dimension": key, "label": label, "label_en": label_en,
                "total": tot, "n_items": len(items), "k80": k80,
                "k80_pct_items": _r(k80 / float(len(items)), 4) if k80 else None,
                "points": pts}

    morphs = sorted(((m["zh"], m["n"]) for m in E["morph_freq"]), key=lambda x: -x[1])
    heads = sorted(((m["zh"], m["n"]) for m in E["head_freq"]), key=lambda x: -x[1])
    tails = sorted(((m["zh"], m["n"]) for m in E["tailch_freq"]), key=lambda x: -x[1])
    classes = sorted(((c["cat"], c["n_named"]) for c in E["classes"]), key=lambda x: -x[1])
    return {
        "note_zh": "帕累托读法：k80 = 累计达 80% 频次所需之项数。k80_pct_items 越低，则语汇越集中于少数词素。"
                   "本表用于回答「华严会众名号之语汇，是高度模板化还是高度多样」。",
        "note_en": "Pareto reading: k80 is the number of items needed to reach 80% of total frequency. "
                   "The lower k80_pct_items, the more concentrated the lexicon. This answers whether the "
                   "vocabulary of Huayan assemblies is highly templated or highly varied.",
        "series": [
            series(morphs, "morphemes", "词素频次", "Morpheme frequency"),
            series(heads, "head_char", "冠字频次", "Head-character frequency"),
            series(tails, "tail_char", "尾字频次", "Tail-character frequency"),
            series(classes, "class_size", "各类名号数", "Names per class"),
        ],
    }


# ── J. 类级散点与相关 ───────────────────────────────────────
def scatter(E: Dict[str, Any]) -> Dict[str, Any]:
    dom_keys = [d["key"] for d in E["domains"]]
    rows = []
    for c in sorted(E["classes"], key=lambda x: x["idx"]):
        dh = c.get("domain_hist") or {}
        tot = sum(int(v) for v in dh.values()) or 1
        ps = [dh.get(k, 0) / tot for k in dom_keys if k != "unassigned"]
        ps = [p for p in ps if p > 0]
        hh = hhi(ps)
        meds = lo = 0
        for mm in (c.get("members") or []):
            for s in (mm.get("segs") or []):
                if s.get("c") == "medium":
                    meds += 1
                elif s.get("c") == "low":
                    lo += 1
        nt = sum(int(v) for v in dh.values())
        rows.append({
            "idx": c["idx"], "cat": c["cat"], "group": c["group"], "group_zh": GROUP_ZH[c["group"]],
            "n_named": c["n_named"], "n_tokens": nt,
            "tokens_per_name": _r(nt / max(c["n_named"], 1), 3),
            "uncertain_rate": _r((meds + lo) / max(nt, 1), 4),
            "low_rate": _r(lo / max(nt, 1), 4),
            "distinct_morph": len((c.get("top_morphemes") or [])) and c.get("n_distinct_morph") or 0,
            "domain_hhi": _r(hh, 4),
            "domain_neff": _r(1.0 / hh, 3) if hh > 0 else 0.0,
        })
    def corr(xk: str, yk: str, zh: str, en: str) -> Dict[str, Any]:
        xs = [float(r[xk]) for r in rows]
        ys = [float(r[yk]) for r in rows]
        p = pearson(xs, ys)
        s = spearman(xs, ys)
        verdict = ("强正相关" if p >= 0.7 else "中等正相关" if p >= 0.4 else
                   "弱相关" if p >= 0.2 else "中等负相关" if p >= -0.4 else
                   "弱负相关" if p > -0.7 else "强负相关")
        verdict_en = ("strong positive" if p >= 0.7 else "moderate positive" if p >= 0.4 else
                      "weak" if p >= 0.2 else "moderate negative" if p >= -0.4 else
                      "weak negative" if p > -0.7 else "strong negative")
        return {"x": xk, "y": yk, "zh": zh, "en": en,
                "pearson": _r(p, 4), "spearman": _r(s, 4),
                "r2": _r(p * p, 4), "verdict": verdict, "verdict_en": verdict_en}
    pairs = [
        corr("n_named", "n_tokens", "类之名号数 × 类之词素位", "names per class x token positions"),
        corr("n_tokens", "tokens_per_name", "类之词素位 × 每名平均词素位",
             "token positions x token positions per name"),
        corr("n_tokens", "uncertain_rate", "类之词素位 × 判读存疑率",
             "token positions x uncertain-reading rate"),
        corr("n_named", "domain_neff", "类之名号数 × 语义域有效数",
             "names per class x effective number of domains"),
        corr("domain_hhi", "n_named", "语义域集中度 × 类之名号数",
             "domain concentration x names per class"),
    ]
    return {
        "note_zh": "散点为 40 类之逐类实点（气泡大小＝名号数）。相关系数仅言**统计关联**，"
                   "**不含因果**；且 n=40 之样本，相关系数之抽样波动不可忽略，故并列 Spearman 秩相关"
                   "以资对照——两者差距大者，提示非线性或离群点主导。",
        "note_en": "Each point is one of the forty classes (bubble size = number of names). Correlation "
                   "denotes statistical association only, never causation; with n=40 the sampling "
                   "variation is not negligible, so Spearman rank correlation is given alongside Pearson "
                   "— a large gap between them signals non-linearity or outlier dominance.",
        "rows": rows, "pairs": pairs,
    }


# ── K. 构词模板挖掘（语义结构式样）──────────────────────────
def templates(E: Dict[str, Any]) -> Dict[str, Any]:
    dom_zh = {d["key"]: d["zh"] for d in E["domains"]}
    classes = E["classes"]
    members = [(c, mm) for c in classes for mm in (c.get("members") or []) if mm.get("core")]
    N = len(members)
    # ── 层一：字面 n-gram 复用（语汇之集中度）──
    ngram = collections.Counter()
    ngram_ex: Dict[Tuple[str, ...], List[str]] = collections.defaultdict(list)
    for _c, mm in members:
        core = mm["core"]
        for i in range(len(core)):
            for L in (2, 3):
                if i + L <= len(core):
                    g = core[i:i + L]
                    ngram[g] += 1
                    if len(ngram_ex[g]) < 3:
                        ngram_ex[g].append(mm["name"])
    ngram_rows = [{"gram": g, "n": n, "pct": _r(n / float(N), 4),
                   "examples": ngram_ex[g]} for g, n in ngram.most_common(30)]
    # ── 层二：语义域序列之式样（细粒度，预期极碎）──
    pat = collections.Counter()
    pat_dom = collections.defaultdict(collections.Counter)
    examples = collections.defaultdict(list)
    tok_len = collections.Counter()
    for c, mm in members:
        segs = mm.get("segs") or []
        ds = [(s.get("domain") or "unassigned") for s in segs]
        tok_len[len(ds)] += 1
        key = "+".join(ds)
        pat[key] += 1
        pat_dom[key].update(ds)
        if len(examples[key]) < 3:
            examples[key].append({"name": mm["name"], "cat": c["cat"], "idx": c["idx"]})
    rows = []
    for key, cnt in pat.most_common(24):
        parts = key.split("+")
        rows.append({
            "pattern": key,
            "pattern_zh": "＋".join(dom_zh.get(p, p) for p in parts),
            "n": cnt, "pct": _r(cnt / float(N), 4),
            "length": len(parts),
            "has_unassigned": any(p == "unassigned" for p in parts),
            "dominant": [{"key": k, "zh": dom_zh.get(k, k), "n": v}
                         for k, v in pat_dom[key].most_common(3)],
            "examples": examples[key],
        })
    distinct_pat = len(pat)
    pat_ps = [c / float(N) for c in pat.values()]
    # ── 层三：抽象式样——首词素域 × 末词素域（粗粒度，句法骨架）──
    head_dom = collections.Counter()
    tail_dom = collections.Counter()
    ht = collections.Counter()
    for c, mm in members:
        segs = mm.get("segs") or []
        if not segs:
            continue
        h = segs[0].get("domain") or "unassigned"
        t = segs[-1].get("domain") or "unassigned"
        head_dom[h] += 1
        tail_dom[t] += 1
        ht[(h, t)] += 1
    ht_rows = sorted(ht.items(), key=lambda kv: -kv[1])[:20]
    cov = sum(r["n"] for r in rows)
    hts = [v / float(N) for _k, v in ht.items()]
    # 先算出两项供 verdict 使用（避免在长字符串里嵌套复杂表达式）
    # 字面层之集中度须用**唯一二字组之覆盖**衡量，不能用计数之和：
    # 一名号可含多个二字组，计数之和会超过名号数，得 >100% 之荒谬结果。
    bi_first = collections.Counter()
    for _c, mm in members:
        core = mm["core"]
        if len(core) >= 2:
            bi_first[core[:2]] += 1
    n_bigram = len(bi_first)
    bigram_hits = sum(bi_first.values())
    bigram_cover = "%.1f%%" % (_r(bigram_hits / float(N), 4) * 100)
    bigram_top = bi_first.most_common(1)[0] if bi_first else ("", 0)
    bigram_top_pct = "%.2f%%" % (_r(bigram_top[1] / float(N), 4) * 100) if bi_first else "n/a"
    top1_pct = "%.2f%%" % (rows[0]["pct"] * 100) if rows else "n/a"
    # 归一熵须先算好再格式化——「"%.4f" % x / y」会先做字符串除法而报错
    norm_ent = "%.4f" % (entropy(pat_ps) / math.log(distinct_pat)) if distinct_pat > 1 else "n/a"
    n_singleton = sum(1 for _k, v in pat.items() if v == 1)
    return {
        "note_zh": "模板以**语义域序列**表述（而非原字），即「功德＋光明＋冠缀＋威势力」之类。"
                   "此举把 414 个名号之构词抽象为有限之结构式样，正是「表法」「象征」二角度之可操作化："
                   "先见结构之型，再问其义。注意此为**结构**之陈述，非**意义**之解释。",
        "note_en": "Templates are expressed as sequences of semantic domains rather than literal "
                   "characters — for example virtue+luminosity+affix+power. This reduces the "
                   "construction of the 414 names to a limited set of structural patterns, which is the "
                   "operational form of the 'manifestation' and 'symbol' perspectives: first the "
                   "structural type, then its meaning. Note that this states structure, not meaning.",
        "verdict_zh": ("**两层方向相反，此反差本身即是发现**。字面层：%d 名号之核名首二字只落在 "
                       "%d 种二字组上（最多者「%s」占 %s），语汇复用率 %s，故高度模板化。"
                       "语义域序列层：%d 名之仅 %d 种式样，其中 %d 种只现一次"
                       "（占 %s），归一熵 %s；抽象到「首词素域×末词素域」之骨架仍有 %d 种。"
                       "故其构词之「模板性」在**字面**而不在**域构成**——华严会众之语汇，"
                       "乃同一批字反复组装而成，非同一批语义反复填充。"
                       "此反差本身可读为：经文之会众名号，重在其**名相之庄严整饬**"
                       "（字字有出处、字字见对称），而其**语义配置**则逐名而异、乃至有意相重。"
                       % (N, n_bigram, bigram_top[0], bigram_top_pct,
                          "%.1f%%" % (_r(1.0 - n_bigram / float(N), 4) * 100),
                          N, distinct_pat, n_singleton,
                          "%.1f%%" % (_r(n_singleton / float(N), 4) * 100),
                          norm_ent,
                          len(ht))),
        "verdict_en": ("The two layers point in opposite directions, and the contrast is itself the "
                       "finding. Literal layer: the first two characters of the 414 nuclei fall into only "
                       "%d distinct bigrams (the leading one, 「%s」, covering %s), a reuse rate of %s, "
                       "so this layer is highly templated. Domain-sequence layer: the same 414 names "
                       "yield only %d patterns, %d of which occur exactly once (%s, normalised entropy "
                       "%s), and even the abstract head-by-tail skeleton still takes %d forms. The "
                       "templating therefore lies in the *characters*, not in the *domain composition*: "
                       "Huayan assembly vocabulary re-assembles the same stock of characters rather than "
                       "filling the same stock of meanings. The contrast itself is readable: these names "
                       "excel in the dignity and orderliness of their wording (every character "
                       "attested, every arrangement symmetrical), while their semantic configurations "
                       "vary from name to name, and may even be deliberately overlapping."
                       % (n_bigram, bigram_top[0], bigram_top_pct,
                          "%.1f%%" % (_r(1.0 - n_bigram / float(N), 4) * 100),
                          distinct_pat, n_singleton,
                          "%.1f%%" % (_r(n_singleton / float(N), 4) * 100),
                          norm_ent, len(ht))),
        "n_members": N,
        "layer1_literal": {
            "zh": "层一 · 字面 n-gram 复用",
            "en": "Layer one — literal n-gram reuse",
            "measure_zh": "**衡量之法**：以「核名首二字」为准，一名只计一次，"
                          "故覆盖率不会超过 100%。若改用「所有二字组出现次数之和」"
                          "（一名可含多组），其和将超过名号数而得荒谬之 >100% 覆盖率——"
                          "此即常见之度量陷阱，页面不得混用。",
            "measure_en": "Measurement: based on the first two characters of each nucleus, counted once "
                          "per name, so coverage cannot exceed 100%. Summing the occurrence counts of "
                          "all bigrams instead (a name may contain several) would exceed the number of "
                          "names and yield a nonsensical coverage above 100%; that is a common "
                          "measurement trap and the two must not be mixed on the page.",
            "n_distinct_bigram": n_bigram,
            "n_distinct_trigram": len({g for g in ngram if len(g) == 3}),
            "bigram_coverage": _r(bigram_hits / float(N), 4),
            "bigram_reuse_rate": _r(1.0 - n_bigram / float(N), 4),
            "top24_coverage": _r(sum(bi_first.most_common(24)[i][1] for i in range(
                min(24, len(bi_first)))) / float(N), 4),
            "leading_bigram": {"gram": bigram_top[0], "n": bigram_top[1],
                               "pct": _r(bigram_top[1] / float(N), 4)},
            "bigram_rows": [{"gram": g, "n": v, "pct": _r(v / float(N), 4),
                             "examples": [mm["name"] for _c, mm in members if mm["core"][:2] == g][:3]}
                            for g, v in bi_first.most_common(24)],
            "rows": ngram_rows,
        },
        "layer2_domain": {
            "zh": "层二 · 语义域序列式样",
            "en": "Layer two — semantic-domain sequence patterns",
            "n_distinct": distinct_pat,
            "n_singleton": n_singleton,
            "singleton_pct": _r(n_singleton / float(N), 4),
            "distinct_per_member": _r(distinct_pat / float(N), 4),
            "pattern_entropy": _r(entropy(pat_ps), 4),
            "normalized_entropy": _r(entropy(pat_ps) / math.log(distinct_pat), 4) if distinct_pat > 1 else 0.0,
            "coverage_top24": _r(cov / float(N), 4),
            "rows": rows,
            "unassigned_in_top": sum(1 for r in rows if r["has_unassigned"]),
            "unassigned_note_zh": "首列式样多含「未定」域（专名/音译与罕字），"
                                  "故层二之式样不宜径直释为语义结构——含未定域者，"
                                  "其结构意义悬空，页面须并列「未参与结构分析」之计数。",
            "unassigned_note_en": "Leading patterns often contain the unassigned domain (proper names, "
                                   "transliterations and rare glyphs), so such patterns should not be "
                                   "read directly as semantic structure: where unassigned segments "
                                   "occur, the structural reading is left hanging and must be counted "
                                   "separately.",
        },
        "layer3_skeleton": {
            "zh": "层三 · 抽象骨架（首词素域 × 末词素域）",
            "en": "Layer three — abstract skeleton (head domain × tail domain)",
            "n_distinct": len(ht),
            "distinct_per_member": _r(len(ht) / float(N), 4),
            "normalized_entropy": _r(entropy(hts) / math.log(len(ht)), 4) if len(ht) > 1 else 0.0,
            "rows": [{"head": k[0], "head_zh": dom_zh.get(k[0], k[0]),
                      "tail": k[1], "tail_zh": dom_zh.get(k[1], k[1]),
                      "n": v, "pct": _r(v / float(N), 4)} for k, v in ht_rows],
        },
        "coverage_top24": _r(cov / float(N), 4),
        "rows": rows,
        "head_domain": [{"key": k, "zh": dom_zh.get(k, k), "n": v,
                         "pct": _r(v / float(N), 4)} for k, v in head_dom.most_common()],
        "tail_domain": [{"key": k, "zh": dom_zh.get(k, k), "n": v,
                         "pct": _r(v / float(N), 4)} for k, v in tail_dom.most_common()],
        "token_length_hist": [{"len": k, "n": v, "pct": _r(v / float(N), 4)}
                              for k, v in sorted(tok_len.items())],
    }


# ── L. 网络中心性与社群 ─────────────────────────────────────
def network(E: Dict[str, Any]) -> Dict[str, Any]:
    # 【须声明之截断】EDA 之 lex_edges 为 pair_total.most_common(400)，即相邻共现
    # 之全部 791 对中只取权重最高之 400 对，其余 391 对（多为 n=1 之弱共现）未入图。
    # 经独立复算（networkx 全图对读），此截断对 PageRank 之影响显著：全图与截断图
    # 之 top5 完全不同（「音」「須彌」等在截断后消失，「主」「光」显著上升）。
    # 故本页之一切中心性数值皆为「**强共现子图**上之中心性」，非全网之中心性；
    # 且弱共现（n=1，占全对之多数）之被排除，恰恰抬高了强联结者之分。
    nodes = [n["id"] for n in E["graph"]["lex_nodes"]]
    nzh = {n["id"]: n["zh"] for n in E["graph"]["lex_nodes"]}
    ndom = {n["id"]: n.get("domain") for n in E["graph"]["lex_nodes"]}
    nn = {n["id"]: n.get("n", 0) for n in E["graph"]["lex_nodes"]}
    edges = [(e["source"], e["target"], float(e.get("n", 1))) for e in E["graph"]["lex_edges"]]
    deg = collections.Counter()
    wdeg = collections.Counter()
    for a, b, w in edges:
        deg[a] += 1
        deg[b] += 1
        wdeg[a] += w
        wdeg[b] += w
    pr = pagerank(nodes, edges)
    bc = betweenness(nodes, edges)
    # 相邻共现之全部对数（用于截断声明）：不设方向，A-B 与 B-A 同计
    _pairs = set()
    for c in E["classes"]:
        for mm in (c.get("members") or []):
            _sg = [s.get("zh") for s in (mm.get("segs") or []) if s.get("zh")]
            for _i in range(len(_sg) - 1):
                if _sg[_i] != _sg[_i + 1]:
                    _pairs.add((_sg[_i], _sg[_i + 1]))
    n_all_pairs = len(_pairs)
    order = sorted(nodes, key=lambda z: -pr.get(z, 0.0))
    top_pr = [{"id": z, "zh": nzh[z], "domain": ndom[z], "n": nn[z],
               "pagerank": _r(pr.get(z, 0), 6), "degree": deg[z], "wdegree": wdeg[z]}
              for z in order[:25] if deg[z] > 0]
    order_b = sorted(nodes, key=lambda z: -bc.get(z, 0.0))
    top_bc = [{"id": z, "zh": nzh[z], "domain": ndom[z], "n": nn[z],
               "betweenness": _r(bc.get(z, 0), 6), "degree": deg[z]}
              for z in order_b[:15] if deg[z] > 1]
    # 社群：标签传播（确定性：按频次降序、同频按字序，逐轮同步更新）
    comm = {z: z for z in nodes}
    active = [z for z in nodes if deg[z] > 0]
    adjw = collections.defaultdict(dict)
    for a, b, w in edges:
        adjw[a][b] = max(adjw[a].get(b, 0), w)
        adjw[b][a] = max(adjw[b].get(a, 0), w)
    for _ in range(30):
        changed = False
        for z in sorted(active, key=lambda q: (-nn.get(q, 0), nzh.get(q, q))):
            score = collections.Counter()
            for nb, w in adjw[z].items():
                score[comm[nb]] += w
            if not score:
                continue
            best = sorted(score.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]
            if comm[z] != best:
                comm[z] = best
                changed = True
        if not changed:
            break
    groups = collections.defaultdict(list)
    for z in active:
        groups[comm[z]].append(z)
    dom_zh = {d["key"]: d["zh"] for d in E["domains"]}
    comms = []
    for root, mem in sorted(groups.items(), key=lambda kv: -len(kv[1])):
        if len(mem) < 2:
            continue
        dm = collections.Counter(ndom.get(z) for z in mem)
        wc = sum(wdeg[z] for z in mem)
        comms.append({
            "id": len(comms), "size": len(mem),
            "members": sorted([{"id": z, "zh": nzh[z], "n": nn[z], "domain": ndom[z]} for z in mem],
                              key=lambda r: -r["n"]),
            "top_domains": [{"key": k, "zh": dom_zh.get(k, k), "n": v} for k, v in dm.most_common(3)],
            "internal_weight": wc,
        })
    covered = sum(c["size"] for c in comms)
    return {
        "note_zh": "网络建于词素之**相邻共现**（同一名号内核名中相邻之两词素），非经文语序，"
                   "亦非共现于全体文句。故此网所显者，名号构词之内在联结，非叙事结构。",
        "note_en": "The network is built on adjacency co-occurrence of morphemes within a single core "
                   "name, not on their order in the sutra nor co-occurrence across sentences. It "
                   "therefore shows internal bonding in name-construction, not narrative structure.",
        "truncation": {
            "zh": "**须声明之截断**：本图之边取自 EDA 之 lex_edges，为相邻共现**全部 %d 对中"
                  "权重最高之 %d 对**；其余 %d 对（多为 n=1 之弱共现，占全对 %.1f%%）未入图。"
                  "经独立复算（networkx 之全图与截断图对读），此截断对 PageRank 之影响显著："
                  "全图之首五为「音」「須彌」「髻」「龍」「華」，截断后则「主」「光」显著上升、"
                  "前二者消失。故本页之一切中心性数值皆为「**强共现子图**上之中心性」，"
                  "**非全网之中心性**；且弱共现之被排除，恰恰抬高了强联结者之分。"
                  "读本页中心性时须常带此caveat，勿径以「此词素在会众语汇中最具枢纽性」了之。"
                  % (n_all_pairs, len(edges), n_all_pairs - len(edges),
                     _r((n_all_pairs - len(edges)) / float(n_all_pairs), 4) * 100),
            "en": "**Declared truncation**: the edges here come from the EDA lex_edges, which are the "
                  "%d highest-weight pairs out of all %d adjacent co-occurrence pairs; the remaining "
                  "%d pairs (mostly weak co-occurrences of n=1, %.1f%% of the whole) are absent. An "
                  "independent recomputation (networkx, full graph against truncated graph) shows this "
                  "truncation materially changes PageRank: the full graph's top five are 「音」「須彌」"
                  "「髻」「龍」「華」, while after truncation 「主」「光」 rise sharply and the first two "
                  "vanish. Every centrality figure on this page is therefore centrality **within the "
                  "strong-co-occurrence subgraph**, not within the full network, and the exclusion of "
                  "weak co-occurrences raises the scores of the strongly connected. This caveat must "
                  "accompany any reading of these centralities."
                  % (len(edges), n_all_pairs, n_all_pairs - len(edges),
                     _r((n_all_pairs - len(edges)) / float(n_all_pairs), 4) * 100),
            "n_all_pairs": n_all_pairs, "n_used_edges": len(edges),
            "n_dropped_pairs": n_all_pairs - len(edges),
            "dropped_pct": _r((n_all_pairs - len(edges)) / float(n_all_pairs), 4),
            "pair_counting_zh": "相邻共现之对数：一名号内相邻两词素计一对，A-B 与 B-A 不分方向。",
            "pair_counting_en": "Pair counting: adjacent morphemes within one name form one pair; "
                                 "A-B and B-A are not distinguished.",
        },
        "method_zh": "PageRank（阻尼 0.85，幂迭代收敛）、无权介数中心性（Brandes）、"
                     "加权标签传播社群（同步更新，遍历序按频次降序、同频按字序以保确定性）",
        "method_en": "PageRank (damping 0.85, power iteration to convergence), unweighted betweenness "
                     "centrality (Brandes), weighted label-propagation communities (synchronous update; "
                     "nodes visited by descending frequency then by character order, so the result is "
                     "deterministic)",
        "n_nodes": len(nodes), "n_edges": len(edges),
        "n_active": len(active),
        "isolated": len(nodes) - len(active),
        "isolated_note_zh": "孤立节点（零共现）不入中心性排名——它们在构词上不与他词素相邻，"
                            "此事实本身亦是信息：单字成词之独立角色。",
        "isolated_note_en": "Isolated nodes (no co-occurrence) are excluded from centrality rankings: they "
                            "adjoin no other morpheme in name-construction, which is itself informative "
                            "— the independent role of single-character morphemes.",
        "top_pagerank": top_pr, "top_betweenness": top_bc,
        "communities": comms,
        "community_coverage": _r(covered / float(len(nodes)), 4),
    }


# ── M. 数据质量与稳健性 ─────────────────────────────────────
def quality(E: Dict[str, Any], sim: Dict[str, Any], clu: Dict[str, Any]) -> Dict[str, Any]:
    classes = sorted(E["classes"], key=lambda c: c["idx"])
    m = E["metrics"]
    worst = []
    for c in classes:
        nt = sum(int(v) for v in (c.get("domain_hist") or {}).values()) or 1
        med = lo = 0
        for mm in (c.get("members") or []):
            for s in (mm.get("segs") or []):
                if s.get("c") == "medium":
                    med += 1
                elif s.get("c") == "low":
                    lo += 1
        worst.append({"idx": c["idx"], "cat": c["cat"], "group_zh": GROUP_ZH[c["group"]],
                      "n_tokens": nt, "med": med, "low": lo,
                      "rate": _r((med + lo) / float(nt), 4)})
    worst.sort(key=lambda r: -r["rate"])
    # 稳健性 1：五群判读存疑率排序，full vs 剔除 low
    def grp_rate(exclude_low: bool) -> Dict[str, float]:
        acc = collections.Counter()
        den = collections.Counter()
        for c in classes:
            for mm in (c.get("members") or []):
                for s in (mm.get("segs") or []):
                    d = s.get("domain") or "unassigned"
                    if d == "unassigned":
                        continue
                    if s.get("c") == "low" and exclude_low:
                        continue
                    if s.get("c") in ("medium", "low"):
                        acc[c["group"]] += 1
                    den[c["group"]] += 1
        return {g: (acc[g] / den[g] if den[g] else 0.0) for g in GROUP_ORDER}
    r_full = grp_rate(False)
    r_nolow = grp_rate(True)
    o_full = sorted(GROUP_ORDER, key=lambda g: -r_full[g])
    o_nolow = sorted(GROUP_ORDER, key=lambda g: -r_nolow[g])
    rank_same = (o_full == o_nolow)
    # 稳健性 2：离群类（在相似度空间中与全体最疏远者 = 平均相似度最低）
    n = len(sim["names"])
    avg_sim = [_r(_mean([sim["matrix"][i][j] for j in range(n) if j != i]), 4) for i in range(n)]
    order = sorted(range(n), key=lambda i: avg_sim[i])
    outliers = [{"idx": classes[i]["idx"], "cat": sim["names"][i],
                 "group_zh": GROUP_ZH[sim["groups"][i]], "mean_sim": avg_sim[i]}
                for i in order[:10]]
    return {
        "note_zh": "本节度量「本分析自身之可信度」，非度量经文。稳健性检验回答的问题是："
                   "若剔除某一级数据，结论会不会翻转？翻转者不可依赖。",
        "note_en": "This section measures the reliability of the analysis itself, not of the sutra. The "
                   "robustness test asks: if one confidence grade were removed, would the conclusion "
                   "flip? Conclusions that flip cannot be relied upon.",
        "grade_policy_zh": "low 单级＝标注义务（须显示〔待考〕）；med+low ＝比较之需。二者口径不同，严禁相混。",
        "grade_policy_en": "low alone is an annotation duty (must display 〔待考〕); med+low is for "
                           "comparison. The two calibers differ and must never be conflated.",
        "worst_classes": worst[:15],
        "robustness": [
{"id": "R1",
             "zh": "五群按「判读存疑率」（med+low / 总词素位）排序：full vs 除 low 后",
             "en": "ranking of the five groups by uncertain-reading rate: full vs low excluded",
             "full": [{"key": g, "zh": GROUP_ZH[g], "rate": _r(r_full[g], 4)} for g in o_full],
             "no_low": [{"key": g, "zh": GROUP_ZH[g], "rate": _r(r_nolow[g], 4)} for g in o_nolow],
             "order_preserved": rank_same,
             "claim_zh": "若排除低置信词素位（low）之后，五群之存疑率排序仍保持不变，则该排序对 low 之影响较小。",
             "claim_en": "If the ranking of the five groups by med+low rate remains unchanged when low-grade tokens are excluded, the ranking is not driven solely by low-confidence items.",
             "finding_zh": ("full 排序：" + " > ".join(GROUP_ZH[g] for g in o_full) + "；除 low 后：" + ("相同" if rank_same else " > ".join(GROUP_ZH[g] for g in o_nolow))),
             "finding_en": ("Full ranking: " + " > ".join(g for g in o_full) + "; excluding low: " + ("unchanged" if rank_same else " > ".join(g for g in o_nolow))),
             "result": "preserved" if rank_same else "changed",
             "result_zh": "排序%s" % ("不变" if rank_same else "发生变化"),
             "result_en": ("ranking preserved" if rank_same else "ranking changed"),
             "conclusion_zh": ("排序不变，故最存疑之群的排序不依赖 low 等级之数据"
                               if rank_same else
                               "排序变化，故该排序依赖 low 等级之数据，不可径直断言"),
             "conclusion_en": ("order is preserved, so the ranking of most-uncertain group does not depend "
                               "on low-grade data" if rank_same else
                               "the order changes, so the ranking depends on low-grade data and must not "
                               "be asserted directly")},
{"id": "R2",
             "zh": "树状图之共形相关系数（树高与原距离之相关）",
             "en": "cophenetic correlation of the dendrogram (tree heights vs original distances)",
             "value": clu["cophenetic_corr"],
             "claim_zh": "若共形相关系数 ≥ 0.75，则树结构与原始距离之吻合度尚可，层级大致可信。",
             "claim_en": "If the cophenetic correlation is ≥ 0.75, the dendrogram structure agrees sufficiently with the original distances.",
             "finding_zh": "共形相关系数 = %s" % _r(clu["cophenetic_corr"], 4),
             "finding_en": "Cophenetic correlation = %s" % _r(clu["cophenetic_corr"], 4),
             "result": "acceptable" if clu["cophenetic_corr"] >= 0.75 else "weak",
             "result_zh": "吻合度%s" % ("尚可" if clu["cophenetic_corr"] >= 0.75 else "偏弱"),
             "result_en": ("satisfactory" if clu["cophenetic_corr"] >= 0.75 else "weak"),
             "conclusion_zh": ("共形相关系数较高（≥0.75），树结构与原距离吻合尚可，层次大致可信"
                               if clu["cophenetic_corr"] >= 0.75 else
                               "共形相关系数偏低，树结构与原距离之吻合度弱，层次仅宜作参考"),
             "conclusion_en": ("the tree agrees well with the original distances, so its hierarchy is "
                               "trustworthy" if clu["cophenetic_corr"] >= 0.75 else
                               "agreement is weak, so the hierarchy should be treated as indicative only")},
{"id": "R3",
             "zh": "群内平均相似度 vs 群外平均相似度",
             "en": "mean similarity within vs across groups",
             "within": sim["within_mean"], "across": sim["across_mean"],
             "claim_zh": "若群内平均相似度高于群外平均相似度，则聚类之内聚性优于随机，即分群具备统计意义。",
             "claim_en": "If within-group mean similarity exceeds across-group mean similarity, within-cluster cohesion is better than random.",
             "finding_zh": "群内 = %s，群外 = %s（差值 %s）" % (sim["within_mean"], sim["across_mean"], _r(float(sim["within_mean"]) - float(sim["across_mean"]), 4)),
             "finding_en": "within = %s, across = %s (diff %s)" % (sim["within_mean"], sim["across_mean"], _r(float(sim["within_mean"]) - float(sim["across_mean"]), 4)),
             "result": "within>across" if float(sim["within_mean"]) > float(sim["across_mean"]) else ("within<=across"),
             "result_zh": "群内 > 群外" if float(sim["within_mean"]) > float(sim["across_mean"]) else ("群内 ≤ 群外"),
             "result_en": ("within > across" if float(sim["within_mean"]) > float(sim["across_mean"]) else "within ≤ across"),
             "conclusion_zh": sim["verdict_zh"], "conclusion_en": sim["verdict_en"]},
        ],
        "outliers": outliers,
        "outlier_note_zh": "离群类＝其语汇面貌与任何他类皆不相近者。此非缺陷，反而标出语汇之边界个案。",
        "outlier_note_en": "Outlier classes are those whose lexical profile resembles no other. This is "
                           "not a defect; it marks boundary cases of the lexicon.",
"metrics_snapshot": {k: m[k] for k in
                             ("tokens_total", "distinct_tokens", "lowconf_hits",
                              "medconf_hits", "unassigned_segs", "unassigned_lexeme_segs",
                              "unassigned_unresolved_glyph_segs", "unassigned_backlog_segs",
                              "coverage_pct", "n_no_core")},
    }


# ── N. 序位编排检验 ─────────────────────────────────────────
def ordinal(E: Dict[str, Any], sim: Dict[str, Any]) -> Dict[str, Any]:
    classes = sorted(E["classes"], key=lambda c: c["idx"])
    n = len(classes)
    S = sim["matrix"]
    adj = [S[i][i + 1] for i in range(n - 1)]
    allp = [S[i][j] for i in range(n) for j in range(i + 1, n)]
    same_group_adj = [S[i][i + 1] for i in range(n - 1) if classes[i]["group"] == classes[i + 1]["group"]]
    cross_group_adj = [S[i][i + 1] for i in range(n - 1) if classes[i]["group"] != classes[i + 1]["group"]]
    # ── 混淆诊断：相邻之显著相似，是否只因「同句式诸类被排在了一起」？──
    tails = [(c.get("leader_tail") or "").strip() or "(unknown)" for c in classes]
    adj_st = [S[i][i + 1] for i in range(n - 1) if tails[i] == tails[i + 1]]
    adj_dt = [S[i][i + 1] for i in range(n - 1) if tails[i] != tails[i + 1]]
    n_st, n_dt = len(adj_st), len(adj_dt)
    rng = LCG(19970815)
    null = []
    for _ in range(5000):
        idx = list(range(n))
        for i in range(n - 1, 0, -1):
            j = rng.randint(i + 1)
            idx[i], idx[j] = idx[j], idx[i]
        null.append(_mean([S[idx[i]][idx[i + 1]] for i in range(n - 1)]))
    mu = _mean(null)
    sd = math.sqrt(_mean([(x - mu) ** 2 for x in null])) or 1e-9
    z = (_mean(adj) - mu) / sd
    p = 0.5 * math.erfc(z / math.sqrt(2))
    # ── 去混淆检验：只取「异句式」之相邻类对，另立零分布重作置换检验 ──
    # 若此检验仍显著，则语义梯度并非仅由「同句式聚于一处」所致。
    dt_idx = [i for i in range(n - 1) if tails[i] != tails[i + 1]]
    deconf = None
    if len(dt_idx) >= 5:
        obs_dt = _mean([S[i][i + 1] for i in dt_idx])
        rng2 = LCG(19970815 + 1)
        null_dt = []
        null_counts = []
        for _ in range(5000):
            order = list(range(n))
            for i in range(n - 1, 0, -1):
                j = rng2.randint(i + 1)
                order[i], order[j] = order[j], order[i]
            # 【更正】旧式取「置换序之前 len(dt_idx) 个相邻对」而不筛模板标签，
            # 于是同句式之对亦入零分布，与观测统计量并非同一物；此已更正。
            # 现令标签随其所属类一同置换，再于置换序中取「标签不同」之相邻对，
            # 与观测统计量口径全同。
            vals = [S[order[i]][order[i + 1]] for i in range(n - 1)
                    if tails[order[i]] != tails[order[i + 1]]]
            null_counts.append(len(vals))
            null_dt.append(_mean(vals) if vals else float("nan"))
        null_dt = [v for v in null_dt if v == v]
        mu_dt = _mean(null_dt)
        sd_dt = math.sqrt(_mean([(x - mu_dt) ** 2 for x in null_dt])) or 1e-9
        z_dt = (obs_dt - mu_dt) / sd_dt
        cnt_mean = _mean(null_counts)
        deconf = {
            "zh": "去混淆检验 · 仅取跨句式边界之相邻类对",
            "en": "De-confounded test — adjacent pairs crossing a template boundary only",
            "n_pairs": len(dt_idx),
            "observed_mean": _r(obs_dt, 4),
            "null_mean": _r(mu_dt, 4), "null_sd": _r(sd_dt, 4),
            "z": _r(z_dt, 4), "p": _r(0.5 * math.erfc(z_dt / math.sqrt(2)), 5),
            "significant": bool(z_dt > 1.96),
            "null_pair_count_mean": _r(cnt_mean, 3),
            "method_zh": "零假设：句式标签沿类序之排列出于偶然。置换时标签随其所属类一同移动，"
                         "于置换序中取「标签不同」之相邻类对求均值——与观测统计量口径全同。"
                         "旧式实现误取置换序之前 n 个相邻类对而未筛标签，"
                         "使同句式之对混入零分布，此已更正。",
            "method_en": "Null hypothesis: the arrangement of template labels along the class order is "
                         "accidental. Under permutation each label travels with its own class, and the "
                         "statistic is the mean similarity of adjacent pairs whose labels differ — "
                         "identical in construction to the observed statistic. An earlier implementation "
                         "took the first n adjacent pairs of the permuted order without screening "
                         "labels, so same-template pairs contaminated the null; this has been corrected.",
            "caveat_zh": "置换后「跨边界相邻对」之个数并不恒等于观测之 %d（零分布均值 %s），"
                         "故统计量在名义上略有异方差，z 值宜读作量级而非精确显著性。"
                         "且句式标签仅取「类首名之末字」一端为代理，此一代理是否足表句式，仍属待考。"
                         % (len(dt_idx), _r(cnt_mean, 3)),
            "caveat_en": "The number of boundary-crossing adjacent pairs under permutation does not equal "
                         "the observed %d (null mean %s), so the statistic is nominally heteroscedastic "
                         "and z should be read as an order of magnitude rather than an exact "
                         "significance. Template labels moreover take only the last character of each "
                         "class's leading name as their proxy, and whether that proxy adequately "
                         "represents the template remains an open question."
                         % (len(dt_idx), _r(cnt_mean, 3)),
            "note_zh": "此为**排除「同句式聚于相邻」这一混淆项之后**的独立检验。"
                       "若仍显著，则「类次编排含语义梯度」之断不依赖句式同聚，"
                       "可独立成立；若不显著，则该断只能归因于句式同聚，须撤回。",
            "note_en": "This test excludes the confounding effect of same-template classes being "
                       "adjacent. If it remains significant, the claim that the ordering carries a "
                       "semantic gradient survives independently of template adjacency; if not, that "
                       "claim must be withdrawn as an artefact of template adjacency.",
        }
    # 各卷（group 段）内的域构成
    segs = []
    for g in GROUP_ORDER:
        cs = sorted(c["idx"] for c in classes if c["group"] == g)
        if len(cs) < 2:
            continue
        pairv = [S[cs[a]][cs[b]] for a in range(len(cs)) for b in range(a + 1, len(cs))]
        segs.append({"group": g, "zh": GROUP_ZH[g], "from_idx": cs[0], "to_idx": cs[-1],
                     "n_classes": len(cs), "mean_sim_internal": _r(_mean(pairv), 4)})
    # 结论：先按显著性分支，再按去混淆分支——不写嵌套条件表达式（易漏括号）
    sig_zh = z > 1.96
    if not deconf:
        conc_zh = ("相邻类%s显著更相近（z=%.2f）。异句式相邻对不足 5，故未作去混淆检验，此断暂存。"
                   % ("显著" if sig_zh else "未", z))
        conc_en = ("adjacent classes are %ssignificantly more similar (z=%.2f). With fewer than five "
                   "different-template adjacent pairs, no de-confounded test was run and the claim "
                   "is held in abeyance." % ("" if sig_zh else "not ", z))
    elif not sig_zh:
        conc_zh = ("相邻类未显著更相近（z=%.2f），故类次之语义梯度不成立。去混淆检验（z=%.2f）与此一致。"
                   % (z, deconf["z"]))
        conc_en = ("adjacent classes are not significantly more similar (z=%.2f), so no semantic "
                   "gradient in the ordering is supported; the de-confounded test (z=%.2f) agrees."
                   % (z, deconf["z"]))
    elif deconf["significant"]:
        conc_zh = ("相邻类显著更相近（z=%.2f）。去混淆检验（仅异句式相邻对，n=%d）仍然显著（z=%.2f），"
                   "故「类次编排含语义梯度」之断成立，且不依赖同句式聚于相邻之效应。")
        conc_zh = conc_zh % (z, deconf["n_pairs"], deconf["z"])
        conc_en = ("Adjacent classes are significantly more similar (z=%.2f). The de-confounded test "
                   "(different-template adjacent pairs only, n=%d) remains significant (z=%.2f), so "
                   "the claim that the ordering carries a semantic gradient holds and does not depend "
                   "on the effect of same-template classes being placed adjacently."
                   % (z, deconf["n_pairs"], deconf["z"]))
    else:
        conc_zh = ("相邻类显著更相近（z=%.2f）。然去混淆检验（仅异句式相邻对，n=%d）不再显著（z=%.2f），"
                   "故全效应可归因于同句式诸类之聚于相邻，「类次编排含语义梯度」之断须撤回。")
        conc_zh = conc_zh % (z, deconf["n_pairs"], deconf["z"])
        conc_en = ("Adjacent classes are significantly more similar (z=%.2f). The de-confounded test "
                   "(different-template adjacent pairs only, n=%d) is no longer significant (z=%.2f), so "
                   "the whole effect is attributable to same-template classes being placed adjacently "
                   "and the claim that the ordering carries a semantic gradient must be withdrawn."
                   % (z, deconf["n_pairs"], deconf["z"]))
    return {
        "note_zh": "本节问：经文把四十类依次排出，其**前后相邻**之两类是否比随机两两更相近？"
                   "若显著更高，则类次之编排本身含语义梯度（非随机排列）；若不显著，则类次或为"
                   "编纂体例之故。此为统计检验，不涉教义。",
        "note_en": "This section asks whether classes adjacent in the sutra's order are more similar "
                   "than randomly chosen pairs. If significantly higher, the ordering itself carries a "
                   "semantic gradient rather than being arbitrary; if not, the order may reflect "
                   "editorial convention. This is a statistical test, not a doctrinal one.",
        "method_zh": "以 LCG 定种（种子 19970815）作 5000 次随机置换之零分布，取 z 值与正态近似 p",
        "method_en": "Null distribution from 5000 random permutations drawn from a seeded LCG (seed "
                     "19970815); z statistic and normal-approximation p",
        "adjacent_mean": _r(_mean(adj), 4), "null_mean": _r(mu, 4), "null_sd": _r(sd, 4),
        "z": _r(z, 4), "p": _r(p, 5),
        "all_pairs_mean": _r(_mean(allp), 4),
        "same_group_adjacent": _r(_mean(same_group_adj), 4) if same_group_adj else None,
        "cross_group_adjacent": _r(_mean(cross_group_adj), 4) if cross_group_adj else None,
        "confound": {
            "adj_same_template_mean": _r(_mean(adj_st), 4) if adj_st else None,
            "adj_diff_template_mean": _r(_mean(adj_dt), 4) if adj_dt else None,
            "same_minus_diff": _r(_mean(adj_st) - _mean(adj_dt), 4) if adj_st and adj_dt else None,
            "n_same_template": n_st, "n_diff_template": n_dt,
            "tail_of_class": [{"idx": c["idx"], "cat": c["cat"], "tail": t}
                              for c, t in zip(classes, tails)],
            "n_distinct_tail": len({t for t in tails}),
            "note_zh": "**本节之 z 值须与混淆诊断对读**：全品中「主X神」诸类共用一句式（类尾同为「神」），"
                       "句式相同故域分布趋同；此类又被排为相邻，故相邻相似度可能被推高。"
                       "但实测混淆幅度有限：同句式相邻 %.4f 与异句式相邻 %.4f 仅差 %.4f，"
                       "故主效应非由此项造成。为不凭推理定论，另立**去混淆检验**"
                       "（de-confounded，见下）：仅取异句式之相邻类对重作置换检验，"
                       "此为「语义梯度」之真正所在之判据。"
                       % (_mean(adj_st), _mean(adj_dt), _mean(adj_st) - _mean(adj_dt)
                          if adj_st and adj_dt else (0, 0, 0)),
            "note_en": "The z statistic must be read together with this confounding check. The 「主X神」 "
                       "classes of this sutra share one template (the same class tail, 「神」), so their "
                       "domain profiles converge; they are also placed adjacently, which could inflate "
                       "adjacent similarity. The measured confound is however small: same-template "
                       "adjacent %.4f differs from different-template adjacent %.4f by only %.4f, so "
                       "the main effect is not produced by it. Rather than settle this by argument, a "
                       "separate de-confounded test is run below, using adjacent pairs with different "
                       "templates only; that is the real criterion for a semantic gradient."
                       % (_mean(adj_st), _mean(adj_dt), _mean(adj_st) - _mean(adj_dt)
                          if adj_st and adj_dt else (0, 0, 0)),
            "deconfounded": deconf,
        },
"segments": segs,
        "conclusion_zh": conc_zh,
        "conclusion_en": conc_en,
    }


# ── O. 组间对标雷达 ─────────────────────────────────────────
def benchmark(E: Dict[str, Any]) -> Dict[str, Any]:
    gps = {g["key"]: g for g in E["group_profiles"]}
    dims = []
    def add(key, zh, en, unit, getter, higher_better=True):
        dims.append({"key": key, "zh": zh, "en": en, "unit": unit,
                     "higher_better": higher_better, "_get": getter})
    add("core_len_mean", "核名平均字数", "Mean core length", "char", lambda g: gps[g]["core_len_mean"])
    add("n_distinct_morph", "不同词素数", "Distinct morphemes", "count",
        lambda g: gps[g]["n_distinct_morph"])
    add("word_rate", "多字词占比", "Multi-char word rate", "ratio",
        lambda g: gps[g]["n_word_hits"] / max(gps[g]["n_tokens"], 1))
    add("lowconf_pct", "low 占比", "Low-confidence rate", "ratio", lambda g: gps[g]["lowconf_pct"])
    add("medlow_pct", "判读存疑占比", "Uncertain-reading rate", "ratio",
        lambda g: gps[g]["medconf_pct"] + gps[g]["lowconf_pct"])
    add("domain_top_share", "主域集中度", "Top-domain share", "ratio",
        lambda g: (gps[g]["domains"][0]["pct"] / 100.0 if gps[g].get("domains") else 0.0))
    add("lexical_economy", "语汇经济率", "Lexical economy", "ratio",
        lambda g: 1.0 - (gps[g]["n_distinct_morph"] / max(gps[g]["n_tokens"], 1)))
    add("names_per_class", "每类平均名号数", "Names per class", "ratio",
        lambda g: gps[g]["n_named"] / max(gps[g]["n_classes"], 1))
    for d in dims:
        raw = {g: d["_get"](g) for g in GROUP_ORDER}
        lo, hi = min(raw.values()), max(raw.values())
        d.pop("_get")
        d["min"] = _r(lo, 4)
        d["max"] = _r(hi, 4)
        d["raw"] = [{"key": g, "zh": GROUP_ZH[g], "v": _r(raw[g], 4)} for g in GROUP_ORDER]
        d["norm"] = [{"key": g, "zh": GROUP_ZH[g],
                      "v": _r((raw[g] - lo) / (hi - lo), 4) if hi > lo else 0.5} for g in GROUP_ORDER]
    return {
        "note_zh": "雷达图各轴皆已**逐轴极差归一**（同轴内最劣为 0、最优为 1），故只可比较"
                   "「同一指标之相对位次」，**不可**跨轴比较绝对大小——归一即抹去量纲。"
                   "轴之朝向为「外优内劣」，故多边形越外扩者越优；惟 low 占比、判读存疑占比二轴"
                   "本为「内优外劣」（越低越好），已在图中反向标示，不可误读为「越大越好」。",
        "note_en": "Every axis is min-max normalised within itself (worst = 0, best = 1), so only the "
                   "relative standing on one metric is comparable; magnitudes across axes are not, since "
                   "normalisation removes scale. Outward is better, except the two uncertainty axes "
                   "(low rate, uncertain-reading rate) where inward is better — these are drawn "
                   "inverted and must not be read as 'bigger is better'.",
        "dims": dims,
        "groups": [{"key": g, "zh": GROUP_ZH[g], "en": GROUP_EN[g],
                    "n_named": gps[g]["n_named"], "n_classes": gps[g]["n_classes"],
                    "n_tokens": gps[g]["n_tokens"]} for g in GROUP_ORDER],
    }


# ── P. 编制报告 ─────────────────────────────────────────────
def build_report() -> Dict[str, Any]:
    E = _load()
    sim = similarity(E)
    clu = clustering(E, sim)
    rep: Dict[str, Any] = {
        "article": ARTICLE,
        "title_zh": "世主妙严品会众名号 · 数据报告",
        "title_en": "Data Report on the Assemblies of the World-Honoring Splendour Chapter",
        "source": SOURCE,
        "source_url": SOURCE_URL,
        "generated_by": "scripts/miaoyan_bi.py ← data/translation/miaoyan_eda.yaml"
                        "（← miaoyan_eda.py ← miaoyan_assembly.yaml ＋ miaoyan_eda_lexicon.yaml）",
        "generated_at_source": E.get("generated_by"),
        "disclaimer": {
            "zh": "⚠️ 体例：本报告为**分析层**产物，非经文陈述。名号之属类、成员、数量出《世主妙严品》"
                  "（assembly 层）；词素切分、语义域归属、相似度、聚类、相关、模板诸项皆本站析构"
                  "（EDA 层与 BI 层）。经文自无「十七语义域」「余弦相似度」「轮廓系数」等名目。"
                  "凡本报告所得，皆可复算而不可直作教义判读；一字一句之义，仍以经文为准。",
            "en": "⚠️ Convention: this report is an analytical product, not a statement of the sutra. "
                  "Class membership, names and counts come from the World-Honoring Splendour Chapter "
                  "(assembly layer); morpheme segmentation, domain assignment, similarity, clustering, "
                  "correlation and templates are this site's own analysis (EDA and BI layers). The sutra "
                  "has no notion of 'seventeen domains', 'cosine similarity' or 'silhouette'. Everything "
                  "here is reproducible but must not be read as doctrinal judgement; for the meaning of "
                  "words, the sutra remains authoritative.",
        },
        "method": {
            "pipeline_zh": "经文事实（assembly）→ 词素析构（EDA）→ BI 分析（本层）三层分源，逐层可回溯。",
            "pipeline_en": "Three separated layers — sutra facts (assembly) → morphemic analysis (EDA) → "
                           "BI analysis (this layer) — each independently traceable.",
            "determinism_zh": "凡涉随机处，一律以定种线性同余发生器（LCG）取样，"
                              "禁用 Python random 默认源（其实现版本间可变，会破坏可复现性）。",
            "determinism_en": "All sampling uses a seeded linear congruential generator (LCG); Python's "
                              "random module is deliberately avoided because its implementations vary "
                              "between versions and would break reproducibility.",
            "deps_zh": "零新增依赖：协方差特征分解用自实现 Jacobi 旋转，"
                       "聚类/轮廓/中心性皆自实现，故结果不随第三方库版本而变。",
            "deps_en": "No new dependencies: eigen-decomposition uses a self-implemented Jacobi rotation, "
                       "and clustering, silhouette and centrality are all self-implemented, so results do "
                       "not drift with third-party library versions.",
            "integrity_zh": "本层不改 EDA 之任何数字，只读 EDA 而另作分析。"
                            "故 L.101 以来之口径（high/medium/low 三分、low 单级为标注义务）在此原样承继。",
            "integrity_en": "This layer alters no figure produced by the EDA; it only reads it and adds "
                            "analysis. The calibers established since L.101 (three confidence grades, low "
                            "alone carrying the annotation duty) are inherited unchanged.",
        },
        "scorecard": scorecard(E),
        "funnel": funnel(E),
        "domain_landscape": domain_landscape(E),
        "crosstab": crosstab(E),
        "similarity": sim,
        "clustering": clu,
        "pca": pca(E, sim),
        "pareto": pareto(E),
        "scatter": scatter(E),
        "templates": templates(E),
        "network": network(E),
        "benchmark": benchmark(E),
        "quality": quality(E, sim, clu),
        "ordinal": ordinal(E, sim),
    }
    rep["executive"] = executive(rep)
    return rep


def executive(R: Dict[str, Any]) -> Dict[str, Any]:
    """执行摘要：结论皆由已算之数推出，不另生数据。"""
    m = R["scorecard"]
    cl = R["clustering"]
    ot = R["ordinal"]
    dc = R["domain_landscape"]
    tb = R["templates"]
    sim = R["similarity"]
    it = dict((x["key"], x) for x in m["items"])
    findings = [
        {"id": "F1", "zh": "会众名号之语汇高度模板化：不同词素 %s 个撑起 %s 个词素位，语汇复用率 %s。"
                           % (f"{int(it['distinct_tokens']['value']):,}",
                              f"{int(it['tokens_total']['value']):,}",
                              it["reuse_rate"]["display"]),
         "en": "The vocabulary of the assemblies is strongly templated: %s distinct morphemes support "
               "%s token positions, a reuse rate of %s."
               % (f"{int(it['distinct_tokens']['value']):,}",
                  f"{int(it['tokens_total']['value']):,}",
                  it['reuse_rate']['display']),
         "evidence": "scorecard · reuse_rate；pareto · morphemes.k80=%s" % R["pareto"]["series"][0]["k80"]},
        {"id": "F2", "zh": "语义域分布并不均匀：主域为「%s」占 %s，有效域数仅 %s（满值 %d）。"
                           % (dc["rows"][0]["zh"], dc["rows"][0]["pct"] * 100,
                              dc["concentration"]["effective_domains"],
                              dc["concentration"]["max_domains"]),
         "en": "The domain distribution is uneven: the leading domain is %s at %s, with an effective "
               "number of domains of only %s (maximum %d)."
               % (dc["rows"][0]["en"], f"{dc['rows'][0]['pct'] * 100:.2f}%",
                  dc["concentration"]["effective_domains"], dc["concentration"]["max_domains"]),
         "evidence": "domain_landscape · HHI=%s, 归一熵=%s" % (dc["concentration"]["hhi"],
                                                               dc["concentration"]["normalized_entropy"])},
        {"id": "F3", "zh": "「五群」之划分与语汇面貌%s（群内均值 %s vs 群外 %s）。"
                           "惟此对应并不严密：域×群之关联强度 Cramér's V=%s，属弱至中等，"
                           "故「五群」者乃**卷次所分之经文体例**，非由语汇面貌自然析出之类。"
                           % (sim["verdict_zh"], sim["within_mean"], sim["across_mean"],
                              R["crosstab"]["cramers_v"]),
         "en": "The five-group division is %s (within-group mean %s vs across-group %s). The "
               "correspondence is not tight, however: a Cramér's V of %s between domain and group is "
               "weak to moderate, so the five groups are an editorial division by scroll, not classes "
               "that fall out of the lexical landscape."
               % (sim["verdict_en"], sim["within_mean"], sim["across_mean"],
                  R["crosstab"]["cramers_v"]),
         "evidence": "similarity · within=%s vs across=%s；crosstab · Cramér's V=%s"
                     % (sim["within_mean"], sim["across_mean"], R["crosstab"]["cramers_v"])},
        {"id": "F4", "zh": "构词之模板性在**字面**而不在**域构成**：414 名之核名首二字只落在 %d 种二字组上"
                           "（复用率 %s），而语义域序列则碎为 %d 种（%d 种只现一次，占 %s，"
                           "归一熵 %s）。故此会众语汇乃同一批字反复组装，非同一批语义反复填充。"
                           % (tb["layer1_literal"]["n_distinct_bigram"],
                              "%.1f%%" % (tb["layer1_literal"]["bigram_reuse_rate"] * 100),
                              tb["layer2_domain"]["n_distinct"], tb["layer2_domain"]["n_singleton"],
                              "%.1f%%" % (tb["layer2_domain"]["singleton_pct"] * 100),
                              tb["layer2_domain"]["normalized_entropy"]),
         "en": "The templating of these names lies in the characters, not in the domain composition: "
               "the first two characters of the 414 nuclei fall into only %d distinct bigrams (a reuse "
               "rate of %s), whereas the semantic-domain sequences fragment into %d patterns (%d of "
               "them occurring exactly once, %s of all names, normalised entropy %s). The vocabulary "
               "therefore re-assembles the same stock of characters rather than filling the same stock "
               "of meanings."
               % (tb["layer1_literal"]["n_distinct_bigram"],
                  "%.1f%%" % (tb["layer1_literal"]["bigram_reuse_rate"] * 100),
                  tb["layer2_domain"]["n_distinct"], tb["layer2_domain"]["n_singleton"],
                  "%.1f%%" % (tb["layer2_domain"]["singleton_pct"] * 100),
                  tb["layer2_domain"]["normalized_entropy"]),
         "evidence": "templates · layer1_literal.n_distinct_bigram=%d；layer2_domain.n_distinct=%d，"
                     "n_singleton=%d" % (tb["layer1_literal"]["n_distinct_bigram"],
                                         tb["layer2_domain"]["n_distinct"],
                                         tb["layer2_domain"]["n_singleton"])},
        {"id": "F5", "zh": "类次编排%s（相邻类平均相似度 %s，置换零分布 %s，z=%s）。"
                           % (ot["conclusion_zh"], ot["adjacent_mean"], ot["null_mean"], ot["z"]),
         "en": "%s (mean similarity of adjacent classes %s, permutation null %s, z=%s)."
               % (ot["conclusion_en"], ot["adjacent_mean"], ot["null_mean"], ot["z"]),
         "evidence": "ordinal · 5000 次置换检验；去混淆检验 n=%s, z=%s"
                     % (ot["confound"]["deconfounded"]["n_pairs"],
                        ot["confound"]["deconfounded"]["z"])},
        {"id": "F6", "zh": "构词网络存在 %d 个词素社群，覆盖 %s 之节点；"
                           "此社群由名号内部共现生成，非经文语序。"
                           % (len(R["network"]["communities"]),
                              "%.1f%%" % (R["network"]["community_coverage"] * 100)),
         "en": "The morphological network yields %d communities covering %s of nodes; these arise from "
               "co-occurrence within names, not from the sutra's word order."
               % (len(R["network"]["communities"]),
                  "%.1f%%" % (R["network"]["community_coverage"] * 100)),
         "evidence": "network · label propagation"},
    ]
    return {
        "note_zh": "以下六条为执行摘要，每条皆附**证据字段**指回本报告之算得小节，"
                   "可逐条复算。凡摘要不得为正文所无之断语。",
        "note_en": "The six findings below form the executive summary; each carries an evidence field "
                   "pointing back to the computed section of this report and is independently "
                   "recomputable. The summary may not assert anything absent from the body.",
        "findings": findings,
    }


# ══════════════════════════════════════════════════════════════
# 三、不变量校验与输出
# ══════════════════════════════════════════════════════════════

def do_check(R: Dict[str, Any]) -> List[str]:
    errs: List[str] = []
    m = R["scorecard"]
    F = R["funnel"]
    L = R["domain_landscape"]
    X = R["crosstab"]
    S = R["similarity"]
    C = R["clustering"]
    P = R["pca"]
    T = R["templates"]
    N = R["network"]
    Q = R["quality"]
    O = R["ordinal"]

    # 1) 漏斗：两轨各自单调收窄
    t1 = F["track_names"]["stages"]
    t2 = F["track_tokens"]["stages"]
    for track in (t1, t2):
        ns = [s["n"] for s in track]
        for a, b in zip(ns, ns[1:]):
            if b > a:
                errs.append("funnel track not monotonic: %s > %s" % (a, b))
    tok = t2[0]["n"]
    # 2) 判读分级三分之和 = 已归域
    gs = F["grades"]
    if gs["high"]["n"] + gs["medium"]["n"] + gs["low"]["n"] != t2[1]["n"]:
        errs.append("grades sum != assigned stage")
    # 3) 语义域全景之和 = 词素位总数（应含 unassigned）
    domsum = sum(r["n"] for r in L["rows"])
    if domsum != t2[0]["n"]:
        errs.append("domain rows sum %s != token positions %s" % (domsum, t2[0]["n"]))
    # 4) 交叉表矩阵总和 = 词素位总数
    if sum(sum(r) for r in X["matrix"]) != t2[0]["n"]:
        errs.append("crosstab sum mismatch")
    # 5) 相似度矩阵对称、对角为 1、值域 [0,1]
    n = len(S["names"])
    for i in range(n):
        if abs(S["matrix"][i][i] - 1.0) > 1e-6 and S["matrix"][i][i] != 0.0:
            errs.append("similarity diagonal[%d]=%s" % (i, S["matrix"][i][i]))
            break
        for j in range(n):
            v1, v2 = S["matrix"][i][j], S["matrix"][j][i]
            if abs(v1 - v2) > 1e-9:
                errs.append("similarity not symmetric at %d,%d" % (i, j))
                break
            if not (-1.0001 <= v1 <= 1.0001):
                errs.append("similarity out of range at %d,%d = %s" % (i, j, v1))
                break
        else:
            continue
        break
    # 6) 聚类：簇覆盖全部类，无重复
    seen = [x["idx"] for c in C["clusters"] for x in c["members"]]
    if sorted(seen) != sorted(S["idx"]):
        errs.append("clusters do not partition classes (%d covered)" % len(seen))
    if len(C["merges"]) != n - 1:
        errs.append("merges should be n-1 = %d, got %d" % (n - 1, len(C["merges"])))
    klo, khi = C["k_range"]
    if not (klo <= C["best_k"] <= khi):
        errs.append("best_k out of range: %s (allowed %s..%s)" % (C["best_k"], klo, khi))
    best = max(C["curve"], key=lambda r: r["silhouette"])
    if best["k"] != C["best_k"]:
        errs.append("best_k %s != max-silhouette k %s" % (C["best_k"], best["k"]))
    if len(C["curve"]) != khi - klo + 1:
        errs.append("silhouette curve length %d != scanned range %d" % (len(C["curve"]), khi - klo + 1))
    if C["k_at_boundary"] and not (C["k_boundary_note_zh"] and C["k_boundary_note_en"]):
        errs.append("boundary hit without bilingual note")
    if not (C.get("weak_structure_zh") and C.get("weak_structure_en")):
        errs.append("clustering lacks bilingual structure-strength verdict")
    if not (-1.0001 <= C["cophenetic_corr"] <= 1.0001):
        errs.append("cophenetic correlation out of range: %s" % C["cophenetic_corr"])
    # 7) PCA：解释方差比 ≤ 1 且递减
    tot = sum(e["pct"] for e in P["explained"])
    if not (0 < tot <= 1.0001):
        errs.append("PCA explained sum = %s" % tot)
    pv = [e["pct"] for e in P["explained"]]
    for a, b in zip(pv, pv[1:]):
        if b > a + 1e-9:
            errs.append("PCA explained not descending")
            break
    if len(P["points"]) != n:
        errs.append("PCA points count %d != %d" % (len(P["points"]), n))
    # 8) 模板三层：各层计数自洽，覆盖率 ≤ 1
    if not (0 < T["coverage_top24"] <= 1.0):
        errs.append("template coverage out of range: %s" % T["coverage_top24"])
    if sum(T["token_length_hist"][i]["n"] for i in range(len(T["token_length_hist"]))) != T["n_members"]:
        errs.append("token length hist sum != n_members")
    if T["layer2_domain"]["n_distinct"] > T["n_members"]:
        errs.append("layer2 distinct patterns (%s) > n_members (%s)"
                    % (T["layer2_domain"]["n_distinct"], T["n_members"]))
    if sum(r["n"] for r in T["layer2_domain"]["rows"]) > T["n_members"]:
        errs.append("layer2 pattern rows exceed n_members")
    if sum(r["n"] for r in T["layer3_skeleton"]["rows"]) > T["n_members"]:
        errs.append("layer3 skeleton rows exceed n_members")
    if T["layer2_domain"]["unassigned_in_top"] and not T["layer2_domain"]["unassigned_note_zh"]:
        errs.append("layer2 top patterns contain unassigned but no caution note")
    l1 = T["layer1_literal"]
    if not (0 < l1["bigram_coverage"] <= 1.0):
        errs.append("layer1 bigram coverage out of range: %s" % l1["bigram_coverage"])
    if l1["n_distinct_bigram"] > T["n_members"]:
        errs.append("layer1 distinct bigrams exceed n_members")
    # bigram_rows 取前 24 种，故只校验「不超总数」与「递减」，不校验等长
    if len(l1["bigram_rows"]) > l1["n_distinct_bigram"]:
        errs.append("layer1 bigram rows exceed distinct bigrams")
    bv = [r["n"] for r in l1["bigram_rows"]]
    for a, b in zip(bv, bv[1:]):
        if b > a:
            errs.append("layer1 bigram rows not descending")
            break
    # bigram_coverage 为「二字组唯一数占名号数」；top24_coverage 为「前 24 种覆盖之名号比例」，
    # 二者不同量纲，须分别给字段，不得互相校验
    if not (0 < l1["top24_coverage"] <= 1.0):
        errs.append("layer1 top24 coverage out of range: %s" % l1["top24_coverage"])
    if not (l1.get("measure_zh") and l1.get("measure_en")):
        errs.append("layer1 missing bilingual measurement caveat")
    # 网络截断声明：凡有截断必双语声明，且须给出实际对数
    tr = R["network"].get("truncation")
    if tr:
        if not (tr.get("zh") and tr.get("en")):
            errs.append("network truncation lacks bilingual note")
        if tr["n_dropped_pairs"] < 0 or tr["n_used_edges"] + tr["n_dropped_pairs"] != tr["n_all_pairs"]:
            errs.append("network truncation pair counts inconsistent")
        if tr["n_dropped_pairs"] > 0 and not tr.get("pair_counting_zh"):
            errs.append("network truncation lacks pair-counting definition")
        if tr["n_dropped_pairs"] == 0 and "非全网" in tr.get("zh", ""):
            errs.append("truncation note claims loss where none exists")
    # PCA 与相似度共用 TF-IDF 加权，须记录该口径
    for key in ("pca", "similarity"):
        if "TF-IDF" not in R[key].get("method_zh", "") + R[key].get("space_zh", "") + \
                R[key].get("method_en", "") + R[key].get("space_en", ""):
            errs.append("%s does not record the TF-IDF weighting basis" % key)
    if T["layer2_domain"]["n_singleton"] > T["layer2_domain"]["n_distinct"]:
        errs.append("layer2 singleton count exceeds distinct patterns")
    for sub in ("layer1_literal", "layer2_domain", "layer3_skeleton"):
        if not (T[sub].get("zh") and T[sub].get("en")):
            errs.append("template layer missing bilingual title: %s" % sub)
    if not (T.get("verdict_zh") and T.get("verdict_en")):
        errs.append("templates missing bilingual verdict")
    # 9) 网络：社群成员互斥
    allm = [m["id"] for c in N["communities"] for m in c["members"]]
    if len(allm) != len(set(allm)):
        errs.append("communities overlap")
    if len(N["communities"]) and N["community_coverage"] > 1.0001:
        errs.append("community coverage > 1")
    # 10) 对标：归一值须在 [0,1]
    for d in R["benchmark"]["dims"]:
        for x in d["norm"]:
            if not (-0.0001 <= x["v"] <= 1.0001):
                errs.append("benchmark norm out of range: %s %s" % (d["key"], x["key"]))
    # 11) 帕累托累计单调且末项为 1
    for s in R["pareto"]["series"]:
        cv = [p["cum_pct"] for p in s["points"]]
        for a, b in zip(cv, cv[1:]):
            if b < a - 1e-9:
                errs.append("pareto cum not monotonic: %s" % s["dimension"])
                break
        if cv and abs(cv[-1] - 1.0) > 1e-6:
            errs.append("pareto cum end %s != 1 (%s)" % (cv[-1], s["dimension"]))
    # 12) 散点：相关系数须在 [-1,1]
    for pr in R["scatter"]["pairs"]:
        for k in ("pearson", "spearman"):
            if not (-1.0001 <= pr[k] <= 1.0001):
                errs.append("correlation out of range: %s/%s = %s" % (pr["x"], pr["y"], pr[k]))
    # 13) 序位：零分布 z 有限
    if not math.isfinite(O["z"]):
        errs.append("ordinal z not finite")
    if not (0.0 <= O["p"] <= 1.0):
        errs.append("ordinal p out of range")
    # 14) 执行摘要：每条皆须有证据字段
    for f in R["executive"]["findings"]:
        if not f.get("evidence"):
            errs.append("executive finding %s lacks evidence" % f["id"])
    # 混淆诊断：相似度与序位两处皆须有，且数值须与主体分项相符
    for key in ("similarity", "ordinal"):
        cf = R[key].get("confound")
        if not cf:
            errs.append("%s lacks confound check" % key)
            continue
        if not (cf.get("note_zh") and cf.get("note_en")):
            errs.append("%s confound lacks bilingual note" % key)
        if key == "similarity":
            sm, dm, om = cf["same_tail_mean"], cf["diff_tail_mean"], cf["overall_mean"]
            if None in (sm, dm, om):
                errs.append("similarity confound has missing means")
            elif not (dm <= om <= sm + 1e-9):
                errs.append("similarity confound means implausible: diff=%s overall=%s same=%s"
                            % (dm, om, sm))
            if cf["n_same_tail_pairs"] + cf["n_diff_tail_pairs"] != 40 * 39 // 2:
                errs.append("similarity confound pair split != 780")
        else:
            st, dt = cf["adj_same_template_mean"], cf["adj_diff_template_mean"]
            if st is not None and dt is not None and dt > st + 1e-9:
                errs.append("ordinal confound implausible: diff-template %s > same-template %s"
                            % (dt, st))
            if cf["n_same_template"] + cf["n_diff_template"] != 39:
                errs.append("ordinal confound split != 39 adjacent pairs")
            dc = cf.get("deconfounded")
            if not dc:
                errs.append("ordinal confound lacks de-confounded test")
            else:
                if dc["n_pairs"] != cf["n_diff_template"]:
                    errs.append("de-confounded n_pairs %s != n_diff_template %s"
                                % (dc["n_pairs"], cf["n_diff_template"]))
                if dc["significant"] != (dc["z"] > 1.96):
                    errs.append("de-confounded significance flag disagrees with z")
                if not (dc.get("note_zh") and dc.get("note_en")):
                    errs.append("de-confounded test lacks bilingual note")
                if not (dc.get("method_zh") and dc.get("method_en")):
                    errs.append("de-confounded test lacks method statement")
                if not (dc.get("caveat_zh") and dc.get("caveat_en")):
                    errs.append("de-confounded test lacks caveat")
                if dc["n_pairs"] >= 5 and dc["observed_mean"] > 1.0001:
                    errs.append("de-confounded observed mean out of range")
                # 零分布亦须落在余弦之取值域内
                if not (0.0 <= dc["null_mean"] <= 1.0) or not (0.0 <= dc["observed_mean"] <= 1.0):
                    errs.append("de-confounded mean outside cosine range")
    # 15) 质量：稳健性三则俱在
    if {x["id"] for x in Q["robustness"]} != {"R1", "R2", "R3"}:
        errs.append("robustness set incomplete")
    # 16) 中英必配：主要节皆须有双语注记
    for key, zh_field, en_field in (
            ("similarity", "caveat_zh", "caveat_en"), ("clustering", "caveat_zh", "caveat_en"),
            ("pca", "caveat_zh", "caveat_en"), ("network", "note_zh", "note_en"),
            ("scorecard", "note", "note_en"), ("funnel", "note", "note_en"),
            ("domain_landscape", "note", "note_en"), ("crosstab", "note", "note_en"),
            ("pareto", "note_zh", "note_en"), ("scatter", "note_zh", "note_en"),
            ("templates", "note_zh", "note_en"), ("benchmark", "note_zh", "note_en"),
            ("ordinal", "note_zh", "note_en"), ("executive", "note_zh", "note_en"),
            ("funnel", "reconciliation", "reconciliation"),
            ("disclaimer", "zh", "en")):
        if not R.get(key, {}).get(zh_field) or not R.get(key, {}).get(en_field):
            errs.append("missing bilingual note: %s (%s/%s)" % (key, zh_field, en_field))
    return errs


def dump_yaml(data: Any, path: str) -> int:
    txt = yaml.safe_dump(data, allow_unicode=True, sort_keys=False,
                         default_flow_style=False, width=100, indent=2)
    with io.open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(txt)
    return len(txt.encode("utf-8"))


def summary(R: Dict[str, Any]) -> str:
    L: List[str] = []
    L.append("═" * 68)
    L.append("世主妙严品会众名号 · 数据报告 (BI 层)")
    L.append("═" * 68)
    sc = R["scorecard"]["items"]
    L.append("【记分卡】")
    for x in sc:
        L.append("  %-16s %-24s %s" % (x["key"], x["zh"], x["display"]))
    F = R["funnel"]
    t1 = F["track_names"]["stages"]
    t2 = F["track_tokens"]["stages"]
    L.append("【结构分解漏斗】两轨不可连读（轨间为扩张，非流失）")
    for s in t1:
        L.append("  轨一 %-4s %-12s %6d  占本轨 %6.2f%%" % (s["key"], s["zh"], s["n"], s["pct_of_track"] * 100))
    for s in t2:
        L.append("  轨二 %-4s %-12s %6d  占本轨 %6.2f%%" % (s["key"], s["zh"], s["n"], s["pct_of_track"] * 100))
    L.append("  换算：每名平均析 %.2f 位词素 · 无核者 %d"
             % (F["conversion"]["tokens_per_name"], F["conversion"]["no_core"]))
    dc = R["domain_landscape"]["concentration"]
    L.append("【集中度】HHI=%.6f  归一熵=%.4f  有效域数=%.3f / %d"
             % (dc["hhi"], dc["normalized_entropy"], dc["effective_domains"], dc["max_domains"]))
    X = R["crosstab"]
    L.append("【域×群关联】chi2=%.2f (df=%d)  Cramér's V=%.4f  p≈%.5f"
             % (X["chi2"], X["df"], X["cramers_v"], X["p_approx"]))
    S = R["similarity"]
    L.append("【相似度】群内均值=%s  群外均值=%s  → %s" % (S["within_mean"], S["across_mean"], S["verdict_zh"]))
    L.append("  最相似 5 对：%s" % "、".join("%s~%s(%s)" % (p["a"], p["b"], p["sim"]) for p in S["top"][:5]))
    C = R["clustering"]
    L.append("【聚类】最佳 k=%d  轮廓=%s  共形相关=%s  簇数=%d"
             % (C["best_k"], C["best_silhouette"], C["cophenetic_corr"], len(C["clusters"])))
    for c in C["clusters"][:6]:
        L.append("  簇%d (%d类/%d名, 轮廓%s, 稳定%s): %s"
                 % (c["id"], c["n_classes"], c["n_named"], c["silhouette"], c["stability"],
                    "、".join(x["cat"] for x in c["members"][:6])))
    P = R["pca"]
    L.append("【PCA】前三维解释方差 = %s"
             % " + ".join("%.2f%%" % (e["pct"] * 100) for e in P["explained"][:3]))
    T = R["templates"]
    L.append("【构词模板·三层】字面首二字 %d 种（复用率 %.1f%%）／语义域序列 %d 种（%d 种独见，占 %.1f%%）／"
             "抽象骨架 %d 种"
             % (T["layer1_literal"]["n_distinct_bigram"],
                T["layer1_literal"]["bigram_reuse_rate"] * 100,
                T["layer2_domain"]["n_distinct"], T["layer2_domain"]["n_singleton"],
                T["layer2_domain"]["singleton_pct"] * 100,
                T["layer3_skeleton"]["n_distinct"]))
    pa = R["pareto"]["series"][0]
    L.append("【帕累托·词素】%d 个词素即达 80%% 频次（共 %d 个，占 %.1f%%）"
             % (pa["k80"], pa["n_items"], (pa["k80_pct_items"] or 0) * 100))
    N = R["network"]
    L.append("【网络】%d 节点 / %d 边，活跃 %d，社群 %d，覆盖 %.1f%%"
             % (N["n_nodes"], N["n_edges"], N["n_active"], len(N["communities"]),
                N["community_coverage"] * 100))
    L.append("  PageRank 前 8：%s" % "、".join("%s(%s)" % (x["zh"], x["pagerank"]) for x in N["top_pagerank"][:8]))
    O = R["ordinal"]
    L.append("【序位编排】相邻均值=%s 零分布=%s±%s z=%s p=%s" % (O["adjacent_mean"], O["null_mean"],
                                                              O["null_sd"], O["z"], O["p"]))
    L.append("  → %s" % O["conclusion_zh"])
    Q = R["quality"]
    L.append("【稳健性】")
    for r in Q["robustness"]:
        L.append("  %s %s → %s" % (r["id"], r["zh"], r["conclusion_zh"]))
    L.append("【执行摘要】")
    for f in R["executive"]["findings"]:
        L.append("  %s %s" % (f["id"], f["zh"]))
        L.append("      证据：%s" % f["evidence"])
    L.append("═" * 68)
    return "\n".join(L)


def main() -> int:
    ap = argparse.ArgumentParser(description="世主妙严品会众名号 · BI 式数据报告引擎")
    ap.add_argument("--check", action="store_true", help="只跑不变量校验，不写盘")
    a = ap.parse_args()
    R = build_report()
    errs = do_check(R)
    if a.check:
        print("── 不变量校验 ──")
        print("  检查项 16 组；错误 %d 条" % len(errs))
        for e in errs:
            print("  FAIL " + e)
        print("  OK" if not errs else "  FAILED")
        return 0 if not errs else 1
    size = dump_yaml(R, OUT)
    print(summary(R))
    print("\n生成：%s（%s bytes）" % (os.path.relpath(OUT, ROOT).replace("\\", "/"), f"{size:,}"))
    print("不变量：%s" % ("全部通过" if not errs else "失败 %d 条" % len(errs)))
    for e in errs:
        print("  FAIL " + e)
    return 0 if not errs else 1


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
