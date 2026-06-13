import re
with open('index.html','r',encoding='utf-8') as f:
    html = f.read()

sections = ['id="products"','id="ecosystem"','id="community"','id="blog"','id="token"','<footer','newsletter','donation']
for s in sections:
    i = html.find(s)
    if i>=0:
        snippet = html[i:i+120].encode('ascii','replace').decode('ascii')
        print(f'FOUND "{s}" at offset {i}: ...{snippet}...')
    else:
        print(f'NOT FOUND: "{s}"')

print('---')
print('HTML length:', len(html))

# Find the end of products section and area before footer
ecosystem_end = html.find('</section>', html.find('id="ecosystem"'))
print(f'\nEcosystem section ends near offset: {ecosystem_end}')
ctx = html[ecosystem_end:ecosystem_end+400].encode('ascii','replace').decode('ascii')
print(f'Context: {ctx}')
