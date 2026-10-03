# -*- coding: utf-8 -*-
"""_lib_extract.py — 一次性文本抽取（祖师大德 CBETA PDF → 工作区内 UTF-8 txt）。

从 C:\\华严\\经典著作 中按 CBETA 编号匹配 PDF，用 pypdf 抽取文字层，
写入 data/references/cbeta_txt/。仅为构建可回源的对读/引文语料，非交付物。
"""
import os
import sys
import pypdf

SRC_DIR = r"C:\华严\经典著作"
OUT_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data", "references", "cbeta_txt",
)

# CBETA 编号 -> (输出文件名, 著者题)
TARGETS = {
    "CBETA_T1735": ("T1735_澄观_华严经疏.txt", "唐澄观《大方广佛华严经疏》"),
    "CBETA_T1736": ("T1736_澄观_随疏演义钞.txt", "唐澄观《华严经随疏演义钞》"),
    "CBETA_T1733": ("T1733_法藏_探玄记.txt", "唐法藏《华严经探玄记》"),
    "CBETA_T1732": ("T1732_法藏_搜玄记.txt", "唐法藏《华严经搜玄分齐通智方轨》"),
    "CBETA_T1739": ("T1739_李通玄_新华严经论.txt", "唐李通玄《新华严经论》"),
    "CBETA_X0223": ("X0223_李通玄_华严经合论.txt", "唐李通玄《华严经合论》"),
    "CBETA_L1557": ("L1557_澄观_华严经疏钞会本.txt", "《华严经疏钞会本》"),
    "CBETA_B0002": ("B0002_道霈_华严经疏论纂要.txt", "清道霈《华严经疏论纂要》"),
}


def find_pdf(siglum):
    for fn in os.listdir(SRC_DIR):
        if siglum in fn and fn.lower().endswith(".pdf"):
            return os.path.join(SRC_DIR, fn)
    return None


def extract(pdf_path, out_name, title):
    r = pypdf.PdfReader(pdf_path)
    n = len(r.pages)
    chunks = ["# %s\n# 来源 PDF: %s\n# 共 %d 页\n\n" % (title, os.path.basename(pdf_path), n)]
    for i, page in enumerate(r.pages):
        try:
            t = page.extract_text() or ""
        except Exception as e:  # noqa: BLE001
            t = "\n[[PAGE %d ERROR: %s]]\n" % (i, e)
        chunks.append("\n<<<PAGE %d>>>\n" % i)
        chunks.append(t)
    out = os.path.join(OUT_DIR, out_name)
    with open(out, "w", encoding="utf-8") as f:
        f.write("".join(chunks))
    print("  OK %-42s pages=%-5d -> %s" % (os.path.basename(pdf_path)[:40], n, out_name))


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    only = sys.argv[1:] or list(TARGETS)
    for sig, (out_name, title) in TARGETS.items():
        if only and sig not in only:
            continue
        pdf = find_pdf(sig)
        if not pdf:
            print("  MISS %s (未找到 PDF)" % sig)
            continue
        print(">> %s %s" % (sig, title))
        try:
            extract(pdf, out_name, title)
        except Exception as e:  # noqa: BLE001
            print("  FAIL %s: %s" % (sig, e))
    print("done ->", OUT_DIR)


if __name__ == "__main__":
    main()
