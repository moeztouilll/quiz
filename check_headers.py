import re

with open("C:\\Users\\MSI\\.gemini\\antigravity\\brain\\b5ca7adb-12a1-485d-800f-60a1aebf975b\\scratch\\elements_debug.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Let's search for lines containing question number indicators
# Like "16. " or "79. "
lines = text.split("\n")
q_headers = []
for idx, line in enumerate(lines):
    match = re.search(r'^\s*<strong>\s*(\d+)\.\s+', line)
    if not match:
        match = re.search(r'^\s*(\d+)\.\s+', line)
    if match:
        q_headers.append((idx, line.strip()))

print(f"Found {len(q_headers)} headers via regex in elements_debug.txt")
# Let's inspect some of the headers
for h in q_headers[:20]:
    print(f"Line {h[0]}: {h[1]}")
