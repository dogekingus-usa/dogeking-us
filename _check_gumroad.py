import re
with open('index.html','r',encoding='utf-8') as f:
    html = f.read()
for m in re.finditer(r'gumroad\.com[^\s"\'<>]+', html):
    print(m.group())
