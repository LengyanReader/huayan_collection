#!/usr/bin/env python3
"""Batch A: Fill chapters.title_en for all 41 chapters (80 华严 39 品 + 2 Tibetan-unique).

English names follow the standard scholarly convention of Thomas Cleary's
"The Flower Ornament Scripture" (1993) / 84000 Toh 44 Phal chen translations.
These are established academic English renderings, not invented translations.

NOTE(2026-09-27): keyed by title_zh instead of chapter id. Rowids are NOT
stable across `db-reset`/rebuild (old DB ids 526-566 became 1-41 after the
import pipeline re-ran, silently zeroing this backfill). title_zh is the
stable natural key for chapters.
"""
import sqlite3, sys, io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "catalog" / "huayan.db"

# title_zh -> English title (natural key, rebuild-stable)
TITLES_EN = {
    "世主妙严品": "The Wondrous Adornments of the Rulers of the Worlds",
    "如来现相品": "Apparitions of the Buddha",
    "普贤三昧品": "The Samādhi of Universal Good",
    "世界成就品": "Completions of the Worlds",
    "华藏世界品": "The Flower Bank World",
    "毗卢遮那品": "Vairocana",
    "如来名号品": "The Names of the Buddha",
    "四圣谛品": "The Four Holy Truths",
    "光明觉品": "Awakening by Light",
    "菩萨问明品": "Statements of the Questioning Bodhisattvas",
    "净行品": "Pure Practices",
    "贤首品": "The Chief of Worthies",
    "升须弥山顶品": "Ascending to the Peak of Mount Sumeru",
    "须弥顶上偈赞品": "Eulogies on the Peak of Mount Sumeru",
    "十住品": "The Ten Abodes",
    "梵行品": "The Practice of Purity",
    "初发心功德品": "Merits of the First Aspiration for Awakening",
    "明法品": "Understanding the Teaching",
    "升夜摩天宫品": "Ascending to the Palace of the Heaven of Yāma",
    "夜摩宫中偈赞品": "Eulogies in the Palace of the Heaven of Yāma",
    "十行品": "The Ten Practices",
    "十无尽藏品": "The Ten Inexhaustible Treasures",
    "升兜率天宫品": "Ascending to the Palace of Tuṣita Heaven",
    "兜率宫中偈赞品": "Eulogies in the Palace of Tuṣita Heaven",
    "十回向品": "The Ten Transferences",
    "十地品": "The Ten Grounds",
    "十定品": "The Ten Concentrations",
    "十通品": "The Ten Supernatural Powers",
    "十忍品": "The Ten Patiences",
    "阿僧祇品": "Incalculable Numbers",
    "寿量品": "Lifespans",
    "诸菩萨住处品": "The Residences of the Bodhisattvas",
    "佛不思议法品": "The Unthinkable Qualities of the Buddhas",
    "如来十身相海品": "The Ocean of Marks of the Ten Bodies of the Buddha",
    "如来随好光明功德品": "The Merits of the Great Marks of Light of the Buddha",
    "普贤行品": "The Practices of Universal Good",
    "如来出现品": "The Apparition of the Buddha",
    "离世间品": "Detachment from the World",
    "入法界品": "Entry into the Dharma Realm",
    "如来华严品": "The Adornment of the Buddha",
    "普贤宣说品": "The Disquisition of Universal Good",
}

conn = sqlite3.connect(str(DB))
conn.row_factory = sqlite3.Row

count = miss = 0
for zh, en in TITLES_EN.items():
    cur = conn.execute("UPDATE chapters SET title_en = ? WHERE title_zh = ?", (en, zh))
    if cur.rowcount:
        count += cur.rowcount
        print(f"  {zh}  =>  {en}")
    else:
        miss += 1
        print(f"  WARN: title_zh {zh!r} not found in chapters")

conn.commit()

# Verify coverage
stats = conn.execute("""
    SELECT COUNT(*) as total,
           SUM(CASE WHEN title_en IS NOT NULL AND title_en != '' THEN 1 ELSE 0 END) as has_en
    FROM chapters
""").fetchone()
print(f"\nChapters title_en coverage: {stats['has_en']}/{stats['total']} (updated={count}, missing_keys={miss})")

conn.close()
