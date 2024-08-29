
import asyncio
import uuid

class Client:
    def __init__(self, reader, writer, name):
        self.reader = readergc
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
            self.updated_game
            # ... (your game-specific logic) ...

    async def send_message(self, message):
        data = json.dumps(message).encode()
        await self.writer.write(data + b'\n')
         cawait asyncio.drain(self.writer)

    def generate_unique_id(self):
        return str(uuid.uuid4())


addr = 'localhost'

async def main(player):
    reader, writer = await asyncio.open_connection(addr, 8888)
    client = Client(reader, writer, player.name)
    await client.run()

if __name__ == '__main__':
    #asyncio.run(main())

    