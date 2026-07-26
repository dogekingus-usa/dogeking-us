import subprocess
import sys

blob_hash = "0447d50e8e344c019aa77c42c9322e2553e500b4"
cwd = r"C:\Users\SAMPC\.openclaw\workspace-website-architect\dogeking-us-clone"

result = subprocess.run(['git', 'cat-file', '-p', blob_hash], capture_output=True, cwd=cwd)

if result.returncode != 0:
    print(f"Error: {result.stderr.decode()}")
    sys.exit(1)

raw = result.stdout
print(f"Raw blob size: {len(raw)} bytes")

# Find 'DogeKing ' in the raw bytes
pos = raw.find(b'DogeKing ')
if pos >= 0:
    chunk = raw[pos+9:pos+15]
    print(f"Bytes after DogeKing: {chunk.hex()}")
    print(f"As latin-1: {chunk.decode('latin-1', errors='replace')}")
    print(f"As utf-8: {chunk.decode('utf-8', errors='replace')}")

# Look for UTF-8 multibyte sequences
# Em-dash is 0xE2 0x80 0x94 in UTF-8
for i in range(len(raw) - 2):
    if raw[i] == 0xE2 and raw[i+1] == 0x80 and raw[i+2] == 0x94:
        print(f"Found proper em-dash at byte {i} (UTF-8 0xE2 0x80 0x94) - CLEAN!")
        break
    if raw[i] == 0xCE and raw[i+1] == 0x93:
        context = raw[max(0,i-5):i+10]
        print(f"Found GAMMA (corruption!) at byte {i}: {context.hex()}")
        break

# Also check for copyright - UTF-8 0xC2 0xA9  
for i in range(len(raw) - 1):
    if raw[i] == 0xC2 and raw[i+1] == 0xA9:
        print(f"Found proper copyright (0xC2 0xA9) at byte {i}")
        break
    if raw[i] == 0xE2 and raw[i+1] == 0x89 and raw[i+2] == 0x88:
        print(f"Found ⊈ (corruption!) at byte {i}")
        break

print(f"\nFirst 100 bytes (hex): {raw[:100].hex()}")
