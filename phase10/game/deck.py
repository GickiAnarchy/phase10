#!/usr/bin/env python

import json
from json import JSONEncoder
from random import shuffle

from .card import Card, Wild, Skip


class Deck:
    def __init__(self):
        self.cards = []
        self.name = "Deck"
        self.image = "phase10/assets/images/CardBack.png"

    def can_take_card(self):
        if len(self.cards) >= 1:
            return True
        else:
            return False

    def create_deck(self):
        if Card.count >= 108:
            raise Exception("Too many Cards")
            return
        for w in range(8):
            self.cards.append(Wild())
        for s in range(4):
            self.cards.append(Skip())
        for c in ["Red", "Blue", "Green", "Yellow"]:
            for x in range(2):
                for n in range(12):
                    card = Card(n + 1, c)
                    self.cards.append(card)

    def remaining_cards(self):
        return len(self.cards)

    def draw_card(self):
        return self.cards.pop()

    def shuffle(self):
        shuffle(self.cards)
        shuffle(self.cards)
        shuffle(self.cards)

    def __iter__(self):
        return iter(self.cards)

    def to_dict(self):
        data = json.dumps(self, indent=4, cls=DeckEncoder)
        return data


#   #   #   #   @   #   #   #   #   #
class DeckEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
