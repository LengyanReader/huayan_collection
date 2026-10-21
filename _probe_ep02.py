"""_probe_ep02.py — scan Ep 2 cues: slide markers + chapter structure."""
import re, io

SRC = "docs/hy_refs/sub_extract/delivery/ep02.md"
CUE = re.compile(r"^`\[(\d\d):(\d\d):(\d\d)[–-](\d\d):(\d\d):(\d\d)\]`\s*(.+)$")

# slide-marker patterns (chapter/section headings shown on-screen)
slide_pat = re.compile(
    r"第[一二三四五六七八九十百]+[章節节回會会]"
    r"|玄談|華嚴經|一佛乘|判教|法界|理事|空有|般若"
    r"|^[A-Z]$"  # single uppercase = likely slide artifact
)

total = 0
slides = []
noise = []

with io.open(SRC, encoding="utf-8") as f:
    for line in f:
        m = CUE.match(line.strip())
        if not m:
            continue
        total += 1
        h, mi, s = int(m.group(1)), int(m.group(2)), int(m.group(3))
        tsec = h * 3600 + mi * 60 + s
        text = m.group(7).strip()
        if slide_pat.search(text):
            slides.append((tsec, text))
        if len(text) <= 2 and not re.match(r"[\u4e00-\u9fff]", text):
            noise.append((tsec, text))

print(f"total cues: {total}")
print(f"slide markers: {len(slides)}")
print(f"noise (<=2 chars non-CJK): {len(noise)}")
valid = total - len(noise)
print(f"valid cues (est): {valid}")

print("\n--- first 30 slide markers ---")
for t, txt in slides[:30]:
    mm, ss = divmod(t, 60)
    hh, mm2 = divmod(mm, 60)
    print(f"  [{hh:02d}:{mm2:02d}:{ss:02d}] {txt[:80]}")

print("\n--- last 10 slide markers ---")
for t, txt in slides[-10:]:
    mm, ss = divmod(t, 60)
    hh, mm2 = divmod(mm, 60)
    print(f"  [{hh:02d}:{mm2:02d}:{ss:02d}] {txt[:80]}")
