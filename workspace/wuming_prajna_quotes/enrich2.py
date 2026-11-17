# -*- coding: utf-8 -*-
"""L.505 续研批：新增 §七（问无明者谁：自指＋施设评估）与 §八（维度模型评估），
结语改 §九；引言路线、编者按、附录B 同步；§3.5 五门、§3.7 十玄六相微补。锚点断言唯一。"""
import io, sys

sys.stdout.reconfigure(encoding='utf-8')
PATH = r'C:\DA_Practice\huayan_collection\docs\宗派研究\无明与般若.md'
s = io.open(PATH, encoding='utf-8').read()
orig = len(s)

def uniq(a):
    n = s.count(a)
    if n != 1:
        raise SystemExit('ANCHOR FAIL (%d): %s' % (n, a[:50]))

INS = []
def after(anchor, text):
    INS.append((anchor, anchor + '\n\n' + text))

# ── 0. 编者按续研说明 ──
after('本文自判标〔本文判断〕。',
      '本文自判标〔本文判断〕。**续研说明**：§七、§八为整理者就草稿未尽之问（问无明者谁、无明施设、维度模型）新增的评估与经证，超出草稿范围，新引经证另行回源（附录 B）。')

# ── 1. 引言路线图更新 ──
INS.append(('破幻现真与方便说（§六），最后给出结论（§七）。',
            '破幻现真与方便说（§六），评估「以无明问无明」的自指结构与「无明只是施设」之说（§七）、「维度」模型（§八），最后给出结论（§九）。'))

# ── 2. §3.5 五门微补 ──
after('奢摩他、三摩钵提、禅那三观及其二十五轮〔大意〕。',
      '奢摩他、三摩钵提、禅那三观及其二十五轮〔大意〕。《起信论》自身的修法一线：由「信成就发心」起行，行五门——施、戒、忍、进、止观〔大意〕。')

# ── 3. §3.7 十玄六相微补 ──
after('「初發心時即得阿耨多羅三藐三菩提，知一切法即心自性，成就慧身，不由他悟」（T10n0279；通行括语「初发心时便成正觉」，逐字则如所引）——智在初发心位已全。',
      '「初發心時即得阿耨多羅三藐三菩提，知一切法即心自性，成就慧身，不由他悟」（T10n0279；通行括语「初发心时便成正觉」，逐字则如所引）——智在初发心位已全。观法一线则有法藏《妄尽还源观》与十玄门、六相之观〔大意〕：以「一即一切」的观门把四法界落到当下事相上。')

# ── 4. 新 §七 ＋ §八，结语改 §九 ──
SEC7 = '''## 七、问无明者谁：「以无明问无明」与「无明只是施设」的评估

本节把三个互相咬合的追问摆上台面。**甲**：追问无明的本原或「为什么出现」，是否本身就是处在无明状态的表现——严重无明处根本无法明白？**乙**：无明是否只是佛陀为「需要被破解之物」方便施设的名言——无体、不具备「可被追问」的属性，只是描述「不觉」状态的标签？**丙**：既因无明而有山河大地、森罗万象，再回头追问无明本源或因何发生，是否属于自我指涉——以无明问无明，从一开始发问就已经表明得不到答案？甲是问者的处境，乙是被问者的地位，丙是问法本身的命运。三者佛典都有可直接回源的回应：先摆经证，再逐步评估。

### 7.1 经证检索：佛教自己如何对待「问不出答案的问题」

第一个事实必须摆正：**「有些问题不可答」不是本文的发明，而是佛教自己的一套成熟制度**。早期经典把十四类形而上学问题列为「无记」（不作定答）〔大意〕；《中部》63 与其汉译平行《中阿含·箭喻经》（经 221，T01n0026）以中毒之箭立原则：先拔箭，不先追问射箭者。但「无记」不是敷衍：龙树《中论·观本际品》给出了论证形态——「大聖之所說，本際不可得，生死無有始，亦復無有終」「若無有始終，中當云何有？是故於此中，先後共亦無」（T30n1564）：不是拒绝回答，而是拆掉问题预设——无始无终，则立于始终之间的「中」亦无；「第一点」在缘起结构中无处安放。

更直接的是《圆觉经·金刚藏章》。金刚藏问出「本來成佛，何故復有一切無明」之后，佛陀的回答下了两刀。第一刀承认**问者状态污染问题本身**：「未出輪迴而辨圓覺，彼圓覺性即同流轉；若免輪迴，無有是處。譬如動目能搖湛水……」（T17n0842）——以轮回心辨圆觉，所辨的圆觉即随之流转，如目动则见静水摇；问题在被提出时已被问者的状态加工。第二刀直接拆掉问题两端：「一切如來妙圓覺心本無菩提及與涅槃，亦無成佛及不成佛，無妄輪迴及非輪迴」——在圆觉心上，「成佛／不成佛」「轮回／非轮回」这一对问题所依赖的分别本就不立。这不是「没有答案」，而是**答案的类型不是发问者要求的那一种**。

自指结构在《楞严》里有逐字的表达。卷五：「知見立知即無明本；知見無見斯即涅槃無漏真淨」（T19n0945）——在知见上再立一个能知，正是无明的根本；知见上不立知，即是涅槃。卷一又以「認賊為子，失汝元常，故受輪轉」点破无明的现行方式：把妄认当作自家主人。以此看「追问无明本原」这一问：发问所用的装备——能所、时间起点、事件感——恰是无明所铸；问「觉明何来」，就是在知见上再立知。演若达多问「我的头为何丢了」：问话本身即是狂走。此与 §4.2 的「视角不对称」、§4.6 的「谁在问」互为表里。

### 7.2 评估甲：「追问无明本原是无明的表现」——成立，但要三步精确化

**第一步，它对什么成立。**当追问以「无明是真实发生过的事件＋存在可定位的起点」为预设时，此问由无明的实体化活动驱动，问式本身即无明的现行（知见立知）。严重无明处，连苦的条件链都看不清，遑论自审无明——经论不否认这一点，《圆觉》甚至把它写成警告。故「处严重无明状态无法明白」在「自审无明之体」这一种问上成立。〔本文判断〕

**第二步，它不能一刀切。**若凡从无明出发的问都自指无效，则四谛亦不可说、教法亦不可能——而佛教恰以「苦的条件与止息」为核心教法。实际的区分是：**机制之问可答，本体之问不立**。无明当下如何生起、靠什么维持、凭什么止息——有完整答案（《增支部》10.61 条件链、十二因缘、转依道次）；无明「最初为何存在」——问式被拆而非被答。自指论证的功能是**筛选问题**，不是取消提问。〔本文判断〕

**第三步，自指的出口不在答案，在转向。**注意佛陀答富楼那之问的完整形态：既给判定（「妄性如是，因何為在」——狂走之问无实答），又给转向指令（「汝但不隨分別世間、業果、眾生、三種相續」）；《圆觉》给「知幻即離，不作方便；離幻即覺，亦無漸次」；禅宗给「谁在问」的自照。「知见无见」不是再得一个更高的见，而是立知活动的止息——自指被照见的那一刻，即是它的解消。〔本文判断〕

### 7.3 评估乙：「无明无体，只是施设」——半立，且须防两个滑坡

「无明只是描述不觉状态的名言施设」，分系统看是一条谱系而非一个立场：

| 系统 | 无明的存在地位 | 「只是施设」是否成立 |
|---|---|---|
| 有部／阿毗达磨 | 独立实有的心所，六根本烦恼之一 | 不成立 |
| 唯识 | 依他起有：种子与末那俱起，缘起而有效力 | 部分成立（世俗有，非纯标签） |
| 中观 | 世俗假名安立，缘起而有作用；胜义无自性 | 成立（假名≠虚构≠无效） |
| 《起信》《圆觉》 | 无体而幻用：「念無自相」「非實有體」 | 成立且最彻底 |
| 大圆满 | 无明「无根」 | 成立（术语另立：Rigpa／Marigpa） |

据此，这一说法**胜义层成立、世俗层须立即补全**。三点限定〔本文判断〕。其一，**施设≠虚构**。名言施设可以指谓一个真实有效力的条件结构：无明有稳定的指谓（不如实知）、稳定的食（《增支部》10.61）、稳定的作用（能生诸染）、稳定的止息方式——把这四样都划成「纯属方便设置」，苦的结构与道次随之蒸发，即落断灭；《圆觉》恰在此设防：「以幻修幻亦復如是，諸幻雖盡不入斷滅」。其二，**无明与如来藏的施设性不对称**：如来藏可说是疗愈性施设（为离怖畏而说，《楞伽》明文），无明却站在施设的另一头——它不是为安慰而设，而是苦的结构性描述；它不是被佛陀「设置」出来供破解，而是先于教法已在运作、被教法如实指认。其三，**「不具备可追问的属性」须拆成两问**：问其体（第一因、真实生起）——无此属性，故此问不立；问其用（条件、相续、止息）——属性俱在，故此问必答且必须先答。「无明无体」若推进为「无明无事」，便与「夢時非無」相违：梦里的泪是真的。

### 7.4 综合判定：丙问的命运

三问合观〔本文判断〕：追问无明的本原，**作为「体问」自陷自指**——发问者以无明问无明，问处即病现，所要求的答案类型（第一因叙事）在缘起结构中不存在；**作为「用问」完全可答**——条件、相续、止息皆有可复检的答案。无明无体，故「它从何而来」不立；施设有用，故「它如何运作、如何止息」必答。而自指的照见本身即是出口：知见不立知处，问者与所问同时脱落——这是「同体模型」最深刻处，也是其最须防的滑坡（以「无修无证」饰放逸，宗密之诫）。所以「从一开始发问已经表明得不到答案」应精确为：**从一开始就表明所要求的那个答案类型不存在，而另一类答案（机制与止息，外加一个转向指令）一直可得。**问题的解消不在得到一个答案，而在问者被如实照见。

> **英译对读 · 第七节**
>
> Buddhism itself institutionalized "unanswerable questions": the fourteen undeclared (avyākata)〔大意〕, the arrow parable (MN 63; Chinese parallel Zhong Ahan 221, T01n0026), and — not evasion but argument — Nāgārjuna's analysis of the ultimate limit: with no beginning and no end, no middle can be established (T30n1564). The Perfect Enlightenment's Jingangzang chapter answers "why ignorance if originally Buddha" with two cuts: first, the questioner's state contaminates the question — "not yet out of saṃsāra, one inquires into perfect awakening, and that perfect-awakening nature turns with the cycle" — a stirring eye shakes the still water; second, the terms themselves dissolve — "the wondrous perfect-awakening mind of all Tathāgatas fundamentally has neither bodhi nor nirvāṇa, neither becoming Buddha nor not becoming Buddha, neither deluded saṃsāra nor non-saṃsāra" (T17n0842). The Śūraṅgama states the reflexive structure verbatim: "to establish knowing within knowing is the root of ignorance; knowing without established knowing is nirvāṇa" (T19n0945) — and "taking the thief for one's son, losing what is constant in you" names how ignorance operates.
>
> Is asking after the origin of ignorance itself an expression of ignorance? **Yes, for the substance-question**: it presupposes a real event with a locatable first point, and its very instrument — subject and object, time, eventhood — is the mis-knowing it asks about; the severely deluded cannot even see the condition-chain, which is why practice enters through given suffering, not through self-audit of ignorance. **No, as a blanket ban**: mechanism-questions (how it feeds, how it ceases) are answerable and must be answered first; self-reference filters questions, it does not silence all of them. And its exit is not an answer but a redirect: "do not follow discrimination" (Śūraṅgama), "knowing the illusion is leaving it; no expedient means" (Perfect Enlightenment), "who is asking?" (Chan).
>
> Is ignorance then a mere designation, posited to be broken? A spectrum, not a stance: a real mental factor (Sarvāstivāda); dependently real (Yogācāra); nominally real yet causally efficacious (Madhyamaka); substanceless yet functionally real (Awakening of Faith, Perfect Enlightenment); "rootless" (Dzogchen). Designation ≠ fiction ≠ inefficacy: ignorance has a stable referent, food, function and cessation — dissolve all four as "mere convenience" and the structure of suffering and the path evaporates; hence the warning "the illusions exhausted, one does not enter extinction" (T17n0842). The construct is asymmetric: tathāgatagarbha may be therapeutic positing (Laṅkāvatāra says so); ignorance is not posited for comfort — it operates prior to any teaching and is honestly named by it. Of its "questionable properties": ask about substance — none, so no first-cause question stands; ask about function — all present, so that question is answerable and mandatory. "No answer from the start" should therefore read: from the start, the demanded *type* of answer does not exist, while another type — mechanism, cessation, and a redirect — has always been available. What dissolves is the questioner, seen through in the act of asking.'''

SEC8 = '''## 八、「维度」模型评估：迷悟之差、可去之无明与可证之菩提

第三种说法是现代读者常用的地图：觉悟者与非觉悟者之间存在**对真理感受的维度差别**；立「无明」之名，是为了标出阻碍维度提升之物；只要如法修行，无明可去、维度可提升、菩提可证。这一说法值得认真对待——它大体正确且经证充足，但有三处必须限定的滑坡。

### 8.1 经证对应：这张地图几乎处处有落点

「维度差别」的经典对应物成套：三惑、二障、五盖——「惑」「障」「盖」三字本身就是遮蔽与阻隔的意象，且分粗细层次；唯识以二障说「障」、天台以三惑分层，正是「阻隔有层」的经典版。《起信论》把觉悟写成**有阶段的显发**：不觉——相似觉——随分觉——究竟觉，「随分」即「随其分位而显」〔大意〕；天台六即与菩萨十地同此。而「同一个世界、两种经验方式」正是无明与般若的关系：動則有苦，覺則不動（T32n1666）；圣弟子身受同而心不受第二箭〔大意〕。就这些落点说，「维度」是诚实而好用的现代善巧地图。〔本文判断〕

### 8.2 三重限定：滑坡在哪里

**其一，「提升」实为「显发」，不是在本体上加高。**维度隐喻容易把无明想成一堵墙、把修行想成爬墙。但依 §七，无明无体，阻隔不是墙而是误认：「認賊為子，失汝元常」——不是少了一层，是认错了主人。故「提升」的准确形态是破妄显真：《楞严》说得最重——「歇即菩提，勝淨明心本周法界，不從人得」（T19n0945）：那个更高的维度本来就是周遍的，不从外得、不由造加。道元之问（「既圆满何须修」）与其答（修证一等），正是对「爬梯子」隐喻的传统校正。

**其二，「无明可去、菩提可证」的担保，因系统而异。**「只要好好修行就……」的确定语气，暗含「人人皆可成佛」的普遍担保。这一担保在如来藏／佛性系统内有充分依据（真如内熏、佛性本有，《大般涅槃经》一切众生悉有佛性〔大意〕）；中观只承诺**可变**（烦恼无自性故可断），不承诺必成；唯识五种姓之说甚至撤回普遍担保。把一宗的担保当全部佛法的公理，是把地图当疆域。诚实的说法是：无明有终（各宗共许），菩提可证（如来藏系担保、中观许可能变、唯识有条件）——担保的强度是立场的函数，不是修行的自动回报。〔本文判断〕

**其三，「对真理的感受」须精确。**般若不是新增的感受器官，觉悟者也不是在原维度上多了一种「真理感」。经验面的转变是真实的——第二支箭不再、动则有苦变为觉则不动——但那是**执取结构解消后的经验面**，不是感官升级。《楞严》两种根本分得最清：众生以攀缘心为自性，故真味反失；所谓「维度差」，差在认取方向，不在感受器的数量。〔本文判断〕

### 8.3 「好好修行就……」的实践条款

这句话的实践内核成立，但条款要写全：无明有终、道有次第（闻思修、戒定慧、信解行证）；条件稀缺——亲近善人与听闻正法是全链条的第一环（《增支部》10.61 正向链）；「维度可提升」应作**修行地图**用，不作形而上学承诺用。如此，「菩提可证」既是精进的理由，也不至沦为要求宇宙兑现的期票。〔本文判断〕

> **英译对读 · 第八节**
>
> The "dimensional" map has classical anchoring everywhere: the very words for delusion — obscuration, hindrance, confusion — image blockage in graded layers (three delusions, two obstructions, five hindrances); the Awakening of Faith stages awakening as graded manifestation (similar, partial, final); the six identities and the ten grounds plot the ascent; and "one world, two ways of experiencing" is precisely the ignorance/prajñā relation — stirring entails suffering, awakening does not stir (T32n1666); the noble disciple takes the first arrow, not the second〔大意〕. Three limits keep the map honest. (1) "Raising" is really *manifesting*: ignorance is no wall but a mis-taking ("taking the thief for his son, losing what is constant in you"); the "higher dimension" is already all-pervasive — "the supremely pure luminous mind pervades the whole dharmadhatu and is not gained from anyone" (T19n0945) — and Dōgen's practice-awakening-as-one corrects the ladder picture. (2) The guarantee differs by system: tathāgatagarbha guarantees universal Buddhahood (inner perfuming by suchness); Madhyamaka guarantees only *changeability*; Yogācāra's five gotras withdraw the universal promise. "Ignorance ends" is shared; "bodhi is certifiable for all" is a stance, not an axiom. (3) "Feeling truth" needs precision: prajñā adds no sense organ; the transformed experience (no second arrow; motion without suffering) is the experiential face of a dissolved grasping structure — the dimension differs in the direction of recognition, not in the number of senses. Practice clause: the path has stages and the conditions are scarce — good persons and hearing the Dhamma are the first link; "the dimension can rise" is a practice map, not a metaphysical promissory note.'''

INS.append(('\n## 七、结语：无明之所以是无明，在于妄执',
             '\n' + SEC7 + '\n\n' + SEC8 + '\n\n## 九、结语：无明之所以是无明，在于妄执'))

# ── 5. 附录B 更新 ──
INS.append(('命中共 **103 条／15 部经论，全绿**', '命中共 **115 条／16 部经论，全绿**'))
INS.append(('| 圆觉经 | T17n0842 | 金刚藏问、文殊章无明段、无生处故、以幻修幻、依幻说觉、金矿喻 |',
            '| 圆觉经 | T17n0842 | 金刚藏问、文殊章无明段、无生处故、以幻修幻、依幻说觉、金矿喻、知幻即离离幻即觉、诸幻虽尽不入断灭、未出轮回而辨圆觉、本无菩提及与涅槃 |'))
INS.append(('| 大佛顶首楞严经 | T19n0945 | 两种根本、富楼那两问、性觉必明、觉明为咎、演若达多、识迷无因、因缘自然理穷于是、歇即菩提 |',
            '| 大佛顶首楞严经 | T19n0945 | 两种根本、富楼那两问、性觉必明、觉明为咎、演若达多、识迷无因、因缘自然理穷于是、歇即菩提、知见立知即无明本、认贼为子 |'))
INS.append(('| 中论 | T30n1564 | 三是偈（「我說即是無」）、以有空义故、若一切不空、本际不可得 |',
            '| 中论 | T30n1564 | 三是偈（「我說即是無」）、以有空义故、若一切不空、本际不可得、若无有始终中当云何有 |'))
INS.append(('| 杂阿含经（仓内底本） | T02n0099 | 266 经：无明所盖、爱结所系、不知苦之本际 |',
            '| 杂阿含经（仓内底本） | T02n0099 | 266 经：无明所盖、爱结所系、不知苦之本际 |\n| 中阿含经（仓内底本） | T01n0026 | 箭喻经（经 221，MN 63 汉译平行；「先拔箭」原则） |'))

# ── 执行 ──
for anchor, repl in INS:
    uniq(anchor)
    s = s.replace(anchor, repl, 1)

io.open(PATH, 'w', encoding='utf-8', newline='').write(s)
print('OK: %d -> %d chars (+%d), %d edits' % (orig, len(s), len(s) - orig, len(INS)))
