import re
with open('web/demo/articles/index.html','r',encoding='utf-8') as f:
    c=f.read()
# Remove all occurrences
pattern = r'<div style=\"display:flex;flex-direction:column;gap:6px;background:var\(--card\);border:1px solid var\(--line\);border-left:4px solid var\(--gold\);border-radius:10px;padding:14px 16px\">.*?huayan-sidi-pin.html.*?</div>\s*</div>'
c2, n = re.subn(pattern, '', c, flags=re.S)
print(n)
with open('web/demo/articles/index.html','w',encoding='utf-8') as f:
    f.write(c2)
