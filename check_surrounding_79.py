import re

with open(r"C:\Users\MSI\.gemini\antigravity\brain\b5ca7adb-12a1-485d-800f-60a1aebf975b\scratch\elements_debug.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Let's clean the HTML tags first to make text matching easier
clean_text = re.sub(r'<[^>]+>', '', text)

# Let's search for lines containing question number patterns around 78, 79, 80
for match in re.finditer(r'(\d+)\.\s+[a-zA-Z]', clean_text):
    num = int(match.group(1))
    if 75 <= num <= 85:
        # print match window
        start = max(0, match.start() - 50)
        end = min(len(clean_text), match.end() + 150)
        print(f"--- MATCH {num} ---")
        print(clean_text[start:end].replace('\n', ' '))
