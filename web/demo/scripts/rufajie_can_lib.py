# -*- coding: utf-8 -*-
"""rufajie_can_lib.py — L.491 入法界品·五十三参子页（54 卡号系＋总目）

单一事实源：
  1. P39 主页 md 各参节（### 参N·名）——参题解/要点/阐释/对照启发/深释表/经文全引（人工核订内容·照录）
  2. 〈五十三参行历〉页内嵌 RUFAJIE_DATA（L.407/L.413/L.415 维护）——54 卡元数据＋三译师名
  3. data/research/huayan_80_40_deep_corpus.json（L.421）/huayan_60_40_deep_corpus.json（L.456）——参 2-51 四件套引文
本库运行时组装 doc_md（不产中间文件·随主页更新自动同步）；不编造内容：语料库未覆盖之参如实注明。
"""
import io
import json
import os
import re

CAN_GROUP = '入法界·五十三参'
P39_MD = 'docs/经学文献/华严经细读/第九会_逝多林_证入法界/华严经细读_第三十九部_入法界品.md'
JOURNEY_HTML = 'web/demo/articles/huayan-rufajie-journey.html'
CORPUS_8040 = 'data/research/huayan_80_40_deep_corpus.json'
CORPUS_6040 = 'data/research/huayan_60_40_deep_corpus.json'

_HEAD_RE = re.compile(r'^### 参(\d+)·([^\n]+)$', re.M)


def _read(path, root):
    with open(os.path.join(root, path), encoding='utf-8') as f:
        return f.read()


def _han(s):
    return len(re.findall(r'[\u3400-\u9fff]', s))


def _load_journey(root):
    """行历页内嵌 RUFAJIE_DATA + SPECIAL（54 卡·三译师名·span）。"""
    t = _read(JOURNEY_HTML, root)
    i = t.find('var RUFAJIE_DATA = ')
    if i < 0:
        raise RuntimeError('journey page: RUFAJIE_DATA not found')
    j = t.find('};', i)
    d = json.loads(t[i + len('var RUFAJIE_DATA = '):j + 1])
    cards = sorted(d['visits'], key=lambda v: v['card_no'])
    assert [v['card_no'] for v in cards] == list(range(1, len(cards) + 1)), 'card_no not 1..N'
    special = {}
    i2 = t.find('var SPECIAL = ')
    if i2 >= 0:
        j2 = t.find('};', i2)
        try:
            special = json.loads(t[i2 + len('var SPECIAL = '):j2 + 1])
        except Exception:
            special = {}
    return cards, special, d.get('meta', {})


def _load_md_sections(root):
    """P39 主页 54 参节：{no: {'head': 原标题行, 'name': 点后全名, 'body': 节体（去标题行）}}。"""
    md = _read(P39_MD, root)
    marks = [(m.start(), int(m.group(1)), m.group(2).rstrip()) for m in _HEAD_RE.finditer(md)]
    secs = {}
    for k, (pos, no, title) in enumerate(marks):
        end = marks[k + 1][0] if k + 1 < len(marks) else len(md)
        nxt = md.find('\n## ', pos + 1)
        if 0 < nxt < end:
            end = nxt
        chunk = md[pos:end]
        lines = chunk.split('\n')
        head_line = lines[0].lstrip('#').strip()
        body = '\n'.join(lines[1:]).strip()
        secs[no] = {'head': head_line, 'name': head_line.split('·', 1)[1] if '·' in head_line else head_line,
                    'body': body}
    return secs


def _load_corpora(root):
    out = {}
    for key, path in (('c8040', CORPUS_8040), ('c6040', CORPUS_6040)):
        try:
            d = json.loads(_read(path, root))
            out[key] = {int(r['no']): r for r in d.get('rows', []) if str(r.get('no', '')).lstrip('-').isdigit()}
        except Exception as e:
            print('  ! corpus %s: %s' % (path, e))
            out[key] = {}
    return out


def _short(s, n=260):
    s = (s or '').strip()
    return s if _han(s) <= n else s[:s.rfind('。', 0, n) + 1 if s.rfind('。', 0, n) > n // 2 else n] + '……'


def _corpus_table(rows, ver, ver_label):
    """四件套语料行 → md 表（行·件·原文，截断标注）。"""
    if not rows:
        return ''
    order = ['arrive', 'gate', 'point', 'leave']
    zh = {'arrive': '到会', 'gate': '法门自陈', 'point': '指授（→后参）', 'leave': '辞退'}
    lines = []
    for r in rows:
        t = r.get(ver) or {}
        for k in order:
            for q in (t.get(k) or [])[:2]:
                lines.append('| %s | %s |' % (zh[k], _short(q)))
    if not lines:
        return ''
    return ('| 件 | %s 原文（节引·逾 260 字句界截断） |\n|---|---|\n' % ver_label) + '\n'.join(lines)


def _can_no_label(card):
    cn = card.get('canon_no')
    if isinstance(cn, int):
        return '第%d参（经文层计数）' % cn
    return str(cn or '—')


def _assemble_card(root, card, sec, prev_card, next_card, corpora, special):
    n = card['card_no']
    n40, n80, n60 = card.get('n40', ''), card.get('n80', ''), card.get('n60', '')
    span = card.get('span') or [0, 0]
    cjk = card.get('cjk', 0)
    gate = card.get('gate', '—')
    role, city = card.get('role', '—'), card.get('city', '—')
    star = special.get(str(n), '')
    sec_id = 'huayan-rufajie-can-%02d' % n
    prev_id = ('huayan-rufajie-can-%02d' % (n - 1)) if prev_card else None
    next_id = ('huayan-rufajie-can-%02d' % (n + 1)) if next_card else None

    nav = ['📘 [子页总目](huayan-rufajie-can-index.html)', '🗺 [行历图](huayan-rufajie-journey.html)',
           '📄 [主页 §参%d](huayan-rufajie-pin.html)' % n]
    if prev_card:
        nav.insert(0, '← [参%d·%s](%s.html)' % (prev_card['card_no'], prev_card.get('n40', ''), prev_id))
    if next_card:
        nav.append('[参%d·%s →](%s.html)' % (next_card['card_no'], next_card.get('n40', ''), next_id))

    L = []
    L.append('# 参%d·%s —— 入法界品·五十三参子页' % (n, sec['name'] if sec else n40))
    L.append('')
    L.append('> **体例与来源**：底本四十华严 `T10n0293`（般若译·善财历参）；对读八十 `T10n0279`、六十 `T09n0278`（引文各照底本）。'
             '本页由程序汇编（L.491）：§一 照录自主页《华严经细读·第三十九部》§参%d 全文（参题解·要点·阐释·对照启发·三译深释表·经文全引——'
             '人工核订内容·原样保留，含其中〔本文判断〕〔待核〕标注）；§二 自四件套语料库（L.421/L.456）程序汇编；'
             '数据卡自行历图数据（L.407/L.413/L.415）。**阐释性文字之性质以原文标注为准；本页不新增判断。**' % n)
    L.append('')
    L.append('> ' + ' ｜ '.join(nav))
    L.append('')
    L.append('## 〇、本参数据卡（程序汇编·L.491）')
    L.append('')
    L.append('| 项 | 值 |')
    L.append('|---|---|')
    L.append('| 参号 | 第%d参（54 卡号系·L.327/L.407 重排）｜%s' % (n, _can_no_label(card)))
    L.append('| 善知识·四十 | **%s**（`T10n0293`）' % n40)
    L.append('| ·八十 | %s（`T10n0279`）' % n80)
    L.append('| ·六十 | %s（`T09n0278`）' % n60)
    if card.get('n_pan'):
        L.append('| 三译名判 | %s' % card['n_pan'])
    L.append('| 身份 | %s' % role)
    L.append('| 处所 | %s' % city)
    L.append('| 法门自陈（「我唯得/知此」） | %s' % gate)
    L.append('| 本参经文 | %s CJK（T0293 span %s–%s）' % ('{:,}'.format(cjk), '{:,}'.format(span[0]), '{:,}'.format(span[1])))
    if prev_card:
        L.append('| 前参 | 参%d·%s（法门：%s）' % (prev_card['card_no'], prev_card.get('n40', ''), prev_card.get('gate', '—')))
    if next_card:
        L.append('| 后参 | 参%d·%s（法门：%s）' % (next_card['card_no'], next_card.get('n40', ''), next_card.get('gate', '—')))
    if star:
        L.append('| 特殊标记 | ★ %s' % star)
    L.append('')
    L.append('## 一、主页参节全文（照录·零删改）')
    L.append('')
    if sec:
        L.append(sec['body'])
    else:
        L.append('〔主页 §参%d 节未定位——如实留空，待补。〕' % n)
    L.append('')

    # ── §二 三译四件套（语料库·参 2-51 覆盖）──
    r80 = corpora.get('c8040', {}).get(n)
    r60 = corpora.get('c6040', {}).get(n)
    L.append('## 二、三译四件套对读（语料库·程序汇编）')
    L.append('')
    if r80 or r60:
        L.append('> 语料库行口径：到会（到达·顶礼·请法）／法门自陈／指授（转介后参）／辞退。引文各照底本；'
                 '本表为程序抽取节引（句界截断），全文见各参经文。')
        L.append('')
        if r80:
            L.append('### 2.1 八十／四十（`T10n0279` ／ `T10n0293`）')
            L.append('')
            L.append(_corpus_table([r80], 't80', '八十') or '（该行无可用引文·如实留空）')
            L.append('')
        else:
            L.append('### 2.1 八十／四十')
            L.append('')
            L.append('（语料库未覆盖本参——序参/摄归参不属历参四件套口径；对读见主页 §6.4-6.7。）')
            L.append('')
        if r60:
            L.append('### 2.2 六十／四十（`T09n0278` ／ `T10n0293`）')
            L.append('')
            L.append(_corpus_table([r60], 't60', '六十') or '（该行无可用引文·如实留空）')
            L.append('')
        else:
            L.append('### 2.2 六十／四十')
            L.append('')
            L.append('（语料库未覆盖本参；见主页 §6.4-6.7。）')
            L.append('')
    else:
        L.append('（本参为%s，四件套语料库（参2-51 历参口径）未覆盖；三译对读见主页 §6.4-6.7 与 §五之B。）' %
                 ('序参（文殊指授）' if n == 1 else '摄归参' if n >= 52 else '非历参位'))
        L.append('')

    # ── §三 评注与延伸指针 ──
    L.append('## 三、评注与延伸指针（只指不代·不生成无据内容）')
    L.append('')
    L.append('- **古注诸家**：主页 §6.2 李通玄《新华严经论》窗、§五之B 计数诸说辨析；澄观《华严经疏》总纲见主页 §2.0′。')
    L.append('- **今人讲记**：海云继梦《华藏妙海》对读见主页 §6.2（〔OCR 待校〕）；九九华严讲记线见〈海云法师·九九华严讲记校勘工作台〉。')
    L.append('- **平行线**：藏译 Toh 44 对应章见主页「藏译对读窗」；〈五十三参行历〉交互图可按身份/篇幅回看全程。')
    if star:
        L.append('- **本参标记**：★%s（行历图八处特殊标记之一）。' % star)
    L.append('')
    L.append('## 四、台账')
    L.append('')
    L.append('- L.491（2026-11-16）：子页建立——程序汇编（主页 §参%d 照录＋行历数据卡＋四件套语料）；内容源批次 L.289–L.304（参批1-16）·'
             'L.316（参33 补卡）·L.407/L.413/L.415（行历·三译师名）·L.421/L.456（四件套语料库）。' % n)
    L.append('- 主页各参节后续修订后重跑 build 即自动同步本页 §一（运行时组装·无中间文件）。')
    return '\n'.join(L) + '\n'


def _assemble_index(root, cards, special, corpora):
    L = []
    L.append('# 五十三参子页·总目 —— 入法界品（54 卡号系）')
    L.append('')
    L.append('> **体例**：入法界品（第三十九品·第九会逝多林）善财历参逐参子页总目。底本四十华严 `T10n0293`；'
             '54 卡号系（L.327/L.407 重排：参33 普遍吉祥無垢光为勘出补卡·参5 彌伽补·参52-54 彌勒/文殊遥指/普賢摄归）。'
             '每参一页：数据卡＋主页参节全文照录＋三译四件套＋延伸指针。经文引文回源纪律同全站。')
    L.append('')
    L.append('🗺 [行历图（交互）](huayan-rufajie-journey.html) ｜ 📄 [主页·入法界品之拼读](huayan-rufajie-pin.html) ｜ '
             '★＝行历图八处特殊标记')
    L.append('')
    L.append('| 参 | 四十（`T10n0293`） | 八十 | 六十 | 身份 | 处所 | 法门自陈 | 篇幅 CJK | 子页 |')
    L.append('|---|---|---|---|---|---|---|---|---|')
    for c in cards:
        n = c['card_no']
        star = '★ ' if special.get(str(n)) else ''
        L.append('| %s%d | %s | %s | %s | %s | %s | %s | %s | [%s](huayan-rufajie-can-%02d.html) |' % (
            star, n, c.get('n40', ''), c.get('n80', ''), c.get('n60', ''), c.get('role', ''),
            c.get('city', ''), _short(c.get('gate', ''), 30), '{:,}'.format(c.get('cjk', 0)),
            '页↗', n))
    L.append('')
    L.append('## 读法')
    L.append('')
    L.append('- **行程读**：自参1 文殊指授起沿「前参指授→本参法门→转介后参」顺序读；每页导航行可前后跳。')
    L.append('- **对读读**：任一页 §二 四件套并观三译（到会/法门/指授/辞退），观「同一行迹·异译门名」。')
    L.append('- **专题读**：特殊参（★疑一·刀山／疑二·治罚／险门·离欲／四十二字母／彌勒楼阁／文殊遥指／十愿王）直取。')
    L.append('')
    L.append('## 台账')
    L.append('')
    L.append('- L.491（2026-11-16）：总目建立；54 卡自行历图数据（L.407/L.413/L.415），四件套语料 L.421/L.456（参2-51），主页参节 L.289-L.304/L.316。')
    return '\n'.join(L) + '\n'


def nav_items(articles):
    """pin_nav 抽屉「入法界·五十三参」组：总目＋54 卡。"""
    items = [{'id': 'huayan-rufajie-can-index', 'icon': '📘', 'no': 0, 'name': '子页总目'}]
    for a in articles:
        if a.get('family') == 'huayan_can' and a['id'] != 'huayan-rufajie-can-index':
            items.append({'id': a['id'], 'icon': a.get('icon', '🧭'), 'no': a.get('can_no'),
                          'name': a.get('can_name', '')})
    return items


def load_articles(root):
    """返回总目＋54 参子页 article dicts（doc_md 运行时组装）。"""
    cards, special, _meta = _load_journey(root)
    secs = _load_md_sections(root)
    corpora = _load_corpora(root)
    articles = []

    # 总目
    articles.append({
        'id': 'huayan-rufajie-can-index',
        'file': 'articles/huayan-rufajie-can-index.html',
        'title': '入法界品专题 · 五十三参子页·总目',
        'title_sub': '54 卡号系 · 每参一页深读（数据卡＋主页参节照录＋三译四件套＋延伸指针） · 程序汇编自主页与语料库',
        'icon': '📘', 'group': CAN_GROUP, 'family': 'huayan_can', 'order_in_group': 0,
        'version': 'v1.0', 'meta': '', 'doc': '', 'doc_label': '汇编自 华严经细读_第三十九部_入法界品.md',
        'updated_at': '2026-11-16',
        'back': {'tab': 'gap', 'view': 'avatamsaka-studies', 'label': '文献页 · 华严经学'},
        'views': ['avatamsaka-studies'],
        'doc_md': _assemble_index(root, cards, special, corpora),
    })

    for k, card in enumerate(cards):
        n = card['card_no']
        sec = secs.get(n)
        prev_card = cards[k - 1] if k > 0 else None
        next_card = cards[k + 1] if k + 1 < len(cards) else None
        n40 = card.get('n40', '参%d' % n)
        md_no = sec['head'].split('·')[0].replace('参', '') if sec else str(n)
        star = special.get(str(n), '')
        title_sub = '%s｜%s｜%s ｜ %s CJK · 主页参节全文照录＋三译四件套' % (
            card.get('role', ''), card.get('city', ''), _short(card.get('gate', ''), 42),
            '{:,}'.format(card.get('cjk', 0)))
        if star:
            title_sub = '★' + star + ' · ' + title_sub
        articles.append({
            'id': 'huayan-rufajie-can-%02d' % n,
            'file': 'articles/huayan-rufajie-can-%02d.html' % n,
            'title': '入法界品 · 参%d·%s' % (n, n40) + ('（★%s）' % star if star else ''),
            'title_sub': title_sub,
            'icon': '🧭', 'group': CAN_GROUP, 'family': 'huayan_can', 'order_in_group': n,
            'version': 'v1.0', 'meta': '', 'doc': '', 'doc_label': '汇编自 华严经细读_第三十九部_入法界品.md §参%s' % md_no,
            'updated_at': '2026-11-16',
            'back': {'tab': 'gap', 'view': 'avatamsaka-studies', 'label': '文献页 · 华严经学'},
            'views': ['avatamsaka-studies'],
            'can_no': n, 'can_name': n40,
            'doc_md': _assemble_card(root, card, sec, prev_card, next_card, corpora, special),
        })
    return articles
