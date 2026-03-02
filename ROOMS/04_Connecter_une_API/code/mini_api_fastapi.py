# mini_api_fastapi.py - Mini serveur FastAPI qui interroge un LLM
# Room 04 - Connecter une API
# Lancer avec : python -m uvicorn code.mini_api_fastapi:app --reload --port 8000

import os
import sys

from fastapi import FastAPI
from pydantic import BaseModel

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from utils import MODELE, creer_client

client = creer_client()
app = FastAPI(title="Mini Assistant LLM", version="1.0")

MAX_ECHANGES = 10
MAX_MESSAGES = MAX_ECHANGES * 2
SYSTEM_MESSAGE = {"role": "system", "content": "Tu es un assistant concis et pedagogique."}

# Historique en memoire, maintenu cote serveur.
historique_messages: list[dict[str, str]] = []


class QuestionRequest(BaseModel):
    question: str


class ReponseResult(BaseModel):
    question: str
    reponse: str
    tokens_utilises: int


class Message(BaseModel):
    role: str
    content: str


class HistoriqueResponse(BaseModel):
    messages: list[Message]


@app.post("/question", response_model=ReponseResult)
def poser_question(req: QuestionRequest):
    """Recoit une question, l'envoie au LLM et retourne la reponse."""
    user_message = {"role": "user", "content": req.question}

    completion = client.chat.completions.create(
        model=MODELE,
        messages=[SYSTEM_MESSAGE, *historique_messages, user_message],
        temperature=0.3,
        max_tokens=300,
    )

    reponse_modele = completion.choices[0].message.content or ""
    assistant_message = {"role": "assistant", "content": reponse_modele}

    historique_messages.extend([user_message, assistant_message])
    if len(historique_messages) > MAX_MESSAGES:
        del historique_messages[:-MAX_MESSAGES]

    tokens = completion.usage.total_tokens if completion.usage else 0
    return ReponseResult(
        question=req.question,
        reponse=reponse_modele,
        tokens_utilises=tokens,
    )


@app.get("/historique", response_model=HistoriqueResponse)
def get_historique():
    """Retourne la liste des messages user/assistant en memoire."""
    return HistoriqueResponse(messages=historique_messages)


@app.post("/reset", response_model=HistoriqueResponse)
def reset_historique():
    """Vide l'historique de conversation."""
    historique_messages.clear()
    return HistoriqueResponse(messages=[])


@app.get("/sante")
def verifier_sante():
    """Retourne un message simple pour verifier que le serveur est operationnel."""
    return {"statut": "ok", "message": "Le serveur fonctionne correctement."}
