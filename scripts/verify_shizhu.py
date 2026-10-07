#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verify_shizhu.py —— 《世主妙严品》专书常设门禁（L107 立）

背景：本轮全量校勘（L106–L107）所依赖的核验，此前皆为一次性 scratch 脚本
（_audit_jingwen.py / _roll_verify.py / hyq*.py），不常设、不可重跑、结论无法被
后续批次复现。本脚本把其中**可自动化的部分**固化为五道断言：

  A 实测口径  —— 字/句/门/组数须与 miaoyan_metrics.py 同源实测一致（防旧数回潮）
  B 旧数扫描  —— 扫「已作废的旧统计数」，命中即失败，但**须豁免校勘记段**
                  （校勘记本就应记录旧误，扫到它属门禁自身缺陷，非文之过）
  C 引文回源  —— 分作用域逐条比对：作用域①六十本对读/诸家强调块；作用域②标「逐字
                  照录」之行。二者皆以「任一可信源命中」为通过（因同一行可能并引
                  经文＋注疏＋海云，不可强求单一来源）
  D 海云专段  —— 另统计海云讲记命中率并要求「海云归属＋逐字照录」之引文必有据
  E 溯源自洽  —— 所声明的来源文件须真实存在，且不得保留已证伪之来源系

退出码 0 = 全绿；非 0 = 有断言失败。须以 PYTHONIOENCODING=utf-8 运行。

**方法论要点（勿删）**：CBETA txt 用**康熙部首/中日韩部首兼容字**（⽣ U+2F65、
⼤ U+2F27、⾨ U+2F28…），且 NFKC **不覆盖** U+2E80–U+2EF3 区。故凡回源比对
必须 NFKC + RAD 双层归一；此前多轮「查无原文」的伪报，皆源于漏此归一，非文献有误。
反之，若门禁本身出现假阳性，**当先修门禁，不得迁就文档**（L107 已因此重写本段）。
"""
import io
import os
import re
import sys
import unicodedata

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE = r'C:\DA_Practice\huayan_collection'
# 文档路径可由环境变量覆盖（供反向验证在副本上作破坏性变异；勿用于日常运行）
DOC = os.environ.get('SHIZHU_DOC') or os.path.join(
    BASE, r'docs\经学文献\华严经细读_第一部_世主妙严品.md')

# ── 归一层：NFKC 不收 U+2E80–U+2EF3（康熙/中日韩部首补充块），须 RAD 兜底 ──
RAD = {
    '⻆': '日', '⻇': '月', '⻑': '長', '⻕': '門', '⻚': '頁', '⻛': '風', '⻜': '飛',
    '⻣': '食', '⻮': '魚', '⻯': '鳥', '⻰': '龍', '⻢': '馬', '⻤': '鬼', '⻥': '魚',
    '⻦': '鳥', '⻧': '鹵', '⻨': '鹿', '⻩': '黃', '⻬': '齊', '⻭': '齒',
    '⻮': '齒', '⻯': '龍', '⻰': '龍', '⻱': '龜', '⻲': '龜',
    '丨': '丨', '⺀': '一', '⺁': '丨', '⺉': '乙', '⺊': '卜', '⺌': '小',
    '⺍': '小', '⺏': '尢', '⺑': '尸', '⺒': '貝', '⺓': '爿', '⺔': '气',
    '⺕': '网', '⺖': '心', '⺗': '心', '⺘': '手', '⺙': '攴', '⺚': '无',
    '⺛': '无', '⺜': '見', '⺝': '角', '⺞': '言', '⺟': '示', '⺠': '民',
    '⺡': '水', '⺢': '貝', '⺣': '言', '⺤': '食', '⺥': '飠', '⺦': '食',
    '⺧': '食', '⺨': '犬', '⺩': '玉', '⺪': '瓦', '⺫': '甘', '⺬': '生',
    '⺭': '用', '⺮': '竹', '⺯': '糸', '⺰': '糸', '⺱': '网', '⺲': '网',
    '⺳': '网', '⺴': '网', '⺵': '网', '⺶': '网', '⺷': '网', '⺸': '网',
    '⺹': '网', '⺺': '网', '⺼': '肉', '⻂': '邑', '⻃': '酉', '⻄': '西',
    '⻅': '見', '⻈': '角', '⻉': '貝', '⻊': '足', '⻋': '車', '⻌': '辵',
    '⻍': '辵', '⻎': '辵', '⻏': '邑', '⻐': '金', '⻑': '長', '⻒': '镸',
    '⻓': '長', '⻔': '門', '⻖': '阜', '⻗': '雨', '⻘': '青', '⻙': '韋',
    '⻚': '頁', '⻛': '風', '⻜': '飛', '⻝': '食', '⻞': '飠', '⻟': '飠',
    '⻠': '飠', '⻢': '馬', '⻣': '髟', '⻤': '鬼', '⻥': '魚', '⻦': '鳥',
    '⻧': '鹵', '⻨': '鹿', '⻩': '黃', '⻪': '黍', '⻫': '黑', '⻬': '齊',
    '⻭': '齒', '⻮': '齒', '⻯': '龍', '⻰': '龍', '⻱': '龜', '⻲': '龜',
}


def norm(s: str) -> str:
    """NFKC + 康熙部首 RAD 双层归一（缺此则误报，勿简化）"""
    s = unicodedata.normalize('NFKC', s)
    return ''.join(RAD.get(ch, ch) for ch in s)


def cjk(s: str) -> str:
    return ''.join(ch for ch in norm(s) if '\u3400' <= ch <= '\u9fff')


PUNCT = re.compile(
    r'[，。、；：？！（）()「」『』《》〈〉〔〕【】…—－·,.;:?!\'"“”‘’\[\]{}<>｜|]')


def squash(s: str) -> str:
    """归一 + 去空白 + 去标点 + 去 markdown 强调，用于引文逐字比对"""
    s = norm(s).replace('**', '').replace('……', '').replace('…', '')
    s = PUNCT.sub('', s)
    return re.sub(r'[\s　]', '', s)


# ── 语料 ──────────────────────────────────────────────────────────────────
def read(path: str) -> str:
    with open(path, encoding='utf-8', errors='replace') as f:
        return f.read()


doc = read(DOC)
lines = doc.split('\n')

# 文档头部（题名／英文题名／完备度声明）到首个独立 `---` 之间为前言区：
# 其中的「」是版块名等标签（如「逐组细读」「六十本对读」），非引文，故豁免回源。
_sep = next((i for i, l in enumerate(lines) if l.strip() == '---'), 0)
BODY = _sep + 1          # 正文起始行号（0-based）

CB = os.path.join(BASE, r'data\references\cbeta_txt')
YD = os.path.join(BASE, r'docs\huayanhai\义学专题\经论原典')
HY = os.path.join(BASE, r'docs\huayanhai\华严云海\浩瀚华严海\八十华严之01品世主妙严品')

fails: list = []
notes: list = []


def check(cond, tag, msg):
    if cond:
        print('  [OK]   %s %s' % (tag, msg))
    else:
        print('  [FAIL] %s %s' % (tag, msg))
        fails.append('%s %s' % (tag, msg))


print('=' * 74)
print('verify_shizhu.py —— 《世主妙严品》专书门禁（L107）')
print('=' * 74)

# ── 校勘记段识别（豁免旧数扫描用；须先于 A 段定义）────────────────────
PROOF = ('〔校', '已校', '校勘', '订正', '正之', '误', '舊', '旧稿', '回源撤',
         '撤回', '更正', '不确', '不確', '口径辨析', '勿混')


def is_proof(ln: str) -> bool:
    """校勘记/凡例/自述段：其中记录旧误属合法，不得按「旧数残留」判失败"""
    return any(k in ln for k in PROOF)


# ── A 实测口径 ────────────────────────────────────────────────────────────
print('\n【A】实测口径（须与 miaoyan_metrics.py 同源，防旧数回潮）')
sys.path.insert(0, os.path.join(BASE, 'scripts'))
try:
    import miaoyan_metrics as MM
    st = MM.stats()
    pin = st['pin']
    notes.append('实测 卷一–五 %d 字 / %d 句（逐卷 %s）'
                 % (st['pin_cjk'], st['pin_sent'],
                    '/'.join(str(st['per_juan'][str(n)]['cjk']) for n in range(1, 6))))
    check(st['pin_cjk'] == 31953 and st['pin_sent'] == 700, 'A1',
          '卷一–五 字句 = %d / %d（应 31953 / 700）' % (st['pin_cjk'], st['pin_sent']))
    groups = (pin['承佛威力'] + pin['承佛威神'] + pin['承佛神力'] + pin['復承如來威神之力'])
    utter = pin['而說頌言'] + pin['即說頌言'] + pin['而說頌曰']
    check(groups == 52 and utter == 52, 'A2',
          '导语式 52 / 说颂式 52（实 %d / %d）' % (groups, utter))
    check(pin['解脫門'] == 442, 'A3', '本品解脫門 442（实 %d）' % pin['解脫門'])
    check(st['quan']['解脫門'] == 551, 'A4', '全经解脫門 551（实 %d）' % st['quan']['解脫門'])
    check(pin['爾時'] == 56 and pin['如是等而為上首'] == 41, 'A5',
          '本品 爾時 56 / 如是等而為上首 41（实 %d / %d）' % (pin['爾時'], pin['如是等而為上首']))
    check(pin['而說頌曰'] == 1, 'A6', '本品「而說頌曰」1（卷二月天子，实 %d）' % pin['而說頌曰'])
    # 正文自述数须与实测一致，且**须与单位绑定**（只验「存在」会被同句他处之旧数蒙过，
    # 此为 L107 反向验证实测之盲区，故此处以「数字＋字/句」为判据）
    claim = '{:,}'.format(st['pin_cjk'])
    check(re.search(re.escape(claim) + r'\s*字', doc) is not None, 'A7',
          '正文自述字数与单位绑定（%s 字）' % claim)
    check(re.search(r'700\s*句', doc) is not None, 'A8', '正文自述句数与单位绑定（700 句）')
    check('{:,}'.format(32018) in doc, 'A9', '正文载 T279 同段对照数 32,018')
    # 旧数扫描：正文不得复称旧数为「本品字数」；但若该数出现于**近旁有口径辨析者**
    # （如 72,180 之于数据科学层之另一口径），则属已辨明之并存实测，正当保留
    for stale in ('72,180', '1,821'):
        bad = []
        for i, l in enumerate(lines, 1):
            if stale not in l or is_proof(l):
                continue
            near = ''.join(lines[max(0, i - 7):i + 6])
            if '口径辨析' in near or '勿混' in near:
                continue
            bad.append(i)
        check(not bad, 'A10', '正文无未辨明之旧数「%s」%s'
              % (stale, ('  ← 命中行 ' + str(bad[:6])) if bad else ''))
except Exception as e:                      # 口径不可测即失败，不得静默跳过
    check(False, 'A0', 'miaoyan_metrics 导入失败：%r' % (e,))

# ── 旧数扫描 ────────────────────────────────────────────────────────────
print('\n【B】旧数/失效结论扫描（防回退；豁免校勘记段）')
BANNED = [
    ('四十二类', '本品为 40 类，非 42'),
    ('四十二位', '本品为 40 类，非 42'),
    ('欲界六组', '卷二欲界为七组，非六组'),
    ('卷二十二组', '卷次误引，正为「卷二·十二组」'),
]
for bad, why in BANNED:
    hits = [i for i, l in enumerate(lines, 1) if bad in l and not is_proof(l)]
    check(not hits, 'B:' + bad, '正文（除校勘记）无「%s」——%s%s'
          % (bad, why, ('  ← 命中行 ' + str(hits[:6])) if hits else ''))
# 「引文逐字照录」不得作为被引内容出现在引号内（此前 L921/L2506 之误即此）
quoted_marker = [i for i, l in enumerate(lines, 1)
                 if re.search(r'「[^」]*(引文逐字照录|逐字照录|逐字引录)[^」]*」', l)]
check(not quoted_marker, 'B5', '「逐字照录」未被当作引文内容（命中行 %s）' % (quoted_marker[:6] or '无'))
check('四十类' in doc, 'B6', '正述 40 类')
check(re.search(r'414\s*名', doc) is not None, 'B7', '正述 414 名（数字与单位绑定）')

# ── C 引文回源（分作用域）────────────────────────────────────────────────
print('\n【C】引文回源（作用域：①六十本对读/诸家强调 ②标「逐字照录」之行）')
SRC = {}
SRC['T279'] = cjk(re.sub(r'<[^>]+>', '', read(os.path.join(BASE, r'data\references\cbeta\T10n0279.xml'))))
for key, fn in (('简本', '八十华严-简-大华严寺袖珍版_1.txt'),
                ('繁本', '八十华严-繁-大华严寺袖珍版_1.txt'),
                ('六十', '六十华严_1.txt')):
    p = os.path.join(YD, fn)
    if os.path.exists(p):
        SRC[key] = cjk(read(p))
for fn in sorted(os.listdir(CB)):
    if fn.endswith('.txt'):
        SRC[fn.split('_')[0]] = cjk(read(os.path.join(CB, fn)))
HY_FILES = [f for f in sorted(os.listdir(HY)) if f.endswith('.txt')] if os.path.isdir(HY) else []
for f in HY_FILES:
    SRC['HY:' + f[:6]] = cjk(read(os.path.join(HY, f)))
notes.append('可信源 %d 份（含海云讲记 %d 卷）' % (len(SRC), len(HY_FILES)))

MARK = '逐字照录'
SCOPE1_HEAD = ('**六十本对读**', '**诸家强调')
sc1 = sc1_miss = sc2 = sc2_miss = 0
sc1_bad, sc2_bad = [], []
active = False
for i, ln in enumerate(lines, 1):
    if i <= BODY:
        continue
    if ln.startswith(SCOPE1_HEAD):
        active = True
    elif ln.strip() and not ln.startswith('- '):
        active = False
    quotes = [q for q in re.findall(r'「([^」]+)」', ln)]
    in_s1 = active
    in_s2 = (MARK in ln) or ('引文逐字照录' in ln)
    if not (in_s1 or in_s2) or is_proof(ln):
        continue
    for q in quotes:
        if q.strip() in (MARK, '引文逐字照录', '逐字引录'):
            continue
        for part in re.split(r'……|…|／|、|（', q):
            p = cjk(part)
            if len(p) < 4:
                continue
            hit = any(p in v for v in SRC.values())
            if in_s1:
                sc1 += 1
                if not hit:
                    sc1_miss += 1
                    sc1_bad.append('L%d %s' % (i, part[:40]))
            elif in_s2:
                sc2 += 1
                if not hit:
                    sc2_miss += 1
                    sc2_bad.append('L%d %s' % (i, part[:40]))
check(sc1_miss == 0, 'C1', '作用域① 引文回源 %d 条全中（miss=%d）%s'
      % (sc1, sc1_miss, ('  ← ' + str(sc1_bad[:5])) if sc1_bad else ''))
check(sc2_miss == 0, 'C2', '作用域② 引文回源 %d 条全中（miss=%d）%s'
      % (sc2, sc2_miss, ('  ← ' + str(sc2_bad[:5])) if sc2_bad else ''))

# ── D 海云专段 ────────────────────────────────────────────────────────────
print('\n【D】海云讲记归属核验（五卷独立文件为唯一来源）')
check(len(HY_FILES) == 5, 'D0', '海云讲记五卷独立文件齐备（实 %d）' % len(HY_FILES))
hai = squash(''.join(read(os.path.join(HY, f)) for f in HY_FILES))
HY_TAG = ('海云继梦', '海云法师', '海云讲记', '海云继梦法师')
d_chk = d_hai = d_other = 0
d_bad = []
for i, ln in enumerate(lines, 1):
    if i <= BODY or not any(t in ln for t in HY_TAG) or MARK not in ln or is_proof(ln):
        continue
    for q in re.findall(r'「([^」]+)」', ln):
        if q.strip() in (MARK, '引文逐字照录', '逐字引录'):
            continue
        qq = squash(q)
        if len(qq) < 4:
            continue
        d_chk += 1
        if qq in hai:
            d_hai += 1
        elif any(qq in v for v in SRC.values()):
            d_other += 1                     # 同行并引经文/注疏，非伪引
        else:
            d_bad.append('L%d %s' % (i, q[:50]))
check(not d_bad, 'D1', '海云归属＋逐字照录 之引文 %d 条皆有据'
      '（海云 %d ／ 同行他源 %d ／ 无据 %d）%s'
      % (d_chk, d_hai, d_other, len(d_bad), ('  ← ' + str(d_bad[:5])) if d_bad else ''))
check('讲记引用皆依袖珍版' not in doc, 'D2', '已撤回「海云讲记引自袖珍版」之误系（M4X3 更正）')
check('独立文件' in doc, 'D3', '已正述海云讲记真实来源（五卷独立文件）')

# ── E 溯源自洽 ────────────────────────────────────────────────────────────
print('\n【E】来源声明自洽（防假出处）')
paths = set(re.findall(r'\]\(\.\./\.\./\.\./(docs/[^)]+)\)', doc))
paths |= set(re.findall(r'`(docs/[^`]+\.txt)`', doc))
bad_paths = [p for p in paths if not os.path.exists(os.path.join(BASE, p.replace('/', os.sep)))]
check(not bad_paths, 'E1', '文中所引 %d 个本地路径皆存在%s'
      % (len(paths), ('  ← 缺失 ' + str(bad_paths)) if bad_paths else ''))

# ── 汇总 ──────────────────────────────────────────────────────────────────
print('\n' + '=' * 74)
for n in notes:
    print('  · %s' % n)
print('=' * 74)
if fails:
    print('FAILED %d 项：' % len(fails))
    for f in fails:
        print('  - %s' % f)
    sys.exit(1)
print('ALL CHECKS PASSED —— 《世主妙严品》门禁全绿')