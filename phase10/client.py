import asyncio
import json
from pyexpat.errors import messages

from common import Client  # Assuming this is your base client class
from messages import get_client_message
from phase10.game.classes.player import Player
from phase10.game.classes.game_encoder import GameEncoder, game_decoder  # Your custom encoder/decoder


class GameClient(Client):
    def __init__(self, gui=None):
        super().__init__()
        self.reader = None
        self.writer = None
        self.player:Player

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

        try:
            tmp_pl = message_dict.get('player')
            self.set_player(Player.from_dict(tmp_pl))
        except Exception as e:
            print(e)


        if message_dict["type"] == "load":
            print("in client->receive_message()->type load")
            tmp_p = Player.from_dict(message_dict.get('player'))
            self.set_player(tmp_p)
            print(self.player.to_dict())

        if message_dict["type"] == "create":
            print("in client->receive_message()->type create")
            data = message_dict.get('player')
            tmp_p = Player.from_dict(data)
            self.set_player(tmp_p)
            print(self.player.to_dict())

        else:
            print("Message from server:")
            try:
                print(message_dict.keys())
                print(message_dict.values())
            except Exception as e:
                print(e)

    def set_player(self, newp:Player):
        self.player = newp

    async def test_message(self, msg=None):
        if msg is None:
            msg = {"type": "test", "name": self.player.name, "desc": "Test sending message"}
        await self.send_message(msg)
        await self.receive_message()

    async def draw_card(self, target):
        message = self.create_message("draw_card")
        await self.send_message(message)
        await self.receive_message()

    def create_message(self, msg_type, **kwargs):
        if msg_type not in ['connect', 'disconnect', 'join', 'leave', 'load_player', 'create_player', 'turn_complete',
                            'skipped', 'draw_deck', 'draw_discards', 'play_card', 'play_skip', 'discard', 'pass',
                            'phase_complete', 'win', 'deal_cards']:
            print(
                "Message type must be one of the following: \n['connect', 'disconnect', 'join', 'leave', 'load_player', 'create_player', 'turn_complete', 'skipped', 'draw_deck', 'draw_discards',\n 'play_card', 'play_skip', 'discard', 'pass', 'phase_complete', 'win', 'deal_cards']")
            return
        message = {}
        try:
            message = get_client_message(msg_type, **kwargs)
        except ValueError as e:
            print(e)
            return
        return message
