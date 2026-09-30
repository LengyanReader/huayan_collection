# -*- coding: utf-8 -*-
"""report.py — 硬字幕 OCR 重建报告（自包含 HTML），按 vid 生成。

用法：python report.py <vid>
读取 <workspace>/<vid>/<vid>.md + runs.tsv + <vid>.info.json，
输出 <workspace>/<vid>/字幕重建報告_<title>.html。
"""
import base64
import csv
import json
import re
import sys
from pathlib import Path

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

TOOL_DIR = Path(__file__).resolve().parent
CONF = json.loads((TOOL_DIR / "config.json").read_text(encoding="utf-8"))
WS = Path(CONF["workspace"])
if not WS.is_absolute():
    WS = (TOOL_DIR / WS).resolve()

LINE_RE = re.compile(r"`\[(\d{2}:\d{2}:\d{2})–(\d{2}:\d{2}:\d{2})\]` (.+)")


def b64(p: Path) -> str:
    return base64.b64encode(p.read_bytes()).decode()


def sec(hms):
    h, m, s = (int(x) for x in hms.split(":"))
    return h * 3600 + m * 60 + s


def load_entries(md):
    out = []
    for line in md.read_text(encoding="utf-8").splitlines():
        m = LINE_RE.match(line)
        if m:
            out.append((m.group(1), m.group(2), m.group(3).strip()))
    return out


def load_runmap(d):
    m = {}
    with open(d / "runs.tsv", encoding="utf-8") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            m[int(float(r["start_sec"]))] = d / "reps" / r["rep_frame"]
    return m


def pick_samples(entries, n=12):
    cand = [e for e in entries if "|" not in e[2] and 6 <= len(e[2]) <= 30]
    if len(cand) <= n:
        return cand
    picked = []
    for i in range(n):
        seg = cand[int(i * len(cand) / n):int((i + 1) * len(cand) / n)]
        if seg:
            picked.append(seg[len(seg) // 2])
    return picked


def frame_for(ts, runmap):
    s = sec(ts)
    for dd in range(0, 4):
        for cand in (s + dd, s - dd):
            p = runmap.get(cand)
            if p and p.exists():
                return p
    return None


CSS = """
body{font-family:'Noto Serif TC','MS Mincho',serif;max-width:960px;margin:0 auto;
padding:2rem 1.2rem;color:#2b2b2b;line-height:1.75;background:#faf7f2}
h1{font-size:1.7rem;border-bottom:3px double #8b5e3c;padding-bottom:.5rem}
h2{font-size:1.25rem;color:#6b4a2b;margin-top:2.2rem;border-left:5px solid #8b5e3c;padding-left:.6rem}
.meta{background:#fff;border:1px solid #e0d5c5;border-radius:8px;padding:1rem 1.4rem;font-size:.95rem}
.meta td{padding:.15rem .8rem .15rem 0;vertical-align:top}
.note{background:#fdf3e7;border-left:4px solid #c98a3d;padding:.6rem 1rem;margin:.8rem 0;font-size:.92rem}
figure{margin:1.2rem 0;background:#fff;border:1px solid #ddd;padding:.8rem;border-radius:6px}
figure img{width:100%;display:block;border-radius:3px}
figcaption{font-size:.88rem;color:#666;margin-top:.45rem}
.cap{font-family:Consolas,monospace;font-size:.9rem;background:#2e2a26;color:#f5ead6;padding:.35rem .7rem;border-radius:4px}
table.subs{border-collapse:collapse;width:100%;font-size:.93rem;background:#fff}
table.subs td{border-bottom:1px solid #eee;padding:.3rem .6rem}
table.subs td.t{white-space:nowrap;color:#8b5e3c;font-family:Consolas,monospace;font-size:.85rem}
table.subs tr:hover{background:#fbf3e6}
.step{display:flex;gap:.8rem;margin:.7rem 0;align-items:flex-start}
.step .n{flex:0 0 1.9rem;height:1.9rem;border-radius:50%;background:#8b5e3c;color:#fff;text-align:center;line-height:1.9rem;font-weight:700}
code{background:#f0e8dc;padding:.1rem .35rem;border-radius:3px;font-size:.88em}
footer{margin-top:3rem;color:#999;font-size:.85rem;border-top:1px solid #ddd;padding-top:1rem}
"""


def main(vid):
    d = WS / vid
    entries = load_entries(d / f"{vid}.md")
    runmap = load_runmap(d)
    info = {}
    ij = WS / f"{vid}.info.json"
    if ij.exists():
        info = json.loads(ij.read_text(encoding="utf-8"))
    title = info.get("title", vid)
    dur = info.get("duration", 0)
    hh, rem = divmod(int(dur), 3600)
    mm, ss = divmod(rem, 60)
    durstr = f"{hh}:{mm:02d}:{ss:02d}（{dur} 秒）" if dur else "未知"

    samples = pick_samples(entries)
    shot_html = []
    for i, (t0, t1, txt) in enumerate(samples, 1):
        fp = frame_for(t0, runmap)
        if not fp:
            continue
        shot_html.append(
            f'<figure><img src="data:image/jpeg;base64,{b64(fp)}">'
            f'<div class="cap">[{t0}–{t1}]　{txt}</div>'
            f'<figcaption>样本 {i} · 字幕带帧（1fps 抽帧，OCR 结果叠加图下）</figcaption></figure>')
    rows = "".join(f"<tr><td class='t'>{t0}–{t1}</td><td>{txt}</td></tr>"
                   for t0, t1, txt in entries)

    html = f"""<!DOCTYPE html>
<html lang="zh-Hant"><head><meta charset="utf-8">
<title>{title} · 硬字幕 OCR 重建報告</title><style>{CSS}</style></head><body>
<h1>寺方字幕檔案恢復 · OCR 重建報告<br><small style="font-size:.6em;color:#6b4a2b">{title}</small></h1>
<div class="meta"><table>
<tr><td>視頻</td><td><a href="https://www.youtube.com/watch?v={vid}">{title}（{vid}）</a></td></tr>
<tr><td>來源</td><td>{info.get('channel','大华严寺')} · 時長 {durstr} · 上傳 {info.get('upload_date','')}</td></tr>
<tr><td>產出性質</td><td><b>OCR 重建稿 · 待校定</b>（寺方原始字幕稿件已遺失，本稿為硬字幕影像還原，仍需三源互證重新校定）</td></tr>
<tr><td>授權依據</td><td>維護者（華嚴弟子）已獲寺方授權 · 用途為傳播正法（見 harness/compliance.md §五/§七）</td></tr>
<tr><td>生成日期</td><td>{__import__('datetime').date.today().isoformat()}</td></tr>
</table></div>

<h2>一 · 為什麼要做影像字幕提取（解讀）</h2>
<p>該講座視頻由大華嚴寺官方頻道發布，字幕<b>直接燒錄在畫面內</b>（hardsub），經 <code>yt-dlp --list-subs</code> 實測無任何字幕軌。
寺方原始字幕稿件已遺失，畫面內硬字幕成為唯一存續形態——故以 OCR 把字幕帶畫面還原為帶時間碼的文本檔案，作為後續重新校定的基礎稿。</p>

<h2>二 · 提取流水線（四步 · 全部實測可復跑）</h2>
<div class="step"><div class="n">1</div><div><b>下載</b>：yt-dlp 取 720p。字幕白字黑邊約 50px 高，720p 足夠識別。</div></div>
<div class="step"><div class="n">2</div><div><b>抽字幕帶幀</b>：ffmpeg 以 1fps 只裁畫面<b>中央 64% 寬 × 底部 15.5% 高</b>，覆蓋字幕區並避開右側豎排角標與左下幻燈頁腳。</div></div>
<div class="step"><div class="n">3</div><div><b>掩碼去重</b>：對白/黃文字像素做遮罩、相鄰幀算 IoU，同字幕連續幀合併為 run，僅留代表幀。</div></div>
<div class="step"><div class="n">4</div><div><b>OCR + 合成</b>：PaddleOCR（PP-OCRv6 · 繁體）逐 run 識別，按文本框水平位置二次過濾污染，相鄰同文合併 → {len(entries)} 條帶時間碼字幕。</div></div>
<div class="note">工程要點：PaddleOCR 3.x Windows CPU 須 <code>enable_mkldnn=False</code>；時間碼精度 ±1 秒（1fps 採樣）。</div>

<h2>三 · 字幕截圖對照（{len(shot_html)} 例 · 全片均勻抽樣）</h2>
{''.join(shot_html)}

<h2>四 · 已知瑕疵清單（校定時留意）</h2>
<ol>
<li>片頭動畫時段可能產生亂碼條目，可整段丟棄；</li>
<li>幻燈片時段帶內多行文字以「 | 」拼接，非純口播字幕；</li>
<li>時間碼精度 ±1s，快語速換句可能丟首字；</li>
<li>繁體為主、偶見簡繁混排，校定時統一；</li>
<li>本稿僅為<b>影像層還原</b>——與講義、錄音的語詞級校定（三源互證）另行進行。</li>
</ol>

<h2>五 · 全量字幕文本（{len(entries)} 條）</h2>
<table class="subs"><tbody>
{rows}
</tbody></table>
<footer>生成：tools/sub_extract/report.py · 流水線 pipeline.py · 本報告自包含（圖片內嵌），可直接轉交寺方。</footer>
</body></html>
"""
    safe = re.sub(r'[\\/:*?"<>|]', "_", title)[:40]
    out = d / f"字幕重建報告_{safe}.html"
    out.write_text(html, encoding="utf-8")
    print(f"[ok] {out.name}  {out.stat().st_size/1024:.0f}KB  entries={len(entries)} shots={len(shot_html)}")


if __name__ == "__main__":
    main(sys.argv[1])
