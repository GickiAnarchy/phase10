from .cards import Card, WildCard, SkipCard, BasicCard, LowCard, HighCard, Deck, Discards, Hand
from .phases import Phase, Goal, SetGoal, RunGoal, ColorGoal
from .player import Player
from .game import Game
from .gui import Phase10App
from .gui import PlayerDisplay, OpponentDisplay, SelectableCard, SelectableHand, ButtonBox
from .gui import PlayerCreationScreen, SelectPlayerPopup
from .gui import PhaseDisplay, GoalDisplay
from .gamestate import Gamestate
from .client import Client


__all__ = ["Card", "WildCard", "SkipCard", "BasicCard", "LowCard", "HighCard", "Deck", "Hand", "Player", "Phase", "Goal", "SetGoal", "RunGoal", "ColorGoal", "Game", "Phase10App"]


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
    10:Phase("Phase 10",[SetGoal(5), SetGoal(3)]),
    11:Phase("All complete!",[])
    }