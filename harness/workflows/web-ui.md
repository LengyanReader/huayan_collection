# Workflow — 前端 · 数据驱动导航与渲染（Web UI / Nav / Rendering）

> **何时用**：改 6 个 tab 的**侧栏导航、子页/独立文章、中英渲染、视图切换、可视化**等任何前端呈现时。
> **本项目大量迭代发生在此层**（导航重构、降级子项、独立文章页、多语渲染…）。原则同 [`principles.md`](../principles.md) §1：**改数据/配置，不改产物**。

## 架构一瞥

- **产物**：`build.py` 生成 `web/demo/tabs/*.html`（6 tab：lineage/gap/jiaoxing/cosmology/frontier/resources）+ `web/demo/articles/*.html`（独立文章）+ 复用 `web/demo/js/*`、`css/*`。
- **运行时 JS**（`web/demo/src/` 是源，`web/demo/js/` 是构建复制/内联目标）：
  `practice.js`(2290L·教行) · `lineage.js`(1769L·谱系) · `gap.js`(917L·空白) · `common.js`(890L·共享渲染) · `cosmology.js` · `frontier.js` · `spirit.js` · `init.js` · `article.js`(独立文章渲染) · `data.js`。

## 数据驱动的三处配置（改这些，不改 HTML）

| 想做什么 | 改哪里 | 机制 |
|---|---|---|
| 侧栏导航项/层级 | `data/navigation.yaml` | `build.py: render_sidebar()`（L244）按 spec 生成；`_action_js()`（L216）把 `action` 渲染为 `<a href>` 或 `onclick` 调用；`subsub:true` → `.sub-sub-link` 三级 |
| 前沿域→文章 子项 | `data/frontier/*` + `navigation.yaml` | `inject_frontier_subs()`（L285）自动注入，须在通用 subs 之前 |
| 独立文章页 | `data/translation/standalone_articles.yaml`(`others:`)/`topic_studies.yaml` | `load_standalone_articles()`（L791）+ `build_articles()`（L1377）→ `articles/<id>.html`；`back:{tab,view,label}` 驱动面包屑/返回 |

- **视图切换**：`switchPracticeView(view, btn)` 切 `#pv-<view>`、跑 `articleChip(view,...)`、存 `localStorage practice_sub`。子项跳转用 `jxSubNav(view, anchor)`（滚到 `#anchor`）。
- **文章↔导航关联**：数据 `views:` 字段 → 运行时 `common.js: articleChip()`（L836）生成"库中藏·去读专文"chip，**不在 YAML 重复**（见 memory〈standalone article pages via views field〉）。

## ⚠️ 双源渲染器（最易踩）

同一呈现可能有两份**同构代码**，改一处必镜像另一处：
- `build.py: WIZ_LIB_RENDER`（L951，生成静态 article）**↔** `practice.js: renderWizLibrary()`（L901，运行时），注释已互标"同步"（如 `esc` 转义 L896）。
- 加/改海云讲法库渲染时**两处一起改**，否则静态页与交互页不一致。

### ✔ 收敛法：把重复逻辑上抽为 common.js 单一渲染源（refs 已落地）

当同一段逻辑散落在 **N 个渲染点**（`practice.js` / `gap.js` / `cosmology.js` + `build.py` 内联 `CHAN_TRACES_RENDER`/`GAP_TOPICS_RENDER`）时，逐一镜像不可持续。解法：**在 `common.js` 里放一个 `window.xxx` 全局函数**，各调用点一律 `(window.xxx ? xxx(data) : '')` 委托：
- **🔴 头号陷阱**：`common.js` 的**唯一真源是 `web/demo/src/common.js`**——`build.py: read_src('common.js')`（L1683）每次 build 都**覆盖** `web/demo/js/common.js`。只编辑 `js/`（构建产物）会在下次 build 被静默清空，而所有调用点走 `? : ''` 兜底 → **参考文献渲染为空却不报错**。务必改 `src/` 后 `build`，并核 `Get-FileHash src == js`。
- **可达性前提**：tab（`build_page`）与独立 article（`build_articles` L1477）**都先加载 `common.js`**，故一处定义全站复用；独立页里 `common.js` 是外链 `<script src>`，helper 运行时才产 DOM，故构建产物 HTML 里只出现**调用点**、不含其内部标记（如"信度分级"图例）——**核验应数调用点，不以图例计数**。
- **零回归要点**：helper 必须**向后兼容旧入参形态**（字符串数组 / 对象数组 / 类目映射三态自适），并提供 `opts.fmt` 注入各页既有格式化器（如 `_dynMD`/`_escC`/全局 `mdToHTML`），使"仅改 JS/py 源、不碰 YAML"即可安全收敛；每处保留 `? : ''` 兜底。
- **落地例**：`window.renderRefList(refs, {fmt|md|legend})` 统一 参考文献 渲染（A/B/C 信度分级徽标 + 🔗核对链接），取代此前 ~15 处重复 `refs.forEach(r=>'<li>'+r)`。新增分级参考文献**只改 YAML 数据结构，渲染端零改动**。
- **适用边界**：域内视觉差异大（如 `xf` 分组）时用 `{legend:false}` 逐组调用而非整块；不同数据域（frontier_dialogue 等）先评估再收敛，勿为统一而越界改坏语义。

## 中英双语渲染链（勿插坏）

`.en-line`(块级独占一行) / `.en-inline`(行内配对) / `en-block`(块级整段) 由 `common.js: _markEnBlocks(root)` 生成；语言切换 `_applySiteLang()` 只切 `html[data-lang]` + `body.en-mode`。
- **会话级**：`sessionStorage site_lang` 覆盖 `localStorage site_lang`（`init.js` 应用），偏好仍留 localStorage（L.㉝）。
- 英文只在英文模式显示靠 CSS；"仅中文/英文泄漏/括号混杂"三类缺陷的**反向自证扫描**见 L.㊾⑭（`&nbsp;` 占位行是有意双语对照，非残留）。
- 数据层英文字段用 **plain-text**（`_en` 字段禁 markdown 链接/转义，否则 `_en()`→`_dynMD()` 渲染为空，L.㊾⑯⑰）。

## 两个高频配方（源自近期真实迭代）

**A. 新增一篇独立研究文章**
1. 写 `docs/<标题>.md`（含 front-matter：id/title/`chapters:[{file,anchor,format}]`）。
2. 在 `standalone_articles.yaml`（或 `topic_studies.yaml` 的 `chapters`，自动展开）登记 `{id, file, label, zh_only?, back:{tab,view,label}, desc}`。
3. `build.py` → 生成 `articles/<id>.html`；`verify_demo.py` ✅。
4. 若要它出现在导航：给相关数据加 `views:` 字段（走 `articleChip`），或在 `navigation.yaml` 加一条 `action.href: articles/<id>.html`。

**B. 调整侧栏层级（如"降级/归并"一项）**
1. 只改 `navigation.yaml`：把目标项并入父组 `subs`（必要时 `subsub:true`），删原顶级组。
2. 校验产物：顶级组头计数应为 0、`sub-link`/`sub-sub-link` 各应现（见 L.㊾⑨ 海云讲法降级同款）。
3. 已知小限：被降级项变成 `.sub-link` 后，`jxSubNav` 只匹配顶级 `.nav-link` 打光，故进入其视图时**顶级标题不再高亮**（纯视觉，功能不受影响）。

## 验证（本层特别重要：静态 ≠ 交互）

- `node --check <js>`（`verify_demo.py` 已集成）——防 JS 语法回归（无语法检查曾吞整块导航，L.㊾⑭）。
- **headless Chrome `--dump-dom`**：量 CSS/HTML/DOM 产物、`data-count` 校验（最稳）。
- **CDP**：测点击/切换等交互态——但本机 CDP 常 `10053` 断连，**不稳定**；退化方案：注入脚本 + `--dump-dom` 断言 `body` 属性/类（L.㊾⑭）。
- **铁律**（memory〈Interactive State Verification Requirement〉）：渲染/交互改动**不得只静态核验**，须以"真人用户"路径触发（点击、切页、查 DOM/截图/网络）；浏览器自动化失败必须显式报告并给替代方案，不得以静态检查冒充已验。
- **缓存陷阱**（memory〈Three-layer cached JavaScript〉）：`file://` 下 `page.reload(ignoreCache=True)` **不刷新 src/js**；须用 query-string 绕缓存或经 HTTP。

## 门禁

`build.py` ✅ → `verify_demo.py` ✅(+node --check) → 交互态实测（dump-dom/CDP 或注入断言）→ 涉数据一致性 `test_pipeline.py` ✅ → 更新 `docs/next-phase-plan.md` + `make evolve`。
