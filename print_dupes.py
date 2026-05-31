import json
import re

qs_path = r"C:\Users\MSI\Downloads\quiz\public\questions.json"
with open(qs_path, "r", encoding="utf-8") as f:
    qs = json.load(f)

# Print all duplicates with their full data
nums = [q["num"] for q in qs]
dupes = set(n for n in nums if nums.count(n) > 1)

for num in sorted(dupes):
    all_with_num = [q for q in qs if q["num"] == num]
    print(f"\n=== DUPLICATE Q{num} ({len(all_with_num)} entries) ===")
    for q in all_with_num:
        print(f"  text: {q['question_text'][:100]}")
        print(f"  choices: {len(q.get('choices', []))} | table: {'YES' if q.get('table') else 'NO'} | image: {q.get('image')}")
