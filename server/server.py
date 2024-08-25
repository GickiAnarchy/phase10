
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
            game.add_client(reader, writer, player_name)
            player_name = message['name']
        elif message['type'] == 'draw_card':
            # Handle card drawing
            player = get_player_by_name(message['player'])
            card = game.draw_card()
            player.hand.append(card)
            broadcast_game_state()
        elif message['type'] == 'play_cards':
            # Handle card playing
            player = get_player_by_name(message['player'])
            cards = message['cards']
            # ... validate card play and update game state ...
            broadcast_game_state()
        elif message['type'] == 'discard_card':
            # Handle card discarding
            player = get_player_by_name(message['player'])
            card = message['card']
            # ... discard card and update game state ...
            broadcast_game_state()
        else:
            print("Unknown message type")

    writer.close()
    print("Client connection closed")

addr = 'localhost'

async def main():
    server = await asyncio.start_server(handle_client, addr, 8888)
    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    asyncio.run(main())
