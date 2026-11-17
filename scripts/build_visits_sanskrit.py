# -*- coding: utf-8 -*-
"""T9 逐参名·梵本对照：字面有异者的「同指」判（§17.24 十八组 ＋ §17.27 十七组）。

§17.22 只判字面：`＝`/`≈`/`≠`。字面异不等于所指异，但要说「所指同」，
须有第三方 witness。梵本《入法界品》（Vaidya 1960，GRETIL 电子转写）在库，
其指授句「gaccha kulaputra … tatra X nāma Y prativasati」与汉本逐参对应，
可作独立锚。

口径（要紧）：§17.22 中字面有异者共 35 组——
  ① 恰有一对同名、第三本独异：18 组（§17.24 所判：80=60≠40 九组 ＋ 80=40≠60 九组）
  ② 三本全异：17 组（§17.27 所判）
  ③ 三本同字：15 组（未逐条核梵；其中参45 已核为梵本空缺，余 14 组待核）
合计 18＋17＋15＝50 行，与 §17.22 的五十参一致。

对位用三重锚，不靠音写猜：
  ① 角色（比丘／長者／優婆夷／夜神…）
  ② 处所（īṣāṇo＝伊沙那、siṃhavijṛmbhitaṃ＝師子頻申、potalaka＝補怛洛迦…）
  ③ 次序（全部三十五组并入同一「指授事件」序，须不降；相等处必为空缺位）

「指授事件」= `asti/gaccha kulaputra` 起句、且其后 900 字内出现 `upasaṃkramya` 者，
全文恰 50 次，其中 48 次带 `nāma`（末次一句两名，故 49 位善知识）。

输出只作「同指／待核」，不做教义判，也不评音写精当。
"""
import hashlib
import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(r"C:\DA_Practice\huayan_collection")
SRC_REL = "data/references/sanskrit/gandavyuha_vaidya.txt"
SRC = ROOT / SRC_REL
OUT = ROOT / "data" / "research" / "visits_sanskrit.json"
VN = ROOT / "data" / "research" / "visits_names.json"

# §17.24：§17.22 中「恰有一对同名、第三本独异」的十八组
CASES = [
    dict(no=4, probe="supratisthito nāma bhikṣuḥ", skt="supratisthita",
         role="bhikṣuḥ（比丘）", place="sāgaratīraṃ nāma laṅkāpatham（楞伽道·海岸）",
         verdict="同指·义译",
         basis="su-pratiṣṭhita＝善／妙＋住；八十「善住」、四十「妙住」各取一侧"),
    dict(no=8, probe="āśā nāmopāsikā", skt="āśā",
         role="upāsikā（優婆夷）", place="samudravetāḍī；samantavyūhaṃ udyānaṃ（海潮處·普莊嚴園）",
         verdict="待核·对音不合",
         basis="梵本作 āśā（suprabha 王之妻）；八十「休捨」、四十「伊舍那」皆非其直接对音"),
    dict(no=10, probe="jayoṣmāyatano nāma brāhmaṇaḥ", skt="jayoṣmāyatana",
         role="brāhmaṇaḥ（婆羅門）", place="īṣāṇo nāma janapadaḥ（伊沙那聚落）",
         verdict="同指·义译",
         basis="jaya＋uṣma＝勝＋熱，八十／四十「勝熱」即其义译；六十「方便命」与梵名无对音关系",
         flag="六十「方便命」名源待核"),
    dict(no=11, probe="maitrāyaṇī nāma kanyā", skt="maitrāyaṇī",
         role="kanyā（童女，siṃhaketu 王之女）", place="siṃhavijṛmbhitaṃ nāma nagaram（師子頻申城）",
         verdict="同指·音义并存",
         basis="六十「彌多羅尼」为音写、四十「慈行」取 maitrī＝慈，同出一名"),
    dict(no=17, probe="samantanetro nāma gāndhikaḥ", skt="samantanetra",
         role="gāndhikaḥ śreṣṭhī（香師·長者）", place="vetramūlako janapadaḥ；samantamukhaṃ nagaram（藤根國·普門城）",
         verdict="同指·义译",
         basis="samanta-netra＝普眼；六十「普眼妙香」把 gāndhika（香師）也译进名里"),
    dict(no=21, probe="sarvagāmī nāma parivrājakaḥ", skt="sarvagāmin",
         role="parivrājakaḥ（外道）", place="tosalaṃ nāma nagaram（都薩羅城）",
         verdict="同指·义译",
         basis="sarva＋gāmin＝遍＋行（八十／四十「遍行」）；六十「隨順一切眾生」为同一名的散译"),
    dict(no=23, probe="vairo nāma dāśaḥ", skt="vaira",
         role="dāśaḥ（船師）", place="kūṭāgāraṃ nāma nagaram（海岸樓閣大城）",
         verdict="同指·对音",
         basis="八十／四十「婆施羅」为 vaira 的音写；六十「自在」与梵名无对音关系",
         flag="六十「自在」名源待核"),
    dict(no=24, probe="jayottamo nāma śreṣṭhī", skt="jayottama",
         role="śreṣṭhī（長者）", place="nandihāraṃ nāma nagaram（樂瓔珞城）",
         verdict="同指·义译",
         basis="jaya＋uttama＝勝＋無上；八十／六十「無上勝」、四十「最勝」皆其义译，唯词序不同"),
    dict(no=25, probe="siṃhavijṛmbhitā nāma bhikṣuṇī", skt="siṃhavijṛmbhitā",
         role="bhikṣuṇī（比丘尼）", place="kaliṅgavanaṃ nāma nagaram（羯陵迦林）",
         verdict="同指·义译",
         basis="siṃha＋vijṛmbhita＝師子＋頻申／奮迅；八十／四十「頻申」、六十「奮迅」同义异词"),
    dict(no=26, probe="vasumitrā nāma bhāgavatī", skt="vasumitrā",
         role="bhāgavatī（女）", place="ratnavyūhaṃ nāma nagaram（寶莊嚴城）",
         verdict="同指·对音",
         basis="婆須蜜多／伐蘇蜜多皆 vasumitrā 的音写异形（v/b 互换）"),
    dict(no=28, probe="avalokiteśvaro nāma bodhisattvaḥ", skt="avalokiteśvara",
         role="bodhisattvaḥ（菩薩）", place="potalako nāma parvataḥ（補怛洛迦山）",
         verdict="同指·音义并存",
         basis="avalokita＋īśvara＝觀＋自在（八十／四十）；六十「觀世音」为旧译一系"),
    dict(no=29, probe=None, skt=None, role=None, place=None,
         verdict="待核·梵本无对应",
         basis="观自在指授之后直入大天，其间一万五千余字无第三位指授句；四十「正性無異行」亦无梵名可对",
         gap=("avalokiteśvaro nāma bodhisattvaḥ", "mahādevo devaḥ")),
    dict(no=31, probe="sthāvarā nāma", skt="sthāvarā",
         role="pṛthvīdevatā（地神）", place="bodhimaṇḍe（菩提場）",
         verdict="同指·义译",
         basis="sthāvara＝住／不動；八十／六十「安住」、四十「自性不動」皆其义译"),
    dict(no=34, probe="pradakṣiṇena pramuditanayanajagadvirocanā nāma rātridevatā",
         skt="pramuditanayanajagadvirocanā",
         role="rātridevatā（夜神）", place="vairocanabodhimaṇḍa（菩提場右旋）",
         verdict="同指·义译",
         basis="pramudita-nayana＝喜目、jagad-virocana＝觀察／普照眾生；四十多一「一切」正对 jagat"),
    dict(no=40, probe="sutejomaṇḍalaratiśrīrnāma lumbinīvanadevatā",
         skt="sutejomaṇḍalaratiśrī",
         role="lumbinīvanadevatā（林神）", place="lumbinīvana（嵐毘尼園）",
         verdict="同指·义译",
         basis="su-tejo-maṇḍala-rati-śrī；八十「妙德圓滿」、四十「妙威德圓滿愛敬」皆压缩译"),
    dict(no=41, probe="gopā nāma", skt="gopā",
         role="śākyakanyā（釋女）", place="kapilavastu mahānagara（迦毘羅城）",
         verdict="同指·对音",
         basis="瞿波（八十／四十）与瞿夷（六十）皆 gopā 的音写，新旧译用字不同"),
    dict(no=46, probe="bhadrottamā nāmopāsikā", skt="bhadrottamā",
         role="upāsikā（優婆夷）", place="vartanakaṃ nagaram（婆呾那城）",
         verdict="同指·义译",
         basis="bhadra＋uttama＝賢＋勝；八十／六十「賢勝」、四十「最勝賢」唯词序倒置"),
    dict(no=50, probe="śivarāgro nāma brāhmaṇaḥ", skt="śivarāgra",
         role="brāhmaṇaḥ（婆羅門）", place="dharmagrāmaḥ（法聚落）",
         verdict="同指·音义并存",
         basis="śiva＝寂靜／尸毘；八十「最寂靜」取义、六十「尸毘最勝」取音"),
]

# §17.27：三本全异十七组
ALL_DIFF = [
    dict(no=2, probe="meghaśrīrnāma bhikṣuḥ", skt="meghaśrī",
         role="bhikṣuḥ（比丘）", place="rāmāvarānta janapada；sugrīva parvata（勝樂國·妙峯山）",
         verdict="同指·义译",
         basis="megha＝雲、śrī＝吉祥／德；八十「德雲」、六十「功德雲」、四十「吉祥雲」各取 śrī 之一训"),
    dict(no=9, probe="bhīṣmottaranirghoṣo nāma ṛṣiḥ", skt="bhīṣmottaranirghoṣa",
         role="ṛṣiḥ（仙人）", place="samudravetāḍī；nālayur janapada（海潮處·那羅素國）",
         verdict="同指·音义并存",
         basis="bhīṣma＝可畏／威猛、nirghoṣa＝聲，四十「大威猛聲」全为义译；八十「毘目瞿沙」之「瞿沙」＝ghoṣa 音写、六十「毘目多羅」之「多羅」＝(t)tara 音写，各取一名之一节"),
    dict(no=12, probe="sudarśano nāma bhikṣuḥ", skt="sudarśana",
         role="bhikṣuḥ（比丘）", place="trinayano janapada（三眼國）",
         verdict="同指·义译",
         basis="su＝善／妙、darśana＝見（亦训「現」）；八十「善見」、六十「善現」、四十「妙見」同出一名"),
    dict(no=13, probe="indriyeśvaro nāma dārakaḥ", skt="indriyeśvara",
         role="dārakaḥ（童子）", place="śramaṇamaṇḍala janapade sumukhaṃ nagaram（名聞國·河渚）",
         verdict="同指·义译",
         basis="indriya＝根、īśvara＝自在（主）；四十「根自在主」最全，八十「自在主」省「根」，六十「釋天主」以 indra（釋天）解 indriya，名源待核",
         flag="六十「釋天主」以 indra 解 indriya"),
    dict(no=14, probe="prabhūtā nāmopāsikā", skt="prabhūtā",
         role="upāsikā（優婆夷）", place="samudrapratiṣṭhānaṃ nagaram（海住城）",
         verdict="同指·义译",
         basis="prabhūta＝丰足／广大；八十「具足」、四十「辨具足」皆取「具足」一义，六十「自在」与梵名无对音／义译关系",
         flag="六十「自在」名源待核"),
    dict(no=15, probe="vidvānnāṃ gṛhapatiḥ", skt="vidvat（vidvānnāṃ … gṛhapatiḥ）",
         role="gṛhapatiḥ（居士）", place="mahāsaṃbhavaṃ nagaram（大興城）",
         verdict="同指·义译",
         basis="vidvat＝有智／明智；八十「明智」、四十「具足智」皆取「智」，六十「甘露頂」与梵名无对音关系",
         flag="六十「甘露頂」名源待核"),
    dict(no=16, probe="ratnacūḍo nāma dharmaśreṣṭhī", skt="ratnacūḍa",
         role="dharmaśreṣṭhī（長者）", place="siṃhapotaṃ nagaram（師子宮城）",
         verdict="同指·音义并存",
         basis="ratna＝寶、cūḍa＝髻；六十「周羅」是 cūḍā 的音写，八十／六十另增「法」字"),
    dict(no=18, probe="analo nāma rājā", skt="anala",
         role="rājā（王）", place="tāladhvajaṃ nagaram（多羅幢城）",
         verdict="待核·名源不合",
         basis="anala＝火，唯四十「甘露火」存「火」字；八十「無厭足」、六十「滿足」与 anala 无对音／义译关系。角色、处所、次序三锚皆合，故段位可定而名源不合",
         flag="八十「無厭足」／六十「滿足」名源待核"),
    dict(no=22, probe="tatrotpalabhūtirnāma gāndhikaśreṣṭhī", skt="utpalabhūti",
         role="gāndhikaśreṣṭhī（鬻香長者）", place="pṛthurāṣṭraṃ janapadaḥ（廣大國）",
         verdict="同指·义译",
         basis="utpala＝優鉢羅／青蓮華；六十「香」出 gāndhika（香師）而非名内，四十「具足」疑对 bhūti〔本文判断〕"),
    dict(no=27, probe="veṣṭhilo nāma gṛhapati", skt="veṣṭhila",
         role="gṛhapatiḥ（居士）", place="śubhapāraṃgamaṃ nagaram（善度城）",
         verdict="同指·对音",
         basis="八十「鞞瑟胝羅」、四十「毘瑟底羅」皆 veṣṭhila 的音写；六十「安住」与梵名无对音关系，疑与参31 sthāvarā（安住）相涉",
         flag="六十「安住」名源待核"),
    dict(no=32, probe="vāsantī nāma rātridevatā", skt="vāsantī",
         role="rātridevatā（主夜神）", place="kapilavastu（迦毘羅城）",
         verdict="同指·音义并存",
         basis="vasanta＝春，四十「春和」取义；八十「婆珊婆演底」、六十「婆娑婆陀」皆 vāsantī 的音写"),
    dict(no=33, probe="samantagambhīraśrīvimalaprabhā nāma rātridevatā",
         skt="samantagambhīraśrīvimalaprabhā",
         role="rātridevatā（主夜神）", place="bodhimaṇḍa（菩提場）",
         verdict="同指·义译",
         basis="samanta＝普遍／普、gambhīra＝甚深、śrī＝吉祥／妙德、vimala＝無垢／淨、prabhā＝光；三本繁简各不同而元素俱全"),
    dict(no=35, probe="samantasattvatrāṇojaḥśrī nāma rātridevatā",
         skt="samantasattvatrāṇojaḥśrī",
         role="rātridevatā（主夜神）", place="tathāgataparṣanmaṇḍala（如來眾會）",
         verdict="同指·义译",
         basis="samanta＝普、sattva＝眾生、trāṇa＝救護、ojas＝威力／威德、śrī＝妙德／吉祥；三本词序互倒而元素同"),
    dict(no=36, probe="praśāntarutasāgaravatī nāma rātridevatā",
         skt="praśāntarutasāgaravatī",
         role="rātridevatā（主夜神）", place="bodhimaṇḍa（菩提場）",
         verdict="同指·义译",
         basis="praśānta＝寂靜、ruta＝音、sāgara＝海、vatī＝具足／有；六十「寂靜音」省「海」与 vatī，八十／四十全译"),
    dict(no=37, probe="sarvanagararakṣāsaṃbhavatejaḥśrīrnāma rātridevatā",
         skt="sarvanagararakṣāsaṃbhavatejaḥśrī",
         role="rātridevatā（主夜神）", place="vairocanasya parṣanmaṇḍala（菩提場如來會）",
         verdict="同指·义译",
         basis="sarva＝一切、nagara＝城、rakṣā＝守護、saṃbhava＝增長／生、tejaḥ＝威力／威德、śrī＝妙德／吉祥"),
    dict(no=38, probe="sarvavṛkṣapraphullanasukhasaṃvāsā nāma rātridevatā",
         skt="sarvavṛkṣapraphullanasukhasaṃvāsā",
         role="rātridevatā（主夜神）", place="bhagavato vairocanasya pādamūla（佛足下）",
         verdict="同指·义译",
         basis="sarva＝一切、vṛkṣa＝樹、praphullana＝開敷、sukha＝安樂、saṃvāsā＝共住／所依"),
    dict(no=39, probe="sarvajagadrakṣāpraṇidhānavīryaprabhā nāma rātridevatā",
         skt="sarvajagadrakṣāpraṇidhānavīryaprabhā",
         role="rātridevatā（主夜神）", place="bodhimaṇḍa（道場）",
         verdict="同指·义译",
         basis="sarva-jagat＝一切眾生、rakṣā＝守護／救護、praṇidhāna＝願、vīrya＝精進力、prabhā＝光明"),
]

# §17.28：三本同字十五组中的十三组（参45 为梵本空缺、参51 为一句两名，另列）
SAME_CASES = [
    dict(no=3, probe="sāgaramegho nāma bhikṣuḥ", skt="sāgaramegha",
         role="bhikṣuḥ（比丘）", place="sāgaramukhaḥ dikpratyuddeśaḥ（海門·海岸）",
         verdict="同指·义译",
         basis="sāgara＝海、megha＝雲；三本皆作「海雲」，全为义译"),
    dict(no=5, probe="megho nāma dramiḍaḥ", skt="megha",
         role="dramiḍaḥ（達羅毗荼人）", place="vajrapuraṃ nāma dramiḍapaṭṭanam（金剛城·商埠）",
         verdict="同指·对音",
         basis="megha 音写作「彌伽」；三本同字同音写，非义译"),
    dict(no=6, probe="muktako nāma śreṣṭhī", skt="muktaka",
         role="śreṣṭhī（長者）", place="vanavāsī nāma janapadaḥ（住林聚落）",
         verdict="同指·义译",
         basis="mukta＝解脫；三本皆作「解脫」，取义不取音"),
    dict(no=7, probe="sāradhvajo nāma bhikṣuḥ", skt="sāradhvaja",
         role="bhikṣuḥ（比丘）", place="milaspharaṇaṃ nāma jambūdvīpaśīrṣam（摩利聚落·閻浮頂）",
         verdict="同指·义译",
         basis="dhvaja＝幢，与三本「海幢」之「幢」合；sāra＝堅／實，非海，「海」字无对",
         flag="「海」字无对（sāra＝堅／實），疑所据本作 sāgara-dhvaja〔本文判断〕"),
    dict(no=19, probe="mahāprabho nāma rājā", skt="mahāprabha",
         role="rājā（王）", place="suprabhaṃ nāma nagaram（妙光城）",
         verdict="同指·义译",
         basis="mahā＝大、prabhā＝光；三本皆作「大光」"),
    dict(no=20, probe="acalā nāmopāsikā", skt="acalā",
         role="upāsikā（優婆夷）", place="sthirā nāma rājadhānī（安住王都）",
         verdict="同指·义译",
         basis="a-calā＝不動；三本皆作「不動」，取义"),
    dict(no=30, probe="mahādevo devaḥ", skt="mahādeva",
         role="devaḥ（天神）", place="dvāravatī nāma nagarī（多羅婆底城）",
         verdict="同指·义译",
         basis="mahā＝大、deva＝天；三本皆作「大天」"),
    dict(no=42, probe="māyā nāma devī", skt="māyā",
         role="devī（佛母）", place="kapilavastu（迦毘羅城）；bhagavato vairocanasya pādamūle（佛足下）",
         verdict="同指·对音",
         basis="māyā 音写作「摩耶」；三本同字同音写"),
    dict(no=43, probe="surendrābhā nāma devakanyā", skt="surendrābhā",
         role="devakanyā（天女）", place="tridaśendrabhavana（三十三天）",
         verdict="同指·义译",
         basis="surendra＝天主（釋天）、ābhā＝光；三本皆作「天主光」"),
    dict(no=44, probe="viśvāmitro nāma dārakācāryaḥ", skt="viśvāmitra",
         role="dārakācāryaḥ（童子師）", place="kapilavastu mahānagara（迦毘羅城）",
         verdict="同指·义译",
         basis="viśva＝遍、mitra＝友；三本皆作「遍友」"),
    dict(no=47, probe="muktāsāro nāma hairaṇyakaḥ", skt="muktāsāra",
         role="hairaṇyakaḥ（金師）", place="bharukacchaṃ nāma nagaram（婆羅吸摩城）",
         verdict="同指·义译",
         basis="mukta＝解脫、sāra＝堅固；梵名词序倒，三本皆作「堅固解脫」"),
    dict(no=48, probe="sucandro nāma gṛhapatiḥ", skt="sucandra",
         role="gṛhapatiḥ（居士）", place="bharukacchaṃ nāma nagaram（婆羅吸摩城）",
         verdict="同指·义译",
         basis="su＝妙／善、candra＝月；三本皆作「妙月」"),
    dict(no=49, probe="ajitaseno nāma gṛhapatiḥ", skt="ajitasena",
         role="gṛhapatiḥ（居士）", place="rorukaṃ nāma nagaram（路羅城）",
         verdict="同指·义译",
         basis="a-jita＝無勝、senā＝軍；三本皆作「無勝軍」"),
]

# 附见：不在三十五组内，但同一次核梵时直接读出、值得单列的发现
BYPRODUCTS = [
    dict(no=51, probe="śrīsaṃbhavo nāma dārakaḥ", also="śrīmatiśca nāma dārikā",
         skt="śrīsaṃbhava＋śrīmatī",
         role="dārakaḥ＋dārikā（童子＋童女）", place="sumanāmukhaṃ nāma nagaram（名聞國）",
         basis="梵本一句并举两名：「śrīsaṃbhavo nāma dārakaḥ prativasati, śrīmatiśca nāma dārikā」；"
               "汉本作「德生·有德」并列一处，是梵本如此，非编者合并"),
]

# 附见：三本同字（不在三十五组内）而梵本实无指授句者
SAME_GAPS = [
    dict(no=45, between=("viśvāmitro nāma dārakācāryaḥ", "bhadrottamā nāmopāsikā"),
         basis="viśvāmitra（遍友）之後直入 bhadrottamā（賢勝），其間無第三位指授句；"
               "Vaidya 本无「善知眾藝」一位（śilpa 只见于教法文句，非独立善知识）"),
]


def normalize(text: str):
    out, idx = [], []
    for i, ch in enumerate(text):
        if ch.isspace():
            if out and out[-1] == " ":
                continue
            out.append(" ")
            idx.append(i)
        else:
            out.append(ch)
            idx.append(i)
    return "".join(out), idx


def main() -> int:
    raw = SRC.read_text(encoding="utf-8", errors="replace")
    t, _ = normalize(raw)

    # 指授事件：asti/gaccha kulaputra 起句，且 900 字内出现 upasaṃkramya
    instr = []
    for m in re.finditer(r"(?:asti|gaccha) kulaputra", t):
        w = t[m.start():m.start() + 900]
        u = w.find("upasaṃkramya")
        if u >= 0:
            instr.append(m.start())
    if len(instr) != 50:
        print(f"!! 指授事件 {len(instr)} != 50")
        return 1

    pages = [(m.start(), int(m.group(1))) for m in re.finditer(r"\(gv (\d+)\)", t)]
    spans = []
    for s in instr:
        w = t[s:s + 900]
        spans.append((s, s + w.find("upasaṃkramya") + 20))

    def gv_at(pos: int):
        best = None
        for p, n in pages:
            if p <= pos:
                best = n
            else:
                break
        return f"gv {best}" if best else None

    def ord_at(pos: int):
        k = 0
        for s in instr:
            if s <= pos:
                k += 1
            else:
                break
        return k or None

    def locate(probe: str):
        """返回唯一命中位；正文复述造成的多重命中，限定在指授句内。"""
        hits = [m.start() for m in re.finditer(re.escape(probe), t)]
        if len(hits) > 1:
            hits = [h for h in hits if any(a <= h <= b for a, b in spans)]
        return hits

    vn = json.loads(VN.read_text(encoding="utf-8"))
    by_no = {r["no"]: r for r in vn["rows"]}

    # §17.22 的三分：恰一对同名（§17.24）／三本全异（§17.27）／三本同字
    tri = {r["no"]: {r["n80"], r["n60"], r["n40"]} for r in vn["rows"]}
    one_eq = sorted(n for n, s in tri.items() if len(s) == 2)
    all_diff = sorted(n for n, s in tri.items() if len(s) == 3)
    all_same = sorted(n for n, s in tri.items() if len(s) == 1)
    if [c["no"] for c in CASES] != one_eq:
        print("!! CASES 与「恰一对同名」的十八组不一致")
        print("   cases:", [c["no"] for c in CASES])
        print("   one_eq:", one_eq)
        return 8
    if [c["no"] for c in ALL_DIFF] != all_diff:
        print("!! ALL_DIFF 与「三本全异」的十七组不一致")
        print("   all_diff:", [c["no"] for c in ALL_DIFF])
        print("   expected:", all_diff)
        return 8
    same_covered = sorted([c["no"] for c in SAME_CASES]
                          + [g["no"] for g in SAME_GAPS]
                          + [b["no"] for b in BYPRODUCTS])
    if same_covered != all_same:
        print("!! SAME_CASES／SAME_GAPS／BYPRODUCTS 与「三本同字」的十五组不一致")
        print("   covered:", same_covered)
        print("   expected:", all_same)
        return 16

    def build_case(c):
        row = by_no[c["no"]]
        rec = {
            "no": c["no"],
            "n80": row["n80"], "n60": row["n60"], "n40": row["n40"],
            "rel80_60": row["rel80_60"], "rel80_40": row["rel80_40"],
            "skt": c["skt"], "skt_role": c["role"], "skt_place": c["place"],
            "verdict": c["verdict"], "basis": c["basis"],
            "flag": c.get("flag"),
            "probe": c["probe"],
        }
        if c["probe"]:
            hits = locate(c["probe"])
            if len(hits) != 1:
                raise SystemExit(f"!! probe not unique ({len(hits)}): 参{c['no']} {c['probe']}")
            pos = hits[0]
            rec["pos"] = pos
            rec["ord"] = ord_at(pos)
            rec["gv"] = gv_at(pos)
        else:
            a = t.find(c["gap"][0])
            b = t.find(c["gap"][1])
            if a < 0 or b < 0 or b < a:
                raise SystemExit(f"!! gap anchors not found: 参{c['no']}")
            inner = [s for s in instr if a < s < b]
            own = max([s for s in instr if s < b], default=None)
            inner = [s for s in inner if s != own]
            if inner:
                raise SystemExit(f"!! gap for 参 {c['no']} is not empty: {len(inner)}")
            rec["pos"] = a
            rec["ord"] = ord_at(a)
            rec["gv"] = gv_at(a)
            rec["gv_to"] = gv_at(b)
            rec["gap_chars"] = (own - a) if own else (b - a)
            rec["gap_between"] = list(c["gap"])
        return rec

    cases = [build_case(c) for c in CASES]
    diffs = [build_case(c) for c in ALL_DIFF]
    sames = [build_case(c) for c in SAME_CASES]

    # 附见：一句两名的梵本 witness
    byp = []
    for b in BYPRODUCTS:
        hits = [m.start() for m in re.finditer(re.escape(b["probe"]), t)]
        if len(hits) != 1:
            print(f"!! byproduct probe not unique ({len(hits)}): {b['probe']}")
            return 6
        near = t[hits[0]:hits[0] + 200]
        if b["also"] not in near:
            print(f"!! byproduct second name not adjacent: {b['also']}")
            return 7
        row = by_no[b["no"]]
        byp.append({
            "no": b["no"], "n80": row["n80"], "n60": row["n60"], "n40": row["n40"],
            "skt": b["skt"], "skt_role": b["role"], "skt_place": b["place"],
            "probe": b["probe"], "also": b["also"],
            "pos": hits[0], "ord": ord_at(hits[0]), "gv": gv_at(hits[0]),
            "basis": b["basis"],
        })

    # 附见：同字而梵本空缺（参45）
    gaps_same = []
    for g in SAME_GAPS:
        a = t.find(g["between"][0])
        b2 = t.find(g["between"][1])
        if a < 0 or b2 < 0 or b2 < a:
            print(f"!! same-gap anchors missing: 参{g['no']}")
            return 10
        own = max([s for s in instr if s < b2], default=None)
        inner = [s for s in instr if a < s < b2 and s != own]
        if inner:
            print(f"!! same-gap for 参 {g['no']} is not empty: {len(inner)}")
            return 11
        row = by_no[g["no"]]
        gaps_same.append({
            "no": g["no"], "n80": row["n80"], "n60": row["n60"], "n40": row["n40"],
            "between": list(g["between"]), "basis": g["basis"],
            "pos": a, "ord": ord_at(a),
            "gv": gv_at(a), "gv_to": gv_at(b2),
            "gap_chars": (own - a) if own else (b2 - a),
        })

    # 次序自检（全表）：三十五组＋三本同字十五组 并入同一指令序，须不降；
    # 相等对数必等于已被前一位占据的空缺案数（参29 前有 28、参45 前有 44）
    combined = [(c["no"], c["ord"]) for c in cases + diffs + sames]
    combined += [(g["no"], g["ord"]) for g in gaps_same]
    combined += [(b["no"], b["ord"]) for b in byp]
    combined.sort()
    filled, prev = [], None
    for no, o in combined:
        if o is None:
            o = prev
        prev = o
        filled.append((no, o))
    ords_all = [o for _, o in filled]
    if ords_all != sorted(ords_all):
        print("!! Sanskrit ordinals decrease:", ords_all)
        return 5
    dup_all = sum(1 for a, b in zip(ords_all, ords_all[1:]) if a == b)
    # 相等处只会落在「空缺位」，且其前一位也须在本表内。
    nos_all = {c["no"] for c in cases + diffs + sames} | {b["no"] for b in byp}
    gaps_expected = sum(1 for c in cases if not c["probe"]) + \
        sum(1 for g in gaps_same if (g["no"] - 1) in nos_all)
    if dup_all != gaps_expected:
        print(f"!! ordinals equal {dup_all} times but in-table gaps {gaps_expected}:", ords_all)
        return 9
    for g in gaps_same:
        after = min((c for c in cases + diffs + sames if c["no"] > g["no"]),
                    key=lambda c: c["no"])
        if after["ord"] != g["ord"] + 1:
            print(f'!! same-gap 参{g["no"]} does not occupy exactly one slot: '
                  f'{g["ord"]} -> {after["ord"]} (参{after["no"]})')
            return 15
    sords = [c["ord"] for c in sames]
    if sords != sorted(sords) or len(set(sords)) != len(sords):
        print("!! §17.28 ordinals not strictly increasing:", sords)
        return 17

    # §17.24 内单独复检（同一套指令序，十八组自不降、一相等）
    ords = [c["ord"] for c in cases if c["ord"]]
    if ords != sorted(ords):
        print("!! §17.24 ordinals decrease:", ords)
        return 12
    dup = sum(1 for a, b in zip(ords, ords[1:]) if a == b)
    gaps = sum(1 for c in cases if not c["probe"])
    if dup != gaps:
        print(f"!! §17.24 ordinals equal {dup} != gap cases {gaps}:", ords)
        return 13
    dords = [c["ord"] for c in diffs]
    if dords != sorted(dords) or len(set(dords)) != len(dords):
        print("!! §17.27 ordinals not strictly increasing:", dords)
        return 14

    def tally(rows):
        same = sum(1 for c in rows if c["verdict"].startswith("同指"))
        pend = sum(1 for c in rows if c["verdict"].startswith("待核"))
        bv = {}
        for c in rows:
            bv[c["verdict"]] = bv.get(c["verdict"], 0) + 1
        return same, pend, bv

    same, pend, bv = tally(cases)
    dsame, dpend, dbv = tally(diffs)
    ssame, spend, sbv = tally(sames)
    same_unprobed = [n for n in all_same
                     if n not in {c["no"] for c in sames}
                     and n not in {g["no"] for g in gaps_same}
                     and n not in {b["no"] for b in byp}]

    stats = {
        "cases": len(cases),
        "same": same,
        "pending": pend,
        "by_verdict": bv,
        "flagged": [c["no"] for c in cases if c["flag"]],
        "ord_first": min(ords),
        "ord_last": max(ords),
        "all_diff_cases": len(diffs),
        "all_diff_same": dsame,
        "all_diff_pending": dpend,
        "all_diff_by_verdict": dbv,
        "all_diff_flagged": [c["no"] for c in diffs if c["flag"]],
        "diff_ord_first": min(dords),
        "diff_ord_last": max(dords),
        "same_cases": len(sames),
        "same_same": ssame,
        "same_pending": spend,
        "same_by_verdict": sbv,
        "same_flagged": [c["no"] for c in sames if c["flag"]],
        "same_ord_first": min(sords),
        "same_ord_last": max(sords),
        "rows": len(tri),
        "rows_diff": len(one_eq) + len(all_diff),
        "rows_judged": (len(cases) + len(diffs) + len(sames)
                        + len(gaps_same) + len(byp)),
        "rows_same": len(all_same),
        "rows_same_gap": len(gaps_same),
        "rows_same_probed": len(sames),
        "rows_same_byproduct": len(byp),
        "rows_same_unprobed": len(same_unprobed),
        "same_gap_nos": [g["no"] for g in gaps_same],
        "same_unprobed_nos": same_unprobed,
        "ord_all_first": min(ords_all),
        "ord_all_last": max(ords_all),
        "ord_all_equal_pairs": dup_all,
    }

    data = {
        "meta": {
            "operator": "T9",
            "title": "入法界品五十参·梵本同指判（§17.24 十八组／§17.27 十七组／§17.28 十五组）",
            "date": date.today().isoformat(),
            "method": ("取 §17.22 的五十参，先在梵本《入法界品》定位其指授句"
                       "（asti/gaccha kulaputra … X nāma Y prativasati … upasaṃkramya），"
                       "以角色＋处所＋次序三锚对位；判据为译名与梵名之对音／义译关系，"
                       "只判同指与否，不判音写精当。五十行并入同一指授事件序自检，"
                       "相等处必为空缺位（参29 正趣、参45 善知眾藝）。"
                       "全篇此类事件 50 次，末次为弥勒场景、无教师名，故善知识对位至第 49 事件。"),
            "scope": (f'五十行全部核梵：§17.24 十八组（恰有一对同名：{one_eq[0]}…{one_eq[-1]}）'
                      f'＋§17.27 十七组（三本全异：{all_diff[0]}…{all_diff[-1]}）'
                      f'＋§17.28 十五组（三本同字：{all_same[0]}…{all_same[-1]}；'
                      f'十三组直核、参 {gaps_same[0]["no"]} 空缺、'
                      f'参 {byp[0]["no"]} 一句两名）。'),
            "source": {
                "path": SRC_REL,
                "bytes": SRC.stat().st_size,
                "sha256": hashlib.sha256(SRC.read_bytes()).hexdigest(),
                "edition": "P. L. Vaidya, Gaṇḍavyūhasūtram, Darbhanga: Mithila Institute, 1960 (BST 5)",
                "etext": "GRETIL (sa_gaNDavyUhasUtra), 2020-07-31 版转写",
                "pagination": "文中 (gv N) 为 GRETIL 依 Vaidya 书页所加页码标记",
            },
        },
        "cases": cases,
        "byproducts": byp,
        "stats": stats,
        "boundaries": [
            "这是「同指」判，不是译名优劣判：同指只表两本指同一位善知识，不评谁译得准。",
            "单一写本系统：所用为 Vaidya 校本之电子转写，非多本会校；故「Vaidya 本无对应」只能记作该本无，不得推为梵本原无。",
            (f'对位靠角色＋处所＋次序三锚；次序单调性由脚本自检——§17.24 十八组的梵本指令序不降'
             f'（{stats["ord_first"]}–{stats["ord_last"]} 段，唯一相等处即正趣空缺位，沿用观自在之序），'
             f'§17.27 十七组、§17.28 十三组与参45 空缺、参51 并入同一指令序'
             f'（{stats["ord_all_first"]}–{stats["ord_all_last"]} 段）仍不降，'
             f'两处相等处恰为两个空缺位（参 29、参 45）。处所名逐条附于表内可复检。'),
            "音写是否合于梵音、义译是否尽义，皆不在本节判内；只记两本名与该梵名有无可判的关系。",
            (f'五十行至此全部核梵：字面有异 35 组（§17.24＋§17.27）'
             f'＋三本同字 15 组（§17.28：十三组直核、参 {stats["same_gap_nos"][0]} 空缺、'
             f'参 {byp[0]["no"]} 一句两名），已核 {stats["rows_judged"]}/50。'
             f'「同指」不等于「同本」：字面同者亦已逐名核梵，非以字面偶合充数；'
             f'same 组未核者 {len(same_unprobed)}。'),
        ],
        "all_diff": {
            "meta": {
                "operator": "T9",
                "title": "入法界品三本全异十七组·梵本同指判（续 §17.24）",
                "date": date.today().isoformat(),
                "method": ("取 §17.22 中三本全异的十七组，逐组定位梵本指授句，以角色＋处所＋次序三锚对位；"
                           "与 §17.24 十八组并入同一指授事件序自检。"),
                "scope": f'十七组（{all_diff[0]}…{all_diff[-1]}）。',
            },
            "cases": diffs,
            "gaps": gaps_same,
            "stats": {
                "cases": len(diffs),
                "same": dsame,
                "pending": dpend,
                "by_verdict": dbv,
                "flagged": [c["no"] for c in diffs if c["flag"]],
                "ord_first": min(dords),
                "ord_last": max(dords),
            },
            "boundaries": [
                "这是「同指」判，不是译名优劣判：三本字面全异，只判其是否同出一梵名，不评谁译得准。",
                "单一写本系统：所用为 Vaidya 校本之电子转写；参 18 的梵名 anala 与八十／六十之名不合，只能记作该本如此，不得推为梵本原无别名。",
                (f'次序与 §17.24、§17.28 同用一套指令序（{stats["ord_all_first"]}–{stats["ord_all_last"]} 段）；'
                 f'本节十七组的序（{min(dords)}–{max(dords)}）严格递增，无相等。'
                 f'附表「參45」非本节十七组之一，乃三本同字而梵本空缺者，一并核出。'),
                "音写是否合于梵音、义译是否尽义，皆不在本节判内。",
                (f'三本同字十五组见 §17.28（十三组直核、参 {gaps_same[0]["no"]} 空缺、'
                 f'参 {byp[0]["no"]} 一句两名）；至此五十行全部核梵，'
                 f'本节与 §17.24 的字面有异者不再是「判而未核」的悬案。'),
            ],
        },
        "same": {
            "meta": {
                "operator": "T9",
                "title": "入法界品三本同字十五组·梵本逐名核（续 §17.27）",
                "date": date.today().isoformat(),
                "method": ("取 §17.22 中三本字面全同的十五组，逐组在梵本《入法界品》定位指授句，"
                           "核其梵名与汉名之对音／义译关系；十三组直核，"
                           "参45 为「Vaidya 本无指授句」，参51 为一句两名（śrīsaṃbhava＋śrīmatī）。"),
                "scope": (f'十五组（{all_same[0]}…{all_same[-1]}）：'
                          f'十三组直核＋参 {gaps_same[0]["no"]} 空缺＋参 {byp[0]["no"]} 一句两名。'),
            },
            "cases": sames,
            "gaps": gaps_same,
            "byproducts": byp,
            "stats": {
                "cases": len(sames),
                "same": ssame,
                "pending": spend,
                "by_verdict": sbv,
                "flagged": [c["no"] for c in sames if c["flag"]],
                "ord_first": min(sords),
                "ord_last": max(sords),
                "gap_nos": [g["no"] for g in gaps_same],
                "byproduct_nos": [b["no"] for b in byp],
            },
            "boundaries": [
                "这是「同指」判：三本字面相同，仍须核其梵名，不得以字面偶合径判已核。",
                "单一写本系统：所用为 Vaidya 校本之电子转写；参 45 只记「该本无指授句」，不得推为梵本原无。",
                (f'十三组直核＋参 {gaps_same[0]["no"]} 空缺＋参 {byp[0]["no"]} 一句两名，合十五组；'
                 f'本节组的序（{min(sords)}–{max(sords)}）严格递增，无相等。'),
                "参 7「海幢」与 sāradhvaja：dhvaja＝幢合，sāra＝堅／實非海，「海」字无对，判同指·义译而附记此疑；不擅改汉名。",
                "参 51 梵本一句两名（śrīsaṃbhava 童子＋śrīmatī 童女），汉本合为「德生·有德」一位；只记梵本如此，不作分合判。",
                "音写是否合于梵音、义译是否尽义，皆不在本节判内。",
            ],
        },
    }

    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f'§17.24 cases {stats["cases"]}  same {same}  pending {pend}  ord {stats["ord_first"]}..{stats["ord_last"]}')
    for c in cases:
        print(f'{c["no"]:>3} {c["n80"]:<8} {c["n60"]:<8} {c["n40"]:<10} | '
              f'{str(c["skt"]):<32} {str(c["gv"]):>7} | {c["verdict"]}'
              + (f'  [{c["flag"]}]' if c["flag"] else ""))
    print(f'§17.27 cases {len(diffs)}  same {dsame}  pending {dpend}  ord {min(dords)}..{max(dords)}')
    for c in diffs:
        print(f'{c["no"]:>3} {c["n80"]:<8} {c["n60"]:<8} {c["n40"]:<10} | '
              f'{str(c["skt"]):<40} {str(c["gv"]):>7} | {c["verdict"]}'
              + (f'  [{c["flag"]}]' if c["flag"] else ""))
    print(f'§17.28 cases {len(sames)}  same {ssame}  pending {spend}  '
          f'ord {min(sords)}..{max(sords)}  gap {stats["same_gap_nos"]}  '
          f'byproduct {[b["no"] for b in byp]}')
    for c in sames:
        print(f'{c["no"]:>3} {c["n80"]:<10} {c["n60"]:<10} {c["n40"]:<12} | '
              f'{str(c["skt"]):<14} {str(c["gv"]):>7} | {c["verdict"]}'
              + (f'  [{c["flag"]}]' if c["flag"] else ""))
    print(f'全表 ord {stats["ord_all_first"]}..{stats["ord_all_last"]}  '
          f'equal_pairs {stats["ord_all_equal_pairs"]}  judged {stats["rows_judged"]}/50')
    print("written", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
