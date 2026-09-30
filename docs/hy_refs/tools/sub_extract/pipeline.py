# -*- coding: utf-8 -*-
"""pipeline.py — 硬字幕 OCR 提取流水线（四阶段 CLI）

用法：
  python pipeline.py extract <vid> [--start S --dur D]
  python pipeline.py dedup   <vid>
  python pipeline.py ocr     <vid> [--limit N --offset N]
  python pipeline.py merge   <vid>

vid = YouTube 视频 ID。mp4 / 输出文件位于 config.workspace 指定目录。
"""
import argparse
import csv
import json
import subprocess
import sys
import unicodedata
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


def work(vid):
    d = WS / vid
    (d / "frames").mkdir(parents=True, exist_ok=True)
    (d / "reps").mkdir(parents=True, exist_ok=True)
    return d


def video_path(vid):
    v = WS / f"{vid}.mp4"
    if not v.exists():
        raise SystemExit(f"[fail] 视频不存在：{v}")
    return v


# ---------------------------------------------------------------- extract
def cmd_extract(conf, vid, start, dur):
    v = video_path(vid)
    d = work(vid)
    out = d / "frames"
    vf = (f"fps={conf['fps']},"
          f"crop=iw*{conf['crop_w']}:ih*{conf['crop_h']}:iw*{conf['crop_x']}:ih*{conf['crop_y']}")
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-stats"]
    if start:
        cmd += ["-ss", str(start)]
    if dur:
        cmd += ["-t", str(dur)]
    cmd += ["-i", str(v), "-vf", vf, "-q:v", "2", str(out / "frame_%06d.jpg")]
    print("[extract]", " ".join(cmd), flush=True)
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    print((r.stderr or "").strip()[-200:], flush=True)
    print(f"[extract] {vid} frames={len(list(out.glob('frame_*.jpg')))} exit={r.returncode}", flush=True)


# ------------------------------------------------------------------- dedup
def _mask(img, conf):
    import cv2
    import numpy as np
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    white = cv2.inRange(gray, conf.get("white_v", 200), 255)
    yellow = cv2.inRange(hsv, (15, 80, 150), (40, 255, 255))
    m = cv2.bitwise_or(white, yellow)
    return cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((3, 5), np.uint8))


def cmd_dedup(conf, vid):
    import cv2
    d = work(vid)
    frames = sorted((d / "frames").glob("frame_*.jpg"))
    if not frames:
        raise SystemExit(f"[fail] {d/'frames'} 为空，先跑 extract")
    reps = d / "reps"
    iou_t = conf.get("mask_iou", 0.82)
    ink_t = conf.get("ink_min", 0.0035)

    def iou(a, b):
        inter = cv2.bitwise_and(a, b).sum()
        union = cv2.bitwise_or(a, b).sum()
        return 1.0 if union == 0 else inter / union

    rows = []
    cur_start_i = 0
    first = cv2.imread(str(frames[0]))
    cur_mask = _mask(first, conf)
    cur_ink = float(cur_mask.mean()) / 255
    best_i, best_ink = 0, cur_ink

    def flush(end_i):
        nonlocal cur_start_i
        rows.append((cur_start_i + 1, cur_start_i / conf["fps"],
                     (end_i + 1) / conf["fps"], frames[best_i].name, cur_ink))
        cur_start_i = end_i + 1

    for i, fp in enumerate(frames):
        if i == 0:
            continue
        img = cv2.imread(str(fp))
        if img is None:
            continue
        m = _mask(img, conf)
        ink = float(m.mean()) / 255
        same = iou(cur_mask, m) >= iou_t and (cur_ink < ink_t) == (ink < ink_t)
        if same:
            cur_mask = cv2.bitwise_or(cur_mask, m)
            if ink > best_ink:
                best_i, best_ink = i, ink
        else:
            flush(i - 1)
            cur_mask, cur_ink = m.copy(), ink
            best_i, best_ink = i, ink
        if i % 1000 == 0:
            print(f"[dedup] {vid} {i}/{len(frames)}", flush=True)
    flush(len(frames) - 1)

    with open(d / "runs.tsv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["frame_idx", "start_sec", "end_sec", "rep_frame", "ink"])
        w.writerows(rows)
    import shutil
    n_txt = 0
    for r in rows:
        if r[4] >= ink_t:
            shutil.copyfile(d / "frames" / r[3], reps / r[3])
            n_txt += 1
    print(f"[dedup] {vid} runs={len(rows)} 含字幕={n_txt}", flush=True)


# --------------------------------------------------------------------- ocr
def cmd_ocr(conf, vid, limit, offset):
    import os
    n_th = str(conf.get("ocr_threads", 1))
    for var in ("OMP_NUM_THREADS", "MKL_NUM_THREADS",
                "OPENBLAS_NUM_THREADS", "FLAGS_num_threads"):
        os.environ[var] = n_th
    from paddleocr import PaddleOCR
    import paddle
    try:
        paddle.base.core.set_num_threads(int(n_th))
    except Exception:
        pass
    import cv2
    d = work(vid)
    ocr = PaddleOCR(lang=conf.get("ocr_lang", "chinese_cht"),
                    use_doc_orientation_classify=False,
                    use_doc_unwarping=False,
                    use_textline_orientation=False,
                    enable_mkldnn=False)
    out_tsv = d / "ocr_out.tsv"
    done = set()
    if out_tsv.exists():
        with open(out_tsv, encoding="utf-8") as f:
            for row in csv.DictReader(f, delimiter="\t"):
                done.add(row["rep_frame"])
    todo = [p for p in sorted((d / "reps").glob("frame_*.jpg")) if p.name not in done]
    if offset:
        todo = todo[offset:]
    if limit:
        todo = todo[:limit]
    new = not out_tsv.exists() or not done
    with open(out_tsv, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter="\t")
        if new:
            w.writerow(["rep_frame", "text"])
        lo, hi = conf.get("box_cx_min", 0.2), conf.get("box_cx_max", 0.8)
        for n, p in enumerate(todo, 1):
            img = cv2.imread(str(p))
            w_ = img.shape[1]
            try:
                res = ocr.predict(img)
                segs = []
                for r in res:
                    texts = r.get("rec_texts", [])
                    polys = r.get("rec_polys", None)
                    for i, t in enumerate(texts):
                        if polys is not None and i < len(polys):
                            xs = [pt[0] for pt in polys[i]]
                            if not (lo <= sum(xs) / len(xs) / w_ <= hi):
                                continue
                        segs.append(t)
                txt = " | ".join(segs)
            except AttributeError:
                res = ocr.ocr(img, cls=False)
                txt = " | ".join(line[1][0] for im in res for line in im if line)
            w.writerow([p.name, txt])
            f.flush()
            if n % 50 == 0 or n == len(todo):
                print(f"[ocr] {vid} {n}/{len(todo)}", flush=True)
    print(f"[ocr] {vid} done", flush=True)


# ------------------------------------------------------------------- merge
def _norm(s):
    s = unicodedata.normalize("NFKC", s).strip()
    for ch in " ，。、！？；：,.!?;:~—-「」『』\"'()（）【】":
        s = s.replace(ch, "")
    return s


def cmd_merge(conf, vid):
    d = work(vid)
    rows, texts = [], {}
    with open(d / "runs.tsv", encoding="utf-8") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))
    if (d / "ocr_out.tsv").exists():
        with open(d / "ocr_out.tsv", encoding="utf-8") as f:
            for r in csv.DictReader(f, delimiter="\t"):
                texts[r["rep_frame"]] = r["text"].strip()
    ink_t = conf.get("ink_min", 0.0035)
    entries = []
    for r in rows:
        if float(r["ink"]) < ink_t:
            continue
        txt = texts.get(r["rep_frame"], "").strip()
        if not txt:
            continue
        s, e = float(r["start_sec"]), float(r["end_sec"])
        if entries and _norm(entries[-1][2]) == _norm(txt):
            entries[-1] = (entries[-1][0], e, entries[-1][2])
        else:
            entries.append((s, e, txt))

    def ts(sec):
        h, rem = divmod(int(sec), 3600)
        m, s2 = divmod(rem, 60)
        return f"{h:02d}:{m:02d}:{s2:02d}"

    with open(d / f"{vid}.srt", "w", encoding="utf-8") as f:
        for i, (s, e, t) in enumerate(entries, 1):
            f.write(f"{i}\n{ts(s)},000 --> {ts(e)},000\n{t}\n\n")
    with open(d / f"{vid}.md", "w", encoding="utf-8") as f:
        f.write(f"# {vid} 硬字幕提取稿（OCR 重建 · 待校定）\n\n")
        for s, e, t in entries:
            f.write(f"`[{ts(s)}–{ts(e)}]` {t}\n\n")
    print(f"[merge] {vid} entries={len(entries)} -> {vid}.srt / {vid}.md", flush=True)


def main():
    ap = argparse.ArgumentParser(description="硬字幕 OCR 提取流水线")
    ap.add_argument("stage", choices=["extract", "dedup", "ocr", "merge"])
    ap.add_argument("vid")
    ap.add_argument("--start", type=int, default=0)
    ap.add_argument("--dur", type=int, default=0)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--offset", type=int, default=0)
    a = ap.parse_args()
    {"extract": lambda: cmd_extract(CONF, a.vid, a.start, a.dur),
     "dedup": lambda: cmd_dedup(CONF, a.vid),
     "ocr": lambda: cmd_ocr(CONF, a.vid, a.limit, a.offset),
     "merge": lambda: cmd_merge(CONF, a.vid)}[a.stage]()


if __name__ == "__main__":
    main()
