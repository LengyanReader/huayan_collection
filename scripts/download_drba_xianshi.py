# -*- coding: utf-8 -*-
"""download_drba_xianshi.py — L.477：DRBA 宣化《華嚴經淺釋》101 分卷页全量扫取
服务器稳定（cp950·curl 可直取）·每页存 HTML→文本·含卷题解析
"""
import os, re, subprocess, sys, time

sys.stdout.reconfigure(encoding='utf-8')
BASE = 'https://www.drbachinese.org/online_reading/sutra_explanation/Ava/'
OUT_HTML = 'data/references/huayan_daodu/宣化淺釋_html'
OUT_TXT = 'data/references/huayan_daodu/宣化淺釋'
os.makedirs(OUT_HTML, exist_ok=True)
os.makedirs(OUT_TXT, exist_ok=True)

# 从 contents.htm 解析链接与卷题
raw = open('_ava_contents.html', 'rb').read().decode('cp950', errors='ignore')
pairs = []
for m in re.finditer(r'<a\s+href="(Ava[^"]+)"[^>]*>(.*?)</a>', raw, re.S):
    href = m.group(1)
    label = re.sub(r'<[^>]+>', '', m.group(2))
    label = re.sub(r'\s+', ' ', label).strip()
    pairs.append((href, label))
print('contents 解析: %d 卷页' % len(pairs))

def han(s):
    return len(re.findall(r'[\u3400-\u9fff]', s))

ok, fail = [], []
t0 = time.time()
for i, (href, label) in enumerate(pairs, 1):
    fn = os.path.join(OUT_HTML, href)
    txt_fn = os.path.join(OUT_TXT, href.replace('.htm', '.txt'))
    if os.path.exists(txt_fn) and os.path.getsize(txt_fn) > 2000:
        ok.append((href, label))
        continue
    good = False
    for attempt in range(3):
        r = subprocess.run(['curl', '-sL', BASE + href, '-o', fn, '--max-time', '120',
                            '-A', 'Mozilla/5.0'], capture_output=True)
        if os.path.exists(fn) and os.path.getsize(fn) > 5000:
            raw2 = open(fn, 'rb').read()
            t = raw2.decode('cp950', errors='ignore')
            body = re.sub(r'<script.*?</script>|<style.*?</style>', '', t, flags=re.S)
            body = re.sub(r'<[^>]+>', '\n', body)
            body = re.sub(r'&nbsp;', ' ', body)
            body = re.sub(r'\n{3,}', '\n\n', body)
            lines = [ln.strip() for ln in body.split('\n') if ln.strip() and han(ln) > 10]
            out = ('宣化上人《大方廣佛華嚴經淺釋》\n卷题：%s\n来源：https://www.drbachinese.org/online_reading/sutra_explanation/Ava/%s\n'
                   '性质：宣化浅释·限量引用标来源\n\n' % (label, href)) + '\n'.join(lines)
            with open(txt_fn, 'w', encoding='utf-8', newline='') as f:
                f.write(out)
            good = True
            break
        time.sleep(2)
    if good:
        ok.append((href, label))
        print('✓ %s | %s（%d/%d·%.0fs）' % (href, label[:24], len(ok), len(pairs), time.time() - t0), flush=True)
    else:
        fail.append((href, label))
        print('✗ %s' % href, flush=True)

print('\n完成：%d 成功 · %d 失败 · %.0fs' % (len(ok), len(fail), time.time() - t0))
if fail:
    print('失败:', fail)
