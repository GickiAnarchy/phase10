from typing import List

from card import Card
from goal import SetGoal, RunGoal, ColorGoal, Goal


class Phase:
    def __init__(self, number, name: str, goals: List[Goal]):
        self.number = number
        self.name = name
        self.goals = goals
        self.complete = False

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
        g = [g.to_dict() for g in self.goals]
        return {
            "number":self.number,
            "name":self.name,
            "goals":self.goals,
            "complete":self.complete
        }
        
"""
    def check_for_plays(self, cards, wilds = 0):
        possible_plays = 0
        for g in self.goals:
            #Sort Cards
            if g.g_type in ["Set", "Run"]:
                cards.sort(key=lambda x: x.number)
            elif g.g_type == "Color":
                cards.sort(key=lambda x: x.color)
            #Check conditions
            if not g.complete:
                for i in range(wilds):
                    i += 1
                    cards.append(Wild())
                    for group in iterate_by_groups(cards, g.min_cards - i):
                        if g.check_cards(group):
                            possible_plays += 1
            elif g.complete:
                for card in iterate_by_groups(cards, 1):
                    if g.check_cards(card):
                        possible_plays += 1
        print("checked")
        return possible_plays
        """




PHASES_DATA = {
    1: Phase(1, "Phase 1", [SetGoal(3), SetGoal(3)]),
    2: Phase(2, "Phase 2", [SetGoal(3), RunGoal(4)]),
    3: Phase(3, "Phase 3", [SetGoal(4), RunGoal(4)]),
    4: Phase(4, "Phase 4", [RunGoal(7)]),
    5: Phase(5, "Phase 5", [RunGoal(8)]),
    6: Phase(6, "Phase 6", [RunGoal(9)]),
    7: Phase(7, "Phase 7", [SetGoal(4), SetGoal(4)]),
    8: Phase(8, "Phase 8", [ColorGoal(7)]),
    9: Phase(9, "Phase 9", [SetGoal(5), SetGoal(2)]),
    10: Phase(10, "Phase 10", [SetGoal(5), SetGoal(3)])
}
