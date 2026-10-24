with open('web/demo/articles/index.html','r',encoding='utf-8') as f:
    c=f.read()
idx = c.find('href=\"rulai-minghao.html\"')
print(idx)
