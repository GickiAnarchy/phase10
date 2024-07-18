#THIS FILE WILL BE DELETED!

goals = [
    [PhaseSet(3),PhaseSet(3)],
    [PhaseSet(3), PhaseRun(4)],
    [PhaseSet(4), PhaseRun(4)],
    [PhaseRun(7)],
    [PhaseRun(8)],
    [PhaseRun(9)],
    [PhaseSet(4),PhaseSet(4)],
    [PhaseColor(7)],
    [PhaseSet(5), PhaseSet(2)],
    [PhaseSet(5), PhaseSet(3)]
    ]
phases_dict = {
    0:{"name":"Phase 1",
        "goal":[]
    },
    1:{"name":"Phase 2",
        "goal":[]
    },
    2:{"name":"Phase 3",
        "goal":[]
    },
    3:{"name":"Phase 4",
        "goal":[]
    },
    4:{"name":"Phase 5",
        "goal":[]
    },
    5:{"name":"Phase 6",
        "goal":[]
    },
    6:{"name":"Phase 7",
        "goal":[]
    },
    7:{"name":"Phase 8",
        "goal":[]
    },
    8:{"name":"Phase 9",
        "goal":[]
    },
    9:{"name":"Phase 10",
        "goal":[]
    },
    10:{"name":"NA",
        "goal":[]
    }
}


class Phase(Stack):
    def __init__(self, number:int,goals:list):
        self.number = number
        self.goals = goals




"""
class PhaseStack:
    def __init__(self, min_cards:int):
        self.min_cards = min_cards
        self.cards = Stack()
        self.isComplete = False

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



"""