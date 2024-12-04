from kivy.properties import ListProperty, StringProperty
from kivy.uix.screenmanager import Screen, ScreenManager


class MiniGamesManager(ScreenManager):
    pass

class MiniGameWaiting(Screen):
    game_id = StringProperty()
    players = ListProperty()

    def __init__(self, max_players, **kwargs):
        super().__init__(**kwargs)
        self.max_players = max_players
    
    def join_waiting(self, player):
        if len(self.players) >= self.max_players:
            return False
    
    def on_players(self, ins, value):
        pass
        

class RPSScreen(Screen):
    players = ListProperty()
    p1_choice = StringProperty("")
    p2_choice = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)