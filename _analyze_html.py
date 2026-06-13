with open('index.html','r',encoding='utf-8') as f:
    html = f.read()

# Find where sections end
for sid in ['products', 'ecosystem', 'community', 'blog', 'dashboard', 'token']:
    start = html.find(f'id="{sid}"')
    end = html.find('</section>', start) + len('</section>') if start > 0 else -1
    if start > 0 and end > 0:
        print(f'=== {sid} === offset {start} to {end} (len={end-start})')

# Last section before footer
footer_start = html.find('<footer')
print(f'\nFooter starts at: {footer_start}')

# Show content between last section and footer
section_ends = []
for sid in ['products', 'ecosystem', 'community', 'blog', 'dashboard']:
    s = html.find(f'id="{sid}"')
    if s > 0:
        e = html.find('</section>', s) + len('</section>')
        section_ends.append(e)

last_section_end = max(section_ends)
print(f'\nLast section ends at: {last_section_end}')
print(f'Content between last section and footer:')
between = html[last_section_end:footer_start]
print(between[:2000].encode('ascii','replace').decode('ascii'))
print(f'\n...({len(between)} chars total)')

# Also show products section for payment integration
prod_start = html.find('id="products"')
prod_end = html.find('</section>', prod_start) + len('</section>')
print(f'\n=== PRODUCTS SECTION ({prod_start} to {prod_end}) ===')
print(html[prod_start:prod_start+2000].encode('ascii','replace').decode('ascii'))
