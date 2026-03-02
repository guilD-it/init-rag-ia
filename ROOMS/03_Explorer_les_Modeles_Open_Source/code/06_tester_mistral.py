# Script 06 - Interroger Mistral-7B-Instruct via Inference Providers (Hugging Face)
# Room 03 - Explorer les modèles open source

import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# Chargement du token Hugging Face depuis .env
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

# ID du modèle instruction Mistral sur Hugging Face
MODEL_ID = "mistralai/Mistral-7B-Instruct-v0.3:fastest"

# Le prompt à envoyer - utilisez le même prompt pour les 3 modèles
prompt = "Explique en 3 phrases simples ce qu'est une base de données relationnelle."

print("=== Interrogation de Mistral-7B-Instruct ===")
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
    completion = client.chat.completions.create(
        model=MODEL_ID,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=250
    )
    texte_genere = completion.choices[0].message.content
    print("=== Réponse de Mistral-7B-Instruct ===")
    print(texte_genere)
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
