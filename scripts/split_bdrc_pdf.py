#!/usr/bin/env python3
"""Split a BDRC volume PDF into per-page JPEGs (batched to avoid memory/timeout)."""
import argparse
import os
from pdf2image import convert_from_path

BATCH = 25


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf", required=True)
    parser.add_argument("--vol", type=int, required=True)
    parser.add_argument("--output-dir", default="data/references/tibetan/bdrc/T00AG0322/images")
    parser.add_argument("--dpi", type=int, default=150)
    args = parser.parse_args()

    vol_dir = os.path.join(args.output_dir, f"vol_{args.vol:03d}")
    os.makedirs(vol_dir, exist_ok=True)

    # determine total pages
    from pypdf import PdfReader
    total = len(PdfReader(args.pdf).pages)
    print(f"vol {args.vol}: {total} pages")

    for start in range(1, total + 1, BATCH):
        end = min(start + BATCH - 1, total)
        pages = convert_from_path(args.pdf, dpi=args.dpi, fmt="jpeg",
                                 first_page=start, last_page=end)
        for i, img in enumerate(pages):
            pg = start + i
            out = os.path.join(vol_dir, f"{pg:04d}.jpg")
            img.save(out, "JPEG", quality=90)
        print(f"  done {end}/{total}")
    print(f"Done: {total} pages -> {vol_dir}")


if __name__ == "__main__":
    main()
