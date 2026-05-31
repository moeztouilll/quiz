import json
import re

text = open(r'C:\Users\MSI\.gemini\antigravity\brain\b5ca7adb-12a1-485d-800f-60a1aebf975b\scratch\elements_debug.txt', 'r', encoding='utf-8').read()
elements = re.split(r'=== ELEMENT \d+ \([^)]+\) ===\n', text)[1:]

# List of { index, src }
images = []
# List of { index, num, text }
headers = []

for i, el in enumerate(elements):
    if '<img' in el:
        srcs = re.findall(r'src="([^"]+)"', el)
        # some images are base64 or small icons, ignore if they don't look like real images
        for src in srcs:
            if "ccnareponses" in src or "reponseccna" in src or "itexamanswers" in src:
                images.append({"index": i, "src": src})
                
    match = re.search(r'<strong>\s*(\d+)\.\s*(.*?)</strong>', el, re.DOTALL)
    if match:
        headers.append({"index": i, "num": int(match.group(1)), "text": match.group(2).strip()})
    elif '<strong' in el:
        match2 = re.search(r'>\s*(\d+)\.\s*(.*?)<', el, re.DOTALL)
        if match2:
            headers.append({"index": i, "num": int(match2.group(1)), "text": match2.group(2).strip()})

image_mapping = {}

for img in images:
    img_idx = img["index"]
    src = img["src"]
    
    closest_after = None
    for h in headers:
        if h["index"] > img_idx:
            closest_after = h
            break
            
    closest_before = None
    for h in reversed(headers):
        if h["index"] < img_idx:
            closest_before = h
            break

    # To decide, let's check the text of closest_after and closest_before
    assigned_num = None
    
    # If the image is VERY close to the AFTER header (distance 1 or 2)
    # AND the BEFORE header is far, or the AFTER header explicitly says "Examinez", "Reportez-vous", "Associez"
    # Actually, CCNA dumps often put the image right BEFORE the question text.
    
    if closest_after and (closest_after["index"] - img_idx) <= 2:
        assigned_num = closest_after["num"]
    elif closest_before:
        assigned_num = closest_before["num"]
        
    if assigned_num:
        # If multiple images for the same question, store them as a list
        if assigned_num not in image_mapping:
            image_mapping[assigned_num] = []
        image_mapping[assigned_num].append(src)

# Now, we read questions.json and fix it!
questions_path = r"C:\Users\MSI\Downloads\quiz\public\questions.json"
with open(questions_path, "r", encoding="utf-8") as f:
    qs = json.load(f)

# Clear ALL existing images first to avoid leftover wrong images
for q in qs:
    # use original_num if it exists, otherwise num (in case user hasn't randomized yet, or to be safe, wait!)
    # Actually, questions.json STILL has `q['num']` as the original sequential number, because `app.js` randomizes IN MEMORY.
    # Let's verify if `questions.json` has `num` sequential.
    q["image"] = None

for q in qs:
    num = q.get("original_num", q["num"]) # Fallback to num if original_num doesn't exist
    if num in image_mapping:
        # Just take the FIRST image if there are multiple, usually the diagram.
        # Unless the first is tiny, but our regex filtered for valid domains.
        # Actually, let's take the first one.
        q["image"] = image_mapping[num][0]

with open(questions_path, "w", encoding="utf-8") as f:
    json.dump(qs, f, ensure_ascii=False, indent=2)

print("Mapped the following images:")
for num, srcs in image_mapping.items():
    print(f"Q{num}: {srcs[0]}")
