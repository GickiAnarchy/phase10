from game.game import Game
import client
from cclass import Client
from view import Phase10App

class Room:
    def __init__(self):
        self.players = {}

    def connect_player(self, info):
        self.players[info["client_id"]] = info["player"]
        print(f"{info["player"].name} connected")
    
    def get_player_by_id(self, client_id):
        for k,v in self.players:
            if k == client_id:
                return v

    def get_player_by_name(self, name):
        for k,v in self.players:
            if v.name == name:
                return v