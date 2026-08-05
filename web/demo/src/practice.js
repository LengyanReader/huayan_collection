// ═══ PRACTICE TAB ═══
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
  h+="<div id=pv-system class=pv-section style=display:block>";

  // ── 子目录导航 ──
  h+="<div style='display:flex;gap:6px;flex-wrap:wrap;margin-bottom:12px;padding:8px 10px;background:var(--panel);border:1px solid var(--line);border-radius:8px;font-size:0.75em'><b style=color:var(--gold)>📐 修行体系:</b>"
    +"<a href='#sys-stages' style=color:var(--blue)>三阶段</a>·<a href='#sys-blueprint' style=color:var(--blue)>四阶段蓝图</a>·<a href='#sys-six' style=color:var(--blue)>六科五大行法</a>·<a href='#sys-lineages' style=color:var(--blue)>法脉分工</a>·<a href='#sys-projects' style=color:var(--blue)>四大工程</a>·<a href='#sys-cognition' style=color:var(--blue)>识根智</a>·<a href='#sys-refuge' style=color:var(--blue)>三缘念</a>·<a href='#sys-evolution' style=color:var(--blue)>演进脉络</a></div>";

  // ── Header ──
  h+="<div class=section style=border-left:4px solid var(--gold)><h2>🧘 华严行法 — 普贤乘修行体系</h2>";
  h+="<p style=line-height:1.8>参考大华严寺海云继梦和上所立 <b>普贤乘华严宗</b> 修行体系。以华严禅法为核心，透过<b>心法工程</b>止住安心、令真心起作用。体系涵盖从资粮道到正行、从初信到法身大士的完整修行次第。</p></div>";

  // ── 三阶段卡片 ──
  h+="<div style='display:flex;gap:16px;flex-wrap:wrap;justify-content:center;margin:12px 0'>";
  h+="<div style='flex:1;min-width:180px;background:rgba(184,134,60,0.08);border:1px solid #b8863c;border-radius:10px;padding:16px;text-align:center'>";
  h+="<div style='font-size:1.05em;font-weight:700;color:#b8863c;margin-bottom:4px'>禅修入门</div>";
  h+="<div style='font-size:0.8em;color:#8a7060'>发心工程（资粮道）</div><div style='font-size:0.7em;color:#a09080;margin-top:4px'>五科：戒·律·调身·调息·调心</div></div>";
  h+="<div style='display:flex;align-items:center;color:#c0b098;font-size:1.2em'>→</div>";
  h+="<div style='flex:1;min-width:180px;background:rgba(94,139,158,0.08);border:1px solid #5e8b9e;border-radius:10px;padding:16px;text-align:center'>";
  h+="<div style='font-size:1.05em;font-weight:700;color:#5e8b9e;margin-bottom:4px'>禅修前行</div>";
  h+="<div style='font-size:0.8em;color:#6a7060'>内摄工程</div><div style='font-size:0.7em;color:#a09080;margin-top:4px'>安般守意·四种观法</div></div>";
  h+="<div style='display:flex;align-items:center;color:#c0b098;font-size:1.2em'>→</div>";
  h+="<div style='flex:1;min-width:180px;background:rgba(196,107,93,0.08);border:1px solid #c46b5d;border-radius:10px;padding:16px;text-align:center'>";
  h+="<div style='font-size:1.05em;font-weight:700;color:#c46b5d;margin-bottom:4px'>禅修正行</div>";
  h+="<div style='font-size:0.8em;color:#8a6060'>等持工程（内观）</div><div style='font-size:0.7em;color:#a09080;margin-top:4px'>三摩呬多→三摩钵底→三摩地</div></div>";
  h+="</div>";

  // ── 修行三阶段 ──
  h+="<div class=section id=sys-stages><h2>📐 修行三阶段（据大华严寺官网「修行蓝图」2025.11）</h2>";
  h+="<div class=stage-box><b>一、禅修入门 — 发心工程（资粮道）</b><br>三门必修: 人格健康+出离心+菩提心。含<b>五科</b>（戒·律·调身·调息·调心）。技术面: 纯化禅(动→静)→象限转移→瞬间定。工程面: 心性培养+戒律基础。官网: 「发心——出三界、入法界之志,建立信根与定位。」</div>";
  h+="<div class=stage-box><b>二、禅修前行 — 内摄工程</b><br>核心: 安那般那数息观(数.随.止)。官网: 「调息安稳,气息有序;守意——令心不外驰,身息心三者逐步协同。」观法次第: <b>驻佇心观</b>(停心前行)-><b>唯心识观</b>(钝根先修.毗钵舍那)-><b>真如实观</b>(利根直修.奢摩他)-><b>毗婆舍那</b>-><b>奢摩他</b>。详见「📐 禅观法要」子页。</div>";
  h+="<div class=stage-box><b>三、禅修正行 — 等持工程（内观）</b><br>前半程三摩呬多→后半程三摩钵底→究竟三摩地。官网: 「以观导定、以定成观,当下验果,不逐境界名相而重身心之柔和、稳定、清明。」课程配比: <b>70%修行面 + 30%健康面</b>。延伸: 一日禅·二日禅·忍可禅七。</div></div>";

  // ── 四阶段修行蓝图 ──
  h+="<div class=section id=sys-blueprint><h2>🪜 四阶段修行蓝图（海云法师判摄）</h2>";
  h+="<p style=font-size:0.8em;color:var(--text2);margin-bottom:8px>据海云法师《四十华严讲记》第四卷第67讲及大华严寺官网「修行蓝图」页面。整套蓝图涵盖从信众到证量的完整阶次。</p>";
  h+="<div class=stage-box><b>一、出离乘</b>（出离心→出离道→出离行）<br>以脱离轮回、了生死为基础动机，建立「出三界、入法界」之志。</div>";
  h+="<div class=stage-box><b>二、菩提乘</b>（菩提心→菩提道→菩提行）<br>发心求觉悟。法师称此「只是起步」。</div>";
  h+="<div class=stage-box><b>三、菩萨乘</b>（菩萨心→菩萨道→菩萨行）<br>法师称此「还没有究竟」——仍属因地修行。</div>";
  h+="<div class=stage-box><b>四、普贤乘</b>（普贤心→普贤行→普贤道）<br><b style=color:var(--gold)>究竟归趣。</b>法师称「究竟要到普贤乘来」——此即「普贤乘华严宗」名称的义理出处。</div></div>";

  // ── 华严六科 + 五大行法 ──
  h+="<div class=section id=sys-six><h2>🎯 华严六科 & 五大行法</h2>";
  h+="<p style=font-size:0.8em;color:var(--text2);margin-bottom:8px>海云法师将传统华严义学重组为可依次修学的课程架构。「五大行法」即六科中除总论外的五项——禅、净、律、密、经教——主张华严宗并非纯粹「解门」而有完整「行门」。</p>";
  h+="<table class=v-table><tr><th>科目</th><th>内容</th></tr>";
  h+="<tr><td>华严学概论</td><td>华严经结构·五教十宗·法界缘起（总纲性导论）</td></tr>";
  h+="<tr><td>华严经教行法</td><td>经文解读·修行法门·善财五十三参（经教门）</td></tr>";
  h+="<tr><td>华严禅行法</td><td>安般守意·置心一处·三摩地次第（禅门）</td></tr>";
  h+="<tr><td>华严戒律观</td><td>菩萨戒·梵网经·现代持戒（律门）</td></tr>";
  h+="<tr><td>华严净土法门</td><td>华藏世界·毗卢遮那净土（净门）</td></tr>";
  h+="<tr><td>华严密法</td><td>华严字母·曼荼罗·真言持诵·秽迹金刚法（密门）</td></tr>";
  h+="</table></div>";

  // ── 三大法脉行法分工 ──
  h+="<div class=section id=sys-lineages><h2>⚡ 三大法脉行法分工</h2>";
  h+="<p style=font-size:0.8em;color:var(--text2);margin-bottom:4px>海云法师对三条汇流法脉在体系中各自的功能分工（据大华严寺官网及讲记）：</p>";
  h+="<div class=stage-box><b>中观论派 →「解」</b><br>义理/空性论证——负责「理解」层面的理论基础。</div>";
  h+="<div class=stage-box><b>华严思想 →「架构」</b><br>提供整体的世界观与义理框架——「事事无碍法界」「法界缘起」等核心世界观。</div>";
  h+="<div class=stage-box><b>瑜伽行派 →「行」</b><br>禅观正行/实修技术来源。源自印度 Maha Yoga 传承（胜师子王菩萨），法师将其等同于「禅宗的禅观正行」。<br><span style=font-size:0.75em;color:var(--text2)>注: 官网将这支传承直接注解为「大乘瑜伽行派／Yogācāra 之行门精义」，读者可留意其中的诠释性跨度。</span></div></div>";

  // ── 四大工程 ──
  h+="<div class=section id=sys-projects><h2>🏗 四大工程</h2><table class=v-table><tr><th>工程</th><th>性质</th></tr>";
  h+="<tr><td><b>结界工程</b></td><td>短期共修——调整身心频率的具体操作</td></tr>";
  h+="<tr><td><b>华藏工程</b></td><td>双重意涵: ①个人前行阶段必修课程（建立语言/思维模式）②跨世代文明教育志业——法师称「华藏工程五百年」</td></tr>";
  h+="<tr><td><b>华严大学</b></td><td>体制化培育弘法与研究人才的当代项目（非月霞法师等创办的历史性华严大学）</td></tr>";
  h+="<tr><td><b>BQ广场</b></td><td>四大工程之一，目前公开资料中未见「BQ」具体所指的清晰界定</td></tr>";
  h+="</table></div>";

  // ── 识·根·智 ──
  h+="<div class=section id=sys-cognition><h2>🔬 识·根·智 — 三层认知转换</h2>";
  h+="<p style=font-size:0.8em;color:var(--text2);margin-bottom:4px>法师自创的认知层次术语，用以区分凡夫、行者、法身大士三个阶段所依靠的不同认知机制：</p>";
  h+="<div class=stage-box><b>识性（凡夫阶段）</b><br>「能」——妄想心。「识性的能绑虚妄的身」——凡夫是「身心混杂」状态。</div>";
  h+="<div class=stage-box><b>根性（初果至四果阶段）</b><br>「所」。此阶段关键操作是<b>「舍识用根」</b>。</div>";
  h+="<div class=stage-box><b>智（十信位圆满之后）</b><br>此后「以智为先导」，不再「以所为先导」。<br><span style=font-size:0.75em;color:var(--text2)>注: 法师坦承这套区分是借助现代汉语语法结构对古典义理的诠释性翻译，非声称唯一表述。</span></div></div>";

  // ── 三缘念 ──
  h+="<div class=section id=sys-refuge><h2>🙏 三缘念 — 修行归依</h2>";
  h+="<p style=line-height:1.8>海云法师在传统「皈依三宝」之外，提出更具操作性的归依框架：<br>";
  h+="<b>① 缘念道场</b> — 缘念僧团，以道场为修行依止处；<br>";
  h+="<b>② 缘念善知识</b> — 缘念具体指导的师长，接受僧团制度性指导；<br>";
  h+="<b>③ 缘念法门</b> — 缘念自己实际修学的具体法门，不杂修不盲从。<br>";
  h+="<span style=font-size:0.78em;color:var(--text2)>修行态度: 法师强调「自顾灵山，不顾名山」「知道不算，做到才算」——真正的修行来自扎实的日常践行。</span></p></div>";

  // ── 最新动态 ──

  // ── 演进脉络 ──
  h+="<div class=section id=sys-evolution><h2>📅 工程面·技术面 演进脉络 & 时间线</h2>";
  h+="<table class=v-table><tr><th>时期</th><th>关键节点</th><th>体系特征</th></tr>";
  h+="<tr><td><b>1981-1991</b></td><td>在家讲经探索期</td><td>以现代语言诠释华严·业余讲经·无僧团建制</td></tr>";
  h+="<tr><td><b>1991.12.22</b></td><td>梦参老和尚剃度(弥陀诞日)</td><td>临济宗第47代·确立僧团身份·正式出家弘法</td></tr>";
  h+="<tr><td><b>2004-2010</b></td><td>西安/北京系统弘法</td><td>陕师大华严研究所·社科院演讲(2005.1)·北京广化寺《四十华严》全本讲解(2006.11-2010.6)</td></tr>";
  h+="<tr><td><b>2008</b></td><td>三脉汇流</td><td>钦因传华严衣钵(贤首42世, 9月10日求法.9月21日传法大典)+印度胜师子王菩萨传瑜伽行法(年底)<br>提出「普贤乘华严宗」·工程面/技术面双轨教学确立</td></tr>";
  h+="<tr><td><b>2011-2013</b></td><td>密集出版·框架定型</td><td>华严六科·五大行法·三部曲·禅观体系完整出版</td></tr>";
  h+="<tr><td><b>2014-2019</b></td><td>讲经扩展·制度细化</td><td>药师/地藏/各品讲记密集出版·忍可灌顶制度·华严专宗学院</td></tr>";
  h+="<tr><td><b>2020-2023</b></td><td>数位化转型</td><td>线上讲经·电子书出版·国立台北大学杰出校友(2023)</td></tr>";
  h+="<tr><td><b>2024-2026</b></td><td>第四期佛教·AI时代</td><td>九九华严五年讲座(TICC)·支提山大华严寺动土(2026.7)·台北大学合作</td></tr>";
  h+="</table></div>";

  h+="</div>"; // close pv-system

  // ═══════════════════════════════════════════
  // SUB-PAGE 2: 禅观法要 (hidden)
  // ═══════════════════════════════════════════
  h+="<div id=pv-meditation class=pv-section style=display:block>";
  h+="<div style='display:flex;gap:6px;flex-wrap:wrap;margin-bottom:12px;padding:8px 10px;background:var(--panel);border:1px solid var(--line);border-radius:8px;font-size:0.75em'><b style=color:var(--gold)>🗺 禅观法要:</b><a href='#med-overview' style=color:var(--blue)>体系总览</a>·<a href='#med-paths' style=color:var(--blue)>次第道与圆融道</a>·<a href='#med-stage1' style=color:var(--blue)>资粮道</a>·<a href='#med-stage2' style=color:var(--blue)>前行</a>·<a href='#med-stage3' style=color:var(--blue)>正行</a>·<a href='#med-classical' style=color:var(--blue)>古典义理地基</a>·<a href='#med-wujiao' style=color:var(--blue)>贤首五教仪</a>·<a href='#med-yicheng' style=color:var(--blue)>一乘不共别圆</a>·<a href='#med-texts' style=color:var(--blue)>典籍阐释</a>·<a href='#med-verify' style=color:var(--blue)>验证机制</a>·<a href='#med-heart' style=color:var(--blue)>实修心要</a></div>";

    // ── 体系总览 ──
  h+="<div class=section id=med-overview style=border-left:4px solid var(--gold)><h2>🗺 华严禅观体系总览</h2>";
  h+="<p style=font-size:.8em;line-height:1.8;margin-bottom:10px>海云继梦和上华严禅观<b>三阶段</b>: <b>资粮道</b>(发心工程.驻佇心观) → <b>前行</b>(界内定.四种观法) → <b>正行</b>(界外定.法界三观)。<b>技术面</b>(修定.身法)与<b>工程面</b>(修慧.心法)始终双轨并行。</p>";
  h+="<table class=v-table style=font-size:.72em;margin-bottom:12px><tr><th>阶段</th><th>定位</th><th>核心工程</th><th>观法</th><th>禅定</th><th>果位</th></tr>";
  h+="<tr><td rowspan=2><b>资粮道</b></td><td>发心工程<br>界外准备</td><td>五科(戒.律.调身.调息.调心)<br>驻佇心观(停心)<br>净化禅->象限转移</td><td>驻佇心观<br>(根本前行)</td><td>瞬定境(妙高定)<br>粗住->细住->欲界定</td><td>三信位前<br>(发心位)</td></tr>";
  h+="<tr><td colspan=2 style=font-size:.68em;color:var(--text2)>制度入门: 前行三年(教材/听经笔记/华藏工程)->禅师团审核->正授行法。三要件各有三。</td><td colspan=2 style=font-size:.68em;color:var(--text2)>课程配比70%修行面+30%健康面。一日禅.二日禅.忍可禅七。</td></tr>";
  h+="<tr><td rowspan=2><b>前行</b></td><td rowspan=2>内摄工程<br><b>界内定</b></td><td rowspan=2>安那般那数息观<br>(数.随.止)<br>安般守意</td><td>数法/随法</td><td>粗住->细住<br>->欲界定->未到定</td><td>二信~四信位</td></tr>";
  h+="<tr><td>止法+四种观法<br>(1)唯心识(初-二信)<br>(2)真如实(二信+)<br>(3)毗婆舍那(中信)<br>(4)奢摩他(后信)</td><td>四天王定->忉利定<br>->空居天定->色界定<br>->无色界定->出界定</td><td>初信~十信位<br><span style=font-size:.65em;color:var(--text2)>初果(初信)->四果(七信)->十信满心</span></td></tr>";
  h+="<tr><td rowspan=2><b>正行</b></td><td rowspan=2>等持工程<br><b>界外定</b></td><td rowspan=2>三摩呬多->三摩钵底<br>->三摩地(海印三昧)</td><td>杜顺法界三观<br>(真空绝相.理事无碍.周遍含容)</td><td>初禅定关口:<br>左转->四禅八定(外道)<br>右转->四果成就(解脱)</td><td>十信满心<br>->初住至七地(37位)</td></tr>";
  h+="<tr><td>四次灌顶<br>(1)忍可(破无明)<br>(2)行者(证初果)<br>(3)进阶(能所合一)<br>(4)高阶(能所双泯)</td><td>界外定.无功用行</td><td>八地至妙觉(5位)<br><b>共42位圆满</b></td></tr></table>";
  h+="<p style=font-size:.7em;color:var(--text2);margin-top:4px>📎 三阶段架构名称据大华严寺官网「修行蓝图: 华严禅观全程」(2025年11月访问)。观法细节(四种观法/界内定界外定/果位对应等)据海云继梦《四十华严讲记》第67讲(2009.2.26)+《海云继梦禅观概论》(2015)+《迈向佛陀的境界》(2011)。凡官网与讲记表述有异处,以官网为框架、讲记为展开。</p>";
  h+="</div>";

  // ── 次第道与圆融道 ──
  h+="<div class=section id=med-paths><h2>🛤 次第道与圆融道 — 两条修行路径</h2>";
  h+="<p style=font-size:.8em;color:var(--text2);margin-bottom:8px>海云和上将修行路径分为两条: <b>次第道</b>(圣解脱道/智德门)与<b>圆融道</b>(普贤道/福德门)。核心差异: 次第道必须证得空性、即身成就; 圆融道<b>不必证空性,凡夫亦可修</b>,具足信根即可,经分段生死至他方净土证无生。法师明确开示:「凡夫行圆融道,就是没有那个充分条件,你没有证得空性。你行圆融道就那么一个条件,要尽形寿行菩萨道,对三宝具足信心。」但凡夫行圆融道须避讳「聚财」与「聚众」,否则在缺乏空性的前提下易入歧途。若避此忌,报尽必生净土。华严禅观三段教学法(前行->正授行法->妙行)中,前两区块属入法界次第道,第三区块「妙行」属已入法界后的圆融道。</p>";

  h+="<table class=v-table style=font-size:.7em;margin-bottom:10px><tr><th style=width:12%>维度</th><th style=width:44%>次第道(入法界次第道)</th><th style=width:44%>圆融道(法界圆融道)</th></tr>";
  h+="<tr><td><b>空性条件</b></td><td>必须证得空性</td><td>不必证空性,以<b>信根具足</b>替代</td></tr>";
  h+="<tr><td><b>生死方式</b></td><td>变易生死,<b>即身成就</b>(依色身)</td><td>分段生死,<b>即生成就</b>(依法身),经他方净土证无生</td></tr>";
  h+="<tr><td><b>实践目标</b></td><td>目的论明显,止观双运.定慧等持</td><td>无明显目的性,重行法过程,以<b>信愿行</b>为归</td></tr>";
  h+="<tr><td><b>核心技术</b></td><td>以「定」为范围,<b>置心一处</b>为归</td><td>以歌咏赞叹诸佛为归,<b>理事合一地置心一处</b></td></tr>";
  h+="<tr><td><b>工程面</b></td><td>以《大经》(华严经)为归</td><td>以<b>十大愿王</b>为依归</td></tr>";
  h+="<tr><td><b>性质</b></td><td>由凡入圣——清除人性杂质恶质,由粗糙转入精微</td><td>由圣入圣——法身本具但迷不晓,藉佛号唱颂内引法身</td></tr></table>";

  h+="<div class=wu-door onclick='this.classList.toggle(\"open\")'><span class=arrow>▶</span><span class=ttl>📐 圆融道三大条件 + 凡夫行圆融道避讳</span><div class=body>";
  h+="<p style=font-size:.75em;line-height:1.8;margin-bottom:4px><b>三大核心条件:</b> (1)对三宝的具足信——信心绝对,毫无折扣,100分 (2)尽形寿奋进于菩萨道——定位明确,一辈子做一件事(事修),从生命尊重与人性关怀出发服务众生 (3)一再的归零功课——每日反复检视自身,遇到挫折压力则拜忏(一百零八拜),将业力寄放在法界。</p>";
  h+="<p style=font-size:.75em;line-height:1.8;margin-bottom:4px><b>凡夫行圆融道的避讳:</b> 必须避讳「聚财」与「聚众」,否则在缺乏空性的前提下易入歧途——善者落人天善道,恶者成魔成精。若避此忌,报尽必生净土。</p>";
  h+="<p style=font-size:.75em;line-height:1.8;margin-bottom:2px>法师以<b>德雷莎修女</b>为例: 具足对上帝的绝对信心(信根),一辈子只做「服务最穷的人」这一件事(事修),尽形寿不改——「行一法即行一切法」。<b>梦参老和尚</b>被关33年仍坚守信仰,亦属圆融道行者的典范。</p>";
  h+="<p style=font-size:.7em;color:var(--text2);margin-top:6px>📎 出处: 海云继梦《华严禅观的入法界次第道》(fjdh.cn 2013.9) . 《四十华严讲记》第14讲.第68讲 . <a href='https://www.fjdh.cn/wumin/2013/09/175337285861.html' target=_blank>入法界次第道全文</a></p>";
  h+="</div></div>";

  h+="<div class=wu-door onclick='this.classList.toggle(\"open\")'><span class=arrow>▶</span><span class=ttl>🙏 十大愿王 — 圆融道的工程面核心</span><div class=body>";
  h+="<p style=font-size:.75em;line-height:1.8;margin-bottom:4px>普贤十大愿王是善财童子五十三参的总结与精要——「《入不思议解脱境界普贤行愿品》中,不思议解脱境界即是法界,而普贤行愿是<b>直接入法界的行法</b>。」海云和上先后<b>五次</b>重要讲解: 1992年台北初讲.2001年5月加拿大湛山精舍(共52讲,分三册出版: 《普贤行愿》2002/《不思议解脱》2003/《大方广境界》2003).2006年台北(《普贤十大愿王行法精要》).2007年槟城+2008年新加坡(合并出版《十大愿王修行法要》)。另有2011年昆明开示系列(fjdh.cn收录)。</p>";
  h+="<p style=font-size:.75em;color:var(--gold);margin-bottom:2px><b>十大愿王三层次结构</b></p>";
  h+="<table class=v-table style=font-size:.7em;margin-bottom:6px><tr><th>层次</th><th>愿目</th><th>修行定位</th></tr>";
  h+="<tr><td><b>根本</b>(第1-3愿)</td><td>礼敬诸佛.称赞如来.广修供养</td><td>真正要实修的根本,可各选一门主修</td></tr>";
  h+="<tr><td><b>补充</b>(第4愿)</td><td>忏悔业障</td><td>修前三愿遇挫折时以此补救,<b>具关键性地位</b></td></tr>";
  h+="<tr><td><b>圆融扩大</b>(第5-7愿)</td><td>随喜功德.请转法轮.请佛住世</td><td>使基础修行圆满</td></tr>";
  h+="<tr><td><b>无限扩大</b>(第8-10愿)</td><td>常随佛学(百).恒顺众生(千/重重无尽).普皆迴向(万/无有止境)</td><td>代表无限的扩大——「虚空界尽.众生界尽.众生业尽.众生烦恼尽,我此愿力无有穷尽」</td></tr></table>";
  h+="<p style=font-size:.75em;line-height:1.8;margin-bottom:4px><b>核心要领:</b> (1)<b>普贤行愿力</b>——海云和上在2011年昆明《普贤行愿品》开示中指出: 「普贤菩萨是法界的第一尊佛,你看得到,你能够认识到佛的第一个形象,就是普贤菩萨。那么在自性海中所修行的法,都叫普贤行愿。你在自性海中所修行的法,所产生的威神力,叫做普贤行愿力。」「我以普贤行愿力故,深心信解,如对目前」(即亲自体验证得,非推测想象) (2)<b>四无尽观</b>——每一大愿皆以虚空界尽.众生界尽.众生业尽.众生烦恼尽为所依,四者无有尽故修行无有穷尽,心量无限放大 (3)<b>念念相续无有疲厌</b>——倾向于圆融道行法,不可一曝十寒。</p>";
  h+="<p style=font-size:.7em;color:var(--text2);margin-top:6px>📎 出处: 《普贤十大愿王行法精要》(空庭书苑, 2006年台北讲记, ISBN 9789867484734) . 《十大愿王修行法要》(空庭书苑, 2007槟城+2008新加坡) . 2011年昆明开示系列(fjdh.cn收录) . <a href='https://findbook.com.tw/9789867484734' target=_blank>购买</a></p>";
  h+="</div></div>";
  h+="</div>";

  // ── 第一阶段: 资粮道 ──
  h+="<div class=section id=med-stage1><h2>🔰 第一阶段: 禅修入门 — 发心工程（资粮道）</h2>";
  h+="<p style=font-size:.8em;color:var(--text2);margin-bottom:10px>资粮道是一切禅观的<b>基础准备</b>，约需1-3年。核心任务是<b>发心工程</b>——使行者从散乱中「静下来」。通过<b>「驻佇心观」(停心)</b>将心初步收摄，成为「堪受法器」后方可进入前行。</p>";

  h+="<div class=wu-door onclick='this.classList.toggle(\"open\")'><span class=arrow>▶</span><span class=ttl>📋 制度性入门 — 修行不是DIY</span><div class=body>";
  h+="<p style=font-size:.78em;line-height:1.8;margin-bottom:4px>法师强调:「它是一套制度」——个人能走到哪一步靠「法的传承」，但能否进入这套体系靠「宗的传承」建制。</p>";
  h+="<p style=font-size:.78em;line-height:1.8;margin-bottom:4px><b>前行三年:</b> 完成道场指定基础教材、听经笔记(共修时核实)、每周共修、参加「华藏工程」建立语言和思维模式。经禅师团同意、道场推荐、禅师团审核，方取得「正授行法」资格。</p>";
  h+="<p style=font-size:.78em;line-height:1.8;margin-bottom:4px><b>五科训练:</b> 戒.律.调身.调息.调心。课程配比: 70%修行面(戒/律/调心)+30%健康面(调身/调息)。</p>";
  h+="<p style=font-size:.78em;line-height:1.8;margin-bottom:4px><b>三要件各有三:</b> (1)心性要件-行者先决条件 (2)内摄要件-调身+调息=暖身二法 (3)内观要件-等持工程三昧基础，属一乘不共别圆。</p>";
  h+="<p style=font-size:.7em;color:var(--text2)>📎 出处: 大华严寺官网「资粮道」页面 . 海云继梦《四十华严讲记》第67讲(2009年2月26日开示, fjdh.cn收录逐字稿)</p>";
  h+="</div></div>";

  h+="<div class=wu-door onclick='this.classList.toggle(\"open\")'><span class=arrow>▶</span><span class=ttl>🪑 调身.调息.调心 — 五科训练详解</span><div class=body>";
  h+="<p style=font-size:.78em;line-height:1.8;margin-bottom:4px>五科(戒.律.调身.调息.调心)是资粮道的实操基础。海云和上指出: <b>身.息.心三者一体不二</b>——调息可及于调身,调身效果又可及于调心。实际行法中三者同时并行,非先后次第。核心著作: 《煖身: 华严禅修入门》(布克文化 2021, ISBN 9789865405984)。</p>";

  h+="<p style=font-size:.78em;color:var(--gold);margin-bottom:2px><b>🔹 调身 — 毗卢遮那七支坐相</b></p>";
  h+="<p style=font-size:.7em;color:var(--text2);margin-bottom:4px>据海云和上《迈向佛陀的境界——华严禅前行概论》第六章「毗卢遮那七支坐法」(fjdh.cn收录全文)。和上强调:「七支坐相的目的,旨在调身……若人以此来摄心,即能顿证佛性海。」</p>";
  h+="<table class=v-table style=font-size:.7em;margin-bottom:6px><tr><th style=width:18%>支分</th><th>要点</th></tr>";
  h+="<tr><td><b>(1)跏趺坐</b></td><td>双盘为佳,单盘或金刚坐亦可。臀与两膝三点鼎立成正三角形,稳固久坐不倾</td></tr>";
  h+="<tr><td><b>(2)手结定印</b></td><td>两掌相迭掌心向上,拇指轻拄(指甲碰指甲即可)。「五心向上」(两掌心/两足心/顶门)令气流畅</td></tr>";
  h+="<tr><td><b>(3)头正颈正</b></td><td>头不左右偏。「头正、颈正」与「脊直、肩平」构成十字形</td></tr>";
  h+="<tr><td><b>(4)脊直肩平</b></td><td>脊椎挺直,两肩平正放松,神经/血液/内分泌系统自然运作</td></tr>";
  h+="<tr><td><b>(5)眼平视</b></td><td>眼帘自然下垂以遮光为度,取「三分慈眼」。「此三相摄三千威仪」(头正/脊直/眼平视)</td></tr>";
  h+="<tr><td><b>(6)舌抵颚</b></td><td>舌尖轻顶上颚齿龈(上门牙牙龈处),口水自然由舌根两旁下流入咽喉</td></tr>";
  h+="<tr><td><b>(7)收下颚</b></td><td>头不前后偏,百会穴与海底穴重迭。如此方能「经劫不替」,久坐不倾</td></tr></table>";

  h+="<p style=font-size:.78em;color:var(--gold);margin-bottom:2px><b>🔹 调息 — 息之四相与数息法</b></p>";
  h+="<p style=font-size:.7em;color:var(--text2);margin-bottom:4px>息之四相出自智者大师《释禅波罗蜜次第法门》,海云和上在《禅修前行》第六集(fjdh.cn 2013.11)中引用并详加解说: 「守风则散,守喘则结,守气则劳,守息即定。」</p>";
  h+="<table class=v-table style=font-size:.7em;margin-bottom:4px><tr><th>息相</th><th>特征</th><th>含义/对治</th></tr>";
  h+="<tr><td><b>风相</b></td><td>鼻息粗重,出入有声</td><td>身心不安宁->先安心,放下身心世界</td></tr>";
  h+="<tr><td><b>喘相</b></td><td>息无声但出入结滞不通</td><td>身体多病->宽放身体,放松情绪</td></tr>";
  h+="<tr><td><b>气相</b></td><td>息不结滞但不细</td><td>初修状态->观想气行遍毛孔肢节,愈微愈妙</td></tr>";
  h+="<tr><td><b>息相</b></td><td>无声.不结.不粗,出入绵密若存若亡</td><td><b>调相</b>——可入定</td></tr></table>";
  h+="<p style=font-size:.75em;line-height:1.8;margin-bottom:4px><b>数息要领:</b> 注意力集中于「风门」(鼻中膈底部,两鼻孔间接近上唇处),觉知息入息出。在「息入尽」及「息出尽」的换气处数息(一入一出为一圈)。初学者从数「一至三」起,稳定后增至「一至五」->「一至七」->「一至十」。</p>";

  h+="<p style=font-size:.78em;color:var(--gold);margin-bottom:2px><b>🔹 调心 — 治沉.浮.宽.急四相</b></p>";
  h+="<table class=v-table style=font-size:.7em;margin-bottom:4px><tr><th>心相</th><th>表现</th><th>对治方法</th></tr>";
  h+="<tr><td><b>沉相</b></td><td>昏沉欲睡.精神涣散.低头垂颈</td><td>补充营养(综合维他命);意守<b>风门</b>,守息入息出</td></tr>";
  h+="<tr><td><b>浮相</b></td><td>精神亢奋.心念多缘.身躁动</td><td>少食五辛.补品.牛羊肉等;系念<b>丹田</b></td></tr>";
  h+="<tr><td><b>宽相</b></td><td>心意不举.身好躺卧.口中多水</td><td>饮食多温热少寒凉;摄身挺腰,心安住息中</td></tr>";
  h+="<tr><td><b>急相</b></td><td>胸中疼痛.气上举不调</td><td>多食寒凉少食燥热;放宽身心,意不卑不亢</td></tr></table>";
  h+="<p style=font-size:.75em;line-height:1.8;margin-bottom:4px>若风门举意仍无效,可提意至<b>眉间</b>(风门至眉间称「金刚宝剑」,道家称「小周天」)。</p>";

  h+="<p style=font-size:.78em;color:var(--gold);margin-bottom:2px><b>🔹 入相.住相.出相 — 一座禅修的三阶段</b></p>";
  h+="<p style=font-size:.75em;line-height:1.8;margin-bottom:2px><b>入相(由粗到细):</b> 调身(七支坐相)->调息(觉息相.数息)->调心(治沉浮宽急)。<b>住相(住于细中):</b> 摄心于息,同时觉知身.息.心三相是否调和,随觉随治。<b>出相(由细到粗):</b> 先放心异缘(调心)->开口放气,息从百脉散(调息)->微动身躯.肩臂.头颈.双足,揉毛孔.摩掌熨眼(调身),待身热后方可出入,站定后拍打全身。</p>";
  h+="<p style=font-size:.7em;color:var(--text2);margin-top:6px>📎 出处: 《煖身: 华严禅修入门》(布克文化 2021, ISBN 9789865405984) . 七支坐相原文: 海云和上《迈向佛陀的境界——华严禅前行概论》第六章(fjdh.cn 2013.11) <a href='https://www.fjdh.cn/wumin/2013/11/183343302811.html' target=_blank>全文</a> . 《禅修正行》第12集 . 《禅修前行》第6集 . <a href='https://play.google.com/store/books/details?id=QREREAAAQBAJ' target=_blank>Google Play</a></p>";
  h+="</div></div>";

  h+="<div class=wu-door onclick='this.classList.toggle(\"open\")'><span class=arrow>▶</span><span class=ttl>🧱 驻佇心观(停心工程) — 一切禅观的根本前行</span><div class=body>";
  h+="<p style=font-size:.78em;line-height:1.8;margin-bottom:6px>海云法师:「你要能够停下心来，然后，我们要观心！停心是一个前行，都办不到了，怎么观心啊？」核心次第: <b>「停心」->「观心」</b>。</p>";
  h+="<p style=font-size:.78em;color:var(--gold);margin-bottom:2px><b>停心(体.相二门)</b></p>";
  h+="<p style=font-size:.75em;line-height:1.8;margin-bottom:4px><b>体上停心:</b> 心念不起，六根对六尘境界不会攀缘。<br><b>相上停心:</b> 不妄加猜测、攀缘分别。标准——「心是不是静止下来，像墙壁一样，动都不动！」</p>";
  h+="<p style=font-size:.78em;color:var(--gold);margin-bottom:2px><b>四种停心方法</b></p>";
  h+="<p style=font-size:.75em;line-height:1.8;margin-bottom:4px>(1)参话头: 「看话头就是把心停在那里」 (2)置心一处: 心安鼻端风门,心跑掉就拉回来 (3)数息/随息: 从呼吸入手 (4)依禅堂规矩: 该动则动.该静则静.身心放下。</p>";
  h+="<p style=font-size:.78em;color:var(--gold);margin-bottom:2px><b>观心与验证</b></p>";
  h+="<p style=font-size:.75em;line-height:1.8;margin-bottom:4px>停心之后才能<b>观心</b>——六根对六尘如何作用,看得清清楚楚,「没有任何推理、没有任何意识形态」。法师强调:「不停心你看不到！」六项自检: <b>空.明.定.智.善心.柔软</b>。</p>";
  h+="<p style=font-size:.7em;color:var(--text2);margin-top:6px>📎 出处: 海云继梦《华严禅行法—禅观》第四集 . <a href='https://www.fjdh.cn/wumin/2013/11/165329303084.html' target=_blank>fjdh.cn文字稿</a> . <a href='https://www.fjdh.cn/wumin/2013/09/155711285715.html' target=_blank>停心.观心全文</a></p>";
  h+="</div></div>";
  h+="</div>";

  // ── 第二阶段: 前行 ──
  h+="<div class=section id=med-stage2><h2>⚙️ 第二阶段: 禅修前行 — 内摄工程</h2>";
  h+="<p style=font-size:.8em;color:var(--text2);margin-bottom:10px>前行是禅观体系的<b>核心训练阶段</b>，在<b>界内定</b>中进行。四种观法构成工程面主干，贯穿初信至十信位。前二种出自《占察善恶业报经》(T17n0839)，后二种是标准大乘止观。</p>";

  h+="<div class=wu-door onclick='this.classList.toggle(\"open\")'><span class=arrow>▶</span><span class=ttl>🔧📐 技术面.工程面双轨详解</span><div class=body>";
  h+="<h3 style=color:var(--gold)>🔺 参禅金三角 — 置心一处 . 放轻松 . 息入息出</h3>";
  h+="<p style=font-size:.75em;line-height:1.8;margin-bottom:6px>参禅金三角是海云和上禅修教学中<b>最核心的入门架构</b>,三个条件缺一不可。法师强调:「这三点若能做到及格,触功德就会发起,身心得到调整,人格性可达七十五分以上。完成参禅金三角即进入<b>心一境性</b>。」</p>";
  h+="<table class=v-table style=font-size:.72em;margin-bottom:6px><tr><th style=width:18%>要素</th><th style=width:38%>说明</th><th style=width:44%>操作要点</th></tr>";
  h+="<tr><td><b>(1)置心一处</b></td><td>将心念安住「风门」(鼻孔气息出入处)</td><td>用数息法从一到十循环计数。莫用大脑推理思考,只用<b>感受</b></td></tr>";
  h+="<tr><td><b>(2)放轻松</b></td><td>身体肌肉.神经系统都要放下;心理上也完全放松,不起执着</td><td>不能为了专注而肩膀紧绷。「呼吸归呼吸,妄想归妄想」——不跟妄想纠缠</td></tr>";
  h+="<tr><td><b>(3)息入息出清楚</b></td><td>对呼吸的出入看得清清楚楚,不能昏沉睡着</td><td>「六根门头全开放」——心在宁静中保持鲜活。守住风门,身心放松,妄念停止</td></tr></table>";
  h+="<p style=font-size:.75em;line-height:1.8;margin-bottom:4px><b>整体流程:</b> 调身(七支坐相)->调息(自然呼吸,数息1-10)->置心一处于风门->同时放松身心->息入息出清清楚楚->达成金三角(心一境性)->触功德发起(轻安舒服感)->继续觉照根性->象限转移->破无明->入菩提道。<b>⚠ 警示:</b> 修得轻安感后不可耽于禅味,否则会掉入四禅八定而失去对根性的觉照。</p>";
  h+="<p style=font-size:.7em;color:var(--text2);margin-top:4px>📎 出处: 海云继梦《何谓参禅金三角》(fjdh.cn 2013.12) . <a href='https://www.fjdh.cn/fjask/2013/12/133616318955.html' target=_blank>全文</a> . <a href='http://read.goodweb.top/news/news_view.asp?newsid=82958' target=_blank>禅修释疑</a></p>";

  h+="<h3 style=color:var(--gold)>技术面: 安那般那 — 数.随.止三法</h3>";
  h+="<table class=v-table style=font-size:.75em><tr><th>法位</th><th>境界</th><th>关键操作</th><th>易犯误区</th></tr>";
  h+="<tr><td><b>数法</b></td><td>粗住->细住->欲界定</td><td>置心风门,1数到10循环。克服四种妄想: 心理/物理/生理/社会制度</td><td>⚠ 掉入「舒服禅」——枯木禅非真修</td></tr>";
  h+="<tr><td><b>随法</b></td><td>欲界定->未到定</td><td>注意「息入尽」与「息出尽」的每一个细节。妄想被堵住</td><td>追求境界名相,忽略身心柔和</td></tr>";
  h+="<tr><td><b>止法</b></td><td>置心一处.心一境性</td><td>所有妄想脱落,心境合一。八触十功德</td><td>⚠ 左转入外道禅;须「右转」向四果</td></tr></table>";
  h+="<h3 style=color:var(--gold)>工程面: 三阶段心法 + 三层功夫</h3>";
  h+="<p style=font-size:.75em;line-height:1.8><b>A阶段:</b> 感受息之长短与动静差异 <b>B阶段:</b> 洞悉呼吸因果轨迹(法师称「生命的秘笈」) <b>C阶段:</b> 心王.心所.境界(公开资料未完全展开)</p>";
  h+="<p style=font-size:.75em;line-height:1.8><b>内摄(技术面):</b> 「妄想一起,把心抓回来放在风门」 <b>内观(工程面):</b> 在数随止中感受法身存在,分三级: 寂而常照/照而常寂/寂照双亡 <b>禅观:</b> 粗(数随止中感受)->细(置心一处后)->微妙(十信圆满后)</p>";
  h+="<p style=font-size:.7em;color:var(--text2);margin-top:6px>📎 出处: 大华严寺官网「修行蓝图」. 海云继梦《禅修正行》《禅观》系列 . 《海云继梦禅观概论》(2015)第四章</p>";
  h+="</div></div>";

  h+="<div class=wu-door onclick='this.classList.toggle(\"open\")'><span class=arrow>▶</span><span class=ttl>👁 四种观法体系 — 前行工程面核心</span><div class=body>";
  h+="<table class=v-table style=font-size:.72em;margin-bottom:8px><tr><th>观法</th><th>信位</th><th>禅定</th><th>工程</th><th>核心操作</th><th>成就</th></tr>";
  h+="<tr><td><b>(1)唯心识观</b></td><td>初信~二信</td><td>四天王定(煖法)</td><td>自省三业</td><td>守记内心;避免无记攀缘;行禅/闭眼抬手训练</td><td>色寂三昧</td></tr>";
  h+="<tr><td><b>(2)真如实观</b></td><td>二信位+</td><td>忉利定(顶法)</td><td>观五蕴流转</td><td>思惟心性无生无灭;反观自性;超越四空定</td><td>相似空三昧->心寂三昧->一行三昧</td></tr>";
  h+="<tr><td><b>(3)毗婆舍那观</b></td><td>中信位</td><td>空居天定->色界定</td><td>观根尘识;照住色受间</td><td>观六根六尘六识流动;照住色受动态止观</td><td>渐舍五识(色界定)</td></tr>";
  h+="<tr><td><b>(4)奢摩他观</b></td><td>后信位</td><td>无色界定->出界定</td><td>照见五蕴空;入正真位</td><td>舍意识;能所双泯;照见五蕴皆空</td><td>十信满心;入法界;圆教初住位</td></tr></table>";

  h+="<p style=font-size:.78em;color:var(--gold);margin-bottom:2px><b>📜 经典出处 & 利钝分判</b></p>";
  h+="<p style=font-size:.75em;line-height:1.8;margin-bottom:4px>《占察善恶业报经》:「若欲依一实境界修信解者,应当学习二种观道。何等为二?一者唯心识观,二者真如实观。」海云法师称此经为<b>「小本华严」</b>。<br>📎 <a href='https://cbeta.buddhism.org.hk/xml/T17/T17n0839_002.xml' target=_blank>CBETA 大正藏 T17n0839</a></p>";
  h+="<p style=font-size:.75em;line-height:1.8;margin-bottom:6px><b>利钝分判:</b> 利根者(阴盖轻微.散乱心少)->直修真如实观; 钝根者(染着情厚.心难调伏)->先修唯心识观。海云法师补充: 钝根先以唯心识观摄心,令妄想降伏后方转入真如实观,此即<b>「由相入性」</b>。</p>";

  h+="<p style=font-size:.78em;color:var(--gold);margin-bottom:2px><b>(1) 唯心识观 — 毗钵舍那(观).法相宗.钝根先修</b></p>";
  h+="<p style=font-size:.75em;line-height:1.8;margin-bottom:4px>定位: 初信~二信位。工程: <b>自省三业</b>(身.语.意),在定中境中唯观一切三业「唯心生.唯心灭」。<b>四天王定</b>是行者从「定外境」转入「定内境」的起点,属坚信位「煖法」;<b>忉利定</b>属「顶法」,不仅唯见三业之既成,更能见到「三业中心之所由起」。</p>";
  h+="<p style=font-size:.75em;line-height:1.8;margin-bottom:4px>「学唯心识观者,于一切时一切处,随身口意所有作业,悉当观察,<b>知唯是心</b>。勿令使心无记攀缘,不自觉知。」「一切法唯心想生。若使离心,则无一法一相而能自见有差别也。」</p>";
  h+="<p style=font-size:.75em;line-height:1.8;margin-bottom:4px><b>两大重点:</b> (正面)守记内心-念念清楚;(反面)避免无记攀缘-口头禅.摸头发等惯性动作。<b>具体训练:</b> (1)闭眼抬手-「手在哪里?你知道吗?要很清楚地感知到」 (2)行禅-脚步慢慢抬起->停->放下,清清楚楚了知 (3)口诀-「唯心识观就是不用大脑,让灵性生命浮现出来」。得<b>色寂三昧</b>。</p>";

  h+="<p style=font-size:.78em;color:var(--gold);margin-bottom:2px><b>(2) 真如实观 — 奢摩他(止).法性宗.利根直修</b></p>";
  h+="<p style=font-size:.75em;line-height:1.8;margin-bottom:4px>定位: 二信位及以上。工程: <b>观五蕴流转</b>。与唯心识观的差别: 前者看「身语意三业(表层)」,后者深入「五蕴(身心基本元素)」的微观生灭。法理: 大乘起信论「一心开二门」—唯心识观对心生灭门(心之用),真如实观对心真如门(心之体)。</p>";
  h+="<p style=font-size:.75em;line-height:1.8;margin-bottom:4px>「思惟心性<b>无生无灭</b>,不住见闻觉知,永离一切分别之想,渐渐能过空处.识处.无少处.非想非非想处等定境界相,得<b>相似空三昧</b>。」「展转能入<b>心寂三昧</b>……即复能入<b>一行三昧</b>,见佛无数,发深广行心,住<b>坚信位</b>。」</p>";
  h+="<p style=font-size:.75em;line-height:1.8;margin-bottom:4px><b>海云判摄</b>[语境: 2013年高雄《占察善恶业报经》开示]: 「唯心识观是让你了解心的存在跟作用-它像<b>流水</b>一样,前念接后念。真如实观是直接去看那个<b>源头</b>-心性的本源,无生无灭的那个。」</p>";

  h+="<p style=font-size:.78em;color:var(--gold);margin-bottom:2px><b>(3) 毗婆舍那观 — 深化观照.中信位</b></p>";
  h+="<p style=font-size:.75em;line-height:1.8;margin-bottom:4px>定位: 中信位(约五~六信位)。含两个递进层面: (a)观照六根六尘相接时的六识流动-比唯心识观更精微,从行为觉知深入到感知通道机制 (b)照住色与受之间的动态止观-「色」(物质性感受)与「受」(心理性感受)的细微边界。成就: 渐舍五识,进入色界定。</p>";

  h+="<p style=font-size:.78em;color:var(--gold);margin-bottom:2px><b>(4) 奢摩他观 — 究竟止观.后信位.能所双泯</b></p>";
  h+="<p style=font-size:.75em;line-height:1.8;margin-bottom:4px>定位: 后信位(七~十信位)。三步骤: (a)舍意识-三界定功总纲最后阶段 (b)能所双泯-完全泯除主客二元对立,即《心经》「照见五蕴皆空」 (c)入正真位.十信满心-得「能所双泯」,正式「入法界」,成<b>圆教初住位</b>,转入正行。</p>";

  h+="<p style=font-size:.78em;color:var(--gold);margin-bottom:2px><b>📐 三界定功总纲(海云法师判摄)</b></p>";
  h+="<table class=v-table style=font-size:.72em;margin-bottom:6px><tr><th>界定层次</th><th>核心工程</th><th>对应观法</th><th>对应信位</th></tr>";
  h+="<tr><td><b>欲界定</b></td><td>捨妄念</td><td>唯心识观+真如实观</td><td>初信~四信位</td></tr>";
  h+="<tr><td><b>色界定</b></td><td>捨五识</td><td>毗婆舍那观</td><td>五信~六信位</td></tr>";
  h+="<tr><td><b>无色界定</b></td><td>捨意识</td><td>奢摩他观</td><td>七信~九信位</td></tr>";
  h+="<tr><td><b>出界定</b></td><td>能所双泯.入法界</td><td>奢摩他观究竟</td><td>十信满心</td></tr></table>";

  h+="<p style=font-size:.7em;color:var(--text2);margin-top:6px>📎 出处: 《非常占察经》讲记三册(空庭书苑 2015-2017, ISBN 9789867484918/4932/4949) . 播客「普賢乘華嚴宗」S18(46集) . <a href='https://podcasts.apple.com/au/podcast/%E6%99%AE%E8%B3%A2%E4%B9%98%E8%8F%AF%E5%9A%B4%E5%AE%97/id1523368889' target=_blank>🎙 Apple Podcast</a> . <a href='https://open.spotify.com/show/2ZDlq4cOOiynQvlzPARkmc' target=_blank>🎧 Spotify</a></p>";
  h+="</div></div>";

  h+="<div class=wu-door onclick='this.classList.toggle(\"open\")'><span class=arrow>▶</span><span class=ttl>📊 十信法门.果位对应 — 四种观法的阶位映射</span><div class=body>";
  h+="<p style=font-size:.78em;line-height:1.8;margin-bottom:6px>海云法师将声闻「四果」与华严「十信位」逐级对应。「破根本无明」是初果的门槛而非彻悟终点——「破根本无明才叫做悟后起修！」[语境: 2009年2月26日《四十华严讲记》第67讲, 台北]</p>";
  h+="<table class=v-table style=font-size:.72em><tr><th>传统果位</th><th>华严信位</th><th>对应观法</th><th>禅定层次</th><th>关键标准</th></tr>";
  h+="<tr><td>初果(预流果)</td><td><b>初信位</b></td><td>唯心识观</td><td>四天王定(煖法)</td><td>「舍识用根」</td></tr>";
  h+="<tr><td>—</td><td><b>二信位</b></td><td>唯心识->真如实</td><td>忉利定(顶法)</td><td>确认菩提心.毗卢遮那七支坐相.收心工程</td></tr>";
  h+="<tr><td>二果(一来果)</td><td><b>三信位</b></td><td>真如实观</td><td>欲界空居天定</td><td>开始运用「观照」.具轻安三相+天王三德</td></tr>";
  h+="<tr><td>—</td><td><b>四信位</b></td><td>真如实观</td><td>同上</td><td>安般守意工程: 置心于风门</td></tr>";
  h+="<tr><td>三果(不还果)</td><td><b>五信位</b></td><td>毗婆舍那观</td><td>色界定</td><td>渐舍五识</td></tr>";
  h+="<tr><td>四果向</td><td><b>六信位</b></td><td>毗婆舍那观</td><td>色界定</td><td>照住-色受动态止观</td></tr>";
  h+="<tr><td>四果(阿罗汉)</td><td><b>七信位</b></td><td>奢摩他观</td><td>无色界定</td><td>我法二执尚未双破</td></tr>";
  h+="<tr><td>发心破法执</td><td><b>八信位</b></td><td>奢摩他观</td><td>无色界定</td><td>回小向大</td></tr>";
  h+="<tr><td>我执法执双破</td><td><b>九信位</b></td><td>奢摩他观</td><td>出界定</td><td>渐舍意识</td></tr>";
  h+="<tr><td>十信位圆满</td><td><b>十信位</b></td><td>奢摩他究竟</td><td>出界定.入法界</td><td>能所双泯=照见五蕴皆空.成<b>圆教初住位</b></td></tr></table>";
  h+="<p style=font-size:.7em;color:var(--text2);margin-top:4px>十信位之后: <b>初住位至七地</b>(37位.正行.对应金刚界曼荼罗37尊)-><b>八地至妙觉</b>(5位.无功用行)——共<b>42位</b>圆满佛果。</p>";
  h+="</div></div>";

  h+="<div class=wu-door onclick='this.classList.toggle(\"open\")'><span class=arrow>▶</span><span class=ttl>🔬 三重观照技术: 观照.照住.照见</span><div class=body>";
  h+="<p style=font-size:.75em;line-height:1.8;margin-bottom:4px>贯穿四种观法的操作层面技术: <b>观照</b>(二果开始,能所分离,唯心识观在此运作)-> <b>照住</b>(至四果,能所合一,毗婆舍那观在此深化)-> <b>照见</b>(十信满心,能所双泯,奢摩他观在此圆满)。</p>";
  h+="<p style=font-size:.72em;color:var(--text2)>法师说明:《心经》《金刚经》在他的判摄里都属于<b>圆教初住位</b>的教法——证量标的其实是「十信位圆满.入法界」之后的境界。</p>";
  h+="</div></div>";
  h+="</div>";

  // ── 第三阶段: 正行 ──
  h+="<div class=section id=med-stage3><h2>🎯 第三阶段: 禅修正行 — 等持工程（内观）</h2>";
  h+="<p style=font-size:.8em;color:var(--text2);margin-bottom:10px>十信满心之后,转入正行。<b>等持工程</b>为官网正式名称。前半程三摩呬多(samahita),后半程定慧等持(三摩钵底 samapatti),究竟等至(三摩地 samadhi)。官网: 「以观导定、以定成观,当下验果,端身正坐,置心风门,依次第而进,步步可检核。」海云和上在讲记中进一步以「界内定/界外定」区分前行与正行的禅定层次,并以杜顺法界三观为究竟指导。</p>";

  h+="<div class=wu-door onclick='this.classList.toggle(\"open\")'><span class=arrow>▶</span><span class=ttl>🌐 杜顺法界三观 — 正行核心指导框架</span><div class=body>";
  h+="<p style=font-size:.78em;line-height:1.8;margin-bottom:4px>杜顺和尚(华严初祖)所立三重观法,是华严禅观正行的<b>究竟指导</b>。海云和上指出: 龙树将三法印汇归<b>一法印——空性</b>(真空绝相观);杜顺进一步推进为<b>理事无碍观</b>;最终倡<b>事事无碍观(周遍含容观)</b>——举事即能通事,无需再透过理的转辙,<b>此唯法身大士之行径</b>。</p>";
  h+="<table class=v-table style=font-size:.72em;margin-bottom:6px><tr><th>观法</th><th>对应法界</th><th>核心义理</th><th>海云法师判摄</th></tr>";
  h+="<tr><td><b>(1)真空绝相观</b></td><td>理法界</td><td>会色归空,明空即色,空色无碍。一切法当体即空</td><td>龙树空性一法印之极致——理无碍即阿罗汉空性观</td></tr>";
  h+="<tr><td><b>(2)理事无碍观</b></td><td>理事无碍法界</td><td>理遍于事,事遍于理。理(真如)不碍事(万象),事不碍理</td><td>事无碍即生活中的一切事物——「吾辈行者,亦当力行乎此」</td></tr>";
  h+="<tr><td><b>(3)周遍含容观</b></td><td>事事无碍法界</td><td>事如理融,遍摄无碍。如因陀罗网,一即一切,重重无尽</td><td>举事即通事,不经理之转辙——唯法身大士境界。即海印三昧现前</td></tr></table>";
  h+="<p style=font-size:.7em;color:var(--text2)>📎 出处: 杜顺《法界观门》 . 海云继梦《迈向佛陀的境界》(空庭书苑 2011) . <a href='http://wuming.xuefo.net/nr/6/59482.html' target=_blank>事事无碍周遍含融(fjdh.cn)</a></p>";
  h+="</div></div>";

  h+="<div class=wu-door onclick='this.classList.toggle(\"open\")'><span class=arrow>▶</span><span class=ttl>💠 正授行法 — 四次灌顶制度</span><div class=body>";
  h+="<table class=v-table style=font-size:.78em><tr><th>灌顶</th><th>目标</th><th>关键</th></tr>";
  h+="<tr><td><b>(1)忍可灌顶</b></td><td>破根本无明</td><td>约十人中八人被「踢出去」重修</td></tr>";
  h+="<tr><td><b>(2)行者灌顶</b></td><td>证初果.寻生命原形</td><td>通过后取得正式「行者」资格</td></tr>";
  h+="<tr><td><b>(3)进阶灌顶</b></td><td>能所合一.破我法二执</td><td>成就四智</td></tr>";
  h+="<tr><td><b>(4)高阶灌顶</b></td><td>能所双泯.入法界</td><td>「照见根性,能所双泯」=「照见五蕴皆空」</td></tr></table>";
  h+="</div></div>";

  h+="<div class=wu-door onclick='this.classList.toggle(\"open\")'><span class=arrow>▶</span><span class=ttl>🎯 三摩呬多.三摩钵底.三摩地</span><div class=body>";
  h+="<table class=v-table style=font-size:.75em><tr><th>名相</th><th>梵语</th><th>定位</th><th>操作要点</th></tr>";
  h+="<tr><td><b>三摩呬多</b></td><td>Samahita</td><td>入定前.专注调心</td><td>粗住->细住->欲界定。排除妄想执著</td></tr>";
  h+="<tr><td><b>三摩钵底</b></td><td>Samapatti</td><td>以观导定.定慧双运</td><td>勘定三界定。须善知识勘定</td></tr>";
  h+="<tr><td><b>三摩地</b></td><td>Samadhi</td><td>究竟.心一境性.海印三昧</td><td>出入自在。破法执我执</td></tr></table>";
  h+="<p style=font-size:.7em;color:var(--text2);margin-top:4px>⚠ 术语说明: 「三摩地」(samadhi)标准译语为「等持」,「三摩钵底」(samapatti)标准译语为「等至」。大华严寺官方资料中的配对与此恰好相反——此系道场自身的术语使用习惯。</p>";
  h+="</div></div>";
  h+="</div>";

  // ── 古典义理地基: 五教止观 ──
  h+="<div class=section id=med-classical><h2>📜 古典义理地基 — 杜顺和尚五教止观</h2>";
  h+="<p style=font-size:.8em;color:var(--text2);margin-bottom:8px>华严初祖杜顺大师所立五教止观,是华严宗禅观的<b>古典义理框架</b>。海云和上的四种观法是<b>实际操作体系</b>,五教止观则是其<b>背后的意识状态分类学</b>——二者构成「行」与「解」的互补关系。</p>";

  h+="<div class=wu-door onclick='this.classList.toggle(\"open\")'><span class=arrow>▶</span><span class=ttl>一.法有我无门(小乘教)</span><div class=body>破除「我执」,体悟我空,但法执犹存。对应四禅八定。<br><span style=font-size:.7em;color:var(--text2)>在海云体系中对应: 资粮道阶段的基本停心功夫。</span></div></div>";
  h+="<div class=wu-door onclick='this.classList.toggle(\"open\")'><span class=arrow>▶</span><span class=ttl>二.生即无生门(大乘始教)</span><div class=body>体悟「法空」——外境皆由阿赖耶识变现。<br><span style=font-size:.7em;color:var(--text2)>在海云体系中对应: 唯心识观——「知唯是心」的义理背景。</span></div></div>";
  h+="<div class=wu-door onclick='this.classList.toggle(\"open\")'><span class=arrow>▶</span><span class=ttl>三.事理圆融门(大乘终教)</span><div class=body>空有不二,理事圆融无碍。<br><span style=font-size:.7em;color:var(--text2)>在海云体系中对应: 真如实观——理(真如)与事(五蕴流转)融合的义理背景。</span></div></div>";
  h+="<div class=wu-door onclick='this.classList.toggle(\"open\")'><span class=arrow>▶</span><span class=ttl>四.语观双绝门(大乘顿教)</span><div class=body>言语道断,心行处灭。<br><span style=font-size:.7em;color:var(--text2)>在海云体系中对应: 奢摩他观——「舍意识」「能所双泯」的义理背景。</span></div></div>";
  h+="<div class=wu-door onclick='this.classList.toggle(\"open\")'><span class=arrow>▶</span><span class=ttl>五.华严三昧门(一乘圆教.究竟)</span><div class=body>见法界缘起之相——万象影现,一即一切、圆融无碍。此即海印三昧。<br><span style=font-size:.7em;color:var(--text2)>在海云体系中对应: 正行究竟——三摩地.海印三昧.法界三观现前.42位圆满。</span></div></div>";
  h+="</div>";

  // ── 贤首五教仪: 华严判教体系 ──
  h+="<div class=section id=med-wujiao><h2>📐 贤首五教仪 — 华严判教: 小.始.终.顿.圆</h2>";
  h+="<p style=font-size:.8em;color:var(--text2);margin-bottom:8px>贤首五教仪由华严三祖法藏(贤首国师)创立,清续法大师集大成,是华严宗<b>判教理论的核心框架</b>。海云继梦和上称判教为<b>「文化解剖学」</b>——将印度佛教文明基因与中国文明基因进行重组的方式。五教与杜顺五教止观一一对应: 小教(法有我无门).始教(生即无生门).终教(事理圆融门).顿教(语观双绝门).圆教(华严三昧门)。法师于<b>2008年5月19日至7月17日</b>在台北讲授《贤首五教仪—法界观》,可确认至少<b>53集</b>。播客音频于2020年3月9日前后由「海云继梦法师讲经」频道集中上传至Spotify/Apple Podcast等平台。</p>";

  h+="<table class=v-table style=font-size:.72em;margin-bottom:10px><tr><th>五教</th><th>核心义理</th><th>海云法师判摄</th><th>修证品数</th></tr>";
  h+="<tr><td><b>小教</b></td><td>只说人空,不明法空。依六识三毒建立染净根本。<br>「如木作灰,如色归空,断烦恼障,灭分段死」</td><td>封闭型心态,只执一法门。总相念=始教十回向</td><td>—</td></tr>";
  h+="<tr><td><b>始教</b></td><td>分空始教(般若)与相始教(唯识)。说一切皆空或分别诸法性相。定性二乘不成佛</td><td>「如镜离垢,如月出云,断二障,灭二死,显二空,证二果」</td><td>十二品</td></tr>";
  h+="<tr><td><b>终教</b></td><td>说如来藏随缘成阿赖耶识。定性二乘.无性阐提悉当成佛。少说法相,广说真性</td><td>「如器成金,如冰即水」——将事相会归于理体,大乘至极之说</td><td>四十二品</td></tr>";
  h+="<tr><td><b>顿教</b></td><td><b>一念不生,即名为佛。</b>唯是一念,无时可说。无明不起时即无时空;无明起时便有三大阿僧祇劫</td><td>「如狂迷歇,如睡梦觉」——一切烦恼本来自离,不是烦恼缠你,是你招揽烦恼。关键: <b>置心一处</b></td><td>五十二品</td></tr>";
  h+="<tr><td><b>圆教</b></td><td><b>一切即一,一即一切。</b>念劫圆融,自在无碍。一位即一切位,十信满心即摄五位成正觉。依普贤法界,性相圆融,主伴无尽</td><td>「如拆棉花,如融金狮」——不破而圆融,一切时分同时具足。初住至妙觉,三地超顿教妙觉</td><td>六十二品</td></tr></table>";

  h+="<p style=font-size:.7em;color:var(--text2);margin-top:4px>📎 出处: 海云继梦 2008年台北《贤首五教仪—法界观》53集+ . <a href='https://www.listennotes.com/podcasts/%E6%B5%B7%E4%BA%91%E7%BB%A7%E6%A2%A6%E6%B3%95%E5%B8%88%E8%AE%B2%E7%BB%8F-%E6%92%AD%E5%AE%A2/' target=_blank>ListenNotes播客</a> . <a href='https://open.spotify.com/show/2ZDlq4cOOiynQvlzPARkmc' target=_blank>Spotify</a> . 续法《贤首五教仪》原著</p>";

  h+="<div class=wu-door onclick='this.classList.toggle(\"open\")'><span class=arrow>▶</span><span class=ttl>🔀 渐教.顿教的实践义 — 从判教到操作</span><div class=body>";
  h+="<p style=font-size:.75em;line-height:1.8;margin-bottom:4px>海云和上将判教转化为实际操作: <b>渐教</b>(始教+终教)——次第修证路线,对应四种观法中的唯心识观->真如实观->毗婆舍那观,一级一级深入。<b>顿教</b>——「一念不生,即名为佛」「唯是一念,无时可说」。关键操作: <b>置心一处</b>——守住风门(或佛号.咒语.数息),其他六尘境界一概不理,「能置心一处,一切烦恼自然离开」。顿教与始教.终教的根本区别: 小教与始教都在「无明的前提下」讲时间与次第;顿教直接告诉你<b>无明不起时,即无时间可得</b>——这是大脑想象不到.言语道断的境界。</p>";
  h+="<p style=font-size:.7em;color:var(--text2)>📎 出处: 海云继梦《贤首五教仪—法界观》第40-45集(2008.7.8-7.10)</p>";
  h+="</div></div>";
  h+="</div>";

  // ── 一乘不共别圆 ──
  h+="<div class=section id=med-yicheng><h2>📐 一乘不共别圆 — 普贤乘的判教定位</h2>";
  h+="<p style=font-size:.8em;color:var(--text2);margin-bottom:8px>「一乘不共别圆」是华严宗对自身教义的最高定位——「别人所没有的,所以叫做『别』」。「不共」谓不与三乘共,独为圆顿大根菩萨所说;「别圆」指有别于天台宗以《法华》为圆教的立场,华严自许为最圆满的别教一乘。海云和上特别强调: 这种不共别圆的特质不在理论层面,而在<b>行法的内在蕴藏</b>——「他在经文里头表达得很清楚,但是因为你不懂这种语言模式跟思维模式,所以你以为经文好像讲故事一样讲过去。」</p>";
  h+="<table class=v-table style=font-size:.72em;margin-bottom:8px><tr><th>概念</th><th>定位</th><th>特点</th></tr>";
  h+="<tr><td><b>别教一乘</b></td><td>《华严经》——纯圆至实,别于三乘</td><td>智俨《孔目章》:「别教者,别于三乘故。」法藏《五教章》: 分「性海果分」(佛自证,不可说)与「缘起因分」(普贤境界,可说)</td></tr>";
  h+="<tr><td><b>同教一乘</b></td><td>《法华经》——会三归一,摄末归本</td><td>智俨: 开三乘方便显一乘真实。法藏判同教一乘较别教一乘低一位,因须「会三归一」方显一乘</td></tr></table>";
  h+="<p style=font-size:.75em;line-height:1.8;margin-bottom:6px>海云和上以「<b>普贤乘</b>」名其体系——此即华严别教一乘的实践展开。法师在《四十华严讲记》第68讲中指出: 「普贤乘」的关键在<b>直接兑现</b>,非如三乘出离需次第渐修——「能观心即生成报身(文殊),所观心则生成法身(普贤),置心一处可滋长法身慧命。」并强调此不共别圆的特质不在理论,而在行法的内在蕴藏——「他在经文里头表达得很清楚,但是因为你不懂这种语言模式跟思维模式,所以你以为经文好像讲故事一样讲过去。」[语境: 2009年《四十华严》第68讲,台北]</p>";
  h+="<p style=font-size:.7em;color:var(--text2);margin-top:4px>📎 出处: 智俨《华严经孔目章》.法藏《五教章》.海云继梦《四十华严讲记》第68讲 . 《华严学报》第3期(2012)</p>";
  h+="</div>";

  // ── 重要华严典籍的现代阐释 ──
  h+="<div class=section id=med-texts><h2>📖 重要华严典籍的现代阐释</h2>";

  h+="<div class=wu-door onclick='this.classList.toggle(\"open\")'><span class=arrow>▶</span><span class=ttl>🦁 法藏《华严金师子章》 — 十门妙诠华严法界玄奥</span><div class=body>";
  h+="<p style=font-size:.78em;line-height:1.8;margin-bottom:4px>《金师子章》是华严三祖法藏为武则天讲解华严奥义之作——以殿中金狮子为喻,从明缘起.辨色空.约三性.显无相.说无生.论五教.勒十玄.括六相.成菩提.入涅槃<b>十门</b>,仅约一千五百字,妙诠华严法界玄奥。海云继梦和上于<b>2006年在台北开示,共14集</b>。后由空庭书苑整理出版为《华严金师子章讲记》(265页,2010年出版)。讲记逐字稿于2013年11月由fjdh.cn(佛教导航)集中发布。</p>";
  h+="<p style=font-size:.75em;line-height:1.8;margin-bottom:4px><b>核心判摄:</b> 十段分三——(1~3)缘起/色空/三性=基础理论 (4~5)无相/无生=般若空性 (6)五教=判教入华严 (7)十玄=事事无碍最高境界 (8)六相=综合圆融(初地) (9)成菩提=二次圆融 (10)入涅槃=三次圆融,重重无尽。</p>";
  h+="<p style=font-size:.75em;line-height:1.8;margin-bottom:4px><b>十玄门要义:</b> 同时具足相应门(金体与师子相同时成立).因陀罗网境界门(一一毛处各有金师子,重重无尽,一即一切).十世隔法异成门(九世融于一念)。</p>";
  h+="<p style=font-size:.75em;line-height:1.8;margin-bottom:2px><b>修行三区块:</b> 凡夫区(变异念->善恶念->净识念).行者区(初果向到破我法二执).法身区(根本智->后得智->自受用->他受用)。法师强调:「知道不算,做到才算。」</p>";
  h+="<p style=font-size:.7em;color:var(--text2);margin-top:6px>📎 出处: 海云继梦《华严金师子章讲记》(空庭书苑 2010) . <a href='http://wuming.xuefo.net/nr/7/70462.html' target=_blank>fjdh.cn逐字稿(14集)</a> . <a href='https://www.got1shop.com/mobile/index.php?m=default&c=goods&a=index&id=3459706' target=_blank>购买</a></p>";
  h+="</div></div>";

  h+="<div class=wu-door onclick='this.classList.toggle(\"open\")'><span class=arrow>▶</span><span class=ttl>💎 澄观《心要法门》 — 「至道本乎其心,心法本乎无住」</span><div class=body>";
  h+="<p style=font-size:.78em;line-height:1.8;margin-bottom:4px>《心要法门》是华严四祖清凉澄观大师(738-839)所撰,全文仅数百字,阐述<b>「至道本乎其心,心法本乎无住」</b>的华严心法核心要义——无住心体是华严禅观的终极归趣。海云继梦和上以现代语言逐段译解,出版为<b>《解心: 心要法门讲记》</b>(空庭书苑 2001年6月30日初版, ISBN 9573067129, 326页; 宗教文化出版社 2005年9月简体版, 187页)。</p>";
  h+="<p style=font-size:.75em;line-height:1.8;margin-bottom:4px><b>核心思想:</b> 「无住心体」——真心不执著于任何一处,灵知不昧,性相寂然,包含德用,该摄内外。能证此者,即入法界。「心法本乎无住」——一切心法的根本在于无住,无住即不执取,不执取即解脱。</p>";
  h+="<p style=font-size:.75em;line-height:1.8;margin-bottom:4px><b>海云法师判摄:</b> 此即华严禅观的终极指向——四种观法(唯心识->真如实->毗婆舍那->奢摩他)层层深入,最终所证即是此「无住心体」。<b>「无心于万物,而万物未尝无」</b>——不是消灭万物,而是于万物中不执取,此即事事无碍法界的日常体现。</p>";
  h+="<p style=font-size:.75em;line-height:1.8;margin-bottom:2px>法师后续出版《是心,非心,还是心!——从心要法门谈心》(空庭书苑 2013, ISBN 9789867484710),进一步深化「无住心体」与华严禅观修行次第的内在关联。</p>";
  h+="<p style=font-size:.7em;color:var(--text2);margin-top:6px>📎 出处: 海云继梦《解心: 心要法门讲记》(空庭书苑 2001/宗教文化出版社 2005) . <a href='https://www.buybook.tw/book-0010164666.htm' target=_blank>购买</a> . <a href='https://webpac.taichung.gov.tw/bookDetail/730070' target=_blank>图书馆</a></p>";
  h+="</div></div>";

  h+="<div class=wu-door onclick='this.classList.toggle(\"open\")'><span class=arrow>▶</span><span class=ttl>📐 华严三品行法 — 净行品·梵行品·普贤行愿品</span><div class=body>";
  h+="<p style=font-size:.75em;line-height:1.8;margin-bottom:4px>据《华藏妙海》听经笔记整理,海云和上将华严三品对应修行三阶段: <b>净行品</b>——前行阶段的修行法门,信位菩萨所修,在日常生活中即可修; <b>梵行品</b>——正行阶段的修行法门; <b>普贤行愿品</b>——成佛以后的修学法门,「众生有尽,我愿无穷」。三品都是行门,构成从初学到究竟的完整行法链条。</p>";
  h+="<p style=font-size:.75em;line-height:1.8;margin-bottom:4px><b>结界工程</b>(据同来源): 结界是针对自己弱点,在自己能力范围内做最妥善的调整与安排,是个人修行资粮道的基础。从结界中可以学到如何肯定自己、认识自己——「结界工程是个人资粮道的基础」。</p>";
  h+="<p style=font-size:.7em;color:var(--text2);margin-top:6px>📎 出处: 《华藏妙海》听经笔记整理版(docs/notes4it目录)。<br>🔗 弥勒菩萨章: 海云和上于善财五十三参第51参详讲弥勒菩萨——毗卢遮那庄严藏楼阁,共<b>12集</b>视频(B站 BV1X142147EN)+播客(Podwise)。此为法师关于弥勒的最主要讲记,目前文字整理尚不完整,建议直接观看视频。</p>";
  h+="</div></div>";
  h+="</div>";

  // ── 验证机制 & 关键原则 ──
  h+="<div class=section id=med-verify><h2>⚠ 贯穿全程 — 验证机制.关键原则</h2>";
  h+="<div class=wu-door onclick='this.classList.toggle(\"open\")'><span class=arrow>▶</span><span class=ttl>✅ 验证机制 — 200+测验 & 归零重修</span><div class=body>";
  h+="<p style=font-size:.78em;line-height:1.8>法师强调修行进程「绝对理性」「不能讲人情」: 全程设有<b>两百余种具体测验</b>——制造顺境诱发贪着反应、制造逆境激发嗔心反应。<br><br><b>失败重修的规则极为严格</b>: 并非退回上一级,而是<b>打回初信(初果)从头开始</b>——「四果再重修,就从这个地方开始,再从初果开始。」</p>";
  h+="</div></div>";

  h+="<div class=wu-door onclick='this.classList.toggle(\"open\")'><span class=arrow>▶</span><span class=ttl>⚠ 三大关键原则</span><div class=body>";
  h+="<p style=font-size:.78em;line-height:1.8;margin-bottom:6px><b>(1)不走四禅八定:</b> 法师称其为「共外道法」——「我们不走那条路,我们直接走出三界。」[语境: 2009年《四十华严讲记》第67讲]</p>";
  h+="<p style=font-size:.78em;line-height:1.8;margin-bottom:6px><b>(2)大脑临界点:</b> 置心一处之前可运用理性思维;一旦跨过初果门槛,必须弃用概念思维——「只要用大脑,初果进不去,就这么简单。」[语境: 2009年《四十华严讲记》第67讲]</p>";
  h+="<p style=font-size:.78em;line-height:1.8;margin-bottom:4px><b>(3)两种歧路:</b> 置心一处后产生「舒服.喜悦.轻安」或「恐惧」。若被执取,<b>两种都会导向外道禅</b>——必须连这类感受也一并放下。</p>";
  h+="</div></div>";
  h+="</div>";

  // ── 实修心要文章链接 ──

  // ── 完整出处 ──

  h+="<div id=med-heart class=pv-section style=display:none>";
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

  h+="</div>"; // close pv-heart
  h+="</div>"; // close pv-meditation

  // ═══════════════════════════════════════════
  // SUB-PAGE 3: 实修心要 (hidden)
  // ═══════════════════════════════════════════

  // Auto-restore saved data (only right columns, not left article text)
  setTimeout(function(){
    var raw=localStorage.getItem('huayan_heart_data_v2');
    if(!raw)return;
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
  h+="<div id=pv-news class=pv-section style=display:block>";
  h+="<div style='display:flex;gap:6px;flex-wrap:wrap;margin-bottom:12px;padding:8px 10px;background:var(--panel);border:1px solid var(--line);border-radius:8px;font-size:0.75em'><b style=color:var(--gold)>📰 最新动态:</b><a href='#news-updates' style=color:var(--blue)>近期动态</a>·<a href='#news-academic' style=color:var(--blue)>学术活动</a></div>";
  h+="<div class=section id=news-updates><h2>📡 最新动态（2023-2026）</h2>";
  h+="<div class=stage-box><b>2023 — 国立台北大学杰出校友</b><br>获遴选为母校杰出校友(2023年)。2024年1月促成华严学会与台北大学签署学术合作协议(一期两年.合计三期共六年),合办「新世纪永续发展」高峰论坛(2024-2025年)。</div>";
  h+="<div class=stage-box><b>2026 — 「九九华严」五年讲座（TICC）</b><br>于台北国际会议中心举行，每月举办。将华严哲理「转化为通俗易懂的现代心理学与生命科学」语言，回应「AI科技与永续新时代」的挑战——「AI给得了答案，但给得了心安吗？」</div>";
  h+="<div class=stage-box><b>2026.7.9 — 支提山大华严寺动土</b><br>苗栗县通霄镇。面向台湾海峡，与福建宁德支提华严祖庭隔海相望——「山海相应、法脉相承」。四百余位护法善信参与，五十三位嘉宾共同执铲（呼应善财五十三参）。</div>";
  h+="<div class=stage-box><b>第四期佛教</b><br>大华严寺官网对海云法师使命的表述——「以中兴汉传佛教，开展<b>第四期佛教思想发展</b>为使命」。目前尚未见对第一至第三期的系统性论述。</div></div>";

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

  h+="<div id=pv-resources class=pv-section style=display:block>";
  h+="<div style='display:flex;gap:6px;flex-wrap:wrap;margin-bottom:12px;padding:8px 10px;background:var(--panel);border:1px solid var(--line);border-radius:8px;font-size:0.75em'><b style=color:var(--gold)>📡 讲法资源:</b><a href='#res-total' style=color:var(--blue)>全网总目</a>·<a href='#res-topics' style=color:var(--blue)>主题分类</a>·<a href='#res-books' style=color:var(--blue)>著作</a>·<a href='#res-yt' style=color:var(--blue)>YouTube</a>·<a href='#res-temples' style=color:var(--blue)>道场</a>·<a href='#res-sources' style=color:var(--blue)>出处参考</a>·<a href='#res-more' style=color:var(--blue)>检索补遗</a></div>";

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

  // ── YouTube 频道最新内容 ──
  h+="<div class=section id=res-yt><h2>📺 YouTube 频道 · 最新系列</h2>";
  h+="<p style=font-size:0.78em;color:var(--text2);margin-bottom:8px>数据来源: RSS Feed (最后同步: 2026-07-30)。频道持续更新中。</p>";
  h+="<table class=v-table><tr><th>频道</th><th>系列</th><th>内容</th><th>最近更新</th><th>直达</th></tr>";
  h+="<tr><td rowspan=4 style=font-size:0.78em><b><a href='https://www.youtube.com/@huayen-world' target=_blank>@huayen-world</a></b><br><span style=font-size:0.7em;color:var(--text2)>主频道</span></td>";
  h+="<td><b>🔴 海雲法語</b></td><td>和上法语开示短片: 转凡成圣、发愿行法、佛菩萨加持、泯除瞋心、净土关键等</td><td>2026-07-29</td><td><a href='https://www.youtube.com/@huayen-world/videos' target=_blank>📺</a></td></tr>";
  h+="<tr><td><b>🟠 華嚴教海</b></td><td>经典讲解: 《佛法玄谈》(至第6集)、《九九華嚴》TICC录影(第6集上线)</td><td>2026-07-27</td><td><a href='https://www.youtube.com/@huayen-world/playlists' target=_blank>📋</a></td></tr>";
  h+="<tr><td><b>🟡 Shorts</b></td><td>修行要点精选: 戒律/佛菩萨示现/念佛持咒（节录自2008北美药师经开示等）</td><td>2026-07-26</td><td><a href='https://www.youtube.com/@huayen-world/shorts' target=_blank>📱</a></td></tr>";
  h+="<tr><td><b>🟢 藥師經北美講座</b></td><td>2008年北美药师经系列开示（近期海雲法語的母体讲座来源）</td><td>节录连载中</td><td><a href='https://www.youtube.com/results?search_query=%E8%97%A5%E5%B8%AB%E7%B6%93+%E6%B5%B7%E9%9B%B2%E7%B9%BC%E5%A4%A2+%E5%8C%97%E7%BE%8E' target=_blank>🔍</a></td></tr>";
  h+="</table>";
  h+="<p style='font-size:0.72em;color:var(--text2);margin-top:6px'>📌 RSS同步源 (待扩展多频道): <code>https://www.youtube.com/feeds/videos.xml?channel_id=UCJr3ifkvTs76XnR6SuyIfFQ</code></p></div>";

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
  localStorage.setItem('practice_sub',view);
  // Force-reload lazy images when switching to heart (now med-heart)
  if(view==='meditation'){setTimeout(function(){
    document.querySelectorAll('#med-heart img').forEach(function(img){
      var s=img.src;img.src='';img.src=s;
    });
  },200);}
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
    // SUB-PAGE RESTORE DISABLED FOR DEBUG
    // var sub=localStorage.getItem('practice_sub')||'system';
    // if(sub==='heart')sub='meditation';
    // if(sub&&['system','meditation','news','resources'].indexOf(sub)>=0){
    //   switchPracticeView(sub);
    // }
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
  localStorage.setItem(STORAGE_KEY,t.trim());ghToken=t.trim();
  fetch('https://api.github.com/user',{headers:{'Authorization':'Bearer '+ghToken,'Accept':'application/vnd.github+json'}})
  .then(function(r){return r.json();})
  .then(function(u){
    _update();_toast(u.login==='LengyanReader'?'✅ '+u.login+' · Push已启用':'⚠ Token属于'+u.login);
  }).catch(function(){_update();_toast('✅ Token已保存');});
};
// Push
window.heartPushToGitHub=function(){
  if(!_isOkay()){_toast('❌ 请先🔑配置Token');heartLogin();return;}
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
