import random
import copy
import os


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
        return self.number == other.number

    def __lt__(self, other):
        return self.number < other.number

    def __gt__(self, other):
        return self.number > other.number


class WildCard(Card):
    def __init__(self, name="Wild", points=25, color="None"):
        super().__init__(name, points, color)
        self.mimic = None

    def mimicCard(self, card: Card):
        self.mimic = card

    @property
    def mimic(self):
        return self._mimic

    @mimic.setter
    def mimic(self, newmimic):
        if newmimic == None or issubclass(newmimic, Card):
            self._mimic = newmimic
        else:
            print("Not a proper format for mimic attribute.")

    @mimic.deleter
    def mimic(self):
        del self._mimic

    def __eq__(self, other):
        if other.name == "Skip":
            return False
        else:
            self.mimic = other
            return True

    def __lt__(self, other):
        if other.name == "Skip":
            return False
        else:
            self.mimic = other
            return True

    def __gt__(self, other):
        if other.name == "Skip":
            return False
        else:
            self.mimic = other
            return True


class SkipCard(Card):
    def __init__(self, name="Skip", points=25, color="None"):
        super().__init__(name, points, color)

    # TO-DO
    def useSkip(self, player):
        # implement code to skip Player 'player'.
        pass

    def __eq__(self, other):
        return self.name == other.name

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
        self.cards = self.createDeck()

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

    def drawCard(self):
        if len(self.cards) > 0:
            print("drawing card")
            return self.cards.pop(0)
        else:
            return False

    def deal(self, players):
        self.shuffle()
        for i in range(10):
            for p in players:
                print(f"{str(i)} rounds dealt")
                p.hand.addToStack(self.drawCard())

    def addToStack(self, other):
        if isinstance(other, Card):
            self.cards.append(other)


class Hand(Stack):
    def __init__(self):
        self.cards = []

    def showHand(self, name):
        print()
        print(f"{name}'s Hand")
        print("#################")
        i = 1
        for c in self.cards:
            print(f"{str(i)} - {c.description()}")
            i += 1
        print("#################")

    def addToStack(self, other):
        if isinstance(other, Card):
            self.cards.append(other)


###
#   PHASES
class Phase:
    def __init__(self, name: str, goal: list, complete: bool):
        self.name = name
        self.goal = goal
        self.complete = complete

    def __str__(self):
        return self.name

    def __repr__(self):
        self.__str__()

    def checkComplete(self):
        for g in self.goal:
            if not g.complete:
                self.complete == False
                return False
        self.complete == True
        return True

    @property
    def complete(self):
        return self._complete

    @complete.setter
    def complete(self, newc):
        self._complete = newc


class PhaseGoal(Stack):
    def __init__(self, ptype: int, min_cards: int):
        # ptype: 1=Set, 2=Run, 3=Color
        self.ptype = ptype
        self.min_cards = min_cards
        self.target = None
        self.complete = False

    def __str__(self):
        return f"{P_TYPES[self.ptype]} of {self.min_cards} cards"

    def addToStack(self, other):
        if self.ptype not in [1, 2, 3]:
            return False
        if isinstance(other, Card):
            other = Stack(cards=[other])
        if isinstance(other, list):
            other = Stack(cards=other)
        if self.complete:
            if other.cards[0] not in self.target:
                return False
            else:
                super().addToStack(other)
        if self.ptype == 1:
            if not self.checkSet(other):
                return False
            else:
                self.target = [self.cards[0].number]
        if self.ptype == 2:
            if not self.checkRun(other):
                return False
            else:
                self.target = [(self.cards[0].number - 1), (self.cards[-1].number + 1)]
        if self.ptype == 3:
            if not self.checkColor(other):
                return False
            else:
                self.target = [self.cards[0].color]
        self.complete == True
        super().addToStack(other)

    def checkSet(self, stack: Stack):
        unique_numbers = set(card.number for card in stack.cards)
        return (
            len(unique_numbers) == len(stack.cards)
            and len(stack.cards) >= self.min_cards
        )

    def checkRun(self, stack: Stack):
        stack.sortByNumber()
        # Check if the difference between consecutive cards is 1 (excluding Wild cards)
        for i in range(1, len(stack.cards)):
            if stack.cards[i].number - stack.cards[
                i - 1
            ].number != 1 and not isinstance(stack.cards[i - 1], WildCard):
                return False
        return len(stack.cards) >= self.min_cards

    def checkColor(self, stack: Stack):
        if len(stack.cards) == 0:
            return False
        color = stack.cards[0].color
        for card in stack.cards:
            if card.color != color and not isinstance(card, WildCard):
                return False
        return len(stack.cards) >= self.min_cards

    @property
    def complete(self):
        return self._complete

    @complete.setter
    def complete(self, newc):
        self._complete = newc


###
#   PLAYERS
class Player:
    def __init__(self, name: str = "Default"):
        self.hand = Hand()
        self.name = name
        self.phases = []
        self.setupPhases()
        self.points = 0

    def setupPhases(self):
        for args in phases_dict.values():
            p = Phase(**args)
            print(p)
            self.phases.append(p)

    def showHand(self):
        self.hand.showHand(self.name)

    def drawCard(self, card):
        self.hand.addToStack(card)

    def discardCard(self):
        self.showHand()
        while True:
            try:
                sel = int(input("Select card to discard: "))
                if sel <= len(self.hand.cards):
                    ret = self.hand.cards.pop(sel - 1)
                    return ret
                else:
                    print(
                        "Selection out of range. Please choose a number between 1 and",
                        i,
                    )
            except ValueError:
                print("Invalid input. Please enter a number.")

    def checkCurrentPhase(self):
        for p in self.phases:
            if p.checkComplete():
                p.complete = True
                continue
            else:
                return p

    def addPoints(self):
        for c in self.hand.cards:
            self.points += c.points

    def layCards(self, cards, goal: PhaseGoal):
        if goal.addToStack(cards):
            print("Phase goal completed")
            return True
        else:
            print("Cards wont work for this Phase Goal")
            return False

    def chooseGoalCLI(self):
        print("Choose the goal you want to fill:")
        i = 0
        cur_phase = self.checkCurrentPhase()
        for g in cur_phase.goal:
            print(f"{i + 1}) {g}")
            i += 1
        while True:
            sel = input("Enter a number: ")
            try:
                sel = int(sel)
                return cur_phase.goal[sel - 1]
            except:
                print("No beans, buddy.")


###
#   GAME LOGIC
class Game:
    def __init__(self, players: list):
        self.deck = Deck()
        self.discards = Stack()
        self.players = players

    def start(self):
        os.system("clear")
        self.deck.deal(self.players)
        while True:
            for p in self.players:
                self.turn(p)

    def turn(self, player):
        os.system("clear")
        print(f"{player.name}'s Turn")
        # Draw card
        drw = self.deck.drawCard()
        player.drawCard(drw)
        # Action
        print(player.checkCurrentPhase())
        player.showHand()
        self.actionsCLI(player)
        # Discard card
        dis = player.discardCard()
        self.discards.addToStack(dis)

    def actionsCLI(self, player):
        while True:
            print("What would you like to do?")
            print("'n' - Sort hand by number")
            print("'c' - Sort hand by color")
            print("'p' - Lay down cards.")
            print("Press enter to do nothing.")
            sel = input(" ")
            if self.action(player, sel):
                continue
            else:
                break

    def action(self, player, sel):
        match sel.lower():
            case "c":
                player.hand.sortByColor()
                player.showHand()
                return True
            case "n":
                player.hand.sortByNumber()
                player.showHand()
                return True
            case "p":
                print("not ready yet")
                return True
            case _:
                return False


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
}
# Global Phase Variables
phases_dict = {
    1: {
        "name": "Phase 1",
        "goal": [PhaseGoal(1, 3), PhaseGoal(1, 3)],
        "complete": False,
    },
    2: {
        "name": "Phase 2",
        "goal": [PhaseGoal(1, 3), PhaseGoal(2, 4)],
        "complete": False,
    },
    3: {
        "name": "Phase 3",
        "goal": [PhaseGoal(1, 4), PhaseGoal(2, 4)],
        "complete": False,
    },
    4: {"name": "Phase 4", "goal": [PhaseGoal(2, 7)], "complete": False},
    5: {"name": "Phase 5", "goal": [PhaseGoal(2, 8)], "complete": False},
    6: {"name": "Phase 6", "goal": [PhaseGoal(2, 9)], "complete": False},
    7: {
        "name": "Phase 7",
        "goal": [PhaseGoal(1, 4), PhaseGoal(1, 4)],
        "complete": False,
    },
    8: {"name": "Phase 8", "goal": [PhaseGoal(3, 7)], "complete": False},
    9: {
        "name": "Phase 9",
        "goal": [PhaseGoal(1, 5), PhaseGoal(1, 2)],
        "complete": False,
    },
    10: {
        "name": "Phase 10",
        "goal": [PhaseGoal(1, 5), PhaseGoal(1, 3)],
        "complete": False,
    },
}
P_TYPES = ["", "Set", "Run", "Color"]


###
#
def testShuffle():
    p1 = Player(name="Corey")
    p2 = Player(name="Sam")
    pls = [p1, p2]
    g = Game(pls)
    g.start()


if __name__ == "__main__":
    testShuffle()
