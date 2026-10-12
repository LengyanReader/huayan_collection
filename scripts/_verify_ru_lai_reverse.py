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
    ('偈数回旧误数并回潮：卷六合计 140 偈 → 132 偈',
     '卷六偈颂合计 **140 偈**', '卷六偈颂合计 **132 偈**', 'B:132 偈'),
    ('§5 注疏伪引：T1739「問有三十七問」→ 問有三十八問',
     '問有三十七問', '問有三十八問', 'C2'),
      ('§3 旁参伪引（改经字·觀→瞻）', '坐寶蓮華眾所觀', '坐寶蓮華眾所瞻', 'C3'),
      ('§3 旁参数字脱钩（1,995→1,994）', '1,995 字', '1,994 字', 'E9'),
      # ── L.122 续补 F 段 ──────────────────────────────────────────────
      ('§1.1 回退〔待续〕占位', '如來是能現之人', '如來是能現之人〔待续〕', 'F1'),
      ('§6.1 〇′ 十光名错字（寶幢照→寶幢光照）', '寶幢照光明', '寶幢光照光明', 'F5'),
      ('§6.2 藏译对应品抹去（de bzhin gshegs pa）',
       'de bzhin gshegs pa', 'de bzhin gshegs p', 'F9'),
      ('§6.4 藏名形破坏（rmad ga cad→rmad gacad）',
       'rmad ga cad', 'rmad gacad', 'F11'),
      ('§7.4 数据文件抹去（ru_lai_studies.yaml）',
       'ru_lai_studies.yaml', 'ru_lai_studies_X.yaml', 'F12'),
      ('§7.4 回退旧记（已落→未做）', '本品数据层已落', '本品数据层未做', 'F13'),
    # ── G L.124 附录契约（附录内容／旧数销项）──────────────────────────
    ('附录一 全经数破坏：551 → 552', '**551** 见', '**552** 见', 'G11'),
    ('附录二 十方名相抹除：清淨光蓮華莊嚴 → 截尾（非子串变异）',
     '清淨光蓮華莊嚴', '清淨光蓮華', 'G13'),
    ('附录三 十光名破坏：眾寶華遍照光明 → 截尾（非子串变异）',
     '眾寶華遍照光明', '眾寶華遍照', 'G14'),
    ('附录九 三级破坏：A1 经证 → A壹', '**A1 经证**', '**A壹 经证**', 'G16'),
    ('附录十一 四视角破坏：Burnside → Bernside（非子串变异）',
     'Burnside', 'Bernside', 'G17'),
    ('§7.2 旧数回潮：承佛威神 9 → 8', '「承佛威神」**9** 见', '「承佛威神」8 见', 'G18'),
    ('§5.4.3 交叉引用回潮：见 §2.1 → 见 §7 待补',
     '见 **§2.1**', '见 §7 待补', 'G20'),
    # ── H L.125 §2.7 逐颂细读（引文回源／偈数／勘误）────────────────────
    ('§2.7 伪引：前①颂末偈加字（永出思議眾度海→…阿）',
     '永出思議眾度海', '永出思議眾度海阿', 'H1'),
    ('§2.7 伪引：末组加字（不得其邊際→不得其邊際阿）',
     '不得其邊際', '不得其邊際阿', 'H1'),
    ('§2.7 偈数回潮：140 偈 → 132 偈（旧误数）', '140 偈', '132 偈', 'E8'),
    ('§2.7 组数抹除：第 14 组小节标题破坏（2.7.14→2.7.14x）',
     '#### 2.7.14 ', '#### 2.7.14x ', 'H2'),
    ('§2.7 前①勘误抹除：40 句＝10 偈 → 40 句＝2 偈',
     '40 句＝10 偈', '40 句＝2 偈', 'H4'),
    ('§八 附录目录标题失一致：附录七（本品骨架）→（光明网络意向图）',
     '- 附录七：结构可视化（本品骨架）',
     '- 附录七：结构可视化（光明网络意向图）', 'G21'),
    # ── I §6.5 六十全量逐段对照（引文回源／十方表／契约串）──────────────
    ('§6.5 伪引：八十结通加字（而來集會→而來集會阿）',
     '十方各有一億世界海微塵數諸菩薩眾而來集會',
     '十方各有一億世界海微塵數諸菩薩眾而來集會阿', 'I2'),
    ('§6.5 伪引：六十勝音颂加字（佛故处此菩提树→…阿）',
     '佛故处此菩提树', '佛故处此菩提树阿', 'I2'),
    ('§6.5 十方表破坏：六十東世界海截尾（淨蓮華勝光莊嚴→淨蓮華勝光）',
     '淨蓮華勝光莊嚴', '淨蓮華勝光', 'I4'),
    ('§6.5 十方表破坏：六十上世界海截尾（雜寶光海莊嚴→雜寶光海）',
     '雜寶光海莊嚴', '雜寶光海', 'I4'),
    ('§6.5 契约串破坏：说颂者 11→1 → 11→2', '11→1', '11→2', 'I5'),
    ('§6.5 契约串破坏：念请问目 40→25 → 40→24', '40→25', '40→24', 'I6'),
    ('§6.5 契约串破坏：勝音「3 偈」→「4 偈」', '3 偈', '4 偈', 'I7'),
    ('§6.5 底本经号抹除：T10n0279 → T10n0000（I8 契约）',
     'T10n0279', 'T10n0000', 'I8'),
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