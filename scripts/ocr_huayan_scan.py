# -*- coding: utf-8 -*-
"""OCR image-only scanned Huayan PDFs into a durable local reference corpus.

RapidOCR (onnxruntime) pipeline — pure-pip, CPU-friendly, no PaddleOCR/mkldnn
pitfall. Pairs with the existing scripts/ocr_hy_refs.py (PaddleOCR path) but is
the working route when paddle is unavailable.

Output convention: raw OCR corpus goes to docs/hy_refs/text/ (kept LOCAL —
.gitignore `docs/hy_refs/*` intentionally excludes raw 语料原件 from git). This
script itself is tracked so the run is reproducible and resumable.

Usage:
  python scripts/ocr_huayan_scan.py --src "C:\\华严\\经典著作\\《堪玄记 一》（华严经枢纽）.pdf" \
      --label 勘玄记_华严经枢纽 --start 1 --end 232 [--dpi 200] [--batch 8]

Resumable: re-run the same command; a sidecar checkpoint (*.ckpt.json) records
finished pages and they are skipped. Progress prints ASCII-safe on Windows.
"""
import os, sys, io, json, time, hashlib, argparse

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEXT_DIR = os.path.join(ROOT, "docs", "hy_refs", "text")
os.makedirs(TEXT_DIR, exist_ok=True)

POPPLER = r"c:\poppler\poppler-24.08.0\Library\bin"


def total_pages(src):
    import pypdf
    return len(pypdf.PdfReader(src).pages)


def main():
    ap = argparse.ArgumentParser(description="RapidOCR scan → durable corpus")
    ap.add_argument("--src", required=True, help="absolute path to scanned PDF")
    ap.add_argument("--label", required=True, help="safe output name (no spaces/punct)")
    ap.add_argument("--start", type=int, default=1)
    ap.add_argument("--end", type=int, default=0, help="0 = through last page")
    ap.add_argument("--dpi", type=int, default=200)
    ap.add_argument("--batch", type=int, default=8)
    args = ap.parse_args()

    if not os.path.exists(args.src):
        print(f"[ERR] source not found: {args.src}"); return
    from pdf2image import convert_from_path
    from rapidocr_onnxruntime import RapidOCR
    import numpy as np

    npages = total_pages(args.src)
    end = args.end or npages
    out_md = os.path.join(TEXT_DIR, f"{args.label}.md")
    ckpt = os.path.join(TEXT_DIR, f"{args.label}.ckpt.json")
    done = set(json.load(open(ckpt, encoding="utf-8"))) if os.path.exists(ckpt) else set()

    if not os.path.exists(out_md):
        with open(out_md, "w", encoding="utf-8") as f:
            f.write(f"# {args.label}（RapidOCR 自动提取）\n\n")
            f.write(f"**来源:** {os.path.basename(args.src)}  \n")
            f.write(f"**总页数:** {npages}  \n**产出:** {time.strftime('%Y-%m-%d %H:%M')}\n\n")
            f.write("> ⚠ 本文件由 RapidOCR 从扫描图自动识别，可能存在个别字句误识（尤以手写/异体字）。\n")
            f.write("> 引用前须对照原始 PDF 校正；本语料仅作文义参考，不逐字入正文。\n\n---\n")

    ocr = RapidOCR()
    print(f"[{args.label}] OCR pages {args.start}-{end} of {npages}; already done {len(done)}", flush=True)
    p = args.start
    while p <= end:
        hi = min(p + args.batch - 1, end)
        todo = [q for q in range(p, hi + 1) if q not in done]
        if todo:
            t0 = time.time()
            imgs = convert_from_path(args.src, dpi=args.dpi, first_page=p, last_page=hi, poppler_path=POPPLER)
            pmap = {p + k: im for k, im in enumerate(imgs)}
            with open(out_md, "a", encoding="utf-8") as f:
                for q in todo:
                    im = pmap.get(q)
                    if im is None:
                        continue
                    res, _ = ocr(np.array(im))
                    txt = "\n".join(l[1] for l in res) if res else ""
                    f.write(f"\n\n<!-- page {q} -->\n{txt}\n")
                    done.add(q)
            json.dump(sorted(done), open(ckpt, "w", encoding="utf-8"))
            print(f"  pages {p}-{hi} ok ({time.time()-t0:.1f}s) · cumulative {len(done)}", flush=True)
        p = hi + 1
    print(f"[{args.label}] DONE. corpus: {out_md}", flush=True)


if __name__ == "__main__":
    main()
