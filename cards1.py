import random
import sys

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


###
###
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

#
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

#
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

#
class BasicCard(Card):
    def __init__(self, name:str, points:int, color:str):
        super().__init__(name,points,color)

#
class LowCard(BasicCard):
    def __init__(self, name:str, color:str, points = 5):
        super().__init__(name,points,color)

#
class HighCard(BasicCard):
    def __init__(self, name:str, color:str, points = 10):
        super().__init__(name,points,color)


###
###
class Stack:
    def __init__(self):
        self.cards = []
    
    @property
    def cards(self):
        return self._cards
    @cards.setter
    def cards(self, newcards):
        if isinstance(newcards, list):
            self._cards = newcards
        else:
            self.cards.clear()
            self._cards.append(newcards)

    def acceptCard(self, card):
        self.cards.append(card)
        if Card.count > 108:
            print("Too many cards")
            #sys("exit")

    def combineStack(self, other):
        if isinstance(other, Stack):
            self.cards = self.cards + other.cards

    def sortByNumber(self):
        self.cards.sort(key = lambda x : x.number)

    def sortByColor(self):
        self.cards.sort(key = lambda x : x.color)

#
class Deck(Stack):
    def __init__(self):
        super().__init__()
        self.cards = createDeck()

    def createDeck(self):
        if len(self.deck) == 0:
            for c in colors:
                for lc in low_numbers:
                    self.deck.append(LowCard(name = lc, color = c))
                    print(f"{str(Card.getCount())} - {self.deck[-1].description()}")
                    self.deck.append(LowCard(name = lc, color = c))
                    print(f"{str(Card.getCount())} - {self.deck[-1].description()}")
                for hc in high_numbers:
                    self.deck.append(HighCard(name = hc, color = c))
                    print(f"{str(Card.getCount())} - {self.deck[-1].description()}")
                    self.deck.append(HighCard(name = hc, color = c))
                    print(f"{str(Card.getCount())} - {self.deck[-1].description()}")
            for i in range(8):
                newcard = WildCard()
                self.deck.append(newcard)
                print(f"{str(Card.getCount())} - {self.deck[-1].description()}")
            for i in range(4):
                newcard = SkipCard()
                self.deck.append(newcard)
                print(f"{str(Card.getCount())} - {self.deck[-1].description()}")
    
    def shuffle(self):
        random.shuffle(self.deck)
    
    def drawCard(self):
        if len(self.deck) > 0:
            return self.deck.pop(0)
        else:
            return False

    def dealToStack(self, stack, amount = 10):
        self.shuffle()
        for i in range(amount):
            stack.acceptCard(self.drawCard())
        
    def dealCards(self, players:list):
        self.shuffle()
        cards = []
        card_amount = len(players)*10
        for deal in range(card_amount):
            cards.append(self.drawCard())
        while len(cards) > 0:
            pass

    def addStack(self, stack):
        for c in stack:
            if c.name == "Wild":
                del c.mimic
        self.deck = self.deck + stack
        self.shuffle()

    @property
    def deck(self):
        return self._deck
    @deck.setter
    def deck(self, newitem):
        if isinstance(newitem, list):
            self._deck = newitem
        else:
            del self.deck
            self._deck.append(newitem)
    @deck.deleter
    def deck(self):
        self._deck.clear()

#
class Hand(Stack):
    def __init__(self):
        super().__init__()
    
    def showHand(self):
        #self.sortByNumber()
        print()
        print()
        print("Your Hand")
        print("#################")
        for c in self.cards:
            print(c.description())
        print("#################")
            
    def acceptCard(self, card):
        if len(self.cards) >= 10:
            print("Hand has too many cards")
            return False
        super().acceptCard(card)

    
###
###


###
###

#
#
#
#
def testShuffle():
    g = Game()
    players = g.players
    for p in players:
        p.hand.showHand()
    """d = Deck()
    d.createDeck()
    h = Hand()
    d.dealToStack(h)
    h.showHand()"""

if __name__ == "__main__":
    testShuffle()