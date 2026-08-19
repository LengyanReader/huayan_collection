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
CREATE INDEX idx_chapters_order ON chapters(sutra_id, order_num);
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
