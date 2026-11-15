# -*- coding: utf-8 -*-
"""extract_hgs_baihua.py — L.477b：新加坡白话浅释 PDF→按品归档文本
产出：data/references/huayan_daodu/hgs_baihua/品NN.txt（多分册合并·含页码标记）
"""
import os, re, sys, glob
import pypdfium2 as pdfium

sys.stdout.reconfigure(encoding='utf-8')
DL = 'data/references/huayan_daodu/hgs_baihua_pdf'
OUT = 'data/references/huayan_daodu/hgs_baihua'
os.makedirs(OUT, exist_ok=True)

def han(s):
    return len(re.findall(r'[\u3400-\u9fff]', s))

groups = {}
for fp in sorted(glob.glob(DL + '/chapter_*.pdf')):
    m = re.match(r'chapter_(\d+)(?:-(\d+))?\.pdf$', os.path.basename(fp))
    if not m:
        continue
    ch = int(m.group(1))
    try:
        pdf = pdfium.PdfDocument(fp)
        n = len(pdf)
        txt = []
        for j in range(n):
            page = pdf[j]; tp = page.get_textpage()
            txt.append('【页%d】\n' % (j + 1) + tp.get_text_bounded())
            page.close(); tp.close()
        pdf.close()
        groups.setdefault(ch, []).append('\n'.join(txt))
    except Exception as e:
        print('✗ %s: %s' % (fp, str(e)[:50]))

total = 0
for ch in sorted(groups):
    body = ('\n\n【分册 %d 之 %d】\n\n'.join('') ) # placeholder
    merged = '\n\n【分册续】\n\n'.join(groups[ch]) if len(groups[ch]) > 1 else groups[ch][0]
    body = '新加坡華嚴禪寺《網路白話華嚴經淺釋》〈第%d品〉（釋法欣 整理）\n' \
           '来源：http://hgs.sg/hgs/05_buddha/buddha_03/（%d 分册）\n' \
           '性质：二手整理·白话浅释·可引用须标来源（用户裁定 L.139.0）\n\n' % (ch, len(groups[ch])) + merged
    fp = os.path.join(OUT, '品%02d.txt' % ch)
    with open(fp, 'w', encoding='utf-8', newline='') as f:
        f.write(body)
    total += han(body)
    print('品%02d: %d 分册 · %d CJK ✓' % (ch, len(groups[ch]), han(body)))
print('\n归档 %d 品 · 合计 %d CJK' % (len(groups), total))
