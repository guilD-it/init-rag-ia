# Theory - Room 03 : Explorer les modèles open source

## Problème concret de départ

Vous savez maintenant interroger un LLM via une API gratuite (comme Groq). Mais il existe des centaines de modeles open source, disponibles librement sur des plateformes dediees. Comment les trouver, les tester, et choisir celui qui convient a votre besoin ?

---

## Notion 1 - Le modèle de base

**Définition** : un modèle de base (ou "base model") est un modèle entraîné uniquement à prédire le mot suivant dans un texte. Il n'a pas été entraîné à répondre à des questions ni à suivre des instructions.

**Exemple** : si vous envoyez "Quelle est la capitale de la France ?" à un modèle de base, il pourrait répondre :

```
Quelle est la capitale de l'Allemagne ? Quelle est la capitale de l'Italie ?
```

Il complète le texte comme s'il devait écrire la suite d'un document contenant des questions. Il ne répond pas à la question.

**Ce qu'il faut retenir** : un modèle de base n'est pas conçu pour dialoguer. Il prolonge du texte.

---

## Notion 2 - Le modèle instruction (ou modèle "chat")

**Définition** : un modèle instruction est un modèle de base qui a subi un entraînement supplémentaire pour apprendre à suivre des instructions et à produire des réponses utiles. Cette étape s'appelle le "fine-tuning" (affinage).

**Exemple** : le même prompt "Quelle est la capitale de la France ?" envoyé à un modèle instruction donne :

```
La capitale de la France est Paris.
```

**Comment les reconnaître** : les modèles instruction portent souvent des suffixes comme "Instruct", "Chat" ou "it" dans leur nom.
- `Mistral-7B` → modèle de base
- `Mistral-7B-Instruct-v0.1` → modèle instruction

---

## Notion 3 - La taille d'un modèle

**Définition** : la taille d'un modèle se mesure en nombre de paramètres. Un paramètre est un coefficient numérique que le modèle a appris pendant son entraînement. Plus un modèle a de paramètres, plus il est capable de capter des relations complexes dans le texte, mais plus il consomme de mémoire et de temps de calcul.

**Ordres de grandeur** :

| Modèle | Paramètres | Mémoire approximative |
|--------|-----------|----------------------|
| Flan-T5-base | 250 millions | ~500 Mo |
| Flan-T5-large | 780 millions | ~1.5 Go |
| Mistral-7B | 7 milliards | ~14 Go |
| Llama 2 13B | 13 milliards | ~26 Go |

**Ce qu'il faut retenir** : un modele plus gros n'est pas toujours meilleur pour votre tache. Un petit modele bien affine peut surpasser un grand modele generaliste sur une tache precise.

**Note** : ces chiffres sont indicatifs et evoluent rapidement. De nouveaux modeles sortent chaque mois avec des performances ameliorees. Verifiez les pages officielles des modeles pour les donnees a jour.

---

## Notion 4 - Hugging Face Hub

**Définition** : Hugging Face est une plateforme en ligne (https://huggingface.co) qui héberge des milliers de modèles de machine learning. On peut y télécharger des modèles pour les exécuter localement ou les interroger via une API d'inférence gratuite.

**Exemple** : sur Hugging Face, chaque modèle a une page avec :
- Le nom du modèle (ex. `mistralai/Mistral-7B-Instruct-v0.1`)
- Sa documentation (comment l'utiliser, quelles tâches)
- Un espace de test en ligne (parfois)
- Le nombre de téléchargements et d'avis

**Ce qu'il faut retenir** : Hugging Face est la bibliothèque de référence pour les modèles open source. Vous l'utiliserez régulièrement dans la suite du cours.

---

## Notion 5 - L'inférence via API

**Définition** : l'inférence est le processus qui consiste à utiliser un modèle entraîné pour produire une réponse à partir d'une entrée. L'inférence via API signifie que le modèle est hébergé sur un serveur distant et que vous l'interrogez via une requête HTTP, sans avoir à le télécharger.

**Exemple** : au lieu de télécharger 14 Go pour Mistral-7B, vous appelez l'API Inference Providers de Hugging Face (routeur `https://router.huggingface.co/v1`) avec votre token `HF_TOKEN` et vous recevez la réponse en retour.

**Avantage** : aucune installation lourde, pas besoin de GPU.
**Inconvénient** : le temps de réponse dépend de la charge du serveur, et l'API gratuite a des limites d'utilisation.

---

## Les 3 modèles que vous allez comparer

| Modèle | Créateur | Paramètres | Type |
|--------|----------|-----------|------|
| Mistral-7B-Instruct | Mistral AI | 7 milliards | Instruction |
| Llama 2 7B Chat | Meta | 7 milliards | Instruction |
| Flan-T5-large | Google | 780 millions | Instruction |

Ces trois modèles ont des architectures et des tailles différentes. La comparaison sur un même prompt vous permettra d'observer concrètement ces différences.
