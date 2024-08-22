


from cards import Hand, Card, Phase, Goal


class Player():
    def __init__(self, name: str, **kwargs):
        self.name = name
        self.wins, self.losses = 0
        self.hand = Hand()
        self.phases = self.createPhases()

    #   Phase Interactions
    def createPhases(self) -> list:
        p_list = []
        for k,v in PHASES_DICT.items():
            v.setOwner(self.name)
            p_list.append(v)
        print(f"10 Phases created for {self.name}")
        return p_list

    def getCurrentPhase(self) -> Phase:
        for phase in self.phases:
            if not phase.complete:
                return phase
        return None
        
    #   Scoring
    def addPoints(self) -> int:
        for c in self.hand.cards:
            self.points += c.points
        print(f"{self.name} has {self.points} points")
        return self.points

    #   Turn Actions
    def drawCard(self, card):
        self.hand.addCards(card)

    def getCard(self, card) -> Card:
        ind = self.hand.getIndex(card)
        return self.hand.cards.pop(ind)

    #   Metadata
    def getPlayerData(self) -> dict:
        ret = {
            "name":self.name,
            "wins":self.wins,
            "losses":self.losses
            }
        return ret


PHASES_DICT = {
    1:Phase("Phase 1", [SetGoal(3), SetGoal(3)]),
    2:Phase("Phase 2",[SetGoal(3), RunGoal(4)]),
    3:Phase("Phase 3", [SetGoal(4), RunGoal(4)]),
    4:Phase("Phase 4", [RunGoal(7)]),
    5:Phase("Phase 5", [RunGoal(8)]),
    6:Phase("Phase 6", [RunGoal(9)]),
    7:Phase("Phase 7", [SetGoal(4), SetGoal(4)]),
    8:Phase("Phase 8", [ColorGoal(7)]),
    9:Phase("Phase 9", [SetGoal(5), SetGoal(2)]),
    10:Phase("Phase 10",[SetGoal(5), SetGoal(3)])
    }