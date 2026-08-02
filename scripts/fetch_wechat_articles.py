#!/usr/bin/env python3
"""Fetch WeChat public account articles using mobile user-agent.

Usage: python scripts/fetch_wechat_articles.py URL [URL2 ...]

The script fetches each article, extracts title/metadata/content,
and saves as markdown in docs/hy_refs/wechat/
"""
import sys, os, re, json, subprocess, io, html as h

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "docs", "hy_refs", "wechat")
os.makedirs(OUT_DIR, exist_ok=True)

MOBILE_UA = (
    "Mozilla/5.0 (Linux; Android 10; K) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/115.0.0.0 Mobile Safari/537.36"
)

def fetch_article(url):
    """Fetch a WeChat article and extract content."""
    import subprocess
    cmd = [
        "curl", "-sL", "--connect-timeout", "10", "--max-time", "30",
        "-H", f"User-Agent: {MOBILE_UA}",
        "-H", "Accept: text/html,application/xhtml+xml",
        "-H", "Accept-Language: zh-CN,zh;q=0.9",
        url
    ]
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode != 0:
        return {"error": f"curl failed: {result.stderr.decode('utf-8','ignore')}"}

    # Decode from bytes, trying UTF-8 first
    raw = result.stdout
    try:
        content = raw.decode('utf-8')
    except UnicodeDecodeError:
        content = raw.decode('utf-8', errors='replace')
    if not content or len(content) < 500:
        return {"error": "Empty or too-short response (anti-bot block?)"}

    # Extract metadata - try multiple methods
    meta = {}
    # Method 1: og:title meta tag
    m = re.search(r'<meta property="og:title" content="([^"]+)"', content)
    if m: meta['og_title'] = m.group(1)
    # Method 2: description meta
    m = re.search(r'<meta name="description" content="([^"]+)"', content)
    if m: meta['msg_desc'] = m.group(1)
    # Method 3: JS variables
    for pat in ['msg_title', 'nickname', 'create_time']:
        m = re.search(fr'{pat}\s*=\s*"([^"]*)"', content)
        if m and m.group(1):
            val = m.group(1)
            try: val = val.encode('latin-1').decode('unicode_escape')
            except: pass
            if val: meta[pat] = val
    # Derive title
    title = meta.get('og_title', '').replace('实修心要 | ', '').strip()
    if not title:
        title = meta.get('msg_title', 'UNKNOWN').strip()

    # Extract article body from js_content div
    m = re.search(r'<div[^>]*id="js_content"[^>]*>(.*?)</div>\s*<script', content, re.DOTALL)
    if not m:
        m = re.search(r'id="js_content"[^>]*>(.*?)</div>', content, re.DOTALL)

    body_text = ""
    if m:
        body_text = m.group(1)
        # Decode HTML entities
        body_text = h.unescape(body_text)
        # Remove HTML tags, keep structure
        body_text = re.sub(r'<br\s*/?>', '\n', body_text)
        body_text = re.sub(r'<p[^>]*>', '\n', body_text)
        body_text = re.sub(r'</p>', '\n', body_text)
        body_text = re.sub(r'<img[^>]*>', '[图片]', body_text)
        body_text = re.sub(r'<[^>]+>', '', body_text)
        # Clean up whitespace
        body_text = re.sub(r'\n{3,}', '\n\n', body_text)
        body_text = re.sub(r' +', ' ', body_text)
        body_text = body_text.strip()

    # Also extract image URLs
    images = re.findall(r'data-src="([^"]+)"', content)

    return {
        "url": url,
        "title": title,
        "account": meta.get("nickname", "永远的犍陀罗"),
        "description": meta.get("msg_desc", ""),
        "create_time": meta.get("create_time", ""),
        "source_url": meta.get("msg_source_url", ""),
        "body_length": len(body_text),
        "images_count": len(images),
        "body": body_text,
        "images": images[:5],
    }


def save_article(article):
    """Save article as markdown."""
    safe_title = re.sub(r'[\\/:*?"<>|]', '_', article["title"])
    fname = f"{safe_title}.md"
    fpath = os.path.join(OUT_DIR, fname)

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(f"# {article['title']}\n\n")
        f.write(f"**来源:** {article.get('account','?')} · 微信公众号「永远的犍陀罗」· 实修心要专辑\n\n")
        f.write(f"**摘要:** {article.get('description','')}\n\n")
        if article.get('source_url'):
            f.write(f"**原文链接:** {article['url']}\n\n")
        f.write(f"**提取日期:** 2026-08-02\n\n")
        f.write("---\n\n")
        f.write(article["body"])

    return fpath


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/fetch_wechat_articles.py URL [URL2 ...]")
        print("   or: python scripts/fetch_wechat_articles.py --file urls.txt")
        return

    urls = sys.argv[1:]
    results = []

    for i, url in enumerate(urls):
        print(f"\n[{i+1}/{len(urls)}] {url[:60]}...")
        article = fetch_article(url)
        if "error" in article:
            print(f"  ❌ {article['error']}")
            results.append(article)
            continue

        print(f"  ✅ {article['title']}")
        print(f"     Account: {article['account']}")
        print(f"     Body: {article['body_length']} chars, {article['images_count']} images")

        fpath = save_article(article)
        print(f"     Saved: {fpath}")
        results.append({"title": article["title"], "file": fpath, "url": url})

    # Save catalog
    cat_path = os.path.join(OUT_DIR, "_catalog.json")
    with open(cat_path, "w", encoding="utf-8") as f:
        json.dump({"version": "0.1.0", "date": "2026-08-02", "articles": results},
                  f, ensure_ascii=False, indent=2)
    print(f"\nDone. {len(results)} articles processed. Catalog: {cat_path}")


if __name__ == '__main__':
    main()
