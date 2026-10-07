
import io,re,sys
sys.stdout.reconfigure(encoding='utf-8')
xml=io.open('data/references/cbeta/T10n0279.xml',encoding='utf-8',errors='replace').read()
text=re.sub(r'<[^>]+>','',xml)
i6=text.find('卷第六'); i7=text.find('卷第七')
v6=text[i6:i7]
hits=[m.start() for m in re.finditer(r'光明|普照|如來現相|如来现相', v6)]
print('n=',len(hits))
for h in hits[:3]: print(repr(v6[h-12:h+36]))
