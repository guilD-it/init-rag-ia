# Script 12 - Client Python qui interroge le serveur FastAPI local
# Room 04 - Connecter une API
# Prerequis : le serveur mini_api_fastapi.py doit tourner sur le port 8000

import requests

# Adresse du serveur local
URL_SERVEUR = "http://127.0.0.1:8000"


# Verification que le serveur est operationnel
print("=== Verification du serveur ===")
try:
    r = requests.get(f"{URL_SERVEUR}/sante", timeout=10)
    if r.status_code == 200:
        print(f"Serveur OK : {r.json()['message']}")
    else:
        print(f"Le serveur a repondu avec le code {r.status_code}")
except requests.ConnectionError:
    print("Impossible de se connecter au serveur.")
    print("Assurez-vous que le serveur est lance avec :")
    print("  python -m uvicorn code.mini_api_fastapi:app --reload --port 8000")
    raise SystemExit(1)
except requests.Timeout:
    print("Le serveur met trop de temps a repondre (timeout).")
    print("Verifiez que FastAPI est bien demarre et disponible sur le port 8000.")
    raise SystemExit(1)

print()

# Boucle interactive : l'utilisateur pose des questions
print("=== Client interactif ===")
print("Posez vos questions au serveur local.")
print("Commandes : 'historique', 'reset', 'quitter'.")
print()


while True:
    question = input("Votre question : ").strip()
    commande = question.lower()

    if commande == "quitter":
        print("Au revoir.")
        break

    if commande == "historique" or commande == "logs":
        try:
            r = requests.get(f"{URL_SERVEUR}/historique", timeout=10)
            if r.status_code == 200:
                messages = r.json().get("messages", [])
                if not messages:
                    print("\nHistorique vide.\n")
                else:
                    print("\nHistorique complet :")
                    for i, msg in enumerate(messages, start=1):
                        print(f"{i:02d}. [{msg['role']}] {msg['content']}")
                    print()
            else:
                print(f"Erreur du serveur : {r.status_code}")
        except requests.ConnectionError:
            print("Connexion perdue avec le serveur.")
        except requests.Timeout:
            print("Le serveur ne repond pas a temps. Reessayez dans quelques secondes.")
        continue

    if commande == "reset":
        try:
            r = requests.post(f"{URL_SERVEUR}/reset", timeout=10)
            if r.status_code == 200:
                print("Historique reinitialise.\n")
            else:
                print(f"Erreur du serveur : {r.status_code}")
        except requests.ConnectionError:
            print("Connexion perdue avec le serveur.")
        except requests.Timeout:
            print("Le serveur ne repond pas a temps. Reessayez dans quelques secondes.")
        continue

    if not question:
        print("Veuillez entrer une question.")
        continue

    # Envoi de la question au serveur local via une requete POST
    try:
        r = requests.post(
            f"{URL_SERVEUR}/question",
            json={"question": question},
            timeout=30,
        )

        if r.status_code == 200:
            data = r.json()
            print(f"\nReponse : {data['reponse']}")
            print(f"Tokens utilises : {data['tokens_utilises']}")

            # Affiche l'historique complet apres chaque reponse.
            h = requests.get(f"{URL_SERVEUR}/historique", timeout=10)
            if h.status_code == 200:
                messages = h.json().get("messages", [])
                print("\nHistorique complet :")
                for i, msg in enumerate(messages, start=1):
                    print(f"{i:02d}. [{msg['role']}] {msg['content']}")
            else:
                print("Impossible de recuperer l'historique.")
        else:
            print(f"Erreur du serveur : {r.status_code}")

    except requests.ConnectionError:
        print("Connexion perdue avec le serveur.")
    except requests.Timeout:
        print("Le serveur ne repond pas a temps. Reessayez dans quelques secondes.")

    print()
