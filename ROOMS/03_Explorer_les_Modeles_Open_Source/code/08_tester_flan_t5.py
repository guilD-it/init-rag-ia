# Script 08 - Interroger Flan-T5-large via Inference Providers (Hugging Face)
# Room 03 - Explorer les modèles open source

import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

# ID du modele Flan-T5
# C'est un modele instruction cree par Google, beaucoup plus petit que Mistral ou Llama 2
MODEL_ID = "google/flan-t5-large"

# Le même prompt que pour les autres modèles
prompt = "Explique en 3 phrases simples ce qu'est une base de données relationnelle."

print("=== Interrogation de Flan-T5-large ===")
print(f"Prompt : {prompt}")
print("En attente de la réponse...")
print()

if not HF_TOKEN or HF_TOKEN.startswith("hf_votre_"):
    print("HF_TOKEN manquant ou invalide dans le fichier .env")
    print("Ajoutez un token Hugging Face valide : HF_TOKEN=hf_...")
    print("Permission requise : Make calls to Inference Providers.")
    raise SystemExit(1)

client = InferenceClient(api_key=HF_TOKEN, timeout=60)

try:
    texte_genere = client.text_generation(
        prompt=prompt,
        model=MODEL_ID,
        max_new_tokens=250,
        temperature=0.3
    )
    print("=== Réponse de Flan-T5-large ===")
    print(texte_genere)
    print()
    print("Note : Flan-T5 est 10 fois plus petit que Mistral et Llama 2.")
    print("Observez la différence de longueur et de détail dans la réponse.")
except Exception as e:
    status_code = getattr(getattr(e, "response", None), "status_code", None)
    if status_code == 401:
        print("Erreur 401 : token HF invalide ou absent.")
    elif status_code == 403:
        print("Erreur 403 : token sans permission Inference Providers.")
    elif status_code == 429:
        print("Erreur 429 : quota/limite atteinte. Reessayez plus tard.")
    elif status_code == 503:
        print("Erreur 503 : modele en cours de chargement, reessayez dans 30 secondes.")
    else:
        print(f"Erreur lors de l'appel API : {e}")
