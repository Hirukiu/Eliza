import asyncio
from duckduckgo_search import DDGS


async def fetch(question: str) -> str:
    # duckduckgo_search est synchrone, on l'exécute dans un thread séparé
    def rechercher():
        with DDGS() as ddgs:
            return list(ddgs.text(question, max_results=3))

    resultats = await asyncio.to_thread(rechercher)

    if not resultats:
        return "Aucun résultat trouvé."

    lignes = ["Résultats de recherche :"]
    for r in resultats:
        lignes.append(f"\n- {r['title']}\n  {r['body']}")
    return "\n".join(lignes)
