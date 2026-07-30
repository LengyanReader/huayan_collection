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
    li = p.get('lineage_branch')
    # Multi-lineage persons: primary in 贤首宗高原法系, secondary shown as ghost
    multi=[]
    if p['id']=='person_042': li='贤首宗高原法系'; multi=['临济宗']
    if p['id']=='person_019': li='临济宗'
    if p['id']=='person_044': li='月霞系'; multi=['临济宗']  # 真禅: 月霞系+临济
    if p['id']=='person_003': li='华严五祖'; multi=['译师']  # 法藏: 五祖+参与译场
    nodes.append({
        'id': p['id'], 'n': p['name_zh'], 'dy': p.get('dynasty', ''), 'ti': p.get('title', '') or '',
        'li': li, 'multi': multi, 'tp': p.get('type', 'practitioner'),
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
# ── Additional persons: 福慧寺 体化性果 ──
nodes.append({'id':'person_f01','n':'思元慧三','dy':'近现代','ti':'高原法系40世·福慧寺开山','li':'贤首宗高原法系','tp':'patriarch','b':1901,'d':1986,'bio':'宛平人，俗姓霍。北京广善寺第11代住持。1948年赴台，创树林福慧寺。民国37年来台时已47岁，随身仅带一尊华严三圣像。为高原法系在台根本道场开创者。','wk':[]})
nodes.append({'id':'person_f02','n':'体化性果','dy':'当代','ti':'福慧寺第三代住持','li':'贤首宗高原法系','tp':'patriarch','b':1950,'d':None,'bio':'钦因长老法嗣。福慧寺第三代住持。继承贤首宗高原法系在台弘法事业。','wk':[]})
edges.append({'s':'person_f01','t':'person_041','r':'MASTER','li':'贤首宗高原法系'})
edges.append({'s':'person_041','t':'person_f02','r':'MASTER','li':'贤首宗高原法系'})

# Update 钦因 birth year and bio
for n in nodes:
    if n['id']=='person_041':
        n['b']=1928
        n['bio']='北京人，俗名阎凤麟。贤首宗高原法系第41世。2008年9月21日于台北大华严寺举行传法大典，将法脉衣钵传予海云继梦(42世)。'

# ── Additional persons: Japan lineage ──
nodes.append({'id':'person_j01','n':'良弁','dy':'唐/日本','ti':'东大寺初代别当','li':'日本华严','tp':'patriarch','b':689,'d':773,'bio':'审祥弟子。东大寺开山。主持《华严经》讲说。','wk':[]})
nodes.append({'id':'person_j02','n':'实忠','dy':'日本','ti':'东大寺二代','li':'日本华严','tp':'patriarch','b':726,'d':800,'bio':'良弁弟子。继承东大寺华严教学。','wk':[]})
nodes.append({'id':'person_j03','n':'等定','dy':'日本','ti':'东大寺华严','li':'日本华严','tp':'patriarch','b':800,'d':870,'bio':'日本华严宗传承者。','wk':[]})
nodes.append({'id':'person_j04','n':'圣宝','dy':'日本','ti':'醍醐寺开山','li':'日本华严','tp':'patriarch','b':832,'d':909,'bio':'理源大师。兼传真言与华严。','wk':[]})
nodes.append({'id':'person_j05','n':'观贤','dy':'日本','ti':'东大寺别当','li':'日本华严','tp':'patriarch','b':853,'d':925,'bio':'东大寺华严教学之中兴。','wk':[]})

# ── Additional persons: contemporary scholars ──
nodes.append({'id':'person_s01','n':'魏道儒','dy':'当代','ti':'中国社科院学部委员','li':'当代学者','tp':'scholar','b':1955,'d':None,'bio':'中国社会科学院学部委员。著有《中国华严宗通史》。','wk':['中国华严宗通史']})
nodes.append({'id':'person_s02','n':'王颂','dy':'当代','ti':'北京大学教授','li':'当代学者','tp':'scholar','b':1965,'d':None,'bio':'北京大学哲学系教授。华严思想与佛教史研究。','wk':[]})
nodes.append({'id':'person_s03','n':'邱高兴','dy':'当代','ti':'中国人民大学教授','li':'当代学者','tp':'scholar','b':1966,'d':None,'bio':'中国人民大学哲学院教授。华严宗与佛教中国化研究。','wk':['华严宗与佛教中国化']})
nodes.append({'id':'person_s04','n':'张文良','dy':'当代','ti':'中国人民大学教授','li':'当代学者','tp':'scholar','b':1966,'d':None,'bio':'中国人民大学佛教与宗教学理论研究所教授。华严思想研究。','wk':[]})

# ── Additional persons: 元晓(新罗) + 慧苑(唐) + 续法(清) ──
nodes.append({'id':'person_060','n':'元晓','dy':'唐/新罗','ti':'新罗华严学僧','li':'高丽华严','tp':'scholar','b':617,'d':686,'bio':'新罗学僧。与义湘同代，二人曾结伴入唐但中途折返。后自悟大乘起信论奥义。著华严经疏、起信论疏，与法藏、慧远并称东亚起信论三大疏。对朝鲜半岛华严思想影响深远。','wk':['华严经疏','大乘起信论疏','十门和诤论']})
nodes.append({'id':'person_070','n':'慧苑','dy':'唐','ti':'法藏弟子·华严异解者','li':'华严五祖','tp':'scholar','b':673,'d':743,'bio':'法藏上首弟子。著续华严经略疏刊定记，改五教为四教、以十门代十玄。澄观在华严经疏中系统批判其说。慧苑异解是推动澄观集大成的关键思想动力。','wk':['续华严经略疏刊定记','华严旋澓章']})
nodes.append({'id':'person_080','n':'续法','dy':'清','ti':'清代华严集大成者','li':'华严五祖','tp':'patriarch','b':1641,'d':1728,'bio':'清代华严宗最重要弘传者。字柏亭，号灌顶，仁和人。著贤首五教仪系统整理法藏判教；编华严宗佛祖传梳理传承谱系。讲华严经二十余遍，为清代华严学集大成者。','wk':['贤首五教仪','华严宗佛祖传','法界宗莲花章']})

# Edge: Japan lineage chain
edges.append({'s':'person_050','t':'person_j01','r':'MASTER','li':'日本华严'})
edges.append({'s':'person_j01','t':'person_j02','r':'MASTER','li':'日本华严'})
edges.append({'s':'person_j02','t':'person_j03','r':'MASTER','li':'日本华严'})
edges.append({'s':'person_j03','t':'person_j04','r':'INFLUENCE','li':'日本华严'})
edges.append({'s':'person_j03','t':'person_j05','r':'MASTER','li':'日本华严'})

# Edges: 元晓 慧苑 续法
edges.append({'s':'person_003','t':'person_070','r':'MASTER','li':'华严五祖'})
edges.append({'s':'person_070','t':'person_004','r':'INFLUENCED','li':'华严五祖'})
edges.append({'s':'person_001','t':'person_060','r':'INFLUENCED','li':'华严五祖'})
edges.append({'s':'person_021','t':'person_080','r':'INFLUENCED','li':'华严五祖'})

# Location: 东大寺
locs.append({'id':'l_nara','n':'奈良东大寺','lat':34.69,'lng':135.84,'tp':'temple','dy':'唐/日本','ds':'日本华严宗本山。审祥首次讲说《华严经》之处。','ps':['person_050','person_j01','person_j02']})

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

# ── Save external JSON (for future fetch-based loading) ──
with open(os.path.join(ROOT, 'web', 'demo', 'graph.json'), 'w', encoding='utf-8') as f:
    f.write(GRAPH)
with open(os.path.join(ROOT, 'web', 'demo', 'gap.json'), 'w', encoding='utf-8') as f:
    f.write(GAP)

# ── Assemble (inline embed for backward compat) ──
data_js = data_js.replace('__GRAPH__', GRAPH).replace('__GAP__', GAP)
# Strip any stray leading characters from source files
def clean(s):
    while s and s[0] not in '<':
        s = s[1:]
    return s

frontier_js = read_src('frontier.js')
html = clean(template_top) + data_js + lineage_js + gap_js + practice_js + frontier_js + init_js + clean(template_bot)

out = os.path.join(ROOT, 'web', 'demo', 'index.html')
with open(out, 'w', encoding='utf-8') as f:
    f.write(html)

print(f'OK  {out}')
print(f'    {len(html):,} bytes | {len(nodes)} persons | {len(edges)} edges | {len(locs)} locations')
