#!/usr/bin/env python3
"""Build web/demo/index.html from src/ files + data/ directory.
Run from project root: python web/demo/scripts/build.py
"""
import json, yaml, os

ROOT = os.getcwd()
SRC = os.path.join(ROOT, 'web', 'demo', 'src')
DATA_DIR = os.path.join(ROOT, 'data')

def read_src(name):
    with open(os.path.join(SRC, name), encoding='utf-8') as f:
        return f.read()

# ── Load source files ──
template_top = read_src('template_top.html')
data_js      = read_src('data.js')
lineage_js   = read_src('lineage.js')
gap_js       = read_src('gap.js')
practice_js  = read_src('practice.js')
init_js      = read_src('init.js')
template_bot = read_src('template_bottom.html')

# ── Build GRAPH data ──
with open(os.path.join(DATA_DIR, 'knowledge_graph', 'personas.json'), encoding='utf-8') as f:
    personas = json.load(f)
with open(os.path.join(DATA_DIR, 'knowledge_graph', 'lineages.json'), encoding='utf-8') as f:
    lineages = json.load(f)
with open(os.path.join(DATA_DIR, 'knowledge_graph', 'locations.json'), encoding='utf-8') as f:
    locations = json.load(f)
with open(os.path.join(DATA_DIR, 'translation', 'diff_matrix.yaml'), encoding='utf-8') as f:
    diff = yaml.safe_load(f)

nodes = []
for p in personas['persons']:
    nodes.append({
        'id': p['id'], 'n': p['name_zh'], 'dy': p.get('dynasty', ''), 'ti': p.get('title', '') or '',
        'li': p.get('lineage_branch'), 'tp': p.get('type', 'practitioner'),
        'b': p.get('birth_year'), 'd': p.get('death_year'),
        'bio': (p.get('biography', '') or '')[:150], 'wk': (p.get('key_works') or [])[:2]
    })

edges = []
for lin in lineages['lineages']:
    for e in lin['edges']:
        if e['from'] == e['to']: continue
        r = e['relation']
        if r not in ('MASTER_OF', 'INFLUENCED', 'LINEAGE', 'CONTEMPORARY'): r = 'MASTER'
        edges.append({'s': e['from'], 't': e['to'], 'r': r, 'li': lin['name']})

locs = []
for loc in locations['locations']:
    locs.append({
        'id': loc['id'], 'n': loc['name_zh'], 'lat': loc['lat'], 'lng': loc['lng'],
        'tp': loc.get('type', 'temple'), 'dy': loc.get('dynasty', ''),
        'ds': (loc.get('description', '') or '')[:120], 'ps': loc.get('related_persons', [])
    })
locs.append({'id': 'l_h', 'n': '南投大华严寺', 'lat': 23.92, 'lng': 120.88, 'tp': 'temple', 'dy': '当代',
             'ds': '海云继梦导师。普贤乘根本道场。', 'ps': ['person_042']})
locs.append({'id': 'l_f', 'n': '台北福慧寺', 'lat': 24.98, 'lng': 121.42, 'tp': 'temple', 'dy': '当代',
             'ds': '钦因长老住持。', 'ps': ['person_041', 'person_043']})

colors = {'华严五祖': '#b8863c', '华严莲社': '#5e8b9e', '月霞系': '#7a9ec0', '李通玄系': '#c8893e',
          '高丽华严': '#6d9a6e', '日本华严': '#8b7a9e', '贤首宗高原法系': '#c46b5d', '临济宗': '#d48476',
          '慈舟系': '#8b7a9e', '译师': '#a09080', '印度源流': '#9e8b6e', '当代学者': '#b0a898', 'null': '#b0a898'}

GRAPH = json.dumps({'nodes': nodes, 'edges': edges, 'locations': locs, 'lineage_colors': colors}, ensure_ascii=False)

# ── Build GAP data ──
gap_chapters = []
for ch in diff.get('chapters', []):
    dt = ch.get('diff_type', '')
    if dt in ('A', 'B', 'C'):
        gap_chapters.append({'bo': ch.get('order'), 'z80': ch.get('order_zh_80'),
                             'ti': ch.get('title_zh', ''), 'sa': ch.get('title_sa', ''),
                             'tp': dt, 'sm': (ch.get('diff_summary', '') or '')[:150]})

GAP = json.dumps({
    'vs': [{'n': '藏文德格版 (Toh 44)', 'c': 45, 'v': '4册', 't': '胜友、智军', 'p': '9世纪初'},
           {'n': '汉文八十华严 (T10n0279)', 'c': 39, 'v': '80卷', 't': '实叉难陀', 'p': '699年'},
           {'n': '汉文六十华严 (T09n0278)', 'c': 34, 'v': '60卷', 't': '佛驮跋陀罗', 'p': '420年'},
           {'n': '汉文四十华严 (T10n0293)', 'c': 1, 'v': '40卷', 't': '般若', 'p': '798年'}],
    'sm': {'A': 2, 'B': 3, 'C': 3, 'D': 1, 'E': 32}, 'cs': gap_chapters,
    'wn': ['⚠ T0309 法藏判为非十住品亦非十地品']
}, ensure_ascii=False)

# ── Assemble ──
data_js = data_js.replace('__GRAPH__', GRAPH).replace('__GAP__', GAP)
html = template_top + data_js + lineage_js + gap_js + practice_js + init_js + template_bot

out = os.path.join(ROOT, 'web', 'demo', 'index.html')
with open(out, 'w', encoding='utf-8') as f:
    f.write(html)

print(f'OK  {out}')
print(f'    {len(html):,} bytes | {len(nodes)} persons | {len(edges)} edges | {len(locs)} locations')
