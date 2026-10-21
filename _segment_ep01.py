# -*- coding: utf-8 -*-
"""L.138b helper: 分段合并 ep01 cues · 剔除 slide 与片头乱码 · 生成可读段
6 topic-chapter 分界（依 OCR slide 标记与 talk 自然转段·见 _probe_ep01 输出）：
  §A  03:10 – 07:00   请法因缘 · 玄谈定位 · 60 次规模
  §B  07:00 – 17:00   三问立宗 · 菩提树下成道 · 觉他自觉
  §C  17:00 – 42:00   外道禅定 · 修行工程 · 阿罗逻迦兰 · 不用大脑
  §D  42:00 – 60:00   佛世 → 部派 → 大乘 · 西域佛教 · 三乘
  §E  60:00 – 67:00   华严系统 · 小小一本 · 心量
  §F  67:00 – 96:20   中国形成的宗派 · 贤首 · 化身/报身 · 直接成佛 · 康熙诏定
"""
import io, re, sys
for _s in (sys.stdout, sys.stderr):
    try: _s.reconfigure(encoding="utf-8", errors="replace")
    except: pass

txt = io.open('docs/hy_refs/sub_extract/delivery/ep01.md', encoding='utf-8').read()
CUE = re.compile(r"^`\[(\d\d):(\d\d):(\d\d)[–\-](\d\d):(\d\d):(\d\d)\]`\s*(.+)$")
cues = []
for line in txt.splitlines():
    m = CUE.match(line)
    if m:
        h, mm, s, h2, mm2, s2, text = m.groups()
        sec = int(h)*3600 + int(mm)*60 + int(s)
        end = int(h2)*3600 + int(mm2)*60 + int(s2)
        cues.append((sec, end, f"{h}:{mm}:{s}", text))

SEGMENTS = [
    ("A", "请法因缘·玄谈定位·六十次规模",     3*60+10, 7*60),
    ("B", "三问立宗·菩提树下成道·自觉觉他",   7*60,     17*60),
    ("C", "外道禅定·修行工程·阿罗逻迦兰",     17*60,    42*60),
    ("D", "佛世→部派→大乘·西域·三乘",         42*60,    60*60),
    ("E", "华严系统·小小一本·心量",           60*60,    67*60),
    ("F", "中国形成的宗派·贤首·化身报身",     67*60,    96*60+20),
]

# Slide-marker patterns (pipe + 第X 章 markers = slide, drop)
SLIDE = re.compile(r"第一章|第二章|第[一二三四五六七八九十]+節|第[一二三四五六七八九十]+节|法講座|玄談|華嚴經|華嚴學|华嚴經|华厂经|華廠經|华严经|的過去|過去、|現在、|未来|未來|現在|此其|看下面|下一頁|賢首宗|四大宗|白漫|漫去|經康熙")

def is_slide_or_noise(t):
    if '|' in t and SLIDE.search(t):
        return True
    # very short single-char noise
    if len(t.strip()) <= 1:
        return True
    return False

out = io.open('.tmp_ep01_segments.txt', 'w', encoding='utf-8', newline='\n')
for key, label, a, b in SEGMENTS:
    seg = [c for c in cues if a <= c[0] < b]
    cleaned = [(s, e, t, x) for (s, e, t, x) in seg if not is_slide_or_noise(x)]
    # merge consecutive into paragraphs: break when gap > 2.5s OR sentence-end punctuation
    paras = []
    buf = []
    prev_end = None
    for s, e, t, x in cleaned:
        gap = s - (prev_end if prev_end else s)
        if buf and (gap > 2500/1000 or (buf and buf[-1][3] and buf[-1][3][-1] in '。？！?')):
            paras.append(buf)
            buf = []
        buf.append((s, e, t, x))
        prev_end = e
    if buf:
        paras.append(buf)
    # emit
    a_tc = seg[0][2] if seg else 'N/A'
    b_tc = seg[-1][2] if seg else 'N/A'
    out.write(f"### §{key}  {label}  [{a_tc} – {b_tc}]\n\n")
    for pi, p in enumerate(paras, 1):
        # timecode range
        trange = f"{p[0][2]}–{p[-1][2]}" if len(p)>1 else p[0][2]
        merged = ''.join(x[3] for x in p)
        # add punctuation gap markers
        out.write(f"**P{pi:02d}** `[OCR {trange}]` {merged}\n\n")
    out.write(f"\n=== 段 {key} ·  原始 cues {len(seg)} · 清洗后 {len(cleaned)} · 合并段 {len(paras)} ===\n\n---\n\n")
out.close()
print("wrote .tmp_ep01_segments.txt")
