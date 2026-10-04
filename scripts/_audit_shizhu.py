# -*- coding: utf-8 -*-
"""世主妙严品页面 · 全方位机械审计（报告模式，不改文件）"""
import io, sys, re, json
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

DOC = Path('docs/经学文献/华严经细读_第一部_世主妙严品.md')
t = DOC.read_text(encoding='utf-8')
L = t.split('\n')

def sec_of(line_no):
    cur = '(前言)'
    for i in range(line_no - 1, -1, -1):
        m = re.match(r'^(#{1,4}) (.+)$', L[i])
        if m:
            cur = re.sub(r'^#+\s*', '', m.group(2))
            break
    return cur

# ── 1. 标记清点 ────────────────────────────────────────────
print('=' * 60)
print('1. 标记清点（〔…〕）')
marks = {}
for m in re.finditer(r'〔([^〕]{1,12})〕', t):
    marks.setdefault(m.group(1), []).append(m.start())
rows = []
for k, v in marks.items():
    secs = {}
    for p in v:
        secs[sec_of(t[:p].count('\n') + 1)] = secs.get(sec_of(t[:p].count('\n') + 1), 0) + 1
    rows.append((len(v), k, len(secs), list(secs)[:3]))
for n, k, ns, ss in sorted(rows, reverse=True):
    print('  %-14s x%-5d 跨%-3d节  例:%s' % (k, n, ns, '、'.join(ss)))

# ── 2. EN 配对（中英必配）────────────────────────────────
print('=' * 60)
print('2. EN 配对')
print('  en-line 块:', len(re.findall(r'class="en-line"', t)))
print('  EN对应 标记:', len(re.findall(r'EN\s*(?:对应|—|-)\s*\d', t)))
figs = re.findall(r'<figcaption>(.*?)</figcaption>', t, re.S)
noen = [i for i, f in enumerate(figs, 1) if 'en-line' not in f]
print('  figcaption 共 %d，其中无 en-line：%s' % (len(figs), noen or '无'))
# 中文段后紧跟 en-line 的比例（粗判：中文块 vs en-line 块）
cn_blocks = len(re.findall(r'<div class="zh">', t))
print('  zh 块:', cn_blocks)

# ── 3. 引用可溯 ────────────────────────────────────────────
print('=' * 60)
print('3. 引用可溯')
urls = re.findall(r'https?://[^\s\)\]<>"]+', t)
print('  URL 总数:', len(urls), '｜去重:', len(set(urls)))
from collections import Counter
dom = Counter(re.sub(r'^https?://([^/]+).*', r'\1', u) for u in urls)
for d, c in dom.most_common(20):
    print('    %-42s x%d' % (d, c))
cbeta = sorted(set(re.findall(r'\bT\d{2}n\d{4}(?:_\d+)?\b', t)))
print('  CBETA 号 %d 个: %s' % (len(cbeta), ' '.join(cbeta)))
xuz = sorted(set(re.findall(r'\bX\d{4}\b', t)))
print('  续藏 X 号:', ' '.join(xuz) or '无')

# ── 4. 交叉引用有效性 ──────────────────────────────────────
print('=' * 60)
print('4. 内部交叉引用')
heads = [re.sub(r'^#+\s*', '', m.group(2)) for m in re.finditer(r'^(#{1,4}) (.+)$', t, re.M)]
nums = set(re.findall(r'〇-(\d+)', t))
print('  图编号 〇-N:', sorted(nums, key=int))
refs = sorted(set(re.findall(r'图\s*〇-(\d+)', t)), key=int)
print('  被引用之图:', refs, '｜悬空:', sorted(set(refs) - nums))
secnums = set(re.findall(r'〇之二\.(\d)', t))
print('  〇之二 小节引用:', sorted(secnums))
# 章节号引用
apx = set(re.findall(r'附录([一二三四五六七八九十]+)', t))
print('  附录引用:', sorted(apx))
exist = sorted(set(re.findall(r'^## 附录([一二三四五六七八九十]+)', t, re.M)))
print('  附录实际存在:', exist)
print('  悬空附录引用:', [a for a in apx if a not in exist])

# ── 5. 数字一致性 ──────────────────────────────────────────
print('=' * 60)
print('5. 关键数字出现处')
for key in ['414', '527', '40 类', '四十', '39', '190', '412', '20／190']:
    hits = []
    for m in re.finditer(re.escape(key), t):
        ln = t[:m.start()].count('\n') + 1
        hits.append(sec_of(ln))
    from collections import Counter as C2
    c = C2(hits)
    print('  %-8s x%-4d 节数%-3d %s' % (key, len(hits), len(c), list(c)[:4]))

# ── 6. 脏字符／排版 ────────────────────────────────────────
print('=' * 60)
print('6. 脏字符与排版')
for bad, label in [('\ufffd', 'U+FFFD 替换符'), ('\\"', '反斜杠引号'),
                   ('「」', '空书名号'), ('  ', '双空格'), ('\t', '制表符'),
                   ('？？', '双问号'), ('。。', '双句号')]:
    c = t.count(bad)
    if c: print('  %-16s x%d' % (label, c))
ws = len(re.findall(r'[ \t]+$', t, re.M))
print('  行尾空白行:', ws)
print('  强调 ** 出现:', len(re.findall(r'\*\*[^*]+\*\*', t)), '｜密度 %.2f/千字'
      % (len(re.findall(r'\*\*[^*]+\*\*', t)) / (len(t) / 1000)))

# ── 7. 表格完整性 ──────────────────────────────────────────
print('=' * 60)
print('7. 表格')
rows_ = re.findall(r'^\|(.+)\|\s*$', t, re.M)
print('  表格行:', len(rows_))
bad_tbl = 0
i = 0
lines = L
while i < len(lines):
    if lines[i].startswith('|'):
        blk = []
        while i < len(lines) and lines[i].startswith('|'):
            blk.append(lines[i]); i += 1
        if len(blk) >= 2 and not re.match(r'^\|[\s:|-]+\|\s*$', blk[1]):
            print('   ! 无分隔行 @', i - len(blk) + 1, blk[0][:60]); bad_tbl += 1
    else:
        i += 1
print('  缺分隔行之表:', bad_tbl)

# ── 8. 图/SVG ─────────────────────────────────────────────
print('=' * 60)
print('8. 图形')
print('  <svg> 块:', len(re.findall(r'<svg', t)))
print('  <figure>:', len(re.findall(r'<figure>', t)))
print('  <img>:', len(re.findall(r'<img', t)))
print('  en-line in figcaption:', len([f for f in figs if 'en-line' in f]))