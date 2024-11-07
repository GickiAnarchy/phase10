import asyncio
import json

from common import Client  # Assuming this is your base client class
from phase10.game.classes.game_encoder import GameEncoder, game_decoder  # Your custom encoder/decoder
from phase10.game.classes.player import Player


class GameClient(Client):
    def __init__(self):
        super().__init__()
        self.reader = None
        self.writer = None
        self.player = None

    async def start_client(self):
        await self.connect()
        await self.register()
        print("Client registered!")

    async def connect(self, addr="127.0.0.1", port=8888):
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
        await self.receive_message()

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

        m_type = message_dict['type']

        if m_type == "create_true":
            n = message_dict['name']
            p = message_dict['pin']
            pl = Player()
            pl.name = n
            pl.pin = p
            pl.player_id = message_dict['client_id']
            self.player = pl
            await self.send_save_message(self.player)
            return True

        if m_type == "create_false":
            return False

        if m_type == "load_true":
            self.player = Player.from_dict(message_dict['player'])
            return True

        if m_type == "load_false":
            return False

        if m_type == "save_true":
            return True

        if m_type == "save_false":
            return False

        else:
            print("Message from server:")
            try:
                print(message_dict.keys())
                print(message_dict.values())
            except Exception as e:
                print(e)

    async def send_create_message(self, name, pin):
        message = {"type": "create", "client_id": self.client_id, "name": name, "pin": pin,
                   "description": "Create player"}
        await self.send_message(message)
        return await self.receive_message()

    async def send_load_message(self, name, pin):
        message = {"type": "load", "client_id": self.client_id, "name": name, "pin": pin}
        print("Sending load_player message...")
        await self.send_message(message)
        return await self.receive_message()

    async def send_save_message(self, player):
        message = {"type": "save", "client_id": self.client_id, "player": player.to_dict(),
                   "description": "Create player"}
        print("Sending save message...")
        await self.send_message(message)
        return await self.receive_message()

    async def test_message(self, msg=None):
        if msg is None:
            msg = {"type": "test", "desc": "Test sending message"}
        await self.send_message(msg)
        await self.receive_message()


    async def draw_card(self, target):
        pass
