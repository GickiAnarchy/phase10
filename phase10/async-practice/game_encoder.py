import json


class GameEncoder(json.JSONEncoder):
    def default(self, obj):
        '''if isinstance(obj, Goal):
            return {'__goal__': True, **obj.to_dict()}'''
        return super().default(obj)


def game_decoder(obj):
    '''if '__goal__' in obj:
        return Goal.from_dict(obj)'''
    return obj
