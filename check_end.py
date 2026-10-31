with open(r'C:\DA_Practice\huayan_collection\web\demo\articles\ai-wisdom-alignment.html', encoding='utf-8', errors='ignore') as f:
    content = f.read()
idx = content.find('renderArticle()')
if idx >= 0:
    start = content.rfind('\n', 0, max(0, idx-80))
    end = content.find('\n\n', idx) + 50
    if end == 49: end = idx + 100
    print(content[start:end])
else:
    print('not found')
