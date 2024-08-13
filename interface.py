from cards import Player, Stack, Deck, Hand, Card, Game, Phase, Goal, RunGoal, SetGoal, ColorGoal, SkipCard

from gui import Phase10App, SelectableHand, SelectableCard, ButtonBox, PlayerCreationScreen


class GameInterface:
    def __init__(self, game: Game):
        self. game = Game()
        self.active_player: Player = None

    def game_ready(self):
        if self.game.players()
        self.active_player = self.game.getActivePlayer()

    def addPlayer(self, newplayer):
        self.game.addPlayer(newplayer)

