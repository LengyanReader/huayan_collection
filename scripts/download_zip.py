import urllib.request, zipfile, os

out_dir = 'data/references/tibetan/derge_kangyur'
zip_path = os.path.join(out_dir, 'deka_vol_txt_v1905.zip')

found = []
with zipfile.ZipFile(zip_path, 'r') as z:
    namelist = z.namelist()
    for name in namelist:
        if not name.endswith('.txt'):
            continue
        data = z.read(name)
        text = data.decode('utf-8')
        if 'སངས་རྒྱས་ཕལ་པོ་ཆེ' in text:
            found.append(name)

with open(os.path.join(out_dir, 'avatamsaka_volumes.txt'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(found))
print('total files:', len(namelist))
print('avatamsaka volumes:', len(found))
for fn in found:
    print('VOL:', fn.encode('ascii', 'replace').decode('ascii'))
