# -*- coding: utf-8 -*-
"""_e16_full.py — L.196 第十六部《梵行品》充实批：八十/六十全文结构化 dump＋澄观疏窗口
   仿 _e15_full.py 范式（SKIP-tag 平文器 · CJK-only 前向游标 · 限品界防 byline 串味）
   八十品界：梵行品第十六 → 初發心功德品第十七（卷第十七·短品）
   六十品界：T09n0278_juan8「大方廣佛華嚴經梵行品第十二」→「大方廣佛華嚴經卷第八」尾题
   疏窗口：T1735 NFKD「梵行品第十六」→「初發心功德品第十七」
"""
import io, re, unicodedata
import xml.etree.ElementTree as ET

OUT = io.open('_e16_dump.txt', 'w', encoding='utf-8')
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

def cjk(s):
    return ''.join(ch for ch in s if '\u4e00' <= ch <= '\u9fff')

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
ONLY = lambda s: ''.join(ch for ch in s if '\u4e00' <= ch <= '\u9fff')
fullC = ONLY(full)

# ── 八十品界（梵行品第十六 → 初發心功德品第十七）──
iC = fullC.find('梵行品第十六')
kC = fullC.find('初發心功德品第十七', iC + 6)
assert iC > 0 and kC > iC, (iC, kC)
emit('== 八十品界(CJK口径) @%d–%d · CJK%d ==' % (iC, kC, kC - iC))

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

# body80 for downstream use
body80 = fullC[iC:kC]
emit('== body80 len=%d ==' % len(body80))

# ── 六十侧（卷八·梵行品第十二·至卷题止）──
j8 = io.open('data/references/cbeta_txt/T09n0278_juan8.txt', encoding='utf-8').read()
lines8 = [l for l in j8.splitlines() if not l.startswith('#')]
s12 = e12 = None
for n, l in enumerate(lines8):
    ls = l.strip()
    if '梵行品第十二' in ls and s12 is None:
        s12 = n
    elif s12 is not None and n > s12 and ('品第' in ls or '卷第八' in ls):
        e12 = n
        break
if e12 is None:
    e12 = len(lines8)
emit('== 六十品界 juan8 行 %d–%d ==' % (s12, e12))
body60 = [l for l in lines8[s12:e12] if l.strip()]
cjk60 = sum(len(cjk(l)) for l in body60)
emit('== 六十侧 CJK 计 %d · 有效行计 %d ==' % (cjk60, len(body60)))
for n, l in enumerate(body60):
    emit('[60-%03d|CJK%d] %s' % (n, len(cjk(l)), l.strip()))

# ── 澄观疏窗口（T1735·NFKD 归一·60 字标尺）──
shu = io.open('data/references/cbeta_txt/T1735_澄观_华严经疏.txt', encoding='utf-8').read()
def norm(ch):
    d = unicodedata.normalize('NFKD', ch)
    return d[0] if d else ch
nsh = ''.join(norm(c) for c in shu)
assert len(nsh) == len(shu)
a = nsh.find('梵行品第十六')
b = nsh.find('初發心功德品第十七', a + 5)
assert 0 < a < b, (a, b)
emit('== 疏窗口(nsh 口径) %d–%d · 疏文长 %d ==' % (a, b, b - a))
win = nsh[a:b]
for n in range(0, len(win), 60):
    emit('[SH-%04d] %s' % (n, win[n:n+60]))

OUT.close()
print('E16_FULL done · units=%d · p60=%d · shun=%d · body80=%d' % (len(units), len(body60), len(win), len(body80)))
