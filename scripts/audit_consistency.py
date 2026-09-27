#!/usr/bin/env python3
"""
audit_consistency.py — P1-3 · 全站一致性审计 v1（报告模式 · 不删改）

两条轴，都直接服务内容【准确度】：
  A. 〔待核〕台账——全库待核对标记按文件清点（欠账可视化·配合"随时间不断更新进化"）
  B. CBETA 号审计（T卷n号）：
     B1 格式异常：卷号越出大正藏全藏 1–86（正编55+续诸宗部+史传部+补编）/ 编号非 4 位 / 书写风格不统一
     B2 配对候选冲突：同一 sigla 挂多个《经名》、同一《经名》挂多个 sigla
        （仅列候选——多名同号可能合法，如《华严经》有 60/80 卷别本；裁决须回一手源）

用法：
  python scripts/audit_consistency.py            # 人读报告
  python scripts/audit_consistency.py --json     # 机读
  python scripts/audit_consistency.py --glob "docs/汉传佛教/*.md"
退出码恒 0（报告模式）；纳入闸口与否由 make verify-data 决定。
"""
import argparse
import io
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SIGLA = re.compile(r"T(\d{1,3})n(\d{3,4})")          # 含非标准位数变体
TITLE_NEAR = re.compile(r"《([^》]{1,24})》[^《》]{0,12}?$", re.M)
PENDING = re.compile(r"〔待核〕|【待核】|\[待核\]")
SCAN_DEFAULT = ["docs/*.md", "docs/**/*.md", "web/demo/articles/*.md"]


def scan_files(globs):
    seen, out = set(), []
    for g in globs:
        for p in ROOT.glob(g):
            if p.is_file() and p not in seen and "node_modules" not in str(p):
                seen.add(p)
                out.append(p)
    return sorted(out)


def pending_ledger(files):
    led = {}
    for p in files:
        try:
            n = len(PENDING.findall(p.read_text(encoding="utf-8", errors="replace")))
        except OSError:
            n = 0
        if n:
            led[_rel(p)] = n
    return led


def _rel(p):
    return str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else str(p)


def cbeta_audit(files):
    sigla_titles = defaultdict(lambda: defaultdict(int))   # sigla -> {title: 次数}
    title_siglas = defaultdict(lambda: defaultdict(int))
    fmt_issues = []                                        # (file,line,sigla,问题)
    total = 0
    for p in files:
        rel = _rel(p)
        for lineno, line in enumerate(
                p.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            for m in SIGLA.finditer(line):
                total += 1
                vol, no = int(m.group(1)), m.group(2)
                sig = f"T{vol:02d}n{no}"
                if not (1 <= vol <= 86):
                    # 大正藏合法卷次：正编 1–55 · 续诸宗部 56–62 · 史传部 63–84 · 补编 85–86
                    fmt_issues.append((rel, lineno, sig, "卷号越出大正藏全藏 1–86"))
                if len(no) != 4:
                    fmt_issues.append((rel, lineno, sig, f"编号非 4 位: {no}"))
                if m.group(1) != f"{vol:02d}":
                    fmt_issues.append((rel, lineno, sig, "卷号未补零(书写风格不统一)"))
                # sigla 前文最近的《经名》（窗口 40 字符）
                ctx = line[max(0, m.start() - 40):m.start()]
                tm = None
                for tm in TITLE_NEAR.finditer(ctx):
                    pass
                if tm:
                    sigla_titles[sig][tm.group(1)] += 1
                    title_siglas[tm.group(1)][sig] += 1
    conflicts = {
        "same_sigla_multi_titles": {k: dict(v) for k, v in sigla_titles.items() if len(v) > 1},
        "same_title_multi_siglas": {k: dict(v) for k, v in title_siglas.items() if len(v) > 1},
    }
    return total, fmt_issues, conflicts


def main(argv=None):
    ap = argparse.ArgumentParser(description="全站一致性审计（报告模式）")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--glob", action="append", help="覆盖扫描范围(可多次)")
    a = ap.parse_args(argv)
    files = scan_files(a.glob or SCAN_DEFAULT)

    led = pending_ledger(files)
    total, fmt, conf = cbeta_audit(files)

    if a.json:
        print(json.dumps({"files_scanned": len(files), "pending_ledger": led,
                          "cbeta_total": total, "cbeta_format_issues": fmt,
                          "cbeta_conflicts": conf}, ensure_ascii=False))
        return 0

    print(f"=== 一致性审计 v1 · {len(files)} 文件 ===")
    print(f"\n[A] 〔待核〕台账 · 合计 {sum(led.values())} 处 / {len(led)} 文件")
    for f, n in sorted(led.items(), key=lambda kv: -kv[1]):
        print(f"  {n:4}  {f}")
    print(f"\n[B] CBETA 号 · 出现 {total} 次")
    print(f"  [B1] 格式异常 {len(fmt)} 处")
    for rel, ln, sig, why in fmt[:20]:
        print(f"    {rel}:L{ln} {sig} — {why}")
    if len(fmt) > 20:
        print(f"    …余 {len(fmt)-20} 处（--json 全量）")
    c1, c2 = conf["same_sigla_multi_titles"], conf["same_title_multi_siglas"]
    print(f"  [B2] 一号多名(候选) {len(c1)} · 一名多号(候选) {len(c2)}")
    for sig, ts in list(c1.items())[:10]:
        print(f"    {sig} ← {ts}")
    for t, ss in list(c2.items())[:10]:
        print(f"    《{t}》 → {ss}")
    print("\n注：候选≠错误·多号同名可能合法(别本/异译)；裁决须回 CBETA 一手源(宁缺不伪)。")
    return 0


if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.exit(main())
