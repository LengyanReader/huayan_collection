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

  // ── Header ──
  h+="<div class=section style=border-left:4px solid var(--gold)><h2>🧘 华严行法 — 普贤乘修行体系</h2>";
  h+="<p style=line-height:1.8>参考大华严寺海云继梦和上所立 <b>普贤乘华严宗</b> 修行体系。以华严禅法为核心，透过<b>心法工程</b>止住安心、令真心起作用。体系涵盖从资粮道到正行、从初信到法身大士的完整修行次第。</p></div>";

  // ── 三阶段卡片 ──
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
  h+="</div>";

  // ── 修行三阶段 ──
  h+="<div class=section><h2>📐 修行三阶段</h2>";
  h+="<div class=stage-box><b>一、资粮道 — 发心工程</b><br>三门必修: 人格健康+出离心+菩提心。含<b>五科</b>（戒·律·调身·调息·调心）。技术面: 纯化禅(动→静)→象限转移→瞬间定。工程面: 心性培养+戒律基础。</div>";
  h+="<div class=stage-box><b>二、前行 — 内摄工程（界内定）</b><br>核心: 安那般那数息观(数·随·止·观·还·净)。观法次第: <b>驻佇心观</b>（停心前行）→ <b>唯心识观</b>（钝根先修·毗钵舍那）→ <b>真如实观</b>（利根直修·奢摩他）。训练重点: 调息安稳、气息有序、令心不外驰。详见「禅观法要」→「三种观法」。</div>";
  h+="<div class=stage-box><b>三、正行 — 等持工程（界外定）</b><br>前半程三摩呬多→后半程三摩钵底→究竟三摩地。依杜顺法界三观，透过海印三昧呈现华严境界。课程配比: <b>70%修行面 + 30%健康面</b>。</div></div>";

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
  h+="<div class=stage-box><b>2023 — 国立台北大学杰出校友</b><br>获遴选为母校杰出校友。2024年1月促成华严学会与台北大学签署学术合作协议（一期两年、合计三期），合办「新世纪永续发展」高峰论坛。</div>";
  h+="<div class=stage-box><b>2026 — 「九九华严」五年讲座（TICC）</b><br>于台北国际会议中心举行，每月举办。将华严哲理「转化为通俗易懂的现代心理学与生命科学」语言，回应「AI科技与永续新时代」的挑战——「AI给得了答案，但给得了心安吗？」</div>";
  h+="<div class=stage-box><b>2026.7.9 — 支提山大华严寺动土</b><br>苗栗县通霄镇。面向台湾海峡，与福建宁德支提华严祖庭隔海相望——「山海相应、法脉相承」。四百余位护法善信参与，五十三位嘉宾共同执铲（呼应善财五十三参）。</div>";
  h+="<div class=stage-box><b>第四期佛教</b><br>大华严寺官网对海云法师使命的表述——「以中兴汉传佛教，开展<b>第四期佛教思想发展</b>为使命」。目前尚未见对第一至第三期的系统性论述。</div></div>";

  // ── 演进脉络 ──
  h+="<div class=section><h2>📅 工程面·技术面 演进脉络 & 时间线</h2>";
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

  h+="</div>"; // close pv-system

  // ═══════════════════════════════════════════
  // SUB-PAGE 2: 禅观法要 (hidden)
  // ═══════════════════════════════════════════
  h+="<div id=pv-meditation class=pv-section style=display:none>";

  // ── 制度性入门 ──
  h+="<div class=section><h2>📋 制度性入门 — 修行不是DIY</h2>";
  h+="<p style=line-height:1.8;margin-bottom:8px>海云法师蓝图中最具特色的一面——修行在其体系中首先是<b>有明确准入门槛的建制</b>。法师强调:「它是一套制度」——个人能走到哪一步靠「法的传承」，但能否进入这套体系靠「宗的传承」建制。</p>";
  h+="<div class=stage-box><b>前行三年</b><br>须完成道场指定的基础教材课程、听经笔记（共修时核实）、每周共修、参加「华藏工程」以建立「语言模式跟思维模式」。经禅师团同意、道场推荐、禅师团审核，方取得参加「正授行法」的资格。</div>";
  h+="<div class=stage-box><b>五科 — 资粮道训练</b><br><b>戒·律·调身·调息·调心</b>。课程配比: 70%修行面（戒/律/调心）+ 30%健康面（调身/调息）。延伸课程: 一日禅、二日禅、忍可禅七（七日密集）。</div>";
  h+="<div class=stage-box><b>三要件各有三</b><br>①<b>心性要件</b>: 行者先决条件，避免落入修行陷阱；②<b>内摄要件</b>: 调身+调息为「暖身二法」；③<b>内观要件</b>: 等持工程的三昧基础，属「一乘不共别圆」。</div>";
  h+="<div class=stage-box><b>四次灌顶</b><br>第一次: <b>忍可灌顶</b>——约十人中八人被「踢出去」重修；第二次: <b>行者灌顶</b>——通过后证初果，取得正式「行者」资格；第三、四次: 公开资料未展开。</div></div>";

  // ── 技术面·工程面双轨 ──
  h+="<div class=section><h2>⚙️ 技术面·工程面 — 双轨详解</h2>";
  h+="<p style=line-height:1.8;margin-bottom:8px>海云法师将华严禅法分为<b>技术面</b>（修定·身法）与<b>工程面</b>（修慧·心法），比喻为「建设部门与工程师」——「没有技术面，工程面推不动；没有工程面，技术面只是空壳」。</p>";

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

  // ── 观照·照住·照见 ──
  h+="<div class=section><h2>🔬 观照·照住·照见 — 三重技术</h2>";
  h+="<p style=font-size:0.8em;color:var(--text2);margin-bottom:4px>对应果位的「操作层面」技术描述:</p>";
  h+="<div class=stage-box><b>观照</b>（二果开始训练）→ <b>照住</b>（至四果·能所合一）→ <b>照见</b>（十信位·能所双泯）<br>法师特别说明:《心经》《金刚经》在他的判摄里都属于<b>圆教初住位</b>的教法——即这两部通行极广的经典，其证量标的其实是「十信位圆满、入法界」之后的境界。</div></div>";

  // ── 关键原则 ──
  h+="<div class=section><h2>⚠ 关键原则与警示</h2>";
  h+="<div class=stage-box><b>不走四禅八定</b><br>法师明言不采用四禅八定路径，称其为「共外道法」——「我们不走那条路，我们直接走出三界。」</div>";
  h+="<div class=stage-box><b>大脑临界点</b><br>置心一处之前，仍可运用理性思维（「大脑」）；一旦跨过初果门槛，就必须完全弃用概念思维——「只要用大脑，初果进不去，就这么简单。」此后训练「只有一个工作，就是用真心观照，感受根性的存在」。</div>";
  h+="<div class=stage-box><b>两种歧路</b><br>置心一处后产生两种状态: 一种是「很舒服、很喜悦、很轻安」，另一种是「恐惧」。若被执取，<b>两种都会导向外道禅</b>，甚至滑入四禅八定的初禅定——必须连这类感受也一并放下，才可能「真正出三界」。</div></div>";

  // ── 五教止观 ──
  h+="<div class=section><h2>📜 五教止观（杜顺和尚·点击展开）</h2>";
  h+="<p style=font-size:0.8em;color:var(--text2);margin-bottom:6px>华严初祖杜顺大师所立——渐进意识状态分类学。每一门对应特定教位与禅定境界。</p>";
  h+="<div class=wu-door onclick='this.classList.toggle(\"open\")'><span class=arrow>▶</span><span class=ttl>一、法有我无门（小乘教）</span><div class=body>破除「我执」，体悟我空，但法执犹存。一切法因缘和合，因果历然。对应四禅八定中的初、二、三、四禅。</div></div>";
  h+="<div class=wu-door onclick='this.classList.toggle(\"open\")'><span class=arrow>▶</span><span class=ttl>二、生即无生门（大乘始教）</span><div class=body>体悟「法空」——外境皆由阿赖耶识变现，生而无生。达我法二空之境。此门始破「法执」，识心无体，境不自境。</div></div>";
  h+="<div class=wu-door onclick='this.classList.toggle(\"open\")'><span class=arrow>▶</span><span class=ttl>三、事理圆融门（大乘终教）</span><div class=body>空有不二，悲智双运。实现「空有双亡」之境——理（真如）不碍事（万象），事不碍理，理事圆融无碍。</div></div>";
  h+="<div class=wu-door onclick='this.classList.toggle(\"open\")'><span class=arrow>▶</span><span class=ttl>四、语观双绝门（大乘顿教）</span><div class=body>离心行言说之境。言语道断，心行处灭。唯有真如及真如智。言语不能及，观想不能到，唯证相应。</div></div>";
  h+="<div class=wu-door onclick='this.classList.toggle(\"open\")'><span class=arrow>▶</span><span class=ttl>五、华严三昧门（一乘圆教·究竟）</span><div class=body>见法界缘起之相——万象影现，一即一切、圆融无碍。若能当下认证万法从缘，便可顿入法界缘起。此即海印三昧——如大海映现万象，佛心如海，一时普现十方法界无尽缘起。</div></div>";
  h+="</div>";

  // ── 三种观法（驻佇心观·唯心识观·真如实观）──
  h+="<div class=section><h2>👁 三种观法 — 驻佇心观·唯心识观·真如实观</h2>";
  h+="<p style=font-size:0.8em;color:var(--text2);margin-bottom:10px>海云法师将《占察善恶业报经》(大正藏 No.839, 天竺三藏菩提灯译) 中地藏菩萨为坚净信菩萨开示的<b>「二种观道」</b>——唯心识观与真如实观——纳入华严禅观体系，并在此基础上建立<b>「驻佇心观」</b>（停心）作为根本前行。三种观法由浅入深、由相入性，构成完整的华严禅观工程面。</p>";

  // ── 经典出处 ──
  h+="<div class=wu-door onclick='this.classList.toggle(\"open\")'><span class=arrow>▶</span><span class=ttl>📜 经典出处 — 《占察善恶业报经》原文</span><div class=body>";
  h+="<p style=font-size:0.78em;line-height:1.8;margin-bottom:8px><b>总纲：</b>「若欲依一实境界修信解者，应当学习二种观道。何等为二？一者唯心识观，二者真如实观。」</p>";
  h+="<p style=font-size:0.78em;line-height:1.8;margin-bottom:8px><b>利钝分判：</b>「其利根者，先已能知一切外诸境界，唯心所作，虚诳不实，如梦如幻等，决定无有疑虑。阴盖轻微，散乱心少。如是等人，即应学习真如实观。其钝根者，先未能知一切外诸境界，悉唯是心，虚诳不实故，染著情厚，盖障数起，心难调伏，应当先学唯心识观。」</p>";
  h+="<p style=font-size:0.78em;line-height:1.8><b>海云判摄：</b>法师称《占察善恶业报经》为<b>「小本华严」</b>，指出「禅观下手处的工程面就在《占察善恶业报经》里面」——该经是华严行法的前行指导，通过建立信心、堪为法器，方可进入禅观的技术面修行。<br>📎 <a href='https://cbeta.buddhism.org.hk/xml/T17/T17n0839_002.xml' target=_blank>CBETA 大正藏 T17n0839 原文</a></p>";
  h+="</div></div>";

  // ── 一、驻佇心观 ──
  h+="<div class=wu-door onclick='this.classList.toggle(\"open\")'><span class=arrow>▶</span><span class=ttl>一、驻佇心观（停心前行） — 以「停心」为基、「观心」为用</span><div class=body>";
  h+="<p style=font-size:0.8em;line-height:1.8;margin-bottom:6px>「驻佇心观」是海云法师华严禅观体系中<b>最根本的前行功夫</b>，核心次第为<b>「停心」→「观心」</b>。法师原话：「你要能够停下心来，然后，我们要观心！观心的整个过程没有那么容易，停心是一个前行，都办不到了，怎么观心啊？」</p>";

  h+="<p style=font-size:0.8em;color:var(--gold);margin-bottom:2px><b>🔹 停心（体·相二门）</b></p>";
  h+="<p style=font-size:0.78em;line-height:1.8;margin-bottom:6px><b>体上停心：</b>心念不起，六根对六尘境界不会攀缘——「心要停止妄想，其它随其自然！如果是用你的意识形态去推动它，那就一点都不对了！」<br><b>相上停心：</b>不要自己妄加猜测、攀缘分别——「这个人怎样？那个人怎样？这句话什么意思？」统统放下。停心的标准是——「心是不是静止下来，像墙壁一样，动都不动！这个叫停心。」</p>";

  h+="<p style=font-size:0.8em;color:var(--gold);margin-bottom:2px><b>🔹 四种停心方法</b></p>";
  h+="<p style=font-size:0.78em;line-height:1.8;margin-bottom:6px>① <b>参话头：</b>「看话头就是把心停在那里——在话头上！然后，渐渐的就会浮现你的心理作用。」守住「念佛是谁？」「未生之前，什么样子？」等话头。<br>② <b>置心一处：</b>将心安在鼻端风门，心跑掉就拉回来——「若心他缘，摄之令返」。<br>③ <b>数息/随息：</b>从数呼吸入手，过渡到随法，心自然安住。<br>④ <b>依禅堂规矩：</b>该动则动、该静则静、该跑则跑、该坐则坐，身心放下，自然停心。</p>";

  h+="<p style=font-size:0.8em;color:var(--gold);margin-bottom:2px><b>🔹 停心之后：观心</b></p>";
  h+="<p style=font-size:0.78em;line-height:1.8;margin-bottom:6px>停心之后才能真正<b>「观心」</b>——看清楚六根对六尘境界是如何作用的，心对色声香味触法的整个反应过程明明白白，这中间「没有任何推理、没有任何意识形态」，才是标准的观心。法师强调：「不停心你看不到！」</p>";

  h+="<p style=font-size:0.8em;color:var(--gold);margin-bottom:2px><b>🔹 修验证验（六项自检标准）</b></p>";
  h+="<p style=font-size:0.78em;line-height:1.8;margin-bottom:4px>停心成就后，十功德现前。海云法师列出六项自我检验标准：<b>空、明、定、智、善心、柔软</b>——「停住心后，善心、柔软心自然流露，与天地宇宙、一切众生相应，生命改造便从此开始。」</p>";

  h+="<p style=font-size:0.75em;color:var(--text2);margin-top:6px>📎 出处：海云继梦《华严禅行法—禅观》第四集 (fjdh.cn 逐字稿) · <a href='https://www.fjdh.cn/wumin/2013/11/165329303084.html' target=_blank>文字稿</a> · <a href='https://www.youtube.com/results?search_query=%E6%B5%B7%E9%9B%B2%E7%B9%BC%E5%A4%A2+%E7%A6%AA%E8%A7%80+%E7%AC%AC%E5%9B%9B%E9%9B%86' target=_blank>▶ YouTube</a> · <a href='https://search.bilibili.com/all?keyword=%E6%B5%B7%E4%BA%91%E7%BB%A7%E6%A2%A6+%E7%A6%85%E8%A7%82+%E7%AC%AC%E5%9B%9B%E9%9B%86' target=_blank>📺 Bilibili</a></p>";
  h+="</div></div>";

  // ── 二、唯心识观 ──
  h+="<div class=wu-door onclick='this.classList.toggle(\"open\")'><span class=arrow>▶</span><span class=ttl>二、唯心识观（毗钵舍那·钝根先修） — 守记内心·知唯是心</span><div class=body>";
  h+="<p style=font-size:0.8em;line-height:1.8;margin-bottom:6px>唯心识观出自《占察经》，海云法师将其定位为华严禅观工程面的<b>核心入门观法</b>，对应<b>毗钵舍那（观）</b>，法相宗所依。适用于<b>钝根行者</b>（染著情厚、盖障数起、心难调伏者）。</p>";

  h+="<p style=font-size:0.8em;color:var(--gold);margin-bottom:2px><b>🔹 经典定义</b></p>";
  h+="<p style=font-size:0.78em;line-height:1.8;margin-bottom:6px>「学唯心识观者，所谓于一切时一切处，随身口意所有作业，悉当观察，<b>知唯是心</b>。乃至一切境界，若心住念，皆当察知，勿令使心无记攀缘，不自觉知。于念念间，悉应观察。」<br>「当知一切境界自无分别想故……一切法唯心想生。若使离心，则无一法一相而能自见有差别也。」—— 《占察善恶业报经》卷下</p>";

  h+="<p style=font-size:0.8em;color:var(--gold);margin-bottom:2px><b>🔹 两大修行重点</b></p>";
  h+="<table class=v-table style='font-size:0.78em'><tr><th style=width:20%>要点</th><th>说明</th><th style=width:35%>海云法师开示</th></tr>";
  h+="<tr><td><b>守记内心</b><br>(正面训练)</td><td>对身·语·意三业念念清楚、事事明白，每一个动作细节都清清楚楚了知</td><td>「常应如是守记内心，知唯妄念，无实境界，勿令休废，是名修学唯心识观。」</td></tr>";
  h+="<tr><td><b>避免无记攀缘</b><br>(反面警惕)</td><td>心不知自己在做什么的惯性行为——口头禅（「嗯…」「这个…」）、无意识撩头发、摸鼻子等</td><td>「当你处于无记攀缘时，心就用不上——你对自己的身语意业观得不清楚，因为全是惯性。」</td></tr>";
  h+="</table>";

  h+="<p style=font-size:0.8em;color:var(--gold);margin-bottom:2px><b>🔹 具体训练方法（「让妄想摄心」）</b></p>";
  h+="<p style=font-size:0.78em;line-height:1.8;margin-bottom:6px>海云法师在2013年高雄《占察经》开示中给出具体操作：<br>① <b>闭眼抬手训练：</b>「坐着，眼睛闭起来，手慢慢抬起来——手在哪里？你知道吗？手在做什么？你知道吗？要很清楚地感知到，清清楚楚地知道。」因为专注感知手部动作时，「没有办法想别的东西，一想别的，手去了哪里就不知道了」——此即「摄心」。<br>② <b>行禅：</b>走路走得很慢，脚步慢慢抬起→停→慢慢放下，对每一个动作细节都清清楚楚了知——「这个就是唯心识观。」<br>③ <b>心法口诀：</b>「唯心识观就是不用大脑——停止五官、五尘、五识的识性运作，让灵性生命浮现出来。」</p>";

  h+="<p style=font-size:0.8em;color:var(--gold);margin-bottom:2px><b>🔹 修行成就</b></p>";
  h+="<p style=font-size:0.78em;line-height:1.8;margin-bottom:4px>得<b>「色寂三昧」</b>——「当知如是唯心识观，名为最上智慧之门。所谓能令其心猛利，长信解力，疾入空义，得发无上大菩提心故。」（入圆五品观行即佛位）</p>";

  h+="<p style=font-size:0.75em;color:var(--text2);margin-top:8px>📎 出处：海云继梦 2013年高雄《占察善恶业报经》开示 · 2014年台中《占察经略解》(32集) · 《非常占察经》讲记(一)(二)册 · <a href='https://www.fjdh.cn/wumin/2013/09/155711285715.html' target=_blank>文字稿: 让妄想摄心的训练</a> · <a href='https://www.youtube.com/results?search_query=%E6%B5%B7%E9%9B%B2%E7%B9%BC%E5%A4%A2+%E5%8D%A0%E5%AF%9F%E7%B6%93' target=_blank>▶ YouTube</a> · <a href='https://search.bilibili.com/all?keyword=%E6%B5%B7%E4%BA%91%E7%BB%A7%E6%A2%A6+%E5%8D%A0%E5%AF%9F%E5%96%84%E6%81%B6%E4%B8%9A%E6%8A%A5%E7%BB%8F' target=_blank>📺 Bilibili</a></p>";
  h+="</div></div>";

  // ── 三、真如实观 ──
  h+="<div class=wu-door onclick='this.classList.toggle(\"open\")'><span class=arrow>▶</span><span class=ttl>三、真如实观（奢摩他·利根直修） — 思惟心性·无生无灭</span><div class=body>";
  h+="<p style=font-size:0.8em;line-height:1.8;margin-bottom:6px>真如实观与唯心识观并列，同出《占察经》，海云法师将其定位为<b>更深一层的观法</b>，对应<b>奢摩他（止）</b>，法性宗所依。适用于<b>利根行者</b>（阴盖轻微、散乱心少、已知外境唯心者）。</p>";

  h+="<p style=font-size:0.8em;color:var(--gold);margin-bottom:2px><b>🔹 经典定义</b></p>";
  h+="<p style=font-size:0.78em;line-height:1.8;margin-bottom:6px>「若学习真如实观者，思惟心性<b>无生无灭</b>，不住见闻觉知，永离一切分别之想，渐渐能过空处、识处、无少处、非想非非想处等定境界相，得<b>相似空三昧</b>。」—— 《占察善恶业报经》卷下<br>「得相似空三昧时，识想受行粗分别相不现在前……展转能入<b>心寂三昧</b>。得是三昧已，即复能入<b>一行三昧</b>。入是一行三昧已，见佛无数，发深广行心，住<b>坚信位</b>。」</p>";

  h+="<p style=font-size:0.8em;color:var(--gold);margin-bottom:2px><b>🔹 修行要义</b></p>";
  h+="<p style=font-size:0.78em;line-height:1.8;margin-bottom:6px>① <b>不缘外境、反观自性：</b>类似观音菩萨「反闻闻自性」——「永离一切分别之想」，直接体证心性本自不生不灭。<br>② <b>超越四空定：</b>渐渐能过空无边处、识无边处、无所有处、非想非非想处等定境界相——不走四禅八定之路。<br>③ <b>照见五蕴皆空：</b>「识想受行粗分别相不现在前」——即《心经》「照见五蕴皆空」的境界，超越三界六道。<br>④ <b>海云判摄：</b>「唯心识观是让你了解这个心的存在跟作用——它像流水一样，前念接后念，一直过来。真如实观就是直接去看那个源头——心性的本源，无生无灭的那个。」</p>";

  h+="<p style=font-size:0.8em;color:var(--gold);margin-bottom:2px><b>🔹 修证次第</b></p>";
  h+="<table class=v-table style='font-size:0.78em'><tr><th style=width:22%>证量</th><th>说明</th></tr>";
  h+="<tr><td><b>相似空三昧</b></td><td>初步证入，识想受行粗分别相不现前。超越四空定等境界相</td></tr>";
  h+="<tr><td><b>心寂三昧</b></td><td>「从是修学，为善知识大慈悲者守护长养，是故离诸障碍，勤修不废」</td></tr>";
  h+="<tr><td><b>一行三昧</b></td><td>见佛无数，发深广行心，住坚信位——于奢摩他、毗婆舍那二种观道决定信解</td></tr>";
  h+="</table>";

  h+="<p style=font-size:0.75em;color:var(--text2);margin-top:8px>📎 出处：海云继梦《非常占察经》讲记第三册 · Apple Podcast/Spotify「普賢乘華嚴宗」S18 (46集) · <a href='https://podcasts.apple.com/au/podcast/%E6%99%AE%E8%B3%A2%E4%B9%98%E8%8F%AF%E5%9A%B4%E5%AE%97/id1523368889' target=_blank>🎙 Apple Podcast</a> · <a href='https://open.spotify.com/show/2ZDlq4cOOiynQvlzPARkmc' target=_blank>🎧 Spotify</a></p>";
  h+="</div></div>";

  // ── 三种观法总持 ──
  h+="<div class=wu-door onclick='this.classList.toggle(\"open\")'><span class=arrow>▶</span><span class=ttl>📐 三种观法总持 — 修行次第对照表</span><div class=body>";
  h+="<table class=v-table style='font-size:0.78em'><tr><th>维度</th><th>驻佇心观</th><th>唯心识观</th><th>真如实观</th></tr>";
  h+="<tr><td><b>定位</b></td><td>根本前行·停心工程</td><td>毗钵舍那（观）·法相宗</td><td>奢摩他（止）·法性宗</td></tr>";
  h+="<tr><td><b>经典依据</b></td><td>《华严经》+ 禅门话头传统</td><td>《占察善恶业报经》卷下</td><td>《占察善恶业报经》卷下</td></tr>";
  h+="<tr><td><b>适用根器</b></td><td>一切行者（共通前行）</td><td>钝根（染著情厚·心难调伏）</td><td>利根（散乱心少·已知唯心）</td></tr>";
  h+="<tr><td><b>核心操作</b></td><td>停妄想→起观照<br>参话头/置心一处/数息</td><td>守记内心·知唯是心<br>行禅/闭眼抬手/摄心训练</td><td>思惟心性无生无灭<br>反观自性·永离分别想</td></tr>";
  h+="<tr><td><b>修行成果</b></td><td>空·明·定·智·善心·柔软<br>（六项自检十功德现前）</td><td>色寂三昧<br>（入圆五品观行即佛位）</td><td>相似空三昧→心寂三昧<br>→一行三昧（住坚信位）</td></tr>";
  h+="<tr><td><b>在华严体系中的位置</b></td><td>资粮道·发心工程</td><td>前行·内摄工程（工程面）</td><td>正行·等持工程（内观）</td></tr>";
  h+="<tr><td><b>海云法师核心开示</b></td><td>「停心以后我们才能观心——不停心你看不到！」</td><td>「唯心识观就是不用大脑——让灵性生命浮现出来。」</td><td>「直接去看那个源头——心性的本源，无生无灭的那个。」</td></tr>";
  h+="</table>";
  h+="</div></div>";

  // ── 讲法资源汇总 ──
  h+="<div class=wu-door onclick='this.classList.toggle(\"open\")'><span class=arrow>▶</span><span class=ttl>📚 三种观法·讲法资源汇总</span><div class=body>";
  h+="<table class=v-table style='font-size:0.78em'><tr><th>类型</th><th>资源名称</th><th>规模/详情</th><th>获取方式</th></tr>";
  h+="<tr><td>📖 书籍</td><td>《非常占察经》一·二·三册<br>海雲和上《占察善恶业报经》讲记</td><td>三册·空庭书苑出版<br>ISBN: 9789867484918 / 4932<br>2015-2017年</td><td><a href='https://www.got1shop.com/goods.php?id=281160' target=_blank>购买</a> · <a href='https://webpac.taichung.gov.tw/bookDetail/670127' target=_blank>图书馆</a></td></tr>";
  h+="<tr><td>🎙 播客</td><td>普賢乘華嚴宗 · S18<br>《佔察善惡業報經》</td><td><b>46集</b>（已完结）<br>2013年高雄/台北开示</td><td><a href='https://podcasts.apple.com/au/podcast/%E6%99%AE%E8%B3%A2%E4%B9%98%E8%8F%AF%E5%9A%B4%E5%AE%97/id1523368889' target=_blank>Apple Podcast</a> · <a href='https://open.spotify.com/show/2ZDlq4cOOiynQvlzPARkmc' target=_blank>Spotify</a></td></tr>";
  h+="<tr><td>📺 视频</td><td>《占察善恶业报经》<br>大華嚴寺 | 海雲和上 @ 檳城</td><td>2013年 720P 46集<br>2014年 台中略解 32集<br>东南亚弘法系列 5集</td><td><a href='https://www.youtube.com/results?search_query=%E6%B5%B7%E9%9B%B2%E7%B9%BC%E5%A4%A2+%E5%8D%A0%E5%AF%9F%E5%96%84%E6%81%B6%E6%A5%AD%E5%A0%B1%E7%B6%93' target=_blank>▶ YouTube</a> · <a href='https://search.bilibili.com/all?keyword=%E6%B5%B7%E4%BA%91%E7%BB%A7%E6%A2%A6+%E5%8D%A0%E5%AF%9F%E5%96%84%E6%81%B6%E4%B8%9A%E6%8A%A5%E7%BB%8F' target=_blank>📺 Bilibili</a></td></tr>";
  h+="<tr><td>📝 文字</td><td>《华严禅行法—禅观》<br>《占察善恶业报经》讲记逐字稿</td><td>第四集: 五停心观<br>fjdh.cn 收录多集文字稿</td><td><a href='https://www.fjdh.cn/wumin/2013/11/165329303084.html' target=_blank>禅观第四集</a> · <a href='https://www.fjdh.cn/wumin/2013/09/155711285715.html' target=_blank>停心·观心</a></td></tr>";
  h+="<tr><td>🌐 官网</td><td>大华严寺 · 占察行法班</td><td>每周日 14:00-17:00<br>中和分会四楼大殿</td><td><a href='https://www.huayenworld.org/buddhist-practice-curriculum/the-ksitigarbha-divination-method-buddhist-practice-curriculum/' target=_blank>占察行法页面</a></td></tr>";
  h+="<tr><td>🎧 音频</td><td>北美《占察善恶业报经》</td><td>8集音频 + 3集行法实践</td><td>海云继梦全集移动硬盘</td></tr>";
  h+="</table>";

  h+="<p style=font-size:0.72em;color:var(--text2);margin-top:8px>⚠ <b>说明：</b>北京/各地华严学会定期举办「占察行法班」结界共修，依蕅益大师《占察行法仪轨》进行，包含五悔法（祈请·忏悔·随喜·发愿·迴向）、称念礼拜过去七佛及五十三佛、拜忏后静坐持咒摄心。需先完成结界前行方可参加——「戒不清净，二观决不易修；二观不修，一实何由证契？」（蕅益大师）</p>";
  h+="</div></div>";

  h+="</div>";

  // ── 十信法门（增强版）─
  h+="<div class=section><h2>📊 十信法门 · 果位对应</h2>";
  h+="<p style=font-size:0.8em;color:var(--text2);margin-bottom:6px>海云法师将传统声闻「四果」与华严「十信位」逐级对应。「破根本无明」是初果的门槛而非彻悟终点——法师: 「破根本无明才叫做悟后起修！」</p>";
  h+="<table class=v-table><tr><th>传统果位</th><th>华严信位</th><th>关键标准</th></tr>";
  h+="<tr><td>初果（预流果）</td><td>初信位</td><td>「舍识用根」——能看到根性。开始探寻人生价值与生命意义，能自我约束反省</td></tr>";
  h+="<tr><td>—</td><td>二信位</td><td>确认菩提心。净化禅训练·毗卢遮那七支坐相·收心工程完成·具足三要件九条目</td></tr>";
  h+="<tr><td>二果（一来果）</td><td>三信位</td><td>开始运用「观照」技术。具轻安三相+天王三德·忍可天王定·可成立檀道场</td></tr>";
  h+="<tr><td>—</td><td>四信位</td><td>安般守意工程: 端身正坐，置心于风门，调息，使心不乱——试修心法的起步</td></tr>";
  h+="<tr><td>三果（不还果）</td><td>五信位</td><td>—</td></tr>";
  h+="<tr><td>四果向</td><td>六信位</td><td>—</td></tr>";
  h+="<tr><td>四果（阿罗汉·破我执）</td><td>七信位</td><td>我法二执尚未双破</td></tr>";
  h+="<tr><td>发心破法执</td><td>八信位</td><td>传统「回小向大」在八、九信位之间完成</td></tr>";
  h+="<tr><td>我执法执双破</td><td>九信位</td><td>—</td></tr>";
  h+="<tr><td>十信位圆满</td><td>十信位</td><td>「能所双泯」=「照见五蕴皆空」·入法界·成<b>圆教初住位</b></td></tr>";
  h+="</table>";
  h+="<p style=font-size:0.78em;color:var(--text2);margin-top:4px>十信位之后: <b>初住位至七地</b>（37位·正行·对应金刚界曼荼罗37尊）→<b>八地至妙觉</b>（5位·无功用行·究竟圆满）——共<b>42位</b>圆满佛果。</p></div>";

  // ── 验证机制 ──
  h+="<div class=section><h2>✅ 验证机制 — 200+测验 & 归零重修</h2>";
  h+="<div class=stage-box>法师强调修行进程「绝对理性」「不能讲人情」: 全程设有<b>两百余种具体测验</b>——包括制造顺境（提供美食）诱发贪着反应、制造逆境（当众令难堪）激发嗔心反应，检验是否仍被习气带走。<br><br><b>失败重修的规则极为严格</b>: 并非退回上一级，而是<b>打回初信（初果）从头开始</b>——法师: 「四果再重修，就从这个地方开始，再从初果开始。」</div></div>";

  // ── 三摩地三阶段 ──
  h+="<div class=section><h2>🎯 三摩呬多·三摩钵底·三摩地</h2><table class=v-table><tr><th>名相</th><th>梵语</th><th>定位</th><th>操作要点</th></tr>";
  h+="<tr><td>三摩呬多</td><td>Samāhita</td><td>入定前·专注调心</td><td>粗住→细住→欲界定。排除妄想执著</td></tr>";
  h+="<tr><td>三摩钵底</td><td>Samāpatti</td><td>以观导定·定慧双运</td><td>勘定三界定。须善知识勘定</td></tr>";
  h+="<tr><td>三摩地</td><td>Samādhi</td><td>究竟·心一境性</td><td>出入自在。破法执我执</td></tr>";
  h+="</table><p style='font-size:0.75em;color:var(--text2);margin-top:6px'>⚠ 术语说明: 据主流汉传辞书(如《瑜伽师地论》注疏)，「三摩地」(samādhi)标准译语为「等持」，「三摩钵底」(samāpatti)标准译语为「等至」。大华严寺官方资料中的配对与此恰好相反——此系道场自身的术语使用习惯，本文如实呈现，读者可自行留意。</p></div>";

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
    {t:'📖 华严经讲记系列',d:'《华严经导读》(三册)《探玄记悬谈讲记》(四册)《世主妙严品》《光明觉品》《净行品》《贤首品》《明法品》《普贤三昧品》《普贤行品》《四圣谛品》等单品讲记。2006-2010北京广化寺《四十华严》全本讲记。',yt:'华严经+海云继梦',bl:'华严经+海云继梦'},
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
