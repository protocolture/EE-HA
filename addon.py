import asyncio
import aiohttp
import os
import sys

async def poll_ee_status(host, port, ship_name, interval):
    url = f"http://{host}:{port}/get.lua"
#Build query string for EE API
    params = {
        "_OBJECT_": f"getPlayerShipByCallSign('{ship_name}')",
        "hull": "getHull()"
    }
# Set Timeout 
    timeout = aiohttp.ClientTimeout(total=5)

    async with aiohttp.ClientSession(timeout=timeout) as session:
        while True:
            try:
                async with session.get(url, params=params) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        print(f"Status: {data}")
                    else:
                        print(f"HTTP error: {resp.status}")
            except asyncio.TimeoutError:
                print("Timeout talking to EE server.")
            except aiohttp.ClientError as e:
                print(f"Connection error: {e}")
            except Exception as ex:
                print(f"Unexpected error: {ex}")

            await asyncio.sleep(interval)

def parse_config():
#Input validation
    host = os.getenv("HOST")
    port = os.getenv("PORT")
    ship_name = os.getenv("SHIP_NAME")
    interval = os.getenv("POLL_INTERVAL")

    if not host or not port or not ship_name:
        print("Error: HOST, PORT, and SHIP_NAME must be set.")
        sys.exit(1)

    try:
        port = int(port)
    except ValueError:
        print("Error: PORT must be an integer.")
        sys.exit(1)

    try:
        interval = float(interval) if interval else 0.5
    except ValueError:
        print("Error: POLL_INTERVAL must be a number.")
        sys.exit(1)

    return host, port, ship_name, interval

if __name__ == "__main__":
    cfg = parse_config()
    asyncio.run(poll_ee_status(*cfg))
