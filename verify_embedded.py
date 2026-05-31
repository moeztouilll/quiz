import json
import re

qs_path = r"C:\Users\MSI\Downloads\quiz\public\questions.json"
with open(qs_path, "r", encoding="utf-8") as f:
    qs = json.load(f)

# These "embedded question" false positives are because the question TEXT itself
# contains a port number like "69." followed by a capital letter (e.g., "port 69. Quelle")
# That is NOT an embedded question - it's a port number in the question text.
# Let's filter by checking if the "embedded" number is preceded by "port" or "destination de"

real_problems = []
for q in qs:
    text = q.get("question_text", "")
    matches = re.finditer(r'(\d{2,3})\.\s+([A-ZÀ-Ÿ])', text)
    for m in matches:
        num_str = m.group(1)
        start = max(0, m.start() - 30)
        context_before = text[start:m.start()]
        # If the number appears after "port" or "de", it's a port number, not a Q number
        if re.search(r'(port|destination de|numéro de port)\s*$', context_before.strip()):
            continue  # False positive - port number
        if re.search(r'^\d{1,3}\.\d{1,3}\.\d{1,3}', text[m.start():]):
            continue  # False positive - IP address
        real_problems.append(f"Q{q['num']}: number {num_str} -> context: '{context_before[-20:]}|{m.group()}'")

if real_problems:
    print("REAL embedded question problems:")
    for p in real_problems:
        print(" -", p)
else:
    print("No real embedded question problems! (All were port numbers or IPs in question text)")
