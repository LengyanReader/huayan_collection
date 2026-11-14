# -*- coding: utf-8 -*-
"""enrich_giant3.py — L.474：全经最大三品（P25 十回向·P26 十地·P38 离世间）注疏深窗增补
在 L.472 通用批之上追加：①疏文续引·二（正释段第二窗）②探玄记窗（P26/P38）③道霈深窗
④华藏妙海（海云玄谈·二手整理·标来源）相关段。全部程序抽取·逐字回源。
"""
import io, re, sys, glob, unicodedata
sys.stdout.reconfigure(encoding='utf-8')

APPLY = '--apply' in sys.argv

def load(fp):
    t = re.sub(r'<[^>]+>', '', io.open(fp, encoding='utf-8', errors='ignore').read())
    t = unicodedata.normalize('NFKC', t)
    return re.sub(r'\s+', '', t)

def han(s):
    return len(re.findall(r'[\u3400-\u9fff]', s))

SRC = {
    'shu': load('data/references/cbeta/T35n1735.xml'),
    'tanxuan': load('data/references/cbeta_txt/T1733_法藏_探玄记.txt'),
    'daopei': load('data/references/cbeta_txt/B0002_疏论纂要_epub提取本.txt'),
    'miaohai': load('data/references/huayan_daodu/华藏妙海_整理版_提取本.txt'),
}

HAN_RE = re.compile(r'[\u3400-\u9fff]')

def sentence_cut(text, limit):
    if han(text) <= limit:
        return text, False
    acc, cut = 0, 0
    for i, ch in enumerate(text):
        if HAN_RE.match(ch):
            acc += 1
        if acc >= limit and ch in '。！？」』':
            cut = i + 1
            break
    if cut == 0:
        cut = limit
    return text[:cut], True

# 品段起点（与 enrich_p1938_notes.py 同法·仅 P25/26/38 及其邻品锚）
REL = re.compile(r'(將釋此品|釋此一品|解此一品|釋此一會|釋此)[^。]{0,26}(分別|初來意|來意)')
CHS = [
    (25, r'十[迴回向廻]向品|十[迴回]向品'),
    (26, r'十地品'),
    (27, r'十定品'),
    (37, r'如來出現品|寶王如來性起品'),
    (38, r'離世間品'),
    (39, r'入法界品'),
]

def shu_section(pin):
    """T1735 本品疏段（起点=品题+釋品/來意锚·终点=下一品锚·单调）"""
    text = SRC['shu']
    cands = {}
    for p, tre in CHS:
        for m in re.finditer(tre, text):
            w = text[m.start():m.start() + 160]
            if REL.search(w) or '來意' in w[:110]:
                cands.setdefault(p, []).append(m.start())
    res, cursor = {}, 0
    for p, _tre in CHS:
        for pos in cands.get(p, []):
            if pos >= cursor:
                res[p] = pos
                cursor = pos
                break
    keys = sorted(res)
    i = keys.index(pin)
    start = res[pin]
    nxt = [res[k] for k in keys[i + 1:] if res[k] > start]
    end = min(nxt) if nxt else len(text)
    seg = re.sub(r'^[\d\s]+', '', text[start:end])
    seg = re.sub(r'[\d\s]+$', '', seg)
    return seg

def best_window(text, title_re, cap, junk=None, skip_first=0, min_han=200):
    pos = [m.start() for m in re.finditer(title_re, text)]
    if len(pos) < 2:
        return None, None
    spans = []
    for a, b in zip(pos, pos[1:]):
        seg = text[a:b]
        if han(seg) < min_han:
            continue
        if re.search(r'目次|贊助|編輯說明|>>', seg[:400]):
            continue
        if junk and junk.search(seg[:200]):
            continue
        spans.append(seg)
    spans = spans[skip_first:]
    if not spans:
        return None, None
    spans.sort(key=han, reverse=True)
    return sentence_cut(spans[0], cap)

JUNK_DP = re.compile(r'品疏論纂要.{0,60}品疏論纂要|品疏論纂要.{0,30}第八十')

# 三品的品题窗正则（各源检索用）
TITLE = {
    25: r'十[迴回]向品',
    26: r'十地品',
    38: r'離世間品',
}
KEYS = {25: '第二十五部', 26: '第二十六部', 38: '第三十八部'}

for pin in (25, 26, 38):
    g = glob.glob('docs/经学文献/华严经细读/**/华严经细读_%s_*.md' % KEYS[pin], recursive=True)
    if not g:
        print('品%d: md 未定位' % pin)
        continue
    fp = g[0]
    md = io.open(fp, encoding='utf-8').read()
    adds = []

    # ① 疏文续引·二（正释段第二窗）
    seg = shu_section(pin)
    if seg and han(seg) > 3000:
        rest = seg[2800:]
        cut, trimmed = sentence_cut(rest, 2800)
        adds.append(('5.1', '**澄观《華嚴經疏》·疏文续引（正释段第二窗·程序抽取逐字回源·L.474）**：\n\n> ' + cut +
                     ('\n\n……（后文从略——全文回源 `T1735`）' if trimmed else '')))

    # ② 探玄记窗（P26/P38·探玄记不释十回向·P25 跳过）
    if pin in (26, 38):
        cut, trimmed = best_window(SRC['tanxuan'], TITLE[pin], 1500)
        if cut:
            adds.append(('5.2', '**法藏《華嚴經探玄記》**（%d 字·程序抽取逐字回源%s）：\n\n> %s%s' % (
                han(cut), '·句界截断' if trimmed else '', cut,
                '\n\n……（后文从略）' if trimmed else '')))

    # ③ 道霈深窗（第二段·cap 1200）
    cut, trimmed = best_window(SRC['daopei'], TITLE[pin], 1200, junk=JUNK_DP, skip_first=1)
    if cut:
        adds.append(('5.2', '**道霈《華嚴經疏論纂要》·第二窗**（%d 字·程序抽取逐字回源%s）：\n\n> %s%s' % (
            han(cut), '·句界截断' if trimmed else '', cut,
            '\n\n……（后文从略）' if trimmed else '')))

    # ④ 华藏妙海（海云玄谈·二手整理·标来源）
    cut, trimmed = best_window(SRC['miaohai'], TITLE[pin], 800, min_han=120)
    if cut:
        adds.append(('5.2', '**海云《華藏妙海》（整理版·二手整理·标来源引用）**（%d 字·程序抽取%s）：\n\n> %s%s' % (
            han(cut), '·句界截断' if trimmed else '', cut,
            '\n\n……（后文从略）' if trimmed else '')))

    # 去重：已在文中的块跳过（以块头 20 字查）
    real = []
    for dst, blk in adds:
        key = re.search(r'> (.{20})', blk)
        if key and key.group(1) in md:
            continue
        real.append((dst, blk))

    print('品%-3d 增补块: %d（5.1:%d 5.2:%d）· %s' % (
        pin, len(real), sum(1 for d, _ in real if d == '5.1'),
        sum(1 for d, _ in real if d == '5.2'), fp[-26:]))

    if APPLY and real:
        # 5.1 续引追加到 5.1 末尾（5.2 之前）
        a51 = [b for d, b in real if d == '5.1']
        if a51:
            i52 = md.find('### 5.2')
            md = md[:i52] + '\n\n' + '\n\n'.join(a51) + '\n\n' + md[i52:]
        # 5.2 新块追加到 5.2 末尾（下一 ###/## 之前）
        a52 = [b for d, b in real if d == '5.2']
        if a52:
            i52 = md.find('### 5.2')
            mnext = re.search(r'\n### |\n## ', md[i52:])
            end = i52 + (mnext.start() + 1 if mnext else len(md) - i52)
            md = md[:end] + '\n\n' + '\n\n'.join(a52) + '\n' + md[end:]
        io.open(fp, 'w', encoding='utf-8', newline='').write(md)

print('== 干跑 ==' if not APPLY else '== 已写入 ==')
