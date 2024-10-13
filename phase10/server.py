import asyncio
import json
from dataclasses import dataclass

from common import Client
from phase10 import Player, Game


clients = {}

async def handle_client(reader, writer):
    while True:
        data = await reader.read(1024)
        if not data:
            break
        message_json = data.decode()
        message = json.loads(message_json)

        msg_type = None

        try:
            msg_type = message["type"]
        except:
            print("There is no 'type' value in the message.")
            break

        if msg_type == "register":
            new_client = Client(reader,writer)
            new_client.set_client_id(message["client_id"])
            c_id = message["client_id"]
            clients[c_id] = new_client

            print(f"Received message: {message}")
            rep = {"type":"success","client_id":c_id}
            rep_e = json.dumps(rep)
            writer.write(rep_e.encode())
            print(f"Message received: Registered Client {c_id}")
            await writer.drain()

        if msg_type == "ready":
            rep = {"type": "success", "client_id": c_id, "desc":"Got Ready Message"}
            rep_e = json.dumps(rep)
            writer.write(rep_e.encode())
            print(f"Message received: Registered Client {c_id}")
            await writer.drain()

        if msg_type == "test":
            rep = {"type": "success", "client_id": c_id, "desc":"BUTTON SMASHER"}
            rep_e = json.dumps(rep)
            writer.write(rep_e.encode())
            print(f"Test Successful\nMessage sending to Client {c_id}")
            await writer.drain()

        if msg_type == "connect_player":
            player_name = message["name"]
            c_id = message["client_id"]
            pl_client = clients.get(c_id)
            pl_client.player = player_name

            rep = {"type":"connect_player","desc":"added player name"}
            rep_e = json.dumps(rep)
            writer.write(rep_e.encode())
            print(f"Client {c_id} added the player name: {player_name}")
            await writer.drain()

        else:
            print(f"Type:{msg_type} is not recognized by the server")



async def main():
    server = await asyncio.start_server(
        handle_client, "127.0.0.1", 8888
    )

    async with server:
        print("Server Listening")
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())