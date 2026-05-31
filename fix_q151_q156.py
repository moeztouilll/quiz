import json

qs_path = r"C:\Users\MSI\Downloads\quiz\public\questions.json"
with open(qs_path, "r", encoding="utf-8") as f:
    qs = json.load(f)

# Find Q151 (which currently contains both Q151 AND Q156 merged)
for i, q in enumerate(qs):
    if q["num"] == 151:
        # Fix Q151 to be a proper MATCHING question
        q["question_text"] = "Associez une instruction au modèle de réseau associé. (Toutes les options ne sont pas utilisées.)"
        q["choices"] = []
        q["table"] = [
            {"left": "Aucun serveur dédié n'est requis", "right": "Réseau pair à pair"},
            {"left": "Les rôles client et serveur sont définis par requête", "right": "Réseau pair à pair"},
            {"left": "Nécessite une interface utilisateur spécifique", "right": "Application peer-to-peer"},
            {"left": "Un service d'arrière-plan est requis", "right": "Application peer-to-peer"}
        ]
        q["explanation"] = "Les réseaux peer-to-peer ne nécessitent pas l'utilisation d'un serveur dédié, et les appareils peuvent assumer simultanément les rôles de client et de serveur sur demande. Les applications peer-to-peer nécessitent une interface utilisateur et un service d'arrière-plan pour s'exécuter."
        q["image"] = "images/q_151.png"
        print(f"Fixed Q151")
        idx_151 = i
        break

# Check if Q156 already exists
q156_exists = any(q["num"] == 156 for q in qs)

if not q156_exists:
    # Create Q156 as a new separate question
    q156 = {
        "num": 156,
        "question_text": "Quelle caractéristique décrit un IPS ?",
        "image": None,
        "choices": [
            {"text": "Un protocole de tunneling qui fournit aux utilisateurs distants un accès sécurisé au réseau d'une organisation", "is_correct": False},
            {"text": "Un appareil réseau qui filtre l'accès et le trafic entrant dans un réseau", "is_correct": False},
            {"text": "Logiciel qui identifie les menaces à propagation rapide", "is_correct": True},
            {"text": "Logiciel sur un routeur qui filtre le trafic en fonction des adresses IP ou des applications", "is_correct": False}
        ],
        "table": None,
        "explanation": "Un IPS (Intrusion Prevention System) est un logiciel qui identifie les menaces à propagation rapide et peut bloquer automatiquement le trafic malveillant en temps réel, contrairement à un IDS qui se contente de détecter.",
        "extra_text": []
    }
    # Insert Q156 right after Q151 in the list
    qs.insert(idx_151 + 1, q156)
    print(f"Created Q156")
else:
    print("Q156 already exists - only fixing Q151")

with open(qs_path, "w", encoding="utf-8") as f:
    json.dump(qs, f, ensure_ascii=False, indent=2)

print("Done. Total questions:", len(qs))
