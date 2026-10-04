#!/usr/bin/env python3
# scratch 文本分析层: network + complex-systems analysis of 世主妙嚴品.
# Substrate: canonical ARTICLE_ASSEMBLY (40 classes / 414 members, T279-verified)
#            + T279 品 continuous text (89k chars).
# Outputs scripts/_analysis_out.json + human summary.
import re, io, sys, json, math, random, unicodedata
from collections import Counter, defaultdict
import numpy as np
import networkx as nx
from networkx.algorithms.community import greedy_modularity_communities, modularity
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

base = r'c:\DA_Practice\huayan_collection'
RAD = {'\u2ef6':'日','\u2ef7':'月','\u2ed1':'長','\u2ec5':'門','\u2eda':'頁','\u2edb':'風','\u2ed8':'飛','\u2ec3':'食'}
def norm(s):
    s = unicodedata.normalize('NFKC', s); return ''.join(RAD.get(c, c) for c in s)
def cjk(s):
    return ''.join(c for c in norm(s) if '\u3400' <= c <= '\u9fff')

asm = json.load(open(base + r'\scripts\_assembly.json', encoding='utf-8'))
classes = asm['classes']
raw = open(base + r'\data\references\cbeta\T10n0279.xml', encoding='utf-8').read()
txt = norm(re.sub(r'<[^>]+>', '', raw))
seg = txt[txt.find('世主妙嚴品'): txt.find('如來名號品')]
body = cjk(seg)                      # continuous CJK-only text
out = {}

# ---------- helper: co-occurrence graph from token list, window w ----------
def cooc_graph(strings, w=None):
    """undirected weighted graph; chars co-occurring within window w of each string.
    w=None -> whole string is the window."""
    E = Counter()
    for s in strings:
        ch = list(s)
        n = len(ch)
        win = n if w is None else min(w, n)
        for i in range(n):
            for j in range(i + 1, min(n, i + win)):
                if ch[i] != ch[j]:
                    E[(ch[i], ch[j])] += 1
    G = nx.Graph()
    for (a, b), v in E.items():
        G.add_edge(a, b, weight=v)
    return G

# ---------- G1: morpheme co-occurrence inside member names ----------
names = [cjk(m['name']) for c in classes for m in c.get('members', []) if m.get('name')]
catnames = [cjk(c['cat']) for c in classes]
G1 = cooc_graph(names)
def stats(G):
    n, m = G.number_of_nodes(), G.number_of_edges()
    cc = nx.average_clustering(G) if n else 0
    if nx.is_connected(G):
        pl = nx.average_shortest_path_length(G); diam = nx.diameter(G)
    else:
        sg = max(nx.connected_components(G), key=len)
        H = G.subgraph(sg); pl = nx.average_shortest_path_length(H); diam = nx.diameter(H)
    comp = nx.number_connected_components(G)
    return dict(n=n, m=m, avg_deg=2*m/n if n else 0, density=nx.density(G),
                clustering=cc, avg_path=pl, diameter=diam, components=comp)

def powerlaw_mle(degseq):
    """Clauset-Shalizi-Newman discrete MLE exponent, xmin by minimizing KS."""
    xs = np.array([d for d in degseq if d >= 1], float)
    if len(xs) < 10: return None
    def alpha_hat(xmin):
        xt = xs[xs >= xmin]
        if len(xt) < 3: return None, len(xt)
        a = 1 + len(xt)/np.sum(np.log(xt/(xmin-0.5)))
        return a, len(xt)
    cands = sorted(set(xs[xs >= 2]))[:30]
    best = None
    for xmin in cands:
        a, cnt = alpha_hat(xmin)
        if a is None: continue
        # KS between empirical tail and fitted CDF
        xt = np.sort(xs[xs >= xmin]); nT = len(xt)
        cdf = 1 - (xt/xmin)**(a-1)
        ks = np.max(np.abs(np.arange(1, nT+1)/nT - cdf))
        if best is None or ks < best[0]:
            best = (ks, a, xmin, cnt)
    if not best: return None
    ks, a, xmin, cnt = best
    # log-log OLS R2 for readability
    c = Counter(int(d) for d in degseq if d >= 1)
    rx = np.log(np.array(sorted(c), float)); ry = np.log(np.array([c[k] for k in sorted(c)], float))
    r = np.corrcoef(rx, ry)[0,1] if len(rx) > 2 else float('nan')
    return dict(alpha=round(a,3), xmin=xmin, ks=round(ks,4), n_tail=cnt, loglog_r=round(float(r),3))

def smallworld(G, seeds=20):
    n, m = G.number_of_nodes(), G.number_of_edges()
    if n < 3: return None
    C = nx.average_clustering(G)
    L = nx.average_shortest_path_length(G) if nx.is_connected(G) else np.nan
    Cr, Lr = [], []
    nodes = list(G.nodes)
    for k in range(seeds):
        random.seed(k)
        R = nx.gnm_random_graph(n, m)
        if not nx.is_connected(R): R = max(nx.connected_components(R), key=lambda c: R.subgraph(c).number_of_nodes())
        Rn = G.subgraph([]); pass
        Rg = nx.Graph(); 
        R = nx.gnm_random_graph(n, m)
        # largest component
        comps = list(nx.connected_components(R))
        big = max(comps, key=len); Rb = R.subgraph(big).copy()
        Cr.append(nx.average_clustering(Rb))
        Lr.append(nx.average_shortest_path_length(Rb) if nx.is_connected(Rb) else np.nan)
    C_rand = float(np.nanmean(Cr)); L_rand = float(np.nanmean(Lr))
    gamma = C/C_rand if C_rand else np.nan
    delta = L/L_rand if L_rand else np.nan
    sigma = (gamma*delta) if (gamma and delta) else np.nan
    return dict(C=round(C,4), L=round(L,4), C_rand=round(C_rand,4), L_rand=round(L_rand,4),
                gamma=round(gamma,3), delta=round(delta,3), sigma=round(sigma,3))

s1 = stats(G1)
out['G1_names_morpheme'] = dict(**s1,
    smallworld=smallworld(G1),
    top_degree=[(v, d) for v, d in sorted(G1.degree(), key=lambda x: -x[1])[:15]],
    top_between=[(v, round(d,1)) for v, d in sorted(nx.betweenness_centrality(G1).items(), key=lambda x:-x[1])[:12]])
com1 = list(greedy_modularity_communities(G1))
out['G1_communities'] = dict(count=len(com1), modularity=round(modularity(G1, com1), 4),
    sizes=sorted([len(c) for c in com1], reverse=True)[:8])

# ---------- G3: whole-text sliding-window char co-occurrence ----------
W = 7
E3 = Counter()
b = body
for i in range(len(b)):
    for j in range(i+1, min(len(b), i+W)):
        if b[i] != b[j]: E3[(b[i], b[j])] += 1
G3 = nx.Graph()
for (a2, b2), v in E3.items(): G3.add_edge(a2, b2, weight=v)
s3 = stats(G3)
out['G3_text_window'] = dict(W=W, **s3,
    top_degree=[(v, d) for v, d in sorted(G3.degree(), key=lambda x:-x[1])[:15]],
    vocabulary=len(set(b)), tokens=len(b))
com3 = list(greedy_modularity_communities(G3))
out['G3_communities'] = dict(count=len(com3), modularity=round(modularity(G3, com3), 4))

# ---------- G2: assembly sequence (directed) + doctrinal partition ----------
G2 = nx.DiGraph()
for c in classes:
    G2.add_node(c['cat'] and c['cat'] + '#' + str(c['idx']))
seq = [c['cat'] + '#' + str(c['idx']) for c in classes]
for x, y in zip(seq, seq[1:]): G2.add_edge(x, y)
out['G2_sequence'] = dict(nodes=len(G2), edges=G2.number_of_edges(),
    is_directed_acyclic_path=nx.is_directive if False else (G2.number_of_edges()==len(G2)-1))
# realm / group community -> modularity on undirected projection where two classes share realm
U2 = nx.Graph()
for c in classes:
    U2.add_node(c['idx'])
for c1 in classes:
    for c2 in classes:
        if c1['idx'] < c2['idx'] and c1.get('realm') == c2.get('realm'):
            U2.add_edge(c1['idx'], c2['idx'])
part_realm = [set(c['idx'] for c in classes if c.get('realm') == r) for r in set(c.get('realm') for c in classes)]
part_group = [set(c['idx'] for c in classes if c.get('group') == g) for g in set(c.get('group') for c in classes)]
out['G2_realm_partition'] = dict(realms=sorted(set(str(c.get('realm')) for c in classes)),
    n_realm=len(part_realm), Q_realm=round(modularity(U2, [p for p in part_realm if p]), 4))
out['G2_group_partition'] = dict(groups=sorted(set(str(c.get('group')) for c in classes)),
    n_group=len(part_group), Q_group=round(modularity(U2, [p for p in part_group if p]), 4))

# ---------- complex-systems text signatures ----------
def zipf(series):
    c = Counter(series); items = sorted(c.values(), reverse=True)
    r = np.arange(1, len(items)+1, dtype=float); fr = np.array(items, dtype=float)
    R = np.corrcoef(np.log(r), np.log(fr))[0,1]
    slope = np.polyfit(np.log(r), np.log(fr), 1)[0]
    return dict(types=len(c), tokens=int(sum(items)), zipf_R=round(float(R),4),
                exponent=round(float(-slope),3))
morph_freq = [ch for nm in names for ch in nm]
out['zipf_names_morpheme'] = zipf(morph_freq)
out['zipf_text_chars'] = zipf(list(body))
# Shannon entropy
def ent(series):
    c = Counter(series); N = sum(c.values())
    H = -sum((v/N)*math.log2(v/N) for v in c.values())
    return round(H, 3)
out['entropy'] = dict(text_char_H=ent(list(body)), text_chars=body and len(set(body)),
                      names_morpheme_H=ent(morph_freq))
# Heaps' law over continuous text
tok = list(body); N = len(tok); uniq = 0; seen = set(); pts = []
step = max(1, N//40)
for i, t in enumerate(tok, 1):
    seen.add(t)
    if i % step == 0: pts.append((i, len(seen)))
xs = np.log([p[0] for p in pts]); ys = np.log([p[1] for p in pts])
heap_slope = float(np.polyfit(xs, ys, 1)[0])
out['heaps'] = dict(exponent=round(heap_slope, 3), V_final=len(seen), T_final=N)
# recursion / self-similarity motifs (因陀羅網 proxies) — verbatim source counts
def cnt(*subs): return sum(seg.count(x) for x in subs)
out['recurrence_motifs'] = dict(
    yiyi=cnt('一一'), yiqie=cnt('一切'), wuliang=cnt('無量','无量'),
    weichen=cnt('微塵'), haizhong=cnt('海中'), xianjian=cnt('中現','中見','現','見'),
    foshan=cnt('佛剎'), chongchong_note='一一/一切/無量 为层层互摄句式')
# multiplicity (count_expr) distribution -> heavy tail of 「數」 expressions
mult = Counter()
for c in classes:
    e = c.get('count_expr') or ''
    key = '微塵數' if '微塵' in e else ('不可思議' if '不可思議' in e else ('無量' if '無量' in e else ('有十' if '十佛世界' in e else ('三千' if '三千' in e else '其他'))))
    mult[key]+=1
out['multiplicity_classes'] = dict(mult)
# --- proper quantifier prefix from count_expr (heavy-tail of unbounded scale) ---
qcnt = Counter()
for c in classes:
    e = norm(c.get('count_expr') or '')
    if '十佛世界' in e: q = '十佛世界微塵數'
    elif '三千' in e: q = '三千大千世界'
    elif '不可思議' in e: q = '不可思議數'
    elif '無量' in e and '塵' not in e: q = '無量'
    elif '微塵' in e or '塵數' in e: q = '佛世界微塵數'
    else: q = '其他:' + e[:6]
    qcnt[q] += 1
out['quantifier_prefix'] = dict(qcnt)

# --- NON-circular community recovery: lexical class-similarity -> communities -> NMI vs realm ---
def jaccard(a, b):
    A, B = set(a), set(b); return len(A & B)/len(A | B) if A | B else 0
morphset = {c['idx']: set(cjk(''.join(m['name'] for m in c.get('members', []) if m.get('name')))) for c in classes}
idxs = [c['idx'] for c in classes]
realm_lab = {c['idx']: str(c.get('realm')) for c in classes}
group_lab = {c['idx']: str(c.get('group')) for c in classes}
def nmi(comm, labels):
    N = len(labels)
    def H(groups):
        tot = sum(len(g) for g in groups)
        return -sum((len(g)/tot)*math.log2(len(g)/tot) for g in groups if g)
    U = [set(c) for c in comm]
    Gg = defaultdict(set)
    for node, lab in labels.items(): Gg[lab].add(node)
    Gr = list(Gg.values())
    I = 0.0
    for u in U:
        for g in Gr:
            p = len(u & g)/N
            if p: I += p*math.log2(p/((len(u)/N)*(len(g)/N)))
    HC = H(U); HG = H(Gr)
    return I/math.sqrt(HC*HG) if HC and HG else 0
def build_L(TH):
    g = nx.Graph()
    for c in classes: g.add_node(c['idx'])
    for i in range(len(idxs)):
        for j in range(i+1, len(idxs)):
            s = jaccard(morphset[idxs[i]], morphset[idxs[j]])
            if s >= TH: g.add_edge(idxs[i], idxs[j], weight=s)
    return g
sweep = []
best = None
for TH in [0.12, 0.15, 0.18, 0.20, 0.22, 0.25, 0.28, 0.32]:
    g = build_L(TH)
    if g.number_of_edges() == 0: continue
    coms = list(greedy_modularity_communities(g))
    Q = modularity(g, coms)
    rec = dict(threshold=TH, edges=g.number_of_edges(), comm=len(coms), Q=round(Q, 4),
               NMI_realm=round(nmi(coms, realm_lab), 4), NMI_group=round(nmi(coms, group_lab), 4))
    sweep.append(rec)
    if best is None or Q > best['Q']: best = rec
out['lexical_similarity'] = dict(sweep=sweep, best=best)
out['class_sizes'] = dict(min_n=min(c.get('n_named',0) for c in classes),
                          max_n=max(c.get('n_named',0) for c in classes),
                          mean_n=round(np.mean([c.get('n_named',0) for c in classes]),2),
                          total_named=sum(c.get('n_named',0) for c in classes),
                          n_classes=len(classes))

# ---------- 会众名号数据剖面 (assembly-name data profile) ----------
# NOTE: purely quantitative profile of the 414 member names; doctrinal 归类见附录二,
#       构词矩阵见附录七·三 — no duplication, this feeds the network layer.
nlen = [len(x) for x in names if x]
bucket = Counter()
for x in nlen:
    bucket[str(x) if x <= 7 else '8+'] += 1
heads = Counter(x[0] for x in names if x)
tails = Counter(x[-1] for x in names if x)
morph = Counter(ch for x in names for ch in x)
# 〔本文判断〕 heuristic: names carrying a Sanskrit-transliteration cue
TRANS = ['那羅','摩天','闥婆','修羅','迦樓','佛陀','摩睺','優鉢','拘留','曼陀','三漫',
         '須彌','般遮','缽頭','摩訶','莎羅','由梨','目眞','目真','離婆','睒摩','尼拘',
         '陀羅','彌伽','蜜伽','薩','嚩','伽','呬']
ntrans = sum(1 for x in names if any(t in x for t in TRANS))
out['name_profile'] = dict(
    n_names=len(names), distinct=len(set(names)),
    len_mean=round(float(np.mean(nlen)), 2), len_median=int(np.median(nlen)),
    len_mode=int(Counter(nlen).most_common(1)[0][0]), len_min=min(nlen), len_max=max(nlen),
    len_dist={k: bucket[k] for k in sorted(bucket, key=lambda s: int(s.replace('+', '')))},
    heads_top12=heads.most_common(12), tails_top15=tails.most_common(15),
    morph_top25=morph.most_common(25),
    transliterated_approx=ntrans, semantic_approx=len(names) - ntrans,
    pu_prefixed=sum(1 for x in names if x.startswith('普')),
    per_group={str(g): sum(c.get('n_named', 0) for c in classes if c.get('group') == g)
               for g in sorted(set(c.get('group') for c in classes))},
    per_realm={str(r): sum(c.get('n_named', 0) for c in classes if c.get('realm') == r)
               for r in sorted(set(c.get('realm') for c in classes))},
)

json.dump(out, open(base + r'\scripts\_analysis_out.json','w',encoding='utf-8'), ensure_ascii=False, indent=1)
# summary print
for k in out:
    v = out[k]
    print('==', k, '==')
    if isinstance(v, dict):
        for kk, vv in v.items():
            if isinstance(vv, list) and len(str(vv))>90: vv=str(vv)[:90]+'...'
            print('   %-16s %s' % (kk, vv))
