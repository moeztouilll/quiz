import json
import re

qs_path = r"C:\Users\MSI\Downloads\quiz\public\questions.json"
with open(qs_path, "r", encoding="utf-8") as f:
    qs = json.load(f)

print(f"Total questions: {len(qs)}\n")

problems = []

for q in qs:
    text = q.get("question_text", "")
    
    # Check if question text contains another question number (e.g., "156. Quelle...")
    embedded = re.findall(r'\d{2,3}\.\s+[A-ZÀ-Ÿ]', text)
    if embedded:
        problems.append(f"Q{q['num']}: EMBEDDED QUESTION? -> {embedded} | text: {text[:100]}")
    
    # Check if choices are empty AND no table (broken question)
    if not q.get("choices") and not q.get("table"):
        problems.append(f"Q{q['num']}: NO CHOICES NO TABLE -> image: {q.get('image')} | text: {text[:80]}")

if problems:
    print("PROBLEMS FOUND:")
    for p in problems:
        print(" -", p)
else:
    print("No problems found!")

# Also verify all nums are unique
nums = [q["num"] for q in qs]
dupes = [n for n in nums if nums.count(n) > 1]
if dupes:
    print(f"\nDUPLICATE NUMS: {set(dupes)}")
else:
    print("\nAll nums are unique!")
