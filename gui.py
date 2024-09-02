
import random
import asyncio

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
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

from phases import Goal, Phase
from cards import Deck, Discards, Hand, Card
from player import Player, loadPlayer, savePlayer
from game import Game
from client import Client

'''
class SelectableCard(ToggleButton):
    """Card displays as a button"""
    def __init__(self, card, **kwargs):
        super().__init__(**kwargs)
        self.card = card
        self.background_normal = Image(source = card.getImage())
        self.background_color = (1, 1, 1, 1)
        self.size_hint = (None, None)
        self.size = (73, 150)
        with self.canvas.before:
            self.border_color = Color(0, 1, 0, 1)  # Green border
            self.border = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_border, size=self.update_border,
                  state=self.update_border)

    def update_border(self, *args):
        self.border.pos = self.pos
        self.border.size = self.size
        if self.state == 'down':
            self.border_color.a = 1  # Fully opaque
        else:
            self.border_color.a = 0  # Fully transparent

class SelectableHand(BoxLayout):
    """ A players hand as a collection
        of SelectableCards """
    def __init__(self, hand, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.spacing = 10
        self.hand = hand
        self.update_hand()

    def update_hand(self):
        self.clear_widgets()
        for card in self.hand.cards:
            self.add_widget(SelectableCard(card))

    def get_selected_cards(self) -> list:
        return [widget.card for widget in self.children if widget.state == 'down']

    def isPressed(self) -> bool:
        return len(self.get_selected_cards()) > 0

class SelectableDeck(ToggleButton):
    def __init__(self, deck: Deck, **kwargs):
        super().__init__(**kwargs)
        self.deck = deck
        self.background_normal = Image(source = "images/CardBack.png")
        self.background_color = (1, 1, 1, 1)  # White background
        self.size_hint = (None, None)
        self.size = (73, 150)
        with self.canvas.before:
            self.border_color = Color(0, 1, 0, 1)  # Green border
            self.border = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_border, size=self.update_border,
                  state=self.update_border)

    def update_border(self, *args):
        self.border.pos = self.pos
        self.border.size = self.size
        if self.state == 'down':
            self.border_color.a = 1  # Fully opaque
        else:
            self.border_color.a = 0  # Fully transparent

    def isPressed(self) -> bool:
        if self.state == "down":
            return True
        else:
            return False

class SelectableDiscards(ToggleButton):
    def __init__(self, discards: Discards, **kwargs):
        super().__init__(**kwargs)
        self.discards = discards
        self.background_normal = Image()
        self.background_color = (1, 1, 1, 1)  # White background
        self.size_hint = (None, None)
        self.size = (73, 150)
        with self.canvas.before:
            self.border_color = Color(0, 1, 0, 1)  # Green border
            self.border = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_border, size=self.update_border,
                  state=self.update_border)

    def update_border(self, *args):
        self.border.pos = self.pos
        self.border.size = self.size
        if self.state == 'down':
            self.border_color.a = 1  # Fully opaque
        else:
            self.border_color.a = 0  # Fully transparent

    def isPressed(self) -> bool:
        if self.state == "down":
            return True
        else:
            return False

class GoalButton(Button):
    def __init__(self, goal, **kwargs):
        super().__init__(**kwargs)
        self.disabled = True
        self.goal = goal

    @property
    def goal(self):
        return self._goal

    @goal.setter
    def goal(self, newgoal):
        self._goal = newgoal
    
    def on_press(self) -> Goal:
        if not self.disabled:
            return self.goal
            
'''

##
class PlayerCreationPopup(Screen):
    """Popup to have the user name itself"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (0.5,0.5)
        self.game = Game().getGameInstance()
        self.root = BoxLayout(orientation = "vertical")
        self.name_label = Label(text='Player Name:')
        self.name_input = TextInput(multiline=False)
        self.pin_input = TextInput(multiline = False)
        self.create_button = Button(text='Create Player')
        self.create_button.bind(on_press=self.create_player)
        self.load_button = Button(text = "Load Player")
        self.load_button.bind(on_press = self.load_player)
        self.root.add_widget(self.name_label)
        self.root.add_widget(self.name_input)
        self.root.add_widget(Label(text = "PIN:"))
        self.root.add_widget(self.pin_input)
        self.buttons = BoxLayout(orientation = "horizontal")
        self.buttons.add_widget(self.create_button)
        self.buttons.add_widget(self.load_button)
        self.root.add_widget(self.buttons)
        self.add_widget(self.root)

    def create_player(self, instance) -> Player:
        player_name = self.name_input.text
        pin = self.pin_input.text
        if player_name:
            self.p = Player(player_name)
            if savePlayer(self.p, pin):
                self.game.add_player(self.p)
            #self.dismiss()
            self.manager.current = 'Main'
            return self.p
        else:
            print("Please enter a player name.")

    def load_player(self, instance) -> Player:
        player_name = self.name_input.text
        pin = self.pin_input.text
        if player_name:
            self.p = loadPlayer(player_name, pin)
            self.game.add_player(self.p)
            #self.dismiss()
            self.manager.current = 'Main'
            return self.p
        else:
            print("Please enter a player name.")



class HomeScreen(Screen):

    def make_player(self):
        self.manager.current = 'Create'



class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_current(self, instance, value):
        print("Main on_current")
        try:
            pl = self.get_screen('Create').p
            self.manager.me = self.get_screen('Create').p
            print(f"Self.ME = {pl.name}")
        except:
            print("Some error somewhere")


class Phase10Manager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.me = None
        self.add_widget(HomeScreen(name = "Home"))
        self.add_widget(MainScreen(name = "Main"))
        self.add_widget(PlayerCreationPopup(name = "Create"))




class Phase10App(App):
    def build(self):
        self.man = Phase10Manager()
        return self.man





if __name__ == "__main__":
    game = Game()
    Phase10App().run()

