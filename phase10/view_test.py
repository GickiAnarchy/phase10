

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.image import Image, AsyncImage
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen

from game.phases import Goal, Phase
from game.cards import Deck, Discards, Hand, Card
from game.player import Player, loadPlayer, savePlayer
from game.game import Game
from client import 

class TestWidget(BoxLayout):
    def __init__(self):
        self.player_name = ObjectProperty(None)

    def update_player(self, player):
        self.player_name = player.name


class P10TestApp(App):
    def build(self, game):
        game = Game().getGameInstance()
        self.twidget = TestWidget()
        
        