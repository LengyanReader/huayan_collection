# -*- coding: utf-8 -*-
"""enrich_xuanhua_thin.py — L.479：宣化浅释为薄章限量取件（P19/21/22/23/24·各 2 段）
来源：data/references/huayan_daodu/宣化淺釋/Ava_Vol*.txt（卷题已带品名）
限量：每章 2 段×~400 字（句界截断）；标「限量引用·来源 DRBA 在线文本」。
"""
import io, re, sys, glob
sys.stdout.reconfigure(encoding='utf-8')

APPLY = '--apply' in sys.argv
SRC = 'data/references/huayan_daodu/宣化淺釋/'

def han(s):
    return len(re.findall(r'[\u3400-\u9fff]', s))
HAN_RE = re.compile(r'[\u3400-\u9fff]')

def sc(text, limit):
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

def passages(fp, n=2, cap=400):
    """从宣化卷页取 n 段最有内容的讲解段（跳过经文引文行——宣化体例为「经文+浅释」交替）"""
    t = io.open(fp, encoding='utf-8').read()
    lines = t.split('\n')
    # 浅释段特征：含「宣化上人」讲解语气词或以（A）（B）分点；经文行较短且常带引号
    paras, cur = [], ''
    # 切掉每文件固定版头：到「願解如來真實義」止（开经偈末句）
    t_body = '\n'.join(lines)
    cut_at = t_body.find('願解如來真實義')
    if cut_at >= 0:
        t_body = t_body[cut_at + len('願解如來真實義'):]
    lines = t_body.split('\n')
    for ln in lines:
        ln = ln.strip()
        if not ln:
            if cur:
                paras.append(cur); cur = ''
            continue
        cur += ln
    if cur:
        paras.append(cur)
    # 跳过纯版头段（整段 < 200 字且含「講述/開經偈」特征——正文讲解段不受影响）
    paras = [p for p in paras
             if not (han(p) < 200 and ('講述' in p[:60] or '無上甚深微妙法' in p))]
    # 取含讲解性关键词的段
    scored = []
    for p in paras:
        score = 0
        for kw in ['什麼叫', '怎麼', '為什麼', '這個', '就是你', '我們', '修行', '菩薩', '因為']:
            if kw in p:
                score += p.count(kw)
        if han(p) >= 150:
            scored.append((score, p))
    scored.sort(key=lambda x: -x[0])
    out = []
    seen = set()
    for score, p in scored:
        key = p[:30]
        if key in seen:
            continue
        seen.add(key)
        cut, trimmed = sc(p, cap)
        out.append((cut, trimmed))
        if len(out) >= n:
            break
    return out

TARGETS = {
    '第十九部': ('昇夜摩天宮品第十九', 'P19 昇夜摩天宮品'),
    '第二十一部': ('十行品第二十一', 'P21 十行品'),
    '第二十二部': ('十無盡藏品第二十二', 'P22 十無盡藏品'),
    '第二十三部': ('昇兜率天宮品第二十三', 'P23 昇兜率天宮品'),
    '第二十四部': ('兜率宮中偈讚品第二十四', 'P24 兜率宮中偈讚品'),
}

for key, (volpat, label) in TARGETS.items():
    g = glob.glob('docs/经学文献/华严经细读/**/华严经细读_%s_*.md' % key, recursive=True)
    if not g:
        print(label, 'md 未定位'); continue
    fp = g[0]
    md = io.open(fp, encoding='utf-8').read()
    if '宣化上人《華嚴經淺釋》' in md:
        print(label, '已有·跳过'); continue
    vols = sorted(glob.glob(SRC + 'Ava_Vol*.txt'))
    hits = [v for v in vols if volpat[:4] in io.open(v, encoding='utf-8').read(200)]
    if not hits:
        print(label, '宣化卷页未定位（%s）' % volpat); continue
    blocks = []
    vi = 0
    for v in hits:
        for cut, tr in passages(v, n=1, cap=400):
            vi += 1
            lab = io.open(v, encoding='utf-8').read(120)
            m = re.search(r'卷题：([^\n]+)', lab)
            blocks.append('**宣化上人《華嚴經淺釋》·%s**（%d 字·限量引用·句界截断·来源：法界佛教总会在线文本）：\n\n> %s%s' % (
                (m.group(1) if m else volpat), han(cut), cut, '\n\n……（后文从略）' if tr else ''))
            if vi >= 2:
                break
        if vi >= 2:
            break
    if not blocks:
        print(label, '未取得合格段'); continue
    i52 = md.find('### 5.2')
    mnext = re.search(r'\n### |\n## ', md[i52:])
    end = i52 + (mnext.start() if mnext else len(md) - i52)
    md = md[:end] + '\n\n' + '\n\n'.join(blocks) + '\n' + md[end:]
    if APPLY:
        io.open(fp, 'w', encoding='utf-8', newline='').write(md)
    print('%s: %d 段 · %d 字 ✓' % (label, len(blocks), sum(han(b.split('> ')[1]) for b in blocks)))

print('== 干跑 ==' if not APPLY else '== 已写入 ==')
