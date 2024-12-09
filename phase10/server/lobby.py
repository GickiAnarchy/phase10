from phase10.client.common import Client
from phase10.server.game.gamesbase import GameBase


class Lobby:
    """ Essentially a list(with particular methods) of clients and games the server will contain. """
    def __init__(self, clients = None, games = None):
        if clients is None:
            clients = {}
        self.clients = clients
        if games is None:
            games = {}
        self.games = games

    # CLIENTS
    def get_clients(self):
        return self.clients

    def get_client(self, c_id):
        try:
            c = self.clients.get(c_id)
            return c
        except Exception as e:
            print(e)

    def get_client_ids(self):
        return self.clients.keys()

    def add_client(self, client):
        if isinstance(client,Client) and client.client_id not in self.clients.keys():
            self.clients[client.client_id] = client.__dict__()

    def remove_client(self, c_id):
        rc = self.clients.pop(c_id)

    # GAMES
    def get_games(self):
        return self.games

    def get_game(self, g_id):
        try:
            g = self.games.get(g_id)
            return g
        except Exception as e:
            print(e)

    def get_game_ids(self):
        return self.games.keys()

    def join_game(self, client, game_type):
        # Check list of games for the game type and see if its waiting for players
        for g in self.games:
            if g.game_type == game_type and g.is_waiting:
                g.add_player(client) # Add Player to game
                print(f"{client.client_id} joined game {g.game_id}")
                return
        # Create a new game to wait in.
        new_game = GameBase.create_game(game_type)
        new_game.add_player(client) # Add player to game
        self.games.append(new_game) # Add game to games list
        print(f"{client.client_id} joined game {new_game.game_id}")

    def close_game(self, g_id):
        try:
            rg = self.games.pop(g_id)
            print(f"Removed game: {g_id} from server")
        except Exception as e:
            print(e)


