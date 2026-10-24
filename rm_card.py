with open('web/demo/articles/index.html','r',encoding='utf-8') as f:
    c=f.read()
start = c.find('<article class="card">')
# find the one with huayan-sidi-pin
while start >= 0:
    end = c.find('</article>', start)
    if end >= 0:
        block = c[start:end]
        if 'huayan-sidi-pin' in block:
            c2 = c[:start].rstrip() + '\n' + c[end+len('</article>'):].lstrip()
            with open('web/demo/articles/index.html','w',encoding='utf-8') as f:
                f.write(c2)
            print('done')
            break
    start = c.find('<article class="card">', end+1)
else:
    print('not found')
