# -*- coding: utf-8 -*-
"""enrich_p1938_notes.py — L.472 批A/B：P19-P38 注疏选要充实（六源程序抽取·逐字回源）

原则：
  · 全部引文自仓内一手源程序抽取（繁体原字形·NFKC 部首归一），不手写；
  · 抽取即回源（文本直接取自源文件），截断只允许句界＋「……」＋从略注记；
  · 卷号自文中「疏卷第X」标记实测推导，不臆造；
  · 道霈取窗修复：跳过卷首目录块，锚正文段。

用法：python scripts/enrich_p1938_notes.py          # 干跑
      python scripts/enrich_p1938_notes.py --apply  # 写入
"""
import io, os, re, sys, glob, unicodedata
sys.stdout.reconfigure(encoding='utf-8')

APPLY = '--apply' in sys.argv
ROOT = '.'

def load(fp):
    """清洗为纯文本；去全部空白；epub 提取本做 NFKC 部首归一（⼗→十 等）"""
    raw = io.open(fp, encoding='utf-8', errors='ignore').read()
    t = re.sub(r'<[^>]+>', '', raw)
    t = unicodedata.normalize('NFKC', t)
    return re.sub(r'\s+', '', t)

def han(s):
    return len(re.findall(r'[\u3400-\u9fff]', s))

SRC = {
    'shu': load('data/references/cbeta/T35n1735.xml'),
    'chao': load('data/references/cbeta_txt/T1736_澄观_随疏演义钞.txt'),
    'lilun': load('data/references/cbeta_txt/T1739_李通玄_新华严经论.txt'),
    'helun': load('data/references/cbeta_txt/X0223_李通玄_华严经合论.txt'),
    'huiyuan': load('data/references/cbeta_txt/X0221_慧苑_续华严略疏刊定记.txt'),
    'daopei': load('data/references/cbeta_txt/B0002_疏论纂要_epub提取本.txt'),
}

# ── 品表（八十华严序·含写法变体）──
CHAPTERS = [
    (19, r'[升昇]夜摩天[宮宫]品'),
    (20, r'夜摩[宮宫]中偈[讚赞]品'),
    (21, r'十行品'),
    (22, r'十無盡藏品'),
    (23, r'[升昇]兜率天[宮宫]品'),
    (24, r'兜率[宮宫]中偈[讚赞]品'),
    (25, r'十[迴回向廻]向品|十[迴回]向品'),
    (26, r'十地品'),
    (27, r'十定品'),
    (28, r'十通品'),
    (29, r'十忍品'),
    (30, r'阿僧祇品'),
    (31, r'壽量品|壽命品'),
    (32, r'諸菩薩住處品|菩薩住處品'),
    (33, r'佛不思議法品'),
    (34, r'十身相海品|如來十身相海品'),
    (35, r'隨好光明'),
    (36, r'普賢行品|普賢菩薩行品'),
    (37, r'如來出現品|寶王如來性起品'),
    (38, r'離世間品'),
]

RELEASE_ANCHOR = re.compile(
    r'(將釋此品|釋此一品|解此一品|釋此一會|釋此)[^。]{0,26}(分別|初來意|來意)')

SENT_END = re.compile(r'[。！？」』]')
HAN_RE = re.compile(r'[\u3400-\u9fff]')

def sentence_cut(text, limit):
    """句界截断：han 计数达限后，落在下一个句末符处（绝不切句中）"""
    if han(text) <= limit:
        return text, False
    acc = 0
    cut = 0
    for i, ch in enumerate(text):
        if HAN_RE.match(ch):
            acc += 1
        if acc >= limit and ch in '。！？」』':
            cut = i + 1
            break
    if cut == 0:
        cut = limit
    return text[:cut], True

def section_start(text, title_re, from_pos=0):
    """品题出现且其后 140 字内有 釋品/來意 锚 → 视为该品疏解段起点"""
    for m in re.finditer(title_re, text[from_pos:]):
        pos = from_pos + m.start()
        window = text[pos:pos + 140]
        if RELEASE_ANCHOR.search(window) or '來意' in window[:100]:
            return pos, m.group(0)
    return None, None

def juan_before(text, pos):
    """pos 前最近一处「疏卷第X」→ 漢数字卷号"""
    seg = text[:pos]
    ms = re.findall(r'疏卷第([一二三四五六七八九十百]+)', seg)
    return ms[-1] if ms else None

def t1735_section(pin, title_re, starts_map=None, ordered=None):
    """澄观疏：本品段（起点=全局单调分配的品题+釋品/來意锚；终点=下一品锚）"""
    text = SRC['shu']
    if starts_map is None:
        starts_map, ordered = t1735_starts()
    idx = CHAPTERS.index([c for c in CHAPTERS if c[0] == pin][0])
    start = starts_map.get(pin)
    if start is None:
        return None
    nxt = [starts_map[c[0]] for c in CHAPTERS[idx + 1:] if c[0] in starts_map and starts_map[c[0]] > start]
    end = min(nxt) if nxt else len(text)
    seg = text[start:end]
    vol = juan_before(text, start)
    return seg, vol

def t1735_starts():
    """一次性收集全部品段的合格起点（品题±160 内有釋品/來意），按文件序单调分配"""
    text = SRC['shu']
    cands = {}
    for pin, tre in CHAPTERS:
        for m in re.finditer(tre, text):
            w = text[m.start():m.start() + 160]
            if RELEASE_ANCHOR.search(w) or '來意' in w[:110]:
                cands.setdefault(pin, []).append(m.start())
    res, cursor = {}, 0
    for pin, _tre in CHAPTERS:
        for pos in cands.get(pin, []):
            if pos >= cursor:
                res[pin] = pos
                cursor = pos
                break
    return res, CHAPTERS

OTHER_TITLES = [re.compile(c[1]) for c in CHAPTERS] + [
    # 全经品题（防窗跨品串 Content）
    re.compile(r'世主妙嚴品|如來現相品|普賢三昧品|世界成就品|華藏世界品|毘盧遮那品'),
    re.compile(r'如來名號品|四聖諦品|四諦品|光明覺品|如來光明覺品'),
    re.compile(r'菩薩問明品|菩薩明難品|淨行品|賢首品|賢首菩薩品'),
    re.compile(r'佛[升昇]須彌[頂顶]品|[升昇]須彌[山山頂顶]品|須彌[頂顶]上偈[讚赞]品'),
    re.compile(r'菩薩雲集妙勝殿上說偈品|十住品|菩薩十住品|梵行品'),
    re.compile(r'初發心功德品|初發心菩薩功德品|明法品'),
    re.compile(r'入法界品'),
]

def window_passages(text, title_re, n=2, cap=1100, min_han=160, junk_extra=None):
    """论/记/钞类：品题间跨度取窗（n 段·最长优先）；
    窗内在首个「他品题」处截断（防串品）；过滤 epub 目录/版式家具"""
    pos = [m.start() for m in re.finditer(title_re, text)]
    if len(pos) < 2:
        return []
    spans = []
    for a, b in zip(pos, pos[1:]):
        seg = text[a:b]
        # 串品截断：窗内 50 字后首个他品题处切
        cuts = [m.start() for rgt in OTHER_TITLES
                for m in [rgt.search(seg[50:])] if m]
        if cuts:
            seg = seg[:50 + min(cuts)]
        if han(seg) < min_han:
            continue
        if re.search(r'目次|贊助|編輯說明|>>', seg[:400]):
            continue
        if junk_extra and junk_extra.search(seg[:200]):
            continue
        spans.append(seg)
    spans.sort(key=han, reverse=True)
    out = []
    for seg in spans[:n]:
        cut, trimmed = sentence_cut(seg, cap)
        out.append((cut, trimmed))
    return out

def daopei_body(title_re, min_han=160):
    """道霈纂要正文窗：目录串污染过滤（『品疏論纂要』连现即弃）＋他品题截断"""
    junk = re.compile(r'品疏論纂要.{0,60}品疏論纂要|品疏論纂要.{0,30}第八十')
    wins = window_passages(SRC['daopei'], title_re, n=1, cap=800, min_han=min_han,
                           junk_extra=junk)
    return wins[0] if wins else (None, None)

# ── md 定位与替换 ──
def md_path(pin):
    g = glob.glob('docs/经学文献/华严经细读/**/华严经细读_第%s部_*.md' % '一二三四五六七八九十'[pin - 1] if pin <= 10 else
                  ('第%s部' % _cn(pin)), recursive=True)
    return g[0] if g else None

def _cn(n):
    if n <= 10:
        return '一二三四五六七八九十'[n - 1]
    if n < 20:
        return '十' + '一二三四五六七八九'[n - 11]
    if n == 20:
        return '二十'
    if n < 30:
        return '二十' + '一二三四五六七八九'[n - 21]
    if n == 30:
        return '三十'
    if n < 40:
        return '三十' + '一二三四五六七八九'[n - 31]
    return str(n)

def replace_section(md, sec_start_marker, sec_end_re, new_body):
    """替换 sec_start_marker 之后至 sec_end_re 之前的内容（保留 marker 行）"""
    i = md.find(sec_start_marker)
    if i < 0:
        return md, False
    i_end_head = i + len(sec_start_marker)
    m = re.search(sec_end_re, md[i_end_head:])
    if not m:
        return md, False
    return md[:i_end_head] + '\n' + new_body + '\n\n' + md[i_end_head + m.start():], True

# ── 主流程 ──
report = []
for pin, title_re in CHAPTERS:
    fp = None
    g = glob.glob('docs/经学文献/华严经细读/**/*第%s部_*.md' % _cn(pin), recursive=True)
    if not g:
        report.append('品%d: md 未定位' % pin)
        continue
    fp = g[0]
    md = io.open(fp, encoding='utf-8').read()

    # ── 5.1 澄观疏全段 ──
    sec = t1735_section(pin, title_re)
    new51 = None
    if sec:
        seg, vol = sec
        seg = re.sub(r'^[\d\s]+', '', seg)          # 削品号残留（如段首「32」）
        seg = re.sub(r'[\d\s]+$', '', seg)
        cut, trimmed = sentence_cut(seg, 2800)
        note = '（《疏》%s·本品疏文全段·程序抽取逐字回源%s——来意/释名/宗趣/正释四门见引·L.472）' % (
            ('卷' + vol) if vol else '（卷号未定位）', '·后正释从略' if trimmed else '')
        new51 = '> ' + cut + '\n\n' + ('……（疏文后段从略——全文回源 `T1735`）\n\n' if trimmed else '') + note

    # ── 5.2 诸家：钞/李论/合论/慧苑/道霈 ──
    blocks = []
    # 钞：本品牌题窗
    chao = window_passages(SRC['chao'], title_re, n=1, cap=1100)
    if chao:
        blocks.append(('澄观《隨疏演義鈔》', chao[0]))
    # 论两种：取窗
    for key, label in [('lilun', '李通玄《新華嚴經論》'), ('helun', '李通玄《華嚴經合論》'), ('huiyuan', '慧苑《續華嚴略疏刊定記》')]:
        wins = window_passages(SRC[key], title_re, n=1, cap=1000)
        if wins:
            blocks.append((label, wins[0]))
    # 道霈正文窗（批B：修卷首目录污染）
    dp, dp_trim = daopei_body(title_re)
    if dp:
        blocks.append(('道霈《華嚴經疏論纂要》', (dp, dp_trim)))
    if not blocks:
        # 兜底：道霈宽窗（min_han 60）
        dp2, dp2_trim = daopei_body(title_re, min_han=60)
        if dp2:
            blocks.append(('道霈《華嚴經疏論纂要》', (dp2, dp2_trim)))

    new52 = '（程序抽取逐字回源·各一段·L.472）\n\n' + '\n\n'.join(
        '**%s**（%d 字·程序抽取%s）：\n\n> %s%s' % (
            label, han(cut), '·句界截断' if trimmed else '', cut,
            '\n\n……（后文从略）' if trimmed else '')
        for label, (cut, trimmed) in blocks) if blocks else '（本批程序取窗未获诸家对本品的独立疏解段——如实记阙·待后续批专检。）'

    report.append('品%-3d 5.1:%s 5.2块:%d  文件:%s' % (
        pin, (str(han(cut)) + ('截' if trimmed else '')) if sec else '未定位', len(blocks), os.path.basename(fp)[:20]))

    if APPLY and (new51 or blocks):
        # 5.1 替换
        m51 = re.search(r'### 5\.1[^\n]*\n', md)
        if m51 and new51:
            head_end = m51.end()
            m52 = re.search(r'### 5\.2', md[head_end:])
            body_end = head_end + (m52.start() if m52 else 0)
            md = md[:head_end] + '\n' + new51 + '\n\n' + md[body_end:]
        # 5.2 替换
        m52 = re.search(r'### 5\.2[^\n]*\n', md)
        if m52 and blocks:
            head_end = m52.end()
            mnext = re.search(r'\n### |\n## ', md[head_end:])
            body_end = head_end + (mnext.start() + 1 if mnext else len(md) - head_end)
            md = md[:head_end] + '\n' + new52 + '\n\n' + md[body_end:]
        io.open(fp, 'w', encoding='utf-8', newline='').write(md)

print('== 干跑 ==' if not APPLY else '== 已写入 ==')
for line in report:
    print(line)
