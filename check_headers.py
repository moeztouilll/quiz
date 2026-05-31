import re

text = open(r'C:\Users\MSI\.gemini\antigravity\brain\b5ca7adb-12a1-485d-800f-60a1aebf975b\scratch\elements_debug.txt', 'r', encoding='utf-8').read()
images = re.finditer(r'<img[^>]+src="([^"]+)"', text)

for m in images:
    src = m.group(1)
    if 'ccnareponses' not in src and 'reponseccna' not in src and 'itexamanswers' not in src: continue
    
    start = max(0, m.start() - 500)
    end = min(len(text), m.end() + 500)
    context = text[start:end]
    
    headers_before = re.findall(r'>\s*(\d+)\.\s*', text[start:m.start()])
    headers_after = re.findall(r'>\s*(\d+)\.\s*', text[m.end():end])
    
    print(f'IMAGE: {src.split("/")[-1]} | BEFORE: {headers_before[-1] if headers_before else None} | AFTER: {headers_after[0] if headers_after else None}')
