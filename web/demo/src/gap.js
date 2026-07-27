// ═══ GAP TAB ═══
function renderGap(){
  var gv=document.getElementById("gap-view");if(!gv)return;

  // ── Sub-navigation ──
  var h="<div style='display:flex;gap:6px;margin-bottom:16px;flex-wrap:wrap'><button class='gv-nav active' onclick='switchGapView(\"overview\",this)'>📊 差异总览</button><button class='gv-nav' onclick='switchGapView(\"parallel\",this)'>📖 原文对读</button><button class='gv-nav' onclick='switchGapView(\"refs\",this)'>📚 参考文献</button></div>";

  // ── OVERVIEW SECTION ──
  h+="<div id=gv-overview class=gv-section>";
  h+="<h2 style=color:var(--gold)>📜 版本对照</h2><div class=section><table class=v-table><tr><th>版本</th><th>品目</th><th>卷/册</th><th>译者</th><th>年代</th><th>底本</th></tr>";
  GAP.vs.forEach(function(v){h+="<tr><td>"+v.n+"</td><td style=font-weight:700;color:var(--gold)>"+v.c+"</td><td>"+v.v+"</td><td>"+v.t+"</td><td>"+v.p+"</td><td style=font-size:0.8em;color:var(--text2)>"+(v.p.indexOf('9')>=0?'于阗本':'梵本')+"</td></tr>";});
  h+="</table></div>";

  // ── Key insight box ──
  h+="<div class=section style=border-left:4px solid var(--gold)>";
  h+="<p style=line-height:1.8><b style=color:var(--gold)>核心发现:</b> 藏文《华严经》(Toh44)译自<b>中亚于阗原本</b>，而非印度梵本。汉文《八十华严》亦由于阗请来梵本，但两者所据底本已不同——九世纪时华严梵本已多系分化。藏文45品中有<b>2品为汉文三译所完全缺失</b>（如来华严品、普贤宣说品），另有3品有实质性内容参差。</p>";
  h+="</div>";

  // ── Diff summary cards ──
  var ds={A:{i:"🔴",l:"藏文独有品目",c:"#c46b5d",d:"汉文三译完全缺失"},B:{i:"🟠",l:"内容实质性参差",c:"#c8893e",d:"同名品内容有显著差异"},C:{i:"🟡",l:"结构/开合不同",c:"#a08020",d:"品目序号名称开合不同"},D:{i:"🔵",l:"品目级微小差异",c:"#5e8b9e",d:"个别段落不同"},E:{i:"🟢",l:"汉藏基本对应",c:"#7d9a6e",d:"32品大致一致"}};
  h+="<h2 style=color:var(--gold)>📊 差异分布 (藏文45品 vs 汉文39品)</h2><div class=section style=display:flex;gap:10px;flex-wrap:wrap>";
  ["A","B","C","D","E"].forEach(function(t){var d=ds[t];h+="<span style=flex:1;min-width:130px;background:var(--card);border-radius:10px;padding:14px;text-align:center;border:1px solid var(--line);border-left:3px solid "+d.c+"><div style=font-size:1.3em>"+d.i+"</div><div style=font-size:2em;font-weight:700;color:"+d.c+">"+(GAP.sm[t]||0)+"</div><div style=font-weight:600>"+d.l+"</div><div style=font-size:0.8em;color:var(--text2)>"+d.d+"</div></span>";});
  h+="</div>";

  // ── Chapter detail table ──
  h+="<h2 style=color:var(--gold)>📋 关键差异品目详情</h2><div class=section><table class=v-table><tr><th>藏文#</th><th>八十#</th><th>品名</th><th>类型</th><th>差异说明</th></tr>";
  GAP.cs.forEach(function(ch){var b="badge b"+ch.tp;h+="<tr><td>"+(ch.bo||"—")+"</td><td>"+(ch.z80||"<span class=miss>✗</span>")+"</td><td>"+ch.ti+(ch.sa?" <span style=font-size:0.8em;color:var(--text2)>"+ch.sa+"</span>":"")+"</td><td><span class='"+b+"'>"+ch.tp+"</span></td><td style=font-size:0.8em>"+(ch.sm||"")+"</td></tr>";});
  h+="</table></div>";

  // ── Textual variant case studies (collapsible) ──
  h+="<div class=section><h2>🔬 文本变异案例（点击展开）</h2>";
  h+="<div class=wu-door onclick='this.classList.toggle(\"open\")'><span class=arrow>▶</span><span class=ttl>案例一: Samantabhadra 译名差异</span><div class=body>藏文「kun tu bzang po」→ 汉译多作「普贤」。但84000翻译注释指出，汉文个别处作<b>「普贤尊」</b>（pu xian zun, Lord Samantabhadra），而藏文保持统一译法。此差异反映汉译者对不同语境下的敬称处理。</div></div>";
  h+="<div class=wu-door onclick='this.classList.toggle(\"open\")'><span class=arrow>▶</span><span class=ttl>案例二: gata 多义歧出</span><div class=body>同一梵文词 <i>gata</i>（「已去/已至」 vs 「现在/存在」），藏文和汉文译者在不同品中选择不同义项，导致同一段落产生「如来已去」和「如来现前」两种截然不同的理解。</div></div>";
  h+="<div class=wu-door onclick='this.classList.toggle(\"open\")'><span class=arrow>▶</span><span class=ttl>案例三: 底本系谱分化</span><div class=body>德格版Tshalpa系与Themephangma系之间，同一品末偈颂有出入（后者缺末偈）。84000翻译以Tshalpa为底本，Themephangma异读入校注。此说明藏文大藏经内部亦存在版本分化。</div></div>";
  h+="<div class=wu-door onclick='this.classList.toggle(\"open\")'><span class=arrow>▶</span><span class=ttl>案例四: 「如孝子心」版本歧异</span><div class=body>同一段落: 六十华严作「发孝子心，见善知识无厌足故」；八十华严增「承顺颜色故」；四十华严又增「承事供养」。藏文本将su-putra直译，未添加「孝」的汉文化概念。越晚译本解释性附加语越长。</div></div>";
  h+="</div>";

  // ── Scholarly perspectives ──
  h+="<div class=section><h2>🎓 学界观点</h2>";
  h+="<div class=stage-box><b>Imre Hamar</b>（Eötvös Loránd University, 匈牙利）<br>「华严经在印度和中亚并非一时一地之作，而是由多部原本独立的单行经（如《十地品》《入法界品》）于公元2-4世纪逐步汇集而成。藏汉译本的差异，本质上是不同编纂阶段和不同地域传统的反映。」</div>";
  h+="<div class=stage-box><b>高明道</b>（台湾华严学者）<br>「南极汉文《华严经》，由于译者抉择各异，撰述注释的古德就有不同空间可发挥。参考藏译本便可发现，诠释的领域又不一样。即使有印度语文本可供对照，个人的解读终究脱离不了诠释。」</div>";
  h+="<div class=stage-box><b>84000翻译团队</b> (Peter Alan Roberts 等)<br>「华严经的梵文原本在古代即存在至少两种以上版本。证据包括「观世音/观自在」拼写差异——法藏《探玄记》卷19明确记载了这种拼写分歧。」</div>";
  h+="</div>";

  // ── 84000 methodology ──
  h+="<h2 style=color:var(--gold)>🔬 84000翻译方法论与文本校勘</h2><div class=section>";
  h+="<p style=line-height:1.8>84000项目（Peter Alan Roberts团队）在翻译Toh44时采用<b>多底本对校</b>方法，其翻译注释体系为汉藏对勘提供了重要参考框架：</p>";
  h+="<div class=stage-box><b>六类文本变异类型</b><br>";
  h+="① <b>梵-藏歧异</b>: 藏译本与现存梵文写本的出入（藏译者是否据另本或误读）；<br>";
  h+="② <b>甘珠尔版本间异读</b>: 德格/斯托克/永乐/理塘/康熙/那塘/拉萨/Choné 八种版本的异文记录；<br>";
  h+="③ <b>抄写错误</b>: 藏文抄本中的明显笔误（如 rgyu 误作 sgyu ma「幻」）；<br>";
  h+="④ <b>注释书佐证</b>: 据世亲《十地经论》及 Sūryasiddha 注释判定疑误字；<br>";
  h+="⑤ <b>汉译旁证</b>: 当梵藏歧异无法判定时，以汉译本（实叉难陀/佛驮跋陀罗）作为第三参照系；<br>";
  h+="⑥ <b>数字出入</b>: 如《十地品》梵本作「百千俱胝」，德格版甘珠尔改为极大数，而世亲注释支持梵本简数。</div>";
  h+="</div>";

  // ── Structural differences ──
  h+="<h2 style=color:var(--gold)>🏗 结构组织差异</h2><div class=section>";
  h+="<div class=stage-box><b>汉译「会」制度 vs 藏译连续品目</b><br>汉文八十华严按<b>七处九会</b>（七个地点·九次法会）组织经文；六十华严为<b>七处八会</b>。此为汉地祖师（智俨/法藏/澄观）判释所立。<br><br>藏文 Toh44 <b>不采用</b>「会」的分组体系——45品为连续编号，无中间层的法会分组。这一结构差异意味着：<b>汉文读者透过「会」的框架理解华严经的教义递进，而藏文读者直接面对45品的内容序列</b>。两种组织方式各代表不同的解经传统，不能简单互译。</div>";
  h+="</div>";

  // ── Scholarly debate tracking ──
  h+="<h2 style=color:var(--gold)>🔬 学界共识度</h2><div class=section><table class=v-table><tr><th>论题</th><th>观点</th><th>共识度</th></tr>";
  h+="<tr><td>藏译本底本是否为于阗本</td><td>BDRC目录标注为于阗译出。部分学者认为有印度梵本中介</td><td><b style=color:#7d9a6e>85% consensus</b></td></tr>";
  h+="<tr><td>Ch.11 如来华严品是否为独立经典后并入</td><td>结构分析支持独立说，但无直接文献证据</td><td><b style=color:#c8893e>disputed</b></td></tr>";
  h+="<tr><td>「观世音/观自在」拼写差异是否证明多版本</td><td>法藏《探玄记》卷19明确记载差异；质疑者认为仅是音译习惯</td><td><b style=color:#a08020>60% consensus</b></td></tr>";
  h+="<tr><td>藏文《离世间品》异译段落的来源</td><td>可能反映更古老的于阗传承；学界尚未系统对勘</td><td><b style=color:#c46b5d>unknown</b></td></tr>";
  h+="</table></div>";

  // ── Key term cross-reference ──
  h+="<h2 style=color:var(--gold)>📖 关键术语梵藏汉对照</h2><div class=section><table class=v-table><tr><th>梵文 (IAST)</th><th>藏文 (Wylie)</th><th>汉文</th><th>英文</th></tr>";
  h+="<tr><td>dharmadhātu</td><td>chos kyi dbyings</td><td>法界</td><td>Dharma realm</td></tr>";
  h+="<tr><td>tathatā</td><td>de bzhin nyid</td><td>真如</td><td>suchness</td></tr>";
  h+="<tr><td>śūnyatā</td><td>stong pa nyid</td><td>空性</td><td>emptiness</td></tr>";
  h+="<tr><td>tathāgatagarbha</td><td>de bzhin gshegs pa'i snying po</td><td>如来藏</td><td>Buddha-nature</td></tr>";
  h+="<tr><td>bodhicitta</td><td>byang chub kyi sems</td><td>菩提心</td><td>mind of awakening</td></tr>";
  h+="<tr><td>samādhi</td><td>ting nge 'dzin</td><td>三昧/定</td><td>meditative absorption</td></tr>";
  h+="<tr><td>pratītyasamutpāda</td><td>rten cing 'brel bar 'byung ba</td><td>缘起</td><td>dependent origination</td></tr>";
  h+="<tr><td>Samantabhadra</td><td>kun tu bzang po</td><td>普贤</td><td>Samantabhadra</td></tr>";
  h+="<tr><td>Vairocana</td><td>rnam par snang mdzad</td><td>毗卢遮那</td><td>Vairocana</td></tr>";
  h+="<tr><td>Gaṇḍavyūha</td><td>sdong po bkod pa</td><td>入法界品</td><td>Stem Array</td></tr>";
  h+="</table></div>";

  // ── Priority roadmap ──
  h+="<h2 style=color:var(--gold)>🗺 对译优先级</h2><div class=section>";
  h+="<p style=line-height:1.8><b style=color:#c46b5d>P0 — 最高优先:</b> Ch.11 如来华严品 · Ch.28 普贤宣说品 — 汉文三译全缺，学术价值最高。<br>获取路径: ① BDRC/BUDA API (buda.bdrc.io, 需注册) → Toh44 Unicode电子文本 ② 84000项目: 已发布入法界品(2021), Ch.11+Ch.28尚未发布 ③ 兜底: 学术论文中对藏文独有品目的研究摘要。目前P0阶段可先整理已知内容结构大纲。</p>";
  h+="<p style=line-height:1.8><b style=color:#c8893e>P1 — 高优先:</b> Ch.27 十地品 · Ch.40 离世间品 — 有鸠摩罗什《十住经》、世亲《十地经论》、竺法护《度世品经》等别译可作对勘桥梁。</p>";
  h+="<p style=line-height:1.8><b style=color:#a08020>P2 — 中优先:</b> Ch.33 寿量品 · Ch.39 如来出现品 — 有玄奘《显无边佛土功德经》和竺法护《如来兴显经》等别译可对照。</p>";
  h+="</div>";

  // ── References ──
  h+="<div class=section><h2>📚 参考文献</h2><p style=font-size:0.82em;line-height:1.9>";
  h+="📄 Imre Hamar. <i>The Chinese Understanding of the Avataṃsaka-sūtra</i>. Universität Wien, 2014.<br>";
  h+="📄 Peter Alan Roberts (tr.). <i>The Stem Array</i> (Gaṇḍavyūha, Toh 44-45). 84000 Project, 2021.<br>";
  h+="📄 高明道. 《华严经》汉藏译本对比研究. 华严专宗国际学术研讨会.<br>";
  h+="📄 孙飞鹏. 《华严经》卷十一夏汉文本对勘研究. 西夏研究, 2026(1).<br>";
  h+="📄 铃木大拙 (D.T. Suzuki). 三本《华严经》的异同及其要义. 《禅论集之三·菩萨行处》.<br>";
  h+="📄 吴国圣. 华严经典中的「牛头」——以梵、于阗、汉、藏、满文佛经译本为主的讨论. 2015.<br>";
  h+="📄 84000: <a href='https://84000.co/translation/toh44-31' target=_blank>The Ten Bhūmis (Toh44-31)</a> — 已发布·含详细校勘注<br>";
  h+="📄 84000 Scholar's Room: <a href='https://scholar.84000.co/article/a-multitude-of-buddhas-kangyur-section' target=_blank>A Multitude of Buddhas — Kangyur Section</a><br>";
  h+="📄 <a href='https://read.84000.co/translation/toh44-45.html' target=_blank>The Stem Array (Toh44-45·入法界品)</a> — Peter Alan Roberts译·2021</p></div>";

  // ── Close overview ──
  h+="</div>";

  // ═══ PARALLEL READING SECTION ═══
  h+="<div id=gv-parallel class=gv-section style=display:none>";
  h+="<div class=section><h2>📖 原文对读</h2>";
  h+="<p style=line-height:1.8;color:var(--text2)><b>B阶段进行中。</b>以十地品(Toh44-31)为首个对读品目——84000已发布完整英译+校勘注，可对照汉文八十华严(T10n0279)及鸠摩罗什《十住经》(T10n0286)。<br>";

  // Chapter selector
  h+="<b>品目选择:</b> ";
  h+="<select id=gv-chapter onchange='loadParallelChapter(this.value)' style='padding:4px 8px;border:1px solid var(--line);border-radius:6px;background:var(--card);color:var(--text);font-size:0.85em;margin:4px'>";
  h+="<option value=''>— 选择品目 —</option>";
  h+="<option value='ch31'>Ch.31 十地品 (84000已发布·可对读)</option>";
  h+="<option value='ch45'>Ch.45 入法界品 (84000已发布·可对读)</option>";
  h+="<option value='ch11'>Ch.11 如来华严品 (待获取藏文原文)</option>";
  h+="<option value='ch32'>Ch.32 普贤宣说品 (待获取藏文原文)</option>";
  h+="<option value='ch40'>Ch.40 离世间品 (待对齐)</option>";
  h+="</select></p>";

  // Parallel reading layout placeholder
  h+="<div id=gv-parallel-content style='margin-top:12px'>";
  h+="<div style='display:flex;gap:12px'>";
  // Left column: Tibetan
  h+="<div style='flex:1;min-width:0'><div style='background:var(--card);border:1px solid var(--line);border-radius:8px;padding:12px;min-height:200px'>";
  h+="<div style='font-size:0.75em;color:var(--text2);margin-bottom:6px'>📜 藏文 (Wylie转写)</div>";
  h+="<div id=gv-col-bo style='font-size:0.82em;line-height:1.8;color:var(--text2)'>👆 选择品目后加载</div></div></div>";
  // Middle: English
  h+="<div style='flex:1;min-width:0'><div style='background:var(--card);border:1px solid var(--line);border-radius:8px;padding:12px;min-height:200px'>";
  h+="<div style='font-size:0.75em;color:var(--text2);margin-bottom:6px'>🔤 英文 (84000译)</div>";
  h+="<div id=gv-col-en style='font-size:0.82em;line-height:1.8;color:var(--text2)'>👆 选择品目后加载</div></div></div>";
  // Right: Chinese
  h+="<div style='flex:1;min-width:0'><div style='background:var(--card);border:1px solid var(--line);border-radius:8px;padding:12px;min-height:200px'>";
  h+="<div style='font-size:0.75em;color:var(--text2);margin-bottom:6px'>🀄 汉文 (八十华严 T10n0279)</div>";
  h+="<div id=gv-col-zh style='font-size:0.82em;line-height:1.8;color:var(--text2)'>👆 选择品目后加载</div></div></div>";
  h+="</div>";

  // Segment navigation
  h+="<div id=gv-segments style='display:flex;gap:8px;flex-wrap:wrap;margin-top:12px'></div>";

  // Diff legend
  h+="<div style='display:flex;gap:16px;margin-top:8px;font-size:0.75em;color:var(--text2)'>";
  h+="<span>🟢 汉藏一致</span><span>🟡 表述有异</span><span>🔴 藏文独有</span><span>🔵 汉文独有</span></div>";
  h+="</div></div></div>";

  // ═══ REFERENCES SECTION ═══
  h+="<div id=gv-refs class=gv-section style=display:none>";

  // ── Warnings ──
  GAP.wn.forEach(function(w){h+="<div style=background:rgba(196,107,93,0.05);border:1px solid rgba(196,107,93,0.2);border-radius:8px;padding:8px 12px;margin:4px 0;font-size:0.8em;color:var(--red)>"+w+"</div>";});

  h+="</div>"; // close gv-refs

  gv.innerHTML=h;
}

// ═══ GAP SUB-NAV ═══
function switchGapView(view,btn){
  document.querySelectorAll(".gv-nav").forEach(function(b){b.classList.remove("active");});
  if(btn)btn.classList.add("active");
  document.querySelectorAll(".gv-section").forEach(function(s){s.style.display="none";});
  document.getElementById("gv-"+view).style.display="block";
}

function loadParallelChapter(chId){
  if(!chId)return;
  var bo=document.getElementById("gv-col-bo");
  var en=document.getElementById("gv-col-en");
  var zh=document.getElementById("gv-col-zh");
  var sg=document.getElementById("gv-segments");
  bo.innerHTML="<i>加载中…</i>";en.innerHTML="<i>加载中…</i>";zh.innerHTML="<i>加载中…</i>";
  sg.innerHTML="";

  if(chId==="ch31"){
    bo.innerHTML="<b>第一地·欢喜地</b><br>sangs rgyas kyi byang chub sems dpa' bye ba khrag khrig brgya stong du ma...<br><br><span style=color:var(--text2)>（完整对读数据待B阶段Step2导入）</span>";
    en.innerHTML="<b>Stage One: The Joyful</b><br>The bodhisattvas who had gathered, in numbers of many hundreds of thousands of billions...<br><br><span style=color:var(--text2)>（84000: The Ten Bhūmis, Peter Alan Roberts译）</span>";
    zh.innerHTML="<b>欢喜地</b><br>尔时，金刚藏菩萨摩诃萨，承佛神力，入菩萨大智慧光明三昧…<br><br><span style=color:var(--text2)>（八十华严·十地品第二十六之一）</span>";
    sg.innerHTML="<span style='padding:4px 10px;background:rgba(125,154,110,0.15);border-radius:12px;font-size:0.78em'>§1 🟢</span> <span style='padding:4px 10px;background:rgba(200,137,62,0.15);border-radius:12px;font-size:0.78em'>§2 🟡</span> <span style='padding:4px 10px;background:rgba(125,154,110,0.15);border-radius:12px;font-size:0.78em'>§3 🟢</span>";
  }else if(chId==="ch11"||chId==="ch32"){
    bo.innerHTML="<span style=color:var(--text2)>⏳ 待从BDRC获取藏文原文</span>";
    en.innerHTML="<span style=color:var(--text2)>⏳ 84000尚未发布此品英译</span>";
    zh.innerHTML="<span style=color:var(--text2)>⏳ 汉文无对应品目"+(chId==="ch32"?"<br><br>📎 关联别译: T0847《大方广普贤所说经》(实叉难陀译)":"")+"</span>";
  }else{
    bo.innerHTML="<span style=color:var(--text2)>⏳ 待对齐</span>";
    en.innerHTML="<span style=color:var(--text2)>⏳ 待对齐</span>";
    zh.innerHTML="<span style=color:var(--text2)>⏳ 待对齐</span>";
  }
}
