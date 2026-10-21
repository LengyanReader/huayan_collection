# -*- coding: utf-8 -*-
"""L.138b helper: 扫 ep01 delivery · 按 cue 结构 · slide 标记 · 分段"""
import io, re, sys
for _s in (sys.stdout, sys.stderr):
    try: _s.reconfigure(encoding="utf-8", errors="replace")
    except: pass

txt = io.open('docs/hy_refs/sub_extract/delivery/ep01.md', encoding='utf-8').read()
CUE = re.compile(r"^`\[(\d\d):(\d\d):(\d\d)[–-](\d\d):(\d\d):(\d\d)\]`\s*(.+)$")
cues = []
for line in txt.splitlines():
    m = CUE.match(line)
    if m:
        h, mm, s, _, _, _, text = m.groups()
        sec = int(h)*3600 + int(mm)*60 + int(s)
        cues.append((sec, f"{h}:{mm}:{s}", text))

print(f"total cues: {len(cues)}")
print(f"first: {cues[0][1]} · {cues[0][2][:60]}")
print(f"last:  {cues[-1][1]} · {cues[-1][2][:60]}")

# Detect slide markers — cues with "|" pipe are typically slides pasted
slide_pat = re.compile(r"第一章|第二章|第三章|第九节|第十|第[一二三四五六七八九十]+節|第[一二三四五六七八九十]+节")
slide_marks = []
for sec, t, txt_cue in cues:
    if '|' in txt_cue and slide_pat.search(txt_cue):
        slide_marks.append((sec, t, txt_cue[:120]))

print(f"\n=== slide-marker cues (| present + 第X chapter pattern): {len(slide_marks)} ===")
seen_titles = set()
for sec, t, x in slide_marks:
    # Extract chapter title core
    core = re.search(r"第一章玄談.{0,20}|第二章.{0,20}|第三章.{0,20}", x)
    key = core.group(0) if core else x[:20]
    if key in seen_titles: continue
    seen_titles.add(key)
    print(f"{t}  {x}")
