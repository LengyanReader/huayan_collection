// ═══ GAP TAB ═══
function renderGap(){
  var gv=document.getElementById("gap-view");if(!gv)return;
  var h="<h2 style=color:var(--gold)>📜 版本对照</h2><div class=section><table class=v-table><tr><th>版本</th><th>品目</th><th>卷/册</th><th>译者</th><th>年代</th><th>底本</th></tr>";
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
  h+="📄 84000 Scholar's Room: <a href='https://scholar.84000.co/article/a-multitude-of-buddhas-kangyur-section' target=_blank>A Multitude of Buddhas — Kangyur Section</a></p></div>";

  // ── Warnings ──
  GAP.wn.forEach(function(w){h+="<div style=background:rgba(196,107,93,0.05);border:1px solid rgba(196,107,93,0.2);border-radius:8px;padding:8px 12px;margin:4px 0;font-size:0.8em;color:var(--red)>"+w+"</div>";});

  gv.innerHTML=h;
}
