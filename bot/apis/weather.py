import httpx
import re


def extraire_ville(question: str) -> str:
    # Cherche un nom de ville après "à", "de", "sur", "pour"
    match = re.search(r"(?:à|a|de|sur|pour)\s+([A-ZÀ-Üa-zà-ü\-]+)", question)
    if match:
        return match.group(1)
    return "Paris"  # ville par défaut


async def fetch(question: str) -> str:
    ville = extraire_ville(question)
    async with httpx.AsyncClient() as client:
        rep = await client.get(
            f"https://wttr.in/{ville}",
            params={"format": "j1"},
            headers={"Accept": "application/json"},
        )
        rep.raise_for_status()
        data = rep.json()

    actuel = data["current_condition"][0]
    desc = actuel["weatherDesc"][0]["value"]
    temp = actuel["temp_C"]
    ressenti = actuel["FeelsLikeC"]
    humidite = actuel["humidity"]

    return (
        f"Météo à {ville} :\n"
        f"- Conditions : {desc}\n"
        f"- Température : {temp}°C (ressenti {ressenti}°C)\n"
        f"- Humidité : {humidite}%"
    )
