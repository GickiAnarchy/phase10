

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


class GetPlayer(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.auto_dismiss = False
        #self.box = BoxLayout(orientation = 'vertical', size_hint = (0.5,0.5))
        self.name_lbl = Label(text = "Name ")
        self.name_in = TextInput(multiline = False)
        self.make_btn = Button(text = "Test Me!")
        #self.box.add_widget(self.name_lbl)
        #self.box.add_widget(self.name_in)
        #self.box.add_widget(self.make_btn)
        self.make_btn.bind(on_press = self.dismiss)
        self.bind(on_dismiss = self.make_player)

    def make_player(self):
        my_name = self.name_in.text
        #self.dismiss()
        return my_name




class P10TestApp(App):
    def build(self):
        game = Game().getGameInstance()
        popme = GetPlayer()
        self.me = ""
        while self.me == "":
            self.me = popme.open()
        game.add_player(Player(self.me))
        self.twidget = TestWidget(self.me)
        return self.twidget

        
if __name__ == "__main__":
    client.send_message({"type": 'join'})
    P10TestApp().run()
