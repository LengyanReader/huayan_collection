# -*- coding: utf-8 -*-
# 单页深度自查（校勘闸配套）：嵌套「」配对体检 + 直查盘内逐字命中（不经报告）
# 用法：python scripts/quote_selfcheck.py <页文件> [更多页...]（缺省=jingjian）
import re, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.quote_koushu import QUOTE, SPLIT, norm, find, load_index  # noqa

targets = [Path(p) for p in sys.argv[1:]] or [
    Path(r"docs/草稿/高僧传/僧传画像/portraits/jingjian.html")]
idx = load_index()
out = []
for t_path in targets:
    t = t_path.read_text(encoding="utf-8")
    for i, line in enumerate(t.splitlines(), 1):
        # 原始行内「」计数（配对体检）
        if line.count("「") != line.count("」"):
            out.append(f"{t_path.name} L{i} PAIR-UNBALANCED {line.strip()[:70]}")
        for q in QUOTE.findall(line):
            for frag in SPLIT.split(q):
                f = norm(frag)
                if len(f) < 6:
                    continue
                if not find(f, idx):
                    subs = [norm(s) for s in re.split(r"[·＝=＋+]", frag)
                            if len(norm(s)) >= 4]
                    if subs and all(find(norm(s), idx) for s in subs):
                        continue
                    out.append(f"{t_path.name} L{i} MISS {frag[:60]!r}")
print("\n".join(out) if out else "CLEAN")
print("issues:", len(out))
