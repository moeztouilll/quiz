import json
import requests
from bs4 import BeautifulSoup
import re
import urllib.request

url = "https://ccnareponses.com/ccna-1-examen-final-itnv7-questions-et-reponses-francais/"
headers = {'User-Agent': 'Mozilla/5.0'}
print("Fetching original site...")
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

print("Parsing original site...")
# Questions are typically inside <p><strong>1. ...</strong></p>
# Images are in <figure><img> or <p><img>
elements = soup.find('div', class_='entry-content').find_all(['p', 'figure', 'ul', 'div'])

image_mapping = {}
current_q_num = None

for el in elements:
    text = el.get_text(strip=True)
    match = re.search(r'^(\d+)\.\s', text)
    if match:
        current_q_num = int(match.group(1))
    
    imgs = el.find_all('img')
    for img in imgs:
        src = img.get('src')
        if not src or "data:image" in src: continue
        
        # If we have an image, it belongs to the CURRENT question if it appears AFTER the question header,
        # OR sometimes CCNA responses puts the image in a <figure> right BEFORE the question header!
        # If current_q_num is set, it might belong to it, but let's check if the NEXT element is a question header.
        
        # Actually, let's find the closest strong tag with a number in the DOM
        parent = img.find_parent()
        next_sib = parent.find_next_sibling()
        prev_sib = parent.find_previous_sibling()
        
        assigned_num = current_q_num
        
        if next_sib:
            ns_text = next_sib.get_text(strip=True)
            ns_match = re.search(r'^(\d+)\.\s', ns_text)
            if ns_match:
                # The image is right before the NEXT question, so it belongs to the NEXT question!
                assigned_num = int(ns_match.group(1))
                
        if assigned_num:
            if assigned_num not in image_mapping:
                image_mapping[assigned_num] = []
            if src not in image_mapping[assigned_num]:
                image_mapping[assigned_num].append(src)

print("Found mapping:")
for k, v in image_mapping.items():
    print(f"Q{k}: {v}")

qs_path = r"C:\Users\MSI\Downloads\quiz\public\questions.json"
with open(qs_path, "r", encoding="utf-8") as f:
    qs = json.load(f)

for q in qs:
    q["image"] = None # clear all
    num = q.get("original_num", q["num"])
    if num in image_mapping and len(image_mapping[num]) > 0:
        # Use the first image
        q["image"] = image_mapping[num][0]
        
with open(qs_path, "w", encoding="utf-8") as f:
    json.dump(qs, f, ensure_ascii=False, indent=2)

print("Updated questions.json")
