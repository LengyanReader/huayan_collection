# -*- coding: utf-8 -*-
"""build_rufajie_can_guzhu.py — L.493 入法界品·五十三参子页 古注取窗

三源（均 epub 提取本·NFKC 归一＋剥页码家具）：
  疏 = T1735 澄观《华严经疏》（八十底本·入法界品疏带）
  论 = T1739 李通玄《新华严经论》（八十·入法界品论带）
  探 = T1733 法藏《探玄记》（六十底本·入法界品疏带·覆盖如实）
锚定：逐卡单调游标（沿行历次序），候选名形（长→短）：md「八十作X」→ n80+身份后缀 → n80（→变体）。
窗：锚点起 ~380 CJK 句界截断（。；），照录；记锚名与最近页码（<<<PAGE N>>>）。
产出 data/research/rufajie_can_guzhu.json；未命中如实记 miss，不代生成。
"""
import json
import re
import sys
import unicodedata

sys.stdout.reconfigure(encoding='utf-8')

JOURNEY = 'web/demo/articles/huayan-rufajie-journey.html'
OUT = 'data/research/rufajie_can_guzhu.json'
SRC = {
    'shu': ('data/references/cbeta_txt/T1735_澄观_华严经疏.txt', '澄观《华严经疏》T1735（八十）'),
    'yan': ('data/references/cbeta_txt/T1736_澄观_随疏演义钞.txt', '澄观《随疏演义钞》T1736（八十·疏之演义）'),
    'lun': ('data/references/cbeta_txt/T1739_李通玄_新华严经论.txt', '李通玄《新华严经论》T1739（八十）'),
    'tan': ('data/references/cbeta_txt/T1733_法藏_探玄记.txt', '法藏《探玄记》T1733（六十）'),
}
HAN = re.compile(r'[\u3400-\u9fff]')
PAGE = re.compile(r'<<<PAGE (\d+)>>>')


def han(s):
    return len(HAN.findall(s))


def load_norm(path):
    t = open(path, encoding='utf-8').read()
    pages = [(m.start(), m.group(1)) for m in PAGE.finditer(t)]
    t2 = PAGE.sub('', t)
    t2 = unicodedata.normalize('NFKC', t2)
    return t2, pages


def page_at(pages, pos, t):
    """剥页码前的字节位置近似映射（NFKC 长度变化可忽略·只作参考页码）。"""
    best = None
    for p, n in pages:
        if p <= pos:
            best = n
        else:
            break
    return best


def sentence_cut(text, limit):
    if han(text) <= limit:
        return text
    acc = 0
    for i, ch in enumerate(text):
        if HAN.match(ch):
            acc += 1
        if acc >= limit and ch in '。；':
            return text[:i + 1]
    return text[:limit]


# ── 旅程卡（54 卡·n40/n80/n60/role）──
t = open(JOURNEY, encoding='utf-8').read()
i = t.find('var RUFAJIE_DATA = ')
j = t.find('};', i)
cards = sorted(json.loads(t[i + len('var RUFAJIE_DATA = '):j + 1])['visits'], key=lambda v: v['card_no'])
assert [c['card_no'] for c in cards] == list(range(1, 55))

# P39 主页 md 的「八十作X」补形（长形优先）
md = open('docs/经学文献/华严经细读/第九会_逝多林_证入法界/华严经细读_第三十九部_入法界品.md', encoding='utf-8').read()
md_alt = {}
for m in re.finditer(r'^### 参(\d+)·[^\n]*?八十作([^·）\n]{2,14})', md, re.M):
    md_alt[int(m.group(1))] = m.group(2).strip()
md_alt60 = {}
for m in re.finditer(r'^### 参(\d+)·[^\n]*?六十作([^·）\n]{2,14})', md, re.M):
    md_alt60[int(m.group(1))] = m.group(2).strip()

ROLE_SUFX = {'比丘': '比丘', '比丘尼': '比丘尼', '長者': '長者', '居士': '居士', '優婆夷': '優婆夷',
             '王': '王', '婆羅門': '婆羅門', '仙人': '仙人', '外道': '外道', '船師': '船師',
             '童子': '童子', '童子師': '童子師', '童女': '童女', '女': '女', '釋女': '女',
             '夜神': '夜神', '天神': '', '地神': '地神', '天女': '天女', '林神': '神',
             '菩薩': '菩薩', '佛母': '夫人', '童子童女': '童子'}

# 特例补形（八十名与 T0293 名系差异·P39 §四/勘订）
EXTRA = {
    22: ['鬻香長者', '鬻香'],
    26: ['婆須蜜女', '婆須蜜'],
    25: ['師子嚬申', '嚬申'],
    32: ['婆珊', '婆珊那演底'],
    33: ['普德淨光', '普德淨光夜神'],
    34: ['喜目觀察眾生主', '喜目'],
    35: ['普救眾生妙德眼', '普救眾生'],
    37: ['守護一切城'],
    38: ['開敷一切樹花主夜神', '開敷一切樹花', '開敷'],
    39: ['大願精進', '大願精進力'],
    40: ['妙德圓滿神', '妙德圓滿'],
    44: ['天主光'],
    45: ['遍友'],
    51: ['德生童子', '德生'],
}

SOURCES = {}
for key, (path, label) in SRC.items():
    txt, pages = load_norm(path)
    starts = [m.start() for m in re.finditer('入法界品', txt)]
    if key == 'shu':
        band0 = min([p for p in starts if p > 600000] or [starts[-1]])
    elif key == 'yan':
        band0 = min([p for p in starts if p > 1000000] or [starts[-1]])
    else:
        band0 = max([p for p in starts if p > 400000] or [starts[-1]])
    SOURCES[key] = {'label': label, 'txt': txt, 'pages': pages, 'band0': band0,
                    'cursor': band0}
    print('%s band0=%d（%s 之后）' % (key, band0, label))


def find_anchor(skey, card):
    """单调游标取锚：候选名形长→短；返回 (pos, used) 或 (None, None)。"""
    S = SOURCES[skey]
    txt = S['txt']
    n = card['card_no']
    if n == 54 and skey in ('shu', 'yan', 'lun'):
        # 普賢摄归章为疏/论末段——单调首现会误落彌勒段，改取带内最末「普賢」
        p = txt.rfind('普賢', S['band0'])
        if p > S['cursor']:
            return p, '普賢（末段）'
        return None, None
    names = []
    if skey == 'tan' and n in md_alt60:
        names.append(md_alt60[n])
    if n in md_alt:
        names.append(md_alt[n])
    suf = ROLE_SUFX.get(card.get('role', ''), '')
    n80 = (card.get('n80') or '').strip()
    n60 = (card.get('n60') or '').strip()
    base = n80 if skey != 'tan' else n60
    if not base:
        return None, None
    if n in EXTRA:
        names += EXTRA[n]
    if suf and base + suf not in names:
        names.append(base + suf)
    names.append(base)
    if n == 33 and skey != 'shu' and skey != 'lun':
        pass
    for nm in names:
        if not nm:
            continue
        p = txt.find(nm, S['cursor'])
        if p >= 0:
            return p, nm
    return None, None


_TAIL_JUNK = re.compile(r'(CBETA 贊助.*$)|(\s*?(新華嚴經論|花嚴經探玄記|大方廣佛華嚴經疏|大方廣佛華嚴經隨疏演義鈔)卷第[一二三四五六七八九十百]+)', re.S | re.M)


def window(skey, pos, name):
    S = SOURCES[skey]
    txt = S['txt']
    raw = txt[pos:pos + 1600]
    ci = raw.find('CBETA 贊助')
    if ci > 0:
        raw = raw[:ci]
    raw = _TAIL_JUNK.sub('', raw)
    w = sentence_cut(raw, 380)
    pg = page_at(S['pages'], pos, txt)
    return {'anchor': name, 'char_pos': pos, 'page_ref': ('PDF/册页 ' + pg) if pg else '',
            'text': w, 'cjk': han(w)}


result = {'meta': {
    'date': '2026-11-17', 'batch': 'L.493',
    'sources': {k: v['label'] for k, v in SOURCES.items()},
    'band0': {k: v['band0'] for k, v in SOURCES.items()},
    'method': '逐卡单调游标（行历 54 卡次序）·候选名形长→短·NFKC 归一·句界截断 380·页码留痕',
    'note': '程序取窗·照录；引前须对 CBETA 原书核（epub 提取本·字准待校）。未命中如实记 miss。',
}, 'cards': {}}

for card in cards:
    n = card['card_no']
    entry = {}
    for skey in ('shu', 'yan', 'lun', 'tan'):
        pos, used = find_anchor(skey, card)
        if pos is None:
            entry[skey] = {'miss': True}
            continue
        w = window(skey, pos, used)
        entry[skey] = w
        SOURCES[skey]['cursor'] = pos + 1
    result['cards'][str(n)] = entry

cov = {k: sum(1 for e in result['cards'].values() if not e.get(k, {}).get('miss')) for k in ('shu', 'yan', 'lun', 'tan')}
print('覆盖：疏 %d/54 · 钞 %d/54 · 论 %d/54 · 探 %d/54' % (cov['shu'], cov['yan'], cov['lun'], cov['tan']))
misses = {n: [k for k in ('shu', 'yan', 'lun', 'tan') if e[k].get('miss')] for n, e in result['cards'].items() if any(e[k].get('miss') for k in ('shu', 'yan', 'lun', 'tan'))}
if misses:
    print('miss:', misses)

json.dump(result, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('written', OUT)
