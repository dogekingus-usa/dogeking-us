import subprocess, os, re

cwd = r"C:\Users\SAMPC\.openclaw\workspace-website-architect\dogeking-us-clone"

# Get current HEAD HTML (has all features)
current = subprocess.run(["git", "show", "HEAD:index.html"], capture_output=True, cwd=cwd).stdout.decode("utf-8")

# Get original first-commit HTML (has original design)
orig = subprocess.run(["git", "show", "e77a35e:index.html"], capture_output=True, cwd=cwd).stdout.decode("utf-8")

# Step 1: Get the original inline style (with all animations)
s = orig.index("<style>")
e = orig.index("</style>") + 8
orig_style = orig[s:e]

# Step 2: Replace style in current with original style
cs = current.index("<style>")
ce = current.index("</style>") + 8
current = current[:cs] + orig_style + current[ce:]

# Step 3: Add original hero elements into the current hero section
# Current hero currently has: badge, SVG crown, h1, p, CTAs
# Need to add: floating crown emoji, ticker, featured product

# Find the hero section
hero_match = re.search(r'<section class="hero">.*?</section>', current, re.DOTALL)
if hero_match:
    hero = hero_match.group(0)
    print(f"Found hero section: {len(hero)} chars")
    
    # Insert floating crown after badge
    hero = hero.replace(
        '<div class="hero-badge">',
        '<div class="hero-icon floating">👑</div>\n<div class="hero-badge">'
    )
    
    # Add shimmer gradient to h1 (already has it from inline style)
    
    # Add ticker after the CTA divs (before closing </section>)
    ticker_html = '''\n  <div class="meme-ticker">
    <div class="meme-ticker-inner">
      <span class="ticker-item">🐕 DOGE <span class="up">+12.4%</span></span>
      <span class="ticker-item">👑 DKING <span class="up">+8.2%</span></span>
      <span class="ticker-item">🐱 PEPE <span class="up">+5.7%</span></span>
      <span class="ticker-item">🟢 BONK <span class="up">+15.1%</span></span>
      <span class="ticker-item">🪙 WIF <span class="up">+3.2%</span></span>
      <span class="ticker-item">🚀 SOL <span class="up">+2.8%</span></span>
      <span class="ticker-item">🐕 DOGE <span class="up">+12.4%</span></span>
      <span class="ticker-item">👑 DKING <span class="up">+8.2%</span></span>
      <span class="ticker-item">🐱 PEPE <span class="up">+5.7%</span></span>
      <span class="ticker-item">🟢 BONK <span class="up">+15.1%</span></span>
      <span class="ticker-item">🪙 WIF <span class="up">+3.2%</span></span>
      <span class="ticker-item">🚀 SOL <span class="up">+2.8%</span></span>
    </div>
  </div>'''
    
    hero = hero.replace("</section>", f"{ticker_html}\n</section>")
    
    # Replace hero in current
    current = current[:hero_match.start()] + hero + current[hero_match.end():]
    print("Added floating crown + ticker to hero")

# Step 4: Add featured product before the hero or after CTAs
# Find where CTAs end
cta_match = re.search(r'<a href="https://dogeking0\.gumroad\.com/.*?</a>', current)
if cta_match:
    # Add featured product after last CTA
    featured_html = '''\n  <div class="featured-product pulse-glow">
    <h3>🐕 DogeKing Crypto Bundle</h3>
    <p>The ultimate toolkit for meme coin traders — guides, checklists, wallet setups, and insider strategies.</p>
    <div class="price">$29</div>
    <a href="https://dogeking0.gumroad.com/l/dogeking-crypto-bundle" class="cta-button">Get the Bundle →</a>
  </div>'''
    
    pos = cta_match.end()
    current = current[:pos] + featured_html + current[pos:]
    print("Added featured product")

# Step 5: Add stats section before the first new section (token)
token_match = re.search(r'<section[^>]*id="token"', current)
if token_match:
    # Add stats before token section
    stats_html = '''<section class="section">
  <div class="container">
    <div class="stats">
      <div class="stat-card"><div class="stat-number">397+</div><div class="stat-label">Articles & Guides</div></div>
      <div class="stat-card"><div class="stat-number">2</div><div class="stat-label">Topic Categories</div></div>
      <div class="stat-card"><div class="stat-number">100%</div><div class="stat-label">Free Content</div></div>
      <div class="stat-card"><div class="stat-number">397+</div><div class="stat-label">Up-to-Date Guides</div></div>
    </div>
  </div>
</section>'''
    pos = token_match.start() - 1
    # Find the previous </section> to insert after
    prev_section_end = current.rfind("</section>", 0, pos)
    if prev_section_end >= 0:
        current = current[:prev_section_end + 10] + "\n\n" + stats_html + "\n\n" + current[prev_section_end + 10:]
        print("Added stats section")

# Step 6: Ensure html has theme class
if 'class="theme-dogeking"' not in current:
    current = current.replace('<html lang=', '<html class="theme-dogeking" lang=')

# Write
with open(os.path.join(cwd, "index.html"), "wb") as f:
    f.write(current.encode("utf-8"))

print(f"\nWritten: {len(current)} bytes")
print(f"Floating: {'hero-icon floating' in current}")
print(f"Ticker: {'meme-ticker' in current}")
print(f"Featured: {'pulse-glow' in current}")
print(f"Stats: {'class=\"stats\"' in current}")
print(f"All features preserved: token={chr(0x2705) if 'id=\"token\"' in current else chr(0x274C)} product={chr(0x2705) if 'id=\"products\"' in current else chr(0x274C)} eco={chr(0x2705) if 'id=\"ecosystem\"' in current else chr(0x274C)} dash={chr(0x2705) if 'id=\"dashboard\"' in current else chr(0x274C)}")
