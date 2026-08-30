# 多语对读文章设计规范（中文为主文 · 外文为平行对读批注）

> 适用对象：《识与心灵》《识与心灵之镜》两篇独立文章页及其后续多语文章
> 相关文档：《华严文献·多语对读》架构见 docs/multilingual-alignment.md；来源分级见 docs/verification-framework.md；玄奘体翻译规范见 docs/translation-guide.md

## 一、设计目标

将一份「中文学术长文」以**中文为主文、外文为平行对读批注**的方式呈现，使知识与思想的流动不被语言隔断：

1. **主文连续可读**：中文原文完整保留为正文，不因外文注释割裂。
2. **外文为译注而非第二页面**：英文（及法、日、梵、藏）以「对读批注」形态内嵌，读中文如同读文言文配白话笺注——外文解释中文，而不是另起炉灶。
3. **不留隔膜、不堆砌**：一个中文词汇或语句可用**多个外文语词**分角度诠释（如 ālayavijñāna 可释为 encet store consciousness / base consciousness / all-ground consciousness），但只放到「必要且恰当」处，忌逐字逐句机械对译。
4. **各语言各取其优**：梵文取词源义、藏文取经藏用语、英文取当代哲学术语、法文日文取宗派/文化译法——发挥每门语言的精神内核，仅在其确有意义时加入。
5. **全程考证约束**：一切译文与转写均有据可查（文本自身英译、CBETA/T84000、权威双语词典）；无把握者一律标〔待核〕；严禁自创翻译、严禁以音代义、严禁幻觉式对译。

## 二、呈现模型

```
中文主文（完整原文，作为正文流）
 ├─ 全句级对读  ▸「英译对读」引用块：整段/整句的英文平行文本（取作者英文版实际文句）
 ├─ 术语级格义  ▸「术语格义」引用块：一中文术语 ↔ 多语言语词（梵/藏/英/日/法）＋出处/待核
 └─ 主题级批注  ▸「主题对读注」引用块：段落或主题层面的对读说明（含比较、慎思、存疑）
```

- 主文标题层级沿用原文章（`## 第X节` / `### 一、`）。
- 对读批注一律使用 markdown **引用块**（行首 `>`），由 `_mdDocEmbed` 渲染为金边引用样式（web/demo/src/common.js:676），与正文段落视觉上区隔。
- 术语格义可选用 `|` 表格（多行）以避免连续引用块过重；表格列须固定，避免过宽。
- 每篇文档头部以 `> 研究说明` 块给出：源文本、出版信息、对读体例、信源分级、校对状态。

## 三、批注格式规范

### 3.1 全句级「英译对读」

```
> **英译对读 · 摘要**（底本：作者英文修订版 *Vijñāna and Mind 0415*，2026-04-15）
> This paper draws on the philosophical resources ...
```

- 英文必须**原样引用作者英文版文句**，不得改写转译；无英文原文处（如作者未发表英译）应标〔无英文本〕而非代拟。
- 底本选择策略：同一文章存在中英两版时，以「发行日期与修订状态」定底本（本项目两文均以 04-15 修订版为底本），并在头部注明。

### 3.2 术语级「术语格义」

单个术语（引用块）：

```
> **术语格义 · 转依**
> **梵** āśraya-parāvṛtti
> **藏** གནས་འགྱུར།（gnas 'gyur，转舍所依）
> **英** transformation of the basis · revolution of the support · fundamental reorientation of one's cognitive basis
> **日** 転依（てんね）　**法** revirement du fondement ¤〔待核：待补法文文献用例〕
> **注** 本文第五节以「转依不可外包或模拟」为核心；不见于 CBETA T31n1585 正文此译文？——〔待核〕
```

多术语汇总（表格）：

```
| 中文术语 | 梵 | 藏 | 英（本文用法/备选） | 日 / 法 | 注 |
|---|---|---|---|---|---|
| 识变论 | vijñaptimātratā | རྣམ་རིག་ཙམ།（rnam rig tsam） | representation-only · vijñāna-transformation | 唯識（ゆいしき）/ seule-représentation ¤ | 本文自译“识变论” |
```

### 3.3 主题级「主题对读注」

```
> **主题对读注 · 意识难问题与难问题预设】
> Chalmers 的“硬问题”在现代心灵哲学中的位置……此处唯识的倒转策略是……
> 〔待核〕关于条件——见 CBETA T31n1585 卷二「……」（待回原文核对卷次）。
```

### 3.4 校对状态标记

- 〔待核〕＋注明待核对象（卷次、译名、出处、年代），不阻断展示；
- 〔待批注〕＋说明本段暂未附多语批注，纳入路线图某阶段；
- 〔存疑〕＝信息冲突、两个来源不可调和时使用（复用 docs/verification-framework.md 的存疑语义）。

## 四、语言范围与取舍准则

| 语言 | 定位 | 取舍准则 |
|---|---|---|
| 中文 | 主文 | 全文保留 |
| 英文 | 平行对读主外文 | 凡作者已有英文本，全句级对读引用其原句；无英文本处不代拟 |
| 梵文 | 词源义 | 唯识/佛教核心术语必备（IAS 转写）；有出处可溯 |
| 藏文 | 经藏用语 | Toh/甘珠尔藏译术语（如 ཀུན་གཞིའི་རྣམ་ཤེས།）；把握不足标〔待核〕 |
| 日文 | 日本唯识/华严传统译语 | 仅限确有日文佛教学用语的术语（阿頼耶識・末那識・転依・念等） |
| 法文 | 法语佛学/哲学译语 | 仅在法语学界有通行译法处（如 pleine conscience）；无通行者不强行收录 |

「恰到好处」判据：**该术语是否因多语对读而增益理解**——增益则注，否则不注；宁缺勿滥，杜绝逐行逐词堆砌。

## 五、来源与可靠性

1. 术语格义复用本项目三级信源分级（docs/verification-framework.md）：
   - **T0** 一手典籍（CBETA 电子佛典编号 T31n1585 等 / 84000 Toh）；
   - **T1** 作者原文（本项目论文的中英文原稿）；
   - **T2** 权威二手（流通佛学工具书、学术专著）；
   - 凡 T2 以下或跨源冲突，必标〔待核〕/〔存疑〕。
2. 每条批注尽量给出出处锚点（CBETA 编号、DOI、页码、作者英文版小节号）。
3. 严格禁止：以另一篇文章的文句冒充本文文句；对无英文底本的文本自行拟译英文长句冒充对读；转写/语法把握不足仍强拉梵藏文词形。

## 六、工程接入

| 环节 | 约定 |
|---|---|
| 文档存放 | docs/×_多语对读.md（独立文章注册表 doc 字段指向之） |
| 独立文章页 | data/translation/standalone_articles.yaml 的 others 登记，views 指向所在 Tab 子视图 |
| Tab 内入口 | 所在子视图域容器插入 `articleChip(view, '#fv-<key>-<domain_id>')`；域容器 id 由 frontier_dialogue.yaml 中 domain.id 派生 |
| 渲染 | build.py 原样读入 docs/*.md → 内嵌 ARTICLE/ARTICLE_DOCS → common.js `_mdDocEmbed` 渲染 |
| 出处登记 | data/references/bibliography.yaml 增补条目（tags 含 frontier），供文献总目索引 |

## 七、两篇目标文章路线图

| 阶段 | 内容 | 状态 |
|---|---|---|
| P0 | 设计规范、文章页骨架、摘要/关键词/核心术语批注示范、后端接入「与佛教的对话·瑜伽行派」域 | ✅ 完成 |
| P1 | 全节「EN对应」——每节中文小节正文后配作者英文修订版同小节原句全文（两版节内小节一一对应，信息无损） | ✅ 完成 |
| P2 | 术语格义表覆盖正文全部核心唯识术语（梵/藏/英为主） | 🔄 进行中 |
| P3 | 法/日文批注按「四、语言的取舍准则」精选补入；全文档〔待核〕清零闭环 | ⬜ |

*状态：P0/P1 完成（2026-08-30）。*

> **EN对应 配对基准**：中文每节内 `### ……` 小节的出现次序 ↔ 英文同节内 `### N. / I. / Footnotes` 次序（两版逐一相同，脚本核验）；特例 en_2 第 13 节中文 4 小节、英文 3 小节，经 per-section override 映射对齐（en §3 覆盖中文 §灵性绕过+§印顺警示）。

## 八、前沿对话页双语（文章页机制的页级推广）

**L-F 序列第 2 步（frontier 页面级）**：数据源 `data/frontier/frontier_dialogue.yaml` 结构化 `en` 字段 → build.py 内嵌 FRONTIER_DATA → `frontier.js` 渲染中英对照。

- 数据约定（均写入 YAML，不硬编码 JS）：
  - 节级：`sections.{huayan,chinese,buddhist,others,litreview}.en` — 节 intro 的英文对应（一句话式概述）。
  - 域级：`domains[].en_domain`（英文域名）、`en_core`（核心议题逐条英文）、`en_persp`（华严视角英文对应：按中文 (1)(2)… 要点逐条覆盖，语义无损）或 `en_key_findings`（key_findings 域的逐条英文并行列表）。
- 呈现：`frontier.js` 在域名/核心议题/华严视角各块之后渲染 `.en-line`（蓝字金边小段）；页顶固定「🌐 英文对应·显示/隐藏」开关，状态存 `localStorage['frontier_en']`；`.en-line` 由 `#frontier-view.en-hidden .en-line{display:none}` 隐藏——机制与 `article.js` 折叠一致，仅作用域不同（页级 vs 文档级）。
- 统计（2026-08-30）：5 节 intro `en` + 18 域 `en_domain`/`en_core`/`en_persp`（17）+ `en_key_findings`（1，神经科学域）——全部为项目策展文本的英文对应，非典籍译名硬译；术语沿用统一惯译。

## 九、全站阅读语言切换（L-F 序列第 3 步第一梯队）

**机制（中英对照 ⇄ 仅中文）**：

- **按钮**：build.py 四个页面模板的 `<header id="header">` 统一注入 `<button id="lang-toggle" class="lang-btn">`（lineage 页无右侧登录位，按钮自带 `margin-left:auto`）。
- **JS**：`common.js` 第 9 节 `window.toggleSiteLang()` / `window._applySiteLang()`；偏好存 `localStorage['site_lang']`（'0' = 仅中文，缺省/其他 = 中英对照）；common.js 底部 IIFE 在页面解析后自动恢复状态（common.js 均位于 header 之后的 body 部加载，此时按钮已存在）。按钮随状态切换文案「🌐 中·EN ⇄ 🌐 仅中文」。
- **CSS**：`body.zh-only` 全局隐藏 EN 对应块——`body.zh-only .en-line, body.zh-only .en-block, body.zh-only .en-note, body.zh-only .en-cell { display:none !important; }`。article.js 折叠（en-block）与 frontier.js 页级开关（en-line）不受影响，叠加作用于同一批元素。
- **约定**：凡全站双语内容一律使用受管 CSS 类——`en-line`（单行/块级英文对应）、`en-block`（文章外文批注）、`en-note`、`en-cell`——使「仅中文」开关一处覆盖全站，无需逐块写显隐逻辑。

**数据落地（2026-08-30）**：

- **YAML 分支（Tab6 灵性仁本）**：`data/spirit/spirit_content.yaml` 增段级 `title_en` + `summary_en`（overview）/`en`（节 intro，共 5 节）、主题级 `en`（标题）+ `en_body`（正文，19 主题）；`spirit.js` 在节标题/摘要/引言/主题处渲染 `.en-line`（`.sp-en-title/.sp-en-t/.sp-en-b`）。海云法师**原文辑录**（haiyun quotes）因其为讲法逐字稿、不宜代拟英文而暂不翻译〔待核〕；`environmental_humanities.yaml` 留待后续梯队。
- **SQLite 分支（Tab2 术语库）**：`glossary` 表 50 条 `definition_zh`/`definition_en` 全补齐（补 037-042 六波罗蜜与 044 十信位共 7 条 definition_en，038-041 同时补 definition_zh）；build.py `load_gap` 注入 `db_reader.load_glossary()` → `GAP.glossary`；gap.js 以数据驱动 50 行「梵-藏-汉-英」对照表替换原硬编码 30 行，并新增「术语格义 · 中英释义」卡（`definition_en` 以 `.en-line` 呈现，随全局开关显隐）。——顺带消除了原 gap.js 中的术语表硬编码。
- 数据皆进 YAML/SQLite 权威源，不在 JS/HTML 写死（符合「杜绝硬编码」）。

> 全站「中文为主文 · 简明优雅英文无损对应」双语原则及全站推广序列见 `docs/next-phase-plan.md` → **L-F**。