# -*- coding: utf-8 -*-
"""〇之二内容地图层·扩展 P23–P37（依赖 p7_p18_atlas.apply）
用法：python scripts/p23_p37_atlas.py P23 P24 ...   （无参＝全部）
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p7_p18_atlas as base

DIR5 = os.path.join('docs', '经学文献', '华严经细读', '第五会_兜率天宫_回向位')
DIR6 = os.path.join('docs', '经学文献', '华严经细读', '第六会_他化自在天宫_十地位')
DIR7 = os.path.join('docs', '经学文献', '华严经细读', '第七会_普光明殿_等觉')
DIR8 = os.path.join('docs', '经学文献', '华严经细读', '第八会_普光明殿_离世间')
DIR9 = os.path.join('docs', '经学文献', '华严经细读', '第九会_逝多林_证入法界')

W = 'width="100%" style="max-width:1000px;height:auto"'

P23 = {
    "tag": "P23",
    "path": os.path.join(DIR5, "华严经细读_第二十三部_十回向品.md"),
    "hui": "第五会（兜率天宫·回向位）",
    "dingwei": "本品 75,744 CJK 为**全经最大单一品**，金刚幢菩萨说十回向。读法以**心量十级放大**为纲：从「救护一人」到「等法界量」，每一回向是心量的一次换挡；而十向的愿文皆以「令一切眾生……」领起——放大不是向内收摄，是向众生的普遍化（§4.5 会读十卡）。",
    "yiju": "**以无相之体，行无尽之愿，等法界之量**——回自向他、回因向果，而实无所回（§4.5 总汇）。",
    "sanwen": "①回向回向何处？三处（众生·菩提·实际）如何不偏？②十向递进是位次还是心量？③「離眾生相」与「恒順眾生」如何同持？",
    "tiyao": "本品占**卷第二十三～三十三**，剥校勘 **CJK 75,744 字**。**长行 341 段＋偈组 10**；结构：**序分（金刚幢入定加持）→ 十回向各说（每向：问式＋愿海连排＋利益结）→ 重颂**。会读十卡见 §4.5（L.287 补齐）。",
    "xufa": "先观图 〇-1 以得其量（心量十级放大），次观图 〇-2 以得其构（体行两翼），次读 §2 十向全引（问式与愿格式），次读 §4.5 十卡四件套，末以 §7 数据层核其量。",
    "en_map": "At 75,744 characters this is the longest single chapter of the sūtra. Vajra-Garbha expounds ten dedications, each opening with 'How does a bodhisattva dedicate…?' and unfolding oceans of vows 'for all beings' — the heart's measure放大 enlarged ten times, from rescuing one being to equaling the dharmadhātu.",
    "figs": [
        {
            "n": 1,
            "title": "心量十级放大图",
            "what": "十回向＝心量的十次换挡",
            "one": "救护一人→等法界量：级级外推",
            "svg": f"""<svg viewBox="0 0 1000 380" {W} xmlns="http://www.w3.org/2000/svg" font-family="serif">
<text x="500" y="26" text-anchor="middle" font-size="14.5" font-weight="bold" fill="#7a5a28">十回向：心量的十级放大（§4.5）</text>
<text x="500" y="46" text-anchor="middle" font-size="11.5" fill="#8a7a5e">阶梯＝心量外推；右侧＝本参之眼目</text>
""" + "".join(
f"""<rect x="{60+i*92}" y="{300-i*24}" width="86" height="{24+i*24}" fill="#f6efe1" stroke="#b8863c"/>
<text x="{103+i*92}" y="{315-i*24//1}" text-anchor="middle" font-size="10" fill="#7a5a28">{['①救护','②不坏','③等佛','④至处','⑤无尽','⑥坚固','⑦随顺','⑧真如','⑨解脱','⑩法界'][i]}</text>"""
for i in range(10)) + f"""
<text x="60" y="340" font-size="11" fill="#5a5147">①救一人 → ⑩等法界：量有上限即心有上限（卡⑩）</text>
<text x="500" y="364" text-anchor="middle" font-size="12" fill="#5a5147">愿文皆以「令一切眾生……」领起——放大即向众生的普遍化</text>
</svg>""",
            "cap": "十级放大：①救一人、②信不坏、③等佛、④遍至、⑤无尽、⑥坚固、⑦随顺、⑧真如、⑨解脱、⑩等法界（§4.5 十卡）。",
            "en": "Ten dedications read as ten enlargements of the heart's measure, from rescuing beings to equaling the dharmadhātu.",
            "dufa": [
                "先看阶梯的**方向**：不是位次爬高，是心量外推——每级多容纳一类众生。",
                "再看每级**眼目**（右侧会读卡）：⑥坚固是炼金段、⑦乞者反转是最具杀伤力的一句。",
                "末记总汇：三处回向（众生·菩提·实际）在「实无所回」处合流。",
            ],
        },
        {
            "n": 2,
            "title": "体行两翼图",
            "what": "十回向的体段与行段",
            "one": "①②⑧⑨⑩为体翼；③④⑤⑥⑦为行翼",
            "svg": f"""<svg viewBox="0 0 1000 380" {W} xmlns="http://www.w3.org/2000/svg" font-family="serif">
<text x="500" y="26" text-anchor="middle" font-size="14.5" font-weight="bold" fill="#7a5a28">体行两翼：十回向的骨架（§4.5）</text>
<rect x="60" y="60" width="380" height="280" fill="#f6efe1" stroke="#b8863c"/>
<text x="250" y="88" text-anchor="middle" font-size="13" font-weight="bold" fill="#7a5a28">体翼（所依）</text>
<text x="250" y="126" text-anchor="middle" font-size="11.5" fill="#5a5147">① 救護眾生離眾生相——无相之体</text>
<text x="250" y="156" text-anchor="middle" font-size="11.5" fill="#5a5147">② 不壞——不坏信之基</text>
<text x="250" y="196" text-anchor="middle" font-size="11.5" fill="#5a5147">⑧ 真如相——理体枢纽</text>
<text x="250" y="226" text-anchor="middle" font-size="11.5" fill="#5a5147">⑨ 無著無縛解脫——能行之相</text>
<text x="250" y="266" text-anchor="middle" font-size="11.5" fill="#5a5147">⑩ 等法界無量——量之终点</text>
<text x="250" y="310" text-anchor="middle" font-size="10.5" fill="#8a7a5e">※⑨⑩名目照经正（L.287）</text>
<rect x="560" y="60" width="380" height="280" fill="none" stroke="#d4a03c" stroke-dasharray="5,3"/>
<text x="750" y="88" text-anchor="middle" font-size="13" font-weight="bold" fill="#7a5a28">行翼（能行）</text>
<text x="750" y="126" text-anchor="middle" font-size="11.5" fill="#5a5147">③ 等一切佛——随学</text>
<text x="750" y="156" text-anchor="middle" font-size="11.5" fill="#5a5147">④ 至一切處——遍至</text>
<text x="750" y="186" text-anchor="middle" font-size="11.5" fill="#5a5147">⑤ 無盡功德藏——无尽</text>
<text x="750" y="216" text-anchor="middle" font-size="11.5" fill="#5a5147">⑥ 隨順堅固——坚固（炼金段·施身）</text>
<text x="750" y="246" text-anchor="middle" font-size="11.5" fill="#5a5147">⑦ 等隨順一切眾生——随顺（乞者反转）</text>
<text x="750" y="300" text-anchor="middle" font-size="10.5" fill="#8a7a5e">两翼交错：前行后体，体行不二</text>
<text x="500" y="364" text-anchor="middle" font-size="12" fill="#5a5147">以无相之体，行无尽之愿，等法界之量</text>
</svg>""",
            "cap": "体行两翼：体翼立所依（无相·不坏·真如·解脱·等量），行翼立能行（随学·遍至·无尽·坚固·随顺）。",
            "en": "The ten dedications split into a 'substance wing' and a 'practice wing', interlocking so that practice rests on emptiness and emptiness issues practice.",
            "dufa": [
                "先分翼读：遇每一向先问它是「立体」还是「起行」。",
                "再看翼间**钩连**：②之信为③随学之基，⑧之真如为⑥坚固之淬炼场。",
                "末以总汇一句收：回向之名由此立——回而无回。",
            ],
        },
    ],
    "weici_note": "本品居第五会正宗：承十藏（品22）之流出，启十地（品24）之入位；六十本〈十回向品〉同题对应〔逐段对勘未竟〕。",
    "weici": [
        ["十無盡藏品（品 22）", "卷二十三前", "第四会末·藏之体", "藏重含摄", "本品十向＝藏之流出（用）"],
        ["十地品（品 24）", "卷三十四起", "第六会·十地位", "回向满故入地", "⑩等法界量→初地证法界"],
        ["藏译 Toh 44", "德格 035 卷（L.201 TOC）", "本品对应章", "开篇实测", "逐字对勘未竟"],
        ["六十《十回向品》", "晋译同题", "品次对应", "文较略", "对读未竟"],
        ["会读十卡（§4.5）", "L.287 补齐", "本品读法层", "四件套×10", "深化批成果"],
    ],
    "teshe_note": "本品之形特征以体量与格式为最；数字出处逐条标注。",
    "teshe": [
        ["篇幅", "75,744 CJK／341 `<p>`＋10 `<lg>`（§7）", "品24 的 43,413", "全经最大单一品"],
        ["问式", "「云何為菩薩摩訶薩X迴向」", "十地向十定皆有问式", "参学语法之源"],
        ["愿格式", "「令一切眾生……」连排", "〈普賢行願品〉同构", "愿皆他利"],
        ["名目对勘", "⑨無著無縛解脫·⑩等法界無量", "旧记「無縛無著·入法界無量」", "照经正（L.287）"],
    ],
    "dufa5": [
        ["放大读法", "图 〇-1 → §4.5 十卡", "结构读者", "心量十级外推"],
        ["体行读法", "图 〇-2 → §2 各向", "义理读者", "两翼交错·体行不二"],
        ["名目读法", "§2.0 总表＋⑨⑩纠错", "校勘读者", "照经正名"],
        ["会读读法", "§4.5 十卡四件套", "会读读者", "乞者反转·真如枢纽"],
        ["数据读法", "§7＋dataset", "数据读者", "75,744/341p/10lg"],
    ],
    "shu": [
        ["**T0 经文明文**", "问式＋愿海连排", "§2（`T10n0279` 全引）", "结构总量"],
        ["**T0 本文实测**", "75,744 CJK／341p＋10lg", "§7（剥校勘）", "篇幅与信度"],
        ["**T1 注疏**", "金刚幢入定加持", "`T1735` §5.1", "疏之判"],
        ["**会读层**", "十卡四件套＋同异辨", "§4.5（L.287）", "深化成果"],
        ["**T0·六十本实测**", "晋译同题对应", "`T09n0278`（§6）", "对读未竟"],
        ["**T0·藏本实测**", "Toh44 开篇", "L.201 TOC", "对勘未竟"],
    ],
    "shu_note": "> 【读法】本品之数以「**放大**」为性：十向即十次心量换挡——读时逐级自问「我的心量停在第几级」。\n",
}

P24 = {
    "tag": "P24",
    "path": os.path.join(DIR6, "华严经细读_第二十四部_十地品.md"),
    "hui": "第六会（他化自在天宫·十地位）",
    "dingwei": "本品 43,413 CJK 跨七卷，金刚藏菩萨入定受加、解脱月三请而说十地——**全经教义最高峰之一**。读法以**十地阶梯**为纲：每一地一波罗蜜增上、一果报王身、一「是名略说」收束印；十印三处句式变体是本品的校勘指纹（L.285）。",
    "yiju": "**回向满故入地——地是修行之实证阶位，一地一波罗蜜，一地一王身。**",
    "sanwen": "①「地」如何读——位次还是心量？②十印三变体说了什么编纂秘密？③果报「多作某王」与因地行如何对表？",
    "tiyao": "本品占**卷第三十四～四十**，剥校勘 **CJK 43,413 字**。**长行 264 段＋偈组 27**；结构：**序分→金刚幢入定→解脱月三请→十地各说（每地含入地心·行相·果报）→重颂（十山喻·十相·摩尼珠喻）**。",
    "xufa": "先观图 〇-1 以得其阶（十地十度十王），次观图 〇-2 以得其缝（十印切分与三变体），次读 §2 全引（L.285 四批注入），次读 §4 义理，末以 §7 核量。",
    "en_map": "At 43,413 characters across seven fascicles, Vajra-Garbha expounds the ten grounds, each marked by one perfected pāramitā and a kingly rebirth, sealed ten times by closing formulas in three textual variants.",
    "figs": [
        {
            "n": 1,
            "title": "十地阶梯图",
            "what": "一地一度一王身",
            "one": "欢喜（布施）→法云（智）",
            "svg": f"""<svg viewBox="0 0 1000 380" {W} xmlns="http://www.w3.org/2000/svg" font-family="serif">
<text x="500" y="26" text-anchor="middle" font-size="14.5" font-weight="bold" fill="#7a5a28">十地阶梯：一地一度一王（§2 十印切分）</text>
""" + "".join(
f"""<rect x="{50+i*92}" y="{316-i*28}" width="88" height="{28+i*28}" fill="#f6efe1" stroke="#b8863c"/>
<text x="{94+i*92}" y="{332-i*28}" text-anchor="middle" font-size="9.5" fill="#7a5a28">{['①欢喜·布施','②离垢·持戒','③发光·忍','④焰慧·精进','⑤难胜·禅','⑥现前·般若','⑦远行·方便','⑧不动·愿','⑨善慧·力','⑩法云·智'][i]}</text>
<text x="{94+i*92}" y="{346-i*28}" text-anchor="middle" font-size="8.5" fill="#8a7a5e">{['閻浮提王','轉輪聖王','三十三天','須夜摩天','兜率天','善化天','自在天','—','—','摩醯首羅'][i]}</text>"""
for i in range(10)) + f"""
<text x="50" y="352" font-size="10.5" fill="#8a7a5e">下排＝果报「多作某王」（①⑦⑩实测；⑧⑨标「—」待深化批）·上排＝地·度</text>
<text x="500" y="372" text-anchor="middle" font-size="12" fill="#5a5147">回向满故入地——地是行愿的实证阶位</text>
</svg>""",
            "cap": "十地阶梯：每地一增上波罗蜜、一果报王身（§2 逐地节头·L.285 实测）。",
            "en": "A staircase of ten grounds, each with its pāramitā and kingly rebirth, sealed by closing formulas.",
            "dufa": [
                "先看阶梯与王身的**对表**：因行与果报隔一印相望。",
                "再注意⑧⑨的「—」：非经无文，是深化批定位未竟（如实）。",
                "末沿阶梯自问：当前立在何地之门外？",
            ],
        },
        {
            "n": 2,
            "title": "十印三变体图",
            "what": "收束印的句式指纹",
            "one": "「入初地門／是名菩薩／略說諸菩薩」",
            "svg": f"""<svg viewBox="0 0 1000 380" {W} xmlns="http://www.w3.org/2000/svg" font-family="serif">
<text x="500" y="26" text-anchor="middle" font-size="14.5" font-weight="bold" fill="#7a5a28">十印切分与三处变体（L.285 勘定）</text>
<text x="120" y="70" text-anchor="middle" font-size="12" font-weight="bold" fill="#7a5a28">标准式 ×7</text>
<rect x="40" y="84" width="380" height="46" fill="#f6efe1" stroke="#b8863c"/>
<text x="230" y="104" text-anchor="middle" font-size="11" fill="#5a5147">「是名：略說菩薩摩訶薩第X〔地名〕地」</text>
<text x="230" y="122" text-anchor="middle" font-size="9.5" fill="#8a7a5e">二四五六七十（L.285 实测位）</text>
<text x="120" y="170" text-anchor="middle" font-size="12" font-weight="bold" fill="#7a5a28">变体一（初地）</text>
<rect x="40" y="184" width="380" height="46" fill="none" stroke="#d4a03c" stroke-dasharray="5,3"/>
<text x="230" y="204" text-anchor="middle" font-size="11" fill="#5a5147">「略說菩薩摩訶薩**入菩薩初地門**，廣說則有……」</text>
<text x="230" y="222" text-anchor="middle" font-size="9.5" fill="#8a7a5e">初地以「门」代「地」——入处之语</text>
<text x="120" y="270" text-anchor="middle" font-size="12" font-weight="bold" fill="#7a5a28">变体二、三（三地·八地）</text>
<rect x="580" y="184" width="380" height="46" fill="none" stroke="#d4a03c" stroke-dasharray="5,3"/>
<text x="770" y="204" text-anchor="middle" font-size="11" fill="#5a5147">「**是名菩薩**第三發光地」·「略說**諸**菩薩……第八不動地」</text>
<text x="770" y="222" text-anchor="middle" font-size="9.5" fill="#8a7a5e">省「略說」／多「諸」——编纂层微迹</text>
<text x="500" y="330" text-anchor="middle" font-size="11.5" fill="#5a5147">十印为切分锚：印后随己地果报段（多作X王·波罗蜜偏多）</text>
<text x="500" y="356" text-anchor="middle" font-size="12" fill="#5a5147">变体不是讹误，是编纂层的指纹——照各底本、不统一</text>
</svg>""",
            "cap": "十印切分与三变体：标准式七处＋初地「门」式＋三地八地微变（L.285 勘定）。",
            "en": "Ten closing seals in three textual variants — the compilation fingerprint guiding this chapter's segmentation.",
            "dufa": [
                "先认印：每地读毕即遇印，印后是本地的果报段。",
                "再看变体：三处微差是底本层痕迹，各照底本不统一。",
                "末以图 〇-1 回看全阶：印与印之间即一地。",
            ],
        },
    ],
    "weici_note": "本品居第六会正宗：承十回向（品23）之满，启十定（品25）之等觉；六十〈十地品〉同题、世亲《十地经论》为古疏大宗〔论不在仓·存目〕。",
    "weici": [
        ["十回向品（品 23）", "卷二十三起", "第五会·回向位", "等法界量", "回向满故入地"],
        ["十定品（品 25）", "卷四十起", "第七会·等觉", "定境展开", "地满入定"],
        ["藏译 Toh 44 ch 28–29", "德格 035 卷 fol 347b/368b", "跨章对应", "开篇实测（L.266）", "逐字对勘未竟"],
        ["六十《十地品》", "晋译同题", "品次对应", "文较略", "对读未竟"],
        ["重颂组", "27 `<lg>`", "十山喻·十相·摩尼珠", "偈体总持", "§2 结分全引"],
    ],
    "teshe_note": "本品之形特征以跨卷与印式为最；数字出处逐条标注。",
    "teshe": [
        ["篇幅", "43,413 CJK／264 `<p>`＋27 `<lg>`（§7）", "品23 的 75,744", "跨七卷"],
        ["收束印", "十印·三变体", "他品无此密集印式", "编纂指纹（图〇-2）"],
        ["果报段", "印后「多作某王」+「波罗蜜偏多」", "各段结构同构", "因地对表"],
        ["重颂", "十山喻·十相·摩尼珠", "品22 重颂 2,280", "偈体总持相当"],
    ],
    "dufa5": [
        ["阶梯读法", "图 〇-1 → §2 十地全引", "结构读者", "一地一度一王"],
        ["印式读法", "图 〇-2 → §2 切分", "校勘读者", "十印三变体"],
        ["因果读法", "节头「增上／多作」", "义理读者", "因地果报对表"],
        ["重颂读法", "结分（十山喻等）", "文学读者", "长行偈颂互锁"],
        ["对勘读法", "§6.3＋藏 Toh44", "版本学读者", "逐字对勘未竟"],
    ],
    "shu": [
        ["**T0 经文明文**", "十地名目＋十印", "§2（`T10n0279` 全引）", "结构总量"],
        ["**T0 本文实测**", "43,413 CJK／264p＋27lg", "§7", "篇幅与信度"],
        ["**T1 注疏**", "「藏者含摄」等", "`T1735` §5.1", "疏之训"],
        ["**果报实测**", "增上波罗蜜＋多作王（节头）", "L.285 meta", "七地核实·三处标—"],
        ["**T0·藏本实测**", "ch28–29 开篇", "L.201 TOC", "对勘未竟"],
        ["**T0·六十本实测**", "晋译同题", "`T09n0278`", "对读未竟"],
    ],
    "shu_note": "> 【读法】本品之数以「**阶**」为性：十地十印十王——读时以印为节，一印一歇。\n",
}

P25 = {
    "tag": "P25",
    "path": os.path.join(DIR7, "华严经细读_第二十五部_十定品.md"),
    "hui": "第七会（普光明殿·等觉位）",
    "dingwei": "本品 27,028 CJK 为第七会首品，普贤说十种三昧——读法以**十定即十遍**为纲：普光明（遍光）至無礙輪（遍轮），每一定内含一组十法；念请（无口问·世尊劝敬「想普賢身現在其前」）是本品的仪式眼。",
    "yiju": "**定非枯坐——十定即十种遍入法界之行相。**",
    "sanwen": "①定如何读为「遍」？②念请与观想如何成为请法？③名目七误如何正（L.282）？",
    "tiyao": "本品占**卷第四十～四十四**，剥校勘 **CJK 27,028 字**。**长行 49 段＋偈组 0（纯长行）**；结构：**序分（念请＋劝敬）→ 十种三昧各说（每定「云何」发问·内含十法组）**。L.282 纠骨架手抄名目七处。",
    "xufa": "先观图 〇-1 以得其遍（十定十遍），次观图 〇-2 以得其正（名目纠错对照），次读 §2 全引，次读 §4 义理（定中法数），末以 §7 核量。",
    "en_map": "At 27,028 characters, the assembly asks only in thought; the Buddha bids them venerate Samantabhadra, who expounds ten samādhis — each a mode of pervading the dharmadhātu, each unfolding its own tenfold dharma-set.",
    "figs": [
        {
            "n": 1,
            "title": "十定十遍图",
            "what": "每一定一个「遍」",
            "one": "普光明→無礙輪",
            "svg": f"""<svg viewBox="0 0 1000 300" {W} xmlns="http://www.w3.org/2000/svg" font-family="serif">
<text x="500" y="26" text-anchor="middle" font-size="14.5" font-weight="bold" fill="#7a5a28">十定即十遍（§2.2 实测纠错版）</text>
""" + "".join(
f"""<rect x="{40+(i%5)*188}" y="{56+(i//5)*92}" width="176" height="76" rx="8" fill="#f6efe1" stroke="#b8863c"/>
<text x="{128+(i%5)*188}" y="{82+(i//5)*92}" text-anchor="middle" font-size="10.5" font-weight="bold" fill="#7a5a28">{i+1}.{['普光明','妙光明','次第遍往諸佛國土神通','清淨深心行','知過去莊嚴藏','智光明藏','了知一切世界佛莊嚴','一切眾生差別身','法界自在','無礙輪'][i]}</text>
<text x="{128+(i%5)*188}" y="{104+(i//5)*92}" text-anchor="middle" font-size="10" fill="#8a7a5e">{['遍光','遍明','遍刹游历','遍心行','遍过去藏','遍智光','遍佛庄严','遍众生身','遍法界','遍轮无碍'][i]}〔本文判〕</text>
<text x="{128+(i%5)*188}" y="{122+(i//5)*92}" text-anchor="middle" font-size="9" fill="#5a5147">节首：有十種{['無盡法','無盡藏','無礙業','深心行','莊嚴藏','光明藏','佛莊嚴','差別身','自在法','無礙輪'][i]}〔核订〕</text>"""
for i in range(10)) + f"""
<text x="500" y="286" text-anchor="middle" font-size="12" fill="#5a5147">定不是收敛而是展开——每定一法数组（§4）</text>
</svg>""",
            "cap": "十定十遍：普光明→無礙輪，每定节首句眼「有十種X」〔核订〕。",
            "en": "Ten samādhis read as ten modes of pervading: from Universal Light to Unobstructed Wheel, each containing its tenfold set.",
            "dufa": [
                "先按「遍」字读十名：定名即行相。",
                "再入任一定内读其十法组：定中有数。",
                "末回念请段：观想即请法。",
            ],
        },
        {
            "n": 2,
            "title": "名目纠错对照图",
            "what": "骨架手抄误→经文正",
            "one": "七处依经正（L.282）",
            "svg": f"""<svg viewBox="0 0 1000 300" {W} xmlns="http://www.w3.org/2000/svg" font-family="serif">
<text x="500" y="26" text-anchor="middle" font-size="14.5" font-weight="bold" fill="#7a5a28">名目纠错：手抄误 → 经文正（L.282）</text>
""" + "".join(
f"""<text x="70" y="{70+i*40}" font-size="11" fill="#a04a3a" text-decoration="line-through">{e[0]}</text>
<text x="330" y="{70+i*40}" font-size="11" fill="#5a5147">→</text>
<text x="370" y="{70+i*40}" font-size="11" fill="#4a7c59" font-weight="bold">{e[1]}</text>"""
for i, e in enumerate([
    ('普光大三昧','普光明三昧'), ('妙光明大三昧','妙光明三昧'),
    ('次第遍往諸方國土大三昧','次第遍往諸佛國土神通三昧'),
    ('知過去莊嚴藏大三昧','知過去莊嚴藏三昧'),
    ('了知一切佛福德大三昧','了知一切世界佛莊嚴三昧'),
    ('普現一切如來前大三昧','一切眾生差別身三昧'),
    ('無著清淨大三昧','無礙輪三昧'),
])) + f"""
<text x="500" y="272" text-anchor="middle" font-size="11.5" fill="#5a5147">教训：名目必须程序回源——手抄七误皆因「凭印象补名」</text>
</svg>""",
            "cap": "名目纠错对照：骨架期七处手抄误（左）依经文正（右）——M0.4 之实例教学。",
            "en": "Seven mis-copied samādhi names corrected against the text — a worked example of source-verification discipline.",
            "dufa": [
                "对照读：左列即「编造风险」清单。",
                "右列读法：以经文节首「云何為菩薩摩訶薩X」为唯一权威。",
                "末记教训：凡引名必回源。",
            ],
        },
    ],
    "weici_note": "本品居第七会首：承十地（品24）之满，启十通（品26）之用；六十本阙此品（阙本考〔待深化批〕）。",
    "weici": [
        ["十地品（品 24）", "卷三十四起", "第六会·十地位", "地满", "定之基"],
        ["十通品（品 26）", "卷四十五", "第七会·果用", "定生通", "通为定之用"],
        ["藏译 Toh 44", "德格 035 卷（fol 375b 一带〔核订〕）", "对应章", "开篇待实测", "逐字对勘未竟"],
        ["六十本", "阙此品", "三十四品不具", "阙本考〔待深化批〕", "新旧译品次异"],
        ["念请格式", "「作是念」＋世尊劝敬", "参27 念请之先声", "观想即请法", "仪式眼"],
    ],
    "teshe_note": "本品之形特征以纯长行与念请为最。",
    "teshe": [
        ["篇幅", "27,028 CJK／49 `<p>`＋0 `<lg>`（§7）", "品26 的 3,646", "等觉位大体量"],
        ["纯长行", "无偈颂组", "品26 同为纯长行", "定境非偈咏所能传"],
        ["念请", "无启请人·心念十问", "品39 参学口问", "观想即请法"],
        ["名目纠错", "七处（图〇-2）", "P24 十印变体", "M0.4 实例"],
    ],
    "dufa5": [
        ["十遍读法", "图 〇-1 → §2.2", "结构读者", "定名即行相"],
        ["纠错读法", "图 〇-2 → §2.0 表", "校勘读者", "名目必回源"],
        ["念请读法", "§2.1 序分", "仪式读者", "观想即请法"],
        ["法数读法", "节首「有十種X」", "义理读者", "定中有法数"],
        ["阙本读法", "§6.3＋六十阙考", "版本学读者", "新旧译品次异"],
    ],
    "shu": [
        ["**T0 经文明文**", "十定名目（节首十法组）", "§2.2（`T10n0279` 全引）", "结构总量"],
        ["**T0 本文实测**", "27,028 CJK／49p＋0lg", "§7", "篇幅与信度"],
        ["**T1 注疏**", "「初明來意」（变体）", "`T1735` §5.1（L.282 程序化）", "疏之判"],
        ["**纠错层**", "名目七处正（图〇-2）", "L.282", "M0.4 实例"],
        ["**T0·六十本实测**", "阙此品", "六十 34 品", "阙本考待批"],
        ["**T0·藏本实测**", "fol 375b 一带〔核订〕", "L.201 TOC", "对勘未竟"],
    ],
    "shu_note": "> 【读法】本品之数以「**遍**」为性：十定十遍，遍遍有法——读时逐定问「此遍遍的是什么」。\n",
}

P26 = {
    "tag": "P26",
    "path": os.path.join(DIR7, "华严经细读_第二十六部_十通品.md"),
    "hui": "第七会（普光明殿·等觉位）",
    "dingwei": "本品 3,646 CJK，普贤说十种智通——读法以**通即遍知**为纲：十通皆「以X智通」起（知心·见·忆念·知劫·闻·住无体性·知语·现色身·知法·灭），通是认知半径的扩展，非神异夸饰。",
    "yiju": "**十通非神异夸饰——一一智通皆「知」字当头，通即遍知。**",
    "sanwen": "①通与定何关？②「知」为何是通之体？③末通以「滅」收束何义？",
    "tiyao": "本品占**卷第四十五**，剥校勘 **CJK 3,646 字**。**长行 27 段＋偈组 0（纯长行）**；结构：**总标（有十種通）→ 十段各说（句式两处变体：天耳「成就」起·第六「住無體性」起）**。",
    "xufa": "先观图 〇-1 以得其知（十通知谱），次观图 〇-2 以得其生（定通相即），次读 §2 全引，末以 §7 核量。",
    "en_map": "At 3,646 characters Samantabhadra unfolds ten superknowledges — from knowing minds to the knowledge of ceasing — each an extension of knowing that serves beings.",
    "figs": [
        {
            "n": 1,
            "title": "十通知谱",
            "what": "十通各知什么",
            "one": "他心→滅一切",
            "svg": f"""<svg viewBox="0 0 1000 300" {W} xmlns="http://www.w3.org/2000/svg" font-family="serif">
<text x="500" y="26" text-anchor="middle" font-size="14.5" font-weight="bold" fill="#7a5a28">十通即十知（§2.2 锚点切分）</text>
""" + "".join(
f"""<rect x="{40+(i%5)*188}" y="{56+(i//5)*88}" width="176" height="72" rx="8" fill="#f6efe1" stroke="#b8863c"/>
<text x="{128+(i%5)*188}" y="{80+(i//5)*88}" text-anchor="middle" font-size="10.5" font-weight="bold" fill="#7a5a28">{i+1}.{['他心','無礙清淨天眼','宿住隨念','知盡未來際劫','無礙清淨天耳','住無體性','善分別言音','出生無量色身','一切法','一切法滅盡三昧'][i]}</text>
<text x="{128+(i%5)*188}" y="{102+(i//5)*88}" text-anchor="middle" font-size="10" fill="#8a7a5e">{['知心差别','见生死了此生彼','知过去','知未来劫','闻一切声','住无体性神通','知众生言辞','现种种色身','知法无名字','入灭尽而不退'][i]}</text>"""
for i in range(10)) + f"""
<text x="500" y="284" text-anchor="middle" font-size="12" fill="#5a5147">末通以「滅」收束——知的尽头是戏论灭（与如空忍同构）</text>
</svg>""",
            "cap": "十通知谱：他心→滅一切，十种「知」的扩展。",
            "en": "Ten knowledges from mind-reading to ceasing — cognition widened into a practice.",
            "dufa": [
                "按「知」读十段：每通先问知什么。",
                "注意末通之灭：知极而戏论灭。",
                "对照两处句式变体（成就/住）。",
            ],
        },
        {
            "n": 2,
            "title": "定通相即图",
            "what": "十定生十通·末位同以否定收",
            "one": "無礙輪↔滅一切",
            "svg": f"""<svg viewBox="0 0 1000 260" {W} xmlns="http://www.w3.org/2000/svg" font-family="serif">
<text x="500" y="26" text-anchor="middle" font-size="14.5" font-weight="bold" fill="#7a5a28">定通相即（品25→品26）</text>
<rect x="60" y="56" width="360" height="150" rx="10" fill="#f6efe1" stroke="#b8863c"/>
<text x="240" y="86" text-anchor="middle" font-size="12.5" font-weight="bold" fill="#7a5a28">十定（品25）</text>
<text x="240" y="116" text-anchor="middle" font-size="11" fill="#5a5147">普光明 → …… → 無礙輪</text>
<text x="240" y="146" text-anchor="middle" font-size="10.5" fill="#8a7a5e">定＝展开（遍）</text>
<text x="240" y="180" text-anchor="middle" font-size="10.5" fill="#8a7a5e">纯长行·念请</text>
<rect x="580" y="56" width="360" height="150" rx="10" fill="none" stroke="#d4a03c" stroke-dasharray="5,3"/>
<text x="760" y="86" text-anchor="middle" font-size="12.5" font-weight="bold" fill="#7a5a28">十通（品26）</text>
<text x="760" y="116" text-anchor="middle" font-size="11" fill="#5a5147">他心知 → …… → 滅一切</text>
<text x="760" y="146" text-anchor="middle" font-size="10.5" fill="#8a7a5e">通＝遍知（知）</text>
<text x="760" y="180" text-anchor="middle" font-size="10.5" fill="#8a7a5e">纯长行·直告</text>
<text x="500" y="136" text-anchor="middle" font-size="16" fill="#7a5a28">→</text>
<text x="500" y="244" text-anchor="middle" font-size="12" fill="#5a5147">末位否定收束对照：無礙輪（定）↔ 滅一切（通）——知至极处即戏论灭〔本文判断〕</text>
</svg>""",
            "cap": "定通相即：定展开、通遍知；末位同以否定收束。",
            "en": "Samādhi expands, superknowledge knows; both series close with a negation.",
            "dufa": [
                "连读两品末位：轮与灭。",
                "中段看「以」字：通以定起。",
                "末回到伦理：知为利生。",
            ],
        },
    ],
    "weici_note": "本品承十定（品25）之安住，启十忍（品27）之印法；六十本阙〔阙本考同品25〕。",
    "weici": [
        ["十定品（品 25）", "卷四十起", "第七会·等觉", "定安住", "通之基"],
        ["十忍品（品 27）", "卷四十五起", "第七会·印法", "通了别境", "忍法承当"],
        ["藏译 Toh 44", "对应章〔核订〕", "开篇待实测", "—", "逐字对勘未竟"],
        ["六十本", "阙此品", "同品25", "阙本考", "新旧译品次异"],
        ["句式变体", "天耳「成就」起·「住無體性」起", "L.283 勘定", "锚点切分", "照实不齐一"],
    ],
    "teshe_note": "本品为第七会体量最小品之一；句式变体如实。",
    "teshe": [
        ["篇幅", "3,646 CJK／27 `<p>`＋0 `<lg>`（§7）", "品25 的 27,028", "短品"],
        ["句式", "「以X智通」×8＋变体2", "锚点切分", "标准＋变体"],
        ["末位", "滅一切智通", "品25 無礙輪", "否定收束同构"],
        ["伦理结构", "每通先能知后所益", "「令眾生」句式", "通被菩提心化"],
    ],
    "dufa5": [
        ["知谱读法", "图 〇-1 → §2.2", "结构读者", "十通十知"],
        ["相即读法", "图 〇-2 → §3", "贯通读者", "定生通"],
        ["变体读法", "§2.2 标注", "校勘读者", "两处变体"],
        ["伦理读法", "§4 要点2", "义理读者", "认知半径利生"],
        ["数据读法", "§7", "数据读者", "3,646/27p"],
    ],
    "shu": [
        ["**T0 经文明文**", "十通名目＋行相", "§2.2（`T10n0279` 全引）", "结构总量"],
        ["**T0 本文实测**", "3,646 CJK／27p", "§7", "篇幅"],
        ["**T1 注疏**", "来意窗（程序化）", "`T1735` §5.1", "「以二品明業用廣大」"],
        ["**变体层**", "两处句式变体", "L.283 勘定", "照实"],
        ["**T0·六十本实测**", "阙此品", "六十 34 品", "阙本考"],
    ],
    "shu_note": "> 【读法】本品之数以「**知**」为性：十通十知，知而知灭——读时每通问「知的半径扩到哪」。\n",
}

P27 = {
    "tag": "P27",
    "path": os.path.join(DIR7, "华严经细读_第二十七部_十忍品.md"),
    "hui": "第七会（普光明殿·等觉位）",
    "dingwei": "本品 5,705 CJK（含偈 2,140），普贤说十种忍——读法以**三体七喻**为纲：前三忍为体（音声·顺·无生法），后七忍以喻印法（幻·焰·夢·響·影·化·空），一喻比一喻更彻底，至如空忍能所俱寂。",
    "yiju": "**如幻如響如影如化——七喻连环，忍的可不是道理，是「本来如此」。**",
    "sanwen": "①「如」字为何不可省？②七喻递进的次序何义？③忍（kṣānti）与忍辱何别？",
    "tiyao": "本品占**卷第四十五～四十六**，剥校勘 **CJK 5,705 字**（偈 2,140 占 37%）。**长行 9 段＋偈组 1**；结构：**总标→十忍各说（「云何為菩薩摩訶薩X忍」问式）→结偈**。名目「如焰忍」已正（L.283）。",
    "xufa": "先观图 〇-1 以得其构（三体七喻），次观图 〇-2 以得其进（七喻阶梯），次读 §2 全引与结偈，末以 §7 核量。",
    "en_map": "Ten forbearances: three substantive (hearing, according, realizing the unborn) and seven simile-based — illusion, mirage, dream, echo, shadow, conjuring, space — each a step further in seeing phenomena as unreal.",
    "figs": [
        {
            "n": 1,
            "title": "三体七喻图",
            "what": "忍之体与喻之印",
            "one": "闻→思→证；幻→空",
            "svg": f"""<svg viewBox="0 0 1000 300" {W} xmlns="http://www.w3.org/2000/svg" font-family="serif">
<text x="500" y="26" text-anchor="middle" font-size="14.5" font-weight="bold" fill="#7a5a28">三体七喻（§2.2 实测·焰字已正）</text>
<rect x="40" y="56" width="300" height="210" rx="10" fill="#f6efe1" stroke="#b8863c"/>
<text x="190" y="84" text-anchor="middle" font-size="12.5" font-weight="bold" fill="#7a5a28">体（三忍·闻思修）</text>
<text x="190" y="120" text-anchor="middle" font-size="11.5" fill="#5a5147">① 音聲忍——闻教不怖</text>
<text x="190" y="152" text-anchor="middle" font-size="11.5" fill="#5a5147">② 順忍——随顺思惟</text>
<text x="190" y="184" text-anchor="middle" font-size="11.5" fill="#5a5147">③ 無生法忍——证无生理</text>
<text x="190" y="232" text-anchor="middle" font-size="10.5" fill="#8a7a5e">闻→思→证之序</text>
<rect x="620" y="56" width="340" height="210" rx="10" fill="none" stroke="#d4a03c" stroke-dasharray="5,3"/>
<text x="790" y="84" text-anchor="middle" font-size="12.5" font-weight="bold" fill="#7a5a28">喻（七忍·印所证境）</text>
<text x="790" y="116" text-anchor="middle" font-size="11" fill="#5a5147">④ 如幻 ⑤ 如焰 ⑥ 如夢</text>
<text x="790" y="144" text-anchor="middle" font-size="11" fill="#5a5147">⑦ 如響 ⑧ 如影 ⑨ 如化</text>
<text x="790" y="176" text-anchor="middle" font-size="11.5" font-weight="bold" fill="#a04a3a">⑩ 如空——能所俱寂</text>
<text x="790" y="232" text-anchor="middle" font-size="10.5" fill="#8a7a5e">「如」字不可省——非「是幻」乃「如幻」</text>
<text x="500" y="284" text-anchor="middle" font-size="12" fill="#5a5147">体立而后喻印：忍不是忍辱，是忍可</text>
</svg>""",
            "cap": "三体七喻：前三忍为闻思修之体，后七喻印诸法非实，至如空忍收束。",
            "en": "Three substantive forbearances followed by seven similes, sealed by space-like forbearance.",
            "dufa": [
                "先分体喻两栏。",
                "再查「如」字：每喻一句皆「如X」。",
                "末对空忍：能所俱寂收束。",
            ],
        },
        {
            "n": 2,
            "title": "七喻递进图",
            "what": "七喻为空之七级阶梯",
            "one": "幻→焰→夢→響→影→化→空",
            "svg": f"""<svg viewBox="0 0 1000 260" {W} xmlns="http://www.w3.org/2000/svg" font-family="serif">
<text x="500" y="26" text-anchor="middle" font-size="14.5" font-weight="bold" fill="#7a5a28">七喻递进（§4 阐释）</text>
""" + "".join(
f"""<rect x="{30+i*134}" y="{190-i*20}" width="126" height="{30+i*20}" rx="6" fill="#f6efe1" stroke="#b8863c"/>
<text x="{93+i*134}" y="{208-i*20}" text-anchor="middle" font-size="11" font-weight="bold" fill="#7a5a28">{['如幻','如焰','如夢','如響','如影','如化','如空'][i]}</text>
<text x="{93+i*134}" y="{224-i*20}" text-anchor="middle" font-size="9" fill="#8a7a5e">{['现而无实','误认有水','醒后成空','无实往来','随质无体','无业而作','受不受等'][i]}</text>"""
for i in range(7)) + f"""
<text x="30" y="240" font-size="10.5" fill="#5a5147">一级比一级彻底：从「现而无实」到「受与不受等」〔本文判断：七喻为空之七级阶梯〕</text>
<text x="500" y="254" text-anchor="middle" font-size="11" fill="#8a7a5e">〈金剛經〉六喻（梦幻泡影露电）与此七喻互参——彼少「響焰」而收于电</text>
</svg>""",
            "cap": "七喻阶梯：幻焰夢響影化空，递进至能所俱寂。",
            "en": "Seven similes as seven steps toward emptiness, from illusion to space.",
            "dufa": [
                "沿阶梯读：每喻问「破了什么执」。",
                "对照金刚六喻：喻组可互训。",
                "末住空忍：受与不受等。",
            ],
        },
    ],
    "weici_note": "本品承十通（品26）之了别，启阿僧祇（品30）之入量；六十本阙〔阙本考同品25〕。",
    "weici": [
        ["十通品（品 26）", "卷四十五", "第七会·果用", "通了别", "忍之承当"],
        ["阿僧祇品（品 30）", "卷四十四末起", "第七会·数法", "由理入量", "忍后问数"],
        ["藏译 Toh 44", "对应章〔核订〕", "开篇待实测", "—", "逐字对勘未竟"],
        ["六十本", "阙此品", "同品25", "阙本考", "新旧译品次异"],
        ["名目勘定", "「如焰忍」（L.283）", "旧记「如燄忍」", "照经正名", "焰燄之辨"],
    ],
    "teshe_note": "本品以偈颂占比与喻组为特征。",
    "teshe": [
        ["篇幅", "5,705 CJK／9 `<p>`＋1 `<lg>`（偈 2,140·37%）", "品26 的 3,646", "偈比最高"],
        ["喻组", "七喻连排", "〈金剛經〉六喻", "喻组对照"],
        ["名目勘定", "焰（非燄）", "L.283", "照经正名"],
        ["收束", "如空忍·能所俱寂", "品26 滅一切", "否定收束同构"],
    ],
    "dufa5": [
        ["构架读法", "图 〇-1 → §2.2", "结构读者", "三体七喻"],
        ["阶梯读法", "图 〇-2 → §4", "义理读者", "七级递进"],
        ["字眼读法", "「如」字逐句", "精读读者", "不坏现象破实执"],
        ["对勘读法", "§6.3＋阙本考", "版本学读者", "六十阙"],
        ["数据读法", "§7", "数据读者", "偈占 37%"],
    ],
    "shu": [
        ["**T0 经文明文**", "十忍名目＋七喻", "§2.2（`T10n0279` 全引）", "结构总量"],
        ["**T0 本文实测**", "5,705 CJK／偈 2,140", "§7", "篇幅"],
        ["**T1 注疏**", "来意窗（程序化）", "`T1735` §5.1", "「智慧深奧故次來」"],
        ["**名目层**", "焰字勘定", "L.283", "照经正名"],
        ["**T0·六十本实测**", "阙此品", "六十 34 品", "阙本考"],
    ],
    "shu_note": "> 【读法】本品之数以「**喻**」为性：三体七喻，一喻一撤——读时沿阶梯逐级放下「实」字。\n",
}

ALL_EXT = [P23, P24, P25, P26, P27]

if __name__ == "__main__":
    want = set(sys.argv[1:])
    for d in ALL_EXT:
        if want and d["tag"] not in want:
            continue
        base.apply(d)
