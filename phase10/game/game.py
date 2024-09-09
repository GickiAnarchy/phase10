
import random
import copy
import os
import json
from itertools import cycle
import asyncio
from functools import wraps
import pprint
import pickle

from .cards import Card, SkipCard, Deck, Discards, Hand
from .player import Player, savePlayer, loadPlayer, getSaves
from .phases import Goal, Phase

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
        self.active_player = None
        self.deck = None
        self.discards = None
        
        """
        self.all_hands = []
        self.all_phases = []
        self.all_goals = []
        """

        self.game_locked = False
        
        Game.instance = self
        self.clients = {}

    def prestart(self) -> bool:
        if len(self.players) < 2:
            print("Not enough players to start")
            return False
        self.player_cycle = cycle(self.players)
        self.deck = Deck()
        self.discards = Discards()
        for player in self.players:
            player.hand.extend(self.deck.deal())
        self.random_starting_player()
        return True

    def random_starting_player(self):
        i = random.randint(1,10)
        for _ in i:
            self.active_player = next(self.player_cycle)
        print(f"{self.active_player.name} goes first.")

    def start(self):
        if self.prestart():
            self.game_locked = True

    # Player handling
    def add_player(self, player):
        if self.players == []:
            self.active_player = player
        self.players.append(player)
        print(f"{player.name} added to the game")

    def getPlayer(self, player_name):
        for p in self.players:
            if p.name == player_name:
                return p

    def getOpponent(self, player_name):
        for p in self.players:
            if p.name != player_name:
                return p

    def checkWin(self, player) -> bool:
        """
        Checks if player has won.

        Returns:
            bool
        """

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
            self.active_player = next(self.player_cycle)

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

    def play_on_goal(self, player, card, goal):
        pass

    def play_skip(self, card, opp) -> bool:
        try:
            opp.toggleSkip()
            self.discards.addCard(card)
        except:
            print("play skip failed")
            return False

    def getGoals(self):
        ret = []
        for p in self.players:
            ret.append(p.getCurrentPhase().getGoals())
        return ret

    # Game class methods
    @staticmethod
    def getGameInstance():
        return Game().instance

    def to_json(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def from_json(data = None):
        '''
        Updates the game instance.
        '''
        return Game(**json.loads(data))

    # Client/Server methods
    def add_client(self, client):
        self.clients[client.client_id] = client

    def remove_client(self, client_id):
        del self.clients[client_id]

    def get_clients(self) -> dict:
        return self.clients


if __name__ == "__main__":
    pass