import subprocess

cwd = r"C:\Users\SAMPC\.openclaw\workspace-website-architect\dogeking-us-clone"
data = subprocess.run(['git', 'show', 'HEAD:index.html'], capture_output=True, cwd=cwd).stdout

print(f"Size: {len(data)} bytes")
print(f"Has connect-wallet: {'connect-wallet' in data.decode('utf-8')}")
print(f"Has token section: {'id=\"token\"' in data.decode('utf-8')}")
print(f"Has dashboard: {'id=\"dashboard\"' in data.decode('utf-8')}")
print(f"Has ecosystem: {'id=\"ecosystem\"' in data.decode('utf-8')}")
print(f"Has wallet-modal: {'wallet-modal' in data.decode('utf-8')}")
print(f"Has meme-ticker: {'meme-ticker' in data.decode('utf-8')}")
print(f"Has pulse-glow: {'pulse-glow' in data.decode('utf-8')}")
