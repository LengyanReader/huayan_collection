#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""_verify_data_science_reverse.py — 反向验证：以破坏性变异确认
`verify_data_science_render.js` 之各断言真能捕获失败（L106 立「全绿不足为凭，须证门禁能红」）。

对两篇文章页（ru-lai-xian-xiang＝十节点全枚举；shizhu-miaoyan＝四十节点限维）之
内嵌 ARTICLE_DS 数据与渲染器源施加变异，逐例运行门禁并断言其非零退出；
末以未变异之正本断言零退出。用法：python scripts/_verify_data_science_reverse.py
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
GATE = os.path.join(ROOT, 'scripts', 'verify_data_science_render.js')
SRC = os.path.join(ROOT, 'web', 'demo', 'src', 'data_science.js')
NODE = 'node'

PAGES = [
    os.path.join(ROOT, 'web', 'demo', 'articles', 'ru-lai-xian-xiang.html'),
    os.path.join(ROOT, 'web', 'demo', 'articles', 'shizhu-miaoyan.html'),
]

# 数据级变异：追加到渲染器源末尾之 JS（在 renderDataScience 定义之后、门禁取值之前执行）。
# 皆加守卫，使两种数据形状（octagon/census；全枚举/限维）皆如期失败。
DATA_MUT = [
    ('meta.article 脱钩', "global.ARTICLE_DS.meta.article='x';"),
    ('Zipf 斜率转正', "global.ARTICLE_DS.linguistic.zipf.slope=1;"),
    ('L2 代数脱钩', ("if(global.ARTICLE_DS.algebra.octagon_symmetry)"
                    "global.ARTICLE_DS.algebra.octagon_symmetry.num_orbits=4;"
                    "else global.ARTICLE_DS.algebra.census=[{title_zh:'x',rows:[]}];")),
    ('过滤 β1 恒等破坏', "global.ARTICLE_DS.topology.filtration.steps[0].beta1+=1;"),
    ('旗复形 t=1 β1 破坏', "global.ARTICLE_DS.topology.flag_complex.at_t1.beta1+=1;"),
    ('t=1 边密度脱钩', "global.ARTICLE_DS.topology.graph.density_t1=0.123;"),
    ('L4 单纯形数脱钩', "global.ARTICLE_DS.geometry.n_simplices=Math.pow(2,global.ARTICLE_DS.topology.graph.nodes);"),
    ('L4 H0 本质类脱钩', "global.ARTICLE_DS.geometry.essential.H0=[];"),
    ('L4 最大维脱钩', "global.ARTICLE_DS.geometry.max_dim=999;"),
    ('Betti 曲线末行 β0 破坏',
     "var _cv=global.ARTICLE_DS.geometry.betti_curve;_cv[_cv.length-1].beta0=3;"),
    ('谱和脱钩（Σλ ≠ 2m）', "global.ARTICLE_DS.geometry.spectral.sum_eigen_equals_2m+=1;"),
    ('谱零特征值数脱钩', "global.ARTICLE_DS.geometry.spectral.n_zero_eigen+=1;"),
    ('Fiedler 二分不覆盖全节点',
     "global.ARTICLE_DS.geometry.spectral.fiedler.id_pos=[];global.ARTICLE_DS.geometry.spectral.fiedler.id_neg=[];"),
]

# 渲染器源级变异：文本替换。
SRC_MUT = [
    ('抹去拓扑节 id', lambda t: repl(t, "'ds-topology'", "'ds-TP'", 'ds-topology')),
    ('抹去几何节 id', lambda t: repl(t, "'ds-geometry'", "'ds-GE'", 'ds-geometry')),
    ('引入 undefined 泄漏', lambda t: repl(t, "'ds-linguistic'", "'ds-linguistic'+undefined", 'ds-linguistic')),
]


def repl(text, old, new, label):
    if old not in text:
        print('  !! 变异锚点缺失：%s —— 反向验证无效（须先修锚点）' % label)
        sys.exit(2)
    return text.replace(old, new, 1)


def run(page, src):
    env = dict(os.environ)
    env['DS_SRC'] = src
    return subprocess.run([NODE, GATE, page], capture_output=True, text=True,
                          encoding='utf-8', errors='replace', env=env)


def main():
    tmp = tempfile.mkdtemp(prefix='ds_rev_')
    src0 = open(SRC, encoding='utf-8').read()
    fails = 0
    total = 0
    n = 0

    for page in PAGES:
        tag = os.path.basename(page)
        page0 = open(page, encoding='utf-8').read()
        p = os.path.join(tmp, tag)
        open(p, 'w', encoding='utf-8').write(page0)
        s0 = os.path.join(tmp, 'src_ok_%s.js' % tag)
        open(s0, 'w', encoding='utf-8').write(src0)

        total += 1
        r = run(p, s0)
        if r.returncode == 0 and (r.stdout or '').strip():
            print('[ok] %s 正本（未变异）通过' % tag)
        else:
            print('  XX %s 正本竟未通过：%r' % (tag, (r.stdout or r.stderr)[:200]))
            fails += 1

        for label, js in DATA_MUT:
            total += 1
            n += 1
            s = os.path.join(tmp, 'src_d%03d.js' % n)
            open(s, 'w', encoding='utf-8').write(src0 + '\n' + js + '\n')
            r = run(p, s)
            if r.returncode != 0:
                print('  ok 如期失败 [%s]：%s' % (tag, label))
            else:
                print('  XX 未捕获 [%s]：%s' % (tag, label))
                fails += 1

        for label, fn in SRC_MUT:
            total += 1
            n += 1
            s = os.path.join(tmp, 'src_s%03d.js' % n)
            open(s, 'w', encoding='utf-8').write(fn(src0))
            r = run(p, s)
            if r.returncode != 0:
                print('  ok 如期失败 [%s]：%s' % (tag, label))
            else:
                print('  XX 未捕获 [%s]：%s' % (tag, label))
                fails += 1

    print('─' * 60)
    if fails:
        print('反向验证失败：%d 项（共 %d）' % (fails, total))
        return 1
    print('反向验证通过：%d/%d 如期失败 + 两正本通过' % (total - 2, total - 2))
    return 0


if __name__ == '__main__':
    sys.exit(main())