import subprocess
import re
import os

cwd = r"C:\Users\SAMPC\.openclaw\workspace-website-architect\dogeking-us-clone"
output_path = os.path.join(cwd, "index.html")

# Get the ORIGINAL first-commit style block (clean)
orig = subprocess.run(
    ['git', 'show', 'e77a35e:index.html'],
    capture_output=True, cwd=cwd
).stdout

orig_str = orig.decode('utf-8')
style_start = orig_str.index('<style>')
style_end = orig_str.index('</style>') + 8
orig_style_block = orig_str[style_start:style_end]
print(f"Original style block: {len(orig_style_block)} chars")

# Get the CURRENT index.html from git HEAD
# (this has all features: token, dashboard, ecosystem, wallet, etc.)
current = subprocess.run(
    ['git', 'show', 'HEAD:index.html'],
    capture_output=True, cwd=cwd
).stdout
current_str = current.decode('utf-8')
print(f"Current HTML: {len(current_str)} chars")

# Check current for existing style block
has_style = '<style>' in current_str and '</style>' in current_str
print(f"Current has <style>: {has_style}")

# Insert the original style block into current
if has_style:
    old_s = current_str.index('<style>')
    old_e = current_str.index('</style>') + 8
    new_html = current_str[:old_s] + orig_style_block + current_str[old_e:]
    print("Replaced existing style block")
else:
    new_html = current_str.replace('</head>', f'{orig_style_block}\n</head>')
    print("Inserted style block before </head>")

# Also ensure html tag has theme class
if 'class="theme-dogeking"' not in new_html:
    new_html = new_html.replace('<html lang="en">', '<html class="theme-dogeking" lang="en">')
    print("Added theme class to html tag")

# Also add a { color: var(--accent); } if missing from external CSS
# The original style already has this in the inline block

# Write with proper UTF-8 (no BOM, no PowerShell corruption)
with open(output_path, 'wb') as f:
    f.write(new_html.encode('utf-8'))

# Verify written file
with open(output_path, 'rb') as f:
    verify = f.read()

print(f"\nWritten: {len(verify)} bytes to index.html")

# Check character integrity
checks = [
    (b'\xe2\x80\x94', 'Em-dash'),
    (b'\xc2\xa9', 'Copyright'),
    (b'\xf0\x9f\x91\x91', 'Crown emoji 👑'),
    (b'\xe2\x9c\x88', 'Airplane emoji ✈'),
    (b'\xf0\x9f\x92\xac', 'Speech bubble 💬'),
]
for pattern, name in checks:
    if pattern in verify:
        print(f"  ✅ {name}: present")
    else:
        print(f"  ❌ {name}: MISSING")

# Check NO corruption
corruption_patterns = [
    (b'\xce\x93\xc3\x87', 'ΓÇ (mojibake)'),
    (b'\xc3\x82\xc2\xa9', 'Â© (mojibake)'),
]
for pattern, name in corruption_patterns:
    if pattern in verify:
        print(f"  ❌ {name}: PRESENT!")
    else:
        print(f"  ✅ {name}: absent")

# Check key features
features = [
    (b'@keyframes float', 'float animation'),
    (b'@keyframes shimmer', 'shimmer animation'),
    (b'@keyframes pulse-glow', 'pulse-glow animation'),
    (b'shimmer 3s', 'shimmer on h1'),
    (b'class="hero-icon floating"', 'floating crown'),
    (b'meme-ticker', 'meme ticker'),
    (b'pulse-glow', 'pulse-glow element'),
    (b'id="token"', 'token section'),
    (b'id="products"', 'products section'),
    (b'id="dashboard"', 'dashboard section'),
    (b'id="ecosystem"', 'ecosystem section'),
    (b'connect-wallet', 'wallet connect'),
    (b'class="theme-dogeking"', 'theme class'),
]
print()
for pattern, name in features:
    if pattern in verify:
        print(f"  ✅ {name}")
    else:
        print(f"  ❌ {name}")

print(f"\nOpen http://localhost:8889/ in your browser!")
