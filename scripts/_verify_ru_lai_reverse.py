# -*- coding: utf-8 -*-
"""_verify_ru_lai_reverse.py —— verify_ru_lai.py 之反向验证（L.116）

原则（L.106 立、L.107 承）：此前必以**破坏性变异**确认各断言真能捕获错误，
否则「全绿」不足为凭。变异施加于**文档副本**（env RU_LAI_DOC），原文档不动。

变异一律以 (锚点, 替换) 对写就，且**前置断言锚点须存在**（否则为空操作、假绿）。
锚点择**非留痕段**之正文，俾不因校勘豁免而误判。
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
GATE = os.path.join(BASE, r'scripts\verify_ru_lai.py')
DOC = os.path.join(BASE, r'docs\经学文献\华严经细读_第二部_如来现相品.md')

MUT = [
    # (描述, 锚点, 替换, 期望捕获之 tag)
    ('旧数回潮：8,119 字／208 句 → 18,472 字／406 句',
     '8,119 字／208 句', '18,472 字／406 句', 'B:18,472'),
    ('范围回潮：本品＝卷第六 → 本品＝卷六～卷七',
     '本品＝卷第六', '本品＝卷六～卷七', 'B:卷六～卷七'),
    ('伪引：篡改 §6.1 八十引文（加字使不源于底本）',
     '能入菩提之妙道', '能入菩提之妙道阿', 'C1'),
    ('假出处：六十底本经号 T09n0278 → T09n9999',
     'T09n0278', 'T09n9999', 'D2'),
    ('契约破坏：本品＝卷第六 → 卷第七',
     '本品＝卷第六', '本品＝卷第七', 'E1'),
    ('记阙抹除：四十华严「不涉本品」→ 另见别处',
     '不涉本品', '另见别处', 'B7'),
    ('记阙抹除：四十华严「惟〈入法界品〉」→ 另為一會',
     '惟〈入法界品〉', '另為一會', 'B7'),
    ('数字脱绑：8,119 字 → 8,119 餘字（A4 单位绑定失效）',
     '8,119 字', '8,119 餘字', 'A4'),
    ('偈颂支分数破坏：132 偈 → 1320 偈',
     '132 偈', '1320 偈', 'E8'),
    ('§5 注疏伪引：T1739「問有三十七問」→ 問有三十八問',
     '問有三十七問', '問有三十八問', 'C2'),
      ('§3 旁参伪引（改经字·觀→瞻）', '坐寶蓮華眾所觀', '坐寶蓮華眾所瞻', 'C3'),
      ('§3 旁参数字脱钩（1,995→1,994）', '1,995 字', '1,994 字', 'E9'),
]


def main():
    orig = open(DOC, encoding='utf-8').read()
    # 前置：每锚点须存在
    for desc, a, b, tag in MUT:
        if a not in orig:
            print('[ERR] 锚点不存在，变异为空：%s' % desc)
            return 2

    tmp = tempfile.mkdtemp(prefix='rulai_rev_')
    env0 = dict(os.environ, RU_LAI_DOC=DOC)
    r0 = subprocess.run([sys.executable, GATE], capture_output=True,
                        encoding='utf-8', errors='replace', env=env0)
    if 'ALL CHECKS PASSED' not in (r0.stdout or ''):
        print('[ERR] 原始门禁未全绿，反向验证无据')
        print((r0.stdout or '')[-800:])
        return 2

    passed = 0
    for desc, a, b, tag in MUT:
        mut = orig.replace(a, b)
        if mut == orig:
            print('[FAIL] %s —— 变异未生效' % desc)
            continue
        p = os.path.join(tmp, 'mut.md')
        open(p, 'w', encoding='utf-8').write(mut)
        env = dict(os.environ, RU_LAI_DOC=p)
        r = subprocess.run([sys.executable, GATE], capture_output=True,
                           encoding='utf-8', errors='replace', env=env)
        caught = (r.returncode != 0) and (tag in (r.stdout or ''))
        if caught:
            passed += 1
            print('[PASS] %s → 捕获 %s' % (desc, tag))
        else:
            print('[FAIL] %s → 期望 %s，实 rc=%d' % (desc, tag, r.returncode))
    shutil.rmtree(tmp, ignore_errors=True)
    print('\n反向验证 %d/%d 如期失败' % (passed, len(MUT)))
    return 0 if passed == len(MUT) else 1


if __name__ == '__main__':
    sys.exit(main())