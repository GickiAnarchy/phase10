from uuid import uuid4

from phase10.game.classes.deck import Deck


class War:
    def __init__(self, **kwargs):
        self.game_id = str(uuid4())
        self.player1 = None
        self.p1_card = None
        self.p2_card = None
        self.player2 = None
        self.deck:Deck = Deck()
        self.discards = []

    def join_player(self, player):
        if not self.player1:
            self.player1 = player
            print(f"Player 1 is {self.player1.name}")
        elif not self.player2:
            self.player2 = player
            print(f"Player 2 is {self.player2.name}")

    def start_game(self):
        if self.player1 and self.player2:
            self.deck.create_deck()
            x = 12
            self.deck.cards = self.deck.cards[x:]
            self.deck.print_cards()
            self.deck.shuffle()
            while len(self.deck.cards) > 0:
                self.player1.add_card(self.deck.draw_card())
                self.player2.add_card(self.deck.draw_card())

    def lay_card(self, player_id):
        if self.player1.player_id == player_id:
            self.p1_card = self.player1.hand.pop()
            return True
        if self.player2.player_id == player_id:
            self.p2_card = self.player2.hand.pop()
            return True
        return False

    def check_winner(self):
        if self.p1_card == self.p2_card:
            print("Draw")
        if self.p1_card > self.p2_card:
            print(f"{self.player1.name} Won")
        if self.p1_card < self.p2_card:
            print(f"{self.player2.name} Won")
        self.discards.append(self.p1_card)
        self.discards.append(self.p2_card)
        self.p1_card = None
        self.p2_card = None

    def to_dict(self):
        return {
            "game_id": str(self.game_id),
            "player1": self.player1.to_dict(),
            "player2": self.player2.to_dict(),
            "deck": self.deck.to_dict(),
            "p1_card": self.p1_card.to_dict() if self.p1_card else None,
            "p2_card": self.p2_card.to_dict() if self.p2_card else None
        }

    @classmethod
    def from_dict(cls, data):
        obj = cls(
            game_id = data.get("game_id"),
            player1 = data.get("player1"),
            player2 = data.get("player2"),
            deck = data.get("deck"),
            p1_card = data.get("p1_card"),
            p2_card = data.get("p2_card")
        )
        return obj