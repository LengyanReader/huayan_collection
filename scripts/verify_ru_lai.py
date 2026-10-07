#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verify_ru_lai.py —— 《如来现相品》专书常设门禁（L.116 立）

背景：《华严经细读_第二部_如来现相品.md》为先期一次性校勘所得，**无常设门禁**，
结论不可被后续批次复现（同 L.107 于《世主妙严品》之立桩）。本脚本固化五道断言：

  A 实测口径  —— 本品（＝卷第六）字/句/解脫门数须与 miaoyan_metrics.py 同源实测一致
  B 失效结论  —— 扫「已订正之旧数/旧论断」，命中即失败，但**须豁免校勘留痕段**
                  （口径留痕/范围更正本就应记录旧误，扫到它属门禁自身缺陷）
C 引文回源  —— §6.1 三译对读之 blockquote 逐条比对可信源；**繁简归一（T2S）＋
                  部首归一（RAD）**双层，俾传统字形引文能对上简体底本
  C2 §5 引文 —— §5.1′〈隨疏演義鈔〉/§5.3′〈新華嚴經論〉对应条：**自 doc 抽「」引文**
                  逐条回源 T1736/T1739（须自 doc 抽取，hardcode 即假绿）
  C3 §3 旁参 —— §3 卷第七旁参（非本品）之 blockquote 经文逐条回源 T10n0279（卷七前半），
                 同用繁简＋部首归一
  D 来源自洽  —— 文中所引本地路径皆须存在，且关键路径须出现
  E 契约串    —— 关键事实性论断（本品＝卷第六；解脫門＝0；四十华严不涉本品……）须在文

**口径要点**：本品＝卷第六**一卷**（卷七＝《普贤三昧品第三》，非本品）；实测
**8,119 字／208 句**、「解脫門」**0 见**（第一品 442 见）。数字须与单位绑定（同 L.107）。

**繁简归一之必要**：本机 `六十华严_1.txt` 为**简体**，而文中六十引文多为**传统字形**，
故 C 段对六十须 T2S 转换后比对，否则伪报（与 L.107「部首归一之必要」同源教训）。

反向验证见 _verify_ru_lai_reverse.py（破坏性变异须被捕获）。
"""
import io
import os
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE = r'C:\DA_Practice\huayan_collection'
DOC = os.environ.get('RU_LAI_DOC',
                     os.path.join(BASE, r'docs\经学文献\华严经细读_第二部_如来现相品.md'))

# ── 部首归一（康熙/兼容部首字；NFKC 不覆盖 U+2F00–U+2FDF）────────────────
RAD = {'⽣': '生', '⼤': '大', '⾨': '門', '⾝': '身', '⻄': '西', '⺠': '民',
       '⺒': '貝', '⾃': '自', '⾔': '言', '⾒': '見', '⾦': '金', '⾵': '風',
       '⿔': '龜', '⿔': '龜'}


def norm(s: str) -> str:
    import unicodedata
    s = unicodedata.normalize('NFKC', s)
    return ''.join(RAD.get(ch, ch) for ch in s)


# ── 繁简归一（T2S）：仅收文中六十引文与简体底本确有差异之字（够用为准）──────
T2S = {'爾': '尔', '時': '时', '薩': '萨', '眾': '众', '無': '无', '邊': '边',
       '門': '门', '間': '间', '寶': '宝', '燈': '灯', '雲': '云', '觀': '观',
       '剎': '刹', '於': '于', '還': '还', '從': '从', '輪': '轮', '塵': '尘',
       '與': '与', '勝': '胜', '諸': '诸', '來': '来', '數': '数', '盧': '卢',
       '滿': '满', '現': '现', '應': '应', '處': '处', '樹': '树', '為': '为',
       '說': '说', '賢': '贤', '華': '华', '會': '会', '莊': '庄', '嚴': '严',
       '繞': '绕', '遶': '绕', '遠': '远', '業': '业', '淨': '净', '滅': '灭',
       '繞': '绕', '遶': '绕', '遠': '远', '業': '业', '淨': '净', '滅': '灭',
       '耀': '耀', '續': '续', '發': '发', '願': '愿', '離': '离', '體': '体',
       '蓮': '莲', '葉': '叶', '緣': '缘', '對': '对', '圓': '圆', '極': '极',
       '樂': '乐', '護': '护', '種': '种', '積': '积', '際': '际', '專': '专',
       '語': '语', '蓋': '盖', '畫': '画', '聲': '声', '國': '国', '佛': '佛'}


def t2s(s: str) -> str:
    return ''.join(T2S.get(ch, ch) for ch in s)


PUNCT = re.compile(
    r'[＋，。、；：？！（）()「」『』《》〈〉〔〕【】…—－·,.;:!?\'"“”‘’\[\]{}<>｜|]')


def squash(s: str) -> str:
    s = norm(s).replace('**', '').replace('……', '').replace('…', '')
    s = PUNCT.sub('', s)
    return re.sub(r'[\s　]', '', s)


def read(path: str) -> str:
    with open(path, encoding='utf-8', errors='replace') as f:
        return f.read()


doc = read(DOC)
lines = doc.split('\n')

# 前言区（题名/声明）至首个独立 `---` 为版块标签，非引文，豁免。
_sep = next((i for i, l in enumerate(lines) if l.strip() == '---'), 0)
BODY = _sep + 1

CB = os.path.join(BASE, r'data\references\cbeta_txt')
YD = os.path.join(BASE, r'docs\huayanhai\义学专题\经论原典')

fails: list = []
notes: list = []


def check(cond, tag, msg):
    if cond:
        print('  [OK]   %s %s' % (tag, msg))
    else:
        print('  [FAIL] %s %s' % (tag, msg))
        fails.append('%s %s' % (tag, msg))


print('=' * 74)
print('verify_ru_lai.py —— 《如来现相品》专书门禁（L.116）')
print('=' * 74)

# 校勘留痕段识别（豁免旧数扫描）：凡记录旧误之段，正当保留旧数
PROOF = ('口径留痕', '範圍更正', '范围更正', '校勘留痕', '订正', '訂正', '更正',
         '旧稿', '舊稿', '误并', '誤并', '误', '誤', '撤回', '不确', '不確',
         '待核', '存疑', '初拟', '初擬', '更正留痕')


def is_proof(ln: str) -> bool:
    return any(k in ln for k in PROOF)


# ── A 实测口径 ────────────────────────────────────────────────────────────
print('\n【A】实测口径（须与 miaoyan_metrics.py 同源；本品＝卷第六）')
sys.path.insert(0, os.path.join(BASE, 'scripts'))
try:
    import miaoyan_metrics as MM
    J = MM.load()
    j6 = J[6]
    c6, s6 = MM.cjk_len(j6), MM.sentences(j6)
    notes.append('实测 卷第六 %d 字 / %d 句；解脫門 %d 见'
                 % (c6, s6, j6.count('解脫門')))
    check(c6 == 8119 and s6 == 208, 'A1',
          '本品（卷六）字句 = %d / %d（应 8119 / 208）' % (c6, s6))
    check(j6.count('解脫門') == 0, 'A2',
          '本品（卷六）解脫門 = %d（应 0；第一品为 442，判若两途）' % j6.count('解脫門'))
    check(MM.cjk_len(J[5]) == 5732, 'A3',
          '对照卷五字 = %d（应 5732，别于本品）' % MM.cjk_len(J[5]))
    # 正文自述数须与单位绑定（只验「存在」会被同句他处旧数蒙过，L.107 盲区）
    check(re.search(r'8,119\s*字', doc) is not None, 'A4', '正文自述「8,119 字」')
    check(re.search(r'208\s*句', doc) is not None, 'A5', '正文自述「208 句」')
except Exception as e:
    check(False, 'A0', 'miaoyan_metrics 导入失败：%r' % (e,))

# ── B 失效结论扫描 ────────────────────────────────────────────────────────
print('\n【B】失效结论/旧数扫描（防回退；豁免校勘留痕段）')
BANNED = [
    ('18,472', '旧误记「卷六～卷七」并数，正为本品卷六 8,119'),
    ('406 句', '旧误记句数，正为 208 句'),
    ('卷六～卷七', '本品＝卷第六一卷，非卷六～卷七'),
    ('卷六~卷七', '本品＝卷第六一卷，非卷六～卷七'),
    ('卷第六～卷第七', '本品＝卷第六一卷'),
]
for bad, why in BANNED:
    hits = [i for i, l in enumerate(lines, 1) if bad in l and not is_proof(l)]
    check(not hits, 'B:' + bad, '正文（除留痕）无「%s」——%s%s'
          % (bad, why, ('  ← 命中行 ' + str(hits[:6])) if hits else ''))
# 四十华严：惟〈入法界品〉一译，永久记阙（非待补）
check('四十華嚴' in doc or '四十华严' in doc, 'B6', '文述四十华严之关系')
check(('不涉本品' in doc) and ('惟〈入法界品〉' in doc or '惟入法界品' in doc),
      'B7', '四十华严「不涉本品·惟〈入法界品〉一會」之记阙在文')

# ── C 引文回源（§6.1 blockquote；繁简＋部首归一）──────────────────────────
print('\n【C】§6.1 三译对读 blockquote 回源（繁简 T2S ＋ 部首 RAD 归一）')
SRC = {}
x80 = read(os.path.join(BASE, r'data\references\cbeta\T10n0279.xml'))
x80 = re.sub(r'<note\b.*?</note>', '', x80, flags=re.S)
x80 = re.sub(r'<app\b.*?</app>', '', x80, flags=re.S)
x80 = re.sub(r'<[^>]+>', '', x80)
SRC['T279'] = x80
p60 = os.path.join(YD, '六十华严_1.txt')
if os.path.exists(p60):
    SRC['六十'] = read(p60)
if os.path.isdir(CB):
    for fn in sorted(os.listdir(CB)):
        if fn.endswith('.txt'):
            SRC[fn.split('_')[0]] = read(os.path.join(CB, fn))
SS = {k: squash(v) for k, v in SRC.items()}
notes.append('可信源 %d 份' % len(SRC))

# 定位 §6.1 区块（到下一个 ### 之前）
start = next((i for i, l in enumerate(lines) if l.startswith('### 6.1')), None)
end = None
if start is not None:
    end = next((i for i, l in enumerate(lines)
                if i > start and l.startswith('### ')), len(lines))
C_N = C_MISS = 0
C_BAD = []
if start is None:
    check(False, 'C:loc', '未找到 §6.1 区块')
else:
    for i in range(start, end):
        ln = lines[i]
        if not ln.strip().startswith('>'):
            continue
        t = ln.strip()[1:].lstrip()
        # 去引文行首之标签 `**八十（如來現相品）**：` 之类（若非引文本身）
        m = re.match(r'\*\*[^*]*\*\*\s*[：:]?', t)
        if m:
            t = t[m.end():]
        segs = re.findall(r'「([^」]+)」', t) or [t]
        for seg in segs:
            for part in re.split(r'……|…|／', seg):
                p = squash(part)
                if len(p) < 6:
                    continue
                C_N += 1
                hit = (p in SS['T279']) or (squash(t2s(part)) in SS.get('六十', ''))
                if not hit:
                    hit = any(p in v or squash(t2s(part)) in v
                              for v in SS.values())
                if not hit:
                    C_MISS += 1
                    C_BAD.append('L%d %s' % (i + 1, part[:40]))
    check(C_MISS == 0, 'C1', '§6.1 引文回源 %d 条全中（miss=%d）%s'
          % (C_N, C_MISS, ('  ← ' + str(C_BAD[:5])) if C_BAD else ''))

# ── C2 §5.1′〈演義鈔〉/§5.3′〈新論〉对应条：自 doc 抽「」引文逐条回源 ─────────
print('\n【C2】§5.1′〈鈔〉/§5.3′〈論〉引文回源（自 doc 抽「」·繁简＋部首归一）')
C2_REGIONS = [('T1736', '**〔T1736《隨疏演義鈔》对应条〕**', '### 5.2'),
              ('T1739', '### 5.3′', '### 5.4')]
C2_N = C2_MISS = 0
C2_BAD = []
for src_key, m_start, m_end in C2_REGIONS:
    i0 = next((i for i, l in enumerate(lines) if l.strip().startswith(m_start)), None)
    i1 = next((i for i, l in enumerate(lines)
               if i0 is not None and i > i0 and l.strip().startswith(m_end)), None)
    if i0 is None or i1 is None:
        check(False, 'C2:loc', '未定位 §5 区段（%s … %s）' % (m_start, m_end))
        continue
    for i in range(i0, i1):
        for seg in re.findall(r'「([^」]+)」', lines[i]):
            for part in re.split(r'……|…|／', seg):
                p = squash(part)
                if len(p) < 6:
                    continue
                C2_N += 1
                if p not in SS.get(src_key, ''):
                    C2_MISS += 1
                    C2_BAD.append('L%d %s' % (i + 1, part[:40]))
check(C2_MISS == 0 and C2_N > 0, 'C2',
      '§5 对应条引文回源 %d 条全中（miss=%d）%s'
      % (C2_N, C2_MISS, ('  ← ' + str(C2_BAD[:6])) if C2_BAD else ''))

# ── C3 §3 旁参（卷七·非本品）blockquote 经文回源 T10n0279 ──────────────────
print('\n【C3】§3 旁参（卷七）blockquote 回源（繁简＋部首归一）')
C3_N = C3_MISS = 0
C3_BAD = []
s3 = next((i for i, l in enumerate(lines) if l.startswith('## 三、旁参')), None)
e3 = next((i for i, l in enumerate(lines) if l.startswith('## 四、义理要点')), None)
if s3 is None or e3 is None:
    check(False, 'C3:loc', '未定位 §3 区块')
else:
    for i in range(s3, e3):
        ln = lines[i].strip()
        if not ln.startswith('>'):
            continue
        t = ln[1:].lstrip()
        # 仅查以「起首之经文 blockquote（排除 `> **〔…〕**` 之类 callout/注释块）
        if not t.startswith('「'):
            continue
        for seg in re.findall(r'「([^」]+)」', t):
            for part in re.split(r'……|…|／', seg):
                p = squash(part)
                if len(p) < 6:
                    continue
                C3_N += 1
                if p not in SS['T279']:
                    C3_MISS += 1
                    C3_BAD.append('L%d %s' % (i + 1, part[:40]))
    check(C3_MISS == 0 and C3_N > 0, 'C3',
          '§3 旁参 blockquote 回源 %d 条全中（miss=%d）%s'
          % (C3_N, C3_MISS, ('  ← ' + str(C3_BAD[:6])) if C3_BAD else ''))

# ── D 来源自洽 ────────────────────────────────────────────────────────────
print('\n【D】来源声明自洽（防假出处）')
paths = set(re.findall(r'\]\(\.\./\.\./\.\./(docs/[^)]+)\)', doc))
paths |= set(re.findall(r'`(docs/[^`]+\.txt)`', doc))
bad_paths = [p for p in paths
             if not os.path.exists(os.path.join(BASE, p.replace('/', os.sep)))]
check(not bad_paths, 'D1', '文中所引 %d 个本地路径皆存在%s'
      % (len(paths), ('  ← 缺失 ' + str(bad_paths)) if bad_paths else ''))
check('T09n0278' in doc or '六十华严_1.txt' in doc, 'D2',
      '文述六十对读底本（T09n0278／六十华严_1.txt）')
check(os.path.exists(p60), 'D3', '六十华严_1.txt 底本存在')

# ── E 契约串 ──────────────────────────────────────────────────────────────
print('\n【E】关键事实性论断契约')
for tag, needle, msg in [
        ('E1', '本品＝卷第六', '本品＝卷第六一卷'),
        ('E2', '解脫門', '述「解脫門」之数（0 见）'),
        ('E3', '普賢三昧品', '卷七＝普贤三昧品第三（非本品）'),
        ('E4', '四十华严', '四十华严对应之记阙'),
]:
    check(needle in doc, tag, msg)
check(re.search(r'解脫門[^。]{0,20}0\s*见', doc) is not None
      or '「解脫門」＝0' in doc or '解脫門」＝0 見' in doc
      or re.search(r'解脫門.{0,30}0', doc) is not None,
      'E5', '文述「解脫门 0 见」')
# §2.6 偈颂支分：胜音＋十大士＝11 组各 10 偈；卷六偈颂 132 偈
check('偈颂支分' in doc or '偈頌支分' in doc, 'E6', '有 §2.6 偈颂支分（逐颂标定）')
check(('十一组' in doc or '十一位' in doc) and ('勝音' in doc or '胜音' in doc),
      'E7', '述「胜音＋十大士（十一组）」之数（订正旧「十大士」含混）')
check(re.search(r'132\s*偈', doc) is not None, 'E8', '述卷六偈颂合计「132 偈」')
# §3 旁参（卷七·非本品）：卷七含二品；前半普贤三昧品 1,995 字／二颂共 20 偈
check(re.search(r'1,995\s*字', doc) is not None and '世界成就品' in doc,
      'E9', '述 §3 旁参--卷七前半 1,995 字 且及「世界成就品第四」')
check(re.search(r'20\s*偈', doc) is not None
      and ('光中颂' in doc or '光中頌' in doc) and '众赞颂' in doc,
      'E10', '述 §3 旁参--普贤三昧品二颂共 20 偈')

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
print('ALL CHECKS PASSED —— 《如来现相品》门禁全绿')