

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
from client import update_lobby
import client


class Screens(ScreenManager):
    pass

class Lobby(Screen):
    conn_lbl = ObjectProperty()
    id_lbl = ObjectProperty()
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def ask_update(self):
        client.update_lobby()

    @staticmethod
    def update_connection(self, update):
        self.id_lbl.text = update["id"]
        self.conn_lbl.text = update["players"]


class P10TestApp(App):
    def build(self):
        self.screens = Screens()
        self.add_widget(self.screens)
        return self.screens

    
        
if __name__ == "__main__":
    P10TestApp().run()
