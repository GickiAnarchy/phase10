

import random
import copy
import os
import json
from itertools import cycle

from cards import Deck, Discards, Hand
from phases import Phase, Goal
from player import Player


##
##
class Game:
    def __init__(self):
        self.players = []
        self.deck = None
        self.discards = None
        self.current_goals = []

    def prestart(self) -> bool:
        if len(self.players) < 2:
            print("Not enough players to start")
            return False
        self.deck = Deck()
        self.discards = Discard()
        for player in self.players:
            player.hand.extend(self.deck.deal())
        return True
    
    def start(self):
        if self.prestart():
            pass

    def addPlayer(self, player):
        self.players.append(player)

    @property
    def current_goals(self):
        self._current_goals = []
        for p in self.players:
            self._current_goals.extend(p.getCurrentPhase().getGoals())
        return self._current_goals

    @current_goals.setter
    def current_goals(self, newgoals):
        if isinstance(newgoals, list):
            self._current_goals = newgoals
        if isinstance(newgoals, Goal):
            newgoals = [newgoals]




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