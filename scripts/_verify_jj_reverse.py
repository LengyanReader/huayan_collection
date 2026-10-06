# -*- coding: utf-8 -*-
"""L.111《九九華嚴》OCR 立册门禁 · 反向验证（职责分离）

〔为何独立成文件〕依 L.106／L.107 之规：**指派「应捕获之门禁」者，
不得同时充当「验证该门禁真能捕获」之执行者**，二者须异文件、异进程。

以八类破坏性变异确认 `verify_jj_lectures.py` 之断言**真能捕获**：
  drop_calibration 摘除「待校定」而无凭据      falsify_number 台账数字与实测脱钩
  break_url        出处链接失效                 admit_t0       OCR 稿被塞进 T0 一手栈
  soften_neg       否定记录之「不可」限定被软化 shout_verified 自我定性改为「已校定」
  drop_ep          逐集条目缺失                 month_drift     元数据月份与实测脱钩

〔防假绿·两道〕① 变异器若为空操作（正则未命中／落点在无关处），须以
  rc=2 明示「变异未生效」，上层即判测试无意义——**不得**计为通过；
  ② 输出为空（locale 解码失败）亦计失败，沿 L.105 之规。
"""
import io
import os
import subprocess
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

HERE = os.path.dirname(os.path.abspath(__file__))
GATE = os.path.join(HERE, "verify_jj_lectures.py")
MUTS = ["drop_calibration", "falsify_number", "break_url", "admit_t0",
        "soften_neg", "shout_verified", "drop_ep", "month_drift"]


def main():
    if not os.path.exists(GATE):
        print("【缺门禁】%s" % GATE)
        return 1
    caught = []
    for m in MUTS:
        p = subprocess.run([sys.executable, GATE, "--mutate", m],
                           capture_output=True, encoding="utf-8",
                           errors="replace")
        out = (p.stdout or "") + (p.stderr or "")
        if not out.strip():
            print("  ✗ %-16s 输出为空（防假绿：计失败）" % m)
            continue
        if p.returncode == 1:
            caught.append(m)
            first = next((l for l in out.splitlines()
                          if l.strip().startswith("✗")), "")
            print("  ✓ %-16s 如期捕获｜%s" % (m, first.strip()[:96]))
        elif p.returncode == 2:
            print("  ✗ %-16s 变异未生效——**变异器自身失效**，此项不算通过"
                  % m)
        else:
            print("  ✗ %-16s 变异后门禁仍通过（rc=%d）——**假绿**" % (m, p.returncode))
    print("反向验证：%d/%d 如期捕获" % (len(caught), len(MUTS)))
    return 0 if len(caught) == len(MUTS) else 1


if __name__ == "__main__":
    sys.exit(main())