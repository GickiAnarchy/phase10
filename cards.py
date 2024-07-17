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

#
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

#
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
###
class Player:
    def __init__(self, name:str = "Default"):
        self.hand = Hand()
        self.name = name

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
            sel = input("Select card to discard: ")
            try:
                sel = int(sel)
                if sel <= i:
                    ret = self.hand.cards.pop(sel-1)
                    return ret
            except:
                print("Not a proper input.")
                


###
###
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
        

#
#
#
#
def testShuffle():
    p1 = Player(name = "Corey")
    p2 = Player(name = "Sam")
    pls = [p1,p2]
    g = Game(pls)
    g.start()
    
if __name__ == "__main__":
    testShuffle()