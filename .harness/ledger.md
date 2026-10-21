# Ledger (append-only)

> Memory depth: **durable**. Never overwrite history; corrections are new rows.

| time | actor | action | basis | result |
|---|---|---|---|---|
| 2026-10-16T23:04:05+00:00 | harness-factory | init | task intake | scaffold generated (13 files) |
| 2026-10-17 | agent | 定制 AGENTS.md 为薄入口（SSOT 声明+入口地图+五硬规则+本仓铁律） | R4 确认：薄入口 | done |
| 2026-10-17 | agent | 登记本仓既有 `verify_*` 为 `.harness/gates.md` 硬门 | `Makefile` L96 `verify-all` | done |
| 2026-10-17 | agent | 填 `capabilities.local.md` 落地表；记 `.harness/decisions.md` R4 决策；补 `PROVENANCE.md` 推导来源 | M0.4/M0.5 | done |
| 2026-10-17 | agent | (A) 批·一：经文回源审计（块119/串2,612）→ 修复真缺陷 2 例（第三部 `辭辨智`→`辭辯智`；第五部 疏引「百一偈」据 `T1735` 订正） | T10n0279／T09n0278／T1735 逐字回源 | done（本地 commit，未 push） |
| 2026-10-17 | agent | `华严经学_三十九品深度研究.md` 内部矛盾订正 6 项（五周因果表回源·七处九会表·各会品—卷实检·十回向品卷数·四十华严经号·藏译二品会归属）＋文末修订志 | T1735 五周因果原文；T10n0279 卷首品题实检；Toh44 位次＋84000 | done |
| 2026-10-17 | agent | 观察：全仓「引文见于 CBETA」自动判定缺完整简→繁表，噪声极大（2,485/9,902 多为误报）→ 记为待办，不据此改文 | 自建审计 v1–v5（temp，已清理） | recorded |
| 2026-10-17 | agent | 第六品《毗盧遮那品》专篇成篇（§〇–§九·1,315 行；卷11·offset 309864–332004；实测 4,939 字／73 颂／四佛 2,426·1,082·479·131） | 用户裁示「按计划开写」＋`T10n0279` 卷十一回源 | done（本地 commit，未 push） |
| 2026-10-17 | agent | 第六品注疏三家会读（澄观 `T1735` 品6科判／法藏 `T1733` 二光二遍／李通玄 `T1739` 十五条）；新得「大威光＝毗盧遮那」补文（`T1735` L5089–5091）与「经来未尽」「所信因果会竟」两判 | T1735/T1733/T1739 逐字回源 | done |
| 2026-10-17 | agent | 用户裁示③「六十卷四约20名对勘」本批交付：**第五部 §6.9 新立**，逐名对勘八十中央世界种二十重；订正原图（对「中央二十重」非「十海首名」）；附录四#8〔待核〕→✅已办 | `T09n0278` 卷四原文＋`T10n0279` 卷八中央二十重 | done |
| 2026-10-17 | agent | 第六品登记发布（`standalone_articles.yaml` 新增 `piluzhena`；系列总纲同步；`next-phase-plan.md` 增 L.133）；新脚本 `scripts/pilu_shena_studies.py` | 系列体例 | done |
| 2026-10-17 | agent | 门禁全绿：`build` 42 files｜28,365,369 B；`verify_demo` ✅ ALL CHECKS PASSED；`test_pipeline` ✅；`verify_sources` EXIT=0；`git diff --check` 净 | verify_* 五关 | done（真机渲染未确认） |
| 2026-10-17 | agent | 观察：`docs/草稿/高僧传/僧传画像/*.html` 有他会话在途改动（13→20 层）；`docs/祖师人物/不空三藏…md` 未跟踪——**本批未触碰、未纳入提交** | `git status` | recorded |
| 2026-10-17 | agent | SSOT 漂移订正：`系列总纲` §二 品6「⬜待开」→「✅已成篇」（与 §三.1 自相矛盾）；`CLAUDE.md` 当前进度补登 L.133（第六品） | 自我 commit 遗漏＋门禁重跑全绿 | done（本地 commit `a2576e2`，未 push） |
| 2026-10-17 | agent | 评估：按七处九会，**第一会（品1–6·卷1–11·所信因果周）六品皆已成篇＝完整**；附记 `三十九品研究` §2.1「第一会 场所＝世间净眼普严殿」于 `T10n0279` 无此组合〔待核〕 | `三十九品研究` §2.1/§2.2（据 `T1735`）＋澄观「所信因果會竟」（`T1735` L5090） | recorded |
| 2026-10-17 | agent | L.135 第一会部 2–6 补 `### 5.2′`（智俨 `T1732`）／`### 5.2″`（慧苑 `X0221`）；部 1 附录八补 `### 八.9`／`### 八.10`（共 12 处插入） | 用户「先落实第 2、3 项」＋二帙部首归一后逐字回源 | done（本地 commit，未 push） |
| 2026-10-17 | agent | 结构判定并落实：**`T1732` 依六十本**（其〈盧舍那佛品第二〉统摄八十品 2–6）→ 部 3–6 之 5.2′ 只引其品 2 通判并明此理；**`X0221` 依八十本** → 逐品直引 | `T1732` L170/L422–454；`X0221` 品 2–6 | done |
| 2026-10-17 | agent | §5 体例订正（(A) 批·二之体例骨架一致性·部分）：部 3/4/5/6 计数标题及台账行改「诸家」；部 4/5 体例「取古今四家——」（仅列 3 家·旧稿误计）→「三家」 | 现有对照表实列 3 家（澄观/法藏/李通玄） | done |
| 2026-10-17 | agent | 新增门禁 `scripts/verify_round_h2.py`：6 部新增节 `> 「…」` 引文按底本归一逐片段子串校 → **34 片段／0 失配**；**揪出并订正 3 处误引**（部 6「無異」→底本「無失」；部 5 梵名删夹注小字 `(入呼)(上呼)` 致不连续；部 1 十门·部 2 科判之撮录当逐字引） | `T1732`/`X0221` 归一比对 | done |
| 2026-10-17 | agent | 门禁全绿：`.harness/check.py` ✅；`verify_sources` 系列 7 篇仍入覆盖（存疑各 +2：部1 231·部2 49·部3 39·部4 38·部5 41·部6 40）；`t1_quote --check` ✅（31 条/0 失配）；`verify_t1_bikan` ✅；`build` 42 files｜28,399,096 B；EOL 保持（部1 CRLF 4475/0；部2 仍 16 裸 LF 未增；部3–6 纯 LF） | verify_* 诸关 | done（本地 commit，未 push） |
| 2026-10-17 | agent | 观察（勿提交）：工作树含他会话在途件（`docs/草稿/高僧传/僧传画像/**`·`docs/祖师人物/不空三藏/玄奘_全方位文献综述.md`·CBETA ingest `T50n*.xml`/`INGEST_log.md`·`data/references/cbeta/README.md`·**已 staged 之** `scripts/cbeta_extract.py`/`fetch_cbeta_history.py`）——本批未触碰、以显式路径提交 | `git status` | recorded |
| 2026-10-17 | agent | L.136 (A) 批·二 ① 体例骨架一致性：部 3 台账节→`## 九、台账（成篇自陈）`列式；部 2 末尾新增 §九；部 3 §七去尾缀；部 2 §八→`## 八、附录（十一类）`；部 4 补 `---`＋成篇识；残留「四家」清零（部 3 L477·部 4 L614·部 5 L897·部 5/部 6 成篇识） | 与部 4/5/6 台账模板对齐；用户「1，2」 | done（本地 commit，未 push） |
| 2026-10-17 | agent | L.136 ② 标记完备度普查：六部 §〇 皆声明标识符号·附录皆 11 类·部 2–6 §九 四要件齐；计数 待核 257／本文判断 233／未竟 12／存疑 50／转述 2；`〔校记〕/〔校异〕/〔据实〕/〔修订〕` 六部皆 0 | 自建普查＋标题 dump（temp，已清） | done |
| 2026-10-17 | agent | L.136 ③ 数据层复算核验（复跑自陈脚本＋独立重算）：部 1/2/4/6 全合；**订正 部 3「三昧」32→29·「世界海」22→18；部 5「有世界，名：」240→247·「香水海」99 说明改为「＝环10＋外围89，中央别计」**；部 5 §7.5「一切数字皆此一命令所出」→别白 | `miaoyan_metrics`/`ru_lai_studies`/`sjcj_puxian_studies`/`huazang_shijie_studies`/`pilu_shena_studies` ＋ `T10n0279` 重算 | done |
| 2026-10-17 | agent | L.136 发现（待授权）：①部 4 §5.1–5.3 注疏引文作简体（与「引注疏原文一律繁体照底本」不合；部 4 无繁体「無礙」0/47，部 5 9／部 6 12；部 4／部 5 §5〔体例〕注较部 6 L735 缺该句）②部 1 L55/L61 重复 H3（全仓唯一）③Zipf 口径 部 1/2（秩1–200）vs 部 3–6（全秩）不统一 | 引文简繁普查＋重复标题扫描＋脚本源码 | recorded |
| 2026-10-17 | agent | L.136 核订 `三十九品研究` §2.1：`世间净眼普严殿`→`阿兰若法菩提场`＋〔L.136 校订〕注（`X0221` L3181「約處。名摩竭提國法阿蘭若菩提場會」一手佐证） | X0221／T1735／T10n0279 | done |
| 2026-10-17 | agent | L.136 第 2 项：`T1871`《華嚴經旨歸》补入 `三十九品研究`（§2.4＋§八 参考文献＋修订志 3 条）与 `系列总纲`（§五 bullet／§六 行／新 §八 十义大纲／L5）；细目逐字核实底本；底本自歧二处照录不统一 | `cbeta_txt/T1871_法藏_华严经旨归.txt` L45–451 | done |
| 2026-10-17 | agent | L.136 门禁全绿：`.harness/check.py` ✅｜`verify_round_h2` 34 片段/0 失配｜`verify_sources` EXIT=0｜`t1_quote --check` 31 条/0 失配｜`verify_t1_bikan` ALL PASSED｜`build` 42 files｜28,412,788 B｜EOL 全保 | verify_* 诸关 | done |

- 2026-10-17 kx2 校勘落改闭合：8页~35处（MISS✓ 9→0·错挂史源归位 huineng/jianzhen/huiyuan/zhiyi/peixiu·盘外降◐ bukong/fazang+两页图例全局校勘注·T2061立碑真逐字升级·扫描器 SIGLA 复形与命名檔兜底二修 attr?62→6）·四闸全绿·零入库；下轮 jj1 净检深填。

- 2026-10-17 jj1 净检深填闭合：jingjian.html 拉平 20 层 A–U（T50n2063 本传并序 79 片段全命中✓·待核 0 全站唯一全净·新增「莫由諮稟/晋咸康中」归位与「其法不成」主体考定）；新建 scripts/quote_selfcheck.py 严格自查仪·四闸全绿·零入库；下轮 jq1 金乔觉。
- 2026-10-17 jq1 金乔觉新建页闭合：新建 portraits/jinqiaojue.html（order=10·单源丙C）·盘内 T50n2061 卷廿一〈九华山地藏传〉约500字逐字回采·20层A–U全拉平·64片段全命中待核0（全站第二全净页）；守律=本传不书「乔觉」(◐九华山志层追称)·本传未言「化身」(戊E不裁)·神异丁D与史实双栏；新建后自查8处省笔/简体标签「」→〔〕·复扫CLEAN；index 加金乔觉卡+规划中缩为仅空海+footer 11人；四闸全绿(build check 11页/harness/linkcheck 36/tagcheck)·零入库；下轮 kh1 空海（先估 T55n2161 御请来目录在盘史源）。
| 2026-10-18 | agent | 收束：品六 §5.3 十五条科判表格内李通玄原文节引繁体照底本订正（L856–L872），第一会 §5 格式一致性收束。 | 收束批次 | done（本地） |
| 2026-10-18 | agent | 品四 §5 补充关键术语精到英文对应（四門判/世界海/dhātu-samudra/差之無差-無差之差/二源成就/infinite interpenetration） | 英文对应试水 | done（本地） |
| 2026-10-18 | agent | 第一会六品 §5 补充关键术语精到英文对应（统一风格：fourfold analysis/main theme/textual division/ocean of worlds/infinite interpenetration 等） | 英文对应全六品 | done（本地） |
| 2026-10-18 | agent | 第二会首品《如来名号品》第七部框架创建（卷十二），沿用既定体例 | 第七品起草 | done（本地） |
| 2026-10-18 | agent | 第七品《如来名号品》**成篇**（§〇–§九；卷十二·品7）：211 名号＋序/请/说经文＋十方表＋六十本对读，逐字回源全相符 | `T10n0279` 卷十二／`T09n0278` 卷四／四家注疏 | done |
| 2026-10-18 | agent | 回源复核揪并订正：§5.2「聖同」→「世界同」；「此中有」→「於中有」（李通玄）；§2.6「十徵·三世佛母」误系李通玄→实出`T1735`澄观＋「為顯」→「為彰」；§1.2「信自己是佛」→「信自心是佛」；§2.5/§2.12 李通玄引文复原 | 归一子串比对 `T1735`/`T1739` | done |
| 2026-10-18 | agent | 第七品数据层**口径订正**：旧「3,223/独字406/含标点4,197」系**越界含次品品题『四聖諦品』**→ 净界重定 **含品题 3,226／净 3,219；独字 404；含标点 4,199**；「不可思議」1→2；§7.4 脚本改 XML 净界（剥 note/rdg/app） | `T10n0279` 净界复算 | done |
| 2026-10-18 | agent | §5.3′ 海云听录引文口径统一：**照听录原文（简体）逐字引录**（源为简体，与第一会同例），标点依例归一；`verify_haiyun_sec.py` **0 失配** | 听录二档逐片比对 | done |
| 2026-10-18 | agent | 第七品门禁：`.harness/check.py .` ✅OK｜`verify_round_h2.py` ✅ALL PASS（34/0，回归）｜繁体引文回源**零失配** | 门禁诸关 | done |
| 2026-10-19 | agent | 藏译独有品〈如来华严品〉（藏 11·`Toh 44-11`·梵 *Tathāgatāvataṃsaka*·汉译全缺）补入部 6、部 7 两篇；**会归属判归第一会末**〔本文判断〕三证（位次承汉 6／藏传段名「前十一章」/法义「无说法唯放光」·掌中世界海同汉品 2），反面读法并存 | 84000 编目·萨尔吉 2013〔T2〕·Park 2014〔T2〕 | done（未提交） |
| 2026-10-19 | agent | **扫描器登记补漏（本批最高价值）**：`第二会_普光明殿_差别因果周/` 未登记于三处扫描器（`evolution_config.yaml` scan.include／`audit_style.py`／`verify_sources.py` 之 RESEARCH_DOC_DIRS）→ 第七部**自创建起即被静默漏扫**；已补三处。验证：verify_sources 第七部入表（存疑x23·citex4）；audit_style files 53→54 | 三处同步铁律 | done（未提交） |
| 2026-10-19 | agent | **第七品结构复核**：① 补 **§5.4 诸家对读小结**（**其余六部皆有，唯第七部缺**）——五家表＋一家之见＋身业会归＋请数不强断；② §三/§四 粗体伪标题 → `###`（与六部体例归一，纯格式零改字）；③ §4.3 澄观三业补一手引证（`T1736` **卷十五**「先明如來三業正報。謂身語意…九身語既彰。意業將顯」）；④ 附录八／§九 台账同步 | 体例一致性 | done（未提交） |
| 2026-10-19 | agent | **发现（待授权·未擅改）**：部 6 §5 引言／§5.3／§5.4 表／§6.1 会读皆作「**李通玄就六十本立论**」，然一手核 `T1739`：目录为**八十 39 品序次**、用八十品名（毘盧遮那品）与「大威光」（**0 见**「普莊嚴童子」「盧舍那佛品」）→ 所依本**实为八十**；§6.1「第三·四佛之断」实为本机六十语料（卷3–4）之局限 | `T1739` 目录+正文一手核 | ⚠ 待授权 |
| 2026-10-19 | agent | 第七部括号：〔〕68/68·（）460/460·《》54/54 全平；「」411/412 之差＝§7.4 代码块内字符串（须含底本 」以精确匹配，非缺陷）；`check.py` OK／`verify_round_h2` ALL PASS（34/0） | 门禁诸关 | done |
| 2026-10-19 | agent | **用户授权：「先做 1,2，然后规划后续，最后 push」** → ①成篇登记（yaml 增 `rulai-minghao`＋总纲 §二/§3.1/§3.2/§五/§六/L5）②部 6 李通玄所依本六处订正（六十→**八十**，各留〔校订 2026-10-19〕）③`next-phase-plan.md` 增 **L.137** 十项＋`tasks/PLAN.md` 增 L.137 与六条后继规划 ④`build` **43 files／28,570,508 B**（新增 `rulai-minghao.html` 131,812 B）⑤本地 commit **1875b1e**（25 files）仅收本会话文件，他会话在途改动未触 | 用户明示授权 | done |
| 2026-10-19 | agent | **push 已办**：`daf67e3..1875b1e main->main`（rc=0）→ 线上核验：`web/demo/articles/rulai-minghao.html` **200／80,867 B**（与本地构建一致；「如来名号品」×25·「如来华严品」×7·「诸家对读小结」×3）、`articles/index.html` 200／31,009 B、`articles/piluzhena.html` 200／111,458 B | 用户「最后 push」明示 | done |
| 2026-10-19 | agent | **`verify_demo` 1 错·与他批无关（如实记录）**：唯一 FAIL＝`verify_jj_lectures.py`「B meta.episodes 12 ≠ 目录实测 14 集·台账漏收新集」＋ 8 项 measured 对账差。**根因**：`docs/hy_refs/*` 属 `.gitignore:37` 忽略区，他会话本地新增 OCR **ep13/ep14**（tracked-clean＝ignored，`git ls-files` 0 项），而 tracked 之 `data/research/jj_huayan_lectures.yaml` 仍 `episodes: 12` 未重跑 `jj_ocr_audit → _jj_build_lib`。**证与本批无关**：`git diff --stat HEAD~1 HEAD -- data/research/jj_huayan_lectures.yaml docs/hy_refs/` **为空**。**未代他批修**（不越权改他人在途语料台账）· 建议其重跑立册 | 观察／记录（M4 只观察不擅改） | open（他批待办） |
| 2026-10-18 | agent | **Ep 13/14 OCR 提取**：`docs/hy_refs/sub_extract/` 工具链产出 ep13 (dPzOJ_HLBJg · 720p · 3402 cues) + ep14 (xNej63VlSCw · 360p fallback · 3200 cues) 六件。Ep 14 因 YouTube SABR 新上传限制 403 → `--extractor-args "youtube:player_client=android"` 退 format 18·质略降（毗盧遮那三形异出）·已标 ⚠️ | 用户「把 13/14 提取」 | done |
| 2026-10-21 | agent | **L.138 Phase 0·SSOT 修复**：重跑 `jj_ocr_audit.py --json` → `_jj_build_lib.py`·`jj_huayan_lectures.yaml` 由 `episodes:12` → **`episodes:14`** (43,272 cues · 388,848 汉字·均 99.3%)；`verify_jj_lectures.py` **ALL CHECKS PASSED**（消 L.137 遗留唯一 FAIL） | 用户 R4 确认 Phase 0 | done |
| 2026-10-21 | agent | **L.138 Phase 1a·新开人定元数据**：新档 `data/research/jj_huayan_collation.yaml`，与实测台账职责分离；segment 三档 (玄談6/宏觀6/正行2) × 14·anchor_pin/juan/cbeta 预开 Ep13 世主妙嚴品卷1·Ep14 如來現相卷6+毘盧遮那卷11 | 不手录铁律 | done |
| 2026-10-21 | agent | **L.138 Phase 1b/1c·Ep 1 试点**：新建 `docs/经学文献/海云讲记_九九华严/` 目录，README (100 行 七节 凡例) + `episodes/ep01.md` (168 行·5,804 字·四片段·与 `huayanhai 玄谈01` 同题比对·4【待听核】·4【本文判断】) | 用户 ep1 试点裁定 | done |
| 2026-10-21 | agent | **L.138 Phase 3·发布页**：新脚本 `build_jj_collation_page.py` (403 行) → `web/demo/articles/jj-huayan-collation.html` (45,596 B·三 tab·17/17 自测全绿)；`standalone_articles.yaml` 开 `jj-huayan-collation` 条目（与 `haiyun-lectures` 并列不吞并） | 用户独立新页裁定 | done |
| 2026-10-21 | agent | **L.138.1 Ep1 全量升级**（用户反餉：先完整 ep01·信息无损·结构得当）：新建 `_probe_ep01.py` 扫全 1728 cues → slide 定位 6 段分界；`_segment_ep01.py` 自动清洗 (剔除 slide marker 47条+单字 noise) → 1681 有效 cues · 74 可读段；重写 `episodes/ep01.md` 从 168行·4段 → **705行·74段·22403汉字·94584字节**；6 讲章（§A请法因缘·§B三问立宗·§C外道禅定·§D佛世→部派→大乘·西域·§E华严系统·§F中国形成的宗派） | 用户 R4确认🅑 Elevated | done |
| 2026-10-21 | agent | **L.138.1 huayanhai 比对全量化**：从 Ep1 试点仅对比 `huayanhai 玄谈01` → **01/05/07/08/09/11 全量** (6集入库·6集待续已标)；新增 §五比对表 25 行演化观察 + §5.3 同内核跨 12 年总判 + §5.1 入库状态 | 用户 R4 确认•清晰标明 | done |
| 2026-10-21 | agent | **L.138.1 台账与发布同步**：`jj_huayan_collation.yaml` Ep1 从 `试點精校` → **`已校·信息无损`**；新字段 collation_coverage/sections/paragraphs/huayanhai_xuantan_ref(6)/pending(6)；重跑 `build_jj_collation_page.py` → `web/demo/articles/jj-huayan-collation.html` 从 45,596 B → **141,333 B**；门禁全绿 (check · verify_jj_lectures · audit_classify · verify_sources) | 无 | done |
| 2026-10-21 | agent | **L.138.1 标识体系建立**：本文判断 47条·OCR 待校 8条·待听核 12条·待核 5条·讲记比对 24条；不擅改原则：金剛四句偈·郑燮《竹石》引语·佛历3053口径·高原法系25世/42世·九二一地震接法—**均保留原字形不统一** | 本仓铁律 | done |
| 2026-10-21 | user+agent | **分层铁律确认**（用户补充提醒）：**99 华严讲记 = 主体内容**；huayanhai 玄谈旧整理 + 外部 `C:\华严\经典著作` 华严导读/玄谈类 = **仅作参照与对比**·不逆向授权修正主体·不引入外部权威判读。例外：Ep 13+ 正行段 CBETA `T10n0279` 回源为最高铁律（不属本分层）。已写入 `.harness/decisions.md # 9` + `ep01.md §〇` 与 `§五开头` + `README §2.0 主体vs参照` · memory已创 | 用户显式提醒 | done |
| 2026-10-21 | agent | **L.138.2 外部导读参照源接入（目录级）**：用户扩展比对源至 `C:\华严\经典著作`·R4确认 Q1(b) 一级同名 4 件《堪/勘玄记》一/02/三/04 + Q2 🅐 目录级不做抽取· Q3 先 commit L.138.1(`73a23de`) 后另起 L.138.2：ep01.md 新增 §5.4 6 行对照表（E1–E6·主论题映射候选 + 内容提取状态） + 未纳入项与理由（白话/图解/注疏/经本 四类 + 华藏妙海 整理版.pdf 标〔待核〕不预设）；`jj_huayan_collation.yaml` 新字段 `external_daodu_ref{tier1×4+tier2×2}` / `external_daodu_pending×1` / `external_daodu_layering_principle` ；重建发布页 143,762 → **148,488 B**·严守分层铁律**未新增未存疑引文**·门禁全绿·本地 commit · 未 push | 用户确认+铁律提醒 | done |
| 2026-10-21 | agent | **L.139.0 用户四项裁定**：① `华藏妙海 整理版.pdf` 定性为**二手整理资料·可引用·须标明来源**（yaml `external_daodu_pending` → owner_confirmed）·② Ep 2–12 精校可开始·③ Ep 13 CBETA 回源同意·④ PDF 抽取同意。另补 Ep 14 未列入原因（需 720p 重跑避 SABR 前置） | 用户逐项裁定 | done |
| 2026-10-21 | user | **并行稳健性铁律**：用户提醒「确保并行工作的稳健性·不要互相影响导致质量下滑」→ 采**严格串行**（一集一流水线·每步验证后再入下一步）·不得赶进度 | 用户显式要求 | done |
| 2026-10-21 | agent | **L.139.1 Ep 2 全量精校**：`_probe_ep02.py`（扫 2632 cues·143 slide marker·13 噪）→ `_segment_ep02.py`（修两轮 gap bug→88 段群·6 讲章）→ `episodes/ep02.md`（480 行·6 讲章 84 可讀區塊＝88群−2 slide 噪·D15–D17 併 1 块＝86 言说段·§二正文 21,925 汉字）·含现场问答 E/F·E20–E22 图解 OCR 严重损坏段标〔OCR 待校〕不重构·不擅改原则全覆盖 | 用户裁定②+方法论 | done |
| 2026-10-21 | agent | **L.139.1 跨集元数据一致性审计**（响应用户质量铁律）：发现 ep02 三处段数不一致（概要 88 / §九 86 / 实测区块 84）与字数冲突（22,838 vs 24,863）→ 统一为「84 可讀區塊·§二正文 21,925 汉字」稳定口径；发现 Ep1（已关）陈旧数（1681 cues / 22,403 字 / 100% 覆盖）与实测 SSOT（1728 cues / 98.4%）冲突→校正行数/字数/覆盖·区分「cue 入段覆盖 100%」vs「时间覆盖 98.4%」；删除易漂移的「全檔字数」只留稳定§二正文数·5 档（ep01/ep02/README/yaml/html）全 clean | 真相优先·单一事实源 | done |
| 2026-10-21 | agent | **L.139.1 构建脚本修复+重建**：`build_jj_collation_page.py` 补 `import os`（原缺·ep02 条件读取会崩）·修控制台「汉字」mislabel（len(md)→真 CJK 计数）·扩展支持 ep02.md → `jj-huayan-collation.html` 148,488 → **256,333 B**（含 Ep2 tab） | 代码与数据互证 | done |
| 2026-10-21 | agent | **L.140 独立文章总目录重排**（用户「页面目录/显示结构·分类做好」·选 A 分层重构）：修 build.py 崩溃根因（`data_source: list` 在 `practice.get(list)` 报 unhashable）·新增 `skip_html: true` 语义（外部专项脚本产物·build.py 只登记 index 入口·不覆写同名 .html）·panjiao 归组到 宗派与判教（7→8 目→、7 组→6 组）·新数据字段 `family` + `order_in_group`（单品依品数 1→7·祖师 5+2 依 杜顺→…→梦参·haiyun-lectures/jj-huayan-collation 置于修学 前 2）·yaml `group_order` 新增 `summary` 行（页头小标题旁）·verify_demo.py 新 skip_html 分支（存…DOCTYPE/收尾/体量三检）·**jj-huayan-collation 首次上 index 目录**（用户提醒：「别忘添加海云法师 99 华严讲法字幕梳理」）·index.html 33→34 篇·重建后 tabs 嵌入 `var ARTICLES` 同步 | 用户 选 A 分层重构 | done |

