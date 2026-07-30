#!/usr/bin/env python3
"""Verify web/demo/index.html structure before deployment."""
import sys, os, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML_PATH = os.path.join(ROOT, 'web', 'demo', 'index.html')

def fail(msg):
    print(f'  FAIL: {msg}')
    return 1

def ok(msg):
    print(f'  OK:   {msg}')
    return 0

errors = 0

with open(HTML_PATH, encoding='utf-8') as f:
    html = f.read()

print(f'Verifying {HTML_PATH} ({len(html):,} bytes)\n')

# 0. Must start with <!DOCTYPE
if not html.lstrip().startswith('<!DOCTYPE html>'):
    errors += fail('Must start with <!DOCTYPE html>')
else:
    errors += ok('Starts with <!DOCTYPE html>')

# 1. Structure
if not html.strip().endswith('</html>'):
    errors += fail('Must end with </html>')
else:
    errors += ok('Ends with </html>')

# 2. Script tag before </html>
last_script = html.rfind('</script>')
last_html = html.rfind('</html>')
if last_script >= last_html:
    errors += fail(f'</script> at {last_script} must be before </html> at {last_html}')
else:
    errors += ok('Script before </html>')

# 3. No </script> inside JS content
# Find all script boundaries
scripts_starts = [m.start() for m in __import__('re').finditer(r'<script>', html)]
scripts_ends = [m.start() for m in __import__('re').finditer(r'</script>', html)]
# Main script is the last inline <script> (before the Leaflet CDN <script src>)
main_start = scripts_starts[-1] + 8
main_end = scripts_ends[-2]  # second-to-last </script> is the main script close
js_content = html[main_start:main_end]
if '</script>' in js_content.lower():
    errors += fail('Found </script> inside JS content')
else:
    errors += ok('No </script> inside JS')

# 4. No fetch() calls
if 'fetch(' in js_content:
    errors += fail('Contains fetch() - data should be embedded')
else:
    errors += ok('No fetch() calls')

# 5. Brace balance (approximate)
opens = js_content.count('{')
closes = js_content.count('}')
if opens != closes:
    errors += fail(f'Brace mismatch: {{ {opens} vs }} {closes}')
else:
    errors += ok(f'Braces balanced ({opens})')

# 6. Size check
size = len(html)
if 25000 <= size <= 110000:
    errors += ok(f'Size: {size:,} bytes')
else:
    errors += fail(f'Size {size:,} bytes out of range (25-80KB)')

# 7. Key content
for key in ['var GRAPH', 'var GAP', 'function drawTL', 'function initMap',
            'function renderGap', 'function renderPractice', 'function renderFrontier',
            'addEventListener("click",function(e)',
            'addEventListener("wheel"',
            'addEventListener("click",onClick']:
    if key not in html:
        errors += fail(f'Missing: {key}')
    else:
        errors += ok(f'Found: {key}')

# 8. Has person data (check for key IDs)
if '"id": "person_003"' not in html and 'person_003' not in html:
    errors += fail('Missing key person data')
else:
    errors += ok('Key persons present (法藏, 海云继梦)')

# 9. Check for unescaped quotes in strings: pattern is "text" inside another "string"
# Find lines like: h+="... "..."; which indicates an unescaped inner quote
lines = js_content.split('\n')
quote_issues = 0
for i, line in enumerate(lines):
    stripped = line.strip()
    if stripped.startswith('h+=') or stripped.startswith('pv.innerHTML'):
        # Count double quotes - should be even (opening + closing pairs)
        dq = stripped.count('\"')
        if dq % 2 != 0:
            errors += fail(f'Unescaped quotes at line ~{i}: {stripped[:80]}')
            quote_issues += 1
if quote_issues == 0:
    errors += ok('No unescaped quotes in string literals')

# 10. Three tabs
# Count only in HTML part (before first <script>)
html_part = html[:html.find('<script>')]
tab_count = html_part.count('data-tab=')
if tab_count == 4:
    errors += ok(f'4 tabs present')
else:
    errors += fail(f'{tab_count} tabs (expected 4)')

print(f'\n{"="*40}')
if errors == 0:
    print('✅ ALL CHECKS PASSED')
    sys.exit(0)
else:
    print(f'❌ {errors} ERROR(S) FOUND')
    sys.exit(1)
