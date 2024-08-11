import random
import copy
import os
import json
import itertools
from abc import ABC, abstractmethod
from typing import List, Union

###
#   CARDS
class Card:
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
        image_directory = "images/"
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

###
#   CARD STACKS
class Stack:
    def __init__(self, cards=[]):
        self.cards = cards

    @property
    def cards(self):
        return self._cards

    @cards.setter
    def cards(self, newcards):
        if isinstance(newcards, list):
            self._cards = newcards
        if isinstance(newcards, Card):
            self._cards.append(newcards)

    def addToStack(self, other):
        if isinstance(other, Card):
            self._cards.append(other)
        if isinstance(other, Stack):
            for c in other.cards:
                self._cards.append(c)

    def shuffle(self):
        random.shuffle(self.cards)

    def sortByNumber(self):
        self.cards.sort(key=lambda x: x.number)

    def sortByColor(self):
        self.cards.sort(key=lambda x: x.color)

class Deck(Stack):
    def __init__(self):
        super().__init__()
        self.createDeck()

    def createDeck(self):
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

    def drawCard(self):
        if len(self.cards) > 0:
            print("drawing card")
            return self.cards.pop(0)
        else:
            return False

    def deal(self, player):
        for _ in range(10):
            print(f"{player.name} was dealt a card")
            player.recieveCard(self.drawCard())

        def addToStack(self, other):
            if isinstance(other, Card):
                print("Card added to deck")
                self.cards.append(other)

class Hand(Stack):
    def __init__(self):
        self.cards = []

    def showHand(self, name):
        ret = ""
        ret += f"{name}'s Hand"
        ret += "#################"
        i = 1
        for c in self.cards:
            ret += f"{str(i)} - {c.description()}"
            i += 1
        ret += "#################"
        return ret

    def addToStack(self, other):
        if isinstance(other, Card):
            self.cards.append(other)

    def __iter__(self):
        return iter(self.cards)

###
#   PHASE
class Phase:
    def __init__(self, name: str, goals: List[Goal]):
        self.name = name
        self.goals = goals
        self.complete = False

    def check_complete(self) -> bool:
        self.complete = all(goal.complete for goal in self.goals)
        return self.complete

    def add_cards_to_goal(self, goal_index: int, cards: List['Card']) -> bool:
        if 0 <= goal_index < len(self.goals):
            return self.goals[goal_index].add_cards(cards)
        return False

class Goal(ABC):
    def __init__(self, min_cards: int):
        self.min_cards = min_cards
        self.cards = []
        self.complete = False
        self.name =  ""

    @abstractmethod
    def check_cards(self, cards: List['Card']) -> bool:
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
        
    
    
    def add_cards(self, cards: List['Card']) -> bool:
        if self.check_cards(cards):
            self.cards.extend(cards)
            self.complete = len(self.cards) >= self.min_cards
            return True
        return False

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
        return all(sorted_cards[i].number - sorted_cards[i-1].number == 1 
                   for i in range(1, len(sorted_cards)))

class ColorGoal(Goal):
    def check_cards(self, cards: List['Card']) -> bool:
        if not cards:
            return False
        return all(card.color == cards[0].color for card in cards)

###
class Player:
    def __init__(self, name: str, score:int = 0):
        self.hand = Hand()
        self.name = name
        self.phases = self.setupPhases()
        self.points = 0
        self.score = score
        self.isReady = False #Indicates player is ready to play;
        self.gotSkipped = False

    def getInfo(self):
        return {
            "name":self.name,
            "score":self.score
            }

    def setupPhases(self):
        phase_list = []
        for k,v in phases_dict.items():
            phase_list.append(v)
            print(f"{v.name} added to {self.name}'s phase list")
        return phase_list

    def recieveCard(self, card):
        print(f"{self.name} drew a {card.name}")
        self.hand.addToStack(card)

    def discardCard(self, c_index) -> bool:
        print(f"{self.name} is discarding {c_index.name}")
        self.hand.cards.remove(c_index)
        return True

    def showHand(self):
        return self.hand.showHand(self.name)

    def addPoints(self):
        for c in self.hand.cards:
            self.points += c.points
        print(f"{self.name} has {self.points} points")

    def lay_cards(self, cards: List['Card'], goal_index: int) -> bool:
        current_phase = self.get_current_phase()
        if current_phase.add_cards_to_goal(goal_index, cards):
            for card in cards:
                self.hand.cards.remove(card)
            if current_phase.check_complete():
                print(f"{self.name} completed {current_phase.name}!")
            return True
        return False

    def get_current_phase(self) -> Phase:
        for phase in self.phases:
            if not phase.complete:
                return phase
        return None  # All phases complete

    def toggle_ready(self):
        self.isReady = not self.isReady
        print(f"{self.name} ready: {self.isReady}")

    def toggle_skip(self):
        self.gotSkipped = not self.gotSkipped

###
#   GAME LOGIC
class GameApp:
    saved_players = []
    def __init__(self):
        self.deck = Deck()      #Phase 10 deck
        self.discards = Stack() #Discard Pile
        self.players = []       #Player list
        self.currentPlayer = None
        self.turn_phase_cycle = itertools.cycle(["Draw","Play","Discard"])

    def begin(self) -> None:
        if len(self.players) < 2:
            print("Need more players")
            self.player_cycle = itertools.cycle(self.players)
            self.cycleTurnPhase()
            self.nextPlayer()
            return

    def cycleTurnPhase(self) -> None:
        self.turn_phase = next(self.turn_phase_cycle)
        print(f"TURN PHASE: {self.turn_phase}")
        return

    def nextPlayer(self) -> None:
        self.currentPlayer = next(self.player_cycle)
        if self.currentPlayer.gotSkipped:
            print(f"{self.currentPlayer.name} was skipped")
            self.currentPlayer.toggle_skip()
            self.currentPlayer = next(self.player_cycle)
        print(f"It is {self.currentPlayer.name}'s turn")
        return

    def create_player(self, name) -> Player:
        newp = Player(name)
        self.players.append(newp)
        return newp

    def draw(self) -> None:
        c = self.deck.drawCard()
        self.currentPlayer.recieveCard(c)
        self.cycleTurnPhase()
        return

    def discard(self, card) -> None:
        if isinstance(card, Stack) and len(card.cards) == 1:
            card = card.cards[0]
        if isinstance(card,Card):
            self.currentPlayer.discardCard(card)
            self.cycleTurnPhase()
            return
        else:
            print("GameApp.discard() needs a Card passed into it")
            return

    def play(self, cards, goal: Goal = None) -> None:
        if goal == None and isinstance(cards, Card):
            pass
        if isinstance(cards, list):
            cards = Stack(cards)

    def getOpponent(self) -> Player:
        for p in self.players:
            if p.name != self.currentPlayer.name:
                return p

    #TODO ALL

##GLOBAL VARIABLES
# Global Card Variables
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
#   PLAYER SAVES
playersfile = "saved_players.json"


def save_players():
    player_dict = {}
    if GameApp().saved_players == []:
        print("There are no players to save")
        return
    for p in GameApp.saved_players:
        player_dict[p.name] = p.getInfo()
    with open(playersfile, "w") as f:
        json.dump(player_dict, f)
        f.close()
    print("Players saved")

def load_players():
    try:
        with open(playersfile, "r+") as f:
            data = json.load(f)
            print("Players Loaded")
            for k,v in data.items():
                GameApp.saved_players.append(Player(v["name"],v["score"]))
    except FileNotFoundError:
        print("No saved players found.")

###
#


if __name__ == "__main__":
    pass
