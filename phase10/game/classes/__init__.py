#game.classes

from .classes.card import Card, Wild, Skip
from .classes.deck import Deck
from .classes.discards import Discards
from .classes.player import Player
from .classes.phase import Phase
from .classes.goal import Goal

__all__ = ["Card","Wild","Skip","Deck","Discards","Player","Phase","Goal"]
