with open('web/demo/articles/index.html','r',encoding='utf-8') as f:
    c=f.read()
idx = c.find('经论茶歇')
if idx >= 0:
    end = c.find('</section>', idx)
    if end >= 0:
        section = c[idx:end]
        import re
        for m in re.finditer(r'href=\"([^\"]+)\"', section):
            href = m.group(1)
            if any(x in href for x in ['huayan-studies','huayan-series','avatamsaka','shizhu','ru-lai','puxian','shijie','huazang','piluzhena','rulai-minghao','sidi']):
                print(href)
