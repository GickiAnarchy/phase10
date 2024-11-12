from kivy.layout.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.properties import ObjectProperty



from phase10.game.classes.player import Player


class PlayerBox(GridLayout):
    player = ObjectProperty(Player)
    hand = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        