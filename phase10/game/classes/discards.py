#!/usr/bin/env python

from phase10.game.classes.card import Card


class Discards:
    def __init__(self, name = "Discards", cards = None):
        self.name = name
        if cards is None:
            cards = []
        self.cards = cards

    def number_of_cards(self):
        return len(self.cards)

    def can_take_card(self) -> bool:
        if self.number_of_cards() <= 0:
            return False
        if self.cards[-1].name == "Skip":
            return False
        return True

    def get_top_card(self):
        if self.number_of_cards() <= 0:
            return None
        c = self.cards[-1]
        return (c.get_description(), c.image())

    def take_top_card(self):
        if self.can_take_card():
            return self.cards.pop(-1)
        else:
            return None

    def add_card(self, card):
        self.cards.append(card)

    @property
    def image(self):
        if self.number_of_cards() == 0:
            return 'phase10/assets/images/empty_slot.png'
        else:
            (d, i) = self.get_top_card()
            return i

    def __iter__(self):
        return iter(self.cards)

    # JSON
    def to_dict(self):
        cards_list = []
        if len(self.cards) > 0:
            for c in self.cards:
                cards_list.append(c.to_dict())
        return {"name":self.name,"cards":cards_list,"image":self.image}

    @classmethod
    def from_dict(cls, data):
        cards = []
        for c in data.get('cards'):
            cards.append(Card.from_dict(c))
        return cls(name = data.get('name'), cards = cards)