import httpx
import re


def extraire_gare(question: str) -> str:
    # Cherche un nom de gare/ville après "gare de", "depuis", "à", "pour"
    match = re.search(r"(?:gare de|depuis|à|pour|train pour|train de)\s+([A-ZÀ-Üa-zà-ü\- ]+?)(?:\s*\?|$)", question)
    if match:
        return match.group(1).strip()
    return None


async def fetch(question: str) -> str:
    gare = extraire_gare(question)

    # Si on trouve une gare, on cherche ses infos sur l'open data SNCF
    if gare:
        async with httpx.AsyncClient() as client:
            rep = await client.get(
                "https://ressources.data.sncf.com/api/explore/v2.1/catalog/datasets/referentiel-gares-voyageurs/records",
                params={
                    "where": f'gare_alias_libelle_nonotes like "{gare}"',
                    "limit": 3,
                    "select": "gare_alias_libelle_nonotes,departement_libellemin,commune_libellemin",
                },
            )
            rep.raise_for_status()
            data = rep.json()

        if data["total_count"] == 0:
            return f"Aucune gare trouvée pour '{gare}'."

        lignes = [f"Gares SNCF correspondant à '{gare}' :"]
        for g in data["results"]:
            nom = g.get("gare_alias_libelle_nonotes", "?")
            dept = g.get("departement_libellemin", "?")
            commune = g.get("commune_libellemin", "?")
            lignes.append(f"- {nom} ({commune}, {dept})")
        return "\n".join(lignes)

    # Sans gare précise, on retourne les infos générales sur le trafic
    async with httpx.AsyncClient() as client:
        rep = await client.get(
            "https://ressources.data.sncf.com/api/explore/v2.1/catalog/datasets/tgvmax/records",
            params={"limit": 3, "select": "origine,destination,heure_depart,heure_arrivee"},
        )
        rep.raise_for_status()
        data = rep.json()

    lignes = ["Exemples de trajets TGV Max disponibles :"]
    for t in data["results"]:
        lignes.append(f"- {t['origine']} → {t['destination']} | départ {t['heure_depart']} arrivée {t['heure_arrivee']}")
    return "\n".join(lignes)
