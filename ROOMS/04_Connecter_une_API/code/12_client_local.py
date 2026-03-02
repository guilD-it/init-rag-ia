# Script 12 - Client Python qui interroge le serveur FastAPI local
# Room 04 - Connecter une API
# Prerequis : le serveur mini_api_fastapi.py doit tourner sur le port 8000

import requests

# Adresse du serveur local
URL_SERVEUR = "http://127.0.0.1:8000"

# Vérification que le serveur est opérationnel
print("=== Vérification du serveur ===")
try:
    r = requests.get(f"{URL_SERVEUR}/sante", timeout=10)
    if r.status_code == 200:
        print(f"Serveur OK : {r.json()['message']}")
    else:
        print(f"Le serveur a répondu avec le code {r.status_code}")
except requests.ConnectionError:
    print("Impossible de se connecter au serveur.")
    print("Assurez-vous que le serveur est lancé avec :")
    print("  python -m uvicorn code.mini_api_fastapi:app --reload --port 8000")
    exit(1)
except requests.Timeout:
    print("Le serveur met trop de temps a repondre (timeout).")
    print("Verifiez que FastAPI est bien demarre et disponible sur le port 8000.")
    exit(1)

print()

# Boucle interactive : l'utilisateur pose des questions
print("=== Client interactif ===")
print("Posez vos questions au serveur local. Tapez 'quitter' pour arrêter.")
print()

while True:
    question = input("Votre question : ").strip()

    if question.lower() == "quitter":
        print("Au revoir.")
        break

    if not question:
        print("Veuillez entrer une question.")
        continue

    # Envoi de la question au serveur local via une requête POST
    try:
        r = requests.post(
            f"{URL_SERVEUR}/question",
            json={"question": question},
            timeout=30
        )

        if r.status_code == 200:
            data = r.json()
            print(f"\nRéponse : {data['reponse']}")
            print(f"Tokens utilisés : {data['tokens_utilises']}")
        else:
            print(f"Erreur du serveur : {r.status_code}")

    except requests.ConnectionError:
        print("Connexion perdue avec le serveur.")
    except requests.Timeout:
        print("Le serveur ne repond pas a temps. Reessayez dans quelques secondes.")

    print()
