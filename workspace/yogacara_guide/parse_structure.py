# -*- coding: utf-8 -*-
"""从 CBETA TEI 提取《瑜伽师地论》结构：卷界、cb:div 层级、head 标题。
输出：卷号 → 起止字符偏移 + 该卷内出现的结构标题（按出现顺序）。"""
import re, sys, os

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, 'xml', 'T30n1579.xml')

xml = open(P, encoding='utf-8').read()
print('file bytes:', len(xml.encode('utf-8')))

# 1) 卷界：<cb:juan n="001"> ... 或 <milestone unit="juan" n="001">
juan_pos = [(m.start(), m.group(1)) for m in re.finditer(r'<cb:juan[^>]*n="(\d+)"', xml)]
if not juan_pos:
    juan_pos = [(m.start(), m.group(1)) for m in re.finditer(r'<milestone[^>]*unit="juan"[^>]*n="(\d+)"', xml)]
print('juan markers:', len(juan_pos), juan_pos[:3], juan_pos[-3:] if juan_pos else '')

# 2) 标题：<head>…</head>（可能带 rend/type）
heads = []
for m in re.finditer(r'<head([^>]*)>(.*?)</head>', xml, re.S):
    attrs, body = m.group(1), m.group(2)
    txt = re.sub(r'<[^>]+>', '', body)
    txt = re.sub(r'\s+', '', txt)
    heads.append((m.start(), attrs.strip(), txt))

def juan_of(pos):
    cur = None
    for p, n in juan_pos:
        if p <= pos:
            cur = n
        else:
            break
    return cur

print('\n=== HEADS (pos | juan | attrs | text) ===')
for pos, attrs, txt in heads:
    a = attrs.replace('"', "'")
    print('%7d | j%s | %-28s | %s' % (pos, juan_of(pos), a[:28], txt[:60]))
print('\ntotal heads:', len(heads))
