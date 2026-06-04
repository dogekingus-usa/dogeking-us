import os
import glob

root = r'C:\content-sites\dogeking.us'
files_fixed = 0

# Fix article and blog HTML files
for pattern in ['articles/*.html', 'blog/*.html', 'short/*.html']:
    for f in glob.glob(os.path.join(root, pattern)):
        with open(f, 'r', encoding='utf-8', errors='replace') as fh:
            content = fh.read()
        
        original = content
        
        # Title tags
        content = content.replace('| Doge King', '| DogeKing')
        content = content.replace('\u2014 Doge King', '\u2014 DogeKing')
        content = content.replace('- Doge King', '- DogeKing')
        
        # Meta content
        content = content.replace('name="Doge King"', 'name="DogeKing"')
        content = content.replace('"name":"Doge King"', '"name":"DogeKing"')
        
        # Footer
        content = content.replace('2026 Doge King', '2026 DogeKing')
        content = content.replace('\u00a9 2026 Doge King', '\u00a9 2026 DogeKing')
        
        # Nav items with closing anchor tag
        content = content.replace('Doge King</a>', 'DogeKing</a>')
        
        # In description meta tags
        content = content.replace('Doge King crypto', 'DogeKing crypto')
        content = content.replace('Doge King guides', 'DogeKing guides')
        content = content.replace('Doge King tutorials', 'DogeKing tutorials')
        
        # Author in schema
        content = content.replace('"name":"Doge King"', '"name":"DogeKing"')
        
        if content != original:
            with open(f, 'w', encoding='utf-8', errors='replace') as fh:
                fh.write(content)
            files_fixed += 1
            print(f'Fixed: {os.path.basename(f)}')

print(f'Total files fixed: {files_fixed}')
