-- ============================================================
-- 华严宗部文献目录数据库 Schema
-- 版本: 0.2.0
-- 数据库: SQLite 3
-- ============================================================

PRAGMA journal_mode = WAL;
PRAGMA foreign_keys = ON;

-- -----------------------------------------------------------
-- 人物表 — 华严宗祖师、译者、行者、学者
-- -----------------------------------------------------------
DROP TABLE IF EXISTS persons;
CREATE TABLE persons (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    source_id       TEXT    UNIQUE,                        -- 原始ID (如 person_042)
    name_zh         TEXT    NOT NULL,
    name_bo         TEXT,                                  -- 藏文名 (Wylie)
    name_sa         TEXT,                                  -- 梵文名 (IAST)
    name_en         TEXT,                                  -- 英文/拼音
    name_ja         TEXT,                                  -- 日文名
    alt_names       TEXT,                                  -- 别名/号，JSON数组: ["贤首国师","香象大师"]
    title           TEXT,                                  -- 头衔/称号 (如 "华严宗三祖")
    type            TEXT    NOT NULL DEFAULT 'practitioner',
                    -- patriarch | translator | practitioner | scholar | patron | monarch
    birth_year      INTEGER,
    death_year      INTEGER,
    dynasty         TEXT,                                  -- 唐/宋/元/明/清/近现代/当代
    biography       TEXT,                                  -- 生平简介
    lineage_branch  TEXT,                                  -- 所属传承支系
    lineage_order   INTEGER,                               -- 在支系中的辈分序位 (1=初祖, 2=二祖...)
    key_works       TEXT,                                  -- 代表著作，JSON数组
    works_links     TEXT,                                  -- 著作链接，JSON对象 {"作品名":"url"}
    multi_lineage   TEXT,                                  -- 多重传承支系，JSON数组 ["临济宗","曹洞宗"]
    source          TEXT,                                  -- 传记出处 (如 《宋高僧传》卷五)
    verified        INTEGER DEFAULT 0,                     -- 0=传统记载 1=学术确认
    created_at      TEXT    DEFAULT (datetime('now')),
    updated_at      TEXT    DEFAULT (datetime('now'))
);

CREATE UNIQUE INDEX idx_persons_source_id ON persons(source_id);
CREATE INDEX idx_persons_dynasty ON persons(dynasty);
CREATE INDEX idx_persons_type ON persons(type);
CREATE INDEX idx_persons_lineage ON persons(lineage_branch);

-- -----------------------------------------------------------
-- 文献表 — 经典、章疏、仪轨、讲记
-- -----------------------------------------------------------
DROP TABLE IF EXISTS texts;
CREATE TABLE texts (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    title_zh        TEXT    NOT NULL,                       -- 中文标题
    title_bo        TEXT,                                   -- 藏文标题 (Wylie)
    title_sa        TEXT,                                   -- 梵文标题 (IAST)
    title_en        TEXT,                                   -- 英文标题
    type            TEXT    NOT NULL DEFAULT 'sutra',
                    -- sutra | vinaya | shastra | commentary | ritual |
                    -- record | study | lecture | collection | catalog
    sub_type        TEXT,                                   -- 华严部 / 般若部 / 涅槃部 ...
    taisho_no       TEXT,                                   -- 大正藏编号 (T0279)
    cbeta_id        TEXT,                                   -- CBETA 内部 ID (T10n0279)
    tohk_no         TEXT,                                   -- 德格版编号 (Toh 44)
    yitian_status   TEXT,                                   -- 义天录: extant|lost|disputed|not_listed
    yitian_ref      TEXT,                                   -- 义天录引用位置
    author_id       INTEGER REFERENCES persons(id),         -- 作者
    translator_id   INTEGER REFERENCES persons(id),         -- 译者
    dynasty         TEXT,                                   -- 成书/翻译朝代
    date_text       TEXT,                                   -- 年份描述 ("约699年")
    date_range      TEXT,                                   -- 年代范围 (如"420-699")
    volumn_count    INTEGER,                                -- 卷数
    chapter_count   INTEGER,                                -- 品数
    structure       TEXT,                                   -- 结构描述 (如"七处九会")
    abstract        TEXT,                                   -- 内容简介
    language        TEXT    DEFAULT 'zh',                   -- 主要语言
    source_url      TEXT,                                   -- 数字化链接
    in_cbeta        INTEGER DEFAULT 1,                      -- 是否在CBETA中
    in_bdrc         INTEGER DEFAULT 0,                      -- 是否在BDRC中
    has_tibetan     INTEGER DEFAULT 0,                      -- 是否有藏译本
    has_sanskrit    INTEGER DEFAULT 0,                      -- 是否有梵文原本/残片
    created_at      TEXT    DEFAULT (datetime('now')),
    updated_at      TEXT    DEFAULT (datetime('now'))
);

CREATE INDEX idx_texts_type ON texts(type);
CREATE INDEX idx_texts_taisho ON texts(taisho_no);
CREATE INDEX idx_texts_cbeta ON texts(cbeta_id);
CREATE INDEX idx_texts_tohk ON texts(tohk_no);
CREATE INDEX idx_texts_dynasty ON texts(dynasty);
CREATE INDEX idx_texts_yitian ON texts(yitian_status);

-- 全文检索
CREATE VIRTUAL TABLE IF NOT EXISTS texts_fts USING fts5(
    title_zh, title_bo, title_sa, title_en,
    abstract, dynasty, date_text,
    content='texts', content_rowid='id'
);

-- -----------------------------------------------------------
-- 品目表
-- -----------------------------------------------------------
DROP TABLE IF EXISTS chapters;
CREATE TABLE chapters (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    sutra_id        INTEGER NOT NULL REFERENCES texts(id),
    title_zh        TEXT    NOT NULL,                       -- 汉文品名
    title_bo        TEXT,                                   -- 藏文品名
    title_sa        TEXT,                                   -- 梵文品名
    title_en        TEXT,                                   -- 英文品名
    order_num       INTEGER NOT NULL,                       -- 品目序号
    volumn_start    INTEGER,                               -- 起始卷
    volumn_end      INTEGER,                               -- 结束卷
    in_60huayan     INTEGER DEFAULT 0,                     -- 六十华严是否有此品
    in_80huayan     INTEGER DEFAULT 0,                     -- 八十华严是否有此品
    in_40huayan     INTEGER DEFAULT 0,                     -- 四十华严是否有此品
    in_tibetan      INTEGER DEFAULT 0,                     -- 藏文是否有此品
    tibetan_order   INTEGER,                               -- 藏文品目序号 (可能不同)
    is_unique_to_bo INTEGER DEFAULT 0,                     -- 藏文独有
    is_unique_to_zh INTEGER DEFAULT 0,                     -- 汉文独有
    content_diff    TEXT,                                   -- 内容差异说明
    source          TEXT,                                   -- 品目列表来源
    created_at      TEXT    DEFAULT (datetime('now'))
);

CREATE INDEX idx_chapters_sutra ON chapters(sutra_id);
-- UNIQUE 必需：import_chapters 用 INSERT OR REPLACE，无 UNIQUE 则每次导入追加一份而非替换
CREATE UNIQUE INDEX idx_chapters_order ON chapters(sutra_id, order_num);
CREATE INDEX idx_chapters_unique_bo ON chapters(is_unique_to_bo);

-- -----------------------------------------------------------
-- 地点表
-- -----------------------------------------------------------
DROP TABLE IF EXISTS locations;
CREATE TABLE locations (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    source_id       TEXT,                                   -- 原始ID (如 loc_001, l_h)
    name_zh         TEXT    NOT NULL,                       -- 古地名
    current_name    TEXT,                                   -- 现代地名
    lat             REAL,                                   -- 纬度
    lng             REAL,                                   -- 经度
    type            TEXT    DEFAULT 'temple',
                    -- temple | mountain | region | city | translation_site
    dynasty         TEXT,
    city            TEXT,                                   -- 所在城市
    province        TEXT,                                   -- 所在省份
    description     TEXT,
    related_persons TEXT,                                   -- 关联人物 ID，JSON 数组
    source          TEXT,
    created_at      TEXT    DEFAULT (datetime('now'))
);

CREATE UNIQUE INDEX idx_locations_source_id ON locations(source_id);
CREATE INDEX idx_locations_type ON locations(type);

-- -----------------------------------------------------------
-- 法系表 — 传承谱系元数据
-- -----------------------------------------------------------
DROP TABLE IF EXISTS lineages;
CREATE TABLE lineages (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    source_id       TEXT    UNIQUE,                         -- 原始ID
    name            TEXT    NOT NULL UNIQUE,                 -- 法系名称
    description     TEXT,
    period          TEXT,                                   -- 时间跨度
    color           TEXT,                                   -- 渲染颜色 (hex)
    created_at      TEXT    DEFAULT (datetime('now'))
);

-- -----------------------------------------------------------
-- 传承边表 — 法脉传承关系
-- -----------------------------------------------------------
DROP TABLE IF EXISTS lineage_edges;
CREATE TABLE lineage_edges (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    from_person_id  TEXT    NOT NULL,                       -- 源人物ID (如 person_003)
    to_person_id    TEXT    NOT NULL,                       -- 目标人物ID
    relation        TEXT    NOT NULL DEFAULT 'MASTER_OF',
                    -- MASTER_OF | INFLUENCED | LINEAGE | CONTEMPORARY
    lineage_name    TEXT,                                   -- 所属法系 (如 华严五祖)
    lineage_id      INTEGER REFERENCES lineages(id),        -- 关联法系表
    note            TEXT,                                   -- 出处说明
    source          TEXT,                                   -- 文献依据
    created_at      TEXT    DEFAULT (datetime('now'))
);

CREATE INDEX idx_edges_from ON lineage_edges(from_person_id);
CREATE INDEX idx_edges_to ON lineage_edges(to_person_id);
CREATE INDEX idx_edges_lineage ON lineage_edges(lineage_name);

-- -----------------------------------------------------------
-- 人物-地点关联 (多对多)
-- -----------------------------------------------------------
DROP TABLE IF EXISTS person_locations;
CREATE TABLE person_locations (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id       INTEGER NOT NULL REFERENCES persons(id),
    location_id     INTEGER NOT NULL REFERENCES locations(id),
    relation        TEXT,                                   -- born | died | taught | visited | resided
    period_start    TEXT,                                   -- 开始时间
    period_end      TEXT,                                   -- 结束时间
    note            TEXT,
    UNIQUE(person_id, location_id, relation)
);

-- -----------------------------------------------------------
-- 文献互参表
-- -----------------------------------------------------------
DROP TABLE IF EXISTS cross_refs;
CREATE TABLE cross_refs (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    from_text_id    INTEGER NOT NULL REFERENCES texts(id),
    to_text_id      INTEGER NOT NULL REFERENCES texts(id),
    relation        TEXT    NOT NULL,
                    -- cites | commentary_on | subcommentary_on |
                    -- alternate_trans | expanded_version | related |
                    -- ritual_based_on | lecture_on
    note            TEXT,
    source          TEXT,
    UNIQUE(from_text_id, to_text_id, relation)
);

CREATE INDEX idx_crossrefs_from ON cross_refs(from_text_id);
CREATE INDEX idx_crossrefs_to ON cross_refs(to_text_id);

-- -----------------------------------------------------------
-- 四语术语表
-- -----------------------------------------------------------
DROP TABLE IF EXISTS glossary;
CREATE TABLE glossary (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    source_id       TEXT,                                   -- 原始ID
    term_sa         TEXT,                                   -- 梵文 (IAST)
    term_bo         TEXT,                                   -- 藏文 (Unicode)
    term_bo_wylie   TEXT,                                   -- 藏文 (Wylie 转写)
    term_bo_unicode TEXT,                                   -- 藏文 (Unicode)
    term_zh         TEXT    NOT NULL,                       -- 汉文
    term_en         TEXT,                                   -- 英文
    category        TEXT    DEFAULT 'doctrine',
                    -- doctrine | practice | cosmology | name | place |
                    -- scripture | lineage | ritual | virtue | state
    definition_zh   TEXT,                                   -- 中文释义
    definition_en   TEXT,                                   -- 英文释义
    source_text_id  INTEGER REFERENCES texts(id),           -- 主要出处
    alt_translations TEXT,                                  -- 其他译法 (JSON)
    created_at      TEXT    DEFAULT (datetime('now'))
);

CREATE INDEX idx_glossary_zh ON glossary(term_zh);
CREATE INDEX idx_glossary_sa ON glossary(term_sa);
CREATE INDEX idx_glossary_category ON glossary(category);

-- 全文检索术语
CREATE VIRTUAL TABLE IF NOT EXISTS glossary_fts USING fts5(
    term_zh, term_sa, term_bo, term_en,
    definition_zh, definition_en,
    content='glossary', content_rowid='id'
);

-- -----------------------------------------------------------
-- 对译单元表
-- -----------------------------------------------------------
DROP TABLE IF EXISTS translation_units;
CREATE TABLE translation_units (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    chapter_id      INTEGER NOT NULL REFERENCES chapters(id),
    paragraph_num   INTEGER,                               -- 段落编号
    source_text     TEXT    NOT NULL,                       -- 藏文原文 (Unicode)
    source_text_roman TEXT,                                 -- 藏文转写 (Wylie)
    chinese_draft   TEXT,                                   -- 汉译草稿
    english_draft   TEXT,                                   -- 英译草稿
    chinese_final   TEXT,                                   -- 汉译定稿
    english_final   TEXT,                                   -- 英译定稿
    status          TEXT    DEFAULT 'pending',
                    -- pending | draft | review | final
    translator_note TEXT,                                   -- 译注
    has_chinese_ref INTEGER DEFAULT 0,                      -- 是否有汉文对应段落 (用于锚定)
    chinese_ref_id  INTEGER REFERENCES chapters(id),        -- 对应汉文品目
    created_at      TEXT    DEFAULT (datetime('now')),
    updated_at      TEXT    DEFAULT (datetime('now'))
);

CREATE INDEX idx_trans_units_chapter ON translation_units(chapter_id);
CREATE INDEX idx_trans_units_status ON translation_units(status);

-- -----------------------------------------------------------
-- 文章知识图谱：名相 · 会处 · 术语（文章级节点）
-- 权威源 data/translation/article_knowledge/<article_id>.yaml
--   → import_all_to_sqlite.py → SQLite → db_reader.load_article_knowledge() → build.py
-- 信度五级（与各文凡例九一致，勿另立名目）：
--   A1 经文直证 | A2 古注明证（注疏判摄名）| B 文献转述
--   C 单一来源或仅见转引待考（含近人自取名）| D 疑讹·不见于经与历代注疏（status=rejected，正文不采用）
-- status：used（本文采用）| rejected（D 级已否之名，仅存于「已否之名」）
--         | coined（近人自取名，非经非古注术语，仅作其用语引述）
-- -----------------------------------------------------------
CREATE TABLE IF NOT EXISTS article_terms (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    article_id     TEXT    NOT NULL,                          -- 对应 articles/<id>.html
    term_id        TEXT    NOT NULL,                          -- 篇内唯一术语 id
    term_zh        TEXT    NOT NULL,                          -- 术语（本名）
    aliases        TEXT,                                      -- JSON 数组：异名/简称/繁体，供正文自动命中
    category       TEXT,                                      -- site|assembly|chapter|doctrine|person|text|method|coined
    grade          TEXT    NOT NULL DEFAULT 'C',              -- A1|A2|B|C|D
    status         TEXT    NOT NULL DEFAULT 'used',           -- used|rejected|coined
    definition_zh  TEXT,                                      -- 释义（中文）
    definition_en  TEXT,                                      -- 释义（英文）
    source_note    TEXT,                                      -- 出处：经号·卷次·首倡者
    source_url     TEXT,                                      -- 可点击回查链接
    note           TEXT,                                      -- 存疑/推断/校记等注记
    created_at     TEXT    DEFAULT (datetime('now')),
    UNIQUE(article_id, term_id)
);

CREATE INDEX IF NOT EXISTS idx_article_terms_article ON article_terms(article_id);
CREATE INDEX IF NOT EXISTS idx_article_terms_grade   ON article_terms(grade);
CREATE INDEX IF NOT EXISTS idx_article_terms_status  ON article_terms(status);

-- 文章知识图谱：边（术语 ↔ 术语／人物／经卷／品／道场／法系／外部资源）
-- to_type：term（本篇内之任一条目，类别见 article_terms.category，含会处/人物/品名等）
--          | chapter | location | person | text | lineage | external（篇外文献，to_ref 给经号如 T45n1738）
CREATE TABLE IF NOT EXISTS article_term_links (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    article_id   TEXT    NOT NULL,
    from_term_id TEXT    NOT NULL,                            -- → article_terms.term_id
    rel          TEXT    NOT NULL,                            -- 关系型：located_at|preached_by|commented_by|alias_of|see_also|defined_by|same_as…
    to_type      TEXT    NOT NULL DEFAULT 'term',             -- 目标实体类型
    to_ref       TEXT    NOT NULL,                            -- 目标 id（既有表 source_id / 经号 / 本文 term_id）
    to_label     TEXT,                                        -- 目标显示名
    note         TEXT,
    UNIQUE(article_id, from_term_id, rel, to_type, to_ref)
);

CREATE INDEX IF NOT EXISTS idx_atl_from  ON article_term_links(article_id, from_term_id);
CREATE INDEX IF NOT EXISTS idx_atl_to    ON article_term_links(to_type, to_ref);
CREATE INDEX IF NOT EXISTS idx_atl_rel   ON article_term_links(article_id, rel);

-- -----------------------------------------------------------
-- 文章附录：艺术品 · 文物 · 壁画 · 考古资料（依品逐条登记）
-- 权威源 data/translation/article_artifacts/<article_id>.yaml
--   → import_all_to_sqlite.py → SQLite → db_reader.load_article_artifacts() → build.py
--   → common.js renderArticleArtifacts()：默认折叠的 <details> 卡片墙
-- 信度五级（同上，勿另立名目）：
--   A1 一手实物/一手著录直接对应本品内容（有定年、有编号或官方释文）
--   A2 学界/机构研究确认为华严系统（著录、专著、论文可据）
--   B 文献转述或同类题材（与本品有涉但非专为本品而作）
--   C 单一来源或仅见转引，细节待考 | D 不采用（status=rejected，不入页面）
-- status：confirmed（已确认可展示）| pending（待核，先登记不展示）| rejected（不采用）
-- 版权与外链：href 必填（指向原始藏品页/权威著录页），thumb_url 可选（公开许可缩略图）；
--   license 与 source_note 必填；无从可点者如实标注〔无链接〕，不硬凑。
-- -----------------------------------------------------------
CREATE TABLE IF NOT EXISTS article_artifacts (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    article_id     TEXT    NOT NULL,                          -- 对应 articles/<id>.html
    artifact_id    TEXT    NOT NULL,                          -- 篇内唯一 id
    title_zh       TEXT    NOT NULL,                          -- 藏品/遗迹名（中文）
    title_en       TEXT,                                      -- 英文名
    era            TEXT,                                      -- 年代
    location       TEXT,                                      -- 现存地/遗址
    category       TEXT,                                      -- mural|sculpture|painting_scroll|manuscript|print|architecture|relic|archaeology
    grade          TEXT    NOT NULL DEFAULT 'C',              -- A1|A2|B|C|D
    status         TEXT    NOT NULL DEFAULT 'pending',        -- confirmed|pending|rejected
    relevance_zh   TEXT,                                      -- 与本品的关联（须具体到会/品/情节，不可泛泛）
    relevance_en   TEXT,
    href           TEXT,                                      -- 原始藏品页/权威著录页（必填）
    thumb_url      TEXT,                                      -- 公开许可缩略图（可选，外链不落盘）
    source_note    TEXT,                                      -- 出处/著录（必填）
    license        TEXT,                                      -- 许可/版权说明（必填）
    note           TEXT,                                      -- 〔待核〕/〔存疑〕/并存诸说
    created_at     TEXT    DEFAULT (datetime('now')),
    UNIQUE(article_id, artifact_id)
);

CREATE INDEX IF NOT EXISTS idx_artifacts_article ON article_artifacts(article_id);
CREATE INDEX IF NOT EXISTS idx_artifacts_grade   ON article_artifacts(grade);
CREATE INDEX IF NOT EXISTS idx_artifacts_status  ON article_artifacts(status);

-- -----------------------------------------------------------
-- 会众结构：品类（四十类）· 成员（四百一十四名）· 所主 · 誓愿
-- 权威源 data/translation/<article_id>_assembly.yaml
--   → import_all_to_sqlite.py → SQLite → db_reader.load_article_assembly() → build.py
-- 用途：《世主妙严品》会众列名段的 EDA 基座（构词法/语义场/网络/维度矩阵）。
--
-- 【实测依据】T10n0279 卷一「而為上首」恰四十次 ↔ 四十类，互证。
--   · 异生三十九类通例各实列十名（上首一＋同类九），非仅列上首一名；
--     十一名之孤例四类：日天子、三十三天王、化樂天王、遍淨天王（已逐条对源核）。
--   · 菩萨轨实列二十名。故卷一实列名共 414 名。
--   · 与《華嚴經三十八卷本》袖珍版编者按「20/190/80/71/51＝412」之关系：
--     菩萨20、神190、八部80、色界天51 四项与本表**完全吻合**（说明编者按系据
--     实列名统计），惟欲界天编者按作71、本表实测73，差二（〔存疑〕待考）。
--
-- 【n_named 语义】该类经文明列之成员数，≠ 该类众数（后者为「微塵數／無量」，
--   经文不确指）。executive 类的 count_expr 存经文原数词。
-- 【vow】该类结句。执金刚神一类长达 128 字（分号分七句），为三十九类誓愿之最
--   （余多在 8–22 字），此不对称为经文事实，非抽取误差。
-- 【vow_kind】结句语法有二，不可合并统计：「誓愿」为三十九类之集总誓语；
--   「成就」仅菩萨轨一（314 字之成就赞叹）。菩萨之结句与异生之结句不同质，
--   早期版本误截为 14 字（「往昔皆與毘盧遮那如來共集善根」），已复原全段。
-- 【collective_zh / collective_pos】集总词与其位置。**位置不可省**：主藥神作
--   「性皆離垢」、主空神作「心皆離垢」，集总词「皆」在第二字；若以「是否以集总词
--   起首」判有无，此二类连同数词混入之四类共六类将被误记为无。实测全四十类中
--   确无集总词者仅主水神、主方神二类（与「十九类神十七类用总词」之说相合）。
-- 【punct_variant / glyph_variant】CBETA 异文与字形异文，据实登记，不擅改经文。
-- -----------------------------------------------------------
CREATE TABLE IF NOT EXISTS article_assembly_classes (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    article_id      TEXT    NOT NULL,                          -- 对应 articles/<id>.html
    cls_idx         INTEGER NOT NULL,                          -- 卷一列名次第，0=菩萨轨
    cat_zh          TEXT    NOT NULL,                          -- 类名（依 CBETA 字形，如「阿脩羅王」）
    group_key       TEXT    NOT NULL,                          -- bodhisattva|deities|eight|desire|form
    group_zh        TEXT,                                      -- 同生众·菩萨／异生众·十九类神 等
    realm           TEXT,                                      -- 智正觉世间主／器世间主／天众／众生世间主
    count_expr      TEXT,                                      -- 经文数词原样：復有無量／復有佛世界微塵數
    leader_zh       TEXT,                                      -- 上首（所列首名）
    n_named         INTEGER NOT NULL,                          -- 经文明列成员数（非众数）
    domain_zh       TEXT,                                      -- 所主/职能：城郭宫殿／山岳／四王 等
    collective_zh   TEXT,                                      -- 集总词：皆／悉已／莫不皆得
    collective_pos  TEXT,                                      -- 集总词位置：起首／句中
    vow_kind        TEXT,                                      -- 结句性质：誓愿／成就
    vow_zh          TEXT,                                      -- 结句（集总誓愿或成就赞叹）全量
    punct_variant   TEXT,                                      -- 标点异文：所謂；／所謂
    glyph_variant   TEXT,                                      -- 字形异文：寶峯 等
    source_note     TEXT,                                      -- 出处：T10n0279 卷一
    created_at      TEXT    DEFAULT (datetime('now')),
    UNIQUE(article_id, cls_idx)
);

CREATE INDEX IF NOT EXISTS idx_aac_article ON article_assembly_classes(article_id);
CREATE INDEX IF NOT EXISTS idx_aac_group   ON article_assembly_classes(article_id, group_key);

CREATE TABLE IF NOT EXISTS article_assembly_members (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    article_id      TEXT    NOT NULL,
    cls_idx         INTEGER NOT NULL,                          -- 所属类（外键逻辑关联，勿加 FK 以保可重导）
    member_idx      INTEGER NOT NULL,                          -- 类内次第，1=上首
    member_zh       TEXT    NOT NULL,                          -- 成员名（依 CBETA 字形）
    is_leader       INTEGER NOT NULL DEFAULT 0,               -- 1=该类上首
    created_at      TEXT    DEFAULT (datetime('now')),
    UNIQUE(article_id, cls_idx, member_idx)
);

CREATE INDEX IF NOT EXISTS idx_aam_article ON article_assembly_members(article_id);
CREATE INDEX IF NOT EXISTS idx_aam_cls     ON article_assembly_members(article_id, cls_idx);

-- -----------------------------------------------------------
-- 会众名号构词法 EDA（世主妙严品卷一 414 名）
--   权威源 data/translation/miaoyan_eda.yaml（由 scripts/miaoyan_eda.py 生成，
--   其语义标注源为 data/translation/miaoyan_eda_lexicon.yaml，人工编纂）
--   → import_all_to_sqlite.py → SQLite → db_reader.load_article_eda()
--   → build.py 内嵌 var ARTICLE_EDA → common.js renderArticleEDA()
--
-- ⚠ 铁律：本组三表装的是**编辑性析构分析**，非经文自述数据。
--   ① 切分（词级最长匹配 + 逐字退段）是工具的**方法选择**，非经文原貌；
--   ② domain 语义域是**单一判读视角**下每词素归一域，非该字全部义项；
--   ③ confidence=c 逐条标 high/medium/low，low 者前端须显示〔待考〕；
--   ④ n_named（明列成员数）≠ 该类众数（经文作「微塵數／無量」），严禁混用；
--   ⑤ method_json 存全部方法声明，渲染层须原样呈现，不得只挑好看的数。
--   故本组表与 article_assembly_* 分立：前者是经文事实，后者是编者分析。
-- -----------------------------------------------------------
CREATE TABLE IF NOT EXISTS article_eda_docs (
    article_id      TEXT    NOT NULL UNIQUE,                    -- 对应 articles/<id>.html
    source          TEXT,                                       -- 经号·卷次
    source_url      TEXT,                                       -- 可点击回查链接
    generated_by    TEXT,                                       -- 生成器（脚本路径＋源文件）
    method_json     TEXT,                                       -- 方法声明（method 段全量 JSON）
    metrics_json    TEXT,                                       -- 统计指标（metrics 段全量 JSON）
    payload_json    TEXT,                                       -- 渲染所需全量文档（热力图/矩阵/图/类目…）
    created_at      TEXT    DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS article_eda_morphemes (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    article_id      TEXT    NOT NULL,
    zh              TEXT    NOT NULL,                          -- 词素（词级或多字，单字皆可能）
    n               INTEGER NOT NULL,                          -- 两段切分下的出现次数
    n_char_only     INTEGER NOT NULL DEFAULT 0,               -- 纯逐字对照下的出现次数
    seg_mode        TEXT    NOT NULL DEFAULT 'char',           -- word=多字词命中 | char=逐字
    domain          TEXT,                                       -- 十六语义域之一
    confidence      TEXT,                                       -- high|medium|low（判读置信度）
    gloss           TEXT,                                       -- 中文释义
    gloss_en        TEXT,
    rank            INTEGER NOT NULL DEFAULT 0,                -- 频次序（1=最高）
    UNIQUE(article_id, zh)
);

CREATE INDEX IF NOT EXISTS idx_aem_article ON article_eda_morphemes(article_id, rank);

CREATE TABLE IF NOT EXISTS article_eda_member_segs (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    article_id      TEXT    NOT NULL,
    cls_idx         INTEGER NOT NULL,                          -- 所属类
    member_idx      INTEGER NOT NULL,                          -- 类内次第
    seq             INTEGER NOT NULL,                          -- 词素在核名中之序（1=首）
    token           TEXT    NOT NULL,                          -- 词素字面
    seg_mode        TEXT    NOT NULL,                          -- word|char
    known           INTEGER NOT NULL DEFAULT 1,               -- 0=未入词素表（待补）
    domain          TEXT,                                       -- 语义域（unassigned=未定）
    confidence      TEXT,
    UNIQUE(article_id, cls_idx, member_idx, seq)
);

CREATE INDEX IF NOT EXISTS idx_aems_member ON article_eda_member_segs(article_id, cls_idx, member_idx);
CREATE INDEX IF NOT EXISTS idx_aems_token  ON article_eda_member_segs(article_id, token);

-- -----------------------------------------------------------
-- 实体百科：有名有姓之存在（众·天王·菩萨·金刚神·龙·八部·诸神·佛）
--   权威源 data/encyclopedia/beings.yaml
--   → import_all_to_sqlite.py → SQLite → db_reader.load_entity_registry()
--   → build.py 内嵌 var ENTITY_REGISTRY（全站共用一份，故非 article-scoped）
--   → common.js markEntityRefs()／openEntityCard()：正文点开实体卡
-- 与 article_terms（名相·会处·术语）之别：
--   article_terms 管「法义名相」（如「业变力」「教轮」）；
--   entities 管「有名有姓之存在」（如「善化天王」「文殊师利菩萨」「阿修罗」）。
--   二者不重复登记：entities.relations 可指向 article_terms 之 term（to_type='term'）。
-- 信度五级（与全站一致，勿另立名目）：
--   A1 经文直证（本经明文作此名号/此事）| A2 古注明证（历代注疏原文明文）
--   B 文献转述 | C 单一来源或仅见转引，待考 | D 疑讹（status='rejected'，不入正文）
-- status：used（采用）| pending（待核，先登记不展示）| rejected（D 疑讹，不采用）
-- 「断言级信度」：实体整体之 grade 只管其名号；小传中每一项事实之可信度
--   由 entity_claims.grade 逐条独立判定——故名号可 A1 而梵名/世系为 C，二者并存不悖。
--   铁律：每条 claim 必带 grade，且必带 source（经号·卷次），
--   否则须于 note 明写〔待核〕/〔无出处〕，严禁无源之断言（编务总则第 0/3/7 条）。
-- -----------------------------------------------------------
CREATE TABLE IF NOT EXISTS entities (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    entity_id     TEXT    NOT NULL UNIQUE,                      -- 全局唯一 id
    name_zh       TEXT    NOT NULL,                             -- 本名（如「善化天王」）
    name_full     TEXT,                                         -- 全称/领众全名（如「一切善化天众」之主）
    name_sa       TEXT,                                         -- 梵名（无据则留空并于 note 标〔待核〕）
    name_en       TEXT,                                         -- 英文名（循全站固定译名）
    aliases       TEXT,                                         -- JSON 数组：异名/简称/繁体，供正文自动命中
    category      TEXT,                                         -- 天众|菩萨|金刚神|龙|八部|诸神|佛|人名
    grade         TEXT    NOT NULL DEFAULT 'C',                 -- A1|A2|B|C|D（管名号本身）
    status        TEXT    NOT NULL DEFAULT 'used',              -- used|pending|rejected
    auto_link     INTEGER NOT NULL DEFAULT 1,                  -- 0 = 不作正文自动命中（泛称/易误命中者）
    bio_zh        TEXT,                                         -- 小传（中文）
    bio_en        TEXT,                                         -- 小传（英文）
    source_note   TEXT,                                         -- 出处：经号·卷次
    source_url    TEXT,                                         -- 可点击回查链接（CBETA Online）
    note          TEXT,                                         -- 存疑/待核/边界说明
    created_at    TEXT    DEFAULT (datetime('now')),
    updated_at    TEXT    DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_entities_cat   ON entities(category);
CREATE INDEX IF NOT EXISTS idx_entities_grade ON entities(grade);
CREATE INDEX IF NOT EXISTS idx_entities_status ON entities(status);

-- 实体小传之逐条考据（断言级信度之载体）
CREATE TABLE IF NOT EXISTS entity_claims (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    entity_id   TEXT    NOT NULL,                               -- → entities.entity_id
    seq         INTEGER NOT NULL,                               -- 序（保持 YAML 顺序）
    text        TEXT    NOT NULL,                               -- 该条事实
    grade       TEXT    NOT NULL DEFAULT 'C',                  -- A1|A2|B|C|D
    source      TEXT,                                           -- 经号·卷次·首倡者
    source_url  TEXT,                                           -- 可点击回查
    note        TEXT,                                           -- 〔待核〕/〔存疑〕/校记
    UNIQUE(entity_id, seq)
);

CREATE INDEX IF NOT EXISTS idx_entity_claims_entity ON entity_claims(entity_id);
CREATE INDEX IF NOT EXISTS idx_entity_claims_grade  ON entity_claims(grade);

-- 实体之关系（可互点跳转；to_type='entity' 者前端可续查）
CREATE TABLE IF NOT EXISTS entity_relations (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    from_id    TEXT    NOT NULL,                                -- → entities.entity_id
    rel        TEXT    NOT NULL,                                -- leads|heads|同会|统属|所对|所住|师|眷属|化身|见…
    to_type    TEXT    NOT NULL DEFAULT 'entity',              -- entity|person|location|text|chapter|term|external
    to_ref     TEXT    NOT NULL,
    to_label   TEXT,
    grade      TEXT    NOT NULL DEFAULT 'C',
    note       TEXT,
    UNIQUE(from_id, rel, to_type, to_ref)
);

CREATE INDEX IF NOT EXISTS idx_entity_rel_from ON entity_relations(from_id);
CREATE INDEX IF NOT EXISTS idx_entity_rel_to   ON entity_relations(to_type, to_ref);

-- -----------------------------------------------------------
-- 触发器: 保持 FTS 索引同步
-- -----------------------------------------------------------
CREATE TRIGGER IF NOT EXISTS texts_ai AFTER INSERT ON texts BEGIN
    INSERT INTO texts_fts(rowid, title_zh, title_bo, title_sa, title_en,
                          abstract, dynasty, date_text)
    VALUES (new.id, new.title_zh, new.title_bo, new.title_sa, new.title_en,
            new.abstract, new.dynasty, new.date_text);
END;

CREATE TRIGGER IF NOT EXISTS texts_ad AFTER DELETE ON texts BEGIN
    INSERT INTO texts_fts(texts_fts, rowid, title_zh, title_bo, title_sa, title_en,
                          abstract, dynasty, date_text)
    VALUES ('delete', old.id, old.title_zh, old.title_bo, old.title_sa, old.title_en,
            old.abstract, old.dynasty, old.date_text);
END;

CREATE TRIGGER IF NOT EXISTS texts_au AFTER UPDATE ON texts BEGIN
    INSERT INTO texts_fts(texts_fts, rowid, title_zh, title_bo, title_sa, title_en,
                          abstract, dynasty, date_text)
    VALUES ('delete', old.id, old.title_zh, old.title_bo, old.title_sa, old.title_en,
            old.abstract, old.dynasty, old.date_text);
    INSERT INTO texts_fts(rowid, title_zh, title_bo, title_sa, title_en,
                          abstract, dynasty, date_text)
    VALUES (new.id, new.title_zh, new.title_bo, new.title_sa, new.title_en,
            new.abstract, new.dynasty, new.date_text);
END;
