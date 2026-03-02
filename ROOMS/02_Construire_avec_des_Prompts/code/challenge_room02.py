# Script 05 - Assistant pédagogique interactif
# Room 02 - Construire avec des prompts
# Complétez les parties marquées "# A COMPLETER"

import json
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from utils import creer_client, MODELE

client = creer_client()


def quizz(sujet):

    # file = "./ROOMS/02_Construire_avec_des_Prompts/challenge_room02_prompt.txt"
    # with open(file, "r", encoding="utf-8") as f:
    #     prompt = f.read()
    prompt = f"""
En tant qu'expert de la culture général, tu vas générer un quizz de 5 questions pour un utilisateur par rapport au sujet demandé : {sujet}.
Il faut trier aléatoirement les réponses
Réponds UNIQUEMENT avec un objet JSON valide, sans texte avant ni après.
Utilise exactement cette structure : 
{{
  "sujet": "...",
  "questions": [
    {{
      "numero": 1,
      "question": "...",
      "options": ["A. ...", "B. ...", "C. ...", "D. ..."],
      "bonne_reponse": "A"
    }}
  ]
}}
"""
    reponse = client.chat.completions.create(
        model=MODELE,
        messages=[{"role": "user", "content": prompt }],
        temperature=0.2,
        max_tokens=600
    )
    return reponse.choices[0].message.content


print("=== Générateur de quizz ===")
print("Entrez un sujet pour obtenir un quizz de 5 questions")
print("Tapez 'quitter' pour arrêter.")
print()

while True:

    sujet = input("Sujet à interroger : ").strip()

    if sujet.lower() == "quitter":
        print("Au revoir !")
        break

    if not sujet:
        print("Veuillez entrer un sujet.")
        continue

    result = quizz(sujet)
    print(result)

    try:
        answer_raw = json.loads(result)

        print("=== JSON valide - Contenu extrait ===")
        print(f"Titre : {answer_raw['sujet']}")
        print()

        cpt = 0

        for question in answer_raw['questions']:
            print(f"Question {question['numero']}")
            print(question['question'])

            for option in question['options']:
                print(option)

            choice = input("Votre réponse : ").strip().upper()

            if choice == question['bonne_reponse']:
                print("\nBonne réponse !")
                cpt += 1
            else:
                print("Mauvaise réponse !")

            print()

        print(f"Score final : {cpt} / {len(answer_raw['questions'])}")
        print("\n" + "-"*50 + "\n")

    except json.JSONDecodeError as e:
        print("Erreur : le modèle n'a pas retourné du JSON valide.")
        print(f"Détail de l'erreur : {e}")