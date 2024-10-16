#!/usr/bin/env python

import random

from .deck import Deck
from .discards import Discards
from .player import Player


class Game:
    def __init__(self):
        self.players = []
        self.deck = Deck()
        self.discards = Discards()
        self.turn_steps = {1:"Waiting",2:"Draw",3:"Main",4:"Discard"}


    def ready(self):
        if len(self.players) >= 2:
            self.deck.create_deck()
            self.deck.shuffle()
            self.deal_cards()
            self.random_first_active()

    def add_player(self, pl):
        self.players.append(pl)

    def deal_cards(self):
        for player in self.players:
            for i in range(10):
                player.add_card(self.deck.draw_card())


    # TURN MANAGEMENT
    def random_first_active(self):
        random.choice(self.players).toggle_active()
        self.active_player.current_turn_step = self.turn_steps[2]


    def draw_card(self, target:str, player:Player):
        if self.active_player == player:
            match target:
                case "Deck":
                    player.add_card(self.deck.draw_card())
                case "Discards":
                    player.add_card(self.discards.take_top_card())
                case _:
                    return False
            return True

    def discard_card(self, card_id, player):
        if self.active_player == player:
            self.discards.add_card(player.take_card_by_id(card_id))

















    # PROPERTIES
    @property
    def active_player(self):
        for p in self.players:
            if p.is_active:
                return p

