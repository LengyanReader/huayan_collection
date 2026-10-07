
import io,re,sys
sys.stdout.reconfigure(encoding='utf-8')
xml=io.open('data/references/cbeta/T10n0279.xml',encoding='utf-8',errors='replace').read()
text=re.sub(r'<[^>]+>','',xml)
i6=text.find('卷第六'); i7=text.find('卷第七')
v6=text[i6:i7]
# 十身
hits=[m.start() for m in re.finditer(r'十身|法身|應身|化身|受用身', v6)]
print('n=',len(hits))
for h in hits[:4]: print(repr(v6[h-15:h+50]))
