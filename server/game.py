
import random
import copy
import os
import json
from itertools import cycle
import asyncio
import uuid
from functools import wraps

from cards import SkipCard, Deck, Discards, Hand
from phases import Phase, Goal
from player import Player

def singleton(cls):
    instance = None

    @wraps(cls)
    def __init__(self, *args, **kwargs):
        if instance is not None:
            raise Exception("Singleton already created")
        instance = super().__init__(*args, **kwargs)
        return instance
    return cls
    
@singleton
class Game:
    def __init__(self):
        self.players = []
        self.deck = None
        self.discards = None
        self.active_player = None
        self.clients = {}
        self.all_hands = []
        self.all_phases = []
        self.all_goals = []
        Game.instance = self

    def prestart(self) -> bool:
        if len(self.players) < 2:
            print("Not enough players to start")
            return False
        self.player_turn_cycle = itertools.cycle(self.players)
        self.deck = Deck()
        self.discards = Discard()
        for player in self.players:
            player.hand.extend(self.deck.deal())
        return True
    
    def start(self):
        if self.prestart():
            pass

    def add_player(self, player):
        self.players.append(player)

    def getPlayer(self, player_name):
        for p in self.players:
            if p.name == player_name:
                return p

    def turn_draw(self, player) -> bool:
        if player.skipped:
            player.toggleSkip()
            self.active_player = next(self.player_turn_cycle)
            return False
        player.drawCard(self.deck.drawCard)
        return True

    def turn_play(self, cards, goal=None):
        if goal:
            goal.addCards(cards)
        if isinstance(cards, SkipCard):
            self.play_skip(cards, target)
            
    def play_skip(self, skip, target):
        target.toggleSkip()

    @property
    def all_goals(self):
        self._all_goals = []
        for p in self.players:
            self._all_goals.extend(p.getCurrentPhase().getGoals())
        return self._all_goals

    @all_goals.setter
    def all_goals(self, newgoals):
        if isinstance(newgoals, list):
            self._all_goals = newgoals
        if isinstance(newgoals, Goal):
            newgoals = [newgoals]

    @property
    def all_hands(self):
        self.all_hands.clear()
        for p in self.players:
            self.all_hands.append(p.hand)
        return self.all_hands
    
    @all_hands.setter
    def all_hands(self, newhands):
        if isinstance(newhands, list):
            self._all_hands = newhands

    @property
    def all_phases(self):
        self.all_phases = []
        for p in self.players:
            self.all_phases.append(p.getCurrentPhase())
        return self.all_phases

    @all_phases.setter
    def all_phases(self, newphases):
        if isinstance(newphases, list):
            self._all_phases = newphases

    @property
    def active_player(self):
        self._active_player = next(self.player_turn_cycle)
        return self._active_player

    @active_player.setter
    def active_player(self, newactive):
        self._active_player = newactive

    def getGame(self):
        return json.dumps(self.__dict__)

    def saveGame(self, gstate):
        with open("savedGame.json", "w") as f:
            f.write(gstate)
            f.close()

    @staticmethod
    def from_json(data = None, load_saved = False):
        if data == None and load_saved == True:
            return Game(Game.loadGame())
        return Game(**json.loads(data))

    @staticmethod
    def loadGame():
        with open("savedGame.json","r") as f:
            return json.load(f)

    def add_client(self, client):
        client_id = self.generate_unique_id()
        self.clients[client_id] = Client(client.reader, client.writer, client.name)

    def remove_client(self, client_id):
        del self.clients[client_id]

    def get_clients(self):
        return self.clients

    async def broadcast_game_state(self):
        game_state_json = self.getGame()
        for client_id, client_data in self.clients.items():
            client_data['writer'].write(game_state_json.encode())
            await client_data['writer'].drain()

    def generate_unique_id(self):
        return str(uuid.uuid4())

    @staticmethod
    def getGameInstance():
        return Game.instance


if __name__ == "__main__":
    game = Game()
    a = game.generate_unique_id()
    b = game.generate_unique_id()
    c = game.generate_unique_id()
    
    print(a)
    print(b)
    print(c)