import asyncio
import json
import logging
from game.game import Game

class Client:
    def __init__(self, reader, writer):
        self.reader = reader
        self.writer = writer
        self.id = id(self)  # Unique identifier

clients = []  # List to store Client objects

async def handle_client(reader, writer):
    client = Client(reader, writer)
    clients.append(client)
    logger = logging.getLogger(__name__)
    logger.info(f"New connection from Client {client.id}")

    try:
        while True:
            data = await client.reader.readuntil(b'\n')
            if data is None:
                logger.info(f"Client {client.id} disconnected")
                clients.remove(client)
                break

            message = json.loads(data.decode().strip())
            logger.info(f"Received message from Client {client.id}: {message}")

            # Process the message here
            response = Game().getGameInstance()
            await client.writer.write(json.dumps(response).encode() + b'\n')
            await writer.drain()
    except asyncio.CancelledError:
        logger.info(f"Connection {client.id} canceled")
        clients.remove(client)

async def broadcast_game():
    g_instance = Game().getGameInstance()
    for client in clients:
        await client.writer.write(g_instance.to_json().encode())
        await writer.drain()

async def main():
    logging.basicConfig(level=logging.DEBUG)

    server = await asyncio.start_server(
        handle_client, "127.0.0.1", 8888
    )

    addr = server.sockets[0].getsockname()
    print(f"Serving on {addr}")
    
    game = Game()

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    game = Game()
    asyncio.run(main())
