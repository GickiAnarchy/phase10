import asyncio
import json
import os

from common import Client
from phase10.game.classes.player import Player
from phase10.game.classes.game_encoder import GameEncoder, game_decoder  # Your custom encoder/decoder




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
            message = json.loads(message_json, object_hook=game_decoder)

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
                    rep_e = json.dumps(rep,cls=GameEncoder)
                    writer.write(rep_e.encode())
                    print(f"Message received: Registered Client {c_id}")
                    await writer.drain()

                case "load":
                    name = message["name"]
                    pin = message["pin"]
                    msg = {}
                    p = load_player(name,pin)
                    if isinstance(p, Player):
                        msg = {"type": "load_true", "client_id": c_id, "player": p.to_dict()}
                        print("Load SUCCESS")
                    else:
                        msg = {"type": "load_false", "client_id": c_id}
                        print("Load FAIL")
                    rep_e = json.dumps(msg,cls=GameEncoder)
                    writer.write(rep_e.encode())
                    print(f"Message received: Load Player {c_id}")
                    await writer.drain()

                case "create":
                    name = message["name"]
                    pin = message["pin"]
                    okay =  check_duplicate_save(name)
                    msg = {}
                    if not okay:
                        msg = {"type":"create_true","client_id":c_id, "name":name, "pin":pin}
                        print("create TRUE")
                    elif okay:
                        msg = {"type":"create_false", "client_id": c_id}
                        print("create FALSE")
                    rep_e = json.dumps(msg,cls=GameEncoder)
                    writer.write(rep_e.encode())
                    print(f"Message received: Create Player {c_id}")
                    await writer.drain()

                case "save":
                    data = message.get('player')
                    new_pl = Player.from_dict(data)
                    msg = {}
                    print(f"\n\n\n{new_pl.name}\n{new_pl.score}\n\n\n")
                    if save_player(new_pl):
                        msg = {"type":"save_true", "client_id":c_id}
                    else:
                        msg = {"type": "save_false", "client_id": c_id}
                    rep_e = json.dumps(msg, cls=GameEncoder)
                    writer.write(rep_e.encode())
                    print(f"Message received: Create Player {c_id}")
                    await writer.drain()

                case "ready":
                    rep = {"type": "success", "client_id": c_id, "desc": "Got Ready Message"}
                    rep_e = json.dumps(rep,cls=GameEncoder)
                    writer.write(rep_e.encode())
                    print(f"Message received: Ready Player {c_id}")
                    await writer.drain()

                case "join_war":
                    pass

                case "test":
                    rep = {"type": "success", "client_id": c_id, "desc": "BUTTON SMASHER"}
                    rep_e = json.dumps(rep,cls=GameEncoder)
                    writer.write(rep_e.encode())
                    print(f"Test Successful\nMessage sending to Client {c_id}")
                    await writer.drain()

                case "connect":
                    print("\n\n\t\tConnected\n\n")

                case "print_clients":
                    print_clients()
                    gameclient = clients.get(c_id)



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
        print("saved_players_file didn't exist. Creating now..")
        with open(saved_players_file, "w") as f:
            saved_players = {}
            f.write(json.dumps(saved_players,cls=GameEncoder))
            f.close()
    else:
        print("saved_players_file already exists")
    try:
        server = await asyncio.start_server(handle_client, "127.0.0.1", 8899)
        async with server:
            print("Server Listening")
            await server.serve_forever()
    except Exception as e:
        print(f"Failed to start server: {e}")


"""GAME QUEUES"""
class WaitingRoom:
    def __init__(self):
        self.waiting = []
        self.ready = []

    def add_client(self, client:Client):
        self.waiting.append(client)
        if len(self.waiting) == 2:
            p1 = self.waiting.pop()
            p2 = self.waiting.pop()
            self.ready.append((p1,p2))
            p1 = None
            p2 = None

    def get_next_ready(self) -> tuple:
        if len(self.ready) > 0:
            return self.ready.pop()


"""
    Saving and loading players
"""
def check_duplicate_save(name):
    saves = get_saved_players(just_names=True)
    for n in saves:
        if name == n:
            return True
    return False


def get_saved_players(just_names = False):
    print("in server.py->get_saved_players()")
    with open(saved_players_file, "r") as f:
        data = json.load(f)
        f.close()
    print("leaving server.py->get_saved_players()")
    if just_names:
        data = data.keys()
    return data


def save_player(player:Player):
    print("in server.py->save_player()")
    print(f"\n\t\t{player.name}\n\n")
    try:
        data = get_saved_players()
        data[player.name] = player.to_dict()
        print(f"saving {player.name}")
        with open(saved_players_file,"w") as f:
            json.dump(data, f, indent=4)
            f.close()
    except Exception as e:
        print(e)
        return False
    print(f"saved {player.name}")
    print("leaving server.py->save_player()")
    return True


def load_player(name, pin):
    print("in server.py->load_player()")
    data = get_saved_players()
    if name in data.keys():
        if pin == data[name]['pin']:
            return Player.from_dict(data.get(name))
    print("failed:leaving server.py->load_player()")
    return False

# CLIENTS
def print_clients():
    for i,c in enumerate(clients):
        print(f"{i}>>{c}")








if __name__ == "__main__":
    asyncio.run(main())
