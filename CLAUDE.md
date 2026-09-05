# CLAUDE.md — 华严宗部文献与修行资料数字化梳理

## 项目概述

构建以华严宗为核心的佛法文献与修行资料数字化系统：
1. **多维知识图谱**：华严宗祖师/行者传承谱系、地理道场、经典关联（**95 人**，30 处地点/道场，**98 条**传承边，24 法系，174 条人物行迹，73 处文明疆域）
2. **多维格义**：梵-于阗-藏-汉-满-英多语对读 + 藏汉华严品目差异比对 (Toh44 45品 vs 汉文39品)
3. **华严宇宙观**：华藏世界海曼荼罗 + 三界诸天图

## Demo

**[web/demo/index.html](web/demo/index.html)** — 导航主页，链接到6个独立Tab页面- Tab 1: **法脉传承**·时空长河 (Canvas时间轴 + 理论/修行图层 + 主地图 + 全球文明迷你地图 + 95节点动画 + 古地图模式 + 174条人物行迹)
- Tab 2: **华严文献**·汉藏差异 (子导航多页: 华严经学/以经证经/判教互判/华严祖师/专题研究 + 三语对读 + 50条术语 + 文本系谱)
- Tab 3: **华严教行** (子导航四页·修行体系/禅观法要/实修心要/讲法资源 + YouTube集成)
- Tab 4: **前沿对话** (AI/计算现象学/神经科学/心灵哲学 + 文献综述)
- Tab 5: **世主妙严** (华藏世界海曼荼罗 + 三界诸天图 + 艺术珍品 + 梵呗)
- Tab 6: **灵性仁本**·澄明永续 (灵性经济学/人本经济学/修行传统与永续/本土知识体系)

## 知识管理架构（三层数据栈）

```
L1: SQLite (权威数据源)  →  L2: db_reader.py (数据服务层)  →  L3: build.py → HTML
```

- **SQLite** (`data/catalog/huayan.db`): persons, texts, chapters, locations, glossary, lineages, lineage_edges + FTS5全文检索
- **db_reader.py** (`scripts/db_reader.py`): 从SQLite读取，输出graph.json兼容格式，供build.py消费
- **YAML/JSON**: 非图谱数据（修行体系/宇宙观/前沿对话等）仍以YAML为权威源
- **策展**: 直接操作SQLite (`scripts/import_all_to_sqlite.py` 多源合并导入)

数据流: JSON/YAML源文件 → `import_all_to_sqlite.py` → SQLite → `db_reader.py` → `build.py` → HTML

详见 [docs/knowledge-management.md](docs/knowledge-management.md)

## 📌 当前进度·下一步（新会话快速上手）

- **进度权威源**：`docs/next-phase-plan.md`（长期待办、待续梯队、历次 L 系列批次登记都在此，**每次任务收尾必更新**）
- **近期已收尾批次**（最近提交，倒序）：⑪华严经学＋判教互判·各自独立地址（㊶——给「华严经学」与「判教互判」各建**可分享独立地址**，依用户指示采**数据驱动全量独立页**方案（参照 chan-traces 的 data_source 模式，YAML 全文渲染成独立 HTML、正文单源存 YAML、零硬编码）：`standalone_articles.yaml` `others:` 新增 **avatamsaka-studies**（📚, data_source avatamsaka_studies, data_pool gap→`articles/avatamsaka-studies.html` 307,367B/54,803 doc 字）与 **panjiao**（⚖️, data_source panjiao_hupan, data_pool gap→`articles/panjiao.html` 150,385B/13,984 doc 字），独立文章 18→20；build.py 新增 `data_pool` 字段 + 通用 `GAP_TOPICS_RENDER`/`renderDynTopics()`（sections+topics schema、节标题+计数、每专题折叠门 wu-door〔默认每节首题展开〕、title_en/intro_en/body/en_body/.en-line 中英对照、sources 复数与 source 单数兼容、links、参考文献、`_dynMD` 内联 md、顶部目录锚点），`build_articles` 按 pool 从 `load_gap()`/`load_practice()` 内嵌 `GAP_DATA`/`PRACTICE_DATA`；verify_demo 数据驱动页判定补认 `var GAP_DATA`+`function renderDynTopics`；build 30 files｜18,743,234 B＋verify_demo ALL CHECKS PASSED（20 文章页全检）＋test_pipeline ALL TESTS PASSED＋headless Chrome CDP 实测两页 44 门/72 门、EN 行/TOC 锚点齐备、0 异常）＋L.㊷（独立页**全宽+分享+判教深度化**——①共通容器 `.content-article` 全宽化 `max-width:min(1500px,96vw)`（原 1080px 宽屏留白致「文字靠左 1/3」，实测 1500px/89% 视口）；②独立页顶栏新增**「🔗 分享地址」按钮**（build.py 模板+`SHARE_JS`+`copyPageLink()`/clipboard→execCommand fallback＋toast 复制提示）；③判教互判深度化 `panjiao_hupan.yaml` 20→23 节、72→95 题、doc 字 13,984→21,358——`world` 3→8 题（犹太教/耆那教/琐罗亚斯德/锡克/巴哈伊）、新增 `dimensions` 判教分析维度·九维方法论（9 题）、`summary` 总结·横向综览（4 题）、`metapanjiao` 华严立场之 meta判教·对诸判教之判教（5 题），逐条中英对照+source 注明出处、references 14→17；④教海行云 `renderPanjiaoSection()` 顶部加「⚖️ 判教互判」article-chip 链接 → articles/panjiao.html；build 30 files｜19,134,477 B＋verify_demo/test_pipeline ALL PASSED＋CDP 判教 24 节/95 门/1500px/三新节齐备/0 异常）⑬㊷续（**华严经学连续全文化（独立页+Tab2 视图同步）＋判教末节非法字符校勘**——①依用户指示以 zhenwei.html 布局重构华严经学：CDP 实测两页容器宽已一致（1500px/1444px），差异在阅读形态（zhenwei 连续全文 vs 华严经学 44 折叠门），用户选定「连续全文·像 zhenwei」，并进一步确认 **Tab2 视图也要连续全文**；独立页 `GAP_TOPICS_RENDER.renderDynTopics(data,mode)` 增 `mode='article'`（面包屑+页头横幅+🧭自动目录〔9 节 gold＋44 题缩进逐题锚点〕+📄全文〔border-left gold 屏风、9 节 h3 计数、每题编号 1. 题名 border-left 蓝子块、body/en_body/📎/🔗全展开〕+参考文献〔_dynMD〕+页脚），默认 `'doors'` 保持折叠门；build_articles 依 a['id'] 传 `'article'`（仅 avatamsaka-studies），ARTICLE 补 icon/title_sub/back；avataramsaka-studies.html 227,149→314,954 B、独立页 CDP 0 折叠门/9 h3/88 逐题锚点/98 EN 行/1500px/0 异常；**Tab2 gap.js `renderAvatamsakaStudies()` 同步连续化**（移除 wu-door 折叠门与 avsDoors 展开/收起控制，改头注+🧭自动目录+连续全文：9 节 h3 计数、每题编号 1. 题名 border-left 蓝子块全展开、参考文献，keep `gv-avatamsaka_studies`/`avs-<sec.id>` 锚点与 articleChip 入口不变；gap.html 3,146,773→3,208,703 B，CDP `switchGapView('avatamsaka_studies')` 实测 display:block/0 门/9 h3/88 锚点/98 EN 行/0 异常）；②判教末节校勘——metapanjiao 导言「末节为全篇之**『振《》』**」（脏写入乱码）依句意订正为「末节为全篇之**纲领**」，整库扫描空《》/空「」/U+FFFD/空〔〕/振X 其余 0 命中；panjiao 仍 95 门 envelope 布局不受影响、0 异常；build 30 files｜19,147,976 B＋verify_demo/test_pipeline ALL PASSED）⑫EN斜杠清理＋引用资源可点化＋判教反斜杠脏字符归一（㊸——①**英文斜杠清理**：judgments 与华严经学两文件 EN 字段斜杠 61→0——名称变体→“A (B)”/“A — B”（Gimello (2005; 1987)、Jigme Lingpa (1729 or 1730–1798)）、成对概念→“A vs. B”/and、期刊卷期 `17/1:1-20`→`17(1):1–20`（4处）`69/4`→`69(4)`（2处）`8/12`→`8(12)`（1处）、表头 `Fascicles/Chapters`→`Fascicles (Chapters)`、`(2007/2021/2026):`→`(2007; 2021; 2026)`（仅EN）；**保留**中文文本斜杠（《十地经论》/《菩萨地》等中文惯例）、URL/DOI、馆藏号 **Or 15010/155**（Hoernle，EN 唯一保留）；EN 字段验证须同时匹配 `*_en`**或** `en_body`（后者不以 _en 结尾易漏检）；②**EN 句误插中文词修复**（约20处：that汇集/and论证/infinite展开/Avataṃsaka境界/causes感/in还原/the导引/Huayan特色/one消融/本来光明/dialogue模式/dual运/The排列; PJ effects延续→continuing、to避→to avoid、is决 not→“is by no means”、念佛samādhi→buddha-recitation samādhi、越来越少→grows fewer and fewer），终检 CJK-in-EN 仅 3 处有意双语注释保留（穿衣吃饭·行路睡觉/口业清净/方便）③**PJ `\"` 渲染脏字符 1014 处归一**（AV 为 0；`\"`→`"` 后 yaml parse 23 节完好、结构不变、0 反斜杠引号 artifact），页面 JSON 仅剩正常转义；④**引用资源可点化**：AV 4 处 references/sources 裸 URL 包成 `[label](url)`（华严专宗学院 huayencollege.org、SEP Huayan Buddhism 2024 entry、Shambhala Cleary全译本）+杨维中 2005（普门学报26期 页85-143）/2002（闽南佛学第一辑）补 **NTU 可点链接**（seq=206722/207530）；PJ 3 处 section source（fjdh.cn 三圣圆融观 / wuming.xuefo.net 金狮子章讲记 / wuming.xuefo.com 天台小止观讲解）同样包链；build.py **doors 模式 references 循环补 `_dynMD`**（原 `'<li>'+r+'</li>'` 致门页参考文献 markdown 链接不可点，article 模式本已支持），门页（panjiao.html）参考文献自此可点；⑤**新原则入册**：编务总则 七条→八条＋新增「**引用可点·出处可溯**」（凡引用资源尽量给可点链接，`[text](url)` 嵌入 YAML sources/references/body 由 `_dynMD` 渲染，无从可点者如实标注〔无链接〕/〔待核〕不硬凑）；build 30 files｜19,143,690 B＋verify_demo/test_pipeline ALL PASSED＋`[label](url)` 8 处内联实测齐备＋JS 正则转换模拟通过）⑩华严经学·起源深研＋三十九品深度批注＋独立页面（㊵——Tab2 华严经学三线深化，详登记见 next-phase-plan：①**起源段由 4 题拓为 10 题**——四阶段重写（Nattier 2005 T280/T281/T282/T283 原始一本拆数本的重建＋Proto 中释迦非毗卢遮那居中）、新增「印度根源」（Skilling & Saerji 2013：印度各品从未作华严整体被引）、新增「印度编纂说」（Seok 2015 五反证/平川彰·大竹晋）、扩「于阗编纂说」（ysa 于阗语指纹/Hamar 皇家赞助）、扩「编辑手法」（Toyobunko 2024 藏译第31/32/43品留独立结尾＝编辑未竟物证）、新增「断代问题」（下限420/上限1-2世纪/Khadaliq 梵文残片叶码382·5-6世纪＝最接近完整华严物证）、扩「于阗故乡」（《于阗国授记》护法/Devendraprajñā）、扩「Bathang写本」（Park 2017）、新增「华严宗形成」五阶段；②**三十九品逐品详解**充入祖师大德批注/学者阐释（每品澄观《疏》/法藏《探玄记》/印顺/方东美/海云继梦等 2-3 家点睛）＋补**八十/六十/四十/藏译四版本对照行**（标「十定品」六十阙·㊲ 六十作「如来兴显经」·㊴ 四十全经即此品·藏译另有二品独有）；③**独立地址**——新建 `docs/华严经学_三十九品深度研究.md`（顶部目录照佛门真伪体例）＋注册 `standalone_articles.yaml` `id: huayan-studies`（back gap/avatamsaka-studies）→ `articles/huayan-studies.html`；独立文章 16→18；build 28 files | 18,280,912 B＋verify_demo ALL CHECKS PASSED＋test_pipeline ALL TESTS PASSED；④**布局优化·折叠门**（gap.js renderAvatamsakaStudies 纯渲染层：9 节 44 题由「单页长墙」改为逐专题**折叠门 wu-door**〔默认仅首节首题展开作阅读入口，贴合既有 L.㊱ 安全模式、无反斜杠〕＋章节名旁计数＋**顶部 sticky 章节导航条**〔avs-nav：各节跳转锚点＋展开全部/收起全部〕＋avsFocus 平滑滚动；内容仍全量来自 avatamsaka_studies.yaml、零硬编码；headless Chrome CDP 实测 44 门/1 默认展开/sticky 条 1/点开显示/点闭合/0 异常；build 18,282,018 B＋verify_demo ALL CHECKS PASSED＋test_pipeline ALL TESTS PASSED）；⑨人员数据深化·未核实人物考证（㉲——`verified=0` 23→**14**：考实升 9 条——魏道儒（《中国华严宗通史》江苏古籍 1998 初版·旧记 2001 有误、2011 当选学部委员）／王颂（《宋代华严思想研究》宗教文化 2008、ISBN 9787801239594）／邱高兴（现任职**中国计量大学**教授院长〔旧记人大已勘误〕·1993-96 人大读博）／张文良（人大哲学院教授·东大博士）４学者 source 升具体书目·T2＋胜友（=Jinamitra 吐蕃译师·T1）／高原明昱（周叔迦《中国佛学史》+《相宗八要解》《明昱诗集》存世）／净海（莲社第五任住持+《老实僧本色》法鼓 2020）／钦因（法名敬缘·1928 北平生·2008 传法海云继梦）／思元慧三（宛平·1901-1986·福慧寺开山）５宗派人物补实；source 去「官网/特刊/著录制」等 VAGUE 词后 4 学者复归 T2、score 76；余 14 条如实留 0（菩提流支卒年诸说·当代无传记 4·系派内梦中授法 5·《元亨释书》孤证 3·谱系自述 1）；import→DB（81 人 0 缺源）→export→build 17,130,669 B；verify_sources/verify_demo/test_pipeline 全绿）①渲染修复·禅观法要折叠块 onclick 语法错误（㊱——根因：`data/practice/chan_contemplation.yaml` 内 17 处 `wu-door` 的 `onclick='...toggle(\"open\")'` 写成带反斜杠 `\"`，单引号属性内属非法 JS 起始 token，点击折叠即抛 `Uncaught SyntaxError: Invalid or unexpected token`；`renderChanContemplation` 经 `h += b.html` 原样注入数据 HTML 即活代码。修复：去掉反斜杠改 `toggle("open")`（17/17），重建 jiaoxing.html，Chrome CDP 实测点击该块 `display:none`→`block` 正常展开且 0 错误、正文含 263 中文字符；全库扫描无 `onclick=...\"` 残留；verify_demo ✅ ALL CHECKS PASSED・test_pipeline 0 失败。「只有英文无中文」系旧缓存/localStorage 语言开关残留（同 L.㉝，刷新即恢复），非数据缺中文）②信息源考证·locations 14 处无来源补证（㉟——14/14 全补 `source`，T0 14→0：T1 原典 5（逍遥园《高僧传》T2059・大慈恩寺/弘福寺《大慈恩寺三藏法师传》T2053・龟兹/那烂陀×2《大唐西域记》T2087）、T2 学术 2（甘丹寺＝谢志斌〈宗喀巴·创建格鲁派〉2022・广州地域泛称）、T3 官网 5（大华严寺 huayen.world・罗摩克里希纳/贝卢尔寺 belurmath.org・东大寺 todaiji.or.jp・Aurobindo ashram・Ramanasramam）、〔待核〕2（台北福慧寺所指未明、阿弥塔巴·LIFE Mission无对应道场——考证优先不臆造）；**源头持久化**三步落地：graph.json 14 条 l_* 补 source＋import_locations 改 `lo.get('source') or gr.get('source')`＋db_reader.load_graph 导出 locations source，重导入/再导出源码全程保留，locations.json 随 load_locations 16→30 条（原 16 条 enriched 字段无损）；locations 30/30 全来源 0 T0；build 17,094,721 B＋verify_demo/test_pipeline ALL PASSED）②双语纵深·批次A/B/C部分（㉞，⚠️推进至此处后按用户指示**先转信息源考证**，双语剩余已登记 next-phase-plan 待续梯队——A批次 SQLite chapters 41 品全补 title_en ［八十华严39品＋藏文独有2品，循 Cleary/84000 通行英译］0/41→41/41，gap.js 品目表补渲染 title_en；B批次 cosmology——cosmo_layers 20 层世界名＋住佛名、three_realms 19 层天＋columns/legend 全补 _en ［含梵文转写 Akaniṣṭha/Tuṣita 等］，cosmology.js 两图下增中英对照折叠表；C批次部分——panjiao_hupan 20 节 72 题＋avatamsaka_studies 5 节 17 题全量 title_en/intro_en/en_body，gap.js renderAvatamsakaStudies/renderPanjiaoHupan 补渲染，顺带修 panjiao_hupan 的 YAML 语法问题（星号被解析为 alias、单引号内撇号）与 4 处 title_en 冒号未引号；build 17,088,370 B，verify_demo ALL CHECKS PASSED；_en 键 translation 103→242 ・ cosmology 41→107）②①独立文章/全站英文不显示修复（㉝——根因：浏览器 localStorage 残留全站「仅中文」开关 site_lang=0 与文章页 article_en_hide=1，common.js 载入读它给 body 加 zh-only 以 display:none!important 永久隐藏全站英文块；数据本身完整，vijnana-mind 72 引用块/69 EN 块实测渲染正常；修复：src/common.js + src/article.js 阅读语言开关改「会话级 sessionStorage」——默认恒为中英对照，仅中文只影响当前标签页会话、关标签即恢复，载入不再读旧值，切换时 removeItem 清理旧 localStorage；重建全站，verify_demo ALL CHECKS PASSED，用户免清缓存刷新即恢复英文显示）②双语纵深三批收官（㉚ complete_catalog.yaml 51 条＋3 主经共 54 条补齐 	itle_en 3/54→54/54，import_texts 补幂等 UPDATE，SQLite/db_reader 全 54/54；㉛ source-audit T3 36→10——36 注册目标依 id 替换源（26 升 T1/T2、10 如实保留 T3）＋扩展补 20 条非注册 T3 共 56 条，评分 68→76，并修 import_edges 主循环补 source=graph.json` 使 DB 98 边 0 缺源；㉜ 善财 L-C 闭环——docs/善财五十三参深度研究.md §3.1 表 9/10、21/22、31-39、41-50 行（梵名＋地点＋中文名）依 CBETA T279 原文＋84000 术语表音写（Vāsantī/Gopā/Sarvajagadrakṣāpraṇidhānavīryaprabhā 等；84000 站点直连不通已绕过）填完，第 38 参校正为「大願精進力救護一切眾生主夜神」，编次注按 T279 v73 校正，文档〔待核〕清零；全链路 import→verify→build→verify_demo ✅ ALL CHECKS PASSED，6 tab 变更经 JSON 层核对仅为 src/title_en 数据衍生非损坏/非回退）③Tab4 前沿对话·条目级 EN 补齐（㉙ `frontier_dialogue.yaml` 19 域 83 条 related 学者卡全补 `description_en`＋45 条中文机构/人名 `affiliation_en`/`name_en`，循全站术语表逐条对译；frontier.js related 卡 EN 副行 `.en-line` 渲染，域级+条目级 EN 至此齐备，build 16,498,369 B）；④人员数据深化·锚点错位勘误+考证实录（㉘ 修正 ㉗ 日系 edit 锚点错位——审祥 person_050 实未翻青翻为 1＋补「精選版大辞典：742没」注、良弁 source 还原「（有773/774异说）」、实忠 verified 回到 0；菩提流支死年 527 与《续高僧传》「至天平二十余年」（534-537 仍在译经）抵触→留空〔待核〕注明卒年诸说未定；慧果灌顶名考证闭环——「遍照金刚」系弟子空海所受，惠果本人无通行梵文灌顶名，name_sa 如实留空；固化人名级 edit 以 name_zh 唯一锚定惯例）；⑤人员数据深化·verified 回填二度（㉗ `verified` 54→72——慈舟 1877-1958/慧苑 673-743/均如 923-973/子璿 965-1038/元晓 617-686/慧光 468-537/真禅 1916-1995/虚云 1840-1959/净慧 1933-2013/南怀瑾 1918-2012/良弁 689-774/圣宝 832-909/明惠 1173-1232/凝然 1240-1321/审祥 d.742/马鸣 80-150/无著 310-390/海云继梦 b.1950 共 18 条逐条考实回填，来源与〔并存/约〕见批次登记；菩提流支〔卒年诸说未定〕、当代学者、大华严寺瑜伽行法脉〔普拉梵纳德等系派内传承记录〕保持 0 待核）；⑥人员数据深化·确证子集（㉖ 龙树生卒补实 150/250 + `verified` 回填 43→54——月霞/常惺/南亭/成一/智光/应慈/了中/持松/贤度/梦参/龙树 逐条考实；考证确证**玄奘无梵文个人名**（Mahāyānadeva/Mokṣadeva 系称号），name_sa 保持 30/95 不臆补；顺带修复 `import_chapters` INSERT→OR REPLACE 既有非幂等瑕疵）；⑦lineage.js 遗留 curated 数据迁移·三块清零（㉕ `dynasties` 时间轴代色带 6 段→`timeline_dynasty_bands.yaml`、`_huayanCore` 6 核心id→`huayan_core.yaml`、`_MINI_REGIONS` 10 区域→`mini_map_regions.yaml`，lineage.js curated 数据清零）；⑧init.js `_aliases` 搜索别名映射数据化（㉔ 硬编码 10+2 组人名别名迁入 `data/events/search_aliases.yaml`→build 注入 SEARCH_ALIASES，init.js 零硬编码）；⑨lineage 人名 EN 数据回填·59/59 清零+全站人名英译校正（㉓ personas.json 15 条补全+44 条 graph-only 入册，**95 人全部有 name_en**（name_sa 30/95）；顺带把 ㉑㉒ 误植的全站错体「Haiyun Jihong/Jirong」统一校正为官方正体 **Haiyun Jimeng**（大华严寺 huayen.world 官方英文站核实），并修正固定术语表）；⑩Tab3 华严教行 res-sources 出处表清零+孤儿数据激活（㉒ practice.js 尾段书目/播客/链接表迁入已载入未渲染的 `meditation_essentials.reference_table`——激活死数据+删硬编码双收，中文零回归+全量 EN）；⑪Tab3 practice.js 遗两块硬编码清零（㉑ renderYikongSection 法脉传承表 11 行 + 最新动态一句式 迁入 `yikong_daodi.lineage_table` / `teaching_resources.latest_news`，中英对照）；⑫Tab2/Tab5 死码覆盖清零（⑳ cosmology.js 华藏世界海+三界诸天、gap.js 总览/差异卡/案例/学界观点/84000方法论 全部接入 COSMO_DATA/GAP.content）；⑬lineage.js 死码覆盖清零续扫（⑲ TRANS_STORY/OTHER_SCHOOLS/geoFeatures 3 处亦清零，共 11 处数据驱动）；⑭lineage.js 死码覆盖清零·8 个 YAML 全局接入（⑱，a4eff3e）；⑮‘内容采集与编务总则’七条固化（6d934d8）
- **当前下一步（见计划待续梯队）**：①信息源考证·locations 已 30/30 全来源、**0 〔待核〕**（㉟ T0 14→0；㊱后续又把最后 2 处〔待核〕考证闭环——663 台北福慧寺＝树林福慧寺（新北市树林区三兴路77号，官网 fuhuisih.org＋大华严寺官网＋成观《华严法门集要》序），674 阿弥塔巴·LIFE Mission＝印度 LIFE Mission（Lakulish International Fellowship's Enlightenment Mission，胜师子王菩萨/Swami Rajarshi Muni 1993 创立于古吉拉特邦，官网 lifemission.org.in；系印度瑜伽·印度教拉克鲁希传承机构，非正统佛教道场——此即原「无对应正规佛教道场」的根因，边界已如实说明；source/city/province 已入库，T0=0、verify_sources/verify_demo/test_pipeline 全绿）；双语/多语续推已登记 next-phase-plan ㉞ 待续梯队——批次C余 gap_content/diff_matrix/intertextual_canon/huayan_masters EN＋gap.js 概览硬编码重构、批次D practice references EN、批次E locations name_en、title_sa/title_bo 多语、person bio EN；②人员数据深化——17 条 no_dates person 保持留空〔待核〕（世亲/支娄迦谶/般若/胜友/智军等古代译师无个人生卒可考、燃灯佛/迦叶佛/毗卢遮那佛/六师外道等神话·集体人物本无年代）；`verified=0` 已由 41→23→**14**（㉗ 回填 18 条、㉘ 勘误后净数不变、㉲ 未核实人物考证再升 9 条——魏道儒/王颂/邱高兴/张文良 4 学者 source 升具体书目·T2＋胜友/高原明昱/净海/钦因/思元慧三 5 宗派人物补实，score 76/100），余 14 条为菩提流支〔卒年诸说未定，527 已删留空〕/明度·体佛·如孝·雪窦〔当代无成卷传记〕/拉克鲁希·巴布基·克利普梵纳德·胜师子王菩萨·普拉梵纳德〔系派内传承·梦中授法〕/实忠·等定·观贤〔日本《元亨释书》孤证〕/体化性果〔谱系自述〕，无力考者保持 0+注明；name_sa 65 缺中多为中文/日系人名本无梵文名（〔待核〕留空），慧果灌顶名考证已闭环（本人无通行梵名，留空）；③`import_chapters` 非幂等已于㉖修复（OR REPLACE，重导入已验证通过）；Tab2-6/article.js 已证实数据驱动无 stray 硬编码；④双语纵深——经目 title_en 全 54/54（㉚）、T3 来源 36→10（㉛）、L-C 善财〔待核〕闭环（㉜）均已完工；后续补 title_sa/title_bo 多语（title_sa 6・title_bo 1，多语不全待补），source-audit T3 余 10 条系无独立史料者（明度/体佛/如孝/雪窦/成观/拉克鲁希/巴布基/克利普梵纳德/思元慧三/体化性果）保持〔待核〕/〔待考〕，L-B 专题定值复审（推广至杜顺/智俨/李通玄/梦参/文殊普贤等专题）未二轮
- 所有内容/进度/原则详见下方文档索引与「内容采集与编务总则」八条，新会话按需读取即可接续

## 核心文档索引

| 文档 | 路径 | 说明 |
|------|------|------|
| 后续计划 | [docs/next-phase-plan.md](docs/next-phase-plan.md) | v2.0重构 P0-P4 路线图 |
| 架构设计 | [docs/architecture.md](docs/architecture.md) | 三层数据栈、数据模型、模块职责 |
| 知识管理 | [docs/knowledge-management.md](docs/knowledge-management.md) | SQLite/Neo4j/YAML三层规范 |
| **参考文献管理** | [docs/reference-management.md](docs/reference-management.md) | 文献知识库维护规范 (新增) |
| 工程工作流 | [docs/engineering-workflow.md](docs/engineering-workflow.md) | Loop/Graph Engineering |
| 翻译规范 | [docs/translation-guide.md](docs/translation-guide.md) | 藏汉对译玄奘体规范 |
| 多语对读 | [docs/multilingual-alignment.md](docs/multilingual-alignment.md) | 梵-于阗-藏-汉-满-英对读架构 |
| 校验框架 | [docs/verification-framework.md](docs/verification-framework.md) | 三级来源分级 + 验证状态机 |
| 可视化研究 | [docs/visualization-research.md](docs/visualization-research.md) | 系谱可视化方案分析 |
| 海云体系 | [docs/ref海云继梦法师_佛法修行体系研究.md](docs/ref海云继梦法师_佛法修行体系研究.md) | 外部参考文档（只读） |
| **文殊普贤信仰** | [docs/文殊普贤信仰专题研究.md](docs/文殊普贤信仰专题研究.md) | 二圣信仰专题（梵藏汉英·艺术·修行） |
| **善财五十三参** | [docs/善财五十三参深度研究.md](docs/善财五十三参深度研究.md) | 五十三参版本考·地理考·心地境界·象征结构 |
| **李通玄长者** | [docs/李通玄长者_综合深度研究.md](docs/李通玄长者_综合深度研究.md) | 长者生平·著作·思想·与五祖关系·历史影响 |
| 华严二祖综合 | [docs/华严宗二祖智俨_综合深度研究.md](docs/华严宗二祖智俨_综合深度研究.md) | 智俨综合研究（合并二祖研究） |
| **梦参长老** | [docs/梦参老和尚_综合深度研究.md](docs/梦参老和尚_综合深度研究.md) | 梦参综合研究（1915-2017·华严/地藏·信源分级+存疑标注） |

## 技术栈

- **前端 Demo**: 纯 HTML/CSS/JS + Canvas + Leaflet (CDN), 6个独立HTML页面
- **数据库**: SQLite 3 (权威数据源) + Neo4j (图验证)
- **数据交换**: YAML/JSON → build.py 构建内嵌
- **ETL**: Python 3.12 (conda env: `hy_py312`)
- **部署**: 本地双击 → GitHub Pages

## ⚠️ 工程核心原则

0. **考证优先（Verification First）** — ⭐内容与信息依据的考证、确认永远是**最前提、最重要**的事，优先于一切功能与进度：一切数据、结论、名号、数字、参次、年代、地点必须先经一手典籍（CBETA/T84000/原始文献）或权威来源对勘；一时无法确认者必须明确标注〔待核〕/〔存疑〕并如实说明，严禁编造、猜测或以"约第XX参"式占位充数。宁可内容少而可靠，不可多而失实。
1. **知识图谱驱动** — 所有开发、管理、维护以结构化知识图谱（SQLite + YAML）为核心，不依赖手工编码的数据

## ⚠️ 内容采集与编务总则（八条，后续所有新增内容必须遵守）

0. **一口优先·还原分级真实性** — 凡采用的信息来源，**尽可能使用第一手材料**（CBETA/T84000/原始文献/一手档案与采访）；无法直取一手者用可靠二手并据实注明。凡**存疑者必须标明〔待核〕/〔存疑〕**；凡**线索性、局部、信息不充分者必须标明〔线索〕/〔待补〕**，如实交代信息边界，严禁把半成品当作定论。
1. **中英必配·多语酌情** — **凡新增内容，一律同时提供中文与英文各一版本**（映照全站 `.en-line` 中英对照机制）；其他语言（梵/藏/于阗/满/日/韩…）视具体情况酌情使用，不勉强、不硬凑。凡暂无把握之译名照「多语 EN 翻译原则」明示标注。
2. **多译本并存·考据成一** — 凡同一内容存在**多个翻译/版本**（如异译、异本、品目卷数分歧、译名异写），尽可能**梳理清楚并存版本、说明取舍依据与考据出处**，不得只取其一而隐去其余、更不得把某一家译法冒充唯一标准；多版本难以裁决时保留并行并注〔并存/待考〕。
3. **严禁假信息** — **千万避免使用假信息**：不编造年代/地点/名号/引文/数字/参次，不虚构出处，不把口耳相传或二手转述冒充原典；凡来源不明或无法核实者，宁可留白并标注，也不以虚构填充（与考证优先原则互证）。
4. **穷尽采集·分层落地** — **尽可能穷尽信息**；当信息量过大时，先**收集与梳理信息来源、登记入后续计划（docs/next-phase-plan.md）**，分批次慢速提取与实现，不因求全而牺牲可靠性，也不因求快而遗漏来源。
5. **进度留痕·计划滚动** — **每完成一个任务，记得更新进度与下一步计划**：在 `docs/next-phase-plan.md`（及必要的 `docs/*.md`/README）如实登记已完成项、构建/校验结果、遗留问题与**下一批待办梯队**，使项目状态可持续交接、不因会话结束而丢失上下文；新登记内容同时遵守 0-4 及各原则。
6. **边界自知·局限留档** — **清楚自己的局限在哪里，主动暴露信息与方法论的边界**：凡**采集不到、采集不全、有待进一步考察、或受工具/语种/一手资料可得性所限无法确认**之处，一律如实登记（标〔待核〕/〔线索〕/〔无法获取〕，并注明**为何受限**：如史料散佚、语种不通、一手文献未见、核对工具缺失等），纳入 `docs/next-phase-plan.md` 的待考梯队；既不夸大已掌握的信息，也不隐瞒盲区——这些记录即为后续**自我完善与进化的路线图**，使后续工作能针对性地补采、补考、补译。
7. **引用可点·出处可溯** — **凡引用资源（参考文献/出处/链接/经号等），尽量给出可点击链接**（CBETA Online `https://cbetaonline.dila.edu.tw/zh/T10n0279`、84000、NTU 佛学图书馆、出版社/官网等权威 URL），以 `[text](url)` 标记嵌入 YAML 的 `sources`/`references`/`body` 字段，由 `_dynMD` 渲染为可点链接（build.py `GAP_TOPICS_RENDER` 与 gap.js 均已支持；纯文本 URL 优先包成 `[label](url)`）；一时无稳定 URL 或无法直连者，如实标注〔无链接〕/〔待核〕，不硬凑虚假链接（与考证优先/严禁假信息互证）。

> 注：以上与「考证优先」（工程核心原则 0）及「多语 EN 翻译原则」互证互补；英文传导、译名规范具体仍循「多语 EN 翻译原则」七条执行。
2. **源头治理** — 问题在数据源头（SQLite/YAML）解决，不下游修补
3. **灵活优先** — 架构设计以可扩展性为第一优先级，新内容 = 新数据行，不改代码
4. **杜绝硬编码** — 数据进 SQLite/YAML → build.py 读取 → 前端渲染，禁止在 JS/HTML/Python 中写死任何内容

## ⚠️ 知识管理核心规则

**所有展示内容必须来源于结构化源文件或SQLite数据库，严禁硬编码在 build.py 或 JS 中。**

| Tab | 内容类型 | 权威源 | 交换格式 |
|-----|---------|--------|---------|
| 法脉传承 | 人物/边/地点 | SQLite persons表 | graph.json |
| 法脉传承 | 事件/动画/传播 | `data/events/*.yaml` | graph.json (扩展) |
| 华严文献 | 差异矩阵/术语 | SQLite chapters/glossary表 | gap.json |
| 华严文献 | 案例/观点/方法论 | `data/translation/gap_content.yaml` | gap.json (扩展) |
| 华严文献 | 经学/对读/祖师/判教 | `data/translation/avatamsaka_studies.yaml` `intertextual_canon.yaml` `huayan_masters.yaml` `panjiao_hupan.yaml` | gap.json (扩展) |
| 华严文献 | 专题研究 (整篇docs/*.md注入) | `data/translation/topic_studies.yaml` + `docs/佛门真伪问题_综合深度研究.md` 等 | gap.json (扩展: topic_studies) |
| 全站 | **独立文章页** (每篇完整文章独立URL) | `data/translation/standalone_articles.yaml` (sources: topic_studies+huayan_masters 自动展开; others 显式登记整篇 docs/*.md) | `articles/<id>.html` (build.py生成, 全Tab页内嵌 `var ARTICLES` 提供入口条) |
| 华严教行 | 修行体系 | `data/practice/*.yaml` | practice.json |
| 前沿对话 | 文献/论文 | `data/frontier/*.yaml` | frontier.json |
| 世主妙严 | 宇宙观/艺术 | `data/cosmology/*.yaml` | cosmology.json |

**新增内容流程**: ①SQLite INSERT/UPDATE 或 YAML → ②导出脚本 → ③build.py构建 → ④验证人数/边数 → ⑤提交

## ⚠️ 多语 EN 翻译原则（与全文校对结合，重实质不逐字）

本项目的 EN 对照（全站 `*_en` 字段）遵循以下原则，作为后续所有翻译批次的统一约束：

0. **翻译与校对结合、不偏废** — 翻译产出必须纳入完整质量门禁：术语表一致性、教理准确性、考证优先（〔待核〕/〔存疑〕标注、严禁编造史实/观点）、结构/引号安全。翻译≠成稿，一律经主编全文审查后再 render/commit。
1. **重实质、不逐字** — 多语言之间的对应，注重的是**实质内容的对应和准确**（义·理·境的对等），不须拘泥于逐字翻译。意译优先于直译，只要名相所指与教理判断不偏离即可；译名仍循全站固定术语表保持一致。
2. **考证与来源分级** — 一切 EN 内容不得超出中文正文范围，不得新增文件里没有的年代/地点/史实/观点；一时无法确认者标〔待核〕。引用文献/语录有英文原文者照用原题原句；祖师/法师语录正文保持中文原文（zh-only），EN 用最精到阐释转述。
3. **固定术语表** — 全站统一译法（五种姓=five lineages/gotras、三性三无性、八识=eight consciousnesses、阿赖耶识=ālayavijñāna、十玄=ten mysterious gates、华严三昧=Huayan samādhi、五教止观=five teachings of calming and contemplation、即身成佛、三密、法界=dharmadhātu……详见会话里程碑）。人名照拼音/梵文通行拼写（玄奘=Xuanzang、法藏=Fazang、杜顺=Dushun、海云继梦=Haiyun Jimeng（繼夢=jìmèng→Jimeng，循其官方英文网站大华严寺/世界华严总会 huayen.world 与 Triple Crane lineage 页正体）……）。
4. **EN 渲染约定** — EN 块一律 `.en-line` 随全局显隐（默认中英对照）；正文级 EN 块前缀 📖；标题/主题副行 `title_en`、intro 用 `intro_en`、正文用 `en_body`；引用文献英文原文照用。
5. **YAML 转义纪律** — ①单引号串内 `\'` 非法，用 `''`；②单引号串内撇号（Buddha's）会提前闭合——用双引号串或 `''`；③双引号串内嵌双引号须转义；④双引号包裹含中文「」的字符串会被拆坏——用单引号或 `''`；⑤`en_body`/长 EN 一律用 `|` 块标量（4空格 key / 6空格内容），**禁止单引号包裹英文长文本**；`title_en` 含冒号或撇号必须双引号包裹。
6. **翻译 API 仅作辅助** — 以文本质量为优先对象，在线翻译（如 GLM-4-Flash 免费档）仅作上量初稿辅助、可插拔（无 key 自动回退子代理著写），质量门禁与主编审查始终保留、不因接入 API 而放松。详见 `docs/engineering-workflow.md`「多语 EN 翻译管线」。
7. **正式用词·不硬翻·不幻觉·无对应即明示** — EN 名相一律采用**学界与佛界通行的正式用词/固定术语表**（梵文转写优先，如 śamatha、vipaśyanā、cittamātra、dharmadhātu；专名循全站统一译法）。严禁「字面硬翻」与「自造译名」——不得因中文某词没有思路而凭空组合不存在的英译（例如将经名拆字硬拼），也不得在 EN 中臆造文件里没有的年代/地点/史实/观点。凡学界/佛界**无通行对应译名或暂无把握者**，必须明示标注（〔待核〕/〔无通行英译〕＋保留原名或给出带「本文暂译」的说明），而非硬译充数。

## 目录约定

```
huayan_collection/
├── web/demo/
│   ├── index.html              # 导航主页（构建产出）
│   ├── css/common.css          # 共享样式（构建产出）
│   ├── js/common.js            # 共享脚本（构建产出）
│   ├── tabs/                   # Tab页面（构建产出）
│   │   ├── lineage.html        # Tab1 法脉传承
│   │   ├── gap.html            # Tab2 华严文献
│   │   ├── jiaoxing.html       # Tab3 华严教行
│   │   ├── frontier.html       # Tab4 前沿对话
│   │   └── cosmology.html      # Tab5 世主妙严
│   ├── articles/               # 独立文章页（构建产出, 每篇一个URL）
│   │   ├── index.html          # 独立文章目录
│   │   └── <id>.html           # 如 zhenwei / master-fazang / mimi
│   ├── src/                    # 源文件（供build.py组装）
│   │   ├── data.js             # 数据占位 + 全局变量
│   │   ├── lineage.js          # Tab1 Canvas/Map/Select/Interact
│   │   ├── gap.js              # Tab2 汉藏差异
│   │   ├── jiaoxing.js         # Tab3 华严教行
│   │   ├── frontier.js         # Tab4 前沿对话
│   │   ├── cosmology.js        # Tab5 宇宙观
│   │   ├── article.js          # 独立文章页渲染器
│   │   ├── init.js             # 初始化 + 评论系统 + GitHub认证
│   │   └── common.css/js       # 共享样式/脚本模板
│   ├── data/                   # 构建产出的JSON（build.py写入）
│   └── scripts/build.py        # 构建脚本
├── data/                       # 数据文件
│   ├── catalog/                # SQLite Schema + 种子SQL + huayan.db
│   ├── knowledge_graph/        # JSON（从SQLite导出）
│   ├── translation/            # YAML（差异矩阵·术语库·gap内容）
│   ├── practice/               # YAML（修行体系·禅观法要·讲法资源）
│   ├── frontier/               # YAML（跨界对话·文献综述）
│   ├── cosmology/              # YAML（华藏世界海·三界诸天·艺术珍品）
│   ├── events/                 # YAML（历史事件·动画节点·传播故事）
│   └── references/             # 参考文档
├── docs/                       # 项目文档
├── scripts/                    # 导出/验证/Neo4j脚本
│   ├── init_db.py              # SQLite初始化
│   ├── import_all_to_sqlite.py # 多源JSON→SQLite合并导入
│   ├── db_reader.py            # SQLite→JSON数据服务层
│   ├── export_sqlite_to_json.py # 导入/导出/验证
│   ├── test_pipeline.py        # 全链路数据一致性测试
│   ├── verify_demo.py          # 构建产物验证
│   ├── verify_sources.py       # 来源可靠性验证
│   └── load_neo4j.py           # Neo4j加载+验证
└── src/                        # Python后端（待实现）
```

## 快速命令

```bash
# 初始化/导入数据
python scripts/init_db.py                    # 初始化空数据库
python scripts/import_all_to_sqlite.py       # 多源JSON→SQLite导入
python scripts/export_sqlite_to_json.py --verify  # 数据完整性验证

# 图验证: SQLite → Neo4j + Cypher检查
python scripts/load_neo4j.py --verify-sqlite  # SQLite直接图验证（无需Neo4j服务器）
python scripts/load_neo4j.py --generate       # 导出Cypher脚本
python scripts/load_neo4j.py --verify         # Neo4j在线验证（需服务器）

# 来源可靠性验证
python scripts/verify_sources.py

# 全链路测试
python scripts/test_pipeline.py              # 数据一致性测试

# 构建Demo (6个HTML + CSS + JS)
python web/demo/scripts/build.py

# 构建产物验证
python scripts/verify_demo.py
```
