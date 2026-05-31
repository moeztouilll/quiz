import json
import re

qs_path = r"C:\Users\MSI\Downloads\quiz\public\questions.json"
with open(qs_path, "r", encoding="utf-8") as f:
    qs = json.load(f)

# For Q7, Q87, Q111, Q120, Q123: "port de destination est 69. Quelle application..."
# These are correct! "69. Quelle..." is part of asking "port 69, what is the application?"
# The question title already says the port number, then asks the question in the SAME sentence.
# Example: "Le numéro de port de destination du paquet est 69. Quelle application de couche..."
# -> That IS the actual question text, not an embedded separate question.
# Let's confirm by checking the choices - if they have valid choices, the question is fine.

for q in qs:
    if q["num"] in [7, 87, 111, 120, 123, 169, 179, 141]:
        print(f"Q{q['num']}: choices={len(q.get('choices',[]))} | text: {q['question_text']}")
        print()

# Q101 and Q147 are the real issues
# Q101: "...d'aide d'un préfixe /29. A..." -> embedded Q text?
# Q147: "...Les options ne sont pas utilisées.) 148. Quelle..." -> definitely merged!

print("\n=== Q101 ===")
q101 = next(q for q in qs if q["num"] == 101)
print(q101["question_text"])
print("\n=== Q147 ===")
q147 = next(q for q in qs if q["num"] == 147)
print(q147["question_text"])
print("table:", q147.get("table"))
print("choices:", len(q147.get("choices", [])))
