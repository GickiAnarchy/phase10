import asyncio
import json
from common import Client  # Assuming this is your base client class

class GameClient(Client):
    def __init__(self):
        super().__init__()
        self.make_client_id()  # Ensure this method sets client_id correctly
        self.reader = None
        self.writer = None

    async def connect(self, addr="127.0.0.1", port=8888):
        print(f"Attempting to connect to {addr}:{port}...")
        try:
            self.reader, self.writer = await asyncio.open_connection(addr, port)
            print(f"Client created and connected: {self.client_id}")
        except Exception as e:
            print(f"Connection failed: {e}")

    async def start_client(self):
        await self.connect()  # Make sure this is being called
        await self.register()  # Register after connection
        print("Client registered!")

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

#-----------MESSAGES------------------
    async def test_message(self, msg = None):
        if msg is None:
            msg = {
                "type":"test",
                "desc":"Test sending message"
            }
        await self.send_message(msg)
        await self.receive_message()


























'''import asyncio
import json


from common import Client



class GameClient(Client):
    def __init__(self):
        super().__init__()
        self.make_client_id()


    def add_client(self,client):
        self.reader = client.reader
        self.writer = client.writer
        try:
            self.client_id = client.client_id
        except:
            print("No client_id for GameClient")


    def get_client_id(self):
        return self.client_id


    async def connect(self, addr = "127.0.0.1", port = 8888):
        self.reader,self.writer =  await asyncio.open_connection(addr, port)
        print(f"Client created and connected:\n\t{self.client_id}")


    async def send_message(self, message: dict):
        message_json = json.dumps(message)
        self.writer.write(message_json.encode())
        await self.writer.drain()


    async def draw_card(self, target):
        if target in [0, "deck"]:
            target = "deck"
        else:
            target = "discards"
        message = {
            "type": "draw_card",
            "target": target,
            "client_id": self.client_id
                   }
        await self.send_message(message)
        await self.receive_message()


    async def register(self):
        print("registering client")
        message_d = {
            "type": "register",
            "client_id": self.client_id
        }
        await self.send_message(message_d)
        await self.receive_message()


    async def test_message(self, msg = None):
        if msg is None:
            msg = {
                "type":"test",
                "desc":"Test sending message"
            }
        await self.send_message(msg)
        await self.receive_message()


    # async def start_client(self):
    #     await self.connect()
    #     await self.register()
    #     self.writer.close()
    #     await self.writer.wait_closed()

    async def start_client(self):
        try:
            print("Attempting to connect to server...")
            await self.connect()  # Ensure that the connection logic is correct
            await self.register()  # Perform registration after connection
            print("Client registered!")
        except Exception as e:
            print(f"Error in start_client: {e}")


    async def receive_message(self):
        data = await self.reader.read(1024)
        message_json = data.decode()
        message_dict = json.loads(message_json)
        print(f"Received: {message_dict}")


    def run(self,dt):
        print(f"running client\n{dt}")
        asyncio.ensure_future(self.start_client())






if __name__ == "__main__":
    pass'''