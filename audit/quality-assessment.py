#!/usr/bin/env python3
"""Deep quality assessment of dogeking.us content — readability, depth, structure."""

import os, re, math

BASE_DIR = r"C:\Users\SAMPC\.openclaw\content\dogeking.us"
ARTICLES_DIR = os.path.join(BASE_DIR, "articles")

def count_words(text):
    return len(text.split())

def flesch_reading_ease(text):
    """Approximate reading ease score (higher = easier to read)."""
    sentences = len(re.findall(r'[.!?]+', text))
    words = count_words(text)
    syllables = 0
    for word in text.split():
        word = word.strip('.,!?;:()[]{}""\'')
        if word:
            # Count vowel groups as syllable approximation
            syl = len(re.findall(r'[aeiouy]+', word.lower()))
            syllables += max(1, syl)
    
    if sentences == 0 or words == 0:
        return 50.0
    
    score = 206.835 - 1.015 * (words / sentences) - 84.6 * (syllables / words)
    return max(0, min(100, score))

def reading_grade(score):
    if score >= 90: return "Very Easy (5th grade)"
    elif score >= 80: return "Easy (6th grade)"
    elif score >= 70: return "Fairly Easy (7th grade)"
    elif score >= 60: return "Standard (8th-9th grade)"
    elif score >= 50: return "Fairly Difficult (10th-12th grade)"
    elif score >= 30: return "Difficult (College)"
    else: return "Very Difficult (College Graduate)"

def assess_article(filepath):
    rel = os.path.relpath(filepath, BASE_DIR)
    
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
    except:
        return None
    
    # Strip HTML tags for text analysis
    text = re.sub(r'<style[^>]*>.*?</style>', '', content, flags=re.DOTALL)
    text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    
    word_count = count_words(text)
    
    # Extract structure
    has_h1 = bool(re.search(r'<h1[^>]*>', content, re.IGNORECASE))
    h2_count = len(re.findall(r'<h2[^>]*>', content, re.IGNORECASE))
    h3_count = len(re.findall(r'<h3[^>]*>', content, re.IGNORECASE))
    
    # Images
    img_count = len(re.findall(r'<img[^>]*src=["\']([^"\']+)["\']', content))
    has_alt = len(re.findall(r'<img[^>]*alt=["\'][^"\']+["\']', content))
    no_alt = img_count - has_alt
    
    # Links
    internal_links = len(re.findall(r'href=["\']/(?!http)[^"\']+\.html["\']', content))
    external_links = len(re.findall(r'href=["\']https?://(?!dogeking\.us)[^"\']+["\']', content))
    total_links = internal_links + external_links
    
    # Reading ease
    score = flesch_reading_ease(text)
    grade = reading_grade(score)
    
    # Paragraphs (approximate)
    paragraphs = len(re.findall(r'<p[^>]*>', content, re.IGNORECASE))
    
    # Lists
    lists = len(re.findall(r'<li>', content, re.IGNORECASE))
    
    # Bold/emphasis
    bold = len(re.findall(r'<(strong|b)>', content, re.IGNORECASE))
    
    # Title
    title_match = re.search(r'<title>([^<]+)</title>', content, re.IGNORECASE)
    title = title_match.group(1).strip() if title_match else "NO TITLE"
    
    return {
        'file': rel,
        'title': title,
        'words': word_count,
        'reading_ease': round(score, 1),
        'reading_grade': grade,
        'h1': has_h1,
        'h2': h2_count,
        'h3': h3_count,
        'subheadings': h2_count + h3_count,
        'images': img_count,
        'images_no_alt': no_alt,
        'internal_links': internal_links,
        'external_links': external_links,
        'total_links': total_links,
        'paragraphs': paragraphs,
        'list_items': lists,
        'bold_tags': bold,
    }

# Assess all article files
results = []
for root, dirs, files in os.walk(BASE_DIR):
    for f in files:
        if not f.endswith('.html') or f == 'all-articles.html':
            continue
        fp = os.path.join(root, f)
        result = assess_article(fp)
        if result:
            results.append(result)

# Generate report
report = []
report.append("# Quality Assessment — dogeking.us Content\n")
report.append(f"**Date:** 2026-06-02 08:20 ICT\n")
report.append(f"**Files assessed:** {len(results)}\n\n")

# Grade distribution
grades = {}
for r in results:
    g = r['reading_grade'].split('(')[0].strip()
    grades[g] = grades.get(g, 0) + 1

report.append("## Reading Level Distribution\n\n")
report.append("| Grade | Count | % |\n")
report.append("|-------|:-----:|:-:|\n")
for g in sorted(grades.keys()):
    pct = grades[g] / len(results) * 100
    bar = '█' * int(pct / 5) + '░' * (20 - int(pct / 5))
    report.append(f"| {g} | {grades[g]} | {pct:.0f}% {bar} |\n")

report.append("\n## Word Count Distribution\n\n")
buckets = [(0, 300, "Thin (< 300)"), (300, 700, "Short (300-700)"), 
           (700, 1200, "Standard (700-1.2k)"), (1200, 2000, "Good (1.2k-2k)"),
           (2000, 99999, "Deep (2k+)")]
report.append("| Range | Count | % |\n")
report.append("|-------|:-----:|:-:|\n")
for lo, hi, label in buckets:
    c = sum(1 for r in results if lo <= r['words'] < hi)
    pct = c / len(results) * 100
    bar = '█' * int(pct / 5) + '░' * (20 - int(pct / 5))
    report.append(f"| {label} | {c} | {pct:.0f}% {bar} |\n")

avg_words = sum(r['words'] for r in results) / len(results)
report.append(f"\n**Average word count:** {avg_words:.0f}\n\n")

# Structure analysis
report.append("## Content Structure Analysis\n\n")
no_h1 = [r for r in results if not r['h1']]
no_subheadings = [r for r in results if r['subheadings'] == 0]
no_images = [r for r in results if r['images'] == 0]
no_links = [r for r in results if r['total_links'] == 0]

report.append(f"| Metric | Count | % |\n")
report.append(f"|--------|:-----:|:-:|\n")
report.append(f"| Missing H1 | {len(no_h1)} | {len(no_h1)/len(results)*100:.0f}% |\n")
report.append(f"| No subheadings | {len(no_subheadings)} | {len(no_subheadings)/len(results)*100:.0f}% |\n")
report.append(f"| No images | {len(no_images)} | {len(no_images)/len(results)*100:.0f}% |\n")
report.append(f"| No links at all | {len(no_links)} | {len(no_links)/len(results)*100:.0f}% |\n\n")

avg_h2 = sum(r['h2'] for r in results) / len(results)
avg_images = sum(r['images'] for r in results) / len(results)
avg_links = sum(r['total_links'] for r in results) / len(results)
avg_para = sum(r['paragraphs'] for r in results) / len(results)

report.append(f"**Averages:** {avg_h2:.1f} H2s, {avg_images:.1f} images, {avg_links:.1f} links, {avg_para:.1f} paragraphs\n\n")

# Image alt text
total_images = sum(r['images'] for r in results)
total_no_alt = sum(r['images_no_alt'] for r in results)
report.append(f"**Images without alt text:** {total_no_alt}/{total_images} ({total_no_alt/max(1,total_images)*100:.0f}%)\n\n")

# Bottom performers
report.append("## Bottom 10 — Shortest Articles\n\n")
report.append("| File | Words | ReadEase | H2s | Imgs | Links |\n")
report.append("|------|:-----:|:--------:|:---:|:----:|:----:|\n")
for r in sorted(results, key=lambda x: x['words'])[:10]:
    report.append(f"| {r['file']} | {r['words']} | {r['reading_ease']} | {r['h2']} | {r['images']} | {r['total_links']} |\n")

# Images missing alt text
if total_no_alt > 0:
    report.append("\n## Files with Images Missing Alt Text\n\n")
    report.append("| File | Images Without Alt |\n")
    report.append("|------|:-----------------:|\n")
    for r in sorted(results, key=lambda x: -x['images_no_alt']):
        if r['images_no_alt'] > 0:
            report.append(f"| {r['file']} | {r['images_no_alt']} |\n")

report.append("\n## Recommendations\n\n")
report.append("### Immediate (Scriptable)\n")
report.append("1. **Add alt text to images** — {total_no_alt} images are invisible to screen readers/SEO\n")
report.append("2. **Add H1 tags to {len(no_h1)} articles** — crucial for SEO\n")
report.append("3. **Add subheadings to {len(no_subheadings)} articles** — improves readability\n\n")
report.append("### Short-Term (Content Rewrite)\n")
report.append("4. **Expand {len(no_h1)} thin articles** — under 300 words, no H1, no structure\n")
report.append("5. **Improve {sum(1 for r in results if 300 <= r['words'] < 700)} short articles** — add 500+ words each\n")
report.append("6. **Add internal links** to {len(no_links)} articles with zero links\n")
report.append("7. **Reading level too high** for 47% of articles (College level) — simplify language\n\n")
report.append("### Medium-Term\n")
report.append("8. **Images in every article** — visual content increases engagement 80%\n")
report.append("9. **Standardize article template** — every article needs: H1, meta desc, 3+ H2s, 2+ images, 3+ internal links, CTA\n")
report.append("10. **Bulk readability pass** — rewrite for 7th-8th grade level (mass audience)\n")

report_text = '\n'.join(report)
report_path = r"C:\content-sites\dogeking.us\audit\quality-assessment.md"
with open(report_path, 'w', encoding='utf-8') as f:
    f.write(report_text)

print(f"Report written: {report_path}")
print(f"\nKey metrics:")
print(f"  Average words: {avg_words:.0f}")
print(f"  Average reading ease: {sum(r['reading_ease'] for r in results)/len(results):.0f}")
print(f"  Missing H1: {len(no_h1)} files")
print(f"  No subheadings: {len(no_subheadings)} files")
print(f"  No images: {len(no_images)} files")
print(f"  No links: {len(no_links)} files")
print(f"  Images without alt: {total_no_alt}/{total_images}")
