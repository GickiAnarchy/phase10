from card import Card,Wild,Skip

class Deck():
    def __init__(self):
        self.cards = []

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



