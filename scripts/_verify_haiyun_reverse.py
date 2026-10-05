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
DOC = os.path.join(BASE, r'docs\随笔参考\海云继梦法师_复原·重构·建构的修行体系（草稿）.md')
S_EVID = os.path.join(BASE, r'scripts\verify_haiyun_evidence.py')
S_DRAFT = os.path.join(BASE, r'scripts\verify_haiyun_draft.py')

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
    ('台账谎报：meta.counts 之 strong 10→11', 'yml',
     '  counts:\n    strong: 10', '  counts:\n    strong: 11', 'Y'),
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
]

orig_yml = io.open(YML, encoding='utf-8').read()
orig_doc = io.open(DOC, encoding='utf-8').read()


def apply_mutation(src, find, repl):
    if find.startswith('re:'):
        return re.sub(find[3:], repl, src)
    return src.replace(find, repl)


# 前置自检：锚点必存在且变异必真实发生（否则为空操作＝假绿）
bad = []
for desc, tgt, find, repl, _exp in MUTATIONS:
    o = orig_yml if tgt == 'yml' else orig_doc
    m = apply_mutation(o, find, repl)
    if m == o or not m.strip():
        bad.append(desc)
if bad:
    print('!! 锚点不存在或变异为空操作：%s' % bad)
    sys.exit(2)

tmp = tempfile.mkdtemp(prefix='haiyun_rev_')
cp_yml = os.path.join(tmp, 'ev.yaml')
cp_doc = os.path.join(tmp, 'draft.md')
shutil.copy(YML, cp_yml)
shutil.copy(DOC, cp_doc)

env = {**os.environ, 'HAI_EVIDENCE': cp_yml, 'HAI_DRAFT': cp_doc,
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
    o = orig_yml if tgt == 'yml' else orig_doc
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
        io.open(cp_doc, 'w', encoding='utf-8').write(m)
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
