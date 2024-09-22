
from typing import List

from .card import Card
from .goal import SetGoal,RunGoal,ColorGoal,Goal



class Phase:
    def __init__(self, name: str, goals: List[Goal]):
        self.name = name
        self.goals = goals
        self.complete = False

    def checkComplete(self) -> bool:
        if self.goals == []:
            return False
        self.complete = all(goal.complete for goal in self.goals)
        return self.complete

    def addCardsToGoal(self, goal_index: int, cards: List['Card']) -> bool:
        if 0 <= goal_index < len(self.goals):
            return self.goals[goal_index].addCards(cards)
        return False

    def getGoals(self) -> list:
        return [goal for goal in self.goals]



PHASES_DATA = {
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
