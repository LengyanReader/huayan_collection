# -*- coding: utf-8 -*-
"""稳健下载 CBETA xml-p5 单文件：断点续传 + </TEI> 完整性校验。
用法：python fetch.py T30n1579 [T30n1580 ...]
"""
import os, subprocess, sys, time

BASE = 'https://raw.githubusercontent.com/cbeta-org/xml-p5/master/T'
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'xml')

def size(p):
    try:
        return os.path.getsize(p)
    except OSError:
        return 0

def complete(p):
    if size(p) < 1000:
        return False
    with open(p, 'rb') as f:
        f.seek(max(0, size(p) - 64))
        return b'</TEI>' in f.read()

for tid in sys.argv[1:]:
    os.makedirs(OUT, exist_ok=True)
    pre = tid[:3]
    url = '%s/%s/%s.xml' % (BASE, pre, tid)
    path = os.path.join(OUT, tid + '.xml')
    for attempt in range(40):
        if complete(path):
            break
        before = size(path)
        subprocess.run(['curl', '-s', '-L', '--max-time', '240', '-C', '-', url, '-o', path],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        after = size(path)
        print('%s attempt %d: %d -> %d bytes%s' % (tid, attempt + 1, before, after,
              ' (complete)' if complete(path) else ''), flush=True)
        if complete(path):
            break
        if after == before:
            time.sleep(3)
    print('%s FINAL: %d bytes, complete=%s' % (tid, size(path), complete(path)), flush=True)
