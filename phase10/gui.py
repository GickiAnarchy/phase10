import asyncio

from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.togglebutton import ToggleButton

from client import GameClient
from phase10.game.deck import Deck
from phase10.game.discards import Discards
from phase10.game.player import Player


#   SELECTABLE
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


#   SCREENS
class PageMaster(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.open = OpenScreen(name = "open")
        self.add_widget(self.open)

class OpenScreen(Screen):
    def player_pop(self, instance):
        self.pop = PlayerPopup()
        if instance.text == "Load Player":
            self.pop.ids.popup_btn.text = "Load"
        if instance.text == "New Player":
            self.pop.ids.popup_btn.text = "Create"
        self.pop.open()
        
class PlayerPopup(Popup):
    def make_player(self, instance):
        name_in = self.ids.name_input.text
        pin_in = self.ids.pin_input.text
        if instance.text == "Load":
            print(f"\t{name_in}\n\t{pin_in}")
            App.get_running_app().load_player(name_in,pin_in)
        if instance.text == "Create":
            print(f"\t{name_in}\n\t{pin_in}")
            newp = Player(name = name_in,pin = pin_in)
            App.get_running_app().set_player(newp)
            App.get_running_app().create_player(name_in,pin_in)
            App.get_running_app().save_player()
            self.dismiss()
        
#   #   #   #   #   #   #   #   #   #
class PhaseTenApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.player = None
        self.client = GameClient(self)
        self.client.make_client_id()
        self.loop = asyncio.new_event_loop()

    def build(self):
        self.app_root = PageMaster()
        self.app_root.current = "open"
        return self.app_root

    def start_async_loop(self, dt=None):
        in_cl = asyncio.ensure_future(self.init_client())  # Start the client asynchronously
        print("\tin start_async_loop()\nRunning init_client()")
        self.loop.run_until_complete(in_cl)

    async def init_client(self):
        """Initialize the GameClient and connect to the server."""
        print("Initializing client...")
        await self.client.start_client()
        print("Client connected!")

    def connect_player(self, instance=None):
        """Trigger the client to bind the client_id to this player, adding them to the game"""
        asyncio.set_event_loop(self.loop)
        print(f"Client {self.client.client_id} is connecting")
        print("running start_async_loop()...")
        self.start_async_loop()
        msg = {
            "type": "connect",
            "client_id": self.client.client_id,
            "instance": instance
        }
        con_pl = asyncio.ensure_future(self.client.send_message(msg))
        self.loop.run_until_complete(con_pl)
        print(f"Client {self.client.client_id} is connected")

    def test_client(self):
        """Trigger the client to send a message and wait for the server response."""
        print("Sending test message...")
        t_cl = asyncio.ensure_future(self.client.test_message())  # Send the message asynchronously
        self.loop.run_until_complete(t_cl)

    def load_player(self, name:str, pin:str):
        """User requests to load a player from the server"""
        message = {"type":"load", "client_id": self.client.client_id, "name": name, "pin": pin, "description": "Load player"}
        print("Sending load_player message...")
        fload = asyncio.ensure_future(self.client.send_message(message))  # Send the message asynchronously
        self.loop.run_until_complete(fload)
        if self.client.player:
            self.player = self.client.player

    def create_player(self, name, pin):
        """User requests to create a player"""
        message = {"type": "create", "client_id": self.client.client_id, "name": name, "pin": pin,
                   "player": self.player, "description": "Create player"}
        print("Sending create message...")
        fcreate = asyncio.ensure_future(self.client.send_message(message))  # Send the message asynchronously
        self.loop.run_until_complete(fcreate)
        return

    def save_player(self):
        message = {"type": "save", "client_id": self.client.client_id, "player": self.player, "description": "Create player"}
        print("Sending save message...")
        fsave = asyncio.ensure_future(self.client.send_message(message))  # Send the message asynchronously
        self.loop.run_until_complete(fsave)

    def update_label(self, message):
        """Update the label text with a message (for feedback purposes)."""
        Clock.schedule_once(lambda dt: setattr(self, 'title', message), 0)  # Update UI safely in the main thread

    def on_stop(self):
        super().on_stop()
        print("stop")
        if self.client.player:
            self.save_player()  # Save player before close.

    def on_pause(self):
        super().on_pause()
        print("pause")
        self.save_player()  # Save player before close.

    def on_start(self):
        super().on_start()
        self.connect_player()

    def set_player(self, newp):
        self.player = newp
        self.set_client_player(newp)
        print("Set the player in gui")

    def set_client_player(self, newp):
        self.client.player = newp
        print("Set the player in client")

if __name__ == '__main__':
    app = PhaseTenApp()
    app.run()
