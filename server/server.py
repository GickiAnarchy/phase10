
import json
import asyncio


from gamestate import Gamestate
from game import Game



async def handle_client(reader, writer):
    while True:
        game = Game.getGameInstance()
        data = await reader.readuntil(b'\n')
        if not data:
            break

        message = json.loads(data.decode())
        print(f"Received message: {message}")
        if message['type'] == 'join':
            player_name = message['name']
            reader = message['reader']
            writer = message['writer']
            game.add_client(reader, writer, player_name)
        elif message['type'] == 'draw_card':
            # Handle card drawing
            player = game.getPlayer(message['player'])
            game.turn_draw(player)
        elif message['type'] == 'play_cards':
            player = get_player_by_name(message['player'])
            cards = message['cards']
        elif message['type'] == 'discard_card':
            player = get_player_by_name(message['player'])
            card = message['card']
        else:
            print("Unknown message type")
    await game.broadcast_game_state()
    writer.close()
    print("Client connection closed")

addr = 'localhost'

async def main():
    server = await asyncio.start_server(handle_client, addr, 8888)
    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    asyncio.run(main())
