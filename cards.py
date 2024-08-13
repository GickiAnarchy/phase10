

import random
import copy
import os
import json
import itertools
from abc import ABC, abstractmethod
from typing import List, Union
from itertools import cycle


""" Phase 10 Card Classes """

class Card():
    count = 0
    def __init__(self, name: str, points: int, color: str):
        self.name = name
        self.points = points
        Card.count += 1
        self.color = color
        self.number = number_value[self.name]

    def description(self):
        if self.color == "None":
            return self.name
        else:
            return f"{self.color} {self.name}"

    def getImage(self):
        image_directory = "./images/"
        if isinstance(self, WildCard):
            return f"{image_directory}Wild.png"
        if isinstance(self, SkipCard):
            return f"{image_directory}Skip.png"
        return f"{image_directory}{self.color}_{self.number}.png"

    @classmethod
    def getCount(cls):
        return cls.count

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, newname):
        self._name = newname

    @name.deleter
    def name(self):
        del self._name

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, newcolor):
        self._color = newcolor

    @color.deleter
    def color(self):
        del self._color

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, newpoints):
        self._points = newpoints

    @points.deleter
    def points(self):
        del self._points

    def __eq__(self, other):
        return self.number == other

    def __lt__(self, other):
        return self.number < other.number

    def __gt__(self, other):
        return self.number > other.number

class WildCard(Card):
    def __init__(self, name="Wild", points=25, color="None"):
        super().__init__(name, points, color)
        self.mimic = None

    def description(self):
        ret = super().description()
        return f"**{ret}"

    def set_mimic(self, card):
        if isinstance(card, Card):
            self.mimic = card

    def __eq__(self, other):
        if other.name == "Skip":
            return False
        else:
            self.set_mimic(other)

    def __lt__(self, other):
        if other.name == "Skip":
            return False
        else:
            self.set_mimic(other)
            return True

    def __gt__(self, other):
        if other.name == "Skip":
            return False
        else:
            self.set_mimic(other)
            return True

class SkipCard(Card):
    def __init__(self, name="Skip", points=25, color="None"):
        self.number = 60
        super().__init__(name, points, color)

    def __eq__(self, other):
        return self.number == other

    def __lt__(self, other):
        return False

    def __gt__(self, other):
        return False

class BasicCard(Card):
    def __init__(self, name: str, points: int, color: str):
        super().__init__(name, points, color)

class LowCard(BasicCard):
    def __init__(self, name: str, color: str, points=5):
        super().__init__(name, points, color)

class HighCard(BasicCard):
    def __init__(self, name: str, color: str, points=10):
        super().__init__(name, points, color)



""" The Phases """

class Goal(ABC):
    def __init__(self, min_cards: int):
        self.min_cards = min_cards
        self.cards = []
        self.complete = False
        self.name = ""

    @abstractmethod
    def checkCards(self, cards: List['Card']) -> bool:
        pass

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

class Phase:
    def __init__(self, name: str, goals: List[Goal]):
        self.name = name
        self.goals = goals
        self.complete = False

    def checkComplete(self) -> bool:
        self.complete = all(goal.complete for goal in self.goals)
        return self.complete

    def addCardsToGoal(self, goal_index: int, cards: List['Card']) -> bool:
        if 0 <= goal_index < len(self.goals):
            return self.goals[goal_index].addCards(cards)
        return False

    def grabAllCards(self) -> Stack:
        if checkComplete:
            cards_list = []
            for g in self.goals:
                cards_list.append(g.cards)
            return Stack(cards_list)

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


""" Card Management """

class Stack:
    def __init__(self, cards=None):
        if cards is None:
            cards = []
        self.cards = cards

    def __iter__(self):
        return iter(self.cards)

    @property
    def cards(self):
        return self._cards

    @cards.setter
    def cards(self, newcards):
        if isinstance(newcards, list):
            self._cards = newcards
        if isinstance(newcards, Card):
            self._cards.append(newcards)

    def addToStack(self, other) -> bool:
        if isinstance(other, Card):
            self._cards.append(other)
        if isinstance(other, Stack):
            self._cards.extend(other.cards)
            return True
        return False

    def shuffle(self):
        random.shuffle(self.cards)

    def sortByNumber(self):
        self.cards.sort(key=lambda x: x.number)

    def sortByColor(self):
        self.cards.sort(key=lambda x: x.color)

class Hand(Stack):
    def __init__(self):
        self.cards = []

class Deck(Stack):
    def __init__(self):
        super().__init__()
        self.createDeck()

    def createDeck(self) -> None:
        if len(self.cards) == 0:
            for c in colors:
                for lc in low_numbers:
                    self.cards.append(LowCard(name=lc, color=c))
                    print(f"{str(Card.getCount())} - {self.cards[-1].description()}")
                    self.cards.append(LowCard(name=lc, color=c))
                    print(f"{str(Card.getCount())} - {self.cards[-1].description()}")
                for hc in high_numbers:
                    self.cards.append(HighCard(name=hc, color=c))
                    print(f"{str(Card.getCount())} - {self.cards[-1].description()}")
                    self.cards.append(HighCard(name=hc, color=c))
                    print(f"{str(Card.getCount())} - {self.cards[-1].description()}")
            for i in range(8):
                newcard = WildCard()
                self.cards.append(newcard)
                print(f"{str(Card.getCount())} - {self.cards[-1].description()}")
            for i in range(4):
                newcard = SkipCard()
                self.cards.append(newcard)
                print(f"{str(Card.getCount())} - {self.cards[-1].description()}")
            print("Deck has been created")
            return

    def drawCard(self) -> Card:
        if len(self.cards) > 0:
            print("drawing card")
            return self.cards.pop(0)
        else:
            return False

    def deal(self, player):
        """ Deals 10 cards to @player """
        for _ in range(10):
            print(f"{player.name} was dealt a card")
            player.recieveCard(self.drawCard())



""" Player Classes """


class Player():
    def __init__(self, name: str, **kwargs):
        self.name = name
        self.wins, self.losses = 0
        self.hand = Hand()
        self.phases = self.createPhases()

    #   Phase Interactions
    def createPhases(self) -> list:
        p_list = []
        for k,v in phases_dict.items():
            v.owner = self.name
            p_list.append(v)
        print(f"10 Phases created for {self.name}")
        return p_list

    def getCurrentPhase(self) -> Phase:
        for phase in self.phases:
            if not phase.complete:
                return phase
        return None
        
    #   Scoring
    def addPoints(self) -> None:
        for c in self.hand.cards:
            self.points += c.points
        print(f"{self.name} has {self.points} points")

    #   Turn Actions
    def drawCard(self, card):
        self.hand.addToStack(card)

    def discardCard(self, card_index) -> Card:
        return self.hand.cards.pop(card_index)

    def addCardsToGoal(self, cards, goal_index):
        #Use the method in the Phase class
        pass

    #   Metadata
    def getPlayerData(self) -> dict:
        ret = {
            "name":self.name,
            "wins":self.wins,
            "losses":self.losses
            }
        return ret



##
##
class Game():
    def __init__(self):
        self.deck = Deck()
        self.discards = Stack()
        self.players = None
        self.player_cycle = itertools.cycle(self.players)
        self.turn_step = None
        self.active_player:Player = None
        self.turn_steps = ["Draw", "Play", "Discard"]


    def addPlayer(self, newplayer:Player):
        if newplayer not in self.players:
            self.players.append(newplayer)
            return True
        else:
            return False

    def getActivePlayer(self) -> Player:
        if self.active_player:
            return self.active_player

    def nextTurnStep(self) -> str:
        match self.turn_step:
            case None:
                self.turn_step = self.turn_steps[0]
            case "Draw":
                if len(self.deck.cards) <= 0:
                    self.reshuffleDeck()
                self.turn_step = self.turn_steps[1]
                print("Draw -> Play")
            case "Play":
                self.turn_step = self.turn_steps[2]
                print("Play -> Discard")
            case "Discard":
                self.turn_step = self.turn_steps[0]
                self.active_player = next(self.player_cycle)
                print(f"Discard -> Draw\nSwitching: {self.active_player.name}'s turn.")
        return self.turn_step

    def checkWin(self) -> bool:
        for p in self.players:
            if p.getCurrentPhase().name == "Phase 10" and p.checkComplete():
                print(f"{p.name} has won the game!!")
                return True

    def reshuffleDeck(self) -> None:
        for _ in self.deck.cards:
            c = self.discard.pop(0)
            self.deck.addToStack(c)


colors = ["Red", "Blue", "Green", "Yellow"]
low_numbers = ["One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine"]
high_numbers = ["Ten", "Eleven", "Twelve"]
number_value = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
    "Six": 6,
    "Seven": 7,
    "Eight": 8,
    "Nine": 9,
    "Ten": 10,
    "Eleven": 11,
    "Twelve": 12,
    "Skip": 99,
    "Wild": 99,
    "Mimic": 99
}
phases_dict = {
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
playersfile = "saved_players.json"
