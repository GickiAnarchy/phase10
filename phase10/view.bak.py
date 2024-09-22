
import random
import asyncio

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
from client import Client


class SelectableCard(ToggleButton):
    """Card displays as a button"""
    def __init__(self, name, card_img, card_id, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.card_id = card_id
        self.card_img = card_img
        self.background_normal = Image(source = self.card_img)
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
        for card in self.hand:
            self.add_widget(SelectableCard(card["name"], card["image"], card["id"]))

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
        self.update_display(discards)

    def update_display(self, discards):
        self.discards = discards
        self.background_normal.source = self.discards.getImage()

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


class P10TopBorder(BoxLayout):
    def __init__(self, opp):
        self.opponent = opp
        self.opp_name_lbl = ObjectProperty(None)
        self.opp_cur_phase = ObjectProperty(None)
        self.goal_1 = ObjectProperty(None)
        self.goal_2 = ObjectProperty(None)

    def update_display(self, opp):
        self.opponent = opp
        self.opp_name_lbl.text = self.opponent.name
        self.opp_cur_phase = self.opponent.getCurrentPhase().name
        self.goal_1.text = ""
        
class P10BottomBorder(BoxLayout):
    def __init__(self):
        self.draw_button = ObjectProperty(None)
        self.discard_button = Button()

    def discard_card(self):

class P10Table(FloatLayout):
    def __init__(self, game):
        self.game = game
        self.deck_center = SelectableDeck(self.game.deck)
        self.discards_center = SelectableDiscards(self.game.discards)
        
        self.hand_bc = ObjectProperty(None)
        
        self.goal_tl = ObjectProperty(None)
        self.goal_tr = ObjectProperty(None)
        self.goal_bl = ObjectProperty(None)
        self.goal_br = ObjectProperty(None)
        

    def update_display(self):
        self.deck = 


class Phase10App(App):
    def build(self, client):
        self.p10_top = ObjectProperty(None)
        self.p10_bottom = ObjectProperty(None)
        self.p10_table = ObjectProperty(None)
        self.client = client
        self.game = Game().getGameInstance()
        self.player = self.game.getPlayer(self.client.name)
        self.opponent = self.game.getOpponent(self.client.name)
        self.hand = SelectableHand(self.player.hand)
        self.player_goals = None
        self.opponent_goals = None
        self.deck = None
        self.discards = None

    def update_display(self):
        pass
        




if __name__ == "__main__":
    pass