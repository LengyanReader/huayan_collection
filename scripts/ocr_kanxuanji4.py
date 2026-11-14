# -*- coding: utf-8 -*-
"""ocr_kanxuanji4.py — L.474：海云《勘玄记04》（离世间品）370 页 OCR 入仓
管线：pypdfium2 渲染（300 DPI）＋ tesseract 5.4.0 chi_tra（TESSDATA_PREFIX 指仓内 tessdata）
产出：data/references/huayan_daodu/堪玄记04_离世间品_OCR提取本.txt（逐页【Pn】标记·残误如实保留）
"""
import io, os, re, sys, time
import pypdfium2 as pdfium
import subprocess

sys.stdout.reconfigure(encoding='utf-8')
PDF = "C:/华严/经典著作/《勘玄记04》（离世间品）.pdf"
OUT = 'data/references/huayan_daodu/堪玄记04_离世间品_OCR提取本.txt'
LOG = 'data/references/huayan_daodu/堪玄记04_ocr_progress.log'
TESS = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
ENV = {**os.environ, 'TESSDATA_PREFIX': os.path.abspath('tools/tesseract/tessdata')}

def han(s):
    return len(re.findall(r'[\u3400-\u9fff]', s))

pdf = pdfium.PdfDocument(PDF)
n = len(pdf)
t0 = time.time()
parts = []
with open(LOG, 'w', encoding='utf-8') as log:
    for i in range(n):
        page = pdf[i]
        bmp = page.render(scale=300 / 72)
        png = '_ocr_page.png'
        bmp.to_pil().save(png)
        page.close()
        r = subprocess.run([TESS, png, 'stdout', '-l', 'chi_tra', '--psm', '3'],
                           capture_output=True, text=True, env=ENV)
        txt = r.stdout.strip()
        parts.append('\n【P%d】\n' % (i + 1) + txt)
        el = time.time() - t0
        log.write('页 %d/%d · CJK %d · 累计 %.0fs\n' % (i + 1, n, han(txt), el))
        log.flush()
        if (i + 1) % 20 == 0:
            print('页 %d/%d · 累计 CJK %d · %.0fs' % (i + 1, n, sum(han(p) for p in parts), el), flush=True)
pdf.close()
os.remove('_ocr_page.png')

full = '\n'.join(parts)
io.open(OUT, 'w', encoding='utf-8', newline='').write(full)
print('完成：%s · %d 页 · %d CJK · %.0fs' % (OUT, n, han(full), time.time() - t0), flush=True)
