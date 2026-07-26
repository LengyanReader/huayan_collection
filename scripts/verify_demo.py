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
inline_start = html.find('<script>', html.find('tab-gap'))
inline_end = html.rfind('</script>')
js_content = html[inline_start+8:inline_end]
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
if 25000 <= size <= 80000:
    errors += ok(f'Size: {size:,} bytes')
else:
    errors += fail(f'Size {size:,} bytes out of range (25-80KB)')

# 7. Key content
for key in ['var GRAPH', 'var GAP', 'function drawTL', 'function initMap',
            'function renderGap', 'function renderPractice',
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

# 9. Three tabs
tab_count = html.count('data-tab=')
if tab_count == 3:
    errors += ok(f'3 tabs present')
else:
    errors += fail(f'{tab_count} tabs (expected 3)')

print(f'\n{"="*40}')
if errors == 0:
    print('✅ ALL CHECKS PASSED')
    sys.exit(0)
else:
    print(f'❌ {errors} ERROR(S) FOUND')
    sys.exit(1)
