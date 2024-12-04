#!/usr/bin/env python

from typing import List

from phase10.server.classes.card import Card


class Goal:
    goal_counter = 0
    def __init__(self, min_cards=None, cards=None, name=None, complete=None, g_type=None, goal_id=None):
        Goal.goal_counter += 1
        self.min_cards = min_cards
        if cards is None:
            cards = []
        self.cards = cards
        self.name = name
        if complete is None:
            complete = False
        self.complete = complete
        self.g_type = g_type
        if goal_id is None:
            goal_id = Goal.goal_counter
        self.goal_id = goal_id

    def check_cards(self, cards: List['Card']) -> bool:
        match self.g_type:
            case 'Set':
                self.set_check_cards(cards)
            case 'Run':
                self.run_check_cards(cards)
            case 'Color':
                self.color_check_cards(cards)

    def get_id(self):
        return self.goal_id

    @property
    def name(self):
        match self.g_type:
            case 'Set':
                self._name = f"Set of \n{self.min_cards} cards"
            case 'Run':
                self._name = f"Run of \n{self.min_cards} cards"
            case 'Color':
                self._name = f"Colors of \n{self.min_cards} cards"
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    def add_cards(self, cards: List['Card']) -> bool:
        if self.check_cards(cards):
            self.cards.extend(cards)
            self.complete = len(self.cards) >= self.min_cards
            return True
        return False

    def check_complete(self):
        if len(self.cards) >= self.min_cards:
            if self.check_cards(self.cards):
                self.complete = True
        return False

    def sort_number(self):
        self.cards.sort(key=lambda x: x.number)

    def sort_color(self):
        self.cards.sort(key=lambda x: x.color)

    def set_check_cards(self, cards: List['Card']) -> bool:
        if not cards:
            return False
        return all(card.number == cards[0].number for card in cards)

    def run_check_cards(self, cards: List['Card']) -> bool:
        if not cards:
            return False
        sorted_cards = sorted(cards, key=lambda c: c.number)
        return all(sorted_cards[i].number - sorted_cards[i - 1].number == 1
                   for i in range(1, len(sorted_cards)))

    def color_check_cards(self, cards: List['Card']) -> bool:
        if not cards:
            return False
        return all(card.color == cards[0].color for card in cards)

    def to_dict(self):
        return {
            "min_cards": self.min_cards,
            "cards": self.cards,
            "name": self.name,
            "complete": self.complete,
            "goal_id": self.goal_id,
            "g_type": self.g_type
        }

    @classmethod
    def from_dict(cls, data):
        if isinstance(data, Goal):
            return data
        obj = cls(
            min_cards=data.get("min_cards"),
            cards=[Card.from_dict(c) for c in data.get("cards", [])],
            name=data.get("name"),
            complete=data.get("complete"),
            goal_id=data.get("goal_id"),
            g_type=data.get("g_type")
        )
        return obj