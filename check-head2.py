import subprocess
cwd = r"C:\Users\SAMPC\.openclaw\workspace-website-architect\dogeking-us-clone"
d = subprocess.run(["git","show","HEAD:index.html"], capture_output=True, cwd=cwd).stdout.decode("utf-8", errors="replace")
print("HEAD length:", len(d))
print("Has token:", 'id="token"' in d)
print("Has products:", 'id="products"' in d)
print("Has ecosystem:", 'id="ecosystem"' in d)
print("Has dashboard:", 'id="dashboard"' in d)
print("Has blog:", 'id="blog"' in d)
print("Has community:", 'id="community"' in d)
print("Has wallet:", 'connect-wallet' in d)
print("Has floating:", 'hero-icon floating' in d)
print("Has ticker:", 'meme-ticker' in d)
print("Has style:", '<style>' in d and '</style>' in d)
