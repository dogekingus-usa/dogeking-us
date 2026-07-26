import os

cwd = r"C:\Users\SAMPC\.openclaw\workspace-website-architect\dogeking-us-clone"
path = os.path.join(cwd, "live-html.html")

with open(path, 'rb') as f:
    data = f.read()

text = data.decode('utf-8', errors='replace')

print(f"Size: {len(data)} bytes")
checks = [
    "connect-wallet", "wallet-modal", 'id="token"',
    'id="dashboard"', 'id="ecosystem"', 'id="products"',
    'id="blog"', 'id="community"',
    '<style>', '@keyframes float', '@keyframes shimmer',
    'pulse-glow', 'meme-ticker', 'class="theme-dogeking"',
    'href="crown-design-system.css'
]
for c in checks:
    print(f"  {c}: {c in text}")

# Check character integrity
print("\nCharacter check:")
bad = ['\u0393', '\u00c7', '\u00f6']  # ΓÇö corrupted chars
for b in bad:
    if b in text:
        print(f"  BAD: char U+{ord(b):04X} ({b}) found!")
    else:
        print(f"  OK: char U+{ord(b):04X} not found")
