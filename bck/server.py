import asyncio
import json
import os

from common import Client
from phase10.game.classes.player import Player

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
            c_id = message["client_id"]  #always include the client_id

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
                        pass  #Add Player to the game then update all gui in game
                    reply = {"type": "load", "client_id": c_id, "player": loaded_p.to_json()}
                    rep_e = json.dumps(reply)
                    writer.write(rep_e.encode())
                    print(f"Message received: Client {c_id} loaded their player")
                    await writer.drain()

                case "create":
                    name = message.get('name')
                    pin = message.get('pin')
                    try:
                        new_player = Player(name=name, pin=pin)  # Add to the game. then update all gui in game.
                    except Exception as e:
                        print(e)
                        return
                    reply = {"type": "create", "client_id": c_id, "player": new_player.to_json()}
                    rep_e = json.dumps(reply)
                    writer.write(rep_e.encode())
                    print(f"Message received: Client {c_id} created their player")
                    await writer.drain()

                case "save":
                    p = message["player"]
                    player:Player = player.generate_from_json(player)
                    player.generate_from_json(player)
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


async def broadcast_game():
    pass


async def main():
    """ Create saved_players_file file if nonexistent"""
    if not os.path.exists(saved_players_file):
        print("saved_players_file didnt exist. Creating now..")
        with open(saved_players_file, "w") as f:
            saved_players = {}
            f.write(json.dumps(saved_players))
            f.close()
    else:
        print("saved_players_file already exists")
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


def get_saved_players():
    global saved_players_file
    data = None
    with open(saved_players_file, "r") as rf:
        data = rf.read()
        rf.close()
    return data


def save_player(player):
    data = get_saved_players()
    saved_players = data

    with open(saved_players_file, "w") as f:
        f.write(json.dumps(saved_players))
    print(f"Saved {player.name}")


def load_player(name, pin):
    saved_players = get_saved_players()
    print(saved_players)
    return saved_players


if __name__ == "__main__":
    asyncio.run(main())
