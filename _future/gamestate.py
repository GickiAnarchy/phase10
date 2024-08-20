import json
from cards import Game

class GameState:
    def __init__(self):
        self.players = {} #All players current state
        self.deck = None
        self.discard_pile = None
        self.current_player_ = #Name of active player
        self.goal_data = {}  # Dictionary to store all player's current goal information

    def to_json(self, game):
        return json.dumps(self.__dict__)

    @classmethod
    def from_json(cls, data):
        return GameState(**json.loads(data))
