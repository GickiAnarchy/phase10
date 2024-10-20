#!/usr/bin/env python

import random
import json
from json import JSONEncoder
import pickle

from .deck import Deck
from .discards import Discards
from .player import Player


class Game:
    def __init__(self):
        self.players = []
        self.deck = Deck()
        self.discards = Discards()
        self.turn_steps = {1:"Waiting",2:"Draw",3:"Main",4:"Discard", 5:"Done"}

    def ready(self):
        if len(self.players) >= 2:
            self.deck.create_deck()
            self.deck.shuffle()
            self.deal_cards()
            self.random_first_active()

    def add_player(self, pl):
        self.players.append(pl)

    def get_player_by_id(self, pid):
        for p in self.players:
            if p.player_id == pid:
                return p

    # CARD MANAGEMENT
    def deal_cards(self):
        for player in self.players:
            for i in range(10):
                player.add_card(self.deck.draw_card())
    
    def reshuffle_discards(self):
        print("reshuffling discards into deck")
        self.deck.cards.extend(self.discards.cards)
        self.deck.shuffle()

    # TURN MANAGEMENT
    def random_first_active(self):
        random.choice(self.players).toggle_active()
        self.active_player.current_turn_step = self.turn_steps[2]
    
    def next_turn(self):
        for p in self.players:
            if p.is_active:
                p.toggle_active()
                p.current_turn_step = self.turn_steps[1]
            elif not p.is_active: 
                p.toggle_active()
                p.current_turn_step = self.turn_steps[2]

    # "DRAW" STEP
    def draw_card(self, target:str, player:Player):
        if self.active_player == player:
            match target:
                case "Deck":
                    if not self.deck.can_take_card():
                        self.reshuffle_discards()
                    player.add_card(self.deck.draw_card())
                case "Discards":
                    if self.discards.can_take_card():
                        player.add_card(self.discards.take_top_card())
                case _:
                    return False
            player.current_turn_step = self.turn_steps[3]
            return True

    # "MAIN" STEP
    def play_card(self, target:str, card_id:int, player:Player, goal_id = None, target_player_id = None) -> bool:
        card = player.take_card_by_id(card_id)
        match target:
            case "play_goal":
                for goal in player.get_goals():
                    if goal.goal_id == goal_id:
                        if goal.check_cards(card):
                            goal.add_cards(card)
                            player.current_turn_step = self.turn_steps[4]
                            return True
            case "play_skip":
                self.discards.add_card(card)
                player.current_turn_step = self.turn_steps[4]
                #add add skip to player
                return True
        player.add_card(card)
        return False

    # "DISCARD" STEP
    def discard_card(self, card_id, player):
        if self.active_player == player:
            self.discards.add_card(player.take_card_by_id(card_id))
            player.current_turn_step = self.turn_steps[5]

    # PROPERTIES
    @property
    def active_player(self):
        for p in self.players:
            if p.is_active:
                return p

    # JSON
    def to_json(self):
        data = json.dumps(self, indent = 4, cls = GameEncoder)
        return data

#   #   #   #   #   #   #   #   #   #
class GameEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__