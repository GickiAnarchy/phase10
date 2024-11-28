from uuid import uuid4

"""
The base game for all other games.
"""

class BaseGame:
    def __init__(self, game_id = None, players = None):
        if game_id is None:
            game_id = str(uuid4())
        self.game_id = game_id
        if players is None:
            players = []
        self.players = players
    
    @property
    def game_id(self):
        return self._game_id
    
    @game_id.setter
    def game_id(self, newid):
        self._game_id = newid

    @property
    def players(self):
        return self._players
    
    @players.setter
    def players(self, newplayers):
        self._players = newplayers

    def start(self):
        pass

    def to_dict(self):
        pass

    @classmethod
    def from_dict(cls, data):
        pass