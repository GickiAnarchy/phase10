import asyncio
import json

from cclass import Client
from view_test import Lobby

from view_test import P10TestApp
from game.game import Game  # Assuming game.game is a separate module



_client = None
p10 = P10TestApp()

async def send_message(client = None, message = None):
    if client == None:
        client = _client
    print(f"Sending message: {message}")
    client.writer.write(json.dumps(message).encode() + b'\n')
    await client.writer.drain()

async def update_lobby():
    await send_message(_client, {"type":"lobbyinfo"})

async def receive_message(client):
    data = await client.reader.readuntil(b'\n')
    return json.loads(data.decode())

async def handle_game_update(client, update):
    # Update local game state based on server update (e.g., hand changes, discard pile)
    client.game.update(update)
    # Display updated game state to the player (e.g., using a GUI)


async def run(client):
    while True:
        message = await receive_message(client)
        if message["type"] == "game_update":
            await handle_game_update(client, message["data"])
        elif message["type"] == "your_turn":
            await play_turn(client)
        elif message["type"] == "lobbyinfo":
            message["target"] = "lobby"
            p10.update(message)
        # Handle other message types (e.g., game start, game end)

async def main():
    p10.run()
    reader, writer = await asyncio.open_connection('localhost', 8888)
    client = Client(reader, writer)
    _client = client
    await send_message(client, {"type": "register", "client_id": client.client_id})  # Send client ID
    await run(_client)

if __name__ == '__main__':
    asyncio.run(main())
