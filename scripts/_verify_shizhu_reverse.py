# -*- coding: utf-8 -*-
"""verify_shizhu.py 之反向验证（L107）

原则（L106 已立）：门禁若从未失败过，则其「全绿」不足为凭。遂对文档副本作
破坏性变异，确认各项断言**如期失败**。变异施于副本（SHIZHU_DOC 覆盖），原件不动。

**首轮教训（L107 自纠）**：初版把变异写成「若串已存在则原地保留」，致三项变异
成为**空操作**（`mutated = orig`），门禁「未失败」被误读为「门禁有盲区」——
此即 L.106 已记之「假绿由 harness 自伤」。故本版一律用显式 (锚点, 替换) 对：
锚点须确实存在于原文（否则 loudly 报错），替换串必与锚点不同，变异必真实发生。
另：锚点一律取**非校勘段**正文行，否则会被 B 段之校勘豁免规则正当放过（那不是盲区）。
"""
import io
import os
import re
import shutil
import subprocess
import sys
import tempfile

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE = r'C:\DA_Practice\huayan_collection'
SRC = os.path.join(BASE, r'docs\经学文献\华严经细读_第一部_世主妙严品.md')
SCRIPT = os.path.join(BASE, r'scripts\verify_shizhu.py')

ANCHOR = '**天众十二类**'          # 正文非校勘行，稳锚

# (说明, 锚点, 替换, 期望失败的断言标签)
MUTATIONS = [
    ('旧数回潮：欲界七组→欲界六组', '欲界七组', '欲界六组', 'B:欲界六组'),
    ('旧数回潮：注入「四十二位领众」', ANCHOR, '**四十二位领众**\n' + ANCHOR, 'B:四十二位'),
    ('卷次误引回潮：卷二·十二组→卷二十二组', '为卷二·十二组两译同名之少数例', '为卷二十二组两译同名之少数例', 'B:卷二十二组'),
    ('冒称逐字：把转述注改回「引文逐字照录」并置引号内',
     '旧稿于此处引有', '**〔转述·非逐字引文〕**「引文逐字照录」；旧稿于此处引有', 'B5'),
    ('伪引（海云）：注入查无原文之逐字照录引文', ANCHOR,
     '- **海云继梦**法师云「此句实为海云所独有之妙义无有穷尽」，引文逐字照录。\n' + ANCHOR, 'D1'),
    ('伪引（作用域②）：注入无据引文并标逐字照录', ANCHOR,
     '- 某某注云「此系古德所立而今已无人问津之法门」，引文逐字照录。\n' + ANCHOR, 'C2'),
    ('假出处：注入不存在的本地路径', ANCHOR,
     '（见 [某缺失文件](../../../docs/huayanhai/义学专题/经论原典/不存在之底本.txt)）\n' + ANCHOR, 'E1'),
    ('来源系回退：恢复「海云讲记引自袖珍版」之误系',
     '五卷独立文件**（', '讲记引用皆依袖珍版（M4X3），非五卷独立文件（', 'D2'),
    ('正文数字与底本脱钩：自述字数 31,953 字→30,000 字', '31,953 字', '30,000 字', 'A7'),
    ('组数脱钩：抹去 414 名之实数', r're:414(\s*\**\s*名)', r'四百一十四\1名', 'B7'),
]

orig = open(SRC, encoding='utf-8').read()


def apply_mutation(find: str, repl: str) -> str:
    """以 `re:` 前缀者按正则全量替换，否则字面全量替换。
    L107 教训：字面替换常只覆盖部分写法（如 '**414** 名' vs '414 名'），
    致变异不彻底、门禁'未失败'被误读为盲区 —— 故此处一律全量。"""
    if find.startswith('re:'):
        return re.sub(find[3:], repl, orig)
    return orig.replace(find, repl)


# 前置自检：锚点必须存在，否则变异不发生，测试即为空操作（假绿之源）
missing = [d for d, f, r, e in MUTATIONS if not apply_mutation(f, r) or apply_mutation(f, r) == orig]
if missing:
    print('!! 锚点不存在或变异为空操作：%s' % missing)
    sys.exit(2)

tmpdir = tempfile.mkdtemp(prefix='shizhu_rev_')
passed = failed = 0
print('=' * 74)
print('verify_shizhu.py 反向验证 —— 破坏性变异须被捕获')
print('=' * 74)

cp = os.path.join(tmpdir, 'baseline.md')
shutil.copy(SRC, cp)
env = {**os.environ, 'SHIZHU_DOC': cp, 'PYTHONIOENCODING': 'utf-8'}
r = subprocess.run([sys.executable, SCRIPT], capture_output=True, text=True,
                   encoding='utf-8', errors='replace', env=env)
print('[基线] rc=%d %s' % (r.returncode, 'OK' if r.returncode == 0 else '!! 基线竟失败'))
if r.returncode != 0:
    print(r.stdout[-1500:])
    sys.exit(2)
print('-' * 74)

for desc, find, repl, expect in MUTATIONS:
    mutated = apply_mutation(find, repl)
    if mutated == orig:
        print('[FAIL] %-52s → 变异未发生（空操作）' % desc)
        failed += 1
        continue
    cp = os.path.join(tmpdir, 'm.md')
    open(cp, 'w', encoding='utf-8').write(mutated)
    env = {**os.environ, 'SHIZHU_DOC': cp, 'PYTHONIOENCODING': 'utf-8'}
    r = subprocess.run([sys.executable, SCRIPT], capture_output=True, text=True,
                       encoding='utf-8', errors='replace', env=env)
    caught = (r.returncode != 0) and (expect in r.stdout)
    if caught:
        passed += 1
        print('[PASS] %-52s → %s' % (desc, expect))
    else:
        failed += 1
        print('[FAIL] %-52s → 期望 %s，实得 rc=%d' % (desc, expect, r.returncode))
        for l in [x for x in r.stdout.splitlines() if 'FAIL' in x][:3]:
            print('         %s' % l.strip())

print('-' * 74)
print('反向验证 %d/%d 如期失败' % (passed, passed + failed))
shutil.rmtree(tmpdir, ignore_errors=True)
sys.exit(0 if failed == 0 else 1)