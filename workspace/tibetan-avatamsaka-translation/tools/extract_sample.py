import os, sys
sys.stdout.reconfigure(encoding='utf-8')

# Extract a sample passage from Derge vol 035 for testing
path = r'C:\DA_Practice\huayan_collection\data\references\tibetan\derge_kangyur\avatamsaka\035_α╜òα╜úα╝ïα╜åα╜║α╜ôα╝ì_α╜Ç.txt'
with open(path, encoding='utf-8') as f:
    content = f.read()

# Find the actual sutra start (after titles)
# Look for "འདི་སྐད་བདག་གིས་ཐོས་པའི་དུས་གཅིག་ན།"
idx = content.find('འདི་སྐད་བདག་གིས་ཐོས་པའི་དུས་གཅིག་ན།')
if idx >= 0:
    # Extract a paragraph
    sample = content[idx:idx+500]
    print(sample)
    # Save
    with open(r'C:/DA_Practice/huayan_collection/workspace/tibetan-avatamsaka-translation/data/sample_test.txt', 'w', encoding='utf-8') as out:
        out.write(sample)
    print('\n---SAVED---')
else:
    print('NOT FOUND')
