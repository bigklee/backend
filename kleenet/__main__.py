import asyncio

from kleenet.web import KleenetServer

if __name__ == "__main__":
    server = KleenetServer()
    loop = asyncio.get_event_loop()
    asyncio.gather(loop.run_until_complete(server.start()))
