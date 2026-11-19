# -*- coding: utf-8 -*-
"""_audit_pins_l513.py — 拼读系列 39 品全站评估（只读·实测）"""
import glob, re, io, json, os, sys
sys.stdout.reconfigure(encoding='utf-8')

HAN = re.compile(r'[\u3400-\u9fff]')
_D = {'一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9}


def cnum(s):
    if s == '十':
        return 10
    if '十' in s:
        a, _, b = s.partition('十')
        return (_D.get(a, 1) if a else 1) * 10 + _D.get(b, 0)
    return _D[s]


files = sorted(glob.glob('docs/经学文献/华严经细读/*/华严经细读_第*部_*.md'))
print('files:', len(files))

# ── 源文本规模（c80 p0NN.json 按品）──
src = {}
for pin in range(1, 40):
    p = 'web/demo/data/sutra/c80/p%03d.json' % pin
    if os.path.exists(p):
        d = json.load(open(p, encoding='utf-8'))
        txt = '\n'.join(x for s in d.get('segs', []) for x in s.get('paras', []))
        src[pin] = len(HAN.findall(txt))
    else:
        src[pin] = None

rows = []
for fp in files:
    pin = cnum(re.search(r'第([一二三四五六七八九十]+)部', fp).group(1))
    hui = re.sub(r'^docs.经学文献.华严经细读.', '', os.path.dirname(fp).replace('\\', '/'))
    md = io.open(fp, encoding='utf-8').read()
    han = len(HAN.findall(md))
    def has(p): return len(re.findall(p, md, re.M))
    row = dict(
        pin=pin, hui=hui.split('_')[0], han=han,
        src=src.get(pin), kb=len(md.encode('utf-8')) // 1024,
        h2=has(r'^## '), h3=has(r'^### '),
        svg=md.count('<svg'), fig=md.count('<figure'),
        tbl=has(r'^\|\s*-{3,}'), bq=has(r'^> '),
        en=has(r'^> \*\*EN '),
        s59=has(r'5\.9 新加坡'), s510=has(r'5\.10 宣化'),
        s512=has(r'5\.12|九九華嚴|《99华严|99華嚴'),
        d57=has(r'5\.2′'),
        zy=has(r'智俨《華嚴經搜玄|智俨《華嚴經搜玄分齊'),
        lun=has(r'李通玄《新華嚴經論》'), hel=has(r'李通玄《華嚴經合論》'),
        hy=has(r'慧苑《續華嚴略疏刊定記》'), dp=has(r'道霈《華嚴經疏論纂要》'),
        yc=has(r'演義鈔》'), tj=has(r'探玄記》'),
        zj=has(r'2\.0′ 玄记体总纲'),
        deep=has(r'^## 四′|^### 四″|深考|修門|行門深觀'),
        d60=has(r'^### 6\.[^ ]*[^\n]*六十'), d40=has(r'^### 6\.[^\n]*四十'),
        zang=has(r'6\.3 藏译|藏譯（Toh|藏译（Toh'),
        xh=has(r'宣化'), dg=has(r'新'),
        th=has(r'〔待核〕'), wj=has(r'〔未竟'),
        xf=has(r'行法|觀心|观心|觀法|观法|觀門|观门|行門|行门'),
        lastL=max([int(x) for x in re.findall(r'\*\*L\.(\d+)', md)] or [0]),
    )
    rows.append(row)

# ── 表 1：按部次序全表 ──
print('\n=== 表1 按 39 部次序（han=文章汉字·src=经源汉字·density=han/src）===')
print('%-4s %-5s %7s %7s %6s | %3s %3s %3s %3s %3s | %3s %3s %3s %3s | %3s %3s %3s %3s %3s %3s %3s %3s | %2s %2s %2s | %3s' % (
    '部', '会', 'han', 'src', 'den', 'h2', 'h3', 'svg', 'tbl', 'EN',
    '59', '510', '512', "5.2'", '智俨', '李论', '合论', '慧苑', '道霈', '演义', '探玄', '2.0′',
    '深', '三译', '藏', 'L'))
for r in rows:
    den = ('%.2f' % (r['han'] / r['src'])) if r['src'] else '-'
    print('%-4d %-5s %7d %7s %6s | %3d %3d %3d %3d %3d | %3d %3d %3d %4d | %3d %3d %3d %3d %3d %3d %3d %4d | %2d %2d %2d | %3d' % (
        r['pin'], r['hui'], r['han'], r['src'] or '-', den, r['h2'], r['h3'], r['svg'], r['tbl'], r['en'],
        r['s59'], r['s510'], r['s512'], r['d57'], r['zy'], r['lun'], r['hel'], r['hy'], r['dp'], r['yc'], r['tj'], r['zj'],
        r['deep'], r['d60'] + r['d40'], r['zang'], r['lastL']))

# ── 会汇总 ──
print('\n=== 表2 会汇总 ===')
from collections import defaultdict
agg = defaultdict(lambda: dict(n=0, han=0, svg=0, en=0, h3=0))
for r in rows:
    a = agg[r['hui']]
    a['n'] += 1; a['han'] += r['han']; a['svg'] += r['svg']; a['en'] += r['en']; a['h3'] += r['h3']
for k in sorted(agg):
    a = agg[k]
    print('%s: %2d 部 · %8d 字 · 图 %2d · EN %2d · 节 %3d · 均 %6.0f' % (k, a['n'], a['han'], a['svg'], a['en'], a['h3'], a['han'] / a['n']))

# ── 薄弱点排序（密度 + 覆盖缺口）──
print('\n=== 表3 密度排序（文章字 / 经源字，低=需要加强）===')
cands = [r for r in rows if r['src'] and r['src'] > 3000]
for r in sorted(cands, key=lambda x: x['han'] / x['src']):
    print('P%-2d den=%.2f han=%7d src=%7d svg=%d EN=%d 59=%d 510=%d 512=%d L=%d' % (
        r['pin'], r['han'] / r['src'], r['han'], r['src'], r['svg'], r['en'], r['s59'], r['s510'], r['s512'], r['lastL']))
print('\n（小品 src<=3000 不入密度排序：', [r['pin'] for r in rows if not r['src'] or r['src'] <= 3000], '）')
