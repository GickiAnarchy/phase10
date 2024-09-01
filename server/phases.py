
from abc import ABC, abstractmethod
from typing import List, Union




class Goal(ABC):
    count = 0
    def __init__(self, min_cards: int):
        self.min_cards = min_cards
        self.cards = []
        self.owner = None
        self.complete = False
        self.name = ""
        Goal.count += 1
        self.id = Goal.count

    def getID(self) -> int:
        return self.id

    @abstractmethod
    def checkCards(self, cards: List['Card']) -> bool:
        pass

    def setOwner(self, newowner) -> None:
        if self.owner == None:
            self.owner = newowner

    @property
    def name(self):
        if isinstance(self, SetGoal):
            self._name = f"Set of \n{self.min_cards} cards"
        if isinstance(self, RunGoal):
            self._name = f"Run of \n{self.min_cards} cards"
        if isinstance(self, ColorGoal):
            self._name = f"Colors of \n{self.min_cards} cards"
        return self._name

    @name.setter
    def name(self, newname):
        self._name = newname

    def addCards(self, cards: List['Card']) -> bool:
        if self.checkCards(cards):
            self.cards.extend(cards)
            self.complete = len(self.cards) >= self.min_cards
            return True
        return False

    def sortNumber(self):
        self.cards.sort(key=lambda x: x.number)

    def sortColor(self):
        self.cards.sort(key=lambda x: x.color)

class Phase:
    def __init__(self, name: str, goals: List[Goal]):
        self.name = name
        self.goals = goals
        self.owner = None
        self.complete = False

    def setOwner(self, newowner) -> None:
        if self.owner == None:
            self.owner = newowner
            for g in self.goals:
                g.setOwner(self.owner)

    def checkComplete(self) -> bool:
        self.complete = all(goal.complete for goal in self.goals)
        return self.complete

    def addCardsToGoal(self, goal_index: int, cards: List['Card']) -> bool:
        if 0 <= goal_index < len(self.goals):
            return self.goals[goal_index].addCards(cards)
        return False

    def grabAllCards(self) -> list:
        if self.checkComplete:
            cards_list = []
            for g in self.goals:
                cards_list.extend(g.cards)
            cards_list.resetWilds()
            return cards_list

    def getGoals(self) -> list:
        return [goal for goal in self.goals]

class SetGoal(Goal):
    def checkCards(self, cards: List['Card']) -> bool:
        if not cards:
            return False
        return all(card.number == cards[0].number for card in cards)

class RunGoal(Goal):
    def checkCards(self, cards: List['Card']) -> bool:
        if not cards:
            return False
        sorted_cards = sorted(cards, key=lambda c: c.number)
        return all(sorted_cards[i].number - sorted_cards[i - 1].number == 1
                   for i in range(1, len(sorted_cards)))

class ColorGoal(Goal):
    def checkCards(self, cards: List['Card']) -> bool:
        if not cards:
            return False
        return all(card.color == cards[0].color for card in cards)

