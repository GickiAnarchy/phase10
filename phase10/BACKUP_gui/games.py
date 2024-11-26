import random

from kivy.properties import ObjectProperty, ListProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder

from phase10.client import GameClient
from phase10.game.classes.deck import Deck
from phase10.game.classes.player import Player
from phase10.gui.selectable import SelectableCard


Builder.load("games.kv")



class HighCardGame:
    def __init__(self, players):
        if players == None:
            players = []
        self.players = players
        self.scores = {player: 0 for player in players}
        self.deck = Deck()
        self.current_cards = {}

    def start_game(self):
        self.deck.create_deck_nmbrs()
        while len(self.deck.cards)>0:
            self.players[0].add_card(self.deck.draw_card())
            self.players[1].add_card(self.deck.draw_card())

    def flip_card(self):
        pass

    def get_game_state(self):
        return {
            "scores": self.scores,
            "current_cards": self.current_cards,
            "remaining_cards": {p: len(deck) for p, deck in self.decks.items()},
        }


class WarGame(Screen):
    player = ObjectProperty(None)
    opponent = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

