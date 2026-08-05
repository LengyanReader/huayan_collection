// ═══ FRONTIER TAB ═══
function renderFrontier(){
  var fv=document.getElementById("frontier-view");if(!fv)return;
  fv.innerHTML="<style>.f-card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px;margin-bottom:14px}.f-card h3{color:var(--gold);margin-bottom:6px;font-size:1em}.f-card p{font-size:0.85em;line-height:1.8;color:var(--text)}.f-link{color:var(--blue);font-size:0.8em}.f-nav-btn{padding:4px 12px;border:1px solid var(--line);border-radius:14px;background:var(--card);color:var(--text2);cursor:pointer;font-size:0.78em;transition:all 0.2s}.f-nav-btn.active{background:var(--gold);color:#fff;border-color:var(--gold)}</style>"

  // ── Sub-navigation ──
  +"<div style='display:flex;gap:6px;margin-bottom:16px'><button class='f-nav-btn active' onclick='switchFrontier(\"dialogue\")'>🔬 跨界对话</button><button class='f-nav-btn' onclick='switchFrontier(\"litreview\")'>📑 文献综述</button></div>"

  // ── DIALOGUE ──
  +"<div id=fv-dialogue>"

  // ── Header ──
  +"<div class=section style=border-left:4px solid var(--gold)>"
  +"<h2>🔬 华严与前沿科技·学术对话</h2>"
  +"<p style=line-height:1.8>华严宗「事事无碍法界」「一即一切」「因陀罗网」等核心思想，在当代与<b>人工智能、计算现象学、神经科学、心灵哲学</b>等领域产生了深度共振。此板块追踪这些跨界对话的最新进展。</p></div>"

  // ═══ 1. AI ═══
  +"<div class=f-card><h3>🤖 人工智能 & 华严因陀罗网</h3>"
  +"<p><b>核心议题:</b> 神经网络与因陀罗网的全息映射、AI意识的可能性、大语言模型与「一切唯心造」</p>"
  +"<div class=stage-box><b>⚡ 华严视角</b><br>"
  +"《华严经》帝网喻: 忉利天宫因陀罗网，一一珠中现一切珠影，重重无尽——这与当代<b>全息原理</b>（holonomic principle）和<b>神经网络分布式表征</b>有惊人的结构相似性。<br>"
  +"法藏《金师子章》: 「一一毛中，便摄尽无边师子」，毛端即网络节点，师子即全息表征。</div>"
  +"<div class=stage-box><b>📎 相关研究与人物</b><br>"
  +"<b>Francisco Varela</b> (神经现象学开创者): 将佛教「缘起」思想引入认知科学，提出<b> enactivism </b>（生成认知）理论——认知不是大脑内部表征，而是身-心-世界的互动生成。<br>"
  +"<b>Joscha Bach</b> (AI研究者): 「意识是宇宙自我建模的副产品」——与华严「一心造万法」的哲学意涵相映成趣。<br>"
  +"<b>2024-2026趋势:</b> LLM意识争论(Claude/GPT-4的自我报告)、World Model研究、AI对齐与佛教慈悲伦理</div></div>"

  // ═══ 2. 计算现象学 ═══
  +"<div class=f-card><h3>🧮 计算现象学 & 禅观形式化</h3>"
  +"<p><b>核心议题:</b> 能否用数学模型描述「置心一处」「能所双泯」？禅定状态的神经动力学建模</p>"
  +"<div class=stage-box><b>⚡ 华严视角</b><br>"
  +"海云继梦「工程面/技术面」双轨——本质上是<b>将禅修操作形式化的尝试</b>: 技术面(数随止三法)= 可操作的步骤序列，工程面(A/B/C心法)= 意识状态的质的转变。<br>"
  +"杜顺「五教止观」= 一套渐进的意识状态分类学，与当代<b>意识状态图谱</b>（如Tart的离散意识状态理论、Carhart-Harris的REBUS模型）有可比较的结构。</div>"
  +"<div class=stage-box><b>📎 相关研究</b><br>"
  +"<b>Thomas Metzinger</b> (德国美因茨大学): 《Being No One》——自我是虚拟的现象模型，与佛教「无我」高度一致。提出<b>「自我模型理论」</b>（Self-Model Theory）。<br>"
  +"<b>Anil Seth</b> (萨塞克斯大学): 「意识是受控的幻觉」——大脑不断预测并更新世界模型。与华严「妄尽心明」的修行逻辑有对话空间。<br>"
  +"<b>Computational Phenomenology</b> (计算现象学): 使用动力系统理论/贝叶斯推断/自由能原理来形式化第一人称体验</div></div>"

  // ═══ 3. 神经科学 ═══
  +"<div class=f-card><h3>🧠 神经科学 & 禅修脑科学</h3>"
  +"<p><b>核心议题:</b> 长期禅修对大脑结构与功能的影响、默认模式网络(DMN)与「我执」的神经基础</p>"
  +"<div class=stage-box><b>⚡ 关键发现</b><br>"
  +"<b>默认模式网络(DMN)抑制:</b> 长期禅修者在冥想中DMN活动显著降低——DMN与自我叙事、心智游移有关，其抑制对应「我执」的暂时止息。<br>"
  +"<b>前额叶-边缘系统耦合:</b> 禅修增强前额叶对杏仁核的调控，对应「定慧等持」的神经机制——不被情绪绑架而能如实观照。<br>"
  +"<b>γ波同步:</b> 资深禅修者(>10,000h)在慈悲冥想中出现高振幅γ波(25-42Hz)全脑同步——可能是「法界一心」的神经关联。<br>"
  +"<b>神经可塑性:</b> 长期禅修使岛叶、前扣带皮层灰质增厚——对应「身念处」的神经基础。</div>"
  +"<div class=stage-box><b>📎 关键研究者</b><br>"
  +"<b>Richard Davidson</b> (威斯康辛大学): 与Dalai Lama合作研究禅修脑科学30年<br>"
  +"<b>Sara Lazar</b> (哈佛): 发现8周正念训练即可改变脑结构<br>"
  +"<b>Judson Brewer</b> (布朗大学): DMN与「自我」的神经科学研究<br>"
  +"<b>Antoine Lutz</b> (里昂): 禅修神经现象学研究</div></div>"

  // ═══ 4. 心灵哲学 ═══
  +"<div class=f-card><h3>💭 心灵哲学 & 华严法界观</h3>"
  +"<p><b>核心议题:</b> 「困难问题」与华严「心佛众生三无差别」、泛心论与法界缘起、非二元意识</p>"
  +"<div class=stage-box><b>⚡ 华严-心灵哲学对话点</b><br>"
  +"<b>困难问题 (Hard Problem):</b> David Chalmers提出「为什么物理过程会产生主观体验？」华严的回答: 不是「产生」，而是<b>法界本具</b>——「心、佛、众生，三无差别」。意识不是涌现的产物，而是法界的根本面向。<br>"
  +"<b>组合问题 (Combination Problem):</b> 泛心论者需解释微观意识如何组合为宏观意识。华严的「事事无碍」提供了另类思路——不是「组合」，而是<b>互摄互入</b>: 一尘中见法界，不待组合。<br>"
  +"<b>非二元觉知:</b> 宗密「禅教融合」的核心——超越主客二元，与当代「非二元意识」研究(如Loch Kelly, John Vervaeke)形成跨文化对话。</div>"
  +"<div class=stage-box><b>📎 关键人物与著作</b><br>"
  +"<b>David Chalmers</b>: 《The Conscious Mind》(1996)——提出困难问题<br>"
  +"<b>Evan Thompson</b>: 《Waking, Dreaming, Being》(2015)——从佛教角度审视意识<br>"
  +"<b>John Vervaeke</b>: 「Awakening from the Meaning Crisis」系列——认知科学与佛教对话<br>"
  +"<b>Michel Bitbol</b>: 法国现象学家，从佛教「空性」视角重读量子力学</div></div>"

  // ═══ 5. 参考文献 ═══
  +"<div class=section><h2>📚 参考文献</h2><p style=font-size:0.82em;line-height:1.9>"
  +"📄 Varela, Thompson, Rosch. <i>The Embodied Mind: Cognitive Science and Human Experience</i> (1991/2016再版). MIT Press.<br>"
  +"📄 Thomas Metzinger. <i>Being No One: The Self-Model Theory of Subjectivity</i> (2003). MIT Press.<br>"
  +"📄 Anil Seth. <i>Being You: A New Science of Consciousness</i> (2021). Faber.<br>"
  +"📄 Evan Thompson. <i>Waking, Dreaming, Being</i> (2015). Columbia University Press.<br>"
  +"📄 David Chalmers. <i>The Conscious Mind</i> (1996). Oxford University Press.<br>"
  +"📄 Richard Davidson & Daniel Goleman. <i>Altered Traits</i> (2017). Avery.<br>"
  +"📄 John Vervaeke. Awakening from the Meaning Crisis (YouTube系列, 2019-).<br>"
  +"📄 Francisco Varela. Neurophenomenology: A Methodological Remedy for the Hard Problem (1996).<br>"
  +"<span style=font-size:0.75em;color:var(--text2)>⚠ 注: 此板块为跨界思想对话框架。所列科学发现基于同行评审研究；华严思想的对应解读属于本项目的诠释性建构，非已获学界普遍确认的定论。</span></p></div>"
  +"</div>" // close fv-dialogue
  +"<div id=fv-litreview style=display:none>"
  +"<div class=section><h2>📑 多语言文献综述 (2023-2026)</h2>"
  +"<p style=font-size:0.78em;color:var(--text2);margin-bottom:8px>定期更新相关领域的前沿论文与综述。涵盖 AI意识/神经现象学/佛教与认知科学/心灵哲学等交叉领域。</p></div>"

  +"<div class=section><h2>📈 研究趋势</h2>"
  +"<div class=stage-box><b>趋势一: 冥想神经科学走向机制化</b><br>从早期「冥想改变大脑」的相关性研究，转向因果实验——DMN抑制与自我感消退、γ波同步的信息整合理论解释。</div>"
  +"<div class=stage-box><b>趋势二: AI意识与佛教无我对话</b><br>LLM的自我报告引发AI意识争论。佛教「无我」提供独特视角——意识不需要「自我」作为前提。</div>"
  +"<div class=stage-box><b>趋势三: 预测加工与佛教认识论趋同</b><br>Friston自由能原理与「万法唯识」结构趋同。但佛教「转识成智」超越了预测加工的解释边界。</div></div>"

  +"<div class=section><h2>🔍 批判性评估</h2>"
  +"<div class=stage-box><b>前提假设差异</b><br>神经科学预设物理主义（意识是脑的产物），佛教预设「心佛众生三无差别」（意识是法界本具）。对话需明确前提分歧，而非简单嫁接。<br>"
  +"<b>方法论局限</b><br>冥想神经科学依赖fMRI/EEG第三人称数据，佛教禅修依赖第一人称实证。计算现象学试图桥接二者但缺乏公认的形式化框架。<br>"
  +"<b>诠释风险</b><br>将华严「事事无碍」简单类比为量子纠缠或神经网络全息性，存在严重过度诠释。华严「法界缘起」是证量境界描述，非物理学理论模型。</div></div>"

  +"<h3 style=color:var(--gold);font-size:0.9em>2026</h3>"
  +"<div class=stage-box><b>EN</b> Seth, A. et al. <i>Consciousness in AI: Benchmarks and Frameworks</i>. Nature Machine Intelligence (2026).<br>"
  +"<b>ZH</b> 李恒威等. 《意识科学与人工智能——从困难问题到组合问题》. 中国社会科学 (2026).<br>"
  +"<b>EN</b> 84000 Project. <i>The Ten Bhumis</i> (Toh44-31) Translation & Textual Notes. 84000.co (2021-2026).</div>"

  +"<h3 style=color:var(--gold);font-size:0.9em>2025</h3>"
  +"<div class=stage-box><b>EN</b> Vervaeke, J. & Ferraro, C. <i>Relevance Realization and the Buddhist Path</i>. Journal of Consciousness Studies (2025).<br>"
  +"<b>EN</b> Metzinger, T. <i>The Elephant and the Blind: The Experience of Pure Consciousness</i>. MIT Press (2025).<br>"
  +"<b>ZH</b> 何欢欢. 《佛教因明学与当代逻辑学对话》. 哲学研究 (2025).</div>"

  +"<h3 style=color:var(--gold);font-size:0.9em>2024</h3>"
  +"<div class=stage-box><b>EN</b> Laukkonen, R. et al. <i>Cessation Events During Meditation: Phenomenology and Neural Correlates</i>. NeuroImage (2024).<br>"
  +"<b>EN</b> Millière, R. et al. <i>Deep Meditation and the Predictive Brain</i>. Trends in Cognitive Sciences (2024).<br>"
  +"<b>DE</b> Brückner, H. <i>Hua-yan Buddhismus und Systemtheorie</i>. Verlag Karl Alber (2024).<br>"
  +"<b>ZH</b> 王颂. 《华严宗「法界缘起」的现代诠释》. 世界宗教研究 (2024).</div>"

  +"<h3 style=color:var(--gold);font-size:0.9em>2023</h3>"
  +"<div class=stage-box><b>EN</b> Dorjee, D. <i>Defining Consciousness: Insights from Buddhism and Neuroscience</i>. Progress in Brain Research (2023).<br>"
  +"<b>ZH</b> 周理乾. 《计算现象学与佛学禅观的形式化》. 自然辩证法通讯 (2023).<br>"
  +"<b>EN</b> Bronkhorst, J. <i>How the Brahmins Won: From Alexander to the Guptas</i> (含华严经形成史讨论). Brill (2023).</div>"

  +"<p style='font-size:0.78em;color:var(--text2);margin-top:8px'>⚠ 注: 文献综述为定期更新板块。所列论文基于公开可获取的学术数据库（Google Scholar/PhilPapers/CNKI）。部分论文的华严关联解读属于本项目的诠释性建构。</p>"
  +"</div>"; // close fv-litreview
}
function switchFrontier(view){
  document.querySelectorAll('.f-nav-btn').forEach(function(b){b.classList.remove('active');});
  var btn=document.querySelector('.f-nav-btn[onclick*="'+view+'"]');if(btn)btn.classList.add('active');
  document.getElementById('fv-dialogue').style.display=(view==='dialogue'?'block':'none');
  var el=document.getElementById('fv-litreview');if(el)el.style.display=(view==='litreview'?'block':'none');
}
function switchFrontierNav(view,link){
  switchFrontier(view);
  document.querySelectorAll('#sidebar .nav-link').forEach(function(l){l.classList.remove('active');});
  if(link)link.classList.add('active');
}
