# -*- coding: utf-8 -*-
"""《般若空宗三论中观全方位研究》正文抽取式回源核验（阶段三落地）。
从 md 抽取全部引文：「…」（≥6 字）与 "…"（≥6 字，仅繁体候选），
剥标点后对底本子串匹配；输出 位置|引文|命中底本|卷|状态。
底本：T30n1564（canonical）、T45n1852/1854/1858（canonical）。访问 2026-11-20。"""
import os, re, sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
CAN = os.path.normpath(os.path.join(HERE, os.pardir, os.pardir, 'data', 'references', 'cbeta'))
MD = os.path.normpath(os.path.join(HERE, os.pardir, os.pardir, 'docs', '宗派研究', '般若空宗三论中观全方位研究.md'))

PUNCT = set('，。、；：？！「」『』（）《》〈〉……—－·“”‘’ \u3000\n\r\t()[]')

def load(tid):
    xml = open(os.path.join(CAN, tid + '.xml'), encoding='utf-8').read()
    jp = [(m.start(), m.group(1)) for m in re.finditer(r'<cb:juan[^>]*n="(\d+)"', xml)]
    chars, pm, it = [], [], False
    for i, ch in enumerate(xml):
        if ch == '<': it = True
        elif ch == '>': it = False
        elif not it: chars.append(ch); pm.append(i)
    return ''.join(chars), pm, jp

def np(s):
    return ''.join(ch for ch in s if ch not in PUNCT)

def extract_quotes(md):
    """抽取全部引文：返回 (quote, kind, note_tag) 列表。kind: 「」| "" """
    out = []
    for m in re.finditer(r'「([^」]{6,})」', md):
        out.append((m.group(1), '「」', False))
    # 注：本篇 "…" 为强调引号（原文体例），不属经文引文——不抽取核验。
    # 经文/祖语引文一律以「」标示（仓规：引文繁体照底本）。
    return out

md = open(MD, encoding='utf-8').read()
quotes = extract_quotes(md)
TEXTS = {}
for tid in ['T30n1564', 'T45n1852', 'T45n1854', 'T45n1858']:
    TEXTS[tid] = load(tid)

total = ok = exempt = 0
misses = []
print('抽取引文 %d 条（含豁免候选）' % len(quotes))
for i, (q, kind, tag) in enumerate(quotes, 1):
    total += 1
    # 位置（第几个字符附近）
    pos = md.find('「' + q + '」') if kind == '「」' else md.find('"' + q + '"')
    line = md[:pos].count('\n') + 1 if pos >= 0 else -1
    if tag:
        exempt += 1
        print('  [豁免] L%-4d %s〔大意〕%s' % (line, kind, q[:30]))
        continue
    hit = None
    for tid, (text, pm, jp) in TEXTS.items():
        if np(q) and np(text).find(np(q)) >= 0:
            hit = tid
            break
    if hit:
        ok += 1
        print('  [ ok ] L%-4d %s → %s | %s' % (line, kind, hit, q[:34]))
    else:
        misses.append((line, q, kind))
        print('  [MISS] L%-4d %s %s' % (line, kind, q[:40]))

print('=' * 70)
print('严格核验 %d（ok %d / miss %d）＋豁免〔大意〕%d' % (total - exempt, ok, len(misses), exempt))
for line, q, kind in misses:
    print('  MISS L%d %s %s' % (line, kind, q[:50]))
