// ═══ PRACTICE TAB ═══
// Safe md converter with fallback (common.js may fail to load via file://)
var _m2h = (typeof mdToHTML==='function') ? mdToHTML : function(s){return s||'';};
function renderPractice(){
  var pv=document.getElementById("practice-view");if(!pv)return;
  var h="";
  h+="<style>.wu-door{cursor:pointer;padding:10px 14px;margin:4px 0;background:var(--card);border:1px solid var(--line);border-radius:8px;transition:all 0.2s}.wu-door:hover{border-color:var(--gold-l)}.wu-door .arrow{display:inline-block;transition:transform 0.2s;margin-right:6px}.wu-door.open .arrow{transform:rotate(90deg)}.wu-door .body{display:none;margin-top:8px;padding-top:8px;border-top:1px solid var(--line);font-size:0.9em;line-height:1.8;color:var(--text2)}.wu-door.open .body{display:block}.wu-door .ttl{font-weight:600;color:var(--gold);font-size:1em}.topic-card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px 14px;margin-bottom:8px}.topic-card h4{color:var(--gold);font-size:0.88em;margin-bottom:4px}.topic-card p{font-size:0.78em;line-height:1.7;color:var(--text2)}.topic-card a{color:var(--blue);font-size:0.75em}</style>";

  // ── WIP Notice (页面最顶部) ──
  h+="<div style='background:rgba(184,134,60,0.06);border:1px solid #b8863c40;border-radius:8px;padding:8px 12px;margin-bottom:12px;font-size:0.75em;color:var(--text2);line-height:1.6'>"
    +"⚠ <b>内容声明：</b>本页面内容基于大华严寺官网(2025.11版)和海云继梦和上已公开的讲经视频/音频/逐字稿/出版物整理。"
    +"法师讲法内容不断更新演化，当前整理仍不完整，需要大量结构化梳理和补充核实，<b>仅供参考</b>，持续更新中。"
    +"最新修行体系请以大华严寺官网为准。<br>"
    +"📅 最近更新："+new Date().toISOString().slice(0,10)+"</div>";

  // ═══════════════════════════════════════════
  // SUB-PAGE 1: 修行体系 (default visible)
  // ═══════════════════════════════════════════
  h+="<div id=pv-system class=pv-section>";

  // ── Sub-navigation moved to left sidebar ──

  // ── Header ──
  h+=renderCultivationSystem();

  // ── 助道资粮 (从 PRACTICE_DATA.zhuandao_ziliang) ──
  h+=renderZhuandaoSection();

  // ── 三十七道品 (从 PRACTICE_DATA.sanshiqi_daopin) ──
  h+=renderSanShiQiDaoPin();

  h+="</div>"; // close pv-system

  // ═══════════════════════════════════════════
  // SUB-PAGE 2: 禅观法要 (hidden)
  // ═══════════════════════════════════════════
  h+="<div id=pv-meditation class=pv-section style=display:none>";

  h += renderChanContemplation();

  // ── 实修心要文章链接 ──

  // ── 完整出处 ──

  h+="<div id=med-heart class=section>";
  h+="<style>"
    +".h3col{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:14px}"
    +".h3col-l{flex:1.4;min-width:300px;background:#fefdf9;border:1px solid var(--line);border-radius:10px;padding:16px 20px;font-size:.84em;line-height:2;max-height:560px;overflow-y:auto;color:#3d3427;font-family:'Noto Serif SC','Songti SC','SimSun',serif}"
    +".h3col-l p{margin:0 0 16px 0;text-align:justify}"
    +".h3col-l h4{color:var(--gold);font-size:1em;margin:20px 0 10px;text-align:center;font-weight:600}"
    +".h3col-l .himg{text-align:center;margin:12px 0}"
    +".h3col-l .himg img{max-width:38%;max-height:160px;border-radius:6px;box-shadow:0 1px 6px rgba(0,0,0,0.1);cursor:pointer;transition:transform .2s}"
    +".h3col-l .himg img:hover{transform:scale(1.02)}"
    +".h3col-l b{color:#8b6914}"
    +".h3col-r1{flex:1;min-width:240px;background:rgba(184,134,60,0.05);border:1px solid rgba(184,134,60,0.2);border-radius:10px;padding:10px 12px;font-size:.72em;line-height:1.7;max-height:520px;overflow-y:auto}"
    +".h3col-r2{flex:1;min-width:240px;background:rgba(94,139,158,0.05);border:1px solid rgba(94,139,158,0.2);border-radius:10px;padding:10px 12px;font-size:.72em;line-height:1.7;max-height:520px;overflow-y:auto}"
    +".h3col h3{font-size:.95em;margin-bottom:4px}"
    +".h3col .src{font-size:.82em;color:var(--text2);margin-top:6px;border-top:1px dotted var(--line);padding-top:4px}"
    +".h3col-tbar{position:absolute;top:4px;right:4px;display:flex;gap:2px;opacity:0;transition:opacity .2s}"
    +".h3col-l:hover .h3col-tbar,.h3col-r1:hover .h3col-tbar,.h3col-r2:hover .h3col-tbar{opacity:1}"
    +".h3col-tbar button{font-size:11px;padding:1px 4px;border:1px solid var(--line);border-radius:3px;background:var(--card);color:var(--text2);cursor:pointer}"
    +".h3col-tbar button:hover{background:var(--gold);color:#fff}"
    +".h3col-l,.h3col-r1,.h3col-r2{position:relative}"
    +".heart-note{background:rgba(184,134,60,0.12);border-left:3px solid var(--gold);padding:4px 8px;margin:4px 0;font-size:.9em;border-radius:0 4px 4px 0}"
    +"</style>";
  h+="<div style='display:flex;gap:6px;flex-wrap:wrap;margin-bottom:12px;padding:8px 10px;background:var(--panel);border:1px solid var(--line);border-radius:8px;font-size:0.75em'><b style=color:var(--gold)>❤️ 实修心要:</b><a href='#heart-intro' style=color:var(--blue)>十讲总览</a>·<a href='#heart-articles' style=color:var(--blue)>十篇文章对照</a>·<a href='#heart-gandhara' style=color:var(--blue)>犍陀罗导航</a></div>";
  h+="<div class=section id=heart-intro style=border-left:4px solid var(--gold)><h2>❤️ 实修心要 — 海云继梦和上禅修入门十讲</h2>";
  h+="<p style=font-size:.78em;color:var(--text2);line-height:1.7>来源: 微信公众号「永远的犍陀罗」· 实修心要专辑(共10篇)。海云继梦和上开示,仁悦整理。<b>左栏:全部原文 · 中栏:海云华严行法对照 · 右栏:其他宗派/道家相互印证。</b></p>";
  h+="<p style=font-size:.72em;color:var(--text2);margin-bottom:8px>"
    +"<span id=heart-git-status style=font-size:.68em;color:var(--text2)></span>"
    +"</p></div>";

  h+="<div class=section id=heart-gandhara><h2>📰 实修心要 — 永远的犍陀罗·禅修实操系列</h2>";
  h+="<p style=font-size:.78em;color:var(--text2);margin-bottom:6px>以下10篇文章来自微信公众号「<b>永远的犍陀罗</b>」· <b>实修心要</b>专辑。内容为海云继梦和上关于禅修实操的开示,由仁悦整理。原文链接为微信公众号文章,全文已保存至 <code>docs/hy_refs/wechat/</code> 目录。</p>";
  h+="<div style='display:flex;gap:6px;flex-wrap:wrap;font-size:0.73em'>";
  [{n:1,t:'别用大脑修行',d:'暖身二法·调身调息·内脏内动',u:'https://mp.weixin.qq.com/s/S2D9BOc3jFwDRQr2tbzG6g'},
   {n:2,t:'四段呼吸的奥秘',d:'呼吸四阶段的辨识与运用',u:'http://mp.weixin.qq.com/s?__biz=MzkyMzQxOTMyMg==&mid=2247497426&idx=1&sn=7fa8a139ce472314116bbe138e50db10&chksm=c1e7e107f6906811acd86cfb3a27c4bfa0d19b60bb896feb46af3ae1010838b36e9f2c668c1b#wechat_redirect'},
   {n:3,t:'闭气不是憋气',d:'闭气与憋气的关键区别',u:'http://mp.weixin.qq.com/s?__biz=MzkyMzQxOTMyMg==&mid=2247497428&idx=1&sn=04845b578927e6631786c3cc725bf763&chksm=c1e7e101f69068177af7b3cda755545cf3835e01bfe05feca8321e1cc77169421a7fb4856812#wechat_redirect'},
   {n:4,t:'摸着那个「转折点」',d:'呼吸中阻力的转折与突破',u:'http://mp.weixin.qq.com/s?__biz=MzkyMzQxOTMyMg==&mid=2247497449&idx=1&sn=a8e12d77fca6019f4981a30d5beb8a65&chksm=c1e7e13cf690682af9445df95091817ab56d68c9192ddd5f71e0e464ef0533dd3b9b9842624b#wechat_redirect'},
   {n:5,t:'呼吸里的一股「力」',d:'息之力的感知与运用',u:'http://mp.weixin.qq.com/s?__biz=MzkyMzQxOTMyMg==&mid=2247497472&idx=1&sn=3b28886bf8e854a0958bba7354beef9f&chksm=c1e7e0d5f69069c3e18903d286c2740854421f8757c83402ed71ebe4880346dbf757dc1366c7#wechat_redirect'},
   {n:6,t:'置心一处的三大工程',d:'置心一处的技术面三大要素',u:'http://mp.weixin.qq.com/s?__biz=MzkyMzQxOTMyMg==&mid=2247497479&idx=1&sn=c4784e020ce863182a89632d52d56664&chksm=c1e7e0d2f69069c4fa173212ce7490d78b05d7ab06deb6731e1dbc9bd3707dcf0fd744571a4a#wechat_redirect'},
   {n:7,t:'心跑了，抓回来！',d:'摄心——若心他缘摄之令返',u:'http://mp.weixin.qq.com/s?__biz=MzkyMzQxOTMyMg==&mid=2247497491&idx=1&sn=f568ae4dfdafb48b16a268156cabc90e&chksm=c1e7e0c6f69069d0a64c9ae7e9a47d0c1731bd0d7de9dd5f31105d1092682a790dda21dd7f43#wechat_redirect'},
   {n:8,t:'别躲清静，去「防震」',d:'动中修行的防震训练',u:'http://mp.weixin.qq.com/s?__biz=MzkyMzQxOTMyMg==&mid=2247497501&idx=1&sn=ed9c44ca78f777c38e46b78fb3bc1450&chksm=c1e7e0c8f69069de0275257c938825b419168b3f2bd7e3be7efa9f5ae9aa239d1f9ffade304f#wechat_redirect'},
   {n:9,t:'内动来了，用「金钥匙」',d:'参禅金钥匙的触发与运用',u:'http://mp.weixin.qq.com/s?__biz=MzkyMzQxOTMyMg==&mid=2247497540&idx=1&sn=a44a18d9d5867cf254ed387fe524a062&chksm=c1e7e091f6906987832b9af27aba864456f1cb9d1337752fba024d7969943fb657d8435411b8#wechat_redirect'},
   {n:10,t:'入禅九阶：从暖身到金钥匙',d:'系统总结——禅修九阶次第',u:'http://mp.weixin.qq.com/s?__biz=MzkyMzQxOTMyMg==&mid=2247497558&idx=1&sn=670085792928af68ec9ef60b3574febe&chksm=c1e7e083f69069951f0e0bf69f96e9810a1a0df9109fa4e3be7cfea1ef4579286d4540decf03#wechat_redirect'}]
  .forEach(function(a){h+="<span style='padding:4px 10px;background:rgba(94,139,158,0.06);border:1px solid rgba(94,139,158,0.2);border-radius:10px;min-width:160px'><b style=color:#5e8b9e>第"+a.n+"篇</b> <a href='"+a.u+"' target=_blank style=font-weight:600>"+a.t+"</a><br><span style=font-size:0.85em;color:var(--text2)>"+a.d+"</span></span>";});
  h+="</div>";
  h+="<p style=font-size:.68em;color:var(--text2);margin-top:6px>📌 <b>来源:</b> 微信公众号「永远的犍陀罗」· 实修心要专辑 · 海云继梦和上开示 · 仁悦整理 · 2026-08-02批量提取</p>";
  h+="</div>";
  // Cross-reference data indexed by article title keyword
  var heartXRef={
    '别用大脑':{r1:'◆ <b>调身·调息·调心(五科训练)</b>: 海云和上《煖身:华严禅修入门》(布克文化2021)系统阐述,强调「身·息·心三者一体不二」。本文「暖身二法」即五科中调身+调息的实操展开。<br>◆ <b>驻佇心观(停心工程)</b>: 《华严禅行法—禅观》第四集:「你要能够停下心来,然后我们要观心!停心是一个前行。」本文「不能用大脑」即停心基本操作。<br>◆ <b>华严初祖·杜顺《法界观门》真空观·泯绝无寄</b>(CBETA T45n1884):「不可言即色不即色,亦不可言即空不即空,一切法皆不可,不可亦不可,此语亦不受。迥绝无寄,非言所及,非解所到。」此即「不能用大脑」的华严宗源头——「生心动念,即乖法体、失正念故。」<br>◆ <b>华严四祖·澄观</b>: 「心心无住,念念无着。」与本文「不用大脑,用身体感知」归趣一致。<br>◆ <b>参禅金三角</b>: fjdh.cn(2013.12)「置心一处·放轻松·息入息出很清楚」。<br><span class=src>📎 禅观法要→调身调息调心·驻佇心观 · T45n1884 法界观门</span>',
      r2:'◆ <b>天台·智者大师《小止观》调和第四(CBETA T46n1915)</b>: 「行者修习,善调五事,必使和适,则三昧易生。」<b>调身</b>——「不宽不急,是身调相。」<b>调息</b>——息有四相(风喘气息),「守风则散,守喘则结,守气则劳,守息即定。不涩不滑,是调息相。」<b>调心</b>——治沉浮宽急,「不沉不浮,是心调相。」身息心三事「的无前后,随不调者而调适之。」与本文调身调息调心体系完全互证。<br>◆ <b>禅宗·《六祖坛经》坐禅品(CBETA T48n2008)</b>: 「外于一切善恶境界,心念不起,名为坐;内见自性不动,名为禅。」「外离相为禅,内不乱为定。」坛经之禅定不在形躯而在心性——但惠能同时批判「空心静坐,百物不思」的枯禅(与本文「不能用大脑」非弃绝思维而是转向身体感知,有对应之妙)。<br>◆ <b>道家·庄子心斋</b>: 《庄子·人间世》:「若一志,无听之以耳而听之以心,无听之以心而听之以气。听止于耳,心止于符。气也者,虚而待物者也。唯道集虚。虚者,心斋也。」「听之以气」即甩开意识思维,归于气息感知——与本文「不能用大脑,用身体感知」异曲同工。郭象注:「遗耳目,去心意,而付气性之自得。」<br>◆ <b>道家·列子·心凝形释</b>: 《列子·黄帝》:「心凝形释,骨肉都融,不觉形之所倚,足之所履。」与停心后身心消融的状态相通。<br>◆ <b>儒家·《大学》知止</b>: 「知止而后有定,定而后能静,静而后能安。」知止即大脑停歇——与「不能用大脑」的先秦儒学源头遥相呼应。<br>◆ <b>瑜伽·Pratyahara(制感)</b>: Patanjali《瑜伽经》2.54-55: svaviṣayāsamprayoge cittasya svarūpānukāra ivendriyāṇāṁ pratyāhāraḥ. 感官从外境收摄向内,如心之本形——对应本文从「大脑外驰」转向「身体内觉」。<br><span class=src>📎 CBETA T46n1915 · T48n2008 ·《老子》1/3/11(有之以为利无之以为用)/14/19/21(道之为物惟恍惟惚)/28/37/45/47/48/52/56/70/81(信言不美)·《庄子》逍遥游/养生主/人间世/大宗师/在宥/天地/缮性/庚桑楚/知北游/渔父/应帝王/列御寇/天下/骈拇/马蹄/胠箧·《列子》黄帝/天瑞/杨朱(全性保真)·《大学》·《瑜伽经》2.54</span>'},
    '四段呼吸':{r1:'◆ <b>安那般那数息观(数·随·止)</b>: 禅观法要·技术面详解。数法1→10循环;随法注意「息入尽」与「息出尽」每一细节。本文「四段呼吸——息入·息住·息出·息停」对应随法对呼吸全过程的精细觉知。<br>◆ <b>华严三祖·法藏《妄尽还源观》</b>(CBETA T45n1876): 第二门「依体起二用」中,海印三昧心如大海澄净万象影现——此澄净之用,以息之细密调柔为入门方便。法藏云:「言海印者,真如本觉也。妄尽心澄,万象齐现。」调息至「息相」(出入绵绵若存若亡)即是「妄尽心澄」的前行基础。<br>◆ <b>息之四相</b>: 从粗至细——风→喘→气→息,四段呼吸的清晰觉知正是从「气相」趋入「息相」的关键。<br><span class=src>📎 禅观法要→安那般那数息观· 调息息之四相 · T45n1876 妄尽还源观</span>',
      r2:'◆ <b>天台·《小止观》息之四相(CBETA T46n1915)</b>: 「不声不结不粗,出入绵绵,若存若亡,资神安稳,情抱悦豫——此是息相也。守风则散,守喘则结,守气则劳,守息即定。」海云和上息之四相全出于此。<br>◆ <b>南传·安那般那念(MN 118)</b>: 十六阶段安般念从「知入息长」到「观灭·观舍」，与四段呼吸有对应的微观觉照结构。<br>◆ <b>道家·《抱朴子》胎息</b>: 「得胎息者,能不以鼻口嘘吸,如在胞胎之中,则道成矣。」即息相「出入绵密若存若亡」之极致。<br>◆ <b>藏传·密勒日巴尊者</b>: 《十万歌集》:「气之出入往来处,即是心之所行处。」「持气之法如灯烛,微风不动光焰住。」藏传那洛六法之「瓶气」(rlung bum pa can)细分为入、满、消、射四段——与本文「息入·息住·息出·息停」结构完全对应。<br>◆ <b>儒家·朱熹《调息箴》</b>: 朱子晚年静坐调息之作——《晦庵集》卷八十五:「鼻端有白,我其观之。随时随处,容与猗移。静极而嘘,如春沼鱼。动极而翕,如百虫蛰。氤氲阖辟,其妙无穷。谁其尸之?不宰之功。」朱子以鼻端白为观想对象,与置心风门异曲同工。<br><span class=src>📎 CBETA T46n1915 · MN 118 ·《抱朴子·释滞》· 密勒日巴· 朱熹 ·《老子》5(橐龠)/12(五色令人目盲五音令人耳聋)/42·《庄子》天运/刻意/盗跖(全真)·《庄子·则阳》:「安危相易,祸福相生,缓急相摩,聚散以成。」</span>'},
    '闭气不是憋气':{r1:'◆ <b>参禅金钥匙·吸闭吐</b>: 第九讲详述——「吸(自然吸气)→闭(自然停住,不憋气)→吐(自然呼气),三个动作自然连贯。」本文是金钥匙「闭」字的准确诠释。<br>◆ <b>华严五祖·宗密《禅源诸诠集都序》</b>(CBETA T48n2015):「息妄者,非谓息灭其心,但令不起妄念而已。如水有波,波因风起;风息波停,水自澄净。」自然闭气恰如「风息波停」——非强力止波(憋气),而是风(用力)自息,水(呼吸)自澄。宗密以禅教融合之见,释「自然息妄」——与本文「自然闭气非憋气」完全互证。<br>◆ <b>数于尽处</b>: 在「息入尽」与「息出尽」的O点——即自然闭气之处数息。<br><span class=src>📎 禅观法要→参禅金三角·技术面数随止 · T48n2015 禅源诸诠集都序</span>',
      r2:'◆ <b>瑜伽·Kumbhaka(住气)</b>: 《哈达瑜伽之光》(Haṭha Yoga Pradīpikā) 2.44-47: Sahita Kumbhaka(有作住气)为刻意屏息,Kevala Kumbhaka(无作住气)为自然呼吸停止——无需用力,呼吸自然止息。后者与本文「自然闭气」完全一致。<br>◆ <b>道家·《庄子·大宗师》踵息</b>: 「古之真人……其息深深。真人之息以踵,众人之息以喉。」真人之息深至脚跟,闭气是深息的自然结果,非强制憋气。成玄英疏:「踵,足根也。真人息于踵,至深至细。」<br>◆ <b>道家·《老子》第10章</b>: 「专气致柔,能如婴儿乎?」柔和自然的呼吸如婴儿,闭气是柔和的延伸而非刚强的对抗。<br><span class=src>📎 《哈达瑜伽之光》Ch.2 ·《庄子·大宗师》·《老子》10/16/20/43/55/76/78/50(出生入死生之徒十有三)·《庄子》刻意/外物(荃者所以在鱼得鱼而忘荃)· 辨喜·拉玛那</span>'},
    '转折点':{r1:'◆ <b>工程面A阶段·感受息之长短动静</b>: 本文O点感知即A阶段的具体操作——在「息入尽」与「息出尽」的转折处感受能量的转换。<br>◆ <b>华严二祖·智俨《华严一乘十玄门》同时具足相应门</b>(CBETA T45n1868):「如海一滴,具百川味。」一念间具足万法——息入息出之O点,虽微细如一滴,实含呼吸全体因果。在此转折处顿见息之全体大用,即华严「微细相容安立门」的禅观实践。<br>◆ <b>参禅金三角·息入息出清楚</b>: 「对呼吸的出入看得清清楚楚」——看清O点即是看得最清楚的时刻。<br><span class=src>📎 禅观法要→工程面A阶段·参禅金三角 · T45n1868 十玄门</span>',
      r2:'◆ <b>天台·六妙门「止」门原文(CBETA T46n1917)</b>: 「息诸缘虑,不念数随,凝寂其心,是名修止。」「止」的入口即在息之转折——O点不属入也不属出,是最自然的「止」处。智者在《六妙门》中进一步说:「以止为妙门者,行者因止心故,即便次第发五轮禅。」<br>◆ <b>道家·《老子》第6章·玄牝之门</b>: 「谷神不死,是谓玄牝。玄牝之门,是谓天地根。绵绵若存,用之不勤。」呼吸转折处如玄牝之门——似无实有,绵绵不绝,是天地之根。河上公注:「玄,天也,于人为鼻。牝,地也,于人为口。」鼻口之间的呼吸转折即天地之根。<br>◆ <b>道家·《列子·天瑞》</b>: 「生物者不生,化物者不化。」息入息出的O点——不属生灭、不属出入——即「不生不化」之处。<br><span class=src>📎 CBETA T46n1917 ·《老子》6/36(将欲歙之必固张之)/73(勇于不敢则活)·河上公注 ·《列子·天瑞》·《庄子·养生主》·《庄子·徐无鬼》:「无鬼,忘乎物,忘乎天,其名为忘己。」</span>'},
    '呼吸里的':{r1:'◆ <b>工程面B阶段·洞悉呼吸因果轨迹</b>: 「明了呼吸的轨迹——清楚呼吸的因与果。掌握此即长寿法基础,法师称此为『生命的秘笈』。」本文「息之力」即B阶段所述呼吸因果轨迹的内在动力。<br>◆ <b>华严三祖·法藏《华严经义海百门》</b>(CBETA T45n1875):「了法无生,知法无我,则能所俱寂,心境双融。」息之「力」——当能感知到气息中的生命动能,即是从「法有我无」转向「心境双融」的关键。<br>◆ <b>般那不外漏</b>: 参禅金三角中保存息之「力」。<br><span class=src>📎 禅观法要→工程面B阶段·参禅金三角 · T45n1875 义海百门</span>',
      r2:'◆ <b>儒家·《孟子·公孙丑上》浩然之气</b>: 「我善养吾浩然之气。……其为气也,至大至刚,以直养而无害,则塞于天地之间。其为气也,配义与道;无是,馁也。是集义所生者,非义袭而取之也。」孟子之气非呼吸之气,而是道德生命之「力」——「直养无害」即本文「自然感知息之力,不造作」。<br>◆ <b>道家·《庄子·庚桑楚》卫生之经</b>: 「儿子终日嗥而嗌不嗄,和之至也;终日握而手不掜,共其德也。」婴儿啼哭而喉不哑——和之至也。此「和」即生命能量(息之力)自然充沛而无耗损。「抱一勿失」即于息中感知此「一」之力。<br>◆ <b>瑜伽·Prana五气</b>: 《泰迪黎亚奥义书》2.3: Prana由命根气·下行气·通行气·上行气·等住气构成。瑜伽即对Prana的调控。《哈达瑜伽之光》2.2:「当呼吸在动,心也在动;呼吸止,心亦止。」<br>◆ <b>道家·先天炁</b>: 《云笈七签》卷56:「炁者,天地之元,万物之始。」又《钟吕传道集》:「道生一,一生二,二生三,三生万物。一者,先天一炁也。」与息之力为同类概念。<br>◆ <b>中医·宗气</b>: 《黄帝内经·灵枢》邪客篇:「宗气积于胸中,出于喉咙,以贯心脉而行呼吸焉。」此宗气即息之「力」的医学表述。<br><span class=src>📎 《孟子·公孙丑上》·《庄子·庚桑楚》·《老子》4(道冲而用之或不盈)/7/21/42·《泰迪黎亚奥义书》2.3 ·《哈达瑜伽之光》2.2 ·《云笈七签》56 ·《钟吕传道集》·《黄帝内经·灵枢》·《列子·周穆王》·《列子·说符》:「持后而处先。」</span>'},
    '置心一处':{r1:'◆ <b>置心一处·四种停心方法</b>: 《华严禅行法—禅观》:(1)参话头(2)置心风门(3)数息随息(4)依禅堂规矩。本文概为三大工程:调身→调息→调心,三者一体不二。<br>◆ <b>华严三祖·法藏《修华严奥旨妄尽还源观》</b>(CBETA T45n1876):「显一体者,谓自性清净圆明体。……如是等,过恒沙也。自下依体起二用者,谓依前净体,起于二用。一者海印森罗常住用,二者法界圆明自在用。」法藏以「海印三昧」为置心一处的究竟归趣——心如大海澄净,万象同时影现,无出无入。<br>◆ <b>华严三祖·法藏《妄尽还源观》六门</b>: 摄境归心(即置心一处)→从心现境(即法界圆明)→心境圆融。置心一处即「摄境归心」——一切境相皆摄归于一心。<br>◆ <b>内摄·内观·禅观三层</b>: 内摄=技术面·摄心于风门;内观=感受法身存在;禅观=粗→细→微妙。此为杜顺至法藏一脉相承的华严观法在当代的实操化。<br><span class=src>📎 禅观法要→驻佇心观·四种停心方法·三层功夫 · T45n1876 妄尽还源观</span>',
      r2:'◆ <b>禅宗·《六祖坛经》定慧品(CBETA T48n2008)</b>: 「一行三昧者,于一切处行住坐卧,常行一直心是也。」「但行直心,于一切法勿有执著。」六祖批判「常坐不动,妄不起心」的枯坐——与本文「置心一处不是用力集中,而是身息心自然统一」的精神完全一致。<br>◆ <b>禅宗·《六祖坛经》无念法</b>: 「无念者,于念而无念。」「于诸境上,心不染,曰无念。」不是百物不思(那是法缚),而是念起不随——与本文置心一处后「不评判不懊恼」的态度一致。<br>◆ <b>天台·《小止观》系缘守境(CBETA T46n1915)</b>: 五种系缘法——系心顶上/发际/鼻柱(即风门)/脐间/地轮。引《禅门要略》:「系心在鼻柱者,鼻是风门,觉知息入息出。」与置心风门完全对应。<br>◆ <b>大乘·《大乘起信论》止观门(CBETA T32n1666)</b>: 马鸣菩萨:「若修止者,住于静处,端坐正意。不依气息,不依形色…一切诸想,随念皆除,亦遣除想。」此为「唯心识观」之置心一处的义理根源。<br>◆ <b>道家·《庄子·达生》佝偻承蜩</b>: 「虽天地之大,万物之多,而唯蜩翼之知。吾不反不侧,不以万物易蜩之翼,何为而不得!」——置心一处,天地不管,只管那一个目标。<br>◆ <b>儒家·《中庸》</b>: 「道也者,不可须臾离也;可离非道也。」「致中和,天地位焉,万物育焉。」诚之者,择善而固执之——专注一处的儒家版本。<br><span class=src>📎 CBETA T48n2008 · T46n1915 · T32n1666 ·《庄子·达生》·《庄子·天下》:「独与天地精神往来,而不敖倪于万物。」·《中庸》· 冈波巴·宗喀巴·《老子》22章:「曲则全,枉则直。」</span>'},
    '心跑了':{r1:'◆ <b>内摄·技术面核心——摄心</b>: 《华严禅行法》:「妄想一起,记得把心抓回来放在风门。」克服四种妄想。要点:不评判不懊恼,温和地摄回。<br>◆ <b>华严居士·李通玄(枣柏)《新华严经论》</b>(CBETA T36n1739): 「以信自心分别之性,本来是智慧。但以随情逐境,故成流浪。若了境如幻,情念自息。」——心随境转即流浪(心跑了),了境如幻则自息(抓回来)。李通玄以居士身著论,开华严实修之门,其「自心即佛」与本文摄心实践完全契合。<br>◆ <b>参禅金三角·放轻松</b>: 「呼吸归呼吸,妄想归妄想」——不跟妄想纠缠。<br><span class=src>📎 禅观法要→内摄·四种妄想·参禅金三角 · T36n1739 新华严经论</span>',
      r2:'◆ <b>南传·马哈希内观标记法</b>: Mahasi Sayadaw(1904-1982)《实用内观禅修》:心散乱时标记「妄想、妄想」三遍,不排斥不追随,温和地回到腹部起伏。与本文「不评判,温和地抓回来」是完全一致的操作原则。<br>◆ <b>大乘·《楞严经》卷五(CBETA T19n0945)</b>: 周利盘陀伽尊者「忆持如来一句伽陀,于一百日,得前遗后,得后遗前。佛愍其愚,教安居调息。我时观息,微细穷尽,生住异灭,诸行刹那,其心豁然,得大无碍。」最笨的弟子通过调息摄心也能成道——与本文「笨办法——就跑掉抓回来」的修行精神一致。<br>◆ <b>道家·庄子坐忘</b>: 《庄子·大宗师》:「堕肢体,黜聪明,离形去知,同于大通,此谓坐忘。」坐忘即放下一切攀缘——心跑了忘了它,自然「同于大通」。又《庄子·齐物论》:「吾丧我」——放下自我执着。与摄心返照的内在逻辑一致。<br><span class=src>📎 Mahasi Sayadaw《实用内观禅修》 · CBETA T19n0945 ·《庄子》大宗师/齐物论/庚桑楚/德充符「才全而德不形」·《老子》33章「自知者明」· 奥罗宾多: 「心的静止来自对内在之力的觉知。」</span>'},
    '别躲清静':{r1:'◆ <b>依禅堂规矩(第四种停心方法)</b>: 「该动则动、该静则静、该跑则跑、该坐则坐,身心放下。」海云和上禅堂训练体系中,「忍可禅七」即专门考验行者在各种境界中是否能保持置心一处。<br>◆ <b>大脑临界点与两种歧路</b>: 日常防震训练即在临界点前打好根基。<br><span class=src>📎 禅观法要→四种停心方法·三大关键原则</span>',
      r2:'◆ <b>禅宗·永嘉玄觉《证道歌》(CBETA T48n2014)</b>: 「行亦禅,坐亦禅,语默动静体安然。纵遇锋刀常坦坦,假饶毒药也闲闲。」——行住坐卧皆是禅,不于静中求玄,正与本文「别躲清静」互为印证。永嘉早岁精研天台止观,后参六祖得「一宿觉」,此歌即悟后之作。<br>◆ <b>禅宗·马祖道一(洪州禅)</b>: 「平常心是道。何谓平常心?无造作,无是非,无取舍,无断常,无凡无圣。」(《景德传灯录》卷六)日用平常中修——正是本文「别躲清静」的精神源头。<br>◆ <b>禅宗·黄檗希运(断际禅师)《传心法要》(CBETA T48n2012A)</b>: 「但于见闻觉知处认本心,然本心不属见闻觉知,亦不离见闻觉知。但莫于见闻觉知上起见解,亦莫于见闻觉知上动念。」不离日常作用而不被境界转——在动乱中不失本心。<br>◆ <b>大乘·《维摩诘经》(CBETA T14n0475)</b>: 「不入烦恼大海,则不能得一切智宝。」不断烦恼而入涅槃。<br>◆ <b>道家·《庄子·人间世》</b>: 叶公子高问仲尼,仲尼答:「乘物以游心,托不得已以养中,至矣。」不离世间纷扰而游心养中。<br>◆ <b>道家·《庄子·秋水》</b>: 「知道者必达于理,达于理者必明于权,明于权者不以物害己。」随时应变而不执着——即行住坐卧皆是禅的道家版本。<br>◆ <b>儒家·董仲舒《春秋繁露》</b>: 「正其义不谋其利,明其道不计其功。」——正心明道不避世事,与本文不离世间修行的精神相应。<br><span class=src>📎 CBETA T48n2014 ·《景德传灯录》卷六 · T48n2012A · T14n0475 ·《庄子》人间世/秋水/让王/田子方/山木/至乐/盗跖/说剑·《列子》汤问/力命/杨朱/说符·《老子》8/9/15/38/66(江海所以为百谷王)/67/69(吾不敢为主而为客)/79(天道无亲常与善人)·董仲舒·王阳明·《吕祖百字碑》</span>'},
    '内动来了':{r1:'◆ <b>参禅金三角全程流程</b>: fjdh.cn全文——调身→调息→置心一处→金三角→触功德→内动→金钥匙→觉照根性→象限转移→破无明→入菩提道。本文「内动来了,用金钥匙」处于触功德发起之后。<br>◆ <b>华严四祖·澄观《华严经随疏演义钞》</b>(CBETA T36n1736):「以定发慧,以慧资定。定慧均等,如鸟二翼。」内动是「定」的深化(从散乱到心一境性,产生色身微细变化),金钥匙是「慧」的引导(觉照息之出入——不落无记,不失观照)。澄观此语正是定慧双运的华严正见。<br>◆ <b>触功德·八触十功德</b>: 「内动」即八触中的「动触」——身体内部能量被激活的自然反应。<br><span class=src>📎 <a href=\"https://www.fjdh.cn/fjask/2013/12/133616318955.html\" target=_blank>fjdh.cn·参禅金三角全文</a> · T36n1736 演义钞</span>',
      r2:'◆ <b>瑜伽·Kundalini(拙火)与Bandha(收束法)</b>: 《哈达瑜伽之光》3.5:「沉睡的Kundalini如蛇蜷伏在Mooladhara(根轮),瑜伽士应以各种方法唤醒她。」内动类比Kundalini的觉醒。Bandha(收束法)——Jalandhara(喉锁)·Uddiyana(腹锁)·Mula(根锁)——在Kumbhaka时配合运用,引导Prana向上进入中脉。与金钥匙「闭→吐」的能量引导功能相似。<br>◆ <b>道家·火候·进阳火退阴符</b>: 内丹术语——「子时一阳生,进阳火;午时一阴生,退阴符。」以呼吸配合意念引导内气沿任督二脉运行(小周天)。金钥匙「吸(进火)→闭(温养)→吐(退符)」与内丹火候的进-炼-退结构有对应的模式。《周易参同契》:「朔旦屯直事,至暮蒙当受。昼夜各一卦,用之如次序。」<br>◆ <b>中国武术·丹田内转</b>: 太极拳/形意拳等内家拳以丹田为气机枢纽,「气沉丹田,以意领气」——吸时气沉丹田,闭时气转丹田,吐时气贯四梢。与金钥匙的吸·闭·吐三字诀有共通的身体操作模式。<br><span class=src>📎 《哈达瑜伽之光》Ch.3 ·《周易参同契》·《崔公入药镜》:「先天炁,后天炁,得之者,常似醉。」·《吕祖百字碑》:「气回丹自结,壶中配坎离。」·太极拳丹田论</span>'},
    '入禅九阶':{r1:'◆ <b>体系总览·三阶段</b>: 资粮道→前行→正行。入禅九阶涵盖资粮道至前行初期。<br>◆ <b>华严初祖·杜顺《五教止观》五重次第</b>(CBETA T45n1867): 法有我无门→生即无生门→事理圆融门→语观双绝门→华严三昧门。<br>◆ <b>华严二祖·智俨《搜玄记》</b>(CBETA T35n1732): 十玄门。<br>◆ <b>华严三祖·法藏《金师子章》十门</b>(CBETA T45n1880): 明缘起→辨色空→约三性→显无相→说无生→论五教→勒十玄→括六相→成菩提→入涅槃。<br>◆ <b>华严四祖·澄观</b>·<b>五祖宗密</b>·<b>宋代子璿</b>·<b>净源</b>: 一脉相承的华严修行阶次。<br><span class=src>📎 T45n1867 五教止观 · T35n1732 搜玄记 · T45n1880 金师子章 · 澄观/宗密/子璿/净源</span>',
      r2:'◆ <b>天台·六即佛(CBETA T46n1911 摩诃止观)</b>: 理即→名字即→观行即→相似即→分证即→究竟即。入禅九阶属「观行即」实操展开。智者:「所行如所言,所言如所行。」<br>◆ <b>大乘·《华严经·十地品》(CBETA T10n0279)</b>: 欢喜地至法云地,与海云判摄形成完整对照链。<br>◆ <b>道家·内丹筑基至炼虚</b>: 筑基→炼精化气(百日)→炼气化神(十月)→炼神还虚(三年)→炼虚合道(九年)。《钟吕传道集》:「炼形成气,炼气成神,炼神合道。」<br>◆ <b>道家·张伯端《悟真篇》</b>: 「劝君穷取生身处,返本还源是药王。」——入禅九阶从暖身到金钥匙,即「返本还源」的实操次第。与《悟真篇》内丹次第形成对应。<br>◆ <b>儒家·《荀子·劝学》</b>: 「不积跬步,无以至千里;不积小流,无以成江海。」九阶从第一阶暖身到第九阶入禅,即跬步积至千里的过程。<br>◆ <b>儒家·《荀子·解蔽》</b>: 「虚壹而静,谓之大清明。」——九阶层层深入至入禅,即由虚而壹而静,最终大清明。<br>◆ <b>武术·形意拳三层</b>: 明劲(易骨)→暗劲(易筋)→化劲(易髓)。孙禄堂《拳意述真》三层功夫。<br><span class=src>📎 CBETA T46n1911 · T10n0279 · 张伯端《悟真篇》(1075)·《荀子》劝学/解蔽 · 孙禄堂·《钟吕传道集》·《吕祖百字碑》·《老子》2/25/37/41/54/63/64/40(反者道之动弱者道之用)/65(古之善为道者非以明民将以愚之)·《庄子》知北游/寓言(寓言十九重言十七卮言日出)·《列子》汤问/天瑞/周穆王/说符</span>'}
  };

  // Generate cards from HEART_ARTICLES data with cross-references
  if(typeof HEART_ARTICLES!=='undefined' && HEART_ARTICLES.length>0){
    for(var hi=0; hi<HEART_ARTICLES.length; hi++){
      var a=HEART_ARTICLES[hi], cid='hcard'+hi;
      var wxUrl=a.url||('https://mp.weixin.qq.com/s/S2D9BOc3jFwDRQr2tbzG6g');
      // Find matching cross-ref by scanning title for keywords
      var xr=null;
      var keys=Object.keys(heartXRef);
      for(var ki=0; ki<keys.length; ki++){
        if(a.title.indexOf(keys[ki])>=0){xr=heartXRef[keys[ki]];break;}
      }
      h+="<div class=h3col id="+cid+">"
        +"<div class=h3col-l><div class=h3col-tbar>"
        +"<button onclick=\"heartCopy('"+cid+"-l')\" title=复制左栏原文>📋</button>"
        +"<button onclick=\"heartEdit('"+cid+"-l')\" title=编辑左栏>✏️</button>"
        +"<button onclick=\"heartAddNote('"+cid+"-l')\" title=添加批注>➕</button>"
        +"</div><h3 style=color:var(--gold)>"+a.title+"</h3>"
        +"<div id="+cid+"-l>"+a.body+"</div>"
        +"<p class=src>📎 <a href='"+wxUrl+"' target=_blank>原文链接</a> · 永远的犍陀罗·实修心要</p>"
        +"<textarea id="+cid+"-lcmt placeholder='💬 左栏批注...' style='width:100%;margin-top:4px;font-size:.68em;padding:3px 5px;border:1px dashed var(--line);border-radius:4px;background:var(--card);color:var(--text);resize:vertical;min-height:30px' onchange='heartSaveComment(\""+cid+"-l\")'></textarea>"
        +"</div>"
        +"<div class=h3col-r1><div class=h3col-tbar>"
        +"<button onclick=\"heartCopy('"+cid+"-r1')\" title=复制对照>📋</button>"
        +"<button onclick=\"heartEdit('"+cid+"-r1')\" title=编辑对照>✏️</button>"
        +"<button onclick=\"heartAddNote('"+cid+"-r1')\" title=添加批注>➕</button>"
        +"</div><h3 style=color:var(--gold)>📐 海云华严行法对照</h3>"
        +"<div id="+cid+"-r1>"+(xr?xr.r1:'(对照内容待补)')+"</div>"
        +"<textarea id="+cid+"-r1cmt placeholder='💬 中栏批注...' style='width:100%;margin-top:4px;font-size:.68em;padding:3px 5px;border:1px dashed var(--line);border-radius:4px;background:var(--card);color:var(--text);resize:vertical;min-height:30px' onchange='heartSaveComment(\""+cid+"-r1\")'></textarea>"
        +"</div>"
        +"<div class=h3col-r2><div class=h3col-tbar>"
        +"<button onclick=\"heartCopy('"+cid+"-r2')\" title=复制印证>📋</button>"
        +"<button onclick=\"heartEdit('"+cid+"-r2')\" title=编辑印证>✏️</button>"
        +"<button onclick=\"heartAddNote('"+cid+"-r2')\" title=添加批注>➕</button>"
        +"</div><h3 style=color:#5e8b9e>🔍 佛门诸宗·道门·儒门·诸行者印证</h3>"
        +"<div id="+cid+"-r2>"+(xr?xr.r2:'(印证内容待补)')+"</div>"
        +"<textarea id="+cid+"-cmt placeholder='💬 批注...' style='width:100%;margin-top:8px;font-size:.7em;padding:4px;border:1px dashed var(--line);border-radius:4px;background:var(--card);color:var(--text);resize:vertical;min-height:36px' onchange='heartSaveComment(\""+cid+"\")'></textarea>"
        +"</div></div>";
    }
  }else{
    h+="<p style=color:var(--text2)>⚠ 实修心要文章数据未加载(HEART_ARTICLES为空)。请检查build.py是否正确读取docs/hy_refs/wechat/目录。</p>";
  }

  h+="</div>"; // close med-heart
  h+="</div>"; // close pv-meditation

  // ═══════════════════════════════════════════
  // SUB-PAGE 3: 实修心要 (hidden)
  // ═══════════════════════════════════════════

  // Auto-restore saved data (only right columns, not left article text)
  setTimeout(function(){
    var raw=null;try{raw=localStorage.getItem('huayan_heart_data_v2');
    if(!raw)return;}catch(e){return;}
    try{var data=JSON.parse(raw);
    if(data.edits){Object.keys(data.edits).forEach(function(id){
      if(id.indexOf('-l')>=0)return; // skip left column (article text)
      var el=document.getElementById(id);if(el){el.innerHTML=data.edits[id];}
    });}
    if(data.notes){Object.keys(data.notes).forEach(function(id){
      var el=document.getElementById(id);if(el){(data.notes[id]||[]).forEach(function(n){var d=document.createElement('div');d.className='heart-note';d.innerHTML=n;el.appendChild(d);});}
    });}
    }catch(e){}
  },500);

  // ═══════════════════════════════════════════
  // SUB-PAGE 4: 讲法资源 (hidden, was #3 before 实修心要 added)
  // ═══════════════════════════════════════════
  // ═══════════════════════════════════════════
  // SUB-PAGE: 最新动态 (动态类内容集中)
  // ═══════════════════════════════════════════
  h+="<div id=pv-news class=pv-section style='display:block'>";
  h+="<div class=section style='border-left:4px solid var(--gold)'><h2>📰 最新动态（2023-2026）</h2><p>2023: 国立台北大学杰出校友 · 2026: 九九华严TICC讲座 · 2026.7: 支提山动土 · 第四期佛教。</p></div>";

  h+="<div class=section id=news-academic><h2>🎓 学术活动轨迹 (2010-2025)</h2>";
  h+="<table class=v-table><tr><th>年份</th><th>会议/事件</th><th>主题</th></tr>";
  h+="<tr><td>2010</td><td>第一届华严学术研讨会</td><td>华严学</td></tr>";
  h+="<tr><td>2011</td><td>第二届华严学术研讨会</td><td>华严与科学</td></tr>";
  h+="<tr><td>2011</td><td>首届中国华严国际学术研讨会（西安）</td><td>《华严经》的文献、思想以及修持</td></tr>";
  h+="<tr><td>2013</td><td>海云华严研究所成立（熊琬教授任所长）</td><td>依传统国学研读古德判教注疏</td></tr>";
  h+="<tr><td>2017</td><td>华严学国际论坛</td><td>新时代的华严判教探讨</td></tr>";
  h+="<tr><td>2019</td><td>华严学国际论坛</td><td>华严义学与华严宗史</td></tr>";
  h+="<tr><td>2024-2025</td><td>第一届新世纪永续发展国际学术研讨会</td><td>环境・人文・智慧（与国立台北大学合办）</td></tr>";
  h+="<tr><td>2011-至今</td><td>《华严学报》（已出版14期）</td><td>汇集研讨会及学界最新研究成果</td></tr>";
  h+="</table></div>";

  h+="</div>"; // close pv-news

  h+="<div id=pv-chan_traces class=pv-section style=display:none>";
  h+=renderChanTraces();
  h+="</div>";

  h+="<div id=pv-chengguan class=pv-section style=display:none>";
  h+=renderChengguanSection();
  h+="</div>";


  h+="<div id=pv-vinaya class=pv-section style=display:none>";
  h+=renderVinayaSection();
  h+="</div>";

  h+="<div id=pv-faxiang class=pv-section style=display:none>";
  h+=renderFaxiangSection();
  h+="</div>";

  h+="<div id=pv-yikong class=pv-section style=display:none>";
  h+=renderYikongSection();
  h+="</div>";
  h+="<div id=pv-mimi class=pv-section style=display:none>";
  h+=renderMimiSection();
  h+="</div>";
  h+="<div id=pv-tiantai class=pv-section style=display:none>";
  h+=renderTiantaiSection();
  h+="</div>";
  h+="<div id=pv-resources class=pv-section style=display:none>";

  // ── 全网讲法总目 ──
  h+="<div class=section id=res-total><h2>📡 海云继梦全网讲法总目</h2>";
  h+="<table class=v-table><tr><th>平台</th><th>内容</th><th>规模</th><th>类型</th></tr>";
  h+="<tr><td><b>Bilibili</b></td><td>华严六科(42h)·善财五十三参·禅法开示</td><td>500+视频</td><td>📺视频</td></tr>";
  h+="<tr><td><b>Apple Podcast</b></td><td>普贤乘华严宗: 20+系列(华严学概论·禅行法·密法·净土)</td><td>2000+集</td><td>🎧音频</td></tr>";
  h+="<tr><td><b>Spotify</b></td><td>普贤乘华严宗(每周一/三更新)</td><td>2000+集</td><td>🎧音频</td></tr>";
  h+="<tr><td><b>YouTube</b></td><td><a href='https://www.youtube.com/@huayen-world' target=_blank>@huayen-world</a> · 大华严寺官方频道·讲经合集</td><td>300+视频</td><td>📺视频</td></tr>";
  h+="<tr><td><b>抖音</b></td><td>#海云继梦导师 每日法语</td><td>1000+短片</td><td>📱短视频</td></tr>";
  h+="<tr><td><b>fjdh.cn</b></td><td>华严六科·禅修正行·禅观·讲记逐字稿</td><td>50+文稿</td><td>📝文字</td></tr>";
  h+="<tr><td><b>学佛网</b></td><td>华严禅行法·福慧滋长·修行问答</td><td>100+文稿</td><td>📝文字</td></tr>";
  h+="<tr><td><b>大华严寺</b></td><td>修行蓝图·法脉传承·最新动态</td><td>50+页面</td><td>🌐网页</td></tr>";
  h+="</table></div>";

  // ── 按主题分类讲法资源 ──
  h+="<div class=section id=res-topics><h2>📚 按主题分类讲法资源</h2>";
  h+="<p style=font-size:0.78em;color:var(--text2);margin-bottom:10px>以下按海云法师的讲法主题分类。每类附 YouTube/Bilibili 搜索链接，可直接跳转。</p>";

  // Topic cards
  var topics=[
    {t:'📖 华严经讲记系列',d:'《华严经导读》(三册)《探玄记悬谈讲记》(四册)《世主妙严品》《光明觉品》《净行品》《贤首品》《明法品》《普贤三昧品》《普贤行品》《四圣谛品》等单品讲记。2006年11月-2010年6月北京广化寺《四十华严》全本讲记。',yt:'华严经+海云继梦',bl:'华严经+海云继梦'},
    {t:'🧘 禅修系列',d:'《禅修入门》(2020)《禅修正行——安那般那数息观》(2017)《禅修前行》《禅观概论》(2011)《禅，怎么参？》(2011)《华严禅行法》系列（含《禅修正行》《禅观》等辑）。核心: 安般守意·置心一处·三摩地次第。',yt:'海云继梦+禅修',bl:'海云继梦+禅修'},
    {t:'🔮 密法系列',d:'《根本佛母——准提密法》(2020再版)《神圣的游戏场——华严密法》《生命密境——曼荼罗的世界》《深深密——密行指引》《悠活三昧》《本尊曾于此——十一面观音密法》。贤首宗本宗密法: 秽迹金刚法。',yt:'海云继梦+密法',bl:'海云继梦+密法'},
    {t:'📕 三部曲',d:'《非常坛经》(4册·2004)《非常金刚经》《非常心经》——主张「要懂《心经》先懂《金刚经》，要懂《金刚经》先懂《坛经》」。三经共同构成修行理论体系。',yt:'海云继梦+坛经+金刚经+心经',bl:'海云继梦+心经'},
    {t:'👣 善财五十三参',d:'以《四十华严》（即《入法界品》）为本，逐参讲授。整套「制度性入门—果位对应」蓝图即是他解读善财童子在文殊菩萨座下修学历程时所展开的具体框架。',yt:'海云继梦+善财',bl:'海云继梦+善财'},
    {t:'🌏 地藏/药师系列',d:'《开启灵性的钥匙》(上下·2018)《就从这里入法界——地藏菩萨行法》(2011)《转吧！地藏象限》(2018)《叩问药师佛的法界密码》(2018)《成佛方程式——药师经讲记》(2018)。',yt:'海云继梦+地藏+药师',bl:'海云继梦+地藏'},
    {t:'🙏 净土/行愿系列',d:'《从极乐世界迈向永恒的生命——解弥陀经》(2011)《普贤十大愿王行法精要》(2011)《十大愿王修行法要》。华严与净土法门的会通。',yt:'海云继梦+净土+普贤',bl:'海云继梦+普贤'},
    {t:'💡 生活应用系列',d:'《认真最幸福》(2005)《看见幸福》(2006)《幸福就这样》(2006)《生命故乡的呼唤01——让心活起来》(2019)《幸福冏小孩》(2014)《我们只有一个选择》(2010)。围绕五大人生议题: 事业/健康/家庭/青少年/老人。',yt:'海云继梦+幸福+人生',bl:'海云继梦+人生'},
    {t:'🆕 九九华严（2026最新）',d:'于台北国际会议中心(TICC)举行，为期五年，每月举办。定位: 将华严哲理转化为现代心理学与生命科学语言，回应AI时代挑战。新一季已「从传承走向新时代」，正式进入经文本文讲授。',yt:'九九华严+海云继梦',bl:'九九华严+海云继梦'}
  ];
  topics.forEach(function(tp){
    h+="<div class=topic-card><h4>"+tp.t+"</h4><p>"+tp.d+"</p>";
    h+="<a href='https://www.youtube.com/results?search_query="+encodeURIComponent(tp.yt)+"' target=_blank>▶ YouTube</a> · ";
    h+="<a href='https://search.bilibili.com/all?keyword="+encodeURIComponent(tp.bl)+"' target=_blank>📺 Bilibili</a> · ";
    h+="<a href='https://podcasts.apple.com/au/podcast/%E6%99%AE%E8%B3%A2%E4%B9%98%E8%8F%AF%E5%9A%B4%E5%AE%97/id1523368889' target=_blank>🎙 Podcast</a>";
    h+="</div>";
  });
  h+="</div>";

  // ── 著作清单 ──
  h+="<div class=section id=res-books><h2>📖 海云继梦著作（空庭书苑/光潽文创出版·2002-2026）</h2><p style=font-size:0.8em;line-height:1.9>";
  h+="<b>华严经讲记系列:</b> 《华严经导读》(三册) · 《探玄记悬谈讲记》(四册) · 《华严学导论》(ⅠⅡ) · 《世主妙严品》《光明觉品》《净行品》《贤首品》《明法品》《普贤三昧品》《普贤行品》《四圣谛品》讲记 · 《四十华严》全本讲记(2006-2010北京广化寺)<br>";
  h+="<b>三部曲:</b> 《非常坛经》(4册·2004) · 《非常金刚经》 · 《非常心经》——主张「要懂《心经》先懂《金刚经》，要懂《金刚经》先懂《坛经》」<br>";
  h+="<b>禅修系列:</b> 《禅修入门》(2020) · 《禅修正行——安那般那数息观》(2017) · 《禅修前行》 · 《禅观概论》(2011) · 《禅，怎么参？》(2011) · 《禅，就要这么参！》(2011)<br>";
  h+="<b>解密系列:</b> 《根本佛母——准提密法》(2020再版) · 《神圣的游戏场——华严密法》 · 《生命密境——曼荼罗的世界》 · 《深深密——密行指引》 · 《悠活三昧》<br>";
  h+="<b>地藏/药师系列:</b> 《开启灵性的钥匙》(上下·2018) · 《就从这里入法界——地藏菩萨行法》(2011) · 《转吧！地藏象限》(2018) · 《叩问药师佛的法界密码》(2018) · 《成佛方程式——药师经讲记》(2018)<br>";
  h+="<b>净土/行愿系列:</b> 《从极乐世界迈向永恒的生命——解弥陀经》(2011) · 《普贤十大愿王行法精要》(2011) · 《十大愿王修行法要》<br>";
  h+="<b>生活应用:</b> 《认真最幸福》(2005) · 《看见幸福》(2006) · 《幸福就这样》(2006) · 《生命故乡的呼唤01——让心活起来》(2019) · 《幸福冏小孩》(2014) · 《我们只有一个选择》(2010)<br>";
  h+="<b>最新出版(2025-2026):</b> 《华严经在说什么——九九华严玄谈01·02》(2026) · 《在妄念中觉醒——普贤心经讲记》(2025) · 《摆脱焦虑与杂念的三十七个秘诀》(2025)<br>";
  h+="<b>英文著作:</b> <i>Huayen World: Teachings and Meditation Methods in Mahayana Buddhism</i> (Kongting Shuyuan, 2005) — 据查证为目前唯一确认出版的英文著作<br>";
  h+="<b>出版方:</b> 繁体版由空庭书苑/光潽文创出版(博客来·FindBook·乐天KOBO可购)；简体版曾由九州出版社(2011)、宗教文化出版社(2005)、海南出版社(2016)等在中国大陆发行。</p></div>";

  // ── YouTube 频道卡片 ──
  var ytChannels=[
    {handle:'@huayen-world',id:'UCJr3ifkvTs76XnR6SuyIfFQ',name:'大華嚴寺官方頻道',color:'#c46b5d',desc:'海云继梦导师讲经全集。华严经/禅修/密法/药师经/地藏经等系列讲法。每周持续更新。',series:'海雲法語·華嚴教海·Shorts·藥師經講座'}
    // 更多频道在此追加，格式: {handle, id, name, color, desc, series}
  ];
  h+="<div class=section><h2>🎬 YouTube 频道</h2>";
  h+="<div style='display:flex;gap:12px;flex-wrap:wrap;margin-bottom:12px'>";
  ytChannels.forEach(function(ch){
    h+="<div style='flex:1;min-width:250px;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px'>";
    h+="<div style='font-weight:600;color:"+ch.color+";margin-bottom:6px'>▶ "+ch.name+"</div>";
    h+="<p style=font-size:0.8em;color:var(--text2);line-height:1.6>"+ch.desc+"<br>";
    h+="🔗 <a href='https://www.youtube.com/"+ch.handle+"' target=_blank>youtube.com/"+ch.handle+"</a> (直达频道)<br>";
    h+="📺 <a href='https://www.youtube.com/"+ch.handle+"/videos' target=_blank>全部视频</a> · ";
    h+="📋 <a href='https://www.youtube.com/"+ch.handle+"/playlists' target=_blank>播放清单</a><br>";
    h+="<span style=font-size:0.7em;color:var(--text2)>系列: "+ch.series+"</span></p></div>";
  });
  h+="<div style='flex:1;min-width:250px;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px'>";
  h+="<div style='font-weight:600;color:#5e8b9e;margin-bottom:6px'>📺 Bilibili · 海雲繼夢講經全集</div>";
  h+="<p style=font-size:0.8em;color:var(--text2);line-height:1.6>《华严六科》42小时完整版·善财童子五十三参·禅法开示等。<br>";
  h+="🔗 <a href='https://search.bilibili.com/all?keyword=%E6%B5%B7%E4%BA%91%E7%BB%A7%E6%A2%A6' target=_blank>在Bilibili中搜索</a></p></div>";
  h+="</div>";
  h+="<p style=line-height:1.8;margin-top:8px>";
  h+="🎙 <a href='https://podcasts.apple.com/au/podcast/%E6%99%AE%E8%B3%A2%E4%B9%98%E8%8F%AF%E5%9A%B4%E5%AE%97/id1523368889' target=_blank>Apple Podcast</a> · ";
  h+="<a href='https://open.spotify.com/show/2ZDlq4cOOiynQvlzPARkmc' target=_blank>Spotify</a> (20+系列·每周更新) | ";
  h+="🌐 <a href='https://www.huayenworld.org/' target=_blank>大华严寺官网</a> · ";
  h+="<a href='https://www.huayenworld.org/%e8%8f%af%e5%9a%b4%e7%a6%aa%e7%b0%a1%e4%bb%8b%e7%89%b9%e8%89%b2/' target=_blank>修行蓝图全文</a>";
  h+="</p></div>";

  // ── YouTube 频道 (从 PRACTICE_DATA.youtube_playlists 数据驱动) ──
  h+=renderYoutubeSection();
  h+=renderAvatamsakaLectures();
  h+=renderMengcanSection();
  h+=renderPracticeSources();

  // ── 学术活动轨迹 ──
  // ── 相关道场 ──
  h+="<div class=section id=res-temples><h2>🏛 相关道场</h2><p style=line-height:1.8>";
  h+="📍 <b>南投大华严寺</b> — 海云继梦导师·普贤乘根本道场<br>";
  h+="📍 <b>苗栗支提山大华严寺</b> — 2026.7.9动土·面向台湾海峡·与福建支提华严祖庭隔海相望<br>";
  h+="📍 <b>台北福慧寺</b> — 钦因长老·高原法系<br>";
  h+="📍 <b>台北华严莲社</b> — 贤度法师·华严专宗学院<br>";
  h+="📍 <b>陕西师范大学华严研究所</b> — 海云法师曾任荣誉所长及客座教授</p></div>";

  // ── 检索整理资源总目录 (2026-08, 从 data/practice/haiyun_resources.yaml 注入) ──
  try{
    var hyRes=(typeof HAIYUN_RESOURCES!=='undefined')?HAIYUN_RESOURCES:null;
    if(hyRes){
      h+="<div class=section id=res-more style='border-left:4px solid var(--gold)'><h2>🔍 海云法师资源总目录（检索整理 2026-08）</h2><p style=font-size:0.75em;color:var(--text2)>以下为网络公开检索结果，供查阅参考，以官网为准。</p></div>";
      // YouTube (与上方原有板块合并: 仅显示系列补遗)
      if(hyRes.youtube&&hyRes.youtube.series){
        h+="<div class=section><h2>📺 YouTube 系列补遗</h2>";
        hyRes.youtube.series.forEach(function(s){
          h+="<span class=tag style='background:rgba(196,107,93,0.1);color:#c46b5d'>"+s.name+(s.note?' · '+s.note:'')+"</span>";
        });
        h+="<br><a href='"+(hyRes.youtube.channel.url||'')+"' target=_blank style=font-size:0.75em;color:var(--blue)>访问大华严寺频道</a></div>";
      }
      // Bilibili
      if(hyRes.bilibili){
        h+="<div class=section><h2>📺 B站系列</h2>";
        if(hyRes.bilibili.series)hyRes.bilibili.series.forEach(function(s){
          h+="<span class=tag style='background:rgba(125,154,110,0.1);color:#7d9a6e'>"+s.name+(s.note?' · '+s.note:'')+(s.url?' · <a href='+s.url+' target=_blank style=color:var(--blue)>观看</a>':'')+"</span>";
        });
        h+="<br><a href='"+(hyRes.bilibili.search||'')+"' target=_blank style=font-size:0.75em;color:var(--blue)>🔍 B站搜索更多</a></div>";
      }
      // Publications (与上方著作清单合并: 仅显示2026新书)
      if(hyRes.publications&&hyRes.publications.newest){
        h+="<div class=section><h2>📚 最新出版</h2>";
        hyRes.publications.newest.forEach(function(p){
          h+="<div class=stage-box><b>🆕 "+p.title+"</b> ("+p.year+")<br>"+(p.note||'')+"</div>";
        });
        h+="</div>";
      }
      // Activities
      if(hyRes.activities){
        h+="<div class=section><h2>🎤 社会活动与学术演讲</h2>";
        hyRes.activities.forEach(function(a){
          h+="<div class=topic-card><h4>"+(a.year?a.year+' — ':'')+a.title+"</h4><p>"+(a.note||'')+(a.url?' <a href='+a.url+' target=_blank>详情</a>':'')+"</p></div>";
        });
        h+="</div>";
      }
      // Text teachings
      if(hyRes.text_teachings){
        h+="<div class=section><h2>📝 文字开示（置心一处等实修心要）</h2>";
        hyRes.text_teachings.forEach(function(t){
          h+="<p style=font-size:0.75em;margin:3px 0>🔗 <a href='"+t.url+"' target=_blank style=color:var(--blue)>"+t.title+"</a>"+(t.note?' — <span style=color:var(--text2)>'+t.note+'</span>':'')+"</p>";
        });
        h+="</div>";
      }
      // Official
      if(hyRes.official){
        h+="<div class=section><h2>🏛 官方资源</h2>";
        hyRes.official.forEach(function(o){
          h+="<p style=font-size:0.78em>🌐 <a href='"+(o.url||'#')+"' target=_blank style=color:var(--blue)>"+(o.name||'')+"</a>"+(o.note?' — '+o.note:'')+"</p>";
        });
        h+="</div>";
      }
    }
  }catch(e){console.error('haiyun_resources error:',e);}

  h+="<div class=section id=res-sources><h2>📚 信实可靠的出处与参考资源</h2>";
  h+="<p style=font-size:.8em;color:var(--text2);margin-bottom:10px>以下为本文所依据的全部第一手来源。内容以<b>大华严寺官方资料.海云继梦和上讲经逐字稿.正式出版物</b>为主,凡涉及诠释性跨度之处均已随文标注。</p>";

  h+="<table class=v-table style=font-size:.7em><tr><th>类别</th><th>资源名称</th><th>详情</th><th>获取方式</th></tr>";
  h+="<tr><td>📖书籍</td><td>《非常占察经》一.二.三册</td><td>海雲和上《占察善恶业报经》讲记.空庭书苑 2015-2017. ISBN: 9789867484918/4932/4949</td><td><a href='https://www.got1shop.com/goods.php?id=281160' target=_blank>购买</a> . <a href='https://webpac.taichung.gov.tw/bookDetail/670127' target=_blank>图书馆</a></td></tr>";
  h+="<tr><td>📖书籍</td><td>《海云继梦禅观概论》</td><td>空庭书苑 2015. ISBN: 9789867484888</td><td><a href='https://got1dev.got1shop.com/goods.php?id=219111' target=_blank>购买</a></td></tr>";
  h+="<tr><td>📖书籍</td><td>《迈向佛陀的境界——华严禅前行概论》</td><td>空庭书苑 2011. ISBN: 9789867484512</td><td><a href='https://play.google.com/store/books/details?id=Mm36CgAAQBAJ' target=_blank>Google Play</a></td></tr>";
  h+="<tr><td>🎙播客</td><td>普賢乘華嚴宗 S18《佔察善惡業報經》</td><td><b>46集</b>(已完结). 2013年高雄/台北开示</td><td><a href='https://podcasts.apple.com/au/podcast/%E6%99%AE%E8%B3%A2%E4%B9%98%E8%8F%AF%E5%9A%B4%E5%AE%97/id1523368889' target=_blank>Apple Podcast</a> . <a href='https://open.spotify.com/show/2ZDlq4cOOiynQvlzPARkmc' target=_blank>Spotify</a></td></tr>";
  h+="<tr><td>📺视频</td><td>大華嚴寺官方YouTube @huayen-world</td><td>海雲法語.華嚴教海.Shorts.藥師經講座.九九華嚴</td><td><a href='https://www.youtube.com/@huayen-world' target=_blank>YouTube频道</a></td></tr>";
  h+="<tr><td>📝文字</td><td>fjdh.cn 佛教导航 — 海云继梦文集</td><td>《华严禅行法—禅观》逐字稿.《禅修正行》系列.《四十华严讲记》第67讲</td><td><a href='https://www.fjdh.cn/wumin/2013/11/165329303084.html' target=_blank>禅观第四集</a> . <a href='https://www.fjdh.cn/wumin/2013/09/155711285715.html' target=_blank>停心.观心</a></td></tr>";
  h+="<tr><td>🌐官网</td><td>大华严寺全球资讯网 huayenworld.org</td><td>「华严禅」专栏: 源流与传承.修行蓝图.资粮道.占察行法</td><td><a href='https://www.huayenworld.org/' target=_blank>官网首页</a> . <a href='https://www.huayenworld.org/%e8%8f%af%e5%9a%b4%e7%a6%aa%e7%b0%a1%e4%bb%8b%e7%89%b9%e8%89%b2/' target=_blank>修行蓝图全文</a></td></tr>";
  h+="<tr><td>🌐经典</td><td>CBETA 《占察善恶业报经》</td><td>大正藏 T17n0839.天竺三藏菩提灯译</td><td><a href='https://cbeta.buddhism.org.hk/xml/T17/T17n0839_002.xml' target=_blank>CBETA 原文</a></td></tr>";
  h+="<tr><td>📄论文</td><td>《普贤乘禅观行法初探》</td><td>海云继梦 著.台湾佛教学术期刊</td><td><a href='https://buddhism.lib.ntu.edu.tw/FT/JA/576036.pdf' target=_blank>NTU佛学图书馆 PDF</a></td></tr></table>";

  h+="<p style=font-size:.7em;color:var(--text2);margin-top:8px;line-height:1.6>⚠ <b>来源可靠性说明:</b> (1)大华严寺官网为第一手道场官方资料 (2)讲经逐字稿(fjdh.cn.学佛网)为法师本人第一人称陈述 (3)正式出版物(空庭书苑)为经编辑审定的公开文本。凡涉及道场自身历史叙事.术语诠释性跨度.以及第三四次灌顶的具体内容等,均已在本文中随文标注存疑或说明。建议进一步参阅《华严学报》(已出版14期)等学术出版物。</p>";
  h+="</div>";
  h+="</div>"; // close pv-resources

  pv.innerHTML=h;
}

// ═══ PRACTICE SUB-NAV ═══
function switchPracticeView(view,btn){
  document.querySelectorAll(".pv-nav").forEach(function(b){b.classList.remove("active");});
  if(btn)btn.classList.add("active");
  document.querySelectorAll(".pv-section").forEach(function(s){s.style.display="none";});
  var pvEl=document.getElementById("pv-"+view);
  if(pvEl)pvEl.style.display="block";
  // 独立文章入口条（若本子页对应某篇完整文章的独立页）
  try{articleChip(view,'#pv-'+view);}catch(e){};
  try{localStorage.setItem('practice_sub',view);}catch(e){};
  // Force-reload lazy images when switching to heart (now med-heart)
  if(view==='meditation'){setTimeout(function(){
    document.querySelectorAll('#med-heart img').forEach(function(img){
      var s=img.src;img.src='';img.src=s;
    });
  },200);}
}
// ═══ 华严经讲法全目渲染 (从 PRACTICE_DATA.haiyun_avatamsaka_lectures) ═══
function renderAvatamsakaLectures() {
  var al = (typeof PRACTICE_DATA !== 'undefined' && PRACTICE_DATA.haiyun_avatamsaka_lectures) ? PRACTICE_DATA.haiyun_avatamsaka_lectures : null;
  if (!al) return '';
  var h = '<div class=section id=res-avatamsaka><h2>📜 华严经讲法全目 — 整体·玄谈·品目';
  if (al.overview && al.overview.title_en) h += '<span class="en-line" style="font-size:0.62em;display:block;color:var(--text2);margin-top:2px">' + al.overview.title_en + '</span>';
  h += '</h2>';
  if (al.overview) {
    h += '<p style="font-size:0.75em;color:var(--text2)">' + al.overview.note + '</p>';
    if (al.overview.note_en) h += '<p class="en-line" style="font-size:0.75em;color:var(--text2)">📖 ' + al.overview.note_en.replace(/\n/g,' ') + '</p>';
  }

  // ── 整体讲法 ──
  h += '<h3 style="color:var(--gold);margin-top:10px">📚 一、整体讲法</h3>';
  (al.overall||[]).forEach(function(o) {
    h += '<div class=topic-card style=font-size:0.78em>';
    h += '<b>' + o.title + '</b>' + (o.title_en?' <span class="en-line" style=color:var(--text2)>(' + o.title_en + ')</span>':'') + ' — ' + (o.publisher||'') + ' · ' + (o.year||'') + ' · ' + (o.length||o.format||'');
    h += '<br><span style=color:var(--text2)>' + (o.content||'').replace(/\n/g,'<br>') + '</span>';
    if (o.content_en) h += '<div class="en-line" style="color:var(--text2);font-size:0.95em;line-height:1.7;margin-top:3px">📖 ' + o.content_en.replace(/\n/g,' ') + '</div>';
    if (o.isbn_start) h += '<br>ISBN: ' + o.isbn_start;
    if (o.links) {
      h += '<br>';
      Object.keys(o.links).forEach(function(k) {
        h += '<a href="' + o.links[k] + '" target=_blank style="font-size:0.85em;color:var(--blue)">' + k + '</a> ';
      });
    }
    h += '</div>';
  });

  // ── 玄谈系列 ──
  h += '<h3 style="color:var(--gold);margin-top:10px">🔮 二、玄谈系列</h3>';
  (al.xuantan||[]).forEach(function(x) {
    h += '<div class=topic-card style=font-size:0.78em>';
    h += '<b>' + x.title + '</b>' + (x.title_en?' <span class="en-line" style=color:var(--text2)>(' + x.title_en + ')</span>':'') + ' — ' + (x.platform||x.format||'') + ' · ' + (x.publisher||'');
    h += '<br><span style=color:var(--text2)>' + (x.content||'').replace(/\n/g,'<br>') + '</span>';
    if (x.content_en) h += '<div class="en-line" style="color:var(--text2);font-size:0.95em;line-height:1.7;margin-top:3px">📖 ' + x.content_en.replace(/\n/g,' ') + '</div>';
    if (x.links) {
      h += '<br>';
      Object.keys(x.links).forEach(function(k) {
        h += '<a href="' + x.links[k] + '" target=_blank style="font-size:0.85em;color:var(--blue)">' + k + '</a> ';
      });
    }
    h += '</div>';
  });

  // ── 品目解说 ──
  h += '<h3 style="color:var(--gold);margin-top:10px">📖 三、品目解说</h3>';
  h += '<table class=v-table style=font-size:0.75em><tr><th>品目</th><th>讲题</th><th>平台/载体</th><th>直达</th></tr>';
  (al.chapters||[]).forEach(function(ch) {
    h += '<tr><td><b>' + ch.chapter + '</b></td><td>' + ch.title + '</td><td>' + (ch.platform||ch.publisher||'') + '</td>';
    h += '<td>';
    if (ch.links) Object.keys(ch.links).forEach(function(k) { h += '<a href="' + ch.links[k] + '" target=_blank>' + k + '</a> '; });
    h += '</td></tr>';
    if (ch.title_en || ch.content_en) {
      h += '<tr class="en-line"><td></td><td colspan=3 style="font-size:0.72em;color:var(--text2);line-height:1.7">📖 ' + (ch.title_en||'') + (ch.title_en&&ch.content_en?' — ':'') + (ch.content_en||'').replace(/\n/g,' ') + '</td></tr>';
    }
  });
  h += '</table>';

  // ── Podcast ──
  if (al.podcast_huayan) {
    var ph = al.podcast_huayan;
    h += '<h3 style="color:var(--gold);margin-top:10px">🎧 四、播客全季</h3>';
    h += '<p style=font-size:0.78em><b>' + ph.name + '</b>' + (ph.name_en?' <span class="en-line" style=color:var(--text2)>(' + ph.name_en + ')</span>':'') + ' — ' + ph.platforms + '</p>';
    h += '<p style=font-size:0.75em;color:var(--text2)>华严相关季: ' + (ph.huayan_seasons||[]).join(' · ') + '</p>';
    h += '<p style=font-size:0.72em>';
    Object.keys(ph.links||{}).forEach(function(k) { h += '<a href="' + ph.links[k] + '" target=_blank>' + k + '</a> '; });
    h += '</p>';
  }

  // ── 视频 ──
  if (al.video) {
    h += '<h3 style="color:var(--gold);margin-top:10px">📺 五、视频资源</h3>';
    al.video.forEach(function(v) {
      h += '<div class=topic-card style=font-size:0.75em><b>' + v.title + '</b>' + (v.title_en?' <span class="en-line" style=color:var(--text2)>(' + v.title_en + ')</span>':'') + ' — ' + v.platform + '<br>';
      if (v.content_en) h += '<div class="en-line" style="color:var(--text2);line-height:1.7;margin:2px 0">📖 ' + v.content_en + '</div>';
      (v.subjects||[]).forEach(function(s) { h += '🔹 ' + s + '<br>'; });
      h += '<a href="' + v.link + '" target=_blank>直达</a></div>';
    });
  }

  // ── 快速索引 ──
  if (al.quick_index) {
    var qi = al.quick_index;
    h += '<details style=font-size:0.72em;margin-top:8px><summary>🔍 快速索引</summary>';
    Object.keys(qi).forEach(function(k) {
      h += '<p><b>' + k + '</b>: ';
      Object.keys(qi[k]).forEach(function(sk) {
        h += '<br>  ' + sk + ': ' + qi[k][sk];
      });
      h += '</p>';
    });
    h += '</details>';
  }

  h += '</div>';
  return h;
}

// ═══ YouTube 渲染 (从 PRACTICE_DATA.youtube_playlists) ═══
function renderYoutubeSection() {
  var yt = (typeof PRACTICE_DATA !== 'undefined' && PRACTICE_DATA.youtube_playlists) ? PRACTICE_DATA.youtube_playlists : null;
  if (!yt || !yt.channel) return '<div class=section id=res-yt><h2>📺 YouTube 频道</h2><p style=color:var(--text2)>数据载入中…</p></div>';
  var ch = yt.channel, pls = yt.playlists || [];
  var h = '<div class=section id=res-yt><h2>📺 YouTube 频道 · 播放清单</h2>';
  h += '<p style=font-size:0.78em;color:var(--text2);margin-bottom:8px>' + ch.description.replace(/\n/g,'<br>') + '</p>';
  if (ch.description_en) h += '<p class="en-line" style=font-size:0.78em;color:var(--text2);margin-bottom:8px>📖 ' + ch.description_en.replace(/\n/g,' ') + '</p>';
  h += '<table class=v-table><tr><th>图标</th><th>系列</th><th>类型</th><th>内容</th><th>直达</th></tr>';
  pls.forEach(function(p) {
    var url = p.url_playlist || p.url_shorts || p.url_search || ch.playlists_url;
    h += '<tr><td>' + (p.icon||'📌') + '</td><td><b>' + p.name_zh + '</b><br><span style=font-size:0.7em;color:var(--text2)>' + (p.name_en||'') + '</span></td>';
    h += '<td style=font-size:0.78em>' + p.type + (p.type_en ? ' <span class="en-line" style=font-size:0.88em;color:var(--text2)>(' + p.type_en + ')</span>' : '') + '</td>';
    h += '<td style=font-size:0.75em>' + p.description.replace(/\n/g,'<br>');
    if (p.description_en) h += '<span class="en-line" style=display:block;font-size:0.88em;color:var(--text2);margin-top:3px>📖 ' + p.description_en.replace(/\n/g,' ') + '</span>';
    h += '</td>';
    h += '<td><a href="' + url + '" target=_blank>直达</a></td></tr>';
  });
  h += '</table>';
  h += '<p style=font-size:0.72em;color:var(--text2);margin-top:6px>📌 RSS: <code>' + ch.rss_feed + '</code> · <a href="' + ch.playlists_url + '" target=_blank>全部播放清单</a></p>';
  // Related platforms
  if (yt.related_platforms) {
    h += '<details style=font-size:0.75em;margin-top:8px><summary>🌐 关联平台 (' + yt.related_platforms.length + '个)</summary>';
    yt.related_platforms.forEach(function(rp) {
      h += '<p style=margin:2px 0>🔗 <a href="' + rp.url + '" target=_blank>' + rp.name + '</a>';
      if (rp.sections) h += ' — <span style=color:var(--text2)>' + rp.sections.join(' · ') + '</span>';
      h += '</p>';
    });
    h += '</details>';
  }
  h += '</div>';
  return h;
}

// ═══ 华严判教渲染 (从 PRACTICE_DATA.huayan_panjiao) ═══
function renderPanjiaoSection() {
  var pj = (typeof PRACTICE_DATA !== 'undefined' && PRACTICE_DATA.huayan_panjiao) ? PRACTICE_DATA.huayan_panjiao : null;
  if (!pj || !pj.sections) return '';
  var h = '';
  pj.sections.forEach(function(sec) {
    if (sec.id === 'wujiao') {
      // ── 五教表格 ──
      h += '<div class=section id=med-wujiao><h2>📐 ' + sec.title + '</h2>';
      if (sec.title_en) h += '<div class="en-line" style=font-size:0.72em;color:var(--text2);margin-bottom:4px>' + sec.title_en + '</div>';
      h += '<p style=font-size:.8em;color:var(--text2)>' + sec.description.replace(/\n/g,'<br>') + '</p>';
      if (sec.description_en) h += '<p class="en-line" style=font-size:.8em;color:var(--text2)>📖 ' + sec.description_en.replace(/\n/g,' ') + '</p>';
      h += '<p style=font-size:.72em;color:var(--text2)>📎 ' + sec.classic_ref + '</p>';
      h += '<table class=v-table style=font-size:.72em><tr><th>五教</th><th>别名</th><th>核心教义</th><th>海云法师判摄</th></tr>';
      (sec.teachings||[]).forEach(function(t) {
        h += '<tr><td><b>' + t.name + '</b></td>';
        h += '<td style=font-size:0.75em>' + (t.also_called||'') + '</td>';
        h += '<td style=font-size:0.75em>' + (t.doctrine||'') + '<br><span style=color:var(--text2)>' + (t.key_concept||'') + '</span></td>';
        h += '<td style=font-size:0.75em;color:var(--text2)>' + (t.position||'') + '</td></tr>';
        if (t.name_en || t.doctrine_en || t.position_en) {
          var enp = [];
          enp.push('<b>' + (t.name_en||t.name) + '</b>' + (t.also_called_en ? ' — ' + t.also_called_en : ''));
          if (t.doctrine_en) enp.push(t.doctrine_en + (t.key_concept_en ? ' <i>(' + t.key_concept_en + ')</i>' : ''));
          if (t.position_en) enp.push('<i>' + t.position_en + '</i>');
          h += '<tr class="en-line"><td colspan=4 style="font-size:0.7em;color:var(--text2);line-height:1.7">' + enp.join('<br>') + '</td></tr>';
        }
      });
      h += '</table></div>';
    } else if (sec.id === 'shizong') {
      // ── 十宗 ──
      h += '<div class=wu-door id=med-shizong onclick="this.classList.toggle(\'open\')"><span class=arrow>▶</span><span class=ttl>📋 ' + sec.title + '</span><div class=body>';
      if (sec.title_en) h += '<div class="en-line" style=font-size:0.72em;color:var(--text2);margin-bottom:4px>' + sec.title_en + '</div>';
      h += '<p style=font-size:.78em;color:var(--text2)>' + sec.description.replace(/\n/g,'<br>') + '</p>';
      if (sec.description_en) h += '<p class="en-line" style=font-size:.78em;color:var(--text2)>📖 ' + sec.description_en.replace(/\n/g,' ') + '</p>';
      h += '<table class=v-table style=font-size:.7em><tr><th>#</th><th>宗名</th><th>所属</th><th>核心教义</th></tr>';
      (sec.schools||[]).forEach(function(s) {
        h += '<tr><td>' + s.no + '</td><td><b>' + s.name + '</b></td><td>' + s.level + '</td><td>' + s.doctrine + '</td></tr>';
        if (s.name_en || s.doctrine_en) {
          var se = [];
          se.push('<b>' + (s.name_en||s.name) + '</b>');
          if (s.doctrine_en) se.push(s.doctrine_en);
          if (s.level_en) se.push('<i>' + s.level_en + '</i>');
          h += '<tr class="en-line"><td colspan=4 style="font-size:0.7em;color:var(--text2);line-height:1.7">' + se.join(' — ') + '</td></tr>';
        }
      });
      h += '</table></div></div>';
    } else if (sec.id === 'yicheng') {
      // ── 一乘不共别圆 ──
      h += '<div class=section id=med-yicheng><h2>📐 ' + sec.title + '</h2>';
      if (sec.title_en) h += '<div class="en-line" style=font-size:0.72em;color:var(--text2);margin-bottom:4px>' + sec.title_en + '</div>';
      h += '<p style=font-size:.8em;color:var(--text2)>' + sec.description.replace(/\n/g,'<br>') + '</p>';
      if (sec.description_en) h += '<p class="en-line" style=font-size:.8em;color:var(--text2)>📖 ' + sec.description_en.replace(/\n/g,' ') + '</p>';
      h += '<p style=font-size:.7em;color:var(--text2)>📎 ' + sec.classic_ref + '</p>';
      (sec.key_points||[]).forEach(function(kp) {
        h += '<div class=topic-card><h4>' + kp.title + '</h4>';
        if (kp.title_en) h += '<div class="en-line" style=font-size:0.7em;color:var(--gold);margin-bottom:2px>' + kp.title_en + '</div>';
        h += '<p>' + kp.body.replace(/\n/g,'<br>') + '</p>';
        if (kp.en_body) h += '<div class="en-line" style="font-size:0.75em;color:var(--text2);line-height:1.8;margin-top:3px">📖 ' + kp.en_body.replace(/\n/g,' ') + '</div>';
        h += '</div>';
      });
      h += '</div>';
    } else if (sec.id === 'futian') {
      // ── 与其他宗派比较 ──
      h += '<div class=wu-door id=med-futian onclick="this.classList.toggle(\'open\')"><span class=arrow>▶</span><span class=ttl>🔀 ' + sec.title + '</span><div class=body>';
      if (sec.title_en) h += '<div class="en-line" style=font-size:0.72em;color:var(--text2);margin-bottom:4px>' + sec.title_en + '</div>';
      h += '<p style=font-size:.78em;color:var(--text2)>' + sec.description.replace(/\n/g,'<br>') + '</p>';
      if (sec.description_en) h += '<p class="en-line" style=font-size:.78em;color:var(--text2)>📖 ' + sec.description_en.replace(/\n/g,' ') + '</p>';
      (sec.comparisons||[]).forEach(function(c) {
        h += '<div class=topic-card><h4>' + c.school + ' (' + c.founder + ')</h4>';
        if (c.school_en) h += '<div class="en-line" style=font-size:0.7em;color:var(--gold);margin-bottom:2px>' + c.school_en + ' — ' + (c.founder_en||'') + '</div>';
        h += '<p style=font-size:0.75em><b>判教体系:</b> ' + c.system + '</p>';
        if (c.system_en) h += '<p class="en-line" style=font-size:0.72em;color:var(--text2)><b>Classification:</b> ' + c.system_en + '</p>';
        h += '<p style=font-size:0.75em>' + c.relation_to_huayan.replace(/\n/g,'<br>') + '</p>';
        if (c.relation_to_huayan_en) h += '<div class="en-line" style="font-size:0.72em;color:var(--text2);line-height:1.8;margin-top:3px">📖 ' + c.relation_to_huayan_en.replace(/\n/g,' ') + '</div>';
        h += '</div>';
      });
      h += '</div></div>';
    }
  });
  // References
  if (pj.references) {
    h += '<div class=section style=margin-top:10px><p style=font-size:0.7em;color:var(--text2)>📚 参考文献: ';
    pj.references.forEach(function(r, i) { h += (i>0?' · ':'') + r; });
    h += '</p></div>';
  }
  return h;
}

// ═══ 心法·四禅八定·瑜伽行 原文辑录渲染 ═══
function renderXinfaSection() {
  var xf = (typeof PRACTICE_DATA !== 'undefined' && PRACTICE_DATA.haiyun_xinfa_primary) ? PRACTICE_DATA.haiyun_xinfa_primary : null;
  if (!xf || !xf.sections) return '';
  var h = '';
  xf.sections.forEach(function(sec) {
    h += '<div class=section id=med-' + sec.id + '>';
    h += '<h2>' + (sec.icon||'📌') + ' ' + sec.title + '</h2>';
    if (sec.intro) h += '<p style="font-size:0.8em;color:var(--text2);line-height:1.8;white-space:pre-line">' + _m2h(sec.intro) + '</p>';
    if (sec.quotes) {
      sec.quotes.forEach(function(q) {
        h += '<div class=stage-box style="margin:10px 0">';
        h += '<blockquote style="font-size:0.82em;line-height:1.9;margin:0;white-space:pre-line">' + _m2h(q.text) + '</blockquote>';
        h += '<p style="font-size:0.7em;color:var(--text2);margin-top:6px">📎 ' + q.source + '</p>';
        if (q.context) h += '<p style="font-size:0.68em;color:var(--gold)">' + q.context + '</p>';
        h += '</div>';
      });
    }
    h += '</div>';
  });
  // References
  if (xf.references) {
    h += '<details style="font-size:0.72em;margin-top:8px"><summary><b>📚 参考文献与搜索局限</b></summary>';
    xf.references.forEach(function(g) {
      h += '<p style=margin:4px 0><b>' + g.fmt + '</b></p><ul style=margin:0>';
      g.items.forEach(function(i) { h += '<li>' + i + '</li>'; });
      h += '</ul>';
    });
    h += '</details>';
  }
  return h;
}

// ═══ 杜顺五教止观渲染 (从 PRACTICE_DATA.dushun_wujiao_zhiguan) ═══
function renderDushunSection() {
  var dz = (typeof PRACTICE_DATA !== 'undefined' && PRACTICE_DATA.dushun_wujiao_zhiguan) ? PRACTICE_DATA.dushun_wujiao_zhiguan : null;
  if (!dz || !dz.gates) return '';
  var info = dz.text_info || {};
  var h = '<div class=section id=med-classical><h2>📜 ' + info.title + ' — ' + (info.author||'');
  if (info.title_en) h += '<span class="en-line" style="font-size:0.62em;display:block;color:var(--text2);margin-top:2px">' + info.title_en + '</span>';
  h += '</h2>';
  h += '<p style=font-size:.78em;color:var(--text2);margin-bottom:6px>'
    + (info.canon_ref||'') + ' · <a href="' + (info.cbeta_url||'#') + '" target=_blank>CBETA</a>'
    + ' · <a href="' + (info.wikisource_url||'#') + '" target=_blank>维基文库</a></p>';
  if (info.significance) h += '<p style="font-size:0.78em;color:var(--text2);line-height:1.8">📌 ' + info.significance.replace(/\n/g,'<br>') + '</p>';
  if (info.significance_en) h += '<p class="en-line" style="font-size:0.75em;color:var(--text2);line-height:1.8;margin-top:2px">📖 ' + info.significance_en.replace(/\n/g,' ') + '</p>';
  if (dz.overview) {
    h += '<div class=stage-box style=font-size:0.82em><b>' + (dz.overview.opening_line||'').replace(/\n/g,'<br>') + '</b></div>';
    if (dz.overview.opening_line_en) h += '<div class="en-line" style="font-size:0.78em;color:var(--text2);line-height:1.7;margin-top:4px">📖 ' + dz.overview.opening_line_en.replace(/\n/g,' ') + '</div>';
    if (dz.overview.structure_summary) h += '<p style="font-size:0.75em;color:var(--text2);margin-top:4px">' + dz.overview.structure_summary.replace(/\n/g,'<br>') + '</p>';
    if (dz.overview.structure_summary_en) h += '<p class="en-line" style="font-size:0.75em;color:var(--text2)">📖 ' + dz.overview.structure_summary_en.replace(/\n/g,' ') + '</p>';
  }
  // ── Five Gates ──
  (dz.gates||[]).forEach(function(g, gi) {
    h += '<div class=wu-door onclick="this.classList.toggle(\'open\')"><span class=arrow>▶</span>';
    h += '<span class=ttl>' + (gi+1) + '. ' + g.name + ' <span style=font-size:0.75em;color:var(--text2)>(' + g.panjiao + ')</span>';
    if (g.name_en) h += ' <span class="en-line" style=font-size:0.62em;color:var(--text2)>( ' + g.name_en + ' )</span>';
    h += '</span>';
    h += '<div class=body>';
    // Original text
    h += '<div class=stage-box><b>📜 原文 (T45n1867)</b><p style=font-size:0.78em;line-height:1.9;white-space:pre-line>'
      + (g.original_text||'') + '</p>';
    if (g.original_text_en) h += '<p class="en-line" style="font-size:0.78em;line-height:1.8;color:var(--text2);border-top:1px dashed var(--line);margin-top:6px;padding-top:6px;white-space:pre-line">📖 ' + g.original_text_en + '</p>';
    if (g.practice_en) h += '<p class="en-line" style="font-size:0.72em;color:var(--text2)">(' + g.practice_en + ')</p>';
    h += '</div>';
    // Practice
    if (g.practice) h += '<p style=font-size:0.75em;color:var(--gold)>⚡ 修行法要: ' + g.practice + '</p>';
    // Commentaries (collapsible)
    if (g.commentaries && g.commentaries.length) {
      h += '<details style=font-size:0.78em;margin:4px 0><summary><b>📝 各家注解 (' + g.commentaries.length + '家)</b></summary>';
      g.commentaries.forEach(function(c) {
        h += '<div class=topic-card><h4>' + c.source + '</h4><p>' + (c.text||'').replace(/\n/g,'<br>') + '</p>';
        if (c.text_en) h += '<div class="en-line" style="font-size:0.72em;color:var(--text2);line-height:1.8;margin-top:3px">📖 ' + c.text_en.replace(/\n/g,' ') + '</div>';
        h += '</div>';
      });
      h += '</details>';
    }
    // Critical notes (collapsible)
    if (g.critical_notes && g.critical_notes.length) {
      h += '<details style=font-size:0.78em;margin:4px 0><summary><b>🔍 学术评注 (' + g.critical_notes.length + '篇)</b></summary>';
      g.critical_notes.forEach(function(n) {
        h += '<div class=topic-card><h4>' + n.author + '</h4><p>' + (n.text||'').replace(/\n/g,'<br>') + '</p>';
        if (n.text_en) h += '<div class="en-line" style="font-size:0.72em;color:var(--text2);line-height:1.8;margin-top:3px">📖 ' + n.text_en.replace(/\n/g,' ') + '</div>';
        h += '</div>';
      });
      h += '</details>';
    }
    h += '</div></div>'; // close wu-door
  });
  // ── Lineage development table ──
  if (dz.lineage_development) {
    var ld = dz.lineage_development;
    h += '<details style=font-size:0.78em;margin-top:8px><summary><b>📅 ' + (ld.title||'') + '</b></summary>';
    if (ld.title_en) h += '<div class="en-line" style="font-size:0.72em;color:var(--text2);margin:2px 0">📖 ' + ld.title_en + '</div>';
    h += '<table class=v-table style=font-size:0.75em><tr><th>时代</th><th>人物</th><th>贡献</th><th>关键著作</th></tr>';
    (ld.stages||[]).forEach(function(s) {
      h += '<tr><td>' + s.period + '</td><td><b>' + s.figure + '</b></td><td>' + s.contribution + '</td><td>' + s.key_text + '</td></tr>';
      if (s.contribution_en) h += '<tr class="en-line"><td></td><td colspan=3 style="font-size:0.7em;color:var(--text2);line-height:1.7">📖 ' + s.contribution_en + (s.key_text_en?' — '+s.key_text_en:'') + '</td></tr>';
    });
    h += '</table></details>';
  }
  // References
  if (dz.references) {
    h += '<details style=font-size:0.7em;margin-top:4px><summary>📚 参考文献 (' + dz.references.length + '条)</summary>';
    dz.references.forEach(function(r) { h += '<p style=margin:1px 0>' + r + '</p>'; });
    h += '</details>';
  }
  h += '</div>';
  return h;
}

// ═══ 禅门实迹渲染 (从 PRACTICE_DATA.chan_authentic_traces) ═══
function renderChanTraces() {
  var ct = (typeof PRACTICE_DATA !== 'undefined' && PRACTICE_DATA.chan_authentic_traces) ? PRACTICE_DATA.chan_authentic_traces : null;
  if (!ct || !ct.sections) return '';
  // md helper: **bold** → <b>, *italic* → <i>
  function md(s) {
    return String(s||'')
      .replace(/\*\*(.+?)\*\*/g, '<b>$1</b>')
      .replace(/(^|[^*])\*([^*]+?)\*(?!\*)/g, '$1<i>$2</i>');
  }
  var h = '';
  ct.sections.forEach(function(sec) {
    h += '<div class=section id=chan-' + sec.id.replace('chan_','') + '>';
    h += '<h2>' + (sec.icon||'📌') + ' ' + sec.title;
    if (sec.title_en) h += '<span class="en-line" style="font-size:0.62em;display:block;color:var(--text2);margin-top:2px">' + sec.title_en + '</span>';
    h += '</h2>';
    if (sec.intro) h += '<p style="font-size:0.82em;color:var(--text2);line-height:1.8;white-space:pre-line">' + md(sec.intro) + '</p>';
    if (sec.intro_en) h += '<p class="en-line" style="white-space:pre-line;font-size:0.78em;color:var(--text2);line-height:1.8"><span style="color:var(--gold);font-weight:600">📖 </span>' + sec.intro_en + '</p>';
    if (sec.topics) {
      sec.topics.forEach(function(t, idx) {
        // Collapsible topic
        h += '<div class="wu-door" id=ct-' + sec.id + '-' + idx + ' onclick="this.classList.toggle(\'open\')">';
        h += '<span class=arrow>▶</span><span class=ttl>' + t.title + '</span>';
        if (t.title_en) h += '<div class="en-line" style="font-size:0.62em;color:var(--text2);margin-left:18px;margin-bottom:4px">' + t.title_en + '</div>';
        h += '<div class=body>';
        h += '<p style=font-size:0.8em;line-height:1.8;white-space:pre-line>' + md(t.body) + '</p>';
        if (t.en_body) h += '<div class="en-line" style="white-space:pre-line;font-size:0.82em;color:var(--text2);border-top:1px dashed var(--line);margin-top:6px;padding-top:6px"><span style="color:var(--gold);font-weight:600">📖 </span>' + md(t.en_body) + '</div>';
        if (t.links) {
          Object.keys(t.links).forEach(function(k) {
            h += '<a href="' + t.links[k] + '" target=_blank style="font-size:0.72em;color:var(--blue)">🔗 ' + k + '</a> ';
          });
        }
        if (t.source) h += '<p style=font-size:0.68em;color:var(--text2);margin-top:4px">📎 ' + md(t.source) + '</p>';
        h += '</div></div>';
      });
    }
    h += '</div>';
  });
  // References
  if (ct.references) {
    h += '<details style=font-size:0.72em;margin-top:8px><summary>📚 参考文献 (学术·门内·近现代·海云)</summary>';
    Object.keys(ct.references).forEach(function(k) {
      h += '<p style=margin:4px 0><b>' + k + '</b></p><ul style=margin:0>';
      ct.references[k].forEach(function(r) { h += '<li>' + r + '</li>'; });
      h += '</ul>';
    });
    h += '</details>';
  }
  // ── 法脉传承表 ──
  h += '<div class=section id=chan-diagrams><h2>📊 禅宗法脉传承</h2>';
  h += '<table class=v-table style=font-size:0.75em><tr><th>时期</th><th>人物</th><th>贡献</th></tr>';
  h += '<tr><td>印度</td><td>佛陀二十八代→菩提达摩</td><td>灵山拈花·教外别传</td></tr>';
  h += '<tr><td>隋</td><td>慧可→僧璨→道信→弘忍</td><td>二祖至五祖·东山法门</td></tr>';
  h += '<tr><td>唐</td><td>神秀(北宗) 慧能(南宗)</td><td>南北分宗</td></tr>';
  h += '<tr><td>晚唐五代</td><td>马祖·石头→临济·曹洞·沩仰·云门·法眼</td><td>五家七宗</td></tr>';
  h += '<tr><td>宋</td><td>大慧宗杲(看话) 宏智正觉(默照)</td><td>两大法门</td></tr>';
  h += '<tr><td>明清</td><td>永明延寿→云栖袾宏→蕅益智旭</td><td>禅净合流</td></tr>';
  h += '<tr><td>近现代</td><td>虚云(兼祧五宗) 来果 铃木大拙</td><td>传统坚守·西传</td></tr>';
  h += '<tr><td>当代</td><td>净慧(生活禅) 圣严 一行禅师</td><td>现代体系化</td></tr>';
  h += '</table></div>';
  return h;
}

// ═══ 成其大观渲染 (从 PRACTICE_DATA.chengguan_master) ═══
function renderChengguanSection() {
  var cg = (typeof PRACTICE_DATA !== 'undefined' && PRACTICE_DATA.chengguan_master) ? PRACTICE_DATA.chengguan_master : null;
  if (!cg) return '';
  var h = '';
  // Bio
  if (cg.biography) {
    var b = cg.biography;
    h += '<div class=section id=cg-bio><h2>🌄 成其大观 — 成观法师</h2>';
    h += '<p style=font-size:0.8em;color:var(--text2)>' + b.name_en + ' · ' + b.birth + '- · ' + (b.birthplace||'') + '</p>';
    if (b.birthplace_en) h += '<p class="en-line" style=font-size:0.75em;color:var(--text2)><b>Born:</b> ' + b.birthplace_en + ', ' + b.birth + '</p>';
    h += '<div class=stage-box style=font-size:0.78em>';
    (b.education||[]).forEach(function(e) { h += '🎓 ' + e + '<br>'; });
    h += '✂️ ' + b.ordination + '<br>';
    (b.lineage||[]).forEach(function(l) { h += '📜 ' + l + '<br>'; });
    h += '🏛 ' + b.current_position;
    h += '</div>';
    if (b.education_en || b.ordination_en || b.lineage_en || b.current_position_en) {
      h += '<div class="en-line stage-box" style="font-size:0.72em;color:var(--text2);line-height:1.9;margin-top:4px">';
      (b.education_en||[]).forEach(function(e){ h += '🎓 ' + e + '<br>'; });
      if (b.ordination_en) h += '✂️ ' + b.ordination_en + '<br>';
      (b.lineage_en||[]).forEach(function(l){ h += '📜 ' + l + '<br>'; });
      if (b.current_position_en) h += '🏛 ' + b.current_position_en;
      h += '</div>';
    }
    h += '</div>'; // close cg-bio
  }
  // Institutions
  if (cg.institutions) {
    h += '<div class=section id=cg-institutions><h3>🏛 译经院</h3>';
    cg.institutions.forEach(function(i) {
      h += '<div class=topic-card style=font-size:0.78em>';
      h += '<b>' + i.name + '</b> (' + i.founded + ') — ' + i.location + '<br>';
      h += i.practice + '<br><span style=color:var(--text2)>' + i.note + '</span>';
      if (i.name_en || i.practice_en || i.note_en) {
        h += '<div class="en-line" style="font-size:0.92em;color:var(--text2);line-height:1.8;margin-top:4px;border-top:1px dashed var(--line);padding-top:4px">';
        if (i.name_en) h += '<b>' + i.name_en + '</b><br>';
        if (i.practice_en) h += i.practice_en + '<br>';
        if (i.note_en) h += i.note_en;
        h += '</div>';
      }
      h += '<br><a href="' + i.website + '" target=_blank>官网</a>';
      h += '</div>';
    });
    h += '</div>';
  }
  // Works
  if (cg.works_chinese || cg.works_english) {
    h += '<div class=section id=cg-works><h3>📚 著作全目</h3>';
    if (cg.works_chinese) {
      h += '<p style=font-size:0.78em><b>中文著述 (' + cg.works_chinese.intro + ')</b></p>';
      if (cg.works_chinese.intro_en) h += '<p class="en-line" style=font-size:0.72em;color:var(--text2)><b>In Chinese:</b> ' + cg.works_chinese.intro_en + '</p>';
      h += '<table class=v-table style=font-size:0.72em><tr><th>书名</th><th>备注</th></tr>';
      cg.works_chinese.items.forEach(function(w) {
        h += '<tr><td>' + w.title + '</td><td style=color:var(--text2)>' + (w.note||'') + '</td></tr>';
        if (w.note_en) h += '<tr class="en-line"><td colspan=2 style="font-size:0.92em;color:var(--text2)">📖 ' + w.note_en + '</td></tr>';
      });
      h += '</table>';
    }
    if (cg.works_english) {
      h += '<p style=font-size:0.78em;margin-top:8px><b>英文译著 (' + cg.works_english.intro + ')</b></p>';
      if (cg.works_english.intro_en) h += '<p class="en-line" style=font-size:0.72em;color:var(--text2)><b>In English:</b> ' + cg.works_english.intro_en + '</p>';
      h += '<ul style=font-size:0.75em>';
      cg.works_english.items.forEach(function(w) { h += '<li>' + w + '</li>'; });
      h += '</ul>';
    }
    h += '</div>';
  }
  // Lectures
  if (cg.lecture_highlights) {
    h += '<div class=section id=cg-lectures><h3>🎙 讲法特色 (' + cg.lecture_highlights.length + '系列)</h3>';
    cg.lecture_highlights.forEach(function(l) {
      h += '<div class=topic-card><h4>' + l.topic + '</h4>';
      if (l.topic_en) h += '<div class="en-line sp-en-title" style=font-size:0.7em;color:var(--gold);margin-bottom:2px>' + l.topic_en + '</div>';
      h += '<p style=font-size:0.78em>' + _m2h(l.note||l.significance||'') + '</p>';
      if (l.significance_en) h += '<div class="en-line" style="font-size:0.74em;color:var(--text2);line-height:1.8;margin-top:3px">📖 ' + l.significance_en + '</div>';
      if (l.links && l.links.length) {
        l.links.forEach(function(lk) {
          h += '<a href="' + lk.url + '" target=_blank style="font-size:0.72em;color:var(--blue);margin-right:8px">🔗 ' + lk.name + '</a>';
        });
      }
      h += '</div>';
    });
    h += '</div>';
  }
  // Comparison
  if (cg.comparison_with_haiyun) {
    h += '<div class=stage-box style=font-size:0.75em;margin-top:10px"><b>🔀 与海云继梦法师的比较</b><br>' + cg.comparison_with_haiyun.note +
      (cg.comparison_with_haiyun.note_en ? '<div class="en-line" style=font-size:0.92em;color:var(--text2);margin-top:4px>📖 ' + cg.comparison_with_haiyun.note_en + '</div>' : '') +
      '</div>';
  }
	// ── 海云vs成观 多维对照表 (优化版) ──
	var cmp = (typeof PRACTICE_DATA !== 'undefined' && PRACTICE_DATA.haiyun_chengguan_compare) ? PRACTICE_DATA.haiyun_chengguan_compare : null;
	if (cmp && cmp.compare) {
	  h += '<style>' +
	    '.cmp-card{border:1px solid var(--line);border-radius:12px;margin:10px 0;overflow:hidden;background:var(--card)}' +
	    '.cmp-head{padding:8px 14px;background:linear-gradient(180deg,#f5efe4,#efe6d8);font-weight:700;color:var(--gold);font-size:0.85em}' +
	    '.cmp-grid{display:grid;grid-template-columns:1fr 1fr;gap:0}' +
	    '.cmp-col{padding:12px 14px;font-size:0.75em;line-height:1.75}' +
	    '.cmp-col:first-child{border-right:1px solid var(--line);background:rgba(184,134,60,0.03)}' +
	    '.cmp-col:last-child{background:rgba(196,107,93,0.03)}' +
	    '.cmp-name{font-weight:700;font-size:1.05em;margin-bottom:4px}' +
	    '.cmp-pos{color:var(--gold);font-weight:600;margin-bottom:6px}' +
	    '.cmp-quote{display:block;margin:6px 0;padding:6px 10px;border-left:3px solid var(--gold);background:rgba(184,134,60,0.05);color:var(--text);font-size:0.92em;border-radius:0 6px 6px 0}' +
	    '.cmp-col:last-child .cmp-pos{color:#c46b5d}' +
	    '.cmp-col:last-child .cmp-quote{border-left-color:#c46b5d;background:rgba(196,107,93,0.05)}' +
	    '.cmp-note{color:var(--text2);font-size:0.92em}' +
	    '.cmp-contrast{padding:8px 14px;border-top:1px dashed var(--line);background:rgba(125,154,110,0.05);font-size:0.75em;color:var(--text)}' +
	    '.cmp-contrast b{color:#7d9a6e}' +
	    '@media(max-width:600px){.cmp-grid{grid-template-columns:1fr}.cmp-col:first-child{border-right:none;border-bottom:1px solid var(--line)}}' +
	    '</style>';
	  h += '<div class=section id=cg-compare><h2>🔀 海云继梦 vs 成观法师 — 多维对照</h2>';
	  if (cmp.meta && cmp.meta.note) h += '<p style=font-size:0.75em;color:var(--text2);margin-bottom:12px">' + _m2h(cmp.meta.note) + '</p>';
	  if (cmp.meta && cmp.meta.note_en) h += '<p class="en-line" style=font-size:0.75em;color:var(--text2);margin-bottom:12px">📖 ' + cmp.meta.note_en + '</p>';
	  cmp.compare.forEach(function(row) {
	    h += '<div class=cmp-card>';
	    h += '<div class=cmp-head>' + (row.icon||'') + ' ' + row.topic + (row.topic_en ? '<span class="en-line" style=font-size:0.72em;display:block;color:var(--text2);font-weight:500> ' + row.topic_en + '</span>' : '') + '</div>';
	    h += '<div class=cmp-grid>';
	    // 海云
	    h += '<div class=cmp-col>';
	    h += '<div class=cmp-name style=color:var(--gold)>🌊 海云继梦</div>';
	    h += '<div class=cmp-pos>' + _m2h(row.haiyun.position) + '</div>';
	    if (row.haiyun.position_en) h += '<div class="en-line cmp-pos" style=color:var(--text2);font-size:0.82em>' + row.haiyun.position_en + '</div>';
	    if (row.haiyun.quote) h += '<span class=cmp-quote>' + _m2h(row.haiyun.quote) + '</span>';
	    if (row.haiyun.note) h += '<div class=cmp-note>' + _m2h(row.haiyun.note) + '</div>';
	    if (row.haiyun.note_en) h += '<div class="en-line" style="font-size:0.92em;color:var(--text2);line-height:1.75;margin-top:4px">📖 ' + _m2h(row.haiyun.note_en) + '</div>';
	    h += '</div>';
	    // 成观
	    h += '<div class=cmp-col>';
	    h += '<div class=cmp-name style=color:#c46b5d>🌄 成观法师</div>';
	    h += '<div class=cmp-pos>' + _m2h(row.chengguan.position) + '</div>';
	    if (row.chengguan.position_en) h += '<div class="en-line cmp-pos" style=color:var(--text2);font-size:0.82em>' + row.chengguan.position_en + '</div>';
	    if (row.chengguan.quote) h += '<span class=cmp-quote>' + _m2h(row.chengguan.quote) + '</span>';
	    if (row.chengguan.note) h += '<div class=cmp-note>' + _m2h(row.chengguan.note) + '</div>';
	    if (row.chengguan.note_en) h += '<div class="en-line" style="font-size:0.92em;color:var(--text2);line-height:1.75;margin-top:4px">📖 ' + _m2h(row.chengguan.note_en) + '</div>';
	    h += '</div>';
	    h += '</div>';
	    if (row.contrast) h += '<div class=cmp-contrast><b>📝 对比:</b> ' + _m2h(row.contrast) +
	      (row.contrast_en ? '<br><span class="en-line" style=color:var(--text2)!important>📖 ' + _m2h(row.contrast_en) + '</span>' : '') + '</div>';
	    h += '</div>';
	  });
	  h += '</div>';
	}
  // Links
  if (cg.links) {
    h += '<p style=font-size:0.72em;margin-top:6px">🔗 ';
    cg.links.forEach(function(l) { h += '<a href="' + l.url + '" target=_blank>' + l.name + '</a> · '; });
    h += '</p>';
  }
  return h;
}

// ═══ 梦参老和尚讲法全目 (从 PRACTICE_DATA.mengcan_lectures) ═══
function renderMengcanSection() {
  var mc = (typeof PRACTICE_DATA !== 'undefined' && PRACTICE_DATA.mengcan_lectures) ? PRACTICE_DATA.mengcan_lectures : null;
  if (!mc) return '';
  var h = '<div class=section id=res-mengcan><h2>👴 梦参老和尚 (1915-2017) — 一生讲法全目</h2>';
  if (mc.biography) {
    var b = mc.biography;
    h += '<p style="font-size:0.78em;color:var(--text2);line-height:1.8">'
      + b.name_en + ' · 俗名' + b.secular_name + ' · 世寿' + b.birth + '-' + b.death
      + ' · ' + b.lineage + '</p>';
    h += '<div class=stage-box style=font-size:0.75em>' + (b.key_locations||[]).join('<br>') + '</div>';
    if (b.key_locations_en) h += '<div class="en-line" style="font-size:0.7em;color:var(--text2);line-height:1.8;margin-top:2px">' + b.key_locations_en.join('<br>') + '</div>';
    if (b.relation_to_huayan) h += '<p style="font-size:0.75em;color:var(--gold);margin-top:4px">🪷 ' + b.relation_to_huayan + '</p>';
    if (b.relation_to_huayan_en) h += '<p class="en-line" style="font-size:0.75em;color:var(--text2);margin-top:2px;line-height:1.8">📖 ' + b.relation_to_huayan_en + '</p>';
  }
  // Lectures table
  if (mc.lectures) {
    h += '<table class=v-table style=font-size:0.75em;margin-top:8px><tr><th>经典</th><th>讲题</th><th>地点/年份</th><th>体量</th></tr>';
    mc.lectures.forEach(function(l) {
      h += '<tr><td><b>' + l.sutra + '</b></td><td>' + l.title + '</td>';
      h += '<td>' + (l.venue||'') + (l.year?' · '+l.year:'') + '</td>';
      h += '<td>' + (l.length||'') + '</td></tr>';
      if (l.sutra_en || l.title_en) {
        h += '<tr class="en-line"><td colspan=4 style="font-size:0.72em;color:var(--text2);line-height:1.7">📖 ' + (l.sutra_en||'') + (l.sutra_en&&l.title_en?' — ':'') + (l.title_en||'') + '</td></tr>';
      }
      if (l.significance || l.note) {
        h += '<tr><td></td><td colspan=3 style="font-size:0.85em;color:var(--text2)">' + (l.significance||'') + (l.note?'<br>'+l.note:'') + '</td></tr>';
        if (l.significance_en || l.note_en) {
          h += '<tr class="en-line"><td></td><td colspan=3 style="font-size:0.78em;color:var(--text2);line-height:1.7">📖 ' + (l.significance_en||'') + (l.note_en?'<br>'+l.note_en.replace(/\n/g,'<br>'):'') + '</td></tr>';
        }
      }
    });
    h += '</table>';
  }
  // Resources
  if (mc.other_resources) {
    h += '<p style="font-size:0.72em;margin-top:6px">📡 ';
    mc.other_resources.forEach(function(r) {
      h += '<a href="' + r.link + '" target=_blank style="color:var(--blue)">' + r.name + '</a> (' + r.platform + ') · ';
    });
    h += '</p>';
  }
  if (mc.life_motto) h += '<blockquote style="font-size:0.75em;border-left:3px solid var(--gold);padding-left:10px;margin-top:6px;line-height:1.8">' + mc.life_motto.replace(/\n/g,'<br>') + '</blockquote>';
  if (mc.life_motto_en) h += '<blockquote class="en-line" style="font-size:0.72em;border-left:3px solid var(--line);padding-left:10px;margin-top:2px;line-height:1.8;color:var(--text2)">' + mc.life_motto_en.replace(/\n/g,'<br>') + '</blockquote>';
  if (mc.relation_to_project) h += '<p style="font-size:0.72em;color:var(--text2);margin-top:4px;line-height:1.8">🪷 ' + mc.relation_to_project.replace(/\n/g,'<br>') + '</p>';
  if (mc.relation_to_project_en) h += '<p class="en-line" style="font-size:0.72em;color:var(--text2);line-height:1.8;margin-top:2px">📖 ' + mc.relation_to_project_en.replace(/\n/g,' ') + '</p>';
  h += '</div>';
  return h;
}

// ═══ 全平台修行资源渲染 (从 PRACTICE_DATA.haiyun_practice_sources) ═══
function renderPracticeSources() {
  var ps = (typeof PRACTICE_DATA !== 'undefined' && PRACTICE_DATA.haiyun_practice_sources) ? PRACTICE_DATA.haiyun_practice_sources : null;
  if (!ps) return '';
  var h = '';

  // ── 三阶段快速参考 ──
  if (ps.three_stages_quick_ref) {
    var ts = ps.three_stages_quick_ref;
    h += '<div class=section id=res-stages><h2>📐 三阶段修行速查 <span style=font-size:0.7em;color:var(--text2)>技术面·工程面·出处</span></h2>';
    h += '<table class=v-table style=font-size:0.72em><tr><th>阶段</th><th>技术面</th><th>工程面</th><th>玄门</th><th>来源</th></tr>';
    ['stage1','stage2','stage3'].forEach(function(sk) {
      var s = ts[sk]; if (!s) return;
      h += '<tr><td><b>' + s.name + (s.name_en?' <span class="en-line" style=color:var(--text2);font-size:0.9em>(' + s.name_en + ')</span>':'') + '</b></td><td>' + s.technical + '</td><td>' + s.engineering + '</td><td style=font-size:0.85em>' + s.xuanmen + '</td><td style=font-size:0.75em>' + s.source + '</td></tr>';
      if (s.technical_en || s.engineering_en) {
        h += '<tr class="en-line"><td></td><td colspan=4 style="font-size:0.7em;color:var(--text2);line-height:1.7">📖 technical: ' + (s.technical_en||'') + ' · engineering: ' + (s.engineering_en||'') + '</td></tr>';
      }
    });
    h += '</table></div>';
  }

  // ── 著作 ──
  if (ps.books) {
    h += '<div class=section id=res-sources-books><h2>📚 关键著作 (' + ps.books.length + '本)</h2>';
    ps.books.forEach(function(b) {
      h += '<div class=topic-card style=font-size:0.78em>';
      h += '<b>' + b.title + '</b>' + (b.title_en?' <span class="en-line" style=color:var(--text2)>(' + b.title_en + ')</span>':'') + ' (' + b.year + ') — ' + b.publisher;
      if (b.isbn) h += ' · ISBN ' + b.isbn;
      h += '<br><span style=color:var(--text2)>' + b.content + '</span>';
      if (b.content_en) h += '<div class="en-line" style="color:var(--text2);font-size:0.95em;line-height:1.7;margin-top:3px">📖 ' + b.content_en + '</div>';
      h += '<br>';
      if (b.link_google_play) h += '<a href="' + b.link_google_play + '" target=_blank>Google Play</a> · ';
      if (b.link_buy) h += '<a href="' + b.link_buy + '" target=_blank>购买</a> · ';
      if (b.link_fjdh) h += '<a href="' + b.link_fjdh + '" target=_blank>逐字稿</a>';
      if (b.lectures) h += ' <span style=color:var(--text2)>(' + b.lectures + ')</span>';
      h += '</div>';
    });
    h += '</div>';
  }

  // ── 讲记系列 ──
  if (ps.lecture_series) {
    h += '<div class=section id=res-sources-lectures><h2>🎙 讲记系列 (' + ps.lecture_series.length + '部)</h2>';
    ps.lecture_series.forEach(function(l) {
      h += '<div class=topic-card style=font-size:0.78em>';
      h += '<b>' + l.title + '</b>' + (l.title_en?' <span class="en-line" style=color:var(--text2)>(' + l.title_en + ')</span>':'') + ' — ' + l.episodes + ' · ' + (l.year||'') + ' · ' + l.platform;
      h += '<br><span style=color:var(--text2)>' + l.content + '</span><br>';
      if (l.content_en) h += '<div class="en-line" style="color:var(--text2);font-size:0.95em;line-height:1.7;margin-top:3px">📖 ' + l.content_en + '</div><br>';
      if (l.link_example_fjdh) h += '<a href="' + l.link_example_fjdh + '" target=_blank>📝 讲记</a> · ';
      if (l.spotify) h += '<a href="' + l.spotify + '" target=_blank>🎧 Spotify</a> · ';
      if (l.apple_podcast) h += '<a href="' + l.apple_podcast + '" target=_blank>🎙 Apple</a> · ';
      if (l.listennotes) h += '<a href="' + l.listennotes + '" target=_blank>📋 目录</a>';
      h += '</div>';
    });
    h += '</div>';
  }

  // ── 禅三/禅七 ──
  if (ps.exhaustive_platform_index && ps.exhaustive_platform_index.retreats) {
    var rt = ps.exhaustive_platform_index.retreats;
    h += '<div class=section id=res-sources-retreats><h2>🧘 禅修营·禅七 (' + (rt.confirmed||[]).length + '梯次确认)</h2>';
    h += '<p style=font-size:0.75em;color:var(--text2)><b>⚠ 检索局限:</b> 编号梯次(第X梯)禅三录音搜索引擎索引不完整，需联系大华严寺或逐季检查播客。</p>';
    (rt.confirmed||[]).forEach(function(r) {
      h += '<div class=topic-card style=font-size:0.78em>';
      h += '<b>' + r.type + '</b>' + (r.type_en?' <span class="en-line" style=color:var(--text2)>(' + r.type_en + ')</span>':'') + ' — ' + r.year + ' · ' + (r.venue||'');
      h += '<br><span style=color:var(--text2)>' + r.content + '</span>';
      if (r.content_en) h += '<div class="en-line" style="color:var(--text2);font-size:0.95em;line-height:1.7;margin-top:3px">📖 ' + r.content_en + '</div>';
      if (r.known_batches) {
        h += '<br>📅 已知梯次: ' + r.known_batches.join('; ');
      }
      if (r.link_book) h += '<br><a href="' + r.link_book + '" target=_blank>📖 出版书籍</a>';
      if (r.link_podwise) h += ' · <a href="' + r.link_podwise + '" target=_blank>🎧 播客</a>';
      h += '</div>';
    });
    if (rt.search_advice) {
      h += '<details style=font-size:0.72em;margin-top:4px><summary>🔍 穷尽搜索建议</summary><p style=color:var(--text2);white-space:pre-line>' + rt.search_advice + '</p></details>';
    }
    h += '</div>';
  }

  // ── 全平台索引摘要 ──
  if (ps.exhaustive_platform_index) {
    var ep = ps.exhaustive_platform_index;
    h += '<div class=section id=res-sources-platforms><h2>🌐 全平台资源索引</h2>';
    // Bilibili
    if (ep.bilibili) {
      var bl = ep.bilibili;
      h += '<details style=font-size:0.75em;margin:4px 0><summary><b>📺 Bilibili — ' + (bl.key_series||[]).length + '个系列 · ' + (bl.uploaders||[]).length + '个UP主</b></summary>';
      (bl.key_series||[]).forEach(function(s) {
        h += '<div style=margin:2px 0>🔹 <b>' + s.name + '</b> (' + (s.episodes||s.duration||'') + ') ' + (s.year||'');
        if (s.url) h += ' <a href="' + s.url + '" target=_blank>直达</a>';
        if (s.note) h += '<br><span style=color:var(--text2);font-size:0.9em>' + s.note + '</span>';
        if (s.note_en) h += '<div class="en-line" style="color:var(--text2);font-size:0.9em;line-height:1.7">📖 ' + s.note_en + '</div>';
        h += '</div>';
      });
      h += '</details>';
    }
    // Podcast
    if (ep.podcast) {
      var pd = ep.podcast;
      h += '<details style=font-size:0.75em;margin:4px 0><summary><b>🎧 Spotify/Apple — ' + pd.show_name + ' (' + (pd.series_count||'') + ')</b></summary>';
      h += '<p>' + (pd.update_freq||'') + ' · <a href="' + pd.spotify_url + '" target=_blank>Spotify</a> · <a href="' + pd.apple_url + '" target=_blank>Apple</a></p>';
      (pd.key_series||[]).forEach(function(s) {
        h += '<div>🔹 <b>' + s.name + '</b>: ' + (s.content||'') + (s.episodes?' ('+s.episodes+')':'');
        if (s.content_en) h += ' <span class="en-line" style=color:var(--text2)>' + s.content_en + '</span>';
        h += '</div>';
      });
      h += '</details>';
    }
    // Text transcripts
    if (ep.text_transcripts) {
      var tt = ep.text_transcripts;
      h += '<details style=font-size:0.75em;margin:4px 0><summary><b>📝 文字讲记 — ' + tt.platform + '</b></summary>';
      (tt.key_series||[]).forEach(function(s) {
        h += '<div>🔹 <b>' + s.name + '</b>: ' + s.episodes + (s.url_example?' · <a href="'+s.url_example+'" target=_blank>示例</a>':'') + '</div>';
      });
      h += '</details>';
    }
    // YouTube
    if (ep.youtube) {
      var yt = ep.youtube;
      h += '<details style=font-size:0.75em;margin:4px 0><summary><b>📺 YouTube — ' + yt.channel + '</b></summary>';
      h += '<p><a href="' + yt.channel_url + '" target=_blank>频道</a> · <a href="' + yt.playlists_url + '" target=_blank>播放清单</a></p>';
      (yt.key_series||[]).forEach(function(s) {
        h += '<div>🔹 <b>' + s.name + '</b> (' + (s.type||'') + '): ' + (s.content||'');
        if (s.content_en) h += ' <span class="en-line" style=color:var(--text2)>' + s.content_en + '</span>';
        h += '</div>';
      });
    h += '</details>';
  }
  h += '</div>';  // close res-sources-platforms
  }
  return h;
  }

// ═══ 天台觉景渲染 (从 PRACTICE_DATA.tiantai_juejing) ═══
function renderTiantaiSection() {
  var tt = (typeof PRACTICE_DATA !== 'undefined' && PRACTICE_DATA.tiantai_juejing) ? PRACTICE_DATA.tiantai_juejing : null;
  if (!tt || !tt.sections) return '';
  function md(s) {
    return String(s||'')
      .replace(/\*\*(.+?)\*\*/g, '<b>$1</b>')
      .replace(/(^|[^*])\*([^*]+?)\*(?!\*)/g, '$1<i>$2</i>');
  }
  var h = '';
  tt.sections.forEach(function(sec) {
    h += '<div class=section id=tt-' + sec.id.replace('tt_','') + '>';
    h += '<h2>' + (sec.icon||'📌') + ' ' + sec.title;
    if (sec.title_en) h += '<span class="en-line" style="font-size:0.62em;display:block;color:var(--text2);margin-top:2px">' + sec.title_en + '</span>';
    h += '</h2>';
    if (sec.intro) h += '<p style="font-size:0.82em;color:var(--text2);line-height:1.8;white-space:pre-line">' + md(sec.intro) + '</p>';
    if (sec.intro_en) h += '<p class="en-line" style="white-space:pre-line;font-size:0.78em;color:var(--text2);line-height:1.8"><span style="color:var(--gold);font-weight:600">📖 </span>' + sec.intro_en + '</p>';
    if (sec.topics) {
      sec.topics.forEach(function(t, idx) {
        h += '<div class=wu-door id=tt-topic-' + sec.id + '-' + idx + ' onclick="this.classList.toggle(\'open\')">';
        h += '<span class=arrow>▶</span><span class=ttl>' + t.title + '</span>';
        if (t.title_en) h += '<div class="en-line" style="font-size:0.62em;color:var(--text2);margin-left:18px;margin-bottom:4px">' + t.title_en + '</div>';
        h += '<div class=body>';
        h += '<p style=font-size:0.8em;line-height:1.8;white-space:pre-line>' + md(t.body) + '</p>';
        if (t.en_body) h += '<div class="en-line" style="white-space:pre-line;font-size:0.82em;color:var(--text2);border-top:1px dashed var(--line);margin-top:6px;padding-top:6px"><span style="color:var(--gold);font-weight:600">📖 </span>' + md(t.en_body) + '</div>';
        if (t.links) {
          Object.keys(t.links).forEach(function(k) {
            h += '<a href="' + t.links[k] + '" target=_blank style="font-size:0.72em;color:var(--blue)">🔗 ' + k + '</a> ';
          });
        }
        if (t.source) h += '<p style=font-size:0.68em;color:var(--text2);margin-top:4px">📎 ' + md(t.source) + '</p>';
        h += '</div></div>';
      });
    }
    h += '</div>';
  });
  // References
  if (tt.references) {
    h += '<details style=font-size:0.72em;margin-top:8px><summary>📚 参考文献 (原典·学术·修行·近现代)</summary>';
    Object.keys(tt.references).forEach(function(k) {
      h += '<p style=margin:4px 0><b>' + k + '</b></p><ul style=margin:0>';
      tt.references[k].forEach(function(r) { h += '<li>' + r + '</li>'; });
      h += '</ul>';
    });
    h += '</details>';
  }
  return h;
}

// ═══ 修行体系渲染 (从 PRACTICE_DATA.cultivation_system) ═══
var _csColors={gold:{bd:'#b8863c',bg:'rgba(184,134,60,0.08)',t:'#8a7060',d:'#a09080'},blue:{bd:'#5e8b9e',bg:'rgba(94,139,158,0.08)',t:'#6a7060',d:'#a09080'},red:{bd:'#c46b5d',bg:'rgba(196,107,93,0.08)',t:'#8a6060',d:'#a09080'}};
function renderCultivationSystem() {
  var cs = (typeof PRACTICE_DATA !== 'undefined' && PRACTICE_DATA.cultivation_system) ? PRACTICE_DATA.cultivation_system : null;
  if (!cs) return '';
  var h = '';
  var hd = cs.header || {};
  h += '<div class=section style=border-left:4px solid var(--gold)><h2>🧘 ' + hd.title + '</h2>';
  if (hd.title_en) h += '<span class="en-line" style="font-size:0.62em;display:block;color:var(--text2);margin-top:2px">' + hd.title_en + '</span>';
  h += '<p style=line-height:1.8>' + (hd.description||'').replace(/\n/g,'<br>') + '</p>';
  if (hd.description_en) h += '<p class="en-line" style="font-size:0.78em;color:var(--text2);line-height:1.8">📖 ' + hd.description_en + '</p></div>';

  // ── 三阶段卡片 ──
  var stages = cs.three_stages || [];
  if (stages.length) {
    h += "<div style='display:flex;gap:16px;flex-wrap:wrap;justify-content:center;margin:12px 0'>";
    stages.forEach(function(s, i) {
      if (i>0) h += "<div style='display:flex;align-items:center;color:#c0b098;font-size:1.2em'>→</div>";
      var c = _csColors[s.color] || _csColors.gold;
      h += "<div style='flex:1;min-width:180px;background:" + c.bg + ";border:1px solid " + c.bd + ";border-radius:10px;padding:16px;text-align:center'>";
      h += "<div style='font-size:1.05em;font-weight:700;color:" + c.bd + ";margin-bottom:4px'>" + s.name + "</div>";
      if (s.name_en) h += '<div class="en-line" style="font-size:0.6em;color:var(--text2)">' + s.name_en + '</div>';
      h += "<div style='font-size:0.8em;color:" + c.t + "'>" + s.subtitle + "</div>";
      if (s.subtitle_en) h += '<div class="en-line" style="font-size:0.62em;color:var(--text2)">' + s.subtitle_en + '</div>';
      h += "<div style='font-size:0.7em;color:" + c.d + ";margin-top:4px'>" + s.detail + "</div>";
      if (s.detail_en) h += '<div class="en-line" style="font-size:0.62em;color:var(--text2)">' + s.detail_en + '</div>';
      h += "</div>";
    });
    h += "</div>";

    // ── 修行三阶段 stage-box ──
    h += '<div class=section id=sys-stages><h2>📐 修行三阶段（据大华严寺官网「修行蓝图」2025.11）</h2>';
    if (cs.three_stages_title_en) h += '<div class="en-line" style=font-size:0.7em;color:var(--text2)>📖 ' + cs.three_stages_title_en + '</div>';
    stages.forEach(function(s, i) {
      h += '<div class=stage-box><b>' + (i+1) + '、' + s.name + ' — ' + s.subtitle + '</b><br>' + (s.description||'').replace(/\n/g,'<br>');
      if (s.description_en) h += '<div class="en-line" style="font-size:0.78em;color:var(--text2);line-height:1.7;border-top:1px dashed var(--line);margin-top:4px;padding-top:4px">📖 ' + s.description_en.replace(/\n/g,' ') + '</div>';
      h += '</div>';
    });
    h += '</div>';
  }

  // ── 四阶段修行蓝图 ──
  var fp = cs.four_stages_blueprint;
  if (fp && fp.stages) {
    h += '<div class=section id=sys-blueprint><h2>🪜 四阶段修行蓝图（海云法师判摄）</h2>';
    if (fp.description_en) h += '<div class="en-line" style="font-size:0.7em;color:var(--text2);margin-bottom:4px">📖 ' + fp.description_en + '</div>';
    if (fp.description) h += '<p style=font-size:0.8em;color:var(--text2);margin-bottom:8px>' + fp.description.replace(/\n/g,'<br>') + '</p>';
    fp.stages.forEach(function(s, i) {
      h += '<div class=stage-box><b>' + (i+1) + '、' + s.name + '</b>' + (s.name_en?' <span class="en-line" style=font-size:0.7em;color:var(--text2)>(' + s.name_en + ')</span>':'') + '<br>' + (s.description||'').replace(/\n/g,'<br>');
      if (s.description_en) h += '<div class="en-line" style="font-size:0.75em;color:var(--text2);line-height:1.7">📖 ' + s.description_en.replace(/\n/g,' ') + '</div>';
      h += '</div>';
    });
    h += '</div>';
  }

  // ── 华严六科 + 五大行法 ──
  var sx = cs.six_subjects;
  if (sx && sx.subjects) {
    h += '<div class=section id=sys-six><h2>🎯 华严六科 & 五大行法</h2>';
    if (sx.description_en) h += '<div class="en-line" style="font-size:0.7em;color:var(--text2);margin-bottom:4px">📖 ' + sx.description_en + '</div>';
    if (sx.description) h += '<p style=font-size:0.8em;color:var(--text2);margin-bottom:8px>' + sx.description.replace(/\n/g,'<br>') + '</p>';
    h += '<table class=v-table><tr><th>科目</th><th>内容</th></tr>';
    sx.subjects.forEach(function(s) {
      h += '<tr><td>' + s.name + '</td><td>' + s.content + '</td></tr>';
      if (s.name_en || s.content_en) h += '<tr class="en-line"><td colspan=2 style="font-size:0.7em;color:var(--text2);line-height:1.7">📖 ' + (s.name_en||s.name) + (s.content_en?' — '+s.content_en:'') + '</td></tr>';
    });
    h += '</table></div>';
  }

  // ── 三大法脉行法分工 ──
  var tl = cs.three_lineages;
  if (tl && tl.lineages) {
    h += '<div class=section id=sys-lineages><h2>⚡ 三大法脉行法分工</h2>';
    if (tl.description) h += '<p style=font-size:0.8em;color:var(--text2);margin-bottom:4px>' + tl.description.replace(/\n/g,'<br>') + '</p>';
    if (tl.description_en) h += '<div class="en-line" style="font-size:0.72em;color:var(--text2)">📖 ' + tl.description_en.replace(/\n/g,' ') + '</div>';
    tl.lineages.forEach(function(l) {
      h += '<div class=stage-box><b>' + l.name + ' →「' + l.role + '」</b>' + (l.name_en?' <span class="en-line" style=font-size:0.7em;color:var(--text2)>(' + l.name_en + ')</span>':'') + '<br>' + (l.description||'').replace(/\n/g,'<br>');
      if (l.description_en) h += '<div class="en-line" style="font-size:0.75em;color:var(--text2);line-height:1.7">📖 ' + l.description_en.replace(/\n/g,' ') + '</div>';
      if (l.note) h += '<br><span style=font-size:0.75em;color:var(--text2)>注: ' + l.note + '</span>';
      if (l.note_en) h += '<div class="en-line" style="font-size:0.72em;color:var(--text2)">📖 ' + l.note_en + '</div>';
      h += '</div>';
    });
    h += '</div>';
  }

  // ── 四大工程 ──
  var pr = cs.four_projects;
  if (pr && pr.projects) {
    h += '<div class=section id=sys-projects><h2>🏗 四大工程</h2><table class=v-table><tr><th>工程</th><th>性质</th></tr>';
    pr.projects.forEach(function(p) {
      h += '<tr><td><b>' + p.name + '</b></td><td>' + (p.description||'').replace(/\n/g,'<br>') + '</td></tr>';
      if (p.name_en || p.description_en) h += '<tr class="en-line"><td colspan=2 style="font-size:0.7em;color:var(--text2);line-height:1.7">📖 ' + (p.name_en||p.name) + (p.description_en?' — '+p.description_en.replace(/\n/g,' '):'') + '</td></tr>';
    });
    h += '</table></div>';
  }

  // ── 识·根·智 ──
  var cg = cs.cognitive_levels;
  if (cg && cg.levels) {
    h += '<div class=section id=sys-cognition><h2>🔬 识·根·智 — 三层认知转换</h2>';
    if (cg.description) h += '<p style=font-size:0.8em;color:var(--text2);margin-bottom:4px>' + cg.description.replace(/\n/g,'<br>') + '</p>';
    if (cg.description_en) h += '<div class="en-line" style="font-size:0.72em;color:var(--text2)">📖 ' + cg.description_en.replace(/\n/g,' ') + '</div>';
    cg.levels.forEach(function(l) {
      h += '<div class=stage-box><b>' + l.name + '（' + l.stage + '）</b>' + (l.name_en?' <span class="en-line" style=font-size:0.7em;color:var(--text2)>(' + l.name_en + ')</span>':'') + '<br>' + (l.description||'').replace(/\n/g,'<br>');
      if (l.description_en) h += '<div class="en-line" style="font-size:0.75em;color:var(--text2);line-height:1.7">📖 ' + l.description_en.replace(/\n/g,' ') + '</div>';
      if (l.note) h += '<br><span style=font-size:0.75em;color:var(--text2)>注: ' + l.note + '</span>';
      h += '</div>';
    });
    h += '</div>';
  }

  // ── 三缘念 ──
  var rf = cs.three_refuges;
  if (rf && rf.items) {
    h += '<div class=section id=sys-refuge><h2>🙏 三缘念 — 修行归依</h2>';
    h += '<p style=line-height:1.8>' + (rf.intro||'').replace(/\n/g,'<br>') + '<br>';
    rf.items.forEach(function(it, i) {
      h += '<b>' + (i+1) + ' ' + it.name + '</b>' + (it.name_en?' <span class="en-line" style=font-size:0.7em;color:var(--text2)>(' + it.name_en + ')</span>':'') + ' — ' + it.description + '；<br>';
    });
    if (rf.practice_attitude) h += '<span style=font-size:0.78em;color:var(--text2)>修行态度: ' + rf.practice_attitude.replace(/\n/g,' ') + '</span></p>';
    if (rf.practice_attitude_en) h += '<div class="en-line" style="font-size:0.72em;color:var(--text2)">📖 ' + rf.practice_attitude_en + '</div>';
    h += '</div>';
  }

  // ── 演进脉络 ──
  var ev = cs.evolution_timeline;
  if (ev && ev.length) {
    h += '<div class=section id=sys-evolution><h2>📅 工程面·技术面 演进脉络 & 时间线</h2>';
    h += '<table class=v-table><tr><th>时期</th><th>关键节点</th><th>体系特征</th></tr>';
    ev.forEach(function(e) {
      h += '<tr><td><b>' + e.period + '</b></td><td>' + e.node + '</td><td>' + (e.feature||'').replace(/\n/g,'<br>') + '</td></tr>';
      if (e.feature_en) h += '<tr class="en-line"><td colspan=3 style="font-size:0.7em;color:var(--text2);line-height:1.7">📖 ' + e.feature_en.replace(/\n/g,' ') + '</td></tr>';
    });
    h += '</table></div>';
  }
  return h;
}

// ═══ 禅观法要渲染 (从 PRACTICE_DATA.chan_contemplation) ═══
function renderChanContemplation() {
  var cc = (typeof PRACTICE_DATA !== 'undefined' && PRACTICE_DATA.chan_contemplation) ? PRACTICE_DATA.chan_contemplation : null;
  if (!cc || !cc.sections) return '';
  var h = '';
  cc.sections.forEach(function(sec) {
    // heart 段为运行时逻辑（依赖 HEART_ARTICLES/localStorage），由 renderPractice 内联渲染，此处跳过
    if (sec.id === 'med-heart' || sec.id === 'heart-gandhara') return;
    // 数据驱动调用占位：展开为三个既有数据驱动渲染函数
    if (sec.render === 'data-driven-calls') {
      h += renderXinfaSection() + renderDushunSection() + renderPanjiaoSection();
      return;
    }
    h += '<div class=section';
    if (sec.id) h += ' id=' + sec.id;
    h += '><h2>' + (sec.emoji || '') + (sec.title || '') + '</h2>';
    if (sec.title_en) h += '<div class="en-line" style="font-size:.7em;color:var(--text2);margin-bottom:6px">📖 ' + sec.title_en + '</div>';
    (sec.blocks || []).forEach(function(b) {
      if (b.html) h += b.html;
      if (b.html_en) h += '<div class="en-line" style="font-size:.76em;color:var(--text2);line-height:1.8;border-top:1px dashed var(--line);margin-top:4px;padding-top:4px">📖 ' + b.html_en + '</div>';
    });
    h += '</div>';
  });
  return h;
}

// ═══ 助道资粮渲染 (从 PRACTICE_DATA.zhuandao_ziliang) ═══
function renderZhuandaoSection() {
  var zz = (typeof PRACTICE_DATA !== 'undefined' && PRACTICE_DATA.zhuandao_ziliang) ? PRACTICE_DATA.zhuandao_ziliang : null;
  if (!zz || !zz.topics) return '';
  var h = '';
  h += '<div class=section id=' + (zz.section_id || 'sys-zhuandao') + ' style=border-left:4px solid var(--gold)>';
  h += '<h2>' + (zz.icon || '📦') + ' ' + zz.title +
    (zz.title_en ? '<span class="en-line" style=font-size:0.62em;display:block;color:var(--text2);margin-top:2px>' + zz.title_en + '</span>' : '') + '</h2>';
  if (zz.intro) h += '<p style="font-size:0.82em;color:var(--text2);line-height:1.8;white-space:pre-line">' + _m2h(zz.intro) + '</p>';
  if (zz.intro_en) h += '<div class="en-line" style="font-size:0.82em;color:var(--text2);line-height:1.8;white-space:pre-line"><span style="color:var(--gold);font-weight:600">📖 </span>' + _m2h(zz.intro_en) + '</div>';
  zz.topics.forEach(function(t, idx) {
    h += '<div class=wu-door id=zz-topic-' + (t.id || idx) + ' onclick="this.classList.toggle(\'open\')">';
    h += '<span class=arrow>▶</span><span class=ttl>' + t.title + '</span>';
    if (t.title_en) h += '<div class="en-line" style=font-size:0.62em;color:var(--text2);margin:0 0 2px 18px>' + t.title_en + '</div>';
    h += '<div class=body>';
    h += '<div style="font-size:0.8em;line-height:1.8;white-space:pre-line">' + t.body + '</div>';
    if (t.en_body) h += '<div class="en-line" style="font-size:0.82em;line-height:1.8;white-space:pre-line;color:var(--text2);border-top:1px dashed var(--line);margin-top:6px;padding-top:6px"><span style="color:var(--gold);font-weight:600">📖 </span>' + _m2h(t.en_body) + '</div>';
    if (t.source) h += '<p style="font-size:0.68em;color:var(--text2);margin-top:8px;border-top:1px dotted var(--line);padding-top:6px">📎 ' + _m2h(t.source) + '</p>';
    h += '</div></div>';
  });
  if (zz.references) {
    h += '<details style=font-size:0.72em;margin-top:8px><summary>📚 参考文献 (' + zz.references.length + '条)</summary><ul>';
    zz.references.forEach(function(r) { h += '<li>' + r + '</li>'; });
    h += '</ul></details>';
  }
  h += '</div>';
  return h;
}

// ═══ 三十七道品渲染 (从 PRACTICE_DATA.sanshiqi_daopin) ═══
function renderSanShiQiDaoPin() {
  var sq = (typeof PRACTICE_DATA !== 'undefined' && PRACTICE_DATA.sanshiqi_daopin) ? PRACTICE_DATA.sanshiqi_daopin : null;
  if (!sq || !sq.topics) return '';
  var h = '';
  h += '<div class=section id=' + (sq.section_id || 'sys-sanshiqi') + ' style=border-left:4px solid var(--gold)>';
  h += '<h2>' + (sq.icon || '☸') + ' ' + sq.title +
    (sq.title_en ? '<span class="en-line" style=font-size:0.62em;display:block;color:var(--text2);margin-top:2px>' + sq.title_en + '</span>' : '') + '</h2>';
  if (sq.intro) h += '<p style="font-size:0.82em;color:var(--text2);line-height:1.8;white-space:pre-line">' + _m2h(sq.intro) + '</p>';
  if (sq.intro_en) h += '<div class="en-line" style="font-size:0.82em;color:var(--text2);line-height:1.8;white-space:pre-line"><span style="color:var(--gold);font-weight:600">📖 </span>' + _m2h(sq.intro_en) + '</div>';
  sq.topics.forEach(function(t, idx) {
    h += '<div class=wu-door id=sq-topic-' + (t.id || idx) + ' onclick="this.classList.toggle(\'open\')">';
    h += '<span class=arrow>▶</span><span class=ttl>' + t.title + '</span>';
    if (t.title_en) h += '<div class="en-line" style=font-size:0.62em;color:var(--text2);margin:0 0 2px 18px>' + t.title_en + '</div>';
    h += '<div class=body>';
    h += '<div style="font-size:0.8em;line-height:1.8;white-space:pre-line">' + t.body + '</div>';
    if (t.en_body) h += '<div class="en-line" style="font-size:0.82em;line-height:1.8;white-space:pre-line;color:var(--text2);border-top:1px dashed var(--line);margin-top:6px;padding-top:6px"><span style="color:var(--gold);font-weight:600">📖 </span>' + _m2h(t.en_body) + '</div>';
    if (t.source) h += '<p style="font-size:0.68em;color:var(--text2);margin-top:8px;border-top:1px dotted var(--line);padding-top:6px">📎 ' + _m2h(t.source) + '</p>';
    h += '</div></div>';
  });
  if (sq.references) {
    h += '<details style=font-size:0.72em;margin-top:8px><summary>📚 参考文献 (' + sq.references.length + '条)</summary><ul>';
    sq.references.forEach(function(r) { h += '<li>' + r + '</li>'; });
    h += '</ul></details>';
  }
  h += '</div>';
  return h;
}

// ═══ 侧边子目录导航 (先切子页再滚动到锚点) ═══
function jxSubNav(view,anchor){
  // Switch to the sub-page first
  var navBtn=document.querySelector('#sidebar .nav-link[onclick*="'+view+'"]');
  switchPracticeView(view,navBtn);
  // Then scroll to anchor after render
  setTimeout(function(){
    var el=document.getElementById(anchor);
    if(el)el.scrollIntoView({behavior:'smooth',block:'start'});
  },100);
}

// Restore sub-page on load (heart 已并入 meditation)
(function(){
  setTimeout(function(){
    var sub='system';
    try{
      sub=localStorage.getItem('practice_sub')||'system';
    }catch(e){}
    if(sub==='heart')sub='meditation';
    if(sub&&['system','meditation','news','resources','chan_traces','chengguan','vinaya','faxiang','yikong','mimi','tiantai'].indexOf(sub)>=0){
      switchPracticeView(sub);
    }
  },150);
})();

// ═══ 实修心要持久化 (localStorage + 导出/导入) ═══
var HEART_STORE_KEY='huayan_heart_data_v2';
function heartSaveAll(){
  var data={edits:{},notes:{},ts:new Date().toISOString()};
  document.querySelectorAll('[id$="-r1"],[id$="-r2"]').forEach(function(el){
    var id=el.id, html=el.innerHTML;
    var orig=el.getAttribute('data-orig');
    if(orig!==null && html!==orig) data.edits[id]=html;
    // Collect notes
    el.querySelectorAll('.heart-note').forEach(function(note){
      if(!data.notes[id]) data.notes[id]=[];
      data.notes[id].push(note.innerHTML);
    });
  });
  try{localStorage.setItem(HEART_STORE_KEY,JSON.stringify(data));return true;}catch(e){return false;}
}
function heartLoadAll(){
  try{
    var raw=localStorage.getItem(HEART_STORE_KEY);
    if(!raw)return false;
    var data=JSON.parse(raw);
    // Restore edits
    if(data.edits){Object.keys(data.edits).forEach(function(id){var el=document.getElementById(id);if(el){el.innerHTML=data.edits[id];el.setAttribute('data-orig',data.edits[id]);}});}
    // Restore notes
    if(data.notes){Object.keys(data.notes).forEach(function(id){var el=document.getElementById(id);if(el){(data.notes[id]||[]).forEach(function(n){var d=document.createElement('div');d.className='heart-note';d.innerHTML=n;el.appendChild(d);});}});}
    return !!data.ts;
  }catch(e){return false;}
}
function heartExport(){
  heartSaveAll();
  var data=localStorage.getItem(HEART_STORE_KEY);
  if(!data){heartToast('⚠ 无数据可导出');return;}
  var blob=new Blob([data],{type:'application/json'});
  var a=document.createElement('a');a.href=URL.createObjectURL(blob);
  a.download='huayan_heart_backup_'+new Date().toISOString().slice(0,10)+'.json';
  document.body.appendChild(a);a.click();document.body.removeChild(a);
  heartToast('💾 已导出 JSON (可 git add + commit + push 回仓库)');
}
function heartImport(){
  var input=document.createElement('input');input.type='file';input.accept='.json';
  input.onchange=function(e){
    var file=e.target.files[0];if(!file)return;
    var reader=new FileReader();
    reader.onload=function(ev){
      try{
        var data=JSON.parse(ev.target.result);
        localStorage.setItem(HEART_STORE_KEY,JSON.stringify(data));
        heartToast('📥 已导入 '+Object.keys(data.edits||{}).length+' 项编辑/'+Object.keys(data.notes||{}).length+' 条批注 · 刷新页面生效');
      }catch(ex){heartToast('❌ JSON格式错误');}
    };
    reader.readAsText(file);
  };
  input.click();
}
// Auto-save on edit complete
var _heartAutoSaveTimer=null;
document.addEventListener('blur',function(e){
  if(e.target.contentEditable==='true'||e.target.closest('[contenteditable=true]')){
    clearTimeout(_heartAutoSaveTimer);
    _heartAutoSaveTimer=setTimeout(function(){if(heartSaveAll())heartToast('💾 已自动保存',true);},800);
  }
},true);

// ═══ 实修心要工具栏函数 ═══
function heartCopy(elId){
  var el=document.getElementById(elId);
  if(!el)return;
  var txt=el.innerText||el.textContent||'';
  if(navigator.clipboard&&navigator.clipboard.writeText){
    navigator.clipboard.writeText(txt).then(function(){heartFlash(el,'✅ 已复制');});
  }else{
    // Fallback for older browsers
    var ta=document.createElement('textarea');
    ta.value=txt;ta.style.position='fixed';ta.style.left='-9999px';
    document.body.appendChild(ta);ta.select();
    try{document.execCommand('copy');heartFlash(el,'✅ 已复制');}catch(e){heartFlash(el,'❌ 复制失败');}
    document.body.removeChild(ta);
  }
}
function heartEdit(elId){
  var el=document.getElementById(elId);
  if(!el)return;
  if(el.contentEditable==='true'){
    el.contentEditable='false';
    el.style.outline='';
    // Save on exit edit mode
    if(el.getAttribute('data-orig')===null)el.setAttribute('data-orig',el.innerHTML);
    heartSaveAll();
    heartFlash(el,'💾 已保存');
  }else{
    if(el.getAttribute('data-orig')===null)el.setAttribute('data-orig',el.innerHTML);
    el.contentEditable='true';
    el.style.outline='2px dashed var(--gold)';
    el.focus();
    heartFlash(el,'✏️ 可编辑(失焦=自动保存)');
    el.onkeydown=function(e){if(e.ctrlKey&&e.key==='Enter'){e.preventDefault();heartEdit(elId);}};
  }
}
function heartToast(msg,quiet){
  if(quiet)return;
  var f=document.createElement('div');
  f.style.cssText='position:fixed;top:40%;left:50%;transform:translate(-50%,-50%);background:var(--gold);color:#fff;padding:6px 16px;border-radius:20px;font-size:.85em;z-index:9999;pointer-events:none;opacity:0;transition:opacity .3s';
  f.textContent=msg;document.body.appendChild(f);
  requestAnimationFrame(function(){f.style.opacity='1';});
  setTimeout(function(){f.style.opacity='0';setTimeout(function(){document.body.removeChild(f);},300);},1500);
}
// ── Comment save/restore ──
function heartSaveComment(cid){
  var el=document.getElementById(cid+'-cmt');if(!el)return;
  var all={};try{all=JSON.parse(localStorage.getItem('huayan_comments_v1')||'{}');}catch(e){}
  all[cid]=el.value;localStorage.setItem('huayan_comments_v1',JSON.stringify(all));
}
function heartLoadComments(){
  var all={};try{all=JSON.parse(localStorage.getItem('huayan_comments_v1')||'{}');}catch(e){}
  Object.keys(all).forEach(function(cid){
    var el=document.getElementById(cid+'-cmt');if(el)el.value=all[cid]||'';
  });
}
// Load comments on render
setTimeout(heartLoadComments,600);

function heartAddNote(elId){
  var el=document.getElementById(elId);
  if(!el)return;
  var note=prompt('输入批注内容:','');
  if(!note||!note.trim())return;
  var noteDiv=document.createElement('div');
  noteDiv.className='heart-note';
  noteDiv.innerHTML='💬 '+note.replace(/</g,'&lt;').replace(/>/g,'&gt;')+' <span style=font-size:.75em;color:var(--text2)>('+new Date().toLocaleString('zh-CN')+')</span>';
  el.appendChild(noteDiv);
  heartSaveAll();
  heartToast('➕ 批注已添加');
}
function heartFlash(el,msg){
  var f=document.createElement('div');
  f.style.cssText='position:fixed;top:40%;left:50%;transform:translate(-50%,-50%);background:var(--gold);color:#fff;padding:6px 16px;border-radius:20px;font-size:.85em;z-index:9999;pointer-events:none;opacity:0;transition:opacity .3s';
  f.textContent=msg;document.body.appendChild(f);
  requestAnimationFrame(function(){f.style.opacity='1';});
  setTimeout(function(){f.style.opacity='0';setTimeout(function(){document.body.removeChild(f);},300);},1500);
}

// ═══ GitHub Token 登录 + Push (静态站点唯一可靠方案) ═══
(function(){
var O='LengyanReader',R='huayan_collection',B='main',P='data/user/heart_annotations.json';
var STORAGE_KEY='gh_pat_v4';
var ghToken=localStorage.getItem(STORAGE_KEY);
var _toast=function(m){var e=document.getElementById('git-bar-status');if(e){e.textContent=m;setTimeout(function(){_update();},2500);}};

function _isOkay(){return !!ghToken;}

// Token 输入
window.heartLogin=function(){
  var msg='GitHub Fine-grained Token(仅存浏览器):\n\n生成: GitHub→Settings→Developer settings→Fine-grained tokens→Generate new token\n→Only select: '+O+'/'+R+'\n→Permissions: Contents→Read and Write\n\n粘贴Token:';
  var t=prompt(msg,localStorage.getItem(STORAGE_KEY)||'');
  if(!t||!t.trim())return;
  var token=t.trim();
  fetch('https://api.github.com/user',{headers:{'Authorization':'Bearer '+token,'Accept':'application/vnd.github+json'}})
  .then(function(r){return r.json();})
  .then(function(u){
    // 任何账号均可登录评论; 仅LengyanReader可Push
    localStorage.setItem(STORAGE_KEY,token);ghToken=token;
    localStorage.setItem('gh_username',u.login);
    _update();
    _toast(u.login==='LengyanReader'?'✅ LengyanReader · 评论+Push已启用':'✅ '+u.login+' · 评论已启用 (仅LengyanReader可Push)');
  }).catch(function(){_toast('❌ Token验证失败');});
};
// Push
window.heartPushToGitHub=function(){
  if(!_isOkay()){_toast('❌ 请先🔑配置Token');heartLogin();return;}
  var ghu=localStorage.getItem('gh_username');
  if(ghu!=='LengyanReader'){_toast('⛔ Push仅限LengyanReader');return;}
  var edits={},notes={},comments={};
  try{comments=JSON.parse(localStorage.getItem('huayan_comments_v1')||'{}');}catch(e){}
  document.querySelectorAll('[id$="-l"],[id$="-r1"],[id$="-r2"]').forEach(function(e){var o=e.getAttribute('data-orig');if(o!==null&&e.innerHTML!==o)edits[e.id]=e.innerHTML;});
  document.querySelectorAll('.heart-note').forEach(function(n){var p=n.parentElement.id;if(!notes[p])notes[p]=[];notes[p].push(n.innerHTML);});
  var c=JSON.stringify({ts:new Date().toISOString(),edits:edits,notes:notes,comments:comments},null,2);
  _toast('⏳ Push...');
  var api='https://api.github.com/repos/'+O+'/'+R+'/contents/'+P+'?ref='+B;
  var hd={'Authorization':'Bearer '+ghToken,'Accept':'application/vnd.github+json'};
  fetch(api,{headers:hd}).then(function(r){return r.ok?r.json():null;})
  .then(function(ex){var b={message:'feat: 网页直存 ['+new Date().toISOString().slice(0,19).replace('T',' ')+']',content:btoa(unescape(encodeURIComponent(c))),branch:B};
    if(ex&&ex.sha)b.sha=ex.sha;
    return fetch('https://api.github.com/repos/'+O+'/'+R+'/contents/'+P,{method:'PUT',headers:Object.assign({'Content-Type':'application/json'},hd),body:JSON.stringify(b)});
  }).then(function(r){return r.json();})
  .then(function(d){
    if(d.content||d.commit){_toast('✅ Push: '+d.commit.sha.substring(0,7)+' · Pages自动更新');if(typeof heartSaveAll==='function')heartSaveAll();}
    else{_toast('❌ '+d.message);if(d.message.indexOf('401')>=0){localStorage.removeItem(STORAGE_KEY);ghToken=null;_update();}}
  }).catch(function(e){_toast('❌ '+e.message);});
};
// Logout
window.heartLogout=function(){localStorage.removeItem(STORAGE_KEY);ghToken=null;_update();_toast('🔓 已清除');};
// UI update
function _update(){
  var st=document.getElementById('git-bar-status'),pu=document.getElementById('git-bar-push'),us=document.getElementById('git-bar-user');
  if(ghToken){
    if(st)st.innerHTML='✅ 已授权 · <b>Ctrl+Shift+S</b> 保存至GitHub';
    if(pu)pu.style.display='inline';
    if(us){us.style.display='inline';us.innerHTML='<a href=\"#\" onclick=\"heartLogout();return false\" style=color:var(--text2)>清除</a>';}
  }else{
    if(st)st.innerHTML='<a href=\"#\" onclick=\"heartLogin();return false\">🔑 配置授权</a> · 编辑后可保存至GitHub'
      +' · <a href=\"https://github.com/LengyanReader/huayan_collection/issues/new?title=%E5%BB%BA%E8%AE%AE:&body=%E6%9D%A5%E8%87%AA%E7%BD%91%E9%A1%B5%E7%9A%84%E5%8F%8D%E9%A6%88%0A%0A---%0A%E8%AF%B7%E6%8F%8F%E8%BF%B0%E4%BD%A0%E7%9A%84%E5%BB%BA%E8%AE%AE%E6%88%96%E9%97%AE%E9%A2%98:\" target=_blank style=color:#5e8b9e;font-size:0.9em>💬 提交建议</a>';
    if(pu)pu.style.display='none';if(us)us.style.display='none';
  }
}
// ── Image paste support for comment textareas in 实修心要 ──
document.addEventListener('paste',function(e){
  var ta=e.target.closest('textarea[id$="-cmt"]')||e.target.closest('textarea[id$="-lcmt"]')||e.target.closest('textarea[id$="-r1cmt"]');
  if(!ta)return;
  var items=e.clipboardData&&e.clipboardData.items;if(!items)return;
  for(var i=0;i<items.length;i++){
    if(items[i].type.indexOf('image')===0){
      e.preventDefault();
      var blob=items[i].getAsFile(),reader=new FileReader();
      reader.onload=function(ev){var uri=ev.target.result;if(uri.length>500000){alert('⚠ 图片过大('+Math.round(uri.length/1024)+'KB),建议压缩后贴。');}var img='![图片]('+uri+')';var s=ta.selectionStart;ta.value=ta.value.substring(0,s)+'\n'+img+'\n'+ta.value.substring(ta.selectionEnd);ta.selectionStart=ta.selectionEnd=s+img.length+2;ta.focus();};
      reader.readAsDataURL(blob);break;
    }
  }
});
// Hotkey: Ctrl+Shift+S = Push to GitHub
document.addEventListener('keydown',function(e){
  if(e.ctrlKey&&e.shiftKey&&e.key==='S'){e.preventDefault();heartPushToGitHub();}
});
// Fetch recent GitHub Issues for display
(function loadIssues(){
  fetch('https://api.github.com/repos/LengyanReader/huayan_collection/issues?state=all&per_page=5&sort=updated')
  .then(function(r){return r.json();})
  .then(function(issues){
    if(!issues||!issues.length)return;
    var el=document.getElementById('git-bar-issues');if(!el)return;
    var html='';issues.forEach(function(i){html+=' · <a href='+i.html_url+' target=_blank style=font-size:0.85em title=\"'+i.title.replace(/\"/g,'&quot;')+'\">#'+i.number+'</a>';});
    el.innerHTML=html;
  }).catch(function(){});
})();
setTimeout(function(){_update();},600);
})();

// ═══ 律己戒他渲染 (从 PRACTICE_DATA.vinaya_school) ═══
function renderVinayaSection() {
  var vy = (typeof PRACTICE_DATA !== 'undefined' && PRACTICE_DATA.vinaya_school) ? PRACTICE_DATA.vinaya_school : null;
  if (!vy || !vy.sections) return '';
  var h = '';
  vy.sections.forEach(function(sec) {
    h += '<div class=section id=vy-' + sec.id.replace('vinaya_','') + '>';
    h += '<h2>' + (sec.icon||'📌') + ' ' + sec.title +
      (sec.title_en ? '<span class="en-line" style=font-size:0.62em;display:block;color:var(--text2);margin-top:2px>' + sec.title_en + '</span>' : '') + '</h2>';
    if (sec.intro) h += '<p style="font-size:0.82em;color:var(--text2);line-height:1.8;white-space:pre-line">' + _m2h(sec.intro) + '</p>';
    if (sec.intro_en) h += '<div class="en-line" style="font-size:0.82em;color:var(--text2);line-height:1.8;white-space:pre-line"><span style="color:var(--gold);font-weight:600">📖 </span>' + _m2h(sec.intro_en) + '</div>';
    if (sec.topics) {
      sec.topics.forEach(function(t, idx) {
        h += '<div class=wu-door id=vy-topic-' + idx + ' onclick="this.classList.toggle(\'open\')">';
        h += '<span class=arrow>▶</span><span class=ttl>' + t.title + '</span>';
        if (t.title_en) h += '<div class="en-line" style=font-size:0.62em;color:var(--text2);margin:0 0 2px 18px>' + t.title_en + '</div>';
        h += '<div class=body>';
        h += '<p style=font-size:0.8em;line-height:1.8;white-space:pre-line>' + _m2h(t.body) + '</p>';
        if (t.en_body) h += '<div class="en-line" style="font-size:0.82em;line-height:1.8;white-space:pre-line;color:var(--text2);border-top:1px dashed var(--line);margin-top:6px;padding-top:6px"><span style="color:var(--gold);font-weight:600">📖 </span>' + _m2h(t.en_body) + '</div>';
        if (t.source) h += '<p style=font-size:0.68em;color:var(--text2);margin-top:4px">📎 ' + _m2h(t.source) + '</p>';
        h += '</div></div>';
      });
    }
    h += '</div>';
  });
  // References
  if (vy.references) {
    h += '<details style=font-size:0.72em;margin-top:8px><summary>📚 参考文献 (' + vy.references.length + '条)</summary><ul>';
    vy.references.forEach(function(r) { h += '<li>' + r + '</li>'; });
    h += '</ul></details>';
  }
  return h;
}

// ═══ 法相玄机渲染 (从 PRACTICE_DATA.faxiang_xuanji) ═══
function renderFaxiangSection() {
  var fx = (typeof PRACTICE_DATA !== 'undefined' && PRACTICE_DATA.faxiang_xuanji) ? PRACTICE_DATA.faxiang_xuanji : null;
  if (!fx || !fx.sections) return '';
  var h = '';
  fx.sections.forEach(function(sec) {
    h += '<div class=section id=fx-' + sec.id.replace('fx_','') + '>';
    h += '<h2>' + (sec.icon||'📌') + ' ' + sec.title;
    if (sec.title_en) h += '<span class="en-line" style="font-size:0.62em;display:block;color:var(--text2);margin-top:2px">' + sec.title_en + '</span>';
    h += '</h2>';
    if (sec.intro) h += '<p style="font-size:0.82em;color:var(--text2);line-height:1.8;white-space:pre-line">' + _m2h(sec.intro) + '</p>';
    if (sec.intro_en) h += '<p class="en-line" style="white-space:pre-line;font-size:0.78em;color:var(--text2);line-height:1.8"><span style="color:var(--gold);font-weight:600">📖 </span>' + _m2h(sec.intro_en) + '</p>';
    if (sec.topics) {
      sec.topics.forEach(function(t, idx) {
        h += '<div class=wu-door id=fx-topic-' + idx + ' onclick="this.classList.toggle(\'open\')">';
        h += '<span class=arrow>▶</span><span class=ttl>' + t.title + '</span>';
        if (t.title_en) h += '<div class="en-line" style="font-size:0.62em;color:var(--text2);margin-left:18px;margin-bottom:4px">' + t.title_en + '</div>';
        h += '<div class=body>';
        h += '<p style=font-size:0.8em;line-height:1.8;white-space:pre-line>' + _m2h(t.body) + '</p>';
        if (t.en_body) h += '<div class="en-line" style="white-space:pre-line;font-size:0.82em;color:var(--text2);border-top:1px dashed var(--line);margin-top:6px;padding-top:6px"><span style="color:var(--gold);font-weight:600">📖 </span>' + _m2h(t.en_body) + '</div>';
        if (t.source) h += '<p style=font-size:0.68em;color:var(--text2);margin-top:4px">📎 ' + _m2h(t.source) + '</p>';
        h += '</div></div>';
      });
    }
    h += '</div>';
  });
  if (fx.references) {
    h += '<details style=font-size:0.72em;margin-top:8px><summary>📚 参考文献 (' + fx.references.length + '条)</summary><ul>';
    fx.references.forEach(function(r) { h += '<li>' + r + '</li>'; });
    h += '</ul></details>';
  }
  return h;
}

// ═══ 一空到底渲染 (从 PRACTICE_DATA.yikong_daodi) ═══
function renderYikongSection() {
  var yk = (typeof PRACTICE_DATA !== 'undefined' && PRACTICE_DATA.yikong_daodi) ? PRACTICE_DATA.yikong_daodi : null;
  if (!yk || !yk.sections) return '';
  // md helper: **bold** → <b>, *italic* → <i>
  function md(s) {
    return String(s||'')
      .replace(/\*\*(.+?)\*\*/g, '<b>$1</b>')
      .replace(/(^|[^*])\*([^*]+?)\*(?!\*)/g, '$1<i>$2</i>');
  }
  var h = '';
  yk.sections.forEach(function(sec) {
    h += '<div class=section id=yk-' + sec.id.replace('yk_','') + '>';
    h += '<h2>' + (sec.icon||'📌') + ' ' + sec.title;
    if (sec.title_en) h += '<span class="en-line" style="font-size:0.62em;display:block;color:var(--text2);margin-top:2px">' + sec.title_en + '</span>';
    h += '</h2>';
    if (sec.intro) h += '<p style="font-size:0.82em;color:var(--text2);line-height:1.8;white-space:pre-line">' + md(sec.intro) + '</p>';
    if (sec.intro_en) h += '<p class="en-line" style="white-space:pre-line;font-size:0.78em;color:var(--text2);line-height:1.8"><span style="color:var(--gold);font-weight:600">📖 </span>' + sec.intro_en + '</p>';
    if (sec.topics) {
      sec.topics.forEach(function(t, idx) {
        h += '<div class=wu-door id=yk-topic-' + sec.id + '-' + idx + ' onclick="this.classList.toggle(\'open\')">';
        h += '<span class=arrow>▶</span><span class=ttl>' + t.title + '</span>';
        if (t.title_en) h += '<div class="en-line" style="font-size:0.62em;color:var(--text2);margin-left:18px;margin-bottom:4px">' + t.title_en + '</div>';
        h += '<div class=body>';
        h += '<p style=font-size:0.8em;line-height:1.8;white-space:pre-line>' + md(t.body) + '</p>';
        if (t.en_body) h += '<div class="en-line" style="white-space:pre-line;font-size:0.82em;color:var(--text2);border-top:1px dashed var(--line);margin-top:6px;padding-top:6px"><span style="color:var(--gold);font-weight:600">📖 </span>' + md(t.en_body) + '</div>';
        if (t.links) {
          Object.keys(t.links).forEach(function(k) {
            h += '<a href="' + t.links[k] + '" target=_blank style="font-size:0.72em;color:var(--blue)">🔗 ' + k + '</a> ';
          });
        }
        if (t.source) h += '<p style=font-size:0.68em;color:var(--text2);margin-top:4px">📎 ' + md(t.source) + '</p>';
        h += '</div></div>';
      });
    }
    h += '</div>';
  });
  // References
  if (yk.references) {
    h += '<details style=font-size:0.72em;margin-top:8px><summary>📚 参考文献 (学术·门内·近现代·海云)</summary>';
    Object.keys(yk.references).forEach(function(k) {
      h += '<p style=margin:4px 0><b>' + k + '</b></p><ul style=margin:0>';
      yk.references[k].forEach(function(r) { h += '<li>' + r + '</li>'; });
      h += '</ul>';
    });
    h += '</details>';
  }
  // ── 法脉传承表 ──
  h += '<div class=section id=yk-diagrams><h2>📊 般若·中观·三论法脉传承</h2>';
  h += '<table class=v-table style=font-size:0.75em><tr><th>时期</th><th>人物</th><th>贡献</th></tr>';
  h += '<tr><td>印度奠基</td><td>龙树(约150-250)→提婆(约170-270)</td><td>《中论》《大智度论》·《百论》《四百论》</td></tr>';
  h += '<tr><td>印度分流</td><td>佛护(随应破)·清辨(自续)·月称(应成)</td><td>应成/自续分流·藏传之源头</td></tr>';
  h += '<tr><td>印度综合</td><td>寂护·莲花戒</td><td>随瑜伽行中观·首入西藏</td></tr>';
  h += '<tr><td>汉译开端</td><td>支娄迦谶→朱士行→竺法护</td><td>《道行般若》·《放光般若》·《光赞般若》</td></tr>';
  h += '<tr><td>格义时代</td><td>六家七宗(道安·支遁等)</td><td>玄学类比般若</td></tr>';
  h += '<tr><td>译场</td><td>鸠摩罗什(343-413)→僧肇(384-414)</td><td>译中论百论十二门论·《肇论》终结格义</td></tr>';
  h += '<tr><td>三论宗</td><td>僧朗→僧诠→法朗→吉藏(549-623)</td><td>摄山重光·嘉祥集大成·《三论玄义》</td></tr>';
  h += '<tr><td>日本</td><td>慧灌(625东渡)</td><td>南都六宗·吉藏著述长存</td></tr>';
  h += '<tr><td>藏传</td><td>阿底峡→宗喀巴(1357-1419)</td><td>应成派入藏·格鲁派中观见·辩经学院</td></tr>';
  h += '<tr><td>近现代</td><td>杨仁山·法尊·印顺</td><td>三论章疏重见天日·藏传应成见译回汉文</td></tr>';
  h += '<tr><td>当代</td><td>刘峰(三论义学)·格鲁辩经传统</td><td>汉传三论薪传·藏传活传统</td></tr>';
  h += '</table></div>';
  return h;
}

// ═══ 不密而密渲染 (从 PRACTICE_DATA.mimi_daodi) ═══
function renderMimiSection() {
  var mm = (typeof PRACTICE_DATA !== 'undefined' && PRACTICE_DATA.mimi_daodi) ? PRACTICE_DATA.mimi_daodi : null;
  if (!mm || !mm.sections) return '';
  function md(s) {
    return String(s||'')
      .replace(/\*\*(.+?)\*\*/g, '<b>$1</b>')
      .replace(/(^|[^*])\*([^*]+?)\*(?!\*)/g, '$1<i>$2</i>');
  }
  var h = '';
  mm.sections.forEach(function(sec) {
    h += '<div class=section id=mm-' + sec.id.replace('mm_','') + '>';
    h += '<h2>' + (sec.icon||'📌') + ' ' + sec.title;
    if (sec.title_en) h += '<span class="en-line" style="font-size:0.62em;display:block;color:var(--text2);margin-top:2px">' + sec.title_en + '</span>';
    h += '</h2>';
    if (sec.intro) h += '<p style="font-size:0.82em;color:var(--text2);line-height:1.8;white-space:pre-line">' + md(sec.intro) + '</p>';
    if (sec.intro_en) h += '<p class="en-line" style="white-space:pre-line;font-size:0.78em;color:var(--text2);line-height:1.8"><span style="color:var(--gold);font-weight:600">📖 </span>' + sec.intro_en + '</p>';
    if (sec.topics) {
      sec.topics.forEach(function(t, idx) {
        h += '<div class=wu-door id=mm-topic-' + sec.id + '-' + idx + ' onclick="this.classList.toggle(\'open\')">';
        h += '<span class=arrow>▶</span><span class=ttl>' + t.title + '</span>';
        if (t.title_en) h += '<div class="en-line" style="font-size:0.62em;color:var(--text2);margin-left:18px;margin-bottom:4px">' + t.title_en + '</div>';
        h += '<div class=body>';
        h += '<p style=font-size:0.8em;line-height:1.8;white-space:pre-line>' + md(t.body) + '</p>';
        if (t.en_body) h += '<div class="en-line" style="white-space:pre-line;font-size:0.82em;color:var(--text2);border-top:1px dashed var(--line);margin-top:6px;padding-top:6px"><span style="color:var(--gold);font-weight:600">📖 </span>' + md(t.en_body) + '</div>';
        if (t.links) {
          Object.keys(t.links).forEach(function(k) {
            h += '<a href="' + t.links[k] + '" target=_blank style="font-size:0.72em;color:var(--blue)">🔗 ' + k + '</a> ';
          });
        }
        if (t.source) h += '<p style=font-size:0.68em;color:var(--text2);margin-top:4px">📎 ' + md(t.source) + '</p>';
        h += '</div></div>';
      });
    }
    h += '</div>';
  });
  if (mm.references) {
    h += '<details style=font-size:0.72em;margin-top:8px><summary>📚 参考文献 (原典·教内·近现代·学术)</summary>';
    Object.keys(mm.references).forEach(function(k) {
      h += '<p style=margin:4px 0><b>' + k + '</b></p><ul style=margin:0>';
      mm.references[k].forEach(function(r) { h += '<li>' + r + '</li>'; });
      h += '</ul>';
    });
    h += '</details>';
  }
  return h;
}