# -*- coding: utf-8 -*-
"""《华严宗全方位研究》正文抽取式回源核验。
抽取 md 全部「…」引文（≥6 字），按 …… 切分片段，剥标点后对底本子串匹配。
底本（canonical 全在库）：T10n0279 八十华严 / T35n1733 探玄记 / T45n1866 教义分齐章
＋T35n1735 澄观疏（十玄古今差异实测）。访问 2026-11-22。"""
import os, re, sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
CAN = os.path.normpath(os.path.join(HERE, os.pardir, os.pardir, 'data', 'references', 'cbeta'))
MD = os.path.normpath(os.path.join(HERE, os.pardir, os.pardir, 'docs', '宗派研究', '华严宗全方位研究.md'))

PUNCT = set('，。、；：？！「」『』（）《》〈〉……—－·“”‘’ \u3000\n\r\t()[]0123456789一二三四五六七八九十')

def load(tid):
    xml = open(os.path.join(CAN, tid + '.xml'), encoding='utf-8').read()
    jp = [(m.start(), m.group(1)) for m in re.finditer(r'<cb:juan[^>]*n="(\d+)"', xml)]
    chars, it = [], False
    for ch in xml:
        if ch == '<': it = True
        elif ch == '>': it = False
        elif not it: chars.append(ch)
    return ''.join(chars), jp

def np(s):
    return ''.join(ch for ch in s if ch not in PUNCT)

def juan_of(jp_flat_text, jp, hn_idx):
    # 简易：以剥标点全文位置找 juan
    return None

md = open(MD, encoding='utf-8').read()
quotes = [(m.start(), m.group(1)) for m in re.finditer(r'「([^」]{6,})」', md)]
TEXTS = {tid: load(tid) for tid in ['T10n0279', 'T35n1733', 'T45n1866', 'T35n1735', 'T48n2015']}

total = ok = 0
misses = []
print('抽取引文 %d 条' % len(quotes))
for pos, q in quotes:
    total += 1
    line = md[:pos].count('\n') + 1
    # …… 切分：每段须命中任一底本
    frags = [f for f in re.split(r'……', q) if len(np(f)) >= 4]
    if not frags:
        frags = [q]
    bad = []
    for f in frags:
        hit = None
        for tid, (text, jp) in TEXTS.items():
            if np(text).find(np(f)) >= 0:
                hit = tid
                break
        if not hit:
            bad.append((f, None))
        else:
            bad.append((f, hit))
    miss = [f for f, h in bad if h is None]
    if miss:
        misses.append((line, q, miss))
        print('  [MISS] L%-4d %s' % (line, q[:44]))
        for f in miss:
            print('         └ 片段未中：%s' % f)
    else:
        ok += 1
        hits = ' '.join(sorted(set(h for _, h in bad)))
        print('  [ ok ] L%-4d → %s | %s' % (line, hits, q[:40]))

print('=' * 70)
print('严格核验 %d（ok %d / miss %d）' % (total, ok, len(misses)))

# ---- 十玄古今差异实测 ----
print('\n## 十玄门古今对照实测')
T35 = TEXTS['T35n1733'][0]
T35S = TEXTS['T35n1735'][0]
probes = [
    ('探玄记·廣狹自在無礙門', T35, '廣狹自在無礙門'),
    ('探玄记·隱密顯了俱成門', T35, '隱密顯了俱成門'),
    ('探玄记·祕密隱顯俱成門', T35, '祕密隱顯俱成門'),
    ('探玄记·因陀羅網法界門', T35, '因陀羅網法界門'),
    ('探玄记·主伴圓明具德門', T35, '主伴圓明具德門'),
    ('澄观疏·因陀羅網境界門', T35S, '因陀羅網境界門'),
    ('澄观疏·因陀羅網法界門', T35S, '因陀羅網法界門'),
    ('澄观疏·隱密顯了俱成門', T35S, '隱密顯了俱成門'),
    ('澄观疏·祕密隱顯俱成門', T35S, '祕密隱顯俱成門'),
    ('澄观疏·廣狹自在無礙門', T35S, '廣狹自在無礙門'),
]
for label, text, needle in probes:
    n = np(text).count(np(needle))
    print('  %-24s %s：%d 处' % (label, needle, n))
