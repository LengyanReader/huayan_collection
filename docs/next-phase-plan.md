# 项目后续计划

> 2026-08-05 | 基于 Demo v2.0 重构计划 — 多页面+SQLite+Neo4j+布局重构

---

## 一、当前状态总览

### 整体数据

| 维度 | 数据 |
|------|------|
| 人物 | **92人**（印度源流+华严五祖+高原法系+华严莲社+月霞系+日本华严+高丽华严+临济宗+译师+学者+参考线） |
| 传承边 | **96条**（MASTER/INFLUENCED/LINEAGE/CONTEMPORARY） |
| 地点 | 46处（含大华严寺/福慧寺/东大寺/支提山/那烂陀等） |
| 人物行迹 | **174条**（从YAML person_trajectories 加载） |
| 西方文明事件 | **45条**（古希腊→中世纪→近代→当代，含坐标）+ **73处**文明疆域 |
| 术语 | **50条**（梵藏汉对照 glossary） |
| 历史事件 | 44条（远源/宗教/义学/翻译/禅观/宗派/文化/法难/教育/传承/当代） |
| 动画节点 | 85个（吠陀→奥义书→释迦生平→佛教东传→华严宗→近现代→2026） |
| Tab数 | **5个** |
| 构建 | 6个HTML（独立构建产出） |

### Tab1 法脉传承

| 功能 | 状态 |
|------|------|
| Canvas分层时间轴（64px行距·HiDPI） | ✅ |
| 人物寿命条 + 类型图标[祖/译/学/修] + 可靠性标记(✓/°) | ✅ |
| 死亡→出生贝塞尔传承连线(颜色编码:师徒金/法脉绿/影响蓝) | ✅ |
| 多法脉Ghost显示（虚线轮廓+↳前缀） | ✅ |
| 理论演化带 + 修行谱系带 | ✅ |
| 朝代色带+标签 | ✅ |
| 时代括号标注 | ✅ |
| 地理标记+流动箭头 | ✅ |
| 44条历史事件（10类彩色圆点+图例） | ✅ |
| 语义缩放（千年全景密度图 ←→ 个人传记细节） | ✅ |
| 悬停高亮关系网 + 点击法系行聚焦 | ✅ |
| 主地图 + 西方文明+华严路线双迷你地图（flex并排） | ✅ |
| 古地图模式（sepia+地形+朝代疆域+古地名+世界文明疆域） | ✅ |
| 85节点动画播放（速度可调+地图联动+状态栏） | ✅ |
| 7宗派辅助标记 | ✅ |
| 传播故事串讲 | ✅ |
| 5图层独立开关 | ✅ |
| Shift+点击双人对比 | ✅ |
| 时间书签 + 法系筛选 + 搜索 | ✅ |
| 统计摘要栏 + 增强信息面板+浮动弹窗 | ✅ |
| 移动端适配 + 触摸滚动 | ✅ |

### Tab2 华严文献

| 功能 | 状态 |
|------|------|
| 版本对照表（4版） | ✅ |
| 差异分布卡片 + 逐品详情 | ✅ |
| 文本变异案例（4例） | ✅ |
| 学界观点 + 共识度表 | ✅ |
| 术语梵藏汉对照（30条→目标50条） | ✅ |
| 结构组织差异（七处九会 vs 连续品目） | ✅ |
| 84000六类文本变异方法论 | ✅ |
| 对译优先级 | ✅ |
| 子导航四页（差异总览/原文对读/文本系谱/参考文献） | ✅ |
| 十地品三语对读 + 入法界品对读 | ✅ |
| 十地品84000校勘注摘录 | ✅ |
| 版本时空演进（13版本节点） | ✅ |
| 文本系谱（60+部经典网络+CBETA链接） | ✅ |

### Tab3 华严教行（原华严行法·2026-08 重构更名）

| 功能 | 状态 |
|------|------|
| **子页1·修行体系**：三阶段卡片/蓝图/六科/五大行法/法脉分工/四大工程/识根智/三缘念/最新动态/演进脉络 | ✅ |
| **子页2·禅观法要**：体系总览/次第道圆融道+十大愿王/资粮道/前行(参禅金三角+双轨详解+四种观法+十信法门+三重观照)/正行(法界三观+四次灌顶+三摩地)/五教止观/贤首五教仪/一乘不共别圆/华严三品行法/金师子章/心要法门/验证机制+关键原则/完整出处表 | ✅ |
| **子页3·实修心要**：微信公众号文章三栏对照(原文/华严对照/他宗印证)+编辑标注 | ✅ |
| **子页4·讲法资源**：全网总目/9主题分类(YT+B站+播客)/著作清单/YouTube频道+最新系列/学术活动/道场 | ✅ |
| YouTube频道集成 (@huayen-world + RSS) | ✅ |
| 大华严寺官网「修行蓝图」2025.11版对齐 | ✅ |
| 全篇58处精确日期标注+引述语境标注 | ✅ |
| WIP内容声明 | ✅ |

### Tab4 前沿对话

| 功能 | 状态 |
|------|------|
| 四板块跨界对话（AI/计算现象学/神经科学/心灵哲学） | ✅ |
| 2023-2026多语文献综述 + 研究趋势 + 批判性评估 | ✅ |
| 子导航双页（跨界对话/文献综述） | ✅ |

### Tab5 世主妙严

| 功能 | 状态 |
|------|------|
| 🪷 华藏世界海·同心曼荼罗（20层世界+风轮+香水海+毗卢遮那） | ✅ |
| 🕸 因陀罗网交互开关 + 📋 全部层名显示 | ✅ |
| 点击世界层查看详情（佛名+经文引述） | ✅ |
| 滚轮缩放（0.4×~3×） | ✅ |
| 📐 三界诸天图·二十八天层叠塔（无色/色/欲界+人间） | ✅ |
| 🎨 华严艺术珍品（9组折叠目录） | ✅ |
| 🎵 梵呗·华严四十二字母（B站+YT嵌入） | ✅ |
| 🗺 华严古迹巡礼（6处+多媒体+参考书目） | ✅ |

---

## 二、v2.0 重构优先级

### P0 — 知识管理基础+数据迁移（当前阶段）

| 任务 | 说明 | 状态 |
|------|------|------|
| **SQLite数据库初始化** | 执行schema.sql，创建huayan.db | 🔴 待实施 |
| **JSON→SQLite迁移** | 现有personas/lineages/locations.json → SQLite | 🔴 待实施 |
| **build.py硬编码→SQLite** | ~30人+~30边+~10地从build.py移入SQLite | 🔴 待实施 |
| **Neo4j图验证管线** | SQLite→Neo4j加载+连通性/完备性/一致性Cypher | 🔴 待实施 |
| **SQLite→JSON导出脚本** | export_sqlite_to_json.py | 🔴 待实施 |
| **lineage.js数据→YAML** | ANIM_WAYPOINTS等10组数据→data/events/*.yaml | 🔴 待实施 |
| **法脉动画地图联动完善** | 当前使用简化地图布局，动画双地图同步待恢复 | ✅ 已完成 |

### P1 — 多页面+布局重构（当前阶段）

| 方向 | 内容 | 状态 |
|------|------|------|
| **多页面拆分** | 单HTML→6个HTML(index+5tabs) | ✅ 已完成 |
| **共享CSS/JS提取** | common.css+common.js | ✅ 已完成 |
| **Tab2布局重构** | 华严文献 sidebar+content双栏 | ✅ 已完成 |
| **Tab3布局重构+更名** | 华严行法→华严教行，sidebar双栏 | ✅ 已完成 |
| **Tab4布局重构** | 前沿对话 sidebar双栏 | ✅ 已完成 |
| **Tab5布局重构** | 世主妙严 sidebar双栏 | ✅ 已完成 |
| **cosmology.js数据→YAML** | COSMO_LAYERS等→data/cosmology/*.yaml | ✅ 已完成 |
| **gap.js数据→YAML** | 术语/案例/观点→glossary表+gap_content.yaml | ✅ 已完成 |
| **practice.js数据→YAML** | ~660行→data/practice/*.yaml | ✅ 已完成 |

### P2 — 内容深化

| 方向 | 内容 | 前提 |
|------|------|------|
| **行法** | 弥勒菩萨章文字整理: 善财53参第51参视频→逐字稿 | 视频转录 |
| **行法** | 华藏妙海PDF剩余内容提取 | 已有PDF |
| **行法** | 微信公众号海云法师讲记系统搜集 | 公众号搜索 |
| **行法** | 随大华严寺官网更新同步(当前基准: 2025.11版) | 持续关注 |
| **汉藏** | 术语库30→50条（补充阶位+世界观术语） | 无 |
| **法脉** | 高原法系32-36世补充 | 学术资料 |
| **文献** | 眷属经+别译本CBETA链接逐条补全 | 无 |
| **华严其观** | 七处九会图 + 善财五十三参路线图 | 无 |
| **frontier.js数据→YAML** | 跨界对话文本→data/frontier/*.yaml | 无 |

### P3 — 技术增强

| 方向 | 内容 |
|------|------|
| **文献** | 对读视图术语自动高亮链接 |
| **法脉** | 双人对比地图双标记 |
| **整体** | 自定义域名 + GitHub Actions CI |
| **文献** | CBETA API集成 |
| **数据库** | YAML内容（practice/frontier/cosmology）逐步迁入SQLite |

### P3 — 内容充实（近期）

| 方向 | 内容 | 状态 |
|------|------|------|
| **华严文献** | 文本系谱每部文献嵌入学者简介（出处·成书年代·学术评价） | 📋 待实现 |
| **华严文献** | 华严经学·全球研究：华严学报全期目录·国际期刊论文索引 | 📋 待实现 |
| **教海行云** | 海云法师梯次禅三/禅七录音穷尽搜索（联系大华严寺·逐季播客检查） | 📋 待实现 |
| **灵性仁本** | 海云法师「仁本经济学」术语原文出处确认 | 📋 待查 |
| **法脉传承** | 历史朝代疆域GeoJSON叠加（OpenHistoricalMap·CHGIS） | 📋 调研中 |

### P4 — 新方向

| 方向 | 内容 |
|------|------|
| **世主妙严** | 华严古迹巡礼·七处九会空间分布·善财五十三参地理路线 |
| **世主妙严** | 华严相关艺术品图鉴（普贤菩萨像/木雕/鎏金/犍陀罗造像等） |
| **文献↔法脉** | 文本系谱祖师点击→跳转法脉Tab对应人物 |
| **法脉** | 与天台宗/禅宗法脉对比叠加 |
| **前沿** | YouTube频道视频内容自动分析 |
| **全站** | 双语术语库前端渲染（BILINGUAL_GLOSSARY→页面tooltip/侧栏） |
| **全站** | 滤镜预设系统·底图切换·3D地球仪（法脉传承地图增强） |

---

## 三、开发命令速查

```bash
conda activate causality-nd

# 数据导出
python scripts/export_sqlite_to_json.py

# 图验证
python scripts/load_neo4j.py --verify

# 来源可靠性验证
python scripts/verify_sources.py

# 构建Demo
python web/demo/scripts/build.py

# 构建产物验证
python scripts/verify_demo.py
```

---

## 四、长期维护任务（持续任务，非单次迭代）

### L-A 全库来源可靠性审计与回填（进行中）

> 目标：persons / lineage_edges / locations 全部具备可追溯来源并经核校；今后任何人、边、地点入库必须携带 `source`+`verified`。

现状（2026-08-30，source-audit-report.md）：

| 对象 | 总数 | 缺来源 | 备注 |
|------|------|--------|------|
| persons | 95 | 0 | 评分 68/100；T3（模糊来源）36 项；`verified=0` 未复核 33 项 |
| lineage_edges | 92 | 0 | 已删自环/重复/反向边 6 条 |
| locations | 30 | 0 | T1:12 / T2:8 / T3:10 |

持续动作：

| 任务 | 状态 |
|------|------|
| 36 项 persons T3 → 细化到具体文献（清单见 source-audit-report.md：华严莲社社志、大华严寺法脉、当代瑜伽行传承、近现代佛教史料等） | 📋 待处理 |
| `verified=0` 的 33 项人工复核 → 置 verified=1 | 📋 待处理 |
| 华严莲社 / 大华严寺 / 高原法系 / 瑜伽行等教界自述谱系 → 继续寻找独立史料，否则保留〔存疑〕 | 🔄 持续 |
| 回填链路：源 sql/脚本 → `import_all_to_sqlite.py` → `verify_sources.py --out docs/source-audit-report.md` → `build.py` → `verify_demo.py` | 🔄 持续 |

> 已完成的回填脚本：`scripts/backfill_core_sources.py`（24人/42边/8道场）、`scripts/backfill_secondary_sources.py`（37人/54边）、`scripts/backfill_location_sources.py`（11道场）。

### L-B 研究文档内容定值复审（善财五十三参已闭环，推广至其余专题）

> 背景：`docs/善财五十三参深度研究.md` 原 §3.1 表参次全面错位（婆须蜜多列第8实为25、观自在列10实为27等），已按八十华严经文互证后重写 53 行全表（commit 855b935）。其余专题文档存在同型风险，需逐年复审。

规则：
1. 一切数字（参次、年代、人数、卷品、地点）须经一手典籍或权威二手对勘，不确者标〔待核〕/〔存疑〕，严禁"约第XX参"式占位。
2. 复审清单：李通玄长者_综合深度研究.md、华严宗二祖智俨_综合深度研究.md、梦参老和尚_综合深度研究.md、华严宗初祖杜顺_综合深度研究.md、文殊普贤信仰专题研究.md 等。
3. 机制：`verify_sources.py` docs 存疑标注覆盖率审计 + 人工逐篇复审。

### L-C 善财五十三参〔待核〕项闭环（84000 + CBETA 对勘）

`docs/善财五十三参深度研究.md` §3.1 表遗留待核项，待以 84000 Toh44-45 英译 + CBETA T279/T293 对勘补全后移除〔待核〕：

| 待核项 | 说明 |
|--------|------|
| 梵名 22 行 | 第9胜热、第10慈行、第21优钵罗华、第22婆施罗（梵名学界歧见）；第31-39 九位主夜神与第42-50（天主光……德生/有德）（冗长复合名号，以 84000 为准） |
| 地点 3 行 | 第41摩耶夫人、第43遍友童子（经文卷次明细）；第42天主光（蔚县壁画题记作"三十三天宫"，另一说在迦毗罗城附近） |
| 第38参名号差异 | 八十华严"愿勇光明守护众生主夜神" ↔ 四十华严"大愿精进力救护一切众生主夜神"，已注明并保留 |

### L-D 善财五十三参可视化（规划中）

与 P4「世主妙严·善财五十三参地理路线」、P2「善财五十三参路线图」衔接。L-C 闭环后可将名录结构化入 SQLite（53 参次/善知识/梵名/身份/地点/法门），供 build.py 渲染路线图与法脉关联。

### L-E 多语对读文章《识与心灵》《识与心灵之镜》（P0/P1 完成 2026-08-30）

**目标**：两篇项目作者自有研究长文（唯识学×当代意识科学 / 唯识学×西方心理学）以「中文为主文·外文为平行对读」形态整合为独立文章页，接入前沿对话 Tab「与佛教的对话」→「瑜伽行派 & 华严」域。

- 设计规范：`docs/bilingual-annotation-design.md`（呈现模型/批注格式/语言取舍/来源分级/路线图）
- P0：文章页骨架 + 摘要/关键词/核心术语批注示范 + 后端接入；**已完成**（前后端、注册、出处登记、构建验证）
- P1：全部小节配齐「EN对应」作者英文修订版原句全文（与中文小节一一对应、信息无损）；**已完成**（49 + 60 对；本底两版节内小节结构与次序一致，仅 en_2 第 13 节中文多 1 小节特例对齐）
- P2：术语格义表覆盖正文全部核心唯识术语（梵/藏/英）——进行中
- P3：法/日批注精选补入；全文〔待核〕清零闭环

> 源文本：sleepyowlowlowl.substack.com（作者自有账号）；底本版本为 04-15 发行版（中文原稿 + 英文修订版 *Vijñāna and Mind 0415* / *The Mirror of Mind*）。

### L-F 全站双语原则：中文为主文 · 简明优雅英文无损对应（规划 2026-08-30）

**方向**：在中文信息**无损**的前提下，页面中所有文字内容均以「中文为主文 + 英文无损对应」双语呈现；英文要求**最简明优雅**——直白地对准中文信息要点，克制、不铺陈、不因对仗而失真。

- 适用范围：本规划落地后，所有 Tab 页、文章页、批注、卡片、列表、表格、图表标签等可见文字原则上同此呈现（数据源字段增补 en，构建渲染，英文不得只活在 HTML/JS 里）。
- 信息无损 = 中文语义一点不丢；英文简洁优雅 = 用最直接的名词/短句覆盖要点，允许合并长句而语义等价，术语按 `bilingual_glossary` 统一查表（佛教术语不硬译，沿用惯译/音译并可与汉文并列）。
- 分段呈现：长段落按「节/段」给英文对应，页面默认展开中英对照，可折叠为仅中文阅读模式（沿用 `article.js` 的英文批注折叠机制推广到全站）。
- 落地序列（自 L-E 起）：
  1. L-E 两篇多语对读文章：从「节级英译要义(节首原句)」升级为「全节英文无损对应」，覆盖每一节全部内容块（含漫谈/案例/表格说明）；**已完成**
  2. 前沿对话 Tab 的域卡片与各节 intro：YAML 增 `en` 字段，域名/核心议题/关键发现给出英文对应；**已完成 2026-08-30**（5 节 intro `en` + 18 域 `en_domain`/`en_core`/`en_persp`|`en_key_findings`；frontier.js 渲染 `.en-line` + 页面级「🌐 英文对应·显示/隐藏」开关，localStorage `frontier_en`）
  3. 全站数据 YAML/SQLite 逐表增 `en` 字段 → build.py 渲染中英对照 → 全局「仅中文/中英对照」阅读切换；**进行中 2026-08-30**（第一梯队：①全站阅读切换机制——build.py 四模板 header 注入 `#lang-toggle`，common.js `toggleSiteLang/_applySiteLang` + localStorage `site_lang`，common.css `body.zh-only` 全局隐藏 `.en-line/.en-block/.en-note/.en-cell`，默认中英对照；②Tab6 灵性仁本 `spirit_content.yaml` 全量 EN——6 节 `title_en`+`summary_en`/`en`+19 主题 `en`/`en_body`，spirit.js 渲染；③SQLite glossary 分支——50 条 definition_zh/definition_en 全补齐（补 7 条缺失），build.py `load_gap` 注入 `db_reader.load_glossary()`→`GAP.glossary`，gap.js 以数据驱动双语术语表替换原硬编码 30 行并新增「术语格义·中英释义」卡；④Tab5 世主妙严——`art_treasures.yaml` 9 件艺术珍品 `title_en`/`description_en` + 6 古迹 `name_en`/`desc_en` + `alphabet_intro_en`，`heritage_critical.yaml` 2 节 `title_en`/`intro_en` + 6 主题 `en`/`en_body`；`cosmology.js` 大幅重构：艺术珍品/古迹巡礼/多媒体/书目/字母表/梵呗嵌入 全部改为读 `COSMO_DATA`（**消除该页硬编码**），并新增呈现此前「孤儿数据」`heritage_critical`+`environmental_history`（原载入却从未渲染），EN 块均带 `.en-line` 随全局切换显隐；⑤Tab6 灵性仁本收尾——`environmental_humanities.yaml` 3 节 `title_en`/`intro_en` + 7 主题 `en`/`en_body`（引用原文照用：Chakrabarty「Four Theses」/Todd「An Indigenous Feminist's Take on the Ontological Turn」/Simpson《As We Have Always Done》/Smith「Authorised Heritage Discourse」），spirit.js `renderEnvHumanities` 渲染 EN，至此 Tab6 全量双语；⑥Tab3 华严教行·A期（判教/YouTube）——`huayan_panjiao.yaml` 五教十宗·一乘不共别圆·判教比较 全量 EN（overview 三段 + 4 节 title_en/description_en/description_en + 五教 5 教 `name_en/doctrine_en/position_en` 等 + 十宗 10 宗 `name_en/doctrine_en/level_en` + 一乘 3 要点 `title_en/en_body` + 三宗比较 `school_en/system_en/relation_to_huayan_en`），`youtube_playlists.yaml` channel `description_en` + 7 播放清单 `type_en/description_en`（多为现有英文译名）；practice.js `renderPanjiaoSection`/`renderYoutubeSection` 渲染 EN（表格内 `.en-line` 副行、`.en-line` 块随全局切换显隐）；⑦Tab3 华严教行·B期（深度研究·成观法师块）——`chengguan_master.yaml` 传记/译经院/著作全目/8 讲法特色/与海云之比较 全量 EN（birthplace_en/education_en/ordination_en/lineage_en/current_position_en + 名目 _en），`haiyun_chengguan_compare.yaml` meta note_en + 11 对照行 topic_en/position_en/note_en/contrast_en（引文保持中文原语）；practice.js `renderChengguanSection` 渲染 EN（bio 并行块/教学卡 .en-line/对照表双栏副行）；⑧Tab3 华严教行·B期（深度研究·转道资粮+律宗）——`zhuandao_ziliang.yaml` title_en/intro_en + 6 主题 title_en/en_body（资粮道定义/发心工程/前行道三阶段/唯识五位/体系对比/经典依据，语录保持中文原语），`vinaya_school.yaml` 8 节 title_en + overview intro_en + 16 主题 title_en/en_body（9 大宗派判摄/戒律在中国/授戒规范/持犯开遮/海云戒学 等，引自仰泽《戒律与禅修的连动》）；practice.js `renderZhuandaoSection`/`renderVinayaSection` 渲染 EN（title_en 副行/intro_en 📖 块/en_body 块随 .en-line 切换）；⑨（深度研究·三十七道品）——`sanshiqi_daopin.yaml` title_en/intro_en + 15 主题 title_en/en_body（总论/四念处/四正勤/四如意足/五根五力/七觉支/八正道/印度渊源/南传/汉传/藏传/海云解脱道/现代正念/融合与张力/经典依据，原典引文保留中文、括号注英文书名作者），`renderSanShiQiDaoPin` 渲染 EN；⑩（深度研究·禅门行跡）——`chan_authentic_traces.yaml` 5 节 title_en/intro_en + 32 主题 title_en/en_body（学术观四阶段范式/禅宗实践戒定慧·话头默照·三关·丛林制度·祖师禅与如来禅·禅宗与他宗融合/近现代虚云·来果·净慧·台湾三系统·全球化/海云东山法门·话头疑情·心王心所·身根·一门深入/传承详表·五家七宗·传法偈印可；祖师语录保持中文原语、EN 转述），`renderChanTraces` 渲染 EN；⑪（深度研究·法相+天台两宗）——`faxiang_xuanji.yaml` 10 节 title_en/intro_en + 35 主题 title_en/en_body（名相辨析/印度渊源/汉传法脉/核心教义·八识三性种子五位百法五重观/式微四因/域外三线/近现代复兴·欧阳竟无·太虚·熊十力公案/修行界视角/学术·现象学诠释五大公案/海云成观评述），`tiantai_juejing.yaml` 10 节 title_en/intro_en + 28 主题 title_en/en_body（名相·三大部/法脉奠基慧文智顗灌顶/一心三观一念三千五时八教六即/传承曲折·山家山外/日本天台台密·义天/近现代谛闲倓虚宝静/学术·Swanson Ziporyn 牟宗三/内部视角/诸宗交叉/海云天台判摄），`renderFaxiangSection`/`renderTiantaiSection` 渲染 EN；⑫（深度研究·三论+密教两宗）——`yikong_daodi.yaml` 13 节 title_en/intro_en + 50 主题 title_en/en_body（名相/印度渊源·龙树提婆吉藏/汉传法脉·三论/核心教义·中道二谛八不/式微/域外·藏传格鲁应成见/近现代复兴/修行界视角/学术前沿·Ruegg 空有之诤/融合张力/海云·成观空性诠释），`mimi_daodi.yaml` 10 节 title_en/intro_en + 34 主题 title_en/en_body（名相七称谓/印度渊源·杂密纯密/唐密开元三大士/核心教义·三密即身成佛两部大法/东密台密/藏传金刚乘/近代回传复兴/当代显密圆融/内部视角/融合张力），`renderYikongSection`/`renderMimiSection` 渲染 EN；⑬（修行要义+讲法资源·7 异构件收尾）——`dushun_wujiao_zhiguan.yaml`（杜顺五教止观）text_info/overview/5 gate 全量 EN（title_en/overview 两段_en/每 gate panjiao_en·practice_en·original_text_en + 各家注解 text_en + 学术评注 text_en + lineage_development stages contribution_en/key_text_en），`renderDushunSection` 渲染 EN（gate 名副行·原文 EN 块·注解/评注 `.en-line`·lineage 表副行）；`mengcan_lectures.yaml`（梦参讲法全目）biography key_locations_en/relation_to_huayan_en + 14 lecture 全量 `_en`（sutra_en/title_en/content_en/significance_en/note_en）+ life_motto_en/relation_to_project_en，`renderMengcanSection` 渲染 EN（时间线 EN 副块·讲座表 EN 副行「📖 shelf」·life_motto/relation EN 块）；`haiyun_practice_sources.yaml`（海云全平台修行资源）core_framework description_en + 7 著作 title_en/content_en + 3 讲记 + 3 视频 + 5 平台 + 3 学术 + 三阶段速查表 + exhaustive_platform_index 全平台 `_en`（bilibili/podcast/youtube/text/retreats/搜索局限），`renderPracticeSources` 渲染 EN；`haiyun_avatamsaka_lectures.yaml`（华严经讲法全目）overview/overall 4/玄谈 5/品目 20/podcast/视频/快速索引 全量 `_en`，`renderAvatamsakaLectures` 渲染 EN；外加 3 个「孤儿数据」文件（数据 EN 已在此补齐，前端接入见 ⑯）：`teaching_resources.yaml`（platforms/topics/yt_series/publications/academic_events/temples 全量 `_en`）、`meditation_essentials.yaml`（修行体系/古典地基/四种观法/重要文本/验证速查表 全量 `_en`）、`heart_xref.yaml`（华严本心跨宗互参 10 条目 r1_huayan_en/r2_other_en 全补）。翻译&校对结合：多语对应重实质不逐字。全部 build 15,993,798 B + verify ALL PASSED + 标记抽查命中；⑭（修行体系·硬编码框架重构）——`cultivation_system.yaml`（海云普贤乘修行体系）全量 `_en`（header 三阶段卡片·四阶段蓝图·华严六科·三大法脉·四大工程·识根智·三缘念·演进时间线 各 `name_en/subtitle_en/detail_en/description_en/feature_en` 等），practice.js 删去 pv-system 整段硬编码 HTML（约 90 行）改写为数据驱动 `renderCultivationSystem()`（读 PRACTICE_DATA.cultivation_system，卡片/表格/时间线全部由数据渲染，`.en-line` 随全局显隐），build 16,062,527 B + verify ALL PASSED；⑮（禅观法要·硬编码框架重构）——`chan_contemplation.yaml`（华严禅观法要：卷首对比表格·修行次第五阶段·重要典籍现代阐释·验证机制）全量 `_en`（med-texts 金师子章/心要法门/三品行法与 med-verify 验证机制/三大关键原则 共 5 个 wu-door 各补 `title_en`+`html_en`，med-overview/med-paths/stage1-3 已系数据驱动自带 `_en`，med-heart/heart-gandhara `title_en`；med-xinfa-dushun-panjiao 为 data-driven 占位段）；practice.js 删去卷首硬编码 datatable 与 med-texts/med-verify 整段硬编码 HTML（约 300 行），统一改由 `renderChanContemplation()` 数据驱动渲染（读 PRACTICE_DATA.chan_contemplation，block `html` → `html_en` 以 `.en-line` 随全局切换显隐），build 16,421,695 B + verify ALL PASSED；⑯（practice.js 硬编码清零·三孤儿数据接入）——将⑬标注的 3 个「孤儿数据」文件全部接入前端、消除对应区域硬编码并补 EN 渲染：①`heart_xref.yaml` 10 条目 `entries`（r1_huayan/r2_other + r1_huayan_en/r2_other_en + r1_source/r2_source）替换 practice.js 硬编码 `heartXRef` 对象（约 22 行），新增 `heartTackLine()`（◆ 标签加粗）与 `heartRtf()`（◆ 分段 `<br>` + `class=src` 出处 + `.en-line` 双语块）——先转义再加粗、避免破坏 `<b>` 标签；同时删除该 YAML 中「别用大脑」重复的 r2_other 整块（含 r1 内容与冗余 r1_source），还原 r2 真身；②`teaching_resources.yaml` 替换 Sub-page4/pv-news 多处硬编码：全网讲法总目表（platforms 8 平台）·按主题分类 9 卡（topics + description_en）·著作清单（publications 8 组 + `<key>_en` + english + publisher_en）·YouTube 频道卡（yt_channels content_en）·导览链接（links）·相关道场（temples name_en/description_en）·学术活动轨迹表（academic_events event_en/topic_en），全部改读 PRACTICE_DATA.teaching_resources，EN 以 `.en-line` 随全局切换显隐；③`meditation_essentials.yaml` 在 pv-meditation 顶部（renderChanContemplation 之前）新增 `renderMeditationEssentials()`，呈现此前载入却从未渲染的孤儿内容：system_overview 三阶段总览（description_en + stages_table 一 section=leader 行 + note 横跨注记行）·important_texts 3 项（金师子章/心要法门/三品行法，`<details>` 折叠 + name_en/content_en）·verification 验证机制（title_en + 2 节 title_en/content_en）；并删除该 YAML 中「别用大脑」重复 r2_other 块。新增 `_nl()`（\n→\<br\>）辅助函数。node --check 语法通过 + 全量 10 文章 fixture 运行时渲染验证（heartXRef 10 条 EN body、teaching 平台/主题/道场/学术 EN、meditation overview/texts/verification EN 全命中）+ build 16,398,356 B + verify ALL PASSED。待续梯队：lineage 主线人名 EN（SQLite persons 已有 name_en 36/95 但 lineage.js 零渲染）、其余 stray 硬编码扫描 等）
  4. 沉淀为新内容默认规范（见 `docs/bilingual-annotation-design.md`）。
- 校验：英文对应与中文一一对齐，由批注块前缀/数据字段一致性检查兜底；不因双语引入未经考证的译名。
