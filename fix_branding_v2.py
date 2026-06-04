import os
import glob

root = r'C:\content-sites\dogeking.us'
files_fixed = 0
total_count = 0

# Process ALL html files in the site
for pattern in ['*.html', 'articles/*.html', 'blog/*.html', 'short/*.html']:
    for f in glob.glob(os.path.join(root, pattern)):
        # Skip the sales-cta-overlay (shared template) and index-fixed/deployed backups
        basename = os.path.basename(f)
        if basename in ('sales-cta-overlay.html', 'index-fixed.html', 'deployed-index.html'):
            continue
            
        with open(f, 'r', encoding='utf-8', errors='replace') as fh:
            content = fh.read()
        
        original = content
        count = content.count('Doge King')
        
        if count == 0:
            continue
            
        # Strategic replacements for brand name
        content = content.replace('Doge King</a>', 'DogeKing</a>')
        content = content.replace('Doge King</title>', 'DogeKing</title>')
        content = content.replace('Doge King |', 'DogeKing |')
        content = content.replace('Doge King -', 'DogeKing -')
        content = content.replace('Doge King,', 'DogeKing,')
        content = content.replace('Doge King.', 'DogeKing.')
        content = content.replace('Doge King!', 'DogeKing!')
        content = content.replace('Doge King:', 'DogeKing:')
        content = content.replace('Doge King;', 'DogeKing;')
        content = content.replace('Doge King?', 'DogeKing?')
        content = content.replace('Dogeking', 'DogeKing')  # normalize capitalization
        content = content.replace('doge king', 'DogeKing')
        
        # Fix specific patterns
        content = content.replace('"Doge King"', '"DogeKing"')
        content = content.replace("'Doge King'", "'DogeKing'")
        content = content.replace('name="Doge King"', 'name="DogeKing"')
        content = content.replace('"name":"Doge King"', '"name":"DogeKing"')
        content = content.replace('content="Doge King', 'content="DogeKing')
        
        # Meta tag patterns
        content = content.replace('name="Doge King"', 'name="DogeKing"')
        content = content.replace("name='Doge King'", "name='DogeKing'")
        
        new_count = content.count('Doge King')
        
        if content != original:
            with open(f, 'w', encoding='utf-8', errors='replace') as fh:
                fh.write(content)
            files_fixed += 1
            total_count += (count - new_count)
            print(f'Fixed: {basename} ({count - new_count} replacements)')

print(f'\nTotal files fixed: {files_fixed}')
print(f'Total replacements: {total_count}')
