import aiohttp

async def fetch_raw_html(target_url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(target_url) as response:
            response.raise_for_status()
            return await response.text()