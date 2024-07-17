

"""
- 2 sets of 3
- 1 set of 3 + 1 run of 4
- 1 set of 4 + 1 run of 4
- 1 run of 7
- 1 run of 8
- 1 run of 9
- 2 sets of 4
- 7 cards of one color
- 1 set of 5 + 1 set of 2
- 1 set of 5 + 1 set of 3

PhaseSet(3),PhaseSet(3)
PhaseSet(3), PhaseRun(4)
PhaseSet(4), PhaseRun(4)
PhaseRun(7)
PhaseRun(8)
PhaseRun(9)
PhaseSet(4),PhaseSet(4)
PhaseColor(7)
PhaseSet(5), PhaseSet(2)
PhaseSet(5), PhaseSet(3)
"""


phases_dict = {
    0:{"name":"NA",
        "goal":[]
    },
    1:{"name":"NA",
        "goal":[]
    },
    2:{"name":"NA",
        "goal":[]
    },
    3:{"name":"NA",
        "goal":[]
    },
    4:{"name":"NA",
        "goal":[]
    },
    5:{"name":"NA",
        "goal":[]
    },
    6:{"name":"NA",
        "goal":[]
    },
    7:{"name":"NA",
        "goal":[]
    },
    8:{"name":"NA",
        "goal":[]
    },
    9:{"name":"NA",
        "goal":[]
    },
    10:{"name":"NA",
        "goal":[]
    }
}

class PhaseStack:
    def __init__(self, min_cards:int):
        self.min_cards = min_cards
        self.cards = Stack()
        self.isComplete = False
    
    def addCards(self, cards):
        if isinstance(cards, Stack):
            self.cards.combineStack(cards)

    def checkCards(self, cards):
        pass

    def complete(self):
        self.isComplete = True
    
    @property
    def isComplete(self):
        return self._isComplete
    @isComplete.setter
    def isComplete(self,newone:bool):
        if self._isComplete == False:
            self._isComplete = newone
        elif self._isComplete == True:
            self._isComplete = True

class PhaseSet(PhaseStack):
    def __init__(self, min_cards:int):
        super().__init__(min_cards)
        self.target = None
    
    def checkCards(self, cards):
        pass

    def addCard(self, card):
        pass

class PhaseRun(PhaseStack):
    def __init__(self, min_cards:int):
        super().__init__(min_cards)

class PhaseColor(PhaseStack):
    def __init__(self, min_cards:int):
        super().__init__(min_cards)
        