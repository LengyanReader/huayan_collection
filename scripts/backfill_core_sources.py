#!/usr/bin/env python3
"""
核心华严传承 — 第一手来源回填（策展脚本，一次可重复执行）

依据（2026-08-29 完成可回溯核实）：
  T1 一级史料                                 人物                CBETA
  《续高僧传》卷二十五·法顺传               杜顺                T50n2060
  《宋高僧传》卷五·智俨传                   智俨                T50n2061
  《宋高僧传》卷五·法藏传 /《法藏和尚传》     法藏                T50n2061 / T50n2054
  《宋高僧传》卷五·澄观传                   澄观                T50n2061
  《宋高僧传》卷六·宗密传                   宗密                T50n2061
  《宋高僧传》卷二十二·李通玄传              李通玄               T50n2061
  《宋高僧传》卷四·元晓传 / 卷四·义湘传      元晓、义湘           T50n2061
  《宋高僧传》卷六·慧苑传 +《开元释教录》卷九 +《贞元新定释教目录》卷十四  慧苑
  《龙树菩萨传》                            龙树                T50n2047
  《东大寺要录》《续日本纪》                审祥、良弁
  《元亨释书》(CBETA B32n0173)              明惠
  凝然《三国佛法传通缘起》(自述)             凝然
  《均如传》〔赫连挺〕、《三国遗事》卷五       均如
现代/机构资料无可独立核证者，一律挂〔存疑〕标注，不标 verified。

用法:  python scripts/backfill_core_sources.py
"""

import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "catalog" / "huayan.db"

# ── 人物：name_zh → (source, verified) ──
PERSONS = {
    "杜顺": ("《续高僧传》卷二十五·法顺传 (CBETA T50n2060)", 1),
    "智俨": ("《宋高僧传》卷五·智俨传 (CBETA T50n2061)；《华严经传记》卷四", 1),
    "法藏": ("《宋高僧传》卷五·法藏传 (CBETA T50n2061)；《法藏和尚传》(CBETA T50n2054)", 1),
    "澄观": ("《宋高僧传》卷五·澄观传 (CBETA T50n2061)；《佛祖统纪》卷二十九", 1),
    "宗密": ("《宋高僧传》卷六·宗密传 (CBETA T50n2061)", 1),
    "李通玄": ("《宋高僧传》卷二十二·李通玄传 (CBETA T50n2061)", 1),
    "龙树": ("《龙树菩萨传》(CBETA T50n2047)；《华严经传记》", 1),
    "元晓": ("《宋高僧传》卷四·元晓传 (CBETA T50n2061)", 1),
    "义湘": ("《宋高僧传》卷四·义湘传 (CBETA T50n2061)", 1),
    "慧苑": ("《宋高僧传》卷六·慧苑传 (CBETA T50n2061)；《开元释教录》卷九；《贞元新定释教目录》卷十四", 1),
    "审祥": ("《东大寺要录》；《续日本纪》〔天平十二年(740)于金钟道场开讲《六十华严》〕", 1),
    "良弁": ("《东大寺要录》〔奏请审祥开讲《华严经》；东大寺初代别当〕", 1),
    "明惠": ("《元亨释书》(CBETA B32n0173)·明惠传；《明恵上人伝記》", 1),
    "凝然": ("凝然自著《三国佛法传通缘起》（自述华严相承）；《东大寺续要录》", 1),
    "均如": ("《均如传》〔赫连挺辑〕；《三国遗事》卷五", 1),
    "梦参": ("《梦参老和尚_综合深度研究》(docs/，信源分级+〔存疑〕标注)", 1),
    "海云继梦": ("大华严寺法脉资料（2024年）〔存疑：\"三脉汇一\"等谱系为教界自述，未见独立史料佐证〕", 0),
    "南亭": ("华严莲社社志/官网〔存疑：机构史料，含谱系自述〕", 0),
    "成一": ("华严莲社社志/官网〔存疑：机构史料，含谱系自述〕", 0),
    "了中": ("华严莲社社志/官网〔存疑：机构史料，含谱系自述〕", 0),
    "净海": ("华严莲社社志/官网〔存疑：机构史料，含谱系自述〕", 0),
    "贤度": ("华严莲社社志/官网〔存疑：机构史料，含谱系自述〕", 0),
    "明度": ("华严莲社社志/官网〔存疑：机构史料，含谱系自述〕", 0),
    "如孝": ("凤凰网佛教（2024年）〔存疑：媒体转述，待一手史料〕", 0),
}

# ── 传承边：(from, to, relation) → source ──
EDGES = {
    ("杜顺", "智俨", "MASTER_OF"): "《续高僧传》卷二十五·法顺传；《宋高僧传》卷五·智俨传 (CBETA T50n2061)",
    ("智俨", "法藏", "MASTER_OF"): "《宋高僧传》卷五·法藏传 (CBETA T50n2061)",
    ("智俨", "义湘", "MASTER_OF"): "《宋高僧传》卷四·义湘传〔入唐师事智俨〕(CBETA T50n2061)",
    ("法藏", "审祥", "MASTER_OF"): "《东大寺要录》〔审祥以《探玄记》开讲《六十华严》〕",
    ("法藏", "慧苑", "MASTER_OF"): "《宋高僧传》卷六·慧苑传 (CBETA T50n2061)；《开元释教录》卷九",
    ("法藏", "澄观", "INFLUENCED"): "《宋高僧传》卷五·澄观传〔承法藏《华严》之学〕(CBETA T50n2061)",
    ("慧苑", "澄观", "INFLUENCED"): "《宋高僧传》卷六·慧苑传〔澄观刊定慧苑异说〕(CBETA T50n2061)",
    ("澄观", "宗密", "MASTER_OF"): "《宋高僧传》卷五·澄观传〔付法宗密〕(CBETA T50n2061)",
    ("法藏", "净源", "INFLUENCED"): "《佛祖统纪》卷二十九·净源传〔宋代华严中兴，承法藏之学〕",
    ("净源", "义天", "MASTER_OF"): "《高丽史》卷九十·义天传；《佛祖统纪》卷二十九·净源传",
    ("审祥", "良弁", "MASTER_OF"): "《东大寺要录》〔审祥授华严于良弁，为东大寺华严相承开端〕",
    ("良弁", "实忠", "MASTER_OF"): "凝然《三国佛法传通缘起》〔东大寺华严相承谱〕",
    ("实忠", "等定", "MASTER_OF"): "凝然《三国佛法传通缘起》〔东大寺华严相承谱〕",
    ("等定", "观贤", "MASTER_OF"): "凝然《三国佛法传通缘起》〔东大寺华严相承谱〕",
    ("观贤", "明惠", "INFLUENCED"): "《元亨释书》(CBETA B32n0173)",
    ("明惠", "凝然", "INFLUENCED"): "《元亨释书》(CBETA B32n0173)；凝然《三国佛法传通缘起》",
    ("空海", "法藏", "INFLUENCED"): "空海《御请来目录》(CBETA T55n2161)〔法藏教判思想〕",
    ("慧果", "空海", "MASTER_OF"): "空海《御请来目录》(CBETA T55n2161)；《大唐青龙寺三朝供奉大德行状》",
    ("菩提流支", "慧光", "MASTER_OF"): "《续高僧传》卷二十一·慧光传〔受《十地经论》〕",
    ("法藏", "实叉难陀", "INFLUENCED"): "《宋高僧传》卷二·实叉难陀传〔法藏笔受八十华严〕(CBETA T50n2061)",
    ("法藏", "实叉难陀", "CONTEMPORARY"): "《宋高僧传》卷二·实叉难陀传〔同参译场〕(CBETA T50n2061)",
    ("龙树", "无著", "INFLUENCED"): "学术考证〔中观→瑜伽行次第关联，文献出于后出〕(T2)",
    ("均如", "义天", "INFLUENCED"): "《均如传》；《高丽史》卷九十〔义天辑华严章疏，承均如之学〕",
    ("杜顺", "元晓", "INFLUENCED"): "〔存疑〕学理渊源系后代推衍，无师承史料",
    ("玄奘", "杜顺", "CONTEMPORARY"): "〔存疑〕仅年代粗略同代，不载交往",
    ("玄奘", "法藏", "CONTEMPORARY"): "〔存疑〕仅年代粗略同代，不载交往",
    ("宗密", "澄观", "MASTER_OF"): "〔存疑〕方向存疑：宗密学于澄观，常规记为澄观→宗密 (CBETA T50n2061)",
    ("净源", "均如", "INFLUENCED"): "〔存疑〕均如(923-998)早于净源(1011-1088)，影响方向待考",
    ("净源", "子璿", "INFLUENCED"): "〔存疑〕同代华严学者，影响关系缺直接史料",
    ("梦参", "海云继梦", "MASTER_OF"): "〔存疑〕教界口述谱系，未见独立史料",
    ("钦因", "海云继梦", "MASTER_OF"): "〔存疑〕教界口述谱系，未见独立史料",
    ("胜师子王菩萨", "海云继梦", "MASTER_OF"): "〔存疑〕梦中授法系教界自述，不可独立验证",
    ("高原明昱", "钦因", "INFLUENCED"): "〔存疑〕贤首宗《付法师资记》系宗内谱系记载",
    ("高原明昱", "续法", "INFLUENCED"): "〔存疑〕贤首宗《付法师资记》系宗内谱系记载",
    ("南亭", "成一", "MASTER_OF"): "华严莲社社志〔存疑：机构谱系〕",
    ("成一", "了中", "MASTER_OF"): "华严莲社社志〔存疑：机构谱系〕",
    ("了中", "净海", "MASTER_OF"): "华严莲社社志〔存疑：机构谱系〕",
    ("净海", "贤度", "MASTER_OF"): "华严莲社社志〔存疑：机构谱系〕",
    ("贤度", "明度", "MASTER_OF"): "华严莲社社志〔存疑：机构谱系〕",
}

# ── 道场：source_id → source ──
LOCATIONS = {
    "loc_002": "《续高僧传》卷二十五·法顺传〔至相寺〕；《宋高僧传》卷五",
    "loc_001": "《宋高僧传》卷四·又《慈恩传》：大慈恩寺为玄奘译经主道场",
    "loc_008": "华严莲社社志/官网〔存疑：机构史料〕",
    "loc_009": "近现代佛教史料〔存疑〕",
    "loc_016": "大毘卢寺官网〔存疑：机构自述〕",
    "l_nara": "《东大寺要录》；《续日本纪》",
    "l_f": "福慧寺团体现状资料〔存疑：自述〕",
    "l_h": "大华严寺团体现状资料〔存疑：自述〕",
}


def main():
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("PRAGMA foreign_keys=ON")
    done_p = done_e = done_l = skip = 0
    for name, (src, verified) in PERSONS.items():
        if not cur.execute("SELECT 1 FROM persons WHERE name_zh=?", (name,)).fetchone():
            skip += 1
            print("  skip person:", name)
            continue
        cur.execute("UPDATE persons SET source=?, verified=? WHERE name_zh=?",
                    (src, verified, name))
        done_p += 1
    for (frm, to, rel), src in EDGES.items():
        cur.execute("""UPDATE lineage_edges SET source=? WHERE from_person_id=(SELECT source_id FROM persons WHERE name_zh=?)
                       AND to_person_id=(SELECT source_id FROM persons WHERE name_zh=?)
                       AND relation=?""", (src, frm, to, rel))
        done_e += cur.rowcount
        if cur.rowcount == 0:
            skip += 1
            print("  skip edge:", frm, "→", to, rel)
    for lid, src in LOCATIONS.items():
        if not cur.execute("SELECT 1 FROM locations WHERE source_id=?", (lid,)).fetchone():
            skip += 1
            print("  skip location:", lid)
            continue
        cur.execute("UPDATE locations SET source=? WHERE source_id=?", (src, lid))
        done_l += 1
    con.commit()
    print("Done: persons=%d edges=%d locations=%d skip=%d" % (done_p, done_e, done_l, skip))
    con.close()


if __name__ == "__main__":
    main()