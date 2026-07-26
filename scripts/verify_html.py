with open('web/demo/index.html', encoding='utf-8') as f:
    html = f.read()

checks = [
    ('Ends with </html>', html.strip().endswith('</html>')),
    ('Scripts before </html>', html.rfind('</script>') < html.rfind('</html>')),
    ('JS OK present', 'JS OK' in html),
    ('L(m) defined', 'function L(m)' in html),
    ('INIT starting', 'INIT starting' in html),
    ('drawTL present', 'function drawTL' in html),
    ('initMap present', 'function initMap' in html),
    ('renderGap present', 'function renderGap' in html),
    ('renderPractice present', 'function renderPractice' in html),
    ('3 inline scripts', html.count('<script>') == 3),
    ('Size 30-70KB', 30000 < len(html) < 70000),
    ('Proper closing', html.count('</body>') == 1 and html.count('</html>') == 1),
]

all_ok = True
for label, ok in checks:
    print(f'  {"OK" if ok else "FAIL"}: {label}')
    if not ok: all_ok = False
print(f'\nSize: {len(html)} bytes')
print(f'Script tags: {html.count("<script>")}, Closes: {html.count("</script>")}')
print(f'Result: {"ALL OK" if all_ok else "SOME FAILED"}')
