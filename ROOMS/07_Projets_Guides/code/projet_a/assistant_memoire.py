# Projet A - Assistant mémoire avec historique de conversation
# Room 07 - Projets guidés

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))

from utils import creer_client, MODELE

client = creer_client()

MESSAGE_SYSTEME = {
    "role": "system",
    "content": (
        "Tu es un assistant pédagogique bienveillant et patient. "
        "Tu expliques les concepts de façon simple, avec des exemples concrets. "
        "Tu te souviens de ce que l'utilisateur a dit précédemment dans la conversation."
    )
}

historique = [MESSAGE_SYSTEME]
MAX_ECHANGES = 10


def ajouter_au_contexte(role, contenu):
    """
    Ajoute un message à l'historique et limite la taille de l'historique.

    A COMPLETER :
    - Ajouter le nouveau message à la fin de l'historique
    - Si le nombre de messages (hors message system) dépasse MAX_ECHANGES * 2,
      supprimer les 2 messages les plus anciens (après le message system)
    """
    historique.append({"role": role, "content": contenu})

    # On conserve toujours le message system en position 0.
    # Si on dépasse la limite de paires user/assistant, on retire la plus ancienne paire.
    while len(historique) - 1 > MAX_ECHANGES * 2:
        del historique[1:3]


def envoyer_message(texte_utilisateur):
    """
    Envoie le message de l'utilisateur au LLM avec l'historique complet
    et retourne la réponse.

    A COMPLETER :
    1. Ajouter le message utilisateur à l'historique
    2. Envoyer l'historique complet au LLM (model=MODELE)
    3. Récupérer la réponse
    4. Ajouter la réponse de l'assistant à l'historique
    5. Retourner le texte de la réponse
    """
    ajouter_au_contexte("user", texte_utilisateur)

    completion = client.chat.completions.create(
        model=MODELE,
        messages=historique
    )
    reponse = completion.choices[0].message.content

    ajouter_au_contexte("assistant", reponse)
    return reponse


# --- Programme principal ---
print("=== Assistant mémoire ===")
print("Posez vos questions. L'assistant se souvient de la conversation.")
print("Tapez 'quitter' pour arrêter.")
print("Tapez 'historique' pour voir les messages en mémoire.")
print()

while True:
    texte = input("Vous : ").strip()

    if texte.lower() == "quitter":
        print("Au revoir.")
        break

    if texte.lower() == "historique":
        print(f"\n--- Historique ({len(historique)} messages) ---")
        for msg in historique:
            role = msg["role"].upper()
            contenu = msg["content"][:80]
            print(f"  [{role}] {contenu}...")
        print()
        continue

    if not texte:
        continue

    reponse = envoyer_message(texte)
    if reponse:
        print(f"\nAssistant : {reponse}\n")
