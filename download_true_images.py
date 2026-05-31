import json
import urllib.request
import os

qs_path = r"C:\Users\MSI\Downloads\quiz\public\questions.json"
with open(qs_path, "r", encoding="utf-8") as f:
    qs = json.load(f)

for q in qs:
    img = q.get("image")
    if img and img.startswith("http"):
        num = q.get("original_num", q["num"])
        ext = img.split('.')[-1]
        if len(ext) > 4: ext = "jpg"
        
        local_path = f"images/q_{num}.{ext}"
        full_local_path = f"c:/Users/MSI/Downloads/quiz/public/{local_path}"
        
        try:
            req = urllib.request.Request(img, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response, open(full_local_path, 'wb') as out_file:
                out_file.write(response.read())
            q["image"] = local_path
            print(f"Downloaded {local_path} for Q{num}")
        except Exception as e:
            print(f"Failed to download {img} for Q{num}: {e}")
            # Even if it fails, maybe we already have a fallback or we leave it as http

with open(qs_path, "w", encoding="utf-8") as f:
    json.dump(qs, f, ensure_ascii=False, indent=2)

print("Finished downloading absolute true images.")
