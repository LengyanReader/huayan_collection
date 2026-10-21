# -*- coding: utf-8 -*-
"""L.138b · huayanhai 玄谈 01/05/07/08/09/11 · 抽头 15 lines to construct comparison"""
import io, os, sys
for _s in (sys.stdout, sys.stderr):
    try: _s.reconfigure(encoding="utf-8", errors="replace")
    except: pass

d = 'docs/huayanhai/华严云海/浩瀚华严海/华严经玄谈'
for f in ['华严经玄谈05_1.txt', '华严经玄谈07_1.txt', '华严经玄谈08_1.txt', '华严经玄谈11_1.txt']:
    p = os.path.join(d, f)
    txt = io.open(p, encoding='utf-8').read()
    # 抽 講記 段前 600 字
    k = txt.find('【講記】')
    if k == -1:
        k = 500
    seg = txt[k+4:k+800].replace('\n', ' ').strip()
    print(f"==== {f} · 講記 head 800字 ====")
    print(seg)
    print()
    # 抽 tail (结尾结论段)
    tail = txt[-500:].replace('\n',' ').strip()
    print(f"---- {f} · tail 500字 ----")
    print(tail)
    print()
