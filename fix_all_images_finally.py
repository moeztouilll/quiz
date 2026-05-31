import json
import re

text = open(r'C:\Users\MSI\.gemini\antigravity\brain\b5ca7adb-12a1-485d-800f-60a1aebf975b\scratch\elements_debug.txt', 'r', encoding='utf-8').read()
images = re.finditer(r'<img[^>]+src="([^"]+)"', text)

image_mapping = {}

for m in images:
    src = m.group(1)
    if 'ccnareponses' not in src and 'reponseccna' not in src and 'itexamanswers' not in src: continue
    
    # Find all question headers BEFORE this image
    text_before = text[:m.start()]
    headers_before = re.findall(r'>\s*(\d+)\.\s*', text_before)
    
    if headers_before:
        q_num = int(headers_before[-1])
        if q_num not in image_mapping:
            image_mapping[q_num] = []
        if src not in image_mapping[q_num]:
            image_mapping[q_num].append(src)

qs_path = r"C:\Users\MSI\Downloads\quiz\public\questions.json"
with open(qs_path, "r", encoding="utf-8") as f:
    qs = json.load(f)

# Clear ALL images first
for q in qs:
    q["image"] = None

# Assign true images based on BEFORE logic!
for q in qs:
    num = q.get("original_num", q["num"])
    if num in image_mapping:
        src = image_mapping[num][0] # take the first one (usually diagram)
        # Update it to the local path! We already downloaded them to images/q_{num}.jpg earlier
        ext = src.split('.')[-1]
        if len(ext) > 4: ext = "jpg"
        local_path = f"images/q_{num}.{ext}"
        
        # We need to make sure we actually downloaded them! We downloaded them according to the OLD mapping in download_true_images.py!
        # Oh! If we downloaded them with the WRONG num, the local file is named wrongly!
        # We must re-download them to the CORRECT num!
        q["image"] = src
        print(f"Mapped Q{num} -> {src}")

with open(qs_path, "w", encoding="utf-8") as f:
    json.dump(qs, f, ensure_ascii=False, indent=2)

print("Mapping completed. Now we must download them.")
