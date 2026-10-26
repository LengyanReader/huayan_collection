# -*- coding: utf-8 -*-
"""_e16_stats.py — L.196 P16《梵行品》数据层实测（频计·名数·结构计数）"""
import io, re, unicodedata
import xml.etree.ElementTree as ET

SKIP = {'note', 'rdg', 'mulu', 'pb', 'anchor', 'app'}
ONLY = lambda s: ''.join(ch for ch in s if '\u4e00' <= ch <= '\u9fff')

# Rebuild fullC
acc = []
def walk(el):
    tag = el.tag.split('}')[-1]
    if tag in SKIP: return
    if tag == 'lb': acc.append(' ')
    if el.text: acc.append(el.text)
    for c in el:
        walk(c)
        if c.tail: acc.append(c.tail)
walk(ET.parse('data/references/cbeta/T10n0279.xml').getroot())
full = ''.join(acc)
fullC = ONLY(full)

iC = fullC.find('梵行品第十六')
kC = fullC.find('初發心功德品第十七', iC + 6)
body80 = fullC[iC:kC]
bodyP = ''.join(ch for ch in full[iC if False else 0:] if True)  # placeholder

# Use fullC slice as body (CJK only for frequency)
print(f'body80 CJK={len(body80)}')

# Frequency counts on body80
for kw in ['梵行', '佛子', '十法', '身', '語', '意', '佛', '法', '僧', '戒',
           '清淨', '觀察', '修習', '處非處', '如來', '菩提', '菩薩', '無上']:
    n = body80.count(kw)
    if n > 0:
        print(f'  「{kw}」 ×{n}')

# Unit-level CJK
units_cjk = [6, 50, 5, 669, 193]
print(f'\n== 单元 CJK 明细 ==')
tags = ['head', 'p-问', 'p-过渡', 'p-答(核心)', 'p-十法']
for i, (tg, c) in enumerate(zip(tags, units_cjk)):
    print(f'  80-{i:03d} {tg} CJK={c}')
print(f'  合计 CJK={sum(units_cjk)}')

# Key structural observations
print(f'\n== 结构观察 ==')
print(f'  品题：梵行品第十六 (CJK 6)')
print(f'  问端：正念天子 (CJK 50)·"云何而得梵行清淨"')
print(f'  答法一：十法為所緣·身·身業·語·語業·意·意業·佛·法·僧·戒 (核心段 CJK 669)')
print(f'  答法二：修習十種法·處非處智等·十力·無生法忍 (末段 CJK 193)')
print(f'  无偈颂：本品纯长行 (lg ×0·頌 ×0·偈 ×0)')
# verify no verse
has_lg = '頌' in body80 or '偈' in body80
print(f'  实测「頌」{"在" if "頌" in body80 else "无"}·「偈」{"在" if "偈" in body80 else "无"}')

# 六十 comparison
j8 = io.open('data/references/cbeta_txt/T09n0278_juan8.txt', encoding='utf-8').read()
lines8 = [l for l in j8.splitlines() if not l.startswith('#')]
s12 = e12 = None
for n, l in enumerate(lines8):
    ls = l.strip()
    if '梵行品第十二' in ls and s12 is None:
        s12 = n
    elif s12 is not None and n > s12 and ('品第' in ls or '卷第八' in ls):
        e12 = n; break
if e12 is None: e12 = len(lines8)
body60_raw = lines8[s12:e12]
cjk60 = sum(len(ONLY(l)) for l in body60_raw if l.strip())
print(f'\n== 六十侧 ==')
print(f'  品题：菩薩十住品第十一→梵行品第十二→卷第八尾题')
print(f'  CJK={cjk60} · 八十差值={cjk60-923:+d}')
print(f'  行计={len(body60_raw)}（含品题+卷题）')
