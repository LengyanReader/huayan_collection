
import io,re,sys
sys.stdout.reconfigure(encoding='utf-8')
xml=io.open('data/references/cbeta/T10n0279.xml',encoding='utf-8',errors='replace').read()
text=re.sub(r'<[^>]+>','',xml)
i6=text.find('卷第六'); i7=text.find('卷第七'); i8=text.find('卷第八')
v6=text[i6:i7]; v7=text[i7:i8]
# find segment with strong 光明+普照+現相
seg=v6
hits=[m.start() for m in re.finditer(r'光明[^。]{0,60}普照|普照[^。]{0,60}光明', seg)]
print('n=',len(hits))
for h in hits[:2]: print(repr(seg[h-15:h+80]))
