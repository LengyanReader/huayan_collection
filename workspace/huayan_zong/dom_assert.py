# -*- coding: utf-8 -*-
import sys, io
sys.stdout.reconfigure(encoding='utf-8')
p = r'web\demo\articles\huayan-zong.html'
h = open(p, encoding='utf-8').read()
CHECKS = [
 ('页面标题', '华严宗全方位研究'),
 ('registry 副题', '法界缘起'),
 ('五教引文', '聖教萬差，要唯有五'),
 ('十宗引文', '我法俱有宗'),
 ('十玄列表', '因陀羅網法界門'),
 ('古今差异实测', '祕密隱顯俱成門'),
 ('性起引文', '如來應供等正覺性起正法不可思議'),
 ('觉林偈', '一切唯心造'),
 ('三界一心', '三界所有，唯是一心'),
 ('宗密句繁体', '經是佛語，禪是佛意'),
 ('形成史', 'Nattier'),
 ('义湘', '浮石寺'),
 ('普贤乘', '普贤乘'),
 ('存疑节', '于阗编纂说'),
 ('回源声明', 'canonical'),
]
fails = 0
for name, needle in CHECKS:
    n = h.count(needle)
    status = 'ok' if n > 0 else 'FAIL'
    if n == 0: fails += 1
    print('  [%s] %-14s x%d  %s' % (status, name, n, needle[:30]))
print('DOM 断言：%d/%d 通过' % (len(CHECKS) - fails, len(CHECKS)))
sys.exit(1 if fails else 0)
