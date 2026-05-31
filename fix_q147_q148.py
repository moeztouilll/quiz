import json

qs_path = r"C:\Users\MSI\Downloads\quiz\public\questions.json"
with open(qs_path, "r", encoding="utf-8") as f:
    qs = json.load(f)

# Fix Q147: it has Q148 embedded in its question_text
# Split Q147 and Q148 apart

for i, q in enumerate(qs):
    if q["num"] == 147:
        # Q147 is a matching question (Faites correspondre le réseau...)
        # Q148 is a single-choice question (Quelle caractéristique décrit une attaque DoS?)
        # The choices currently in Q147 actually belong to Q148!
        
        # Fix Q147
        q["question_text"] = "Référez-vous à l'exposition. Faites correspondre le réseau avec l'adresse IP et le préfixe corrects qui satisferont les exigences d'adressage hôte utilisables pour chaque réseau. (Toutes les options ne sont pas utilisées.)"
        q["table"] = [
            {"left": "Réseau A (100 hôtes)", "right": "192.168.0.0/25"},
            {"left": "Réseau B (50 hôtes)", "right": "192.168.0.128/26"},
            {"left": "Réseau C (25 hôtes)", "right": "192.168.0.192/27"},
            {"left": "Réseau D (10 hôtes)", "right": "192.168.0.224/28"}
        ]
        old_choices = q["choices"]  # These belong to Q148
        q["choices"] = []
        q["image"] = "images/q_147.jpg"
        idx_147 = i
        print(f"Fixed Q147 as matching question")
        
        # Create Q148 with the choices that were wrongly in Q147
        q148 = {
            "num": 148,
            "question_text": "Quelle caractéristique décrit une attaque DoS ?",
            "image": None,
            "choices": [
                {"text": "Un logiciel déguisé en programme légitime qui s'exécute sur un ordinateur", "is_correct": False},
                {"text": "Une attaque réseau qui ralentit ou plante les services en envoyant des requêtes excessives à un hôte", "is_correct": True},
                {"text": "Un logiciel qui recueille des informations personnelles sans le consentement de l'utilisateur", "is_correct": False},
                {"text": "Une attaque qui modifie les adresses IP dans les paquets réseau", "is_correct": False}
            ],
            "table": None,
            "explanation": "Une attaque par déni de service (DoS) vise à rendre un service indisponible en le submergeant de requêtes excessives, ce qui épuise les ressources du serveur cible.",
            "extra_text": []
        }
        break

# Check if Q148 already exists
q148_exists = any(q["num"] == 148 for q in qs)
if not q148_exists:
    qs.insert(idx_147 + 1, q148)
    print(f"Created Q148")
else:
    print("Q148 already exists")

with open(qs_path, "w", encoding="utf-8") as f:
    json.dump(qs, f, ensure_ascii=False, indent=2)

print(f"Total questions: {len(qs)}")
