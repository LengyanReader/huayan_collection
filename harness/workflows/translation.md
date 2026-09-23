# Workflow — 翻译 / 多语对读（Translation）

> **何时用**：新增或订正任何 `*_en` 字段、`en_body`/`title_en`/`intro_en`、`.en-line` 对照、品目/术语多语对读。
> **权威原则源（必读，不在本文件重述）**：`CLAUDE.md`〈多语 EN 翻译原则〉七条 +〈编务总则·中英必配〉+ `docs/translation-guide.md`（藏汉玄奘体）+ `docs/multilingual-alignment.md`（梵-于阗-藏-汉-满-英）。

## 配方（步骤）

1. **取约束**：检索记忆〈Academic writing style and terminology standardization〉〈Bilingual editorial and coding conventions〉〈CJK Encoding and Subprocess Safety Conventions〉；加载技能 `academic-research-writer`（如需成文）。
2. **术语先行**：查 `data/references/bilingual_glossary.yaml`、`data/translation/glossary.yaml` 固定术语表；人名/经名循全站统一译法（玄奘=Xuanzang、海云继梦=**Haiyun Jimeng**、法界=dharmadhātu…）。**无通行英译/暂无把握 → 明示〔待核〕/〔无通行英译〕，严禁硬翻自造**（原则7）。
3. **重实质不逐字**：义·理·境对等，意译优先；**EN 不得超出中文正文**、不新增年代/地点/史实/观点（原则2·考证）。祖师语录中文保持原文，EN 用最精到转述。
4. **写数据源**（SQLite/YAML，禁在 JS/build.py 硬编码）：长 EN 用 `|` 块标量；**YAML 转义纪律**（原则5）——单引号串内 `\'` 非法用 `''`、含「」用单引号、`title_en` 含冒号/撇号用双引号。
5. **渲染约定**：EN 块前缀 📖、走 `.en-line` 随全局显隐（默认中英对照）；`title_en`/`intro_en`/`en_body` 分别落位。英文块中的表格会被 `common.js` `_mdFullToHTML` 处理（引用块内表格渲染修复见 L.㊾⑫）。
6. **校对=门禁**：翻译≠成稿——术语一致性 + 教理准确性 + 结构/引号安全，经主编全文审查。
7. **验证**：`python web/demo/scripts/build.py` → `verify_demo.py` →（涉史实）`verify_sources.py` → 交互/显隐态用 headless Chrome 实测（含 zh-only 无英文泄漏、`.en-line` 全隐/全显）。
8. **留痕**：更新 `docs/next-phase-plan.md`；`make evolve`；必要时 `self_evolve --record`。

## API 辅助的边界

在线翻译（如免费档）仅作**初稿上量**、可插拔（无 key 回退子代理著写）；**质量门禁与人工审查绝不因接 API 而放松**（原则6）。

## 常见坑

- 内联 CJK one-liner 改数据 → SyntaxError：写临时 `.py` 脚本执行再删。
- 只补 `*_en` 漏 `en_body`（不以 `_en` 结尾）→ 校验须同时匹配二者。
- PowerShell 重编码使中文计数误显 0 → 用 ASCII 标记（`id="fv-x"`）反证渲染完成。
- "只有英文无中文/英文不显示"多为旧 localStorage 语言开关残留（会话级 sessionStorage 已修，L.㉝ / L.㊾⑭），非数据缺失。

> 〔待落地·高杠杆〕把本节固化为项目专属技能 `huayan-multilingual-en`（见 [`../skills.md`](../skills.md) §四）。
