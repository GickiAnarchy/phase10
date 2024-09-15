

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
import client


class TestWidget(BoxLayout):
    def __init__(self, p):
        self.player = Game().getGameInstance().getPlayer(p.name)
        self.lbl = Label()
        self.add_widget(self.lbl)
        self.update_player(self.player)

    def update_player(self, player):
        self.lbl.text = player.name


class MakePlayer(Popup):
    name_lbl = ObjectProperty()
    name_in = ObjectProperty()
    make_btn = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', spacing=10, padding=10, auto_dismiss=False, **kwargs)




class P10TestApp(App):
    def build(self):
        self.twidget = TestWidget()
        MakePlayer().open()
        return self.twidget



    def make_player(self, name):
        m = {"type":"create player", "name": name}
        client.send_message(m)

        
if __name__ == "__main__":
    client.send_message({"type": 'join'})
    P10TestApp().run()
