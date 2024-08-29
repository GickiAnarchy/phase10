
import random
import copy
import os
import json
from itertools import cycle
import asyncio
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
        self.all_hands = []
        self.all_phases = []
        self.all_goals = []
        Game.instance = self
        
        self.clients = {}


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

    def checkWin(self, player) -> bool:
        '''
        Checks if player has won
        '''
        if player.getCurrentPhase() == None:
            print(f"{player.name} wins the game")
            return True
        else:
            return False


# Player handling
    def add_player(self, player):
        self.players.append(player)

    def getPlayer(self, player_name):
        for p in self.players:
            if p.name == player_name:
                return p


# Turn handling
    def player_draw(self, player):
        '''
        Called when player draws a card.
        '''
        player.drawCard(self.deck.drawCard())

    def player_discard(self, player, card):
        card = player.getCard(card)
        self.discards.addCard(card)

    

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
    def active_player(self):ß
        return self._active_player

    @active_player.setter
    def active_player(self, newactive):
        self._active_player = newactive


# Game class methods
    def getGame(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def getGameInstance():
        Game().instance = self
        return Game().instance


#############
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

    def get_clients(self):
        return self.clients

    async def broadcast_game_state(self):
        game_state_json = self.getGame()
        for client_id, client_data in self.clients.items():
            client_data['writer'].write(game_state_json.encode())
            await client_data['writer'].drain()


if __name__ == "__main__":
    pass