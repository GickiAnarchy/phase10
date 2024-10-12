import asyncio
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


    async def register(self):
        message_d = {
            "type": "register",
            "client_id": self.client_id
        }
        await self.send_message(self, message_d)

        data = await self.reader.read(1024)
        message_dict = data.decode()
        # message_dict = json.loads(message_json)
        print(f"Received: {message_dict}")


    async def start_client(self):
        await self.connect()
        await self.register()
        self.writer.close()
        await self.writer.wait_closed()

    async def run(self):
        await self.start_client()
        while True:
            data = await self.reader.read(1024)
            if not data:
                print("No data: breaking...")
                break
            message_dict = data.decode()
            # message_dict = json.loads(message_json)
            print(f"Received: {message_dict}")






if __name__ == "__main__":
    pass