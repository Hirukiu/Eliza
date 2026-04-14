# Rapport de Projet : Eliza


**Auteurs :** Kamil AKERRAMAMOU, Laurent COSTA, Mathieu JIN

**Projet :** Conception d'un Assistant Virtuel d'Entreprise

---

## Sommaire
1. [Objectif du projet](#objectif-du-projet)
2. [Cibles et Besoin](#cibles-et-besoin)
3. [Fonctionnalités Techniques](#fonctionnalités-techniques)
4. [Modèle Économique](#modèle-économique)
    * [Retour sur Investissement (ROI)](#retour-sur-investissement-roi)
    * [Performance Indicators (KPIs)](#performance-indicators-kpis)
5. [Étude d'Impact Éthique et Responsabilité](#étude-dimpact-éthique-et-responsabilité)
    * [Transparence et Effet ELIZA](#transparence-et-effet-eliza)
    * [Confidentialité et Données](#confidentialité-et-données)
    * [Gestion du Mal-être au Travail](#gestion-du-mal-être-au-travail)
6. [Bibliographie et Sources](#bibliographie-et-sources-de-létude)

---

## Objectif du projet

Le projet Eliza
 est un chatbot pour faciliter l'intégration des nouveaux employée et fluidifier les échanges entre les employés et les services RH et informatiques. Eliza
 est connectée en temps réel aux données de l'entreprise ainsi qu'aux services locaux (horaires de transports, restauration), il centralise l'information pour simplifier et améliorer la qualité de vie au travail.


## Cibles et Besoin

* **Les nouveaux employés :**
    * **Profil :** Nouvelles recrues en phase d'intégration. Elles découvrent l'environnement de travail et les outils de l'entreprise.
    * **Besoins :** S'adapter rapidement sans avoir à demander de l'aide pour des problèmes mineurs et créer une routine de travail qui leur plaît.

* **Les employés réguliers :**
    * **Profil :** Employés déjà familiers avec l'entreprise, mais sui sont souvent confrontés à des petit problèmes qui interrompent leur journée de travail.
    * **Besoins :** Résoudre leurs problèmes quotidiens instantanément pour rester concentrés sur leurs missions, et accéder rapidement aux informations de l'entreprise.

* **Les Équipes Support (RH/IT):**
    * **Profil** Équipes chargées d'assister les employés au quotidien qui souvent surchargées par beaucoup de questions simples et répétitives
    * **Besoin** Filtrer les demandes récurrentes pour gagner du temps et se concentrer sur des dossiers complexes nécessitant une expertise technique ou humaine.


## Fonctionnalités Techniques

[explication du fonctionnement du chatbot]

* **Interface utilisateur :** Le chatbot sera déployé sur Discord afin de s'intégrer naturellement aux outils de travail existants.
* **Moteur d'IA :** Les réponses sont générées par Ollama, ajusté pour adopter un ton professionnel et bienveillant.
* **Les API :** 
    


## Modèle Économique
### Retour sur Investissement (ROI)
L'intégration de Eliza
 crée de la valeur à plusieurs niveaux :

1. **Gain financier :** En automatisant la résolution des requêtes récurrentes , le chatbot réduit drastiquement le volume de tickets d'assistance. Ce filtrage permet de libérer un temps précieux aux experts RH et IT, qui peuvent alors se concentrer sur des tâches importantes. Le coût humain du support interne est ainsi considérablement optimisé.
2. **Gain de temps :** Grâce à un accès instantané et autonome à l'information, les nouvelles recrues ne restent plus bloquées dans l'attente d'une réponse de leur manager ou du support. Cette fluidité accélère leur montée en compétences, leur permettant d'être pleinement opérationnelles et productives beaucoup plus rapidement.

![Graphique représentant le prix des tickets](./img/ticket_price_chart.png)

### Performance Indicators (KPIs)

Pour mesurer le succès de notre solution, nous suivrons les indicateurs suivants :
* **Taux de déflexion :** Réduction des tickets d'assistance ouverts auprès des RH/IT.
* **Temps de résolution moyen :** Passage de 8-9 heures à quelques minutes.
* **Satisfaction Employé :** Note moyenne attribuée par les utilisateurs en fin d'interaction.
* **Taux d'adoption :** Pourcentage des employés utilisant le chatbot mensuellement.

![Graphique représentant le temps passée sur un ticket](./img/MTTR_chart.png)


## Étude d'Impact Éthique et Responsabilité

l'effet ELIZA est le fait de prendre un chatbot pour un 

### Transparence et Effet ELIZA
* Pour éviter toute confusion quant à la nature du chatbot, l'interface rappellera clairement qu'il s'agit d'une intelligence artificielle. Il n'a pas vocation à simuler des émotions humaines ou à remplacer le lien social.

### Confidentialité et Données
* Les requêtes des employés seront [anonymisées / traitées de manière sécurisée] et ne seront pas utilisées pour entraîner des modèles externes. 

### Gestion du Mal-être au Travail
* **Protocole d'urgence :** Si l'IA détecte des termes liés à la détresse psychologique (ex: "burn-out", "harcèlement", "dépression"), elle suspendra sa logique de résolution de problème.
* **Action :** Le chatbot répondra avec une formulation neutre et empathique et fournira immédiatement les contacts humains appropriés (médecine du travail, numéro d'urgence RH, représentants du personnel).

---


## Bibliographie et Sources de l'étude

**Données financières et KPIs (Support IT / RH) :**

* **Help Desk Institute & MetricNet :** *Metric of the Month: Cost per Ticket* et *Mean Time to Resolve*. Benchmarks mondiaux sur le coût de traitement et le temps de résolution des tickets internes.
* **Zendesk :** *Support Benchmarks - AI and Ticket Deflection Best Practices*. Études sur l'impact de l'intelligence artificielle sur le taux de déflexion et la satisfaction collaborateur.

**Ressources Techniques et APIs (Open Data) :**
* **Navitia.io :** Portail Open Data de la mobilité, utilisé pour l'agrégation des données de transports en commun en temps réel.
* **OpenStreetMap (via l'API Overpass) :** Base de données cartographique libre et collaborative, utilisée pour la géolocalisation des infrastructures de restauration locales.
* **Nager.Date :** API Open Source publique recensant le calendrier officiel des jours fériés mondiaux.

**Éthique et Psychologie :**
* **Weizenbaum, Joseph (1966) :** Travaux fondateurs sur le programme *ELIZA* et le biais psychologique d'anthropomorphisme appliqué aux machines.
