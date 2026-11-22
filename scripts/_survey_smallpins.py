# -*- coding: utf-8 -*-
"""_survey_smallpins.py — 小品目（源短·文薄）材料盘点（只读·实测）
对每品测：①文章各层现状（五家窗 token·5.9/5.10·图·§四行数·三译/藏译·EN·九九）
         ②六源对品目的覆盖（T1732/T1733/T1735/T1736/T1739/B0002 品名锚）
         ③九九 episodes（ep01-18）品名提及
"""
import glob, io, re, sys, unicodedata

sys.stdout.reconfigure(encoding='utf-8')
D = {'一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9}


def cnum(s):
    if s == '十':
        return 10
    if '十' in s:
        a, _, b = s.partition('十')
        return (D.get(a, 1) if a else 1) * 10 + D.get(b, 0)
    return D[s]


PINS = {3: '普賢三昧品', 13: '升須彌山頂品', 14: '須彌頂上偈讚品', 16: '梵行品',
        19: '昇夜摩天宮品', 20: '夜摩宮中偈讚品', 24: '兜率宮中偈讚品',
        31: '壽量品', 32: '菩薩住處品'}

def cn_num(n):
    return {3:'三',13:'十三',14:'十四',16:'十六',19:'十九',20:'二十',24:'二十四',31:'三十一',32:'三十二'}[n]

# ── ① 文章层现状 ──
print('═══ ① 文章层现状 ═══')
for pin, name in PINS.items():
    g = glob.glob('docs/经学文献/华严经细读/**/华严经细读_第%s部_*.md' % cn_num(pin), recursive=True)
    md = io.open(g[0], encoding='utf-8').read()
    def has(p): return len(re.findall(p, md, re.M))
    h2s = [(i, l[3:].strip()) for i, l in enumerate(md.split('\n')) if l.startswith('## ')]
    w4 = None
    for k, (i, t) in enumerate(h2s):
        if re.match(r'^四[′、"]', t):
            nxt = h2s[k + 1][0] if k + 1 < len(h2s) else len(md)
            w4 = nxt - i
    print('P%-2d %s: han=%6d 图=%d §四=%s行 | 智俨%d 李论%d 道霈%d 演义钞%d 探玄%d 慧苑%d | 59=%d 510=%d 九九=%d | 三译=%d 藏=%d | 待核%d 未竟%d' % (
        pin, name, len(re.findall(r'[\u3400-\u9fff]', md)), md.count('<svg'),
        w4 if w4 else '-',
        has(r'搜玄|T1732'), has(r'李通玄|T1739'), has(r'道霈|纂要|B0002'),
        has(r'演義鈔|演义钞|T1736'), has(r'探玄記|探玄记|T1733'), has(r'慧苑|刊定記'),
        has(r'5\.9 新加坡'), has(r'5\.10 宣化'), has(r'九九華嚴|99华严|99華嚴|九九华严'),
        has(r'^### 6\.[^\n]*(六十|四十)'), has(r'6\.3 藏译|藏譯（Toh|藏译（Toh'),
        has(r'〔待核〕'), has(r'〔未竟')))

# ── ② 六源品名锚 ──
print('\n═══ ② 六源品名锚（出现次数·前3位） ═══')
SRC = {'智俨T1732': 'data/references/cbeta_txt/T1732_智俨_搜玄记.txt',
       '探玄T1733': 'data/references/cbeta_txt/T1733_法藏_探玄记.txt',
       '演义钞T1736': 'data/references/cbeta_txt/T1736_澄观_随疏演义钞.txt',
       '李论T1739': 'data/references/cbeta_txt/T1739_李通玄_新华严经论.txt',
       '纂要B0002': 'data/references/cbeta_txt/B0002_疏论纂要_epub提取本.txt'}
def norm(p):
    t = io.open(p, encoding='utf-8').read()
    return unicodedata.normalize('NFKC', re.sub(r'<<<PAGE \d+>>>', '', t))
texts = {k: norm(p) for k, p in SRC.items()}
alts = {
 3: ['普賢三昧品', '普賢三昧'],
 13: ['升須彌山頂品', '昇須彌山頂品', '須彌山頂品'],
 14: ['須彌頂上偈讚品', '須彌頂上偈贊品', '偈讚品'],
 16: ['梵行品'],
 19: ['昇夜摩天宮品', '升夜摩天宮品'],
 20: ['夜摩宮中偈讚品', '夜摩宮中偈贊品'],
 24: ['兜率宮中偈讚品', '兜率宮中偈贊品'],
 31: ['壽量品', '如來壽量品'],
 32: ['菩薩住處品', '住處品'],
}
for pin, name in PINS.items():
    row = []
    for k, t in texts.items():
        n = sum(len(re.findall(re.escape(v), t)) for v in alts[pin])
        p1 = min([t.find(v) for v in alts[pin] if t.find(v) >= 0] or [-1])
        row.append('%s=%d@%d' % (k.split('T')[-1].split('B')[-1], n, p1) if n else '%s=0' % k.split('T')[-1].split('B')[-1])
    print('P%-2d %s: %s' % (pin, name, ' '.join(row)))

# ── ③ 九九 episodes 品名提及 ──
print('\n═══ ③ 九九 episodes ep01-18 品名提及 ═══')
eps = sorted(glob.glob('docs/经学文献/海云讲记_九九华严/episodes/ep*.md'))
for pin, name in PINS.items():
    hits = []
    for ep in eps:
        t = unicodedata.normalize('NFKC', io.open(ep, encoding='utf-8').read())
        n = sum(len(re.findall(re.escape(v), t)) for v in alts[pin])
        if n:
            hits.append('%s×%d' % (ep.split('ep')[-1].split('.')[0], n))
    print('P%-2d: %s' % (pin, ' '.join(hits) or '无'))
