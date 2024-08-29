
import json
import asyncio


from gamestate import Gamestate
from game import Game
from player import Player



async def handle_client(reader, writer):
    while True:
        data = await reader.readuntil(b'\n')
        if not data:
            break

        message = json.loads(data.decode())

        print(f"Received message: {message}")
        if message['type'] == 'test':
            print(message["description"])
        if message['type'] == 'join':
            player_name = message['player'].name
            Game.getGameInstance().add_client(reader, writer, player_name)
        else:
            print("Unknown message type")
    await broadcast_game_state()
    writer.close()
    print("Client connection closed")

addr = 'localhost'

async def broadcast_game_state():
    game = Game().getGameInstance()
        game_state_json = game.getGame()
        for client_id, client_data in game.clients.items():
            client_data['writer'].write(game_state_json.encode())
            await client_data['writer'].drain()

async def main():
    server = await asyncio.start_server(handle_client, addr, 8888)
    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    asyncio.run(main())
