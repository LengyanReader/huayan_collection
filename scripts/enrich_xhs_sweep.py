# -*- coding: utf-8 -*-
"""enrich_xhs_sweep.py — L.504 宣化《華嚴經淺釋》限量选段·全面扩样（其余品目）

逐章（品2-38·已有宣化块者跳过）：按品名配 Ava_Vol*（卷题含品名）·取 1-2 段讲解段
（L.479 体例：开经偈切头＋纯版头过滤＋关键词打分·句界截断 400），
插 `### 5.10 宣化上人《華嚴經淺釋》限量选段` 于 §六 之前（5.9 新加坡之后）。
标签 5.10 与 5.9（新加坡）分开；每章 ≤2 段·限量引用。
"""
import glob
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
APPLY = '--apply' in sys.argv
SRC = 'data/references/huayan_daodu/宣化淺釋'
HAN = re.compile(r'[\u3400-\u9fff]')


def han(s):
    return len(HAN.findall(s))


def cut(text, limit=400):
    if han(text) <= limit:
        return text, False
    acc = 0
    for i, ch in enumerate(text):
        if HAN.match(ch):
            acc += 1
        if acc >= limit and ch in '。！？」』':
            return text[:i + 1], True
    return text[:limit], True


def passages(fp, cap=400):
    """L.479 体例：切版头→并段→滤纯版头→打分取 1 段。"""
    t = io.open(fp, encoding='utf-8').read()
    body = t
    k = body.find('願解如來真實義')
    if k >= 0:
        body = body[k + len('願解如來真實義'):]
    paras, cur = [], ''
    for ln in body.split('\n'):
        ln = ln.strip()
        if not ln:
            if cur:
                paras.append(cur)
            cur = ''
            continue
        cur += ln
    if cur:
        paras.append(cur)
    paras = [p for p in paras
             if not (han(p) < 200 and ('講述' in p[:60] or '無上甚深微妙法' in p))]
    scored = []
    for p in paras:
        score = sum(p.count(kw) for kw in
                    ['什麼叫', '怎麼', '為什麼', '這個', '就是你', '我們', '修行', '菩薩', '因為'])
        if han(p) >= 150:
            scored.append((score, p))
    if not scored:
        return None
    scored.sort(key=lambda x: -x[0])
    p = scored[0][1]
    txt, trimmed = cut(p, cap)
    return txt, trimmed


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


CN = {'一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9}


def cn2n(s):
    if '十' in s:
        a, _, b = s.partition('十')
        v = (CN[a] * 10) if a else 10
        if b:
            v += CN[b]
        return v
    return CN.get(s, 0)


def _vskey(v):
    """卷内序号（Vol25-2 → 2·供数值排序）"""
    m = re.search(r'Vol\d+[-_]?(\d*)', v)
    return int(m.group(1)) if (m and m.group(1)) else 0


PIN_VOLS = {}
for v in sorted(glob.glob(SRC + '/Ava_Vol*.txt')):
    h = io.open(v, encoding='utf-8').read(200)
    mt = re.search(r'卷题：\S{2,14}品第([一二三四五六七八九十百]+)', h)
    if mt:
        PIN_VOLS.setdefault(cn2n(mt.group(1)), []).append(v)
for k in PIN_VOLS:
    PIN_VOLS[k].sort(key=_vskey)
VOL_HEAD = {v: io.open(v, encoding='utf-8').read(200) for vs in PIN_VOLS.values() for v in vs}

report = []
for nn in range(2, 39):
    cn = cn_num(nn)
    g = glob.glob('docs/经学文献/华严经细读/**/华严经细读_第%s部_*.md' % cn, recursive=True)
    if not g:
        report.append((nn, 'md缺', 0, ''))
        continue
    fp = g[0]
    md = io.open(fp, encoding='utf-8').read()
    if '宣化上人《華嚴經淺釋》·' in md:
        report.append((nn, '已有', 0, ''))
        continue
    m = re.search(r'华严经细读_第[^_]+_([^_]+)\.md', fp)
    pin_name = m.group(1) if m else None
    if not pin_name:
        report.append((nn, '品名缺', 0, ''))
        continue
    hits = PIN_VOLS.get(nn, [])
    if not hits:
        report.append((nn, '卷缺', 0, pin_name))
        continue
    blocks = []
    total = 0
    for v in (hits[:2] if len(hits) <= 2 else [hits[0], hits[-1]]):
        r = passages(v)
        if not r:
            continue
        txt, trimmed = r
        total += han(txt)
        head = VOL_HEAD[v]
        mt = re.search(r'卷题：([^\n]+)', head)
        blocks.append('**宣化上人《華嚴經淺釋》·%s**（%d 字·限量引用·句界截断·来源：法界佛教总会在线文本 DRBA）：\n\n> %s%s'
                      % ((mt.group(1) if mt else pin_name), han(txt), txt,
                         '\n\n……（后文从略）' if trimmed else ''))
        if len(blocks) >= 2:
            break
    if not blocks:
        report.append((nn, '无合格段', 0, pin_name))
        continue
    sec = ('### 5.10 宣化上人《華嚴經淺釋》限量选段\n\n'
           '> **来源与纪律**：宣化上人《大方廣佛華嚴經淺釋》（法界佛教总会在线文本 DRBA·本仓提取本 '
           '`data/references/huayan_daodu/宣化淺釋/`）。**限量引用**（每章 ≤2 段·句界截断）；'
           '浅释口语照录，讲者之误只标不改。\n\n' + '\n\n'.join(blocks) + '\n')
    m6 = re.search(r'\n## 六[、　]', md)
    if not m6:
        report.append((nn, '无##六', 0, pin_name))
        continue
    if APPLY:
        md = md[:m6.start() + 1] + sec + '\n' + md[m6.start() + 1:]
        io.open(fp, 'w', encoding='utf-8', newline='').write(md)
    report.append((nn, 'OK' if APPLY else 'DRY', total, pin_name + '×%d卷' % len(hits[:2])))

for r in report:
    print(r)
print('合计 %d 字（applied=%s）' % (sum(r[2] for r in report), APPLY))
