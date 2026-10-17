# -*- coding: utf-8 -*-
"""新增引文回源校验（H2 round）：
   扫描 6 部之新增节（部1 八.9/八.10；部2-6 5.2'/5.2"），
   抽出 '「…」' 引文，按底本（T1732 / X0221）归一后逐条子串比对。
"""
import io, re, sys, unicodedata
sys.stdout.reconfigure(encoding='utf-8')

SUP = {0x2ED1: '長', 0x2EC4: '西', 0x2E9F: '母', 0x2EA0: '民'}


def norm(s):
    out = []
    for ch in s:
        o = ord(ch)
        if 0x2F00 <= o <= 0x2FDF:
            out.append(unicodedata.normalize('NFKC', ch))
        elif o in SUP:
            out.append(SUP[o])
        else:
            out.append(ch)
    return ''.join(out)


def squash(s):
    s = norm(s)
    s = re.sub(r'<<<PAGE \d+>>>', '', s)
    s = re.sub(r'\s+', '', s)
    return s


SRC = {
    'T1732': squash(io.open('data/references/cbeta_txt/T1732_智俨_搜玄记.txt',
                             encoding='utf-8', errors='ignore').read()),
    'X0221': squash(io.open('data/references/cbeta_txt/X0221_慧苑_续华严略疏刊定记.txt',
                            encoding='utf-8', errors='ignore').read()),
}

D = 'docs/经学文献/华严经细读/第一会_菩提场_所信因果周/'
FILES = {
    '部1': '华严经细读_第一部_世主妙严品.md',
    '部2': '华严经细读_第二部_如来现相品.md',
    '部3': '华严经细读_第三部_普贤三昧品.md',
    '部4': '华严经细读_第四部_世界成就品.md',
    '部5': '华严经细读_第五部_华藏世界品.md',
    '部6': '华严经细读_第六部_毗卢遮那品.md',
}

CJK = re.compile(r'[\u3400-\u9fff]')


def sections(txt):
    """返回新增节文本 (label, body)。"""
    lines = txt.split('\n')
    out = []
    idx = [(i, l) for i, l in enumerate(lines)
           if l.startswith('### 八.9') or l.startswith('### 八.10')
           or l.startswith('### 5.2′') or l.startswith('### 5.2″')]
    for k, (i, l) in enumerate(idx):
        j = len(lines)
        for m in range(i + 1, len(lines)):
            if re.match(r'^#{2,3} ', lines[m]):
                j = m
                break
        body = '\n'.join(lines[i + 1:j])
        out.append((l[:30], body))
    return out


bad = 0
tot = 0
for tag, fn in FILES.items():
    txt = io.open(D + fn, encoding='utf-8', errors='ignore').read()
    for label, body in sections(txt):
        # 决定底本
        if '八.9' in label or '5.2′' in label:
            src = SRC['T1732']; which = 'T1732'
        elif '八.10' in label or '5.2″' in label:
            src = SRC['X0221']; which = 'X0221'
        else:
            src = SRC['T1732'] + SRC['X0221']; which = 'both'
        quotes = []
        for line in body.split('\n'):
            if line.lstrip().startswith('>'):
                quotes += re.findall(r'「([^」]+)」', line)
        for q in quotes:
            if len(CJK.findall(q)) < 6:
                continue  # 短词/标题不校
            tot += 1
            # 依 '……' / '〔' / '。' 切段，各段独立比对
            for frag in re.split(r'……|〔[^〕]*〕|。', q):
                frag = frag.strip(' ')
                if len(CJK.findall(frag)) < 8:
                    continue
                if squash(frag) not in src:
                    bad += 1
                    print('  MISS [%s %s %s] %s' % (tag, which, label, frag[:70]))

print('引文片段校讫：共 %d 条，失配 %d 条' % (tot, bad))
print('ALL PASS' if bad == 0 else 'HAS MISSES')
