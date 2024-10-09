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
        self.active_player = None

        self.turn_steps = {1:"Waiting",2:"Draw",3:"Main",4:"Discard"}
        self.all_goals = []


    def ready(self):
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

    def random_first_active(self):
        self.active_player = random.choice(self.players)

    @property
    def active_player(self):
        return self._active_player

    @active_player.setter
    def active_player(self,newactive:Player):
        self._active_player = newactive

    @property
    def all_goals(self):
        self._all_goals.clear()
        for p in self.players:
            for g in p.current_phase:
                self._all_goals.extend(g)
        return self._all_goals

    @all_goals.setter
    def all_goals(self, newgoals):
        self._all_goals = newgoals

    # ID GETTERS
    def get_player_by_id(self, player_id):
        for player in self.players:
            if player.player_id == player_id:
                return player
    
    def get_goal_by_id(self, goal_id):
        for goal in self.all_goals():
            if goal.goal_id == goal_id:
                return goal

    def get_card_by_id(self, card_id):
        if isinstance(card_id, list):
            return self.get_cards_by_id(card_id)
        for p in self.players:
            for card in p.hand:
                if card.id == card_id:
                    return card
        for card in self.deck:
            if card.id == card_id:
                return card
        for card in self.discards:
            if card.id == card_id:
                return card
    
    def get_cards_by_id(self, ids):
        cards = []
        for p in self.players:
            for card in p.hand:
                if card.id == card_id:
                    cards.append(card)
        for card in self.deck:
            if card.id == card_id:
                cards.append(card)
        for card in self.discards:
            if card.id == card_id:
                cards.append(card)
        return cards
    
    def to_json(self):
        d = {}
        for i,p in enumerate(self.players,1):
            d[i] = p
        d["Deck"] = self.deck
        d["Discards"] = self.discards
        return d