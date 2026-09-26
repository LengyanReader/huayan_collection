# Workflow — 分级参考文献轨（Bibliography / P-track）

> **何时用**：对任一 `docs/*.md` 研究文档的〈参考文献 / bibliography〉章节做**分级标注 + CBETA 深链 + 逐条核证**时；即本项目反复执行的 "P 轨"（P = Primary/Provenance/Pointed-link）。
> **地位**：是 [`information-assurance.md`](information-assurance.md)（考证优先）与 [`academic-standards.md`](academic-standards.md)（引用可点）在**参考文献章节这一具体界面**上的落地配方。权威模板见 [`docs/分级参考文献_模板.md`](../../docs/分级参考文献_模板.md)。

---

## 一、目标产物（三级 + 深链 + 零伪造）

每条参考文献收敛为统一形态：

```
作者（时代）·《书名》卷次 · **[A]** · 🔗 [CBETA T45n1865](https://cbetaonline.dila.edu.tw/zh/T45n1865)
```

- **`[A]` 原典**：大正藏 / 卍续藏 / 中华大藏经 内的经律论疏（可 CBETA 深链）。
- **`[B]` 学术**：近世学者研究、校注、译著（出版社 + 年份；西文给 ISBN/DOI，中文给出版社）。
- **`[C]` 普及/工具**：辞典、通识读物、网站（可信但非一手）。
- **宁缺不伪**：核不到出处 → 如实标〔待核〕/〔无法获取·原因〕，**绝不硬凑假链接、假 SIGLA、假 ISBN**。

## 二、CBETA URL 构造规律（深链可点）

| 藏 | 前缀 | 例 |
|---|---|---|
| 大正藏 T | `https://cbetaonline.dila.edu.tw/zh/T{vol:02d}n{no:04d}` | `…/zh/T45n1865` |
| 大正藏·具体卷页 | 追加 `_NNN`（三位补零） | `…/zh/T10n0276_004` |
| 卍续藏 X | `https://cbetaonline.dila.edu.tw/zh/X{vol:03d}n{no:04d}` | `…/zh/X55n0891` |
| 中华大藏经 B | `https://cbetaonline.dila.edu.tw/zh/B{no}` | `…/zh/B123` |

> 渲染链：`build.py` 把原始 Markdown 嵌入 `var ARTICLE = {…}`（JSON 字符串）→ 前端 `web/demo/js/common.js` 的 `_mdInline`（约 L850）把 `[text](url)` 转成可点 `<a target=_blank>`。**因此正文里写标准 Markdown 链接即可，勿手插 `<a>`。**

## 三、配方（逐文件·单批次净态提交）

1. **定位章节**：`Grep` 找该文档的〈参考文献 / 一、原典文献〉等小节；`Read` 全段取得完整上下文。
2. **给小节标题打级**：`### N、xxx` → 追加 ` · **[A]**` / `**[B]**` / `**[B/C]**`（混合小节用 `B/C`）。
3. **逐条核证 SIGLA**：对每个 `TxxnXXXX`/`XxxnXXXX` **必须** `WebSearch`/CBETA 反查——册号+番号是否对得上书名与作者。⚠️ **番号最易错**（见〈常见坑〉八识规矩颂案）。
4. **改写为统一形态**：正文旧写法 `。CBETA：https://…TxxnXXXX` → 补 ` · **[A]** · 🔗 [CBETA TxxnXXXX](url)`；EN 镜像块（blockquote）同步处理。
5. **批量机械变换用临时脚本**（文件多、条目多时）：写 `scripts/_<name>_tmp.py`，正则替换后**立即删除脚本**；每步之后 `Read` 抽样核对（尤其空行分隔、孤儿后缀）。
6. **单条订正用 `SearchReplace`**：给足唯一上下文；一次调用打包同一逻辑修改的多处（CN + EN + 脚注）。
7. **验渲染**：`python web/demo/scripts/build.py` → `python scripts/verify_demo.py`（须 ALL CHECKS PASSED）；`Grep -c` 统计成品 HTML 内 `[CBETA …](…)` Markdown 链接数应 > 0、裸 `cbetaonline` 未链接数 = 0。
8. **净态提交**：一个文件一批，commit 前缀 `bib(P-track/<X>):`；全部完成后更新 [`docs/文献待核_backlog.md`](../../docs/文献待核_backlog.md) §F 留痕，再跑 `make evolve`。

## 四、技能 / 工具

- 技能：`citation-verification`（防伪造引文）、`research`（一手反查）、（未来）`huayan-source-audit` / `huayan-bibliography-verification`。
- 工具：`WebSearch`/`WebFetch`（CBETA 反查）、`Grep`/`Read`/`SearchReplace`、临时 `scripts/*_tmp.py`、`verify_demo.py`（构建产物闸）、`verify_sources.py`（来源分级统计）。

## 五、常见坑（本轨亲历，务必规避）

- **SIGLA 张冠李戴**：曾把玄奘《八识规矩颂》误标 `T45n1861`——实为窥基《大乘法苑义林章》；颂文**收于** `T45n1865`（明·如愚《八识规矩补注》，颂八章系每章之首）。**番号必反查**，不可凭印象。订正要同步 CN 书目、EN 镜像、CN 脚注、EN 脚注四处。
- **`\s*$`（MULTILINE）吞换行**：正则里 `…TxxnXXXX\s*$` 会吃掉条目末尾的一个 `\n`，使相邻原典条目**塌缩成同一段**（丢空行分隔）。对策：用 `\n` 显式锚定或匹配后回填空行；写完脚本后 `Read` 验证分隔。→ 长期记忆 `common_pitfalls_experience`〈批量链接化脚本中 `\s*$` 吞换行致 Markdown 段落塌缩〉。
- **孤儿 `\_NNN` 后缀**：EN blockquote 里 CBETA 链接前带转义下划线页码 `\_004`；负向断言漏判 `\_` 会把 CBETA 换进链接、却把 `\_004` 甩在 `)` 之外。对策：二遍脚本把 `[CBETA Txxxnxxxx](url)\_(\d{3})` 重嵌为 `[CBETA Txxxnxxxx 卷N](url/_NNN)`。
- **ISBN 时代错置**：1971 年初版书尚无 978 前缀（1970 年代后才有）；若文献给了 978-0-415（Routledge 影印本）前缀，**并列初版年 + 后期书号并加注**，勿伪造"初版 ISBN"（宁缺不伪）。
- **`SearchReplace` 只匹配前缀**：若 `original_text` 只是某长条目行首前缀，替换后行身会被并入新行造成**串接**。对策：`original_text` 取整行或含尾界。
- **别声称未验证者**：西文 inline ISBN/DOI 若本轮未逐一反查，须在 backlog §F 记为离线待办，**不得在正文假称已核**。

> 度量：一轨做完 = 该文档〈参考文献〉每条都 `[级]` 可判、`[A]` 可点、SIGLA 经反查、核不到者留〔待核〕而非伪造；`verify_demo` 全绿；backlog §F 有留痕。
