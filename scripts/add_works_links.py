#!/usr/bin/env python3
"""Add CBETA/external links to Huayan patriarchs' key works in personas.json"""
import json, sys, io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

WORKS_LINKS = {
    # 杜顺 (557-640)
    '华严法界观门': 'https://cbeta.buddhism.org.hk/xml/T45/T45n1884_001.xml',
    '华严五教止观': 'https://cbeta.buddhism.org.hk/xml/T45/T45n1867_001.xml',
    # 智俨 (602-668)
    '华严经搜玄记': 'https://cbeta.buddhism.org.hk/xml/T35/T35n1732_001.xml',
    '华严一乘十玄门': 'https://cbeta.buddhism.org.hk/xml/T45/T45n1868_001.xml',
    '华严五十要问答': 'https://cbeta.buddhism.org.hk/xml/T45/T45n1869_001.xml',
    # 法藏 (643-712)
    '华严一乘教义分齐章（五教章）': 'https://cbeta.buddhism.org.hk/xml/T45/T45n1866_001.xml',
    '华严经探玄记': 'https://cbeta.buddhism.org.hk/xml/T35/T35n1733_001.xml',
    '华严经义海百门': 'https://cbeta.buddhism.org.hk/xml/T45/T45n1875_001.xml',
    '华严金师子章': 'https://cbeta.buddhism.org.hk/xml/T45/T45n1880_001.xml',
    '大乘起信论义记': 'https://cbeta.buddhism.org.hk/xml/T44/T44n1846_001.xml',
    '十二门论宗致义记': 'https://cbeta.buddhism.org.hk/xml/T42/T42n1826_001.xml',
    # 澄观 (738-839)
    '华严经疏（华严大疏）': 'https://cbeta.buddhism.org.hk/xml/T35/T35n1735_001.xml',
    '华严经随疏演义钞': 'https://cbeta.buddhism.org.hk/xml/T36/T36n1736_001.xml',
    '华严法界玄镜': 'https://cbeta.buddhism.org.hk/xml/T45/T45n1883_001.xml',
    '三圣圆融观门': 'https://cbeta.buddhism.org.hk/xml/T45/T45n1882_001.xml',
    # 宗密 (780-841)
    '注华严法界观门': 'https://cbeta.buddhism.org.hk/xml/T45/T45n1884_001.xml',
    '禅源诸诠集都序': 'https://cbeta.buddhism.org.hk/xml/T48/T48n2015_001.xml',
    '圆觉经大疏释义钞': 'https://cbeta.buddhism.org.hk/xml/X09/X09n0245_001.xml',
    '华严原人论': 'https://cbeta.buddhism.org.hk/xml/T45/T45n1886_001.xml',
    '华严经行愿品疏钞': 'https://cbeta.buddhism.org.hk/xml/X05/X05n0229_001.xml',
    # 李通玄 (635-730)
    '新华严经论': 'https://cbeta.buddhism.org.hk/xml/T36/T36n1739_001.xml',
    '华严经决疑论': 'https://cbeta.buddhism.org.hk/xml/T36/T36n1741_001.xml',
    # 续法 (1641-1728)
    '贤首五教仪': 'https://cbeta.buddhism.org.hk/xml/X58/X58n1024_001.xml',
    '华严宗佛祖传': 'https://cbeta.buddhism.org.hk/xml/X77/X77n1530_001.xml',
}

def main():
    path = 'c:/DA_Practice/huayan_collection/data/knowledge_graph/personas.json'
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    updated = 0
    for p in data['persons']:
        wk = p.get('key_works', [])
        if not wk:
            continue
        links = {}
        for w in wk:
            if w in WORKS_LINKS:
                links[w] = WORKS_LINKS[w]
        if links:
            p['works_links'] = links
            updated += 1
            print(f"  {p['name_zh']}: {len(links)} links added")

    data['last_updated'] = '2026-08-02'
    data['note'] = '扩充版 + CBETA工作链接。覆盖华严五祖→义天高丽→明清中兴→近现代→当代完整传承链，共80+人物。'

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\nUpdated {updated} persons with CBETA links. Total persons: {len(data['persons'])}")

if __name__ == '__main__':
    main()
