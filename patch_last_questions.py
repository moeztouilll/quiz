import json

filepath = r"C:\Users\MSI\Downloads\quiz\public\questions.json"

with open(filepath, "r", encoding="utf-8") as f:
    qs = json.load(f)

for q in qs:
    num = q.get("original_num", q["num"])
    if num == 82:
        q["table"] = [
            {"left": "Ce sont les réseaux les plus simples à configurer.", "right": "Réseau d'égal à égal (Peer-to-Peer)"},
            {"left": "Aucun ordinateur ne contrôle le réseau.", "right": "Réseau d'égal à égal (Peer-to-Peer)"},
            {"left": "Il exige des logiciels et périphériques réseau spécifiques.", "right": "Réseau client-serveur"},
            {"left": "Un serveur gère et contrôle l'accès au réseau.", "right": "Réseau client-serveur"}
        ]
        q["choices"] = []
    elif num == 113:
        q["table"] = [
            {"left": "Permettent au récepteur d'indiquer de façon fiable à l'expéditeur les octets qui ont été reçus correctement", "right": "Accusés de réception"},
            {"left": "Définit le nombre d'octets que le récepteur est capable de traiter à un moment donné", "right": "Taille de la fenêtre"},
            {"left": "Permettent au périphérique de destination de reconstituer les données dans un ordre précis", "right": "Numéros de séquence"}
        ]
        q["choices"] = []
    elif num == 116:
        q["table"] = [
            {"left": "HTTP", "right": "TCP"},
            {"left": "FTP", "right": "TCP"},
            {"left": "SMTP", "right": "TCP"},
            {"left": "TFTP", "right": "UDP"},
            {"left": "DHCP", "right": "UDP"}
        ]
        q["choices"] = []
    elif num == 117:
        q["table"] = [
            {"left": "Empêche ou autorise l'accès en fonction des adresses MAC ou des adresses IP", "right": "Filtrage des paquets"},
            {"left": "Empêche ou autorise l'accès en fonction des ports d'application", "right": "Filtrage des applications"},
            {"left": "S'assure que les connexions TCP sont établies correctement", "right": "Inspection dynamique (Stateful)"}
        ]
        q["choices"] = []

with open(filepath, "w", encoding="utf-8") as f:
    json.dump(qs, f, ensure_ascii=False, indent=2)

print("Manually patched remaining matching questions.")
