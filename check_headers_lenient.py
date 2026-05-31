import re

with open("C:\\Users\\MSI\\.gemini\\antigravity\\brain\\b5ca7adb-12a1-485d-800f-60a1aebf975b\\scratch\\elements_debug.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Let's write a python parser to print any line starting with a number and a dot, regardless of spacing
lines = text.split("\n")
q_headers = []
for idx, line in enumerate(lines):
    # Match any lines containing a number followed by a dot, optionally with bold/strong tag
    # Let's clean the HTML tags first to make text matching easier
    clean_line = re.sub(r'<[^>]+>', '', line).strip()
    match = re.match(r'^(\d+)\.(.*)', clean_line)
    if match:
        q_headers.append((idx, int(match.group(1)), clean_line))

print(f"Found {len(q_headers)} headers")
# Check if numbers are sequential
nums = [h[1] for h in q_headers]
all_nums = set(nums)
expected = set(range(1, max(nums) + 1))
missing = expected - all_nums
print(f"Missing: {sorted(list(missing))}")
print(f"Duplicates: {sorted(list(set([n for n in nums if nums.count(n) > 1])))}")
