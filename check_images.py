import json

with open("C:\\Users\\MSI\\Downloads\\quiz\\questions.json", "r", encoding="utf-8") as f:
    qs = json.load(f)

img_qs = [q for q in qs if q["image"]]
print(f"Total questions with images: {len(img_qs)}")
for q in img_qs[:15]:
    print(f"Q{q['num']}: {q['image']}")
