import json

qs_path = r"C:\Users\MSI\Downloads\quiz\public\questions.json"
with open(qs_path, "r", encoding="utf-8") as f:
    qs = json.load(f)

print("Questions with NO choices AND NO table (image-only):")
for q in qs:
    if not q.get("choices") and not q.get("table"):
        print(f"  Q{q['num']}: {q['question_text'][:80]}... -> image: {q.get('image')}")

print("\nQuestions with empty choices list but WITH image:")
for q in qs:
    if q.get("choices") is not None and len(q.get("choices", [])) == 0 and q.get("image"):
        print(f"  Q{q['num']}: {q['question_text'][:80]}...")

print("\nTotal questions:", len(qs))
