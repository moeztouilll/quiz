import json

filepath = r"C:\Users\MSI\Downloads\quiz\public\questions.json"

with open(filepath, "r", encoding="utf-8") as f:
    qs = json.load(f)

for q in qs:
    if "Associez le type de menace" in q["question_text"] and "2021-11-13_112035" in str(q.get("image", "")):
        q["table"] = [
            {
                "left": "mauvaise gestion des composants électriques clés (décharge électrostatique), manque de pièces de rechange critiques, câblage défaillant et mauvais étiquetage",
                "right": "menaces de maintenance"
            },
            {
                "left": "extrêmes de température (trop chaud ou trop froid) ou extrêmes d'humidité (trop humide ou trop sec)",
                "right": "menaces environnementales"
            },
            {
                "left": "dommages physiques aux serveurs, routeurs, commutateurs, installation de câblage et postes de travail",
                "right": "menaces matérielles"
            },
            {
                "left": "sursauts de tension, tension d'alimentation insuffisante (coupures de courant), alimentation non conditionnée (bruit) et perte totale de puissance",
                "right": "menaces électriques"
            },
            {
                "left": "accès non autorisé entraînant une perte de données",
                "right": ""
            }
        ]
        q["choices"] = []
        break

with open(filepath, "w", encoding="utf-8") as f:
    json.dump(qs, f, ensure_ascii=False, indent=2)

print("Updated questions.json successfully.")
