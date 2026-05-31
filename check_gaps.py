import json

with open(r"C:\Users\MSI\Downloads\quiz\questions.json", "r", encoding="utf-8") as f:
    qs = json.load(f)

nums = [q["num"] for q in qs]
all_nums = set(nums)
expected = set(range(1, max(nums) + 1))
missing = expected - all_nums
print(f"Total questions found: {len(qs)}")
print(f"Max question number: {max(nums)}")
print(f"Missing question numbers: {sorted(list(missing))}")
print(f"Duplicate question numbers: {sorted(list(set([n for n in nums if nums.count(n) > 1])))}")
