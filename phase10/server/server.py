import asyncio
import json
import os

from phase10.client.common import Client
from phase10.game_encoder import game_decoder, GameEncoder
from phase10.server.classes.player import Player, PlayerBase
from phase10.server.lobby import Lobby


LOBBY = Lobby()

async def main():
    init_assets()
    # Start the server at host:port
    try:
        server = await asyncio.start_server(handle_client, "127.0.0.1", 8899)
        async with server:
            print("Server Listening")
            await server.serve_forever()
    except Exception as e:
        print(f"Failed to start server: {e}")


"""
    Saving and loading players
"""

async def handle_client(reader, writer):
    """
    Called when a client connects to host:port.
    """
    c_id = None #initialize c_id for the client_id
    try:
        while True:
            # Continuously check for messages from the client
            data = await reader.read(2048)
            if not data:
                break

            # Decode the message
            message_json = data.decode()
            message = json.loads(message_json, object_hook=game_decoder)

            try:
                # Get the client_id
                c_id = message["client_id"]  # always include the client_id
            except Exception as e:
                print(e)

            try:
                # Get the type of message. Which is sent from the client.
                msg_type = message["type"]
            except Exception as e:
                print(f"There is no 'type' value in the message.\n{e}")
                break

            # Perform action here base on the message type.
            match msg_type:
                case "register":
                    # Register the client in the CLIENTS dictionary
                    new_client = Client(reader, writer)
                    new_client.make_client_id()
                    new_client.set_client_id(message["client_id"])
                    LOBBY.add_client(new_client)

                    # Create the response back to the client and send
                    rep = {"type": "success", "client_id": c_id} # Message to send back to the client
                    rep_e = json.dumps(rep,cls=GameEncoder) # Encode with the GameEncoder
                    writer.write(rep_e.encode()) # Send to client
                    print(f"Message received: Registered Client {c_id}")
                    await writer.drain() # Clear the write buffer

                case "get_clients":
                    ids = LOBBY.get_client_ids()
                    rep = {
                        "type":msg_type,
                        "client_id": c_id,
                        "response": ids
                    }
                    # Create the response back to the client and send
                    rep_e = json.dumps(rep, cls=GameEncoder)  # Encode with the GameEncoder
                    writer.write(rep_e.encode())  # Send to client
                    await writer.drain()  # Clear the write buffer

                case "save_player":
                    try:
                        # Get the player from the message
                        p = Player.from_dict(message.get("player"))
                        # Check if player is already saved
                        if check_duplicate_save(p.name, p.pin):
                            print(f"{p.name} data has been overwritten")
                            return False
                        else:
                            # save player to file
                            save_player(p)
                            # print saved to console
                            print(f"{p.name} saved to server.")
                    except Exception as e:
                        print(e)

                case "load_player":
                    try:
                        # Get Name and PIN from message
                        n = message.get("name")
                        p = message.get("pin")
                        # Load Player from file
                        p = load_player(n,p)
                        print(f"Loaded {p.name}")
                    except Exception as e:
                        print(e)
                    LOBBY.bind_player(c_id, p)
                    return p

                case "create_player":
                    try:
                        # Get Name and PIN from message
                        n = message.get("name")
                        p = message.get("pin")
                        # Make Player
                        pl = PlayerBase(n,p)
                        print(f"Loaded {pl.name}")
                        LOBBY.bind_player(c_id, pl)
                        return pl
                    except Exception as e:
                        print(e)

                case "game_queue":
                    try:
                        # Get game type from message
                        game_type = message.get("game_type")
                        # Get game id from message
                        game_id = message.get("game_id")



                    except Exception as e:
                        print(e)


                case _:
                    print(f"Type:{msg_type} is not recognized by the server")

    finally:
        if c_id and c_id in LOBBY.get_client_ids():
            LOBBY.remove_client(c_id)
        writer.close()
        await writer.wait_closed()


#   Games Management
async def broadcast_game(gamestate, gclients):
    pass
    '''msg = {
        "type":"update",
        "gamestate":gamestate
    }
    for c in gclients:
        try:
            msg = json.dumps(msg, cls=GameEncoder)
            c.writer.write(msg.encode())
            print(f"Sending Game Update to : {c.client_id}")
            await c.writer.drain()
        except Exception as e:
            print(e)'''



#   ASSET HANDLING
data_directory = "../assets/data/"
saved_players_file = "playersaves.p10" #Player saves file

def init_assets():
    # Create data directory is nonexistent
    if not os.path.exists(data_directory):
        print("created data folder")
        os.mkdir(data_directory)
    # Create saved_players_file file if nonexistent
    if not os.path.exists(f"{data_directory}{saved_players_file}"):
        print("saved_players_file didn't exist. Creating now..")
        with open(f"{data_directory}{saved_players_file}", "w") as f:
            saved_players = {}
            f.write(json.dumps(saved_players, cls=GameEncoder))
            f.close()
    else:
        print("saved_players_file already exists")

def check_duplicate_save(name, pin):
    saves = get_saved_names_and_pins()
    for n,p in saves:
        if name == n and pin == p:
            return True
    return False

def get_saved_players(just_names = False):
    print("in server.py->get_saved_players()")
    with open(f"{data_directory}{saved_players_file}", "r") as f:
        data = json.load(f)
        f.close()
    print("leaving server.py->get_saved_players()")
    if just_names:
        data = data.keys()
    return data

def get_saved_names_and_pins():
        names_pins = []
        for pl in get_saved_players().items():
            names_pins.append((pl.name, pl.pin))
        return names_pins

def save_player(player:Player):
    print("in server.py->save_player()")
    print(f"\n\t\t{player.name}\n\n")
    try:
        data = get_saved_players()
        data[player.name] = player.to_dict()
        print(f"saving {player.name}")
        with open(f"{data_directory}{saved_players_file}","w") as f:
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



if __name__ == "__main__":
    asyncio.run(main())
