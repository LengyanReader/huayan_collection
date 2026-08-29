#!/usr/bin/env python3
"""
道场/区域补源（策展脚本，幂等可重复执行）
为地理/道场节点回填可回溯来源（T1 原典 / T2 学术 / 现代道场〔存疑〕如实标注）。

用法:  python scripts/backfill_location_sources.py
"""

import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "catalog" / "huayan.db"

LOCATIONS = {
    "l_changan_t": "《高僧传》卷二·鸠摩罗什传〔逍遥园西明阁译场〕(CBETA T50n2059)",
    "l_changan_x": "《大慈恩寺三藏法师传》(CBETA T50n2053)；玄奘《大唐西域记》〔慈恩/弘福译场〕",
    "l_ganden": "《至尊宗喀巴大师传》〔法尊译〕〔宗喀巴建寺（1409），格鲁派祖庭〕(T2)",
    "l_guangzhou": "《高僧传》卷三·求那跋陀罗传〔南朝海上译经口岸〕(CBETA T50n2059)",
    "l_kolkata": "辨喜《演讲与布道全集》〔1897 创立罗摩克里希纳传道会总部〕(T1)",
    "l_kucha": "《高僧传》卷二·鸠摩罗什传〔龟兹故里〕；玄奘《大唐西域记》卷一",
    "l_nalanda": "玄奘《大唐西域记》卷九·那烂陀僧伽蓝〔无著/世亲/玄奘修学处〕",
    "l_nalanda2": "玄奘《大唐西域记》卷九·那烂陀僧伽蓝（参考位置标注，与前条比对）",
    "l_pondi": "奥罗宾多自著《综合瑜伽》等；奥罗宾多道场史料(第二手史)(T2)",
    "l_ramana": "《Talks with Sri Ramana Maharshi》〔弟子笔录于阿鲁那佳拉山〕(T1)",
    "l_yoga": "当代瑜伽行道场资料(〔存疑〕当代自述) ",
}


def main():
    con = sqlite3.connect(DB)
    cur = con.cursor()
    done = skip = 0
    for lid, src in LOCATIONS.items():
        if not cur.execute("SELECT 1 FROM locations WHERE source_id=?", (lid,)).fetchone():
            skip += 1
            print("  skip location:", lid)
            continue
        cur.execute("UPDATE locations SET source=? WHERE source_id=?", (src, lid))
        done += 1
    con.commit()
    print("Done: locations=%d skip=%d" % (done, skip))
    con.close()


if __name__ == "__main__":
    main()