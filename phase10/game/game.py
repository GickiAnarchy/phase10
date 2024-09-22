
import random
import copy
import os
import json
from itertools import cycle
import asyncio
from functools import wraps
import pprint
import pickle
import uuid

from .cards import Card, SkipCard, Deck, Discards, Hand
from .player import Player, savePlayer, loadPlayer, getSaves
from .phases import Goal, Phase

'''
def singleton(cls):
    instance = None

    @wraps(cls)
    def __init__(self, *args, **kwargs):
        if instance is not None:
            raise Exception("Singleton already created")
        instance = super().__init__(*args, **kwargs)
        return instance
    return cls
'''

#@singleton

class Game:
    def __init__(self):
        self.game_id = uuid.uuid4()
        self.players = []
        self.deck = None
        self.discards = None


    def prestart(self) -> bool:
        if len(self.players) < 2:
            print("Not enough players to start")
            return False
        self.deck = Deck()
        self.discards = Discards()
        for player in self.players:
            player.hand.extend(self.deck.deal())
        return True

    def start(self):
        if self.prestart():
            self.game_locked = True

    # Player handling
    def add_player(self, player):
        player = Player(Player)
        print(f"{player.name} added to the game")
        if len(self.players) >= 2:
            self.start()

    def getPlayer(self, player_name):
        for p in self.players:
            if p.name == player_name:
                    return p

    def getOpponent(self, player_name):
        for p in self.players:
            if p.name != player_name:
                return p

    def checkWin(self, player) -> bool:
        if player.getCurrentPhase().name == "All complete!":
            print(f"{player.name} wins the game")
            return True
        else:
            return False

    def deal_cards(self):
        for p in self.players:
            p.addCards(self.deck.deal())

    def checkPlayerSkip(self, player):
        if player.skipped:
            player.toggleSkip()

    # Turn handling
    def draw_from_deck(self, player) -> bool:
        try:
            player.drawCard(self.deck.drawCard())
            print(f"{player.name} draws a card.")
            return True
        except:
            print("draw card failed")
            return False

    def draw_from_discards(self, player) -> bool:
        card = self.discards.getTopCard()
        if card != None:
            player.drawCard(card)
            return True
        else:
            print("draw card failed")
            return False

    def discard(self, player, card) -> bool:
        try:
            card = player.getCard(card)
            self.discards.addCard(card)
            return True
        except:
            print("discard failed")
            return False

    def play_pass(self, player) -> bool:
        print(f"{player.name} passed their turn.")
        return True

    def play_on_goal(self, player, card, goal) -> bool:
        if not isinstance(card, list):
            card = [card]
        if g in self.getGoals(player):
            g.addCards(card)
        else:
            return False

    def play_skip(self, card, opp) -> bool:
        try:
            opp.toggleSkip()
            self.discards.addCard(card)
        except:
            print("play skip failed")
            return False


#Game Data
    def getGoals(self, player) -> list:
        return player.getCurrentPhase().getGoals()
    
    @staticmethod
    def check_card_count() -> bool:
        return Card().count == 108

    # Game class methods
    def to_json(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def from_json(data = None):
        '''
        Updates the game instance.
        This shouldn't needed, since the client doesnt make any changes directly to the Game
        '''
        return Game(**json.loads(data))

