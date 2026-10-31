#!/usr/bin/env python3
"""Automate BDRC volume PDF download via Playwright (cookie auth).

Prereq: export BDRC session cookies to `bdrc_cookies.txt` (Netscape format) in repo root.
Run:  python scripts/bdrc_pdf_download.py --vol 89  (or --all)
"""
import argparse
import os
import time

VOLUMES = {
    89: "I1PD105152", 90: "I1PD105153", 91: "I1PD105154",
    92: "I1PD105155", 93: "I1PD105156", 94: "I1PD105157",
}

OUT_DIR = "data/references/tibetan/bdrc/T00AG0322/images"
PDF_DIR = "_bdrc_pdfs"


def load_cookies(path):
    cookies = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t")
            if len(parts) < 7:
                continue
            domain, flag, path_, secure, expiry, name, value = parts[:7]
            cookies.append({
                "name": name, "value": value, "domain": domain.lstrip("."),
                "path": path_, "secure": secure.upper() == "TRUE",
                "expires": int(expiry) if expiry.isdigit() else -1,
            })
    return cookies


def download_one_cdp(vol_num, vol_id, cdp_url, timeout):
    from playwright.sync_api import sync_playwright
    pdf_path = os.path.join(PDF_DIR, f"vol_{vol_num:03d}.pdf")
    if os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 1024:
        print(f"  vol {vol_num}: PDF already present, skipping")
        return pdf_path

    url = f"https://library.bdrc.io/show/bdr:{vol_id}"
    with sync_playwright() as pw:
        browser = pw.chromium.connect_over_cdp(cdp_url)
        ctx = browser.contexts[0] if browser.contexts else browser.new_context(accept_downloads=True)
        page = ctx.new_page()
        page.goto(url, wait_until="networkidle", timeout=60000)

        if "login" in page.url.lower() or "signin" in page.url.lower():
            browser.close()
            raise RuntimeError("Not authenticated — log in to BDRC in Brave first")

        try:
            page.locator("#DL").click(timeout=15000)
        except Exception:
            page.get_by_text("Download", exact=False).first.click(timeout=15000)
        time.sleep(1)
        try:
            page.get_by_text("PDF", exact=False).first.click(timeout=15000)
        except Exception:
            pass

        deadline = time.time() + timeout
        downloaded = None
        while time.time() < deadline:
            try:
                with page.expect_download(timeout=5000) as dl_info:
                    for sel in ["button:has-text('Download')", "a:has-text('Download')", "button:has-text('Generate')"]:
                        loc = page.locator(sel)
                        if loc.count() > 0:
                            loc.first.click(timeout=2000)
                            break
                downloaded = dl_info.value
                break
            except Exception:
                time.sleep(3)

        if downloaded is None:
            browser.close()
            raise RuntimeError(f"vol {vol_num}: PDF generation timed out")

        downloaded.save_as(pdf_path)
        page.close()
        browser.close()
    print(f"  vol {vol_num}: saved {pdf_path} ({os.path.getsize(pdf_path)} bytes)")
    return pdf_path


def download_one(vol_num, vol_id, timeout):
    from playwright.sync_api import sync_playwright
    pdf_path = os.path.join(PDF_DIR, f"vol_{vol_num:03d}.pdf")
    if os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 1024:
        print(f"  vol {vol_num}: PDF already present, skipping")
        return pdf_path

    url = f"https://library.bdrc.io/show/bdr:{vol_id}"
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        ctx = browser.new_context(accept_downloads=True)
        ctx.add_cookies(load_cookies("bdrc_cookies.txt"))
        page = ctx.new_page()
        page.goto(url, wait_until="networkidle", timeout=60000)

        # detect login redirect
        if "login" in page.url.lower() or "signin" in page.url.lower():
            browser.close()
            raise RuntimeError("Not authenticated — cookies expired/invalid")

        # click Download
        try:
            page.locator("#DL").click(timeout=15000)
        except Exception:
            page.get_by_text("Download", exact=False).first.click(timeout=15000)
        time.sleep(1)
        try:
            page.get_by_text("PDF", exact=False).first.click(timeout=15000)
        except Exception:
            pass

        # wait for generation: poll for a download link/button
        deadline = time.time() + timeout
        downloaded = None
        while time.time() < deadline:
            try:
                with page.expect_download(timeout=5000) as dl_info:
                    # try clicking a "Download" confirm button if present
                    for sel in ["button:has-text('Download')", "a:has-text('Download')", "button:has-text('Generate')"]:
                        loc = page.locator(sel)
                        if loc.count() > 0:
                            loc.first.click(timeout=2000)
                            break
                downloaded = dl_info.value
                break
            except Exception:
                time.sleep(3)

        if downloaded is None:
            browser.close()
            raise RuntimeError(f"vol {vol_num}: PDF generation timed out")

        downloaded.save_as(pdf_path)
        browser.close()
    print(f"  vol {vol_num}: saved {pdf_path} ({os.path.getsize(pdf_path)} bytes)")
    return pdf_path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--vol", type=int)
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--split", action="store_true", help="Split PDFs after download")
    parser.add_argument("--cdp", default=None, help="CDP URL, e.g. http://localhost:9222 (attach to running Brave)")
    args = parser.parse_args()

    os.makedirs(PDF_DIR, exist_ok=True)
    if not args.cdp and not os.path.exists("bdrc_cookies.txt"):
        raise SystemExit("Missing bdrc_cookies.txt — export cookies first (or use --cdp)")

    targets = list(VOLUMES) if args.all else ([args.vol] if args.vol else [])
    if not targets:
        raise SystemExit("Specify --vol N or --all")

    for v in targets:
        try:
            if args.cdp:
                download_one_cdp(v, VOLUMES[v], args.cdp, args.timeout)
            else:
                download_one(v, VOLUMES[v], args.timeout)
        except Exception as e:
            print(f"  vol {v}: ERROR {e}")
        time.sleep(30)

    if args.split:
        import subprocess
        for v in targets:
            pdf = os.path.join(PDF_DIR, f"vol_{v:03d}.pdf")
            if os.path.exists(pdf):
                subprocess.run(["python", "scripts/split_bdrc_pdf.py", "--pdf", pdf,
                                "--vol", str(v), "--output-dir", OUT_DIR], check=False)


if __name__ == "__main__":
    main()
