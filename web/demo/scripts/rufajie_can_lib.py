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
GUZHU = 'data/research/rufajie_can_guzhu.json'
MIAOHAI = 'data/references/huayan_daodu/华藏妙海_整理版_提取本.txt'
T0293_TXT = 'data/references/cbeta_txt/T10n0293.txt'

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


# ── L.494 EN 对应（编者试译·门名与身份）──
_ROLE_EN = {'比丘': 'bhikṣu (monk)', '比丘尼': 'bhikṣuṇī (nun)', '菩薩': 'bodhisattva', '佛母': 'the Buddha\'s mother',
            '長者': 'elder (lay magnate)', '居士': 'householder', '優婆夷': 'upāsikā (laywoman)',
            '童女': 'maiden', '童子': 'youth', '釋女': 'Śākya maiden', '女': 'woman', '王': 'king',
            '婆羅門': 'brāhmaṇa', '仙人': 'ṛṣi (seer)', '外道': 'tīrthika (non-Buddhist ascetic)',
            '船師': 'shipmaster', '童子師': 'teacher of youths', '童子童女': 'youth & maiden',
            '夜神': 'night devī', '天神': 'deva', '地神': 'earth devī', '天女': 'devī', '林神': 'forest deva',
            '人': 'layman'}
_STAGE_EN = {1: 'Stage I — Aspiration & Instruction (Mañjuśrī\'s assembly)',
             52: 'Stage III — Maitreya\'s Tower (the Adamantine treasury of adornments)',
             53: 'Stage IV — Return & Consummation (Mañjuśrī\'s distant pointing)',
             54: 'Stage IV — Return & Consummation (Samantabhadra\'s Great Vows)'}
_STAGE_EN2 = 'Stage II — the Fifty Teachers (the pilgrimage through good counselors)'
_GATE_EN = {
    1: 'Instruction in seeking good teachers; the Sūtra "Universal Illumination of the Realm of Dharma"',
    2: 'The liberation of unobstructed wisdom, universally seeing the equal realm of mindful recollection of all Buddhas',
    3: 'The Dharma gateway of the Universal Eye',
    4: 'The liberation of universal, swift, heroic and unfailed offering to all Buddhas and ripening of beings',
    5: 'The Dharma gateway of wondrous-sound dhāraṇī radiance',
    6: 'The Tathāgata\'s profound and unobstructed adornment liberation',
    7: 'The samādhi of pure radiance of prajñā-pāramitā',
    8: 'A liberation gateway (name not given in the text)',
    9: 'The bodhisattva liberation of the Unsurpassed Banner',
    10: 'The bodhisattva liberation of the universally complete inexhaustible wheel',
    11: 'The gateway of prajñā-pāramitā universal adornment',
    12: 'The bodhisattva liberation of following along with inexhaustible lamps',
    13: 'The Dharma gateway of the wisdom-radiance of all arts and crafts and great powers',
    14: 'The bodhisattva liberation of the treasury of inexhaustible merit and adornment',
    15: 'The liberation of the treasury of merit arising at will',
    16: 'The bodhisattva liberation of unobstructed vows universally adorning the treasury of merit',
    17: 'The Dharma gateway of delight in universally seeing, serving and honoring the Buddhas with all beings',
    18: 'The Dharma gateway of illusion-like liberation and transformation',
    19: 'The bodhisattva samādhi of the Great Compassion Banner conduct in accord with the world',
    20: 'The bodhisattva liberation of the treasury of wisdom hard to crush',
    21: 'The prajñā-pāramitā of the universal gateway and the bounds of the Dharma realm',
    22: 'The Dharma of incense (discerning all fragrances; name not marked)',
    23: 'Purifying the bodhisattva conduct of the Great Compassion Banner',
    24: 'The Dharma gateway of adornment of pure bodhisattva conduct reaching everywhere',
    25: 'The liberation of extinguishing all subtle discrimination and accomplishing omniscient wisdom',
    26: 'The bodhisattva liberation of the realm of freedom from lust',
    27: 'The bodhisattva liberation of the realm of not passing into nirvāṇa (samādhi of the inexhaustible seed of Buddhas)',
    28: 'The bodhisattva liberation of swift conduct of great compassion',
    29: 'The bodhisattva liberation of the universal gateway of unshaken swift conduct',
    30: 'The bodhisattva liberation of the net of clouds',
    31: 'The liberation of the treasury of wisdom hard to crush',
    32: 'The liberation of light that teaches and tames, dispelling the darkness of delusion of all beings',
    33: 'The liberation of the heroic walking everywhere in the joy of tranquil samādhi',
    34: 'The stainless liberation of the banner of great swiftness and universal joy',
    35: 'The bodhisattva liberation of universally manifesting in all worlds to tame beings',
    36: 'The bodhisattva liberation of vast joy and adornment being born mind after mind',
    37: 'The liberation of profound freedom and lovely wondrous sound',
    38: 'The bodhisattva liberation of the light of vast joy newly arising',
    39: 'The bodhisattva liberation of universally transforming beings to give rise to good roots',
    40: 'The liberation of the psychic transformation of freely manifesting birth everywhere over immeasurable kalpas',
    41: 'Contemplation of all bodhisattva samādhis',
    42: 'The bodhisattva adornment liberation of great-vow wisdom and illusion',
    43: 'The bodhisattva liberation of unobstructed mindfulness and pure adornment',
    44: 'Pure referral (no self-declared gateway)',
    45: 'The liberation of complete mastery of all arts — the Forty-two Syllabaries',
    46: 'The liberation of the inexhaustible wheel of no abiding place',
    47: 'The liberation of unattached mindfulness and pure adornment',
    48: 'The bodhisattva liberation of the stainless light of wisdom',
    49: 'The liberation of inexhaustible characteristics',
    50: 'The liberation of the word of sincere vow',
    51: 'The liberation of illusion-like abiding',
    52: 'The gateway is the Tower itself — the adamantine treasury of adornments, surveying all',
    53: 'The distant pointing — referring all to Samantabhadra',
    54: 'The Ten Great Vows of Samantabhadra',
}
def _stage_of(n):
    if n == 1:
        return '壹·发心与指授（文殊会）'
    if n <= 51:
        return '贰·历参五十（善知识五十位）'
    if n == 52:
        return '叁·彌勒楼阁（一切庄严藏）'
    return '肆·摄归（文殊遥指·普賢愿王）'


_ROLE_ICON = {'比丘': '🧒', '比丘尼': '🪷', '菩薩': '🪷', '佛母': '🌸', '長者': '🏛', '居士': '🏺',
              '優婆夷': '🌿', '童女': '🌼', '童子': '🧒', '釋女': '🌼', '女': '🌼', '王': '👑',
              '婆羅門': '🔥', '仙人': '⛰', '外道': '🜂', '船師': '⛵', '童子師': '📜', '童子童女': '🧒',
              '夜神': '🌙', '天神': '🌌', '地神': '⛰', '天女': '🌙', '林神': '🌳'}


def _role_icon(role):
    return _ROLE_ICON.get(role, '🧭')


def quick_nav_html(root):
    """主页整合中枢（L.496·静态 HTML·JS 填充至 #can-quick-nav 占位）：
    速查网格＋按身份检索＋★特殊参直达＋EN 对应。"""
    cards, special, _m = _load_journey(root)
    chips = []
    chips.append('<a class="cqn-chip cqn-idx" href="huayan-rufajie-can-index.html" '
                 'style="background:rgba(201,162,39,.14);border-color:#c9a45c;color:#a3762a">📘 子页总目（五层检索）</a>')
    for c in cards:
        n = c['card_no']
        star = special.get(str(n))
        tip = '参%d·%s｜%s｜%s｜%s CJK%s' % (n, c.get('n40', ''), c.get('role', ''), c.get('city', ''),
                                            '{:,}'.format(c.get('cjk', 0)), ('｜★' + star) if star else '')
        chips.append(
            '<a class="cqn-chip" href="huayan-rufajie-can-%02d.html" title="%s">%s参%d·%s%s</a>'
            % (n, tip, _role_icon(c.get('role', '')), n, c.get('n40', ''), ('★' if star else '')))
    # 按身份检索（承总目 §二）
    roles = {}
    for c in cards:
        roles.setdefault(c.get('role', '—'), []).append(c['card_no'])
    id_rows = []
    for role, ns in sorted(roles.items(), key=lambda kv: -len(kv[1])):
        links = ' · '.join('<a href="huayan-rufajie-can-%02d.html">%d</a>' % (n, n) for n in ns)
        id_rows.append('<tr><td>%s%s</td><td>%d</td><td>%s</td></tr>' % (_role_icon(role), role, len(ns), links))
    id_table = ('<table style="width:100%;border-collapse:collapse;font-size:.78em">'
                '<tr><th style="text-align:left;padding:3px 6px">身份</th><th style="padding:3px 6px">参位</th>'
                '<th style="text-align:left;padding:3px 6px">参号（点入子页）</th></tr>'
                + ''.join(id_rows) + '</table>')
    stars = ' ｜ '.join('★%s＝<a href="huayan-rufajie-can-%02d.html">参%d·%s</a>' % (
        special[str(n)], n, n, next(c for c in cards if c['card_no'] == n).get('n40', ''))
        for n in sorted(int(k) for k in special))
    html = (
        '<details open>'
        '<summary style="cursor:pointer;font-weight:700;color:#7a5a28">🧭 速查网格（54 参子页·'
        '<span style="font-weight:400">点参名出子页；页内连续阅读用本页目录</span>）</summary>'
        '<div style="display:flex;flex-wrap:wrap;gap:6px;margin:8px 0 4px">' + ''.join(chips) + '</div>'
        '<div style="font-size:.74em;color:var(--text2,#7a7262);margin-top:2px">'
        '四阶段：壹 发心指授（参1）→ 贰 历参五十（参2-51）→ 叁 彌勒楼阁（52）→ 肆 摄归（53-54）。</div>'
        '</details>'
        '<details>'
        '<summary style="cursor:pointer;font-weight:600;color:#7a5a28">🔍 按身份检索（%d 类·承子页总目 §二）</summary>'
        '<div style="margin:6px 0">%s</div></details>'
        '<details open>'
        '<summary style="cursor:pointer;font-weight:600;color:#7a5a28">★ 特殊参直达（八标记）</summary>'
        '<div style="font-size:.82em;line-height:2;margin:6px 0">%s</div></details>'
        '<div class="en-line" style="font-size:.76em;color:var(--text2,#7a7262);margin-top:6px">'
        'EN · Hub of the fifty-four visit sub-pages: quick grid above (icons = role, ★ = special), '
        'identity retrieval, and the embedded pilgrimage map above. Gateway-name renderings are editorial trial translations 〔编者试译〕.</div>'
        % (len(id_rows), id_table, stars))
    return html


_T0293_CACHE = {'key': None, 'txt': ''}


def _skeleton(root, card, nseg=6):
    """L.500 参1/52-54 经文骨架：T0293 span 按句界均分 nseg 段·每段记 CJK 与首句（程序切分·非科判）。"""
    if _T0293_CACHE['key'] != root:
        _T0293_CACHE['key'] = root
        _T0293_CACHE['txt'] = _read(T0293_TXT, root)
    txt = _T0293_CACHE['txt']
    a, b = card.get('span') or [0, 0]
    seg = txt[a:b]
    sents = [s for s in re.split(r'(?<=[。！？」」])', seg) if s.strip()]
    if not sents:
        return None
    per = max(1, (len(sents) + nseg - 1) // nseg)
    rows = []
    for i in range(0, len(sents), per):
        chunk = sents[i:i + per]
        cjk = _han(''.join(chunk))
        head = chunk[0].strip()
        rows.append((i // per + 1, len(chunk), cjk, head))
    return rows


def _assemble_card(root, card, sec, prev_card, next_card, corpora, special, guzhu):
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
    L.append('> **古注取窗（L.493→L.527 五源）**：§三 收澄观《华严经疏》（`T1735`）·澄观《随疏演义钞》（`T1736`·末会多总谈·部分参为类聚引）·李通玄《新华严经论》（`T1739`）·法藏《探玄记》（`T1733`·残存）·道霈《華嚴經疏論纂要》（`B0002`·L.527 五源扩）逐参节引（程序取窗·单调锚定·句界截断·页码留痕）。程序抽取本字准待校，引前须对 CBETA 原书核。')
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
        # L.500 序参/摄归参补「经文骨架」：T0293 span 句界均分六段（程序切分·非科判）
        if n in (1, 52, 53, 54):
            rows = _skeleton(root, card)
            if rows:
                L.append('**经文骨架（L.500·T0293 span 程序切分·句界均分六段·非科判）**：')
                L.append('')
                for ri, nsent, cjk, head in rows:
                    L.append('- **段%d**（%d 句 · 约 %d CJK）：%s……' % (ri, nsent, cjk, head[:36]))
                L.append('')

    # ── §三 古注取窗（L.493→L.499·四源）──
    L.append('## 三、古注取窗（疏·钞·论·探玄记·程序取窗照录）')
    L.append('')
    gz = (guzhu or {}).get('cards', {}).get(str(card['card_no']), {})
    _src_label = {'shu': '澄观《华严经疏》`T1735`（八十·寄位释）',
                  'yan': '澄观《随疏演义钞》`T1736`（八十·钞于末会多总谈，部分参为类聚引）',
                  'lun': '李通玄《新华严经论》`T1739`（八十）',
                  'tan': '法藏《探玄记》`T1733`（六十·残存）',
                  'dao': '道霈《華嚴經疏論纂要》`B0002`（八十·疏论纂·初会多寄位总判·L.527 五源扩）'}
    for k in ('shu', 'yan', 'lun', 'tan', 'dao'):
        w = gz.get(k) or {}
        if w.get('miss') or not w.get('text'):
            L.append('**%s**：（未取窗——该疏论于此参无独立名锚或残存未及，如实留空。）' % _src_label[k])
            L.append('')
            continue
        _p2 = '·二遍扫（类聚引）' if w.get('pass2') else ''
        L.append('**%s**（锚「%s」·%s · %d 字·程序取窗%s·句界截断·引前须对原书核）：' % (
            _src_label[k], w.get('anchor', ''), w.get('page_ref', '') or '页码未录', w.get('cjk', 0), _p2))
        L.append('')
        L.append('> ' + w['text'])
        L.append('')

    # ── L.506 参2 专层：海云《华藏妙海》念佛法门四义＋德云与清凉对照 ──
    if n == 2:
        try:
            _mh = re.sub(r'\s+', '', _read(MIAOHAI, root))
            _mh = re.sub(r'【页\d+】\d*', '', _mh)
            a1 = _mh.find('此法门名称，可分为四')
            b1 = _mh.find('华严法门无量')
            a2 = _mh.find('德云与清凉，总将念佛门归入')
            b2 = _mh.find('三．具体的实相念佛')
            if 0 < a1 < b1 and 0 < a2 < b2:
                w1 = _mh[a1:b1]
                w2 = _mh[a2:b2]
                L.append('**海云继梦《華藏妙海》（華嚴玄談整理版）·念佛法門四義**（%d 字·整理版可引用·标来源 用户裁定 L.139.0）：' % _han(w1))
                L.append('')
                L.append('> ' + w1)
                L.append('')
                L.append('**海云继梦《華藏妙海》·能念心与所念境——德云与清凉对照**（%d 字·同上）：' % _han(w2))
                L.append('')
                L.append('> ' + w2)
                L.append('')
        except Exception as e:
            print('  ! miaohai card2:', e)

    # ── §四 评注与延伸指针 ──
    L.append('## 四、评注与延伸指针（只指不代·不生成无据内容）')
    L.append('')
    L.append('- **古注诸家**：本参取窗见 §三；更完整释文见主页 §6.2 李通玄《新华严经论》窗、§五之B 计数诸说辨析；澄观《华严经疏》总纲见主页 §2.0′。')
    L.append('- **今人讲记**：海云继梦《华藏妙海》对读见主页 §6.2（〔OCR 待校〕）；九九华严讲记线见〈海云法师·九九华严讲记校勘工作台〉。')
    L.append('- **平行线**：藏译 Toh 44 对应章见主页「藏译对读窗」；〈五十三参行历〉交互图可按身份/篇幅回看全程。')
    if star:
        L.append('- **本参标记**：★%s（行历图八处特殊标记之一）。' % star)
    L.append('')
    L.append('> <span class="en-line">**EN corresponding · Visit %d — %s (%s).** A %s at %s; self-declared gateway: "%s" 〔编者试译〕. '
             '%s. Three-translation parallels: 40-fascicle `T10n0293` (base), 80 `T10n0279`, 60 `T09n0278` — see §二; '
             'classical commentary windows: Chengguan\'s *Huayan jing shu* `T1735` and Li Tongxuan\'s *Xin Huayan jing lun* `T1739` — see §三.</span>'
             % (n, card.get('n40', ''), _ROLE_EN.get(card.get('role', ''), 'teacher'),
                _ROLE_EN.get(card.get('role', ''), 'teacher'), card.get('city', ''),
                _GATE_EN.get(n, card.get('gate', '')),
                _STAGE_EN.get(n, _STAGE_EN2)))
    L.append('')
    L.append('## 五、台账')
    L.append('')
    L.append('- L.493（2026-11-17）：古注取窗入 §三（疏/论 54/54 全覆盖·探玄记入法界品疏残存仅 13/54·未及者如实留空）；程序取窗·NFKC 归一·单调锚定·字准待校。')
    L.append('- L.499（2026-11-17）：第四源《随疏演义钞》`T1736` 入 §三（40/54·钞于末会多总谈，部分窗为类聚引·已于源标签注明）。')
    if n == 2:
        L.append('- L.506（2026-11-18）：《华藏妙海》念佛法門四義＋德云与清凉对照入 §三（玄談整理版·海云对参2法门之专论）。')
    L.append('- L.507（2026-11-18）：二遍扫恢复——钞 52/54→**54/54**·探玄记 13→**46/54**（pass2 类聚引已标）；仍 miss 8 处为探玄记未及之参（5/15/16/22/26/33/35/49·残存上限）。')
    L.append('- L.491（2026-11-16）：子页建立——程序汇编（主页 §参%d 照录＋行历数据卡＋四件套语料）；内容源批次 L.289–L.304（参批1-16）·'
             'L.316（参33 补卡）·L.407/L.413/L.415（行历·三译师名）·L.421/L.456（四件套语料库）。' % n)
    L.append('- 主页各参节后续修订后重跑 build 即自动同步本页 §一（运行时组装·无中间文件）。')
    return '\n'.join(L) + '\n'


def _structure_observations(cards, special):
    """L.501 结构观察：身份×阶段·门名自陈·篇幅分布·三译名判（全部程序实测·附口径）。"""
    import statistics
    n40s = [c.get('n40', '') for c in cards]
    cjk = sorted(c.get('cjk', 0) for c in cards)
    roles = {}
    for c in cards:
        roles.setdefault(c.get('role', '—'), []).append(c['card_no'])
    pan = {}
    for c in cards:
        p = c.get('n_pan') or '—'
        pan[p] = pan.get(p, 0) + 1
    gate_named = sum(1 for c in cards if c.get('gate') and '未' not in c.get('gate', '') and '无自陈' not in c.get('gate', '') and '指授' not in c.get('gate', ''))
    top5 = sorted(cards, key=lambda c: -c.get('cjk', 0))[:5]
    low5 = sorted(cards, key=lambda c: c.get('cjk', 0))[:5]
    L = []
    L.append('- **身份分布**：' + ' · '.join('%s %d' % (r, len(ns)) for r, ns in sorted(roles.items(), key=lambda kv: -len(kv[1]))))
    L.append('- **法门自陈**：%d/54 参有「我唯得/知此」句式（序参指授·参44 纯转介·参52-54 摄归无此句式）；' % gate_named +
             '篇幅中位数 %d CJK · 最长五参 ' % int(statistics.median(cjk)) +
             ' / '.join('参%d·%s（%s）' % (c['card_no'], c.get('n40', ''), '{:,}'.format(c.get('cjk', 0))) for c in top5) +
             '；最短五参 ' + ' / '.join('参%d（%s）' % (c['card_no'], '{:,}'.format(c.get('cjk', 0))) for c in low5) + '。')
    L.append('- **三译名判**（行历 L.409/413 口径）：' + ' · '.join('%s %d' % (k, v) for k, v in sorted(pan.items(), key=lambda kv: -kv[1])) +
             '——师名分歧率高于门名（法门名三译义近为主）。')
    L.append('- **特殊参八标记**（★）：' + ' · '.join('参%s %s' % (k, special[k]) for k in sorted(special, key=int)) + '。')
    return '\n'.join(L)


def _assemble_index(root, cards, special, corpora):
    L = []
    L.append('# 五十三参子页·总目 —— 入法界品（54 卡号系）')
    L.append('')
    L.append('> **体例**：入法界品（第三十九品·第九会逝多林）善财历参逐参子页总目。底本四十华严 `T10n0293`；'
             '54 卡号系（L.327/L.407 重排：参33 普遍吉祥無垢光为勘出补卡·参5 彌伽补·参52-54 彌勒/文殊遥指/普賢摄归）。'
             '每参一页：数据卡＋主页参节全文照录＋三译四件套＋延伸指针。经文引文回源纪律同全站。')
    L.append('')
    L.append('<div class="en-line">EN · Index of the fifty-four sub-pages for the Gaṇḍavyūha chapter: each visit gets its own page — '
             'data card (teacher in three translations, role, locale, self-declared gateway, span), the main-page section reproduced verbatim, '
             'three-translation four-element parallels (arrival / gateway / referral / departure), classical commentary windows '
             '(Chengguan\'s *Shu* `T1735` & Li Tongxuan\'s *Lun* `T1739`), and pointers. Gateway-name English renderings are editorial trial translations 〔编者试译〕.</div>')
    L.append('')
    L.append('🗺 [行历图（交互）](huayan-rufajie-journey.html) ｜ 📄 [主页·入法界品之拼读](huayan-rufajie-pin.html) ｜ '
             '★＝行历图八处特殊标记')
    L.append('')
    # ── 按行程阶段分组的主表 ──
    L.append('## 一、行程总目（四阶段）')
    L.append('')
    stage_of = _stage_of
    cur_stage = None
    for c in cards:
        n = c['card_no']
        st = stage_of(n)
        if st != cur_stage:
            cur_stage = st
            L.append('')
            L.append('### %s' % st)
            L.append('')
            L.append('| 参 | 四十（`T10n0293`） | 八十 | 六十 | 身份 | 处所 | 法门自陈 | 篇幅 CJK | 子页 |')
            L.append('|---|---|---|---|---|---|---|---|---|')
        star = '★ ' if special.get(str(n)) else ''
        L.append('| %s%d | %s | %s | %s | %s | %s | %s | %s | [%s](huayan-rufajie-can-%02d.html) |' % (
            star, n, c.get('n40', ''), c.get('n80', ''), c.get('n60', ''), c.get('role', ''),
            c.get('city', ''), _short(c.get('gate', ''), 30), '{:,}'.format(c.get('cjk', 0)),
            '页↗', n))
    L.append('')
    # ── 按身份检索 ──
    L.append('## 二、按身份检索')
    L.append('')
    roles = {}
    for c in cards:
        roles.setdefault(c.get('role', '—'), []).append(c['card_no'])
    role_rows = sorted(roles.items(), key=lambda kv: -len(kv[1]))
    L.append('| 身份 | 参位数 | 参号（点入子页） |')
    L.append('|---|---|---|')
    for role, ns in role_rows:
        links = ' · '.join('[%d](huayan-rufajie-can-%02d.html)' % (n, n) for n in ns)
        L.append('| %s%s | %d | %s |' % (_role_icon(role), role, len(ns), links))
    L.append('')
    # ── 特殊参直达 ──
    L.append('## 三、特殊参直达（★·行历图八标记）')
    L.append('')
    L.append(' ｜ '.join('★%s＝[参%d·%s](huayan-rufajie-can-%02d.html)' % (
        special[str(n)], n, next(c for c in cards if c['card_no'] == n).get('n40', ''), n)
        for n in sorted(int(k) for k in special)))
    L.append('')
    L.append('## 四、读法')
    L.append('')
    L.append('- **行程读**：自参1 文殊指授起沿「前参指授→本参法门→转介后参」顺序读；每页导航行可前后跳。')
    L.append('- **对读读**：任一页 §二 四件套并观三译（到会/法门/指授/辞退），观「同一行迹·异译门名」。')
    L.append('- **专题读**：特殊参（★疑一·刀山／疑二·治罚／险门·离欲／四十二字母／彌勒楼阁／文殊遥指／十愿王）直取。')
    L.append('- **身份读**：§二 按身份检索——比丘沙门系／在家众系／天神夜神系／佛母圣众系，各成一条参学侧线。')
    L.append('')
    L.append('## 五、结构与判读（L.501·程序实测）')
    L.append('')
    L.append(_structure_observations(cards, special))
    L.append('')
    L.append('## 六、台账')
    L.append('')
    L.append('- L.491（2026-11-16）：总目建立；54 卡自行历图数据（L.407/L.413/L.415），四件套语料 L.421/L.456（参2-51），主页参节 L.289-L.304/L.316。')
    L.append('- L.492（2026-11-17）：总目重构——行程四阶段分组·按身份检索·特殊参直达三检索层（利于查阅）。')
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
    try:
        guzhu = json.loads(_read(GUZHU, root))
    except Exception as e:
        print('  ! guzhu load:', e)
        guzhu = {'cards': {}}
    articles = []

    # 总目
    articles.append({
        'id': 'huayan-rufajie-can-index',
        'file': 'articles/huayan-rufajie-can-index.html',
        'title': '入法界品专题 · 五十三参子页·总目',
        'title_sub': '54 卡号系 · 每参一页六层深读（数据卡/主页照录/三译四件套/古注取窗/EN/指针台账） · 程序汇编',
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
        title_sub = '%s｜%s｜%s ｜ %s CJK · 六层：数据卡/主页照录/三译四件套/古注取窗疏论/EN/指针' % (
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
            'doc_md': _assemble_card(root, card, sec, prev_card, next_card, corpora, special, guzhu),
        })
    return articles
