#!/usr/bin/env python3
"""Verify web/demo build output (index + 6 tab pages) structure before deployment."""
import sys, os, re

# Windows console cp1252 下中文输出会 UnicodeEncodeError — 强制 UTF-8
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEMO = os.path.join(ROOT, 'web', 'demo')
ARTICLES = os.path.join(DEMO, 'articles')

TABS = ['lineage', 'gap', 'jiaoxing', 'frontier', 'cosmology', 'spirit']
TAB_TITLES = ['法脉传承', '华严文献', '教海行云', '前沿对话', '世主妙严', '灵性仁本']
DATA_VARS = {
    'lineage': ['var GRAPH'],
    'gap': ['var GAP'],
    'jiaoxing': ['var PRACTICE_DATA'],
    'frontier': ['var FRONTIER_DATA', 'var SPIRIT_DATA'],  # 任一即可
    'cosmology': ['var COSMOLOGY_DATA', 'var SPIRIT_DATA'],
    'spirit': ['var SPIRIT_DATA'],
}

errors = 0

def fail(msg):
    global errors
    errors += 1
    print(f'  FAIL: {msg}')

def ok(msg):
    print(f'  OK:   {msg}')

# ── index.html (导航主页) ──
idx_path = os.path.join(DEMO, 'index.html')
print(f'Verifying {idx_path}\n')
if not os.path.exists(idx_path):
    fail('index.html missing')
else:
    with open(idx_path, encoding='utf-8') as f:
        idx = f.read()
    ok(f'index.html ({len(idx):,} bytes)')
    if not idx.lstrip().startswith('<!DOCTYPE html>'):
        fail('index: missing <!DOCTYPE html>')
    else:
        ok('index: starts with <!DOCTYPE html>')
    if not idx.strip().endswith('</html>'):
        fail('index: must end with </html>')
    else:
        ok('index: ends with </html>')
    for t in TABS:
        if f'tabs/{t}.html' not in idx:
            fail(f'index: missing link to tabs/{t}.html')
    ok('index: links to all 6 tab pages')
    for title in TAB_TITLES:
        if title not in idx:
            fail(f'index: missing module title "{title}"')

print()

# ── 6 个 Tab 页面 ──
for t, title in zip(TABS, TAB_TITLES):
    path = os.path.join(DEMO, 'tabs', f'{t}.html')
    print(f'Verifying tabs/{t}.html ({title})')
    if not os.path.exists(path):
        fail(f'{t}: file missing')
        continue
    with open(path, encoding='utf-8') as f:
        html = f.read()

    # 结构
    if not html.lstrip().startswith('<!DOCTYPE html>'):
        fail(f'{t}: missing <!DOCTYPE html>')
    else:
        ok(f'{t}: DOCTYPE')
    if not html.strip().endswith('</html>'):
        fail(f'{t}: must end with </html>')
    else:
        ok(f'{t}: ends with </html>')

    # div 平衡 (此前多次空白页根因)
    opens = len(re.findall(r'<div\b', html))
    closes = html.count('</div>')
    if opens != closes:
        fail(f'{t}: div mismatch — {opens} open vs {closes} close')
    else:
        ok(f'{t}: div balanced ({opens})')

    # 数据变量已内嵌
    for var in DATA_VARS[t]:
        if var in html:
            ok(f'{t}: {var} embedded')
            break
    else:
        fail(f'{t}: missing embedded data ({DATA_VARS[t]})')

    # 侧边栏导航存在 (lineage用独立布局，无sidebar)
    if t != 'lineage':
        nav_count = html.count('nav-link')
        if nav_count >= 3:
            ok(f'{t}: sidebar nav links ({nav_count})')
        else:
            fail(f'{t}: sidebar nav links missing or too few ({nav_count})')

    # 大小合理 (>10KB)
    if len(html) < 10000:
        fail(f'{t}: size {len(html):,} too small')
    else:
        ok(f'{t}: size {len(html):,} bytes')
    print()

# ── 独立文章页 (articles/<id>.html) ──
print('Verifying articles/ (standalone article pages)\n')
aidx = os.path.join(ARTICLES, 'index.html')
if not os.path.exists(aidx):
    fail('articles/index.html missing')
else:
    with open(aidx, encoding='utf-8') as f:
        idx = f.read()
    if '独立文章目录' not in idx:
        fail('articles/index: missing title')
    else:
        ok('articles/index: catalog title')
    hrefs = re.findall(r'href="([^"]+\.html)"', idx)
    art_files = {h for h in hrefs if not h.startswith('../')}
    ok(f'articles/index: links to {len(art_files)} article pages')
    missing = [h for h in art_files if not os.path.exists(os.path.join(ARTICLES, h))]
    if missing:
        fail(f'articles/index: broken hrefs {missing}')
    else:
        ok('articles/index: all hrefs resolve')

for obj in sorted(os.listdir(ARTICLES)):
    if not obj.endswith('.html') or obj == 'index.html':
        continue
    path = os.path.join(ARTICLES, obj)
    with open(path, encoding='utf-8') as f:
        html = f.read()
    checks = [
        ('DOCTYPE', html.lstrip().startswith('<!DOCTYPE html>')),
        ('ends </html>', html.strip().endswith('</html>')),
        ('ARTICLE embedded', 'var ARTICLE =' in html),
        # 独立文章页分两种形式：doc 驱动（内嵌 doc_md + renderArticle）或数据驱动
        # （内嵌 PRACTICE_DATA 数据源 + 自包含渲染脚本，正文单存于 YAML，如 chan-traces）
        ('doc_md embedded', '"doc_md"' in html or 'var PRACTICE_DATA' in html),
        ('renderer inlined', 'function renderArticle' in html or 'function renderChanTraces' in html),
        ('common.css', '../css/common.css' in html),
    ]
    bad = [c[0] for c in checks if not c[1]]
    if bad:
        fail(f'articles/{obj}: missing {", ".join(bad)}')
    else:
        ok(f'articles/{obj} ({len(html):,} bytes, all checks)')

# ── Tab 页内「独立文章页」入口条链接解析检查 ──
chip_errors = 0
for t in TABS:
    if t == 'lineage':
        continue
    with open(os.path.join(DEMO, 'tabs', f'{t}.html'), encoding='utf-8') as f:
        html = f.read()
    for href in re.findall(r'href="../articles/([^"]+\.html)"', html):
        if not os.path.exists(os.path.join(ARTICLES, href)):
            fail(f'tabs/{t}.html: chip href broken -> articles/{href}')
            chip_errors += 1
if chip_errors == 0:
    ok('tabs: all article-chip hrefs resolve')

# ── gap 侧栏「华严祖师 / 专题研究」→ 直接进入独立文章页 ──
gap_path = os.path.join(DEMO, 'tabs', 'gap.html')
with open(gap_path, encoding='utf-8') as f:
    gp_html = f.read()
gp_need = ['../articles/master-dushun.html', '../articles/master-zhiyan.html',
           '../articles/master-fazang.html', '../articles/master-chengguan.html',
           '../articles/master-zongmi.html', '../articles/master-litongxuan.html',
           '../articles/master-mengcan.html', '../articles/zhenwei.html']
gp_missing = [h for h in gp_need if h not in gp_html]
if gp_missing:
    fail(f'gap sidebar: missing direct article links {gp_missing}')
else:
    ok('gap sidebar: 8 article entries link straight to standalone pages')
if 'articlePageHref' not in gp_html:
    fail('gap: articlePageHref helper missing')
else:
    ok('gap: articlePageHref helper present')

print()

print('=' * 40)
if errors == 0:
    print('✅ ALL CHECKS PASSED')
    sys.exit(0)
else:
    print(f'❌ {errors} ERROR(S) FOUND')
    sys.exit(1)
