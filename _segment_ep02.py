"""_segment_ep02.py — segment Ep 2 cues into 6 topic chapters · auto-merge paragraphs."""
import re, io, json

SRC = "docs/hy_refs/sub_extract/delivery/ep02.md"
CUE = re.compile(r"^`\[(\d\d):(\d\d):(\d\d)[\u2013-](\d\d):(\d\d):(\d\d)\]`\s*(.+)$")

# 6 topic-chapter boundaries (start_sec, end_sec, title)
SEGMENTS = [
    ("A", "承接前講·一佛乘·四法界·下迴向",         0,      1200),
    ("B", "外道辨偽·巫師·拜拜法·真言批判",         1200,   2100),
    ("C", "發菩提心·修行工程·上進·知見標準",       2100,   3300),
    ("D", "叢林法則·人品教育·靈性教室·家庭修行",   3300,   5400),
    ("E", "現場問答·第四期佛教·價值觀·社會建設",   5400,   7200),
    ("F", "問答續·菩提樹喻·書呆子·華嚴經傳播",     7200,   8200),
]

# Slide marker patterns to exclude
SLIDE_PAT = re.compile(
    r"^(第一章|第二章|玄談|法講座\||第一節)"
    r"|^第[一二三四五六七八九十]+[章節节]"
    r"|《華嚴經》的過去、現在、未來"
    r"|賢首兼慈恩宗|四十二世|四十一世"
)

# Load cues — capture both start AND end time
raw_cues = []
with io.open(SRC, encoding="utf-8") as f:
    for line in f:
        m = CUE.match(line.strip())
        if not m:
            continue
        s_h, s_m, s_s = int(m.group(1)), int(m.group(2)), int(m.group(3))
        e_h, e_m, e_s = int(m.group(4)), int(m.group(5)), int(m.group(6))
        start_sec = s_h * 3600 + s_m * 60 + s_s
        end_sec = e_h * 3600 + e_m * 60 + e_s
        text = m.group(7).strip()
        raw_cues.append((start_sec, end_sec, text))

# Filter: remove noise + slide markers
valid = []
for start_sec, end_sec, text in raw_cues:
    if len(text) <= 2 and not re.search(r"[\u4e00-\u9fff]", text):
        continue  # noise
    if SLIDE_PAT.search(text):
        continue  # slide marker echo
    valid.append((start_sec, end_sec, text))

print(f"total: {len(raw_cues)} | valid (after filter): {len(valid)}")

# Merge into paragraphs: gap > 1.0s OR sentence-end OR max_chars > 500 triggers new P
SENT_END = re.compile(r"[。！？!?…]")
MAX_P_CHARS = 500

def fmt_ts(sec):
    h, r = divmod(sec, 3600)
    m, s = divmod(r, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"

all_paras = []  # [{seg, pid, start, end, text}]
for seg_id, seg_title, seg_start, seg_end in SEGMENTS:
    seg_cues = [(ss, es, txt) for ss, es, txt in valid if seg_start <= ss < seg_end]
    if not seg_cues:
        continue
    paras = []
    buf_text = ""
    buf_start = seg_cues[0][0]
    buf_end = seg_cues[0][1]  # END time of first cue
    first = True
    for ss, es, txt in seg_cues:
        if first:
            buf_text = txt
            buf_start = ss
            buf_end = es
            first = False
            continue
        gap = ss - buf_end  # real silence gap
        prev_end = SENT_END.search(buf_text[-15:]) if len(buf_text) > 20 else None
        too_long = len(buf_text) > MAX_P_CHARS
        if gap > 1.0 or prev_end or too_long:
            paras.append((buf_start, buf_end, buf_text))
            buf_text = txt
            buf_start = ss
        else:
            buf_text += txt
        buf_end = es
    if buf_text:
        paras.append((buf_start, buf_end, buf_text))
    for pi, (ps, pe, ptxt) in enumerate(paras, 1):
        pid = f"{seg_id}{pi:02d}"
        all_paras.append({"seg": seg_id, "pid": pid, "start": fmt_ts(ps), "end": fmt_ts(pe), "text": ptxt})
    a_tc = fmt_ts(seg_cues[0][0])
    b_tc = fmt_ts(seg_cues[-1][0])
    print(f"  §{seg_id} ({seg_title}): {len(paras)}P | {a_tc}–{b_tc}")

print(f"\ntotal paragraphs: {len(all_paras)}")
total_chars = sum(len(p["text"]) for p in all_paras)
print(f"total CJK chars in output: {total_chars}")

# Write JSON for downstream
out = {"segments": [{"id": s[0], "title": s[1]} for s in SEGMENTS], "paragraphs": all_paras}
with io.open("_seg_ep02.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("wrote _seg_ep02.json")
