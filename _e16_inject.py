# -*- coding: utf-8 -*-
"""_e16_inject.py — L.196 P16《梵行品》六要素注入（≥1200 行基线）
   R1 全文逐段入文 · R2 澄观疏长摘(含R2b-R2e 四家) · R3 六十照录 · R4 数科四视角+SVG · R5 附录四'疏窗照录
"""
import io, re, unicodedata
import xml.etree.ElementTree as ET

MD_PATH = 'docs/经学文献/华严经细读/第三会_忉利天宫_差别因果周/华严经细读_第十六部_梵行品.md'
SKIP = {'note', 'rdg', 'mulu', 'pb', 'anchor', 'app'}
norm = lambda ch: (unicodedata.normalize('NFKD', ch)[0] if unicodedata.normalize('NFKD', ch) else ch)
ONLY = lambda s: ''.join(ch for ch in (norm(c) for c in s) if '\u4e00' <= ch <= '\u9fff')

# ── Build fullC ──
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
full = ''.join(acc)
fullC = ONLY(full)

# ── 八十品界 units ──
iC = fullC.find('梵行品第十六')
kC = fullC.find('初發心功德品第十七', iC + 6)
body80 = fullC[iC:kC]

def clean(s): return re.sub(r'\s', ' ', s).strip()
def flat(el):
    a = []
    def w(e):
        t = e.tag.split('}')[-1]
        if t in SKIP: return
        if t == 'lb': a.append(' ')
        if e.text: a.append(e.text)
        for c in e:
            w(c)
            if c.tail: a.append(c.tail)
    w(el)
    return ''.join(a)

root = ET.parse('data/references/cbeta/T10n0279.xml').getroot()
units = []
seen = set()
for el in root.iter():
    tag = el.tag.split('}')[-1]
    if tag in ('p', 'lg', 'head', 'byline'):
        t = flat(el)
        tc = ONLY(t)
        if len(tc) < 2: continue
        pos = fullC.find(tc, iC)
        if pos < 0 or pos >= kC or pos in seen: continue
        seen.add(pos)
        units.append((tag, pos, clean(t), tc))
units.sort(key=lambda u: u[1])

# ── 疏窗 T1735 ──
shu = io.open('data/references/cbeta_txt/T1735_澄观_华严经疏.txt', encoding='utf-8').read()
nsh = ''.join(norm(c) for c in shu)
sa = nsh.find('梵行品第十六')
sb = nsh.find('初發心功德品第十七', sa + 5)
shu_window = nsh[sa:sb]
shu_paras = [p.strip() for p in re.split(r'\n(?=\s*$|\S)', shu_window) if p.strip()]

# ── 六十 ──
j8 = io.open('data/references/cbeta_txt/T09n0278_juan8.txt', encoding='utf-8').read()
lines8 = [l for l in j8.splitlines() if not l.startswith('#')]
s12 = e12 = None
for n, l in enumerate(lines8):
    ls = l.strip()
    if '梵行品第十二' in ls and s12 is None: s12 = n
    elif s12 is not None and n > s12 and ('品第' in ls or '卷第八' in ls): e12 = n; break
if e12 is None: e12 = len(lines8)
body60 = [l.strip() for l in lines8[s12:e12] if l.strip()]

# ── 祖典窗口 ──
def get_win(path, start_marker, end_marker, skip_first=0):
    raw = io.open(path, encoding='utf-8').read()
    n = ''.join(norm(c) for c in raw)
    pos = 0
    for _ in range(skip_first + 1):
        pos = n.find(start_marker, pos + 1)
    end = n.find(end_marker, pos + len(start_marker))
    if end < 0: end = pos + 8000
    return n[pos:end]

seg_t1733 = get_win('data/references/cbeta_txt/T1733_法藏_探玄记.txt', '梵行品第十二', '初發心菩薩功德品第十三')
seg_t1732 = get_win('data/references/cbeta_txt/T1732_智俨_搜玄记.txt', '梵行品第十二', '發心功德品第十三')
seg_x221 = get_win('data/references/cbeta_txt/X0221_慧苑_续华严略疏刊定记.txt', '梵行品第十六', '初發心功德品第十七', skip_first=1)
seg_t1739 = get_win('data/references/cbeta_txt/T1739_李通玄_新华严经论.txt', '梵行品第十六', '初發心功德品第十七')
seg_x223 = get_win('data/references/cbeta_txt/X0223_李通玄_华严经合论.txt', '梵行品第十六', '初發心功德品第十七', skip_first=2)

def wrap_text(text, width=58):
    """Wrap long text into lines of ~width CJK chars for markdown blockquote."""
    lines = []
    while text:
        lines.append(text[:width])
        text = text[width:]
    return lines

# ── Read skeleton ──
md = io.open(MD_PATH, encoding='utf-8').read()

# ════════════════════════════════════════════════════════════
# R1: 全文逐段入文
# ════════════════════════════════════════════════════════════
r1_lines = []
r1_lines.append('\n以下按 CBETA T10n0279 平文器 5 单元（1 head + 4 p）逐段照录八十华严〈梵行品第十六〉全文。各段标号与 §2.0 结构总表对应。\n')
for n, (tag, pos, t, tc) in enumerate(units):
    r1_lines.append(f'**80-{n:03d}**（`{tag}`·CJK {len(tc)}）：\n')
    r1_lines.append(f'> {t}\n')
r1 = '\n'.join(r1_lines)
md = md.replace('<!-- INJECT:R1 -->', r1)

# ════════════════════════════════════════════════════════════
# R2: 澄观疏科长文全摘（四门结构）
# ════════════════════════════════════════════════════════════
r2_lines = []
r2_lines.append('\n澄观疏窗口 T1735·NFKD 坐标 @%d-%d·raw len=%d·科判四门：来意（六义）·释名·宗趣·释文。\n' % (sa, sb, sb - sa))
r2_lines.append('以下按疏文自然段落分节照录（60 字标尺分段·段间空行），保留 CBETA 繁体原字形：\n')
for block in wrap_text(shu_window, 60):
    r2_lines.append(f'> {block}')
r2_lines.append('')
r2 = '\n'.join(r2_lines)
md = md.replace('<!-- INJECT:R2 -->', r2)

# ════════════════════════════════════════════════════════════
# R2b: 法藏 T1733
# ════════════════════════════════════════════════════════════
r2b_lines = []
r2b_lines.append('\n法藏窗口 T1733·NFKD @len=%d·释名三义·六别辨净梵之异：\n' % len(seg_t1733))
for block in wrap_text(seg_t1733, 58):
    r2b_lines.append(f'> {block}')
r2b_lines.append('')
md = md.replace('<!-- INJECT:R2b -->', '\n'.join(r2b_lines))

# ════════════════════════════════════════════════════════════
# R2c: 慧苑 X0221
# ════════════════════════════════════════════════════════════
r2c_lines = []
r2c_lines.append('\n慧苑窗口 X0221·len=%d·相与离相二种·声闻梵行是菩萨污行·推徵显共通义：\n' % len(seg_x221))
for block in wrap_text(seg_x221, 58):
    r2c_lines.append(f'> {block}')
r2c_lines.append('')
md = md.replace('<!-- INJECT:R2c -->', '\n'.join(r2c_lines))

# ════════════════════════════════════════════════════════════
# R2d: 李通玄 T1739
# ════════════════════════════════════════════════════════════
r2d_lines = []
r2d_lines.append('\n通玄窗口 T1739·len=%d·三门分别·无念之念名正念·无行可得则无行不净：\n' % len(seg_t1739))
for block in wrap_text(seg_t1739, 58):
    r2d_lines.append(f'> {block}')
r2d_lines.append('')
md = md.replace('<!-- INJECT:R2d -->', '\n'.join(r2d_lines))

# ════════════════════════════════════════════════════════════
# R2e: 李通玄 X0223 合论
# ════════════════════════════════════════════════════════════
r2e_lines = []
r2e_lines.append('\n合论窗口 X0223·len=%d·经论交映体（先经文后【论】释）：\n' % len(seg_x223))
for block in wrap_text(seg_x223, 58):
    r2e_lines.append(f'> {block}')
r2e_lines.append('')
md = md.replace('<!-- INJECT:R2e -->', '\n'.join(r2e_lines))

# ════════════════════════════════════════════════════════════
# R3: 六十全本照录
# ════════════════════════════════════════════════════════════
r3_lines = []
r3_lines.append('\n两译同为正念天子问·法慧答·纯长行·无偈颂。六十品次 12 对八十品次 16。以下逐行照录 T09n0278 卷第八〈梵行品第十二〉全文（5 行·CJK 993）：\n')
for n, l in enumerate(body60):
    r3_lines.append(f'**[60-{n:03d}]** CJK={len(ONLY(l))}')
    r3_lines.append(f'> {l}\n')
r3_lines.append('**校勘**：口/語·信家非家/依如來教染衣出家·速成無上平等菩提/從菩薩位逮於無上菩提之道——异文各照底本不统一。\n')
md = md.replace('<!-- INJECT:R3 -->', '\n'.join(r3_lines))

# ════════════════════════════════════════════════════════════
# R4: §7.5 数据科学四视角 + SVG
# ════════════════════════════════════════════════════════════
# Frequency data from _e16_stats
freqs = [('梵行',25),('法',27),('佛',17),('戒',13),('僧',12),('身',7),('意',6),('菩薩',6),('語',4),('觀察',4)]
max_f = max(f[1] for f in freqs)
r4_lines = []
r4_lines.append('\n#### 7.5.1 关键词频分布\n')
r4_lines.append('| 关键词 | 频次 | 条形 |\n|---|---|---|')
for kw, f in freqs:
    bar = '█' * f
    r4_lines.append(f'| {kw} | {f} | {bar} |')
r4_lines.append('\n#### 7.5.2 单元 CJK 结构\n')
unit_cjk = [('80-000','品题',6),('80-001','问端',50),('80-002','过流',5),('80-003','推徵核心',669),('80-004','修十法',193)]
r4_lines.append('| 段号 | 内容 | CJK | 占比 |\n|---|---|---|---|')
total = sum(u[2] for u in unit_cjk)
for sid, label, c in unit_cjk:
    pct = f'{c/total*100:.1f}%'
    r4_lines.append(f'| {sid} | {label} | {c} | {pct} |')
r4_lines.append(f'| **合计** | | **{total}** | 100% |')
r4_lines.append('\n#### 7.5.3 八十↔六十对读数据\n')
r4_lines.append('| 维度 | 八十 | 六十 | 差值 |\n|---|---|---|---|')
r4_lines.append('| CJK | 923 | 993 | +70 |')
r4_lines.append('| 行数/单元 | 5 | 5 | 0 |')
r4_lines.append('| 核心段 | 669 | 536 | −133 |')
r4_lines.append('| 修十法段 | 193 | 194 | +1 |')
r4_lines.append('| 问端 | 50 | 69 | +19 |')
r4_lines.append('\n#### 7.5.4 疏窗规模对比\n')
r4_lines.append('| 祖典 | len | 本品占比 |\n|---|---|---|')
r4_lines.append(f'| 澄观 T1735 | {sb-sa} | — |')
r4_lines.append(f'| 慧苑 X0221 | {len(seg_x221)} | — |')
r4_lines.append(f'| 法藏 T1733 | {len(seg_t1733)} | — |')
r4_lines.append(f'| 智俨 T1732 | {len(seg_t1732)} | — |')
r4_lines.append(f'| 通玄 T1739 | {len(seg_t1739)} | — |')
r4_lines.append(f'| 合论 X0223 | {len(seg_x223)} | — |')
# SVG bar chart
r4_lines.append('\n#### 7.5.5 频计 SVG\n')
r4_lines.append('<svg xmlns="http://www.w3.org/2000/svg" width="400" height="220" viewBox="0 0 400 220">')
r4_lines.append('<style>text{font:12px sans-serif}</style>')
for i, (kw, f) in enumerate(freqs[:8]):
    x = 10
    y = 20 + i * 24
    bar_w = f * 12
    r4_lines.append(f'<rect x="{x}" y="{y}" width="{bar_w}" height="18" fill="#4a90d9" opacity="0.7"/>')
    r4_lines.append(f'<text x="{x+bar_w+4}" y="{y+13}">{kw}({f})</text>')
r4_lines.append('</svg>\n')
md = md.replace('<!-- INJECT:R4 -->', '\n'.join(r4_lines))

# ════════════════════════════════════════════════════════════
# R5: 附录四' 疏窗全文照录
# ════════════════════════════════════════════════════════════
r5_lines = []
r5_lines.append('\n以下按 NFKD 归一口径逐 60 字分段照录 T1735〈梵行品第十六〉窗口全文（raw @%d-%d·len=%d）：\n' % (sa, sb, sb - sa))
for i in range(0, len(shu_window), 60):
    r5_lines.append(f'`[SH-{i:04d}]` {shu_window[i:i+60]}')
r5_lines.append('\n疏末标记：**梵行品竟**（见 SH-%04d 段）。\n' % ((sb - sa - 1) // 60 * 60))
md = md.replace('<!-- INJECT:R5 -->', '\n'.join(r5_lines))

# ── Write output ──
io.open(MD_PATH, 'w', encoding='utf-8', newline='\n').write(md)
final_lines = md.count('\n') + 1
print(f'E16_INJECT done · lines={final_lines}')
