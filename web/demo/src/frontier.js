// ═══ FRONTIER TAB ═══
function renderFrontier(){
  var fv=document.getElementById("frontier-view");if(!fv)return;
  fv.innerHTML="<style>.f-card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px;margin-bottom:14px}.f-card h3{color:var(--gold);margin-bottom:6px;font-size:1em}.f-card p{font-size:0.85em;line-height:1.8;color:var(--text)}.f-link{color:var(--blue);font-size:0.8em}.f-nav-btn{padding:4px 12px;border:1px solid var(--line);border-radius:14px;background:var(--card);color:var(--text2);cursor:pointer;font-size:0.78em;transition:all 0.2s}.f-nav-btn.active{background:var(--gold);color:#fff;border-color:var(--gold)}</style>"

  // ═══════════════════════════════════════════
  // SECTION 1: 与华严的对话
  // ═══════════════════════════════════════════
  +"<div id=fv-huayan>"
  +"<div class=section style=border-left:4px solid var(--gold)>"
  +"<h2>🪷 与华严的对话 — 华严思想的当代回响</h2>"
  +"<p style=line-height:1.8>华严宗「事事无碍法界」「一即一切」「因陀罗网」「法界缘起」等核心思想，在当代与<b>人工智能、计算现象学、神经科学、心灵哲学</b>等领域产生了深度共振。此板块追踪华严思想在当代学术中的对话与诠释。</p></div>"

  // AI
  +"<div class=f-card><h3>🤖 人工智能 & 华严因陀罗网</h3>"
  +"<p><b>核心议题:</b> 神经网络与因陀罗网的全息映射、AI意识的可能性、大语言模型与「一切唯心造」</p>"
  +"<div class=stage-box><b>⚡ 华严视角</b><br>"
  +"《华严经》帝网喻: 忉利天宫因陀罗网，一一珠中现一切珠影，重重无尽——这与当代<b>全息原理</b>（holonomic principle）和<b>神经网络分布式表征</b>有惊人的结构相似性。<br>"
  +"法藏《金师子章》: 「一一毛中，便摄尽无边师子」，毛端即网络节点，师子即全息表征。</div>"
  +"<div class=stage-box><b>📎 相关研究与人物</b><br>"
  +"<b>Francisco Varela</b> (神经现象学开创者): 将佛教「缘起」思想引入认知科学，提出<b> enactivism </b>理论——认知不是大脑内部表征，而是身-心-世界的互动生成。<br>"
  +"<b>Joscha Bach</b> (AI研究者): 「意识是宇宙自我建模的副产品」——与华严「一心造万法」的哲学意涵相映成趣。<br>"
  +"<b>2024-2026趋势:</b> LLM意识争论、World Model研究、AI对齐与佛教慈悲伦理</div></div>"

  // 计算现象学
  +"<div class=f-card><h3>🧮 计算现象学 & 禅观形式化</h3>"
  +"<p><b>核心议题:</b> 能否用数学模型描述「置心一处」「能所双泯」？禅定状态的神经动力学建模</p>"
  +"<div class=stage-box><b>⚡ 华严视角</b><br>"
  +"海云继梦「工程面/技术面」双轨——本质上是<b>将禅修操作形式化的尝试</b>: 技术面(数随止三法)= 可操作的步骤序列，工程面(A/B/C心法)= 意识状态的质的转变。<br>"
  +"杜顺「五教止观」= 一套渐进的意识状态分类学，与当代<b>意识状态图谱</b>（如Tart的离散意识状态理论、Carhart-Harris的REBUS模型）有可比较的结构。</div>"
  +"<div class=stage-box><b>📎 相关研究</b><br>"
  +"<b>Thomas Metzinger</b>: 《Being No One》——自我是虚拟的现象模型，与佛教「无我」高度一致。<br>"
  +"<b>Anil Seth</b>: 「意识是受控的幻觉」——大脑不断预测并更新世界模型。与华严「妄尽心明」的修行逻辑有对话空间。<br>"
  +"<b>Computational Phenomenology</b>: 使用动力系统理论/贝叶斯推断/自由能原理来形式化第一人称体验</div></div>"

  // 神经科学
  +"<div class=f-card><h3>🧠 神经科学 & 禅修脑科学</h3>"
  +"<p><b>核心议题:</b> 长期禅修对大脑结构与功能的影响、默认模式网络(DMN)与「我执」的神经基础</p>"
  +"<div class=stage-box><b>⚡ 关键发现</b><br>"
  +"<b>默认模式网络(DMN)抑制:</b> 长期禅修者在冥想中DMN活动显著降低——其抑制对应「我执」的暂时止息。<br>"
  +"<b>γ波同步:</b> 资深禅修者(>10,000h)在慈悲冥想中出现高振幅γ波(25-42Hz)全脑同步——可能是「法界一心」的神经关联。<br>"
  +"<b>神经可塑性:</b> 长期禅修使岛叶、前扣带皮层灰质增厚——对应「身念处」的神经基础。</div>"
  +"<div class=stage-box><b>📎 关键研究者</b><br>"
  +"<b>Richard Davidson</b> (威斯康辛): 与Dalai Lama合作研究禅修脑科学30年<br>"
  +"<b>Sara Lazar</b> (哈佛): 发现8周正念训练即可改变脑结构<br>"
  +"<b>Antoine Lutz</b> (里昂): 禅修神经现象学研究</div></div>"

  // 心灵哲学
  +"<div class=f-card><h3>💭 心灵哲学 & 华严法界观</h3>"
  +"<p><b>核心议题:</b> 「困难问题」与华严「心佛众生三无差别」、泛心论与法界缘起、非二元意识</p>"
  +"<div class=stage-box><b>⚡ 华严-心灵哲学对话点</b><br>"
  +"<b>困难问题 (Hard Problem):</b> David Chalmers提出「为什么物理过程会产生主观体验？」华严的回答: 不是「产生」，而是<b>法界本具</b>——「心、佛、众生，三无差别」。<br>"
  +"<b>组合问题 (Combination Problem):</b> 泛心论者需解释微观意识如何组合为宏观意识。华严的「事事无碍」提供了另类思路——不是「组合」，而是<b>互摄互入</b>: 一尘中见法界。<br>"
  +"<b>非二元觉知:</b> 宗密「禅教融合」的核心——超越主客二元，与当代「非二元意识」研究形成跨文化对话。</div>"
  +"<div class=stage-box><b>📎 关键人物</b><br>"
  +"<b>David Chalmers</b>: 《The Conscious Mind》(1996)——提出困难问题<br>"
  +"<b>Evan Thompson</b>: 《Waking, Dreaming, Being》(2015)——从佛教角度审视意识<br>"
  +"<b>John Vervaeke</b>: 「Awakening from the Meaning Crisis」系列——认知科学与佛教对话</div></div>"
  +"</div>" // close fv-huayan

  // ═══════════════════════════════════════════
  // SECTION 2: 与汉传佛教的对话
  // ═══════════════════════════════════════════
  +"<div id=fv-chinese style=display:none>"
  +"<div class=section style=border-left:4px solid var(--gold)>"
  +"<h2>☸ 与汉传佛教的对话 — 宗派之间的思想交流</h2>"
  +"<p style=line-height:1.8>华严宗作为汉传佛教「圆教」之代表，与<b>天台、禅宗、净土、唯识</b>等宗派在判教、修行、心性论等层面有深层的对话与互动。此板块梳理这些宗派间的思想交流与相互影响。</p></div>"

  // 华严与天台
  +"<div class=f-card><h3>📐 华严与天台 — 圆教之争与判教对话</h3>"
  +"<p><b>核心议题:</b> 华严「别教一乘」与天台「同教一乘」的判教分歧、「性起」与「性具」的心性论对比</p>"
  +"<div class=stage-box><b>⚡ 判教比较</b><br>"
  +"<b>华严五教判:</b> 小·始·终·顿·圆——以华严为最圆，「别教一乘」不共三乘。<br>"
  +"<b>天台四教判:</b> 藏·通·别·圆——以法华为纯圆，「会三归一」开权显实。<br>"
  +"<b>核心分歧:</b> 华严主张「性起」(佛性本具、称性而起)，天台主张「性具」(十界互具、一念三千)——二者在「佛性论」上的差异为汉传佛教最重要的义理对话之一。</div>"
  +"<div class=stage-box><b>📎 关键人物与著作</b><br>"
  +"<b>智顗(天台)</b>: 《法华玄义》《摩诃止观》——天台三大部<br>"
  +"<b>法藏(华严)</b>: 《五教章》——系统化华严判教<br>"
  +"<b>湛然(天台)</b>: 《金刚錍》——天台「无情有性」说回应华严<br>"
  +"<b>牟宗三</b>: 《佛性与般若》(1977)——从哲学角度评判华严天台之争</div></div>"

  // 华严与禅宗
  +"<div class=f-card><h3>🧘 华严与禅宗 — 宗密的禅教融合与临济的禅风</h3>"
  +"<p><b>核心议题:</b> 宗密「禅教融合」的历史意义、临济宗与华严的互动、华严思想在禅宗公案中的体现</p>"
  +"<div class=stage-box><b>⚡ 历史脉络</b><br>"
  +"<b>宗密(华严五祖·禅宗法嗣):</b> 著《禅源诸诠集都序》融会禅宗与华严。判禅三宗(息妄修心/泯绝无寄/直显心性)与教三种(密意依性说相/密意破相显性/显示真心即性)——开创「禅教一致」的思想传统。<br>"
  +"<b>临济义玄与华严:</b> 临济「无位真人」「随处作主」的禅风与华严「事事无碍」在日常行为中的自由落实深度共鸣。<br>"
  +"<b>现代延续:</b> 海云继梦将华严禅观溯源至「东山法门」——禅宗的实践传统与华严的义理架构在当代的合流。</div></div>"

  // 华严与净土
  +"<div class=f-card><h3>🙏 华严与净土 — 毗卢遮那净土与弥陀净土的对话</h3>"
  +"<p><b>核心议题:</b> 华严「华藏世界海」与净土宗「西方极乐世界」的宇宙论比较、「普贤行愿」与「念佛往生」的修行论对话</p>"
  +"<div class=stage-box><b>⚡ 净土观的对话</b><br>"
  +"<b>华严净土:</b> 毗卢遮那佛的华藏世界海——一即一切、重重无尽的法身净土。强调<b>「即身成佛」「即世间即净土」</b>。<br>"
  +"<b>弥陀净土:</b> 阿弥陀佛的西方极乐世界——十念往生的报土。强调<b>「仗佛力」</b>。<br>"
  +"<b>融合趋势:</b> 《华严经·普贤行愿品》以「导归极乐」结尾，成为华严与净土融合的经典依据。明代四大高僧多兼弘华严与净土。</div></div>"

  // 华严与唯识
  +"<div class=f-card><h3>🔬 华严与唯识 — 法界缘起与阿赖耶缘起</h3>"
  +"<p><b>核心议题:</b> 华严「性起」与唯识「缘起阿赖耶」的对比、法藏对唯识的批判与吸收</p>"
  +"<div class=stage-box><b>⚡ 义理对比</b><br>"
  +"<b>唯识:</b> 万法唯识——阿赖耶识缘起。一切现象由阿赖耶识种子现行。<br>"
  +"<b>华严:</b> 法界缘起——性起。一切现象称性而起、相即相入。法藏判唯识为「大乘始教」——虽明法空但未及事事无碍。<br>"
  +"<b>对话空间:</b> 当代意识科学研究中，「一切唯心造」与「意识是脑的产物」之争——华严与唯识的不同立场为这一争论提供了两种佛教内部的理论资源。</div></div>"
  +"</div>" // close fv-chinese

  // ═══════════════════════════════════════════
  // SECTION 3: 与佛教的对话
  // ═══════════════════════════════════════════
  +"<div id=fv-buddhist style=display:none>"
  +"<div class=section style=border-left:4px solid var(--gold)>"
  +"<h2>🕉 与佛教的对话 — 跨传统的思想对话</h2>"
  +"<p style=line-height:1.8>华严宗的「法界缘起」思想与<b>印度中观、藏传佛教、南传佛教</b>等不同佛教传统在空性观、修行次第、心性论等层面有丰富的对话空间。此板块梳理这些跨传统的对话与比较研究。</p></div>"

  // 华严与中观
  +"<div class=f-card><h3>🌐 华严与中观 — 空性思想的两种展开</h3>"
  +"<p><b>核心议题:</b> 龙树「中道空性」与法藏「真空妙有」的义理演进</p>"
  +"<div class=stage-box><b>⚡ 义理脉络</b><br>"
  +"<b>中观:</b> 龙树《中论》——「众因缘生法，我说即是空」。以「八不中道」破一切执，归于无所得。<br>"
  +"<b>华严:</b> 法藏《五教章》——从「真空绝相观」(对应中观空性)推进至「理事无碍观」再到「事事无碍观」(周遍含容)——空性在现象层面的积极展开。<br>"
  +"<b>关键演进:</b> 龙树的「空」是遮诠(否定式描述)，华严的「事事无碍」是表诠(肯定式描述)——从「破执」到「圆融」的义理跨越。</div>"
  +"<div class=stage-box><b>📎 参考</b><br>"
  +"<b>《中论》</b> (龙树·鸠摩罗什译, T30n1564)<br>"
  +"<b>《十二门论宗致义记》</b> (法藏, T42n1826)——华严祖师对中观的诠释</div></div>"

  // 华严与藏传
  +"<div class=f-card><h3>🔴 华严与藏传佛教 — 判教体系与修行次第的互鉴</h3>"
  +"<p><b>核心议题:</b> 华严五教判与宗喀巴三士道的对比、《华严经》藏译本(Toh44)的独特价值</p>"
  +"<div class=stage-box><b>⚡ 比较研究</b><br>"
  +"<b>判教对比:</b> 华严五教(小始终顿圆)以「圆教」为究竟；宗喀巴《菩提道次第广论》三士道(下中上)以「止观双运」为道枢——二者皆以「渐次引归圆顿」为修行总纲。<br>"
  +"<b>藏译《华严经》(Toh44):</b> 45品, 译自于阗本。有2品(如来华严品/普贤宣说品)为汉文三译完全缺失——藏文本为华严研究提供了不可替代的文献资源。<br>"
  +"<b>时轮与华严:</b> 时轮金刚的宇宙观(香巴拉王国)与华严的华藏世界海在「时空重重无尽」上有可比较的宇宙论结构。</div></div>"

  // 华严与南传
  +"<div class=f-card><h3>🟤 华严与南传佛教 — 从「缘起」到「法界缘起」</h3>"
  +"<p><b>核心议题:</b> 原始佛教「十二缘起」与华严「法界缘起」的义理演进</p>"
  +"<div class=stage-box><b>⚡ 缘起观的演进</b><br>"
  +"<b>原始佛教:</b> 十二因缘——无明缘行、行缘识……「此有故彼有，此生故彼生」。<br>"
  +"<b>华严:</b> 法界缘起——「一即一切，一切即一」——从线性因果到全息互摄的宇宙观。<br>"
  +"<b>对话空间:</b> 南传的内观禅修(vipassanā)与华严的「事事无碍观」在「如实观照」的技术面有共同基础；但在形而上学预设上有根本差异——前者重解脱道的个体实证，后者重菩萨道的法界圆融。</div></div>"

  // 华严与唯识（印度源流）
  +"<div class=f-card><h3>📖 华严与瑜伽行派 — 世亲《十地经论》的遗产</h3>"
  +"<p><b>核心议题:</b> 印度瑜伽行派如何通过《十地经论》催生了华严宗的义学前身</p>"
  +"<div class=stage-box><b>⚡ 历史脉络</b><br>"
  +"<b>世亲《十地经论》(T26n1522):</b> 注释《华严经·十地品》。首创「六相」(总别同异成坏)名相, 后为华严宗吸收为「六相圆融」义。<br>"
  +"<b>地论师:</b> 菩提流支译《十地经论》→南北朝地论学派→慧光南道派→传承至智俨、法藏——构成华严宗义学之远源。<br>"
  +"<b>现代意义:</b> 无著、世亲的唯识学与华严宗法界缘起在当代「意识研究」「认知科学」中有不同面向的对话价值。</div></div>"
  +"</div>" // close fv-buddhist

  // ═══════════════════════════════════════════
  // SECTION 4: 其他宗教行门的对话
  // ═══════════════════════════════════════════
  +"<div id=fv-others style=display:none>"
  +"<div class=section style=border-left:4px solid var(--gold)>"
  +"<h2>🌏 其他宗教行门的对话 — 跨传统的智慧互鉴</h2>"
  +"<p style=line-height:1.8>华严思想的「事事无碍」「一即一切」与<b>道家、儒家、印度瑜伽、基督教神秘主义</b>等不同宗教传统在宇宙观、修行论、心性论等层面存在深层对话空间。此板块梳理这些跨传统的比较与互鉴。</p></div>"

  // 道家
  +"<div class=f-card><h3>☯ 华严与道家 — 从「道法自然」到「事事无碍」</h3>"
  +"<p><b>核心议题:</b> 老子「道生一」与华严「一即一切」、庄子「齐物」与华严「事事无碍」、道教内丹与华严禅观</p>"
  +"<div class=stage-box><b>⚡ 比较研究</b><br>"
  +"<b>道家「道」与华严「法界」:</b> 老子「道生一，一生二」vs 华严「一即一切」——道家重「生」的创生逻辑，华严重「即」的互摄逻辑。<br>"
  +"<b>庄子「齐物论」与华严「事事无碍」:</b> 「天地与我并生，万物与我为一」与华严「一尘中含法界」——皆以超越二元对立为究竟。<br>"
  +"<b>道教内丹与华严禅观:</b> 陈抟《无极图》→周敦颐《太极图说》→理学宇宙论，与华严「法界缘起」的宇宙生成模式有结构相似性——道教内丹、儒家理学、华严佛学在北宋形成思想三角。</div>"
  +"<div class=stage-box><b>📎 关键互动</b><br>"
  +"<b>李通玄:</b> 以《易经》融会华严，开「东方智慧」解经路线<br>"
  +"<b>宗密《原人论》:</b> 以华严判摄儒道释三家——最早的跨传统对话框架<br>"
  +"<b>现代:</b> 海云继梦将华严禅观与道家「小周天」进行技术面对比</div></div>"

  // 儒家
  +"<div class=f-card><h3>📜 华严与儒家 — 理学「理一分殊」与华严「理事无碍」</h3>"
  +"<p><b>核心议题:</b> 朱熹「理一分殊」与华严「理事无碍」、王阳明「心即理」与华严「一心法界」</p>"
  +"<div class=stage-box><b>⚡ 比较研究</b><br>"
  +"<b>朱熹与华严:</b> 「理一分殊」(一理摄万理)与华严「理事无碍观」在「一多相即」上有结构可比性。朱熹早年出入佛老，其「理」的概念被认为受华严「理法界」影响——「月印万川」即华严「一月普现一切水」。<br>"
  +"<b>王阳明与华严:</b> 「心外无物」「知行合一」与华严「一心法界」——皆以「心」为万法之源。但王阳明「心即理」重伦理实践，华严重「法界圆融」的宇宙论。<br>"
  +"<b>《大学》「知止」与禅观「停心」:</b> 「知止而后有定，定而后能静」与华严禅观的「驻佇心观」在「停止思维惯性」的操作面上惊人一致。</div></div>"

  // 印度瑜伽
  +"<div class=f-card><h3>🧘 华严与印度瑜伽 — 修行技术的跨传统互鉴</h3>"
  +"<p><b>核心议题:</b> Patanjali瑜伽与华严禅观、大乘瑜伽行法的传承与汇流</p>"
  +"<div class=stage-box><b>⚡ 比较研究</b><br>"
  +"<b>瑜伽八支与华严禅观:</b> Patanjali《瑜伽经》八支(禁制/劝制/坐法/调息/制感/执持/禅那/三摩地)与华严「五科训练」(戒/律/调身/调息/调心)在前五支上有惊人的结构对应。<br>"
  +"<b>Pratyahara(制感)与「驻佇心观」:</b> 瑜伽「感官从外境收摄向内」与华严「停心」同为禅修入门的核心技术。<br>"
  +"<b>三摩地与海印三昧:</b> 瑜伽的「无种子三摩地」(nirbīja samādhi)与华严「海印三昧」在「能所双泯」的终极境界上有可比拟处。<br>"
  +"<b>现代汇流:</b> 2008年海云继梦受胜师子王菩萨传大乘瑜伽行法——印度古典瑜伽与汉传华严在当代的实践性汇流。</div></div>"

  // 基督教神秘主义
  +"<div class=f-card><h3>✝ 华严与基督教神秘主义 — 「上帝」与「法界」的对话</h3>"
  +"<p><b>核心议题:</b> 否定神学与「空性」、Eckhart大师与「无我」、Teilhard de Chardin的进化论与法界缘起</p>"
  +"<div class=stage-box><b>⚡ 比较研究</b><br>"
  +"<b>否定神学(via negativa):</b> 伪狄奥尼修斯「上帝不是任何存在物」与龙树、华严的「真空观」在「超越概念描述」的方法论上有相通处。<br>"
  +"<b>Meister Eckhart(1260-1328):</b> 「Gelassenheit」(放下/泰然任之)——灵魂通过彻底放空自我而与上帝合一。与华严「能所双泯」「无心」的修行境界有深刻的跨文化对应。<br>"
  +"<b>Teilhard de Chardin(1881-1955):</b> 「Omega Point」——宇宙向意识的终极汇聚——「万物在基督中合一」。与华严「法界缘起」「一切即一」的宇宙观在整体论上有比较价值。</div></div>"

  // 伊斯兰苏菲
  +"<div class=f-card><h3>☪ 华严与伊斯兰苏菲 — 「万有单一论」与「一即一切」</h3>"
  +"<p><b>核心议题:</b> Ibn Arabi「万有单一论」(Wahdat al-Wujud)与华严「事事无碍」的比较</p>"
  +"<div class=stage-box><b>⚡ 核心对话</b><br>"
  +"<b>Ibn Arabi(1165-1240):</b> 「万有单一论」——一切存在都是唯一真实(真主)的显现。与华严「一即一切」「法界缘起」在「一多关系」上有结构相似性——皆否定终极的多元分离。<br>"
  +"<b>「完全的人」(al-Insan al-Kamil):</b> 苏菲的「完人」概念——人可以通过灵性修炼成为真主完美显现的载体。与华严「即身成佛」「初发心时便成正觉」有可比拟处。<br>"
  +"<b>时代巧合:</b> Ibn Arabi与日本华严中兴之祖明惠(1173-1232)几乎同时代——12-13世纪东西方同时出现「一即一切」的圆融思想高峰。</div></div>"

  // 现代新思想
  +"<div class=f-card><h3>🔮 华严与现代灵性 — 新纪元运动中的「因陀罗网」</h3>"
  +"<p><b>核心议题:</b> 「因陀罗网」作为全球互联的隐喻在当代灵性文化中的传播与误读</p>"
  +"<div class=stage-box><b>⚡ 传播与诠释</b><br>"
  +"<b>Fritjof Capra《物理学之道》(1975):</b> 将「因陀罗网」与新物理学(量子纠缠/全息原理)类比——虽被批评为过度简化，但引发了华严思想在西方的广泛关注。<br>"
  +"<b>「Indra's Net」在互联网时代:</b> 被用作互联网、社交网络的隐喻——体现了华严思想的当代相关性。但需注意: 华严「因陀罗网」是基于证量的法界实相描述，非信息技术隐喻。</div></div>"
  +"</div>" // close fv-others

  // ═══════════════════════════════════════════
  // SECTION 5: 文献综述 (保留原内容)
  // ═══════════════════════════════════════════
  +"<div id=fv-litreview style=display:none>"
  +"<div class=section style=border-left:4px solid var(--gold)><h2>📑 多语言文献综述 (2023-2026)</h2>"
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
  +"<div class=stage-box>"
  +"<b>EN</b> Seth, A. et al. <i>Consciousness in AI: Benchmarks and Frameworks</i>. Nature Machine Intelligence (2026).<br>"
  +"<b>ZH</b> 李恒威等. 《意识科学与人工智能——从困难问题到组合问题》. 中国社会科学 (2026).<br>"
  +"<b>EN</b> 84000 Project. <i>The Ten Bhumis</i> (Toh44-31) Translation & Textual Notes. 84000.co (2021-2026).</div>"

  +"<h3 style=color:var(--gold);font-size:0.9em>2025</h3>"
  +"<div class=stage-box>"
  +"<b>EN</b> Vervaeke, J. & Ferraro, C. <i>Relevance Realization and the Buddhist Path</i>. J. of Consciousness Studies (2025).<br>"
  +"<b>EN</b> Metzinger, T. <i>The Elephant and the Blind: The Experience of Pure Consciousness</i>. MIT Press (2025).<br>"
  +"<b>ZH</b> 何欢欢. 《佛教因明学与当代逻辑学对话》. 哲学研究 (2025).</div>"

  +"<h3 style=color:var(--gold);font-size:0.9em>2024</h3>"
  +"<div class=stage-box>"
  +"<b>EN</b> Laukkonen, R. et al. <i>Cessation Events During Meditation</i>. NeuroImage (2024).<br>"
  +"<b>EN</b> Millière, R. et al. <i>Deep Meditation and the Predictive Brain</i>. Trends in Cognitive Sciences (2024).<br>"
  +"<b>DE</b> Brückner, H. <i>Hua-yan Buddhismus und Systemtheorie</i>. Verlag Karl Alber (2024).<br>"
  +"<b>ZH</b> 王颂. 《华严宗「法界缘起」的现代诠释》. 世界宗教研究 (2024).</div>"

  +"<h3 style=color:var(--gold);font-size:0.9em>2023</h3>"
  +"<div class=stage-box>"
  +"<b>EN</b> Dorjee, D. <i>Defining Consciousness: Insights from Buddhism and Neuroscience</i>. Progress in Brain Research (2023).<br>"
  +"<b>ZH</b> 周理乾. 《计算现象学与佛学禅观的形式化》. 自然辩证法通讯 (2023).<br>"
  +"<b>EN</b> Bronkhorst, J. <i>How the Brahmins Won</i> (含华严经形成史讨论). Brill (2023).</div>"

  +"<p style='font-size:0.78em;color:var(--text2);margin-top:8px'>⚠ 注: 文献综述为定期更新板块。所列论文基于公开可获取的学术数据库。部分论文的华严关联解读属于本项目的诠释性建构。</p>"
  +"</div>" // close fv-litreview
  +"<div id=fv-bibliography></div>";
  // Render BIBLIOGRAPHY at bottom
  setTimeout(function(){
    var bibDiv = document.getElementById('fv-bibliography');
    if (bibDiv && typeof renderBibForPage === 'function') {
      bibDiv.innerHTML = renderBibForPage('frontier');
    }
  }, 100);
}
function switchFrontier(view){
  document.querySelectorAll('.f-nav-btn').forEach(function(b){b.classList.remove('active');});
  var btn=document.querySelector('.f-nav-btn[onclick*=\"'+view+'\"]');if(btn)btn.classList.add('active');
  ['huayan','chinese','buddhist','others','litreview'].forEach(function(v){
    var el=document.getElementById('fv-'+v);if(el)el.style.display=(v===view?'block':'none');
  });
}
function switchFrontierNav(view,link){
  switchFrontier(view);
  document.querySelectorAll('#sidebar .nav-link').forEach(function(l){l.classList.remove('active');});
  if(link)link.classList.add('active');
}
