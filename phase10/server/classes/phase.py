from phase10.server.classes.card import Card
from phase10.server.classes.goal import Goal


class Phase:
    def __init__(self, number = 0, name: str = "", goals=None, complete = False):
        if goals is None:
            goals = []
        self.number = number
        self.name = name
        self.goals = goals
        self.complete = complete

    @classmethod
    def make_phase(cls, n):
        return PHASES_DATA[n]

    def check_complete(self) -> bool:
        if self.goals == []:
            return False
        self.complete = all(goal.complete for goal in self.goals)
        return self.complete

    def get_goals(self) -> list:
        return self.goals

    def try_cards(self, cards):
        if isinstance(cards, Card):
            cards = [cards]
        can_play = 0
        for goal in self.goals:
            if goal.check_cards(cards):
                can_play += 1
        if can_play > 0:
            return True
        else:
            return False

    def play_cards(self, cards, goal_id):
        if isinstance(cards, Card):
            cards = [cards]
        if self.try_cards(cards):
            for goal in self.goals:
                if goal.goal_id == goal_id:
                    goal.add_cards(cards)

    def to_dict(self):
        return {"name": self.name,
               "number": self.number,
               "goals":[g.to_dict() for g in self.goals],
               "complete": self.complete}

    @classmethod
    def from_dict(cls, data):
        obj = cls(
            number=data.get("number"),
            name=data.get("name"),
            goals=[Goal.from_dict(g) for g in data.get("goals", [])],
            complete=data.get("complete")
        )
        return obj


#   #   #   #   @   #   #   #   #   #
PHASES_DATA = {
    1: Phase(1, "Phase 1", [Goal(3,g_type = "Set"), Goal(3,g_type = "Set")]),
    2: Phase(2, "Phase 2", [Goal(3,g_type = "Set"), Goal(4,g_type = "Run")]),
    3: Phase(3, "Phase 3", [Goal(4,g_type = "Set"), Goal(4,g_type = "Run")]),
    4: Phase(4, "Phase 4", [Goal(7,g_type = "Run")]),
    5: Phase(5, "Phase 5", [Goal(8,g_type = "Run")]),
    6: Phase(6, "Phase 6", [Goal(9,g_type = "Run")]),
    7: Phase(7, "Phase 7", [Goal(4,g_type = "Set"), Goal(4,g_type = "Set")]),
    8: Phase(8, "Phase 8", [Goal(7,g_type = "Color")]),
    9: Phase(9, "Phase 9", [Goal(5,g_type = "Set"), Goal(2,g_type = "Set")]),
    10: Phase(10, "Phase 10", [Goal(5,g_type = "Set"), Goal(3,g_type = "Set")])
}
