import json
qs = json.load(open(r'c:\Users\MSI\Downloads\quiz\public\questions.json', encoding='utf-8'))
for q in qs:
    if q.get('image'):
        print(f"Q{q['num']}: {q['question_text'][:80]}... -> {q['image']}")
