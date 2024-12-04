#!/usr/bin/env python

from random import shuffle

from phase10.server.classes.card import Card, Wild, Skip


class Deck:
    def __init__(self, name = "Deck", cards=None, image ="phase10/assets/images/CardBack.png"):
        if cards is None:
            cards = []
        self.cards = cards
        self.name = name
        self.image = image
        self.used = False

    def can_take_card(self):
        if len(self.cards) >= 1:
            return True
        else:
            return False

    def create_deck(self):
        self.used = True
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

    def clear_deck(self):
        self.cards.clear()
        Card.count = 0
        self.used = False
        print("deck cleared and reset")

    def __iter__(self):
        return iter(self.cards)

    def print_cards(self):
        for i,c in enumerate(self.cards):
            print(f"{i}\n{c.get_description()}")

    def to_dict(self):
        cards_dict = []
        for c in self.cards:
            cards_dict.append(c.to_dict())
        return {"name":self.name,"cards":cards_dict,"image":self.image}

    @classmethod
    def from_dict(cls, data):
        cards = []
        for c in data.get('cards'):
            cards.append(Card.from_dict(c))
        return cls(name = data.get('name'), cards = cards, image = data.get('image'))