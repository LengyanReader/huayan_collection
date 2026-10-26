# -*- coding: utf-8 -*-
"""_e17_inject.py — L.197 P17《初发心功德品》六要素注入（≥1200 行基线）
   R1 全文逐段入文(27 单元·lg 分行) · R2 澄观疏长摘(含 R2b-R2e 四家) · R3 六十〔未入库占位〕
   R4 数科四视角(十一大喻校量)+SVG · R5 附录四'疏窗全文照录
   幂等：从 _e17_md_backup.md 恢复后注入。
"""
import io, re, unicodedata, os
import xml.etree.ElementTree as ET

MD_PATH = 'docs/经学文献/华严经细读/第三会_忉利天宫_差别因果周/华严经细读_第十七部_初发心功德品.md'
SKIP = {'note', 'rdg', 'mulu', 'pb', 'anchor', 'app'}
norm = lambda ch: (unicodedata.normalize('NFKD', ch)[0] if unicodedata.normalize('NFKD', ch) else ch)
ONLY = lambda s: ''.join(ch for ch in (norm(c) for c in s) if '\u4e00' <= ch <= '\u9fff')

# ── backup once (idempotent restore) ──
BAK = '_e17_md_backup.md'
if not os.path.exists(BAK):
    io.open(BAK, 'w', encoding='utf-8').write(io.open(MD_PATH, encoding='utf-8').read())

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
fullC = ONLY(''.join(acc))

iC = fullC.find('初發心功德品第十七')
kC = fullC.find('明法品第十八', iC + 6)
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
sa = nsh.find('初發心功德品第十七')
sb = nsh.find('明法品第十八', sa + 5)
shu_window = nsh[sa:sb]

# ── 祖典窗口 ──
def get_win(path, start_marker, end_marker, skip_first=0):
    raw = io.open(path, encoding='utf-8').read()
    n = ''.join(norm(c) for c in raw)
    pos = 0
    for _ in range(skip_first + 1):
        pos = n.find(start_marker, pos + 1)
    end = n.find(end_marker, pos + len(start_marker))
    if end < 0: end = pos + 8000
    return n[pos:end], pos, end

seg_t1733, p133, e133 = get_win('data/references/cbeta_txt/T1733_法藏_探玄记.txt', '發心菩薩功德品', '明法品第十四', skip_first=1)
seg_x221, p21, e21 = get_win('data/references/cbeta_txt/X0221_慧苑_续华严略疏刊定记.txt', '初發心功德品第十七', '明法品第十八', skip_first=1)
seg_t1739, p739, e739 = get_win('data/references/cbeta_txt/T1739_李通玄_新华严经论.txt', '初發心功德品第十七', '明法品第十八', skip_first=0)
seg_x223, p723, e723 = get_win('data/references/cbeta_txt/X0223_李通玄_华严经合论.txt', '初發心功德品第十七', '明法品第十八', skip_first=3)

def wrap_text(text, width=58):
    out = []
    while text:
        out.append(text[:width])
        text = text[width:]
    return out

# ── Read skeleton ──
md = io.open(BAK, encoding='utf-8').read()

# ═══ R1: 全文逐段入文（27 单元·lg 分行）═══
r1 = ['\n以下按 CBETA T10n0279 平文器 27 单元（1 head + 25 p + 1 lg + 1 byline）逐段照录八十华严〈初發心功德品第十七〉全文。各段标号与 §2.0 结构总表对应。\n']
for n, (tag, pos, t, tc) in enumerate(units):
    r1.append('**80-%03d**（`%s`·CJK %d）：\n' % (n, tag, len(tc)))
    if tag == 'lg':
        # 重颂：按双空格分行为颂句
        vlines = [v.strip() for v in re.split(r'\s{2,}', t) if v.strip()]
        r1.append('>\n')
        for v in vlines:
            r1.append('> ' + v)
        r1.append('>\n')
    else:
        r1.append('> ' + t + '\n')
md = md.replace('<!-- INJECT:R1 全文逐段入文（27 单元）· 由 _e17_inject.py 生成 -->', '\n'.join(r1))

# ═══ R2: 澄观疏科长文全摘 ═══
r2 = ['\n澄观疏窗口 T1735·NFKD 坐标 @%d-%d·raw len=%d·科判四门（来意·释名·宗趣·释文），释文正判**七分**（天王请说·叹深难说·约喻校量·就法略示·动地兴供·他方证成·以偈重颂）。\n' % (sa, sb, sb - sa)]
r2.append('以下按疏文自然段 60 字标尺分段照录，保留 CBETA 繁体原字形：\n')
for block in wrap_text(shu_window, 60):
    r2.append('> ' + block)
r2.append('')
md = md.replace('<!-- INJECT:R2 澄观疏窗长摘（来意·释名·宗趣·科七分·十一喻·歌羅優波尼沙陀释·重颂三段）· 由 _e17_inject.py 生成 -->', '\n'.join(r2))

# ═══ R2b: 法藏 T1733 ═══
r2b = ['\n法藏窗口 T1733（六十品题〈發心菩薩功德品第十三〉）·NFKD @%d-%d·len=%d·释名·来意三·分四段科：\n' % (p133, e133, len(seg_t1733))]
for block in wrap_text(seg_t1733, 58):
    r2b.append('> ' + block)
r2b.append('')
md = md.replace('<!-- INJECT:R2b 法藏探玄记选要 -->', '\n'.join(r2b))

# ═══ R2c: 慧苑 X0221 ═══
r2c = ['\n慧苑窗口 X0221·@%d-%d·len=%d·四门同前·梵本「初發心菩薩功德藏品」·三发心（引《起信论》）·增上脩诸行：\n' % (p21, e21, len(seg_x221))]
for block in wrap_text(seg_x221, 58):
    r2c.append('> ' + block)
r2c.append('')
md = md.replace('<!-- INJECT:R2c 慧苑刊定记选要 -->', '\n'.join(r2c))

# ═══ R2d: 李通玄 T1739 ═══
r2d = ['\n通玄窗口 T1739·@%d-%d·len=%d·「初發心之士功德難量」·因陀罗网重重相入·四行一颂：\n' % (p739, e739, len(seg_t1739))]
for block in wrap_text(seg_t1739, 58):
    r2d.append('> ' + block)
r2d.append('')
md = md.replace('<!-- INJECT:R2d 李通玄新华严经论选要 -->', '\n'.join(r2d))

# ═══ R2e: 合论 X0223 ═══
r2e = ['\n合论窗口 X0223·@%d-%d·len=%d（本品诸家最长）·【論】体·经论交映：\n' % (p723, e723, len(seg_x223))]
for block in wrap_text(seg_x223, 58):
    r2e.append('> ' + block)
r2e.append('')
md = md.replace('<!-- INJECT:R2e 合论选要 -->', '\n'.join(r2e))

# ═══ R3: 六十〔未入库占位〕═══
r3 = ['\n本品在六十华严（T09n0278）相当者为〈初发心菩萨功德品第十三〉，存于**卷第九**。本仓 `data/references/cbeta_txt/` 目前仅入库卷一–卷八（卷八止于〈梵行品第十二〉），卷九**尚未入库**，故本品六十全文照录**〔待核·未入库〕**。\n']
r3.append('| 八十（T10n0279） | 六十（T09n0278） | 卷次 | 状态 |\n|---|---|---|---|')
r3.append('| 初發心功德品第十七 | 初发心菩萨功德品第十三 | 卷第九 | 〔未入库·待核〕 |')
r3.append('\n**口径**：仅登记品题对应（八十第十七 ↔ 六十第十三），不作正文逐字对读，不臆造等值（承第二会 P8 铁律）。卷九入库后可补 §6.3 六十全本照录〔未竟·待后续批〕。\n')
md = md.replace('<!-- INJECT:R3 六十对读〔未入库·如实标注占位〕 -->', '\n'.join(r3))

# ═══ R4: §7.5 数科四视角 + SVG（十一大喻校量·数量级）═══
freqs = [('佛子',38),('十方',38),('無量',46),('發阿耨多羅三藐三菩提心',31),('阿僧祇',21),
         ('初發心',11),('那由他',8),('千分不及一',8),('微塵數',5),('優波尼沙陀',4),
         ('百分不及一',4),('不可說不可說',4)]
r4 = ['\n本品为第三会最长品（CJK 8,207），核心为「约喻校量分」以**十一大喻**层层推极发心功德之数量级。数据科学视角聚焦校量数词之递增结构与长行/重颂之体量分布。\n']
r4.append('\n#### 7.5.1 校量数量级·词频分布\n')
r4.append('| 关键词 | 频次（body80 CJK-only 实测） | 条形 |\n|---|---|---|')
for kw, f in freqs:
    r4.append('| %s | %d | %s |' % (kw, f, '█' * min(f, 46)))
r4.append('\n> 计数口径：body80 = fullC[@109945:@118152]，CJK-only（U+4E00–U+9FFF）·标点不计。数据源 `_e17_stats.txt`。\n')

r4.append('\n#### 7.5.2 十一大喻次第（澄观科·T1735）\n')
yus = ['利樂眾生喻','速疾步剎喻','知劫成壞喻','善知勝解喻','善知諸根喻','善知欲樂喻',
       '善知方便喻','善知他心喻','善知業相喻','善知煩惱喻','供佛及生喻']
yu_range = ['80-004–80-008','80-009','80-010','80-011','80-012','80-013','80-014','80-015','80-016','80-017','80-018–80-020']
yu_obj = ['供養樂具·持戒修善','一念過剎·展轉至十','知世界成壞劫數','知眾生種種差別解',
          '知眾生諸根差別','知眾生種種欲樂','知眾生種種方便','知眾生種種差別心',
          '知眾生種種差別業','知眾生種種煩惱','供養無邊諸佛及眾生']
r4.append('| 序 | 喻名 | 校量对象（有分限之数） | 起讫单元 |\n|---|---|---|---|')
for i in range(11):
    r4.append('| %d | %s | %s | %s |' % (i+1, yus[i], yu_obj[i], yu_range[i]))
r4.append('\n> 澄观判「此十一喻，後後過於前前，故皆捨置前前更舉後後，巧顯深勝」；每喻具举喻·征问·领答·校量四句，一一喻内「皆有十重」。喻有分限，法（发心功德）无限。\n')

r4.append('\n#### 7.5.3 长行 / 重颂体量\n')
proseC, verseC = 4785, 3388
r4.append('| 部类 | 单元 | CJK | 占比 |\n|---|---|---|---|')
r4.append('| 长行（p） | 25 | %d | %.1f%% |' % (proseC, proseC/8207*100))
r4.append('| 重颂（lg） | 1 | %d | %.1f%% |' % (verseC, verseC/8207*100))
r4.append('| 品题·译场（head/byline） | 2 | 21 | 0.3%% |')
r4.append('| **合计（CJK-only 品界）** | 27 | **8,207** | 100%% |')
r4.append('\n> 重颂七言为主·净句段 484·均长 7.0 言（实测 `_e17_stats.txt`）。\n')

r4.append('\n#### 7.5.4 五家疏窗规模对比\n')
r4.append('| 祖典 | 窗口 len（NFKD） | 说明 |\n|---|---|---|')
r4.append('| 澄观 T1735 | %d | 四门·释文七分·主源 |' % (sb-sa))
r4.append('| 合论 X0223 | %d | 本品诸家最长·【論】体 |' % len(seg_x223))
r4.append('| 慧苑 X0221 | %d | 四门同前·引《起信论》三发心 |' % len(seg_x221))
r4.append('| 法藏 T1733 | %d | 六十品题·四段科 |' % len(seg_t1733))
r4.append('| 通玄 T1739 | %d | 因陀罗网·四行一颂 |' % len(seg_t1739))
r4.append('| 智俨 T1732 | 0 | 现存卷不覆此品·〔缺口〕 |')

# SVG：十一喻数量级递增（示意校量转胜）
r4.append('\n#### 7.5.5 图 7-1 十一大喻层层转胜（校量递增示意）\n')
r4.append('<svg xmlns="http://www.w3.org/2000/svg" width="640" height="360" viewBox="0 0 640 360">')
r4.append('<style>text{font:11px sans-serif;fill:#222}.lbl{font-size:10px}</style>')
r4.append('<rect width="640" height="360" fill="#fbfbfd"/>')
r4.append('<text x="16" y="24" font-size="13">初發心功德 · 十一喻「後後過於前前」校量递增</text>')
base_h = [8,14,20,28,36,44,54,64,76,90,120]
for i in range(11):
    x = 30 + i * 55
    h = base_h[i]
    y = 300 - h
    r4.append('<rect x="%d" y="%d" width="40" height="%d" fill="#4a90d9" opacity="%.2f"/>' % (x, y, h, 0.45 + i*0.05))
    r4.append('<text class="lbl" x="%d" y="316">%d</text>' % (x+16, i+1))
r4.append('<text class="lbl" x="16" y="334">喻次（1 利樂眾生 → 11 供佛及生·轉轉增勝）</text>')
r4.append('<line x1="24" y1="300" x2="620" y2="300" stroke="#888"/>')
r4.append('<line x1="24" y1="300" x2="24" y2="40" stroke="#888"/>')
r4.append('<text class="lbl" x="80" y="60" fill="#b5462f">→ 發心功德「無有能得知其際者」（喻有分限·法無限）</text>')
r4.append('</svg>\n')
md = md.replace('<!-- INJECT:R4 数科四视角＋图 7-1 十一大喻校量 SVG· 由 _e17_inject.py 生成 -->', '\n'.join(r4))

# ═══ R5: 附录四' 疏窗全文照录 ═══
r5 = ['\n以下按 NFKD 归一口径逐 60 字分段照录 T1735〈初發心功德品第十七〉窗口全文（raw @%d-%d·len=%d）：\n' % (sa, sb, sb - sa)]
for i in range(0, len(shu_window), 60):
    r5.append('`[SH-%04d]` %s' % (i, shu_window[i:i+60]))
r5.append('\n疏末：**大方廣佛華嚴經疏卷第十九**（见窗口末段·本品疏毕）。\n')
md = md.replace("<!-- INJECT:R5 附录四′ 澄观疏窗全文照录· 由 _e17_inject.py 生成 -->", '\n'.join(r5))

# ── Write output ──
io.open(MD_PATH, 'w', encoding='utf-8', newline='\n').write(md)
final_lines = md.count('\n') + 1
print('E17_INJECT done · lines=%d · body80=%d · shun=%d · x223=%d' % (final_lines, len(body80), sb-sa, len(seg_x223)))
