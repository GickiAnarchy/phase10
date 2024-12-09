from phase10.server.game.gamesbase import GameBase





class RPS(GameBase):
    def __init__(self, p1=None, p2=None, m1=None, m2=None, rounds=None, score_keeper=None, **kwargs):
        super().__init__(**kwargs)
        self.max_players = 2
        print(f"{self.game_type} created....\nMax:{str(len(self.clients))}/{str(self.max_players)}")
        print(self.game_id)
        print("")
        self.p1 = p1
        self.p2 = p2
        self.m1 = m1
        self.m2 = m2
        if rounds is None:
            rounds = 3
        self.rounds = rounds # RPS Games are best 2 out of 3.
        if score_keeper is None:
            score_keeper = 0
        self.score_keeper = score_keeper   # score_keeper add 1 if player 1 wins a round and subtracts 1 if player 2 wins, does nothing if tied.

    def go(self):
        if self.is_waiting:
            print("This game is still waiting for players")
            return
        if not self.is_waiting:
            pass  # Launch game here

    def add_player(self, client):
        super().add_player(client)
        if self.p1 is None:
            self.p1 = client
            return True
        elif self.p2 is None:
            self.p2 = client
            return True
        else:
            return False

    # Add Game Logic Here
    def make_move(self, cl, move):
        if self.p1 == cl:
            self.m1 = move
            print(f"{cl} threw {self.m1}")
        if self.p2 == cl:
            self.m2 = move
            print(f"{cl} threw {self.m2}")
        if self.m1 is not None and self.m2 is not None:
            self.check_winner()

    def check_winner(self):
        a = self.m1.lower()
        b = self.m2.lower()
        self.m1 = None
        self.m2 = None
        # Check moves to find the winner of the round
        if a == b:
            print("It's a tie!")
        elif (a == 'rock' and b == 'scissors') or (a == 'scissors' and b == 'paper') or (a == 'paper' and b == 'rock'):
            print(f"{self.p1} wins!")
            if self.score_keeper < 1:  # Check if incrementing would exceed 1
                self.score_keeper += 1
        else:
            print(f"{self.p2} wins!")
            if self.score_keeper > -1:  # Check if decrementing would go below -1
                self.score_keeper -= 1
        # Subtract 1 from rounds
        self.rounds -= 1
        # Declares winner if there are no rounds left
        if self.rounds == 0:
            match self.score_keeper:
                case -1:
                    print(f"{self.p2} wins")
                case 0:
                    print("This should never occur")
                case 1:
                    print(f"{self.p1} wins")
                #TODO
                # Send win out

    # Serialization
    def to_dict(self):
        data = super().to_dict()
        data.update({
            "p1": self.p1,
            "p2": self.p2,
            "m1": self.m1,
            "m2": self.m2,
            "rounds":self.rounds,
            "score_keeper": self.score_keeper
        })
        return data

    @classmethod
    def from_dict(cls, data):
        super().from_dict(data)
        return cls(**data)
