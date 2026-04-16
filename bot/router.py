from apis import holidays, weather, search, transport

ROUTES = [
    (["jour férié", "jours fériés", "férié", "fériés", "pont"], holidays.fetch),
    (["météo", "meteo", "temps qu'il", "quel temps", "fait-il", "fait il", "pluie", "soleil", "température", "neige"], weather.fetch),
    (["train", "sncf", "gare", "trajet", "tgv", "ter", "transport", "comment aller", "comment je vais", "comment je vien", "comment venir", "aller à", "me rendre", "itinéraire", "bus", "métro", "rer", "comment je me rends"], transport.fetch),
    (["cherche", "recherche", "qu'est-ce que", "c'est quoi", "définition", "explique moi", "meilleur prix", "moins cher", "comment trouver", "comment faire", "astuce"], search.fetch),
]


async def router(question: str):
    """
    Regarde si la question contient un mot-clé connu.
    Retourne le resultatde l'API si une API correspond.
    """
    question_minuscule = question.lower()

    for mots_cles, fonction in ROUTES:
        for mot in mots_cles:
            if mot in question_minuscule:
                contexte = await fonction(question)
                return contexte

    return None
