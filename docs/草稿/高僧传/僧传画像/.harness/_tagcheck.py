import io
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")  # 移植安全：不依赖宿主 locale

ROOT = Path(__file__).resolve().parent.parent  # 僧传画像/（可从任意 cwd 运行）
TAGS = ["section", "div", "details", "summary", "table", "tr", "td", "th",
        "svg", "g", "marker", "rect", "line", "text", "html", "body", "head"]
FILES = [ROOT / "index.html", ROOT / "monolith.html"] + \
    sorted((ROOT / "portraits").glob("*.html"))

bad = 0
for f in FILES:
    t = f.read_text(encoding="utf-8")
    probs = []
    for tag in TAGS:
        op = len(re.findall(r"<" + tag + r"[ >]", t))
        cl = len(re.findall(r"</" + tag + r">", t))
        selfc = len(re.findall(r"<" + tag + r"[^>]+/>", t))
        if op - selfc != cl:
            probs.append("%s open=%d self=%d close=%d" % (tag, op, selfc, cl))
    print(("OK   " if not probs else "!!   ") + str(f.relative_to(ROOT)) +
          ("" if not probs else " :: " + "; ".join(probs)))
    bad += len(probs)
print("TAGCHECK " + ("PASSED" if bad == 0 else "FAILED (%d)" % bad))
sys.exit(1 if bad else 0)
