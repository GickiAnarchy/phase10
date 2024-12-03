#!/usr/bin/env python

import json

from phase10.game.classes.card import Card
from phase10.game.classes.phase import Phase


class PlayerBase:
    def __init__(self, name = "", pin = None):
        self.name = name
        self.pin = pin

    def to_dict(self):
        return {
            "name": self.name,
            "pin": self.pin
        }

    @classmethod
    def from_dict(cls, data):
        obj = cls(
            name=data.get("name"),
            pin=data.get("pin")
        )
        return obj

class Player(PlayerBase):
    def __init__(self, name = "", hand=None, score=0, win=False, is_skipped=False, player_id=None, pin = None, is_active=False, current_turn_step=None, current_phase=None, **kwargs):
        super().__init__(**kwargs)
        if hand is None:
            hand = []
        self.hand = hand
        self.score = score
        if isinstance(current_phase,dict):
            self.current_phase = Phase(**current_phase)
        else:
            self.current_phase = current_phase
        self.win = win
        self.is_skipped = is_skipped
        self.is_active = is_active
        self.current_turn_step = current_turn_step
        self.player_id = player_id
        if self.current_phase is None:
            self.current_phase = Phase().make_phase(1)

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
        return {
            "name": self.name,
            "hand": [c.to_dict() for c in self.hand],
            "score": self.score,
            "current_phase": self.current_phase.to_dict(),
            "win": self.win,
            "is_skipped": self.is_skipped,
            "is_active": self.is_active,
            "current_turn_step": self.current_turn_step,
            "player_id": self.player_id,
            "pin": self.pin
        }

    @classmethod
    def from_dict(cls, data):
        obj = cls(
            name=data.get("name"),
            hand=[Card.from_dict(c) for c in data.get("hand", [])],
            score=data.get("score"),
            current_phase=Phase.from_dict(data.get("current_phase", {})),
            win=data.get("win"),
            is_skipped=data.get("is_skipped"),
            is_active=data.get("is_active"),
            current_turn_step=data.get("current_turn_step"),
            player_id=data.get("player_id"),
            pin=data.get("pin")
        )
        return obj