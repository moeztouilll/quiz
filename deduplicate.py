import json

qs_path = r"C:\Users\MSI\Downloads\quiz\public\questions.json"
with open(qs_path, "r", encoding="utf-8") as f:
    qs = json.load(f)

# There are 2 sources of questions that got merged with duplicate nums:
# 1. The original CCNA1 questions
# 2. Bonus questions from a second part of the site
#
# For each duplicate, we keep BOTH but give the second one a new unique num (200+)
# We detect which is "extra" by checking: if q['num'] already appeared, it's a duplicate.

seen = {}
to_reassign = []

for i, q in enumerate(qs):
    num = q["num"]
    if num in seen:
        to_reassign.append(i)
        print(f"Will reassign index {i}: Q{num} -> {q['question_text'][:60]}")
    else:
        seen[num] = i

# Find max num to start new numbering from
max_num = max(q["num"] for q in qs)
next_num = max_num + 1

for i in to_reassign:
    old_num = qs[i]["num"]
    qs[i]["num"] = next_num
    qs[i]["original_num"] = old_num  # keep a trace
    print(f"Reassigned Q{old_num} at index {i} -> Q{next_num}")
    next_num += 1

with open(qs_path, "w", encoding="utf-8") as f:
    json.dump(qs, f, ensure_ascii=False, indent=2)

# Verify
nums = [q["num"] for q in qs]
dupes = set(n for n in nums if nums.count(n) > 1)
print(f"\nTotal questions: {len(qs)}")
print(f"Remaining duplicates: {dupes if dupes else 'None!'}")
