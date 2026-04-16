# Eliza — Assistant Virtuel d'Entreprise

**Auteurs :** Kamil AKERRAMAMOU, Laurent COSTA, Mathieu JIN

Eliza est un chatbot RH déployé sur Discord. Il répond aux questions des employés sur la vie de l'entreprise (congés, IT, cantine, transports) en combinant une base documentaire interne et des APIs externes, le tout propulsé par un modèle IA local via Ollama.

---

## Architecture

```text
Utilisateur
       │
       ▼ (Pose une question via Discord)
Interface : Serveur Discord
       │
       ▼ (Transmet le message via API Discord)
Le Serveur Local
       │
       ├─► Script Python (discord_bot.py avec discord.py)
       │         │
       │         ├─► Router (router.py)
       │         │    ├─► API Météo       (wttr.in)
       │         │    ├─► API Transport   (SNCF Open Data)
       │         │    ├─► API Jours fériés (date.nager.at)
       │         │    └─► API Recherche   (DuckDuckGo)
       │         │
       │         └─► RAG (ChromaDB + SentenceTransformer)
       │              (recherche dans la base documentaire interne)
       │
       ▼ (Transmet la question)
Moteur IA : Ollama (phi3:mini)
       │
       ▼ (Génère la réponse)
Interface : Serveur Discord (Affiche la réponse à l'employé)
```

---

## Prérequis

- Python 3.10+
- [Ollama](https://ollama.com) installé et le modèle `phi3:mini` téléchargé
- Un token de bot Discord

---

## Installation

**1. Cloner le projet**
```bash
git clone <url-du-repo>
cd eliza
```

**2. Créer et activer l'environnement virtuel**
```bash
python -m venv bot/venv
source bot/venv/bin/activate
```

**3. Installer les dépendances**
```bash
pip install discord.py httpx duckduckgo-search ollama chromadb sentence-transformers langchain-core
```

**4. Créer le fichier `.env`**
```bash
# dans le dossier bot/
echo "DISCORD_TOKEN=ton_token_ici" > bot/.env
```

**5. Télécharger le modèle Ollama**
```bash
ollama pull phi3:mini
```

**6. Indexer la base documentaire**
```bash
cd bot
python rag/ingest.py
```

---

## Lancer le bot

```bash
cd bot
source venv/bin/activate
python discord_bot.py
```

---

## Structure du projet

```
eliza/
├── bot/
│   ├── apis/
│   │   ├── holidays.py     # API jours fériés (date.nager.at)
│   │   ├── weather.py      # API météo (wttr.in)
│   │   ├── search.py       # API recherche (DuckDuckGo)
│   │   └── transport.py    # API transport (SNCF Open Data)
│   ├── rag/
│   │   ├── ingest.py       # Indexation des documents dans ChromaDB
│   │   └── retriever.py    # Recherche sémantique
│   ├── data.txt            # Base documentaire interne (FAQ entreprise)
│   ├── router.py           # Routage vers API ou RAG selon la question
│   └── discord_bot.py      # Point d'entrée du bot Discord
├── landing_page/
│   ├── index.html
│   └── style.css
└── rapports/
    └── rapport.md
```
