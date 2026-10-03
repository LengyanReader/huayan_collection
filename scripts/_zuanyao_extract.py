# -*- coding: utf-8 -*-
"""_zuanyao_extract.py — 从《华严经疏论纂要》(道霈 B0002) epub 复现清洗文本 + 世主妙严品分科扫描。

产物 (均落 scripts/, 与 cbeta_txt/ 一手原典分列, 不接入 _roll_verify 的 SRC):
  scripts/_zuanyao_flat.txt   全书扁平化繁体纯文本 (去标签/去空, ~205万字)
  scripts/_zuanyao_fenke_scan.txt  世主妙严品 卷次+道霈○科段 定位表

用法: python scripts/_zuanyao_extract.py
依赖: 本机 C:\\华严\\经典著作\\*纂要*.epub (z-lib, 非权威本; 权威本见 CBETA mobi/pdf)
"""
import re
import os
import glob
import zipfile

BASE = r'c:\DA_Practice\huayan_collection'
EPUB_GLOB = r'C:\华严\经典著作\*纂要*.epub'
FLAT_OUT = os.path.join(BASE, 'scripts', '_zuanyao_flat.txt')
SCAN_OUT = os.path.join(BASE, 'scripts', '_zuanyao_fenke_scan.txt')


def find_epub():
    ps = glob.glob(EPUB_GLOB)
    if not ps:
        raise SystemExit('未找到纂要 epub: %s' % EPUB_GLOB)
    return ps[0]


def strip_html(h):
    h = re.sub(r'(?is)<(script|style).*?</\1>', '', h)
    h = re.sub(r'(?is)<br\s*/?>', '\n', h)
    h = re.sub(r'(?is)</p>', '\n', h)
    h = re.sub(r'(?s)<[^>]+>', '', h)
    h = h.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
    h = re.sub(r'[ \t\u3000]+', '', h)
    return re.sub(r'\n\s*\n+', '\n', h).strip()


def flatten(epub):
    z = zipfile.ZipFile(epub)
    names = [n for n in z.namelist() if re.search(r'/\d{3}\.xhtml$', n)]
    names.sort(key=lambda n: int(re.search(r'(\d{3})\.xhtml$', n).group(1)))
    buf = []
    for n in names:
        buf.append('\n===FILE %s===\n' % os.path.basename(n) + strip_html(z.read(n).decode('utf-8', 'ignore')))
    return ''.join(buf)


def scan_pin(txt):
    """世主妙严品 卷次 + 道霈○科段。"""
    out = []
    start = txt.find('世主妙嚴品第一')
    end = txt.find('如來現相品疏論纂要', start)
    seg = txt[start:end if end > 0 else start + 400000]
    out.append('品段长度 %d\n' % len(seg))
    vols = [(m.start(), m.group(1)) for m in re.finditer(r'大方廣佛華嚴經疏論纂要卷第([一二三四五六七八九十]+)', seg)]

    def vol_of(pos):
        v = '?'
        for p, name in vols:
            if p <= pos:
                v = name
            else:
                break
        return v
    out.append('卷次 %s\n\n' % (vols,))
    for m in re.finditer(r'○', seg):
        p = m.start()
        out.append('[卷%s @%d] %s\n' % (vol_of(p), p, seg[p:p + 44].split('\n')[0]))
    return ''.join(out)


if __name__ == '__main__':
    epub = find_epub()
    flat = flatten(epub)
    open(FLAT_OUT, 'w', encoding='utf-8').write(flat)
    open(SCAN_OUT, 'w', encoding='utf-8').write(scan_pin(flat))
    print('wrote', FLAT_OUT, len(flat), 'chars')
