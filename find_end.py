with open('web/demo/articles/index.html','r',encoding='utf-8') as f:
    c=f.read()
idx = c.find('href=\"rulai-minghao.html\"')
if idx >= 0:
    end = c.find('<div style=\"display:flex;flex-direction:column;gap:6px;background:var(--card)', idx+10)
    print(end)
