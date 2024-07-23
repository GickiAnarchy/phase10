import random
import copy
import sys


###
#   CARDS
class Card():
    count = 0
    def __init__(self, name:str, points:int, color:str):
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

    def __eq__(self,other):
        return self.number == other.number
    def __lt__(self,other):
        return self.number < other.number
    def __gt__(self,other):
        return self.number > other.number

class WildCard(Card):
    def __init__(self, name = "Wild", points = 25, color = "None"):
        super().__init__(name,points,color)
        self.mimic = None
    
    def mimicCard(self, card:Card):
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

    def __eq__(self,other):
        if other.name == "Skip":
            return False
        else:
            self.mimic = other
            return True
        
    def __lt__(self,other):
        if other.name == "Skip":
            return False
        else:
            self.mimic = other
            return True

    def __gt__(self,other):
        if other.name == "Skip":
            return False
        else:
            self.mimic = other
            return True

class SkipCard(Card):
    def __init__(self, name = "Skip", points = 25, color = "None"):
        super().__init__(name,points,color)
    
    #TO-DO
    def useSkip(self, player):
        #implement code to skip Player 'player'.
        pass

    def __eq__(self,other):
        return self.name == other.name
    def __lt__(self,other):
        return False
    def __gt__(self,other):
        return False

class BasicCard(Card):
    def __init__(self, name:str, points:int, color:str):
        super().__init__(name,points,color)

class LowCard(BasicCard):
    def __init__(self, name:str, color:str, points = 5):
        super().__init__(name,points,color)

class HighCard(BasicCard):
    def __init__(self, name:str, color:str, points = 10):
        super().__init__(name,points,color)

###
#   CARD STACKS
class Stack:
    def __init__(self, cards = []):
        self.cards = cards
    
    @property
    def cards(self):
        return self._cards
    @cards.setter
    def cards(self, newcards):
        if isinstance(newcards,list):
            self._cards = newcards
        
    def addToStack(self, other):
        if isinstance(other, Stack):
            while len(other.cards) > 0:
                self.cards.append(other.cards.pop(0))
        if isinstance(other,Card):
            self.cards.append(other)

    def shuffle(self):
        random.shuffle(self.cards)

    def sortByNumber(self):
        self.cards.sort(key = lambda x : x.number)

    def sortByColor(self):
        self.cards.sort(key = lambda x : x.color)

class Deck(Stack):
    def __init__(self):
        super().__init__()
        self.cards = self.createDeck()

    def createDeck(self):
        if len(self.cards) == 0:
            for c in colors:
                for lc in low_numbers:
                    self.cards.append(LowCard(name = lc, color = c))
                    print(f"{str(Card.getCount())} - {self.cards[-1].description()}")
                    self.cards.append(LowCard(name = lc, color = c))
                    print(f"{str(Card.getCount())} - {self.cards[-1].description()}")
                for hc in high_numbers:
                    self.cards.append(HighCard(name = hc, color = c))
                    print(f"{str(Card.getCount())} - {self.cards[-1].description()}")
                    self.cards.append(HighCard(name = hc, color = c))
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
        amt = len(players)*10
        self.shuffle()
        while amt > 0:
            for p in players:
                p.hand.addToStack(self.drawCard())
                amt = amt - 1

class Hand(Stack):
    def __init__(self):
        super().__init__()
    
    def showHand(self,name):
        print()
        print(f"{name}'s Hand")
        print("#################")
        for c in self.cards:
            print(c.description())
        print("#################")

###
#   PHASES
class Phase():
    def __init__(self, number:int,goal:list):
        self.number = number
        self.goal = phases_dict[number]["goal"]
        self.complete = False
    
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
    def complete(self, newCom:bool):
        self._complete = newCom

class PhaseGoal(Stack):
    def __init__(self, ptype:int, min_cards:int):
        #ptype: 1=Set, 2=Run, 3=Color
        self.ptype = ptype
        self.min_cards = min_cards
        self.target = None

    def addToStack(self,other):
        if self.ptype not in [1,2,3]:
            return False
        if isinstance(other, Card):
            other = Stack(cards = [other])
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
                self.target = [
                    (self.cards[0].number - 1),
                    (self.cards[-1].number + 1)
                    ]
        if self.ptype == 3:
            if not self.checkColor(other):
                return False
            else:
                self.target = [self.cards[0].color]
        self.complete == True
        super().addToStack(other)

    def checkSet(self, stack: Stack):
        unique_numbers = set(card.number for card in stack.cards)
        return len(unique_numbers) == len(stack.cards) and len(stack.cards) >= self.min_cards

    def checkRun(self, stack: Stack):
        stack.sortByNumber()
        # Check if the difference between consecutive cards is 1 (excluding Wild cards)
        for i in range(1, len(stack.cards)):
            if stack.cards[i].number - stack.cards[i - 1].number != 1 and not isinstance(stack.cards[i - 1], WildCard):
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

###
#   PLAYERS
class Player:
    def __init__(self, name:str = "Default"):
        self.hand = Hand()
        self.name = name
        self.phases = []

    def setupPhases(self):
        for k,v in phases_dict:
            self.phases.append(Phase(k,k[v]["goal"]))

    def showHand(self):
        self.hand.showHand(self.name)
    
    def drawCard(self,card):
        self.hand.addToStack(card)
    
    def discardCard(self):
        i = 0
        for c in self.hand.cards:
            print(f"{str(i + 1):3}{c.description():^25}")
            i += 1
        while True:
            try:
                sel = int(input("Select card to discard: "))
                if sel <= i:
                    ret = self.hand.cards.pop(sel-1)
                    return ret
                else:
                    print("Selection out of range. Please choose a number between 1 and", i)
            except ValueError:
                print("Invalid input. Please enter a number.")

    def checkCurrentPhase(self):
        for p in self.phases:
            if p.checkComplete:
                p["complete"] = True
                continue
            return 

###
#   GAME LOGIC
class Game:
    def __init__(self, players:list):
        self.deck = Deck()
        self.discards = Stack()
        self.players = players
    
    def start(self):
        self.deck.deal(self.players)
        while True:
            for p in self.players:
                self.turn(p)

    def turn(self, player):
        #Draw card
        player.drawCard(self.deck.drawCard())
        #Action
        #player.showHand()
        
        #Discard card
        self.discards.addToStack(player.discardCard())



##GLOBAL VARIABLES
#Global Card Variables
colors = ["Red","Blue","Green","Yellow"]
low_numbers = ["One","Two","Three","Four","Five","Six","Seven","Eight","Nine"]
high_numbers = ["Ten","Eleven","Twelve"]
number_value = {
    "One": 1,"Two": 2,"Three": 3,
    "Four": 4,"Five": 5,"Six": 6,
    "Seven": 7,"Eight": 8,"Nine": 9,
    "Ten": 10,"Eleven": 11,"Twelve": 12,
    "Skip": 99, "Wild": 99
}
#Global Phase Variables
phases_dict = {
    1:{"name":"Phase 1",
        "goal":[PhaseGoal(1,3),PhaseGoal(1,3)],
        "complete":False
    },
    2:{"name":"Phase 2",
        "goal":[PhaseGoal(1,3), PhaseGoal(2,4)],
        "complete":False
    },
    3:{"name":"Phase 3",
        "goal":[PhaseGoal(1,4), PhaseGoal(2,4)],
        "complete":False
    },
    4:{"name":"Phase 4",
        "goal":[PhaseGoal(2,7)],
        "complete":False
    },
    5:{"name":"Phase 5",
        "goal":[PhaseGoal(2,8)],
        "complete":False
    },
    6:{"name":"Phase 6",
        "goal":[PhaseGoal(2,9)],
        "complete":False
    },
    7:{"name":"Phase 7",
        "goal":[PhaseGoal(1,4),PhaseGoal(1,4)],
        "complete":False
    },
    8:{"name":"Phase 8",
        "goal":[PhaseGoal(3,7)],
        "complete":False
    },
    9:{"name":"Phase 9",
    "goal":[PhaseGoal(1,5), PhaseGoal(1,2)],
    "complete":False
    },
    10:{"name":"Phase 10", 
    "goal" :[PhaseGoal(1,5), PhaseGoal(1,3)],
    "complete":False
    }
}

###
#
def testShuffle():
    p1 = Player(name = "Corey")
    p2 = Player(name = "Sam")
    pls = [p1,p2]
    g = Game(pls)
    g.start()
    
if __name__ == "__main__":
    testShuffle()