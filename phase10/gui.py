import asyncio

from kivy.app import App
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager

from phase10.client import GameClient
from phase10.game import Player

class PlayerPopup(Popup):
    pass

class PageMaster(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.open = OpenScreen(name = "open")
        self.add_widget(self.open)

class OpenScreen(Screen):
    def player_pop(self, instance):
        PlayerPopup().open()
        '''if instance.text == "New Player":
            self.p_up = PlayerPopup()
        elif instance.text == "Load Player":
            self.p_up = PlayerPopup()'''

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

    def test_client(self):
        """Trigger the client to send a message and wait for the server response."""
        print("Sending test message...")
        t_cl = asyncio.ensure_future(self.client.test_message())  # Send the message asynchronously
        self.loop.run_until_complete(t_cl)

    def update_label(self, message):
        """Update the label text with a message (for feedback purposes)."""
        Clock.schedule_once(lambda dt: setattr(self, 'title', message), 0)  # Update UI safely in the main thread

    def connect_player(self, name, instance=None):
        """Trigger the client to bind the client_id to this player, adding them to the game"""
        asyncio.set_event_loop(self.loop)
        print(f"Player {name} attatched to client {self.client.client_id}")
        print("running start_async_loop()...")
        self.start_async_loop()
        msg = {
            "type": "connect",
            "client_id": self.client.client_id,
            "name": name,
            "instance": instance
        }
        con_pl = asyncio.ensure_future(self.client.send_message(msg))
        self.loop.run_until_complete(con_pl)


if __name__ == '__main__':
    app = PhaseTenApp()
    app.run()
