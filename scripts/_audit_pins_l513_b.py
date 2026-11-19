# -*- coding: utf-8 -*-
"""_audit_pins_l513_b.py — §四深度·〇之二.9 位置·§二规模（只读·实测）"""
import glob, io, re, sys
sys.stdout.reconfigure(encoding='utf-8')

D = {'一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9}


def cnum(s):
    if s == '十':
        return 10
    if '十' in s:
        a, _, b = s.partition('十')
        return (D.get(a, 1) if a else 1) * 10 + D.get(b, 0)
    return D[s]


res = []
for fp in sorted(glob.glob('*/华严经细读_第*部_*.md')):
    pin = cnum(re.search(r'第([一二三四五六七八九十]+)部', fp).group(1))
    L = io.open(fp, encoding='utf-8').read().split('\n')
    h2 = [(i, l[3:].strip()) for i, l in enumerate(L) if l.startswith('## ')]
    w4 = w2 = None
    pos9 = '无'
    for k, (i, t) in enumerate(h2):
        nxt = h2[k + 1][0] if k + 1 < len(h2) else len(L)
        if re.match(r'^四[′、"]', t):
            w4 = nxt - i
        if t.startswith('二、') or t.startswith('二，'):
            w2 = nxt - i
    for i, l in enumerate(L):
        if '〇之二.9' in l or '〇之二．9' in l:
            prev = [t for j, t in h2 if j < i]
            prevT = prev[-1] if prev else '(开头)'
            if '〇之二' in prevT or '读法' in prevT or '谱' in prevT:
                pos9 = 'ok(宿:%s)' % prevT[:16]
            else:
                pos9 = '错位!(宿:%s)' % prevT[:16]
            break
    res.append((pin, w4, w2, pos9))

print('%-4s %7s %7s  %s' % ('部', '§四行数', '§二行数', '〇之二.9'))
for pin, w4, w2, p9 in sorted(res, key=lambda r: (r[1] if r[1] is not None else -1)):
    print('%-4d %7s %7s  %s' % (pin, w4, w2, p9))
