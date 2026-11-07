# -*- coding: utf-8 -*-
"""注册表 updated_at 同步（常驻工具·L.370 固化）——向文章最新批日期对齐"""
import io, re, sys, os
sys.stdout.reconfigure(encoding='utf-8')
regp = 'data/translation/standalone_articles.yaml'
TODAY = max(re.findall(r'(20\d\d-\d\d-\d\d)', io.open('tasks/PROGRESS.md', encoding='utf-8').read()))
reg = io.open(regp, encoding='utf-8').read()
entries = list(re.finditer(r'- id: ([^\n]+)\n((?:  [^\n]*\n)+)', reg))
bumped = 0
out = []
last = 0
for m in entries:
    bid, body = m.group(1), m.group(2)
    dm = re.search(r'  doc: ([^\n]+)\n', body)
    um = re.search(r"  updated_at: '?([^'\n]+)'?\n", body)
    if dm and um:
        docp = dm.group(1).strip()
        if os.path.exists(docp):
            at = io.open(docp, encoding='utf-8').read()
            dates = [d for d in re.findall(r'(20\d\d-\d\d-\d\d)', at)]
            dmax = max(dates) if dates else None
            if dmax and dmax > um.group(1).strip() and dmax <= TODAY:
                body = body.replace(um.group(0), "  updated_at: '%s'\n" % dmax, 1)
                bumped += 1
    out.append(reg[last:m.start()] + '- id: ' + bid + '\n' + body)
    last = m.end()
out.append(reg[last:])
io.open(regp, 'w', encoding='utf-8', newline='').write(''.join(out))
print('updated_at 同步:', bumped, '条')
