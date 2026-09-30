# -*- coding: utf-8 -*-
"""batch.py — 硬字幕提取批量驱动器（多 Lane 并行安全）

用法：python batch.py <vid1> <vid2> ...
每片：download(若无 mp4) → extract → dedup → ocr → merge → report。
支持阶段跳过（已完成的不重跑）、OCR 增量续跑。
通过环境变量 LANE 隔离并行 Lane 的状态日志（batch_status_{LANE}.log）。
"""
import json
import os
import subprocess
import sys
import time
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

PY = sys.executable
LANE = os.environ.get("LANE", "x")
STATUS = WS / f"batch_status_{LANE}.log"
FMT = "136+251/398+251/bv*[height<=720]+ba/b[height<=720]"


def log(msg):
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    with open(STATUS, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def sh(args, tag):
    log(f"  -> {' '.join(str(a) for a in args[:6])} ...")
    r = subprocess.run([str(a) for a in args], capture_output=True,
                       text=True, encoding="utf-8", errors="replace")
    tail = (r.stderr or r.stdout or "").strip().splitlines()[-3:]
    log(f"     exit={r.returncode} | {' / '.join(tail)[:200]}")
    return r.returncode == 0


def run_one(vid):
    mp4 = WS / f"{vid}.mp4"
    if not mp4.exists():
        ok = sh([PY, "-m", "yt_dlp", "-f", FMT, "--merge-output-format", "mp4",
                 "--write-info-json", "--no-write-playlist-metafiles",
                 "-o", str(WS / "%(id)s.%(ext)s"),
                 f"https://www.youtube.com/watch?v={vid}"], vid)
        if not ok or not mp4.exists():
            log(f"[FAIL] {vid} download"); return False
        log(f"[OK] {vid} downloaded")
    else:
        log(f"[skip] {vid} mp4 exists")
    # 阶段跳过：已完成的 extract/dedup 不重跑
    frames_dir = WS / vid / "frames"
    n_frames = len(list(frames_dir.glob("frame_*.jpg"))) if frames_dir.exists() else 0
    stages = []
    if n_frames == 0:
        stages.append("extract")
    else:
        log(f"[skip] {vid} extract frames={n_frames} exists")
    if (WS / vid / "runs.tsv").exists():
        log(f"[skip] {vid} dedup runs.tsv exists")
    else:
        stages.append("dedup")
    stages += ["ocr", "merge"]
    for stage in stages:
        if not sh([PY, TOOL_DIR / "pipeline.py", stage, vid], vid):
            log(f"[FAIL] {vid} {stage}"); return False
    sh([PY, TOOL_DIR / "report.py", vid], vid)
    log(f"[DONE] {vid} 全部完成")
    return True


def main():
    vids = sys.argv[1:]
    log(f"==== batch start: {vids} ====")
    done = []
    for v in vids:
        log(f"---- {v} begin ----")
        if run_one(v):
            done.append(v)
    log(f"==== batch finish: {len(done)}/{len(vids)} ok: {done} ====")


if __name__ == "__main__":
    main()
