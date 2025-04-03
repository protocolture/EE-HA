import asyncio
import aiohttp
import os

async def main():
    host = os.getenv("HOST", "localhost")
    port = int(os.getenv("PORT", 8080))
    url = f"http://{host}:{port}/get.lua?hull=getHull()"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            print("Response:", await resp.text())

if __name__ == "__main__":
    asyncio.run(main())
