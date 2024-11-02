import asyncio
import json
import os
import pickle

from common import Client
from phase10.game.classes.player import Player

saved_players_file = "assets/data/playersaves.p10"

clients = {}


async def handle_client(reader, writer):
    c_id = None
    try:
        while True:
            data = await reader.read(2048)
            if not data:
                break
            message_json = data.decode()
            message = json.loads(message_json)

            msg_type = None

            try:
                msg_type = message["type"]
            except Exception as e:
                print(f"There is no 'type' value in the message.\n{e}")
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
                        p = load_player(name,pin)
                    except Exception as e:
                        print(e)
                        return
                    if p is None:
                        print("in handle_client.... p is None")
                        return False
                    msg = {"type": "success", "client_id": c_id, "player": p.__dict__()}
                    rep_e = json.dumps(msg)
                    writer.write(rep_e.encode())
                    print(f"Message received: Load Player {c_id}")
                    await writer.drain()

                case "create":
                    name = message["name"]
                    pin = message["pin"]
                    p = Player(name = name, player_id = c_id, pin = pin)
                    save_player(p)
                    msg = {"type":"success","client_id":c_id, "player": p.__dict__()}
                    rep_e = json.dumps(msg)
                    writer.write(rep_e.encode())
                    print(f"Message received: Create Player {c_id}")
                    await writer.drain()

                case "save":
                    pass

                case "ready":
                    rep = {"type": "success", "client_id": c_id, "desc": "Got Ready Message"}
                    rep_e = json.dumps(rep)
                    writer.write(rep_e.encode())
                    print(f"Message received: Ready Player {c_id}")
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
        with open(saved_players_file, "wb") as f:
            saved_players = {}
            pickle.dump(saved_players,f)
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
    print("in server.py->get_saved_players()")
    with open(saved_players_file, "rb") as f:
        try:
            data = pickle.load(f)
        except Exception as e:
            print(e)
            data = {}
        f.close()
    print("leaving server.py->get_saved_players()")
    for k,v in data.items():
        print(k)
        print(v)
    return data


def save_player(player):
    print("in server.py->save_player()")
    print(f"\n\t\t{player.name}\n\n")
    data = get_saved_players()
    data[player.name] = player.to_dict()
    with open(saved_players_file,"wb") as f:
        pickle.dump(data, f)
        f.close()
    print("leaving server.py->save_player()")


def load_player(name, pin):
    print("in server.py->load_player()")
    data = get_saved_players()
    for k in data.keys():
        if k == name:
            if data.get(k)['pin'] == pin:
                print("success:leaving server.py->load_player()")
                return Player(**data[str(k)])
    print("failed:leaving server.py->load_player()")



if __name__ == "__main__":
    asyncio.run(main())
