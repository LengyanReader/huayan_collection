# -*- coding: utf-8 -*-
"""L.505 充实批：§三逐节英译对读＋海云子节(十一)＋经典侧重表(十二)＋模型节(十三)
＋§四(4.2数学喻/4.3·4.4英译/4.7分歧/4.8三问)＋附录A六组。锚点断言唯一，任一失败不写盘。"""
import io, re, sys

sys.stdout.reconfigure(encoding='utf-8')
PATH = r'C:\DA_Practice\huayan_collection\docs\宗派研究\无明与般若.md'
s = io.open(PATH, encoding='utf-8').read()
orig_len = len(s)

def uniq(a):
    n = s.count(a)
    if n != 1:
        raise SystemExit('ANCHOR FAIL (%d): %s' % (n, a[:60]))

# 1) 模型节改编号
NEW_HEAD = '### 十三、三种「无明—般若」关系模型'
if s.count('### 三种「无明—般若」关系模型') == 1:
    s = s.replace('### 三种「无明—般若」关系模型', NEW_HEAD, 1)
elif s.count(NEW_HEAD) != 1:
    raise SystemExit('models heading unresolved')

# 2) 删除原合并英译块
m = re.search(r'\n> \*\*英译对读 · 第三节\*\*\n(?:.*?\n)*?>.*?being dissolved\.\n', s)
if not m:
    raise SystemExit('old consolidated EN block not found')
s = s[:m.start()] + '\n' + s[m.end():]

def after(anchor, text):
    """在 anchor 之后插入 \n\n text"""
    return (anchor, anchor + '\n\n' + text)

INS = []

# ── §三 各子节英译对读 ──
INS.append(after('不是「从本净生出」。〔大意〕', '''> **英译对读 · 三·一 阿含与部派**
>
> Early Buddhism defines ignorance operationally: not knowing suffering, its origin, its cessation and the path (SN 12.2〔大意〕); not truly knowing the five aggregates (SA 256–258〔大意〕). Saṃsāra is beginningless yet conditioned: "covered by ignorance, bound by craving, beings wander on through the long night, not knowing the far shore of suffering" (SA 266, T02n0099). AN 10.61 gives the finest statement〔大意〕: no first point of ignorance can be found, yet ignorance *has food* — a backward chain (five hindrances ← misconduct ← unguarded senses ← lost mindfulness ← unwise attention ← no faith ← not hearing the Dhamma ← not associating with good persons) and a forward chain culminating in knowledge and release. The mutual conditioning of ignorance and taints appears only in MN 9; its Chinese parallel lacks the reverse link, so the "loop" is not a shared Āgama doctrine.〔本文判断〕 Wisdom (paññā) is knowing-and-seeing, cultivated as hearing-born, reflection-born and cultivation-born. Abhidharma reifies delusion as a real factor, lets the arhat retain "undefiled ignorance" (the seed of the later cognitive obstruction), and hosts the "mind intrinsically pure, defiled by adventitious guests" view — the Indian ancestor of tathāgatagarbha.'''))

INS.append(after('断尽二障方是佛的圆满觉悟。', '''> **英译对读 · 三·二 般若经与中观**
>
> Prajñāpāramitā locates ignorance in reifying anything at all — self, world, causality, the knower, even the attainment. The Heart Sūtra negates not only ignorance and its cessation but wisdom and attainment: prajñā does not destroy a real entity called ignorance; it sees that ignorance never had intrinsic nature. The Diamond Sūtra adds the four no-notions and "arouse the mind without abiding" — not inaction, but no fixed grasping of self, possession, realm or gain. Nāgārjuna turns this into philosophy: whatever is dependently arisen, the text (in Kumārajīva's wording) declares to be "wu (empty)" — later writers conventionally quote it as "emptiness"; designation and the middle way complete the verse. Emptiness itself must not be reified — "emptiness too is empty" — otherwise one has only swapped the world for a subtler essence; and precisely because nothing has intrinsic nature, change, the ceasing of suffering and practice are all possible ("if everything were not empty, there would be no arising and ceasing"). On origins Madhyamaka is categorical: "the highest limit is unobtainable; saṃsāra has no beginning and no end" — the question presupposes a locatable first point, and dependent arising admits none. The two obstructions (afflictive and cognitive) mark the distance from arhatship to Buddhahood.'''))

INS.append(after('五种姓之说使「一切众生皆可成佛」失去普遍保证。〔本文判断〕', '''> **英译对读 · 三·三 唯识**
>
> Yogācāra digs into the structure of mis-knowing: eight consciousnesses, with the seventh (manas) constantly appropriating the eighth's observing aspect as a self, and the store-consciousness (ālaya) carrying seeds that sustain habit and karma — a stream of conditions, not a soul. The three natures say what exactly is mis-taken: the imagined nature (a grasper and a grasped constructed as independent), the dependent nature (conditioned experience), the perfected nature (that very experience seen without the imagined duality). One "beginningless element" grounds both transmigration and nirvāṇa (the verse in the Mahāyānasaṃgraha, T31n1594); since suchness is unconditioned it produces nothing, so the origin question becomes: how are contaminated seeds transformed? By "hearing-perfuming" — right hearing as the seed of the supramundane mind — through the four investigations to the transformation of the basis (āśraya-parāvṛtti), the four wisdoms, and the double severing of both obstructions. The costs are stated openly: beginningless contaminated seeds as a hard fact, and the five-gotra doctrine withdrawing the guarantee that all beings can become Buddha.'''))

INS.append(after('这场争论至今未了。〔大意〕', '''> **英译对读 · 三·四 如来藏系**
>
> The tathāgatagarbha corpus faces the fault line head-on. The Śrīmālā Sūtra asks how defilement is possible at all — "afflictions do not touch the mind, the mind does not touch afflictions" — and the Buddha confirms that both the intrinsically pure mind and its defilement are "hard to understand" (T12n0353). The same sūtra makes tathāgatagarbha the shared ground of saṃsāra and nirvāṇa, and the very reason revulsion from suffering and longing for nirvāṇa are possible. The Nirvāṇa Sūtra fuses the terms: "Buddha-nature is the ultimate truth of emptiness, and the ultimate truth of emptiness is wisdom" (T12n0374). The Laṅkāvatāra guards both flanks: the tathāgatagarbha-with-the-storehouse is "naturally pure, yet veiled by adventitious defilements," and the teaching itself is expedient — preached to attract those afraid of selflessness, so one must rely on "the tathāgatagarbha without a self" (T16n0670). The Ratnagotravibhāga's argument is soteriological, not genealogical: Buddha-nature explains why liberation is possible, not why ignorance arose. Modern "critical Buddhism" attacks the dhātu framing; defenders reply that "depending without substance" is no substance.〔大意〕'''))

INS.append(after('引用其教义时应同时交代这一层。', '''> **英译对读 · 三·五 一心系三经论**
>
> The "One Mind" trio merges the three roles of ultimacy into one system. The Awakening of Faith defines non-enlightenment as "not truly knowing the oneness of true thusness — the mind stirs and thoughts arise; thoughts have no substance of their own and never leave original awakening," like being lost about a direction: the error depends on the real direction and owns nothing ("mistaking east for west, the direction does not turn"). Its three-stage unfolding shows subject and object are not two prior substances but a structure built inside deluded activity: "because of not-awakening the mind stirs — that is karma; awakening does not stir; stirring entails suffering." Wave and water: ignorance's appearance never leaves awakening's nature, "the wetness unharmed"; when ignorance ceases "the knowing nature is not destroyed." Yet the treatise marks its own boundary — such workings "only a Buddha can know" — and, in the second translation, denies any findable first arising: "the initial arising of mind is spoken of only conventionally; seek its first mark and it can never be found" (T32n1667). The Perfect Enlightenment Sūtra goes further: ignorance "is not a real entity — like a person in a dream: while dreaming it is not absent; upon waking, nothing is obtained," for it "has no place of arising"; and gold once refined "never becomes ore again" (T17n0842). The Śūraṅgama stages the whole problem as Pūrṇa's question and Yajñadatta — who ran mad searching for his own never-lost head: "delusion has no true cause… it never truly arose; what is there to extinguish?" — with "when the madness rests, that resting itself is bodhi" (T19n0945).'''))

INS.append(after('人人理即是佛，不等于究竟即是佛。〔大意〕', '''> **英译对读 · 三·六 天台**
>
> Tiantai grades delusion into three (view-and-thought, dust-and-sand, fundamental ignorance), met by the three contemplations of one mind (empty, provisional, middle) and the three knowledges. Its signature is "inherent possession": the Mohe Zhiguan states "ignorance is precisely dharma-nature, dharma-nature is precisely ignorance" (T46n1911), echoing Vimalakīrti's "the real nature of ignorance is itself luminosity" (T14n0475). This does not say affliction is awakening and practice unnecessary; it says ignorance and dharma-nature are not two substances — one and the same thought is deluded as grasping and revealed as prajñā under contemplation. The doctrine that a Buddha does not sever inherent evil converts "where does ignorance come from?" into a paradoxical "inherent," and the six identities (from principle-Buddha to final-Buddha) reconcile what everyone inherently is with what must be cultivated.'''))

INS.append(after('也针对洪州禅「任运」之弊〔大意〕。', '''> **英译对读 · 三·七 华严**
>
> Huayan develops emptiness into dharma-realm dependent arising: four realms culminating in the mutual containment of all phenomena. It is not a creation story — the point is not that A produced B but that nothing stands alone: every phenomenon already presupposes all others. Hence the realm's fullness does not entail each being's experience being whole; structural completeness and experiential freedom are different claims.〔本文判断〕 Prajñā here is not only seeing emptiness but seeing the endless interweaving: difference and equality do not cancel; whole and part do not wall each other off. Fazang's golden lion ("unchanging yet according with conditions"), Chengguan's "true and delusion interpenetrate," and Zongmi's *Origin of Humanity* — which traces beings stepwise from the "one true numinous nature" through the single thought of "not-awakening" — are the school's most direct account of the fault line〔大意〕. Scripturally: "at the very first arousing of the mind he attains unsurpassed awakening, knowing all dharmas as his mind's own nature" (T10n0279), beside the Buddha's cry over beings who possess tathāgata-wisdom yet do not know or see it.'''))

INS.append(after('二者当下不可分〔大意〕。', '''> **英译对读 · 三·八 禅宗**
>
> Chan compresses the theory into practice. Bodhidharma's "entering by principle": one true nature shared by ordinary and sage, veiled by adventitious dust〔大意〕. The Platform Sūtra: "the prajñā of awakening, people originally possess it; only the mind is deluded and cannot awaken by itself" — "a prior thought deluded: an ordinary being; a later thought awakened: a Buddha"; "all prajñā wisdom arises from self-nature, not from outside"; "one deluded thought and prajñā is cut off; one awakened thought and prajñā is born" (T48n2008). No-thought (not being commanded by thoughts), no-form (not fixating appearances), no-abiding (the mind not sticking anywhere) — the life of the Diamond Sūtra's non-abiding. Later methods split: huatou Chan turns the doubt itself — the questioning "why?" as ignorance in operation — into the engine; silent illumination starts from inherent completeness; Dōgen answers "if already perfect, why practice?" with practice-and-awakening as one〔大意〕.'''))

INS.append(after('（Dhp 276〔大意〕）。', '''> **英译对读 · 三·九 净土**
>
> Pure Land builds no separate philosophy of ignorance. Its judgment is realistic: beginningless habits cannot be exhausted in this life, so the gate is faith (in the Buddha's vow), aspiration (birth in the Pure Land) and practice (recitation) — carried by other-power, "with karma remaining," toward final awakening there. Tanluan's two bodies — the dharma-nature body and the body of expedience, "different yet inseparable" — answer "why doesn't the realm protect us?" directly: compassionate function works through the name and the vow, but never coerces〔大意〕. And even a Buddha cannot awaken on another's behalf: "strive yourselves; the Tathāgata only points the way" (Dhp 276〔大意〕).'''))

# ── §三·十 藏传 EN ＋ 十一 海云子节＋EN ＋ 十二 经典侧重表（复合插入）──
TIB_EN = '''> **英译对读 · 三·十 藏传**
>
> Geluk Madhyamaka defines ignorance as reifying persons and things as established "from their own side," and classifies it as a *mistaken cognition* taking the same object as its antidote — hence the two cannot coexist, and analytic meditation dismantles the object of negation. Emptiness and dependent arising establish each other; denying convention is as wrong as reifying the ultimate〔大意〕. Dzogchen speaks another language: rigpa (primordial luminosity) was never lost, only unrecognized (marigpa); the path is direct introduction and spontaneous release — with the warnings that rigpa is not an independently existing cosmic observer, and the "ground" itself is finally "groundless"〔大意〕. Vajrayāna adds the five poisons as five wisdoms: when the grasping structure is purified, the very energies misused by affliction function as wisdom — kin to Yogācāra's transformation of the basis.'''

HAIYUN_ZH = '''### 十一、当代华严禅观：海云继梦的「第一念·第二念」模型

草稿专有一轮研问海云继梦法师的相关讲授，值得单独立节：他是本站普贤乘传承的当代法脉，也是少数把「一念无明怎么来」直接当心性理论核心来讲的当代华严讲师。依公开讲稿转录〔大意〕（《耳根圆通章》第二、三、四集，《华严禅行法·禅观》第五集，佛教导航 fjdh.cn）：

- **心性三结构**：心（心体）、性（心用）、念（心相），人人本具，称「本体念」；
- **第一念**：本体念起相，无明尚未介入；
- **第二念**：无明介入，相转为色，开始识尘相荡，进入受想行识的相续；
- **相续机制**：「相续心为无明本」——心识活动形成模式、模式重复成惯性、惯性不断强化识的运作，无明愈演愈盛；
- **自知边界**：「我们常讲一念无明起，无明怎么来的？关键在无明怎么来的」「无明怎么介入这是另外一个理论」「为什么介入，你也不知道」——他自己在讲稿里承认：单纯沿十二因缘追问会退回循环，而介入之因不在机制说明之内。

另有《地藏菩萨行法·陆》区分「法身一念起」与「无明起」：法身入法界不等于重新产生无明〔大意〕。评估〔本文判断〕：这套模型的价值在**修行性观察**——把「清净心性如何转入分别」讲成可操作的禅观对象，截断相续即截断无明之食；但机制解释（无明如何持续）不等于起源解释（为何最初介入），两者不可混同，§4.5 的三层区分在此同样适用。'''

HAIYUN_EN = '''> **英译对读 · 三·十一 海云继梦**
>
> Master Haiyun Jiumeng, the contemporary Huayan teacher behind this site's Puxian-vehicle materials, works the same fault line in his *Ear-Root Perfect Penetration* lectures. He structures mind as substance, function and appearance (the "thought of the basis"), then splits the **first thought** (appearance arising, ignorance not yet involved) from the **second thought** (ignorance intervening; appearance becomes form; consciousness begins), and names the sustaining mechanism: "the continuity of mind is the root of ignorance" — habits sedimented in memory keep strengthening consciousness, and the stronger consciousness runs, the thicker ignorance grows. But he states the boundary himself: "why it intervenes — you do not know," and "how ignorance intervenes is another theory." The model explains how ignorance persists and where to cut it in practice; it does not explain why there was ever a first intervention. The cited materials are lecture transcripts (fjdh.cn)〔大意〕, not verified originals — the distinction stays on record.'''

CLASSIC_ZH = '''### 十二、重要经典中无明与般若的具体侧重

宗派之外，把经典排开看，各部经论的理论重心并不相同（下表整理自草稿第十五部分，〔本文判断〕）：

| 经典 | 对无明的主要解释 | 对般若或智慧的主要解释 |
|---|---|---|
| 《阿含经》 | 不如实知四圣谛、五蕴、缘起 | 如实知苦集灭道、无常、无我 |
| 《大般若经》 | 对诸法产生实有执著 | 证悟诸法空性、无所得 |
| 《金刚经》 | 执著我相、人相、众生相、法相 | 无住、无相、无所得 |
| 《心经》 | 无明及十二因缘的究竟空性 | 照见五蕴皆空的般若 |
| 《中论》 | 执著诸法有自性 | 缘起性空、中道智慧 |
| 《解深密经》 | 对依他起经验产生遍计所执 | 如实认识三性 |
| 《楞伽经》 | 无始妄想习气、能所分别 | 离分别、转依、证自觉圣智 |
| 《胜鬘经》 | 自性清净心与烦恼染污的关系 | 如来藏与法身的究竟智慧 |
| 《大乘起信论》 | 不觉、妄念及生灭心相续 | 始觉与究竟觉、本觉显发 |
| 《楞严经》 | 妄为明觉、能所分别、妄无所依 | 妙明真心、根本智慧及圆通 |
| 《圆觉经》 | 无明非实有体、无生处故 | 圆觉本性及如实观照 |
| 《华严经》 | 对法界缘起、事理关系不能如实了知 | 法界无碍智、普贤行 |
| 《六祖坛经》 | 心迷、著境、不识自性 | 自性般若、无念、无相、无住 |
| 《大般涅槃经》 | 烦恼客尘、佛性未显 | 佛性、常住法身、如来智慧 |

须注意：这些经典并非在严格意义上提出同一套般若理论——《楞严》重在妙明真心、妄动与圆通，《心经》集中于般若空性，《胜鬘》侧重如来藏与自性清净心。不能因为它们都讲究竟智慧，就把它们混成一套。'''

INS.append(after('各派对五毒五智对应细节解释不一。',
                 TIB_EN + '\n\n' + HAIYUN_ZH + '\n\n' + HAIYUN_EN + '\n\n' + CLASSIC_ZH))

# ── 模型节英译块 ──
INS.append(after('般若与无明的关系从「相违」走向「同体」，「为什么」也随之从被回答变成被消解。〔本文判断〕',
'''> **英译对读 · 三·十三 三种关系模型**
>
> Three underlying models organize all ten systems〔本文判断〕. The **antidote model** (Āgama, Abhidharma, Madhyamaka, Yogācāra): ignorance and wisdom are mutually exclusive cognitions, one replacing the other; the origin is beginningless and not asked; practice is gradual and analytic; the risk is practice becoming a new grasping, with no metaphysical guarantee of success. The **infusion model** (tathāgatagarbha through the Awakening of Faith, used alongside Huayan): awakening and non-awakening share one mind and perfume each other — inner perfuming by suchness, outer conditions from teachers; the origin is "sudden," unsayable; prajñā is initial awakening according with original awakening; the risk is reading it as "the true mind produces the world." The **identity model** (Tiantai's inherent possession, Huayan's mutual containment, Chan, Vajrayāna, Dzogchen, Dōgen): the substance of ignorance is itself luminosity; the question of origin dissolves; practice is recognition, not destruction; the risk is moral slack dressed as no-practice. Along this line the concept of prajñā itself migrates — from the event of severing ignorance, to the mode of seeing emptiness, to the wisdom after transformation, to the nature of mind, to the very face of affliction — and the question "why?" migrates with it: from being answered to being dissolved.'''))

# ── §4.2 数学喻补记 ──
INS.append(after('它标出的是问题形式的边界。〔本文判断〕',
'''顺带把草稿里一个被作者自己否决的比喻记在案：完备的数学系统与使用它出错的人。它只能说明「根本层面的完备，不逻辑必然要求每一依之成立的活动都不出错」；但它预设了系统与一个站在系统之外的使用者——而众生不离真如，恰是这个比喻不能承载之处。弃用是正确的。〔本文判断〕'''))

# ── 4.3 后英译块 ──
INS.append(after('保持谨慎，不是不理解佛法，而是尊重经典自己对这个难题的定位。',
'''> **英译对读 · 四·三 六家安放**
>
> The six placements of the unsayable: each system parks the unlocatable origin somewhere else — in "only a Buddha can know" (Awakening of Faith, with perfuming explaining the return); in the luminosity itself taking itself as object (Śūraṅgama — the closest to a "reason," at the price of admitting a leaning within the perfect, exactly where Tiantai's critique of "pure mind as source" strikes); in dissolving the question (Perfect Enlightenment and Madhyamaka: no place of arising); in inherent possession (Tiantai: the perfect inherently contains the afflictive); in beginningless seeds with a non-producing suchness (Yogācāra — another hard fact, plus the five gotras); and in the ground's natural cognitive potential (Dzogchen — a groundless ground). No school offers a theodicy-grade derivation; each chooses where to put what does not add up — in suchness, seeds, emptiness, inherent nature, or the question itself.'''))

# ── 4.4 后英译块 ──
INS.append(after('辩护者以「依而无体」「不守自性」回应。〔大意〕',
'''> **英译对读 · 四·四 经证合读**
>
> The scriptures read together: the Śūraṅgama separates the *structure* of delusion (intrinsic luminosity mistaken as an object to be illuminated; the object falsely established, the subject follows; sameness and difference blaze forth) from its *groundlessness* ("delusion has no cause of its own; recognize that delusion has no cause and delusion has nothing to rest on; it never truly arose — what is there to extinguish?") and from the *conventional efficacy* of causality (three conditions severed, three causes unborn; "when the madness rests, that resting itself is bodhi"). The Perfect Enlightenment denies a real place of arising; the Laṅkāvatāra declares the beginning of saṃsāra unknowable while its cessation is fully practicable; the Śrīmālā names the whole relation "hard to understand." Read jointly: the nondual was never really made dual; ignorance never really entered; what remains is the conditional mechanism and its cessation.'''))

# ── 4.7 / 4.8（插在 §五 之前）──
SEC47 = '''### 4.7 三大真分歧

草稿第十五部分把各宗的分歧收成三条〔本文判断〕。**其一：无明是认知错误，还是心性上的根本不觉？**早期佛教与中观取前者——不必假设一个原本完整运作的宇宙觉知后来突然不觉；唯识把这种错误认知挖到意识结构深处（末那我执、赖耶种子）；如来藏与本觉则正面描述本来清净、具足觉性的心性及其与不觉的关系——于是必须面对「本来清净的心为何呈现无始染污」，而《胜鬘经》直接承认「難可了知」。这是各家不能混同之处。**其二：般若是破除错误认知，还是显发本来具足的智慧？**中观：如实洞察缘起性空，不另立智慧主体；唯识：认识二取虚妄、转识成智；如来藏本觉：还有显发本具觉性之义；禅：当下见性、无住不染的生命实践。解脱效果上可以相通，对「智慧究竟是什么」的理论定位不同。**其三：究竟是否存在一种本初明觉？**中观的严格解释不立独立恒常的本初意识；某些如来藏、本觉解释强调本来清净明觉的心性；大圆满的 Rigpa 又是另一套本初觉性理论。三者不能视为相同——中观的空性不是觉知主体，如来藏的本觉不是普通意识，Rigpa 也不能理解成独立存在的宇宙观察者。所谓非二元智慧，不能简单等同于各宗共同认可的一种「宇宙意识」。

### 4.8 继续参究的三个问题

结合全篇疑情，有三个问题值得带着修行继续参〔大意＋本文判断〕。**问题一：无明究竟是「不知」，还是「误知」？**若只是没有认识真实，般若就是补足缺失的认识；但若无明本身在运作、主动建立能知主体与所知对象（唯识尤其强调这一层），它就不是空缺，而是一种错误的认知结构——那么般若是否就是彻底看穿这种结构，发现从来没有一个独立的能知者与所知对象？**问题二：般若是本来具足，还是修行产生？**若本具，为何不自动显现？若修生，又如何认识超越生灭、超越能所的实相？宜区分四层：智慧的本具性质、智慧的现行功能、修行中的智慧增长、究竟佛智的圆满显发。**问题三：若般若超越能所，是谁在觉悟？**若还有一个主体在观察空性，就仍未离开能所结构；若般若不是主体的认知活动，又如何理解证悟？中观以无自性与二谛解释，唯识以二取消除与转依解释，如来藏以妄念止息、始觉合本觉解释，禅以无念无住表达——彼此参照，不应强行合并。

> **英译对读 · 四·七/八 分歧与三问**
>
> Three genuine disagreements cut across the schools〔本文判断〕: whether ignorance is a cognitive error or a root-level not-awakening of mind-nature (early Buddhism and Madhyamaka say error; Yogācāra digs the error into the structure of consciousness; tathāgatagarbha affirms a pure, intrinsically awake mind — and must then face why the pure presents as beginninglessly defiled, which the Śrīmālā calls "hard to understand"); whether prajñā dismantles error or manifests an endowed wisdom (seeing emptiness without positing a wisdom-substance; transforming the basis; revealing the innate; seeing one's nature in immediate life — compatible in effect, different in theory); and whether there is a primordial luminosity at all (Madhyamaka strictly declines; some tathāgatagarbha readings affirm; Dzogchen's rigpa is neither of the two — nondual wisdom is not a "cosmic consciousness" all schools endorse). Three questions keep the inquiry honest: is ignorance *not-knowing* or *mis-knowing* — does it merely lack the truth, or actively build the subject-object structure that prajñā then sees through? Is prajñā innate or cultivated — and how would the innate fail to show, the cultivated reach the unconditioned? Distinguish its nature, its function, its growth, its fullness. And if prajñā transcends subject and object, *who* awakens — a subject still watching emptiness has not left duality; each tradition answers differently, and the answers are to be consulted, not merged.'''
INS.append(('\n## 五、苦、受与束缚：感受为什么是真的',
            '\n' + SEC47 + '\n\n## 五、苦、受与束缚：感受为什么是真的'))

# ── 大 §四 英译块尾补数学喻一句 ──
OLD = 'For liberation, this is not a prerequisite: know how ignorance arises, sustains and ceases — the beginningless beginning is not the gate.'
INS.append((OLD, OLD + ' A rejected analogy deserves its verdict on record: the picture of a complete mathematical system with an error-prone *user* cannot carry the case, because its user stands outside the system, while beings never stand outside suchness.〔本文判断〕'))

# ── 附录A 六组读法 ──
INS.append(after('不建议同时遍学一切宗派。',
'''另一条入口是按功能分六组读〔大意〕：①《阿含经》与十二因缘——无明在生命、感受、执取与轮回中的实际作用；②《金刚经》与《心经》——般若如何破我执、法执、能所执与对智慧本身的执；③《中论》与《大智度论》——缘起性空、中道与菩萨般若；④《解深密经》与《瑜伽师地论》——八识、三性、二障、转依；⑤《大乘起信论》《胜鬘经》与《楞伽经》——本觉、不觉、如来藏及其甚深疑难；⑥《华严经》《楞严经》《圆觉经》——法界缘起、妙明真心、妄无所依与无生智慧。'''))

# ── 执行 ──
for anchor, repl in INS:
    uniq(anchor)
    s = s.replace(anchor, repl, 1)

io.open(PATH, 'w', encoding='utf-8', newline='').write(s)
print('OK: %d -> %d chars (+%d), %d edits' % (orig_len, len(s), len(s) - orig_len, len(INS)))
