#!/usr/bin/env python

from game import Game
from phase10 import Player


class Room:
    def __init__(self):
        self.game = None
        self.players = []

    def add_player(self, player: Player):
        self.players.append(player.player_id)
        self.game.add_player(player)

    def remove_player(self, player: Player):
        self.players.remove(player.player_id)
        self.game.
