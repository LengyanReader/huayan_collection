import urllib.request, re, sys

url = "https://lengyanreader.github.io/huayan_collection/web/demo/index.html"
print(f"Fetching {url}...")
with urllib.request.urlopen(url) as resp:
    html = resp.read().decode('utf-8')

print(f"Downloaded: {len(html)} bytes")

# Find inline script
start = html.find('<script>', html.find('tab-practice'))
end = html.rfind('</script>')
js = html[start+8:end]

issues = []
if '</script>' in js.lower():
    issues.append(f'FATAL: </script> in JS at pos {js.lower().find("</script>")}')
if '<script' in js.lower() and 'src=' not in js.lower():
    issues.append(f'FATAL: <script in JS content')

opens = js.count('{'); closes = js.count('}')
if opens != closes:
    issues.append(f'Braces: {opens} vs {closes}')

bt = js.count('`')
if bt % 2 != 0:
    issues.append(f'Backticks: {bt}')

funcs = re.findall(r'function\s+(\w+)', js)
print(f'Functions: {len(funcs)} - {funcs[:8]}...')

# Check renderPractice template
rp = js.find('function renderPractice')
rp_end = js.rfind('}')
rp_js = js[rp:rp_end+1] if rp_end > 0 else ""
bt_rp = rp_js.count('`')
print(f'renderPractice size: {len(rp_js)} chars, backticks: {bt_rp}')

if issues:
    for i in issues: print(i)
else:
    print('JS structure: OK')

# Check for init() call
print(f'Has init IIFE: {"(function init()" in js}')
print(f'Has try-catch: {"try{" in js}')
