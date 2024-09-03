
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
        self.all_hands = []
        self.all_phases = []
        self.all_goals = []

        self.game_locked = False
        
        Game.instance = self
        self.clients = {}

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
        if self.players == []:
            self.active_player = player
        self.players.append(player)
        print(f"{player.name} added to the game")

    def getPlayer(self, player_name):
        for p in self.players:
            if p.name == player_name:
                return p

    def checkWin(self, player) -> bool:
        """
        Checks if player has won.

        Returns:
            bool
        """

        if player.getCurrentPhase() == None or player.getCurrentPhase().name == "All complete!":
            print(f"{player.name} wins the game")
            return True
        else:
            return False

    # Turn handling
    def draw(self, player, from_deck = True) -> bool:
        '''
        Called when player draws a card.

        Args:
            player: player that is drawing
            from_deck: True if player drawing from the deck, False if the player pulls from the discard pile.

        Returns:
            bool: True if method was successful
        '''

        if self.active_player != player:
            return False
        if self.active_player.skipped:
            #skip player
            return False
        if from_deck:
            player.drawCard(self.deck.drawCard())
            return True
        if not from_deck:
            player.drawCard(self.discards.pop())
            return True

    def discard(self, player, card) -> bool:
        card = player.getCard(card)
        self.discards.addCard(card)
        #next players turn
        return True

    def play(self, player, cards, target):
        if not isinstance(cards, list):
            cards = [cards]
        cards = player.getCards(cards)
        if isinstance(target, Goal):
            target.addCards(cards)
        if isinstance(cards[0], SkipCard) and isinstance(target, Player):
            cards = player.getCard(cards[0])
            target.toggleSkip()
            self.discards.addCard(cards)

    # Property Methods  
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
        return self._active_player

    @active_player.setter
    def active_player(self, newactive):
        self._active_player = newactive


    ####
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


############
    # Client/Server methods
    def add_client(self, client):
        self.clients[client.client_id] = client

    def remove_client(self, client_id):
        del self.clients[client_id]

    def get_clients(self) -> dict:
        return self.clients


if __name__ == "__main__":
    pass