import httpx
from datetime import date


async def fetch(query: str) -> str:
    year = date.today().year
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"https://date.nager.at/api/v3/PublicHolidays/{year}/FR")
        resp.raise_for_status()
        holidays = resp.json()

    lines = [f"Jours fériés en France ({year}) :"]
    for h in holidays:
        lines.append(f"- {h['date']} : {h['localName']}")
    return "\n".join(lines)
