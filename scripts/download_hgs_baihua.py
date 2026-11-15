# -*- coding: utf-8 -*-
"""download_hgs_baihua.py — L.477：新加坡華嚴禪寺《網路白話華嚴經淺釋》全 50 分册下载
服务器：hgs.sg（本机 DNS 坏·curl --resolve 钉 IP；传输不稳·断点续传＋pypdfium 验证×3 重试）
"""
import os, subprocess, sys, time
import pypdfium2 as pdfium

sys.stdout.reconfigure(encoding='utf-8')
IP = '101.100.211.131'
BASE = 'http://hgs.sg/hgs/05_buddha/buddha_03/'
DL = 'data/references/huayan_daodu/hgs_baihua_pdf'
os.makedirs(DL, exist_ok=True)

FILES = ['chapter_%02d.pdf' % i for i in range(1, 25)]
FILES += ['chapter_25-01.pdf'] + ['chapter_26-%02d.pdf' % i for i in range(1, 11)]
FILES += ['chapter_27-01.pdf'] + ['chapter_%02d.pdf' % i for i in range(28, 38)]
FILES += ['chapter_38-%02d.pdf' % i for i in range(1, 5)]

def valid(fp):
    try:
        pdf = pdfium.PdfDocument(fp)
        n = len(pdf)
        pdf.close()
        return n > 0
    except Exception:
        return False

ok, fail = [], []
t0 = time.time()
for fn in FILES:
    fp = os.path.join(DL, fn)
    good = False
    for attempt in range(1, 6):
        args = ['curl', '-s', '--resolve', 'hgs.sg:80:' + IP, BASE + fn, '-o', fp,
                '--max-time', '300', '--speed-time', '30', '--speed-limit', '2000']
        if attempt > 1 and os.path.exists(fp):
            args.append('-C')
            args.append('-')
        subprocess.run(args, capture_output=True)
        if os.path.exists(fp) and os.path.getsize(fp) > 5000 and valid(fp):
            good = True
            break
        time.sleep(2)
    el = time.time() - t0
    if good:
        ok.append(fn)
        print('✓ %s（%d/%d·%.0fs）' % (fn, len(ok), len(FILES), el), flush=True)
    else:
        fail.append(fn)
        print('✗ %s（3 次重试仍失败）' % fn, flush=True)

print('\n完成：%d 成功 · %d 失败 · %.0fs' % (len(ok), len(fail), time.time() - t0))
if fail:
    print('失败清单:', fail)
