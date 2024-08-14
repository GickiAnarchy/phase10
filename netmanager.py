
import json
import asyncio


class AsyncNetworkManager:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.reader = None
        self.writer = None
        self.connected = False
        self.on_message_callback = None

    async def start_server(self):
        self.server = await asyncio.start_server(
            self.client_connected, self.host, self.port)
        addr = self.server.sockets[0].getsockname()
        print(f'Serving on {addr}')
        self.connected = True
        async with self.server:
            await self.server.serve_forever()

    async def client_connected(self, reader, writer):
        self.reader = reader
        self.writer = writer
        print('Client connected')
        while True:
            try:
                data = await self.reader.read(1024)
                message = json.loads(data)
                if self.on_message_callback:
                    await self.on_message_callback(message)
            except asyncio.IncompleteReadError:
                break
            except Exception as e:
                print(f"Error handling message: {e}")
                # Handle error gracefully

    async def connect_to_server(self, host, port):
        self.reader, self.writer = await asyncio.open_connection(host, port)
        self.connected = True
        print(f'Connected to server {host}:{port}')

    async def send_data(self, data):
        if self.connected:
            data = json.dumps(data)
            self.writer.write(data.encode())
            await self.writer.drain()
        else:
            print("Not connected")

    async def close(self):
        if self.writer:
            self.writer.close()
            await self.writer.wait_closed()



MESSAGE_TYPES = [
    "CONNECT",
    "DISCONNECT",
    "CARD_DRAWN",
    "CARD_PLAYED",
    "PHASE_COMPLETED",
    "GAME_OVER",
    "PLAYER_REQUEST"]


class Message:
    def __init__(self, type, data):
        self.type = type
        self.data = data

    def to_json(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def from_json(data):
        return Message(**json.loads(data))


