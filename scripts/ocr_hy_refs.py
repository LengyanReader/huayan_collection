#!/usr/bin/env python3
"""OCR scanned Huayan reference PDFs using PaddleOCR.

Requirements: pip install paddlepaddle paddleocr PyPDF2 pdf2image
  ALSO requires poppler (system-level PDF renderer):
    Windows: download from https://github.com/oschwartz10612/poppler-windows/releases/
             extract to e.g. C:\poppler\bin, add to PATH
    Linux:   apt-get install poppler-utils
    Mac:     brew install poppler
Usage: python scripts/ocr_hy_refs.py [--file FILENAME] [--pages N]

For large scanned PDFs, extracts text page-by-page via:
  1. pdf2image converts PDF pages to PNG images
  2. PaddleOCR recognizes Chinese text from images
  3. Output saved as markdown in docs/hy_refs/text/
"""
import os, sys, io, json, argparse

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REFS_DIR = os.path.join(ROOT, "docs", "hy_refs")
OUT_DIR = os.path.join(REFS_DIR, "text")
os.makedirs(OUT_DIR, exist_ok=True)

# ── Files needing OCR (large scanned PDFs with minimal text extraction) ──
OCR_TARGETS = [
    {
        "file": "《堪玄记 一》（华严经枢纽）.pdf",
        "label": "堪玄记一·华严经枢纽",
        "desc": "《华严经》枢纽——海云继梦和上对华严经整体的玄义解析",
    },
    {
        "file": "《勘玄记 三》（普贤行愿品—华严经总结）.pdf",
        "label": "勘玄记三·普贤行愿品",
        "desc": "普贤行愿品——华严经总结",
    },
    {
        "file": "《勘玄记04》（离世间品）--.pdf",
        "label": "勘玄记四·离世间品",
        "desc": "离世间品——华严经修行实践的总结",
    },
]

def ocr_pdf(filepath, max_pages=10):
    """OCR a PDF using PaddleOCR. max_pages limits for large files."""
    try:
        from pdf2image import convert_from_path
        from paddleocr import PaddleOCR
    except ImportError as e:
        return {"error": f"Missing dependency: {e}. Install: pip install pdf2image paddleocr"}

    try:
        ocr = PaddleOCR(lang='ch', use_angle_cls=True, show_log=False)
    except Exception as e:
        return {"error": f"PaddleOCR init failed: {e}"}

    print(f"  Converting PDF to images...")
    try:
        images = convert_from_path(filepath, dpi=200, first_page=1, last_page=max_pages)
    except Exception as e:
        return {"error": f"PDF to image conversion failed: {e}. Install poppler: https://github.com/oschwartz10612/poppler-windows/releases/"}

    print(f"  OCR processing {len(images)} pages...")
    texts = []
    for i, img in enumerate(images):
        try:
            result = ocr.ocr(img, cls=True)
            page_text = []
            if result and result[0]:
                for line in result[0]:
                    if line and len(line) >= 2:
                        page_text.append(line[1][0])
            text = '\n'.join(page_text)
            if text.strip():
                texts.append(f"## 第 {i+1} 页\n\n{text.strip()}")
            if (i + 1) % 5 == 0:
                print(f"    Page {i+1}/{len(images)} done")
        except Exception as e:
            texts.append(f"## 第 {i+1} 页\n\n[OCR error: {e}]")

    return {
        "total_pages_processed": len(images),
        "text": "\n\n".join(texts),
    }


def main():
    parser = argparse.ArgumentParser(description="OCR Huayan reference PDFs")
    parser.add_argument("--file", help="Specific PDF filename to OCR")
    parser.add_argument("--pages", type=int, default=10, help="Max pages to OCR (default: 10)")
    args = parser.parse_args()

    targets = OCR_TARGETS
    if args.file:
        targets = [t for t in OCR_TARGETS if t["file"] == args.file]
        if not targets:
            print(f"File not in OCR targets: {args.file}")
            return

    print("=" * 60)
    print("华严文献 OCR 提取工具 (PaddleOCR)")
    print("=" * 60)

    results = []
    for entry in targets:
        fpath = os.path.join(REFS_DIR, entry["file"])
        if not os.path.exists(fpath):
            print(f"\n⚠ SKIP (not found): {entry['file']}")
            continue

        fsize = os.path.getsize(fpath)
        pages = min(args.pages, 30) if fsize > 200*1024*1024 else args.pages
        print(f"\n📄 {entry['file']} ({fsize/1024/1024:.1f}MB, {pages} pages)")

        result = ocr_pdf(fpath, pages)
        if "error" in result:
            print(f"   ❌ {result['error']}")
            results.append({**entry, "error": result["error"]})
            continue

        # Save markdown
        safe_name = entry["file"].replace(".pdf", "_ocr.md").replace('"','').replace('《','').replace('》','')
        out_path = os.path.join(OUT_DIR, safe_name)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(f"# {entry['label']} (OCR提取)\n\n")
            f.write(f"**来源:** {entry['file']}\n\n")
            f.write(f"**描述:** {entry['desc']}\n\n")
            f.write(f"**OCR页数:** {result['total_pages_processed']}\n\n")
            f.write("> ⚠ 此文件由PaddleOCR自动识别提取,可能存在识别错误。建议对照原始PDF使用。\n\n")
            f.write("---\n\n")
            f.write(result["text"])

        print(f"   ✅ Saved: {out_path} ({len(result['text'])} chars)")
        results.append({**entry, "output": out_path, "chars": len(result['text'])})

    # Save OCR catalog
    cat_path = os.path.join(OUT_DIR, "_ocr_catalog.json")
    with open(cat_path, "w", encoding="utf-8") as f:
        json.dump({"version": "0.1.0", "date": "2026-08-02", "results": results}, f, ensure_ascii=False, indent=2)

    print(f"\n{'=' * 60}")
    print(f"完成! OCR处理 {len(results)} 个文件")
    print(f"输出: {OUT_DIR}")
    print(f"{'=' * 60}")


if __name__ == '__main__':
    main()
