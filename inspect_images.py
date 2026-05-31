import json
import re

text = open(r'C:\Users\MSI\.gemini\antigravity\brain\b5ca7adb-12a1-485d-800f-60a1aebf975b\scratch\elements_debug.txt', 'r', encoding='utf-8').read()
elements = re.split(r'=== ELEMENT \d+ \([^)]+\) ===\n', text)[1:]

for i, el in enumerate(elements):
    if '<img' in el:
        srcs = re.findall(r'src="([^"]+)"', el)
        if not srcs: continue
        src = srcs[0]
        if 'ccnareponses' not in src and 'reponseccna' not in src and 'itexamanswers' not in src:
            continue
            
        print(f"\nIMAGE {src.split('/')[-1]}")
        # look back
        for j in range(max(0, i-4), i):
            match = re.search(r'>\s*(\d+)\.\s*', elements[j])
            if match: print(f"  PREV: Q{match.group(1)}")
        # look forward
        for j in range(i+1, min(len(elements), i+4)):
            match = re.search(r'>\s*(\d+)\.\s*', elements[j])
            if match: print(f"  NEXT: Q{match.group(1)}")
