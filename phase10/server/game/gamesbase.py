from uuid import uuid4
import asyncio

from phase10.server.game.rps import RPS


def get_all_game_types() -> list:
    return [
        "Phase 10",
        "RPS",
        "Coin Flip"
    ]


class GameBase:
    def __init__(self, game_type=None, game_id=None, max_players=10, clients=None):
        self.game_type = game_type

        if game_id is None and self.game_type is not None:
            game_id = str(uuid4())
        self.game_id = game_id
        if clients is None:
            clients = []
        self.clients = clients
        self.max_players = max_players

    def add_player(self, client):
        if len(self.clients) < self.max_players:
            self.clients.append(client)
            self.go()

    def go(self):
        pass



    @property
    def is_waiting(self):
        if len(self.clients) < self.max_players:
            return True
        elif len(self.clients) >= self.max_players:
            return False

    @staticmethod
    def create_game(game_type):
        match game_type:
            case "RPS":
                return RPS(game_type=game_type)
            case _:
                return

    def to_dict(self):
        return {
            "game_type": self.game_type,
            "game_id": self.game_id,
            "clients": self.clients,
            "max_players": self.max_players
        }

    @classmethod
    def from_dict(cls, data):
        obj = cls(
            game_type=data.get("game_type"),
            game_id=data.get("game_id"),
            clients=data.get("clients"),
            max_players=data.get("max_players")
        )
        return obj
