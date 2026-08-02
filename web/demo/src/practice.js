// ═══ PRACTICE TAB ═══
function renderPractice(){
  var pv=document.getElementById("practice-view");if(!pv)return;
  var h="";
  h+="<style>.wu-door{cursor:pointer;padding:10px 14px;margin:4px 0;background:var(--card);border:1px solid var(--line);border-radius:8px;transition:all 0.2s}.wu-door:hover{border-color:var(--gold-l)}.wu-door .arrow{display:inline-block;transition:transform 0.2s;margin-right:6px}.wu-door.open .arrow{transform:rotate(90deg)}.wu-door .body{display:none;margin-top:8px;padding-top:8px;border-top:1px solid var(--line);font-size:0.9em;line-height:1.8;color:var(--text2)}.wu-door.open .body{display:block}.wu-door .ttl{font-weight:600;color:var(--gold);font-size:1em}.topic-card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px 14px;margin-bottom:8px}.topic-card h4{color:var(--gold);font-size:0.88em;margin-bottom:4px}.topic-card p{font-size:0.78em;line-height:1.7;color:var(--text2)}.topic-card a{color:var(--blue);font-size:0.75em}</style>";

  // ── Sub-navigation ──
  h+="<div style='display:flex;gap:6px;margin-bottom:16px;flex-wrap:wrap'><button class='pv-nav active' onclick='switchPracticeView(\"system\",this)'>🧘 修行体系</button><button class='pv-nav' onclick='switchPracticeView(\"meditation\",this)'>📐 禅观法要</button><button class='pv-nav' onclick='switchPracticeView(\"resources\",this)'>📡 讲法资源</button></div>";

  // ═══════════════════════════════════════════
  // SUB-PAGE 1: 修行体系 (default visible)
  // ═══════════════════════════════════════════
  h+="<div id=pv-system class=pv-section>";

  // ── WIP Notice ──
  h+="<div style='background:rgba(184,134,60,0.06);border:1px solid #b8863c40;border-radius:8px;padding:8px 12px;margin-bottom:12px;font-size:0.75em;color:var(--text2);line-height:1.6'>"
    +"⚠ <b>内容声明：</b>本页面内容基于大华严寺官网(2025.11版)和海云继梦和上已公开的讲经视频/音频/逐字稿/出版物整理。"
    +"法师讲法内容不断更新演化，当前整理仍不完整，需要大量结构化梳理和补充核实，<b>仅供参考</b>，持续更新中。"
    +"最新修行体系请以大华严寺官网为准。<br>"
    +"📅 最近更新：2026-08-02</div>";

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
  h+="<div class=section><h2>📐 修行三阶段（据大华严寺官网「修行蓝图」2025.11）</h2>";
  h+="<div class=stage-box><b>一、禅修入门 — 发心工程（资粮道）</b><br>三门必修: 人格健康+出离心+菩提心。含<b>五科</b>（戒·律·调身·调息·调心）。技术面: 纯化禅(动→静)→象限转移→瞬间定。工程面: 心性培养+戒律基础。官网: 「发心——出三界、入法界之志,建立信根与定位。」</div>";
  h+="<div class=stage-box><b>二、禅修前行 — 内摄工程</b><br>核心: 安那般那数息观(数.随.止)。官网: 「调息安稳,气息有序;守意——令心不外驰,身息心三者逐步协同。」观法次第: <b>驻佇心观</b>(停心前行)-><b>唯心识观</b>(钝根先修.毗钵舍那)-><b>真如实观</b>(利根直修.奢摩他)-><b>毗婆舍那</b>-><b>奢摩他</b>。详见「📐 禅观法要」子页。</div>";
  h+="<div class=stage-box><b>三、禅修正行 — 等持工程（内观）</b><br>前半程三摩呬多→后半程三摩钵底→究竟三摩地。官网: 「以观导定、以定成观,当下验果,不逐境界名相而重身心之柔和、稳定、清明。」课程配比: <b>70%修行面 + 30%健康面</b>。延伸: 一日禅·二日禅·忍可禅七。</div></div>";

  // ── 四阶段修行蓝图 ──
  h+="<div class=section><h2>🪜 四阶段修行蓝图（海云法师判摄）</h2>";
  h+="<p style=font-size:0.8em;color:var(--text2);margin-bottom:8px>据海云法师《四十华严讲记》第四卷第67讲及大华严寺官网「修行蓝图」页面。整套蓝图涵盖从信众到证量的完整阶次。</p>";
  h+="<div class=stage-box><b>一、出离乘</b>（出离心→出离道→出离行）<br>以脱离轮回、了生死为基础动机，建立「出三界、入法界」之志。</div>";
  h+="<div class=stage-box><b>二、菩提乘</b>（菩提心→菩提道→菩提行）<br>发心求觉悟。法师称此「只是起步」。</div>";
  h+="<div class=stage-box><b>三、菩萨乘</b>（菩萨心→菩萨道→菩萨行）<br>法师称此「还没有究竟」——仍属因地修行。</div>";
  h+="<div class=stage-box><b>四、普贤乘</b>（普贤心→普贤行→普贤道）<br><b style=color:var(--gold)>究竟归趣。</b>法师称「究竟要到普贤乘来」——此即「普贤乘华严宗」名称的义理出处。</div></div>";

  // ── 华严六科 + 五大行法 ──
  h+="<div class=section><h2>🎯 华严六科 & 五大行法</h2>";
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
  h+="<div class=section><h2>⚡ 三大法脉行法分工</h2>";
  h+="<p style=font-size:0.8em;color:var(--text2);margin-bottom:4px>海云法师对三条汇流法脉在体系中各自的功能分工（据大华严寺官网及讲记）：</p>";
  h+="<div class=stage-box><b>中观论派 →「解」</b><br>义理/空性论证——负责「理解」层面的理论基础。</div>";
  h+="<div class=stage-box><b>华严思想 →「架构」</b><br>提供整体的世界观与义理框架——「事事无碍法界」「法界缘起」等核心世界观。</div>";
  h+="<div class=stage-box><b>瑜伽行派 →「行」</b><br>禅观正行/实修技术来源。源自印度 Maha Yoga 传承（胜师子王菩萨），法师将其等同于「禅宗的禅观正行」。<br><span style=font-size:0.75em;color:var(--text2)>注: 官网将这支传承直接注解为「大乘瑜伽行派／Yogācāra 之行门精义」，读者可留意其中的诠释性跨度。</span></div></div>";

  // ── 四大工程 ──
  h+="<div class=section><h2>🏗 四大工程</h2><table class=v-table><tr><th>工程</th><th>性质</th></tr>";
  h+="<tr><td><b>结界工程</b></td><td>短期共修——调整身心频率的具体操作</td></tr>";
  h+="<tr><td><b>华藏工程</b></td><td>双重意涵: ①个人前行阶段必修课程（建立语言/思维模式）②跨世代文明教育志业——法师称「华藏工程五百年」</td></tr>";
  h+="<tr><td><b>华严大学</b></td><td>体制化培育弘法与研究人才的当代项目（非月霞法师等创办的历史性华严大学）</td></tr>";
  h+="<tr><td><b>BQ广场</b></td><td>四大工程之一，目前公开资料中未见「BQ」具体所指的清晰界定</td></tr>";
  h+="</table></div>";

  // ── 识·根·智 ──
  h+="<div class=section><h2>🔬 识·根·智 — 三层认知转换</h2>";
  h+="<p style=font-size:0.8em;color:var(--text2);margin-bottom:4px>法师自创的认知层次术语，用以区分凡夫、行者、法身大士三个阶段所依靠的不同认知机制：</p>";
  h+="<div class=stage-box><b>识性（凡夫阶段）</b><br>「能」——妄想心。「识性的能绑虚妄的身」——凡夫是「身心混杂」状态。</div>";
  h+="<div class=stage-box><b>根性（初果至四果阶段）</b><br>「所」。此阶段关键操作是<b>「舍识用根」</b>。</div>";
  h+="<div class=stage-box><b>智（十信位圆满之后）</b><br>此后「以智为先导」，不再「以所为先导」。<br><span style=font-size:0.75em;color:var(--text2)>注: 法师坦承这套区分是借助现代汉语语法结构对古典义理的诠释性翻译，非声称唯一表述。</span></div></div>";

  // ── 三缘念 ──
  h+="<div class=section><h2>🙏 三缘念 — 修行归依</h2>";
  h+="<p style=line-height:1.8>海云法师在传统「皈依三宝」之外，提出更具操作性的归依框架：<br>";
  h+="<b>① 缘念道场</b> — 缘念僧团，以道场为修行依止处；<br>";
  h+="<b>② 缘念善知识</b> — 缘念具体指导的师长，接受僧团制度性指导；<br>";
  h+="<b>③ 缘念法门</b> — 缘念自己实际修学的具体法门，不杂修不盲从。<br>";
  h+="<span style=font-size:0.78em;color:var(--text2)>修行态度: 法师强调「自顾灵山，不顾名山」「知道不算，做到才算」——真正的修行来自扎实的日常践行。</span></p></div>";

  // ── 最新动态 ──
  h+="<div class=section><h2>📡 最新动态（2023-2026）</h2>";
  h+="<div class=stage-box><b>2023 — 国立台北大学杰出校友</b><br>获遴选为母校杰出校友(2023年)。2024年1月促成华严学会与台北大学签署学术合作协议(一期两年.合计三期共六年),合办「新世纪永续发展」高峰论坛(2024-2025年)。</div>";
  h+="<div class=stage-box><b>2026 — 「九九华严」五年讲座（TICC）</b><br>于台北国际会议中心举行，每月举办。将华严哲理「转化为通俗易懂的现代心理学与生命科学」语言，回应「AI科技与永续新时代」的挑战——「AI给得了答案，但给得了心安吗？」</div>";
  h+="<div class=stage-box><b>2026.7.9 — 支提山大华严寺动土</b><br>苗栗县通霄镇。面向台湾海峡，与福建宁德支提华严祖庭隔海相望——「山海相应、法脉相承」。四百余位护法善信参与，五十三位嘉宾共同执铲（呼应善财五十三参）。</div>";
  h+="<div class=stage-box><b>第四期佛教</b><br>大华严寺官网对海云法师使命的表述——「以中兴汉传佛教，开展<b>第四期佛教思想发展</b>为使命」。目前尚未见对第一至第三期的系统性论述。</div></div>";

  // ── 演进脉络 ──
  h+="<div class=section><h2>📅 工程面·技术面 演进脉络 & 时间线</h2>";
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
  h+="<div id=pv-meditation class=pv-section style=display:none>";

    // ── 体系总览 ──
  h+="<div class=section style=border-left:4px solid var(--gold)><h2>🗺 华严禅观体系总览</h2>";
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
  h+="<div class=section><h2>🛤 次第道与圆融道 — 两条修行路径</h2>";
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
  h+="<div class=section><h2>🔰 第一阶段: 禅修入门 — 发心工程（资粮道）</h2>";
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
  h+="<div class=section><h2>⚙️ 第二阶段: 禅修前行 — 内摄工程</h2>";
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
  h+="<div class=section><h2>🎯 第三阶段: 禅修正行 — 等持工程（内观）</h2>";
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
  h+="<div class=section><h2>📜 古典义理地基 — 杜顺和尚五教止观</h2>";
  h+="<p style=font-size:.8em;color:var(--text2);margin-bottom:8px>华严初祖杜顺大师所立五教止观,是华严宗禅观的<b>古典义理框架</b>。海云和上的四种观法是<b>实际操作体系</b>,五教止观则是其<b>背后的意识状态分类学</b>——二者构成「行」与「解」的互补关系。</p>";

  h+="<div class=wu-door onclick='this.classList.toggle(\"open\")'><span class=arrow>▶</span><span class=ttl>一.法有我无门(小乘教)</span><div class=body>破除「我执」,体悟我空,但法执犹存。对应四禅八定。<br><span style=font-size:.7em;color:var(--text2)>在海云体系中对应: 资粮道阶段的基本停心功夫。</span></div></div>";
  h+="<div class=wu-door onclick='this.classList.toggle(\"open\")'><span class=arrow>▶</span><span class=ttl>二.生即无生门(大乘始教)</span><div class=body>体悟「法空」——外境皆由阿赖耶识变现。<br><span style=font-size:.7em;color:var(--text2)>在海云体系中对应: 唯心识观——「知唯是心」的义理背景。</span></div></div>";
  h+="<div class=wu-door onclick='this.classList.toggle(\"open\")'><span class=arrow>▶</span><span class=ttl>三.事理圆融门(大乘终教)</span><div class=body>空有不二,理事圆融无碍。<br><span style=font-size:.7em;color:var(--text2)>在海云体系中对应: 真如实观——理(真如)与事(五蕴流转)融合的义理背景。</span></div></div>";
  h+="<div class=wu-door onclick='this.classList.toggle(\"open\")'><span class=arrow>▶</span><span class=ttl>四.语观双绝门(大乘顿教)</span><div class=body>言语道断,心行处灭。<br><span style=font-size:.7em;color:var(--text2)>在海云体系中对应: 奢摩他观——「舍意识」「能所双泯」的义理背景。</span></div></div>";
  h+="<div class=wu-door onclick='this.classList.toggle(\"open\")'><span class=arrow>▶</span><span class=ttl>五.华严三昧门(一乘圆教.究竟)</span><div class=body>见法界缘起之相——万象影现,一即一切、圆融无碍。此即海印三昧。<br><span style=font-size:.7em;color:var(--text2)>在海云体系中对应: 正行究竟——三摩地.海印三昧.法界三观现前.42位圆满。</span></div></div>";
  h+="</div>";

  // ── 贤首五教仪: 华严判教体系 ──
  h+="<div class=section><h2>📐 贤首五教仪 — 华严判教: 小.始.终.顿.圆</h2>";
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
  h+="<div class=section><h2>📐 一乘不共别圆 — 普贤乘的判教定位</h2>";
  h+="<p style=font-size:.8em;color:var(--text2);margin-bottom:8px>「一乘不共别圆」是华严宗对自身教义的最高定位——「别人所没有的,所以叫做『别』」。「不共」谓不与三乘共,独为圆顿大根菩萨所说;「别圆」指有别于天台宗以《法华》为圆教的立场,华严自许为最圆满的别教一乘。海云和上特别强调: 这种不共别圆的特质不在理论层面,而在<b>行法的内在蕴藏</b>——「他在经文里头表达得很清楚,但是因为你不懂这种语言模式跟思维模式,所以你以为经文好像讲故事一样讲过去。」</p>";
  h+="<table class=v-table style=font-size:.72em;margin-bottom:8px><tr><th>概念</th><th>定位</th><th>特点</th></tr>";
  h+="<tr><td><b>别教一乘</b></td><td>《华严经》——纯圆至实,别于三乘</td><td>智俨《孔目章》:「别教者,别于三乘故。」法藏《五教章》: 分「性海果分」(佛自证,不可说)与「缘起因分」(普贤境界,可说)</td></tr>";
  h+="<tr><td><b>同教一乘</b></td><td>《法华经》——会三归一,摄末归本</td><td>智俨: 开三乘方便显一乘真实。法藏判同教一乘较别教一乘低一位,因须「会三归一」方显一乘</td></tr></table>";
  h+="<p style=font-size:.75em;line-height:1.8;margin-bottom:6px>海云和上以「<b>普贤乘</b>」名其体系——此即华严别教一乘的实践展开。法师在《四十华严讲记》第68讲中指出: 「普贤乘」的关键在<b>直接兑现</b>,非如三乘出离需次第渐修——「能观心即生成报身(文殊),所观心则生成法身(普贤),置心一处可滋长法身慧命。」并强调此不共别圆的特质不在理论,而在行法的内在蕴藏——「他在经文里头表达得很清楚,但是因为你不懂这种语言模式跟思维模式,所以你以为经文好像讲故事一样讲过去。」[语境: 2009年《四十华严》第68讲,台北]</p>";
  h+="<p style=font-size:.7em;color:var(--text2);margin-top:4px>📎 出处: 智俨《华严经孔目章》.法藏《五教章》.海云继梦《四十华严讲记》第68讲 . 《华严学报》第3期(2012)</p>";
  h+="</div>";

  // ── 重要华严典籍的现代阐释 ──
  h+="<div class=section><h2>📖 重要华严典籍的现代阐释</h2>";

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
  h+="<div class=section><h2>⚠ 贯穿全程 — 验证机制.关键原则</h2>";
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
  h+="<div class=section><h2>📰 实修心要 — 永远的犍陀罗·禅修实操系列</h2>";
  h+="<p style=font-size:.78em;color:var(--text2);margin-bottom:6px>以下10篇文章来自微信公众号「<b>永远的犍陀罗</b>」· <b>实修心要</b>专辑。内容为海云继梦和上关于禅修实操的开示,由仁悦整理。原文链接为微信公众号文章,全文已保存至 <code>docs/hy_refs/wechat/</code> 目录。</p>";
  h+="<div style='display:flex;gap:6px;flex-wrap:wrap;font-size:0.73em'>";
  [{n:1,t:'别用大脑修行',d:'暖身二法·调身调息·内脏内动'},
   {n:2,t:'四段呼吸的奥秘',d:'呼吸四阶段的辨识与运用'},
   {n:3,t:'闭气不是憋气',d:'闭气与憋气的关键区别'},
   {n:4,t:'摸着那个"转折点"',d:'呼吸中阻力的转折与突破'},
   {n:5,t:'呼吸里的一股"力"',d:'息之力的感知与运用'},
   {n:6,t:'置心一处的三大工程',d:'置心一处的技术面三大要素'},
   {n:7,t:'心跑了，抓回来！',d:'摄心——若心他缘摄之令返'},
   {n:8,t:'别躲清静，去"防震"',d:'动中修行的防震训练'},
   {n:9,t:'内动来了，用"金钥匙"',d:'参禅金钥匙的触发与运用'},
   {n:10,t:'入禅九阶：从暖身到金钥匙',d:'系统总结——禅修九阶次第'}]
  .forEach(function(a){h+="<span style='padding:4px 10px;background:rgba(94,139,158,0.06);border:1px solid rgba(94,139,158,0.2);border-radius:10px;min-width:160px'><b style=color:#5e8b9e>第"+a.n+"篇</b> <b>"+a.t+"</b><br><span style=font-size:0.85em;color:var(--text2)>"+a.d+"</span><br><span style=font-size:0.65em;color:var(--text2)>📁 docs/hy_refs/wechat/"+("0"+a.n).slice(-2)+"_*</span></span>";});
  h+="</div>";
  h+="<p style=font-size:.68em;color:var(--text2);margin-top:6px>📌 <b>来源:</b> 微信公众号「永远的犍陀罗」· 实修心要专辑 · 海云继梦和上开示 · 仁悦整理 · 2026-08-02批量提取</p>";
  h+="</div>";

  // ── 完整出处 ──
  h+="<div class=section><h2>📚 信实可靠的出处与参考资源</h2>";
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

  h+="</div>"; // close pv-meditation

  // ═══════════════════════════════════════════
  // SUB-PAGE 3: 讲法资源 (hidden)
  // ═══════════════════════════════════════════
  h+="<div id=pv-resources class=pv-section style=display:none>";

  // ── 全网讲法总目 ──
  h+="<div class=section><h2>📡 海云继梦全网讲法总目</h2>";
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
  h+="<div class=section><h2>📚 按主题分类讲法资源</h2>";
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
  h+="<div class=section><h2>📖 海云继梦著作（空庭书苑/光潽文创出版·2002-2026）</h2><p style=font-size:0.8em;line-height:1.9>";
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
  h+="</div></div>";
  h+="<p style=line-height:1.8;margin-top:8px>";
  h+="🎙 <a href='https://podcasts.apple.com/au/podcast/%E6%99%AE%E8%B3%A2%E4%B9%98%E8%8F%AF%E5%9A%B4%E5%AE%97/id1523368889' target=_blank>Apple Podcast</a> · ";
  h+="<a href='https://open.spotify.com/show/2ZDlq4cOOiynQvlzPARkmc' target=_blank>Spotify</a> (20+系列·每周更新) | ";
  h+="🌐 <a href='https://www.huayenworld.org/' target=_blank>大华严寺官网</a> · ";
  h+="<a href='https://www.huayenworld.org/%e8%8f%af%e5%9a%b4%e7%a6%aa%e7%b0%a1%e4%bb%8b%e7%89%b9%e8%89%b2/' target=_blank>修行蓝图全文</a>";
  h+="</p></div>";

  // ── YouTube 频道最新内容 ──
  h+="<div class=section><h2>📺 YouTube 频道 · 最新系列</h2>";
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
  h+="<div class=section><h2>🎓 学术活动轨迹 (2010-2025)</h2>";
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

  // ── 相关道场 ──
  h+="<div class=section><h2>🏛 相关道场</h2><p style=line-height:1.8>";
  h+="📍 <b>南投大华严寺</b> — 海云继梦导师·普贤乘根本道场<br>";
  h+="📍 <b>苗栗支提山大华严寺</b> — 2026.7.9动土·面向台湾海峡·与福建支提华严祖庭隔海相望<br>";
  h+="📍 <b>台北福慧寺</b> — 钦因长老·高原法系<br>";
  h+="📍 <b>台北华严莲社</b> — 贤度法师·华严专宗学院<br>";
  h+="📍 <b>陕西师范大学华严研究所</b> — 海云法师曾任荣誉所长及客座教授</p></div>";

  h+="</div>"; // close pv-resources

  pv.innerHTML=h;
}

// ═══ PRACTICE SUB-NAV ═══
function switchPracticeView(view,btn){
  document.querySelectorAll(".pv-nav").forEach(function(b){b.classList.remove("active");});
  if(btn)btn.classList.add("active");
  document.querySelectorAll(".pv-section").forEach(function(s){s.style.display="none";});
  document.getElementById("pv-"+view).style.display="block";
}
