
import random



class Card():
    count = 0
    def __init__(self, name: str, points: int, color: str):
        self.name = name
        self.points = points
        Card.count += 1
        self.color = color
        self.number = NUMBER_VALUE[self.name]

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

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, newpoints):
        self._points = newpoints

    def __eq__(self, other):
        if isinstance(other, int):
            return self.number == other
        if isinstance(other, Card):
            return self.number == other.number and self.color == other.color
        if other in COLORS:
            return self.color == other

    def __lt__(self, other):
        return self.number < other.number

    def __gt__(self, other):
        return self.number > other.number

class WildCard(Card):
    def __init__(self, name="Wild", points=25, color="Wild"):
        super().__init__(name, points, color)
        self.mimic = None

    def description(self):
        ret = super().description()
        return f"*WILD*{ret}"

    def set_mimic(self, card):
        if isinstance(card, Card) and self.mimic == None:
            self.mimic = card

    def clearMimic(self):
        self.mimic = None

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, newname):
        self._name = newname

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, newcolor):
        self._color = newcolor

    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, newnumber):
        self._number = newnumber

    def __eq__(self, other):
        if isinstance(other, Card):
            if other.name == "Skip":
                 return False
            else:
                return True
        if isinstance(other, int):
            if other == 99:
                return False
            else:
                return True

    def __lt__(self, other):
        if other.name == "Skip":
            return False
        else:
            return True

    def __gt__(self, other):
        if other.name == "Skip":
            return False
        else:
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


class Hand:
    def __init__(self):
        self.cards = []

    def __iter__(self):
        return iter(self.cards)

    def __getitem__(self, index):
        return self.cards[index]

    def addCards(self, cards: list):
        self.cards.extend(cards)

    def getIndex(self, card) -> int:
        for i, c in enumerate(self.cards):
            if c.name == card.name and c.number == card.number:
                return i
        raise ValueError(f"Card {card} not found in the hand.")

    def checkForRun(self, min_cards: int = 1) -> bool:
        self.sortNumber()
        count = 0
        wilds = 0
        for c in self.cards:
            if c.name == "Wild":
                wilds += 1
        for i, card in enumerate(self.cards[:-1]):
            if card.number == self.cards[i + 1].number - 1:
                count += 1
            elif card.number == self.cards[i + 1].number:
                count += 0
            else:
                if wilds > 0:
                    wilds -= 1
                    count += 1
                else:
                    count = 0
            if count >= min_cards - 1:  # Adjust for starting count
                print("run found")
                return True
        return False

    def checkForSet(self, min_cards: int = 1) -> bool:
        number_counts = {}
        wilds_used = 0
        for card in self.cards:
            if card.number == 13:
                wilds_used += 1
            else:
                number_counts[card.number] = number_counts.get(card.number, 0) + 1
        for number, count in number_counts.items():
            if count + wilds_used >= min_cards:
                print("set found")
                return True
        return False


    def checkForColor(self, min_cards: int = 1) -> bool:
        color_counts = {}
        wilds = 0
        for card in self.cards:
            if card.name == "Wild":
                wilds += 1
            else:
                color_counts[card.color] = color_counts.get(card.color, 0) + 1
        for color, count in color_counts.items():
            if count + wilds >= min_cards:
                print("color set found")
                return True
        return False

    def sortNumber(self):
        self.cards.sort(key=lambda x: x.number)

    def sortColor(self):
        self.cards.sort(key=lambda x: x.color)

class Deck():
    def __init__(self):
        self.cards = []
        self.createDeck()

    def __iter__(self):
        return iter(self.cards)

    def createDeck(self) -> None:
        if len(self.cards) == 0:
            for c in COLORS:
                for lc in LOW_NUMBERS:
                    self.cards.append(LowCard(name=lc, color=c))
                    print(f"{str(Card.getCount())} - {self.cards[-1].description()}")
                    self.cards.append(LowCard(name=lc, color=c))
                    print(f"{str(Card.getCount())} - {self.cards[-1].description()}")
                for hc in HIGH_NUMBERS:
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
            return self.cards.pop(-1)
        else:
            return False

    def deal(self) -> list:
        """ 
        Shuffles deck then deals 10 cards.
        
        Returns:
            list: of 10 Card objects
        """
        
        self.shuffle()
        return self.cards[:10]

    def shuffle(self, other_cards = None):
        if other_cards != None:
            self.cards.extend(other_cards)
        random.shuffle(self.cards)

class Discards():
    def __init__(self):
        self.cards = []

    def getTopCard(self) -> Card:
        c = self.cards.pop(-1)
        return c

    def addCard(self, card):
        self.cards.append(card)



if __name__ == "__main__":
    deck = Deck()
    hand = Hand()
    hand2 = Hand()
    hand.addCards(deck.deal())
    hand2.addCards(deck.deal())
    
    print("\nhand....")
    hand.checkForRun(4)
    hand.checkForSet(3)
    hand.checkForColor(3)
    print("\nhand2.....")
    hand2.checkForRun(4)
    hand2.checkForSet(3)
    hand2.checkForColor(3)
    print("\n\n")
    for c in hand:
        print(c.description())
    print("")
    for c in hand2:
        print(c.description())
    


COLORS = ["Red", "Blue", "Green", "Yellow"]
LOW_NUMBERS = ["One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine"]
HIGH_NUMBERS = ["Ten", "Eleven", "Twelve"]
NUMBER_VALUE = {
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
    "Wild": 13
}
