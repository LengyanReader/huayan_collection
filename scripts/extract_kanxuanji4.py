# -*- coding: utf-8 -*-
"""extract_kanxuanji4.py — L.474：勘玄记04 OCR 提取本 → P38 离世间品 海云讲记实引
OCR 件引用纪律（daodu_index）：逐字照录并注路径与提取状态；残误 90-95% 字准如实标注。
"""
import io, re, sys, glob
sys.stdout.reconfigure(encoding='utf-8')

APPLY = '--apply' in sys.argv

t = io.open('data/references/huayan_daodu/堪玄记04_离世间品_OCR提取本.txt', encoding='utf-8').read()

def han(s):
    return len(re.findall(r'[\u3400-\u9fff]', s))

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

# 页结构：【Pn】
pages = re.split(r'【P(\d+)】', t)
# pages[0] 空，之后 (num, text) 交替
pg = [(int(pages[i]), pages[i + 1]) for i in range(1, len(pages) - 1, 2)]
print('OCR 页数:', len(pg), '· 总 CJK:', sum(han(x) for _, x in pg))

# 离世间讲记主段：找内容最厚的一组连续页（每页 ≥100 CJK 的最长连续带）
runs, cur = [], []
for num, x in pg:
    if han(x) >= 100:
        cur.append((num, x))
    else:
        if len(cur) >= 3:
            runs.append(cur)
        cur = []
if len(cur) >= 3:
    runs.append(cur)
runs.sort(key=lambda r: sum(han(x) for _, x in r), reverse=True)
print('内容带:', [(r[0][0], r[-1][0], sum(han(x) for _, x in r)) for r in runs[:4]])

# 取第一内容带 → 抽 2-3 段实引（每段 ~800 CJK·句界）
sel = runs[0]
joined = ''.join(x for _, x in sel)
pages_span = (sel[0][0], sel[-1][0])
sents = re.split(r'(?<=[。！？」』])', joined)
passages, curp = [], ''
for s in sents:
    curp += s
    if han(curp) >= 780:
        passages.append(curp)
        curp = ''
if curp and han(curp) > 300:
    passages.append(curp)
passages = passages[:3]
print('页跨 P%d-P%d · 候选段 %d' % (pages_span[0], pages_span[1], len(passages)))

if APPLY:
    fp = glob.glob('docs/经学文献/华严经细读/**/华严经细读_第三十八部_*.md', recursive=True)[0]
    md = io.open(fp, encoding='utf-8').read()
    i52 = md.find('### 5.2')
    mnext = re.search(r'\n### |\n## ', md[i52:])
    end = i52 + (mnext.start() if mnext else len(md) - i52)
    blocks = []
    for i, p in enumerate(passages, 1):
        pclean = re.sub(r'\s+', '', p)   # OCR 件字符间空格清洗（引文体例·无空格块）
        blocks.append('**海云继梦《勘玄記04》（離世間品講記·OCR 提取本）·段%d**（%d 字·程序抽取·'
                      '源勘玄记04 PDF 页 %d-%d·OCR 字准约 90-95%%·引前须对原书核）：\n\n> %s' % (
                          i, han(pclean), pages_span[0], pages_span[1], pclean))
    md = md[:end] + '\n\n' + '\n\n'.join(blocks) + '\n' + md[end:]
    io.open(fp, 'w', encoding='utf-8', newline='').write(md)
    print('已写入 P38 5.2：', len(passages), '段')
else:
    for i, p in enumerate(passages, 1):
        pclean = re.sub(r'\s+', '', p)
        print('段%d（%d 字）: %s' % (i, han(pclean), pclean[:80]))
