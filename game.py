

import random
import copy
import os
import json
from itertools import cycle


##
##
class Game:
    def __init__(self):
        self.deck = Deck()
        #self.discards
        
        self.players = None
        self.active_player = None
        
        self.turn_step = None

    def drawStep(self, active: Player) -> bool:
        if self.turn_step != "Draw":
            return False
        active.drawCard(self.deck.drawCard())
        self.turn_step = "Play"
        return True

    def playStep(self, active: Player, sel_cards, goal = None):
        if goal == None and isinstance(sel_cards, Card):
            cindex = active.hand.getIndex(sel_cards)
            self.discards.addCards(active.discardCard(cindex))
        if goal != None:
            active.





PHASES_DICT = {
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
turn_steps = ["Draw","Play","Discard"]

##
playersfile = "saved_players.json"

def load_players()
