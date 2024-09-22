
from card import Card
from hand import Hand
from phase import Phase
from deck import Deck
from discards import Discards



class Player:
    def __init__(self, name):
        self.name = name
        self.hand = Hand()
        self.current_phase = Phase.make_phase(1)
        self.points = 0
        self.win = False
        self.is_active = False

    # PHASE HANDLING
    def phase_desc(self):
        return self.current_phase.name

    def check_phase_condition(self):
        if self.current_phase.check_complete():
            if self.current_phase.number == 10:
                self.win = True
            phs_num = self.current_phase.number
            self.current_phase = Phase.make_phase(phs_num + 1)

    # HAND HANDLING
    def add_card(self,card):
        self.hand.add_to_hand(card)

    def check_possible_plays(self):
        possible_plays = 0
        min_cards = [goal.min_cards for goal in self.current_phase.get_goals()]
        for m in min_cards:
            for group in self.hand.iterate_by_groups(m,True):
                possible_plays += self.current_phase.check_for_plays(group)
        return possible_plays




    # TURN HANDLING



