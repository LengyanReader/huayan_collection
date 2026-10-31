with open('web/demo/articles/index.html','r',encoding='utf-8') as f:
    c=f.read()
entry = '<div style=\"display:flex;flex-direction:column;gap:6px;background:var(--card);border:1px solid var(--line);border-left:4px solid var(--gold);border-radius:10px;padding:14px 16px\"><div><a href=\"huayan-sidi-pin.html\" style=\"color:var(--gold);font-weight:700;font-size:1.02em;text-decoration:none\">📖 九九华严第八品 四圣谛品之拼读 ↗</a></div><div style=\"font-size:0.75em;color:var(--text2)\">华严经第八品·第二会·差别因果周·卷十二末·十方十世界说四圣谛·四谛各十名共四百名·随众生心乐而异名·与六十对读</div><div style=\"font-size:0.72em;color:var(--text3,var(--text2))\">全文 19,903 字 · <code>华严经细读_第八部_四圣谛品.md</code></div><div style=\"display:flex;gap:14px;font-size:0.75em\"><a href=\"../tabs/gap.html\" style=\"color:var(--blue);text-decoration:none\">栏目: 文献页 · 华严经学</a> <a href=\"../tabs/gap.html\" style=\"color:var(--text2);font-size:0.78em\">返回 文献页 · 华严经学</a></div></div>'
idx = c.find('经论茶歇')
if idx >= 0:
    end = c.find('</section>', idx)
    section = c[idx:end]
    r_idx = section.find('rulai-minghao.html')
    if r_idx >= 0:
        card_end = section.find('</div></div>', r_idx)
        if card_end >= 0:
            insert = card_end + len('</div></div>')
            new_section = section[:insert] + entry + section[insert:]
            c = c[:idx] + new_section + c[end:]
            with open('web/demo/articles/index.html','w',encoding='utf-8') as f:
                f.write(c)
            print('ok')
        else:
            print('no')
    else:
        print('no2')
else:
    print('no3')
