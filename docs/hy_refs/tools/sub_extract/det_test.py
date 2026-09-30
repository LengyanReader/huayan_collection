# -*- coding: utf-8 -*-
"""det_test.py — 验证 OCR 线程数是否改变结果（确定性验证）

用法：python det_test.py [vid] [n_frames]
默认取 workspace 中第一个已完成 vid 的前 40 帧，单线程重跑并比对。
"""
import csv
import json
import os
import sys
import time
from pathlib import Path

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

N_TH = os.environ.get("TH", "1")
for var in ("OMP_NUM_THREADS", "MKL_NUM_THREADS",
            "OPENBLAS_NUM_THREADS", "FLAGS_num_threads"):
    os.environ[var] = N_TH
from paddleocr import PaddleOCR  # noqa: E402  先加载 paddleocr（避 shm.dll 冲突）
import paddle  # noqa: E402
try:
    paddle.base.core.set_num_threads(int(N_TH))
except Exception:
    pass
import cv2  # noqa: E402

TOOL_DIR = Path(__file__).resolve().parent
CONF = json.loads((TOOL_DIR / "config.json").read_text(encoding="utf-8"))
WS = Path(CONF["workspace"])
if not WS.is_absolute():
    WS = (TOOL_DIR / WS).resolve()

vid = sys.argv[1] if len(sys.argv) > 1 else "h5gOAne5G24"
n = int(sys.argv[2]) if len(sys.argv) > 2 else 40
d = WS / vid

# 取已有结果中非空文本的前 n 帧
ref = {}
tsv = d / "ocr_out.tsv"
with open(tsv, encoding="utf-8") as f:
    for r in csv.DictReader(f, delimiter="\t"):
        if r["text"].strip():
            ref[r["rep_frame"]] = r["text"].strip()
frames = list(ref.items())[:n]

ocr = PaddleOCR(lang=CONF.get("ocr_lang", "chinese_cht"),
                use_doc_orientation_classify=False,
                use_doc_unwarping=False,
                use_textline_orientation=False,
                enable_mkldnn=False)

lo, hi = CONF.get("box_cx_min", 0.2), CONF.get("box_cx_max", 0.8)


def do(img):
    w_ = img.shape[1]
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
    return " | ".join(segs)


print(f"=== threads={N_TH} | vid={vid} | frames={len(frames)} ===")
diff = 0
t0 = time.time()
for name, old in frames:
    img = cv2.imread(str(d / "reps" / name))
    new = do(img)
    if new != old:
        diff += 1
        print(f"DIFF {name}\n  ref: {old}\n  new: {new}")
dt = time.time() - t0
print(f"--- mismatches={diff}/{len(frames)}  rate={len(frames)/dt*60:.1f} img/min  total={dt:.1f}s ---")
