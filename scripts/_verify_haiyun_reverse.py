# -*- coding: utf-8 -*-
"""海云实证库两道门禁之反向验证（L109）

原则（L106 已立、L107 沿用）：门禁若从未失败过，则其「全绿」不足为凭。
遂以破坏性变异确认各项断言**如期失败**。

**变异施于副本**：实证库以 HAI_EVIDENCE 覆盖，草稿以 HAI_DRAFT 覆盖，原件不动。

**本轮自纠两处（L107 教训之沿用）**：
1. 一律用显式 (锚点, 替换) 对，且前置断言锚点必存在、变异必真实发生，
   否则「变异未发生」会被误读为「门禁有盲区」（假绿由 harness 自伤）。
2. `escape_t0` 类变异须改**实证库**而非草稿——若改草稿则正文引号仍合法，
   门禁抓不到，故须改被引之库（这正是该项之真正风险面）。
"""
import io
import os
import re
import shutil
import subprocess
import sys
import tempfile

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE = r'C:\DA_Practice\huayan_collection'
YML = os.path.join(BASE, r'data\research\haiyun_practice_system_evidence.yaml')
DOC = os.path.join(BASE, r'docs\随笔参考\海云继梦法师_复原·重构·建构的修行体系.md')
S_EVID = os.path.join(BASE, r'scripts\verify_haiyun_evidence.py')
S_DRAFT = os.path.join(BASE, r'scripts\verify_haiyun_draft.py')
T1 = os.path.join(BASE, r'data\research\t1_bikan_evidence.yaml')

# (说明, 目标[yml|doc], 锚点, 替换[可 re: 前缀], 期望失败的断言标签)
MUTATIONS = [
    # ── 实证库门禁：引文、行号、条目、来源系 ──────────────────
    ('伪引（改一字即使引文失真）', 'yml',
     '失传了、绝种了，怎么又把它接回来', '失传了、绝种了，怎么就把它接回来',
     'C'),
    ('行号脱钩：S10 行 1114→1115', 'yml', 'line: 1114', 'line: 1115', 'C'),
    ('来源系脱钩：S10 底本路径改向无关讲记', 'yml',
     '普贤心经/听录-普贤心经/初稿/《普贤心经》讲记（全）_1.txt',
     '普贤心经/听录-普贤心经/初稿/《普贤心经》讲记（06）_1.txt', 'C'),
    ('条目缺失：删去 N3（否定性记录）', 'yml',
     '  - id: N3\n', '', 'Y'),
    ('条目缺失：删去 L4（第二层警戒）', 'yml', '  - id: L4\n', '', 'Y'),
    ('条目 id 重号：S5 之 id 改为 S4（两处同号）', 'yml',
     '  - id: S5\n', '  - id: S4\n', 'Y'),
    # **不得写死计数**：本条曾写死「strong 10」，及 strong 增至 14 之期
    # 锚点失效、变异退化为空操作（前置自检以 rc=2 拦下，未假绿）。
    # 故改用正则匹配 `\d+`，使计数增减皆不必回改本脚本。
    ('台账谎报：meta.counts 之 strong 谎报为 999', 'yml',
     r're:  counts:\n    strong: \d+', '  counts:\n    strong: 999', 'Y'),
    ('来源系伪标（真改值）：L4 信度 A→C', 'yml',
     '    信度: A\n    status: 已回源\n\n  - id: L3',
     '    信度: C\n    status: 已回源\n\n  - id: L3', 'E'),

    # ── 草稿门禁：编号失联、伪断言回潮、临摩 ──────────────────
    ('编号失联：正文引用不存在的 S99', 'doc',
     '〔实证库 S9〕', '〔实证库 S99〕', 'A'),
    ('伪断言回潮：重提「137 条」', 'doc',
     '### 8.3 已撤回之断言（如实记录，不隐己过）',
     '### 8.3 已撤回之断言（如实记录，不隐己过）\n\n全库抽词共检出 137 条组织性用语候选。', 'E'),
    ('伪占位回潮：引文标「待补入实证库」', 'doc',
     '〔实证库 S9 同段〕', '〔待补入实证库〕', 'E'),

    # ── L.112「三分两用」组：自述义 vs 分析义（rules.md §J5）─────────
    # 以下五条针对 L.112 新立之核心断言，须能如期被门禁拦下。
    ('伪引：S15 法界原型一段改一字', 'yml',
     '这些包罗万象的法界原型，即是今日华严行者的本色与应尽的责任',
     '这些包罗万象的法界原型，即是今日华严行者的本色与应尽的义务', 'C'),
    ('行号脱钩：S17 一脉相承 85→86', 'yml', 'line: 85', 'line: 86', 'C'),
    ('伪断言回潮：删「复原〔未见其语〕」之分标', 'doc',
     '全库 39 处「复原」皆为生理义',
     '全库 39 处「复原」皆为复原本意之用', 'H'),
    ('代拟其语：把「兼容古今」写成其原词', 'doc',
     '〔核〕**「兼容古今」全库 0 命中**，非其原词；其义在 S15 之「承先……启后」。',
     '〔核〕法师以「兼容古今」一语自陈其志；其义在 S15 之「承先……启后」。', 'H'),
    # **本条首轮假绿，已更正**：替换串原写作两段中文之**隐式拼接**，
    # 而拼接处并无 `\n`，致实为「同一行内替换」——该行下文仍含「撤回」二字，
    # H2 遂予豁免，变异**形式上生效而实质未触及断言**（rc=0）。
    # 故此处**必须显式写 `\n`**，令其成为真正的新增行，H2 方能生效。
    ('撤回之断言回潮：重提「建构为最弱一档·仅在无复原/重构依据时才考虑」',
     'doc',
     '〔重要·自我修正〕**本文初版将「建构」定为最弱一档',
     '**建构**为最弱一档，仅在无复原/重构依据时才考虑。\n'
     '〔注〕〔重要·自我修正〕**本文初版将「建构」定为最弱一档', 'H'),

    # ── L.113「两库编号相撞 + T1 库结构破损」组 ──────────────────────
    # 立此组之缘由（本轮实测所得之假绿，非预防性设防）：
    # ① T1 库之 `quotes:` 键**整段缺失**，`- id:` 直接顶在 `meta` 之下，
    #    全库不可解析；而门禁按**纯文本**读取，故该破损**未被拦截**。
    # ② T1 库否定记录原用 N5–N8，与 T0 库之 N1–N7 **三号相撞**；门禁
    #    「只验〔〕内 N 号是否见于 T1 库」之逻辑，使**误引 T0 之 N7
    #    为 T1 之 N7 亦得通过**——本轮 §5.4 之「〔T1 否定记录 N7〕」
    #    （实为 T0 记录）正是这样通过的。
    ('T1 库结构破损：抹去 quotes: 键', 't1',
     'quotes:\n  - id: C01', '  - id: C01', 'F0'),
    ('两库编号相撞：T1 库否定记录复名为 N5', 't1',
     '  - id: T1N1\n', '  - id: N5\n', 'F1'),
    ('引文歧义：以无库名前缀之〔N7〕引 T1 记录', 'doc',
     '〔T0 否定记录 N7〕。', '〔N7〕。', 'F2'),
    ('引文歧义：以无库名前缀之〔N6〕引 T0 记录', 'doc',
     '与 N5「未据含『原』字而纳入」同理',
     '与〔N6〕「未据含『原』字而纳入」同理', 'F2'),

    # ── L.115「附录目录有目必有文」组（check I）──────────────────────
    # 立此组之缘由：本文原目录列附录一／三／四／五，而正文只有附录二与附录七，
    # **四项皆从未成文**，且 §1.2 表一另有「详见附录一」之悬空交叉引用——
    # 门禁先前只验编号与伪断言，**目录这一层无人看**。两条分别验：
    # ① 目录虚列（承诺了而正文无）② 正文标题被撤（兑现物消失）。
    # （expect 用 'I 目录列' 而非单字 'I'——单字 I 在任意输出中过易命中，
    #   会把「被捕获」与「凑巧出现」混为一谈。）
    ('有目无文：目录虚列不存在的「附录九」', 'doc',
     '- **附录五**：祖典比勘要点表（自 T1 比勘库生成）\n',
     '- **附录五**：祖典比勘要点表（自 T1 比勘库生成）\n'
     '- **附录九**：并不存在之附录\n', 'I 目录列'),
    ('有目无文：正文「附录五」标题被撤', 'doc',
     '## 附录五：祖典比勘要点表', '## 附五：祖典比勘要点表',
     'I 目录列'),
]

orig_yml = io.open(YML, encoding='utf-8').read()
orig_doc = io.open(DOC, encoding='utf-8').read()
orig_t1 = io.open(T1, encoding='utf-8').read()


def apply_mutation(src, find, repl):
    if find.startswith('re:'):
        return re.sub(find[3:], repl, src)
    return src.replace(find, repl)


# 前置自检：锚点必存在且变异必真实发生（否则为空操作＝假绿）
bad = []
for desc, tgt, find, repl, _exp in MUTATIONS:
    o = {'yml': orig_yml, 'doc': orig_doc, 't1': orig_t1}[tgt]
    m = apply_mutation(o, find, repl)
    if m == o or not m.strip():
        bad.append(desc)
if bad:
    print('!! 锚点不存在或变异为空操作：%s' % bad)
    sys.exit(2)

tmp = tempfile.mkdtemp(prefix='haiyun_rev_')
cp_yml = os.path.join(tmp, 'ev.yaml')
cp_doc = os.path.join(tmp, 'draft.md')
cp_t1 = os.path.join(tmp, 't1.yaml')
shutil.copy(YML, cp_yml)
shutil.copy(DOC, cp_doc)

env = {**os.environ, 'HAI_EVIDENCE': cp_yml, 'HAI_DRAFT': cp_doc, 'HAI_T1': cp_t1,
       'PYTHONIOENCODING': 'utf-8'}
passed = failed = 0
print('=' * 74)
print('海云实证库门禁 反向验证 —— 破坏性变异须被捕获')
print('=' * 74)


def run(script):
    r = subprocess.run([sys.executable, script], capture_output=True, text=True,
                       encoding='utf-8', errors='replace', env=env)
    return r.returncode, (r.stdout or '')


rc, out = run(S_EVID)
print('[基线·evidence] rc=%d %s' % (rc, 'OK' if rc == 0 else '!! 基线竟失败'))
if rc != 0:
    print(out[-1200:])
    sys.exit(2)
rc, out = run(S_DRAFT)
print('[基线·draft]    rc=%d %s' % (rc, 'OK' if rc == 0 else '!! 基线竟失败'))
if rc != 0:
    print(out[-1200:])
    sys.exit(2)
print('-' * 74)

for desc, tgt, find, repl, expect in MUTATIONS:
    o = {'yml': orig_yml, 'doc': orig_doc, 't1': orig_t1}[tgt]
    m = apply_mutation(o, find, repl)
    if m == o:
        print('[FAIL] %-46s → 变异未发生（空操作）' % desc)
        failed += 1
        continue
    if tgt == 'yml':
        io.open(cp_yml, 'w', encoding='utf-8').write(m)
        shutil.copy(DOC, cp_doc)
        script = S_EVID
    else:
        shutil.copy(YML, cp_yml)
        shutil.copy(T1, cp_t1)
        io.open(cp_doc, 'w', encoding='utf-8').write(m)
        script = S_DRAFT
    if tgt == 't1':
        shutil.copy(YML, cp_yml)
        shutil.copy(DOC, cp_doc)
        io.open(cp_t1, 'w', encoding='utf-8').write(m)
        script = S_DRAFT
    rc, out = run(script)
    caught = (rc != 0) and (expect in out)
    if caught:
        passed += 1
        print('[PASS] %-46s → %s' % (desc, expect))
    else:
        failed += 1
        print('[FAIL] %-46s → 期望 %s，实得 rc=%d' % (desc, expect, rc))
        for l in [x for x in out.splitlines() if 'FAIL' in x][:3]:
            print('         %s' % l.strip())

print('-' * 74)
print('反向验证 %d/%d 如期失败' % (passed, passed + failed))
shutil.rmtree(tmp, ignore_errors=True)
sys.exit(0 if failed == 0 else 1)
