#!/usr/bin/env python3
# scratch: load canonical ARTICLE_ASSEMBLY from built article HTML; print schema.
import re, io, sys, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
base = r'c:\DA_Practice\huayan_collection'
s = open(base + r'\web\demo\articles\shizhu-miaoyan.html', encoding='utf-8').read()
m = re.search(r'ARTICLE_ASSEMBLY\s*=\s*', s)
i = s.index('{', m.end())
# brace-match (string-aware) to capture full object
depth = 0; instr = False; esc = False; end = None
for j in range(i, len(s)):
    c = s[j]
    if esc: esc = False; continue
    if c == '\\': esc = True; continue
    if c == '"': instr = not instr; continue
    if instr: continue
    if c == '{': depth += 1
    elif c == '}':
        depth -= 1
        if depth == 0: end = j + 1; break
obj = json.loads(s[i:end])
cls = obj['classes']
print('classes:', len(cls), '| top keys:', list(obj.keys()))
print('per-class keys:', list(cls[0].keys()))
print('\n-- class[0] --')
for k, v in cls[0].items():
    sv = str(v)
    print('  %-14s %s' % (k, sv[:120]))
print('\n-- all classes: cat / group / realm / count_expr / leader / n_named --')
tot = 0
for c in cls:
    nn = c.get('n_named') or 0
    tot += nn
    print('  [%2d] %-10s %-12s %-8s %-16s lead=%-12s n=%s' % (
        c.get('idx'), c.get('cat',''), c.get('group',''), c.get('realm','')[:8],
        c.get('count_expr',''), c.get('leader','')[:10], nn))
print('sum n_named =', tot)
json.dump(obj, open(base + r'\scripts\_assembly.json', 'w', encoding='utf-8'), ensure_ascii=False)
print('dumped scripts/_assembly.json')
