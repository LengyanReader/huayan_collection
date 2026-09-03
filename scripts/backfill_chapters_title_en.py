#!/usr/bin/env python3
"""Batch A: Fill chapters.title_en for all 41 chapters (80 Hua-yan 39 chapters + 2 Tibetan-unique).

English names follow the standard scholarly convention of Thomas Cleary's
"The Flower Ornament Scripture" (1993) / 84000 Toh 44 Phal chen translations.
These are established academic English renderings, not invented translations.
"""
import sqlite3, sys, io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "catalog" / "huayan.db"

# id -> English title (keyed by chapter id from DB audit)
TITLES_EN = {
    526: "The Wondrous Adornments of the Rulers of the Worlds",
    527: "Apparitions of the Buddha",
    528: "The Samādhi of Universal Good",
    529: "Completions of the Worlds",
    530: "The Flower Bank World",
    531: "Vairocana",
    532: "The Names of the Buddha",
    533: "The Four Holy Truths",
    534: "Awakening by Light",
    535: "Statements of the Questioning Bodhisattvas",
    536: "Pure Practices",
    537: "The Chief of Worthies",
    538: "Ascending to the Peak of Mount Sumeru",
    539: "Eulogies on the Peak of Mount Sumeru",
    540: "The Ten Abodes",
    541: "The Practice of Purity",
    542: "Merits of the First Aspiration for Awakening",
    543: "Understanding the Teaching",
    544: "Ascending to the Palace of the Heaven of Yāma",
    545: "Eulogies in the Palace of the Heaven of Yāma",
    546: "The Ten Practices",
    547: "The Ten Inexhaustible Treasures",
    548: "Ascending to the Palace of Tuṣita Heaven",
    549: "Eulogies in the Palace of Tuṣita Heaven",
    550: "The Ten Transferences",
    551: "The Ten Grounds",
    552: "The Ten Concentrations",
    553: "The Ten Supernatural Powers",
    554: "The Ten Patiences",
    555: "Incalculable Numbers",
    556: "Lifespans",
    557: "The Residences of the Bodhisattvas",
    558: "The Unthinkable Qualities of the Buddhas",
    559: "The Ocean of Marks of the Ten Bodies of the Buddha",
    560: "The Merits of the Great Marks of Light of the Buddha",
    561: "The Practices of Universal Good",
    562: "The Apparition of the Buddha",
    563: "Detachment from the World",
    564: "Entry into the Dharma Realm",
    565: "The Adornment of the Buddha",
    566: "The Disquisition of Universal Good",
}

conn = sqlite3.connect(str(DB))
conn.row_factory = sqlite3.Row

count = 0
for cid, en in TITLES_EN.items():
    row = conn.execute("SELECT title_zh FROM chapters WHERE id = ?", (cid,)).fetchone()
    if not row:
        print(f"  WARN: chapter id {cid} not found, skip")
        continue
    cur = conn.execute("UPDATE chapters SET title_en = ? WHERE id = ?", (en, cid))
    if cur.rowcount:
        count += 1
        print(f"  [{cid}] {row['title_zh']}  =>  {en}")

conn.commit()

# Verify coverage
stats = conn.execute("""
    SELECT COUNT(*) as total,
           SUM(CASE WHEN title_en IS NOT NULL AND title_en != '' THEN 1 ELSE 0 END) as has_en
    FROM chapters
""").fetchone()
print(f"\nChapters title_en coverage: {stats['has_en']}/{stats['total']}")

conn.close()
print(f"\nUpdated {count} chapters.")
