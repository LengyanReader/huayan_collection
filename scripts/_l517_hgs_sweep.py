# -*- coding: utf-8 -*-
"""_l517_hgs_sweep.py — L.517 会1-2 5.9 新加坡补扫（P1-P10·复用 L.503 体例）
P1 为逐卷结构（无 §六 前插位）——单独处理：插于 §五 前（其 ## 五 卷末台账前的注疏段）或如实跳过。
"""
import glob
import io
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
APPLY = '--apply' in sys.argv
HAN = re.compile(r'[\u3400-\u9fff]')
TARGETS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
D = '一二三四五六七八九十'


def han(s):
    return len(HAN.findall(s))


def cn_num(n):
    if n <= 10:
        return D[n - 1]
    if n < 20:
        return '十' + D[n - 11]
    return str(n)


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
for nn in TARGETS:
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
    try:
        t = clean(io.open('data/references/huayan_daodu/hgs_baihua/品%02d.txt' % nn, encoding='utf-8').read())
    except Exception:
        report.append((nn, '源缺', 0, ''))
        continue

    blocks = []
    i1, i2, v1 = find_pair(t, ['一、来意', '一、來意', '壹、来意', '壹、來意'],
                           ['二、释名', '二、釋名', '貮、释名', '貮、釋名', '◎', '（解'])
    i3, i4, v2 = find_pair(t, ['二、释名', '二、釋名', '貮、释名', '貮、釋名', '一、释名', '一、釋名', '一、釋名及宗趣', '一、释名及宗趣'],
                           ['三、宗趣', '叁、宗趣', '叄、宗趣', '二、宗趣', '二、釋文', '二、释文', '◎', '（解'], i2 or 0)
    i5, i6, v3 = find_pair(t, ['三、宗趣', '叁、宗趣', '叄、宗趣', '二、宗趣'],
                           ['四、释文', '四、釋文', '三、释文', '三、釋文', '◎', '（解'], i4 or 0)
    if i1 is not None and i2:
        blocks.append(('來意', t[i1:i2]))
    if i3 is not None and i4 > i3:
        nm3 = '釋名及宗趣' if ('及宗趣' in (v2 or '')) else '釋名'
        blocks.append((nm3, t[i3:i4]))
    if i5 is not None and i6 > i5:
        blocks.append(('宗趣', t[i5:i6]))
    if not blocks:
        report.append((nn, '无可提（源无三门）', 0, ''))
        continue

    parts, total = [], 0
    for name, s in blocks:
        s = cut(s.strip())
        total += han(s)
        parts.append('**新加坡華嚴禪寺《網路白話華嚴經淺釋》·%s**（%d 字·小节整段选录·来源：hgs.sg 在线文本·釋法欣 整理）：\n\n> %s'
                     % (name, han(s), s))
    included = '·'.join(n for n, _ in blocks)
    sec = ('### 5.9 新加坡白话浅释选录（%s）\n\n'
           '> **来源**：新加坡華嚴禪寺《網路白話華嚴經淺釋》〈第%d品〉（釋法欣 整理·hgs.sg 在线文本·'
           '本仓清洗提取本 `data/references/huayan_daodu/hgs_baihua/品%02d.txt`）。二手整理·白话浅释·'
           '可引用须标来源（用户裁定 L.139.0）；体例为华严宗式科判，繁简各照原件。\n\n' % (included, nn, nn)
           + '\n\n'.join(parts)
           + '\n\n> **会读按语**〔本文判断〕来意/释名/宗趣三门与 §一 品题解义对读——'
             '二手白话科判所记之判摄（会次/法门/宗趣）可互校本文之实测。\n')
    # 插入点：标准件在 ## 六 前；P1 无 ## 六（逐卷结构）→ 插 ## 五 前
    m = re.search(r'\n## 六[、　]', md)
    tag = '## 六前'
    if not m:
        m = re.search(r'\n## 五[、　]', md)
        tag = '## 五前'
    if not m:
        report.append((nn, '无插位', 0, ''))
        continue
    if APPLY:
        md = md[:m.start() + 1] + sec + '\n' + md[m.start() + 1:]
        ml = re.search(r'^## 九[、　]台账[^\n]*\n', md, re.M)
        if ml:
            md = md[:ml.end()] + '- **L.517（2026-11-20）补扫批**：新增 §5.9 新加坡白话浅释选录（%s——`hgs_baihua/品%02d.txt`·承 L.503 全站扫描之会1-2 缺口补齐）。\n' % (included, nn) + md[ml.end():]
        io.open(fp, 'w', encoding='utf-8', newline='').write(md)
    report.append((nn, 'OK' if APPLY else 'DRY@' + tag, total, included))

for r in report:
    print(r)
print('合计 %d 字（dry=%s）' % (sum(r[2] for r in report), not APPLY))
