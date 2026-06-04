import os

root = r'C:\content-sites\dogeking.us'
other_files = ['about.html', 'contact.html', 'privacy.html', 'whitepaper.html', 
               'why-dogeking.html', 'thank-you.html', 'sales-thank-you.html',
               'index.html', 'deployed-index.html']

files_fixed = 0
for fname in other_files:
    fpath = os.path.join(root, fname)
    if not os.path.exists(fpath):
        continue
    with open(fpath, 'r', encoding='utf-8', errors='replace') as fh:
        content = fh.read()
    
    original = content
    
    # Fix 'Doge King' to 'DogeKing' in various contexts
    replacements = [
        ('Doge King is', 'DogeKing is'),
        ('Doge King -', 'DogeKing -'),
        ('Doge King |', 'DogeKing |'),
        ('>Doge King<', '>DogeKing<'),
        ('Contact Doge King', 'Contact DogeKing'),
        ('rely on Doge King', 'rely on DogeKing'),
        ('<title>About Doge King', '<title>About DogeKing'),
        ('<title>Contact Us - Doge King</title>', '<title>Contact Us - DogeKing</title>'),
        ('Powered by <a href="https://dogeking0.gumroad.com">Doge King', 
         'Powered by <a href="https://dogeking0.gumroad.com">DogeKing'),
    ]
    
    for old, new in replacements:
        content = content.replace(old, new)
    
    # Handle quotes dynamically
    content = content.replace('"Doge King"', '"DogeKing"')
    content = content.replace("'Doge King'", "'DogeKing'")
    content = content.replace('name="Doge King"', 'name="DogeKing"')
    content = content.replace('"name":"Doge King"', '"name":"DogeKing"')
    content = content.replace('<a href="/">Doge King</a>', '<a href="/">DogeKing</a>')
    
    if content != original:
        with open(fpath, 'w', encoding='utf-8', errors='replace') as fh:
            fh.write(content)
        files_fixed += 1
        print(f'Fixed: {fname}')

print(f'Total other files fixed: {files_fixed}')
