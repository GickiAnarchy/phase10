from card import Card
from deck import Deck
from discards import Discards
from game import Game
from player import Player


def test_deck_create():
    deck = Deck()
    deck.create_deck()


def test_discard_from_deck():
    deck = Deck()
    print("Deck initialized")
    discards = Discards()
    print("Discards initialized")
    deck.create_deck()
    print("Deck created")
    deck.shuffle()
    print("Deck Shuffled")
    discards.add_card(deck.draw_card())
    print("Card drawn from deck and added to discards")
    print(f"Cards:{Card.get_count()}")
    topd, topi = discards.get_top_card()
    print("called on discards.get_top_card()")
    print(f"{topd} was the top card.")
    print(f"Cards:{Card.get_count()}")


def test_hand_sorting():
    deck = Deck()
    deck.create_deck()
    deck.shuffle()
    hand = Hand()
    for i in range(10):
        hand.add_to_hand(deck.draw_card())
        print(f"\tDeck amt: {deck.remaining_cards()}\n\tTotal cards: {Card.get_count()}\n")
    hand.sort_color()
    hand.print_hand()
    hand.sort_number()
    hand.print_hand()
    for group in hand.iterate_by_groups(2):
        print(f"{group[0].get_description()}")
        print(f"{group[1].get_description()}")
    print(f"Wilds: {hand.wilds}\nSkips: {hand.skips}")


def test_hand_possible_plays():
    deck = Deck()
    deck.create_deck()
    deck.shuffle()
    player = Player("Corey")
    for i in range(10):
        player.hand.add_to_hand(deck.draw_card())
        print(f"\tDeck amt: {deck.remaining_cards()}\n\tTotal cards: {Card.get_count()}\n")
    poss = player.check_for_plays()
    player.hand.print_hand()
    print(f"{poss}")


def test_serialize():       #working
    player = Player("Corey")
    g = Game()
    g.add_player(player)
    g.ready()
    d = player.to_dict()
    return d


if __name__ == "__main__":
    print(test_serialize())