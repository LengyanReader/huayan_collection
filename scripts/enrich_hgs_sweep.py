# -*- coding: utf-8 -*-
"""enrich_hgs_sweep.py — L.503 新加坡白话浅释·来意/释名/宗趣 全面扩样（余下品目）

逐章（品2-37·已行者跳过）：取 hgs_baihua/品NN.txt 的 來意/釋名/宗趣 三门（简繁两体锚·句界截断 400），
插 `### 5.9 新加坡白话浅释选录` 于 §六 之前。标签 5.9 与会读系 5.2′（智俨）/5.2″（慧苑）分开。
品39 结构特殊不入本扫（其子页/四源已足）。
"""
import glob
import io
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
APPLY = '--apply' in sys.argv
DONE = {19, 21, 22, 23, 31, 32, 38, 39}
HAN = re.compile(r'[\u3400-\u9fff]')


def han(s):
    return len(HAN.findall(s))


def cut(text, limit=400):
    if han(text) <= limit:
        return text
    acc = 0
    for i, ch in enumerate(text):
        if HAN.match(ch):
            acc += 1
        if acc >= limit and ch in '。！？」』；':
            return text[:i + 1]
    return text[:limit]


def cn_num(n):
    D = '一二三四五六七八九'
    if n <= 9:
        return D[n - 1]
    if n == 10:
        return '十'
    if n < 20:
        return '十' + D[n - 11]
    if n == 20:
        return '二十'
    if n < 30:
        return '二十' + D[n - 21]
    if n == 30:
        return '三十'
    if n < 40:
        return '三十' + D[n - 31]
    return str(n)


def find_pair(t, a_variants, b_variants, start=0):
    ia, va = -1, None
    for v in a_variants:
        i = t.find(v, start)
        if i >= 0 and (ia < 0 or i < ia):
            ia, va = i, v
    if ia < 0:
        return None, None, None
    ib, vb = len(t), None
    for v in b_variants:
        i = t.find(v, ia + len(va))
        if i >= 0 and i < ib:
            ib, vb = i, v
    return ia, ib, va


def clean(t):
    t = re.sub(r'【页\d+】\s*\d*', '', t)
    return re.sub(r'[ \t]+', '', t)


report = []
for nn in range(2, 38):
    if nn in DONE:
        continue
    cn = cn_num(nn)
    g = glob.glob('docs/经学文献/华严经细读/**/华严经细读_第%s部_*.md' % cn, recursive=True)
    if not g:
        report.append((nn, 'md缺', 0, ''))
        continue
    fp = g[0]
    md = io.open(fp, encoding='utf-8').read()
    if '5.9 新加坡' in md:
        report.append((nn, '已有', 0, ''))
        continue
    src = 'data/references/huayan_daodu/hgs_baihua/品%d.txt' % nn
    try:
        t = clean(io.open(src, encoding='utf-8').read())
    except Exception:
        report.append((nn, '源缺', 0, ''))
        continue

    blocks = []
    i1, i2, v1 = find_pair(t, ['一、来意', '一、來意'], ['二、释名', '二、釋名', '◎', '（解'])
    if i1 is None:
        report.append((nn, '來意缺', 0, ''))
        continue
    i3, i4, v2 = find_pair(t, ['二、释名', '二、釋名'], ['三、宗趣', '三、宗趣', '◎', '（解'], i2 or 0)
    i5, i6, v3 = find_pair(t, ['三、宗趣'], ['四、释文', '四、釋文', '◎', '（解'], i4 or 0)
    if i1 is not None and i2:
        blocks.append(('來意', t[i1:i2]))
    if i3 is not None and i4 > i3:
        blocks.append(('釋名', t[i3:i4]))
    if i5 is not None and i6 > i5:
        blocks.append(('宗趣', t[i5:i6]))
    if not blocks:
        report.append((nn, '无可提', 0, ''))
        continue

    parts, total = [], 0
    for name, s in blocks:
        s = s.strip()
        s = cut(s)
        total += han(s)
        parts.append('**新加坡華嚴禪寺《網路白話華嚴經淺釋》·%s**（%d 字·小节整段选录·来源：hgs.sg 在线文本·釋法欣 整理）：\n\n> %s'
                     % (name, han(s), s))
    included = '·'.join(n for n, _ in blocks)
    sec = ('### 5.9 新加坡白话浅释选录（%s）\n\n'
           '> **来源**：新加坡華嚴禪寺《網路白話華嚴經淺釋》〈第%d品〉（釋法欣 整理·hgs.sg 在线文本·'
           '本仓清洗提取本 `data/references/huayan_daodu/hgs_baihua/品%d.txt`）。二手整理·白话浅释·'
           '可引用须标来源（用户裁定 L.139.0）；体例为华严宗式科判，繁简各照原件。\n\n' % (included, nn, nn)
           + '\n\n'.join(parts)
           + '\n\n> **会读按语**〔本文判断〕来意/释名/宗趣三门与 §一 品题解义对读——'
             '二手白话科判所记之判摄（会次/法门/宗趣）可互校本文之实测。\n')
    m = re.search(r'\n## 六[、　]', md)
    if not m:
        report.append((nn, '无##六', 0, ''))
        continue
    if APPLY:
        md = md[:m.start() + 1] + sec + '\n' + md[m.start() + 1:]
        io.open(fp, 'w', encoding='utf-8', newline='').write(md)
    report.append((nn, 'OK' if APPLY else 'DRY', total, included))

for r in report:
    print(r)
print('合计 %d 字（dry=%s）' % (sum(r[2] for r in report), not APPLY))
