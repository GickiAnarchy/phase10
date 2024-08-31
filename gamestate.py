

import pickle
from dataclasses import dataclass

from cards import Hand, Deck, Discards, Card
from phases import Goal, Phase
from player import Player
from game import Game

@dataclass
class Gamestate:
     players:list
     hands:list
     deck: Deck
     discards: Discards
     phases: list
     goals: list
     active_player: Player



def createGamestate():
    game = Game().getGameInstance()
    return Gamestate(game.players, game.all_hands, game.deck, game.discards, game.all_phases,
    game.all_goals, game.active_player)


















