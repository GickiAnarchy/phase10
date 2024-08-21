
import random
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

from phases import Goal, Phase
from cards import Deck, Discards, Hand, Card
from player import Player


##
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
            


##
class PlayerCreationPopup(Popup):
    """Popup to have the user name itself"""
    def __init__(self, game_app, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (0.5,0.5)
        self.game = game_app
        self.root = BoxLayout(orientation = "vertical")
        self.name_label = Label(text='Player Name:')
        self.name_input = TextInput(multiline=False)
        self.create_button = Button(text='Create Player')
        self.create_button.bind(on_press=self.create_player)
        self.root.add_widget(self.name_label)
        self.root.add_widget(self.name_input)
        self.root.add_widget(self.create_button)
        self.add_widget(self.root)

    def create_player(self, instance) -> Player:
        player_name = self.name_input.text
        if player_name:
            p = Player(player_name)
            self.game.addPlayer(p)
            self.dismiss()
            return p
        else:
            print("Please enter a player name.")

class ChooseAGoalPopup(Popup):
    """OBSOLETE"""
    def __init__(self, active_player, goals, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (0.5,0.8)
        self.root = BoxLayout(orientation = "vertical")
        self.lbl = Label(text = "Choose a goal to play on.")
        self.box_root = BoxLayout(orientation = "horizontal")
        self.player_goal_box = BoxLayout(orientation = "vertical")
        self.opponent_goal_box = BoxLayout(orientation = "vertical")
        for k,v in goals:
            if k == active_player:
                for g in v:
                    self.player_goal_box.add_widget(GoalButton(text = v.name, goal = v, on_press = self.getGoal()))
            if k != active_player:
                for g in v:
                    self.opponent_goal_box.add_widget(GoalButton(text = v.name, goal = v, on_press = self.getGoal))

    def getGoal(self, instance):
        return instance.goal

class ButtonBox(GridLayout):
    """OBSOLETE"""
    def __init__(self, **kwargs):
        super().__init__(pos_hint = {'center_y': 0.8}, **kwargs)
        self.size_hint = (1, 0.2)
        #self.pos_hint = {'center_y': 0.8}
        self.cols = 3
        self.padding = 5
        self.spacing = 5
        self.game = Phase10App().getGame()
        self.create_player_btn = Button(text="Create Player", disabled = True, on_press=self.createPlayer)
        self.create_player_btn.disabled = True
        self.draw_btn = Button(text = "Draw", on_press = self.drawPressed)

        self.game.ready()
        self.update_display()

    def update_display(self):
        self.clear_widgets()
        if Phase10App().me == None:
            self.create_player_btn.disabled = False
            self.add_widget(self.create_player_btn)
        if self.game.active_player == Phase10App().me:
            if self.game.turn_step == "Draw":
                self.draw_btn.disabled = False
                self.add_widget(self.draw_btn)
            if self.game.turn_step == "Play":
                pass
            if self.game.turn_step == "Discard":
                pass

    def drawPressed(self, instance):
        self.game.drawCard()

    def createPlayer(self, instance):
        pop = PlayerCreationPopup(self.game)
        Phase10App().me = pop.open()
        if Phase10App().me:
            return True

    def playPressed(self, instance):

##
class Phase10App(App):
    def build(self):
        self.root = BoxLayout(orientation = "vertical")
        self.lbl = Label(text = "PHASE 10", size_hint = (1,0.15))
        #self.deck
        self.root.add_widget(self.lbl)
        return self.root




