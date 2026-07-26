import subprocess
import re
import os

cwd = r"C:\Users\SAMPC\.openclaw\workspace-website-architect\dogeking-us-clone"
blob_hash = "e77a35e"
head_hash = "HEAD"

def git_show(ref, path="index.html"):
    result = subprocess.run(['git', 'show', f'{ref}:{path}'], capture_output=True, cwd=cwd)
    return result.stdout

# Get original clean HTML
orig = git_show(blob_hash)
print(f"Original: {len(orig)} bytes")

# Verify em-dash is clean
if b'\xe2\x80\x94' in orig:
    print("  Em-dash: CLEAN (UTF-8)")
else:
    print("  Em-dash: CORRUPTED")

# Get current HTML for new features
current = git_show("HEAD")
print(f"Current: {len(current)} bytes")

# Find sections in current
sections_html = b""
section_ids = ["token", "products", "blog", "community", "ecosystem", "dashboard"]

for sid in section_ids:
    # Match <section ... id="token" ...> ... </section>
    pattern = rf'<section[^>]*id="{re.escape(sid)}"[^>]*>.*?</section>'
    match = re.search(pattern, current.decode('utf-8'), re.DOTALL)
    if match:
        sections_html += match.group(0).encode('utf-8') + b"\n\n"
        print(f"  Extracted #{sid}: {len(match.group(0))} chars")
    else:
        print(f"  NOT FOUND: #{sid}")

# Get last section (affiliate)
all_sections = re.findall(r'<section[^>]*>.*?</section>', current.decode('utf-8'), re.DOTALL)
if all_sections:
    last = all_sections[-1]
    sections_html += last.encode('utf-8') + b"\n\n"
    print(f"  Extracted affiliate: {len(last)} chars")

# Build merged HTML
orig_str = orig.decode('utf-8')
footer_idx = orig_str.find("<footer")
before_footer = orig_str[:footer_idx].encode('utf-8')
footer_and_after = orig_str[footer_idx:].encode('utf-8')

merged = before_footer + b"\n\n" + sections_html + b"\n" + footer_and_after

# Update nav links
merged_str = merged.decode('utf-8')
old_links = '<a href="/">Home</a>\n<a href="/all-articles.html">Articles</a>\n<a href="/products.html">Products</a>\n<a href="/about.html">About</a>\n<a href="/contact.html">Contact</a>'
new_links = '<a href="/">Home</a>\n<a href="#token">$DKING</a>\n<a href="#products">Products</a>\n<a href="#blog">Blog</a>\n<a href="#community">Community</a>\n<a href="#ecosystem">Ecosystem</a>\n<a href="#dashboard">Dashboard</a>\n<a href="/products.html">Store</a>'
merged_str = merged_str.replace(old_links, new_links)

# Also add wallet buttons to nav
nav_end = merged_str.find('<button class="nav-toggle"')
if nav_end >= 0:
    wallet_html = """<div class="wallet-connected" style="display:none;align-items:center;gap:8px;">
  <span id="wallet-address" style="font-size:0.8rem;color:var(--text-muted);font-family:var(--font-mono);"></span>
</div>
<button class="connect-wallet-btn btn btn-primary" style="padding:8px 16px;font-size:0.85rem;">🔌 Connect Wallet</button>
"""
    merged_str = merged_str[:nav_end] + wallet_html + merged_str[nav_end:]

# Write with proper UTF-8
output_path = os.path.join(cwd, "index.html")
with open(output_path, 'wb') as f:
    f.write(merged_str.encode('utf-8'))

# Verify
with open(output_path, 'rb') as f:
    verify = f.read()

print(f"\nWritten: {len(verify)} bytes to index.html")

# Verify clean
if b'\xe2\x80\x94' in verify:
    print("  Em-dash: CLEAN")
else:
    print("  Em-dash: MISSING!")

if b'\xc2\xa9' in verify:
    print("  Copyright: CLEAN")
else:
    print("  Copyright: MISSING!")

# Check for corruption patterns
for pattern in [b'\xce\x93\xc3\x87', b'\xc3\x82\xc2\xa9', b'\xce\x93']:
    if pattern in verify:
        name = pattern.decode('latin-1')
        print(f"  CORRUPTION: '{name}' still present!")

print("\nOpen http://localhost:8889/ in your browser to preview!")
