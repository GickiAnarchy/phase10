import json
from json import JSONEncoder
from typing import List


from phase10.game.card import Card
from phase10.game.goal import Goal, SetGoal, ColorGoal, RunGoal


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

    def to_json(self):
        return json.dumps(self.__dict__(), indent=4, cls=PhaseEncoder)

    def __dict__(self):
        return {"number": self.number,"name": self.name, "goals": self.goals}
    
    def __repr__(self):
        sup = super().__repr__()
        try:
            ret = self.to_json()
        except Exception as e:
            print(e)
            return sup
        return ret

#   #   #   #   @   #   #   #   #   #
class PhaseEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


#   #   #   #   @   #   #   #   #   #
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
