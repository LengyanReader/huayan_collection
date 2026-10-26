# -*- coding: utf-8 -*-
"""_e16_check_quotes.py — L.196 P16《梵行品》骨架全量引文回源校验（0 臆造闸门）
   双轨提取（承 _e15_check_quotes.py）：pass1 紧口径逐行配对 · pass2 宽口径跨行（限内核无 bracket）
   语料：P16 body80 · P15 body80（互见） · P14 body80（脉络引） · T09n0278_juan8 全本（六十对读） · 六祖典 txt
   miss>0 即非零退出（fail loud）。
"""
import io, re, sys, unicodedata
import xml.etree.ElementTree as ET

MD = 'docs/经学文献/华严经细读/第三会_忉利天宫_差别因果周/华严经细读_第十六部_梵行品.md'
norm = lambda ch: (unicodedata.normalize('NFKD', ch)[0] if unicodedata.normalize('NFKD', ch) else ch)
ONLY = lambda s: ''.join(ch for ch in (norm(c) for c in s) if '\u4e00' <= ch <= '\u9fff')
GAP = lambda s: s.replace('：', '，')

SKIP = {'note', 'rdg', 'mulu', 'pb', 'anchor', 'app'}
acc = []
def walk(el):
    t = el.tag.split('}')[-1]
    if t in SKIP: return
    if t == 'lb': acc.append(' ')
    if el.text: acc.append(el.text)
    for c in el:
        walk(c)
        if c.tail: acc.append(c.tail)
walk(ET.parse('data/references/cbeta/T10n0279.xml').getroot())
fullC = ONLY(''.join(acc))
iC = fullC.find('梵行品第十六')
kC = fullC.find('初發心功德品第十七', iC + 6)
assert 0 < iC < kC, (iC, kC)
CORP = [GAP(fullC[iC:kC])]                    # 本品 body80
CORP.append(GAP(fullC[fullC.find('十住品第十五'):iC]))   # P15 前品（互见）
CORP.append(GAP(fullC[fullC.find('須彌頂上偈讚品第十四'):fullC.find('十住品第十五')]))  # P14（脉络引）
j8 = io.open('data/references/cbeta_txt/T09n0278_juan8.txt', encoding='utf-8').read()
CORP.append(GAP(ONLY(j8)))                    # 六十卷八全本
for p in ['T1735_澄观_华严经疏', 'T1733_法藏_探玄记', 'T1732_智俨_搜玄记',
          'X0221_慧苑_续华严略疏刊定记', 'T1739_李通玄_新华严经论', 'X0223_李通玄_华严经合论']:
    s = io.open('data/references/cbeta_txt/%s.txt' % p, encoding='utf-8').read()
    s = re.sub(r'<<<PAGE\s*\d+>>>', '', s)
    CORP.append(GAP(ONLY(s)))

md = io.open(MD, encoding='utf-8').read()
md = md.replace('**', '')
md = md.replace('六十｜', '照录前缀')
md = md.replace('「六十照录前缀」之标记', '〔元文本〕', 1)
META = [
    '双引号十组全闭合', '每段行首', '单层双引号内套单引号处',
]
checked = set()
hit = 0; missl = []
def check(c, tag):
    global hit
    c = GAP(re.sub(r'\s', '', c))
    if len(c) < 8 or c in checked:
        return
    checked.add(c)
    if any(c in k for k in CORP): hit += 1
    else: missl.append((tag, c[:60]))

for line in md.splitlines():
    for q in re.findall(r'「([^「」]*?)」', line):
        q = re.sub(r'〔[^〕]*〕', '', q); q = re.sub(r'（[^）]*）', '', q)
        for frag in re.split(r'……|…|\.\.\.|／|』|「|」', q):
            check(ONLY(frag), 'p1')
for q in re.findall(r'「([^「」]{1,400}?)」', md, re.S):
    if '照录前缀' in q: continue
    if q.count('\n') > 2: continue
    q = re.sub(r'〔[^〕]*〕', '', q); q = re.sub(r'（[^）]*）', '', q)
    for frag in re.split(r'……|…|\.\.\.|／|』|「|」', q):
        check(ONLY(frag), 'p2')

_OUT = io.open('_e16_cq_miss.txt', 'w', encoding='utf-8')
def emit(s):
    _OUT.write(s + '\n')
    print(s.encode('utf-8', 'replace').decode('utf-8', 'replace'))
real_miss = [(t, c) for t, c in missl if not any(g in c for g in META)]
emit('frags=%d·hit=%d miss=%d（META 豁免 %d）' % (len(checked), hit, len(real_miss), len(missl) - len(real_miss)))
for t, c in real_miss:
    emit('MISS(%s): ' % t + c)
_OUT.close()
sys.exit(1 if real_miss else 0)
