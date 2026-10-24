with open('web/demo/articles/index.html','r',encoding='utf-8') as f:
    c=f.read()
entry = '        <article class=\"card\">\n          <h3><a href=\"huayan-sidi-pin.html\">华严经细读·第八部　四圣谛品</a></h3>\n          <p class=\"meta\">第二会·差别因果周　卷十二末</p>\n          <p>十方十世界说四圣谛，各四谛各十名，共四百名，随众生心乐而异名。</p>\n        </article>\n'
if '四圣谛品' not in c:
    # Try different patterns
    if '</section>' in c:
        c = c.replace('</section>', entry + '      </section>', 1)
    else:
        c += entry
    with open('web/demo/articles/index.html','w',encoding='utf-8') as f:
        f.write(c)
    print('added')
else:
    print('exists')
