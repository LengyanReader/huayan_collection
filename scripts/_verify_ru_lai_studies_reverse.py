#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""_verify_ru_lai_studies_reverse.py — 反向验证：以破坏性变异确认
`verify_ru_lai_studies_render.js` 之各断言真能捕获失败（L106 已立之原则：
「全绿」不足为凭，须证门禁能红）。

对构建产物页面副本与渲染器源副本施加变异，逐例运行门禁并断言其非零退出；
末以未变异之正本断言零退出。用法：python scripts/_verify_ru_lai_studies_reverse.py
"""
import os
import sys
import subprocess
import tempfile

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding='utf-8')
    except Exception:
        pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = os.path.join(ROOT, 'web', 'demo', 'articles', 'ru-lai-xian-xiang.html')
SRC = os.path.join(ROOT, 'web', 'demo', 'src', 'ru_lai_studies.js')
GATE = os.path.join(ROOT, 'scripts', 'verify_ru_lai_studies_render.js')
NODE = 'node'


def run(page, src):
    env = dict(os.environ)
    env['RLS_SRC'] = src
    return subprocess.run([NODE, GATE, page], capture_output=True, text=True,
                          encoding='utf-8', errors='replace', env=env)


def repl(text, old, new, label):
    if old not in text:
        print('  !! 变异锚点缺失：%s —— 反向验证无效（须先修锚点）' % label)
        sys.exit(2)
    return text.replace(old, new, 1)


PAGE_MUT = [
    ('meta.article 脱钩',
     lambda t: repl(t, '"article": "ru-lai-xian-xiang"', '"article": "x"', 'meta.article')),
    ('Burnside 轨道数脱钩',
     lambda t: repl(t, '"num_orbits": 3', '"num_orbits": 4', 'num_orbits')),
    ('过滤 β1 恒等破坏',
     lambda t: repl(t, '"beta1": 0', '"beta1": 5', 'beta1')),
    ('四十问划分破坏',
     lambda t: repl(t, '"group_b_endswith_sea": 20', '"group_b_endswith_sea": 19', 'group_b')),
    ('持久同调单纯形数脱钩',
     lambda t: repl(t, '"n_simplices": 1023', '"n_simplices": 1022', 'n_simplices')),
    ('持久同调最大维脱钩',
     lambda t: repl(t, '"max_dim": 9', '"max_dim": 8', 'max_dim')),
]

SRC_MUT = [
    ('抹去拓扑节 id',
     lambda t: repl(t, 'rls-topology', 'rls-TP', 'rls-topology')),
    ('引入 undefined 泄漏',
     lambda t: repl(t, "'rls-linguistic'", "'rls-linguistic'+undefined", 'rls-linguistic')),
]


def main():
    page0 = open(PAGE, encoding='utf-8').read()
    src0 = open(SRC, encoding='utf-8').read()
    tmp = tempfile.mkdtemp(prefix='rls_rev_')
    fails = 0

    p0 = os.path.join(tmp, 'page_ok.html')
    s0 = os.path.join(tmp, 'src_ok.js')
    open(p0, 'w', encoding='utf-8').write(page0)
    open(s0, 'w', encoding='utf-8').write(src0)
    r = run(p0, s0)
    if r.returncode == 0 and (r.stdout or '').strip():
        print('[ok] 正本（未变异）通过')
    else:
        print('  XX 正本竟未通过：%r' % ((r.stdout or r.stderr)[:200]))
        fails += 1

    total = len(PAGE_MUT) + len(SRC_MUT)
    n = 0
    for label, fn in PAGE_MUT:
        n += 1
        p = os.path.join(tmp, 'page_%d.html' % n)
        open(p, 'w', encoding='utf-8').write(fn(page0))
        r = run(p, s0)
        if r.returncode != 0:
            print('  ok 如期失败：' + label)
        else:
            print('  XX 未捕获：' + label)
            fails += 1

    for label, fn in SRC_MUT:
        n += 1
        s = os.path.join(tmp, 'src_%d.js' % n)
        open(s, 'w', encoding='utf-8').write(fn(src0))
        p = os.path.join(tmp, 'page_s%d.html' % n)
        open(p, 'w', encoding='utf-8').write(page0)
        r = run(p, s)
        if r.returncode != 0:
            print('  ok ->fail: ' + label)
        else:
            print('  XX 未捕获：' + label)
            fails += 1

    print('─' * 60)
    total = len(PAGE_MUT) + len(SRC_MUT)
    if fails:
        print('反向验证失败：%d 项' % fails)
        return 1
    print('反向验证通过：%d/%d 如期失败 + 正本通过' % (total, total))
    return 0


if __name__ == '__main__':
    sys.exit(main())