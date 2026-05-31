import re

with open(r"C:\Users\MSI\.gemini\antigravity\brain\b5ca7adb-12a1-485d-800f-60a1aebf975b\scratch\elements_debug.txt", "r", encoding="utf-8") as f:
    text = f.read()

lines = text.split("\n")
q_headers = []
for idx, line in enumerate(lines):
    # Strip HTML tags
    clean_line = re.sub(r'<[^>]+>', '', line).strip()
    match = re.match(r'^(\d+)\.(.*)', clean_line)
    if match:
        num = int(match.group(1))
        rest = match.group(2).strip()
        # To be a question, it should contain letters (French alphabet)
        # IP addresses and subnet masks won't contain letters
        if re.search(r'[a-zA-ZàâäéèêëïîôöùûüçÀÂÄÉÈÊËÏÎÔÖÙÛÜÇ]', rest):
            q_headers.append((idx, num, clean_line[:100]))

print(f"Filtered headers count: {len(q_headers)}")
nums = [h[1] for h in q_headers]
all_nums = set(nums)
expected = set(range(1, max(nums) + 1))
missing = expected - all_nums
print(f"Missing: {sorted(list(missing))}")
print(f"Duplicates: {sorted(list(set([n for n in nums if nums.count(n) > 1])))}")
for h in q_headers[:10]:
    print(f"Q{h[1]}: {h[2]}")
