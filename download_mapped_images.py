import json
import urllib.request
import os

questions_path = r"C:\Users\MSI\Downloads\quiz\public\questions.json"
with open(questions_path, "r", encoding="utf-8") as f:
    qs = json.load(f)

for q in qs:
    if q.get("image") and q["image"].startswith("http"):
        url = q["image"]
        ext = url.split('.')[-1]
        if len(ext) > 4: ext = "jpg"
        
        # Use original_num if possible, otherwise num
        num = q.get("original_num", q["num"])
        local_path = f"images/q_{num}.{ext}"
        full_local_path = f"c:/Users/MSI/Downloads/quiz/public/{local_path}"
        
        try:
            # Adding headers to bypass simple bot protections
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response, open(full_local_path, 'wb') as out_file:
                out_file.write(response.read())
            q["image"] = local_path
            print(f"Downloaded {local_path}")
        except Exception as e:
            print(f"Failed to download {url}: {e}")
            # If download fails, keep the remote URL or set to None
            pass

with open(questions_path, "w", encoding="utf-8") as f:
    json.dump(qs, f, ensure_ascii=False, indent=2)

print("Finished downloading images.")
