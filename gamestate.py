

class GameState:
    def __init__(self):
        self.players = []
        self.deck = Deck()
        self.discard_pile = Stack()
        self.current_plays = []  # List of lists, each inner list represents a set or run
        self.current_player_index = 0
        self.phase_data = {}  # Dictionary to store player's phase information

    def update(self, player, card):
        # Remove card from player's hand
        player.hand.remove(card)

        # Check if card can be added to an existing set or run
        # ...

        # If no existing set or run, create a new one
        # ...

        # Check for phase completion
        # ...

    def to_json(self):
        return json.dumps(self.__dict__)

    @classmethod
/    def from_json(cls, data):
        return GameState(**json.loads(data))
