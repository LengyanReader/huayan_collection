# -*- coding: utf-8 -*-
"""阶段二·内容扩充：把德格 45 品 TOC + 底本 sha256 台账注入 demo 页 ARTICLE.doc_md。

做法（承本仓 byte-safe 编辑惯例·避免手拼 \\n 转义）：
- 读 data/alignment/tibetan-derge-toc.json（SSOT·由 extract_tibetan_toc.py 逐字回源产出）
- 组装新 doc_md（保留原有对读示例·新增 45 品目录表 + 底本台账 + 阶段进度）
- 用 json 往返安全改写 HTML 内 `var ARTICLE = {...};` 的 doc_md 与 version

诚实边界：45 品汉藏逐品对应一律〔待核〕（需人工比对），只陈述机器可回源的
事实（品目标记、卷号、起始叶码、藏文开篇种子、底本字节 sha256）与既有结构差（藏45 vs 八十39）。
"""
import io, json, re

HTML = 'web/demo/articles/tibetan-avatamsaka-alignment-demo.html'
TOCJ = 'data/alignment/tibetan-derge-toc.json'

d = json.loads(io.open(TOCJ, encoding='utf-8').read())
sf = d['structural_facts']

# --- 底本台账表 ---
bt_rows = []
for bt in d['base_texts']:
    name = bt.get('siglum') or ('德格 v' + bt['vol'])
    kb = round(bt['bytes'] / 1024, 1)
    bt_rows.append('| %s | %s | %s KB | `%s…` |' % (
        name, bt['role'], kb, bt['sha256'][:16]))
bt_table = '\n'.join(bt_rows)

# --- 45 品目录表 ---
toc_rows = []
for e in d['toc']:
    seed = e['tibetan_open'].replace('|', '｜').strip()
    if len(seed) > 46:
        seed = seed[:46] + '…'
    toc_rows.append('| %d | %s | %s | %s | 〔待核〕 |' % (
        e['no'], e['vol'], e['start_folio'], seed))
toc_table = '\n'.join(toc_rows)

new_doc = f"""# 藏汉英对读 · 大方广佛华严经（德格藏文本）初探

> **说明**：本页展示藏汉英对读的结构设计与**阶段二·底本处理**成果。藏文 45 品目录由德格版 `Toh 44`（035-038）文本中 `{{T44-N}}` 品目标记**逐字机械提取**，叶码为底本定位；汉藏逐品对应**需人工比对**，故一律标〔待核〕，不代立论。中文新译为本地模型 `buddhist-nlp/mitra-qwen35-translate`（9B）初步试译，尚未人工校对，仅供技术验证。

## 1. 底本概况

| 版本 | 文本 | 状态 | 备注 |
|---|---|---|---|
| **藏文（主底本）** | 德格版《大方广佛华严经》（*Tohoku* 44） | `data/references/tibetan/derge_kangyur/avatamsaka/`（035-038，4 卷） | **完整**，含《入法界品》（Gaṇḍavyūha），共 115 *bam po*。 |
| **汉文（对勘）** | 六十华严（*T09n0278*·东晋佛驮跋陀罗译） | `data/references/cbeta/T09n0278.xml` | 三十{'' if sf['chinese_60_chapters']!=34 else '四'}品·末品实测〈{sf['chinese_60_last_pin']}〉 |
| **汉文（对勘）** | 八十华严（*T10n0279*·唐实叉难陀译） | `data/references/cbeta/T10n0279.xml` | 三十九品·本项目校勘底本·末品实测〈{sf['chinese_80_last_pin']}〉 |
| **汉文（对勘）** | 四十华严（*T10n0293*·般若译） | *待补充* | 入法界品全译 |

### 1.1 底本字节台账（sha256 · 可校验）

一手语料逐字保真，`sha256` 供跨会话复算核对（承 CBETA `.gitattributes -text` 先例）：

| 底本 | 角色 | 体量 | sha256（前 16 位） |
|---|---|---|---|
{bt_table}

> 复核方式：`python workspace/tibetan-avatamsaka-translation/tools/extract_tibetan_toc.py`（重算并覆写 `data/alignment/tibetan-derge-toc.json`）。

## 2. 藏译 45 品目录（阶段二·机械提取 · 汉藏对勘待核）

结构差（**可回源事实**）：藏译 **{sf['tibetan_chapters']} 品** vs 八十汉译 **{sf['chinese_80_chapters']} 品** vs 六十汉译 **{sf['chinese_60_chapters']} 品**。〔本文判断〕藏本分品较汉本细，逐品一对一对应不成立，须依经文内容段落比对后重建——此为阶段四目标，**本页不作臆测**。〔待核〕

| 品次 | 卷 | 起始叶码 | 藏文开篇（德格原字形·节选） | 汉译对应 |
|---|---|---|---|---|
{toc_table}

> 〔口径〕「品次」= 德格文本 `{{T44-N}}` 东北编号；「起始叶码」= 该标记前最近的 `[Na.b]` 叶行标记；「藏文开篇」= 标记后原文（去叶码/编号标记·去重后节选）。全量种子见 `data/alignment/tibetan-derge-toc.json`。

## 3. 对读示例（首段试译）

以下选取德格藏本卷一（035）开篇经文，展示拟议的对读呈现格式。

### 3.1 藏文原文（Derge 035）

```tibetan
།འདི་སྐད་བདག་གིས་ཐོས་པའི་དུས་གཅིག་ན།
བཅོམ་ལྡན་འདས་ཐོག་མ་མངོན་པར་སངས་རྒྱས་པ།
སངས་རྒྱས་ཀྱི་ཆོས་ཐམས་ཅད་ཤིན་ཏུ་རྣམ་པར་སངས་རྒྱས་པའི་ཐུགས་མངའ་བ།
```

### 3.2 藏译→中文（模型试译，MITRA）

> 如是我闻，一时，世尊最初成正等觉，心具一切佛法，已圆满证悟。

### 3.3 藏译→英文（模型试译，MITRA）

> Thus have I heard. At one time, the Blessed One had just attained unsurpassed, complete enlightenment. His mind possessed all the qualities of the Buddha and had fully realized them.

### 3.4 汉译对勘（八十华严 T10n0279）

> 如是我聞：一時，佛在摩竭提國，阿蘭若法菩提場中，始成正覺。

### 3.5 汉译对勘（六十华严 T09n0278）

> 如是我聞：一時，佛在摩竭提國菩提樹下，成佛未久。

## 4. 对读结构设计

拟采用以下多栏对读布局：

| 栏目 | 用途 |
|---|---|
| **藏文原文** | 德格底本原字形（保留 *tsheg*、句读，逐字可回溯） |
| **藏文分词/直译** | 逐词对应，标注助词、名词、动词等 |
| **中文译文（新译）** | 基于藏文本的新译（模型辅助 + 人工校对） |
| **英文译文（新译）** | 英文对照翻译 |
| **八十华严（T10n0279）** | 实叉难陀译，对勘异同 |
| **六十华严（T09n0278）** | 佛驮跋陀罗等译，对勘异同 |
| **四十华严（T10n0293）** | 般若译，对勘异同（如有对应） |
| **校记** | 异文、术语、存疑（〔待核〕）、推断（〔本文判断〕） |

## 5. 技术路线与阶段进度

1. **底本规范化**：从德格藏文 `.txt` 提取经文，保留行号、页码信息 — *阶段二·进行中*
2. **品目对照**：建立藏汉品目对应表 — *阶段二·藏译 45 品目录已机械提取（见 §2）；汉藏逐品对应待人工比对〔待核〕*
3. **AI 辅助翻译**：`hy_py312` 环境下 `mitra-qwen35-translate` 初译 — *阶段三至四·未启动（仅首段 PoC）*

> **当前进度**：阶段一（底本完整性核查·德格完整）✓；阶段二（底本处理·45 品 TOC + sha256 台账）已落地；阶段三（模型选型评估）、阶段四（逐段对齐翻译）、阶段五（完整对读界面）未启动。〔未竟〕逐品汉藏对齐、名相术语库、偈颂分行对齐——俟后续批推进，不臆造。
"""

# --- 安全回写 HTML 内 ARTICLE 的 doc_md / version / title_sub ---
html = io.open(HTML, encoding='utf-8').read()
m = re.search(r'var ARTICLE = (\{.*?\n\});', html, re.S)
if not m:
    raise SystemExit('ARTICLE 块未找到')
obj = json.loads(m.group(1))
obj['doc_md'] = new_doc
obj['version'] = 'v0.2 · 阶段二 底本处理（德格 45 品 TOC 逐字提取 + 底本 sha256 台账·汉藏对勘待核）'
obj['title_sub'] = ('Tibetan-Chinese-English Parallel Reading · Derge Kangyur 035-038 (Toh 44) · '
                    '45-chapter TOC machine-extracted · sha256 ledger · cross-alignment 待核')
new_block = 'var ARTICLE = ' + json.dumps(obj, ensure_ascii=False, indent=2) + ';'
html2 = html[:m.start()] + new_block + html[m.end():]
io.open(HTML, 'w', encoding='utf-8').write(html2)
print('OK doc_md 注入·长度=%d 字符·toc行=%d·底本行=%d·version=v0.2' % (
    len(new_doc), len(d['toc']), len(d['base_texts'])))
