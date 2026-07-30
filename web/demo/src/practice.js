// ═══ PRACTICE TAB ═══
function renderPractice(){
  var pv=document.getElementById("practice-view");if(!pv)return;
  var h="";
  h+="<style>.wu-door{cursor:pointer;padding:10px 14px;margin:4px 0;background:var(--card);border:1px solid var(--line);border-radius:8px;transition:all 0.2s}.wu-door:hover{border-color:var(--gold-l)}.wu-door .arrow{display:inline-block;transition:transform 0.2s;margin-right:6px}.wu-door.open .arrow{transform:rotate(90deg)}.wu-door .body{display:none;margin-top:8px;padding-top:8px;border-top:1px solid var(--line);font-size:0.9em;line-height:1.8;color:var(--text2)}.wu-door.open .body{display:block}.wu-door .ttl{font-weight:600;color:var(--gold);font-size:1em}</style>";

  h+="<div class=section><h2 id=p-overview>🧘 华严行法 — 修行蓝图</h2><p style=line-height:1.8>参考大华严寺海云继梦和上所立 <b>普贤乘华严宗</b> 修行体系。以华严禅法为核心，透过<b>心法工程</b>止住安心、令真心起作用。</p>";

  h+="<div style='display:flex;gap:16px;flex-wrap:wrap;justify-content:center;margin:12px 0'>";
  h+="<div style='flex:1;min-width:180px;background:rgba(184,134,60,0.08);border:1px solid #b8863c;border-radius:10px;padding:16px;text-align:center'>";
  h+="<div style='font-size:1.05em;font-weight:700;color:#b8863c;margin-bottom:4px'>资粮道</div>";
  h+="<div style='font-size:0.8em;color:#8a7060'>发心工程</div><div style='font-size:0.7em;color:#a09080;margin-top:4px'>三摩呬多 samāhita</div></div>";
  h+="<div style='display:flex;align-items:center;color:#c0b098;font-size:1.2em'>→</div>";
  h+="<div style='flex:1;min-width:180px;background:rgba(94,139,158,0.08);border:1px solid #5e8b9e;border-radius:10px;padding:16px;text-align:center'>";
  h+="<div style='font-size:1.05em;font-weight:700;color:#5e8b9e;margin-bottom:4px'>前行·正行</div>";
  h+="<div style='font-size:0.8em;color:#6a7060'>内摄·等持</div><div style='font-size:0.7em;color:#a09080;margin-top:4px'>三摩钵底 samāpatti</div></div>";
  h+="<div style='display:flex;align-items:center;color:#c0b098;font-size:1.2em'>→</div>";
  h+="<div style='flex:1;min-width:180px;background:rgba(196,107,93,0.08);border:1px solid #c46b5d;border-radius:10px;padding:16px;text-align:center'>";
  h+="<div style='font-size:1.05em;font-weight:700;color:#c46b5d;margin-bottom:4px'>三摩地</div>";
  h+="<div style='font-size:0.8em;color:#8a6060'>海印三昧</div><div style='font-size:0.7em;color:#a09080;margin-top:4px'>三摩地 samādhi</div></div>";
  h+="</div></div>";

  h+="<div class=section><h2 id=p-stages>📐 修行三阶段</h2>";
  h+="<div class=stage-box><b>一、资粮道 — 发心工程</b><br>三门必修: 人格健康+出离心+菩提心。技术面: 纯化禅(动→静)→象限转移→瞬间定。工程面: 心性培养+戒律基础。</div>";
  h+="<div class=stage-box><b>二、前行 — 内摄工程（界内定）</b><br>核心: 安那般那数息观(数·随·止·观·还·净)。四种观法: 唯心识观→真如实现→毗婆舍那→奢摩他。</div>";
  h+="<div class=stage-box><b>三、正行 — 等持工程（界外定）</b><br>前半程三摩呬多→后半程三摩钵底→究竟三摩地。依杜顺法界三观，透过海印三昧呈现华严境界。</div></div>";

  h+="<div class=section><h2 id=p-method>⚙️ 技术面·工程面 — 双轨详解</h2>";
  h+="<p style=line-height:1.8;margin-bottom:8px>海云法师将华严禅法分为<b>技术面</b>（修定·身法）与<b>工程面</b>（修慧·心法），比喻为「建设部门与工程师」——「没有技术面，工程面推不动；没有工程面，技术面只是空壳」。据《华严禅行法》讲记系列（wuming.xuefo.com / fjdh.cn收录）。</p>";

  h+="<h3 style=color:var(--gold)>🔧 技术面：数·随·止 三法</h3>";
  h+="<table class=v-table><tr><th>法位</th><th>境界</th><th>关键操作</th><th>易犯误区</th></tr>";
  h+="<tr><td><b>数法</b></td><td>粗住→细住→欲界定</td><td>置心风门(鼻孔间)，1数到10，循环往复。克服四种妄想: 心理/物理(酸痛麻痒)/生理(光声香触感)/社会制度妄想</td><td>⚠ 掉入「舒服禅」——打坐舒服但生命枯竭，属枯木禅非真修</td></tr>";
  h+="<tr><td><b>随法</b></td><td>欲界定→未到定</td><td>从注意整个呼吸循环→转向注意「息入尽」与「息出尽」的每一个细节。妄想开始被堵住，暗示作用逐渐消除</td><td>追求境界名相，忽略身心柔和稳定</td></tr>";
  h+="<tr><td><b>止法</b></td><td>置心一处·心一境性</td><td>所有妄想脱落，心境合一。产生八触十功德: 色身八大类变化(欲界→色界细胞)与心理十大类喜悦</td><td>⚠ 证得「止」后若追求神通特异功能→左转入外道禅(四禅八定)；须「右转」向四果成就</td></tr>";
  h+="</table>";

  h+="<h3 style=color:var(--gold)>🧠 工程面：数法中的三阶段心法</h3>";
  h+="<table class=v-table><tr><th>阶段</th><th>功夫</th><th>具体操作</th></tr>";
  h+="<tr><td><b>A阶段</b></td><td>感受息之长短与动静差异</td><td>在坐禅(呼吸细长)与行禅/运动(呼吸粗涩)中，对比感受呼吸长短的差异性。对呼吸的存在产生真切感受。即使运动中也必须保持数息不断</td></tr>";
  h+="<tr><td><b>B阶段</b></td><td>洞悉呼吸之因果与影响力</td><td>明了「呼吸的轨迹」——清楚呼吸的因与果。掌握此即长寿法基础，能自主生死（如虚云老和尚刀棒加身仍能活下）。法师称此为「生命的秘笈」</td></tr>";
  h+="<tr><td><b>C阶段</b></td><td>心王·心所·境界</td><td>A+B阶段完成后，转入「句中玄」正行领域，探讨心王、心所与境界的相互关系。（公开资料中此阶段未完全展开，待后续讲记补足）</td></tr>";
  h+="</table>";

  h+="<h3 style=color:var(--gold)>👁 内摄→内观→禅观 三层功夫</h3>";
  h+="<table class=v-table><tr><th>层位</th><th>定位</th><th>操作要义</th></tr>";
  h+="<tr><td><b>内摄</b></td><td>技术面核心——摄心</td><td>「妄想一起，记得把心抓回来放在风门」。将注意力完全收摄在呼吸上——法师称「心跑掉抓回来是一项大工程」</td></tr>";
  h+="<tr><td><b>内观</b></td><td>工程面核心——观照</td><td>在数·随·止三法中感受法身存在(三法功德)。分三级: ①寂而常照(如宁静湖水·一眼看穿) ②照而常寂(作用中保持宁静) ③寂照双亡(最高·超语言)</td></tr>";
  h+="<tr><td><b>禅观</b></td><td>粗→细→微妙</td><td>粗禅观: 数随止中感受法身。细禅观: 置心一处后。微妙禅观: 十信位圆满后·法身大士境界</td></tr>";
  h+="</table></div>";

  h+="<div class=section><h2 id=p-wujiao>📜 五教止观（杜顺和尚·点击展开）</h2>";
  h+="<div class=wu-door onclick='this.classList.toggle(\"open\")'><span class=arrow>▶</span><span class=ttl>一、法有我无门（小乘教）</span><div class=body>破除「我执」，体悟我空，但法执犹存。一切法因缘和合，因果历然。对应四禅八定中的初、二、三、四禅。</div></div>";
  h+="<div class=wu-door onclick='this.classList.toggle(\"open\")'><span class=arrow>▶</span><span class=ttl>二、生即无生门（大乘始教）</span><div class=body>体悟「法空」——外境皆由阿赖耶识变现，生而无生。达我法二空之境。此门始破「法执」，识心无体，境不自境。</div></div>";
  h+="<div class=wu-door onclick='this.classList.toggle(\"open\")'><span class=arrow>▶</span><span class=ttl>三、事理圆融门（大乘终教）</span><div class=body>空有不二，悲智双运。实现「空有双亡」之境——理（真如）不碍事（万象），事不碍理，理事圆融无碍。</div></div>";
  h+="<div class=wu-door onclick='this.classList.toggle(\"open\")'><span class=arrow>▶</span><span class=ttl>四、语观双绝门（大乘顿教）</span><div class=body>离心行言说之境。言语道断，心行处灭。唯有真如及真如智。言语不能及，观想不能到，唯证相应。</div></div>";
  h+="<div class=wu-door onclick='this.classList.toggle(\"open\")'><span class=arrow>▶</span><span class=ttl>五、华严三昧门（一乘圆教·究竟）</span><div class=body>见法界缘起之相——万象影现，一即一切、圆融无碍。若能当下认证万法从缘，便可顿入法界缘起。此即海印三昧——如大海映现万象，佛心如海，一时普现十方法界无尽缘起。</div></div>";
  h+="</div>";

  h+="<div class=section><h2 id=p-bhumis>📊 十信法门</h2><table class=v-table><tr><th>信位</th><th>禅定</th><th>法位</th><th>观法</th><th>关键检验</th></tr>";
  h+="<tr><td>初信</td><td>四天王定</td><td>煖法</td><td>唯心识观</td><td>自省三业·觉醒生命意义</td></tr>";
  h+="<tr><td>二信</td><td>忉利定</td><td>顶法</td><td>观妄念所由生</td><td>确认菩提心·收心工程完成</td></tr>";
  h+="<tr><td>三信</td><td>欲界定</td><td>忍法</td><td>轻安三相</td><td>菩提心稳定·摄众共修</td></tr>";
  h+="<tr><td>四信</td><td>未到定</td><td>世第一法</td><td>安般守意</td><td>置心风门·心不散乱</td></tr>";
  h+="<tr><td>五~十信</td><td>色界·无色界定</td><td>—</td><td>奢摩他·毗婆舍那</td><td>舍妄念→入界外定</td></tr>";
  h+="</table></div>";

  h+="<div class=section><h2>🎯 三摩呬多·三摩钵底·三摩地</h2><table class=v-table><tr><th>名相</th><th>梵语</th><th>定位</th><th>操作要点</th></tr>";
  h+="<tr><td>三摩呬多</td><td>Samāhita</td><td>入定前·专注调心</td><td>粗住→细住→欲界定。排除妄想执著</td></tr>";
  h+="<tr><td>三摩钵底</td><td>Samāpatti</td><td>以观导定·定慧双运</td><td>勘定三界定。须善知识勘定</td></tr>";
  h+="<tr><td>三摩地</td><td>Samādhi</td><td>究竟·心一境性</td><td>出入自在。破法执我执</td></tr>";
  h+="</table><p style='font-size:0.75em;color:var(--text2);margin-top:6px'>⚠ 术语说明: 据主流汉传辞书(如《瑜伽师地论》注疏)，「三摩地」(samādhi)标准译语为「等持」，「三摩钵底」(samāpatti)标准译语为「等至」。大华严寺官方资料中的配对与此恰好相反——此系道场自身的术语使用习惯，本文如实呈现，读者可自行留意。</p></div>";

  h+="<div class=section><h2>📚 华严六科</h2><table class=v-table><tr><th>科目</th><th>内容</th></tr>";
  h+="<tr><td>华严学概论</td><td>华严经结构·五教十宗·法界缘起</td></tr>";
  h+="<tr><td>华严经教行法</td><td>经文解读·修行法门·善财五十三参</td></tr>";
  h+="<tr><td>华严禅行法</td><td>安般守意·置心一处·三摩地次第</td></tr>";
  h+="<tr><td>华严戒律观</td><td>菩萨戒·梵网经·现代持戒</td></tr>";
  h+="<tr><td>华严净土法门</td><td>华藏世界·毗卢遮那净土</td></tr>";
  h+="<tr><td>华严密法</td><td>华严字母·曼荼罗·真言持诵</td></tr>";
  h+="</table></div>";

  h+="<div class=section><h2 id=p-fourstage>🪜 四阶段修行蓝图（海云法师判摄）</h2>";
  h+="<div class=stage-box><b>一、出离乘</b>（出离心→出离道→出离行）<br>以脱离轮回、了生死为基础动机，建立「出三界、入法界」之志。</div>";
  h+="<div class=stage-box><b>二、菩提乘</b>（菩提心→菩提道→菩提行）<br>发心求觉悟。法师称此「只是起步」。</div>";
  h+="<div class=stage-box><b>三、菩萨乘</b>（菩萨心→菩萨道→菩萨行）<br>法师称此「还没有究竟」——仍属因地修行。</div>";
  h+="<div class=stage-box><b>四、普贤乘</b>（普贤心→普贤行→普贤道）<br><b style=color:var(--gold)>究竟归趣。</b>法师称「究竟要到普贤乘来」——此即「普贤乘华严宗」名称的义理出处。整套蓝图涵盖从初信到十信、从资粮道到正行、从初果到法身大士的完整阶次。</div></div>";

  h+="<div class=section><h2>🙏 三缘念 — 修行归依</h2>";
  h+="<p style=line-height:1.8>海云法师在传统「皈依三宝」之外，提出更具操作性的归依框架（据大华严寺官方资料）：<br>";
  h+="<b>① 缘念道场</b> — 缘念僧团，以道场为修行依止处；<br>";
  h+="<b>② 缘念善知识</b> — 缘念具体指导的师长，接受僧团制度性指导；<br>";
  h+="<b>③ 缘念法门</b> — 缘念自己实际修学的具体法门，不杂修不盲从。<br>";
  h+="<span style=font-size:0.8em;color:var(--text2)>注: 「忍可灌顶→行者灌顶→进阶灌顶→高阶保衽灌顶」四次第灌顶制度及「两百余种具体测验」的验证机制，据法师《四十华严讲记》所述，属其体系内部的制度性安排。</span></p></div>";

  h+="<div class=section><h2 id=p-works>📖 海云继梦著作（空庭书苑/光潽文创出版·2002-2026）</h2><p style=font-size:0.8em;line-height:1.9>";
  h+="<b>华严经讲记系列:</b> 《华严经导读》(三册) · 《探玄记悬谈讲记》(四册) · 《华严学导论》(ⅠⅡ) · 《世主妙严品》《光明觉品》《净行品》《贤首品》《明法品》《普贤三昧品》《普贤行品》《四圣谛品》讲记 · 《四十华严》全本讲记(2006-2010北京广化寺)<br>";
  h+="<b>三部曲:</b> 《非常坛经》(4册·2004) · 《非常金刚经》 · 《非常心经》——主张「要懂《心经》先懂《金刚经》，要懂《金刚经》先懂《坛经》」<br>";
  h+="<b>禅修系列:</b> 《禅修入门》(2020) · 《禅修正行——安那般那数息观》(2017) · 《禅修前行》 · 《禅观概论》(2011) · 《禅，怎么参？》(2011) · 《禅，就要这么参！》(2011)<br>";
  h+="<b>解密系列:</b> 《根本佛母——准提密法》(2020再版) · 《神圣的游戏场——华严密法》 · 《生命密境——曼荼罗的世界》 · 《深深密——密行指引》 · 《悠活三昧》<br>";
  h+="<b>地藏/药师系列:</b> 《开启灵性的钥匙》(上下·2018) · 《就从这里入法界——地藏菩萨行法》(2011) · 《转吧！地藏象限》(2018) · 《叩问药师佛的法界密码》(2018) · 《成佛方程式——药师经讲记》(2018)<br>";
  h+="<b>净土/行愿系列:</b> 《从极乐世界迈向永恒的生命——解弥陀经》(2011) · 《普贤十大愿王行法精要》(2011) · 《十大愿王修行法要》<br>";
  h+="<b>生活应用:</b> 《认真最幸福》(2005) · 《看见幸福》(2006) · 《幸福就这样》(2006) · 《生命故乡的呼唤01——让心活起来》(2019) · 《幸福冏小孩》(2014) · 《我们只有一个选择》(2010)<br>";
  h+="<b>最新出版(2025-2026):</b> 《华严经在说什么——九九华严玄谈01·02》(2026) · 《在妄念中觉醒——普贤心经讲记》(2025) · 《摆脱焦虑与杂念的三十七个秘诀》(2025)<br>";
  h+="<b>英文著作:</b> <i>Huayen World: Teachings and Meditation Methods in Mahayana Buddhism</i> (Kongting Shuyuan, 2005) — 据查证为目前唯一确认出版的英文著作。「The Dawn of Enlightenment」是否存在独立英译本，尚待进一步查证。<br>";
  h+="<b>出版方:</b> 繁体版由空庭书苑/光潽文创出版(博客来·FindBook·乐天KOBO可购)；简体版曾由九州出版社(2011)、宗教文化出版社(2005)、海南出版社(2016)等在中国大陆发行。</p></div>";

  h+="<div class=section><h2 id=p-timeline>📅 工程面·技术面 演进脉络 & 时间线</h2>";
  h+="<table class=v-table><tr><th>时期</th><th>关键节点</th><th>体系特征</th></tr>";
  h+="<tr><td><b>1981-1991</b></td><td>在家讲经探索期</td><td>以现代语言诠释华严·业余讲经·无僧团建制</td></tr>";
  h+="<tr><td><b>1991</b></td><td>梦参老和尚剃度</td><td>临济宗第47代·确立僧团身份·正式出家弘法</td></tr>";
  h+="<tr><td><b>2004-2010</b></td><td>西安/北京系统弘法</td><td>陕师大华严研究所·社科院演讲·北京广化寺《四十华严》全本讲解</td></tr>";
  h+="<tr><td><b>2008</b></td><td>三脉汇流</td><td>钦因传华严衣钵(贤首42世)+印度胜师子王菩萨传瑜伽行法<br>提出「普贤乘华严宗」·工程面/技术面双轨教学确立</td></tr>";
  h+="<tr><td><b>2011-2013</b></td><td>密集出版·框架定型</td><td>华严六科·五大行法·三部曲·禅观体系完整出版</td></tr>";
  h+="<tr><td><b>2014-2019</b></td><td>讲经扩展·制度细化</td><td>药师/地藏/各品讲记密集出版·忍可灌顶制度·华严专宗学院</td></tr>";
  h+="<tr><td><b>2020-2023</b></td><td>数位化转型</td><td>线上讲经·电子书出版·国立台北大学杰出校友(2023)</td></tr>";
  h+="<tr><td><b>2024-2026</b></td><td>第四期佛教·AI时代</td><td>九九华严五年讲座(TICC)·支提山大华严寺动土(2026.7)·台北大学合作</td></tr>";
  h+="</table></div>";

  h+="<div class=section><h2>📡 海云继梦全网讲法总目</h2>";
  h+="<table class=v-table><tr><th>平台</th><th>内容</th><th>规模</th><th>类型</th></tr>";
  h+="<tr><td><b>Bilibili</b></td><td>华严六科(42h)·善财五十三参·禅法开示</td><td>500+视频</td><td>📺视频</td></tr>";
  h+="<tr><td><b>Apple Podcast</b></td><td>普贤乘华严宗: 20+系列(华严学概论·禅行法·密法·净土)</td><td>2000+集</td><td>🎧音频</td></tr>";
  h+="<tr><td><b>Spotify</b></td><td>普贤乘华严宗(每周一/三更新)</td><td>2000+集</td><td>🎧音频</td></tr>";
  h+="<tr><td><b>YouTube</b></td><td>大华严寺官方频道·讲经合集</td><td>300+视频</td><td>📺视频</td></tr>";
  h+="<tr><td><b>抖音</b></td><td>#海云继梦导师 每日法语</td><td>1000+短片</td><td>📱短视频</td></tr>";
  h+="<tr><td><b>fjdh.cn</b></td><td>华严六科·禅修正行·禅观·讲记逐字稿</td><td>50+文稿</td><td>📝文字</td></tr>";
  h+="<tr><td><b>学佛网</b></td><td>华严禅行法·福慧滋长·修行问答</td><td>100+文稿</td><td>📝文字</td></tr>";
  h+="<tr><td><b>大华严寺</b></td><td>修行蓝图·法脉传承·最新动态</td><td>50+页面</td><td>🌐网页</td></tr>";
  h+="</table></div>";

  h+="<div class=section><h2 id=p-resources>🎬 讲法资源</h2>";

  // YouTube card
  h+="<div style='display:flex;gap:12px;flex-wrap:wrap;margin-bottom:12px'>";
  h+="<div style='flex:1;min-width:250px;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px'>";
  h+="<div style='font-weight:600;color:#c46b5d;margin-bottom:6px'>▶ YouTube · 大華嚴寺官方頻道</div>";
  h+="<p style=font-size:0.8em;color:var(--text2);line-height:1.6>海云继梦导师讲经全集。华严经/禅修/密法/药师经/地藏经等系列讲法。<br>";
  h+="🔗 <a href='https://www.youtube.com/results?search_query=%E5%A4%A7%E8%8F%AF%E5%9A%B4%E5%AF%BA+%E6%B5%B7%E9%9B%B2%E7%B9%BC%E5%A4%A2' target=_blank>在YouTube中搜索</a></p></div>";

  // Bilibili card
  h+="<div style='flex:1;min-width:250px;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px'>";
  h+="<div style='font-weight:600;color:#5e8b9e;margin-bottom:6px'>📺 Bilibili · 海雲繼夢講經全集</div>";
  h+="<p style=font-size:0.8em;color:var(--text2);line-height:1.6>《华严六科》42小时完整版·善财童子五十三参·禅法开示等。<br>";
  h+="🔗 <a href='https://search.bilibili.com/all?keyword=%E6%B5%B7%E4%BA%91%E7%BB%A7%E6%A2%A6' target=_blank>在Bilibili中搜索</a></p></div>";
  h+="</div>";

  // Audio/Web
  h+="<p style=line-height:1.8;margin-top:8px>";
  h+="🎙 <a href='https://podcasts.apple.com/au/podcast/%E6%99%AE%E8%B3%A2%E4%B9%98%E8%8F%AF%E5%9A%B4%E5%AE%97/id1523368889' target=_blank>Apple Podcast</a> · ";
  h+="<a href='https://open.spotify.com/show/2ZDlq4cOOiynQvlzPARkmc' target=_blank>Spotify</a> (20+系列·每周更新) | ";
  h+="🌐 <a href='https://www.huayenworld.org/' target=_blank>大华严寺官网</a> · ";
  h+="<a href='https://www.huayenworld.org/%e8%8f%af%e5%9a%b4%e7%a6%aa%e7%b0%a1%e4%bb%8b%e7%89%b9%e8%89%b2/' target=_blank>修行蓝图全文</a>";
  h+="</p></div>";

  h+="<div class=section><h2>🏛 相关道场</h2><p style=line-height:1.8>";
  h+="📍 <b>南投大华严寺</b> — 海云继梦导师·普贤乘根本道场<br>";
  h+="📍 <b>台北福慧寺</b> — 钦因长老·高原法系<br>";
  h+="📍 <b>台北华严莲社</b> — 贤度法师·华严专宗学院</p></div>";

  pv.innerHTML=h;
}
