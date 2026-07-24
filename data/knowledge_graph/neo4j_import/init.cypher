// ============================================================
// 华严宗部知识图谱 — Neo4j 初始化脚本
// 版本: 0.1.0
// ============================================================

// --- 约束: 确保数据唯一性 ---

CREATE CONSTRAINT unique_person IF NOT EXISTS
FOR (p:Person) REQUIRE (p.name_zh, p.birth_year) IS UNIQUE;

CREATE CONSTRAINT unique_text IF NOT EXISTS
FOR (t:Text) REQUIRE t.taisho_no IS UNIQUE;

CREATE CONSTRAINT unique_text_cbeta IF NOT EXISTS
FOR (t:Text) REQUIRE t.cbeta_id IS UNIQUE;

CREATE CONSTRAINT unique_location IF NOT EXISTS
FOR (l:Location) REQUIRE (l.name_zh, l.current_name) IS UNIQUE;

CREATE CONSTRAINT unique_chapter IF NOT EXISTS
FOR (c:Chapter) REQUIRE (c.sutra_title, c.order_num) IS UNIQUE;

CREATE CONSTRAINT unique_lineage IF NOT EXISTS
FOR (l:Lineage) REQUIRE l.name IS UNIQUE;

CREATE CONSTRAINT unique_dynasty IF NOT EXISTS
FOR (d:Dynasty) REQUIRE d.name IS UNIQUE;

// --- 索引: 加速查询 ---

CREATE INDEX person_name FOR (p:Person) ON (p.name_zh);
CREATE INDEX person_type FOR (p:Person) ON (p.type);
CREATE INDEX person_dynasty FOR (p:Person) ON (p.dynasty);
CREATE INDEX text_type FOR (t:Text) ON (t.type);
CREATE INDEX text_dynasty FOR (t:Text) ON (t.dynasty);
CREATE INDEX location_type FOR (l:Location) ON (l.type);

// --- 朝代节点 (作为时间锚点) ---

CREATE (:Dynasty {name: '东晋', start_year: 317, end_year: 420});
CREATE (:Dynasty {name: '南北朝', start_year: 420, end_year: 589});
CREATE (:Dynasty {name: '隋', start_year: 581, end_year: 618});
CREATE (:Dynasty {name: '唐', start_year: 618, end_year: 907});
CREATE (:Dynasty {name: '五代', start_year: 907, end_year: 960});
CREATE (:Dynasty {name: '宋', start_year: 960, end_year: 1279});
CREATE (:Dynasty {name: '辽', start_year: 907, end_year: 1125});
CREATE (:Dynasty {name: '金', start_year: 1115, end_year: 1234});
CREATE (:Dynasty {name: '元', start_year: 1271, end_year: 1368});
CREATE (:Dynasty {name: '明', start_year: 1368, end_year: 1644});
CREATE (:Dynasty {name: '清', start_year: 1644, end_year: 1912});
CREATE (:Dynasty {name: '近现代', start_year: 1912, end_year: 2025});

// --- 传承支系节点 ---

CREATE (:Lineage {name: '华严五祖', note: '从杜顺到宗密的华严宗正统传承'});
CREATE (:Lineage {name: '李通玄系', note: '李通玄（枣柏大师）及其后学传承'});
CREATE (:Lineage {name: '高丽华严', note: '高丽义天传入的华严教学传统'});
CREATE (:Lineage {name: '日本华严', note: '日本东大寺等华严传承'});
CREATE (:Lineage {name: '月霞系', note: '清末月霞长老复兴华严的现代传承'});
CREATE (:Lineage {name: '智光系', note: '民国智光法师华严传承'});
CREATE (:Lineage {name: '慈舟系', note: '民国慈舟法师华严传承'});
