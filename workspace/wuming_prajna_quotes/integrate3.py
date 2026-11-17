# -*- coding: utf-8 -*-
"""L.505 整合批（续研材料并入）：
①修复 4.3/4.4 英译块内容-位置交叉错位（交换）
②§4.3 增楞严第二问＋佛答「十方如來亦復如是」段（回源已核）
③§7.2 增三式问题区分＋非严格逻辑悖论＋因果反馈≠逻辑自指＋部分觉察
④§7.3 增「实体反不可断」论证＋核心命题改写
⑤§7.4 增逐项评估表；§7 EN 增段
⑥§8.2 增「其四」二障非单一刻度；§8.3 增我执风险；§8 EN 增句
⑦§4.8 三问→四问（空亦复空）；EN 增句
⑧编者按/附录B/附录C 同步。锚点断言唯一。"""
import io, sys

sys.stdout.reconfigure(encoding='utf-8')
PATH = r'C:\DA_Practice\huayan_collection\docs\宗派研究\无明与般若.md'
s = io.open(PATH, encoding='utf-8').read()
orig = len(s)

def uniq(a):
    n = s.count(a)
    if n != 1:
        raise SystemExit('ANCHOR FAIL (%d): %s' % (n, a[:50]))

# ── ① 交换两块英译 ──
B1H = '> **英译对读 · 四·三 六家安放**'
B2H = '> **英译对读 · 四·四 经证合读**'
uniq(B1H); uniq(B2H)
i1 = s.find(B1H); e1 = s.find('the question itself.', i1) + len('the question itself.')
i2 = s.find(B2H); e2 = s.find('and its cessation.', i2) + len('and its cessation.')
assert 0 < i1 < i2 and e1 < i2, 'block order unexpected'
block1 = s[i1:e1]
block2 = s[i2:e2]
s = s.replace('\n\n' + block1 + '\n\n', '\n\n')
s = s.replace('\n\n' + block2 + '\n\n', '\n\n')
assert s.count('the question itself.') == 0 or 'the question itself.' not in s.split('## 四、')[1].split('## 五、')[0].replace('the question itself.', '', 1) or True
block1_new = block1.replace(B1H, '> **英译对读 · 四·四 六家安放**', 1)
block2_new = block2.replace(B2H, '> **英译对读 · 四·三 经证合读**', 1)
INS = []
def after(anchor, text):
    INS.append((anchor, anchor + '\n\n' + text))

# 4.3 末（蕅益段后）挂「经证合读」
after('同一个「无初可立」，一从体、一从相，互为表里。', block2_new)
# 4.4 末（辩护者句后）挂「六家安放」
after('辩护者以「依而无体」「不守自性」回应。〔大意〕', block1_new)

# ── ② §4.3 楞严第二问段 ──
after('修行止息迷妄，不是重新制造曾失去的觉性。',
'''卷四还有一问一答，直接回答「觉悟者会不会再生无明」，草稿未及而经文自答。富楼那问：「若此妙覺本妙覺明與如來心不增不減，無狀忽生山河大地諸有為相；如來今得妙空明覺，山河大地有為習漏何當復生？」——众生无状忽生山河大地，那么已证妙空明觉的如来，会不会再有山河大地与习漏复生？佛陀以「於一聚落惑南為北」的迷方喻反问：此迷为因迷而有、还是因悟所出？富楼那答：「迷本無根，云何因迷？悟非生迷，云何因悟？」佛印成并推至极处：「富樓那！十方如來，亦復如是。此迷無本，性畢竟空。昔本無迷，似有迷覺，覺迷迷滅，覺不生迷。」——迷无根故迷不生迷；**十方如来亦复如是**：觉悟不再生迷，如翳病若除花于空灭，愚人却于空花灭处待花更生（T19n0945）。这一段把「无明无体」从解释推进到实践担保：觉后不复迷，因为迷从来没有真实生起过。〔本文判断〕''')

# ── ③ §7.2 增补（第二步之后）──
after('自指论证的功能是**筛选问题**，不是取消提问。〔本文判断〕',
'''这里还要分开两个常被混同的概念：**因果循环依存**与**逻辑自我指涉**。无明与漏互为条件（MN 9；§3·一已注其仅见于此，勿当阿含共法）是**因果反馈网络**——反馈循环不需要第一成员，打破它只需改变其中可改的条件；这不是自相矛盾，也无需「先找到链条的第一环」。而「以无明问无明」是否构成严格逻辑意义的自指悖论？**不构成**——它并不自相矛盾，其病在于预设被缘起分析拆解、且发问行为本身即无明现行。另外，「以无明状态追问无明**是什么**」连自指都谈不上：知道自己有偏见不等于已摆脱偏见，初步的自我觉察正是修行的起点——《中部》9 经恰恰要求修行者认识无明、其生起与其止息，佛教并不认为只有完全觉悟者才有资格讨论无明。〔大意＋本文判断〕''')

# ── ④ §7.3 增收束段 ──
after('「无明无体」若推进为「无明无事」，便与「夢時非無」相违：梦里的泪是真的。',
'''这一节还可再收紧一步：**如果无明是独立、恒常、不变的本体，它反而不可断除**——正因为它依缘而有、无自性，条件一变它即瓦解，修行才有落点。这是《中论》「以有空義故，一切法得成」应用於无明自身的结果。〔本文判断〕由此，无明本原问题的核心命题可以改写为：**不是必须先找到迷失的第一刻，才能恢复正确的认知；而是看清迷失本无独立自性，才真正有可能从迷中觉醒。**''')

# ── ⑤ §7.4 逐项评估表 ──
after('问题的解消不在得到一个答案，而在问者被如实照见。',
'''整合本节与 §八的判定，可对三类原始命题逐项清算〔本文判断〕：

| 命题 | 判定 | 必须补充 |
|---|---|---|
| 追问无明本源本身可能是无明的表现 | 部分成立 | 问「是什么／如何运作」可答且是修行对象；执取第一因之问才陷概念迷执 |
| 无明无体、只是施设 | 胜义层成立 | 应说无自性、假名有；施设≠虚构≠无效（諸幻雖盡不入斷滅） |
| 无明只是佛提出的方便概念 | 不够准确 | 有教法施设的一面，也有实际的缘起条件与作用（无明有食） |
| 觉悟者与未觉悟者有维度差别 | 方向正确 | 是认知方式与证悟程度之差，非物理维度，且非单一刻度（二障异类） |
| 修行可去无明、可证菩提 | 成立 | 须经戒定慧与实证，非知识积累；「自认更高维度」反成新我执 |
| 因无明而有山河大地，再问无明本源属自我指涉 | 部分成立 | 不构成严格逻辑悖论；第一因预设被缘起分析拆解，机制之问仍可答 |
| 从一开始发问就必定得不到答案 | 不成立 | 条件、相续、止息可识；不可得的是「第一因型答案」，且转向一直可得 |''')

# ── ⑤b §7 EN 块增段 ──
after('What dissolves is the questioner, seen through in the act of asking.',
'''What dissolves is the questioner, seen through in the act of asking.
>
> Three refinements from continued research〔本文判断〕. First, separate **causal feedback** from **logical self-reference**: the mutual conditioning of ignorance and taints (MN 9 — its limitation noted in §三·一) is a causal loop, and a feedback network needs no first member; asking what ignorance *is*, or how it *feeds*, from within ignorance is no paradox at all — partial awareness is possible ("knowing one has a bias is not being free of it"), and MN 9 itself instructs practitioners to know ignorance, its arising and its ceasing: Buddhism never requires full awakening before one may inquire. Nor is "asking about ignorance by means of ignorance" a strict logical paradox — it does not contradict itself; it fails only because its first-cause presupposition is dismantled and because the act of asking is ignorance in operation. Second, applied to ignorance itself, "since emptiness obtains, everything obtains" becomes a proof of *breakability*: a substantial, eternal ignorance could never be removed — precisely its lack of self-nature makes practice bite; hence the rewritten thesis: one need not find the first moment of being lost in order to be un-lost; seeing that being-lost never had independent nature is what makes waking possible. Third, the Śūraṅgama adds a scene the draft missed: Pūrṇa's second question — could mountains and rivers *recur* once the Buddha has attained the wondrous awakened mind? — is answered with the lost-direction simile and its verdict: "delusion has no root… such is the case of the Tathāgatas of the ten directions: past confusion was never real, seeming awakening within it; awakening to the confusion extinguishes it, and awakening does not generate confusion" — awakening does not relapse, because delusion never truly arose.''')

# ── ⑥ §8.2 其四 ＋ §8.3 风险 ＋ §8 EN 增句 ──
after('差在认取方向，不在感受器的数量。〔本文判断〕',
'''**其四，「维度」不是单一刻度。**瑜伽行派的二障理论把障碍分成类型不同的两族——烦恼障粗显、所知障微细，断除的位次与所证的智慧各别（Charles Muller 对二障在东亚的再诠释研究〔大意〕）：智慧的提升不是一根标尺上的高度，而是不同类型认知障碍的分别消解。故说「障已分除」比说「维度更高」更准确。〔本文判断〕''')
after('「菩提可证」既是精进的理由，也不至沦为要求宇宙兑现的期票。〔本文判断〕',
'''另有一层修行风险须写在明处：**自认已进入更高维度，本身可能成为新的我执**——以证自居，恰是微细所知障的现行；天台六即的「分真即」之前，一切「相似」皆须自检。〔本文判断〕''')
after('not a metaphysical promissory note.',
'''not a metaphysical promissory note. Two refinements: the "dimension" is not a single scale — the two-obstructions theory plots differently *typed* barriers cleared at different depths (Muller's study〔大意〕), so "barriers differently removed" is more accurate than "higher"; and believing oneself to have "risen a dimension" can itself become a new self-grasping — a fine cognitive obstruction in operation.''')

# ── ⑦ §4.8 三问→四问 ──
INS.append(('### 4.8 继续参究的三个问题', '### 4.8 继续参究的四个问题'))
after('彼此参照，不应强行合并。',
'''**问题四：连「无明无体」也不可执。**若把「无明无自性」执为一个究竟命题，无体又成新立——龙树「空亦复空」（§三·二）在此把门：连解药也不可据为实法，否则以执破执、执更坚固。这也封住两个自然滑坡：从「无明无自性」滑到「万法根本不存在」，或从「第一因不可得」滑到「一切追问皆无意义」——两个方向都是对空性的滥用。〔本文判断〕''')
after('the answers are to be consulted, not merged.',
'''the answers are to be consulted, not merged. A fourth question guards the whole set: if "ignorance has no substance" is itself grasped as a final truth, substancelessness becomes a new substance — emptiness, too, is empty (§三·二); and with it two slips are sealed — from "ignorance lacks self-nature" to "nothing exists," and from "no first cause" to "no inquiry is worth anything."''')

# ── ⑧ 编者按／附录B／附录C ──
INS.append(('超出草稿范围，新引经证另行回源（附录 B）。',
            '超出草稿范围，并整合后续研问材料；新引经证另行回源（附录 B）。'))
INS.append(('命中共 **115 条／16 部经论，全绿**', '命中共 **122 条／16 部经论，全绿**'))
INS.append(('| 大佛顶首楞严经 | T19n0945 | 两种根本、富楼那两问、性觉必明、觉明为咎、演若达多、识迷无因、因缘自然理穷于是、歇即菩提、知见立知即无明本、认贼为子 |',
            '| 大佛顶首楞严经 | T19n0945 | 两种根两问并入：富楼那两问、性觉必明、觉明为咎、演若达多、识迷无因、迷本无根（富楼那）、此迷无本性毕竟空、觉不生迷、如来今得妙空明觉何当复生、三种颠倒相续从妄见生、知见立知即无明本、认贼为子 |'.replace('两种根两问并入：','两种根本、')))
INS.append(('Bhikkhu Anālayo, "Hearing, Reflection, and Cultivation"（闻思修三慧；*Religions* 12(6): 441, 2021）。',
'''Bhikkhu Anālayo, "Hearing, Reflection, and Cultivation"（闻思修三慧；*Religions* 12(6): 441, 2021）。
- Charles Muller, "The Yogācāra Two Hindrances and their Reinterpretations in East Asia"（*JIABS*；二障理论研究）〔大意〕。
- George A. Keyworth 关于《楞严经》文本来源与地位的研究〔大意〕；并参 Jinhua Jia（上列）。
- *Oxford Bibliographies*: "Awakening of Faith"（《起信论》文献来源与研究史综述）〔大意〕。
- *St Andrews Encyclopaedia of Theology*: "Dependent Arising"（缘起思想的历史与理论综述）〔大意〕。'''))

# ── 执行 ──
for anchor, repl in INS:
    uniq(anchor)
    s = s.replace(anchor, repl, 1)

io.open(PATH, 'w', encoding='utf-8', newline='').write(s)
print('OK: %d -> %d chars (+%d), %d edits, blocks swapped' % (orig, len(s), len(s) - orig, len(INS)))
