
import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.image import AsyncImage
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty

from cards import Player, Stack, Deck, Hand, Card, Game, Phase, Goal, RunGoal, SetGoal, ColorGoal, SkipCard



class SelectableCard(ToggleButton):
    def __init__(self, card, **kwargs):
        super().__init__(**kwargs)
        self.card = card
        self.background_normal = card.getImage()
        self.background_color = (1, 1, 1, 1)  # White background
        self.size_hint = (None, None)
        self.size = (100, 150)  # Adjust size as needed
        # Add a colored border when selected
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

    def get_selected_cards(self):
        return Stack([widget.card for widget in self.children if widget.state == 'down'])

class PlayerCreationScreen(Popup):
    def __init__(self, game_app, **kwargs):
        super().__init__(**kwargs)
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
            return p
        else:
            print("Please enter a player name.")


class Phase10App(App):
    def build(self):
        self.root = BoxLayout(orientation = "vertical")
        self.me = None
        self.game = Game()
        self.lbl = Label(text = "PHASE 10")
        self.create_player_btn = Button(text="Create Player", on_press = self.createPlayer)
        self.root.add_widget(self.lbl)
        self.root.add_widget(self.create_player_btn)
        return self.root

    def createPlayer(self, instance):
        pop = PlayerCreationScreen(self.game)
        self.me = pop.open()
        return True




if __name__ == "__main__":
    Phase10App().run()


