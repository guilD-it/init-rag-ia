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
        "Tu te souviens de ce que l'utilisateur a dit précédemment dans la conversation. "
        "Tu utilises la mémoire seulement si elle est pertinente pour la question actuelle. "
        "Si une question est ambiguë ou contient une faute, demande d'abord une clarification."
    )
}

historique = [MESSAGE_SYSTEME]
NB_ECHANGES_A_RESUMER = 5
RESUME_PREFIXE = "Mémoire longue (résumé des 5 premiers échanges) : "
resume_premiers_echanges_genere = False


def ajouter_au_contexte(role, contenu):
    """
    Ajoute un message à l'historique (sans suppression)
    et met à jour un résumé des 5 premiers échanges.
    """
    historique.append({"role": role, "content": contenu})
    mettre_a_jour_resume_memoire_longue()


def _premiers_messages_a_resumer():
    messages_conversation = [
        msg for msg in historique if msg["role"] in ("user", "assistant")
    ]
    return messages_conversation[: NB_ECHANGES_A_RESUMER * 2]


def _resumer_messages(messages_a_resumer):
    conversation = "\n".join(
        f"{msg['role'].upper()} : {msg['content']}" for msg in messages_a_resumer
    )

    completion = client.chat.completions.create(
        model=MODELE,
        messages=[
            {
                "role": "system",
                "content": (
                    "Résume fidèlement ces échanges en français. "
                    "Garde les informations durables: objectifs, préférences, contexte."
                ),
            },
            {"role": "user", "content": conversation},
        ],
    )
    return completion.choices[0].message.content


def mettre_a_jour_resume_memoire_longue():
    global resume_premiers_echanges_genere

    if resume_premiers_echanges_genere:
        return

    messages_a_resumer = _premiers_messages_a_resumer()

    # On attend d'avoir 5 échanges complets (10 messages user/assistant).
    if len(messages_a_resumer) < NB_ECHANGES_A_RESUMER * 2:
        return

    resume = _resumer_messages(messages_a_resumer)
    message_resume = {
        "role": "assistant",
        "content": (
            RESUME_PREFIXE
            + resume
            + " (Contexte mémorisé, à utiliser seulement si pertinent.)"
        ),
    }

    # Le résumé est placé juste après le message système principal.
    if len(historique) > 1 and historique[1]["role"] == "assistant" and historique[1][
        "content"
    ].startswith(RESUME_PREFIXE):
        historique[1] = message_resume
    else:
        historique.insert(1, message_resume)

    resume_premiers_echanges_genere = True
    print("\n[Memoire] Résumé des 5 premiers échanges généré.\n")


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
