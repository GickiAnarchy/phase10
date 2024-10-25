import asyncio
import json
import os
import pickle

from common import Client
from phase10.game import Player

saved_players_file = "assets/data/playersaves.p10"

clients = {}


async def handle_client(reader, writer):
    c_id = None
    try:
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
            c_id = message["client_id"] #always include the client_id

            match msg_type:
                case "register":
                    new_client = Client(reader, writer)
                    new_client.make_client_id()
                    new_client.set_client_id(message["client_id"])
                    clients[c_id] = new_client

                    print(f"Received message: {message}")
                    rep = {"type": "success", "client_id": c_id}
                    rep_e = json.dumps(rep)
                    writer.write(rep_e.encode())
                    print(f"Message received: Registered Client {c_id}")
                    await writer.drain()

                case "load":
                    name = message["name"]
                    pin = message["pin"]
                    try:
                        loaded_p = load_player(name, pin)
                    except Exception as e:
                        print(e)
                        print(f"Message received: Client {c_id} could not load their player")
                        return
                    if isinstance(loaded_p, Player):
                        pass #Add Player to the game then update all gui in game
                    reply = {"type":"load", "client_id": c_id, "player": loaded_p}
                    rep_e = json.dumps(reply)
                    writer.write(rep_e.encode())
                    print(f"Message received: Client {c_id} loaded their player")
                    await writer.drain()

                case "create":
                    name = message["name"]
                    pin = message["pin"]
                    try:
                        new_player = Player(name = name, pin = pin) # Add to the game. then update all gui in game.
                    except Exception as e:
                        print(e)
                        return
                    reply = {"type": "create", "client_id": c_id, "player": new_player}
                    rep_e = json.dumps(reply)
                    writer.write(rep_e.encode())
                    print(f"Message received: Client {c_id} loaded their player")
                    await writer.drain()

                case "save":
                    player = message["player"]
                    save_player(player)
                    reply = {"type": "save", "client_id": c_id, "desc": "Saved a player"}
                    rep_e = json.dumps(reply)
                    writer.write(rep_e.encode())
                    print(f"Message received: Client {c_id} saved their player")
                    await writer.drain()

                case "ready":
                    rep = {"type": "success", "client_id": c_id, "desc": "Got Ready Message"}
                    rep_e = json.dumps(rep)
                    writer.write(rep_e.encode())
                    print(f"Message received: Registered Client {c_id}")
                    await writer.drain()

                case "test":
                    rep = {"type": "success", "client_id": c_id, "desc": "BUTTON SMASHER"}
                    rep_e = json.dumps(rep)
                    writer.write(rep_e.encode())
                    print(f"Test Successful\nMessage sending to Client {c_id}")
                    await writer.drain()

                case "connect_player":
                    player_name = message["name"]
                    c_id = message["client_id"]
                    pl_client = clients.get(c_id)
                    pl_client.player = player_name

                    rep = {"type": "connect_player", "desc": "added player name"}
                    rep_e = json.dumps(rep)
                    writer.write(rep_e.encode())
                    print(f"Client {c_id} added the player name: {player_name}")
                    await writer.drain()

                case _:
                    print(f"Type:{msg_type} is not recognized by the server")
    finally:
        if c_id and c_id in clients:
            del clients[c_id]
        writer.close()
        await writer.wait_closed()

async def broadcast_game(room):
    game_json = room.game.to_json()
    message = {"type": "game_update", "game": game_json}
    message_encoded = json.dumps(message).encode()
    for player in room.players:
        client = clients.get(player.player_id)
        if client:
            try:
                client.writer.write(message_encoded)
                await client.writer.drain()
            except Exception as e:
                print(f"Error broadcasting game to client {player.player_id}: {e}")

async def main():
    saved_players_file = "assets/data/playersaves.p10"
    """ Create saved_players_file file if nonexistant"""
    if not os.path.exists(saved_players_file):
        with open(saved_players_file, "wb") as f:
            saved_players = {}
            pickle.dump(saved_players, f)
            f.close()
    try:
        server = await asyncio.start_server(handle_client, "127.0.0.1", 8888)
        async with server:
            print("Server Listening")
            await server.serve_forever()
    except Exception as e:
        print(f"Failed to start server: {e}")


"""
    Saving and loading players
"""



def get_saved_players() -> dict:
    global saved_players_file
    with open(saved_players_file, "rb") as rf:
        return pickle.load(rf)

def save_player(player):
    saved_players = get_saved_players()
    saved_players[player.name] = player
    with open(saved_players_file, "wb") as f:
        pickle.dump(saved_players, f)
        f.close()
    print(f"Saved {player.name}")

def load_player(name, pin):
    saved_players = get_saved_players()
    for k,v in saved_players.items():
        if k == name:
            if v.pin == pin:
                return v
    print(f"Saved {v.name}")

if __name__ == "__main__":
    asyncio.run(main())
