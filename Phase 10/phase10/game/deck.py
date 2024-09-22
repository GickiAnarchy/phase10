
from random import shuffle

from card import Card, Wild, Skip


class Deck:
    def __init__(self):
        self.cards = []
        self.image = "phase10/assets/images/CardBack.png"

    def create_deck(self):
        for w in range(8):
            self.cards.append(Wild())
        for s in range(4):
            self.cards.append(Skip())
        for c in ["Red", "Blue","Green","Yellow"]:
            for x in range(2):
                for n in range(12):
                    card = Card(n + 1,c)
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
