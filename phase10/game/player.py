#!/usr/bin/env python

import json
import uuid
from json import JSONEncoder

from phase import Phase


class PlayerEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__

class Player:
    def __init__(self, name, hand=[],current_phase=None,score=0,win=False,is_skipped=False,player_id=None):
        self.name = name
        self.hand = []
        self.current_phase = Phase.make_phase(1)
        self.score = 0
        self.win = False
        self.is_skipped = False
        self.player_id = str(uuid.uuid4())


    # PLAYER
    def toggle_skipped(self):
        self.is_skipped = not self.is_skipped

    # PHASE HANDLING
    def phase_desc(self):
        return self.current_phase.name

    def check_phase_condition(self):
        if self.current_phase.check_complete():
            if self.current_phase.number == 10:
                self.win = True
            phs_num = self.current_phase.number
            self.current_phase = Phase.make_phase(phs_num + 1)

    def get_goals(self):
        return self.current_phase.goals

    # CARD HANDLING
    def add_card(self, card):
        self.hand.append(card)

    def total_hand_points(self):
        return sum([c.points for c in self.hand])

    def sort_by_number(self):
        self.hand.sort(key=lambda x: x.number)
        
    def sort_by_color(self):
        self.hand.sort(key=lambda x: x.color)

    def to_dict(self):
        data = json.dumps(self, indent = 4, cls = PlayerEncoder)
        return data

"""
    def __dict__(self):
        h = [dict(c) for c in self.hand]
        return {"name":self.name,"hand":h,"current_phase":self.current_phase,"score":self.score,"win":self.win,"is_skipped":self.is_skipped,"player_id":self.player_id}


    def __slots__(self):
        return {
            "name":self.name,
            "hand":self.hand,
            "current_phase":self.current_phase,
            "score":self.score,
            "win":self.win,
            "is_skipped":self.is_skipped,
            "player_id":self.player_id
            }

"""



##########################
def iterate_by_groups(cards, group_size):
    for i in range(len(cards) - group_size + 1):
        yield cards[i:i + group_size]
