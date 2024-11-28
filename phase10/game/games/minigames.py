

class RPS(BaseGame):
    def __init__(**kwargs):
        super().__init__(**kwargs)
        self.choices = ["Rock","Paper","Scissors"]
        self.max_plyrs = 2
        self.p1_choice = None
        self.p2_choice = None
    
    def start(self):
        if self.check_max_players():
            return True
        return False

    def make_choice(self, player, choice):
        if player == self.p1 and self.p1_choice:
            self.p1_choice = choice
            return True
        if player == self.p2 and self.p2_choice:
            self.p2_choice = choice
            return True
        return False

    def get_choices(self, clear = False):
        if self.p1_choice and self.p2_choice:
            ret = self.p1_choice,self.p2_choice
            if clear:
                self.p1_choice, self.p2_choice = None, None
            return ret

    def add_player(self, player):
        if self.check_max_players():
            self.players.append(player)

    def check_max_players(self):
        if len(self.players) > self.max_plyrs:
            return False
        else:
            return True

    def check_win(self):
        c1, c2 = self.get_choices(clear = True)
        if c1 == c2:
            return p1,p2
        if c1 == "Scissors":
            if c2 == "Paper":
                return self.p1
            if c2 == "Rock":
                return self.p2
        if c1 == "Paper":
            if c2 == "Scissors":
                return self.p2
            if c2 == "Rock":
                return self.p1
        if c1 == "Rock":
            if c2 == "Paper":
                return self.p2
            if c2 == "Scissors":
                retuen self.p1
        else:
            return None

    @property
    def p1(self):
        return self.players[0]
    
    @property
    def p2(self):
        return self.players[1]

    def to_dict(self):
        return {
            "game_id":self.game_id,
            "players":self.players,
            "p1_choice":self.p1_choice,
            "p2_choice":self.p2_choice
        }
    
    @classmethod
    def from_dict(cls, data):
        obj = cls(
            game_id = data.get("game_id"),
            players = data.get("players"),
            p1_choice = data.get("p1_choice"),
            p2_choice = data.get("p2_choice")
        )
        return obj