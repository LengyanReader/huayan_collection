with open('web/demo/articles/index.html','r',encoding='utf-8') as f:
    c=f.read()
idx = c.find('经论茶歇')
if idx >= 0:
    end = c.find('</section>', idx)
    if end >= 0:
        section = c[idx:end]
        print(section.count('flex-direction'))
