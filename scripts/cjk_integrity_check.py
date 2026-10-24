# -*- coding: utf-8 -*-
# CJK 实体完整性闸 · 防"手写字面 CJK 时误用近似字/错码点"（犍↔隶、等↔友 一类静默替换）。
# 背景：编辑工具参数里用 \uXXXX 手敲码点极易把低频汉字写成另一合法汉字，无报错、只错字。
# 用法：python scripts/cjk_integrity_check.py [文件/目录 ...]（缺省=本次受影响的随笔与源文件）
# 红线：只观察/报告（M0.4），绝不改写任何实质内容；命中禁串即判失败并退码 1。
import sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# 已知"近似字/易错码点"误替——命中即错。带具体上下文以免误伤合法用字（如"直隶/隶属/隶书"）。
BAD = [
    "永远的隶陀罗",   # 应为 犍(U+728D)，误作 隶(U+96B6)
    "[关书朋友",       # 应为 等(U+7B49)，误作 友(U+53CB)
    "关书朋友2026]",
]
# 规范实体串——出现次数仅计数供人工核对（观察，不判错）。
CANON = ["永远的犍陀罗", "关书朋等", "梁晨2026", "犍陀罗·史料库", "犍陀罗·工具链"]

DEFAULT = [Path("docs/随笔参考"), Path("docs/hy_refs/wechat"),
           Path("scripts/fetch_wechat_articles.py")]


def iter_files(args):
    roots = [Path(a) for a in args] or DEFAULT
    self_name = Path(__file__).name
    for r in roots:
        if r.is_dir():
            yield from (p for p in r.rglob("*")
                        if p.is_file() and p.suffix in (".md", ".py", ".html")
                        and p.name != self_name)   # 跳过自身（内含禁串字面量）
        elif r.is_file() and r.name != self_name:
            yield r


fails, report = [], []
for f in iter_files(sys.argv[1:]):
    try:
        t = f.read_text(encoding="utf-8")
    except Exception:
        continue
    for bad in BAD:
        n = t.count(bad)
        if n:
            fails.append(f"{f} :: 命中禁串 {bad!r} ×{n}")
    hits = {c: t.count(c) for c in CANON if t.count(c)}
    if hits:
        report.append(f"{f.name} :: {hits}")

print("\n".join(report) if report else "(scope 内未发现受保护实体)")
print("-" * 56)
if fails:
    print("\n".join(fails))
    print("CJK INTEGRITY FAILED  issues:", len(fails))
    sys.exit(1)
print("CJK INTEGRITY PASSED  issues: 0")
