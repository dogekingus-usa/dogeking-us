#!/usr/bin/env python3
import re, os

with open('articles-data.js') as f:
    content = f.read()

# Find all slug fields (JS unquoted keys)
slugs = re.findall(r'slug:\s*"([^"]+)"', content)
print(f"Total articles in data file: {len(slugs)}")

cats = re.findall(r'category:\s*"([^"]+)"', content)
unique_cats = sorted(set(cats))
print(f"Unique categories: {len(unique_cats)}")
for c in unique_cats:
    count = cats.count(c)
    print(f"  {c}: {count} articles")

# List all HTML files in the repo root
html_files = [f for f in os.listdir('.') if f.endswith('.html') and os.path.isfile(f)]
print(f"\nHTML files in repo root: {len(html_files)}")

# Check if slug values match HTML filenames
html_slugs = {f.replace('.html', '') for f in html_files}
data_slugs = set(slugs)
matches = data_slugs & html_slugs
missing_html = data_slugs - html_slugs
missing_data = html_slugs - data_slugs

print(f"\nArticles with both data entry + HTML file: {len(matches)}")
print(f"Data entries without HTML file: {len(missing_html)}")
if missing_html:
    print(f"  Missing HTML: {list(missing_html)[:5]}")
print(f"HTML files without data entry: {len(missing_data)}")
if missing_data:
    print(f"  Extra HTML: {list(missing_data)[:10]}")

# Show first article structure
print("\n\nFirst data entry structure:")
idx = content.find('{')
depth = 0
end = idx
for i in range(idx, min(idx+2000, len(content))):
    if content[i] == '{': depth += 1
    elif content[i] == '}': depth -= 1
    if depth == 0:
        end = i+1
        break
print(content[idx:end])

# Check if there's an HTML template/structure we can adapt
print(f"\n\nSample HTML file content (first 1000 chars of a small file):")
sample = [f for f in html_files if os.path.getsize(f) < 15000]
if sample:
    with open(sample[0]) as f:
        print(f.read()[:1000])
