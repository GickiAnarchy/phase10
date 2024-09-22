from typing import List
from .card import Card


class Goal:
    goal_counter = 0
    def __init__(self, min_cards: int):
        self.min_cards = min_cards
        self.cards = []
        self.complete = False
        self.name = ""
        Goal.goal_counter += 1
        self.goal_id = Goal.goal_counter


    def checkCards(self, cards: List['Card']) -> bool:
        pass

    def get_id(self):
        return self.goal_id

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