
with open('web/demo/articles/index.html','r',encoding='utf-8') as f:
    c=f.read()
idx = c.find('如来名号品')
if idx >= 0:
    print(c[max(0,idx-150):idx+150])

