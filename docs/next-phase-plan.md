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
| persons | 95 | 0 | 评分 76/100；T3（模糊来源）10 项（已在 ㉛ 依 id 细化 36 条→10 条）；`verified=1` 72/95 |
| lineage_edges | 92 | 0 | 已删自环/重复/反向边 6 条 |
| locations | 30 | 0 | T1:12 / T2:8 / T3:10 |

持续动作：

| 任务 | 状态 |
|------|------|
| 36 项 persons T3 → 细化到具体文献（清单见 source-audit-report.md：华严莲社社志、大华严寺法脉、当代瑜伽行传承、近现代佛教史料等） | ✅ 已完成 2026-09-02（L.㉛：36 注册目标依 id 替换 26 升 T1/T2 + 10 如实保留 T3，又扩展补 20 条非注册 T3，共 56 条 source 细化，T3 36→10） |
| `verified=0` 的 23 项（确实无力者保持 0 并注明） | 🔄 持续 |
| 华严莲社 / 大华严寺 / 高原法系 / 瑜伽行等教界自述谱系 → 继续寻找独立史料，否则保留〔存疑〕 | 🔄 持续 |
| 回填链路：源 sql/脚本 → `import_all_to_sqlite.py` → `verify_sources.py --out docs/source-audit-report.md` → `build.py` → `verify_demo.py` | 🔄 持续 |

> 已完成的回填脚本：`scripts/backfill_core_sources.py`（24人/42边/8道场）、`scripts/backfill_secondary_sources.py`（37人/54边）、`scripts/backfill_location_sources.py`（11道场）。

### L-B 研究文档内容定值复审（善财五十三参已闭环，推广至其余专题）

> 背景：`docs/善财五十三参深度研究.md` 原 §3.1 表参次全面错位（婆须蜜多列第8实为25、观自在列10实为27等），已按八十华严经文互证后重写 53 行全表（commit 855b935）。其余专题文档存在同型风险，需逐年复审。

规则：
1. 一切数字（参次、年代、人数、卷品、地点）须经一手典籍或权威二手对勘，不确者标〔待核〕/〔存疑〕，严禁"约第XX参"式占位。
2. 复审清单：李通玄长者_综合深度研究.md、华严宗二祖智俨_综合深度研究.md、梦参老和尚_综合深度研究.md、华严宗初祖杜顺_综合深度研究.md、文殊普贤信仰专题研究.md 等。
3. 机制：`verify_sources.py` docs 存疑标注覆盖率审计 + 人工逐篇复审。

### L-C 善财五十三参〔待核〕项闭环（84000 + CBETA 对勘） — ✅ 已完成 2026-09-02（L.㉜）

`docs/善财五十三参深度研究.md` §3.1 表遗留待核项，待以 84000 Toh44-45 英译 + CBETA T279/T293 对勘补全后移除〔待核〕：

| 待核项 | 说明 |
|--------|------|
| 梵名 22 行 | 第9胜热、第10慈行、第21优钵罗华、第22婆施罗（梵名学界歧见）；第31-39 九位主夜神与第42-50（天主光……德生/有德）（冗长复合名号，以 84000 为准） |
| 地点 3 行 | 第41摩耶夫人、第43遍友童子（经文卷次明细）；第42天主光（蔚县壁画题记作"三十三天宫"，另一说在迦毗罗城附近） |
| 第38参名号差异 | 八十华严"愿勇光明守护众生主夜神" ↔ 四十华严"大愿精进力救护一切众生主夜神"，已注明并保留 |

> 闭环记录（L.㉜）：§3.1 表 9/10、21/22、31-39、41-50 行（梵名+地点+中文名）全部依 CBETA T279 原文与 84000 术语表音写（Vāsantī、Gopā、Sarvajagadrakṣāpraṇidhānavīryaprabhā 等，websearch 取 84000 术语表权威音写；站点直连 transport error，已绕过）填完；第 38 参中文名校正为「大願精進力救護一切眾生主夜神」（两称同源 praṇidhānavīryaprabha）；编次说明按 T279 v73 校正；「最后更新」改 2026年9月；文档内〔待核〕残留清零。表下编次注（文殊初参不计、法藏《文殊指南圖讚》使 51/52 后移）沿用。

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
  3. 全站数据 YAML/SQLite 逐表增 `en` 字段 → build.py 渲染中英对照 → 全局「仅中文/中英对照」阅读切换；**进行中 2026-08-30**（第一梯队：①全站阅读切换机制——build.py 四模板 header 注入 `#lang-toggle`，common.js `toggleSiteLang/_applySiteLang` + localStorage `site_lang`，common.css `body.zh-only` 全局隐藏 `.en-line/.en-block/.en-note/.en-cell`，默认中英对照；②Tab6 灵性仁本 `spirit_content.yaml` 全量 EN——6 节 `title_en`+`summary_en`/`en`+19 主题 `en`/`en_body`，spirit.js 渲染；③SQLite glossary 分支——50 条 definition_zh/definition_en 全补齐（补 7 条缺失），build.py `load_gap` 注入 `db_reader.load_glossary()`→`GAP.glossary`，gap.js 以数据驱动双语术语表替换原硬编码 30 行并新增「术语格义·中英释义」卡；④Tab5 世主妙严——`art_treasures.yaml` 9 件艺术珍品 `title_en`/`description_en` + 6 古迹 `name_en`/`desc_en` + `alphabet_intro_en`，`heritage_critical.yaml` 2 节 `title_en`/`intro_en` + 6 主题 `en`/`en_body`；`cosmology.js` 大幅重构：艺术珍品/古迹巡礼/多媒体/书目/字母表/梵呗嵌入 全部改为读 `COSMO_DATA`（**消除该页硬编码**），并新增呈现此前「孤儿数据」`heritage_critical`+`environmental_history`（原载入却从未渲染），EN 块均带 `.en-line` 随全局切换显隐；⑤Tab6 灵性仁本收尾——`environmental_humanities.yaml` 3 节 `title_en`/`intro_en` + 7 主题 `en`/`en_body`（引用原文照用：Chakrabarty「Four Theses」/Todd「An Indigenous Feminist's Take on the Ontological Turn」/Simpson《As We Have Always Done》/Smith「Authorised Heritage Discourse」），spirit.js `renderEnvHumanities` 渲染 EN，至此 Tab6 全量双语；⑥Tab3 华严教行·A期（判教/YouTube）——`huayan_panjiao.yaml` 五教十宗·一乘不共别圆·判教比较 全量 EN（overview 三段 + 4 节 title_en/description_en/description_en + 五教 5 教 `name_en/doctrine_en/position_en` 等 + 十宗 10 宗 `name_en/doctrine_en/level_en` + 一乘 3 要点 `title_en/en_body` + 三宗比较 `school_en/system_en/relation_to_huayan_en`），`youtube_playlists.yaml` channel `description_en` + 7 播放清单 `type_en/description_en`（多为现有英文译名）；practice.js `renderPanjiaoSection`/`renderYoutubeSection` 渲染 EN（表格内 `.en-line` 副行、`.en-line` 块随全局切换显隐）；⑦Tab3 华严教行·B期（深度研究·成观法师块）——`chengguan_master.yaml` 传记/译经院/著作全目/8 讲法特色/与海云之比较 全量 EN（birthplace_en/education_en/ordination_en/lineage_en/current_position_en + 名目 _en），`haiyun_chengguan_compare.yaml` meta note_en + 11 对照行 topic_en/position_en/note_en/contrast_en（引文保持中文原语）；practice.js `renderChengguanSection` 渲染 EN（bio 并行块/教学卡 .en-line/对照表双栏副行）；⑧Tab3 华严教行·B期（深度研究·转道资粮+律宗）——`zhuandao_ziliang.yaml` title_en/intro_en + 6 主题 title_en/en_body（资粮道定义/发心工程/前行道三阶段/唯识五位/体系对比/经典依据，语录保持中文原语），`vinaya_school.yaml` 8 节 title_en + overview intro_en + 16 主题 title_en/en_body（9 大宗派判摄/戒律在中国/授戒规范/持犯开遮/海云戒学 等，引自仰泽《戒律与禅修的连动》）；practice.js `renderZhuandaoSection`/`renderVinayaSection` 渲染 EN（title_en 副行/intro_en 📖 块/en_body 块随 .en-line 切换）；⑨（深度研究·三十七道品）——`sanshiqi_daopin.yaml` title_en/intro_en + 15 主题 title_en/en_body（总论/四念处/四正勤/四如意足/五根五力/七觉支/八正道/印度渊源/南传/汉传/藏传/海云解脱道/现代正念/融合与张力/经典依据，原典引文保留中文、括号注英文书名作者），`renderSanShiQiDaoPin` 渲染 EN；⑩（深度研究·禅门行跡）——`chan_authentic_traces.yaml` 5 节 title_en/intro_en + 32 主题 title_en/en_body（学术观四阶段范式/禅宗实践戒定慧·话头默照·三关·丛林制度·祖师禅与如来禅·禅宗与他宗融合/近现代虚云·来果·净慧·台湾三系统·全球化/海云东山法门·话头疑情·心王心所·身根·一门深入/传承详表·五家七宗·传法偈印可；祖师语录保持中文原语、EN 转述），`renderChanTraces` 渲染 EN；⑪（深度研究·法相+天台两宗）——`faxiang_xuanji.yaml` 10 节 title_en/intro_en + 35 主题 title_en/en_body（名相辨析/印度渊源/汉传法脉/核心教义·八识三性种子五位百法五重观/式微四因/域外三线/近现代复兴·欧阳竟无·太虚·熊十力公案/修行界视角/学术·现象学诠释五大公案/海云成观评述），`tiantai_juejing.yaml` 10 节 title_en/intro_en + 28 主题 title_en/en_body（名相·三大部/法脉奠基慧文智顗灌顶/一心三观一念三千五时八教六即/传承曲折·山家山外/日本天台台密·义天/近现代谛闲倓虚宝静/学术·Swanson Ziporyn 牟宗三/内部视角/诸宗交叉/海云天台判摄），`renderFaxiangSection`/`renderTiantaiSection` 渲染 EN；⑫（深度研究·三论+密教两宗）——`yikong_daodi.yaml` 13 节 title_en/intro_en + 50 主题 title_en/en_body（名相/印度渊源·龙树提婆吉藏/汉传法脉·三论/核心教义·中道二谛八不/式微/域外·藏传格鲁应成见/近现代复兴/修行界视角/学术前沿·Ruegg 空有之诤/融合张力/海云·成观空性诠释），`mimi_daodi.yaml` 10 节 title_en/intro_en + 34 主题 title_en/en_body（名相七称谓/印度渊源·杂密纯密/唐密开元三大士/核心教义·三密即身成佛两部大法/东密台密/藏传金刚乘/近代回传复兴/当代显密圆融/内部视角/融合张力），`renderYikongSection`/`renderMimiSection` 渲染 EN；⑬（修行要义+讲法资源·7 异构件收尾）——`dushun_wujiao_zhiguan.yaml`（杜顺五教止观）text_info/overview/5 gate 全量 EN（title_en/overview 两段_en/每 gate panjiao_en·practice_en·original_text_en + 各家注解 text_en + 学术评注 text_en + lineage_development stages contribution_en/key_text_en），`renderDushunSection` 渲染 EN（gate 名副行·原文 EN 块·注解/评注 `.en-line`·lineage 表副行）；`mengcan_lectures.yaml`（梦参讲法全目）biography key_locations_en/relation_to_huayan_en + 14 lecture 全量 `_en`（sutra_en/title_en/content_en/significance_en/note_en）+ life_motto_en/relation_to_project_en，`renderMengcanSection` 渲染 EN（时间线 EN 副块·讲座表 EN 副行「📖 shelf」·life_motto/relation EN 块）；`haiyun_practice_sources.yaml`（海云全平台修行资源）core_framework description_en + 7 著作 title_en/content_en + 3 讲记 + 3 视频 + 5 平台 + 3 学术 + 三阶段速查表 + exhaustive_platform_index 全平台 `_en`（bilibili/podcast/youtube/text/retreats/搜索局限），`renderPracticeSources` 渲染 EN；`haiyun_avatamsaka_lectures.yaml`（华严经讲法全目）overview/overall 4/玄谈 5/品目 20/podcast/视频/快速索引 全量 `_en`，`renderAvatamsakaLectures` 渲染 EN；外加 3 个「孤儿数据」文件（数据 EN 已在此补齐，前端接入见 ⑯）：`teaching_resources.yaml`（platforms/topics/yt_series/publications/academic_events/temples 全量 `_en`）、`meditation_essentials.yaml`（修行体系/古典地基/四种观法/重要文本/验证速查表 全量 `_en`）、`heart_xref.yaml`（华严本心跨宗互参 10 条目 r1_huayan_en/r2_other_en 全补）。翻译&校对结合：多语对应重实质不逐字。全部 build 15,993,798 B + verify ALL PASSED + 标记抽查命中；⑭（修行体系·硬编码框架重构）——`cultivation_system.yaml`（海云普贤乘修行体系）全量 `_en`（header 三阶段卡片·四阶段蓝图·华严六科·三大法脉·四大工程·识根智·三缘念·演进时间线 各 `name_en/subtitle_en/detail_en/description_en/feature_en` 等），practice.js 删去 pv-system 整段硬编码 HTML（约 90 行）改写为数据驱动 `renderCultivationSystem()`（读 PRACTICE_DATA.cultivation_system，卡片/表格/时间线全部由数据渲染，`.en-line` 随全局显隐），build 16,062,527 B + verify ALL PASSED；⑮（禅观法要·硬编码框架重构）——`chan_contemplation.yaml`（华严禅观法要：卷首对比表格·修行次第五阶段·重要典籍现代阐释·验证机制）全量 `_en`（med-texts 金师子章/心要法门/三品行法与 med-verify 验证机制/三大关键原则 共 5 个 wu-door 各补 `title_en`+`html_en`，med-overview/med-paths/stage1-3 已系数据驱动自带 `_en`，med-heart/heart-gandhara `title_en`；med-xinfa-dushun-panjiao 为 data-driven 占位段）；practice.js 删去卷首硬编码 datatable 与 med-texts/med-verify 整段硬编码 HTML（约 300 行），统一改由 `renderChanContemplation()` 数据驱动渲染（读 PRACTICE_DATA.chan_contemplation，block `html` → `html_en` 以 `.en-line` 随全局切换显隐），build 16,421,695 B + verify ALL PASSED；⑯（practice.js 硬编码清零·三孤儿数据接入）——将⑬标注的 3 个「孤儿数据」文件全部接入前端、消除对应区域硬编码并补 EN 渲染：①`heart_xref.yaml` 10 条目 `entries`（r1_huayan/r2_other + r1_huayan_en/r2_other_en + r1_source/r2_source）替换 practice.js 硬编码 `heartXRef` 对象（约 22 行），新增 `heartTackLine()`（◆ 标签加粗）与 `heartRtf()`（◆ 分段 `<br>` + `class=src` 出处 + `.en-line` 双语块）——先转义再加粗、避免破坏 `<b>` 标签；同时删除该 YAML 中「别用大脑」重复的 r2_other 整块（含 r1 内容与冗余 r1_source），还原 r2 真身；②`teaching_resources.yaml` 替换 Sub-page4/pv-news 多处硬编码：全网讲法总目表（platforms 8 平台）·按主题分类 9 卡（topics + description_en）·著作清单（publications 8 组 + `<key>_en` + english + publisher_en）·YouTube 频道卡（yt_channels content_en）·导览链接（links）·相关道场（temples name_en/description_en）·学术活动轨迹表（academic_events event_en/topic_en），全部改读 PRACTICE_DATA.teaching_resources，EN 以 `.en-line` 随全局切换显隐；③`meditation_essentials.yaml` 在 pv-meditation 顶部（renderChanContemplation 之前）新增 `renderMeditationEssentials()`，呈现此前载入却从未渲染的孤儿内容：system_overview 三阶段总览（description_en + stages_table 一 section=leader 行 + note 横跨注记行）·important_texts 3 项（金师子章/心要法门/三品行法，`<details>` 折叠 + name_en/content_en）·verification 验证机制（title_en + 2 节 title_en/content_en）；并删除该 YAML 中「别用大脑」重复 r2_other 块。新增 `_nl()`（\n→\<br\>）辅助函数。node --check 语法通过 + 全量 10 文章 fixture 运行时渲染验证（heartXRef 10 条 EN body、teaching 平台/主题/道场/学术 EN、meditation overview/texts/verification EN 全命中）+ build 16,398,356 B + verify ALL PASSED；⑰（Tab1 法脉传承·主线人名 EN 接入）——SQLite persons 已有 `name_en`（pinyin，36/95）与 `name_sa`（梵文，14/95），经 db_reader load_graph() 注入 GRAPH，但 lineage.js 原本零渲染；现补 `_enName()`/`_enNameHtml()` 两辅助函数（读 `name_en||name_sa`，EN 块带 `.en-line` 随全局切换显隐，仅在有数据时输出、无 data 自动回退纯中文），并接入 7 处人名展示面：①Canvas 时间轴 有年代标签 高亮时（`<hl>` 命中）下方 8px 小字 EN；②无年代菱形标签 高亮时 下方 EN；③hover 悬浮 tooltip 副行 EN；④详情弹窗 showInfo h1 之下 EN 副行；⑤对比弹窗 showInfo 第二人 h3 之下 EN；⑥主线地图位置弹窗关联人物名旁 EN（`·` 连接）；⑦全人名册 roster 分组，聚合时取 `ne`、徽章人名后 `.en-line` 小字 EN。杜绝硬编码：人名 EN 均来自 SQLite（源头 personas.json）`.en-line` 随全局显隐；node --check + verify 45 checks ALL PASSED + build 16,399,554 B；无 `biography_en`（SQLite 无此列）按考证优先不臆造，姓名级 EN 仅输出已验证者（36 名）缺者自动纯中。⑱（Tab1 法脉传承·lineage.js 死码覆盖清零·8 YAML 全局接入）——lineage.js 顶部 6 个硬编码数组与中后部 2 个（ANIM_WAYPOINTS）原为「死重复覆盖」：build.py 已将 `data/events/*.yaml` 注入为带包装 key 的全局（如 `KEY_EVENTS={"events":[...]}`），而 lineage.js 又用 `var KEY_EVENTS=[...]` 中文同名硬编码重新声明将其**覆盖/作废**（源头治理被回路腰斩）。本轮删除 8 处硬编码字面量（共约 412 行，build 16,399,554→16,369,941 B），改为一处「解包适配」读取注入全局：`THEORY_STAGES.stages`/`PRACTICE_STAGES.stages`/`GEO_FLOW.flow`/`KEY_EVENTS.events`/`ERA_BRACKETS.brackets`/`LOC_ANCIENT.mapping`/`DYNASTY_BOUNDARIES.dynasties`/`ANIM_WAYPOINTS.waypoints`（`typeof!=='undefined'&&…` 空阵回退，防注入缺失崩页）。内容核对：前 7 个 YAML 与硬编码**逐条一致**（key_events 35 条全同），渲染零变化；`ANIM_WAYPOINTS` 系**净去重**——硬编码 111 对象中含 2 对重复（孔 孔子逝世·儒学历程开始/孟子·性善论 各 ×2），YAML 109 条已去重、label 集合完全一致，无内容损失。node --check + runtime 解包 harness（各数组长度 6/6/7/35/5/1、LOC_ANCIENT 为 map）验证 + build + verify ALL PASSED。验证要点：build.py 注入全局必须在 lineage_js **之前**（lineage 页 data_script 在前、wrap_script(lineage_js) 在后），wrap_script 不套 IIFE 故顶层级解包直接读写全局。⑲见后（本轮续扫又证 3 处亦为「死重复覆盖」而非内容缺失，一并清零）。待续梯队（遗留·确属不同形状/需另建源的 curated 内容，勿静默删）：`drawTL` 内时间轴朝代带 `dynasties`（6 段 rgba 填色带，形状与 `dynasty_boundaries.yaml` 不同——非 DYNASTY_BOUNDARIES，需另建源）、`_huayanCore`（6 道 curated 核心人物 id，作为 huayan_annotations 'direct' 层级的兜底；若直接改成「全部 direct 级」会扩增关系图中节点范围=行为变更，需确认后另建 `core_persons` 字段迁数据）、`_MINI_REGIONS`（10 区域地图配置 label/center/zoom/color/key=function 配置，是可接受的代码常量，但 label 文案亦可考虑数据化）。待续梯队：**lineage 人名 EN 数据回填**（personas.json 余 59 条目 name_en/name_sa 逐条考证补全）⑲（Tab1 法脉传承·续扫清零：TRANS_STORY/OTHER_SCHOOLS/geoFeatures 三处亦为死重复或孤儿硬编码）——上一批⑱之后用 node 引擎对 lineage.js 硬编码数组与 `data/events/*.yaml` 注入全局做逐条双扩对比，纠正了两处误判并把死去重复清零干净：①`TRANS_STORY`——注入全局名是 `TRANSMISSION_STORY`（filename→`.upper()`）且包装 key=`story`（`transmission_story.yaml` 25 条），lineage.js 却另用别名 `var TRANS_STORY=[25]` 硬编码；node 逐字段比对（y/p/lat/lng/ev/src）**逐序完全一致**，故为死重复。删除 27 行改为解包适配 `TRANS_STORY=(typeof TRANSMISSION_STORY!=='undefined'&&TRANSMISSION_STORY&&TRANSMISSION_STORY.story)?TRANSMISSION_STORY.story:[]`。②`OTHER_SCHOOLS`——上批误记为「YAML 7 vs 硬编码 14」实为多行对象被行数误算；node 引擎真实解析「7 校且字段 n/y/lat/lng/c/founder/loc/desc/src 逐序一致」，YAML 注释即「从lineage.js OTHER_SCHOOLS提取」。删除 16 行改 `OTHER_SCHOOLS.schools` 解包。③`geoFeatures`（toggleAncient 古地图 8 地名）——此前确无 YAML 源；本轮新建 `data/events/geo_features.yaml`（8 处 name/lat/lng，坐标照抄硬编码值=非新增史实，由 `load_events()` 自动 glob 注入为 `GEO_FEATURES.features`），lineage.js 改读数源（缺则空回退）。至此 lineage.js **注入即用的 YAML 全局全部由数据驱动，无一处死重复覆盖**。验证：node --check + 11 项 runtime 解包 harness（数组长度 6/6/7/35/5/1/109/25/7/8 + LOC_ANCIENT map + GEO_FEATURES 缺源回退空）全 PASS + build 16,362,211→16,364,502 B + verify ALL PASSED。待续梯队：**lineage 人名 EN 数据回填**（personas.json 余 59 条目 name_en/name_sa 逐条考证补全）、`dynasties` 带/`_huayanCore`/`_MINI_REGIONS` curated 数据（见 ⑱ 待续梯队）等）；⑳（Tab2 华严文献 + Tab5 世主妙严·死码覆盖清零）——用 explore 引擎对 Tab2-6 与 article.js 全量扫描后，架 DOM/Canvas/注入全局的双文件 node harness 对「旧硬编码 vs 新数据驱动」做**逐字节渲染对比**，将两处整块死重复覆盖接入注入源：**①Tab5 cosmology.js 华藏世界海**——`COSMO_WINDS`(10 风轮)/`COSMO_LAYERS`(20 世界层) 原为硬编码数组，而 build.py 早已注入 `COSMO_DATA.cosmo_layers{windw,layers}`（内容逐条一致）；删除 14 行字面量改为 `COSMO_WINDS/LAYERS=…COSMO_DATA.cosmo_layers.winds/layers||[]` 解包。**②Tab5 cosmology.js 三界诸天塔 drawTower()**——`data` 22 行硬编码数组 + `colX/colW` 列布局 + 列头标签 + 图例 + 来源脚注，全部由 `data/cosmology/three_realms.yaml` 的 `realms`(18 行逐序一致)/`columns`/`legend`/`source` 驱动；删除多行改 `_tr=COSMO_DATA.three_realms` 读取（`data=_tr.realms||[]`、列头 `(_cols.practice||{}).label||…`、图例 `_tr.legend||[…兜底]`、来源 `_tr.source||…`）。**③Tab2 gap.js 总览区 5 处死重复**：`核心发现`(core_finding)、差异分布 5 卡(field A-E、字段 key 名 icon/label/color/description)、4 文本变异案例(case_studies id/title/content)、3 学界观点(scholarly_perspectives author/affiliation/content)、84000 方法论+结构差异(methodology_84000 intro/categories、structural_differences 多行块)，全部改读 `GAP.content.*`（build.py load_gap 已把 gap_content.yaml 并入 GAP.content）。**渲染零回归验证（关键）**：双文件 harness 注入相同 `COSMO_DATA`/`GAP` 全局（从构建产物提取），对比旧(HEAD)与新(工作区)的 `renderCosmology()`/`renderGap()` 产出 `innerHTML`——cosmology **逐字节 identical=true**；gap 经「剥离 `<b>/<i>` 与空白」归一化后**仅余两处纯样式差异**：(a) 84000 方法论各条目间旧加的 `；` 分隔符去掉（本已 `<br>` 分行，冗余），(b) `核心发现`/案例中旧 `<b>` 加粗去除（YAML 为纯文本、不掺 HTML）。均系**非语义的呈现差异**，无任何内容丢失。node --check + build 16,357,892 B + verify ALL PASSED。待续梯队：**Tab3 practice.js 遗两块硬编码**——`renderYikongSection` 法脉传承表（11 行 龙树→当代，`yikong_daodi.yaml` 无此结构，需另建 `lineage_table` 字段）、`最新动态` 新闻一句式（2023-2026，可迁 `teaching_resources.latest_news`）；`init.js` `_aliases` 人名别名映射（8 组，搜索配置、可考虑数据化）；已证实 Tab4 frontier/spirit/article.js 全数据驱动无 stray 硬编码。⑲ 待续梯队延续：lineage 人名 EN 数据回填、lineage `dynasties` 带/`_huayanCore`/`_MINI_REGIONS` curated 数据（见上）；㉑（Tab3 华严教行·practice.js 遗两块硬编码清零）——⑳ 待续梯队所记 Tab3 两处硬编码迁入 YAML 并补中英对照：**①法脉传承表**——`renderYikongSection()` 尾段 11 行 `<tr>`（印度奠基→当代）及表头/标题为硬编码字面量；`data/practice/yikong_daodi.yaml` 顶层新增 `lineage_table` 字段（headers/headers_en + 11 rows，每行 period/persons/contribution + `_en`，内容照抄原硬编码=非新增史实；EN 为既有中文行的忠实译写并循全站人名/术语表：龙树=Nāgārjuna、鸠摩罗什=Kumārajīva、三论=Three Treatise、应成/自续=Prāsaṅgika/Svātantrika、慧灌=Ekan 等），practice.js 改数据驱动渲染（`lt.rows` 缺则回退不渲染）。**②最新动态一句式**——原 `2023: 国立台北大学杰出校友 · 2026: 九九华严TICC讲座 · 2026.7: 支提山动土 · 第四期佛教。` 硬编码于 renderPractice()；`data/practice/teaching_resources.yaml` 顶层新增 `latest_news`（title/title_en + 4 items 每 date/text/text_en，第四期佛教条目 date 空=原句无年份前缀；事实均有源：2023 杰出校友与 TICC 九九华严见 docs/ref海云继梦法师_佛法修行体系研究.md，支提山动土与 teaching_resources.temples 2026.7.9 描述及 events/anim_waypoints 互证；EN 循既有译法：九九华严=Ninety-Nine Avatamsaka、支提=Chiti、TICC=Taipei International Convention Center）。**渲染零回归验证**：practice_render.js 双文件 harness（同注入构建产物完整 `PRACTICE_DATA`/`HAIYUN_RESOURCES`，DOM stub 捕获 pv.innerHTML）对比 HEAD 硬编码版 vs 数据驱动版——法脉表 zh 去 `.en-line` 归一后 **918==918 字节一致**、12 行（表头+11 数据行）不变、新增 34 EN span（11 行×3 列+标题 EN）；最新动态 zh 句逐字节一致、新增 title_en+EN 句。node --check + build 16,357,892→16,381,035 B（+~23KB：YAML 增容+EN 渲染）+ verify ALL PASSED。待续梯队：**practice.js res-sources「信实可靠的出处与参考资源」表**（renderPractice 尾段硬编码 11 行书目/播客/频道/链接 + 来源可靠性说明，第 404-418 行，静态 curated 参考资源，可迁 `haiyun_resources.yaml` 或新建字段——结构待考）、**`init.js _aliases`** 人名别名映射（8 组搜索配置、可考虑数据化）；⑱⑲ 待续梯队延续：lineage 人名 EN 数据回填、lineage `dynasties`/`_huayanCore`/`_MINI_REGIONS`；**㉒（Tab3 华严教行·res-sources「信实可靠的出处与参考资源」表清零）**——㉑ 待续梯队末项迁入数据并激活「孤儿数据」：**该表此前在 `meditation_essentials.yaml` 已载入 PRACTICE_DATA 却从未被前端消费（死数据）**，且其 `reference_table`（title/description/headers+`_en`、9 行 category/name/detail/links 每项 `_en`、reliability_note+`_en`）与 practice.js renderPractice 尾段硬编码 res-sources 块（原第 404-418 行）**内容逐条一致**，故本轮不再另建 YAML，而是「激活既有源 + 删除硬编码」双收：①YAML `reference_table` 小幅数据校正——补 `title/title_en`/`headers_en`；将 description 三个第一手来源（大华严寺官方资料/海云继梦和上讲经逐字稿/正式出版物）与播客「46集」补 `**` 加粗标记、reliability_note 补「⚠ **来源可靠性说明:**」前缀（均由 `_mdInline` 渲染回 `<b>`，与原硬编码字节一致）；Apple Podcast 链接归一为百分号编码版（与硬编码完全同前，原 YAML 为未编码中文路径）；EN 首字母人名译写从「Jirong」校正为全站固定名「Jihong」（海云继梦）。②practice.js 删除约 20 行硬编码表改为数据驱动渲染（`rt=PRACTICE_DATA.meditation_essentials.reference_table`，缺则回退不渲染；表头/9 行/来源说明全部由数据渲染，EN 以 `.en-line` 随全局显隐）。**渲染零回归验证**：practice_render.js 双文件 harness 对比 HEAD 硬编码版 vs 数据驱动版——res-sources 段 zh 去 `.en-line` 归一后 **2564==2564 字节一致**、10 行（表头+9 数据行）不变、新增 43 EN span（title/description/表头 4+9 行×(category+name+detail+links)）；yk 法脉表与最新动态两项既有验证保持 PASS（918==918、news zh 逐字节一致）。**`_mdInline` 复用**：确认 common.js 内联 md 转换器（`` ` ``→code、`**`→`<b>`、`*`→`<i>`、`[x](y)`→链接）可直接把数据文本安全渲染，无需各自护 HTML。node --check + build 16,381,035→16,381,042 B + verify ALL PASSED。至此 **Tab3 practice.js 遗硬编码全部清零**。待续梯队：**`init.js _aliases`** 人名别名映射（8 组搜索配置、可考虑数据化）；⑱⑲ 待续梯队延续：**lineage 人名 EN 数据回填**（personas.json 余 59 条目 name_en/name_sa 逐条考证补全）、lineage `dynasties` 带/`_huayanCore`/`_MINI_REGIONS` curated 数据；**㉓（lineage 人名 EN 数据回填·59/59 清零 + 全站「Haiyun Jihong→Jimeng」校正）**——待续梯队首项完成：①`personas.json` 15 条既有条目补全——9 条缺 name_en/name_sa 的补全（020b 智军=Yeshe De/Jñānasena〔84000 考据：藏 ye shes sde，梵 jñānasena，英直译 Bande Yeshé Dé/Yeshé Dé/Bandé Yeshé Dé 等皆通行〕、110 法显=Faxian、111 玄奘=Xuanzang、112 义净=Yijing、117 慧超=Hyecho〔en.wiki 条名，梵 Prajñāvikrama，704-787〕、122 一行=Yixing、123 慧果=Huiguo、124 空海=Kūkai、125 六师外道=Six heterodox teachers 集体名）＋6 条仅缺 name_en 的补 en（113 真谛=Paramartha、114 求那跋陀罗=Gunabhadra、115 不空=Amoghavajra、116 竺法护=Dharmaraksa、120 善无畏=Subhakarasimha、121 金刚智=Vajrabodhi）；②44 条仅存于 graph.json 的人补入 personas.json（95 人全量入册，含 name_zh/name_en/name_sa/name_bo/ti/birth_date/death_date/related_huayan/sources/verified 全字段，逐条考证：韩系 Wonhyo/Uisang/Kyunyŏ〔en.wiki 条名〕、日系 Rōben/Jitchū/Tōjō/Shōbō/Kanken/Myōe/Gyōnen〔kotobank 读音〕、唐密三藏、罗什/世亲等印度系、Sanskrit 名 IAST、近现代 Kūkai 常规定名）；经此 **全部 95 人有 name_en，65 人缺 name_sa（中文/日系名无梵文对应对〔待核〕留空）**，导入后 SQLite 校验 persons 95 / name_en=95 / name_sa=30。③顺带发现并纠正全站人名英译错误——批次 ㉑㉒ 曾把 AI 生成错体「Jirong」「Jihong」当固定名写入 `meditation_essentials.yaml`+`CLAUDE.md` 固定术语表，实际 **海云继梦官方英文正体为 "Haiyun Jimeng"**（大华严寺 huayen.world/en 「founder, Master Haiyun Jimeng」、Triple Crane lineage 页「Venerable Master Haiyun Jimeng (海雲繼夢)」、Baidu EN「Venerable Haiyun Jimeng」；繼夢=jìmèng→Jimeng）；本轮将全站 ~40 处「Haiyun Jihong」+8 处「Haiyun Jirong」统一为 **Haiyun Jimeng**（practice/spirit/translation 16 个 YAML 各 `_en` 字段），修正 `CLAUDE.md` 固定术语表，并**保留 ㉒ 历史登记原文不动、仅在本批登记中如实说明**。验证：SQLite 校验 missing_name_en=0・graph.json 重建・build 16,369,519 B・verify_demo ALL PASSED・lineage.html 人名 EN 抽查命中（Yeshe De/Kyunyŏ/Rōben/Swami Pranavanad 等）；graph.json（导出格式）本身不含 name_en，name_en 经 db_reader load_graph() 直接注入 HTML（lineage 页 95 节点全载）。另注：`scripts/import_all_to_sqlite.py` 的 `import_chapters` 用 plain INSERT、对已存在的 41 行 chapters 会报 UNIQUE constraint，属既有非幂等小瑕疵（persons 等前序段已各自 commit，不影响本批），待后续顺手改 OR REPLACE。待续梯队：**`init.js _aliases`** 人名别名映射（8 组搜索配置、可考虑数据化）、⑱ 遗留 `dynasties` 带/`_huayanCore`/`_MINI_REGIONS` curated 数据；18 条 no_dates person（birth/death 缺，需另考史料）、65 条 name_sa 缺（中文/日系人名无梵文对应留空〔待核〕，部分经名化人物如玄奘=Mahāprajñā 等可再考证）；**㉔（init.js `_aliases` 搜索别名映射数据化）**——待续梯队首项完成：新建 `data/events/search_aliases.yaml`（build.py `load_events()` 自动 glob `events/*.yaml` → lineage.html 注入 `var SEARCH_ALIASES`），将 init.js 硬编码 10 组人名别名映射迁出，`_matchSearch` 改为 `_aliases=(SEARCH_ALIASES?.aliases)||{}`（含 ㉓ 已订正之「海云继梦/海雲繼夢」简繁异写新增 2 组）；零硬编码回归（init.js 仅余渲染/交互/下载逻辑），build 16,371,444 B + verify_demo ALL PASSED + node --check 通过。待续梯队：⑱ 遗留 lineage.js `dynasties` 带/`_huayanCore`/`_MINI_REGIONS` curated 数据迁移；18 条 no_dates person（birth/death 缺，需另考史料）；65 条 name_sa 缺；`import_chapters` 非幂等小瑕疵（plain INSERT→UNIQUE，待改 OR REPLACE）；**㉕（lineage.js 遗留 curated 数据迁移·三块清零）**——⑱ 遗留完成：①`dynasties` 时间轴代色带 6 段迁入 `data/events/timeline_dynasty_bands.yaml`（`TIMELINE_DYNASTY_BANDS.bands`，与 dynasty_boundaries.yaml 地图疆域形状不同各自独立）；②`_huayanCore` 关系图核心白名单 6 id（五祖+海云继梦）迁入 `data/events/huayan_core.yaml`（`HUAYAN_CORE.core_persons`）；③`_MINI_REGIONS` 10 区域迷你地图配置迁入 `data/events/mini_map_regions.yaml`（`MINI_MAP_REGIONS.regions`，与原 ⑱ 计划判断「可接受为代码常量」相比更彻底——一并数据化）；三处均按既有模式解包 `(typeof X!=='undefined'&&X&&X.key)?X.key:[]`，lineage.js 自此 curated 数据清零；build 16,381,843 B + verify_demo ALL PASSED + node --check 通过。待续梯队：17 条 no_dates person（birth/death 缺，需另考史料）；**㉖（人员数据深化·确证子集）**——①生卒年补实：龙树（Nāgārjuna）birth 150 / death 250（学界通说 c.150–250 CE，en.wikipedia / IEP / EBSCO 多源交叉印证，source 追加「学界推定」注记）已填入；②`verified` 回填 43→54（+11，逐条考实）：月霞 1858-1917（近现代史传·南海佛教网）、常惺 1896-1939（南通佛教网,「民国28年元月14日圆寂」）、南亭 1900-1982（华严莲社资料+星雲《参学琐忆》1900-1982 + 华严莲社周年论文）、成一 1914-2011（淮南佛教网·生于1914年2月28日、2011年4月27日圆寂，莲社《法脉渊源》论文 1914-2011）、智光 1889-1963（莲社论文）、应慈 1873-1965（莲社《南亭华严思想》论文）、了中 1932-2022（凤凰网讣闻·1932年10月28日生、2022年3月9日圆寂）、持松 1894-1972（百度百科/凤凰/维基 1894-1972 圆寂于11月）、贤度 b.1960（莲社论文「（1960 迄今）」）、梦参 1915-2017（本项目 docs/梦参老和尚_综合深度研究.md）、龙树（学界通说）；③`name_sa` 不造——**考证确证玄奘无梵文个人名**（其在印称号为 Mahāyānadeva 大乘天 / Mokṣadeva 解脱天，系称号非人名），故 ㉔ 记录中「玄奘=Mahāprajñā 可再考证」之假设不成立，name_sa 维持 30/95、中文/日系人名〔待核〕留空不再臆补；④顺带修复既有非幂等小瑕疵：`import_chapters` 两处 plain INSERT→INSERT OR REPLACE（㉓ 已登记待改），重导入不再报 UNIQUE、chapters 41 行稳定。验证：import_all_to_sqlite 全程通过 → export --verify（verified=54、name_sa=30、no_dates=17、no_lineage=8）→ build 16,381,843→16,382,005 B → verify_demo ALL PASSED。待续梯队：17 条 no_dates person（birth/death 缺，需另考史料，其中当代学者/日韩系/大华严寺法脉等无生平可考者保持 0+〔待核〕）；41 条 verified=0 待逐条考实（当代学者、日韩系、大华严寺法脉相关性较弱者可保持 0+注明）；name_sa 65 缺中多为中文/日系人名本无梵文名（〔待核〕留空），仅个别经名化人物待对准（如慧果等密教灌顶名）；**㉗（人员数据深化·verified 回填二度·54→72·18 条）**——㉖ 待续梯队「41 条 verified=0 逐条考实」首批 18 条按考证优先依据权威/一手来源逐条回填＝1（年份分歧或约数均在 source 注明）：①近现代/禅净——慈舟 1877-1958（百度百科＋道源《慈舟大师传》直证：光绪三年九月十九生、民国四十七年一月六日往生〔个别传作 1957〕）、真禅 1916-1995（上海玉佛寺方丈·当代公认）、虚云 1840-1959（《虚云和尚年谱》，出生年 1839/1840 有异说、DB 用通行 1840 世寿120）、净慧 1933-2013、南怀瑾 1918-2012（均当代公认）；②华严宗史/印度系——慧苑 673-743（百度百科/维基/中华典藏多源「约673-743」，source 注〔约〕）、慧光 468-537（《续高僧传》卷廿一·慧光传定说）、子璿 965-1038（维基华严宗条「長水子璿（965-1038）」）、马鸣 80-150（祖传+学界推定，source 注〔约〕）、无著 310-390（《大唐西域记》+学界推定，source 注〔约〕）；③韩系——元晓 617-686（韩国佛教史/学术研究）、均如 923-973（维基华严宗条「均如(균여，923-973)大華嚴首座」）；④日系——良弁 689-774（日本佛教史，注：有 773/774 异说〔并存〕）、圣宝 832-909（醍醐寺开山）、明惠 1173-1232（高山寺中兴）、凝然 1240-1321（东大寺学僧·八宗纲要）、审祥 d.742（精選版日本国語大辞典「七四二年没」＋学术论文「？～742」，另有「生没年不詳」说〔并存〕）；⑤大华严寺系——海云继梦 b.1950（大华严寺法脉资料一手）。**保持 0 不回填〔待核/无独立文献〕**：菩提流支（永平元年 508 至洛阳可证、卒年 527/530 诸说未定）、大华严寺印度瑜伽行法脉（普拉梵纳德 1884-1959/克利普梵纳德 1913-1981/胜师子王菩萨 1931-2023＝派内传承记录）、日系实忠/等定/观贤、福慧寺思元慧三/体化性果、当代学者魏道儒/王颂/邱高兴/张文良（无公开生年）。验证：import 全程通过（verified=72・no_dates=17・name_sa=30・name_en=95）→ build 16,382,005→16,383,361 B → verify_demo ALL PASSED。待续梯队：41 条 verified=0 余 23 条（菩提流支/大华严寺瑜伽行法脉/当代学者/日韩系等，无力考者保持 0+注明）；17 no_dates 保持留空〔待核〕（世亲/支娄迦谶/般若/胜友/智军等古代译师无个人生卒可考、燃灯/迦叶/毗卢遮那/六师外道等神话·集体人物本无年代）；name_sa 65 缺多为中文/日系人名本无梵文名（〔待核〕留空），仅个别经名化人物待对准（如慧果等密教灌顶名）；**㉘（人员数据深化·㉗ 锚点错位勘误＋菩提流支/慧果考证实录）**——①**勘误 ㉗ 日系三 edit 锚点错位（commit 4aade38 后经正文逐条比对发现）**：㉗ 批以「`"id": "person_j02"` 等」为锚，实际匹配到该 id 前置条目，致良弁(j01) 被误安审祥出处注「精選版大辞典：742没」、实忠(j02) 被误翻 verified=1、审祥(person_050) 实际未翻；净数 72 因「实忠替审祥」侥幸未变而掩盖错位。本轮校正：审祥 verified 0→1＋source「日本佛教史（精選版大辞典：742没；另有『生没年不詳』说）」、良弁 source→「日本佛教史（有773/774异说，verified 保持1）」、实忠 verified 1→0＋source→「日本佛教史」。固化惯例：**人名级 data edit 一律以 name_zh 为唯一锚、并以最近 name_zh 校验匹配**，import 后抽查对照。②**菩提流支卒年考证实录**——复核《续高僧传》卷一原文「三藏流支自洛及邺，爰至天平二十馀年」（天平 534-537，彼时尚在译经），**旧标 527 与该一手文献直接抵触**；卒年 527/530 等诸说未定，故 death_year 527→留空〔待核〕，source 注明。③**慧果灌顶名考证实录**——多源（维基/凤凰佛教/中华典藏/世界佛教美術圖說大辭典）印证 746-805（已 verified=1）；「遍照金刚」系其弟子空海 805 所受灌顶名，**慧果本人无通行梵文灌顶名**，name_sa 保持空〔待核〕——㉗ 待续梯队「个别经名化人物待对准」此例的闭环结论即«无可对准、如实留空»。验证：import 全程通过（verified=72〔净数不变〕・no_dates=17・name_sa=30・name_en=95）→ build 16,383,361→16,383,961 B → verify_demo ALL PASSED；**㉙（Tab4 前沿对话·条目级 EN 补齐·83 学者卡）**——2026-09-02 快照列为首要双语缺口，本轮清零：`frontier_dialogue.yaml` 5 节 19 域共 83 条 `related` 卡（相关研究与人物）原全 zh-only，现已全部补 `description_en`（逐条忠实对译、循全站固定术语表：因陀罗网=Indra's Net、事事无碍=total unobstruction、法界缘起=dependent origination of the Dharma-realm、阿赖耶识=ālayavijñāna、性起/性具=arising from the nature/nature-inclusion、无情有性=nonsentient beings possess buddha-nature、理一分殊=one principle, many manifestations、一即一切=one is all, all is one、能所双泯=dissolution of subject and object；专名照原文：Gelassenheit/waḥdat al-wujūd/Prāsaṅgika/vipassanā/śūnyatā；书名给通行对照如「New Commentary on the Avatamsaka Sūtra (Xin Huayan Jing Lun)」；人名全站表：海云继梦=Haiyun Jimeng、法藏=Fazang、宗密=Zongmi、临济义玄=Linji Yixuan、明惠=Myōe、龙树=Nāgārjuna、月称=Candrakīrti、智顗=Zhiyi、牟宗三=Mou Zongsan 等）＋中文机构/人名补 `affiliation_en`/`name_en` 45 条。插入方式：行级 YAML 注入脚本（以 domain id+related index 定位，`yaml.safe_dump` 单行标量并剔除 block 模式自动追加的 `...` 文档结束符；重载校验 83/83、无污染残留）。`frontier.js` 渲染器扩展——related 卡新增 EN 副行 `<div class="en-line rel-en">`（name_en||name ＋ affiliation_en||affiliation ＋ description_en）随全局 `.en-line` 显隐。经此 Tab4 域级（en_domain/en_core/en_persp 已有）与条目级（83 卡）EN 齐备。验证：rel YAML 重载 83/83 → node --check → build 16,383,961→16,498,369 B → verify_demo ALL PASSED。待续梯队：L-C 善财〔待核〕项闭环（84000/CBETA 复核）、source-audit T3 36 条细化、texts.title_en 3/54 多语补充
  4. 沉淀为新内容默认规范（见 `docs/bilingual-annotation-design.md`）。
- 校验：英文对应与中文一一对齐，由批注块前缀/数据字段一致性检查兜底；不因双语引入未经考证的译名。

## 考证/双语完成度快照（2026-09-02 · L.㉜ 后，全站既有内容盘点）

- **考证**：persons 95/95 全有 source（0 缺源，T0 归零）；来源可靠性评分 76/100，T3 模糊来源 10 条（㉛ 已由 36 细化归并，余 10 均无独立一手史料——明度/体佛/如孝/雪窦/成观/拉克鲁希/巴布基/克利普梵纳德/思元慧三/体化性果，已标〔待核〕/〔待考〕）；`verified=1` 72/95（75.8%），`verified=0` 23 条均为无力考者并注明（菩提流支〔卒年诸说未定〕/大华严寺瑜伽行法脉及宗内谱系 6 人〔系派自述无独立史料〕/当代学者·法师〔无公开生卒〕）；生卒年 no_dates 双缺 17 条（古代译师与神话·集体人物本无考）、单缺 11 条；图谱 98 边/24 法系/30 地点（0 缺坐标、16 有 city、均在 import_edges 补 `source='graph.json'` 后 0 缺源）；文献 54 部（CBETA ID 12・大正藏编号 35）、41 品、50 术语、180 人地关联、15 文章页。遗留待核：source-audit T3 余 10 条（均无独立史料）、L-B 专题定值复审未二轮。
- **中英结合**：人名 name_en 95/95（100%）・name_sa 30/95（32%，余 65 中文/日系名无梵文对应留空〔待核〕，玄奘/慧果两例考证已闭环）；术语表 50/50 条 term_en+definition_zh+definition_en 全覆盖、term_sa 32/50；经目 title_en 54/54（㉚ 补齐 3/54→54/54・title_sa 6・title_bo 1，多语仍不全后续补充）；数据层 `_en`/`en` 键：practice 1461・translation 103・cosmology 41・knowledge_graph 96・frontier 88・events 0（地理史料以拉丁文为主）；全站 6 Tab+15 文章页均带 `.en-line` 全局双语机制。遗留缺口：title_en 已全、剩 title_sa/title_bo 多语待补，person bio 级 EN 需 SQLite 增设列（考证优先暂不臆造）。

## 渲染/显示修复登记（2026-09-02 · L.㉝）

- **问题**：`articles/vijnana-mind.html`（及作者怀疑「其他页面」）英文对应不显示。实测该文数据完整（72 引用块 / 69 EN 块经浏览器同款渲染器正确归类为 `.en-block`）；根因是浏览器 `localStorage` 残留的全站「仅中文」开关 `site_lang='0'` 与文章页 `article_en_hide='1'`——`common.js` 载入时读该持久状态给 `body` 加 `zh-only`，common.css 以 `display:none!important` 隐藏全站所有英文块，且跨会话永久生效。
- **修复（㉝，源头治理改 src 再重建）**：①`web/demo/src/common.js` 阅读语言开关由持久 `localStorage` 改为**会话级 `sessionStorage`**——默认恒为中英对照，`仅中文` 只影响当前标签页会话、关标签即恢复；载入不再读旧 `site_lang`，切换时 `removeItem` 清理旧值；②`web/demo/src/article.js` 文章页「英文批注」开关同改会话级；③重建 `web/demo/js/common.js` 与全站页面，确认内置 common.js/article.js 均不再读取旧隐藏键；`verify_demo.py` ✅ ALL CHECKS PASSED。
- **效果**：用户**无需手动清缓存**，刷新即默认显示英文（旧 localStorage 残留被忽略）。此为显示层行为修复，不改变 考证/双语 内容快照数字。
