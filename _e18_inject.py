# -*- coding: utf-8 -*-
"""_e18_inject.py — L.198 P18《明法品》六要素注入（≥1200 行基线）
   R1 全文逐段入文(32 单元·两 lg 分行) · R2 澄观疏长摘 · R2b-R2f 五家（法藏·智俨·慧苑·通玄·合论）
   R3 六十〔卷九未入库占位〕 · R4 数科四视角(十法矩阵)+SVG · R5 附录四'疏窗全文照录
   幂等：从 _e18_md_backup.md 恢复后注入。
   教训承接：「昇」(U+6607) 无 NFKD 折叠——end marker 一律用变体列表取最先命中。
"""
import io, re, unicodedata, os
import xml.etree.ElementTree as ET

MD_PATH = 'docs/经学文献/华严经细读/第三会_忉利天宫_差别因果周/华严经细读_第十八部_明法品.md'
SKIP = {'note', 'rdg', 'mulu', 'pb', 'anchor', 'app'}
norm = lambda ch: (unicodedata.normalize('NFKD', ch)[0] if unicodedata.normalize('NFKD', ch) else ch)
ONLY = lambda s: ''.join(ch for ch in (norm(c) for c in s) if '\u4e00' <= ch <= '\u9fff')

def find_first(s, cands, base):
    best = -1
    for c in cands:
        q = s.find(c, base)
        if q >= 0 and (best < 0 or q < best): best = q
    return best

# ── backup once (idempotent restore) ──
BAK = '_e18_md_backup.md'
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

iC = fullC.find('明法品第十八')
kC = find_first(fullC, ['昇夜摩天宮品第十九', '升夜摩天宮品第十九'], iC + 6)
assert 0 < iC < kC, (iC, kC)
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

# ── 疏窗 T1735（澄观） ──
shu = io.open('data/references/cbeta_txt/T1735_澄观_华严经疏.txt', encoding='utf-8').read()
nsh = ''.join(norm(c) for c in shu)
sa = nsh.find('明法品第十八')
sb = find_first(nsh, ['升夜摩天宮品第十九', '昇夜摩天宮品第十九'], sa + 5)
assert 0 < sa < sb, (sa, sb)
shu_window = nsh[sa:sb]

# ── 祖典窗口（变体 end marker · 最先命中） ──
def get_win(path, start_marker, end_markers, skip_first=0, min_pos=0):
    if isinstance(end_markers, str): end_markers = [end_markers]
    raw = io.open(path, encoding='utf-8').read()
    n = ''.join(norm(c) for c in raw)
    pos = 0
    for _ in range(skip_first + 1):
        pos = n.find(start_marker, max(pos, min_pos - 1) + 1)
    end = -1
    for em in end_markers:
        q = n.find(em, pos + len(start_marker))
        if q >= 0 and (end < 0 or q < end): end = q
    if end < 0: end = pos + 8000
    return n[pos:end], pos, end

seg_t1733, p133, e133 = get_win('data/references/cbeta_txt/T1733_法藏_探玄记.txt', '明法品第十四', '昇夜摩天宮')
seg_t1732, p132, e132 = get_win('data/references/cbeta_txt/T1732_智俨_搜玄记.txt', '明法品第十四', '夜摩')
seg_x221, p21, e21 = get_win('data/references/cbeta_txt/X0221_慧苑_续华严略疏刊定记.txt', '明法品第十八', ['昇夜摩天', '升夜摩天'], skip_first=1)
seg_t1739, p739, e739 = get_win('data/references/cbeta_txt/T1739_李通玄_新华严经论.txt', '明法品第十八', ['昇夜摩天宮品第十九', '升夜摩天宮品第十九'])
seg_x223, p723, e723 = get_win('data/references/cbeta_txt/X0223_李通玄_华严经合论.txt', '明法品第十八', '昇夜摩天宮', min_pos=300000)

def wrap_text(text, width=58):
    out = []
    while text:
        out.append(text[:width])
        text = text[width:]
    return out

# ── Read skeleton ──
md = io.open(BAK, encoding='utf-8').read()

# ═══ R1: 全文逐段入文（32 单元·两 lg 分行）═══
r1 = ['\n以下按 CBETA T10n0279 平文器 32 单元（1 head + 28 p + 2 lg + 1 byline）逐段照录八十华严〈明法品第十八〉全文。各段标号与 §2.0 结构总表对应。\n']
for n, (tag, pos, t, tc) in enumerate(units):
    r1.append('**80-%03d**（`%s`·CJK %d）：\n' % (n, tag, len(tc)))
    if tag == 'lg':
        vlines = [v.strip() for v in re.split(r'\s{2,}', t) if v.strip()]
        r1.append('>\n')
        for v in vlines:
            r1.append('> ' + v)
        r1.append('>\n')
    else:
        r1.append('> ' + t + '\n')
md = md.replace('<!-- INJECT:R1 全文逐段入文（32 单元）· 由 _e18_inject.py 生成 -->', '\n'.join(r1))

# ═══ R2: 澄观疏科长文全摘 ═══
r2 = ['\n澄观疏窗口 T1735·NFKD 坐标 @%d-%d·raw len=%d·科判四门（来意·释名·宗趣·释文），释文正判**三分**（请说·正说·结说），正说分「答前十問。即為十段」，重颂分「十頌分二」。疏末记「第三會竟·大方廣佛華嚴經疏卷第二十」。\n' % (sa, sb, sb - sa)]
r2.append('以下按疏文自然段 60 字标尺分段照录，保留 CBETA 繁体原字形：\n')
for block in wrap_text(shu_window, 60):
    r2.append('> ' + block)
r2.append('')
md = md.replace('<!-- INJECT:R2 澄观疏窗长摘（来意·释名四义·宗趣教理行果·科三分·十段答·十度详释·第三会竟）· 由 _e18_inject.py 生成 -->', '\n'.join(r2))

# ═══ R2b: 法藏 T1733 ═══
r2b = ['\n法藏窗口 T1733（六十品题〈明法品第十四〉）·NFKD @%d-%d·len=%d·四门同前·释名四义·记末结「此上第三會竟」（探玄记卷五尽处）：\n' % (p133, e133, len(seg_t1733))]
for block in wrap_text(seg_t1733, 58):
    r2b.append('> ' + block)
r2b.append('')
md = md.replace('<!-- INJECT:R2b 法藏探玄记选要 -->', '\n'.join(r2b))

# ═══ R2c: 智俨 T1732（本品有文·非缺口）═══
r2c = ['\n智俨窗口 T1732·NFKD @%d-%d·len=%d·**本品现存残卷覆盖**（异于第十七品〔缺口〕）·辨名二门（約教·約行）·来意「用前行德更修，與後地為方便故也」：\n' % (p132, e132, len(seg_t1732))]
for block in wrap_text(seg_t1732, 58):
    r2c.append('> ' + block)
r2c.append('')
md = md.replace('<!-- INJECT:R2c 智俨搜玄记选要 -->', '\n'.join(r2c))

# ═══ R2d: 慧苑 X0221 ═══
r2d = ['\n慧苑窗口 X0221·NFKD @%d-%d·len=%d（本品诸家最长·含「品第十八之餘」段）·按梵本五翻（達摩阿嚕迦娜忙鉢里勿多）·引《摄大乘》五说：\n' % (p21, e21, len(seg_x221))]
for block in wrap_text(seg_x221, 58):
    r2d.append('> ' + block)
r2d.append('')
md = md.replace('<!-- INJECT:R2d 慧苑刊定记选要 -->', '\n'.join(r2d))

# ═══ R2e: 李通玄 T1739 ═══
r2e = ['\n通玄窗口 T1739·NFKD @%d-%d·len=%d·三门分别（释品名目·释品来意·随文释义）·「第一令前五品之法其心更明。第二令後所行之法轉勝明白」立义：\n' % (p739, e739, len(seg_t1739))]
for block in wrap_text(seg_t1739, 58):
    r2e.append('> ' + block)
r2e.append('')
md = md.replace('<!-- INJECT:R2e 李通玄新华严经论选要 -->', '\n'.join(r2e))

# ═══ R2f: 合论 X0223 ═══
r2f = ['\n合论窗口 X0223·NFKD @%d-%d·len=%d·【論】体·经论交映·文末判第四会科由（序分·正说分·流通分）：\n' % (p723, e723, len(seg_x223))]
for block in wrap_text(seg_x223, 58):
    r2f.append('> ' + block)
r2f.append('')
md = md.replace('<!-- INJECT:R2f 合论选要 -->', '\n'.join(r2f))

# ═══ R3: 六十〔卷九未入库占位〕═══
r3 = ['\n本品在六十华严（T09n0278）相当者为〈明法品第十四〉——法藏《探玄记》、智俨《搜玄记》皆依六十品题科之（两疏窗口品题直证·见 §5.2/§5.3）。其文存于**卷第九**。本仓 `data/references/cbeta_txt/` 目前仅入库卷一–卷八（卷八止于〈梵行品第十二〉），卷九**尚未入库**，故本品六十全文照录**〔待核·未入库〕**。\n']
r3.append('| 八十（T10n0279） | 六十（T09n0278） | 卷次 | 状态 |\n|---|---|---|---|')
r3.append('| 明法品第十八 | 明法品第十四 | 卷第九 | 〔未入库·待核〕 |')
r3.append('\n**口径**：仅登记品题对应（八十第十八 ↔ 六十第十四），不作正文逐字对读，不臆造等值（承第二会 P8 铁律）。卷九入库后可补 §6.3 六十全本照录〔未竟·待后续批〕。\n')
md = md.replace('<!-- INJECT:R3 六十对读〔未入库·如实标注占位〕 -->', '\n'.join(r3))

# ═══ R4: §7.5 数科四视角 + SVG（十法矩阵）═══
freqs = [('佛子',34),('如來',29),('莊嚴',26),('波羅蜜',23),('清淨',22),('說法',22),
         ('歡喜',16),('十種',15),('精進',13),('無盡藏',12),('菩薩摩訶薩',12),
         ('一切智',11),('三昧',11),('不放逸',8),('法慧',4),('三寶',4),('菩提心',3),('阿僧祇',1)]
r4 = ['\n本品为第三会收束品（CJK 5,529），核心为「答前十問。即為十段」之**十法矩阵**。数据科学视角聚焦十数条目之密度分布与长行/双颂之体量结构。\n']
r4.append('\n#### 7.5.1 关键词频分布（body80 CJK-only 实测）\n')
r4.append('| 关键词 | 频次 | 条形 |\n|---|---|---|')
for kw, f in freqs:
    r4.append('| %s | %d | %s |' % (kw, f, '█' * min(f, 34)))
r4.append('\n> 计数口径：body80 = fullC[@118152:@123681]，CJK-only（U+4E00–U+9FFF）·标点不计。数据源 `_e18_stats.txt`。「阿僧祇」仅 ×1——与第十七品校量数海（×21）断崖对照。\n')

r4.append('\n#### 7.5.2 十法矩阵·组次索引（答与问段段相应）\n')
grp = [('十不放逸','80-009','護持眾戒乃至恒善觀察自相續力'),
       ('十種清淨','80-010','如說而行乃至於授戒和尚常生尊重'),
       ('十令佛喜·上','80-011','精進不退乃至依無作門修諸淨行'),
       ('十令佛喜·下','80-012','安住不放逸乃至安住智慧觀無所住'),
       ('十速入諸地','80-013','善巧圓滿福智二行乃至與三世佛同體性'),
       ('住地十觀察','80-014','初住地時應善觀察十「隨」'),
       ('十行清淨','80-015','悉捨資財乃至知眾生與如來同體性'),
       ('十增勝法','80-016','他方諸佛皆悉護念乃至知如來方便之力'),
       ('十清淨願','80-017','成熟眾生乃至具普賢行淨治種智之門'),
       ('十法滿願','80-018','心無疲厭乃至常勤守護無上法門'),
       ('十無盡藏','80-019','普見諸佛藏乃至入無邊世界藏'),
       ('隨宜說法','80-020','知其所作·貪多說不淨·三毒等說勝智'),
       ('十波羅蜜','80-021','檀尸忍進禪般若方便願力智·是則能淨結句（CJK 695 最长段）'),
       ('紹三寶種','80-023','教發心·開法藏·善持教法·三番递釋'),
       ('十莊嚴','80-024','身語心佛剎光明眾會神通正教涅槃地巧說')]
r4.append('| 序 | 组名 | 单元 | 纲目（首尾句） |\n|---|---|---|---|')
for i, (g, u, s) in enumerate(grp):
    r4.append('| %d | %s | %s | %s |' % (i+1, g, u, s))
r4.append('\n> 澄观科：「前中答前十問。即為十段。今初段中有五十句。前二十句答前修習。後三十句答令佛歡喜」；另问端行体十句·德用十二事·自在力十一句（见 §4.2）。\n')

r4.append('\n#### 7.5.3 长行 / 双颂体量\n')
proseC, v1, v2 = 4921, 308, 280
r4.append('| 部类 | 单元 | CJK | 占比 |\n|---|---|---|---|')
r4.append('| 长行（p） | 28 | %d | %.1f%% |' % (proseC, proseC/5529*100))
r4.append('| 问端颂（lg·80-006） | 1 | %d | %.1f%% |' % (v1, v1/5529*100))
r4.append('| 结颂（lg·80-029） | 1 | %d | %.1f%% |' % (v2, v2/5529*100))
r4.append('| 品题·译场（head/byline） | 2 | 20 | 0.4%% |')
r4.append('| **合计（CJK-only 品界）** | 32 | **5,529** | 100%% |')
r4.append('\n> 两处重颂七言·双空格分行各 22／20 行·净句段均长 7.0 言（实测 `_e18_stats.txt`）。长行中前后各嵌一颂，为第三会诸品所仅见。\n')

r4.append('\n#### 7.5.4 六家疏窗规模对比\n')
r4.append('| 祖典 | 窗口 len（NFKD） | 说明 |\n|---|---|---|')
r4.append('| 慧苑 X0221 | %d | 本品诸家最长·含「品第十八之餘」 |' % len(seg_x221))
r4.append('| 合论 X0223 | %d | 【論】体·判第四会科由 |' % len(seg_x223))
r4.append('| 澄观 T1735 | %d | 四门·科三分·第三会竟·主源 |' % (sb-sa))
r4.append('| 法藏 T1733 | %d | 六十品题〈明法品第十四〉·此上第三會竟 |' % len(seg_t1733))
r4.append('| 通玄 T1739 | %d | 三门分别·明前明后两义 |' % len(seg_t1739))
r4.append('| 智俨 T1732 | %d | **本品有文**·残卷覆盖（异于 P17 缺口） |' % len(seg_t1732))

# SVG：十法矩阵图（答前十问·十段为经·十数为纬）
r4.append('\n#### 7.5.5 图 7-1 十法矩阵（第三会收束·结归十住位）\n')
r4.append('<svg xmlns="http://www.w3.org/2000/svg" width="680" height="430" viewBox="0 0 680 430">')
r4.append('<style>text{font:11px sans-serif;fill:#222}.t{font-size:13px}.s{font-size:9px;fill:#555}</style>')
r4.append('<rect width="680" height="430" fill="#fbfbfd"/>')
r4.append('<text class="t" x="16" y="24">明法品 · 十法矩阵：精进慧问 → 法慧十段答（单元号标注）</text>')
cells = [('不放逸','009'),('清淨','010'),('佛喜·上','011'),('佛喜·下','012'),
         ('速入地','013'),('住觀察','014'),('行清淨','015'),('增勝','016'),
         ('清淨願','017'),('滿願','018'),('無盡藏','019'),('隨宜說','020'),
         ('十波羅蜜','021'),('紹三寶','023'),('十莊嚴','024'),('趣第四會','→19')]
for i, (g, u) in enumerate(cells):
    x = 24 + (i % 4) * 162
    y = 48 + (i // 4) * 92
    hl = 'fill="#b5462f"' if (g in ('十波羅蜜','無盡藏') or g == '趣第四會') else 'fill="#4a90d9"'
    r4.append('<rect x="%d" y="%d" width="148" height="72" rx="8" %s opacity="0.16" stroke="#4a90d9" stroke-width="1.2"/>' % (x, y, hl))
    r4.append('<text x="%d" y="%d">%s</text>' % (x+12, y+32, g))
    r4.append('<text class="s" x="%d" y="%d">80-%s</text>' % (x+12, y+54, u))
r4.append('<text class="s" x="24" y="420">口径：品界 T10n0279 CJK-only @118152-123681（5,529）·澄观科「答前十問。即為十段」</text>')
r4.append('</svg>\n')
md = md.replace('<!-- INJECT:R4 数科四视角＋图 7-1 十法矩阵 SVG· 由 _e18_inject.py 生成 -->', '\n'.join(r4))

# ═══ R5: 附录四' 疏窗全文照录 ═══
r5 = ['\n以下按 NFKD 归一口径逐 60 字分段照录 T1735〈明法品第十八〉窗口全文（raw @%d-%d·len=%d）：\n' % (sa, sb, sb - sa)]
for i in range(0, len(shu_window), 60):
    r5.append('`[SH-%04d]` %s' % (i, shu_window[i:i+60]))
r5.append('\n疏末：**第三會竟**。**大方廣佛華嚴經疏卷第二十**（本品疏毕·第三会疏终卷）。\n')
md = md.replace("<!-- INJECT:R5 附录四′ 澄观疏窗全文照录· 由 _e18_inject.py 生成 -->", '\n'.join(r5))

# ── Write output ──
io.open(MD_PATH, 'w', encoding='utf-8', newline='\n').write(md)
final_lines = md.count('\n') + 1
print('E18_INJECT done · lines=%d · body80=%d · shun=%d · x221=%d · t1732=%d' % (final_lines, len(body80), sb-sa, len(seg_x221), len(seg_t1732)))
