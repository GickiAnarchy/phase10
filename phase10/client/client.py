import asyncio
import json

from phase10.client.common import Client  # Assuming this is your base client class
from phase10.game_encoder import GameEncoder, game_decoder
from phase10.server.classes.player import Player


class GameClient(Client):
    def __init__(self):
        super().__init__()
        self.reader = None
        self.writer = None
        self.player = None

    @property
    def is_ready(self):
        if self.player is None:
            return False
        else:
            return True

    async def start_client(self):
        await self.connect()
        await self.register()
        print("Client registered!")

    async def connect(self, addr="127.0.0.1", port=8899):
        print(f"Attempting to connect to {addr}:{port}...")
        try:
            self.reader, self.writer = await asyncio.open_connection(addr, port)
            print(f"Client created and connected: {self.client_id}")
        except Exception as e:
            print(f"Connection failed: {e}")

    async def register(self):
        print("Registering client...")
        message = {"type": "register", "client_id": self.client_id}
        await self.send_message(message)

    async def send_message(self, message):
        message_json = json.dumps(message, cls=GameEncoder)
        self.writer.write(message_json.encode())
        await self.writer.drain()
        print(f"Sent message: {message}")

    async def receive_message(self):
        try:
            data = await self.reader.read(1024)
            message_dict = json.loads(data.decode(), object_hook=game_decoder)
        except Exception as e:
            print(f"Error receiving message: {e}")
            return
        try:
            m_type = message_dict['type']
        except Exception as e:
            print(e)

        try:
            response = message_dict['response']
            return response
        except Exception as e:
            print(f"No response from server.\n{e}")

    async def test_get_clients(self):
        message = {"type":"get_clients","client_id":self.client_id}
        await self.send_message(message)
        clients_list = await self.receive_message()
        for cl in clients_list:
            print(cl)

    #   MESSAGES
    async def save_player(self, player: Player):
        message = {
            "type":"save_player",
            "client_id":self.client_id,
            "player": player
        }
        await self.send_message(message)


if __name__ == "__main__":
    c = GameClient()
    c.make_client_id()
    asyncio.run(c.start_client())