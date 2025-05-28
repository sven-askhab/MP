import asyncio
import aiohttp
import sys


async def aio_http_client(url):
    lines_printed = 0

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            async for line in response.content:
                print(line.decode().strip())
                lines_printed += 1

                if lines_printed % 25 == 0:
                    print("Press space to scroll down...")
                    await asyncio.get_event_loop().run_in_executor(None, input)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python aio_http_client.py <url>")
        sys.exit(1)

    asyncio.run(aio_http_client(sys.argv[1]))