-- huayan.db snapshot (FTS5 indexes are derived; rebuilt on replay)
PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE persons (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    source_id       TEXT    UNIQUE,                        -- 原始ID (如 person_042)
    name_zh         TEXT    NOT NULL,
    name_bo         TEXT,                                  -- 藏文名 (Wylie)
    name_sa         TEXT,                                  -- 梵文名 (IAST)
    name_en         TEXT,                                  -- 英文/拼音
    name_ja         TEXT,                                  -- 日文名
    alt_names       TEXT,                                  -- 别名/号，JSON数组: ["贤首国师","香象大师"]
    title           TEXT,                                  -- 头衔/称号 (如 "华严宗三祖")
    type            TEXT    NOT NULL DEFAULT 'practitioner',
                    -- patriarch | translator | practitioner | scholar | patron | monarch
    birth_year      INTEGER,
    death_year      INTEGER,
    dynasty         TEXT,                                  -- 唐/宋/元/明/清/近现代/当代
    biography       TEXT,                                  -- 生平简介
    lineage_branch  TEXT,                                  -- 所属传承支系
    lineage_order   INTEGER,                               -- 在支系中的辈分序位 (1=初祖, 2=二祖...)
    key_works       TEXT,                                  -- 代表著作，JSON数组
    works_links     TEXT,                                  -- 著作链接，JSON对象 {"作品名":"url"}
    multi_lineage   TEXT,                                  -- 多重传承支系，JSON数组 ["临济宗","曹洞宗"]
    source          TEXT,                                  -- 传记出处 (如 《宋高僧传》卷五)
    verified        INTEGER DEFAULT 0,                     -- 0=传统记载 1=学术确认
    created_at      TEXT    DEFAULT (datetime('now')),
    updated_at      TEXT    DEFAULT (datetime('now'))
);
INSERT INTO "persons" VALUES(1,'person_000a','龙树',NULL,'Nāgārjuna','Nagarjuna',NULL,NULL,'华严宗远祖（八宗共祖）','patriarch',150,250,'古印度','大乘中观学派创始人。据传入龙宫取回《华严经》下本十万偈流传人间。造《十住毗婆沙论》（《十地品》注释，又称《大不思议论》），被华严宗奉为法统源头。','华严宗远祖',0,'["十住毗婆沙论", "中论"]',NULL,NULL,'《龙树菩萨传》(CBETA T50n2047)；《华严经传记》',1,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(2,'person_000b','世亲',NULL,'Vasubandhu','Vasubandhu',NULL,NULL,'唯识宗祖师','scholar',NULL,NULL,'古印度','古印度唯识学派大师。造《十地经论》十二卷，系统注释《华严经·十地品》，其「六相」等名相创新深刻影响华严宗教学。汉译催生了南北朝地论师学派。',NULL,NULL,'["十地经论", "唯识三十颂"]',NULL,NULL,'真谛译《婆薮盘豆法师传》(T50n2049)、《十地经论 卷首序》(T26n1522)',1,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(3,'person_001','杜顺',NULL,NULL,'Dushun',NULL,'["法顺", "帝心尊者"]','华严初祖','patriarch',557,640,'唐','华严宗初祖。雍州万年人。年十八出家于因圣寺。以《华严法界观门》开创华严宗观法体系。唐太宗赐号''帝心''。','华严五祖',1,'["华严法界观门", "华严五教止观"]','{"华严法界观门": "https://cbeta.buddhism.org.hk/xml/T45/T45n1884_001.xml", "华严五教止观": "https://cbeta.buddhism.org.hk/xml/T45/T45n1867_001.xml"}',NULL,'《续高僧传》卷二十五·法顺传 (CBETA T50n2060)',1,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(4,'person_002','智俨',NULL,NULL,'Zhiyan',NULL,'["至相尊者", "云华尊者"]','华严二祖','patriarch',602,668,'唐','华严宗二祖。天水人。从杜顺出家，后于至相寺从慧光学华严。著《华严经搜玄记》开华严宗经疏之先河，为法藏之师。','华严五祖',2,'["华严经搜玄记", "华严一乘十玄门", "华严五十要问答"]','{"华严经搜玄记": "https://cbeta.buddhism.org.hk/xml/T35/T35n1732_001.xml", "华严一乘十玄门": "https://cbeta.buddhism.org.hk/xml/T45/T45n1868_001.xml", "华严五十要问答": "https://cbeta.buddhism.org.hk/xml/T45/T45n1869_001.xml"}',NULL,'《宋高僧传》卷五·智俨传 (CBETA T50n2061)；《华严经传记》卷四',1,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(5,'person_003','法藏',NULL,'Dharmamitra','Fazang',NULL,'["贤首国师", "贤首大师", "香象大师", "康藏国师"]','华严三祖·实际创立者','patriarch',643,712,'唐','华严宗实际创立者。祖籍康居，生于长安。从智俨学《华严》。参与实叉难陀译场。武则天赐号''贤首''。系统化''五教十宗''判教与''法界观门''观法。讲说《华严经》三十余遍。','华严五祖',3,'["华严一乘教义分齐章（五教章）", "华严经探玄记", "华严经义海百门", "华严金师子章", "大乘起信论义记", "十二门论宗致义记"]','{"华严一乘教义分齐章（五教章）": "https://cbeta.buddhism.org.hk/xml/T45/T45n1866_001.xml", "华严经探玄记": "https://cbeta.buddhism.org.hk/xml/T35/T35n1733_001.xml", "华严经义海百门": "https://cbeta.buddhism.org.hk/xml/T45/T45n1875_001.xml", "华严金师子章": "https://cbeta.buddhism.org.hk/xml/T45/T45n1880_001.xml", "大乘起信论义记": "https://cbeta.buddhism.org.hk/xml/T44/T44n1846_001.xml", "十二门论宗致义记": "https://cbeta.buddhism.org.hk/xml/T42/T42n1826_001.xml"}','["译师"]','《宋高僧传》卷五·法藏传 (CBETA T50n2061)；《法藏和尚传》(CBETA T50n2054)',1,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(6,'person_004','澄观',NULL,NULL,'Chengguan',NULL,'["清凉国师", "清凉大师", "大统国师"]','华严四祖·集大成者','patriarch',738,839,'唐','华严宗四祖。越州山阴人。历学律、禅、三论、天台、华严诸宗。著《华严经疏》六十卷、《演义钞》九十卷，为华严教学集大成者。历七帝之师。德宗赐号''清凉''。','华严五祖',4,'["华严经疏（华严大疏）", "华严经随疏演义钞", "华严法界玄镜", "三圣圆融观门"]','{"华严经疏（华严大疏）": "https://cbeta.buddhism.org.hk/xml/T35/T35n1735_001.xml", "华严经随疏演义钞": "https://cbeta.buddhism.org.hk/xml/T36/T36n1736_001.xml", "华严法界玄镜": "https://cbeta.buddhism.org.hk/xml/T45/T45n1883_001.xml", "三圣圆融观门": "https://cbeta.buddhism.org.hk/xml/T45/T45n1882_001.xml"}',NULL,'《宋高僧传》卷五·澄观传 (CBETA T50n2061)；《佛祖统纪》卷二十九',1,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(7,'person_005','宗密',NULL,NULL,'Zongmi',NULL,'["圭峰大师", "定慧禅师"]','华严五祖·禅教融合者','patriarch',780,841,'唐','华严宗五祖。果州西充人。初习儒学，后从遂州道圆禅师出家（禅宗荷泽系）。后遇澄观受学华严。融合禅教，著《禅源诸诠集都序》《华严原人论》。','华严五祖',5,'["注华严法界观门", "禅源诸诠集都序", "圆觉经大疏释义钞", "华严原人论", "华严经行愿品疏钞"]','{"注华严法界观门": "https://cbeta.buddhism.org.hk/xml/T45/T45n1884_001.xml", "禅源诸诠集都序": "https://cbeta.buddhism.org.hk/xml/T48/T48n2015_001.xml", "圆觉经大疏释义钞": "https://cbeta.buddhism.org.hk/xml/X09/X09n0245_001.xml", "华严原人论": "https://cbeta.buddhism.org.hk/xml/T45/T45n1886_001.xml", "华严经行愿品疏钞": "https://cbeta.buddhism.org.hk/xml/X05/X05n0229_001.xml"}',NULL,'《宋高僧传》卷六·宗密传 (CBETA T50n2061)',1,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(8,'person_006','佛驮跋陀罗',NULL,'Buddhabhadra','Buddhabhadra',NULL,'["觉贤", "佛度跋陀罗"]','六十华严译者','translator',359,429,'东晋','北天竺迦毗罗卫国人。来华译经大师，于建康道场寺译出《六十华严》（旧华严），共七处八会三十四品。还译《大般泥洹经》等。',NULL,NULL,'["大方广佛华严经（六十华严，T09n0278）"]',NULL,NULL,'《高僧传》卷二',1,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(9,'person_007','实叉难陀',NULL,'Śikṣānanda','Śikṣānanda',NULL,'["学喜", "施乞叉难陀"]','八十华严译者','translator',652,710,'唐','于阗国（今新疆和田）人。奉武则天命来华，主译八十卷《华严经》（T10n0279），法藏曾参与其译场证义。还译《大乘入楞伽经》《大方广普贤所说经》（T0847）等。',NULL,NULL,'["大方广佛华严经（八十华严，T10n0279）", "大方广普贤所说经（T0847）"]',NULL,NULL,'《宋高僧传》卷二',1,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(10,'person_007b','支娄迦谶',NULL,'Lokakṣema','Lokaksema',NULL,'["支谶"]','最早汉译华严经文者','translator',NULL,NULL,'后汉','月氏国人。后汉桓帝时来华。译出《佛说兜沙经》（T10n0280），为《华严经》中最早被翻译过来的单行经（对应《如来名号品》）。',NULL,NULL,'["佛说兜沙经（T10n0280）"]',NULL,NULL,'《高僧传》卷一',1,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(11,'person_008','般若',NULL,'Prajñā','Prajñā',NULL,'["般若三藏"]','四十华严译者','translator',NULL,NULL,'唐','罽宾国（今克什米尔）人。唐贞元年间来华，译出《四十华严》（T10n0293），即全本《入法界品》。文末《普贤菩萨行愿赞》为藏汉佛教共同尊奉。',NULL,NULL,'["大方广佛华严经（四十华严，T10n0293）"]',NULL,NULL,'《宋高僧传》卷三',1,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(12,'person_009','李通玄',NULL,NULL,'Li Tongxuan',NULL,'["枣柏大师", "李长者", "显首"]','华严居士学者','scholar',635,730,'唐','唐代华严学重要在家学者。深通儒释，专精《华严》，于方山著《新华严经论》四十卷。以《易经》融会华严，方法独树一帜。','李通玄系',1,'["新华严经论", "华严经决疑论"]','{"新华严经论": "https://cbeta.buddhism.org.hk/xml/T36/T36n1739_001.xml", "华严经决疑论": "https://cbeta.buddhism.org.hk/xml/T36/T36n1741_001.xml"}',NULL,'《宋高僧传》卷二十二·李通玄传 (CBETA T50n2061)',1,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(13,'person_010','义天',NULL,NULL,'Uicheon',NULL,'["大觉国师", "义天僧统"]','高丽华严初祖','scholar',1055,1101,'宋','高丽文宗第四子。入宋求法于杭州慧因寺，从净源法师受华严教法。回国后编《新编诸宗教藏总录》（义天录），为华严文献学的奠基性著作。','高丽华严',1,'["新编诸宗教藏总录（义天录）", "圆宗文类"]',NULL,NULL,'《高丽史》卷九十',1,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(14,'person_011','净源',NULL,NULL,'Jingyuan',NULL,'["晋水净源"]','宋代华严中兴之祖','patriarch',1011,1088,'宋','宋代华严宗重要复兴者。住杭州慧因寺。传法于高丽义天，义天归国后送金书《华严经》三种译本供养慧因寺。慧因寺世称''华严第一道场''。','华严五祖',NULL,'["华严经疏注", "华严妄尽还源观疏"]',NULL,NULL,'《佛祖统纪》卷二十九',1,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(15,'person_012','月霞',NULL,NULL,'Yuexia',NULL,'["月霞长老"]','近现代华严复兴先驱','patriarch',1858,1917,'清','清末民初华严宗复兴的关键人物。于常熟兴福寺创立华严大学（1914年），为中国近代第一所华严专宗教育机构，培养了一批现代华严学僧。','月霞系',1,NULL,NULL,NULL,'于凌波《中国近现代佛教人物志》〈华严宗卷·释月霞传〉',1,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(16,'person_013','常惺',NULL,NULL,'Changxing',NULL,NULL,'','patriarch',1896,1939,'近现代','月霞长老弟子。继月霞之后主持华严大学，于北京、上海等地弘传华严。曾任闽南佛学院院长。','月霞系',2,NULL,NULL,NULL,'于凌波《中国近现代佛教人物志》、东初《中国佛教近代史》',1,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(17,'person_014','慈舟',NULL,NULL,'Cizhou',NULL,NULL,'','scholar',1877,1958,'近现代','近代华严学者。长期于北京广济寺、济南等地讲说华严。著《华严经普贤行愿品亲闻记》，对《普贤行愿品》在现代的弘扬有重要推动。','慈舟系',1,'["华严经普贤行愿品亲闻记"]',NULL,NULL,'道源《慈舟大师传》（1877-1958）',1,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(18,'person_015','南亭',NULL,NULL,'Nanting',NULL,NULL,'华严莲社第二任住持','patriarch',1900,1982,'近现代','智光法师弟子。1952年与师智光共创台北华严莲社，任第二任住持。长期弘传华严教观，为台湾华严宗发展奠基人。','华严莲社',2,NULL,NULL,NULL,'华严莲社社志/官网〔存疑：机构史料，含谱系自述〕',0,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(19,'person_016','成一',NULL,NULL,'Chengyi',NULL,'["乘一", "觉因"]','华严莲社第三任住持·华严专宗学院创办人','patriarch',1914,2011,'当代','江苏泰县人。15岁出家。1949年赴台，协助师祖南亭和尚创办华严莲社，1972年继任住持。1975年创办华严专宗学院，以''专修、专研、专弘华严''为宗旨。1985年创立美国华严莲社。著有多部华严学著作。1988年后恢复泰州光孝寺等大陆祖庭。','华严莲社',3,'["成一和尚著作集"]',NULL,NULL,'华严莲社社志/官网〔存疑：机构史料，含谱系自述〕',0,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(20,'person_017','贤度',NULL,NULL,'Xiandu',NULL,NULL,'华严莲社第六任住持·华严专宗学院院长','patriarch',1960,NULL,'当代','当代华严宗女性法嗣传承者。成一法师弟子。2005年获印度德里大学哲学博士。推动华严现代化转型：发行《华严乐坛》专辑、AI多媒体文创演绎五十三参。著有《华严学讲义》《华严净土思想与念佛法门》等。','华严莲社',6,'["华严学讲义", "华严净土思想与念佛法门", "大海的印迹：贤度法师传"]',NULL,NULL,'华严莲社社志/官网〔存疑：机构史料，含谱系自述〕',0,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(21,'person_018','智光',NULL,NULL,'Zhiguang',NULL,NULL,'华严莲社首任住持','patriarch',1889,1963,'近现代','近代华严学者。台北华严莲社第一任住持（1952年创社），开启台湾华严宗弘传事业。','智光系',1,NULL,NULL,NULL,'范观澜《江淮名剎泰州光孝寺》〈当代僧皇——智光大師〉',1,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(22,'person_019','梦参',NULL,NULL,'Mengcan',NULL,'["梦参老和尚"]','当代华严弘扬巨擘','practitioner',1915,2017,'当代','当代高僧，临济宗第四十六代。曾于五台山闭关修行多年。晚年大力弘扬《华严经》，讲说全本《八十华严》影响深远。1991年破例为海云继梦剃度（梦中得地藏菩萨示现），赐法名昌一。','临济宗',46,'["华严经讲记（全本）"]',NULL,NULL,'《梦参老和尚_综合深度研究》(docs/，信源分级+〔存疑〕标注)',1,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(23,'person_020','胜友',NULL,'Jinamitra','Jinamitra',NULL,NULL,'藏译华严经主译之一','translator',NULL,NULL,'唐','印度译师。与智军（Ye shes sde）、遍照护（Vairocana）约9世纪初将《华严经》译为藏文（德格版Toh 44）。译自中亚于阗原本。',NULL,NULL,'["藏译华严经（Toh 44）"]',NULL,NULL,'藏译《大方广佛华严经》题记（印度胜友、天王菩提、吐蕃智军共译，遍照护复校，据灵隐寺『学处｜除了三大译本〈华严经〉还有哪些版本』2023、《华严经》藏译著录）、德格版甘珠尔目录、《布顿佛教史》、84000 Toh116 引言共译者',1,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(24,'person_020b','智军','Ye shes sde','Jñānasena','Yeshe De',NULL,NULL,'藏译华严经主译之一','translator',NULL,NULL,'唐','吐蕃著名译师。与印度胜友合作将《华严经》从于阗本译为藏文。为吐蕃王朝佛教翻译事业的核心人物。',NULL,NULL,'["藏译华严经（Toh 44）"]',NULL,NULL,'84000 译注 Toh116（引言主译）、Rhaldi《吐蕃后期的佛教翻译》论文, Bulletin of Tibetology 38 (2002)',1,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(25,'person_021','高原明昱',NULL,NULL,'Gaoyuan Mingyu',NULL,NULL,'华严宗第二十五世','patriarch',NULL,NULL,'明','明代华严宗祖师，华严宗第二十五世传人。自他起华严法脉兼传慈恩宗（唯识/法相宗），开创''贤首兼慈恩''传承体系。钦因长老等现代传人皆属此高原法系。','华严五祖',25,'["相宗八要解", "明昱诗集"]',NULL,NULL,'周叔迦《中国佛学史》（1930辅仁讲义）及《贤首宗付法师资记》著录高原法系创立（据中华典藏录）；存世著作《相宗八要解》《明昱诗集》（金陵刻经处光绪二十八年刻本等）；明末高僧，生卒不详〔待补〕',1,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(26,'person_031','应慈',NULL,NULL,'Yingci',NULL,'["应慈法师", "华严座主"]','近代华严座主','patriarch',1873,1965,'近现代','月霞长老师弟。继承月霞遗志，长期在上海等地弘传华严，被尊为''华严座主''。真禅法师之师。平生讲《华严经》多遍。','月霞系',NULL,NULL,NULL,NULL,'于凌波《中国近现代佛教人物志》〈华严座主释应慈〉',1,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(27,'person_032','了中',NULL,NULL,'Liaozhong',NULL,NULL,'华严莲社第四任住持','patriarch',1932,2022,'当代','华严莲社第四任住持。延续''专研、专修、专弘''华严的莲社传统。','华严莲社',4,NULL,NULL,NULL,'华严莲社社志/官网〔存疑：机构史料，含谱系自述〕',0,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(28,'person_033','净海',NULL,NULL,'Jinghai',NULL,NULL,'华严莲社第五任住持','patriarch',NULL,NULL,'当代','华严莲社第五任住持（华严莲社创社七十周年特刊历任住持表确认）。著有《南传佛教史》（法鼓文化 2014）、《印尼、马来西亚、新加坡、菲律宾四国佛教史》等。','华严莲社',5,'["南传佛教史"]',NULL,NULL,'华严莲社社志/官网〔存疑：机构史料，含谱系自述〕',0,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(29,'person_034','明度',NULL,NULL,'Mingdu',NULL,NULL,'华严莲社第七任住持','patriarch',NULL,NULL,'当代','贤度法师之后，续掌华严莲社。贤首宗''明众生本际，悟诸佛果源''演字辈之一。','华严莲社',7,NULL,NULL,NULL,'华严莲社社志/官网〔存疑：机构史料，含谱系自述〕',0,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(30,'person_041','钦因',NULL,NULL,'Qinyin',NULL,'["敬缘钦因祖师"]','贤首宗第四十一世·高原法系第十七世','patriarch',1928,NULL,'当代','台湾树林福慧寺住持。法名敬缘、号钦因，1928年生于北平（俗姓阎）。贤首宗高原法系第四十一世/第十七世传人。2008年8月30日将华严宗（贤首兼慈恩）衣钵传予海云继梦（第四十二世·高原法系第十八世）。另传法嗣予大慧法师、果峻法师、净严法师、宏慧法师等。演字：''明众生本际，悟诸佛果源''。','贤首宗高原法系',41,NULL,NULL,NULL,'大华严寺〈钦因老和上略传〉（huayenworld.org 2021，法名敬缘号钦因、1928年北平生、俗姓阎）、福慧寺〈历代祖师〉、《贤首宗付法师资记》（大华严寺 2008，2008年传法海云继梦），诸源一致',1,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(31,'person_042','海云继梦',NULL,NULL,'Haiyun Jimeng',NULL,'["昌一", "继梦"]','三脉汇一的当代华严传承者·大华严寺导师','patriarch',1950,NULL,'当代','俗名陈鹤山，台湾宜兰人。中兴大学经济系毕业。1991年于梦参长老座下出家（临济宗第四十七代，法名昌一，号继梦）。2008年受钦因长老传华严宗衣钵（贤首宗第四十二世）。同年得印度胜师子王菩萨传大乘瑜伽行法。汇三脉归一，开创''普贤乘华严宗''，复兴失传八百余年的''东山法门''。现为南投大华严寺导师。建立''无尽藏灯''传灯体系，分四个阶位下传法脉。','普贤乘华严宗',NULL,NULL,NULL,'["临济宗"]','大华严寺法脉资料（2024年）〔存疑："三脉汇一"等谱系为教界自述，未见独立史料佐证〕',0,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(32,'person_043','体佛',NULL,NULL,'Tifo',NULL,NULL,'贤首禅苑','patriarch',NULL,NULL,'当代','钦因长老法嗣之一。创立贤首禅苑，弘扬华严禅法。','贤首宗高原法系',NULL,NULL,NULL,NULL,'电视弘法节目、道场官方网页〔待核：未见成卷传记文献〕',0,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(33,'person_044','真禅',NULL,NULL,'Zhenchan',NULL,NULL,'大陆当代华严禅实践者','patriarch',1916,1995,'当代','当代大陆弘扬华严的代表性高僧。''禅宗临济、教在华严、行归地藏普贤''。师承应慈法师。1980年代后在玉佛寺多次主持华严佛七法会，宣讲《普贤行愿品》《十地品》。著有《玉佛丈室集》十集。','临济宗',NULL,'["玉佛丈室集"]',NULL,'["临济宗"]','真禅自著《玉佛丈室集》(十册)',1,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(34,'person_045','如孝',NULL,NULL,'Ruxiao',NULL,NULL,'华严宗第四十一世法脉传人','scholar',NULL,NULL,'当代','当代华严思想学者。师承星云长老、传印长老、法映长老。十余年研究华严思想当代实践。提出''别教一乘三类体系''''法界十门体系''''八纲体系''等。著有《生命的艺术》《修行的艺术》等丛书。2024年在《三秦宗教》刊发论文。','华严宗',41,'["生命的艺术", "修行的艺术"]',NULL,NULL,'凤凰网佛教（2024年）〔存疑：媒体转述，待一手史料〕',0,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(35,'person_046','雪窦',NULL,NULL,'Xuedou',NULL,NULL,'美国华严莲社','scholar',NULL,NULL,'当代','美国华严莲社相关人员，推动华严教法在海外英语世界的传播。',NULL,NULL,NULL,NULL,NULL,'华严莲社美国分会传承记录〔待考：查无此人，疑与雪窦寺混淆〕',0,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(36,'person_050','审祥',NULL,NULL,'Shinshō',NULL,NULL,'日本华严宗初传','patriarch',NULL,742,'唐/日本','新罗僧。来华从法藏学华严。后赴日本，于东大寺宣讲《华严经》，为日本华严宗之初传。','日本华严',1,NULL,NULL,NULL,'《东大寺要录》；《续日本纪》〔天平十二年(740)于金钟道场开讲《六十华严》〕',1,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(37,'person_060','元晓',NULL,NULL,'Wonhyo',NULL,NULL,'新罗华严学僧','scholar',617,686,'唐/新罗','新罗学僧。与义湘同代，二人曾结伴入唐但中途折返。后自悟大乘起信论奥义。著华严经疏、起信论疏，与法藏、慧远并称东亚起信论三大疏。对朝鲜半岛华严思想影响深远。','高丽华严',NULL,'["华严经疏", "大乘起信论疏", "十门和诤论"]',NULL,NULL,'《宋高僧传》卷四·元晓传 (CBETA T50n2061)',1,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(38,'person_061','义湘',NULL,NULL,'Uisang',NULL,NULL,'海东华严初祖','patriarch',625,702,'唐/新罗','新罗僧。与元晓结伴入唐求法，元晓中途折返，义湘独至长安从智俨学华严。归国后创浮石寺，被尊为海东华严初祖。','高丽华严',NULL,'["华严一乘法界图", "白花道场发愿文"]',NULL,NULL,'《宋高僧传》卷四·义湘传 (CBETA T50n2061)',1,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(39,'person_062','均如',NULL,NULL,'Kyunyŏ',NULL,NULL,'高丽华严学僧','scholar',923,973,'高丽','高丽初期华严学僧。统一高丽华严南北二宗之分歧。著华严经三宝章圆通钞等。早于义天，为高丽华严之前驱。','高丽华严',NULL,'["华严经三宝章圆通钞", "十句章圆通记"]',NULL,NULL,'《均如传》〔赫连挺辑〕；《三国遗事》卷五',1,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(40,'person_070','慧苑',NULL,NULL,'Huiyuan',NULL,NULL,'法藏弟子·华严异解者','scholar',673,743,'唐','法藏上首弟子。著续华严经略疏刊定记，改五教为四教、以十门代十玄。澄观在华严经疏中系统批判其说。慧苑异解是推动澄观集大成的关键思想动力。','华严五祖',NULL,'["续华严经略疏刊定记", "华严旋澓章"]',NULL,NULL,'《宋高僧传》卷六·慧苑传 (CBETA T50n2061)；《开元释教录》卷九；《贞元新定释教目录》卷十四',1,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(41,'person_080','续法',NULL,NULL,'Xufa',NULL,NULL,'清代华严集大成者','patriarch',1641,1728,'清','清代华严宗最重要弘传者。字柏亭，号灌顶，仁和人。著贤首五教仪系统整理法藏判教；编华严宗佛祖传梳理传承谱系。讲华严经二十余遍，为清代华严学集大成者。','华严五祖',NULL,'["贤首五教仪", "华严宗佛祖传", "法界宗莲花章"]',NULL,NULL,'清代佛教史料〔续法自著《贤首五教仪》〕+贤首宗资料(〔存疑〕待核一手传记) ',0,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(42,'person_090','慧光',NULL,NULL,'Huiguang',NULL,NULL,'地论师南道派始祖','scholar',468,537,'北魏','北魏地论师。从勒那摩提学十地经论，开创地论南道派。世称光统律师。其学说经数代传承至智俨、法藏，是为华严宗义学前身。','华严五祖',NULL,'["十地经论疏", "四分律疏"]',NULL,NULL,'《续高僧传》卷二十一·慧光传 (CBETA T50n2060)',1,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(43,'person_091','子璿',NULL,NULL,'Zixuan',NULL,NULL,'宋代华严学者','scholar',965,1038,'宋','宋代华严重要学者。长水子璿，秀州人。从洪敏学楞严，后谒慧觉禅师悟入。著起信论疏笔削记，兼弘贤首与天台。','华严五祖',NULL,'["起信论疏笔削记", "楞严经义疏注经"]',NULL,NULL,'《佛祖统纪》卷二十九〔宋代华严传承〕(〔存疑〕具体卷次待核) ',0,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(44,'person_092','持松',NULL,NULL,'Chisong',NULL,NULL,'月霞系法嗣·华严大学校长','patriarch',1894,1972,'近现代','月霞长老弟子。继常惺之后任华严大学校长。兼弘密法，为近代华严与密教兼通的代表人物。著有贤密教衡等。','月霞系',NULL,'["贤密教衡", "华严宗教义始末记"]',NULL,NULL,'《持松法师传记》等教界史料；自著《密教通关》(〔存疑〕待核对) ',0,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(45,'person_100','释迦牟尼',NULL,'Śākyamuni','Shakyamuni',NULL,NULL,'佛教创始人·华严经教说者','patriarch',-563,-483,'古印度','佛教创始人。据华严宗传统，华严经为释迦成道后最初三七日于菩提树下为法身大士所说。为一切法脉之根源。','印度源流',NULL,NULL,NULL,NULL,'《长阿含经》(CBETA T1n0001)；《佛本行集经》(CBETA T190)',1,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(46,'person_101','马鸣',NULL,'Aśvaghoṣa','Ashvaghosha',NULL,NULL,'大乘论师·起信论造者','scholar',80,150,'古印度','古印度大乘佛教论师。传统著录为大乘起信论作者。该论一心二门三大四信五门之说，为华严宗判教与心性论提供了重要理论资源。','印度源流',NULL,'["大乘起信论"]',NULL,NULL,'《付法藏因缘传》(CBETA T50n2058)；《马鸣菩萨传》(CBETA T50n2046)',1,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(47,'person_102','无著',NULL,'Asaṅga','Asanga',NULL,NULL,'瑜伽行派创始人','scholar',310,390,'古印度','古印度瑜伽行派(Yogācāra)创始人。世亲之兄。其唯识学说经世亲十地经论传入汉地，深刻影响地论学派及华严宗法界缘起思想的形成。','印度源流',NULL,'["瑜伽师地论", "摄大乘论"]',NULL,NULL,'学术〔玄奘《大唐西域记》卷五·摩揭陀国及多罗那他《印度佛教史》〕(T2)',1,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(48,'person_103','鸠摩罗什',NULL,'Kumārajīva','Kumarajiva',NULL,NULL,'四大译经师之首','translator',344,413,'后秦','龟兹人。后秦弘始三年(401)至长安，主持中国历史上规模最大的译场。译十住经(T0286,即十地品别译)、十住毗婆沙论、法华经等。其译经为华严学在中国的传播提供了关键文本基础。','译师',NULL,'["十住经", "十住毗婆沙论", "中论", "法华经"]',NULL,NULL,'《高僧传》卷二·鸠摩罗什传 (CBETA T50n2059)',1,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(49,'person_104','菩提流支',NULL,'Bodhiruci','Bodhiruci',NULL,NULL,'十地经论主译','translator',NULL,527,'北魏','北印度人。北魏永平元年(508)至洛阳，与勒那摩提等译世亲十地经论十二卷。此论译出直接催生了南北朝地论学派，被视为华严宗义学之远源。','译师',NULL,'["十地经论"]',NULL,NULL,'《续高僧传》卷一·菩提流支传 (CBETA T50n2060)',1,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(50,'person_105','燃灯佛',NULL,'Dīpaṃkara','Dipankara',NULL,NULL,'授记释迦成佛之过去佛','patriarch',NULL,NULL,'远古印度','梵名Dīpaṃkara。过去无量劫前之佛。据华严经如来名号品及本生经典，燃灯佛曾为释迦牟尼前身授记: 汝于来世当得作佛号释迦牟尼。此为华严经中佛佛相续无尽法界缘起之始。','印度源流',NULL,NULL,NULL,NULL,'《佛说太子瑞应本起经》(CBETA T185)〔燃灯授记〕',1,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(51,'person_106','迦叶佛',NULL,'Kāśyapa','Kashyapa',NULL,NULL,'贤劫第三佛·释迦前身之师','patriarch',NULL,NULL,'远古印度','梵名Kāśyapa。贤劫千佛之第三尊，释迦牟尼佛之前一佛。据华严经，释迦成道时十方诸佛各遣菩萨来集，其中包括过去诸佛之法身显现。华严宗以十方三世无尽诸佛构成法界缘起之佛佛相望网络。','印度源流',NULL,NULL,NULL,NULL,'《长阿含经》卷一·大本经 (CBETA T1n0001)〔七佛传承〕',1,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(52,'person_107','毗卢遮那佛',NULL,'Vairocana','Vairocana',NULL,NULL,'华严教主·法身本源','patriarch',NULL,NULL,'法身常住','梵名Vairocana，华严经之根本教主。意译光明遍照、大日如来。华严经以毗卢遮那佛法身为宇宙本体，十方三世一切诸佛皆为其化现。华严宗法界缘起、一即一切等核心教义皆围绕毗卢遮那佛法身展开。非历史人物，为华严教义之法身源头。','印度源流',NULL,NULL,NULL,NULL,'《大方广佛华严经》〈世主妙严品〉主尊（卢舍那/毗卢遮那）(CBETA T279/D80)',1,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(53,'person_110','法显',NULL,NULL,'Faxian',NULL,NULL,'西行求法先驱','practitioner',337,422,'东晋','东晋高僧。399年以65岁高龄从长安出发,经河西走廊、西域、中亚至印度,历时14年游历30余国。412年海路归国。著《佛国记》记录印度佛教圣迹,为中国首位完成印度求法之旅的僧人。','求法僧',NULL,'["佛国记(高僧法显传)"]',NULL,NULL,'《高僧传》卷三·法显传',1,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(54,'person_111','玄奘',NULL,NULL,'Xuanzang',NULL,NULL,'大翻译家·法相宗创始人','translator',602,664,'唐','唐代高僧。629年从长安西行,经西域中亚至印度那烂陀寺,师从戒贤。645年归国携657部梵本,主持译场译经75部1335卷。著《大唐西域记》,创中国法相唯识宗。','求法僧',NULL,'["大唐西域记", "大般若经", "成唯识论"]',NULL,NULL,'《续高僧传》卷四·玄奘传 /《大唐大慈恩寺三藏法师传》',1,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(55,'person_112','义净',NULL,NULL,'Yijing',NULL,NULL,'海上求法僧·译经家','translator',635,713,'唐','唐代高僧。671年从广州乘波斯船经海路至印度,游历那烂陀寺等30余国。695年归国携梵本400余部,译经56部230卷,偏重律藏。著《南海寄归内法传》《大唐西域求法高僧传》。与法显、玄奘并称三大求法僧。','求法僧',NULL,'["南海寄归内法传", "大唐西域求法高僧传"]',NULL,NULL,'《宋高僧传》卷一·义净传',1,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(56,'person_113','真谛',NULL,'Paramārtha','Paramartha',NULL,NULL,'四大译经师之一','translator',499,569,'梁/陈','西印度优禅尼国人。梁大同十二年(546)来华,值梁末战乱辗转各地译经。译《摄大乘论》《俱舍论》等64部278卷,系统传译瑜伽行派唯识学。与鸠摩罗什、玄奘、义净并称四大译经师。','译师',NULL,'["摄大乘论", "俱舍论", "大乘起信论(重译)"]',NULL,NULL,'《续高僧传》卷一·真谛传',1,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(57,'person_114','求那跋陀罗',NULL,'Guṇabhadra','Gunabhadra',NULL,NULL,'楞伽经主译','translator',394,468,'刘宋','中印度人。刘宋元嘉十二年(435)经海路至广州,后至建康译经。译《楞伽经》《胜鬘经》《杂阿含经》等52部134卷。其楞伽译本后为禅宗初祖达摩授与二祖慧可,影响禅宗思想深远,亦与华严如来藏思想有深层义学会通。','译师',NULL,'["楞伽阿跋多罗宝经", "胜鬘经", "杂阿含经"]',NULL,NULL,'《高僧传》卷三·求那跋陀罗传',1,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(58,'person_115','不空',NULL,'Amoghavajra','Amoghavajra',NULL,NULL,'密宗开元三大士之一','translator',705,774,'唐','师子国(斯里兰卡)人,一说北印度人。幼来华师事金刚智。741年赴师子国和印度求法,746年归国携梵本500余部。译《金刚顶经》等密教经典,与善无畏、金刚智并称开元三大士。华严宗密法(秽迹金刚)与此传承有历史关联。','译师',NULL,'["金刚顶经", "大乘密严经"]',NULL,NULL,'《宋高僧传》卷一·不空传',1,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(59,'person_116','竺法护',NULL,'Dharmarakṣa','Dharmaraksa',NULL,NULL,'敦煌菩萨·大译经家','translator',239,316,'西晋','月氏侨民,世居敦煌。随师游历西域诸国,通晓36国语言。译经149部,包括华严经中《渐备一切智德经》(十地品异译)、《等目菩萨三昧经》(十定品异译)、《如来兴显经》(如来出现品异译)等多部华严单行经。被尊为''敦煌菩萨''。','译师',NULL,'["渐备一切智德经", "如来兴显经", "正法华经"]',NULL,NULL,'《高僧传》卷一·竺法护传',1,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(60,'person_117','慧超',NULL,'Prajñāvikrama','Hyecho',NULL,NULL,'新罗求法僧','practitioner',704,787,'唐/新罗','新罗僧。约723年从中国出发经海路至印度,游历五天竺佛教圣迹。727年归国后著《往五天竺国传》记录印度、中亚、西域见闻。该书敦煌残卷于1908年为伯希和发现,为研究8世纪中亚印度的珍贵一手文献。','求法僧',NULL,'["往五天竺国传"]',NULL,NULL,'《往五天竺国传》敦煌写本 / 学术研究',1,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(61,'person_120','善无畏',NULL,'Śubhakarasiṃha','Subhakarasimha',NULL,NULL,'开元三大士之首·密宗初传','translator',637,735,'唐','中印度人,甘露王后裔。716年至长安,玄宗礼为国师。译《大日经》七卷,传胎藏界密法。与金刚智、不空并称开元三大士,为中国密宗奠基人。弟子一行协助译经并著《大日经疏》。','译师',NULL,'["大日经(大毗卢遮那成佛神变加持经)", "苏婆呼童子请问经"]',NULL,NULL,'《宋高僧传》卷二·善无畏传',1,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(62,'person_121','金刚智',NULL,'Vajrabodhi','Vajrabodhi',NULL,NULL,'开元三大士·金刚界密法','translator',671,741,'唐','南印度摩赖耶国人。719年经海路至广州,次年抵长安。译《金刚顶经》传金刚界密法。与善无畏、不空并称开元三大士。弟子不空继承其法脉,后传入日本成真言宗。','译师',NULL,'["金刚顶瑜伽中略出念诵经", "七俱胝佛母准提大明陀罗尼经"]',NULL,NULL,'《宋高僧传》卷一·金刚智传',1,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(63,'person_122','一行',NULL,NULL,'Yixing',NULL,NULL,'天文学家·密宗学僧','scholar',683,727,'唐','唐代高僧,俗名张遂。精通天文历算,制《大衍历》。师事善无畏,协助译《大日经》并著《大日经疏》二十卷,为密宗义学之奠基著作。一行亦曾参学禅宗北宗普寂。','译师',NULL,'["大日经疏", "大衍历"]',NULL,NULL,'《宋高僧传》卷五·一行传',1,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(64,'person_123','慧果',NULL,NULL,'Huiguo',NULL,NULL,'密宗第七祖·青龙寺','patriarch',746,805,'唐','唐代密宗高僧。师事不空,兼承善无畏胎藏界与金刚智金刚界两部密法。住长安青龙寺,为密宗集大成者。日本空海入唐即从慧果受法,归国后创立日本真言宗。','译师',NULL,NULL,NULL,NULL,'《宋高僧传》·慧果传 / 空海《御请来目录》',1,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(65,'person_124','空海',NULL,NULL,'Kūkai','Kūkai',NULL,'日本真言宗开祖·弘法大师','patriarch',774,835,'唐/日本','日本真言宗开祖。804年入唐,于长安青龙寺从慧果受两部密法。806年归国后于高野山开创真言宗。著《十住心论》以华严判教框架判摄显密诸宗,体现密教与华严义学之深层对话。','日本华严',NULL,'["十住心论", "即身成佛义", "秘密曼荼罗十住心论"]',NULL,NULL,'空海《御请来目录》/ 日本佛教史',1,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(66,'person_125','六师外道',NULL,NULL,'Six heterodox teachers',NULL,NULL,'佛陀时代非佛教思想家','scholar',NULL,NULL,'古印度','与释迦牟尼同时代的六位印度思想家。据《沙门果经》记载:富兰那迦叶(道德否定论)、末伽梨拘舍罗(宿命论)、散若夷毗罗梨子(不可知论)、阿耆多翅舍钦婆罗(唯物论)、迦罗鸠驮迦旃延(原子论)、尼乾陀若提子(耆那教创始人)。佛教教义正是在与这些学派的对话与辩驳中确立的。','印度源流',NULL,NULL,NULL,NULL,'《长阿含经·沙门果经》(DN 2)',1,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(67,'person_126','成观法师',NULL,NULL,'Cheng Guan',NULL,NULL,'华严宗42世·真言宗53世阿阇梨·大毘卢寺住持','patriarch',1947,NULL,'当代','台北人,台师大英语系毕业(1972),美国德州TCU英研所深造。1988年于纽约庄严寺依天台宗45代显明老和尚出家,同年于基隆海会寺受三坛大戒。1996年于日本高野山入坛受金胎两部大法,得传法灌顶阿阇梨位,为真言宗53世。2010年4月24日于台北福慧寺依钦因长老受华严兼慈恩法脉,为高原法系贤首宗42世。历任台北大毘卢寺住持(1991年创)、美国遍照寺住持。创「新逍遥园译经院」从事佛典注译与英译。','贤首宗高原法系',NULL,'["楞伽经义贯", "大佛顶首楞严经义贯", "大乘百法明门论今注", "唯识三十论颂义贯"]',NULL,NULL,'大毘卢寺法脉记录、百度百科〔待核：无独立学术文献〕',1,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(68,'person_130','拉克鲁希',NULL,'Lakulīśa','Lakulish',NULL,NULL,'湿婆神第28代化身·Lord Lakulish','patriarch',NULL,NULL,'远古印度','Lord Lakulish。相传为4500年前湿婆神第28代化身,为印度古典瑜伽行法之原始指导者。其传承历经千年,于现代示现指导巴布基大瑜伽士。','大乘瑜伽行法',NULL,NULL,NULL,NULL,'当代瑜伽行传承资料(〔存疑〕当代自述，独立史料稀缺) ',0,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(69,'person_131','巴布基',NULL,NULL,'Babuji',NULL,NULL,'大瑜伽士·Babuji','practitioner',NULL,NULL,'近现代','Babuji(巴布基大瑜伽士)。Lord Lakulish示现指导的大成就者,传承古典瑜伽行法。','大乘瑜伽行法',NULL,NULL,NULL,NULL,'当代瑜伽行传承资料(〔存疑〕当代自述) ',0,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(70,'person_132','普拉梵纳德',NULL,NULL,'Swami Pranavanad',NULL,NULL,'Swami Pranavanad','practitioner',1884,1959,'近现代','Swami Pranavanad。1913年普贤菩萨于印度再度示现,为其传法。开创现代大乘瑜伽行法传承。','大乘瑜伽行法',NULL,NULL,NULL,NULL,'当代瑜伽行传承资料(〔存疑〕当代自述) ',0,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(71,'person_133','克利普梵纳德',NULL,NULL,'Swami Kripalavanand',NULL,NULL,'Swami Kripalavanand','practitioner',1913,1981,'近现代','Swami Kripalavanand。1932年从普拉梵纳德接法,继续弘扬大乘瑜伽行法。','大乘瑜伽行法',NULL,NULL,NULL,NULL,'当代瑜伽行传承资料(〔存疑〕当代自述) ',0,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(72,'person_134','胜师子王菩萨',NULL,NULL,'Swami Rajarshi Muni',NULL,NULL,'Swami Rajarshi Muni·印度国师','practitioner',1931,2023,'当代','Swami Rajarshi Muni(惹查西牟尼)。1971年从克利普梵纳德接法。1993年Lakulish以灵性形象示现,遂创立LIFE Mission。被尊为印度国师,2019年获印度总理奖。2008年12月于阿弥塔巴市传大乘瑜伽行法灌顶予海云继梦。已圆寂(约2023年)。','大乘瑜伽行法',NULL,NULL,NULL,NULL,'大华严寺法脉资料(〔存疑〕教界自述，梦中授法不可独立验证) ',0,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(73,'person_140','罗摩克里希纳',NULL,'Rāmakṛṣṇa','Ramakrishna',NULL,NULL,'Ramakrishna·近代印度灵性复兴之源','practitioner',1836,1886,'1836–1886','Ramakrishna Paramahamsa。19世纪印度神秘主义者,加尔各答达克希涅斯瓦尔 Kali 神庙祭司。主张各宗教皆为通向同一真理的路径。其弟子辨喜将吠檀多传向西方。','参考线',NULL,NULL,NULL,NULL,'The Gospel of Sri Ramakrishna（M. 笔录，原典英译本）(T1)',1,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(74,'person_141','辨喜',NULL,'Vivekānanda','Swami Vivekananda',NULL,NULL,'Swami Vivekananda·吠檀多西传第一人','practitioner',1863,1902,'1863–1902','Swami Vivekananda。罗摩克里希纳弟子。1893年芝加哥世界宗教议会演讲轰动西方,创立罗摩克里希纳传道会。将瑜伽与吠檀多哲学系统介绍给西方世界。','参考线',NULL,NULL,NULL,NULL,'辨喜《演讲与布道全集》自著英语第一手(T1)',1,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(75,'person_142','奥罗宾多',NULL,NULL,'Sri Aurobindo',NULL,NULL,'Sri Aurobindo·整体瑜伽创立者','practitioner',1872,1950,'1872–1950','Sri Aurobindo。早年留学剑桥,后投身印度独立运动。1910年起隐居本地治里,创立整体瑜伽(Integral Yoga)。其「超心智」演化哲学与华严事事无碍有深层对话空间。','参考线',NULL,'["The Life Divine", "Savitri"]',NULL,NULL,'奥罗宾多自著《综合瑜伽》等（第一手自著）(T1)',1,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(76,'person_143','拉玛那·马哈希',NULL,'Ramaṇa Maharṣi','Ramana Maharshi',NULL,NULL,'Ramana Maharshi·参问Who am I','practitioner',1879,1950,'1879–1950','Ramana Maharshi。16岁自发证悟自性,后隐居于圣山 Arunachala 终生。以「我是谁」(Who am I?)参问法门教导学人直证自性。其不二论与禅宗「念佛是谁」话头有可比拟处。','参考线',NULL,NULL,NULL,NULL,'《Talks with Sri Ramana Maharshi》〔弟子笔录〕(T1)',1,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(77,'person_150','寂天',NULL,'Śāntideva','Shantideva',NULL,NULL,'Śāntideva·入菩萨行论造者','scholar',685,763,'8世纪','Śāntideva(寂天)。那烂陀寺学僧,中观学派大师。著《入菩萨行论》(Bodhicaryāvatāra)为印度大乘修行纲领。《华严经·普贤行愿品》与寂天菩萨行思想可互相参照。','参考线',NULL,'["入菩萨行论", "学处集要"]',NULL,NULL,'多罗那他《印度佛教史》〔寂天章〕；自著《入菩萨行论》(T2)',1,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(78,'person_151','阿底峡',NULL,'Atiśa','Atisha',NULL,NULL,'Atiśa·菩提道灯论造者','patriarch',982,1054,'982–1054','Atiśa(阿底峡)。孟加拉人,超戒寺学僧,后应请入藏弘法。著《菩提道灯论》建立三士道次第。噶当派始祖,宗喀巴格鲁派之前身。圆寂于拉萨附近聂塘。','参考线',NULL,'["菩提道灯论"]',NULL,NULL,'《阿底峡尊者传》〔热振寺系统史料·法尊译〕(T2)',1,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(79,'person_152','宗喀巴','tsong kha pa',NULL,'Tsongkhapa',NULL,NULL,'Tsongkhapa·格鲁派创始人','patriarch',1357,1419,'1357–1419','Tsongkhapa(宗喀巴)。青海人,藏传佛教格鲁派(黄教)创始人。著《菩提道次第广论》系统化阿底峡三士道思想。与华严判教体系(小始终顿圆)有修行阶次上的对比研究价值。','参考线',NULL,'["菩提道次第广论", "密宗道次第广论"]',NULL,NULL,'《至尊宗喀巴大师传》〔法尊译〕；克主杰《宗喀巴大师传》(T2)',1,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(80,'person_f01','思元慧三',NULL,NULL,'Huisan',NULL,NULL,'高原法系40世·福慧寺开山','patriarch',1901,1986,'近现代','宛平人，俗姓霍（1901-1986）。北京广善寺第11代住持·1948年赴台，创树林福慧寺（贤首宗/慈恩宗祖庭·唐密秽迹金刚根本道场）。民国37年来台时已47岁，随身仅带一尊华严三圣像。为高原法系在台根本道场开创者；后传法敬缘钦因。','贤首宗高原法系',NULL,NULL,NULL,NULL,'贤首宗高原法系宗内资料(〔存疑〕谱系自述) ',0,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(81,'person_f02','体化性果',NULL,NULL,'Tihua',NULL,NULL,'福慧寺第三代住持','patriarch',1950,NULL,'当代','钦因长老法嗣。福慧寺第三代住持。继承贤首宗高原法系在台弘法事业。','贤首宗高原法系',NULL,NULL,NULL,NULL,'贤首宗高原法系宗内资料(〔存疑〕谱系自述) ',0,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(82,'person_j01','良弁',NULL,NULL,'Rōben',NULL,NULL,'东大寺初代别当','patriarch',689,774,'唐/日本','审祥弟子。东大寺开山。主持《华严经》讲说。','日本华严',NULL,NULL,NULL,NULL,'《东大寺要录》〔奏请审祥开讲《华严经》；东大寺初代别当〕',1,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(83,'person_j02','实忠',NULL,NULL,'Jitchū',NULL,NULL,'东大寺二代','patriarch',726,800,'日本','良弁弟子。继承东大寺华严教学。','日本华严',NULL,NULL,NULL,NULL,'凝然《三国佛法传通缘起》〔东大寺华严相承〕',1,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(84,'person_j03','等定',NULL,NULL,'Tōjō',NULL,NULL,'东大寺华严','patriarch',800,870,'日本','日本华严宗传承者。','日本华严',NULL,NULL,NULL,NULL,'凝然《三国佛法传通缘起》〔东大寺华严相承〕',1,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(85,'person_j04','圣宝',NULL,NULL,'Shōbō',NULL,NULL,'醍醐寺开山','patriarch',832,909,'日本','理源大师。兼传真言与华严。','日本华严',NULL,NULL,NULL,NULL,'《东大寺要录》；醍醐寺史料〔理源大师圣宝〕',1,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(86,'person_j05','观贤',NULL,NULL,'Kanken',NULL,NULL,'东大寺别当','patriarch',853,925,'日本','东大寺华严教学之中兴。','日本华严',NULL,NULL,NULL,NULL,'凝然《三国佛法传通缘起》〔东大寺华严相承〕',1,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(87,'person_j06','明惠',NULL,NULL,'Myōe',NULL,NULL,'日本华严中兴之祖','patriarch',1173,1232,'日本','日本镰仓时代华严宗中兴之祖。高山寺开山。复兴东大寺华严教学，兼弘戒律与真言。对日本华严宗有再造之功。','日本华严',NULL,'["摧邪轮", "华严缘起"]',NULL,NULL,'《元亨释书》(CBETA B32n0173)·明惠传；《明恵上人伝記》',1,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(88,'person_j07','凝然',NULL,NULL,'Gyōnen',NULL,NULL,'东大寺学僧','scholar',1240,1321,'日本','日本镰仓时代东大寺学僧。著八宗纲要系统介绍中国八宗要义；著华严法界义镜等。为日本华严教学之集大成者。','日本华严',NULL,'["八宗纲要", "华严法界义镜"]',NULL,NULL,'凝然自著《三国佛法传通缘起》（自述华严相承）；《东大寺续要录》',1,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(89,'person_s01','魏道儒',NULL,NULL,'Wei Daoru',NULL,NULL,'中国社科院学部委员','scholar',1955,NULL,'当代','中国社会科学院学部委员、一级研究员、世界宗教研究所研究员。1955年生，河北景县人。著有《中国华严宗通史》（1998初版）、《华严学与禅学》（2011）、《唐宋佛学》（2017）等。','当代学者',NULL,'["中国华严宗通史"]',NULL,NULL,'魏道儒《中国华严宗通史》(江苏古籍2001)；《华严学与禅学》(T2)',1,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(90,'person_s02','王颂',NULL,NULL,'Wang Song',NULL,NULL,'北京大学教授','scholar',1965,NULL,'当代','北京大学哲学系（宗教学系）教授、博导，北京大学佛教研究中心主任。1971年生，日本国际佛教大学院大学博士。尤专华严宗的历史与思想及东亚汉文化圈佛教。著有《宋代华严思想研究》（2008）、《日本佛教》《华严法界观门校释研究》等。','当代学者',NULL,'["宋代华严思想研究"]',NULL,NULL,'王颂《宋代华严思想研究》(宗教文化2008)(T2)',1,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(91,'person_s03','邱高兴',NULL,NULL,'Qiu Gaoxing',NULL,NULL,'中国计量大学教授（曾任吉林大学教授）','scholar',1966,NULL,'当代','中国计量大学人文与外语学院教授、院长（1993-1996于中国人民大学获哲学博士，曾任吉林大学哲学系教授）。华严宗、宗密思想与佛教中国化研究。著有《李通玄佛学思想述评》（2001）、《禅源诸诠集都序》校释（2008）、《大乘玄论译注》（1997）等。','当代学者',NULL,'["李通玄佛学思想述评"]',NULL,NULL,'当代学界〔华严/宗密研究〕(〔存疑〕书目待核) ',0,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(92,'person_s04','张文良',NULL,NULL,'Zhang Wenliang',NULL,NULL,'中国人民大学教授','scholar',1966,NULL,'当代','中国人民大学哲学院教授、佛教与宗教学理论研究所研究员，日本东京大学博士。专研中国佛教与日本佛教，尤专华严学与禅宗、地论宗。著有《澄观华严思想研究》（日文）、《“批判佛教”的批判》、《〈大乘起信论〉思想史研究》、《涅槃学研究》（2024）等。','当代学者',NULL,'["澄观华严思想研究"]',NULL,NULL,'当代学界〔华严学〕(〔存疑〕书目待核) ',0,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(93,'person_x01','虚云',NULL,NULL,'Xuyun',NULL,NULL,'禅宗泰斗·兼祧五宗·近代佛教复兴先驱','patriarch',1840,1959,'清-中华人民共和国','虚云老和尚(1840-1959)，近代禅宗第一高僧。一生兼祧临济、曹洞、沩仰、法眼、云门五宗法脉。修复大小寺院八十余处，晚年驻锡云居山真如禅寺。对《楞严经》《华严经》用功极深，其开示中屡引华严义理。1959年圆寂，世寿120岁。','临济宗',NULL,'["参禅要旨", "虚云老和尚法汇", "禅七开示录"]',NULL,'["曹洞宗", "沩仰宗", "法眼宗", "云门宗"]','《虚云和尚年谱》〔岑学吕辑〕；虚云《参禅要旨》等语录',1,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(94,'person_x02','净慧',NULL,NULL,'Jinghui',NULL,NULL,'生活禅创立者·虚云法嗣·承五宗法脉','practitioner',1933,2013,'中华人民共和国','净慧长老(1933-2013)，虚云老和尚法嗣，中国佛教协会副会长，河北省佛教协会创会会长。1991年提出「生活禅」理念——将修行落实于生活。任《法音》主编20年。创办柏林禅寺、四祖寺、玉泉寺等道场。2013年圆寂。','临济宗',NULL,'["生活禅钥", "入禅之门", "禅在当下"]',NULL,'["曹洞宗", "沩仰宗", "法眼宗", "云门宗"]','净慧《生活禅钥》自述 + 《虚云和尚年谱》(〔存疑〕法系待核) ',0,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "persons" VALUES(95,'person_x03','南怀瑾',NULL,NULL,'Nan Huaijin',NULL,NULL,'国学大师·禅宗大居士·东西文化摆渡者','scholar',1918,2012,'中华人民共和国','南怀瑾(1918-2012)，浙江温州乐清人。少年习武学文，1943年于峨眉山大坪寺闭关阅藏三年。1949年赴台，着力弘扬儒释道传统文化，讲学六十余年不辍。著作等身（《论语别裁》《老子他说》《禅海蠡测》等60余部），屡引华严经义阐释生命科学与认知科学。倡「身心性命之学」，推动儿童读经运动，兴建太湖大','居士',NULL,'["论语别裁", "老子他说", "禅海蠡测"]',NULL,'["临济宗", "曹洞宗"]','南怀瑾《禅海蠡测》等自述(〔存疑〕教界人物自述师承) ',0,'2026-09-27 08:00:19','2026-09-27 08:00:19');
CREATE TABLE texts (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    title_zh        TEXT    NOT NULL,                       -- 中文标题
    title_bo        TEXT,                                   -- 藏文标题 (Wylie)
    title_sa        TEXT,                                   -- 梵文标题 (IAST)
    title_en        TEXT,                                   -- 英文标题
    type            TEXT    NOT NULL DEFAULT 'sutra',
                    -- sutra | vinaya | shastra | commentary | ritual |
                    -- record | study | lecture | collection | catalog
    sub_type        TEXT,                                   -- 华严部 / 般若部 / 涅槃部 ...
    taisho_no       TEXT,                                   -- 大正藏编号 (T0279)
    cbeta_id        TEXT,                                   -- CBETA 内部 ID (T10n0279)
    tohk_no         TEXT,                                   -- 德格版编号 (Toh 44)
    yitian_status   TEXT,                                   -- 义天录: extant|lost|disputed|not_listed
    yitian_ref      TEXT,                                   -- 义天录引用位置
    author_id       INTEGER REFERENCES persons(id),         -- 作者
    translator_id   INTEGER REFERENCES persons(id),         -- 译者
    dynasty         TEXT,                                   -- 成书/翻译朝代
    date_text       TEXT,                                   -- 年份描述 ("约699年")
    date_range      TEXT,                                   -- 年代范围 (如"420-699")
    volumn_count    INTEGER,                                -- 卷数
    chapter_count   INTEGER,                                -- 品数
    structure       TEXT,                                   -- 结构描述 (如"七处九会")
    abstract        TEXT,                                   -- 内容简介
    language        TEXT    DEFAULT 'zh',                   -- 主要语言
    source_url      TEXT,                                   -- 数字化链接
    in_cbeta        INTEGER DEFAULT 1,                      -- 是否在CBETA中
    in_bdrc         INTEGER DEFAULT 0,                      -- 是否在BDRC中
    has_tibetan     INTEGER DEFAULT 0,                      -- 是否有藏译本
    has_sanskrit    INTEGER DEFAULT 0,                      -- 是否有梵文原本/残片
    created_at      TEXT    DEFAULT (datetime('now')),
    updated_at      TEXT    DEFAULT (datetime('now'))
);
INSERT INTO "texts" VALUES(1,'大方广佛华严经（六十华严）',NULL,'Buddhāvataṃsaka-nāma-mahāvaipulya-sūtra','The Avatamsaka Sutra (60-fascicle)','sutra',NULL,'T09n0278','T09n0278',NULL,'not_listed',NULL,NULL,NULL,'东晋','约418-420年',NULL,60,34,'七处八会','最早汉译全本华严。译自支法领从于阗带回的梵本。 三十四品中，《宝王如来性起品》为八十华严之《如来出现品》所替代， 结构亦有调整。六十华严保留了部分更接近早期梵本的表述。
','zh',NULL,1,0,0,1,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "texts" VALUES(2,'大方广佛华严经（八十华严）',NULL,'Buddhāvataṃsaka-nāma-mahāvaipulya-sūtra','The Avatamsaka Sutra (80-fascicle)','sutra',NULL,'T10n0279','T10n0279',NULL,'not_listed',NULL,NULL,NULL,'唐','约695-699年',NULL,80,39,'七处九会','目前汉传佛教最通用的华严经版本。武则天从于阗请来梵本， 诏实叉难陀等于洛阳佛授记寺翻译。法藏参与证义。 三十九品，七处九会结构较六十华严完整。 缺藏译本中的《如来华严品》和《普贤宣说品》。
','zh',NULL,1,0,0,1,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "texts" VALUES(3,'大方广佛华严经（四十华严）',NULL,'Gaṇḍavyūha-sūtra','The Avatamsaka Sutra (40-fascicle) / The Stem Array','sutra',NULL,'T10n0293','T10n0293',NULL,'not_listed',NULL,NULL,NULL,'唐','约796-798年',NULL,40,1,'单品（入法界品全本）','即《入法界品》的单行全本翻译。内容比六十华严和八十华严中的 《入法界品》更完整。文末附《普贤菩萨行愿赞》，为藏汉佛教 共同尊奉的重要修行文献。善财童子五十三参的故事全本在此。
','zh',NULL,1,0,0,1,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "texts" VALUES(4,'佛说兜沙经',NULL,NULL,'The Tusita Sutra','sutra',NULL,'T10n0280',NULL,NULL,'not_listed',NULL,NULL,NULL,'后汉','约167年',NULL,1,NULL,NULL,'《华严经》中最早被翻译为汉文的单行经。 内容对应于八十华严《如来名号品》的一部分。 是最早传入中国的华严系统经典。
','zh',NULL,0,0,0,0,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "texts" VALUES(5,'佛说菩萨本业经',NULL,NULL,'Sutra on the Original Works of Bodhisattvas','sutra',NULL,'T10n0281',NULL,NULL,'not_listed',NULL,NULL,NULL,'吴',NULL,NULL,1,NULL,NULL,'净行品别译，无偈颂部分','zh',NULL,0,0,0,0,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "texts" VALUES(6,'诸菩萨求佛本业经',NULL,NULL,'Sutra on Bodhisattvas Seeking the Buddha''s Original Works','sutra',NULL,'T10n0282',NULL,NULL,'not_listed',NULL,NULL,NULL,'西晋',NULL,NULL,1,NULL,NULL,'净行品别译','zh',NULL,0,0,0,0,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "texts" VALUES(7,'菩萨十住行道品',NULL,NULL,'Chapter on the Practice Path of the Ten Stages for Bodhisattvas','sutra',NULL,'T10n0283',NULL,NULL,'not_listed',NULL,NULL,NULL,'西晋',NULL,NULL,1,NULL,NULL,'菩萨十住品别译','zh',NULL,0,0,0,0,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "texts" VALUES(8,'佛说菩萨十住经',NULL,NULL,'Sutra on the Ten Stages of Bodhisattvas','sutra',NULL,'T10n0284',NULL,NULL,'not_listed',NULL,NULL,NULL,'东晋',NULL,NULL,1,NULL,NULL,'菩萨十住品另一别译','zh',NULL,0,0,0,0,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "texts" VALUES(9,'渐备一切智德经',NULL,NULL,'Gradual Attainment of All-Wisdom Virtue Sutra','sutra',NULL,'T10n0285',NULL,NULL,'not_listed',NULL,NULL,NULL,'西晋','约297年',NULL,5,NULL,NULL,'十地品早期大本别译。竺法护翻译风格古朴','zh',NULL,0,0,0,0,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "texts" VALUES(10,'十住经',NULL,NULL,'The Dashabhumika Sutra (Ten Stages Sutra)','sutra',NULL,'T10n0286',NULL,NULL,'not_listed',NULL,NULL,NULL,'姚秦','约402-412年',NULL,4,NULL,NULL,'十地品的重要别译。鸠摩罗什译本流畅易读。 与《十地经论》（世亲造，菩提流支译）注解对象高度对应。 是研究华严经在印度流传形态的重要依据。
','zh',NULL,0,0,0,0,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "texts" VALUES(11,'佛说十地经',NULL,NULL,'The Buddha Speaks the Dashabhumika Sutra','sutra',NULL,'T10n0287',NULL,NULL,'not_listed',NULL,NULL,NULL,'唐','约785-805年',NULL,9,NULL,NULL,'十地品晚唐别译。篇幅较大（9卷），与鸠摩罗什的4卷本和内典有出入','zh',NULL,0,0,0,0,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "texts" VALUES(12,'等目菩萨所问三昧经',NULL,NULL,'Sutra of the Samadhi Asked by Equal-Eye Bodhisattva','sutra',NULL,'T10n0288',NULL,NULL,'not_listed',NULL,NULL,NULL,'西晋',NULL,NULL,3,NULL,NULL,'十定品别译','zh',NULL,0,0,0,0,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "texts" VALUES(13,'显无边佛土功德经',NULL,NULL,'Sutra Revealing the Merits of Immeasurable Buddha Lands','sutra',NULL,'T10n0289',NULL,NULL,'not_listed',NULL,NULL,NULL,'唐',NULL,NULL,1,NULL,NULL,'寿量品别译。玄奘译，文体精严','zh',NULL,0,0,0,0,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "texts" VALUES(14,'佛说较量一切佛刹功德经',NULL,NULL,'Sutra on Comparing the Merits of All Buddha Fields','sutra',NULL,'T10n0290',NULL,NULL,'not_listed',NULL,NULL,NULL,'宋',NULL,NULL,1,NULL,NULL,'与寿量品教义相关但不完全对应，属同类题材','zh',NULL,0,0,0,0,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "texts" VALUES(15,'佛说如来兴显经',NULL,NULL,'Sutra on the Arising and Manifestation of the Tathagata','sutra',NULL,'T10n0291',NULL,NULL,'not_listed',NULL,NULL,NULL,'西晋',NULL,NULL,4,NULL,NULL,'如来性起/出现品的早期大本别译','zh',NULL,0,0,0,0,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "texts" VALUES(16,'度世品经',NULL,NULL,'Sutra on Transcending the World (Lishi-jian-pin)','sutra',NULL,'T10n0292',NULL,NULL,'not_listed',NULL,NULL,NULL,'西晋',NULL,NULL,6,NULL,NULL,'离世间品别译。注意：藏文《离世间品》有独特异译段落，对勘时应三方比较','zh',NULL,0,0,0,0,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "texts" VALUES(17,'佛说罗摩伽经',NULL,NULL,'The Ramaka Sutra','sutra',NULL,'T10n0294',NULL,NULL,'not_listed',NULL,NULL,NULL,'西秦',NULL,NULL,3,NULL,NULL,'入法界品部分段落别译','zh',NULL,0,0,0,0,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "texts" VALUES(18,'大方广佛华严经入法界品',NULL,NULL,'Avatamsaka Sutra: Chapter on Entering the Dharmadhatu (continuation)','sutra',NULL,'T10n0295',NULL,NULL,'not_listed',NULL,NULL,NULL,'唐',NULL,NULL,1,NULL,NULL,'续译八十华严入法界品的缺失部分','zh',NULL,0,0,0,0,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "texts" VALUES(19,'文殊师利发愿经',NULL,NULL,'Sutra on Manjusri''s Vows','sutra',NULL,'T10n0296',NULL,NULL,'not_listed',NULL,NULL,NULL,'东晋',NULL,NULL,1,NULL,NULL,'文殊菩萨发愿文，与华严之文殊智慧教义相关','zh',NULL,0,0,0,0,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "texts" VALUES(20,'普贤菩萨行愿赞',NULL,NULL,'Hymn of Samantabhadra''s Practice and Vows','sutra',NULL,'T10n0297',NULL,NULL,'not_listed',NULL,NULL,NULL,'唐',NULL,NULL,1,NULL,NULL,'即《普贤行愿品》之独立赞颂形式。藏汉佛教共同尊奉','zh',NULL,0,0,0,0,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "texts" VALUES(21,'大方广普贤所说经',NULL,NULL,'Mahavaipulya Sutra Spoken by Samantabhadra','sutra',NULL,'T0847',NULL,NULL,'not_listed',NULL,NULL,NULL,'唐',NULL,NULL,1,NULL,NULL,'【高优先级对勘目标】与藏文华严《普贤宣说品》(Toh44.28) 内容高度对应。 汉文大藏经有此别译本但未纳入八十华严正文。 藏汉对译项目核心对比文本。
','zh',NULL,0,0,0,0,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "texts" VALUES(22,'大方广总持宝光明经',NULL,NULL,'Sutra of the Dharani Jewel Radiance','sutra',NULL,'T10n0299',NULL,NULL,'not_listed',NULL,NULL,NULL,'宋',NULL,NULL,5,NULL,NULL,'与华严宝光明教义相关','zh',NULL,0,0,0,0,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "texts" VALUES(23,'大方广佛华严经不思议佛境界分',NULL,NULL,'The Inconceivable Buddha Realms Section of the Avatamsaka Sutra','sutra',NULL,'T10n0300',NULL,NULL,'not_listed',NULL,NULL,NULL,'唐',NULL,NULL,1,NULL,NULL,'华严不思议境界之专论','zh',NULL,0,0,0,0,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "texts" VALUES(24,'大方广如来不思议境界经',NULL,NULL,'Sutra on the Inconceivable Realm of the Tathagata','sutra',NULL,'T10n0301',NULL,NULL,'not_listed',NULL,NULL,NULL,'唐',NULL,NULL,1,NULL,NULL,'如来不思议境界，与前一经为同本异译','zh',NULL,0,0,0,0,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "texts" VALUES(25,'度诸佛境界智光严经',NULL,NULL,'Sutra on Ornamenting with Wisdom-Light Across All Buddha Realms','sutra',NULL,'T10n0302',NULL,NULL,'not_listed',NULL,NULL,NULL,NULL,NULL,NULL,1,NULL,NULL,'佛境界智光庄严之专题经典','zh',NULL,0,0,0,0,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "texts" VALUES(26,'佛华严入如来德智不思议境界经',NULL,NULL,'Sutra on Entering the Inconceivable Realm of Tathagata Virtue','sutra',NULL,'T10n0303',NULL,NULL,'not_listed',NULL,NULL,NULL,'隋',NULL,NULL,2,NULL,NULL,'与T0300-T0302同一题材','zh',NULL,0,0,0,0,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "texts" VALUES(27,'大方广入如来智德不思议经',NULL,NULL,'Mahavaipulya Sutra on Entering the Inconceivable Wisdom-Virtue of the Tathagata','sutra',NULL,'T10n0304',NULL,NULL,'not_listed',NULL,NULL,NULL,'唐',NULL,NULL,1,NULL,NULL,'如来智德相关，实叉难陀译','zh',NULL,0,0,0,0,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "texts" VALUES(28,'信力入印法门经',NULL,NULL,'Sutra of the Dharma-Gate Sealed by the Power of Faith','sutra',NULL,'T10n0305',NULL,NULL,'not_listed',NULL,NULL,NULL,'元魏',NULL,NULL,5,NULL,NULL,'信力法门之详细展开，与华严十信教义相关','zh',NULL,0,0,0,0,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "texts" VALUES(29,'大方广佛花严经修慈分',NULL,NULL,'The Loving-Kindness Meditation Section of the Avatamsaka Sutra','sutra',NULL,'T10n0306',NULL,NULL,'not_listed',NULL,NULL,NULL,'唐',NULL,NULL,1,NULL,NULL,'【修行实践重要文献】华严系统慈心观之专修经典。收录于修行板块','zh',NULL,0,0,0,0,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "texts" VALUES(30,'佛说庄严菩提心经',NULL,NULL,'Sutra on Adorning the Bodhi Mind','sutra',NULL,'T10n0307',NULL,NULL,'not_listed',NULL,NULL,NULL,'姚秦',NULL,NULL,1,NULL,NULL,'菩提心之庄严，与华严发菩提心教义相关','zh',NULL,0,0,0,0,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "texts" VALUES(31,'佛说大方广菩萨十地经',NULL,NULL,'Mahavaipulya Sutra on the Ten Stages of Bodhisattvas','sutra',NULL,'T10n0308',NULL,NULL,'not_listed',NULL,NULL,NULL,'元魏',NULL,NULL,1,NULL,NULL,'【语境注意】以菩萨十地为主题，但与华严《十地品》内容不同。 法藏《华严经传记》判为眷属经。
','zh',NULL,0,0,0,0,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "texts" VALUES(32,'最胜问菩萨十住除垢断结经',NULL,NULL,'Sutra on the Stages Purifying Defilements (asked by the Supreme One)','sutra',NULL,'T10n0309',NULL,NULL,'not_listed',NULL,NULL,NULL,'姚秦',NULL,NULL,10,NULL,NULL,'【重要语境警示】虽以十住为名，但并非华严《十住品》之别译。 法藏《华严经传记》明确判为"非十住品亦非十地品"，属眷属经。
','zh',NULL,0,0,0,0,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "texts" VALUES(33,'十住毗婆沙论',NULL,'Daśabhūmika-vibhāṣā','Dashabhumika-vibhasa (Commentary on the Ten Stages)','shastra',NULL,'T26n1521',NULL,NULL,'not_listed',NULL,NULL,NULL,'姚秦',NULL,NULL,17,NULL,NULL,'【语境注意】经名虽含"十住"，实际是对《华严经·十地品》的注释。 现存仅十七卷（仅注释至第二地），全本已佚。 据传译自《大不思议论》十万颂。 这是现存最早的《十地品》系统注释，被华严宗奉为法统源头之一。
','zh',NULL,0,0,0,1,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "texts" VALUES(34,'十地经论',NULL,'Daśabhūmika-sūtra-śāstra','Dashabhumika-sutra-sastra','shastra',NULL,'T26n1522',NULL,NULL,'not_listed',NULL,NULL,NULL,'后魏',NULL,NULL,12,NULL,NULL,'世亲菩萨对《十地品》的系统注释。创新"六相"等名相范畴， 汉译本催生了南北朝地论师学派。澄观《华严经疏钞》全面吸收 其思想。是连接印度唯识学与汉传华严学的关键论典。
','zh',NULL,0,0,0,1,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "texts" VALUES(35,'大乘起信论',NULL,'Mahāyāna-śraddhotpāda-śāstra','Mahayana-sraddhotpada-sastra (The Awakening of Faith)','shastra',NULL,'T32n1666',NULL,NULL,'not_listed',NULL,NULL,NULL,'梁',NULL,NULL,1,NULL,NULL,'虽非直接注释华严经，但"一心开二门""真如缘起"等核心思想 与华严宗"法界缘起"理论深度关联。法藏著《大乘起信论义记》 为最权威注释之一。
','zh',NULL,0,0,0,1,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "texts" VALUES(36,'华严一乘教义分齐章（五教章）',NULL,NULL,'Chapter on the Five Teachings of Huayan (Wujiao Zhang)','commentary',NULL,NULL,'T45n1866',NULL,'not_listed',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'法藏最具代表性的判教著作。建立五教十宗判教体系，华严宗教学纲领','zh',NULL,1,0,0,0,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "texts" VALUES(37,'华严经探玄记',NULL,NULL,'Investigating the Mysteries of the Avatamsaka Sutra','commentary',NULL,NULL,'T35n1733',NULL,'not_listed',NULL,NULL,NULL,NULL,NULL,NULL,20,NULL,NULL,'法藏对六十华严的系统注释','zh',NULL,1,0,0,0,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "texts" VALUES(38,'华严金师子章',NULL,NULL,'The Golden Lion Chapter','commentary',NULL,NULL,NULL,NULL,'not_listed',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'法藏为武则天讲说华严的记录，以金师子为喻阐述事事无碍法界观','zh',NULL,0,0,0,0,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "texts" VALUES(39,'大乘起信论义记',NULL,NULL,'A Commentary on the Awakening of Faith','commentary',NULL,NULL,'T44n1846',NULL,'not_listed',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'法藏对《大乘起信论》的注释，是理解华严宗''真如缘起''思想的关键','zh',NULL,1,0,0,0,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "texts" VALUES(40,'大方广佛华严经疏',NULL,NULL,'Commentary on the Avatamsaka Sutra','commentary',NULL,NULL,'T35n1735',NULL,'not_listed',NULL,NULL,NULL,NULL,NULL,NULL,60,NULL,NULL,'澄观对八十华严的系统注释。华严教学集大成之作','zh',NULL,1,0,0,0,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "texts" VALUES(41,'华严经随疏演义钞',NULL,NULL,'Expanded Commentary on the Avatamsaka Sutra Commentary','commentary',NULL,NULL,'T36n1736',NULL,'not_listed',NULL,NULL,NULL,NULL,NULL,NULL,90,NULL,NULL,'对《华严经疏》的进一步展开注释','zh',NULL,1,0,0,0,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "texts" VALUES(42,'华严原人论',NULL,NULL,'On the Origin of Humans (Yuanren Lun)','commentary',NULL,NULL,'T45n1886',NULL,'not_listed',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'宗密以华严圆教统摄儒释道诸家之说的人类本源论','zh',NULL,1,0,0,0,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "texts" VALUES(43,'禅源诸诠集都序',NULL,NULL,'Preface to the Collected Commentaries on the Sources of Chan','commentary',NULL,NULL,'T48n2015',NULL,'not_listed',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'宗密融合禅宗与华严教学的纲领性著作','zh',NULL,1,0,0,0,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "texts" VALUES(44,'新华严经论',NULL,NULL,'New Commentary on the Avatamsaka Sutra','commentary',NULL,NULL,'T36n1739',NULL,'not_listed',NULL,NULL,NULL,NULL,NULL,NULL,40,NULL,NULL,'李通玄以《易经》融会华严的独特注释。在家学者视角','zh',NULL,1,0,0,0,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "texts" VALUES(45,'华严经搜玄记',NULL,NULL,'Searching the Profundities of the Avatamsaka Sutra','commentary',NULL,NULL,'T35n1732',NULL,'not_listed',NULL,NULL,NULL,NULL,NULL,NULL,5,NULL,NULL,'华严二祖智俨对六十华严的注释，奠定了华严宗教学基础','zh',NULL,1,0,0,0,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "texts" VALUES(46,'新编诸宗教藏总录（义天录）',NULL,NULL,'New Comprehensive Catalogue of the Canonical Teachings of All Traditions','catalog',NULL,NULL,NULL,NULL,'not_listed',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'【基准目录】收录东亚佛教章疏数千部的总目录，是华严文献存伪鉴定和编目基准','zh',NULL,0,0,0,0,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "texts" VALUES(47,'藏译华严经','Sangs rgyas phal po che zhes bya ba shin tu rgyas pa chen po''i mdo',NULL,'The Stem Array (Tibetan Avatamsaka, Toh 44)','sutra',NULL,NULL,NULL,'Toh 44','not_listed',NULL,NULL,NULL,NULL,'约9世纪初',NULL,4,45,NULL,'【本项目核心文献】藏文华严共45品，比汉文八十华严多2品: - 第11品 《如来华严品》(Tathāgatāvataṃsaka): 汉文全缺 - 第28品 《普贤宣说品》: 汉文有实叉难陀别译单行本(T0847) 此外《离世间品》有部分独特异译段落。 译自中亚于阗原本，而非印度梵本，具有独立的版本传承体系。
','bo',NULL,0,0,1,0,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "texts" VALUES(48,'84000 项目 — 藏文华严英译 (持续出版中)',NULL,NULL,'84000 Project: English Translation of the Tibetan Avatamsaka (ongoing)','translation',NULL,NULL,NULL,NULL,'not_listed',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'国际学术标准的藏译英项目。附带梵-藏-英三语术语库，为本项目核心参考资源','bo','https://84000.co',0,0,1,0,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "texts" VALUES(49,'华严经讲记（全本）',NULL,NULL,'Lectures on the Avatamsaka Sutra (Venerable Mengcan)','lecture',NULL,NULL,NULL,NULL,'not_listed',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'梦参老和尚晚年讲说全本《八十华严》的记录，当代最重要的华严讲记之一','zh',NULL,0,0,0,0,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "texts" VALUES(50,'成一和尚著作集',NULL,NULL,'Collected Works of Venerable Chengyi','study',NULL,NULL,NULL,NULL,'not_listed',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'华严莲社第三任住持成一法师的全集，含多部华严学专著','zh',NULL,0,0,0,0,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "texts" VALUES(51,'华严学讲义',NULL,NULL,'Lectures on Huayan Studies (Venerable Xiandu)','study',NULL,NULL,NULL,NULL,'not_listed',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'贤度法师的华严学教学大纲','zh',NULL,0,0,0,0,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "texts" VALUES(52,'大海的印迹：贤度法师传',NULL,NULL,'Traces in the Ocean: A Biography of Venerable Xiandu','biography',NULL,NULL,NULL,NULL,'not_listed',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'当代华严女性法嗣传承者的传记','zh',NULL,0,0,0,0,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "texts" VALUES(53,'The Flower Adornment Sutra (英译全本)',NULL,NULL,'The Flower Adornment Sutra (Complete English Translation)','translation',NULL,NULL,NULL,NULL,'not_listed',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'基于汉文八十华严的完整英译（3册），附带详尽学术注释与科判','zh',NULL,0,0,0,0,'2026-09-27 08:00:19','2026-09-27 08:00:19');
INSERT INTO "texts" VALUES(54,'Entry Into the Inconceivable (英译入法界品)',NULL,NULL,'Entry Into the Inconceivable (English translation of the Gandavyuha)','translation',NULL,NULL,NULL,NULL,'not_listed',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Cleary译《入法界品》单行本，文学性强','zh',NULL,0,0,0,0,'2026-09-27 08:00:19','2026-09-27 08:00:19');
CREATE TABLE chapters (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    sutra_id        INTEGER NOT NULL REFERENCES texts(id),
    title_zh        TEXT    NOT NULL,                       -- 汉文品名
    title_bo        TEXT,                                   -- 藏文品名
    title_sa        TEXT,                                   -- 梵文品名
    title_en        TEXT,                                   -- 英文品名
    order_num       INTEGER NOT NULL,                       -- 品目序号
    volumn_start    INTEGER,                               -- 起始卷
    volumn_end      INTEGER,                               -- 结束卷
    in_60huayan     INTEGER DEFAULT 0,                     -- 六十华严是否有此品
    in_80huayan     INTEGER DEFAULT 0,                     -- 八十华严是否有此品
    in_40huayan     INTEGER DEFAULT 0,                     -- 四十华严是否有此品
    in_tibetan      INTEGER DEFAULT 0,                     -- 藏文是否有此品
    tibetan_order   INTEGER,                               -- 藏文品目序号 (可能不同)
    is_unique_to_bo INTEGER DEFAULT 0,                     -- 藏文独有
    is_unique_to_zh INTEGER DEFAULT 0,                     -- 汉文独有
    content_diff    TEXT,                                   -- 内容差异说明
    source          TEXT,                                   -- 品目列表来源
    created_at      TEXT    DEFAULT (datetime('now'))
);
INSERT INTO "chapters" VALUES(1,2,'世主妙严品',NULL,NULL,'The Wondrous Adornments of the Rulers of the Worlds',1,NULL,NULL,1,1,0,1,NULL,0,0,NULL,'CBETA/84000','2026-09-27 08:00:19');
INSERT INTO "chapters" VALUES(2,2,'如来现相品',NULL,NULL,'Apparitions of the Buddha',2,NULL,NULL,1,1,0,1,NULL,0,0,NULL,'CBETA/84000','2026-09-27 08:00:19');
INSERT INTO "chapters" VALUES(3,2,'普贤三昧品',NULL,NULL,'The Samādhi of Universal Good',3,NULL,NULL,1,1,0,1,NULL,0,0,NULL,'CBETA/84000','2026-09-27 08:00:19');
INSERT INTO "chapters" VALUES(4,2,'世界成就品',NULL,NULL,'Completions of the Worlds',4,NULL,NULL,1,1,0,1,NULL,0,0,NULL,'CBETA/84000','2026-09-27 08:00:19');
INSERT INTO "chapters" VALUES(5,2,'华藏世界品',NULL,NULL,'The Flower Bank World',5,NULL,NULL,1,1,0,1,NULL,0,0,NULL,'CBETA/84000','2026-09-27 08:00:19');
INSERT INTO "chapters" VALUES(6,2,'毗卢遮那品',NULL,NULL,'Vairocana',6,NULL,NULL,1,1,0,1,NULL,0,0,NULL,'CBETA/84000','2026-09-27 08:00:19');
INSERT INTO "chapters" VALUES(7,2,'如来名号品',NULL,NULL,'The Names of the Buddha',7,NULL,NULL,1,1,0,1,NULL,0,0,NULL,'CBETA/84000','2026-09-27 08:00:19');
INSERT INTO "chapters" VALUES(8,2,'四圣谛品',NULL,NULL,'The Four Holy Truths',8,NULL,NULL,1,1,0,1,NULL,0,0,NULL,'CBETA/84000','2026-09-27 08:00:19');
INSERT INTO "chapters" VALUES(9,2,'光明觉品',NULL,NULL,'Awakening by Light',9,NULL,NULL,1,1,0,1,NULL,0,0,NULL,'CBETA/84000','2026-09-27 08:00:19');
INSERT INTO "chapters" VALUES(10,2,'菩萨问明品',NULL,NULL,'Statements of the Questioning Bodhisattvas',10,NULL,NULL,1,1,0,1,NULL,0,0,NULL,'CBETA/84000','2026-09-27 08:00:19');
INSERT INTO "chapters" VALUES(11,2,'净行品',NULL,NULL,'Pure Practices',11,NULL,NULL,1,1,0,1,NULL,0,0,NULL,'CBETA/84000','2026-09-27 08:00:19');
INSERT INTO "chapters" VALUES(12,2,'贤首品',NULL,NULL,'The Chief of Worthies',12,NULL,NULL,1,1,0,1,NULL,0,0,NULL,'CBETA/84000','2026-09-27 08:00:19');
INSERT INTO "chapters" VALUES(13,2,'升须弥山顶品',NULL,NULL,'Ascending to the Peak of Mount Sumeru',13,NULL,NULL,1,1,0,1,NULL,0,0,NULL,'CBETA/84000','2026-09-27 08:00:19');
INSERT INTO "chapters" VALUES(14,2,'须弥顶上偈赞品',NULL,NULL,'Eulogies on the Peak of Mount Sumeru',14,NULL,NULL,1,1,0,1,NULL,0,0,NULL,'CBETA/84000','2026-09-27 08:00:19');
INSERT INTO "chapters" VALUES(15,2,'十住品',NULL,NULL,'The Ten Abodes',15,NULL,NULL,1,1,0,1,NULL,0,0,NULL,'CBETA/84000','2026-09-27 08:00:19');
INSERT INTO "chapters" VALUES(16,2,'梵行品',NULL,NULL,'The Practice of Purity',16,NULL,NULL,1,1,0,1,NULL,0,0,NULL,'CBETA/84000','2026-09-27 08:00:19');
INSERT INTO "chapters" VALUES(17,2,'初发心功德品',NULL,NULL,'Merits of the First Aspiration for Awakening',17,NULL,NULL,1,1,0,1,NULL,0,0,NULL,'CBETA/84000','2026-09-27 08:00:19');
INSERT INTO "chapters" VALUES(18,2,'明法品',NULL,NULL,'Understanding the Teaching',18,NULL,NULL,1,1,0,1,NULL,0,0,NULL,'CBETA/84000','2026-09-27 08:00:19');
INSERT INTO "chapters" VALUES(19,2,'升夜摩天宫品',NULL,NULL,'Ascending to the Palace of the Heaven of Yāma',19,NULL,NULL,1,1,0,1,NULL,0,0,NULL,'CBETA/84000','2026-09-27 08:00:19');
INSERT INTO "chapters" VALUES(20,2,'夜摩宫中偈赞品',NULL,NULL,'Eulogies in the Palace of the Heaven of Yāma',20,NULL,NULL,1,1,0,1,NULL,0,0,NULL,'CBETA/84000','2026-09-27 08:00:19');
INSERT INTO "chapters" VALUES(21,2,'十行品',NULL,NULL,'The Ten Practices',21,NULL,NULL,1,1,0,1,NULL,0,0,NULL,'CBETA/84000','2026-09-27 08:00:19');
INSERT INTO "chapters" VALUES(22,2,'十无尽藏品',NULL,NULL,'The Ten Inexhaustible Treasures',22,NULL,NULL,1,1,0,1,NULL,0,0,NULL,'CBETA/84000','2026-09-27 08:00:19');
INSERT INTO "chapters" VALUES(23,2,'升兜率天宫品',NULL,NULL,'Ascending to the Palace of Tuṣita Heaven',23,NULL,NULL,1,1,0,1,NULL,0,0,NULL,'CBETA/84000','2026-09-27 08:00:19');
INSERT INTO "chapters" VALUES(24,2,'兜率宫中偈赞品',NULL,NULL,'Eulogies in the Palace of Tuṣita Heaven',24,NULL,NULL,1,1,0,1,NULL,0,0,NULL,'CBETA/84000','2026-09-27 08:00:19');
INSERT INTO "chapters" VALUES(25,2,'十回向品',NULL,NULL,'The Ten Transferences',25,NULL,NULL,1,1,0,1,NULL,0,0,NULL,'CBETA/84000','2026-09-27 08:00:19');
INSERT INTO "chapters" VALUES(26,2,'十地品',NULL,NULL,'The Ten Grounds',26,NULL,NULL,1,1,0,1,NULL,0,0,NULL,'CBETA/84000','2026-09-27 08:00:19');
INSERT INTO "chapters" VALUES(27,2,'十定品',NULL,NULL,'The Ten Concentrations',27,NULL,NULL,0,1,0,1,NULL,0,0,NULL,'CBETA/84000','2026-09-27 08:00:19');
INSERT INTO "chapters" VALUES(28,2,'十通品',NULL,NULL,'The Ten Supernatural Powers',28,NULL,NULL,0,1,0,1,NULL,0,0,NULL,'CBETA/84000','2026-09-27 08:00:19');
INSERT INTO "chapters" VALUES(29,2,'十忍品',NULL,NULL,'The Ten Patiences',29,NULL,NULL,0,1,0,1,NULL,0,0,NULL,'CBETA/84000','2026-09-27 08:00:19');
INSERT INTO "chapters" VALUES(30,2,'阿僧祇品',NULL,NULL,'Incalculable Numbers',30,NULL,NULL,0,1,0,1,NULL,0,0,NULL,'CBETA/84000','2026-09-27 08:00:19');
INSERT INTO "chapters" VALUES(31,2,'寿量品',NULL,NULL,'Lifespans',31,NULL,NULL,0,1,0,1,NULL,0,0,NULL,'CBETA/84000','2026-09-27 08:00:19');
INSERT INTO "chapters" VALUES(32,2,'诸菩萨住处品',NULL,NULL,'The Residences of the Bodhisattvas',32,NULL,NULL,0,1,0,1,NULL,0,0,NULL,'CBETA/84000','2026-09-27 08:00:19');
INSERT INTO "chapters" VALUES(33,2,'佛不思议法品',NULL,NULL,'The Unthinkable Qualities of the Buddhas',33,NULL,NULL,1,1,0,1,NULL,0,0,NULL,'CBETA/84000','2026-09-27 08:00:19');
INSERT INTO "chapters" VALUES(34,2,'如来十身相海品',NULL,NULL,'The Ocean of Marks of the Ten Bodies of the Buddha',34,NULL,NULL,1,1,0,1,NULL,0,0,NULL,'CBETA/84000','2026-09-27 08:00:19');
INSERT INTO "chapters" VALUES(35,2,'如来随好光明功德品',NULL,NULL,'The Merits of the Great Marks of Light of the Buddha',35,NULL,NULL,1,1,0,1,NULL,0,0,NULL,'CBETA/84000','2026-09-27 08:00:19');
INSERT INTO "chapters" VALUES(36,2,'普贤行品',NULL,NULL,'The Practices of Universal Good',36,NULL,NULL,1,1,0,1,NULL,0,0,NULL,'CBETA/84000','2026-09-27 08:00:19');
INSERT INTO "chapters" VALUES(37,2,'如来出现品',NULL,NULL,'The Apparition of the Buddha',37,NULL,NULL,1,1,0,1,NULL,0,0,NULL,'CBETA/84000','2026-09-27 08:00:19');
INSERT INTO "chapters" VALUES(38,2,'离世间品',NULL,NULL,'Detachment from the World',38,NULL,NULL,1,1,0,1,NULL,0,0,NULL,'CBETA/84000','2026-09-27 08:00:19');
INSERT INTO "chapters" VALUES(39,2,'入法界品',NULL,NULL,'Entry into the Dharma Realm',39,NULL,NULL,1,1,0,1,NULL,0,0,NULL,'CBETA/84000','2026-09-27 08:00:19');
INSERT INTO "chapters" VALUES(40,2,'如来华严品',NULL,'Tathāgatāvataṃsaka','The Adornment of the Buddha',112,NULL,NULL,0,0,0,1,NULL,1,0,NULL,'Toh44/84000','2026-09-27 08:00:19');
INSERT INTO "chapters" VALUES(41,2,'普贤宣说品',NULL,'Samantabhadraparivarta','The Disquisition of Universal Good',128,NULL,NULL,0,0,0,1,NULL,1,0,NULL,'Toh44/84000','2026-09-27 08:00:19');
CREATE TABLE locations (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    source_id       TEXT,                                   -- 原始ID (如 loc_001, l_h)
    name_zh         TEXT    NOT NULL,                       -- 古地名
    current_name    TEXT,                                   -- 现代地名
    lat             REAL,                                   -- 纬度
    lng             REAL,                                   -- 经度
    type            TEXT    DEFAULT 'temple',
                    -- temple | mountain | region | city | translation_site
    dynasty         TEXT,
    city            TEXT,                                   -- 所在城市
    province        TEXT,                                   -- 所在省份
    description     TEXT,
    related_persons TEXT,                                   -- 关联人物 ID，JSON 数组
    source          TEXT,
    created_at      TEXT    DEFAULT (datetime('now'))
);
INSERT INTO "locations" VALUES(1,'l_changan_t','长安逍遥园',NULL,34.26,108.92,'temple','后秦',NULL,NULL,'鸠摩罗什译场所在。后秦姚兴为罗什建,八百沙门参与译经。','["person_103"]','《高僧传》卷二·鸠摩罗什传〔逍遥园西明阁译场〕(CBETA T50n2059)','2026-09-27 08:00:19');
INSERT INTO "locations" VALUES(2,'l_changan_x','长安大慈恩寺·弘福寺',NULL,34.22,108.96,'temple','唐',NULL,NULL,'玄奘归国后译场所在。大慈恩寺大雁塔为贮藏梵本所建。','["person_111"]','《大慈恩寺三藏法师传》(CBETA T50n2053)；玄奘《大唐西域记》〔慈恩/弘福译场〕','2026-09-27 08:00:19');
INSERT INTO "locations" VALUES(3,'l_f','台北福慧寺','新北市树林福慧寺',24.98,121.42,'temple','当代','新北市','台湾省','钦因长老住持。2010年成观法师于此受华严兼慈恩法脉。','["person_041", "person_043", "person_126"]','福慧寺团体现状资料〔存疑：自述〕','2026-09-27 08:00:19');
INSERT INTO "locations" VALUES(4,'l_ganden','拉萨·甘丹寺',NULL,29.75,91.47,'temple','明',NULL,NULL,'宗喀巴1409年创建。格鲁派根本道场。','["person_152"]','《至尊宗喀巴大师传》〔法尊译〕〔宗喀巴建寺（1409），格鲁派祖庭〕(T2)','2026-09-27 08:00:19');
INSERT INTO "locations" VALUES(5,'l_guangzhou','广州',NULL,23.13,113.26,'region','历代',NULL,NULL,'海上丝绸之路起点。义净671年从此出发赴印度。','["person_112"]','《高僧传》卷三·求那跋陀罗传〔南朝海上译经口岸〕(CBETA T50n2059)','2026-09-27 08:00:19');
INSERT INTO "locations" VALUES(6,'l_h','南投大华严寺',NULL,23.92,120.88,'temple','当代',NULL,NULL,'海云继梦导师。普贤乘根本道场。','["person_042"]','大华严寺团体现状资料〔存疑：自述〕','2026-09-27 08:00:19');
INSERT INTO "locations" VALUES(7,'l_kolkata','加尔各答·罗摩克里希纳传道会',NULL,22.57,88.36,'temple','近现代',NULL,NULL,'辨喜于1897年创立。全球吠檀多传播中心。','["person_140", "person_141"]','辨喜《演讲与布道全集》〔1897 创立罗摩克里希纳传道会总部〕(T1)','2026-09-27 08:00:19');
INSERT INTO "locations" VALUES(8,'l_kucha','龟兹',NULL,41.7,82.9,'region','古西域',NULL,NULL,'鸠摩罗什故乡。西域佛教重镇,丝绸之路北道枢纽。','["person_103"]','《高僧传》卷二·鸠摩罗什传〔龟兹故里〕；玄奘《大唐西域记》卷一','2026-09-27 08:00:19');
INSERT INTO "locations" VALUES(9,'l_nalanda','那烂陀寺',NULL,25.14,85.44,'temple','古印度',NULL,NULL,'古印度佛教最高学府。玄奘、义净等求法僧曾于此留学。无著、世亲于此弘传瑜伽行派。','["person_000b", "person_102", "person_110", "person_111", "person_112"]','玄奘《大唐西域记》卷九·那烂陀僧伽蓝〔无著/世亲/玄奘修学处〕','2026-09-27 08:00:19');
INSERT INTO "locations" VALUES(10,'l_nalanda2','那烂陀寺(参考)',NULL,25.14,85.44,'temple','古印度',NULL,NULL,'寂天与阿底峡曾驻锡于此。7-12世纪印度佛教最高学府。','["person_150", "person_151"]','玄奘《大唐西域记》卷九·那烂陀僧伽蓝（参考位置标注，与前条比对）','2026-09-27 08:00:19');
INSERT INTO "locations" VALUES(11,'l_nara','奈良东大寺',NULL,34.69,135.84,'temple','唐/日本',NULL,NULL,'日本华严宗本山。审祥首次讲说《华严经》之处。','["person_050", "person_j01", "person_j02"]','《东大寺要录》；《续日本纪》','2026-09-27 08:00:19');
INSERT INTO "locations" VALUES(12,'l_pondi','印度本地治里·Aurobindo Ashram',NULL,11.94,79.83,'temple','当代',NULL,NULL,'奥罗宾多与The Mother创立道场。整体瑜伽发源地。','["person_142"]','奥罗宾多自著《综合瑜伽》等；奥罗宾多道场史料(第二手史)(T2)','2026-09-27 08:00:19');
INSERT INTO "locations" VALUES(13,'l_ramana','印度圣山 Arunachala (Tiruvannamalai)',NULL,12.23,79.07,'mountain','当代',NULL,NULL,'拉玛那·马哈希终生隐修之处。每年吸引全球数千求道者朝圣。','["person_143"]','《Talks with Sri Ramana Maharshi》〔弟子笔录于阿鲁那佳拉山〕(T1)','2026-09-27 08:00:19');
INSERT INTO "locations" VALUES(14,'l_yoga','印度阿弥塔巴·LIFE Mission道场',NULL,23.02,72.57,'temple','当代',NULL,'古吉拉特邦','胜师子王菩萨道场。海云继梦2008年12月于此接受大乘瑜伽行法灌顶传法。','["person_042", "person_134"]','当代瑜伽行道场资料(〔存疑〕当代自述) ','2026-09-27 08:00:19');
INSERT INTO "locations" VALUES(15,'loc_001','大慈恩寺','大慈恩寺',34.2198,108.9598,'temple','唐','长安（今西安）','陕西省','唐代皇家寺院。法藏曾于此参与译场并讲说华严。','["person_003"]','《宋高僧传》卷四·又《慈恩传》：大慈恩寺为玄奘译经主道场','2026-09-27 08:00:19');
INSERT INTO "locations" VALUES(16,'loc_002','终南山','终南山',33.93,108.97,'mountain','唐','长安（今西安）南郊','陕西省','华严宗重要修行圣地。杜顺、智俨、法藏等均曾于此修行或讲法。至相寺位于此山。','["person_001", "person_002", "person_003", "person_103"]','《续高僧传》卷二十五·法顺传〔至相寺〕；《宋高僧传》卷五','2026-09-27 08:00:19');
INSERT INTO "locations" VALUES(17,'loc_003','清凉山（五台山）','五台山',39.0306,113.5648,'mountain','唐','忻州市五台县','山西省','文殊菩萨道场，华严经中明指为清凉山。澄观（清凉国师）曾于此著《华严经疏》，''清凉''之号由此而来。华严宗与五台山渊源极深。唐代大华严寺为山中核心华严道场。','["person_004"]','《华严经·诸菩萨住处品》','2026-09-27 08:00:19');
INSERT INTO "locations" VALUES(18,'loc_004','圭峰','圭峰山',34.03,108.68,'mountain','唐','长安（今西安）西南','陕西省','宗密晚年住此，世称圭峰大师。','["person_005"]','《宋高僧传》卷六','2026-09-27 08:00:19');
INSERT INTO "locations" VALUES(19,'loc_005','方山','方山',38.04,113.21,'mountain','唐','太原市','山西省','李通玄于此处著《新华严经论》。','["person_009"]','《宋高僧传》卷二十二','2026-09-27 08:00:19');
INSERT INTO "locations" VALUES(20,'loc_006','杭州慧因寺','慧因高丽寺',30.23,120.13,'temple','宋','杭州市','浙江省','宋代华严中兴道场。净源法师住此弘传华严，高丽义天入宋求法于此。义天归国后送金书《华严经》三种译本供养此寺。世称''华严第一道场''。','["person_010", "person_011"]','《佛祖统纪》','2026-09-27 08:00:19');
INSERT INTO "locations" VALUES(21,'loc_007','洛阳佛授记寺','（已毁，洛阳故城）',34.68,112.44,'temple','唐','洛阳','河南省','实叉难陀于此处主持《八十华严》译场。法藏参与证义。','["person_003", "person_007", "person_103"]','《宋高僧传》卷二','2026-09-27 08:00:19');
INSERT INTO "locations" VALUES(22,'loc_008','台北华严莲社','华严莲社',25.033,121.565,'temple','当代','台北市','台湾省','现代华严宗弘传中心。南亭法师创立，成一法师、贤度法师相继住持。出版华严典籍、主办国际华严学术研讨。','["person_015", "person_016", "person_017"]','华严莲社社志/官网〔存疑：机构史料〕','2026-09-27 08:00:19');
INSERT INTO "locations" VALUES(23,'loc_009','北京广济寺','广济寺',39.923,116.365,'temple','近现代','北京市','北京市','近代华严弘扬重要道场。慈舟法师曾长期于此讲说华严。','["person_014"]','近现代佛教史料〔存疑〕','2026-09-27 08:00:19');
INSERT INTO "locations" VALUES(24,'loc_010','常熟兴福寺','兴福寺（华严大学旧址）',31.65,120.74,'temple','清','常熟市','江苏省','月霞长老于此处创立华严大学（1914年），开启近现代华严教育之先河。','["person_012"]','近现代佛教史料','2026-09-27 08:00:19');
INSERT INTO "locations" VALUES(25,'loc_011','印度那烂陀寺','那烂陀寺遗址 (Nalanda)',25.1355,85.4432,'temple','','比哈尔邦',NULL,'古印度佛教最高学府。《华严经》中善财童子参访的南方诸城中，多参考此地的学术格局。',NULL,'学术研究','2026-09-27 08:00:19');
INSERT INTO "locations" VALUES(26,'loc_012','于阗','和田地区',37.11,79.91,'region','唐','和田','新疆维吾尔自治区','古于阗国。藏译《华严经》译自于阗原本。实叉难陀故乡。中亚佛教枢纽，华严经流布关键节点。','["person_007"]','学术研究（《华严经》流传史）','2026-09-27 08:00:19');
INSERT INTO "locations" VALUES(27,'loc_013','敦煌','敦煌莫高窟',40.04,94.8,'region','唐','敦煌市','甘肃省','敦煌藏经洞出土华严经写本数百件，包括汉文写本与藏文残片，为版本对勘提供重要实物文献。',NULL,'敦煌学研究','2026-09-27 08:00:19');
INSERT INTO "locations" VALUES(28,'loc_014','尼泊尔加德满都谷地','加德满都',27.71,85.32,'region','','加德满都',NULL,'现存华严经梵文写本的主要发现地。尼泊尔梵文残卷为华严经源流研究提供了第一手文献。',NULL,'梵文写本研究','2026-09-27 08:00:19');
INSERT INTO "locations" VALUES(29,'loc_015','匡山（庐山）','庐山',29.57,115.98,'mountain','唐','九江市','江西省','历代华严行者修行道场之一。',NULL,'佛教史料','2026-09-27 08:00:19');
INSERT INTO "locations" VALUES(30,'loc_016','台北大毘卢寺','大毘卢寺',24.988,121.571,'temple','当代','台北市','文山区','成观法师1991年创立之道场。以禅密为主体兼修他宗,定期举办楞严法会。附设毘卢出版社及新逍遥园译经院(桃园杨梅)。','["person_126"]','大毘卢寺官网〔存疑：机构自述〕','2026-09-27 08:00:19');
CREATE TABLE lineages (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    source_id       TEXT    UNIQUE,                         -- 原始ID
    name            TEXT    NOT NULL UNIQUE,                 -- 法系名称
    description     TEXT,
    period          TEXT,                                   -- 时间跨度
    color           TEXT,                                   -- 渲染颜色 (hex)
    created_at      TEXT    DEFAULT (datetime('now'))
);
INSERT INTO "lineages" VALUES(1,'lineage_临济宗','临济宗','','','#d48476','2026-09-27 08:00:19');
INSERT INTO "lineages" VALUES(2,'lineage_linji_mengcan','临济宗·梦参—海云继梦','梦参长老为临济宗第46代，1991年破例剃度海云继梦，赐法名昌一（第47代）。','1991 CE',NULL,'2026-09-27 08:00:19');
INSERT INTO "lineages" VALUES(3,'lineage_华严·禅宗互动','华严·禅宗互动','','',NULL,'2026-09-27 08:00:19');
INSERT INTO "lineages" VALUES(4,'lineage_华严·译场合作','华严·译场合作','','',NULL,'2026-09-27 08:00:19');
INSERT INTO "lineages" VALUES(5,'lineage_hw5','华严五祖','从杜顺到宗密的华严宗正统传承，奠定华严宗教学与观法体系。后经宋元明清延续至高原明昱（25世），再传至当代钦因长老（41世）。','557 CE — 至今','#b8863c','2026-09-27 08:00:19');
INSERT INTO "lineages" VALUES(6,'lineage_huayen_lotus','华严莲社（智光→南亭→成一→贤度）','1952年创立于台北，七代住持延续华严宗''专修、专研、专弘''传统。成一法师1975年创华严专宗学院。','1952 CE — 至今',NULL,'2026-09-27 08:00:19');
INSERT INTO "lineages" VALUES(7,'lineage_translators','华严译师谱系','汉藏华严经主要翻译者及其文本传承关联。覆盖后汉至唐约500年。','167 CE — 840 CE',NULL,'2026-09-27 08:00:19');
INSERT INTO "lineages" VALUES(8,'lineage_印度源流','印度源流','','','#9e8b6e','2026-09-27 08:00:19');
INSERT INTO "lineages" VALUES(9,'lineage_参考线','参考线','','','#a0a0a0','2026-09-27 08:00:19');
INSERT INTO "lineages" VALUES(10,'lineage_地论→华严','地论→华严','','',NULL,'2026-09-27 08:00:19');
INSERT INTO "lineages" VALUES(11,'lineage_地论学派','地论学派','','',NULL,'2026-09-27 08:00:19');
INSERT INTO "lineages" VALUES(12,'lineage_大乘瑜伽行法','大乘瑜伽行法','','','#d4a574','2026-09-27 08:00:19');
INSERT INTO "lineages" VALUES(13,'lineage_大乘瑜伽行法(2008.12传法灌顶)','大乘瑜伽行法(2008.12传法灌顶)','','',NULL,'2026-09-27 08:00:19');
INSERT INTO "lineages" VALUES(14,'lineage_密宗传承(开元三大士→空海)','密宗传承(开元三大士→空海)','','',NULL,'2026-09-27 08:00:19');
INSERT INTO "lineages" VALUES(15,'lineage_dangdai','当代华严学者网络','如孝法师、贤度法师等当代华严思想研究者与实践弘传者构成的松散网络。','2000 CE — 至今',NULL,'2026-09-27 08:00:19');
INSERT INTO "lineages" VALUES(16,'lineage_cizhou','慈舟系','近代慈舟法师的华严弘扬传承。','1877 CE — 1958 CE','#8b7a9e','2026-09-27 08:00:19');
INSERT INTO "lineages" VALUES(17,'lineage_japan','日本华严','日本东大寺等华严传承。审祥为初传。','740 CE — 至今','#8b7a9e','2026-09-27 08:00:19');
INSERT INTO "lineages" VALUES(18,'lineage_月霞系','月霞系','','','#7a9ec0','2026-09-27 08:00:19');
INSERT INTO "lineages" VALUES(19,'lineage_yuexia','月霞系（华严大学→应慈→真禅）','清末月霞长老开创的现代华严传承。经由华严大学、应慈法师，传至真禅法师。','1858 CE — 1995 CE',NULL,'2026-09-27 08:00:19');
INSERT INTO "lineages" VALUES(20,'lineage_litx','李通玄系','李通玄（枣柏大师）开创的华严学在家学者传统，以《易经》融会华严。','635 CE — 至今','#c8893e','2026-09-27 08:00:19');
INSERT INTO "lineages" VALUES(21,'lineage_求法僧与译师网络','求法僧与译师网络','','',NULL,'2026-09-27 08:00:19');
INSERT INTO "lineages" VALUES(22,'lineage_贤首宗高原法系','贤首宗高原法系','','','#c46b5d','2026-09-27 08:00:19');
INSERT INTO "lineages" VALUES(23,'lineage_xianshou_gaoyuan','贤首宗高原法系（钦因→海云继梦）','自明代高原明昱（25世）起，贤首宗兼传慈恩宗（唯识）。传至41世钦因长老，2008年传衣钵予海云继梦（42世）。','明代 — 至今',NULL,'2026-09-27 08:00:19');
INSERT INTO "lineages" VALUES(24,'lineage_goryeo','高丽华严','高丽义天传入朝鲜半岛的华严教学传统。','1085 CE — 至今','#6d9a6e','2026-09-27 08:00:19');
CREATE TABLE lineage_edges (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    from_person_id  TEXT    NOT NULL,                       -- 源人物ID (如 person_003)
    to_person_id    TEXT    NOT NULL,                       -- 目标人物ID
    relation        TEXT    NOT NULL DEFAULT 'MASTER_OF',
                    -- MASTER_OF | INFLUENCED | LINEAGE | CONTEMPORARY
    lineage_name    TEXT,                                   -- 所属法系 (如 华严五祖)
    lineage_id      INTEGER REFERENCES lineages(id),        -- 关联法系表
    note            TEXT,                                   -- 出处说明
    source          TEXT,                                   -- 文献依据
    created_at      TEXT    DEFAULT (datetime('now'))
);
INSERT INTO "lineage_edges" VALUES(1,'person_001','person_002','MASTER_OF','华严五祖',5,'杜顺传法于智俨','《续高僧传》卷二十五·法顺传；《宋高僧传》卷五·智俨传 (CBETA T50n2061)','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(2,'person_002','person_003','MASTER_OF','华严五祖',5,'智俨传法于法藏','《宋高僧传》卷五·法藏传 (CBETA T50n2061)','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(3,'person_003','person_004','INFLUENCED','华严五祖',5,'法藏后传。澄观私淑法藏之学','《宋高僧传》卷五·澄观传〔承法藏《华严》之学〕(CBETA T50n2061)','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(4,'person_004','person_005','MASTER_OF','华严五祖',5,'澄观传法于宗密','《宋高僧传》卷五·澄观传〔付法宗密〕(CBETA T50n2061)','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(5,'person_003','person_050','MASTER_OF','华严五祖',5,'法藏传法于审祥','《东大寺要录》〔审祥以《探玄记》开讲《六十华严》〕','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(6,'person_021','person_041','INFLUENCED','华严五祖',5,'高原明昱(25世)法脉传至钦因(41世)','〔存疑〕贤首宗《付法师资记》系宗内谱系记载','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(7,'person_011','person_010','MASTER_OF','高丽华严',24,'净源传法于义天','《高丽史》卷九十·义天传；《佛祖统纪》卷二十九·净源传','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(8,'person_003','person_011','INFLUENCED','高丽华严',24,'法藏学说是净源华严教学源头','《佛祖统纪》卷二十九·净源传〔宋代华严中兴，承法藏之学〕','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(9,'person_003','person_050','MASTER_OF','日本华严',17,'法藏传法于审祥','《东大寺要录》〔审祥以《探玄记》开讲《六十华严》〕','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(10,'person_012','person_013','MASTER_OF','月霞系（华严大学→应慈→真禅）',19,'月霞传法于常惺','民国佛教史料〔月霞华严大学法嗣〕（T3 东初《中国佛教近代史》卷）','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(11,'person_012','person_031','MASTER_OF','月霞系（华严大学→应慈→真禅）',19,'月霞师弟应慈，共弘华严','民国佛教史料〔月霞法嗣〕（T3 东初《中国佛教近代史》卷；〔存疑〕待核一手年谱）','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(12,'person_031','person_044','MASTER_OF','月霞系（华严大学→应慈→真禅）',19,'应慈传法于真禅','民国佛教史料〔应慈法嗣〕（T3 东初《中国佛教近代史》卷）','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(13,'person_018','person_015','MASTER_OF','华严莲社（智光→南亭→成一→贤度）',6,'智光(1st)传南亭(2nd)','华严莲社社志(〔存疑〕机构谱系) ','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(14,'person_015','person_016','MASTER_OF','华严莲社（智光→南亭→成一→贤度）',6,'南亭(2nd)传成一(3rd)','华严莲社社志〔存疑：机构谱系〕','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(15,'person_016','person_032','MASTER_OF','华严莲社（智光→南亭→成一→贤度）',6,'成一(3rd)传了中(4th)','华严莲社社志〔存疑：机构谱系〕','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(16,'person_032','person_033','MASTER_OF','华严莲社（智光→南亭→成一→贤度）',6,'了中(4th)传净海(5th)','华严莲社社志〔存疑：机构谱系〕','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(17,'person_033','person_017','MASTER_OF','华严莲社（智光→南亭→成一→贤度）',6,'净海(5th)传贤度(6th)','华严莲社社志〔存疑：机构谱系〕','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(18,'person_017','person_034','MASTER_OF','华严莲社（智光→南亭→成一→贤度）',6,'贤度(6th)传明度(7th)','华严莲社社志〔存疑：机构谱系〕','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(19,'person_021','person_041','INFLUENCED','贤首宗高原法系（钦因→海云继梦）',23,'高原明昱(25世)法脉传至钦因(41世)','〔存疑〕贤首宗《付法师资记》系宗内谱系记载','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(20,'person_041','person_042','MASTER_OF','贤首宗高原法系（钦因→海云继梦）',23,'钦因(41世)2008年传衣钵予海云继梦(42世)','〔存疑〕教界口述谱系，未见独立史料','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(21,'person_041','person_043','MASTER_OF','贤首宗高原法系（钦因→海云继梦）',23,'钦因另传体佛法师等法嗣','教界资料(〔存疑〕师承自述) ','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(22,'person_041','person_126','MASTER_OF','贤首宗高原法系（钦因→海云继梦）',23,'钦因(41世)2010年4月24日传华严兼慈恩法脉予成观法师(42世)','教界资料(〔存疑〕师承自述) ','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(23,'person_019','person_042','MASTER_OF','临济宗·梦参—海云继梦',2,'梦参1991年剃度海云继梦（临济第47代）','〔存疑〕教界口述谱系，未见独立史料','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(24,'person_017','person_045','CONTEMPORARY','当代华严学者网络',15,'贤度与如孝同为当代华严弘扬者','凤凰网佛教（2024年）〔存疑：媒体转述〕','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(25,'person_007b','person_006','INFLUENCED','华严译师谱系',7,'支娄迦谶首译《兜沙经》（167 CE）→佛驮跋陀罗译六十华严（420 CE）','《高僧传》卷一·支娄迦谶传〔译《兜沙经》启华严单品译本〕(CBETA T50n2059)','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(26,'person_006','person_007','INFLUENCED','华严译师谱系',7,'六十华严（420）→八十华严（699）是重译与扩充关系','《宋高僧传》卷二·实叉难陀传〔重译以续前译〕(CBETA T50n2061)','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(27,'person_007','person_008','INFLUENCED','华严译师谱系',7,'八十华严（699）→四十华严（798）补全《入法界品》','《宋高僧传》卷二·般若传〔译《四十华严》〕(CBETA T50n2061)','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(28,'person_003','person_007','INFLUENCED','华严译师谱系',7,'法藏参与实叉难陀译场并证义','《宋高僧传》卷二·实叉难陀传〔法藏笔受八十华严〕(CBETA T50n2061)','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(29,'person_103','person_007','INFLUENCED','华严译师谱系',7,'鸠摩罗什译经传统影响后世译师','〔存疑〕罗什译例影响后世译场，缺直接记载','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(30,'person_103','person_006','INFLUENCED','华严译师谱系',7,'罗什先译十住经,佛驮继译六十华严','〔存疑〕同代长安译场并列，无师承','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(31,'person_103','person_110','INFLUENCED','华严译师谱系',7,'罗什在中亚的声望间接促使法显西行','〔存疑〕年代略交叠，影响不载','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(32,'person_111','person_102','MASTER_OF','求法僧与译师网络',21,'玄奘在那烂陀师从戒贤,戒贤属无著世亲瑜伽行派传承','〔存疑〕玄奘习无著论典而敬奉，非面授师承','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(33,'person_111','person_112','INFLUENCED','求法僧与译师网络',21,'玄奘开创的求法传统直接影响义净','《宋高僧传》卷一·义净传〔继玄奘西行求法〕(CBETA T50n2061)','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(34,'person_110','person_006','INFLUENCED','求法僧与译师网络',21,'法显《佛国记》记录了佛驮跋陀罗故乡迦毗罗卫','《高僧传》卷二·佛驮跋陀罗传〔建康道场寺与法显共译经律〕(CBETA T50n2059)','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(35,'person_110','person_111','INFLUENCED','求法僧与译师网络',21,'法显的求法经历鼓舞了玄奘','学术〔法显《佛国记》为玄奘西行参照〕(T2)','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(36,'person_111','person_001','CONTEMPORARY','求法僧与译师网络',21,'玄奘与杜顺同代,唯识与华严初创期有义学对话','〔存疑〕仅年代粗略同代，不载交往','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(37,'person_111','person_003','CONTEMPORARY','求法僧与译师网络',21,'玄奘与法藏父亲相识,法藏曾参访玄奘译场','〔存疑〕仅年代粗略同代，不载交往','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(38,'person_112','person_003','CONTEMPORARY','求法僧与译师网络',21,'义净与法藏同时代,同为译场主持者','《宋高僧传》卷一·义净传；卷五·法藏传〔同朝同名译场时代〕(CBETA T50n2061)','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(39,'person_008','person_112','CONTEMPORARY','求法僧与译师网络',21,'般若(四十华严译者)与义净同为唐代译师','《宋高僧传》卷二·般若传；卷一·义净传〔同朝译场〕(CBETA T50n2061)','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(40,'person_113','person_104','INFLUENCED','求法僧与译师网络',21,'真谛译摄大乘论→菩提流支译十地经论,唯识学两条入华路径','〔存疑〕同为《摄论》《十地论》系译传，相互影响不载','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(41,'person_113','person_114','INFLUENCED','求法僧与译师网络',21,'真谛与求那跋陀罗同为南朝四大译师','〔存疑〕同属如来藏译传系，关系间接','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(42,'person_115','person_003','CONTEMPORARY','求法僧与译师网络',21,'不空与法藏同代,密宗与华严密法有历史关联','〔存疑〕岁纪未重叠（不空705–774，法藏643–712），对照为误','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(43,'person_116','person_006','INFLUENCED','求法僧与译师网络',21,'竺法护译十地品别译→佛驮跋陀罗译六十华严,补全华严品目','《高僧传》卷一·竺法护传〔译《渐备一切智德经》《如来兴显经》华严单品〕(CBETA T50n2059)','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(44,'person_116','person_007b','INFLUENCED','求法僧与译师网络',21,'竺法护继支谶后继续翻译华严单行经','学术〔华严单品译传：兜沙经→渐备经〕(T2)','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(45,'person_117','person_111','INFLUENCED','求法僧与译师网络',21,'慧超《往五天竺国传》补充了玄奘《大唐西域记》之后的印度信息','〔存疑〕《往五天竺国传》行纪晚于玄奘，影响系推衍','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(46,'person_117','person_112','INFLUENCED','求法僧与译师网络',21,'慧超继义净之后的新罗求法僧,延续海路求法传统','〔存疑〕同上，影响系推衍','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(47,'person_007b','person_116','INFLUENCED','求法僧与译师网络',21,'支谶开华严汉译先河→竺法护系统翻译多部华严单行经','学术〔华严单品译传链〕(T2)','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(48,'person_120','person_122','MASTER_OF','密宗传承(开元三大士→空海)',14,'善无畏传胎藏界密法予一行','《宋高僧传》卷五·一行传〔从善无畏受《大日经》〕(CBETA T50n2061)','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(49,'person_121','person_115','MASTER_OF','密宗传承(开元三大士→空海)',14,'金刚智传金刚界密法予不空','《宋高僧传》卷一·不空传〔师事金刚智〕(CBETA T50n2061)','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(50,'person_120','person_121','CONTEMPORARY','密宗传承(开元三大士→空海)',14,'善无畏与金刚智同在长安开元间传密法,合称开元三大士','《宋高僧传》卷一·金刚智传〔开元三大士同朝〕(CBETA T50n2061)','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(51,'person_115','person_123','MASTER_OF','密宗传承(开元三大士→空海)',14,'不空传两部密法予慧果','空海《御请来目录》(CBETA T55n2161)；圆照《大唐青龙寺三朝供奉大德行状》','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(52,'person_123','person_124','MASTER_OF','密宗传承(开元三大士→空海)',14,'慧果于青龙寺传法予空海,空海归日本创真言宗','空海《御请来目录》(CBETA T55n2161)；《大唐青龙寺三朝供奉大德行状》','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(53,'person_124','person_003','INFLUENCED','密宗传承(开元三大士→空海)',14,'空海《十住心论》以华严判教框架判摄显密,体现密教与华严之对话','空海《御请来目录》(CBETA T55n2161)〔法藏教判思想〕','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(54,'person_115','person_005','CONTEMPORARY','密宗传承(开元三大士→空海)',14,'不空与宗密同代,密宗与华严宗有义学互动','〔存疑〕时代不重叠（不空卒774，宗密生780），对照为误','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(55,'person_122','person_005','CONTEMPORARY','密宗传承(开元三大士→空海)',14,'一行与澄观同时代,天文学与华严宇宙观可比较','〔存疑〕时代不重叠（一行卒727，宗密生780），对照为误','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(56,'person_f01','person_041','MASTER_OF','贤首宗高原法系',22,'','贤首宗高原法系宗内资料(〔存疑〕谱系自述) ','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(57,'person_041','person_f02','MASTER_OF','贤首宗高原法系',22,'','贤首宗高原法系宗内资料(〔存疑〕谱系自述) ','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(58,'person_050','person_j01','MASTER_OF','日本华严',17,'','《东大寺要录》〔审祥授华严于良弁，为东大寺华严相承开端〕','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(59,'person_j01','person_j02','MASTER_OF','日本华严',17,'','凝然《三国佛法传通缘起》〔东大寺华严相承谱〕','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(60,'person_j02','person_j03','MASTER_OF','日本华严',17,'','凝然《三国佛法传通缘起》〔东大寺华严相承谱〕','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(61,'person_j03','person_j04','INFLUENCED','日本华严',17,'','凝然《三国佛法传通缘起》〔东大寺华严相承〕','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(62,'person_j03','person_j05','MASTER_OF','日本华严',17,'','凝然《三国佛法传通缘起》〔东大寺华严相承谱〕','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(63,'person_003','person_070','MASTER_OF','华严五祖',5,'','《宋高僧传》卷六·慧苑传 (CBETA T50n2061)；《开元释教录》卷九','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(64,'person_070','person_004','INFLUENCED','华严五祖',5,'','《宋高僧传》卷六·慧苑传〔澄观刊定慧苑异说〕(CBETA T50n2061)','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(65,'person_001','person_060','INFLUENCED','华严五祖',5,'','〔存疑〕学理渊源系后代推衍，无师承史料','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(66,'person_021','person_080','INFLUENCED','华严五祖',5,'','〔存疑〕贤首宗《付法师资记》系宗内谱系记载','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(67,'person_002','person_061','MASTER_OF','华严五祖',5,'','《宋高僧传》卷四·义湘传〔入唐师事智俨〕(CBETA T50n2061)','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(68,'person_090','person_001','INFLUENCED','华严五祖',5,'','学术〔地论学派思想接引华严初祖〕(T2)','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(69,'person_011','person_091','INFLUENCED','华严五祖',5,'','〔存疑〕同代华严学者，影响关系缺直接史料','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(70,'person_091','person_010','INFLUENCED','华严五祖',5,'','《高丽史》卷九十·义天传〔与宋华严学者交游〕(〔存疑〕具体师长关系待核)','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(71,'person_011','person_062','INFLUENCED','高丽华严',24,'','〔存疑〕均如(923-998)早于净源(1011-1088)，影响方向待考','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(72,'person_062','person_010','INFLUENCED','高丽华严',24,'','《均如传》；《高丽史》卷九十〔义天辑华严章疏，承均如之学〕','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(73,'person_j05','person_j06','INFLUENCED','日本华严',17,'','《元亨释书》(CBETA B32n0173)','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(74,'person_j06','person_j07','INFLUENCED','日本华严',17,'','《元亨释书》(CBETA B32n0173)；凝然《三国佛法传通缘起》','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(75,'person_012','person_092','MASTER_OF','月霞系',18,'','民国佛教史料〔持松受学于月霞〕（T3）','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(76,'person_101','person_000a','INFLUENCED','印度源流',8,'','学术〔大乘佛教史：马鸣启大乘、龙树弘中观〕(T2)','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(77,'person_102','person_000b','MASTER_OF','印度源流',8,'','学术考证〔无著世亲昆仲，世亲回心大乘〕(T2)','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(78,'person_104','person_090','MASTER_OF','华严五祖',5,'','《续高僧传》卷二十一·慧光传〔受《十地经论》〕','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(79,'person_005','person_004','MASTER_OF','华严五祖',5,'','〔存疑〕方向存疑：宗密学于澄观，常规记为澄观→宗密 (CBETA T50n2061)','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(80,'person_005','person_044','INFLUENCED','华严·禅宗互动',3,'','〔存疑〕学理推衍，宗密华严禅对近代华严的整体影响（T3文献综述）','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(81,'person_003','person_007','CONTEMPORARY','华严·译场合作',4,'法藏参与实叉难陀译场并证义','《宋高僧传》卷二·实叉难陀传〔同参译场〕(CBETA T50n2061)','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(82,'person_090','person_001','INFLUENCED','地论→华严',10,'','学术〔地论学派思想接引华严初祖〕(T2)','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(83,'person_104','person_090','MASTER_OF','地论学派',11,'','《续高僧传》卷二十一·慧光传〔受《十地经论》〕','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(84,'person_000a','person_102','INFLUENCED','印度源流',8,'','学术考证〔中观→瑜伽行次第关联，文献出于后出〕(T2)','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(85,'person_101','person_102','INFLUENCED','印度源流',8,'','〔存疑〕年代先后但无直接师承记载','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(86,'person_105','person_100','INFLUENCED','印度源流',8,'','《佛说太子瑞应本起经》(CBETA T185)〔燃灯授记〕','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(87,'person_106','person_100','INFLUENCED','印度源流',8,'','《长阿含经》卷一·大本经 (CBETA T1n0001)〔七佛传承〕','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(88,'person_130','person_131','MASTER_OF','大乘瑜伽行法',12,'','当代瑜伽行传承资料(〔存疑〕当代自述) ','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(89,'person_131','person_132','MASTER_OF','大乘瑜伽行法',12,'','当代瑜伽行传承资料(〔存疑〕当代自述) ','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(90,'person_132','person_133','MASTER_OF','大乘瑜伽行法',12,'','当代瑜伽行传承资料(〔存疑〕当代自述) ','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(91,'person_133','person_134','MASTER_OF','大乘瑜伽行法',12,'','当代瑜伽行传承资料(〔存疑〕当代自述) ','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(92,'person_134','person_042','MASTER_OF','大乘瑜伽行法(2008.12传法灌顶)',13,'','〔存疑〕梦中授法系教界自述，不可独立验证','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(93,'person_140','person_141','MASTER_OF','参考线',9,'','The Gospel of Sri Ramakrishna（M. 笔录）(T1 原典)','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(94,'person_x01','person_x02','MASTER_OF','临济宗',1,'','《虚云和尚年谱》〔净慧承临济法脉〕（T3）','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(95,'person_x01','person_s04','INFLUENCED','临济宗',1,'','〔存疑〕当代学者研修虚云禅法，无直接师承','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(96,'person_x01','person_x03','INFLUENCED','临济宗',1,'','〔存疑〕自述参学，无直接师承记载','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(97,'person_x02','person_x03','CONTEMPORARY','临济宗',1,'','〔存疑〕当代同代人物，无直接关联记载','2026-09-27 08:00:19');
INSERT INTO "lineage_edges" VALUES(98,'person_050','person_050','MASTER_OF','日本华严',17,'审祥赴日，于东大寺弘传华严','graph.json','2026-09-27 08:00:19');
CREATE TABLE person_locations (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id       INTEGER NOT NULL REFERENCES persons(id),
    location_id     INTEGER NOT NULL REFERENCES locations(id),
    relation        TEXT,                                   -- born | died | taught | visited | resided
    period_start    TEXT,                                   -- 开始时间
    period_end      TEXT,                                   -- 结束时间
    note            TEXT,
    UNIQUE(person_id, location_id, relation)
);
INSERT INTO "person_locations" VALUES(1,48,1,'active_in',NULL,NULL,'据 locations.l_changan_t (长安逍遥园) 关联');
INSERT INTO "person_locations" VALUES(2,54,2,'active_in',NULL,NULL,'据 locations.l_changan_x (长安大慈恩寺·弘福寺) 关联');
INSERT INTO "person_locations" VALUES(3,30,3,'active_in',NULL,NULL,'据 locations.l_f (台北福慧寺) 关联');
INSERT INTO "person_locations" VALUES(4,32,3,'active_in',NULL,NULL,'据 locations.l_f (台北福慧寺) 关联');
INSERT INTO "person_locations" VALUES(5,67,3,'active_in',NULL,NULL,'据 locations.l_f (台北福慧寺) 关联');
INSERT INTO "person_locations" VALUES(6,79,4,'associated',NULL,NULL,'据 locations.l_ganden (拉萨·甘丹寺) 关联');
INSERT INTO "person_locations" VALUES(7,55,5,'associated',NULL,NULL,'据 locations.l_guangzhou (广州) 关联');
INSERT INTO "person_locations" VALUES(8,31,6,'active_in',NULL,NULL,'据 locations.l_h (南投大华严寺) 关联');
INSERT INTO "person_locations" VALUES(9,73,7,'associated',NULL,NULL,'据 locations.l_kolkata (加尔各答·罗摩克里希纳传道会) 关联');
INSERT INTO "person_locations" VALUES(10,74,7,'associated',NULL,NULL,'据 locations.l_kolkata (加尔各答·罗摩克里希纳传道会) 关联');
INSERT INTO "person_locations" VALUES(11,48,8,'associated',NULL,NULL,'据 locations.l_kucha (龟兹) 关联');
INSERT INTO "person_locations" VALUES(12,2,9,'active_in',NULL,NULL,'据 locations.l_nalanda (那烂陀寺) 关联');
INSERT INTO "person_locations" VALUES(13,47,9,'active_in',NULL,NULL,'据 locations.l_nalanda (那烂陀寺) 关联');
INSERT INTO "person_locations" VALUES(14,53,9,'associated',NULL,NULL,'据 locations.l_nalanda (那烂陀寺) 关联');
INSERT INTO "person_locations" VALUES(15,54,9,'associated',NULL,NULL,'据 locations.l_nalanda (那烂陀寺) 关联');
INSERT INTO "person_locations" VALUES(16,55,9,'associated',NULL,NULL,'据 locations.l_nalanda (那烂陀寺) 关联');
INSERT INTO "person_locations" VALUES(17,77,10,'associated',NULL,NULL,'据 locations.l_nalanda2 (那烂陀寺(参考)) 关联');
INSERT INTO "person_locations" VALUES(18,78,10,'associated',NULL,NULL,'据 locations.l_nalanda2 (那烂陀寺(参考)) 关联');
INSERT INTO "person_locations" VALUES(19,36,11,'active_in',NULL,NULL,'据 locations.l_nara (奈良东大寺) 关联');
INSERT INTO "person_locations" VALUES(20,82,11,'active_in',NULL,NULL,'据 locations.l_nara (奈良东大寺) 关联');
INSERT INTO "person_locations" VALUES(21,83,11,'associated',NULL,NULL,'据 locations.l_nara (奈良东大寺) 关联');
INSERT INTO "person_locations" VALUES(22,75,12,'associated',NULL,NULL,'据 locations.l_pondi (印度本地治里·Aurobindo Ashram) 关联');
INSERT INTO "person_locations" VALUES(23,76,13,'associated',NULL,NULL,'据 locations.l_ramana (印度圣山 Arunachala (Tiruvannamalai)) 关联');
INSERT INTO "person_locations" VALUES(24,31,14,'active_in',NULL,NULL,'据 locations.l_yoga (印度阿弥塔巴·LIFE Mission道场) 关联');
INSERT INTO "person_locations" VALUES(25,72,14,'active_in',NULL,NULL,'据 locations.l_yoga (印度阿弥塔巴·LIFE Mission道场) 关联');
INSERT INTO "person_locations" VALUES(26,5,15,'active_in',NULL,NULL,'据 locations.loc_001 (大慈恩寺) 关联');
INSERT INTO "person_locations" VALUES(27,3,16,'active_in',NULL,NULL,'据 locations.loc_002 (终南山) 关联');
INSERT INTO "person_locations" VALUES(28,4,16,'active_in',NULL,NULL,'据 locations.loc_002 (终南山) 关联');
INSERT INTO "person_locations" VALUES(29,5,16,'active_in',NULL,NULL,'据 locations.loc_002 (终南山) 关联');
INSERT INTO "person_locations" VALUES(30,48,16,'associated',NULL,NULL,'据 locations.loc_002 (终南山) 关联');
INSERT INTO "person_locations" VALUES(31,6,17,'active_in',NULL,NULL,'据 locations.loc_003 (清凉山（五台山）) 关联');
INSERT INTO "person_locations" VALUES(32,7,18,'active_in',NULL,NULL,'据 locations.loc_004 (圭峰) 关联');
INSERT INTO "person_locations" VALUES(33,12,19,'active_in',NULL,NULL,'据 locations.loc_005 (方山) 关联');
INSERT INTO "person_locations" VALUES(34,13,20,'active_in',NULL,NULL,'据 locations.loc_006 (杭州慧因寺) 关联');
INSERT INTO "person_locations" VALUES(35,14,20,'active_in',NULL,NULL,'据 locations.loc_006 (杭州慧因寺) 关联');
INSERT INTO "person_locations" VALUES(36,5,21,'active_in',NULL,NULL,'据 locations.loc_007 (洛阳佛授记寺) 关联');
INSERT INTO "person_locations" VALUES(37,9,21,'active_in',NULL,NULL,'据 locations.loc_007 (洛阳佛授记寺) 关联');
INSERT INTO "person_locations" VALUES(38,48,21,'associated',NULL,NULL,'据 locations.loc_007 (洛阳佛授记寺) 关联');
INSERT INTO "person_locations" VALUES(39,18,22,'associated',NULL,NULL,'据 locations.loc_008 (台北华严莲社) 关联');
INSERT INTO "person_locations" VALUES(40,19,22,'active_in',NULL,NULL,'据 locations.loc_008 (台北华严莲社) 关联');
INSERT INTO "person_locations" VALUES(41,20,22,'active_in',NULL,NULL,'据 locations.loc_008 (台北华严莲社) 关联');
INSERT INTO "person_locations" VALUES(42,17,23,'active_in',NULL,NULL,'据 locations.loc_009 (北京广济寺) 关联');
INSERT INTO "person_locations" VALUES(43,15,24,'active_in',NULL,NULL,'据 locations.loc_010 (常熟兴福寺) 关联');
INSERT INTO "person_locations" VALUES(44,9,26,'active_in',NULL,NULL,'据 locations.loc_012 (于阗) 关联');
INSERT INTO "person_locations" VALUES(45,67,30,'active_in',NULL,NULL,'据 locations.loc_016 (台北大毘卢寺) 关联');
CREATE TABLE cross_refs (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    from_text_id    INTEGER NOT NULL REFERENCES texts(id),
    to_text_id      INTEGER NOT NULL REFERENCES texts(id),
    relation        TEXT    NOT NULL,
                    -- cites | commentary_on | subcommentary_on |
                    -- alternate_trans | expanded_version | related |
                    -- ritual_based_on | lecture_on
    note            TEXT,
    source          TEXT,
    UNIQUE(from_text_id, to_text_id, relation)
);
INSERT INTO "cross_refs" VALUES(1,1,2,'earlier_translation','最早汉译全本华严。译自支法领从于阗带回的梵本。 三十四品中，《宝王如来性起品》为八十华严之《如来出现品》所替代， 结构亦有调整。六十华严保留了部分更接近早期梵本的表述。
',NULL);
INSERT INTO "cross_refs" VALUES(2,1,3,'earlier_translation','最早汉译全本华严。译自支法领从于阗带回的梵本。 三十四品中，《宝王如来性起品》为八十华严之《如来出现品》所替代， 结构亦有调整。六十华严保留了部分更接近早期梵本的表述。
',NULL);
INSERT INTO "cross_refs" VALUES(3,2,1,'standard_version','目前汉传佛教最通用的华严经版本。武则天从于阗请来梵本， 诏实叉难陀等于洛阳佛授记寺翻译。法藏参与证义。 三十九品，七处九会结构较六十华严完整。 缺藏译本中的《如来华严品》和《普贤宣说品》。
',NULL);
INSERT INTO "cross_refs" VALUES(4,2,3,'standard_version','目前汉传佛教最通用的华严经版本。武则天从于阗请来梵本， 诏实叉难陀等于洛阳佛授记寺翻译。法藏参与证义。 三十九品，七处九会结构较六十华严完整。 缺藏译本中的《如来华严品》和《普贤宣说品》。
',NULL);
INSERT INTO "cross_refs" VALUES(5,2,47,'standard_version','目前汉传佛教最通用的华严经版本。武则天从于阗请来梵本， 诏实叉难陀等于洛阳佛授记寺翻译。法藏参与证义。 三十九品，七处九会结构较六十华严完整。 缺藏译本中的《如来华严品》和《普贤宣说品》。
',NULL);
INSERT INTO "cross_refs" VALUES(6,3,2,'expanded_chapter','即《入法界品》的单行全本翻译。内容比六十华严和八十华严中的 《入法界品》更完整。文末附《普贤菩萨行愿赞》，为藏汉佛教 共同尊奉的重要修行文献。善财童子五十三参的故事全本在此。
',NULL);
INSERT INTO "cross_refs" VALUES(7,3,47,'expanded_chapter','即《入法界品》的单行全本翻译。内容比六十华严和八十华严中的 《入法界品》更完整。文末附《普贤菩萨行愿赞》，为藏汉佛教 共同尊奉的重要修行文献。善财童子五十三参的故事全本在此。
',NULL);
INSERT INTO "cross_refs" VALUES(8,4,2,'alternate_trans','对应: 如来名号品 (八十华严第7品)',NULL);
INSERT INTO "cross_refs" VALUES(9,5,2,'alternate_trans','对应: 净行品 (八十华严第11品)',NULL);
INSERT INTO "cross_refs" VALUES(10,6,2,'alternate_trans','对应: 净行品 (八十华严第11品)',NULL);
INSERT INTO "cross_refs" VALUES(11,7,2,'alternate_trans','对应: 十住品 (八十华严第15品)',NULL);
INSERT INTO "cross_refs" VALUES(12,8,2,'alternate_trans','对应: 十住品 (八十华严第15品)',NULL);
INSERT INTO "cross_refs" VALUES(13,9,2,'alternate_trans','对应: 十地品 (八十华严第26品)',NULL);
INSERT INTO "cross_refs" VALUES(14,10,2,'alternate_trans','对应: 十地品 (八十华严第26品)',NULL);
INSERT INTO "cross_refs" VALUES(15,11,2,'alternate_trans','对应: 十地品 (八十华严第26品)',NULL);
INSERT INTO "cross_refs" VALUES(16,12,2,'alternate_trans','对应: 十定品 (八十华严第27品)',NULL);
INSERT INTO "cross_refs" VALUES(17,13,2,'alternate_trans','对应: 寿量品 (八十华严第31品)',NULL);
INSERT INTO "cross_refs" VALUES(18,14,2,'alternate_trans','对应: 寿量品相关',NULL);
INSERT INTO "cross_refs" VALUES(19,15,2,'alternate_trans','对应: 宝王如来性起品 (六十华严第33品) / 如来出现品 (八十华严第37品)',NULL);
INSERT INTO "cross_refs" VALUES(20,16,2,'alternate_trans','对应: 离世间品 (八十华严第38品)',NULL);
INSERT INTO "cross_refs" VALUES(21,17,2,'alternate_trans','对应: 入法界品 (八十华严第39品)',NULL);
INSERT INTO "cross_refs" VALUES(22,18,2,'alternate_trans','对应: 入法界品 (续译)',NULL);
INSERT INTO "cross_refs" VALUES(23,19,2,'related','文殊菩萨发愿文，与华严之文殊智慧教义相关',NULL);
INSERT INTO "cross_refs" VALUES(24,20,2,'related','即《普贤行愿品》之独立赞颂形式。藏汉佛教共同尊奉',NULL);
INSERT INTO "cross_refs" VALUES(25,21,2,'related','【高优先级对勘目标】与藏文华严《普贤宣说品》(Toh44.28) 内容高度对应。 汉文大藏经有此别译本但未纳入八十华严正文。 藏汉对译项目核心对比文本。
',NULL);
INSERT INTO "cross_refs" VALUES(26,22,2,'related','与华严宝光明教义相关',NULL);
INSERT INTO "cross_refs" VALUES(27,23,2,'related','华严不思议境界之专论',NULL);
INSERT INTO "cross_refs" VALUES(28,24,2,'related','如来不思议境界，与前一经为同本异译',NULL);
INSERT INTO "cross_refs" VALUES(29,25,2,'related','佛境界智光庄严之专题经典',NULL);
INSERT INTO "cross_refs" VALUES(30,26,2,'related','与T0300-T0302同一题材',NULL);
INSERT INTO "cross_refs" VALUES(31,27,2,'related','如来智德相关，实叉难陀译',NULL);
INSERT INTO "cross_refs" VALUES(32,28,2,'related','信力法门之详细展开，与华严十信教义相关',NULL);
INSERT INTO "cross_refs" VALUES(33,29,2,'related','【修行实践重要文献】华严系统慈心观之专修经典。收录于修行板块',NULL);
INSERT INTO "cross_refs" VALUES(34,30,2,'related','菩提心之庄严，与华严发菩提心教义相关',NULL);
INSERT INTO "cross_refs" VALUES(35,31,2,'related','【语境注意】以菩萨十地为主题，但与华严《十地品》内容不同。 法藏《华严经传记》判为眷属经。
',NULL);
INSERT INTO "cross_refs" VALUES(36,32,2,'related','【重要语境警示】虽以十住为名，但并非华严《十住品》之别译。 法藏《华严经传记》明确判为"非十住品亦非十地品"，属眷属经。
',NULL);
INSERT INTO "cross_refs" VALUES(37,33,2,'commentary_on','【语境注意】经名虽含"十住"，实际是对《华严经·十地品》的注释。 现存仅十七卷（仅注释至第二地），全本已佚。 据传译自《大不思议论》十万颂。 这是现存最早的《十地品》系统注释，被华严宗奉为法统源头之一。
',NULL);
INSERT INTO "cross_refs" VALUES(38,34,2,'commentary_on','世亲菩萨对《十地品》的系统注释。创新"六相"等名相范畴， 汉译本催生了南北朝地论师学派。澄观《华严经疏钞》全面吸收 其思想。是连接印度唯识学与汉传华严学的关键论典。
',NULL);
INSERT INTO "cross_refs" VALUES(39,35,2,'commentary_on','虽非直接注释华严经，但"一心开二门""真如缘起"等核心思想 与华严宗"法界缘起"理论深度关联。法藏著《大乘起信论义记》 为最权威注释之一。
',NULL);
INSERT INTO "cross_refs" VALUES(40,36,2,'commentary_on','法藏最具代表性的判教著作。建立五教十宗判教体系，华严宗教学纲领',NULL);
INSERT INTO "cross_refs" VALUES(41,37,2,'commentary_on','法藏对六十华严的系统注释',NULL);
INSERT INTO "cross_refs" VALUES(42,38,2,'commentary_on','法藏为武则天讲说华严的记录，以金师子为喻阐述事事无碍法界观',NULL);
INSERT INTO "cross_refs" VALUES(43,39,2,'commentary_on','法藏对《大乘起信论》的注释，是理解华严宗''真如缘起''思想的关键',NULL);
INSERT INTO "cross_refs" VALUES(44,40,2,'commentary_on','澄观对八十华严的系统注释。华严教学集大成之作',NULL);
INSERT INTO "cross_refs" VALUES(45,41,2,'commentary_on','对《华严经疏》的进一步展开注释',NULL);
INSERT INTO "cross_refs" VALUES(46,42,2,'commentary_on','宗密以华严圆教统摄儒释道诸家之说的人类本源论',NULL);
INSERT INTO "cross_refs" VALUES(47,43,2,'commentary_on','宗密融合禅宗与华严教学的纲领性著作',NULL);
INSERT INTO "cross_refs" VALUES(48,44,2,'commentary_on','李通玄以《易经》融会华严的独特注释。在家学者视角',NULL);
INSERT INTO "cross_refs" VALUES(49,45,2,'commentary_on','华严二祖智俨对六十华严的注释，奠定了华严宗教学基础',NULL);
INSERT INTO "cross_refs" VALUES(50,46,2,'commentary_on','【基准目录】收录东亚佛教章疏数千部的总目录，是华严文献存伪鉴定和编目基准',NULL);
CREATE TABLE glossary (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    source_id       TEXT,                                   -- 原始ID
    term_sa         TEXT,                                   -- 梵文 (IAST)
    term_bo         TEXT,                                   -- 藏文 (Unicode)
    term_bo_wylie   TEXT,                                   -- 藏文 (Wylie 转写)
    term_bo_unicode TEXT,                                   -- 藏文 (Unicode)
    term_zh         TEXT    NOT NULL,                       -- 汉文
    term_en         TEXT,                                   -- 英文
    category        TEXT    DEFAULT 'doctrine',
                    -- doctrine | practice | cosmology | name | place |
                    -- scripture | lineage | ritual | virtue | state
    definition_zh   TEXT,                                   -- 中文释义
    definition_en   TEXT,                                   -- 英文释义
    source_text_id  INTEGER REFERENCES texts(id),           -- 主要出处
    alt_translations TEXT,                                  -- 其他译法 (JSON)
    created_at      TEXT    DEFAULT (datetime('now'))
);
INSERT INTO "glossary" VALUES(1,'term_001','dharmadhātu','ཆོས་ཀྱི་དབྱིངས།','chos kyi dbyings','ཆོས་ཀྱི་དབྱིངས།','法界','Dharma realm','doctrine','一切诸法所依之体，即是真如。华严宗以''事事无碍法界''为究竟，显一多相容、重重无尽之义。','The fundamental ground of all phenomena, synonymous with suchness (tathatā). In Huayan thought, the ''dharma realm of unobstructed interpenetration of all phenomena'' is the ultimate.',NULL,'{"zh": ["法性", "实相", "真如法界"], "en": ["realm of reality", "dharma element", "sphere of truth"]}','2026-09-27 08:00:19');
INSERT INTO "glossary" VALUES(2,'term_002','tathatā','དེ་བཞིན་ཉིད།','de bzhin nyid','དེ་བཞིན་ཉིད།','真如','suchness / thusness','doctrine','诸法真实如是之性，离一切分别妄想。华严宗以真如为法界之体。','The true nature of all things as they actually are, beyond conceptual differentiation.',NULL,NULL,'2026-09-27 08:00:19');
INSERT INTO "glossary" VALUES(3,'term_003','śūnyatā','སྟོང་པ་ཉིད།','stong pa nyid','སྟོང་པ་ཉིད།','空性','emptiness','doctrine','一切法无自性，缘起而生。华严宗以真空不碍妙有，空有不二为宗。','The absence of inherent existence in all phenomena. Huayan emphasizes the non-duality of emptiness and phenomenal existence.',NULL,NULL,'2026-09-27 08:00:19');
INSERT INTO "glossary" VALUES(4,'term_004','pratītyasamutpāda','རྟེན་ཅིང་འབྲེལ་བར་འབྱུང་བ།','rten cing ''brel bar ''byung ba','རྟེན་ཅིང་འབྲེལ་བར་འབྱུང་བ།','缘起','dependent origination','doctrine','一切法依因缘和合而生。华严宗以''法界缘起''为究竟，一即一切，一切即一。','All phenomena arise through the interdependent coming together of causes and conditions. Huayan''s ''dharma realm dependent origination'' is the ultimate expression: one is all, all is one.',NULL,NULL,'2026-09-27 08:00:19');
INSERT INTO "glossary" VALUES(5,'term_005','tathāgatagarbha','དེ་བཞིན་གཤེགས་པའི་སྙིང་པོ།','de bzhin gshegs pa''i snying po','དེ་བཞིན་གཤེགས་པའི་སྙིང་པོ།','如来藏','Buddha-nature / Tathāgata embryo','doctrine','一切众生本具的成佛潜能。华严宗以如来藏为一切众生皆具毗卢遮那佛性海之依据。','The innate potential for Buddhahood present in all sentient beings.',NULL,NULL,'2026-09-27 08:00:19');
INSERT INTO "glossary" VALUES(6,'term_006','āvaraṇa-vimokṣa','','sgrib pa rnam par grol ba','','事事无碍','unobstructed interpenetration of all phenomena','doctrine','华严宗究竟教义。一切事法之间相互融通，无一法能障碍他法，一尘中含法界，一念摄无尽。','The ultimate Huayan doctrine: all phenomena interpenetrate without obstruction; a single dust mote contains the entire Dharma realm.',NULL,'{"zh": ["事事无碍法界", "圆融无碍"], "en": ["non-obstruction among events", "perfect interpenetration"]}','2026-09-27 08:00:19');
INSERT INTO "glossary" VALUES(7,'term_007','','','','','理事无碍','unobstructed interpenetration of principle and phenomena','doctrine','理（真如、空性）与事（差别万象）之间圆融无碍。理遍于事，事揽理成。','The non-obstruction between universal principle (li) and particular phenomena (shi).',NULL,NULL,'2026-09-27 08:00:19');
INSERT INTO "glossary" VALUES(8,'term_008','daśa-bhūmayaḥ','ས་བཅུ།','sa bcu','ས་བཅུ།','十地','ten grounds / ten bhūmis','doctrine','菩萨修行的十个阶位: 欢喜地、离垢地、发光地、焰慧地、难胜地、现前地、远行地、不动地、善慧地、法云地。','The ten stages of bodhisattva practice.',NULL,NULL,'2026-09-27 08:00:19');
INSERT INTO "glossary" VALUES(9,'term_009','samādhi','ཏིང་ངེ་འཛིན།','ting nge ''dzin','ཏིང་ངེ་འཛིན།','三昧 / 定','meditative absorption / concentration','state','心一境性，专注不散。华严经中有''海印三昧''、''华严三昧''等殊胜禅定。','One-pointed concentration. The Avatamsaka Sūtra describes the ''Ocean-Seal Samādhi'' and ''Huayan Samādhi''.',NULL,NULL,'2026-09-27 08:00:19');
INSERT INTO "glossary" VALUES(10,'term_010','','','','','海印三昧','Ocean-Seal Samādhi (sāgara-mudrā-samādhi)','state','佛说华严经时入于海印三昧。譬如大海，能映现一切万象；佛心如海，一时普现十方法界无尽缘起。','The samādhi in which the Buddha taught the Avatamsaka Sūtra. Like the ocean reflecting all images, the Buddha''s mind simultaneously manifests the infinite interdependent arising of all realms.',NULL,NULL,'2026-09-27 08:00:19');
INSERT INTO "glossary" VALUES(11,'term_011','Vairocana','རྣམ་པར་སྣང་མཛད།','rnam par snang mdzad','རྣམ་པར་སྣང་མཛད།','毗卢遮那佛','Vairocana Buddha','name','华严经的本尊佛，光明遍照之意。为华藏世界的教主，是法身佛，一切诸佛之法身。','The central Buddha of the Avatamsaka Sūtra, whose name means ''The Illuminator''. He is the Dharmakāya Buddha presiding over the Lotus Treasury World.',NULL,NULL,'2026-09-27 08:00:19');
INSERT INTO "glossary" VALUES(12,'term_012','Samantabhadra','ཀུན་ཏུ་བཟང་པོ།','kun tu bzang po','ཀུན་ཏུ་བཟང་པོ།','普贤菩萨','Samantabhadra Bodhisattva','name','华严经中代表大行大愿的菩萨，与文殊菩萨同为毗卢遮那佛之胁侍。普贤十大愿王出自《四十华严·普贤行愿品》。','The bodhisattva representing great practice and vows, appearing as Vairocana''s attendant alongside Mañjuśrī.',NULL,NULL,'2026-09-27 08:00:19');
INSERT INTO "glossary" VALUES(13,'term_013','Mañjuśrī','འཇམ་དཔལ་དབྱངས།','jam dpal dbyangs','འཇམ་དཔལ་དབྱངས།','文殊菩萨','Mañjuśrī Bodhisattva','name','华严经中代表智慧第一的菩萨，与普贤菩萨共为毗卢遮那佛之胁侍。','The bodhisattva representing supreme wisdom.',NULL,NULL,'2026-09-27 08:00:19');
INSERT INTO "glossary" VALUES(14,'term_014','','','','','华藏世界','Lotus Treasury World (Padmagarbha-lokadhātu)','cosmology','毗卢遮那佛所教化之世界，由无量香水海、世界种层层环绕而成。二十重世界，重重无尽。','The universe system presided over by Vairocana Buddha, consisting of incalculable worlds within worlds in infinite interpenetration.',NULL,NULL,'2026-09-27 08:00:19');
INSERT INTO "glossary" VALUES(15,'term_015','','','','','七处九会','Seven Locations and Nine Assemblies','cosmology','八十华严的说法结构。佛于七个地点召开九次法会，依次升进，展转深入华严教义。','The structural framework of the 80-fascicle Avatamsaka: nine assemblies held at seven locations, progressively revealing deeper teachings.',NULL,NULL,'2026-09-27 08:00:19');
INSERT INTO "glossary" VALUES(16,'term_016','bodhicitta','བྱང་ཆུབ་ཀྱི་སེམས།','byang chub kyi sems','བྱང་ཆུབ་ཀྱི་སེམས།','菩提心','mind of awakening / bodhicitta','state','发愿成佛、利益众生的心。华严经以''初发心时便成正觉''彰显发心之殊胜。','The aspiration to attain Buddhahood for the benefit of all beings.',NULL,NULL,'2026-09-27 08:00:19');
INSERT INTO "glossary" VALUES(17,'term_017','','','','','十信','ten stages of faith','state','华严修行五十二位之最初十位: 信心、念心、精进心、慧心、定心、不退心、护法心、回向心、戒心、愿心。','The first ten of the 52 stages of Huayan practice, establishing the foundation of faith.',NULL,NULL,'2026-09-27 08:00:19');
INSERT INTO "glossary" VALUES(18,'term_018','','','','','十住','ten abodes','state','十信之后，安住于佛法正理，不再退转: 发心住、治地住、修行住、生贵住、方便具足住、正心住、不退住、童真住、法王子住、灌顶住。','The ten abodes following the ten faiths, where the practitioner stabilizes in authentic understanding.',NULL,NULL,'2026-09-27 08:00:19');
INSERT INTO "glossary" VALUES(19,'term_019','','','','','十行','ten practices','state','十住之后，广行利他: 欢喜行、饶益行、无瞋恨行、无尽行、离痴乱行、善现行、无著行、尊重行、善法行、真实行。','The ten practices of engaged beneficence following the ten abodes.',NULL,NULL,'2026-09-27 08:00:19');
INSERT INTO "glossary" VALUES(20,'term_020','','','','','十回向','ten dedications / ten transfers of merit','state','十行之后，将一切功德回向法界: 救护一切众生离众生相回向、不坏回向、等一切佛回向、至一切处回向、无尽功德藏回向、随顺平等善根回向、随顺等观一切众生回向、真如相回向、无缚解脱回向、法界无量回向。','The ten dedications of all merit to the Dharma realm.',NULL,NULL,'2026-09-27 08:00:19');
INSERT INTO "glossary" VALUES(21,'term_021','','','','','五教十宗','Five Teachings and Ten Schools (Huayan doctrinal classification)','lineage','法藏（贤首国师）建立的判教体系。五教: 小乘教、大乘始教、大乘终教、顿教、圆教（华严）。十宗进一步细分。','Fazang''s system of doctrinal classification placing Huayan at the apex as the ''Perfect Teaching''.',NULL,NULL,'2026-09-27 08:00:19');
INSERT INTO "glossary" VALUES(22,'term_022','','','','','华严五祖','Five Huayan Patriarchs','lineage','杜顺、智俨、法藏、澄观、宗密。华严宗从初创到完成的五位核心祖师。','Dushun, Zhiyan, Fazang, Chengguan, and Zongmi — the five foundational masters of the Huayan school.',NULL,NULL,'2026-09-27 08:00:19');
INSERT INTO "glossary" VALUES(23,'term_023','Gaṇḍavyūha','སྡོང་པོ་བཀོད་པ།','sdong po bkod pa','སྡོང་པོ་བཀོད་པ།','入法界品','The Stem Array / Entry into the Dharma Realm','scripture','华严经最后一品，也是最宏大的一品。善财童子五十三参，遍历一百一十城，参访五十三位善知识，终入法界。','The final and most extensive chapter, recounting Sudhana''s pilgrimage to 53 spiritual teachers.',NULL,NULL,'2026-09-27 08:00:19');
INSERT INTO "glossary" VALUES(24,'term_024','Bhadracarī-praṇidhāna','བཟང་པོ་སྤྱོད་པའི་སྨོན་ལམ།','bzang po spyod pa''i smon lam','བཟང་པོ་སྤྱོད་པའི་སྨོན་ལམ།','普贤行愿品 / 普贤菩萨行愿赞','The King of Aspiration Prayers / Samantabhadra''s Aspiration','scripture','四十华严末品。普贤菩萨开示十大行愿。藏汉佛教共同尊奉为修行日课。','The aspirational prayer of Samantabhadra''s ten great vows, revered in both Chinese and Tibetan Buddhism.',NULL,NULL,'2026-09-27 08:00:19');
INSERT INTO "glossary" VALUES(25,'term_025','Tathāgatāvataṃsaka','','','','如来华严品','The Tathāgata Avatamsaka Chapter','scripture','藏文《华严经》特有品目（第11品）。位于毗卢遮那品后、如来名号品前。汉文诸译本均无此品。','A chapter unique to the Tibetan Avatamsaka (Ch.11), absent from all Chinese translations. A key translation target of this project.',NULL,'{"en": ["The Tathāgata''s Ornament", "The Buddha''s Garland Chapter"]}','2026-09-27 08:00:19');
INSERT INTO "glossary" VALUES(26,'term_026','bhūmi','','sa','','地 / 阶位','stage / ground','state','菩萨修行的阶位。华严经立十地为根本修行框架。','A stage or level of bodhisattva practice. The Avatamsaka establishes ten bhūmis as the fundamental framework.',NULL,NULL,'2026-09-27 08:00:19');
INSERT INTO "glossary" VALUES(27,'term_027','Daśabhūmika','','sa bcu pa','','十地品','The Ten Bhūmis Sūtra','scripture','华严经核心品目。独立流通时有《十地经》《十住经》等别译本。世亲造《十地经论》注释。','A core chapter of the Avatamsaka, also circulating independently.',NULL,NULL,'2026-09-27 08:00:19');
INSERT INTO "glossary" VALUES(28,'term_028','bhadracaryā','','bzang po spyod pa','','普贤行','good conduct / Samantabhadra''s practice','practice','普贤菩萨所行之广大行愿。以十大愿王为纲领。','The vast practice and conduct of Samantabhadra Bodhisattva.',NULL,NULL,'2026-09-27 08:00:19');
INSERT INTO "glossary" VALUES(29,'term_029','praṇidhāna','','smon lam','','愿 / 誓愿','aspiration prayer / vow','practice','菩萨发自内心深处的誓愿。普贤十大愿为此中最殊胜者。','A solemn vow or aspiration arising from the depths of a bodhisattva''s heart.',NULL,NULL,'2026-09-27 08:00:19');
INSERT INTO "glossary" VALUES(30,'term_030','vihāra','','gnas','','住处 / 法会','abode / assembly location','cosmology','华严经七处九会中佛说法的各个地点。','The locations where the Buddha taught in the Avatamsaka''s seven locations and nine assemblies.',NULL,NULL,'2026-09-27 08:00:19');
INSERT INTO "glossary" VALUES(31,'term_031','','','','','法界缘起','dharma-realm dependent origination (dharmadhātu-pratītya-samutpāda)','doctrine','华严宗核心教义。一切法在法界中互为因果、相即相入、重重无尽的缘起关系。超越业感缘起与阿赖耶缘起，为最究竟的缘起义。','The Huayan school''s core teaching: all dharmas arise interdependently within the Dharma realm in mutual identity and interpenetration.',NULL,NULL,'2026-09-27 08:00:19');
INSERT INTO "glossary" VALUES(32,'term_032','ekayāna','','theg pa gcig pa','','一乘','single vehicle / one vehicle','doctrine','唯一佛乘。华严宗以''别教一乘''判摄华严，谓华严教义超越三乘，直显佛之本怀。','The single Buddha vehicle. Huayan classifies itself as the ''distinct teaching of the One Vehicle'' transcending the three vehicles.',NULL,NULL,'2026-09-27 08:00:19');
INSERT INTO "glossary" VALUES(33,'term_033','avaivartika / avinivartanīya','','phyir mi ldog pa','','不退转','non-retrogressing / irreversible','state','修行达到不再退转的阶位。华严十信满心即入不退转位。','The stage at which spiritual progress becomes irreversible.',NULL,NULL,'2026-09-27 08:00:19');
INSERT INTO "glossary" VALUES(34,'term_034','anuttarā-samyak-saṃbodhi','','bla na med pa yang dag par rdzogs pa''i byang chub','','阿耨多罗三藐三菩提','unsurpassed perfect enlightenment','state','无上正等正觉。佛之究竟觉悟。','The supreme, perfect enlightenment of a Buddha.',NULL,NULL,'2026-09-27 08:00:19');
INSERT INTO "glossary" VALUES(35,'term_035','kuśala-mūla','','dge ba''i rtsa ba','','善根','roots of virtue','doctrine','能生一切善法之根本。包括无贪、无瞋、无痴三善根。','The fundamental roots that give rise to all virtuous qualities.',NULL,NULL,'2026-09-27 08:00:19');
INSERT INTO "glossary" VALUES(36,'term_036','pāramitā','','pha rol tu phyin pa','','波罗蜜 / 到彼岸','perfection / transcendent virtue','practice','菩萨修行之六种或十种究竟行法，从生死此岸度至涅槃彼岸。','The six or ten perfections by which the bodhisattva crosses from saṃsāra to nirvāṇa.',NULL,NULL,'2026-09-27 08:00:19');
INSERT INTO "glossary" VALUES(37,'term_037','dāna-pāramitā','','sbyin pa''i pha rol tu phyin pa','','布施波罗蜜','perfection of giving','practice','六波罗蜜之首。财施、法施、无畏施三轮体空之行。','The first of the six perfections — the practice of giving in its three forms (wealth, Dharma, fearlessness) done with the three wheels (giver, receiver, gift) seen as empty of self-nature.',NULL,NULL,'2026-09-27 08:00:19');
INSERT INTO "glossary" VALUES(38,'term_038','śīla-pāramitā','','tshul khrims kyi pha rol tu phyin pa','','持戒波罗蜜','perfection of ethical conduct','practice','以戒律清净身口意三业，防非止恶之行。','The perfection of ethical conduct — discipline that purifies body, speech, and mind, preventing wrongdoing and upholding goodness.',NULL,NULL,'2026-09-27 08:00:19');
INSERT INTO "glossary" VALUES(39,'term_039','kṣānti-pāramitā','','bzod pa''i pha rol tu phyin pa','','忍辱波罗蜜','perfection of patience','practice','安忍于顺逆之境，心无瞋恼之行。','The perfection of patience — enduring favorable and adverse circumstances with equanimity, the mind free from anger and vexation.',NULL,NULL,'2026-09-27 08:00:19');
INSERT INTO "glossary" VALUES(40,'term_040','vīrya-pāramitā','','brtson ''grus kyi pha rol tu phyin pa','','精进波罗蜜','perfection of diligence','practice','勇猛无间于善法，勤修断恶修善之行。','The perfection of diligence — vigorous, untiring effort in wholesome practice, ceaselessly abandoning evil and cultivating good.',NULL,NULL,'2026-09-27 08:00:19');
INSERT INTO "glossary" VALUES(41,'term_041','dhyāna-pāramitā','','bsam gtan gyi pha rol tu phyin pa','','禅定波罗蜜','perfection of meditation','practice','摄心一境，止观双运，得三摩地之行。','The perfection of meditation — gathering the mind in single-pointed concentration, uniting tranquility and insight in samadhi.',NULL,NULL,'2026-09-27 08:00:19');
INSERT INTO "glossary" VALUES(42,'term_042','prajñā-pāramitā','','shes rab kyi pha rol tu phyin pa','','般若波罗蜜','perfection of wisdom','practice','六波罗蜜之核心。照见诸法实相之无分别智。','The perfection of wisdom and the heart of the six perfections — the non-discriminating wisdom that directly discerns the true nature of all dharmas.',NULL,NULL,'2026-09-27 08:00:19');
INSERT INTO "glossary" VALUES(43,'term_043','Buddhāvataṃsaka','','sangs rgyas phal po che','','华严 / 佛华严','Buddha-ornament / Flower Ornament','scripture','华严经之梵文经题。具称《大方广佛华严经》。''华''喻菩萨万行，''严''喻庄严果德。','The Sanskrit title of the Avatamsaka Sūtra, meaning ''Buddha''s Flower Ornament''.',NULL,NULL,'2026-09-27 08:00:19');
INSERT INTO "glossary" VALUES(44,'term_044','','','','','十信位','ten stages of faith','state','海云法师体系中的十信位果位对应：初信(舍识用根)→二信(确认菩提心)→三信(运用观照技术)→五信(三果)→六信(四果向)→七信(四果·破我执)→八信(发心破法执)→九信(我执法执双破)→十信圆满(照见五蕴空)→入法界。','The ten stages of faith in Venerable Haiyun''s system, each with a fruit-correspondence: initial faith (abandoning consciousness, operating from the sense-base) → second (confirming bodhicitta) → third (applying contemplative technique) → fifth (the third fruit) → sixth (toward the fourth fruit) → seventh (fourth fruit, breaking self-grasping) → eighth (resolve to break dharma-grasping) → ninth (self- and dharma-grasping both broken) → tenth perfected (seeing the five aggregates as empty) → entering the dharma-realm.',NULL,NULL,'2026-09-27 08:00:19');
INSERT INTO "glossary" VALUES(45,'term_045','','','','','能所双泯','dissolution of subject-object duality','doctrine','海云继梦禅观体系核心概念。认识心(能)与所观境(所)的二元对立完全消融，为真如实观的究竟境界。','The complete dissolution of the duality between the cognizing subject and the cognized object.',NULL,NULL,'2026-09-27 08:00:19');
INSERT INTO "glossary" VALUES(46,'term_046','','','','','象限转移','quadrant shift','practice','海云法师禅修术语。从凡夫认知象限转移到行者觉知象限的质变过程，为净化禅到安般守意的关键转折。','A qualitative shift from ordinary cognitive mode to practitioner''s awareness mode.',NULL,NULL,'2026-09-27 08:00:19');
INSERT INTO "glossary" VALUES(47,'term_047','','','','','普贤乘华严宗','Samantabhadra Vehicle Huayan School','lineage','海云继梦法师提出的华严宗新定位。以普贤菩萨行愿为修行总纲，融合华严教观与瑜伽行法。','A contemporary re-envisioning of Huayan by Ven. Haiyun Jimeng, centered on Samantabhadra''s practice.',NULL,NULL,'2026-09-27 08:00:19');
INSERT INTO "glossary" VALUES(48,'term_048','','','','','工程面 / 技术面','engineering dimension / technical dimension','practice','海云法师禅观教学双轨。技术面(修定·身法)：可操作的禅修步骤序列；工程面(修慧·心法)：意识状态的质的转变。','A dual-track teaching approach: technical dimension (operational meditation steps) and engineering dimension (qualitative transformation of consciousness).',NULL,NULL,'2026-09-27 08:00:19');
INSERT INTO "glossary" VALUES(49,'term_049','','','','','安般守意','ānāpāna-smṛti / mindfulness of breathing','practice','数息观。海云法师禅观前行核心法门：数、随、止三法次第。','Mindfulness of breathing, the core preliminary meditation method in Haiyun''s system.',NULL,NULL,'2026-09-27 08:00:19');
INSERT INTO "glossary" VALUES(50,'term_050','','','','','驻佇心观','abiding-mind contemplation','practice','海云法师资粮道根本前行观法。停心于一处，为四种观法之基础。','The foundational preliminary contemplation in Haiyun''s system, settling the mind at one point.',NULL,NULL,'2026-09-27 08:00:19');
CREATE TABLE translation_units (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    chapter_id      INTEGER NOT NULL REFERENCES chapters(id),
    paragraph_num   INTEGER,                               -- 段落编号
    source_text     TEXT    NOT NULL,                       -- 藏文原文 (Unicode)
    source_text_roman TEXT,                                 -- 藏文转写 (Wylie)
    chinese_draft   TEXT,                                   -- 汉译草稿
    english_draft   TEXT,                                   -- 英译草稿
    chinese_final   TEXT,                                   -- 汉译定稿
    english_final   TEXT,                                   -- 英译定稿
    status          TEXT    DEFAULT 'pending',
                    -- pending | draft | review | final
    translator_note TEXT,                                   -- 译注
    has_chinese_ref INTEGER DEFAULT 0,                      -- 是否有汉文对应段落 (用于锚定)
    chinese_ref_id  INTEGER REFERENCES chapters(id),        -- 对应汉文品目
    created_at      TEXT    DEFAULT (datetime('now')),
    updated_at      TEXT    DEFAULT (datetime('now'))
);
CREATE VIRTUAL TABLE texts_fts USING fts5(
    title_zh, title_bo, title_sa, title_en,
    abstract, dynasty, date_text,
    content='texts', content_rowid='id'
);
CREATE VIRTUAL TABLE glossary_fts USING fts5(
    term_zh, term_sa, term_bo, term_en,
    definition_zh, definition_en,
    content='glossary', content_rowid='id'
);
INSERT INTO texts_fts(texts_fts) VALUES('rebuild');
INSERT INTO glossary_fts(glossary_fts) VALUES('rebuild');
CREATE TRIGGER texts_ad AFTER DELETE ON texts BEGIN
    INSERT INTO texts_fts(texts_fts, rowid, title_zh, title_bo, title_sa, title_en,
                          abstract, dynasty, date_text)
    VALUES ('delete', old.id, old.title_zh, old.title_bo, old.title_sa, old.title_en,
            old.abstract, old.dynasty, old.date_text);
END;
CREATE TRIGGER texts_ai AFTER INSERT ON texts BEGIN
    INSERT INTO texts_fts(rowid, title_zh, title_bo, title_sa, title_en,
                          abstract, dynasty, date_text)
    VALUES (new.id, new.title_zh, new.title_bo, new.title_sa, new.title_en,
            new.abstract, new.dynasty, new.date_text);
END;
CREATE TRIGGER texts_au AFTER UPDATE ON texts BEGIN
    INSERT INTO texts_fts(texts_fts, rowid, title_zh, title_bo, title_sa, title_en,
                          abstract, dynasty, date_text)
    VALUES ('delete', old.id, old.title_zh, old.title_bo, old.title_sa, old.title_en,
            old.abstract, old.dynasty, old.date_text);
    INSERT INTO texts_fts(rowid, title_zh, title_bo, title_sa, title_en,
                          abstract, dynasty, date_text)
    VALUES (new.id, new.title_zh, new.title_bo, new.title_sa, new.title_en,
            new.abstract, new.dynasty, new.date_text);
END;
CREATE INDEX idx_chapters_order ON chapters(sutra_id, order_num);
CREATE INDEX idx_chapters_sutra ON chapters(sutra_id);
CREATE INDEX idx_chapters_unique_bo ON chapters(is_unique_to_bo);
CREATE INDEX idx_crossrefs_from ON cross_refs(from_text_id);
CREATE INDEX idx_crossrefs_to ON cross_refs(to_text_id);
CREATE INDEX idx_edges_from ON lineage_edges(from_person_id);
CREATE INDEX idx_edges_lineage ON lineage_edges(lineage_name);
CREATE INDEX idx_edges_to ON lineage_edges(to_person_id);
CREATE INDEX idx_glossary_category ON glossary(category);
CREATE INDEX idx_glossary_sa ON glossary(term_sa);
CREATE INDEX idx_glossary_zh ON glossary(term_zh);
CREATE UNIQUE INDEX idx_locations_source_id ON locations(source_id);
CREATE INDEX idx_locations_type ON locations(type);
CREATE INDEX idx_persons_dynasty ON persons(dynasty);
CREATE INDEX idx_persons_lineage ON persons(lineage_branch);
CREATE UNIQUE INDEX idx_persons_source_id ON persons(source_id);
CREATE INDEX idx_persons_type ON persons(type);
CREATE INDEX idx_texts_cbeta ON texts(cbeta_id);
CREATE INDEX idx_texts_dynasty ON texts(dynasty);
CREATE INDEX idx_texts_taisho ON texts(taisho_no);
CREATE INDEX idx_texts_tohk ON texts(tohk_no);
CREATE INDEX idx_texts_type ON texts(type);
CREATE INDEX idx_texts_yitian ON texts(yitian_status);
CREATE INDEX idx_trans_units_chapter ON translation_units(chapter_id);
CREATE INDEX idx_trans_units_status ON translation_units(status);
COMMIT;
