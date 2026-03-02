# Script 05 - Assistant pédagogique interactif
# Room 02 - Construire avec des prompts
# Complétez les parties marquées "# A COMPLETER"

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from utils import creer_client, MODELE

client = creer_client()


def expliquer_sujet(sujet):
    """
    Envoie un sujet au LLM avec un rôle de professeur bienveillant
    et retourne une explication adaptée à un débutant.
    """
    # A COMPLETER : construisez le prompt structuré
    # Il doit contenir :
    #   - Un rôle (professeur bienveillant pour étudiants sans base IA)
    #   - Le sujet à expliquer
    #   - Une contrainte de format (3 paragraphes : définition, analogie, exemple)
    #   - Une contrainte de longueur (maximum 150 mots)
    
    prompt_explication = (
        # A COMPLETER
        f"Explique le sujet suivant : {sujet} .En tant que professeur bienveillant pour étudiants sans base IA, la réponse doit avoir 3 paragraphaque qui suit une structure définition, analogie et exemple et 150 mots maximums"  # Version basique à améliorer
    )

    reponse = client.chat.completions.create(
        model=MODELE,
        messages=[{"role": "user", "content": prompt_explication}],
        temperature=0.3,
        max_tokens=300
    )
    return reponse.choices[0].message.content


def proposer_exercice(sujet):
    """
    Propose un exercice pratique sur le sujet donné.
    """
    # A COMPLETER : construisez un prompt qui demande au modèle de créer
    # un exercice pratique simple sur le sujet fourni.
    prompt_exercice = (
        # A COMPLETER
        f"Propose un exercice sur le sujet suivant : {sujet}"  # Version basique à améliorer
    )

    reponse = client.chat.completions.create(
        model=MODELE,
        messages=[{"role": "user", "content": prompt_exercice}],
        temperature=0.5,
        max_tokens=200
    )
    return reponse.choices[0].message.content


# --- Programme principal ---
print("=== Assistant pédagogique ===")
print("Entrez un sujet pour obtenir une explication et un exercice.")
print("Tapez 'quitter' pour arrêter.")
print()

while True:
    sujet = input("Sujet à apprendre : ").strip()

    if sujet.lower() == "quitter":
        print("Au revoir !")
        break

    if not sujet:
        print("Veuillez entrer un sujet.")
        continue

    print("\n--- Explication ---")
    explication = expliquer_sujet(sujet)
    print(explication)

    print("\n--- Exercice ---")
    exercice = proposer_exercice(sujet)
    print(exercice)

    print("\n" + "-"*50 + "\n")
