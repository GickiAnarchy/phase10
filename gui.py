import random
import copy
import os

from .cards import Card, Deck
from .cards import Phase, PhaseGoal
from .cards import Player, Game

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.widget import Widget


class PlayerCreation(GridLayout):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.cols = 1
        self.add_widget(Label(text='Player Name'))
        self.username = TextInput(multiline=False)
        self.add_widget(self.username)


class CardWidget(Widget):
    def __init__(self, card, **kwargs):
        super().__init__(**kwargs)
        self.card = card  # Store the card object
        # Load card image (replace with your image paths)
        self.image = Image(source=f"images/{card.color}_{card.name}.png")
        self.add_widget(self.image)
        # Add other card properties or functionalities as needed
    
    def on_press(self):
        #Have the card selected
        pass
    




class MyApp(App):
    def build(self):
        return PlayerCreation()


if __name__ == "__main__":
    MyApp.run()
