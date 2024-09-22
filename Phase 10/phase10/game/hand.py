from card import Card


class Hand:
    def __init__(self, cards = []):
        self.cards = cards
        self.wilds,self.skips = self.count_wilds_and_skips()

    def __iter__(self):
        return iter(self.cards)

    def add_to_hand(self, cards):
        if isinstance(cards, Card):
            cards = [cards]
        self.cards.extend(cards)
        self.update()

    def remove_card(self, card):
        self.cards.remove(card)

    def get_length(self):
        return len(self.cards)

    def count_wilds_and_skips(self):
        wilds_count = 0
        skips_count = 0
        for card in self.cards:
            if card.is_wild:
                wilds_count += 1
            if card.is_skip:
                skips_count += 1
        return wilds_count, skips_count

    def update(self):
        self.wilds,self.skips = self.count_wilds_and_skips()

    def iterate_by_groups(self, group_size, keep_wilds ):
        if keep_wilds:
            cards = self.get_basic_cards(keep_wilds=True)
        else:
            cards = self.get_basic_cards()
        for i in range(len(cards) - group_size + 1):
            yield cards[i:i + group_size]

    def get_basic_cards(self, keep_wilds = False):
        basic = []
        for card in self.cards:
            if card.is_skip:
                continue
            if card.is_wild:
                if keep_wilds:
                    basic.append(card)
                    continue
                else:
                    continue
            else:
                basic.append(card)
        return basic

    def print_hand(self):
        for i,card in enumerate(self.cards):
            print(f"{i}-\t{card.get_description()}\n")

    def sort_number(self):
        self.cards.sort(key=lambda x: x.number)

    def sort_color(self):
        self.cards.sort(key=lambda x: x.color)