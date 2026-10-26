# -*- coding: utf-8 -*-
"""_e18_full.py — L.198 第十八部《明法品》充实批：八十全文结构化 dump＋澄观疏窗口
   仿 _e17_full.py 范式（SKIP-tag 平文器 · CJK-only 前向游标 · 限品界防 byline 串味）
   八十品界：明法品第十八 → 昇夜摩天宮品第十九（卷第十八·第三会收束品·会末衔接第四会）
   六十品界：明法品第十四（拟在卷九·本仓 cbeta_txt 仅入库卷一–八）〔待核〕
   疏窗口：T1735 NFKD「明法品第十八」→「夜摩天宮品」次品题
"""
import io, re, unicodedata
import xml.etree.ElementTree as ET

OUT = io.open('_e18_dump.txt', 'w', encoding='utf-8')
def emit(*a):
    OUT.write(' '.join(str(x) for x in a) + '\n')

SKIP = {'note', 'rdg', 'mulu', 'pb', 'anchor', 'app'}

def clean(s):
    return re.sub(r'\s', ' ', s).strip()

def flat(el):
    acc = []
    def walk(e):
        tag = e.tag.split('}')[-1]
        if tag in SKIP:
            return
        if tag == 'lb':
            acc.append(' ')
        if e.text:
            acc.append(e.text)
        for c in e:
            walk(c)
            if c.tail:
                acc.append(c.tail)
    walk(el)
    return ''.join(acc)

ONLY = lambda s: ''.join(ch for ch in s if '\u4e00' <= ch <= '\u9fff')
norm = lambda ch: (unicodedata.normalize('NFKD', ch)[0] if unicodedata.normalize('NFKD', ch) else ch)

def find_first(txt, cands, start=0):
    """在 cands 里取最先出现的 marker·返回 (pos, marker)"""
    best, bmark = -1, None
    for c in cands:
        p = txt.find(c, start)
        if p >= 0 and (best < 0 or p < best):
            best, bmark = p, c
    return best, bmark

acc = []
def walk(el):
    tag = el.tag.split('}')[-1]
    if tag in SKIP:
        return
    if tag == 'lb':
        acc.append(' ')
    if el.text:
        acc.append(el.text)
    for c in el:
        walk(c)
        if c.tail:
            acc.append(c.tail)
walk(ET.parse('data/references/cbeta/T10n0279.xml').getroot())
full = ''.join(acc)
fullC = ONLY(full)

# ── 八十品界（明法品第十八 → 昇/升夜摩天宮品第十九）──
iC = fullC.find('明法品第十八')
kC, kmark = find_first(fullC, ['昇夜摩天宮品第十九', '升夜摩天宮品第十九'], iC + 6)
assert iC > 0 and kC > iC, (iC, kC)
emit('== 八十品界(CJK口径) @%d–%d · CJK%d · 次品题marker=%s ==' % (iC, kC, kC - iC, kmark))

units = []
seen = set()
root = ET.parse('data/references/cbeta/T10n0279.xml').getroot()
for el in root.iter():
    tag = el.tag.split('}')[-1]
    if tag in ('p', 'lg', 'head', 'byline'):
        t = flat(el)
        tc = ONLY(t)
        if len(tc) < 2:
            continue
        pos = fullC.find(tc, iC)
        if pos < 0 or pos >= kC or pos in seen:
            continue
        seen.add(pos)
        units.append((tag, pos, clean(t), tc))
units.sort(key=lambda u: u[1])
emit('== 八十侧单元 %d 个 ==' % len(units))
for n, (tag, pos, t, tc) in enumerate(units):
    emit('[80-%03d|%s|@%d|CJK%d] %s' % (n, tag, pos, len(tc), t))

body80 = fullC[iC:kC]
emit('== body80 len=%d ==' % len(body80))

# ── 六十侧探针：明法品第十四存疑卷次·入库档内直搜 ──
m60 = []
for juan in range(1, 9):
    fn = 'data/references/cbeta_txt/T09n0278_juan%d.txt' % juan
    try:
        raw = io.open(fn, encoding='utf-8').read()
    except OSError:
        raw = ''
        emit('== 卷档缺: %s ==' % fn)
        continue
    n = ''.join(norm(c) for c in raw)
    p = n.find('明法品')
    if p >= 0:
        m60.append((juan, p, n[p:p+20]))
emit('== 六十侧入库卷一–八内「明法品」直搜: %s ==' % (m60 if m60 else '无命中→拟在卷九·未入库'))

# ── 澄观疏窗口（T1735·NFKD 归一·60 字标尺）──
shu = io.open('data/references/cbeta_txt/T1735_澄观_华严经疏.txt', encoding='utf-8').read()
nsh = ''.join(norm(c) for c in shu)
assert len(nsh) == len(shu)
a = nsh.find('明法品第十八')
b, bmark = find_first(nsh, ['昇夜摩天宮品第十九', '升夜摩天宮品第十九', '佛昇夜摩天宮'], a + 5)
assert 0 < a < b, (a, b)
emit('== 疏窗口(nsh 口径) %d–%d · 疏文长 %d · 次品题=%s ==' % (a, b, b - a, bmark))
win = nsh[a:b]
for n in range(0, len(win), 60):
    emit('[SH-%04d] %s' % (n, win[n:n+60]))

OUT.close()
print('E18_FULL done · units=%d · body80=%d · shun=%d' % (len(units), len(body80), len(win)))
