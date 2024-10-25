#!/usr/bin/env python

import json
from json import JSONEncoder
import pickle
import io

from .phase import Phase


class Player:
    def __init__(self, name, hand=[], current_phase=None, score=0, win=False, is_skipped=False, player_id=None, pin = None):
        self.name = name
        self.hand = []
        self.current_phase = Phase.make_phase(1)
        self.score = 0
        self.win = False
        self.is_skipped = False
        self.is_active = False
        self.current_turn_step = None

        self.player_id = None
        self.pin = pin

    # PLAYER
    def toggle_skipped(self):
        self.is_skipped = not self.is_skipped

    def toggle_active(self):
        self.is_active = not self.is_active

    def get_turn_step(self):
        return self.current_turn_step

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

    def take_card_by_id(self, card_id):
        for i, card in enumerate(self.hand):
            if card.id == card_id:
                return self.hand.pop(i)

    def total_hand_points(self):
        return sum([c.points for c in self.hand])

    def sort_by_number(self):
        self.hand.sort(key=lambda x: x.number)

    def sort_by_color(self):
        self.hand.sort(key=lambda x: x.color)

    def to_dict(self):
        data = json.dumps(self, indent=4, cls=PlayerEncoder)
        return data


#   #   #   #   @   #   #   #   #   #
class PlayerEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__