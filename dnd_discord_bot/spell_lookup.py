import aiohttp

BASE_URL = "https://www.dnd5eapi.co/api/spells/"

async def fetch_spell(name: str):
    slug = name.lower().replace(" ", "-")
    url = f"{BASE_URL}{slug}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return {
                    "name": data["name"],
                    "level": data["level"],
                    "school": data["school"]["name"],
                    "casting_time": data["casting_time"],
                    "range": data["range"],
                    "duration": data["duration"],
                    "desc": data["desc"][0] if data["desc"] else "No description.",
                    "components": data["components"],
                    "ritual": data["ritual"],
                    "concentration": data["concentration"],
                    "higher_level": data["higher_level"][0] if data["higher_level"] else "No higher level information."
                }
            else:
                return None
