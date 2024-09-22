from typing import List

from card import Card


class Goal:
    goal_counter = 0
    def __init__(self, min_cards: int):
        Goal.goal_counter += 1
        self.min_cards = min_cards
        self.cards = []
        self.name = ""
        self.complete = False
        self.g_type = self.get_type()
        self.goal_id = Goal.goal_counter


    def check_cards(self, cards: List['Card']) -> bool:
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

    def add_cards(self, cards: List['Card']) -> bool:
        if self.check_cards(cards):
            self.cards.extend(cards)
            self.complete = len(self.cards) >= self.min_cards
            return True
        return False

    def sort_number(self):
        self.cards.sort(key=lambda x: x.number)

    def sort_color(self):
        self.cards.sort(key=lambda x: x.color)

    def get_type(self):
        if isinstance(self, SetGoal):
            return "Set"
        if isinstance(self, RunGoal):
            return "Run"
        if isinstance(self, ColorGoal):
            return "Color"



class SetGoal(Goal):
    def check_cards(self, cards: List['Card']) -> bool:
        if not cards:
            return False
        return all(card.number == cards[0].number for card in cards)


class RunGoal(Goal):
    def check_cards(self, cards: List['Card']) -> bool:
        if not cards:
            return False
        sorted_cards = sorted(cards, key=lambda c: c.number)
        return all(sorted_cards[i].number - sorted_cards[i - 1].number == 1
                   for i in range(1, len(sorted_cards)))


class ColorGoal(Goal):
    def check_cards(self, cards: List['Card']) -> bool:
        if not cards:
            return False
        return all(card.color == cards[0].color for card in cards)