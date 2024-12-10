from dataclasses import dataclass


@dataclass
class Player:
    name: str
    rps_win_loss: tuple


class RPS:
    def __init__(self, p1 = None, p2 = None):
        self.p1 = p1
        self.p2 = p2
        self.rounds = 3
        self.m1 = None
        self.m2 = None
        self.score_keeper = 0

    @property
    def is_waiting(self):
        if self.p1 is None or self.p2 is None:
            return True
        else:
            return False

    @@property
    def round_over(self):
        return self.m1 is not None and self.m2 is not None

    def add_player(self, player):
        if self.is_waiting:
            if self.p1 is None:
                self.p1 = player
                return
            if self.p2 is None:
                self.p2 = player
                return

    def  make_move(self, player, move):
        if self.p1 == player and self.m1 is None:
            self.m1 = move
        if self.p2 == player and self.m2 is None:
            self.m2 = move
        if self.round_over:
            self.check_winner()

    def check_winner(self):
        a = self.m1.lower()
        b = self.m2.lower()
        self.m1 = None
        self.m2 = None
        # Check moves to find the winner of the round
        if a == b:
            print("It's a tie!")
            return
        elif (a == 'rock' and b == 'scissors') or (a == 'scissors' and b == 'paper') or (a == 'paper' and b == 'rock'):
            print(f"{self.p1} wins!")
            if self.score_keeper < 1:  # Check if incrementing would exceed 1
                self.score_keeper += 1
        else:
            print(f"{self.p2} wins!")
            if self.score_keeper > -1:  # Check if decrementing would go below -1
                self.score_keeper -= 1

        self.rounds -= 1
        if self.rounds == 0:
            print("Game Over")
            match self.score_keeper:
                case -1:
                    print(f"{self.p2} wins")
                case 0:
                    print("This should never occur")
                case 1:
                    print(f"{self.p1} wins")
                # TODO
                # Send win out