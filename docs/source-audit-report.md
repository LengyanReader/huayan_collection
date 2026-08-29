# 信息来源可靠性审计报告

> 生成时间：2026-08-29T10:32 · 数据源：SQLite `data/catalog/huayan.db` · 由 `scripts/verify_sources.py` 自动产出，
> 结论仅供人工核校参考；T0/T3 项即需补充第一手来源或标注存疑。

## 总览

| 对象 | 总数 | 缺来源 | 占比 | 备注 |
|------|------|--------|------|------|
| persons | 95 | 37 | 38.9% | 评分 43/100 |
| lineage_edges | 98 | 55 | 56.1% | — |
| docs   | 31 | 无存疑标注 11 篇 | — | — |

## persons 需补来源（T0）

- [ ] `1086` 续法　（无来源）
- [ ] `1087` 慧光　（无来源）
- [ ] `1088` 子璿　（无来源）
- [ ] `1089` 持松　（无来源）
- [ ] `1090` 释迦牟尼　（无来源）
- [ ] `1091` 马鸣　（无来源）
- [ ] `1092` 无著　（无来源）
- [ ] `1093` 鸠摩罗什　（无来源）
- [ ] `1094` 菩提流支　（无来源）
- [ ] `1095` 燃灯佛　（无来源）
- [ ] `1096` 迦叶佛　（无来源）
- [ ] `1097` 毗卢遮那佛　（无来源）
- [ ] `1113` 拉克鲁希　（无来源）
- [ ] `1114` 巴布基　（无来源）
- [ ] `1115` 普拉梵纳德　（无来源）
- [ ] `1116` 克利普梵纳德　（无来源）
- [ ] `1117` 胜师子王菩萨　（无来源）
- [ ] `1118` 罗摩克里希纳　（无来源）
- [ ] `1119` 辨喜　（无来源）
- [ ] `1120` 奥罗宾多　（无来源）
- [ ] `1121` 拉玛那·马哈希　（无来源）
- [ ] `1122` 寂天　（无来源）
- [ ] `1123` 阿底峡　（无来源）
- [ ] `1124` 宗喀巴　（无来源）
- [ ] `1125` 思元慧三　（无来源）
- [ ] `1126` 体化性果　（无来源）
- [ ] `1128` 实忠　（无来源）
- [ ] `1129` 等定　（无来源）
- [ ] `1130` 圣宝　（无来源）
- [ ] `1131` 观贤　（无来源）
- [ ] `1134` 魏道儒　（无来源）
- [ ] `1135` 王颂　（无来源）
- [ ] `1136` 邱高兴　（无来源）
- [ ] `1137` 张文良　（无来源）
- [ ] `1138` 虚云　（无来源）
- [ ] `1139` 净慧　（无来源）
- [ ] `1140` 南怀瑾　（无来源）

## persons 模糊来源（T3，需细化到具体文献）

- [ ] `1047` 世亲　`学术研究`
- [ ] `1060` 月霞　`近现代佛教史料`
- [ ] `1061` 常惺　`近现代佛教史料`
- [ ] `1062` 慈舟　`近现代佛教史料`
- [ ] `1063` 南亭　`华严莲社社志/官网〔存疑：机构史料，含谱系自述〕`
- [ ] `1064` 成一　`华严莲社社志/官网〔存疑：机构史料，含谱系自述〕`
- [ ] `1065` 贤度　`华严莲社社志/官网〔存疑：机构史料，含谱系自述〕`
- [ ] `1066` 智光　`华严莲社资料`
- [ ] `1067` 梦参　`《梦参老和尚_综合深度研究》(docs/，信源分级+〔存疑〕标注)`
- [ ] `1068` 胜友　`德格版甘珠尔目录`
- [ ] `1069` 智军　`学术研究`
- [ ] `1071` 应慈　`近现代佛教史料`
- [ ] `1072` 了中　`华严莲社社志/官网〔存疑：机构史料，含谱系自述〕`
- [ ] `1073` 净海　`华严莲社社志/官网〔存疑：机构史料，含谱系自述〕`
- [ ] `1074` 明度　`华严莲社社志/官网〔存疑：机构史料，含谱系自述〕`
- [ ] `1075` 钦因　`大华严寺法脉资料`
- [ ] `1076` 海云继梦　`大华严寺法脉资料（2024年）〔存疑："三脉汇一"等谱系为教界自述，未见独立史料佐证〕`
- [ ] `1077` 体佛　`网络资料`
- [ ] `1078` 真禅　`当代佛教资料`
- [ ] `1079` 如孝　`凤凰网佛教（2024年）〔存疑：媒体转述，待一手史料〕`
- [ ] `1080` 雪窦　`华严莲社美国分会资料`
- [ ] `1112` 成观法师　`大毘卢寺官网·百度百科·钦因传法记录`

## lineage_edges 缺来源

- [ ] person_012 → person_013　(MASTER_OF)
- [ ] person_012 → person_031　(MASTER_OF)
- [ ] person_031 → person_044　(MASTER_OF)
- [ ] person_018 → person_015　(MASTER_OF)
- [ ] person_041 → person_043　(MASTER_OF)
- [ ] person_041 → person_126　(MASTER_OF)
- [ ] person_017 → person_045　(CONTEMPORARY)
- [ ] person_007b → person_006　(INFLUENCED)
- [ ] person_006 → person_007　(INFLUENCED)
- [ ] person_007 → person_008　(INFLUENCED)
- [ ] person_103 → person_007　(INFLUENCED)
- [ ] person_103 → person_006　(INFLUENCED)
- [ ] person_103 → person_110　(INFLUENCED)
- [ ] person_111 → person_102　(MASTER_OF)
- [ ] person_111 → person_112　(INFLUENCED)
- [ ] person_110 → person_006　(INFLUENCED)
- [ ] person_110 → person_111　(INFLUENCED)
- [ ] person_112 → person_003　(CONTEMPORARY)
- [ ] person_008 → person_112　(CONTEMPORARY)
- [ ] person_113 → person_104　(INFLUENCED)
- [ ] person_113 → person_114　(INFLUENCED)
- [ ] person_115 → person_003　(CONTEMPORARY)
- [ ] person_116 → person_006　(INFLUENCED)
- [ ] person_116 → person_007b　(INFLUENCED)
- [ ] person_117 → person_111　(INFLUENCED)
- [ ] person_117 → person_112　(INFLUENCED)
- [ ] person_007b → person_116　(INFLUENCED)
- [ ] person_120 → person_122　(MASTER_OF)
- [ ] person_121 → person_115　(MASTER_OF)
- [ ] person_120 → person_121　(CONTEMPORARY)
- [ ] person_115 → person_123　(MASTER_OF)
- [ ] person_115 → person_005　(CONTEMPORARY)
- [ ] person_122 → person_005　(CONTEMPORARY)
- [ ] person_f01 → person_041　(MASTER_OF)
- [ ] person_041 → person_f02　(MASTER_OF)
- [ ] person_j03 → person_j04　(INFLUENCED)
- [ ] person_090 → person_001　(INFLUENCED)
- [ ] person_091 → person_010　(INFLUENCED)
- [ ] person_012 → person_092　(MASTER_OF)
- [ ] person_101 → person_000a　(INFLUENCED)
- [ ] person_102 → person_000b　(MASTER_OF)
- [ ] person_005 → person_044　(INFLUENCED)
- [ ] person_090 → person_001　(INFLUENCED)
- [ ] person_101 → person_102　(INFLUENCED)
- [ ] person_105 → person_100　(INFLUENCED)
- [ ] person_106 → person_100　(INFLUENCED)
- [ ] person_130 → person_131　(MASTER_OF)
- [ ] person_131 → person_132　(MASTER_OF)
- [ ] person_132 → person_133　(MASTER_OF)
- [ ] person_133 → person_134　(MASTER_OF)
- [ ] person_140 → person_141　(MASTER_OF)
- [ ] person_x01 → person_x02　(MASTER_OF)
- [ ] person_x01 → person_s04　(INFLUENCED)
- [ ] person_x01 → person_x03　(INFLUENCED)
- [ ] person_x02 → person_x03　(CONTEMPORARY)

## locations 缺来源

- [ ] `l_changan_t` 长安逍遥园（temple）
- [ ] `l_changan_x` 长安大慈恩寺·弘福寺（temple）
- [ ] `l_ganden` 拉萨·甘丹寺（temple）
- [ ] `l_guangzhou` 广州（region）
- [ ] `l_kolkata` 加尔各答·罗摩克里希纳传道会（temple）
- [ ] `l_kucha` 龟兹（region）
- [ ] `l_nalanda` 那烂陀寺（temple）
- [ ] `l_nalanda2` 那烂陀寺(参考)（temple）
- [ ] `l_pondi` 印度本地治里·Aurobindo Ashram（temple）
- [ ] `l_ramana` 印度圣山 Arunachala (Tiruvannamalai)（mountain）
- [ ] `l_yoga` 印度阿弥塔巴·LIFE Mission道场（temple）

## docs 无存疑标注

- [ ] architecture.md　（全篇无「存疑/待考」标注，需复核是否存在不确定内容）
- [ ] engineering-workflow.md　（全篇无「存疑/待考」标注，需复核是否存在不确定内容）
- [ ] knowledge-management.md　（全篇无「存疑/待考」标注，需复核是否存在不确定内容）
- [ ] multilingual-alignment.md　（全篇无「存疑/待考」标注，需复核是否存在不确定内容）
- [ ] next-phase-plan.md　（全篇无「存疑/待考」标注，需复核是否存在不确定内容）
- [ ] reference-management.md　（全篇无「存疑/待考」标注，需复核是否存在不确定内容）
- [ ] scalable-text-architecture.md　（全篇无「存疑/待考」标注，需复核是否存在不确定内容）
- [ ] tech-stack.md　（全篇无「存疑/待考」标注，需复核是否存在不确定内容）
- [ ] verification-framework.md　（全篇无「存疑/待考」标注，需复核是否存在不确定内容）
- [ ] visualization-research.md　（全篇无「存疑/待考」标注，需复核是否存在不确定内容）
- [ ] 善财五十三参深度研究.md　（全篇无「存疑/待考」标注，需复核是否存在不确定内容）
