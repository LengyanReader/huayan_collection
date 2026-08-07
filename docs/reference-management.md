# 参考文献知识管理规范

> 最后更新: 2026-08-08 | 版本: v1.0

## 一、设计原则

1. **单一权威源 (Single Source of Truth)**: `data/references/bibliography.yaml` 为主文献库, 页面 YAML 通过 `id` 引用, 不重复录入
2. **原语优先 (Source-Language First)**: 引文保留梵/藏/汉/英/法原语, 附中英双语批注翻译
3. **四方验证 (Four-Platform Verification)**: 每条文献链接: 出版社官方页 + Goodreads + 豆瓣 + Google Scholar
4. **标签驱动 (Tag-Driven)**: 通过 `tags` 和 `pages_tag` 字段驱动页面注入

## 二、数据结构

```yaml
# data/references/bibliography.yaml 结构
sutras:           # 经典与佛典
books:            # 专著
reports:          # 机构报告与政策文件
haiyun:           # 海云继梦法师体系
online:           # YouTube 系列 / 在线资源

# 每条文献的标准字段:
- id: schumacher-small-is-beautiful    # 唯一标识 (kebab-case)
  title_en: "Small Is Beautiful"       # 英文标题
  title_zh: 小的是美好的                # 中文标题
  author_en: E.F. Schumacher           # 作者 (英文)
  author_zh: E.F. 舒马赫               # 作者 (中文)
  year: 1973                           # 出版年份
  publisher: Harper & Row              # 出版社
  isbn: 978-0060803520                 # ISBN
  quote_original: |                    # 关键引文 (源语言)
  quote_zh: |                          # 关键引文 (中文翻译)
  links:                               # 平台链接
    official: <URL>                    # 出版社/官方页
    goodreads: <URL>                   # Goodreads
    douban: <URL>                      # 豆瓣
  goodreads_rating: {score, ratings, reviews}
  douban_rating: {score, note}
  scholar_citations: "~N"              # Google Scholar 引用量 (近似)
  tags: [spirit, frontier]             # 所属页面
  pages_tag: [section_name]            # 所属章节
```

## 三、维护流程

### 新增文献

```bash
# 1. 在 bibliography.yaml 中新增条目 (认领 id)
# 2. 搜索验证五个平台链接:
#    - 出版社官方页 (Google: "TITLE publisher official")
#    - Goodreads (https://www.goodreads.com/search?q=TITLE)
#    - 豆瓣 (https://book.douban.com/subject_search?search_text=TITLE)
#    - Google Scholar (https://scholar.google.com/scholar?q=TITLE)
# 3. 标签 tags 正确 → build.py 自动注入对应页面
# 4. 在对应的页面 YAML (spirit_content.yaml / frontier_dialogue.yaml) 的
#    references 节使用 id 引用即可
# 5. python web/demo/scripts/build.py   # 重建
# 6. curl http://localhost:8080/tabs/spirit.html | grep <title>  # 验证
```

### 更新评分/引用量

```bash
# Goodreads 评分: 直接访问 Goodreads 页面查看最新数据
# 豆瓣评分: 直接访问豆瓣页面查看
# Google Scholar 引用: 访问 scholar.google.com 搜索标题
# 修改 bibliography.yaml 对应字段后重建即可
```

### 批量校验链接有效性

```bash
# 提取所有 URL 并测试状态码
grep -oP 'https?://[^\s"]+' data/references/bibliography.yaml | sort -u | while read url; do
  code=$(curl -s -o /dev/null -w "%{http_code}" "$url")
  echo "$code $url"
done
```

## 四、数据流

```
┌──────────────────────────────────────────┐
│ data/references/bibliography.yaml (权威源) │
│   id + title + quotes + links + ratings  │
└──────────────┬───────────────────────────┘
               │ build.py load_bibliography()
               ▼
┌──────────────────────────────────────────┐
│ build.py → 注入 SPIRIT_DATA / FRONTIER_DATA │
│   (按 tags 筛选: 匹配页面的文献子集)          │
└──────────────┬───────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────┐
│ tabs/spirit.html  /  tabs/frontier.html   │
│   页面底部渲染参考文献卡片                    │
└──────────────────────────────────────────┘
```

## 五、与现有知识管理架构的整合

遵循项目三层数据栈规范 ([knowledge-management.md](knowledge-management.md)):

| 层级 | 参考文献对应 | 说明 |
|------|-------------|------|
| **L1 权威数据层** | `data/references/bibliography.yaml` | 直接策展录入 |
| **L2 验证层** | Goodreads/豆瓣/Scholar 交叉验证 | 评分+引用量的三方交叉校验 |
| **L3 展示层** | build.py → HTML 页面底部 | 自动注入对应页面 |

策展流程:
1. 研究/发现文献 → 在 bibliography.yaml 中新增条目
2. 填写所有字段 (id, title, quotes, links, ratings, tags)
3. 运行 build.py → 自动注入对应页面
4. 每季度批量校验链接有效性

## 六、当前覆盖统计

| 类别 | 条目数 | 涵盖页面 |
|------|--------|---------|
| 经典与佛典 | 5 | lineage, gap, cosmology, frontier, spirit |
| 专著 (灵性/人本经济学) | 5 | spirit |
| 专著 (修行传统/生态智慧) | 4 | spirit |
| 专著 (意识科学/心灵哲学) | 6 | frontier |
| 机构报告 | 5 | spirit |
| 海云体系 | 1 | spirit |
| 在线资源 | 2 | frontier, jiaoxing |
| **合计** | **27** | 全站覆盖 |

## 七、相关文件索引

| 文件 | 说明 |
|------|------|
| `data/references/bibliography.yaml` | 主文献知识库 |
| `web/demo/scripts/build.py` | 构建脚本: load_bibliography() → 注入页面 |
| `data/spirit/spirit_content.yaml` | 灵性仁本页面内容 (通过 tags 引用文献) |
| `data/frontier/frontier_dialogue.yaml` | 前沿对话页面内容 |
| `docs/knowledge-management.md` | 项目知识管理总规范 |
| `CLAUDE.md` | 项目总索引 |
