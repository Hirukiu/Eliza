### Architechture du projet
```text
Utilisateur
       │
       ▼ (1 Pose une question via chat)
Interface : Serveur Discord
       │
       ▼ (2 Transmet le message via API Discord)
Le Serveur Local
       │
       ├─► Script Python (bot.py avec discord.py)
       │         │
       │         ├─► Base de Connaissances (data.txt)
       │         │    (3 Le script lit les règles de l'entreprise)
       │         │
       │         ├─► API Externe
       │         │    (3bis Ex : Le script va chercher les horaires de bus en temps réel)
       │         │
       │         ▼ (4 Assemble la question + le contexte RH + les données API)
       │
       └──► Moteur IA : Ollama
                 (5 Analyse tout le bloc et génère la réponse parfaite)
                 │
                 ▼ (6 Renvoie le texte généré au script Python)
                   
Interface : Serveur Discord (Affiche la réponse à l'employé)
```