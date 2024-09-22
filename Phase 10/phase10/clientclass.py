import asyncio
import json

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.reader = None
        self.writer = None

    async def connect(self):
        (self.reader, self.writer) = await asyncio.open_connection(self.host, self.port)
        print("Connected to server!")

    async def send_message(self, message):
        data = json.dumps(message).encode() + b'\n'
        await self.writer.write(data)

    async def receive_message(self):
        data = await self.reader.readuntil(b'\n')
        message = json.loads(data.decode())
        return message

    async def close(self):
        await self.writer.close()
        self.reader = None
        self.writer = None
        print("Disconnected from server.")