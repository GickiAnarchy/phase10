#!/usr/bin/env python

class Discards:
    def __init__(self):
        self.name = "Discards"
        self.cards = []

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
        return (c.get_description(), c.get_image())

    def take_top_card(self):
        if self.can_take_card():
            return self.cards.pop(-1)
        else:
            return None

    def add_card(self, card):
        self.cards.append(card)

    def get_image(self):
        if self.number_of_cards() == 0:
            return 'phase10/assets/images/empty_slot.png'
        else:
            (d, i) = self.get_top_card()
            return i

    def __iter__(self):
        return iter(self.cards)
    
    def to_dict(self):
        return {
            "cards": [c.to_dict() for c in self.cards]
        }
