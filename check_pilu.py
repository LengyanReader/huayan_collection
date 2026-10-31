with open(r'C:\DA_Practice\huayan_collection\web\demo\articles\piluzhena.html', encoding='utf-8') as f:
    content = f.read()
idx = content.find('var ARTICLE')
if idx >= 0:
    script_start = content.rfind('<script', 0, idx)
    print(content[script_start:script_start+800])
else:
    print('not found')
