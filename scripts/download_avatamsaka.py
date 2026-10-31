#!/usr/bin/env python3
"""Download Tibetan Avatamsaka Sutra (华严经) images from BDRC IIIF.

Strategy (auto-fallback):
  1. Direct IIIF with a header matrix (cheap; usually blocked -> 0 bytes).
  2. Headless-browser fetch via Playwright (intercept image responses).
  3. Generate a URL manifest for manual download if all automated paths fail.

Usage:
    python download_avatamsaka.py --start-vol 89 --end-vol 94 --output-dir data/references/tibetan/bdrc/T00AG0322/images
    python download_avatamsaka.py --verify --output-dir ...
    python download_avatamsaka.py --manifest-only --output-dir ...
"""

import argparse
import json
import os
import time
import urllib.request
import urllib.error

VOLUMES = {
    89: ("I1PD105152", 567),
    90: ("I1PD105153", 573),
    91: ("I1PD105154", 591),
    92: ("I1PD105155", 525),
    93: ("I1PD105156", 593),
    94: ("I1PD105157", 573),
}

IIIF_URL = "https://iiif.bdrc.io/bdr:{vol_id}::bdr:{vol_id}{page:04d}.jpg/full/full/0/default.jpg"

BROWSER_HEADERS = {
    "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                   "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"),
    "Accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
    "Referer": "https://library.bdrc.io/",
    "Sec-Fetch-Dest": "image",
    "Sec-Fetch-Mode": "no-cors",
    "Sec-Fetch-Site": "cross-site",
}

HEADER_MATRIX = [
    {},
    {"User-Agent": "Mozilla/5.0"},
    BROWSER_HEADERS,
]


def is_jpeg(data: bytes) -> bool:
    return len(data) > 1024 and data[:3] == b"\xff\xd8\xff"


def atomic_write(path: str, data: bytes) -> None:
    tmp = path + ".tmp"
    with open(tmp, "wb") as f:
        f.write(data)
    os.replace(tmp, path)


def try_direct(vol_id: str, page: int, delay: float) -> bytes | None:
    url = IIIF_URL.format(vol_id=vol_id, page=page)
    for hdrs in HEADER_MATRIX:
        try:
            req = urllib.request.Request(url, headers=hdrs)
            with urllib.request.urlopen(req, timeout=30) as r:
                data = r.read()
            if is_jpeg(data):
                return data
        except Exception:
            pass
        time.sleep(delay)
    return None


def try_browser(vol_id: str, pages: list[int], out_dir: str, delay: float) -> dict[int, bool]:
    """Use Playwright to fetch images by intercepting network responses."""
    from playwright.sync_api import sync_playwright

    results = {p: False for p in pages}
    captured: dict[int, bytes] = {}

    def on_response(resp):
        url = resp.url
        # match ...I1PDxxxxNNNN.jpg/...
        for p in pages:
            token = f"{vol_id}{p:04d}.jpg"
            if token in url and resp.status == 200:
                try:
                    body = resp.body()
                    if is_jpeg(body):
                        captured[p] = body
                except Exception:
                    pass

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        ctx = browser.new_context()
        page = ctx.new_page()
        page.on("response", on_response)
        # Open BDRC viewer for this volume to trigger image loads
        viewer_url = f"https://library.bdrc.io/show/bdr:{vol_id}"
        try:
            page.goto(viewer_url, wait_until="networkidle", timeout=60000)
        except Exception:
            pass
        # scroll/paginate to force more loads is volume-specific; rely on captured set
        time.sleep(5)
        browser.close()

    for p, data in captured.items():
        path = os.path.join(out_dir, f"{p:04d}.jpg")
        atomic_write(path, data)
        results[p] = True
    return results


def generate_manifest(out_dir: str, start_vol: int, end_vol: int) -> str:
    manifest_path = os.path.join(out_dir, "bdrc_urls.txt")
    lines = []
    for vol_num in range(start_vol, end_vol + 1):
        if vol_num not in VOLUMES:
            continue
        vol_id, total = VOLUMES[vol_num]
        for page in range(1, total + 1):
            url = IIIF_URL.format(vol_id=vol_id, page=page)
            lines.append(f"vol_{vol_num:03d}\t{page:04d}\t{url}")
    with open(manifest_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return manifest_path


def verify(out_dir: str) -> dict:
    report = {}
    for vol_num, (vol_id, total) in VOLUMES.items():
        vol_dir = os.path.join(out_dir, f"vol_{vol_num:03d}")
        ok = 0
        bad = 0
        missing = 0
        if os.path.isdir(vol_dir):
            for page in range(1, total + 1):
                path = os.path.join(vol_dir, f"{page:04d}.jpg")
                if not os.path.exists(path):
                    missing += 1
                    continue
                with open(path, "rb") as f:
                    data = f.read()
                if is_jpeg(data):
                    ok += 1
                else:
                    bad += 1
        else:
            missing = total
        report[vol_num] = {"expected": total, "ok": ok, "bad": bad, "missing": missing}
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--start-vol", type=int, default=89)
    parser.add_argument("--end-vol", type=int, default=94)
    parser.add_argument("--output-dir", default="data/references/tibetan/bdrc/T00AG0322/images")
    parser.add_argument("--delay", type=float, default=1.0)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--manifest-only", action="store_true")
    parser.add_argument("--browser", action="store_true", help="Use Playwright browser fetch")
    parser.add_argument("--retry-missing", action="store_true",
                        help="Write missing/bad URLs to missing_urls.txt for targeted re-download")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    if args.manifest_only:
        p = generate_manifest(args.output_dir, args.start_vol, args.end_vol)
        print(f"Manifest written: {p}")
        return

    if args.verify:
        rep = verify(args.output_dir)
        print(json.dumps(rep, indent=2, ensure_ascii=False))
        return

    if args.retry_missing:
        rep = verify(args.output_dir)
        missing_lines = []
        for vol_num, (vol_id, total) in VOLUMES.items():
            vol_dir = os.path.join(args.output_dir, f"vol_{vol_num:03d}")
            for page in range(1, total + 1):
                path = os.path.join(vol_dir, f"{page:04d}.jpg")
                bad = True
                if os.path.exists(path):
                    with open(path, "rb") as f:
                        if is_jpeg(f.read()):
                            bad = False
                if bad:
                    url = IIIF_URL.format(vol_id=vol_id, page=page)
                    missing_lines.append(f"vol_{vol_num:03d}\t{page:04d}\t{url}")
        out = os.path.join(args.output_dir, "missing_urls.txt")
        with open(out, "w", encoding="utf-8") as f:
            f.write("\n".join(missing_lines) + ("\n" if missing_lines else ""))
        print(f"Missing/bad: {len(missing_lines)} -> {out}")
        return

    log_path = os.path.join(args.output_dir, "_download_log.json")
    log = {}
    if os.path.exists(log_path):
        with open(log_path, encoding="utf-8") as f:
            log = json.load(f)

    for vol_num in range(args.start_vol, args.end_vol + 1):
        if vol_num not in VOLUMES:
            continue
        vol_id, total = VOLUMES[vol_num]
        vol_dir = os.path.join(args.output_dir, f"vol_{vol_num:03d}")
        os.makedirs(vol_dir, exist_ok=True)
        print(f"\n=== Volume {vol_num} ({vol_id}, {total} pages) ===")

        if args.browser:
            pages = [p for p in range(1, total + 1)
                     if not (args.resume and os.path.exists(os.path.join(vol_dir, f"{p:04d}.jpg")))]
            res = try_browser(vol_id, pages, vol_dir, args.delay)
            ok = sum(1 for v in res.values() if v)
            print(f"  browser fetched {ok}/{len(pages)}")
            continue

        succ = 0
        fail = 0
        for page in range(1, total + 1):
            out_path = os.path.join(vol_dir, f"{page:04d}.jpg")
            if args.resume and os.path.exists(out_path):
                with open(out_path, "rb") as f:
                    if is_jpeg(f.read()):
                        succ += 1
                        continue
            data = try_direct(vol_id, page, args.delay)
            if data is not None:
                atomic_write(out_path, data)
                succ += 1
                log[f"{vol_num}:{page}"] = {"status": "ok", "bytes": len(data)}
            else:
                fail += 1
                log[f"{vol_num}:{page}"] = {"status": "fail"}
            if page % 50 == 0 or page == total:
                print(f"  Progress: {page}/{total} (ok={succ}, fail={fail})")
            time.sleep(args.delay)

        print(f"  Volume {vol_num}: {succ} ok, {fail} failed")
        with open(log_path, "w", encoding="utf-8") as f:
            json.dump(log, f, ensure_ascii=False, indent=1)

    # always (re)generate manifest for manual fallback
    mp = generate_manifest(args.output_dir, args.start_vol, args.end_vol)
    print(f"\nManifest (manual fallback): {mp}")
    print("Done.")


if __name__ == "__main__":
    main()
