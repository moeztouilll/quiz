import re
import sys

sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)
text = open(r'C:\Users\MSI\.gemini\antigravity\brain\b5ca7adb-12a1-485d-800f-60a1aebf975b\scratch\elements_debug.txt', 'r', encoding='utf-8').read()
m = re.search(r'67\.\s', text)
start = m.start() if m else 0
end = m.end() + 2000 if m else 100
print(text[max(0, start):end])
