// ═══ 世主妙严 COSMOLOGY TAB ═══
var COSMO={scale:1,sel:null,net:true,all:false};
var COSMO_WINDS=['平等住','出生宝庄严','清净光','光明轮','普持','不动','普照','法界云','大光明','法界光明云'];
var COSMO_LAYERS=[
  {n:'最胜光遍照',b:'净眼离垢灯佛'},{n:'种种香莲华妙庄严',b:'师子光胜照佛'},
  {n:'一切宝庄严普照光',b:'净光智胜幢佛'},{n:'种种光明华庄严',b:'金刚光明无量精进力善出现佛'},
  {n:'普放妙华光',b:'香光喜力海佛'},{n:'净妙光明',b:'普光自在幢佛'},
  {n:'众华焰庄严',b:'欢喜海功德名称自在光佛'},{n:'出生威力地',b:'广大名称智海幢佛'},
  {n:'出妙音声',b:'清净月光明相无能摧伏佛'},{n:'金刚幢',b:'一切法海最胜王佛'},
  {n:'恒出现帝青宝光明',b:'无量功德海光明佛'},{n:'光明照耀',b:'超释梵光佛'},
  {n:'娑婆世界',b:'毗卢遮那如来',saha:true},{n:'寂静离尘光',b:'遍法界胜音佛'},
  {n:'众妙光明灯',b:'不可摧伏力普照幢佛'},{n:'清净光遍照',b:'清净日功德眼佛'},
  {n:'宝庄严藏',b:'无碍智光明遍照十方佛'},{n:'离尘',b:'无量方便最胜幢佛'},
  {n:'清净光普照',b:'普照法界虚空光佛'},{n:'妙宝焰',b:'福德相光明佛'}
];

function renderCosmology(){
  var cv=document.getElementById("cosmology-view");if(!cv)return;
  var h='<style>.cm-btn{padding:3px 10px;border:1px solid var(--line);border-radius:12px;background:var(--card);color:var(--text2);cursor:pointer;font-size:0.73em}.cm-btn.on{background:var(--gold);color:#fff}#cosmo-info{display:none;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px;margin-top:8px;font-size:0.82em;line-height:1.7}</style>';
  h+='<div class=section style=border-left:4px solid var(--gold)><h2>🪷 世主妙严 · 华藏世界海</h2><p style=font-size:0.82em;color:var(--text2)>据《华严经·华藏世界品》(T10n0279卷八~十)。十重风轮持香水海,海中出大莲华,二十重世界层层叠绕。毗卢遮那佛法身遍满。源: CBETA T10n0279</p></div>';
  h+='<button class="cm-btn on" onclick="COSMO.net=!COSMO.net;this.classList.toggle(\'on\',COSMO.net);drawCosmo()">🕸 因陀罗网</button> ';
  h+='<button class="cm-btn" onclick="COSMO.all=!COSMO.all;this.classList.toggle(\'on\',COSMO.all);drawCosmo()">📋 全部层名</button> ';
  h+='<span style=font-size:0.7em;color:var(--text2)>滚轮缩放 | 点击世界层查看详情 | 金色=娑婆世界</span>';
  h+='<div style=display:flex;gap:16px;flex-wrap:wrap><div style=flex:1.5;min-width:380px;text-align:center;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px><canvas id=cosmo-canvas style=max-width:100%></canvas></div><div style=flex:1;min-width:200px><div id=cosmo-info></div><div class=section style=margin-top:8px><h3 style=color:var(--gold)>📐 结构(从下至上)</h3><p style=font-size:0.78em;line-height:1.9>⑩~① 十重风轮<br>无边妙华光香水海<br>一切香摩尼宝庄严大莲华<br>第1~20重世界<br>★第13重: 娑婆世界(我们所在)<br>一一世界有微尘数佛刹围绕</p></div></div></div>';
  // ── 三界诸天图 ──
  h+="<div class=section style=margin-top:16px><h2>📐 三界诸天·修行对应图 — 海云继梦法师修行体系</h2><p style=font-size:0.78em;color:var(--text2)>据大华严寺官网「华严禅观全程一览表」及海云法师《四十华严讲记》《华严禅行法》系列。二十八天对应<b>三阶修行次第</b>(前行/正行/妙行) + <b>十信位果位</b>(初信~入法界) + <b>禅定进路</b>(四天王定→狮子频申三昧)。源: 大华严寺官网 + fjdh.cn讲记逐字稿</p>"
  h+='<div style=text-align:center;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px><canvas id=cosmo-tower style=max-width:100%></canvas></div></div>';

  // ═══ 华严艺术珍品（折叠目录+缩略图） ═══
  h+='<div class=section><h2>🎨 华严艺术珍品（点击展开·含缩略图快照）</h2>';

  // ── 1. 七处九会 ──
  h+="<div class=wu-door onclick='this.classList.toggle(\"open\")'><span class=arrow>▶</span><span class=ttl>🏛 敦煌·华严经七处九会绢画(五代·吉美博物馆藏)</span><div class=body>";
  h+="<p style=font-size:0.82em;color:var(--gold)>唯一存世的敦煌藏经洞华严经全经绢画 · MG.26462 · 194×179cm · 10世纪</p>";
  h+="<p style=font-size:0.78em;line-height:1.7>敦煌藏经洞出土,近2米大幅绢本。九铺说法图对应七处九会:菩提场、普光明殿(3次)、忉利天宫、夜摩天宫、兜率天宫、他化天宫、逝多林。底部绘莲华藏世界海。据实叉难陀译八十华严绘制。《伯希和敦煌图录》第一卷图22即为莫高窟146窟同类题材。</p>";
  h+="<p style=font-size:0.72em;color:var(--text2)><b>📍 法国吉美国立亚洲艺术博物馆</b>(Musée Guimet, Paris) · 伯希和收集品</p>";
  h+="<p style=font-size:0.68em;margin-top:2px>🔗 <a href='https://www.guimet.fr' target=_blank>吉美博物馆官网</a> · <a href='http://idp.bl.uk/database/oo_scroll_h.a4d?uid=59205289518;bst=1;recnum=13528' target=_blank>IDP 高清大图</a> · <a href='https://www.e-dunhuang.com' target=_blank>数字敦煌</a> · <a href='https://www.sohu.com/a/406251191_467442' target=_blank>图说华严经</a></p>";
  h+="</div></div>";

  // ── 2. 十地品变相图 ──
  h+="<div class=wu-door onclick='this.classList.toggle(\"open\")'><span class=arrow>▶</span><span class=ttl>🏛 敦煌·十地品变相图(唐·绢本设色)</span><div class=body>";
  h+="<p style=font-size:0.78em;line-height:1.7>绢本设色,62.5×20cm,藏经洞出土。毗卢遮那佛于他化自在天宣说十地法门,十幅画面逐层展现欢喜地至法云地的修行次第。两侧胁侍解脱月菩萨与金刚藏菩萨。</p>";
  h+="<p style=font-size:0.72em;color:var(--text2)><b>📍 法国吉美国立东方美术馆</b></p>";
  h+="<p style=font-size:0.68em;margin-top:2px>🔗 <a href='https://www.guimet.fr' target=_blank>吉美博物馆</a> · <a href='https://www.sohu.com/a/406251191_467442' target=_blank>图说华严经</a></p>";
  h+="</div></div>";

  // ── 3. 莫高窟壁画群 ──
  h+="<div class=wu-door onclick='this.classList.toggle(\"open\")'><span class=arrow>▶</span><span class=ttl>🖼 莫高窟·华严经变壁画群(28个洞窟·盛唐~宋)</span><div class=body>";
  h+="<p style=font-size:0.78em;line-height:1.7>敦煌莫高窟现存华严经变洞窟<b>28个</b>(盛唐44窟至宋454窟)。中唐后成熟:九宫格七处九会+底部莲华藏世界+善财五十三参屏风画。代表:第12窟(北壁·数字敦煌有收录)/第237窟(双头瑞像)/第146窟(伯希和图录)。</p>";
  h+="<p style=font-size:0.68em;margin-top:2px>🔗 <a href='https://www.dha.ac.cn' target=_blank>敦煌研究院</a> · <a href='https://www.e-dunhuang.com' target=_blank>数字敦煌(e-dunhuang.com)</a> · <a href='https://dsr.nii.ac.jp/reference/pelliot/entry/1-022.html.zh' target=_blank>伯希和图录 146窟</a></p>";
  h+="</div></div>";

  // ── 4. 东大寺大佛 ──
  h+="<div class=wu-door onclick='this.classList.toggle(\"open\")'><span class=arrow>▶</span><span class=ttl>🗿 奈良东大寺·卢舍那大佛(8世纪·世界遗产) 📷有快照</span><div class=body>";
  h+="<img src='https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/NaraTodaijiDaibutsu0212.jpg/640px-NaraTodaijiDaibutsu0212.jpg' style='max-width:100%;border-radius:8px;margin-bottom:8px' loading=lazy alt='东大寺卢舍那大佛'><br>";
  h+="<span style=font-size:0.65em;color:var(--text2)>📷 东大寺卢舍那大佛 · 金铜铸造 · 高约15m · 752年开眼 · 图片: Wikipedia Public Domain (Fg2, 2005)</span>";
  h+="<p style=font-size:0.78em;line-height:1.7;margin-top:6px>日本华严宗总本山。金铜卢舍那大佛高约15m,743年圣武天皇发愿铸造,752年开眼。大佛殿为世界现存最大木构建筑(宽57m×高49m)。正仓院藏唐代华严相关文物300+件(含全球唯一存世唐五弦琵琶)。1998年世界文化遗产。</p>";
  h+="<p style=font-size:0.68em;margin-top:2px>🔗 <a href='https://www.todaiji.or.jp' target=_blank>东大寺官网</a> · <a href='https://shosoin.kunaicho.go.jp' target=_blank>正仓院(宫内厅)</a> · 🎬 <a href='https://www.youtube.com/results?search_query=%E6%9D%B1%E5%A4%A7%E5%AF%BA+%E5%A4%A7%E4%BD%9B+4K' target=_blank>YT 4K</a> · <a href='https://commons.wikimedia.org/wiki/Category:Todaiji_Daibutsu_in_art' target=_blank>Wikimedia更多</a></p>";
  h+="</div></div>";

  // ── 5. 犍陀罗 ──
  h+="<div class=wu-door onclick='this.classList.toggle(\"open\")'><span class=arrow>▶</span><span class=ttl>🏺 犍陀罗·华严佛传造像(贵霜时期·1-3世纪)</span><div class=body>";
  h+="<p style=font-size:0.78em;line-height:1.7>犍陀罗(今巴基斯坦北部)为大乘佛教发源地之一。贵霜时期大量佛传浮雕:舍卫城神变、燃灯佛授记等场景与《华严经》所述佛陀大光明神变在图像学上有渊源。栗田功《大美之佛像:犍陀罗艺术》(文物出版社2017)为权威参考。</p>";
  h+="<p style=font-size:0.68em;margin-top:2px>🔗 <a href='https://www.britishmuseum.org/collection/search?keyword=gandhara' target=_blank>大英博物馆·犍陀罗</a> · <a href='https://www.metmuseum.org/search?q=gandhara' target=_blank>大都会博物馆</a> · 🎬 <a href='https://www.bilibili.com/search?keyword=%E7%8A%8D%E9%99%80%E7%BD%97+%E4%BD%9B%E5%83%8F' target=_blank>B站犍陀罗</a></p>";
  h+="</div></div>";

  // ── 6. 双头瑞像 ──
  h+="<div class=wu-door onclick='this.classList.toggle(\"open\")'><span class=arrow>▶</span><span class=ttl>🖼 莫高窟第237窟·双头瑞像(中唐·吐蕃时期)</span><div class=body>";
  h+="<p style=font-size:0.78em;line-height:1.7>中唐代表窟。西壁佛龛顶部绘双头瑞像——故事发生在犍陀罗国:两位贫士各请画师绘释迦像,画师收两份钱绘一尊,佛像显灵现双头一身神变。身着吐蕃服装的俗人仰礼,见证汉蕃丝路文化交流。</p>";
  h+="<p style=font-size:0.68em;margin-top:2px>🔗 <a href='https://www.dha.ac.cn/info/1425/3641.htm' target=_blank>敦煌研究院·237窟</a></p>";
  h+="</div></div>";

  // ── 7. 龙门奉先寺 ──
  h+="<div class=wu-door onclick='this.classList.toggle(\"open\")'><span class=arrow>▶</span><span class=ttl>🗿 洛阳龙门·奉先寺卢舍那大佛(唐·17m) 📷有快照</span><div class=body>";
  h+="<img src='https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Vairocana%2C_Fengxian_Temple%2C_Longmen_Grottoes_%2810240207654%29.jpg/640px-Vairocana%2C_Fengxian_Temple%2C_Longmen_Grottoes_%2810240207654%29.jpg' style='max-width:100%;border-radius:8px;margin-bottom:8px' loading=lazy alt='龙门奉先寺卢舍那大佛'><br>";
  h+="<span style=font-size:0.65em;color:var(--text2)>📷 龙门奉先寺卢舍那大佛 · 唐·672年 · 通高17.14m · 图片: Wikimedia CC0 Public Domain</span>";
  h+="<p style=font-size:0.78em;line-height:1.7;margin-top:6px>龙门石窟奉先寺卢舍那大佛(通高17.14m),唐高宗咸亨三年(672)武则天赞助营造。华严教主毗卢遮那佛的盛唐皇家造像巅峰,被誉东方蒙娜丽莎。与东大寺卢舍那、敦煌华严经变并称三大华严艺术瑰宝。</p>";
  h+="<p style=font-size:0.68em;margin-top:2px>🔗 🎬 <a href='https://www.bilibili.com/search?keyword=%E9%BE%99%E9%97%A8+%E5%A5%89%E5%85%88%E5%AF%BA+%E5%8D%A2%E8%88%8E%E9%82%A3' target=_blank>B站龙门</a> · <a href='https://www.youtube.com/results?search_query=Longmen+Grottoes+Vairocana+4K' target=_blank>YT 4K</a></p>";
  h+="</div></div>";

  // ── 8. 犍陀罗佛像 ──
  h+="<div class=wu-door onclick='this.classList.toggle(\"open\")'><span class=arrow>▶</span><span class=ttl>🏺 犍陀罗·佛陀坐像(3-4世纪·CMOA藏) 📷有快照</span><div class=body>";
  h+="<div style=display:flex;gap:8px;flex-wrap:wrap>";
  h+="<img src='https://upload.wikimedia.org/wikipedia/commons/thumb/0/0f/Afghanistan%2C_Gandhara%2C_Hadda%2C_late_Kushan_Period_-_Seated_Buddha_-_1967.39_-_Cleveland_Museum_of_Art.jpg/320px-Afghanistan%2C_Gandhara%2C_Hadda%2C_late_Kushan_Period_-_Seated_Buddha_-_1967.39_-_Cleveland_Museum_of_Art.jpg' style='max-width:48%;border-radius:8px;margin-bottom:4px' loading=lazy alt='犍陀罗佛陀坐像 CMOA'>";
  h+="<img src='https://upload.wikimedia.org/wikipedia/commons/thumb/0/09/The_Buddha_shows_Miracles%2C_Gandhara%2C_3rd_century_AD%2C_schist_-_Ethnological_Museum%2C_Berlin_-_DSC01646.JPG/320px-The_Buddha_shows_Miracles%2C_Gandhara%2C_3rd_century_AD%2C_schist_-_Ethnological_Museum%2C_Berlin_-_DSC01646.JPG' style='max-width:48%;border-radius:8px;margin-bottom:4px' loading=lazy alt='犍陀罗佛陀示现神变'>";
  h+="</div>";
  h+="<span style=font-size:0.65em;color:var(--text2)>📷 左: 犍陀罗佛陀坐像(Afghanistan, Hadda, 3-4世纪, stucco, CMOA CC0) · 右: 佛陀示现神变(3世纪, 柏林民族学博物馆 CC0)</span>";
  h+="<p style=font-size:0.78em;line-height:1.7;margin-top:6px>犍陀罗(今巴基斯坦北部)为大乘佛教发源地之一。贵霜时期大量佛传浮雕:舍卫城神变、燃灯佛授记等场景与《华严经》所述佛陀大光明神变图像学有渊源。栗田功《大美之佛像》(文物出版社2017)为权威参考。</p>";
  h+="<p style=font-size:0.68em;margin-top:2px>🔗 <a href='https://www.britishmuseum.org/collection/search?keyword=gandhara' target=_blank>大英博物馆</a> · <a href='https://commons.wikimedia.org/wiki/Category:Buddhist_statues_of_Gandhara' target=_blank>Wikimedia 86张</a> · 🎬 <a href='https://www.bilibili.com/search?keyword=%E7%8A%8D%E9%99%80%E7%BD%97+%E4%BD%9B%E5%83%8F' target=_blank>B站</a></p>";
  h+="</div></div>";

  // ── 9. 视频嵌入 ──
  h+="<div class=wu-door onclick='this.classList.toggle(\"open\")'><span class=arrow>▶</span><span class=ttl>🎬 华藏世界海·3D可视化视频(YouTube嵌入)</span><div class=body>";
  h+="<p style=font-size:0.78em;line-height:1.7;margin-bottom:6px>以下为华严宇宙观相关的公开视频资源,可点击播放:</p>";
  h+="<p style=font-size:0.72em;color:var(--text2)><b>🌊 华藏世界海·3D:</b> <a href='https://www.youtube.com/results?search_query=Avatamsaka+Sutra+3D+Lotus+World' target=_blank>YouTube搜索</a> · <a href='https://www.bilibili.com/search?keyword=%E5%8D%8E%E4%B8%A5%E7%BB%8F+%E5%8D%8E%E8%97%8F%E4%B8%96%E7%95%8C+3D' target=_blank>B站搜索</a></p>";
  h+="<p style=font-size:0.72em;color:var(--text2)><b>🏛 东大寺大佛·4K:</b> <a href='https://www.youtube.com/results?search_query=Nara+Todaiji+Great+Buddha+4K' target=_blank>YouTube</a></p>";
  h+="<p style=font-size:0.72em;color:var(--text2)><b>🖼 正仓院宝物:</b> <a href='https://www.youtube.com/results?search_query=Shosoin+Treasures' target=_blank>YouTube</a> · <a href='https://www.bilibili.com/search?keyword=%E6%AD%A3%E5%80%89%E9%99%A2' target=_blank>B站正仓院</a></p>";
  h+="<p style=font-size:0.72em;color:var(--text2)><b>🏺 犍陀罗艺术纪录片:</b> <a href='https://www.youtube.com/results?search_query=Gandhara+Art+Documentary' target=_blank>YouTube</a> · <a href='https://www.bilibili.com/search?keyword=%E7%8A%8D%E9%99%80%E7%BD%97+%E8%AE%B0%E5%BD%95%E7%89%87' target=_blank>B站</a></p>";
  h+="</div></div>";
  h+='</div>';

  // ═══ 华严古迹巡礼 + 视频 + 参考（折叠） ═══
  h+='<div class=section><h2>🗺 华严古迹巡礼 · 🎬 多媒体 · 📚 参考（折叠目录）</h2>';

  h+="<div class=wu-door onclick='this.classList.toggle(\"open\")'><span class=arrow>▶</span><span class=ttl>🗺 华严古迹巡礼(6处)</span><div class=body>";
  h+='<table class=v-table style=font-size:0.7em><tr><th>古迹</th><th>地点</th><th>朝代</th><th>说明</th><th>链接</th></tr>';
  h+='<tr><td><b>终南山·至相寺</b></td><td>陕西西安</td><td>隋唐</td><td>华严宗发源地。杜顺、智俨于此创宗立教</td><td>—</td></tr>';
  h+='<tr><td><b>洛阳龙门·奉先寺</b></td><td>河南洛阳</td><td>唐</td><td>卢舍那大佛(17m),武则天赞助。华严教主盛唐造像巅峰</td><td>🎬 <a href=https://www.bilibili.com/search?keyword=%E9%BE%99%E9%97%A8+%E5%A5%89%E5%85%88%E5%AF%BA target=_blank>B站</a></td></tr>';
  h+='<tr><td><b>长安·大慈恩寺</b></td><td>陕西西安</td><td>唐</td><td>玄奘译场。华严经别译本于此译出</td><td>—</td></tr>';
  h+='<tr><td><b>五台山·大华严寺</b></td><td>山西</td><td>唐~今</td><td>澄观著《华严经疏》处。华严宗圣地</td><td>—</td></tr>';
  h+='<tr><td><b>奈良·东大寺</b></td><td>日本奈良</td><td>8世纪</td><td>日本华严宗总本山。审祥首讲华严经</td><td><a href=https://www.todaiji.or.jp target=_blank>官网</a></td></tr>';
  h+='<tr><td><b>支提山·大华严寺</b></td><td>苗栗通霄</td><td>2026动土</td><td>海云继梦。与福建宁德支提华严祖庭隔海相望</td><td><a href=https://www.huayenworld.org target=_blank>官网</a></td></tr></table>';
  h+="</div></div>";

  h+="<div class=wu-door onclick='this.classList.toggle(\"open\")'><span class=arrow>▶</span><span class=ttl>🎬 视频与多媒体资源</span><div class=body>";
  h+='<table class=v-table style=font-size:0.7em><tr><th>主题</th><th>平台</th><th>链接</th></tr>';
  h+='<tr><td>🌊 华藏世界海·3D动画</td><td>B站</td><td><a href=https://www.bilibili.com/search?keyword=%E5%8D%8E%E4%B8%A5%E7%BB%8F+%E5%8D%8E%E8%97%8F%E4%B8%96%E7%95%8C+3D target=_blank>搜索</a></td></tr>';
  h+='<tr><td>🏛 東大寺大佛·4K</td><td>YouTube</td><td><a href=https://www.youtube.com/results?search_query=%E6%9D%B1%E5%A4%A7%E5%AF%BA+%E5%A4%A7%E4%BD%9B+4K target=_blank>搜索</a></td></tr>';
  h+='<tr><td>🏺 犍陀罗佛像艺术</td><td>B站</td><td><a href=https://www.bilibili.com/search?keyword=%E7%8A%8D%E9%99%80%E7%BD%97+%E4%BD%9B%E5%83%8F+%E8%AE%B0%E5%BD%95%E7%89%87 target=_blank>搜索</a></td></tr>';
  h+='<tr><td>🖼 敦煌·华严经变</td><td>B站</td><td><a href=https://www.bilibili.com/search?keyword=%E6%95%A6%E7%85%8C+%E5%8D%8E%E4%B8%A5%E7%BB%8F%E5%8F%98 target=_blank>搜索</a></td></tr>';
  h+='<tr><td>🎨 正仓院·唐代宝物</td><td>YouTube</td><td><a href=https://www.youtube.com/results?search_query=%E6%AD%A3%E5%80%89%E9%99%A2+%E5%AE%9D%E7%89%A9 target=_blank>搜索</a></td></tr></table>';
  h+="</div></div>";

  h+="<div class=wu-door onclick='this.classList.toggle(\"open\")'><span class=arrow>▶</span><span class=ttl>📚 专题参考书目(6部+IDP数据库)</span><div class=body>";
  h+='<p style=font-size:0.7em;color:var(--text2);line-height:1.8>📖 《大美之佛像:犍陀罗艺术》(栗田功·文物出版社 2017)<br>📖 《敦煌石窟全集 第22册·石窟建筑卷》<br>📖 《伯希和敦煌图录》(法·伯希和 1908)<br>📖 《伟大的博物馆:新德里国家博物馆中的敦煌艺术》(罗凯什·钱德拉 2024)<br>📖 《敦煌画研究》(法·吉埃 著)<br>📖 《图解华严经:读懂经中之王》(龙树菩萨释著)<br>🌐 国际敦煌项目 IDP: <a href=http://idp.bl.uk target=_blank>idp.bl.uk</a>（吉美/大英/新德里所有敦煌藏品在线数据库）</p>';
  h+="</div></div>";
  h+='</div>';
  cv.innerHTML=h;
  var c=document.getElementById("cosmo-canvas");if(!c)return;
  c.addEventListener('wheel',function(e){e.preventDefault();COSMO.scale*=e.deltaY<0?1.12:0.89;COSMO.scale=Math.max(0.4,Math.min(3,COSMO.scale));drawCosmo();});
  c.addEventListener('click',clickCosmo);
  drawCosmo();
  drawTower();
}

var _size=550,_minR=0,_layerH=0;
function drawCosmo(){
  var c=document.getElementById("cosmo-canvas");if(!c)return;
  _size=Math.min(550,c.parentElement.clientWidth-30);
  c.width=_size;c.height=_size;c.style.width=_size+'px';c.style.height=_size+'px';
  var ctx=c.getContext("2d"),cx=_size/2,cy=_size/2;
  ctx.clearRect(0,0,_size,_size);
  var bg=ctx.createRadialGradient(cx,cy,0,cx,cy,_size/2);
  bg.addColorStop(0,'#fefdf9');bg.addColorStop(1,'#e0d8c8');
  ctx.fillStyle=bg;ctx.fillRect(0,0,_size,_size);
  var maxR=_size*0.44*COSMO.scale; _minR=_size*0.04*COSMO.scale; _layerH=(maxR-_minR)/20;
  // Wind-wheels
  for(var i=0;i<10;i++){ctx.beginPath();ctx.arc(cx,cy,maxR+5+i*4*COSMO.scale,-0.8*Math.PI,0.8*Math.PI);ctx.strokeStyle='rgba(94,139,158,'+(0.06+i*0.01)+')';ctx.lineWidth=0.8;ctx.setLineDash([2,8]);ctx.stroke();ctx.setLineDash([]);}
  if(COSMO.scale>0.6){ctx.fillStyle='#8a7a6a';ctx.font='9px Microsoft YaHei';ctx.fillText('十重风轮',cx+maxR+10,cy);}
  // Ocean
  ctx.beginPath();ctx.arc(cx,cy,maxR,-0.9*Math.PI,-0.1*Math.PI);ctx.lineTo(cx+maxR*0.6,cy+maxR*0.3);ctx.closePath();
  var og=ctx.createLinearGradient(cx,cy-maxR,cx,cy+maxR);og.addColorStop(0,'rgba(94,139,158,0.02)');og.addColorStop(1,'rgba(70,120,150,0.12)');
  ctx.fillStyle=og;ctx.fill();
  if(COSMO.scale>0.6){ctx.fillStyle='#5e8b9e';ctx.font='bold 9px Microsoft YaHei';ctx.fillText('无边妙华光香水海',cx-45,cy+maxR-8);}
  // Light rays
  for(var r2=0;r2<24;r2++){var ra=(r2/24)*Math.PI*2;ctx.beginPath();ctx.moveTo(cx+Math.cos(ra)*_minR*2,cy+Math.sin(ra)*_minR*2);ctx.lineTo(cx+Math.cos(ra)*maxR*0.85,cy+Math.sin(ra)*maxR*0.85);ctx.strokeStyle='rgba(184,134,60,0.05)';ctx.lineWidth=0.5;ctx.stroke();}
  // 20 layers
  for(var i2=0;i2<COSMO_LAYERS.length;i2++){
    var ly=COSMO_LAYERS[i2],r1=_minR+i2*_layerH,r2=r1+_layerH;
    ctx.beginPath();ctx.arc(cx,cy,r2,0,Math.PI*2);ctx.beginPath();ctx.arc(cx,cy,r1,0,Math.PI*2);
    ctx.fillStyle='rgba(184,134,60,'+(ly.saha?0.2:(i2%2?0.04:0.07))+')';ctx.fill('evenodd');
    ctx.beginPath();ctx.arc(cx,cy,r2,0,Math.PI*2);
    ctx.strokeStyle=ly.saha?'#c46b5d':'rgba(184,134,60,'+(i2===0||i2===19?'0.5':'0.25')+')';ctx.lineWidth=ly.saha?2.5:0.6;ctx.stroke();
    var showL=COSMO.scale>0.7||ly.saha||COSMO.all;
    if(showL){var lr=(r1+r2)/2,a2=-Math.PI/2+i2*0.22,lx=cx+Math.cos(a2)*lr,ly2=cy+Math.sin(a2)*lr;ctx.fillStyle=ly.saha?'#c46b5d':'#5c5040';ctx.font=(ly.saha?'bold 10':'9')+'px Microsoft YaHei';ctx.fillText((ly.saha?'★':'')+(COSMO.all?(i2+1)+'.':'')+ly.n,lx+4,ly2+3);if(COSMO.scale>0.9||ly.saha){ctx.fillStyle='#8a7a6a';ctx.font='8px Microsoft YaHei';ctx.fillText(ly.b,lx+4,ly2+14);}}
  }
  // Indra's Net
  if(COSMO.net){var sel=COSMO.sel||COSMO_LAYERS[12],si=COSMO_LAYERS.indexOf(sel),sr=_minR+si*_layerH+_layerH/2;
    for(var i3=0;i3<COSMO_LAYERS.length;i3++){if(i3===si)continue;var tr=_minR+i3*_layerH+_layerH/2,a3=i3*Math.PI*2/20;
    ctx.beginPath();ctx.moveTo(cx+Math.cos(a3)*sr,cy+Math.sin(a3)*sr);ctx.lineTo(cx+Math.cos(a3+0.15)*tr,cy+Math.sin(a3+0.15)*tr);
    ctx.strokeStyle='rgba(125,154,110,0.12)';ctx.lineWidth=0.5;ctx.stroke();}}
  // Center Vairocana
  var hg=ctx.createRadialGradient(cx,cy,_minR*0.3,cx,cy,_minR*2.5);hg.addColorStop(0,'rgba(255,220,150,0.7)');hg.addColorStop(0.3,'rgba(184,134,60,0.3)');hg.addColorStop(1,'rgba(184,134,60,0)');
  ctx.fillStyle=hg;ctx.beginPath();ctx.arc(cx,cy,_minR*2.5,0,Math.PI*2);ctx.fill();
  ctx.fillStyle='#b8863c';ctx.font='bold '+(16*COSMO.scale)+'px Microsoft YaHei';ctx.fillText('卍',cx-8,cy+4);
  ctx.fillStyle='#8a6040';ctx.font='bold 11px Microsoft YaHei';ctx.fillText('毗卢遮那佛',cx-30,cy-_minR*1.8);
  ctx.fillText('(Vairocana)',cx-28,cy-_minR*1.8+14);
  if(_layerH>0){var sR=_minR+12*_layerH+_layerH/2;ctx.fillStyle='#c46b5d';ctx.font='bold 9px Microsoft YaHei';ctx.fillText('▼ 娑婆(第13层)',cx-48,cy-sR-3);}
}

function clickCosmo(e){
  var c=document.getElementById("cosmo-canvas");if(!c||!_layerH)return;
  var r=c.getBoundingClientRect(),mx=e.clientX-r.left,my=e.clientY-r.top;
  var d=Math.sqrt((mx-c.width/2)*(mx-c.width/2)+(my-c.height/2)*(my-c.height/2));
  for(var i=0;i<COSMO_LAYERS.length;i++){
    var r1=_minR+i*_layerH,r2=r1+_layerH;
    if(d>=r1&&d<=r2){COSMO.sel=COSMO_LAYERS[i];showCosmoInfo(COSMO_LAYERS[i],i);drawCosmo();return;}
  }
  if(d<_minR*2){COSMO.sel=null;var inf=document.getElementById('cosmo-info');if(inf){inf.style.display='block';inf.innerHTML='<h3 style=color:var(--gold)>卍 毗卢遮那佛</h3><p>华严经根本教主。梵名Vairocana,意译<b>光明遍照</b>。法身遍一切处,为华藏世界海之本体。</p><p style=font-size:0.72em;color:var(--text2)>「佛身充满于法界,普现一切众生前;随缘赴感靡不周,而恒处此菩提座。」</p>';}drawCosmo();}
}
// ═══ 三界诸天·修行对应图(海云法师体系) ═══
function drawTower(){
  var c2=document.getElementById("cosmo-tower");if(!c2)return;
  var W=Math.min(900,c2.parentElement.clientWidth-30);var H=Math.max(560,W*0.9);
  c2.width=W;c2.height=H;c2.style.width=W+'px';c2.style.height=H+'px';
  var ctx=c2.getContext("2d");
  ctx.fillStyle='#fdfaf3';ctx.fillRect(0,0,W,H);

  // ── Layout columns ──
  var colX={practice:10,heaven:140,bar:280,stage:560,method:680};
  var colW={practice:120,heaven:40,bar:260,stage:120,method:180};
  var top=40,bot=30,avail=H-top-bot;

  var data=[
    {n:'非想非非想处天',tp:'无色界',tc:'#8b7a9e',c:'rgba(180,170,210,0.12)',
     prac:'妙行·圆融道',xin:'入法界',ding:'狮子频申三昧(华严大定)'},
    {n:'无所有处天',tp:'无色界',tc:'#8b7a9e',c:'rgba(180,170,210,0.08)',ding:'狮子奋迅三昧'},
    {n:'识无边处天',tp:'无色界',tc:'#8b7a9e',c:'rgba(180,170,210,0.08)',xin:'照见·能所双泯',ding:'超越三昧'},
    {n:'空无边处天',tp:'无色界',tc:'#8b7a9e',c:'rgba(180,170,210,0.08)',xin:'十信圆满(照见五蕴空)',ding:'九次第定(灭尽定)'},
    {n:'色究竟天',tp:'色界',tc:'#5e8b9e',c:'rgba(150,180,200,0.12)',
     prac:'正行·等持工程(界外定)',xin:'九信·我执法执双破',ding:'四禅(舍念清净)'},
    {n:'善现·善见·无热·无烦天',tp:'色界',tc:'#5e8b9e',c:'rgba(150,180,200,0.10)',xin:'八信·发心破法执'},
    {n:'无云·福生·广果天',tp:'色界',tc:'#5e8b9e',c:'rgba(150,180,200,0.09)',xin:'七信·四果(破我执)',ding:'四禅'},
    {n:'少净·无量净·遍净天',tp:'色界',tc:'#5e8b9e',c:'rgba(160,190,210,0.09)',xin:'六信·四果向',ding:'三禅'},
    {n:'少光·无量光·光音天',tp:'色界',tc:'#5e8b9e',c:'rgba(170,200,220,0.09)',xin:'五信·三果',ding:'二禅'},
    {n:'梵众·梵辅·大梵天',tp:'色界',tc:'#5e8b9e',c:'rgba(180,210,230,0.09)',xin:'三信·运用观照技术',ding:'初禅'},
    {n:'他化自在天',tp:'欲界',tc:'#c46b5d',c:'rgba(210,160,140,0.12)',
     prac:'正授行法·第3~5次灌顶',xin:'二信·确认菩提心',ding:'未到定'},
    {n:'化乐天',tp:'欲界',tc:'#c46b5d',c:'rgba(210,160,140,0.10)'},
    {n:'兜率天',tp:'欲界',tc:'#c46b5d',c:'rgba(210,160,140,0.10)',ding:'弥勒菩萨内院'},
    {n:'夜摩天',tp:'欲界',tc:'#c46b5d',c:'rgba(210,160,140,0.10)'},
    {n:'忉利天(三十三天)',tp:'欲界',tc:'#c46b5d',c:'rgba(200,155,135,0.12)',
     prac:'第一次灌顶·忍可灌顶',xin:'初信·舍识用根',ding:'忉利定/妙高定'},
    {n:'四天王天',tp:'欲界',tc:'#c46b5d',c:'rgba(200,155,135,0.10)',xin:'煖法·顶法·忍法',ding:'四天王定'},
    {n:'人间(南赡部洲)',tp:'人间',tc:'#b8863c',c:'rgba(184,134,60,0.18)',
     prac:'前行·内摄工程(界内定)',xin:'资粮道·发心工程',ding:'欲界定·安般守意'},
    {n:'畜生·饿鬼·地狱',tp:'恶道',tc:'#8a7060',c:'rgba(140,120,100,0.10)',prac:'五科·人格养成(70分以上)',ding:'起点·凡夫位'}
  ];

  // ── Column headers ──
  ctx.fillStyle='#b8863c';ctx.font='bold 12px Microsoft YaHei';
  ctx.fillText('修行次第(海云法师体系)',colX.practice,top-12);
  ctx.fillText('二十八天',colX.heaven,top-12);
  ctx.fillText('十信位·果位',colX.stage,top-12);
  ctx.fillText('禅定进路',colX.method,top-12);

  // ── Bars ──
  var barH=(avail/data.length)*0.72,gap=(avail/data.length)*0.28;
  for(var i=0;i<data.length;i++){
    var d=data[i],y=top+i*(avail/data.length);
    // Practice column
    if(d.prac){ctx.fillStyle=d.tc;ctx.font='bold 9px Microsoft YaHei';ctx.fillText(d.prac,colX.practice,y+barH/2+3);ctx.strokeStyle=d.tc+'40';ctx.lineWidth=0.5;ctx.setLineDash([2,4]);ctx.beginPath();ctx.moveTo(colX.practice+colW.practice,y+barH/2);ctx.lineTo(colX.heaven,y+barH/2);ctx.stroke();ctx.setLineDash([]);}
    // Heaven bar
    ctx.fillStyle=d.c;ctx.fillRect(colX.bar-60,y,60,barH);
    ctx.strokeStyle=d.tc;ctx.lineWidth=1;ctx.strokeRect(colX.bar-60,y,60,barH);
    ctx.fillStyle=d.tc;ctx.font='9px Microsoft YaHei';ctx.fillText(d.n,colX.bar-56,y+barH/2+3);
    // // Heaven type label
    ctx.fillStyle=d.tc+'80';ctx.font='8px Microsoft YaHei';ctx.fillText(d.tp,colX.heaven,y+barH/2+3);
    // Stage (xin)
    if(d.xin){ctx.fillStyle='#5c5040';ctx.font='8px Microsoft YaHei';ctx.fillText(d.xin,colX.stage,y+barH/2+3);}
    // Method (ding)
    if(d.ding){ctx.fillStyle='#8a7a6a';ctx.font='8px Microsoft YaHei';ctx.fillText(d.ding,colX.method,y+barH/2+3);}
  }

  // ── Legend at bottom ──
  var lx=8,ly=H-18;
  [{n:'无色界(妙行)',c:'#8b7a9e'},{n:'色界(正行)',c:'#5e8b9e'},{n:'欲界(前行)',c:'#c46b5d'},{n:'人间·恶道',c:'#b8863c'}].forEach(function(lg){
    ctx.fillStyle=lg.c;ctx.fillRect(lx,ly-8,10,10);
    ctx.fillStyle='#5c5040';ctx.font='9px Microsoft YaHei';ctx.fillText(lg.n,lx+12,ly+1);
    lx+=ctx.measureText(lg.n).width+20;
  });
  ctx.fillStyle='#a09080';ctx.font='8px Microsoft YaHei';ctx.fillText('源: 大华严寺官网·华严禅观全程一览表 + 海云继梦《四十华严讲记》',lx+10,ly+1);
}

function showCosmoInfo(ly,i){
  var inf=document.getElementById('cosmo-info');if(!inf)return;
  inf.style.display='block';
  inf.innerHTML='<h3 style=color:var(--gold)>🪷 '+ly.n+' <span style=font-size:0.65em>第'+(i+1)+'重</span></h3>'
    +'<p>🙏 <b>住佛</b>: '+ly.b+'</p>'
    +(ly.saha?'<p style=color:#c46b5d>★ <b>娑婆世界</b>——我们所居之三千大千世界。释迦牟尼佛于此示现成道,毗卢遮那佛为此世界之法身本源。</p>':'')
    +"<p style=font-size:0.72em;color:var(--text2)>「一一世界海中,各有不可说佛刹微尘数世界围绕;一一微尘中,悉见一切世界;重重无尽,如因陀罗网。」—— 《华严经·华藏世界品》</p>"
}
