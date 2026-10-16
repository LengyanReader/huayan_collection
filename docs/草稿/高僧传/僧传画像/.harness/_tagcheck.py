import re
from pathlib import Path

t = Path("monolith.html").read_text(encoding="utf-8")
for tag in ["section", "div", "details", "summary", "table", "tr", "td", "th", "svg", "g", "marker", "rect", "line", "text"]:
    op = len(re.findall(r"<" + tag + r"[ >]", t))
    cl = len(re.findall(r"</" + tag + r">", t))
    selfc = len(re.findall(r"<" + tag + r"[^>]*/>", t))
    flag = "OK" if (op - selfc) == cl else "!!"
    print(f"{flag} {tag}: open={op} selfclose={selfc} close={cl} net_open={op-selfc}")
