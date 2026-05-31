import json

with open(r"C:\Users\MSI\Downloads\quiz\public\questions.json", "r", encoding="utf-8") as f:
    qs = json.load(f)

print("Questions with no choices and no table:")
for q in qs:
    if not q.get("choices") and not q.get("table"):
        print(f"Num: {q['num']}, Original Num: {q.get('original_num', 'N/A')}")
        print(f"Text: {q['question_text']}")
        print(f"Image: {q.get('image')}")
        print("-" * 40)
