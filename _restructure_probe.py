import io, re, os

# 1) jj-huayan-collation.html — check size / marker / not overwritten
p = 'web/demo/articles/jj-huayan-collation.html'
sz = os.path.getsize(p)
t = io.open(p, encoding='utf-8').read()
print(f'jj-huayan-collation.html size={sz:,}B')
print('  contains "Ep 2 tab"?', 'Ep 2' in t or '第2集' in t or 'ep02' in t.lower())
print('  contains "D15–D17"?', 'D15' in t)
print('  contains "21,925"?', '21,925' in t)
print('  build_jj_collation_page signature?', '讲记校勘' in t or 'jj_huayan_collation' in t)

# 2) index.html — check ordering & summary
idx = io.open('web/demo/articles/index.html', encoding='utf-8').read()
print(f'\nindex.html size={len(idx.encode("utf-8")):,}B')

# nav line
nav = re.search(r'<div style="padding:7px[^"]*">(.*?)</div>', idx, re.S)
if nav:
    for m in re.findall(r'#grp-\d"[^>]*>([^<]+)</a>', nav.group()):
        print('  nav:', m)

# group order + count in <section>s
print('\n--- groups ---')
for m in re.finditer(r'<section id="grp-(\d)"[^>]*>.*?>([^<]+?) ([^<]+?)</span>\s*<span[^>]*>(\d+) 篇</span>(.*?)</div>', idx, re.S):
    gi, icon, key, n, rest = m.groups()
    sm = re.search(r'>([^<]+)</div>', rest)
    print(f'  grp-{gi} {icon} {key} ({n}) summary={sm.group(1) if sm else "(none)"}')

# 7 pin order check (in grp-0)
sec0 = re.search(r'<section id="grp-0".*?</section>', idx, re.S)
if sec0:
    hrefs = re.findall(r'href="([a-z\-]+)\.html"', sec0.group())
    print('\ngrp-0 (经论茶歇) card order:', hrefs)

# jj-huayan-collation link present?
print('\nindex links jj-huayan-collation.html?', 'href="jj-huayan-collation.html"' in idx)
