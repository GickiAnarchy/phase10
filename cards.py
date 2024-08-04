import random
import copy
import os
import json
import itertools


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
            return f"{image_directory}Skip.png"
        if isinstance(self, SkipCard):
            return f"{image_directory}Wild.png"
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
        self.number = 61

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

#    def __eq__(self, other):
#        if self.number != other:
#            return False
#        else:
#            self.mimic = other
#            return True


class SkipCard(Card):
    def __init__(self, name="Skip", points=25, color="None"):
        self.number = 60
        super().__init__(name, points, color)

    # TO-DO
    def useSkip(self, player):
        # implement code to skip Player 'player'.
        pass

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

"""
    def deal(self, players):
        self.shuffle()
        for i in range(10):
            for p in players:
                print(f"{str(i)} rounds dealt")
                p.hand.addToStack(self.drawCard()
"""

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
    def __init__(self, name, goal, complete = False):
        self.name = name
        self.goal = goal
        self.complete = complete

    def checkComplete(self):
        for g in self.goal:
            if g.complete == False:
                self.complete = False
                return False
        self.complete = True
        return True

class Goal:
    def __init__(self, min_cards):
        self.min_cards = min_cards
        self.cards = Stack()
        self.complete = False
    
    def addToCards(self, cards):
        if self.checkCards(cards):
            self.cards.addToStack(cards)

    def checkCards(self, stack):
        pass

class PhaseSet(Goal):
    def __init__(self, min_cards):
        super().__init__(min_cards)

    def checkCards(self, stack):
        if self.complete:
            target = self.cards.cards[0].number
            for c in stack.cards:
                if c.number != target:
                    return False
            return True
        if not self.complete:
            unique_numbers = set(card.number for card in stack.cards)
            ret = (len(unique_numbers) == len(stack.cards) and len(stack.cards) >= self.min_cards)
            self.complete = ret
        return ret

class PhaseRun(Goal):
    def __init__(self, min_cards):
        super().__init__(min_cards)

    def checkCards(self, stack):
        stack.sortByNumber()
        #nums = [n for n ]
        if self.complete:
            pass
        for i in range(1, len(stack.cards)):
            if stack.cards[i].number - stack.cards[
                i - 1
            ].number != 1 and not isinstance(stack.cards[i - 1], WildCard):
                return False
                return len(stack.cards) >= self.min_cards

class PhaseColor(Goal):
    def __init__(self, min_cards):
        super().__init__(min_cards)

    def checkCards(self, stack):
        if len(stack.cards) == 0:
            return False
        color = stack.cards[0].color
        for card in stack.cards:
            if card.color != color and not isinstance(card, WildCard):
                return False
        return len(stack.cards) >= self.min_cards

"""
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
            len(unique_numbers) == len(stack.cards
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
"""

###
#   PLAYERS
class Player:
    def __init__(self, name: str, score:int = 0):
        self.hand = Hand()
        self.name = name
        self.phases = self.setupPhases()
        self.points = 0
        self.score = score
        self.isReady = False #Indicates player is ready to play;

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

        def getCurrentPhase(self):
            for p in self.phases:
                if p.checkComplete():
                    continue
                if not p.checkComplete():
                    print(f"current phase is {p.name}")
                    return p
            #Should only get here if all phases are complete.
            return Phase("WINNER", [])

    def recieveCard(self, card):
        print(f"{self.name} drew a {card.name}")
        self.hand.addToStack(card)

    def discardCard(self, c_index):
        #dis = self.hand.cards[c_index]
        print(f"{self.name} is discarding {c_index.name}")
        self.hand.cards.remove(c_index)
        return True

    def showHand(self):
        return self.hand.showHand(self.name)

    def addPoints(self):
        for c in self.hand.cards:
            self.points += c.points
        print(f"{self.name} has {self.points} points")

    def layCards(self, cards, goal: Goal):
        if goal.addToStack(cards):
            print("Phase goal completed")
            return True
        else:
            print("Cards wont work for this Phase Goal")
            return False

    def toggle_ready(self):
        self.isReady = not self.isReady
        print(f"{self.name} ready: {self.isReady}")

    ##CLI Methods
    def chooseGoalCLI(self):
        print("Choose the goal you want to fill:")
        i = 0
        cur_phase = self.getCurrentPhase()
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
    def printHand(self):
        print(self.showHand)
    def discardCardCLI(self):
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
                    )
            except ValueError:
                print("Invalid input. Please enter a number.")

###
#   GAME LOGIC
class GameApp:
    saved_players = []
    def __init__(self):
        self.deck = Deck()      #Phase 10 deck
        self.discards = Stack() #Discard Pile
        self.players = []       #Player list
        self.currentPlayer = None
        load_players()


    def getCurrentPlayer(self):
        if self.currentPlayer == None:
            return self.players[0]
        return self.currentPlayer

    def getNextPlayer(self, plyrs):
        while True:
            for cp in plyrs:
                yield cp

    """Player Creation"""
    def createPlayer(self, name):
        cls_list = self.__class__.saved_players
        i = 0
        for n in cls_list:
            if n.name == name:
                print("This player already exists")
                self.players.append(cls_list[i])
                return
            i += 1
        newplayer = Player(name)
        cls_list.append(newplayer)
        self.players.append(newplayer)

    def getPlayer(self, name):
        for player in self.players:
            if player.name == name:
                return player
        print("No player by that name")

    """Main Loop"""
    def startGame(self):
        self.deck.shuffle()
        for p in self.players:
            self.deck.deal(p)    #Deal cards to players
        save_players()

    """Turn Options"""
    def playCards(self, player, cards = None):
        if cards == None:
            return False
        goals = [g for g in player.getCurrentPhase().goal]
        for gl in goals:
            if player.layCards(cards, gl):
                return True #Cards must match one of the current phase goals.
        return False

    def discardCard(self, player, selected_card = None):
        if selected_card == None:
            selected_card = random.choice(player.hand.cards)
            selected_card = [selected_card]
        if isinstance(selected_card, list):
            selected_card = selected_card[0]
        #if player.discardCard(player.hand.cards.index(selected_card)):
        if player.discardCard(selected_card):
            self.discards.addToStack(selected_card)
        

"""
the GameCLI class is commented out because the game needs to be graphical, not text based 
class GameCLI:
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
        player.recieveCard(drw)
        # Action
        print(player.getCurrentPhase())
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

"""

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
    1:Phase("Phase 1", [PhaseSet(3), PhaseSet(3)]),
    2:Phase("Phase 2",[PhaseSet(3), PhaseRun(4)]),
    3:Phase("Phase 3", [PhaseSet(4), PhaseRun(4)]),
    4:Phase("Phase 4", [PhaseRun(7)]),
    5:Phase("Phase 5", [PhaseRun(8)]),
    6:Phase("Phase 6", [PhaseRun(9)]),
    7:Phase("Phase 7", [PhaseSet(4), PhaseSet(4)]),
    8:Phase("Phase 8", [PhaseColor(7)]),
    9:Phase("Phase 9", [PhaseSet(5), PhaseSet(2)]),
    10:Phase("Phase 10",[PhaseSet(5), PhaseSet(3)])
}
P_TYPES = ["", "Set", "Run", "Color"]

###
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
def game_test():
    g = GameApp()
    g.createPlayer("Corey")
    g.createPlayer("Sam")
    g.createPlayer("Corey")
    g.startGame()


if __name__ == "__main__":
    #game_test()
    pass
