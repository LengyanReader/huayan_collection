#!/usr/bin/env python3
"""Audit _classifyPerson logic against all persons (graph + trajectory)."""
import sys, json, yaml, re
sys.stdout.reconfigure(encoding='utf-8')

with open('web/demo/graph.json', encoding='utf-8') as f:
    g = json.load(f)
nodeMap = {n['id']: n for n in g['nodes']}

with open('data/events/person_trajectories.yaml', encoding='utf-8') as f:
    traj = yaml.safe_load(f)

def classify(p_li, p_tp, p_n, traj_name, traj_group):
    li = p_li or ''; tp = p_tp or ''; n = p_n or ''; tname = traj_name or ''
    if traj_group: return traj_group
    # Huayan
    if li in ('华严宗','华严五祖','华严宗远祖'): return '华严宗·五祖时代'
    if li == '李通玄系': return '华严宗·李通玄系'
    if li in ('贤首宗高原法系','智光系'): return '华严宗·高原法系'
    if li == '华严莲社': return '华严宗·华严莲社'
    if li == '月霞系': return '华严宗·月霞系'
    if li == '慈舟系': return '华严宗·慈舟系'
    if li == '日本华严': return '华严宗·日本'
    if li == '高丽华严': return '华严宗·朝鲜半岛'
    if '华严' in li: return '华严宗'
    # Chan branches
    if li == '临济宗': return '禅宗·临济宗'
    if li == '曹洞宗': return '禅宗·曹洞宗'
    if li == '云门宗': return '禅宗·云门宗'
    if li == '法眼宗': return '禅宗·法眼宗'
    if li == '沩仰宗': return '禅宗·沩仰宗'
    if li == '黄龙派': return '禅宗·黄龙派'
    if li == '杨岐派': return '禅宗·杨岐派'
    # Other schools from li
    if li == '天台宗': return '天台宗'
    if li == '净土宗': return '净土宗'
    if li in ('法相宗','唯识宗'): return '法相宗·唯识'
    if li == '三论宗': return '三论宗'
    if li in ('律宗','南山律宗'): return '律宗'
    if li in ('密宗','唐密'): return '密宗·唐密'
    if li == '译师': return '译师'
    if li == '求法僧': return '求法僧'
    # Tibetan
    if li in ('藏传佛教·格鲁派','格鲁派'): return '藏传·格鲁派'
    if li in ('藏传佛教·萨迦派','萨迦派'): return '藏传·萨迦派'
    if li in ('藏传佛教·宁玛派','宁玛派'): return '藏传·宁玛派'
    if li in ('藏传佛教·噶举派','噶举派'): return '藏传·噶举派'
    if li == '藏传佛教' or '藏传' in li: return '藏传佛教'
    # India
    if li in ('印度源流','大乘瑜伽行法'): return '印度佛教·瑜伽行'
    # Theravada
    if li in ('上座部','南传佛教'): return '南传佛教'
    # Scholar / reference
    if li == '当代学者': return '近现代学者'
    if li == '参考线': return '近现代高僧大德'
    # Philosophy/religion from li
    if li == '儒家' or '儒家' in li: return '儒家'
    if li in ('道家','道教') or '道家' in li: return '道家·道教'
    if li in ('西方哲学','西方'): return '西方哲学·宗教'
    if li == '伊斯兰教' or '伊斯兰' in li: return '伊斯兰教'
    if li in ('印度教','耆那教'): return '印度教·耆那教'
    # Japan
    if li == '日本天台宗': return '日本·天台宗'
    if li == '日本真言宗': return '日本·真言宗'
    if li in ('日本禅宗','日本临济宗','日本曹洞宗'): return '日本·禅宗'
    if li in ('日本净土宗','日本净土真宗'): return '日本·净土宗'
    if li == '日本日莲宗': return '日本·日莲宗'
    # Korea
    if li in ('朝鲜佛教','韩国佛教'): return '朝鲜佛教'

    # === NAME PATTERNS (trajectory-only persons) ===
    full = n + tname

    # Scholars FIRST (before Chan/NZ patterns that might false-match)
    if re.search(r'胡适|梁启超|欧阳竟无|吕澂|汤用彤|魏道儒|王颂|邱高兴|张文良', full):
        return '近现代学者'
    # Ancient eminent monks (specific names)
    if re.search(r'安世高|道安|道生|僧祐|永明延寿|大慧宗杲|憨山德清|蕅益智旭|僧肇', full):
        return '汉传高僧'
    # Modern eminent monks
    if re.search(r'虚云|太虚|印光法师|弘一|印顺|梦参|圆瑛|谛闲|倓虚', full):
        return '近现代高僧大德'
    # Pure Land
    if re.search(r'慧远|善导|印光|莲池|昙鸾|道绰|省庵', full):
        return '净土宗'
    # Tiantai
    if re.search(r'智顗|湛然|知礼', full):
        return '天台宗'
    # Faxiang
    if re.search(r'窥基|圆测|世亲', full):
        return '法相宗·唯识'
    # Sanlun
    if re.search(r'吉藏', full):
        return '三论宗'
    # Vinaya
    if re.search(r'道宣|鉴真|元照', full):
        return '律宗'
    # Esoteric
    if re.search(r'善无畏|金刚智|不空|一行|慧果', full):
        return '密宗·唐密'
    # Chan — specific masters, NOT generic 禅 character
    if re.search(r'慧能|弘忍|神秀|达摩|马祖道一|百丈怀海|黄檗希运|沩山灵祐|石头希迁|赵州从谂|雪峰义存|洞山良价|临济义玄|云门文偃|法眼文益|曹山本寂', full):
        return '禅宗'
    # Tibetan
    if re.search(r'宗喀巴|阿底峡|莲花生|米拉日巴|八思巴|寂天', full):
        return '藏传佛教'
    # India
    if re.search(r'马鸣|龙树|无著|拉克鲁希|巴布基|普拉梵|克利普|胜师子', full):
        return '印度佛教'
    # Japan
    if re.search(r'空海|最澄|道元|荣西|日莲|亲鸾|法然|良弁|明惠|凝然', full):
        return '日本佛教'
    # Hindu
    if re.search(r'罗摩克里希纳|辨喜|奥罗宾多|拉玛那', full):
        return '印度教·近代'
    # Confucian
    if re.search(r'孔子|孟子|荀子|董仲舒|朱熹|王守仁|陆九渊|程颢|程颐|周敦颐|张载|邵雍|韩愈|柳宗元|欧阳修|苏轼|王安石|苏洵|苏辙|曾巩|颜回|子思|司马迁|班昭|郑玄|顾炎武|黄宗羲|王夫之', full):
        return '儒家'
    # Daoist
    if re.search(r'老子|庄子|列子|张道陵|王重阳|关尹子|葛洪|寇谦之|吕洞宾|陈抟|丘处机|张三丰|陶弘景|司马承祯|白玉蟾|张伯端', full):
        return '道家·道教'
    # Western
    if re.search(r'耶稣|柏拉图|亚里士多德|奥古斯丁|阿奎那|康德|黑格尔|穆罕默德', full):
        return '西方哲学·宗教'
    # Islamic
    if re.search(r'鲁米|伊本|安萨里|花拉子密', full):
        return '伊斯兰教'
    # Translators
    if re.search(r'胜友|智军|佛驮跋陀罗|实叉难陀|支娄迦谶|般若|鸠摩罗什|真谛|求那跋陀罗|竺法护', full):
        return '译师'
    # Pilgrims
    if re.search(r'法显|义净|玄奘|慧超', full):
        return '求法僧'
    # Practitioners
    if re.search(r'雪窦重显|赵州|百丈|黄檗|石头|雪峰|沩山|洞山|曹山', full):
        return '禅宗'

    # Type fallbacks (LAST resort)
    if tp == 'translator': return '译师'
    if tp == 'scholar': return '近现代学者'
    return '其他'

# Audit
print('=== POTENTIAL MISCLASSIFICATIONS ===')
issues = 0
# Check graph persons
for n in g['nodes']:
    li = n.get('li','') or ''
    tp = n.get('tp','') or ''
    tid = n['id']
    tname = ''
    tgrp = ''
    if tid in traj and isinstance(traj[tid], dict):
        tname = traj[tid].get('name','')
        tgrp = traj[tid].get('group','')
    cls = classify(li, tp, n['n'], tname, tgrp)
    if cls == '其他':
        print('  UNCLASSIFIED graph: '+tid+' '+n['n']+' li='+li+' tp='+tp)
        issues += 1

# Check trajectory-only persons
seen = {n['id'] for n in g['nodes']}
for tid, t in sorted(traj.items()):
    if not tid.startswith('person_'): continue
    if tid in seen: continue
    if not isinstance(t, dict) or not t.get('route'): continue
    name = t.get('name','?')
    n = name.split('·')[0] if '·' in name else name
    grp = t.get('group','')
    cls = classify('', '', n, name, grp)
    flag = ''
    # Detect: scholar misclassified as Chan
    if cls in ('禅宗','禅宗·临济宗','禅宗·曹洞宗') and re.search(r'禅宗史|佛学|学者|研究|著者|教授', name):
        flag = 'SCHOLAR→禅宗'
    # Detect: unclassified
    if cls == '其他' and name not in ('','?'):
        flag = 'UNCLASSIFIED'
    if flag:
        print(f'  {flag}: {tid} {name} → {cls}')
        issues += 1

print(f'\nTotal issues: {issues}')
if issues == 0:
    print('All classifications look correct!')
