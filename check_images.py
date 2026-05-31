import json
qs = json.load(open(r'c:\Users\MSI\Downloads\quiz\public\questions.json', encoding='utf-8'))
for q in qs:
    if q['num'] in [67, 68, 80, 81, 82, 83, 97, 98, 116, 117, 127, 128]:
        print(f"Q{q['num']}: {q.get('image')}")
