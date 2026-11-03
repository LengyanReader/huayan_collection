# -*- coding: utf-8 -*-
"""〇之二内容地图层·扩展 P33–P37（依赖 p7_p18_atlas.apply）"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p7_p18_atlas as base

DIR7 = os.path.join('docs', '经学文献', '华严经细读', '第七会_普光明殿_等觉')
DIR8 = os.path.join('docs', '经学文献', '华严经细读', '第八会_普光明殿_离世间')
DIR9 = os.path.join('docs', '经学文献', '华严经细读', '第九会_逝多林_证入法界')
W = 'width="100%" style="max-width:1000px;height:auto"'

P33 = {
    "tag": "P33",
    "path": os.path.join(DIR7, "华严经细读_第三十三部_随好光明品.md"),
    "hui": "第七会（普光明殿·等觉位）",
    "dingwei": "本品 2,777 CJK，世尊亲说随好「圓滿王」——追述菩萨时兜率放光（光幢王）照破阿鼻、天鼓无说而说无生法——读法以**劣德顿益**为纲：好虽劣于相，其用顿益（澄观）；一好之光即一场完整教化。",
    "yiju": "**一随好之光，照破阿鼻；一天鼓之音，说尽无生——好虽劣于相，其用顿益。**",
    "sanwen": "①光如何是救度？②天鼓无作者何以有说法？③结归金網转轮王三昧何义？",
    "tiyao": "本品占**卷第四十九**，剥校勘 **CJK 2,777 字**。**长行 18 段＋偈组 0**；结构：**品首（世尊告寶手）→ 隨好圓滿王总标 → 兜率放光·地狱离苦 → 足下千辐轮·天鼓说无生（主段）→ 转轮王位 → 月智如来喻 → 初禅喻·摩尼髻光 → 微尘量喻结归**（八段全引）。",
    "xufa": "先观图 〇-1 以得其序（光之行程），次观图 〇-2 以得其眼（无说而说），次读 §2 全引，末以 §7 核量。",
    "en_map": "The secondary mark Perfect King recalls the bodhisattva-era light that freed hell-beings; the speakerless heaven-drum taught the deathless — the lesser adornment works sudden great benefit.",
    "figs": [
        {
            "n": 1,
            "title": "光之行程图",
            "what": "一好之光的一场教化",
            "one": "兜率放光→地狱离苦→生天→天鼓说法→得无生忍",
            "svg": f"""<svg viewBox="0 0 1000 200" {W} xmlns="http://www.w3.org/2000/svg" font-family="serif">
<text x="500" y="26" text-anchor="middle" font-size="14.5" font-weight="bold" fill="#7a5a28">光之行程（§2.1 八段全引）</text>
""" + "".join(
f"""<circle cx="{90+i*130}" cy="96" r="40" fill="#f6efe1" stroke="#b8863c"/>
<text x="{90+i*130}" y="{92}" text-anchor="middle" font-size="9" font-weight="bold" fill="#7a5a28">{['圓滿王','光幢王','照破阿鼻','命終生天','天鼓勸誨','說無生法','得無生忍','金網三昧'][i]}</text>
<text x="{90+i*130}" y="{110}" text-anchor="middle" font-size="8" fill="#8a7a5e">{['總標','菩薩時','光到','離苦','夜神? 鼓音','無生','果熟','結歸'][i]}</text>"""
for i in range(8)) + "".join(
f"""<line x1="{132+i*130}" y1="96" x2="{168+i*130}" y2="96" stroke="#b8863c" stroke-width="1.5" marker-end="url(#a)"/>"""
for i in range(7)) + f"""
<text x="500" y="176" text-anchor="middle" font-size="11.5" fill="#5a5147">一随好＝一教化的完整镜头（§4 阐释：果海不碍叙事，一好即一世界）</text>
</svg>""",
            "cap": "光之行程：随好圆满王的一场教化（八段）。",
            "en": "The journey of one secondary mark's light: a complete teaching event.",
            "dufa": [
                "沿镜头读：光即叙事。",
                "对照品31枚举：彼量此镜。",
                "末回金網：果用归因行。",
            ],
        },
        {
            "n": 2,
            "title": "无说而说图",
            "what": "天鼓之音的认识论",
            "one": "无作者·无去处·音自成就",
            "svg": f"""<svg viewBox="0 0 1000 200" {W} xmlns="http://www.w3.org/2000/svg" font-family="serif">
<text x="500" y="26" text-anchor="middle" font-size="14.5" font-weight="bold" fill="#7a5a28">天鼓无说而说（§2.1 段三、四全引）</text>
<rect x="90" y="60" width="240" height="100" rx="10" fill="#f6efe1" stroke="#b8863c"/>
<text x="210" y="94" text-anchor="middle" font-size="11.5" font-weight="bold" fill="#7a5a28">天子问</text>
<text x="210" y="122" text-anchor="middle" font-size="10.5" fill="#5a5147">「何因發此微妙之音？」</text>
<rect x="380" y="60" width="240" height="100" rx="10" fill="none" stroke="#d4a03c" stroke-dasharray="5,3"/>
<text x="500" y="94" text-anchor="middle" font-size="11.5" font-weight="bold" fill="#7a5a28">天鼓自陈</text>
<text x="500" y="122" text-anchor="middle" font-size="10.5" fill="#5a5147">无作者·无去处</text>
<text x="500" y="140" text-anchor="middle" font-size="10.5" fill="#5a5147">而法音自成</text>
<rect x="670" y="60" width="240" height="100" rx="10" fill="none" stroke="#d4a03c" stroke-dasharray="5,3"/>
<text x="790" y="94" text-anchor="middle" font-size="11.5" font-weight="bold" fill="#7a5a28">义</text>
<text x="790" y="122" text-anchor="middle" font-size="10.5" fill="#5a5147">「说法者无法可说」</text>
<text x="790" y="140" text-anchor="middle" font-size="10.5" fill="#5a5147">无生之法唯无说能说</text>
<text x="500" y="186" text-anchor="middle" font-size="11.5" fill="#5a5147">〔本文判断：天鼓即「音声不思议」之具象〕——把「我有所说」之执从弘法中拆掉</text>
</svg>""",
            "cap": "无说而说：天鼓问答（§2.1）。",
            "en": "The speakerless drum: teaching without a teacher.",
            "dufa": [
                "问答读法：问在因，答在无。",
                "对照品35音声喻：龙王雨与天鼓。",
                "日用落地：弘法先拆我执。",
            ],
        },
    ],
    "weici_note": "本品承十身相海（品32）之相，辨好——「好依相有，德劣於相」；启普贤行（品34）之因行。",
    "weici": [
        ["十身相海品（品 32）", "卷四十八起", "第七会·相", "前品明相", "此品辨好"],
        ["普賢行品（品 34）", "卷四十九起", "第七会·因行", "果用归因行", "末句回指三昧福德"],
        ["藏译 Toh 44", "对应章〔核订〕", "开篇待实测", "—", "逐字对勘未竟"],
        ["澄观来意窗", "「劣德之用用成頓益」", "`T1735` §5.1", "程序化实引", "翻顯大相德難思"],
        ["天鼓段", "无作者而音成", "§2.1 段三四", "音声不思议具象", "与品37音声喻互查〔待批〕"],
    ],
    "teshe_note": "本品以叙事性与「劣德顿益」为特征。",
    "teshe": [
        ["篇幅", "2,777 CJK／18 `<p>`（§7）", "品32 的 6,152", "短品"],
        ["叙事", "一场完整教化镜头", "品31 枚举", "镜头对枚举"],
        ["说主", "世尊亲说（告寶手）", "品32 普贤说", "果分中罕见"],
        ["结构", "八段全引", "—", "§2.1"],
    ],
    "dufa5": [
        ["镜头读法", "图 〇-1 → §2.1", "叙事读者", "一好一世界"],
        ["无说说读法", "图 〇-2 → §2.1", "义理读者", "拆我执"],
        ["劣益读法", "§4 要点+澄观", "义理读者", "劣德顿益"],
        ["对照读法", "§4 对照", "比较读者", "法华化城异趣"],
        ["数据读法", "§7", "数据读者", "八段"],
    ],
    "shu": [
        ["**T0 经文明文**", "八段全引", "§2（`T10n0279` 全引）", "结构总量"],
        ["**T0 本文实测**", "2,777 CJK／18p", "§7", "篇幅"],
        ["**T1 注疏**", "来意窗（程序化）", "`T1735` §5.1", "劣德之用用成顿益"],
        ["**T0·六十本实测**", "对应章〔待核〕", "`T09n0278`", "对读未竟"],
        ["**T0·藏本实测**", "〔核订〕", "L.201 TOC", "对勘未竟"],
    ],
    "shu_note": "> 【读法】本品之数以「**镜**」为性：一枚随好放大为一个世界——读时跟镜头，不数功德。\n",
}

P34 = {
    "tag": "P34",
    "path": os.path.join(DIR7, "华严经细读_第三十四部_普贤行品.md"),
    "hui": "第七会（普光明殿·等觉位）",
    "dingwei": "本品 4,685 CJK，普贤复告——先立全品之纲「我不見一法為大過失，如諸菩薩於他菩薩起瞋心者」（瞋心成百万障门·86 种实测），继以五阶十法递进链（清淨→廣大智→普入→勝妙心→善巧智）与受持劝，终以 2,420 字长偈自誓——读法以**行有次第，故因果平等**为纲。",
    "yiju": "**我不見一法為大過失，如諸菩薩於他菩薩起瞋心者。**",
    "sanwen": "①行品何不说行先说止（瞋）？②五阶连锁的语法何义？③偈颂自誓与重颂何别？",
    "tiyao": "本品占**卷第四十九～五十**，剥校勘 **CJK 4,685 字**（长行 2,265＋偈 2,420·占 51%）。**长行 25 段＋偈组 1**；结构：**品首（百万障门 86 种）→ 五阶十法递进链 → 受持劝 → 长偈**。",
    "xufa": "先观图 〇-1 以得其障（百万障门），次观图 〇-2 以得其阶（五阶连锁），次读 §2 全引与偈，末以 §7 核量。",
    "en_map": "Anger toward fellow bodhisattvas is the single greatest fault — one wrath opening a million obstacles (86 catalogued) — then a five-rung ladder from purity to skillful wisdom, sealed by a self-dedicating verse.",
    "figs": [
        {
            "n": 1,
            "title": "百万障门图",
            "what": "一瞋开百万门",
            "one": "不見菩提障→離三世諸佛菩薩種性障",
            "svg": f"""<svg viewBox="0 0 1000 220" {W} xmlns="http://www.w3.org/2000/svg" font-family="serif">
<text x="500" y="26" text-anchor="middle" font-size="14.5" font-weight="bold" fill="#7a5a28">百万障门（§2.1 实测 86 种）</text>
<rect x="120" y="52" width="760" height="52" rx="8" fill="#f6efe1" stroke="#a04a3a"/>
<text x="500" y="76" text-anchor="middle" font-size="12" font-weight="bold" fill="#a04a3a">一念瞋起 → 百万门开</text>
<text x="500" y="94" text-anchor="middle" font-size="10" fill="#8a7a5e">「我不見一法為大過失，如諸菩薩於他菩薩起瞋心者」</text>
""" + "".join(
f"""<text x="{60+(i%6)*156}" y="{140+(i//6)*30}" font-size="10" fill="#5a5147">{['不見菩提障','不聞正法','生不淨世界','生諸惡趣','生諸難處','多諸疾病','不見佛障','不聞法障','謗法障','謗善知識障','退菩提心障','遠離種性障'][i]}{'…' if i == 11 else ''}</text>"""
for i in range(12)) + f"""
<text x="500" y="200" text-anchor="middle" font-size="11.5" fill="#5a5147">86 种障名实测（首：不見菩提障；末：遠離三世諸佛菩薩種性障）——「百万」举其大数</text>
</svg>""",
            "cap": "百万障门：86 种障名实测（§2.1）。",
            "en": "Eighty-six obstacles catalogued from one wrath.",
            "dufa": [
                "读首末两障：障之极处是种性远离。",
                "自照：一瞋验心。",
                "对照品25念请：一念可请亦可障。",
            ],
        },
        {
            "n": 2,
            "title": "五阶连锁图",
            "what": "条件递进的行法语法",
            "one": "清淨→智→普入→勝妙心→善巧智",
            "svg": f"""<svg viewBox="0 0 1000 240" {W} xmlns="http://www.w3.org/2000/svg" font-family="serif">
<text x="500" y="26" text-anchor="middle" font-size="14.5" font-weight="bold" fill="#7a5a28">五阶十法递进链（§2.2 六段全引）</text>
""" + "".join(
f"""<rect x="{30+i*190}" y="70" width="170" height="70" rx="10" fill="#f6efe1" stroke="#b8863c"/>
<text x="{115+i*190}" y="98" text-anchor="middle" font-size="10.5" font-weight="bold" fill="#7a5a28">{['①十種清淨','②十種廣大智','③十種普入','④十種勝妙心','⑤十種佛法善巧智'][i]}</text>
<text x="{115+i*190}" y="120" text-anchor="middle" font-size="8.5" fill="#8a7a5e">{['通达甚深法…','知眾生心行…','世界入一毛道…','住语言非语言…','了達甚深佛…'][i]}</text>"""
for i in range(5)) + "".join(
f"""<text x="{200+i*190}" y="110" text-anchor="middle" font-size="14" fill="#7a5a28">→</text>"""
for i in range(4)) + f"""
<text x="500" y="176" text-anchor="middle" font-size="11.5" fill="#5a5147">连锁语法：「安住此十法已則能具足」「住此十智已則得入」——后阶以前阶为基（非科目清单）</text>
<rect x="250" y="196" width="500" height="34" rx="8" fill="none" stroke="#d4a03c" stroke-dasharray="5,3"/>
<text x="500" y="218" text-anchor="middle" font-size="11" fill="#5a5147">行有次第，故因果平等（澄观：會前差別因成此普賢之圓因）</text>
</svg>""",
            "cap": "五阶连锁：清净→智→普入→胜妙心→善巧智（§2.2）。",
            "en": "A five-rung conditional ladder of tenfold sets.",
            "dufa": [
                "沿链读：后阶以前阶为门。",
                "自测：清净未成而求普入是躐等。",
                "末对平等因果：行满即佛。",
            ],
        },
    ],
    "weici_note": "本品与如來出現（品35）共明「出現因果·平等因果」——前品称果之因，此品如因之果；启品35性起果德。",
    "weici": [
        ["隨好光明品（品 33）", "卷四十九", "第七会·随好", "果用归因行", "本品承之自说行"],
        ["如來出現品（品 35）", "卷五十起", "第七会·性起", "普贤圆因→性起果", "平等因果一双"],
        ["藏译 Toh 44", "对应章〔核订〕", "开篇待实测", "—", "逐字对勘未竟"],
        ["澄观来意窗", "「亦名平等因果」", "`T1735` §5.1", "程序化实引", "會前差別因果"],
        ["六十本", "对应品待勘〔待核〕", "晋译", "—", "对读未竟"],
    ],
    "teshe_note": "本品以瞋障论与五阶链为特征。",
    "teshe": [
        ["篇幅", "4,685 CJK／25 `<p>`＋1 `<lg>`（偈 2,420·51%）", "品33 的 2,777", "偈占过半"],
        ["障门", "86 种实测", "「百万」举大数", "瞋为第一过"],
        ["链结构", "五阶条件连锁", "品31 34节并列式", "递进对并列"],
        ["偈性质", "自誓（如彼所修行我當次第說）", "他品重颂", "自誓非复述"],
    ],
    "dufa5": [
        ["障门读法", "图 〇-1 → §2.1", "实修读者", "一瞋百万障"],
        ["阶梯读法", "图 〇-2 → §2.2", "结构读者", "条件连锁"],
        ["平等读法", "§4 阐释＋§5.1", "义理读者", "行满即佛"],
        ["偈读法", "§2.3", "文学读者", "自誓文体"],
        ["数据读法", "§7", "数据读者", "86障/51%"],
    ],
    "shu": [
        ["**T0 经文明文**", "百万障＋五阶链＋长偈", "§2（`T10n0279` 全引）", "结构总量"],
        ["**T0 本文实测**", "4,685 CJK／86障", "§7", "篇幅"],
        ["**T1 注疏**", "平等因果窗（程序化）", "`T1735` §5.1", "先通后别"],
        ["**勘正层**", "第六段如实标「聞法受持勸」", "L.271", "非独立十种"],
        ["**T0·六十本实测**", "待勘〔待核〕", "`T09n0278`", "对读未竟"],
    ],
    "shu_note": "> 【读法】本品之数以「**阶**」为性：一瞋之下、五阶之上——读时先自照瞋，再上阶。\n",
}

P35 = {
    "tag": "P35",
    "path": os.path.join(DIR7, "华严经细读_第三十五部_如来出现品.md"),
    "hui": "第七会（普光明殿·等觉位）",
    "dingwei": "本品 23,117 CJK 跨三卷（卷50–52），白毫光名「如來出現」入性起妙德菩萨顶，普贤承问以**四十余喻**说如来出现——读法以**出现＝性起**为纲：非以一缘一事成就，而以身十相·音声十相·心十相（三十喻）＋世界成喻组＋结劝七喻展开；大经卷喻（一尘一卷）为全经义理之眼。",
    "yiju": "**如来出现非以一缘一事——身口意三十喻展开性起之海；一微尘中经卷具在，破尘即出。**",
    "sanwen": "①出现与性起何关？②三十喻何以按身口意三分？③大经卷喻的「破尘者」是谁？",
    "tiyao": "本品占**卷第五十～五十二**，剥校勘 **CJK 23,117 字**。**长行 139 段＋偈组 13**；结构：**序分（白毫光入性起顶）→ 出现总标（十无量事）→ 世界成喻组 → 世界喻偈 → 身十相 → 音声十相 → 音声十无量 → 心十相（大经卷）→ 性起境界·文字无尽 → 结劝七喻**（九段全引）。",
    "xufa": "先观图 〇-1 以得其流（白毫→性起→九段），次观图 〇-2 以得其眼（大经卷喻），次读 §2 九段全引，末以 §7 核量。",
    "en_map": "A white-hair curl beams the light Manifestation into Nature-Arising Marvel-Virtue; Samantabhadra unfolds forty-odd parables of the Buddhas' manifestation, crowning in the Great Scroll parable: a trichiliocosm-sized scroll wholly within one dust-mote.",
    "figs": [
        {
            "n": 1,
            "title": "九段主题流图",
            "what": "白毫→性起→结劝",
            "one": "序分→三十相→文字无尽→结劝",
            "svg": f"""<svg viewBox="0 0 1000 220" {W} xmlns="http://www.w3.org/2000/svg" font-family="serif">
<text x="500" y="26" text-anchor="middle" font-size="14.5" font-weight="bold" fill="#7a5a28">九段主题流（§2 全引·L.272 实测）</text>
""" + "".join(
f"""<rect x="{24+i*118}" y="60" width="110" height="64" rx="8" fill="#f6efe1" stroke="#b8863c"/>
<text x="{79+i*118}" y="{86}" text-anchor="middle" font-size="9" font-weight="bold" fill="#7a5a28">{['①序分','②总标','③世界喻','④世界偈','⑤身十相','⑥音十相','⑦音无量','⑧心十相','⑨结劝'][i]}</text>
<text x="{79+i*118}" y="{104}" text-anchor="middle" font-size="7.5" fill="#8a7a5e">{['白毫入顶','十无量事','风轮大云','长偈','是為身第N','音聲第N','十種無量','大经卷','七喻'][i]}</text>"""
for i in range(9)) + "".join(
f"""<text x="{79+i*118+55}" y="98" text-anchor="middle" font-size="10" fill="#b8863c">→</text>"""
for i in range(8)) + f"""
<text x="500" y="164" text-anchor="middle" font-size="11.5" fill="#5a5147">白毫光名「如來出現」→ 入**性起妙德**菩萨顶——光名·品题·菩萨名三重互文</text>
<text x="500" y="192" text-anchor="middle" font-size="11.5" fill="#5a5147">身取天象（日月虚空）·音声取水声（龙王众水）·心取宝藏（海珠大经卷）〔本文判断〕</text>
<text x="500" y="212" text-anchor="middle" font-size="11" fill="#8a7a5e">实测：是為如來身第×10／音聲第×10／心第×10</text>
</svg>""",
            "cap": "九段主题流（§2 全引·30叠实测）。",
            "en": "Nine thematic movements from white-hair light to the closing charge.",
            "dufa": [
                "沿流读：先序后喻再收。",
                "三分读法：身音心各十相。",
                "句眼读法：一念一尘。",
            ],
        },
        {
            "n": 2,
            "title": "大经卷喻图",
            "what": "一尘一卷·破尘出经",
            "one": "量等三千大千世界，全住一微塵中",
            "svg": f"""<svg viewBox="0 0 1000 220" {W} xmlns="http://www.w3.org/2000/svg" font-family="serif">
<text x="500" y="26" text-anchor="middle" font-size="14.5" font-weight="bold" fill="#7a5a28">大经卷喻（§2.7 程序全引）</text>
<circle cx="220" cy="110" r="46" fill="#f6efe1" stroke="#b8863c" stroke-width="2"/>
<text x="220" y="106" text-anchor="middle" font-size="10" fill="#7a5a28">一微塵</text>
<text x="220" y="124" text-anchor="middle" font-size="8.5" fill="#8a7a5e">全住經卷</text>
<rect x="360" y="70" width="240" height="80" rx="8" fill="none" stroke="#d4a03c" stroke-dasharray="5,3"/>
<text x="480" y="100" text-anchor="middle" font-size="11" font-weight="bold" fill="#7a5a28">大經卷</text>
<text x="480" y="124" text-anchor="middle" font-size="10.5" fill="#5a5147">量等三千大千世界</text>
<text x="480" y="142" text-anchor="middle" font-size="9.5" fill="#8a7a5e">書寫一切世界中事</text>
<text x="640" y="114" text-anchor="middle" font-size="13" fill="#7a5a28">←破→</text>
<rect x="720" y="70" width="240" height="80" rx="8" fill="#f6efe1" stroke="#b8863c"/>
<text x="840" y="100" text-anchor="middle" font-size="11" font-weight="bold" fill="#7a5a28">一人智慧明達</text>
<text x="840" y="124" text-anchor="middle" font-size="10.5" fill="#5a5147">「我當以精進力</text>
<text x="840" y="142" text-anchor="middle" font-size="10.5" fill="#5a5147">破彼微塵，出此經卷」</text>
<text x="500" y="196" text-anchor="middle" font-size="12" fill="#5a5147">众生身中佛智具在——佛之出世即破尘出卷之人（§4）</text>
</svg>""",
            "cap": "大经卷喻：一尘一卷，卷卷等大千（§2.7）。",
            "en": "The Great Scroll parable: a cosmos-sized scroll within one mote.",
            "dufa": [
                "喻读法：尘·卷·破尘人三角色。",
                "日用读法：破一分尘出一分卷。",
                "对照品39参学：善财即破尘人。",
            ],
        },
    ],
    "weici_note": "本品与普贤行（品34）共明平等因果——「前品明稱果之因，此品辨如因之果」；启離世間（品36）二千行门。",
    "weici": [
        ["普賢行品（品 34）", "卷四十九起", "第七会·圆因", "平等因", "本品性起果"],
        ["離世間品（品 36）", "卷五十三起", "第八会·行海", "果为行体", "二千行门"],
        ["六十〈性起品〉", "新旧译标志性异题", "「性起」/「出現」", "同一梵义两译〔本文判断〕", "逐段对勘未竟"],
        ["藏译 Toh 44", "对应章〔核订〕", "开篇待实测", "—", "逐字对勘未竟"],
        ["澄观来意窗", "「前品明稱果之因此品辨如因之果」", "`T1735` §5.1", "程序化实引", "平等因果一双"],
    ],
    "teshe_note": "本品以喻之密度与义理总汇为特征。",
    "teshe": [
        ["篇幅", "23,117 CJK／139 `<p>`＋13 `<lg>`（§7）", "品34 的 4,685", "跨三卷"],
        ["喻数", "40 余喻（30相＋世界组＋结劝）", "品32 97相", "以喻证体"],
        ["三分", "身/音声/心 各十相", "30叠实测", "业用三分"],
        ["大经卷", "一尘一卷·破尘出经", "全经义理之眼", "§2.7 全引"],
    ],
    "dufa5": [
        ["流读法", "图 〇-1 → §2", "结构读者", "九段主题流"],
        ["喻读法", "图 〇-2 → §2.7", "义理读者", "一尘一卷"],
        ["句眼读法", "§4 一念一尘", "精读读者", "小大相入公式"],
        ["对读法", "§6.1 性起品", "版本学读者", "新旧译异题"],
        ["数据读法", "§7", "数据读者", "30叠"],
    ],
    "shu": [
        ["**T0 经文明文**", "九段全引", "§2（`T10n0279` 全引）", "结构总量"],
        ["**T0 本文实测**", "23,117 CJK／30叠", "§7", "篇幅"],
        ["**T1 注疏**", "来意窗（程序化）", "`T1735` §5.1", "如理常現名為出現"],
        ["**勘正层**", "九段切分（段界按喻组）", "L.272", "首尾相接覆盖全品"],
        ["**T0·六十本实测**", "〈性起品〉", "`T09n0278`", "对勘未竟"],
    ],
    "shu_note": "> 【读法】本品之数以「**喻**」为性：四十余喻皆「如」——读时每遇「如」字即性起之注脚。\n",
}

P36 = {
    "tag": "P36",
    "path": os.path.join(DIR8, "华严经细读_第三十六部_离世间品.md"),
    "hui": "第八会（普光明殿·二千行门）",
    "dingwei": "本品 54,872 CJK 跨七卷（卷53–59），普慧云兴二百问、普贤瓶泻二千酬（200组×10＝2,000行门实测）——读法以**工具书**为纲：每条「条件—行相—成效」三段式；如来赞「出世間法門品」正名：离世间者，离世间之执非离世间之境。",
    "yiju": "**普慧云兴二百问，普贤瓶泻二千酬——行门如瓶泻，离世间不离世间而离。**",
    "sanwen": "①二百问如何读？②二千行门如何检索？③「离世间」离的是什么？",
    "tiyao": "本品占**卷第五十三～五十九**，剥校勘 **CJK 54,872 字**。**长行 331 段＋偈组 1（结偈 5,238 字）**；结构：**序分（莲华藏师子座）→ 普贤入佛华庄严三昧 → 普慧二百问 → 200组十答 → 如来赞（品名句）→ 结偈**。",
    "xufa": "先观图 〇-1 以得其问（200问与200组），次观图 〇-2 以得其式（行门三段式），次用 §2.4 总表检索（52卡全引），次读 §4 义理，末以 §7 核量。",
    "en_map": "Puzhi asks two hundred questions; Samantabhadra answers each with ten — two thousand gates of practice — sealed as the gateway of world-transcending dharma and a closing verse urging the diamond mind.",
    "figs": [
        {
            "n": 1,
            "title": "二百问二千酬图",
            "what": "问酬结构",
            "one": "一问酬十·二问答千",
            "svg": f"""<svg viewBox="0 0 1000 220" {W} xmlns="http://www.w3.org/2000/svg" font-family="serif">
<text x="500" y="26" text-anchor="middle" font-size="14.5" font-weight="bold" fill="#7a5a28">普慧云兴二百问·普贤瓶泻二千酬（§2.3-2.4 实测）</text>
<rect x="80" y="56" width="260" height="120" rx="10" fill="#f6efe1" stroke="#b8863c"/>
<text x="210" y="88" text-anchor="middle" font-size="12" font-weight="bold" fill="#7a5a28">普慧菩薩</text>
<text x="210" y="116" text-anchor="middle" font-size="11" fill="#5a5147">二百问（200 问句实测）</text>
<text x="210" y="140" text-anchor="middle" font-size="10" fill="#8a7a5e">「何等為X？云何X？何故X？」杂发</text>
<rect x="660" y="56" width="260" height="120" rx="10" fill="none" stroke="#d4a03c" stroke-dasharray="5,3"/>
<text x="790" y="88" text-anchor="middle" font-size="12" font-weight="bold" fill="#7a5a28">普賢菩薩</text>
<text x="790" y="116" text-anchor="middle" font-size="11" fill="#5a5147">200 组 × 10 ＝ 2,000 行门</text>
<text x="790" y="140" text-anchor="middle" font-size="10" fill="#8a7a5e">「何等為十？……是為十」三十四叠式</text>
<text x="500" y="120" text-anchor="middle" font-size="15" fill="#7a5a28">⇒</text>
<text x="500" y="204" text-anchor="middle" font-size="12" fill="#5a5147">问可以散，行必有则——如来赞「功德行處．決定義華．普入一切佛法．出世間法門品」</text>
</svg>""",
            "cap": "问酬结构：200问→200组二千行门（§2.3-2.4）。",
            "en": "Two hundred questions, two thousand answers.",
            "dufa": [
                "问式读法：杂陈之问。",
                "组式读法：十数成组。",
                "赞语读法：品名自证。",
            ],
        },
        {
            "n": 2,
            "title": "行门三段式图",
            "what": "条件—行相—成效",
            "one": "安住此法，則得／則能",
            "svg": f"""<svg viewBox="0 0 1000 200" {W} xmlns="http://www.w3.org/2000/svg" font-family="serif">
<text x="500" y="26" text-anchor="middle" font-size="14.5" font-weight="bold" fill="#7a5a28">行门三段式（§2.4 二千条同构）</text>
""" + "".join(
f"""<rect x="{60+i*300}" y="60" width="270" height="86" rx="10" fill="#f6efe1" stroke="#b8863c"/>
<text x="{195+i*300}" y="88" text-anchor="middle" font-size="11.5" font-weight="bold" fill="#7a5a28">{['条件','行相','成效'][i]}</text>
<text x="{195+i*300}" y="{112+i*2}" text-anchor="middle" font-size="10" fill="#5a5147">{['安住此十法','所谓：…（十项行相）','則能／則得…'][i]}</text>
<text x="{195+i*300}" y="{132}" text-anchor="middle" font-size="9" fill="#8a7a5e">{['以何为基','行何','得何'][i]}</text>"""
for i in range(3)) + "".join(
f"""<text x="{334+i*300}" y="106" text-anchor="middle" font-size="13" fill="#7a5a28">→</text>"""
for i in range(2)) + f"""
<text x="500" y="184" text-anchor="middle" font-size="12" fill="#5a5147">检索读法：以 §2.4 名目总表为索引，取与自己功课相应之一组十门为日课（§4 工具书读法）</text>
</svg>""",
            "cap": "行门三段式：条件—行相—成效（二千条同构）。",
            "en": "Every gate in three movements: basis, practice, effect.",
            "dufa": [
                "三段读法：任取一组。",
                "检索读法：总表为索引。",
                "落地读法：一组十门为日课。",
            ],
        },
    ],
    "weici_note": "本品居第八会正宗：承如來出現（品35）之果，启入法界（品37）之参学——果为行体，行为果用；六十四开二门之读。",
    "weici": [
        ["如來出現品（品 35）", "卷五十起", "第七会·性起果", "果德圆满", "果后起行"],
        ["入法界品（品 37）", "四十华严全卷", "第九会·参学", "二千门之肉身化", "善财一人走过"],
        ["藏译 Toh 44", "对应章〔核订〕", "开篇待实测", "—", "逐字对勘未竟"],
        ["六十本", "〈離世間品〉同题", "晋译", "对读未竟", "逐组勘〔待批〕"],
        ["如来赞", "品名句（§2.5）", "「出世間法門品」", "离执非离境", "题解之钥"],
    ],
    "teshe_note": "本品以体量与工具性为特征。",
    "teshe": [
        ["篇幅", "54,872 CJK／331 `<p>`＋1 `<lg>`（结偈 5,238）（§7）", "品35 的 23,117", "跨七卷"],
        ["问酬", "200问／200组×10＝2,000", "品31 34节", "行法辞典"],
        ["体例", "条件—行相—成效", "同构二千条", "工具书读法"],
        ["示现段", "「以十事故示現八相」", "八相成道重述", "调伏之示范"],
    ],
    "dufa5": [
        ["问酬读法", "图 〇-1 → §2.3", "结构读者", "一问酬十"],
        ["工具读法", "图 〇-2 → §2.4", "实修读者", "一组为日课"],
        ["题解读法", "§2.5 品名句", "义理读者", "离执非离境"],
        ["示现读法", "§4 要点3", "贯通读者", "八相之问"],
        ["数据读法", "§7", "数据读者", "2,000门"],
    ],
    "shu": [
        ["**T0 经文明文**", "二百问＋200组全引＋赞＋结偈", "§2（`T10n0279` 全引）", "结构总量"],
        ["**T0 本文实测**", "54,872 CJK／2,000门", "§7", "篇幅"],
        ["**勘正层**", "实测54,872（L.262 规划 230,109 系raw字符误计）", "L.274", "M0.4 实例"],
        ["**T0·六十本实测**", "同题对应", "`T09n0278`", "对读未竟"],
        ["**T0·藏本实测**", "〔核订〕", "L.201 TOC", "对勘未竟"],
    ],
    "shu_note": "> 【读法】本品之数以「**门**」为性：二千门同构——读时以检索代通读，一组十门持之终身。\n",
}

P37 = {
    "tag": "P37",
    "path": os.path.join(DIR9, "华严经细读_第三十七部_入法界品.md"),
    "hui": "第九会（逝多林·证入法界）",
    "dingwei": "主体转移四十华严 T0293（261,526 CJK 全卷即一品），四源对读（八十174,902／六十145,080／藏Toh44-45）——读法以**巡礼**为纲：善财五十三参，每参一个法门的肉身化；「入法界」之眼在「入」：以行入，以人入（§5 会读总纲）。",
    "yiju": "**一步一善知识，一参一解脱门——行到极处，法界自身来接引。**",
    "sanwen": "①善知识无定相如何读？②每参一套语式何义？③四十华严的独立价值何在？",
    "tiyao": "T0293 全文 **261,526 CJK**；**序品 21,729 CJK 全引＋52参卡全引**（237,214 CJK·L.289-L.304）；**法门名可标 40/52**；身份 23 类（在家众远多于出家众〔本文判断：道在俗世〕）；特殊参八处（两疑/险门/转介/字母/楼阁/遥指/愿王）。",
    "xufa": "先观图 〇-1 以得其历（五十三参行程），次观图 〇-2 以得其法（参学语式），次巡礼 §参批1-16（逐参分章阐释），次以 §7 数据科学附表核其量，末以页签〈五十三参行历〉（tabs/rufajie.html）互动回看。",
    "en_map": "Sudhana, sent forth by Manjushri, makes fifty-three visits — each teacher a living gateway — closing with Samantabhadra's ten king-vows. Four textual witnesses anchor every reading; the base text is the forty-fascicle Gandavyuha.",
    "figs": [
        {
            "n": 1,
            "title": "五十三参行程图",
            "what": "52卡蛇形行程（数据版见页签）",
            "one": "文殊指授→……→彌勒楼阁→遥指→普贤",
            "svg": f"""<svg viewBox="0 0 1000 240" {W} xmlns="http://www.w3.org/2000/svg" font-family="serif">
<text x="500" y="26" text-anchor="middle" font-size="14.5" font-weight="bold" fill="#7a5a28">五十三参行程（§参批1-16·L.289-L.304）</text>
<rect x="40" y="60" width="180" height="60" rx="10" fill="#f6efe1" stroke="#b8863c"/>
<text x="130" y="86" text-anchor="middle" font-size="10.5" font-weight="bold" fill="#7a5a28">文殊指授（参1）</text>
<text x="130" y="104" text-anchor="middle" font-size="8.5" fill="#8a7a5e">求善知识三戒</text>
""" + "".join(
f"""<rect x="{240+i*150}" y="60" width="140" height="60" rx="10" fill="none" stroke="#d4a03c" stroke-dasharray="4,3"/>
<text x="{310+i*150}" y="86" text-anchor="middle" font-size="9.5" font-weight="bold" fill="#7a5a28">{t}</text>
<text x="{310+i*150}" y="104" text-anchor="middle" font-size="8" fill="#8a7a5e">{s}</text>"""
for i, (t, s) in enumerate([
    ('比丘众（参2-4）','吉祥雲·海雲·妙住'),
    ('长者居士（5-16）','解脱…普眼'),
    ('王与外道（17-20）','甘露火·大光'),
    ('市井诸师（21-28）','香船最勝…正趣'),
    ('天神夜天（29-38）','大天…大願精進'),
    ('母与童子（39-43）','瞿波摩耶字母')])) + f"""
<rect x="240" y="140" width="440" height="60" rx="10" fill="#f6efe1" stroke="#b8863c"/>
<text x="460" y="164" text-anchor="middle" font-size="10" font-weight="bold" fill="#7a5a28">賢勝→無勝軍→最寂靜→德生童子女（44-49）·彌勒楼阁（50）</text>
<text x="460" y="184" text-anchor="middle" font-size="8.5" fill="#8a7a5e">幻住九叠→毘盧遮那莊嚴藏大樓閣（两弹指·一多相即）</text>
<rect x="700" y="140" width="260" height="60" rx="10" fill="none" stroke="#c46b5d" stroke-width="1.5"/>
<text x="830" y="164" text-anchor="middle" font-size="10" font-weight="bold" fill="#c46b5d">文殊遥指（51）→ 普賢十愿王（52）</text>
<text x="830" y="184" text-anchor="middle" font-size="8.5" fill="#8a7a5e">遙申右手摩頂·「速往無量光佛剎」</text>
<text x="500" y="226" text-anchor="middle" font-size="11.5" fill="#5a5147">互动版：tabs/rufajie.html（身份着色·篇幅定径·悬停详card）</text>
</svg>""",
            "cap": "五十三参行程（§参批·互动版见页签）。",
            "en": "The fifty-three visit itinerary, interactive version in the site tab.",
            "dufa": [
                "巡礼读法：随善财自问「云何學菩薩行」。",
                "数据读法：dataset＋§7 附表。",
                "页签回看：互动行程。",
            ],
        },
        {
            "n": 2,
            "title": "参学语式图",
            "what": "每参一套仪式语法",
            "one": "到→礼→白→说→重述→偈→辞行",
            "svg": f"""<svg viewBox="0 0 1000 200" {W} xmlns="http://www.w3.org/2000/svg" font-family="serif">
<text x="500" y="26" text-anchor="middle" font-size="14.5" font-weight="bold" fill="#7a5a28">参学语式（46 请法锚实测）</text>
""" + "".join(
f"""<rect x="{20+i*136}" y="60" width="126" height="56" rx="8" fill="#f6efe1" stroke="#b8863c"/>
<text x="{83+i*136}" y="84" text-anchor="middle" font-size="10" font-weight="bold" fill="#7a5a28">{['到','禮','白','說','重述','偈','辭行'][i]}</text>
<text x="{83+i*136}" y="102" text-anchor="middle" font-size="7.5" fill="#8a7a5e">{['至城邑','禮足繞','我已先發','自陈法门','忆持复述','师说偈','南行'][i]}</text>"""
for i in range(7)) + f"""
<text x="500" y="156" text-anchor="middle" font-size="11.5" fill="#5a5147">「聖者！我已先發阿耨多羅三藐三菩提心，而未知菩薩云何學菩薩行……」</text>
<text x="500" y="184" text-anchor="middle" font-size="11.5" fill="#8a7a5e">善知识的回答方式各异（说法/示现/转介/摩顶），但仪式语法全程不变——参学之「礼」即义理之「路」〔本文判断〕</text>
</svg>""",
            "cap": "参学语式：七步仪式（46锚实测）。",
            "en": "The seven-step ritual grammar of every visit.",
            "dufa": [
                "七步读法：任取一参对表。",
                "变体读法：两疑参如何破式。",
                "末步读法：辞行即启下。",
            ],
        },
    ],
    "weici_note": "本品为全经归结：承離世間（品36）二千行门——善财一人走过；藏译 Toh44 ch39-45＋Toh45；乌茶王献经表文（五十五圣者之说）为版本史家具〔如实存目〕。",
    "weici": [
        ["離世間品（品 36）", "卷五十三起", "第八会·行海", "二千行门", "善财一人走过"],
        ["藏译 Toh44 ch39-45＋Toh45", "德格二函 fol 1b-274b", "章界对应", "TOC 在仓", "逐字对勘未竟"],
        ["八十品39", "卷60末-80·174,902 CJK", "对读主源", "译名对位十余处", "逐参对勘未竟"],
        ["六十末品34", "卷44-60·145,080 CJK", "canon XML 全量", "文较略", "对读未竟"],
        ["乌茶王献经表文", "卷末家具", "「五十五聖者善知識」", "参数异说佐证", "如实识别"],
    ],
    "teshe_note": "本品以主体转移与参学结构为特征。",
    "teshe": [
        ["体量", "261,526 CJK（T0293 全卷）", "八十174,902", "四源之最"],
        ["参学", "52卡全引·237,214 CJK", "46请法锚", "锚点级参界"],
        ["身份", "23类·在家众为主", "比丘仅5+1", "道在俗世〔本文判断〕"],
        ["法门名", "可标40/52", "未举名/转介如实", "回源纪律"],
    ],
    "dufa5": [
        ["巡礼读法", "图 〇-1 → 参批1-16", "全体读者", "随善财一问"],
        ["语式读法", "图 〇-2 → 各参", "精读读者", "七步仪式"],
        ["数据读法", "§7 附表＋dataset", "数据读者", "23类身份"],
        ["互动读法", "tabs/rufajie.html", "可视化读者", "行程页签"],
        ["对勘读法", "§2 四源基线", "版本学读者", "四源并置"],
    ],
    "shu": [
        ["**T0 经文明文**", "序品＋52参全引", "§2-参批（`T10n0293` 主体）", "结构总量"],
        ["**T0 本文实测**", "261,526 CJK／52卡237,214", "§7", "篇幅"],
        ["**对读层**", "八十/六十/canon 全量在仓", "§2 基线", "对勘未竟"],
        ["**藏本层**", "Toh44-45 TOC＋derge实文在仓", "L.201＋derge_kangyur", "对勘待批"],
        ["**可视化层**", "页签行历＋dataset", "L.305-306", "身份23类"],
    ],
    "shu_note": "> 【读法】本品之数以「**参**」为性：五十三参五十三门——读时持一问（云何學菩薩行）巡礼，门自开。\n",
}

ALL_EXT = [P33, P34, P35, P36, P37]

if __name__ == "__main__":
    want = set(sys.argv[1:])
    for d in ALL_EXT:
        if want and d["tag"] not in want:
            continue
        base.apply(d)
