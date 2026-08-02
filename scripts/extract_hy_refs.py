#!/usr/bin/env python3
"""Extract text from Huayan reference PDFs in docs/hy_refs/ → docs/hy_refs/text/
Builds a catalog knowledge graph JSON for downstream content updates.

Usage: python scripts/extract_hy_refs.py
"""
import os, sys, json, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REFS_DIR = os.path.join(ROOT, "docs", "hy_refs")
OUT_DIR = os.path.join(REFS_DIR, "text")
os.makedirs(OUT_DIR, exist_ok=True)

# ── Helper: extract text from PDF ──
def extract_pdf(filepath, max_pages=None):
    """Extract text from PDF using PyPDF2. max_pages limits for large files."""
    from PyPDF2 import PdfReader
    try:
        reader = PdfReader(filepath)
        total = len(reader.pages)
        pages = min(total, max_pages or total)
        texts = []
        for i in range(pages):
            try:
                page = reader.pages[i]
                t = page.extract_text()
                if t and t.strip():
                    texts.append(f"## Page {i+1}\n\n{t.strip()}")
            except Exception as e:
                texts.append(f"## Page {i+1}\n\n[Extraction error: {e}]")
        return {
            "total_pages": total,
            "extracted_pages": pages,
            "text": "\n\n".join(texts),
            "truncated": max_pages and total > max_pages
        }
    except Exception as e:
        return {"error": str(e), "total_pages": 0, "extracted_pages": 0, "text": ""}

# ── File catalog ──
FILES = [
    {
        "file": "《堪玄记 一》（华严经枢纽）.pdf",
        "max_pages": None,  # small file, extract all
        "category": "勘玄记",
        "label": "堪玄记一·华严经枢纽",
        "desc": "《华严经》枢纽——对华严经整体的玄义解析"
    },
    {
        "file": "《勘玄记 三》（普贤行愿品—华严经总结）.pdf",
        "max_pages": 200,  # 211MB, limit extraction
        "category": "勘玄记",
        "label": "勘玄记三·普贤行愿品",
        "desc": "普贤行愿品——华严经总结"
    },
    {
        "file": "《勘玄记04》（离世间品）--.pdf",
        "max_pages": 200,  # 594MB, limit extraction
        "category": "勘玄记",
        "label": "勘玄记四·离世间品",
        "desc": "离世间品——华严经修行实践的总结"
    },
    {
        "file": "《華嚴經》〈淨行品〉剖裂玄義疏(1).pdf",
        "max_pages": 150,
        "category": "玄义疏",
        "label": "净行品剖裂玄义疏",
        "desc": "《华严经·净行品》玄义解析——前行阶段核心经典"
    },
    {
        "file": "华藏妙海 部分听经笔记整理版.pdf",
        "max_pages": None,  # already extracted, but re-extract for completeness
        "category": "听经笔记",
        "label": "华藏妙海·听经笔记",
        "desc": "海云继梦和上讲经听记整理——含三段教学、结界工程、华严三品等"
    },
    {
        "file": '图解华严经：读懂“经中之王” (龙树菩萨释著) (Z-Library).pdf',
        "max_pages": 100,
        "category": "图解",
        "label": "图解华严经·龙树菩萨释",
        "desc": "以图解方式阐释华严经——龙树菩萨释著"
    },
]

# ── Process files ──
catalog = {"version": "0.1.0", "last_updated": "2026-08-02", "source_dir": "docs/hy_refs", "entries": []}

print("=" * 60)
print("华严文献提取工具")
print("=" * 60)

for entry in FILES:
    fname = entry["file"]
    fpath = os.path.join(REFS_DIR, fname)
    if not os.path.exists(fpath):
        print(f"⚠  SKIP (not found): {fname}")
        continue

    fsize = os.path.getsize(fpath)
    print(f"\n📄 {fname} ({fsize/1024/1024:.1f}MB)")

    result = extract_pdf(fpath, entry["max_pages"])

    if "error" in result:
        print(f"   ❌ Error: {result['error']}")
        catalog["entries"].append({**entry, "error": result["error"]})
        continue

    print(f"   ✅ Extracted {result['extracted_pages']}/{result['total_pages']} pages"
          + (" (truncated)" if result.get("truncated") else ""))

    # Save as markdown
    safe_name = fname.replace(".pdf", ".md").replace('"', '').replace('《','').replace('》','')
    out_path = os.path.join(OUT_DIR, safe_name)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(f"# {entry['label']}\n\n")
        f.write(f"**来源:** {fname}\n\n")
        f.write(f"**类别:** {entry['category']}\n\n")
        f.write(f"**描述:** {entry['desc']}\n\n")
        f.write(f"**提取页数:** {result['extracted_pages']}/{result['total_pages']}页\n\n")
        if result.get("truncated"):
            f.write("> ⚠ 文件较大,仅提取了部分页面。完整内容请参阅原始PDF。\n\n")
        f.write("---\n\n")
        f.write(result["text"])

    # Add to catalog
    entry_info = {k: v for k, v in entry.items() if k != "file"}
    entry_info["filename"] = fname
    entry_info["output"] = out_path
    entry_info["pages_extracted"] = result["extracted_pages"]
    entry_info["pages_total"] = result["total_pages"]
    catalog["entries"].append(entry_info)

# ── Save catalog JSON ──
catalog_path = os.path.join(OUT_DIR, "_catalog.json")
with open(catalog_path, "w", encoding="utf-8") as f:
    json.dump(catalog, f, ensure_ascii=False, indent=2)

print(f"\n{'=' * 60}")
print(f"完成! 提取 {len(catalog['entries'])} 个文件")
print(f"输出目录: {OUT_DIR}")
print(f"目录文件: {catalog_path}")
print(f"{'=' * 60}")
