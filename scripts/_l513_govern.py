# -*- coding: utf-8 -*-
"""_l513_govern.py — L.513 全站结构治理：
①〇之二.9 文化资产参证自 §五 等错位归位〇之二系列末（33 品·幂等）
②P26 十地品尾偈残损修复（回源 c80/p026.json 逐字）
③P38 5.9/5.10 节标准化（窗口自 5.2 内迁出立节）
④各受改文件台账一行；含 L.513 总注
"""
import glob, io, json, re, sys

sys.stdout.reconfigure(encoding='utf-8')
LED = '- **L.513（2026-11-20）全站结构治理批**：〇之二.9 文化资产参证自 §五 错位归位〇之二系列末（全站推广·承 L.509/L.510 P37/P30 同类修复）。'

files = sorted(glob.glob('docs/经学文献/华严经细读/*/华严经细读_第*部_*.md'))
moved, skipped, noledger = [], [], []

for fp in files:
    md = io.open(fp, encoding='utf-8').read()
    m9 = re.search(r'^### 〇之二\.9[^\n]*\n(?:(?!\n### |\n## ).)*', md, re.M | re.S)
    if not m9:
        skipped.append((fp.split('/')[-1] if '/' in fp else fp, '无.9'))
        continue
    blk = m9.group(0)
    pre = md[:m9.start()]
    h2 = re.findall(r'^## [^\n]*', pre, re.M)
    last = h2[-1] if h2 else ''
    if last.startswith('## 〇之二'):
        skipped.append((fp[-14:-3], '已在位'))
        continue
    # ── 归位 ──
    md2 = md.replace(blk, '', 1)
    m1 = re.search(r'^## (一、|一　)', md2, re.M)
    if not m1:
        m1 = re.search(r'^## (二、|二　)', md2, re.M)
    assert m1, fp
    md2 = md2[:m1.start()] + blk.rstrip() + '\n\n' + md2[m1.start():]
    # ── 台账 ──
    ml = re.search(r'^## 九[、　]台账[^\n]*\n', md2, re.M)
    if ml:
        md2 = md2[:ml.end()] + LED + '\n' + md2[ml.end():]
    else:
        noledger.append(fp)
    io.open(fp, 'w', encoding='utf-8', newline='').write(md2)
    moved.append(fp[-14:-3])

print('① .9 归位 %d 品: %s' % (len(moved), ' '.join(moved)))
print('   跳过: %s' % skipped)
print('   无台账: %s' % noledger)

# ══ ② P26 尾偈修复 ══
fp26 = None
for g in glob.glob('docs/经学文献/华严经细读/第六会_他化自在天宫_十地位/华严经细读_第二十六部_*.md'):
    fp26 = g
md26 = io.open(fp26, encoding='utf-8').read()
d = json.load(open('web/demo/data/sutra/c80/p026.json', encoding='utf-8'))
txt = '\n'.join(x for s in d['segs'] for x in s['paras'])
j = txt.find('十行超世發心初')
k = txt.find('億劫說此不可盡。」', j)
verse = txt[j:k + len('億劫說此不可盡。」')]
i1 = md26.find('> 十行超世發心初，持戒')
assert i1 > 0, 'garbled anchor not found'
i2 = md26.find('億劫說此不可盡。」', i1) + len('億劫說此不可盡。」')
span = md26[i1:i2]
span_norm = re.sub(r'[>\s]', '', span)
verse_norm = re.sub(r'\s', '', verse)
assert span_norm == verse_norm, '残损拼合与回源不一致！\nMD:%s\nJSON:%s' % (span_norm[:80], verse_norm[:80])
md26 = md26[:i1] + '> ' + verse + '\n' + md26[i2:]
# 台账
ml = re.search(r'^## 九、台账[^\n]*\n', md26, re.M)
assert ml
LED26 = '- **L.513（2026-11-20）全站结构治理批**：①〇之二.9 归位〇之二系列末；②§2.2 尾偈「十行超世發心初」断行错乱修复（原窗断行碎裂·经与 `c80/p026.json` 逐字比对拼合回源·残损系转录断行非异文）。'
md26 = md26[:ml.end()] + LED26 + '\n' + md26[ml.end():]
io.open(fp26, 'w', encoding='utf-8', newline='').write(md26)
print('② P26 尾偈修复 ✓（拼合与回源逐字一致）')

# ══ ③ P38 5.9/5.10 立节 ══
fp38 = None
for g in glob.glob('docs/经学文献/华严经细读/第八会_普光明殿_离世间/华严经细读_第三十八部_*.md'):
    fp38 = g
md38 = io.open(fp38, encoding='utf-8').read()
ix = md38.find('**宣化上人《華嚴經淺釋》·问答结构判**')
ih = md38.find('**新加坡華嚴禪寺《網路白話華嚴經淺釋》·來意·四分五周中之位置**')
i53 = md38.find('### 5.3 海云《勘玄記04》講記選段')
assert 0 < ix < ih < i53, 'P38 window order unexpected: %d %d %d' % (ix, ih, i53)
xuan = md38[ix:ih].rstrip() + '\n'
hgs = md38[ih:i53].rstrip() + '\n'
assert xuan.count('**宣化上人《華嚴經淺釋》·') == 2, xuan.count('**宣化')
assert hgs.count('**新加坡華嚴禪寺') == 3
md38 = md38[:ix] + md38[i53:]
sec = ('### 5.9 新加坡白话浅释选录（來意·釋名·宗趣）\n\n'
       '> **来源**：新加坡華嚴禪寺《網路白話華嚴經淺釋》〈第38品〉（釋法欣 整理·hgs.sg 在线文本）。二手整理·白话浅释·可引用须标来源（用户裁定 L.139.0）；体例为华严宗式科判，繁简各照原件。\n\n'
       + hgs + '\n'
       '### 5.10 宣化上人《華嚴經淺釋》限量选段\n\n'
       '> **来源与纪律**：宣化上人《大方廣佛華嚴經淺釋》（法界佛教总会在线文本 DRBA）。**限量引用**（每章 ≤2 段·句界截断）；浅释口语照录，讲者之误只标不改。\n\n'
       + xuan + '\n')
m6 = re.search(r'^## 六、文本对读', md38, re.M)
assert m6
md38 = md38[:m6.start()] + sec + '\n' + md38[m6.start():]
# 台账（在①已加的 L.513 行上补注）
md38 = md38.replace(LED + '\n', LED.replace('。', '；②§5.9/5.10 自 §5.2 内迁出立节（宣化 2 窗·新加坡 3 窗·位次循 5.2→5.3→5.9→5.10）。') + '\n', 1)
io.open(fp38, 'w', encoding='utf-8', newline='').write(md38)
print('③ P38 5.9/5.10 立节 ✓')
print('L.513 done')
