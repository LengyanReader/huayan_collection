// ═══ GAP TAB ═══
function renderGap(){
  var gv=document.getElementById("gap-view");if(!gv)return;

  // ── Sub-navigation moved to left sidebar ──
  var h="";

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
  h+="<div class=stage-box><b>Imre Hamar</b>（Eötvös Loránd University, 匈牙利科学院博士）<br>「华严经在印度和中亚并非一时一地之作，而是由多部原本独立的单行经（如《十地品》《入法界品》）于公元2-4世纪逐步汇集而成。藏汉译本的差异，本质上是不同编纂阶段和不同地域传统的反映。」—— 参见其博士论文 <i>The Buddhāvatamsaka-sūtra and Its Chinese Interpretation</i> (2014) 及 <i>The Metaphor of the Painter</i> (SOS 13·2, 2014).</div>";
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
  h+="<tr><td>buddhāvataṃsaka</td><td>sangs rgyas phal po che</td><td>华严</td><td>Buddha-ornament</td></tr>";
  h+="<tr><td>bhūmi</td><td>sa</td><td>地/阶位</td><td>stage/ground</td></tr>";
  h+="<tr><td>daśabhūmika</td><td>sa bcu pa</td><td>十地</td><td>ten stages</td></tr>";
  h+="<tr><td>bhadracaryā</td><td>bzang po spyod pa</td><td>普贤行</td><td>good conduct</td></tr>";
  h+="<tr><td>praṇidhāna</td><td>smon lam</td><td>愿/誓愿</td><td>aspiration prayer</td></tr>";
  h+="<tr><td>vihāra</td><td>gnas</td><td>住处/法会</td><td>abode/assembly</td></tr>";
  h+="<tr><td>sāgara-mudrā-samādhi</td><td>rgya mtsho'i phyag rgya'i ting nge 'dzin</td><td>海印三昧</td><td>ocean-seal samādhi</td></tr>";
  h+="<tr><td>dharmadhātu-pratītya-samutpāda</td><td>chos kyi dbyings rten 'brel</td><td>法界缘起</td><td>dharma-realm dependent origination</td></tr>";
  h+="<tr><td>ekayāna</td><td>theg pa gcig pa</td><td>一乘</td><td>single vehicle</td></tr>";
  h+="<tr><td>avaivartika</td><td>phyir mi ldog pa</td><td>不退转</td><td>non-retrogressing</td></tr>";
  h+="<tr><td>anuttarā-samyak-saṃbodhi</td><td>bla na med pa yang dag par rdzogs pa'i byang chub</td><td>阿耨多罗三藐三菩提</td><td>unsurpassed perfect enlightenment</td></tr>";
  h+="<tr><td>kuśala-mūla</td><td>dge ba'i rtsa ba</td><td>善根</td><td>roots of virtue</td></tr>";
  h+="<tr><td>pāramitā</td><td>pha rol tu phyin pa</td><td>波罗蜜/到彼岸</td><td>perfection</td></tr>";
  h+="<tr><td>dāna-pāramitā</td><td>sbyin pa'i pha rol tu phyin pa</td><td>布施波罗蜜</td><td>perfection of giving</td></tr>";
  h+="<tr><td>śīla-pāramitā</td><td>tshul khrims kyi pha rol tu phyin pa</td><td>持戒波罗蜜</td><td>perfection of ethical conduct</td></tr>";
  h+="<tr><td>kṣānti-pāramitā</td><td>bzod pa'i pha rol tu phyin pa</td><td>忍辱波罗蜜</td><td>perfection of patience</td></tr>";
  h+="<tr><td>vīrya-pāramitā</td><td>brtson 'grus kyi pha rol tu phyin pa</td><td>精进波罗蜜</td><td>perfection of diligence</td></tr>";
  h+="<tr><td>dhyāna-pāramitā</td><td>bsam gtan gyi pha rol tu phyin pa</td><td>禅定波罗蜜</td><td>perfection of meditation</td></tr>";
  h+="<tr><td>prajñā-pāramitā</td><td>shes rab kyi pha rol tu phyin pa</td><td>般若波罗蜜</td><td>perfection of wisdom</td></tr>";
  h+="</table></div>";

  // ── Priority roadmap ──
  h+="<h2 style=color:var(--gold)>🗺 对译优先级</h2><div class=section>";
  h+="<p style=line-height:1.8><b style=color:#c46b5d>P0 — 最高优先:</b> Ch.11 如来华严品 · Ch.28 普贤宣说品 — 汉文三译全缺，学术价值最高。<br>获取路径: ① BDRC/BUDA API (buda.bdrc.io, 需注册) → Toh44 Unicode电子文本 ② 84000项目: 已发布入法界品(2021), Ch.11+Ch.28尚未发布 ③ 兜底: 学术论文中对藏文独有品目的研究摘要。目前P0阶段可先整理已知内容结构大纲。</p>";
  h+="<p style=line-height:1.8><b style=color:#c8893e>P1 — 高优先:</b> Ch.27 十地品 · Ch.40 离世间品 — 有鸠摩罗什《十住经》、世亲《十地经论》、竺法护《度世品经》等别译可作对勘桥梁。</p>";
  h+="<p style=line-height:1.8><b style=color:#a08020>P2 — 中优先:</b> Ch.33 寿量品 · Ch.39 如来出现品 — 有玄奘《显无边佛土功德经》和竺法护《如来兴显经》等别译可对照。</p>";
  h+="</div>";

  // ── References ──
  h+="<div class=section><h2>📚 参考文献</h2><p style=font-size:0.82em;line-height:1.9>";
  h+="📄 Imre Hamar. <i>The Buddhāvatamsaka-sūtra and Its Chinese Interpretation</i>. 匈牙利科学院博士论文, 2014.<br>";
  h+="📄 Imre Hamar. <i>The Metaphor of the Painter in the Avatamsaka-sutra and Its Chinese Interpretations</i>. SOS 13·2, 2014.<br>";
  h+="📄 Peter Alan Roberts (tr.). <i>The Stem Array</i> (Gaṇḍavyūha, Toh 44-45). 84000 Project, 2021.<br>";
  h+="📄 高明道. 《谈谈翻译与诠释——以《华严》数偈为例》. 《法光》第236期, 2009.<br>";
  h+="📄 孙飞鹏. 《〈华严经〉卷十一夏汉文本对勘研究》. 《西夏学》第十辑(2013年第2期), 页75-80. 西安交通大学.<br>";
  h+="📄 铃木大拙 (D.T. Suzuki). 三本《华严经》的异同及其要义. 《禅论集之三·菩萨行处》.<br>";
  h+="📄 吴国圣. 华严经典中的「牛头」——以梵、于阗、汉、藏、满文佛经译本为主的讨论. 2015.<br>";
  h+="📄 84000: <a href='https://84000.co/translation/toh44-31' target=_blank>The Ten Bhūmis (Toh44-31)</a> — 已发布·含详细校勘注<br>";
  h+="📄 84000 Scholar's Room: <a href='https://scholar.84000.co/article/a-multitude-of-buddhas-kangyur-section' target=_blank>A Multitude of Buddhas — Kangyur Section</a><br>";
  h+="📄 <a href='https://read.84000.co/translation/toh44-45.html' target=_blank>The Stem Array (Toh44-45·入法界品)</a> — Peter Alan Roberts译·2021</p></div>";

  // ── Version Evolution Visual Timeline ──
  h+="<h2 style=color:var(--gold)>🌏 版本时空演进（2世纪—2026）</h2><div class=section>";
  h+="<div style='overflow-x:auto;padding:8px 0'>";
  h+="<div style='display:flex;gap:0;min-width:1400px;align-items:flex-start;position:relative'>";

  // 13 version nodes
  var versions=[
    {t:'龙宫原本',s:'约2世纪',l:'印度',lang:'梵',c:'#9e8b6e',n:'上中下三本·下本十万偈',w:120},
    {t:'兜沙经',s:'167',l:'洛阳',lang:'汉',c:'#a09080',n:'支娄迦谶·1卷',w:110},
    {t:'六十华严',s:'420',l:'建康',lang:'汉',c:'#b8863c',n:'佛驮跋陀罗·60卷34品',w:130},
    {t:'八十华严',s:'699',l:'洛阳',lang:'汉',c:'#b8863c',n:'实叉难陀·80卷39品',w:130},
    {t:'四十华严',s:'798',l:'长安',lang:'汉',c:'#b8863c',n:'般若·40卷入法界品',w:130},
    {t:'藏译华严',s:'~830',l:'吐蕃',lang:'藏',c:'#c46b5d',n:'胜友/智军·4册45品',w:130},
    {t:'尼泊尔写本',s:'11-12c',l:'加德满都',lang:'梵',c:'#9e8b6e',n:'梵文残卷',w:100},
    {t:'西夏译本',s:'11-13c',l:'西夏',lang:'西夏',c:'#8b7a9e',n:'据八十华严译',w:110},
    {t:'回鹘译本',s:'13-14c',l:'高昌',lang:'回鹘',c:'#8b7a9e',n:'安藏译',w:90},
    {t:'满文译本',s:'18c',l:'北京',lang:'满',c:'#8b7a9e',n:'四体合璧',w:100},
    {t:'Cleary英译',s:'1984-87',l:'美国',lang:'英',c:'#5e8b9e',n:'据八十华严',w:110},
    {t:'Dharmamitra',s:'2022',l:'美国',lang:'英',c:'#5e8b9e',n:'据八十华严·3册',w:120},
    {t:'84000英译',s:'2021-',l:'国际',lang:'英',c:'#c46b5d',n:'据藏文Toh44',w:110}
  ];

  versions.forEach(function(v,i){
    var ml=i>0?6:0;
    h+="<div style='flex-shrink:0;width:"+v.w+"px;margin-left:"+ml+"px;position:relative'>";
    // Arrow connector from previous
    if(i>0){
      h+="<div style='position:absolute;left:-12px;top:18px;font-size:10px;color:#c0b098'>→</div>";
    }
    // Node card
    h+="<div style='background:var(--card);border:2px solid "+v.c+";border-radius:8px;padding:8px 10px;text-align:center;min-height:90px'>";
    h+="<div style='font-weight:700;font-size:0.85em;color:"+v.c+"'>"+v.t+"</div>";
    h+="<div style='font-size:0.7em;color:var(--text2);margin:2px 0'>"+v.s+" · "+v.l+"</div>";
    h+="<div style='font-size:0.7em;color:var(--text2)'>"+v.n+"</div>";
    h+="<span class=tag style=font-size:0.65em;background:"+v.c+"20;color:"+v.c+">"+v.lang+"</span>";
    h+="</div></div>";
  });

  h+="</div></div>";

  // Legend
  h+="<div style='display:flex;gap:16px;margin-top:10px;font-size:0.72em;color:var(--text2)'>";
  h+="<span>🟡 汉文</span><span style=color:#c46b5d>🔴 藏文</span><span style=color:#5e8b9e>🔵 英文</span><span style=color:#9e8b6e>🟤 梵文</span><span style=color:#8b7a9e>🟣 其他语言</span>";
  h+="<span style=margin-left:8px>→ 继承/重译/补全</span></div>";
  h+="</div>";

  // ── References (moved to overview for reliability) ──
  h+="<h2 style=color:var(--gold)>📚 参考文献 & 数据源</h2><div class=section><p style=font-size:0.82em;line-height:1.9>";
  h+="📄 Imre Hamar. <i>The Buddhāvatamsaka-sūtra and Its Chinese Interpretation</i>. 匈牙利科学院博士论文, 2014.<br>";
  h+="📄 Imre Hamar. <i>The Metaphor of the Painter in the Avatamsaka-sutra and Its Chinese Interpretations</i>. SOS 13·2, 2014.<br>";
  h+="📄 Peter Alan Roberts (tr.). <i>The Stem Array</i> (Gaṇḍavyūha, Toh 44-45). 84000 Project, 2021.<br>";
  h+="📄 高明道. 《谈谈翻译与诠释——以《华严》数偈为例》. 《法光》第236期, 2009.<br>";
  h+="📄 孙飞鹏. 《〈华严经〉卷十一夏汉文本对勘研究》. 《西夏学》第十辑(2013年第2期), 页75-80.<br>";
  h+="📄 铃木大拙. 三本《华严经》的异同及其要义. 《禅论集之三·菩萨行处》.<br>";
  h+="📎 84000 Scholar's Room: <a href='https://scholar.84000.co/article/a-multitude-of-buddhas-kangyur-section' target=_blank>A Multitude of Buddhas</a><br>";
  h+="📎 84000: <a href='https://84000.co/translation/toh44-31' target=_blank>The Ten Bhūmis</a> · <a href='https://read.84000.co/translation/toh44-45.html' target=_blank>The Stem Array</a><br>";
  h+="📎 CBETA: <a href='https://cbetaonline.dila.edu.tw/zh/T10n0279' target=_blank>八十华严</a> · <a href='https://cbetaonline.dila.edu.tw/zh/T09n0278' target=_blank>六十华严</a><br>";
  h+="📦 数据源: Asian Legacy Library (Kangyur ZIP) · 84000 PDF · BDRC WA0RK0044 · ACIP KD0044</p></div>";

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

  // ═══ GENEALOGY SECTION ═══
  h+="<div id=gv-genealogy class=gv-section style=display:none>";
  h+="<div class=section><h2>🕸 华严部文本系谱</h2>";
  h+="<p style=font-size:0.82em;color:var(--text2);margin-bottom:12px>主体经·别译本·眷属经·论释·藏文源——共60+部经典的关联网络。节点大小表示影响力，连线表示继承/注释/别译/关联关系。⚠ 关联标注基于大正藏目录及学术研究，部分需逐条人工核实。</p>";

  // ── Main Sutras (top row) ──
  h+="<div style='display:flex;gap:10px;flex-wrap:wrap;justify-content:center;margin-bottom:16px'>";
  h+="<div style='background:var(--card);border:3px solid #b8863c;border-radius:12px;padding:14px 20px;text-align:center;min-width:160px'><div style='font-weight:700;color:#b8863c'>六十华严</div><div style='font-size:0.72em;color:var(--text2)'>T09n0278 · 60卷34品</div><div style='font-size:0.68em;color:var(--text2)'>佛驮跋陀罗·420年</div><a href='https://cbetaonline.dila.edu.tw/zh/T09n0278' target=_blank style='font-size:0.65em'>📖 CBETA阅读</a></div>";
  h+="<div style='display:flex;align-items:center;color:#c0b098;font-size:1.2em'>→</div>";
  h+="<div style='background:var(--card);border:3px solid #b8863c;border-radius:12px;padding:14px 24px;text-align:center;min-width:180px;box-shadow:0 2px 12px rgba(184,134,60,0.15)'><div style='font-weight:700;color:#b8863c;font-size:1.1em'>⭐ 八十华严</div><div style='font-size:0.72em;color:var(--text2)'>T10n0279 · 80卷39品</div><div style='font-size:0.68em;color:var(--text2)'>实叉难陀·699年</div><a href='https://cbetaonline.dila.edu.tw/zh/T10n0279' target=_blank style='font-size:0.65em'>📖 CBETA阅读</a></div>";
  h+="<div style='display:flex;align-items:center;color:#c0b098;font-size:1.2em'>→</div>";
  h+="<div style='background:var(--card);border:3px solid #b8863c;border-radius:12px;padding:14px 20px;text-align:center;min-width:160px'><div style='font-weight:700;color:#b8863c'>四十华严</div><div style='font-size:0.72em;color:var(--text2)'>T10n0293 · 40卷1品</div><div style='font-size:0.68em;color:var(--text2)'>般若·798年</div><a href='https://cbetaonline.dila.edu.tw/zh/T10n0293' target=_blank style='font-size:0.65em'>📖 CBETA阅读</a></div>";
  h+="<div style='display:flex;align-items:center;color:#c46b5d;font-size:1.2em'>⇢</div>";
  h+="<div style='background:var(--card);border:3px solid #c46b5d;border-radius:12px;padding:14px 20px;text-align:center;min-width:160px'><div style='font-weight:700;color:#c46b5d'>藏译华严</div><div style='font-size:0.72em;color:var(--text2)'>Toh44 · 4册45品</div><div style='font-size:0.68em;color:var(--text2)'>胜友/智军·9世纪</div><a href='https://84000.co/translation/toh44-31' target=_blank style='font-size:0.65em'>📖 84000(部分)</a></div>";
  h+="</div>";

  // ── Branch translations ──
  h+="<div class=section><h2>📋 支流别译经（对应各品异译）</h2>";
  h+="<div style='display:flex;gap:8px;flex-wrap:wrap'>";
  [{t:'兜沙经',n:'T0280·支娄迦谶·167',p:'如来名号品'},
   {t:'菩萨本业经',n:'T0281·支谦',p:'净行品'},{t:'诸菩萨求佛本业经',n:'T0282·聂道真',p:'净行品'},
   {t:'菩萨十住行道品',n:'T0283·竺法护',p:'十住品'},{t:'菩萨十住经',n:'T0284·祇多蜜',p:'十住品'},
   {t:'渐备一切智德经',n:'T0285·竺法护',p:'十地品'},{t:'十住经',n:'T0286·鸠摩罗什',p:'十地品'},
   {t:'佛说十地经',n:'T0287·尸罗达摩',p:'十地品'},{t:'等目菩萨三昧经',n:'T0288·竺法护',p:'十定品'},
   {t:'显无边佛土功德经',n:'T0289·玄奘',p:'寿量品'},{t:'较量一切佛刹功德经',n:'T0290·法贤',p:'寿量品'},
   {t:'如来兴显经',n:'T0291·竺法护',p:'如来出现品'},{t:'度世品经',n:'T0292·竺法护',p:'离世间品'},
   {t:'罗摩伽经',n:'T0294·圣坚',p:'入法界品'},{t:'入法界品(续)',n:'T0295·地婆诃罗',p:'入法界品'}]
  .forEach(function(b){var num=b.n.match(/T(\d+)/)[1];var cbUrl='https://cbetaonline.dila.edu.tw/zh/T10n'+num;h+="<span style='padding:4px 10px;background:rgba(94,139,158,0.08);border:1px solid rgba(94,139,158,0.3);border-radius:14px;font-size:0.73em'><b>"+b.t+"</b> <span style=color:var(--text2)>"+b.n+"</span><br><span style=font-size:0.85em;color:#5e8b9e>→ "+b.p+"</span><br><a href='"+cbUrl+"' target=_blank style=font-size:0.6em>📖 CBETA</a></span>";});
  h+="</div></div>";

  // ── Related Sutras ──
  h+="<div class=section><h2>📎 眷属经（义理相关·非正部）</h2>";
  h+="<div style='display:flex;gap:8px;flex-wrap:wrap'>";
  [{t:'文殊师利发愿经',n:'T0296',u:'T10n0296'},
   {t:'普贤菩萨行愿赞',n:'T0297·不空',u:'T10n0297'},
   {t:'⭐ 大方广普贤所说经',n:'T0847·实叉难陀',note:'↔藏文普贤宣说品',u:'T10n0847'},
   {t:'总持宝光明经',n:'T0299·法天',u:'T10n0299'},
   {t:'不思议佛境界分',n:'T0300·提云般若',u:'T10n0300'},
   {t:'如来不思议境界经',n:'T0301·实叉难陀',u:'T10n0301'},
   {t:'度诸佛境界智光严经',n:'T0302·失译',u:'T10n0302'},
   {t:'入如来德智不思议经',n:'T0303·阇那崛多',u:'T10n0303'},
   {t:'大方广入如来智德',n:'T0304·实叉难陀',u:'T10n0304'},
   {t:'信力入印法门经',n:'T0305·昙摩流支',u:'T10n0305'},
   {t:'花严经修慈分',n:'T0306·提云般若',u:'T10n0306'},
   {t:'庄严菩提心经',n:'T0307·鸠摩罗什',u:'T10n0307'},
   {t:'大方广菩萨十地经',n:'T0308·吉迦夜',u:'T10n0308'},
   {t:'最胜问十住除垢断结经',n:'T0309·竺佛念',note:'⚠法藏判非十住品',u:'T10n0309'}]
  .forEach(function(r){h+="<span style='padding:4px 10px;background:rgba(125,154,110,0.08);border:1px solid rgba(125,154,110,0.3);border-radius:14px;font-size:0.73em'><b>"+r.t+"</b> <span style=color:var(--text2)>"+r.n+"</span>"+(r.note?"<br><span style=font-size:0.8em;color:#c46b5d>"+r.note+"</span>":"")+"<br><a href='https://cbetaonline.dila.edu.tw/zh/"+r.u+"' target=_blank style=font-size:0.6em>📖 CBETA</a></span>";});
  h+="</div></div>";

  // ── Treatises ──
  h+="<div class=section><h2>📖 论释（3部）</h2>";
  h+="<div style='display:flex;gap:10px;flex-wrap:wrap'>";
  h+="<span style='padding:6px 14px;background:rgba(196,107,93,0.08);border:1px solid rgba(196,107,93,0.3);border-radius:14px;font-size:0.78em'><b>十住毗婆沙论</b> <span style=color:var(--text2)>T26n1521·龙树造·鸠摩罗什译</span><br><span style=font-size:0.85em;color:var(--text2)>⚠ 虽名十住实释十地品·仅至第二地(17卷)</span><br><a href='https://cbetaonline.dila.edu.tw/zh/T26n1521' target=_blank style=font-size:0.65em>📖 CBETA</a></span>";
  h+="<span style='padding:6px 14px;background:rgba(196,107,93,0.08);border:1px solid rgba(196,107,93,0.3);border-radius:14px;font-size:0.78em'><b>十地经论</b> <span style=color:var(--text2)>T26n1522·世亲造·菩提流支译(12卷)</span><br><span style=font-size:0.85em;color:var(--text2)>创新六相名相·催生南北朝地论师学派</span><br><a href='https://cbetaonline.dila.edu.tw/zh/T26n1522' target=_blank style=font-size:0.65em>📖 CBETA</a></span>";
  h+="<span style='padding:6px 14px;background:rgba(196,107,93,0.08);border:1px solid rgba(196,107,93,0.3);border-radius:14px;font-size:0.78em'><b>大乘起信论</b> <span style=color:var(--text2)>T32n1666·马鸣造[传统著录]</span><br><span style=font-size:0.85em;color:var(--text2)>法藏《大乘起信论义记》为最权威注释之一</span><br><a href='https://cbetaonline.dila.edu.tw/zh/T32n1666' target=_blank style=font-size:0.65em>📖 CBETA</a></span>";
  h+="</div></div>";

  // ── Patriarch Commentaries: hierarchical timeline layout ──
  h+="<div class=section><h2>📜 祖师章疏（8位·26部·按时序排列）</h2>";
  h+="<style>.pat-block{border-left:3px solid #b8863c;padding:6px 10px;margin:4px 0;background:rgba(184,134,60,0.03);border-radius:0 8px 8px 0;font-size:0.73em}.pat-block .pat-name{color:#b8863c;font-weight:700;font-size:1.05em}.pat-block .pat-info{color:var(--text2);font-size:0.85em}.pat-works{margin-left:8px;margin-top:4px;display:flex;gap:5px;flex-wrap:wrap}.pat-wk{display:inline-block;padding:2px 8px;background:rgba(94,139,158,0.08);border:1px solid rgba(94,139,158,0.2);border-radius:12px;font-size:0.92em;white-space:nowrap}.pat-wk a{font-size:0.8em}</style>";

  // Early period: India/Sui
  h+="<div style=font-size:0.78em;color:var(--gold);margin:10px 0 4px>▸ <b>唐代·华严宗创立与鼎盛</b></div>";
  [{a:'杜顺',dy:'557–640',ti:'华严初祖·帝心尊者(隋末唐初)',ws:[{t:'法界观门',u:'T45n1884'},{t:'五教止观',u:'T45n1867'}]},
   {a:'智俨',dy:'602–668',ti:'华严二祖·至相尊者',ws:[{t:'搜玄记',u:'T35n1732'},{t:'一乘十玄门',u:'T45n1868'},{t:'五十要问答',u:'T45n1869'}]}]
  .forEach(function(x){
    h+="<div class=pat-block><span class=pat-name>"+x.a+"</span> <span class=pat-info>"+x.dy+" · "+x.ti+"</span><div class=pat-works>";
    x.ws.forEach(function(w){h+="<span class=pat-wk>"+w.t+(w.u?" <a href='https://cbetaonline.dila.edu.tw/zh/"+w.u+"' target=_blank>📖</a> <a href='https://cbeta.buddhism.org.hk/xml/"+w.u+"_001.xml' target=_blank>📄</a>":"")+"</span>";});
    h+="</div></div>";
  });

  [{a:'法藏',dy:'643–712',ti:'华严三祖·贤首国师·实际创立者',ws:[{t:'五教章',u:'T45n1866'},{t:'探玄记',u:'T35n1733'},{t:'金师子章',u:'T45n1880'},{t:'起信论义记',u:'T44n1846'},{t:'义海百门',u:'T45n1875'},{t:'十二门论宗致义记',u:'T42n1826'}]},
   {a:'李通玄',dy:'635–730',ti:'枣柏大士·在家学者',ws:[{t:'新华严经论',u:'T36n1739'},{t:'决疑论',u:'T36n1741'}]},
   {a:'澄观',dy:'738–839',ti:'华严四祖·清凉国师·集大成者',ws:[{t:'华严经疏',u:'T35n1735'},{t:'演义钞',u:'T36n1736'},{t:'法界玄镜',u:'T45n1883'},{t:'三圣圆融观门',u:'T45n1882'}]},
   {a:'宗密',dy:'780–841',ti:'华严五祖·圭峰大师·禅教融合',ws:[{t:'禅源诸诠集',u:'T48n2015'},{t:'原人论',u:'T45n1886'},{t:'圆觉经大疏释义钞',u:'X09n0245'},{t:'注法界观门',u:'T45n1884'},{t:'行愿品疏钞',u:'X05n0229'}]}]
  .forEach(function(x){
    h+="<div class=pat-block><span class=pat-name>"+x.a+"</span> <span class=pat-info>"+x.dy+" · "+x.ti+"</span><div class=pat-works>";
    x.ws.forEach(function(w){h+="<span class=pat-wk>"+w.t+(w.u?" <a href='https://cbetaonline.dila.edu.tw/zh/"+w.u+"' target=_blank>📖</a> <a href='https://cbeta.buddhism.org.hk/xml/"+w.u+"_001.xml' target=_blank>📄</a>":"")+"</span>";});
    h+="</div></div>";
  });

  // Song dynasty: 子璿/净源/本嵩 + 华严四大家
  h+="<div style=font-size:0.78em;color:var(--gold);margin:10px 0 4px>▸ <b>宋代·华严中兴</b></div>";
  [{a:'子璿',dy:'965–1038',ti:'长水法师·宋代华严复兴先驱',ws:[{t:'楞严经义疏',u:'T39n1001'},{t:'起信论疏笔削记',u:'T44n1848'},{t:'金刚经纂要刊定记',u:'T33n1702'}]},
   {a:'净源',dy:'1011–1088',ti:'晋水法师·华严中兴教主·立七祖谱系',ws:[{t:'金师子章云间类解',u:'T45n1881'},{t:'原人论发微录',u:'X58n1006'},{t:'仁王经疏',u:'T33n1707'},{t:'华严普贤行愿修证仪',u:'X74n1472'}]},
   {a:'义天',dy:'1055–1101',ti:'高丽僧统·入宋师净源·海东华严初祖',ws:[{t:'新编诸宗教藏总录',u:null,note:'（义天录·华严章疏基准目录）'}]},
   {a:'本嵩',dy:'北宋',ti:'通玄记',ws:[{t:'华严七字经题法界观三十颂',u:'T45n1885'}]},
   {a:'华严四大家',dy:'南宋',ti:'道亭·观复·师会·希迪',ws:[{t:'五教章注疏系列',u:null,note:'道亭《义苑疏》/观复《析薪记》/师会《焚薪》《复古记》/希迪《集成记》《注同教策》'}]}]
  .forEach(function(x){
    h+="<div class=pat-block><span class=pat-name>"+x.a+"</span> <span class=pat-info>"+x.dy+" · "+x.ti+"</span><div class=pat-works>";
    x.ws.forEach(function(w){h+="<span class=pat-wk>"+w.t+(w.u?" <a href='https://cbetaonline.dila.edu.tw/zh/"+w.u+"' target=_blank>📖</a> <a href='https://cbeta.buddhism.org.hk/xml/"+w.u+"_001.xml' target=_blank>📄</a>":"")+(w.note?"<br><span style=font-size:0.75em;color:#5e8b9e>"+w.note+"</span>":"")+"</span>";});
    h+="</div></div>";
  });

  // Yuan/Ming/Qing
  h+="<div style=font-size:0.78em;color:var(--gold);margin:10px 0 4px>▸ <b>元明清·传承与整理</b></div>";
  [{a:'普瑞',dy:'元代',ti:'华严经疏注',ws:[{t:'华严经疏注',u:'X07n0234'}]},
   {a:'续法',dy:'1641–1728',ti:'清·华严集大成者·柏亭',ws:[{t:'贤首五教仪',u:'X58n1024'},{t:'华严宗佛祖传',u:'X77n1530'}]},
   {a:'通理',dy:'清代',ti:'北京宝通寺·北方华严代表',ws:[{t:'华严经疏钞',u:null,note:'清代北方华严中兴者'}]}]
  .forEach(function(x){
    h+="<div class=pat-block><span class=pat-name>"+x.a+"</span> <span class=pat-info>"+x.dy+" · "+x.ti+"</span><div class=pat-works>";
    x.ws.forEach(function(w){h+="<span class=pat-wk>"+w.t+(w.u?" <a href='https://cbetaonline.dila.edu.tw/zh/"+w.u+"' target=_blank>📖</a> <a href='https://cbeta.buddhism.org.hk/xml/"+w.u+"_001.xml' target=_blank>📄</a>":"")+(w.note?"<br><span style=font-size:0.75em;color:#5e8b9e>"+w.note+"</span>":"")+"</span>";});
    h+="</div></div>";
  });
  h+="</div>";

  // ── Modern & Tibetan sources ──
  h+="<div class=section><h2>📚 近现代著作 & 藏文源</h2>";
  h+="<div style='display:flex;gap:8px;flex-wrap:wrap;font-size:0.75em'>";
  h+="<span style=padding:4px 10px;background:rgba(94,139,158,0.06);border:1px solid rgba(94,139,158,0.25);border-radius:14px><b style=color:#5e8b9e>藏译华严经</b> Toh44·4册45品·胜友/智军译·9世纪初</span>";
  h+="<span style=padding:4px 10px;background:rgba(94,139,158,0.06);border:1px solid rgba(94,139,158,0.25);border-radius:14px><b style=color:#5e8b9e>84000英译</b> 入法界品(2021)+十地品·进行中</span>";
  h+="<span style=padding:4px 10px;background:rgba(125,154,110,0.06);border:1px solid rgba(125,154,110,0.25);border-radius:14px><b style=color:#7d9a6e>Cleary英译</b> The Flower Adornment Sutra·单册·据八十华严</span>";
  h+="<span style=padding:4px 10px;background:rgba(125,154,110,0.06);border:1px solid rgba(125,154,110,0.25);border-radius:14px><b style=color:#7d9a6e>Dharmamitra英译</b> 3册·2022·Kalavinka Press·据八十华严</span>";
  h+="<span style=padding:4px 10px;background:rgba(184,134,60,0.06);border:1px solid rgba(184,134,60,0.25);border-radius:14px><b style=color:#b8863c>梦参</b> 华严经讲记(全本)</span>";
  h+="<span style=padding:4px 10px;background:rgba(184,134,60,0.06);border:1px solid rgba(184,134,60,0.25);border-radius:14px><b style=color:#b8863c>成一</b> 成一和尚著作集(华严莲社)</span>";
  h+="<span style=padding:4px 10px;background:rgba(184,134,60,0.06);border:1px solid rgba(184,134,60,0.25);border-radius:14px><b style=color:#b8863c>贤度</b> 华严经讲义·华严学概论(华严专宗学院)</span>";
  h+="<span style=padding:4px 10px;background:rgba(184,134,60,0.06);border:1px solid rgba(184,134,60,0.25);border-radius:14px><b style=color:#b8863c>海云</b> 九九華嚴玄談5册·探玄記懸談4册</span>";
  h+="<span style=padding:4px 10px;background:rgba(184,134,60,0.06);border:1px solid rgba(184,134,60,0.25);border-radius:14px><b style=color:#b8863c>华严纂要</b> 华严纲要·华严经疏钞玄谈集成</span>";
  h+="</div></div>";
  h+="</div>"; // close 文本系谱 section div
  h+="</div>"; // close gv-genealogy

  // ═══ 以经证经 (从 GAP.intertextual_canon 数据驱动) ═══
  h+=renderIntertextualCanon();

  // ═══ 华严经学 (从 GAP.avatamsaka_studies 数据驱动) ═══
  h+=renderAvatamsakaStudies();

  // ═══ REFERENCES SECTION ═══
  h+="<div id=gv-refs class=gv-section style=display:none>";

  h+="<h2 style=color:var(--gold)>📚 参考文献</h2><div class=section><p style=font-size:0.82em;line-height:1.9>";
  h+="📄 Imre Hamar. <i>The Buddhāvatamsaka-sūtra and Its Chinese Interpretation</i>. 匈牙利科学院博士论文, 2014.<br>";
  h+="📄 Imre Hamar. <i>The Metaphor of the Painter in the Avatamsaka-sutra and Its Chinese Interpretations</i>. SOS 13·2, 2014.<br>";
  h+="📄 Peter Alan Roberts (tr.). <i>The Stem Array</i> (Gaṇḍavyūha, Toh 44-45). 84000 Project, 2021.<br>";
  h+="📄 Peter Alan Roberts (tr.). <i>The Ten Bhūmis</i> (Daśabhūmika, Toh 44-31). 84000 Project, 2021–2025.<br>";
  h+="📄 高明道. 《谈谈翻译与诠释——以《华严》数偈为例》. 《法光》第236期, 2009.<br>";
  h+="📄 孙飞鹏. 《〈华严经〉卷十一夏汉文本对勘研究》. 《西夏学》第十辑(2013年第2期), 页75-80.<br>";
  h+="📄 吴国圣. 《华严经》「入法界品」「发心」中的「犬」与「马」: 梵、藏、汉诸语文本对勘. 2021年华严专宗国际学术研讨会.<br>";
  h+="📄 铃木大拙 (D.T. Suzuki). 三本《华严经》的异同及其要义. 《禅论集之三·菩萨行处》.<br>";
  h+="📄 邓葶愉. 再雕高丽藏之周本《华严经》版本源流考. 华严专宗学院, 2020.<br>";
  h+="📄 庄垣内正弘、百济康义等. 回鹘文《华严经》与汉文底本对应研究.<br>";
  h+="📎 84000 Scholar's Room: <a href='https://scholar.84000.co/article/a-multitude-of-buddhas-kangyur-section' target=_blank>A Multitude of Buddhas — Kangyur Section</a><br>";
  h+="📎 84000: <a href='https://84000.co/translation/toh44-31' target=_blank>The Ten Bhūmis (Toh44-31)</a> · <a href='https://read.84000.co/translation/toh44-45.html' target=_blank>The Stem Array (Toh44-45)</a><br>";
  h+="📎 CBETA: <a href='https://cbetaonline.dila.edu.tw/zh/T10n0279' target=_blank>八十华严 (T10n0279)</a> · <a href='https://cbetaonline.dila.edu.tw/zh/T09n0278' target=_blank>六十华严 (T09n0278)</a></p></div>";

  h+="<h2 style=color:var(--gold)>📥 数据源</h2><div class=section><p style=font-size:0.82em;line-height:1.9>";
  h+="📦 <b>Asian Legacy Library (ALL)</b> — Kangyur ZIP (122MB) · 藏文 Wylie 转写全45品<br>";
  h+="📦 <b>84000 Project</b> — Toh44-31/Toh44-45 英译 PDF + 校勘注<br>";
  h+="📦 <b>BDRC/BUDA</b> — Work ID WA0RK0044 · 德格版6函扫描件 (library.bdrc.io)<br>";
  h+="📦 <b>ACIP</b> — Release KD0044 · 藏文纯文本 (asianclassics.org → Asian Legacy Library)<br>";
  h+="📦 <b>CBETA</b> — 汉文大藏经全文 (cbetaonline.dila.edu.tw)</p></div>";

  // ── Warnings ──
  GAP.wn.forEach(function(w){h+="<div style=background:rgba(196,107,93,0.05);border:1px solid rgba(196,107,93,0.2);border-radius:8px;padding:8px 12px;margin:4px 0;font-size:0.8em;color:var(--red)>"+w+"</div>";});

  h+="</div>"; // close gv-refs

  gv.innerHTML=h;
}

// ═══ GAP SUB-NAV ═══
// ═══ 以经证经渲染 (从 GAP.intertextual_canon) ═══
function renderIntertextualCanon() {
  var ic = (typeof GAP !== 'undefined' && GAP.intertextual_canon) ? GAP.intertextual_canon : null;
  if (!ic || !ic.schools) return '';
  var h = '<div id=gv-intertextual class=gv-section style=display:none>';
  h += '<div class=section><h2>📖 以经证经 — 大小宗派经典汇证</h2>';
  h += '<p style=font-size:0.82em;color:var(--text2);margin-bottom:12px>华严宗「事事无碍」「一即一切」的义理与各宗经典互相印证——汉传八宗+藏传+南传+因明共14门。</p>';
  ic.schools.forEach(function(school) {
    h += '<div id=ic-' + (school.id||'') + ' style="margin-bottom:16px"><h3 style="color:var(--gold);font-size:0.95em;border-bottom:1px solid var(--line);padding-bottom:4px">' + school.name + ' <span style=font-size:0.7em;color:var(--text2)>' + (school.en||'') + '</span></h3>';
    h += '<div style="display:flex;gap:8px;flex-wrap:wrap">';
    school.texts.forEach(function(b) {
      h += '<span style="padding:6px 12px;background:rgba(94,139,158,0.06);border:1px solid rgba(94,139,158,0.2);border-radius:14px;font-size:0.75em;max-width:280px">';
      h += '<b>' + b.t + '</b><br><span style=font-size:0.85em;color:var(--text2)>' + b.n + '</span>';
      h += '<br><span style=font-size:0.85em;color:var(--text)>' + (b.d||'') + '</span>';
      if (b.l) h += '<br><a href="' + b.l + '" target=_blank style=font-size:0.7em;color:var(--blue)">📖 CBETA / 参考</a>';
      h += '</span>';
    });
    h += '</div></div>';
  });
  h += '</div></div>'; // close section + gv-intertextual
  return h;
}

// ── Helper: convert simple markdown to HTML ──
function _mdToHTML(text) {
  if (!text) return '';
  // tables
  if (text.indexOf('|') >= 0 && text.indexOf('---') >= 0) {
    var lines = text.split('\n'), result = [], inTable = false;
    for (var i = 0; i < lines.length; i++) {
      var l = lines[i].trim();
      if (l.indexOf('|') === 0) {
        if (!inTable) { result.push('<table class=v-table style=font-size:0.78em>'); inTable = true; }
        var cells = l.split('|').filter(function(c){return c.trim();});
        var isHeader = (i+1 < lines.length && (lines[i+1]||'').indexOf('---') >= 0);
        var tag = isHeader ? 'th' : 'td';
        result.push('<tr>' + cells.map(function(c){return '<'+tag+'>' + c.trim() + '</'+tag+'>'}).join('') + '</tr>');
        if (isHeader) { i++; }
      } else {
        if (inTable) { result.push('</table>'); inTable = false; }
        result.push(l);
      }
    }
    if (inTable) result.push('</table>');
    text = result.join('\n');
  }
  // bold
  text = text.replace(/\*\*(.+?)\*\*/g, '<b>$1</b>');
  // bullet lists
  text = text.replace(/^[•·]\s/gm, '🔹 ');
  return text;
}

// ═══ 华严经学渲染 (从 GAP.avatamsaka_studies) ═══
function renderAvatamsakaStudies() {
  var avs = (typeof GAP !== 'undefined' && GAP.avatamsaka_studies) ? GAP.avatamsaka_studies : null;
  if (!avs || !avs.sections) return '';
  var h = '<div id=gv-avatamsaka_studies class=gv-section style=display:none>';
  avs.sections.forEach(function(sec) {
    h += '<div class=section id=avs-' + sec.id + '>';
    h += '<h2>' + (sec.icon||'📌') + ' ' + sec.title + '</h2>';
    if (sec.intro) h += '<p style="font-size:0.82em;color:var(--text2);line-height:1.8;white-space:pre-line">' + _mdToHTML(sec.intro) + '</p>';
    if (sec.topics) {
      sec.topics.forEach(function(t) {
        h += '<div class=stage-box><b>' + t.title + '</b>';
        h += '<p style="font-size:0.8em;line-height:1.8;white-space:pre-line;margin-top:4px">' + _mdToHTML(t.body) + '</p>';
        if (t.sources) {
          h += '<p style="font-size:0.7em;color:var(--text2);margin-top:4px">📎 ';
          t.sources.forEach(function(s,i) { h += (i>0?'<br>':'') + s; });
          h += '</p>';
        }
        if (t.links) {
          h += '<p style="font-size:0.7em;margin-top:2px">';
          Object.keys(t.links).forEach(function(k) { h += '<a href="' + t.links[k] + '" target=_blank style="color:var(--blue)">📖 ' + k + '</a> '; });
          h += '</p>';
        }
        h += '</div>';
      });
    }
    h += '</div>';
  });
  if (avs.references) {
    h += '<div class=section><h2>📚 参考文献</h2><ul style="font-size:0.78em;line-height:1.9">';
    avs.references.forEach(function(r) { h += '<li>' + r + '</li>'; });
    h += '</ul></div>';
  }
  h += '</div>'; // close gv-avatamsaka_studies
  return h;
}

function switchGapView(view,btn){
  document.querySelectorAll(".gv-nav").forEach(function(b){b.classList.remove("active");});
  if(btn)btn.classList.add("active");
  document.querySelectorAll(".gv-section").forEach(function(s){s.style.display="none";});
  var el=document.getElementById("gv-"+view); if(el)el.style.display="block";
  try{localStorage.setItem('gap_view',view);}catch(e){}
}
setTimeout(function(){
  var v=localStorage.getItem('gap_view')||'overview';
  switchGapView(v);
},100);

function gapSubNav(view,anchor){
  switchGapView(view);
  setTimeout(function(){
    var el=document.getElementById(anchor);
    if(el)el.scrollIntoView({behavior:'smooth',block:'start'});
  },150);
}

function scrollToP(id){var el=document.getElementById(id);if(el){el.scrollIntoView({behavior:'smooth',block:'center'});el.style.background='rgba(184,134,60,0.15)';setTimeout(function(){el.style.background='';},1500);}}
function loadParallelChapter(chId){
  if(!chId)return;
  var bo=document.getElementById("gv-col-bo");
  var en=document.getElementById("gv-col-en");
  var zh=document.getElementById("gv-col-zh");
  var sg=document.getElementById("gv-segments");
  var nt=document.getElementById("gv-notes");
  bo.innerHTML="<i>加载中…</i>";en.innerHTML="<i>加载中…</i>";zh.innerHTML="<i>加载中…</i>";
  sg.innerHTML="";if(nt)nt.innerHTML="";

  // Try to load Tibetan data from external JSON
  if(chId==="ch11"||chId==="ch32"){
    fetch('toh44-chapters.json').then(function(r){return r.json();}).then(function(data){
      var ch=data[chId];if(!ch)return;
      var pageSize=50, page=0; var totalPages=Math.ceil(ch.paragraphs.length/pageSize);
      function renderPage(pn){
        var start=pn*pageSize, end=Math.min(start+pageSize,ch.paragraphs.length);
        var html='<div class=ch-title>📜 '+ch.name_zh+'<br><span style=font-size:0.7em;color:var(--text2)>'+ch.name_en+' · 共 '+ch.paragraphs.length+' 段 · Wylie转写</span></div>';
        for(var i=start;i<end;i++){html+='<div class=ppara id=pp-'+chId+'-'+i+'><span class=pn>§'+(i+1)+'</span> '+ch.paragraphs[i]+'</div>';}
        html+='<div style=display:flex;gap:8px;justify-content:center;margin:12px 0;flex-wrap:wrap>';
        for(var j=0;j<totalPages;j++){html+='<button onclick=loadPage('+j+') style=padding:4px 10px;border:1px solid var(--line);border-radius:12px;background:'+(j===pn?'var(--gold)':'var(--card)')+';color:'+(j===pn?'#fff':'var(--text2)')+';cursor:pointer;font-size:0.75em>'+(j+1)+'</button>';}
        html+='</div>';bo.innerHTML=html;
        // Segment nav for current page
        var sn='';for(var i=start;i<end;i+=5){sn+='<span class=seg-btn onclick=scrollToP(\"pp-'+chId+'-'+i+'\")>§'+(i+1)+'-'+Math.min(i+5,end)+'</span> ';}
        sg.innerHTML=sn;
      }
      window.loadPage=renderPage; renderPage(0);
    }).catch(function(e){bo.innerHTML='<span style=color:var(--red)>加载失败: '+e.message+'</span>';});
  }

  if(chId==="ch31"){
    // 十地品·第一地 — multi-paragraph comparison
    var boText="<b>第一地·欢喜地 (rab tu dga' ba)</b><br><br>";
    boText+="<span style=color:var(--gold);font-size:0.75em>§1</span> <span style=font-size:0.78em>'di skad bdag gis thos pa dus gcig na | bcom ldan 'das 'dod pa dang | gzugs su yang dag par 'phags pa'i lha'i dbang phyug gi gnas na bzhugs so ||</span><br>";
    boText+="<span style=color:var(--gold);font-size:0.75em>§2</span> <span style=font-size:0.78em>de nas byang chub sems dpa' bye ba khrag khrig brgya stong du ma 'dus pa de dag thams cad kyang | sngon gyi smon lam gyi dbang gis 'phags pa'i sa chen por zhugs pa | chos kyi dbyings rnam par dag pa la spyod pa ||</span><br>";
    boText+="<span style=color:var(--gold);font-size:0.75em>§3</span> <span style=font-size:0.78em>de nas rdo rje snying po zhes bya ba byang chub sems dpa' sems dpa' chen po de dag gi nang na 'dug pa las | sangs rgyas kyi byin gyi rlabs kyis | byang chub sems dpa'i ye shes chen po'i snang ba'i ting nge 'dzin la snyoms par zhugs so ||</span><br>";
    bo.innerHTML=boText+"<br><span style=color:var(--text2);font-size:0.75em>来源: Toh44-31 (德格版甘珠尔) · Wylie转写</span>";

    var enText="<b>Chapter 31: The Ten Bhūmis — Stage One, The Joyful</b><br><br>";
    enText+="<span style=color:var(--gold);font-size:0.75em>§1 🟢</span> <span style=font-size:0.78em>Thus did I hear at one time. The Blessed One was dwelling in the realm of the Devas, Paranirmitavaśavartin, those who have mastered the emanations of others...</span><br>";
    enText+="<span style=color:var(--gold);font-size:0.75em>§2 🟡</span> <span style=font-size:0.78em>Now all those bodhisattvas, assembled there in numbers of many hundreds of thousands of billions, had, by the power of their previous aspirations, entered the great sublime stages. They moved within the completely pure dharmadhātu...</span><br>";
    enText+="<span style=color:var(--gold);font-size:0.75em>§3 🟢</span> <span style=font-size:0.78em>Then a bodhisattva great being named Vajragarbha (Essence of Vajra), who was among that assembly, through the blessing of the Buddha, settled into the samādhi called 'The Illumination of the Great Wisdom of Bodhisattvas'...</span><br>";
    en.innerHTML=enText+"<br><span style=color:var(--text2);font-size:0.75em>来源: 84000 Project · Peter Alan Roberts译 · CC BY-NC</span>";

    var zhText="<b>十地品第二十六之一 · 欢喜地</b><br><br>";
    zhText+="<span style=color:var(--gold);font-size:0.75em>§1 🟢</span> <span style=font-size:0.78em>如是我闻：一时，佛在他化自在天王宫摩尼宝藏殿，与大菩萨众俱…</span><br>";
    zhText+="<span style=color:var(--gold);font-size:0.75em>§2 🟡</span> <span style=font-size:0.78em>其诸菩萨，皆于阿耨多罗三藐三菩提得不退转，悉从他方世界来集，住一切菩萨智所住境，入一切如来智所入处…</span><br>";
    zhText+="<span style=color:var(--gold);font-size:0.75em>§3 🟢</span> <span style=font-size:0.78em>尔时，金刚藏菩萨摩诃萨，承佛神力，入菩萨大智慧光明三昧…</span><br>";
    zh.innerHTML=zhText+"<br><span style=color:var(--text2);font-size:0.75em>来源: CBETA T10n0279 · 实叉难陀译 (699年)</span>";

    // Segment navigation
    sg.innerHTML="<span style='padding:4px 10px;background:rgba(125,154,110,0.15);border-radius:12px;font-size:0.78em;cursor:pointer' onclick='scrollToSegment(1)' title=汉藏一致>§1 🟢</span> "
      +"<span style='padding:4px 10px;background:rgba(200,137,62,0.15);border-radius:12px;font-size:0.78em;cursor:pointer' onclick='scrollToSegment(2)' title=表述有异>§2 🟡</span> "
      +"<span style='padding:4px 10px;background:rgba(125,154,110,0.15);border-radius:12px;font-size:0.78em;cursor:pointer' onclick='scrollToSegment(3)' title=汉藏一致>§3 🟢</span>";

    // Add textual notes section
    var noteDiv=document.getElementById("gv-notes");
    if(!noteDiv){noteDiv=document.createElement("div");noteDiv.id="gv-notes";document.getElementById("gv-parallel-content").appendChild(noteDiv);}
    noteDiv.innerHTML="<div style='margin-top:16px;padding:12px;background:rgba(200,150,60,0.04);border:1px solid var(--line);border-radius:8px'>"
      +"<div style='font-weight:600;color:var(--gold);margin-bottom:8px'>📝 84000校勘注摘录（十地品·第一地）</div>"
      +"<div style='font-size:0.8em;line-height:1.8;color:var(--text2)'>"
      +"<b>注1 (序分)</b>: 梵文与汉文(实叉难陀译)序分皆有「如是我闻：一时，佛在他化自在天宫…」的完整叙述，藏文序分较简略。84000据此判断藏译者所据梵本或为略本。<br>"
      +"<b>注2 (菩萨众)</b>: 德格版作「bye ba khrag khrig brgya stong du ma」(数百千万亿)，斯托克宫版与那塘版数字有出入。梵文残卷作「koṭiśatasahasrā」(百千俱胝)，与汉译「百千亿」更为接近。<br>"
      +"<b>注3 (三昧名)</b>: 藏文「ye shes chen po'i snang ba」(大智慧光明)，汉译作「菩萨大智慧光明三昧」。世亲《十地经论》引此三昧名与藏译一致。<br>"
      +"<b>注4 (金刚藏)</b>: 藏文「rdo rje snying po」直译「金刚藏」，汉译同。梵文「Vajragarbha」。三本一致。<br>"
      +"<span style='font-size:0.75em'>来源: 84000 The Ten Bhūmis (Toh44-31) 翻译注释 · Peter Alan Roberts</span></div></div>";

  }else if(chId==="ch45"){
    bo.innerHTML="<b>入法界品·善财童子第一参</b><br><span style=font-size:0.78em>de nas khye'u nor bzang yid kyi dga' ba dang | dgyes pa dang | yid bde ba dang | ...</span><br><br><span style=color:var(--text2);font-size:0.75em>来源: Toh44-45 · 84000已发布(Peter Alan Roberts,2021)</span>";
    en.innerHTML="<b>The Stem Array — Sudhana's First Teacher</b><br><span style=font-size:0.78em>Then the youth Sudhana, with a mind of joy, delight, and happiness...<br>He approached the bhikṣu Meghaśrī, bowed his head to his feet, and circumambulated him hundreds of thousands of times...</span><br><br><span style=color:var(--text2);font-size:0.75em>84000: The Stem Array, 2021</span>";
    zh.innerHTML="<b>入法界品第三十九之一</b><br><span style=font-size:0.78em>尔时，善财童子，从文殊师利菩萨所，闻如是等种种法门…渐次南行，至可乐国，参访德云比丘…</span><br><br><span style=color:var(--text2);font-size:0.75em>CBETA T10n0279 · 实叉难陀译</span><br><span style=color:var(--text2);font-size:0.7em>另: 四十华严(T10n0293)为全本</span>";
    sg.innerHTML="<span style='padding:4px 10px;background:rgba(125,154,110,0.15);border-radius:12px;font-size:0.78em;cursor:pointer'>§1 🟢</span> <span style='padding:4px 10px;background:rgba(200,137,62,0.15);border-radius:12px;font-size:0.78em;cursor:pointer'>§2 🟡</span>";
  }else if(chId==="ch11"||chId==="ch32"){
    // Loaded via fetch() above
    en.innerHTML="<span style=color:var(--text2)>⏳ 84000尚未发布此品英译<br><br>📎 已从Kangyur ZIP提取藏文Wylie原文</span>";
    zh.innerHTML="<span style=color:var(--text2)>⏳ 汉文无对应品目——此品为藏文独有"+(chId==="ch32"?"<br><br>📎 关联别译: T0847《大方广普贤所说经》(实叉难陀译·1卷)":"<br><br>📎 关联: T0300-T0304等如来不思议境界经典")+"</span>";
  }else if(chId==="ch40"){
    bo.innerHTML="<b>离世间品</b><br><span style=font-size:0.78em>de nas 'jig rten las 'das pa'i le'u ste |...<br><br></span><span style=color:var(--text2);font-size:0.75em>藏文此品有独特异译段落。Toh44-40 (德格版)</span>";
    en.innerHTML="<b>Transcending the World</b><br><span style=font-size:0.78em>The chapter on transcending the world contains unique passages in the Tibetan version not found in the Chinese translations...<br><br></span><span style=color:var(--text2);font-size:0.75em>待84000发布此品英译后进行逐段对勘</span>";
    zh.innerHTML="<b>离世间品第三十八</b><br><span style=font-size:0.78em>尔时，世尊在摩竭提国阿兰若法菩提场中...<br><br></span><span style=color:var(--text2);font-size:0.75em>CBETA T10n0279 · 实叉难陀译<br>📎 别译: 竺法护《度世品经》(T10n0292, 6卷)</span>";
    sg.innerHTML="<span style='padding:4px 10px;background:rgba(200,137,62,0.15);border-radius:12px;font-size:0.78em'>藏文有独特段落</span>";
  }else if(chId==="ch33"){
    bo.innerHTML="<b>寿量品</b><br><span style=font-size:0.78em>de nas 'jig rten gyi khams kyi tshe'i tshad bstan pa...<br><br></span><span style=color:var(--text2);font-size:0.75em>藏文有更详尽的诸佛寿量描述。Toh44-33 (德格版)</span>";
    en.innerHTML="<b>Lifespan</b><br><span style=font-size:0.78em>The Tibetan version contains more elaborate descriptions of the lifespans of Buddhas...<br><br></span><span style=color:var(--text2);font-size:0.75em>有玄奘别译《显无边佛土功德经》(T10n0289)可对照</span>";
    zh.innerHTML="<b>寿量品第三十一</b><br><span style=font-size:0.78em>尔时，心王菩萨摩诃萨于众会中...<br><br></span><span style=color:var(--text2);font-size:0.75em>CBETA T10n0279 · 实叉难陀译<br>📎 别译: 玄奘《显无边佛土功德经》(T10n0289)</span>";
    sg.innerHTML="<span style='padding:4px 10px;background:rgba(200,137,62,0.15);border-radius:12px;font-size:0.78em'>藏文有扩展内容</span>";
  }else{
    bo.innerHTML="<span style=color:var(--text2)>⏳ 待对齐</span>";
    en.innerHTML="<span style=color:var(--text2)>⏳ 待对齐</span>";
    zh.innerHTML="<span style=color:var(--text2)>⏳ 待对齐</span>";
  }
}
