import asyncio
import json
from common import Client  # Assuming this is your base client class
from phase10 import Player, Game


class GameClient(Client):
    def __init__(self, gui=None):
        super().__init__()
        self.player = None
        self.gui = gui
        self.reader = None
        self.writer = None

    def has_player(self) -> bool:
        """Checks if the GameClient's player attribute is not None."""
        return self.player is not None

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
        message = {"type":"register", "client_id": self.client_id}
        await self.send_message(message)
        await self.receive_message()

    async def send_message(self, message: dict):
        message_json = json.dumps(message)
        self.writer.write(message_json.encode())
        await self.writer.drain()
        print(f"Sent message: {message}")

    async def receive_message(self):
        try:
            data = await self.reader.read(1024)
            message_dict = json.loads(data.decode())
        except Exception as e:
            print(f"Error receiving message: {e}")
            return
        await self.handle_received_message(message_dict)

    async def handle_received_message(self, message_dict: dict):
        try:
            msg_type = message_dict["type"]
        except KeyError as e:
            print(f"Message has no type\n{e}")
            return

        if msg_type == "game_update":
            self.gui.game = Game(message_dict["game"])
        elif msg_type == "connect_player":
            self.player = message_dict["name"]
            print(f"Client has {self.player} as player name")
        print(f"Received: {message_dict}")

    async def test_message(self, msg=None):
        if msg is None:
            msg = {"type": "test", "name": self.player.name, "desc": "Test sending message"}
        await self.send_message(msg)
        await self.receive_message()

    async def draw_card(self, target):
        message = self.create_message("draw_card", {"target": target})
        await self.send_message(message)
        await self.receive_message()

    async def create_message(self, msg_type, additional_data=None):
        """ Creates a message for the server.
        Automatically adds client_id and player name.
        :param msg_type: The message type the server expects.
        :param additional_data: Additional data needed for the message.
        """
        message = {
            "type": msg_type,
            "client_id": self.client_id,
            "player": self.player.name if self.player else None
        }
        if additional_data:
            message.update(additional_data)
        return message
