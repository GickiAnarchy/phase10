
import asyncio
import uuid
import json

from gamestate import Gamestate
from gui import Phase10App

class Client:
    def __init__(self, reader, writer, name):
        self.reader = reader
        self.writer = writer
        self.name = name
        self.id = self.generate_unique_id()
        self.updated_game = None
        
    async def run(self):
        while True:
            data = await self.reader.readuntil(b'\n')
            if not data:
                break
            message = json.loads(data.decode())
            # Handle the received message (e.g., update game state, display information)
            self.updated_game = message
            # ... (your game-specific logic) ...

    async def send_message(self, message):
        data = json.dumps(message).encode()
        await self.writer.write(data + b'\n')
        await asyncio.drain(self.writer)

    def generate_unique_id(self):
        return str(uuid.uuid4())


addr = 'localhost'

async def main(player = None):
    reader, writer = await asyncio.open_connection(addr, 8888)
    if player == None:
        client = Client(reader, writer, "Default")
    else:
        client = Client(reader, writer, player.name)
    await client.run()

    async def startClient(self, player):
        asyncio.run(main(player))

if __name__ == '__main__':
    pass

    