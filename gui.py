import random
import copy
import os
from .cards import *
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput



class PlayerCreation(GridLayout):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.cols = 1
        self.add_widget(Label(text='Player Name'))
        self.username = TextInput(multiline=False)
        self.add_widget(self.username)



class MyApp(App):
    def build(self):
        return PlayerCreation()


if __name__ == "__main__":
    MyApp.run()
