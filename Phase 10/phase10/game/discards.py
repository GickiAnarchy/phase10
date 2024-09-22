
#from card import Card

class Discards:
    def __init__(self):
        self.cards = []

    def number_of_cards(self):
        return len(self.cards)

    def get_top_card(self):
        if self.number_of_cards() <= 0:
            return None
        c = self.cards[-1]
        return (c.get_description(), c.get_image())

    def take_top_card(self):
        if self.number_of_cards() <= 0:
            return None
        return self.cards.pop()

    def add_card(self, card):
        self.cards.append(card)

    def get_image(self):
        if self.number_of_cards() == 0:
            return 'phase10/assets/images/empty_slot.png'
        else:
            (d,i) = self.get_top_card()
            return i

    def __iter__(self):
        return iter(self.cards)