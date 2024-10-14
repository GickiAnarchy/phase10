import asyncio
import json

from urllib3.filepost import writer

from common import Client  # Assuming this is your base client class
from phase10 import Player


class GameClient(Client):
    def __init__(self):
        super().__init__()
        self.player = None
        self.reader = None
        self.writer = None

    def has_player(self):
        if self.player is None:
            return False
        else:
            return True

    async def start_client(self):
        await self.connect()  # Make sure this is being called
        await self.register()  # Register after connection
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
        message_d = {
            "type": "register",
            "client_id": self.client_id
        }
        await self.send_message(message_d)
        await self.receive_message()  # Ensure this is listening for the server's response

    async def send_message(self, message: dict):
        message_json = json.dumps(message)
        print(f"Sending message: {message_json}")
        self.writer.write(message_json.encode())
        await self.writer.drain()

    async def receive_message(self):
        try:
            data = await self.reader.read(1024)
            message_json = data.decode()
            message_dict = json.loads(message_json)
        except Exception as e:
            print(f"Error receiving message: {e}")
            return

        try:
            msg_type = message_dict["type"]
        except Exception as e:
            print(f"Message has no type\n{e}")
            return

        if msg_type == "connect_player":
            self.player = message_dict["name"]
            print(f"Client has {self.player} as player name")

        print(f"Received: {message_dict}")

    async def test_message(self, msg = None):
        if msg is None:
            msg = {
                "type":"test",
                "desc":"Test sending message"
            }
        await self.send_message(msg)
        await self.receive_message()

    def message_factory(self, msg_type, msg:dict):
        """ Function to create a message for the server.
            Adds the client_id and player name automatically.

        :arg    msg_type: The message type the server looks for.
        :arg    msg: A dictionary of other data needed for the message

        :return encoded_message: Dictionary in bytes ready to be sent to the server"""

        message = {
            "type": msg_type,
            "client_id": self.client_id,
            "player": self.player.name
        }

        for k,v in msg.items():
            message[k] = v

        message_json = json.dumps(message)
        encoded_message = message_json.encode()
        return encoded_message


