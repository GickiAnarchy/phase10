

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


















