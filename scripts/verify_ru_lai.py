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
  C3 §3 旁参 —— §3 卷第七旁参（非本品）之 blockquote 经文逐条回源 T10n0279
  H §2.7 逐颂 —— L.125 说颂分逐颂细读（前导三颂＋勝音＋十大士十四组）之 blockquote
                   偈颂逐条回源 T10n0279 卷六（繁简＋部首归一）（卷七前半），
                 同用繁简＋部首归一
  D 来源自洽  —— 文中所引本地路径皆须存在，且关键路径须出现
  E 契约串    —— 关键事实性论断（本品＝卷第六；解脫門＝0；四十华严不涉本品……）须在文
  F 续补契约  —— L.122 新增：§1.1 品题释义（非〔待续〕）／§6.1 〇′ 面门光段十光名
                  （八十回源 T279、六十 T2S 回源）／§6.2·§6.4 藏译对应品坐实（84000）／
                  §7.4 数据科学＋叙事已成（非空登记）
   G 附录契约  —— L.124 新增：附录一～（除四）诸附录皆须**有成文**（非空壳），且附录一
                   载逐卷数（442／129／135／144／551）、附录二载十方名相与四十问、附录三载
                   十光名对照、附录六载讲稿入口、附录九三级（A1/A2/T2）、附录十一四视角；
                   并销 §7.2 旧数（承佛威神 8→9、爾時 44→17）与 §5.4.3 交叉引用（§7→§2.1）
   H §2.7 逐颂 —— L.125：§2.7 说颂分逐颂细读之 blockquote 逐条回源 T10n0279（繁简＋部首）
   I §6.5 全量 —— 本批：§6.5 六十〈卢舍那佛品〉全量逐段对照之 blockquote 逐条回源
                   （T10n0279 或六十华严_1.txt）＋十方表十名＋契约串

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
                     os.path.join(BASE, r'docs\经学文献\华严经细读\第一会_菩提场_所信因果周\华严经细读_第二部_如来现相品.md'))

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
       '語': '语', '蓋': '盖', '畫': '画', '聲': '声', '國': '国', '佛': '佛',
       # L.122 补：§6.1 〇′ 面门光段对读所需（六十底本为简体，引文为传统）
       '齒': '齿', '場': '场', '剛': '刚', '詣': '诣', '屬': '属', '見': '见',
       '謂': '谓', '礙': '碍'}


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
print('verify_ru_lai.py —— 《如来现相品》专书门禁（L.116 立；L.122 F 段；L.124 G 段；L.125 H 段；§6.5 I 段）')
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
    ('132 偈', '旧偈数计入之误，正为 140 偈（前① 10 偈；L.125）'),
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
check('T09n0278' in doc, 'D2',
      '文述六十对读底本经号 T09n0278')
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
check(re.search(r'140\s*偈', doc) is not None, 'E8', '述卷六偈颂合计「140 偈」（旧 132 已订正·L.125）')
# §3 旁参（卷七·非本品）：卷七含二品；前半普贤三昧品 1,995 字／二颂共 20 偈
check(re.search(r'1,995\s*字', doc) is not None and '世界成就品' in doc,
      'E9', '述 §3 旁参--卷七前半 1,995 字 且及「世界成就品第四」')
check(re.search(r'20\s*偈', doc) is not None
      and ('光中颂' in doc or '光中頌' in doc) and '众赞颂' in doc,
      'E10', '述 §3 旁参--普贤三昧品二颂共 20 偈')


# ── F L.122 续补内容契约（品题释义／面门光段／藏译坐实／§7.4）─────────────
print('\n【F】L.122 续补内容契约（§1.1／§6.1〇′／§6.2／§6.4／§7.4）')


def region_text(start_pat, end_pat):
    s = next((i for i, l in enumerate(lines) if l.startswith(start_pat)), None)
    if s is None:
        return None
    e = next((i for i, l in enumerate(lines)
              if i > s and l.startswith(end_pat)), len(lines))
    return '\n'.join(lines[s:e])


t11 = region_text('### 1.1', '### 1.2')
if t11 is None:
    check(False, 'F1:loc', '未找到 §1.1 区块')
else:
    check('〔待续〕' not in t11 and '〔待續〕' not in t11, 'F1',
          '§1.1 品题释义已成立（无〔待续〕占位）')
    check('如來是能現之人' in t11 or '如来是能现之人' in t11, 'F2',
          '§1.1 引澄观「如來是能現之人」')
    check('相是所現之法' in t11 or '相是所现之法' in t11, 'F3',
          '§1.1 引澄观「相是所現之法」')
    check(('现相五义' in t11 or '現相五義' in t11 or '各有五義' in t11
           or '各有五义' in t11), 'F4', '§1.1 述「如来五义合现相五义」')

# §6.1 〇′ 面门光段：十光名对照（八十名回源 T279；六十名 T2S 回源六十底本）
N80 = ['眾寶華遍照光明', '出種種音莊嚴法界光明', '垂布微妙雲光明',
       '十方佛坐道場現神變光明', '一切寶焰雲蓋光明', '充滿法界無礙光明',
       '遍莊嚴一切佛剎光明', '逈建立清淨金剛寶幢光明', '普莊嚴菩薩眾會道場光明',
       '妙音稱揚一切佛名號光明']
N60 = ['寶幢照光明', '法界妙音莊嚴光明', '生樂垂雲光明', '佛十種力嚴淨道場光明',
       '一切寶焰雲光明', '清淨無礙充滿法界光明', '能成一切世界光明',
       '淨寶金剛日幢光明', '往詣菩薩大眾光明', '演出諸佛語輪光明']
t61 = region_text('### 6.1', '### 6.2') or ''
miss_doc = [n for n in (N80 + N60) if n not in t61]
check(not miss_doc, 'F5', '§6.1 〇′ 十光名（80/60 各十）俱见于文%s'
      % (('  ← 缺 ' + str(miss_doc)) if miss_doc else ''))
miss80 = [n for n in N80 if squash(n) not in SS['T279']]
check(not miss80, 'F6', '八十十光名俱回源 T10n0279%s'
      % (('  ← ' + str(miss80)) if miss80 else ''))
miss60 = [n for n in N60 if squash(t2s(n)) not in SS.get('六十', '')]
check(not miss60, 'F7', '六十十光名俱回源六十华严_1.txt（T2S 归一后）%s'
      % (('  ← ' + str(miss60)) if miss60 else ''))
check('面門眾齒之間' in t61 or '面门众齿之间' in t61, 'F8',
      '§6.1 〇′ 述八十放光处「面門眾齒之間」')

# §6.2／§6.4 藏译对应品坐实（84000 编目）
t62 = region_text('### 6.2', '### 6.3') or ''
t64 = region_text('### 6.4', '## 七、') or ''
check('de bzhin gshegs pa' in t62 and '84000' in t62, 'F9',
      '§6.2 坐实藏译对应品（de bzhin gshegs pa／84000）')
check('84000' in t64 and ('不见于任何汉' in t64 or '不見於任何漢' in t64),
      'F10', '§6.4 引 84000 旁证「不见于汉译」')
check('rmad ga cad' in t64, 'F11', '§6.4 载 84000 藏名形 rmad ga cad')

# §7.4 数据科学／叙事已成（非空登记）
t74 = region_text('### 7.4', '## 八、') or ''
check(('ru_lai_studies.yaml' in t74) and ('ru_lai_narrative.yaml' in t74),
      'F12', '§7.4 述数据科学层＋叙事动画之数据文件')
check(('未及·登记' not in t74) and ('未做' not in t74) and
      ('数据科学' in t74 or '数据科學' in t74), 'F13',
      '§7.4 已更新（无「未及·登记／未做」旧记）')

# ── G L.124 附录成套契约 ──────────────────────────────────────────────────
print('\n【G】L.124 附录成套契约（附录一/二/三/五/六/七/八/九/十一非空；旧数销项）')


def apx(title_prefix):
    s = next((i for i, l in enumerate(lines) if l.startswith(title_prefix)), None)
    if s is None:
        return None
    e = next((i for i, l in enumerate(lines) if i > s and l.startswith('### ')), len(lines))
    return '\n'.join(lines[s:e])


A1 = apx('### 附录一·') or ''
A2 = apx('### 附录二·') or ''
A3 = apx('### 附录三·') or ''
for tag, t, need in [
        ('G1', A1, None), ('G2', A2, None), ('G3', A3, None),
        ('G4', apx('### 附录五·') or '', None), ('G5', apx('### 附录六·') or '', None),
        ('G6', apx('### 附录七·') or '', None), ('G7', apx('### 附录八·') or '', None),
        ('G8', apx('### 附录九·') or '', None), ('G9', apx('### 附录十·') or '', None),
        ('G10', apx('### 附录十一·') or '', None)]:
    check(len(t) > 200, tag, '附录有成文（len=%d > 200）' % len(t))
# 附录一：实测数（442 逐卷 129/135/144/34；全经 551）
check(all(k in A1 for k in ('442', '129', '135', '144', '551')) and '解脫門' in A1,
      'G11', '附录一 载解脫门逐卷数（0/129/135/144/34＝442）及全经 551')
check('**0**' in A1 or '**0 见**' in A1 or '＝ **0**' in A1 or '0 见' in A1, 'G12',
      '附录一 述本品解脫门 0 见')
# 附录二：十方名相＋四十问
check(('清淨光蓮華莊嚴' in A2) and ('無礙力精進慧' in A2) and ('甲' in A2 and '乙' in A2),
      'G13', '附录二 载十方世界海名相与四十问（甲/乙）')
# 附录三：十光名对照＋三译位置
check(('眾寶華遍照光明' in A3) and ('寶幢照光明' in A3) and ('T09n0278' in A3)
      and ('T10n0293' in A3), 'G14', '附录三 载十光名对照与三译位置')
# 附录六：讲记入口（西安草堂寺导读）
check(('西安草堂寺' in (apx('### 附录六·') or ''))
      and ('八十华严导读' in (apx('### 附录六·') or '')), 'G15',
      '附录六 载海云《八十华严导读》入口')
# 附录九：三级（A1 经证／A2 注疏／T2 学术）
A9 = apx('### 附录九·') or ''
check(('A1' in A9) and ('A2' in A9) and ('T2' in A9), 'G16',
      '附录九 三级「出处＋信度」（A1/A2/T2）俱在')
# 附录十一：四视角
A11 = apx('### 附录十一·') or ''
check(all(k in A11 for k in ('语言统计', '代数', '拓扑', '几何'))
      and ('Burnside' in A11) and ('Laplacian' in A11), 'G17',
      '附录十一 载数据科学四视角（语言统计/代数/拓扑/几何）')
# 旧数销项：§7.2 承佛威神 9／爾時 17（**限定 §7.2 区段**，避免他处「承佛威神 9」
# 同句蒙过——L.107「数字须与单位绑定」之变体：数字须与**所在区段**绑定）
t72 = region_text('### 7.2', '### 7.3') or ''
check('「承佛威神」**9** 见' in t72, 'G18',
      '§7.2 述「承佛威神 9 见」（旧 8 已销）')
check('**17** 见' in t72 and '「爾時」**：' in t72, 'G19',
      '§7.2 述「爾時 17 见」（旧 44 已销）')
check('见 §7 待补' not in doc and '見 §7 待補' not in doc, 'G20',
      '§5.4.3 交叉引用已改指 §2.1（无「见 §7 待补」）')
_lst = dict(re.findall(r'^- 附录([一二三四五六七八九十]+)：(.*?)\s*$', doc, re.M))
_hd = dict(re.findall(r'^### 附录([一二三四五六七八九十]+)·(.*?)\s*$', doc, re.M))
_mm = [k for k in _lst if _hd.get(k) != _lst[k]]
check(len(_lst) == 11 and not _mm, 'G21',
      '§八 附录目录标题与正文标题一致（%d 条%s）'
      % (len(_lst), '' if not _mm else '；异：' + ','.join(_mm)))

# ── H L.125 §2.7 说颂分·逐颂细读 引文回源 ────────────────────────────────
print('\n【H】L.125 §2.7 逐颂细读·引文回源（繁简＋部首归一；十四组各十偈）')
s7 = next((i for i, l in enumerate(lines) if l.startswith('### 2.7')), None)
e7 = None
if s7 is not None:
    e7 = next((i for i, l in enumerate(lines)
               if i > s7 and l.startswith('## 三、')), None)
if s7 is None or e7 is None:
    check(False, 'H:loc', '未定位 §2.7 区块（### 2.7 … ## 三、）')
else:
    H_N = H_MISS = 0
    H_BAD = []
    reg = '\n'.join(lines[s7:e7])
    for i in range(s7, e7):
        ln = lines[i].strip()
        if not ln.startswith('>'):
            continue
        t = ln[1:].lstrip()
        # §2.7 之偈颂 blockquote 直书经文（未以「」包裹）；排除 callout/注释块
        if t.startswith('**') or t.startswith('〔') or t.startswith('>') or not t:
            continue
        segs = re.findall(r'「([^」]+)」', t) or [t]
        for seg in segs:
            for part in re.split(r'……|…|／', seg):
                p = squash(part)
                if len(p) < 6:
                    continue
                H_N += 1
                if p not in SS['T279']:
                    H_MISS += 1
                    H_BAD.append('L%d %s' % (i + 1, part[:40]))
    check(H_MISS == 0 and H_N >= 100, 'H1',
          '§2.7 逐颂引文回源 %d 条全中（miss=%d）%s'
          % (H_N, H_MISS, ('  ← ' + str(H_BAD[:6])) if H_BAD else ''))
    check(len(re.findall(r'^#### 2\.7\.\d+ ', '\n'.join(lines[s7:e7]), re.M)) >= 15,
          'H2', '§2.7 逐组细读（≥15 小节 #### 2.7.N：十四组＋小结）')
    check(('140 偈' in '\n'.join(lines[s7:e7]))
          or ('一百四十偈' in '\n'.join(lines[s7:e7])), 'H3',
          '§2.7 述卷六说颂合计「140 偈／一百四十偈」')
    check(('40 句＝10 偈' in doc), 'H4',
          '§2.7／§2.6 记前①「自然出音」颂勘误实测「40 句＝10 偈」')

# ── I L.晋级 §6.5 六十全量逐段对照（引文回源＋十方表＋契约）─────────────────
print('\n【I】§6.5 六十〈卢舍那佛品〉全量逐段对照（引文回源＋十方表＋契约）')
s65 = next((i for i, l in enumerate(lines) if l.startswith('### 6.5 ')), None)
e65 = next((i for i, l in enumerate(lines)
            if i > (s65 or 0) and l.startswith('## 七、')), None)
t65 = '\n'.join(lines[s65:e65]) if (s65 is not None and e65 is not None) else ''
check(s65 is not None and e65 is not None and len(t65) > 2000, 'I1',
      '§6.5 全量对照有成文（len=%d > 2000）' % len(t65))
if s65 is not None and e65 is not None:
    I_N = I_MISS = 0
    I_BAD = []
    for i in range(s65, e65):
        ln = lines[i].strip()
        if not ln.startswith('>'):
            continue
        t = ln[1:].lstrip()
        if t.startswith('**') or t.startswith('〔'):
            continue
        segs = re.findall(r'「([^」]+)」', t) or [t]
        for seg in segs:
            for part in re.split(r'……|…|／', seg):
                p = squash(part)
                if len(p) < 6:
                    continue
                I_N += 1
                hit = (p in SS['T279']) or (p in SS.get('六十', ''))
                if not hit:
                    I_MISS += 1
                    I_BAD.append('L%d %s' % (i + 1, part[:40]))
    check(I_MISS == 0 and I_N >= 20, 'I2',
          '§6.5 引文回源 %d 条全中（miss=%d）%s'
          % (I_N, I_MISS, ('  ← ' + str(I_BAD[:6])) if I_BAD else ''))
    # 十方表：六十世界海名（简体·直接比对底本）
    NX10 = ['净莲华胜光庄严', '众宝月光庄严藏', '宝光乐', '琉璃宝光充满藏',
            '阎浮檀玻璃色幢', '普照庄严', '善光照', '宝照光明藏',
            '莲华妙香胜藏', '杂宝光海庄严']
    miss_src = [n for n in NX10 if n not in SS.get('六十', '')]
    check(not miss_src, 'I3', '§6.5 十方表·六十世界海名俱回源六十华严_1.txt%s'
          % (('  ← 缺 ' + str(miss_src)) if miss_src else ''))
    NX10_DOC = ['淨蓮華勝光莊嚴', '眾寶月光莊嚴藏', '寶光樂', '琉璃寶光充滿藏',
                '閻浮檀玻璃色幢', '普照莊嚴', '善光照', '寶照光明藏',
                '蓮華妙香勝藏', '雜寶光海莊嚴']
    miss_doc = [n for n in NX10_DOC if n not in t65]
    check(not miss_doc, 'I4', '§6.5 十方表载十世界海名（传统字形）%s'
          % (('  ← 缺 ' + str(miss_doc)) if miss_doc else ''))
    # 契约串
    check('师子焰光奋迅音' in t65 and '11→1' in t65, 'I5',
          '§6.5 述「说颂者 11→1」（师子焰光奋迅音）')
    check('40→25' in t65 and '二十五目' in t65, 'I6',
          '§6.5 述念请问目「40→25」（并载「二十五目」）')
    check(('勝音' in t65 or '胜音' in t65) and (r'3 偈' in t65), 'I7',
          '§6.5 述勝音六十一颂「3 偈」')
    check('T09n0278' in t65 and 'T10n0279' in t65, 'I8',
          '§6.5 标注二译底本经号')

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