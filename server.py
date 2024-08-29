
import json
import asyncio


from gamestate import Gamestate
from game import Game
from player import Player



async def handle_client(reader, writer):
    while True:
        game = Game.getGameInstance()
        data = await reader.readuntil(b'\n')
        if not data:
            break

        message = json.loads(data.decode())
        #player_name = message['name']
        
        #reader = message['reader']
        #writer = message['writer']
        print(f"Received message: {message}")
        if message['type'] == "test":
            print(message["description"])
        if message['type'] == 'join':
            player_name = message['player'].name
            game.add_client(reader, writer, player_name)
            '''
        elif message['type'] == 'create_player':
            game.add_player(message['player'])
        elif message['type'] == 'draw_card':
            game.turn_draw(message['player'])
        elif message['type'] == 'play_cards':
            player = message['player']
            cards = message['cards']
            goal = message['goal']
            
        elif message['type'] == 'discard_card':
            card = message['card']
            '''
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
