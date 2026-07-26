import re
with open('web/demo/index.html', encoding='utf-8') as f:
    html = f.read()

scripts = []
pos = 0
while True:
    s = html.find('<script>', pos)
    if s < 0: break
    e = html.find('</script>', s)
    scripts.append((s+8, e))
    pos = e + 9

s3_start, s3_end = scripts[-1]
s3 = html[s3_start:s3_end]
print(f'Script 3: {len(s3)} chars')

# Count backticks
bt_count = s3.count(chr(96))
print(f'Backtick count: {bt_count} (even={bt_count % 2 == 0})')

# Find renderPractice function
rp = s3.find('function renderPractice')
print(f'renderPractice at position: {rp}')
if rp > 0:
    rp_code = s3[rp:]
    bt_in_rp = rp_code.count(chr(96))
    print(f'  renderPractice code: {len(rp_code)} chars, backticks: {bt_in_rp}')

# Check for any byte that's not printable ASCII or valid UTF-8
bad_chars = []
for i, b in enumerate(s3.encode('utf-8')):
    if b < 0x20 and b not in (0x09, 0x0a, 0x0d):  # tab, lf, cr
        bad_chars.append((i, hex(b)))
if bad_chars:
    print(f'Non-printable chars: {bad_chars[:10]}')
else:
    print('No bad control characters')

# Check first 200 chars of s3
print(f'First 200 chars of Script 3:')
print(s3[:200])
