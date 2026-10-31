# Examine article structure
with open('web/demo/articles/ai-wisdom-alignment.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find ARTICLE definition
idx = content.find('var ARTICLE')
if idx >= 0:
    # Go back to find script tag
    start = content.rfind('<script', 0, idx)
    end = content.find('</script>', idx)
    if end > idx:
        end = end + len('</script>')
    print(content[start:end][:2000])
else:
    print('NOT FOUND')
