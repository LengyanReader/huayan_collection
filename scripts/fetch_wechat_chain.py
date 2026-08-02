#!/usr/bin/env python3
"""Follow the 下一篇 chain in WeChat 实修心要 articles to fetch them all.

Usage: python scripts/fetch_wechat_chain.py [START_URL]
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

def fetch_html(url):
    cmd = ["curl", "-sL", "--connect-timeout", "10", "--max-time", "30",
           "-H", f"User-Agent: {MOBILE_UA}",
           "-H", "Accept: text/html,application/xhtml+xml",
           "-H", "Accept-Language: zh-CN,zh;q=0.9", url]
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode != 0:
        return None
    try: return result.stdout.decode('utf-8')
    except: return result.stdout.decode('utf-8', errors='replace')

def parse_article(content, url):
    """Parse a WeChat article HTML and extract content + next link."""
    # Title from og:title
    m = re.search(r'<meta property="og:title" content="([^"]+)"', content)
    title = m.group(1).replace('实修心要 | ', '').strip() if m else "UNKNOWN"
    # Description
    m = re.search(r'<meta name="description" content="([^"]+)"', content)
    desc = m.group(1) if m else ""
    # Account nickname
    m = re.search(r'nickname\s*=\s*"([^"]*)"', content)
    nickname = m.group(1) if m else "永远的犍陀罗"
    try: nickname = nickname.encode('latin-1').decode('unicode_escape')
    except: pass

    # Extract NEXT article link from JS variable next_article_link
    m = re.search(r"next_article_link\s*:\s*'([^']+)'", content)
    next_url = None
    if m:
        next_url = m.group(1)
        next_url = next_url.replace('\\x26amp;', '&').replace('&amp;', '&')

    # Extract body text
    m = re.search(r'<div[^>]*id="js_content"[^>]*>(.*?)</div>\s*(?:<script|$)', content, re.DOTALL)
    body = ""
    if m:
        body = h.unescape(m.group(1))
        body = re.sub(r'<br\s*/?>', '\n', body)
        body = re.sub(r'<p[^>]*>', '\n', body)
        body = re.sub(r'</p>', '\n', body)
        body = re.sub(r'<img[^>]*>', '[图片]', body)
        # Preserve links
        body = re.sub(r'<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>', r'\2 (\1)', body)
        body = re.sub(r'<[^>]+>', '', body)
        body = re.sub(r'\n{3,}', '\n\n', body)
        body = body.strip()

    return {"title": title, "desc": desc, "nickname": nickname,
            "next_url": next_url, "body": body, "url": url}

def save_article(art, index):
    safe_title = re.sub(r'[\\/:*?"<>|]', '_', art["title"])
    fname = f"{index:02d}_{safe_title}.md"
    fpath = os.path.join(OUT_DIR, fname)
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(f"# {art['title']}\n\n")
        f.write(f"**来源:** {art['nickname']} · 实修心要专辑\n\n")
        f.write(f"**摘要:** {art['desc']}\n\n")
        f.write(f"**原文:** {art['url']}\n\n")
        if art.get('next_url'):
            f.write(f"**下一篇:** {art['next_url']}\n\n")
        f.write(f"**提取日期:** 2026-08-02\n\n---\n\n")
        f.write(art["body"])
    return fpath

def main():
    start_url = sys.argv[1] if len(sys.argv) > 1 else \
        "https://mp.weixin.qq.com/s/S2D9BOc3jFwDRQr2tbzG6g"

    print("=" * 60)
    print("实修心要文章链抓取")
    print("=" * 60)

    url = start_url
    articles = []
    visited = set()

    for i in range(1, 50):  # max 50 articles
        aid = url.rstrip('/').split('/')[-1]
        if aid in visited:
            print(f"\n⚠ Loop detected at article {i}")
            break
        visited.add(aid)

        print(f"\n[{i}] {url}")
        html = fetch_html(url)
        if not html or len(html) < 500:
            print(f"  ❌ Failed to fetch (anti-bot?)")
            break

        art = parse_article(html, url)
        print(f"  ✅ {art['title']}")
        print(f"     Body: {len(art['body'])} chars")
        if art['next_url']:
            print(f"     Next: {art['next_url'][:60]}...")

        fpath = save_article(art, i)
        print(f"     Saved: {os.path.basename(fpath)}")
        articles.append(art)

        if not art['next_url']:
            print("\n🏁 No more articles (end of chain)")
            break
        url = art['next_url']

    # Save catalog
    cat = {"version": "0.2.0", "date": "2026-08-02", "count": len(articles),
           "articles": [{"idx": j+1, "title": a["title"], "url": a["url"],
                         "next": a.get("next_url","")} for j, a in enumerate(articles)]}
    cat_path = os.path.join(OUT_DIR, "_chain_catalog.json")
    with open(cat_path, "w", encoding="utf-8") as f:
        json.dump(cat, f, ensure_ascii=False, indent=2)

    print(f"\n{'=' * 60}")
    print(f"完成! {len(articles)} 篇文章")
    print(f"目录: {cat_path}")
    print(f"{'=' * 60}")

if __name__ == '__main__':
    main()
