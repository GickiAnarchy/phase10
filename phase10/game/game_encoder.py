import json
from phase10.game.classes.goal import Goal
from phase10.game.classes.phase import Phase
from phase10.game.classes.player import Player
from phase10.game.classes.card import Card
from phase10.game.games.base import BaseGame, RPS

class GameEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Goal):
            return {'__goal__': True, **obj.to_dict()}
        elif isinstance(obj, Phase):
            return {'__phase__': True, **obj.to_dict()}
        elif isinstance(obj, Player):
            return {'__player__': True, **obj.to_dict()}
        elif isinstance(obj, Card):
            return {'__card__': True, **obj.to_dict()}
        elif isinstance(obj, BaseGame):
            return {'__rps__': True, **obj.to_dict()}
        return super().default(obj)


def game_decoder(obj):
    if '__goal__' in obj:
        return Goal.from_dict(obj)
    elif '__phase__' in obj:
        return Phase.from_dict(obj)
    elif '__player__' in obj:
        return Player.from_dict(obj)
    elif '__card__' in obj:
        return Card.from_dict(obj)
    elif '__rps__' in obj:
        return RPS.from_dict(obj)
    return obj
