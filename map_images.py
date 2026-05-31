import json
import re

text = open(r'C:\Users\MSI\.gemini\antigravity\brain\b5ca7adb-12a1-485d-800f-60a1aebf975b\scratch\elements_debug.txt', 'r', encoding='utf-8').read()
elements = re.split(r'=== ELEMENT \d+ \([^)]+\) ===\n', text)[1:]

# Create a list of all images and their EXACT positions
# and a list of all question headers and their EXACT positions
images = []
headers = []

for i, el in enumerate(elements):
    if '<img' in el:
        srcs = re.findall(r'src="([^"]+)"', el)
        for src in srcs:
            images.append({"index": i, "src": src})
    
    # Check for question header
    # Usually in <p><strong>12. ...
    match = re.search(r'<strong>\s*(\d+)\.\s*', el)
    if match:
        headers.append({"index": i, "num": int(match.group(1))})
    elif '<strong' in el:
        # sometimes it's <span style="..."><strong>12.
        match2 = re.search(r'>\s*(\d+)\.\s*', el)
        if match2:
             headers.append({"index": i, "num": int(match2.group(1))})

# Now, for each image, we find the CLOSEST header
image_to_q = {}
for img in images:
    img_idx = img["index"]
    
    # Find closest header AFTER the image
    closest_after = None
    for h in headers:
        if h["index"] > img_idx:
            closest_after = h
            break
            
    # Find closest header BEFORE the image
    closest_before = None
    for h in reversed(headers):
        if h["index"] < img_idx:
            closest_before = h
            break
            
    # Heuristic: 
    # If the distance to closest_after is 1 or 2, it probably belongs to closest_after!
    # Because CCNA dumps often put the image right BEFORE the text "27. Examinez l'illustration"
    # Otherwise, it belongs to closest_before.
    
    assigned_num = None
    if closest_after and (closest_after["index"] - img_idx) <= 2:
        assigned_num = closest_after["num"]
    elif closest_before:
        assigned_num = closest_before["num"]
        
    if assigned_num:
        image_to_q[img["src"]] = assigned_num

# Wait, the images are already downloaded. Their local names in questions.json are like "images/q_66.jpg"
# But they were downloaded from the ORIGINAL urls.
# So I need to map original URL -> correct Q num.
# And then update questions.json!

# Let's see what URLs we had in questions.json originally.
# I can just print the mapping for now to verify.
for src, num in image_to_q.items():
    print(f"Image {src.split('/')[-1]} belongs to Q{num}")
