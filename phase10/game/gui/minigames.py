from kivy.app import App
from kivy.base import EventLoop
from kivy.properties import ObjectProperty, ListProperty, StringProperty
from kivy.uix.floatlayout import floatlayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager

from phase10.game.games.minigames import RPS

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
        

class RPSScreen(Screen):
    players = ListProperty()
    p1_choice = StringProperty("")
    p2_choice = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)