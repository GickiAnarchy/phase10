import asyncio
import random

from kivy.app import App
from kivy.base import EventLoop
from kivy.properties import ObjectProperty, ListProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager

from phase10.client import GameClient
from phase10.game.classes.deck import Deck
from phase10.game.classes.player import Player
from phase10.gui.selectable import SelectableCard
from phase10.gui.widgets import PlayerInfoWidget


# get the Window instance safely
EventLoop.ensure_window()
window = EventLoop.window
EventLoop.window.title = "PPHHAASSEE"

#   SELECTABLE
# Moved to selectable.py


#   SCREENS
class PageMaster(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.open = OpenScreen(name = "open")
        self.play = PlayScreen(name = "play")
        self.test_menu = TestMenu(name = "test_menu")
        self.sel_card = TestSelectCard(name="sel_card")
        self.sel_hand = TestSelectHand(name="sel_hand")
        self.add_widget(self.test_menu)
        self.add_widget(self.sel_card)
        self.add_widget(self.sel_hand)
        self.add_widget(self.play)
        self.add_widget(self.open)

    def goto_play(self):
        self.current = "play"

class PlayScreen(Screen):
    pass

class OpenScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.pop = None
        self.newB = self.ids.new_btn
        self.loadB = self.ids.load_btn

    def player_pop(self, instance):
        self.pop = PlayerPopup()
        if instance.text == "Load Player":
            self.pop.ids.popup_btn.text = "Load"
        if instance.text == "New Player":
            self.pop.ids.popup_btn.text = "Create"
        self.pop.open()

class TestSelectCard(Screen):
    back_btn = ObjectProperty(None)
    selCard = ObjectProperty(None)
    rootbox = ObjectProperty(None)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.deck = Deck()
        self.back_btn.text = "Back"

    def on_enter(self, *args):
        super().on_enter(*args)
        self.deck.create_deck()
        self.deck.shuffle()

    def on_leave(self, *args):
        self.deck.clear_deck()
        super().on_leave(*args)

    def new_card(self):
        self.selCard.add_card(self.deck.draw_card())

class TestSelectHand(Screen):
    pl_hand = ListProperty()
    sel_hand_w = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.deck = Deck()

    def update_hand(self):
        self.sel_hand_w.update_hand(self.pl_hand)

    def deal_hand(self):
        if self.deck.used:
            self.deck.clear_deck()
        if len(self.pl_hand) > 0:
            self.pl_hand.clear()
        self.deck.create_deck()
        self.deck.shuffle()
        for _ in range(10):
            self.pl_hand.append(self.deck.draw_card())
        self.sel_hand_w.update_hand(self.pl_hand)

    def get_selected(self):
        sel_cards = self.sel_hand_w.get_selected_cards()
        if len(sel_cards) > 0:
            for c in sel_cards:
                print(f"{c.get_description()}\n")

    def on_leave(self, *args):
        self.deck.clear_deck()
        super().on_leave(*args)

class TestMenu(Screen):
    def to_sel_hand(self):
        self.manager.current = "sel_hand"

    def to_sel_card(self):
        self.manager.current = "sel_card"

    def get_color(self):
        R = random.random()
        G = random.random()
        B = random.random()
        return R,G,B,1



#   DIALOGS
class PlayerPopup(Popup):
    def make_player(self, instance):
        name_in = self.ids.name_input.text
        pin_in = self.ids.pin_input.text
        okay = None
        if instance.text == "Load":
            print(f"\t{name_in}\n\t{pin_in}")
            okay = App.get_running_app().load_player(name_in,pin_in)
        if instance.text == "Create":
            print(f"\t{name_in}\n\t{pin_in}")
            okay = App.get_running_app().create_player(name_in,pin_in)
        if okay:
            self.dismiss()
            App.get_running_app().app_root.current = "test_menu"
        else:
            self.open()

    def on_dismiss(self):
        super().on_dismiss()

        
#   MAIN APP
class PhaseTenApp(App):
    player = ObjectProperty(Player)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.player_box = None
        self.app_root = None
        self.root_lout = FloatLayout()
        self.client = GameClient()
        self.client.make_client_id()
        self.loop = asyncio.new_event_loop()

    def build(self):
        self.title = "|||    PHASE 10    |||"
        self.player_box = PlayerInfoWidget(size_hint = (0.3,0.2), pos_hint = {'right':1, 'top':1})
        self.app_root = PageMaster()
        self.root_lout.add_widget(self.app_root)
        self.root_lout.add_widget(self.player_box)
        self.app_root.current = "open"
        return self.root_lout

    def on_player(self, *args):
        print("in PhaseTenApp.on_player()")
        self.player_box.player = self.player
        print("\t-PhaseTenApp.player updated")
        print(f"\n{args}")

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

    def test_client(self,mmssgg):
        """Trigger the client to send a message and wait for the server response."""
        print("Sending test message...")
        t_cl = asyncio.ensure_future(self.client.send_message(mmssgg))  # Send the message asynchronously
        self.loop.run_until_complete(t_cl)

    def load_player(self, name:str, pin:str):
        """User requests to load a player from the server"""
        fload = asyncio.ensure_future(self.client.send_load_message(name, pin))  # Send the message asynchronously
        if self.loop.run_until_complete(fload):
            self.player = self.client.player
            return True
        else:
            return False

    def create_player(self, name, pin):
        fcreate = asyncio.ensure_future(self.client.send_create_message(name, pin))  # Send the message asynchronously
        if self.loop.run_until_complete(fcreate):
            self.player = self.client.player
            print(f"{self.player.name} is new player")
            return True
        else:
            print("Couldn't create player")
            return False

    def save_player(self, player):
        fsave = asyncio.ensure_future(self.client.send_save_message(player))  # Send the message asynchronously
        self.loop.run_until_complete(fsave)

    def on_stop(self):
        super().on_stop()
        print("stop")# Save player before close.

    def on_start(self):
        super().on_start()
        self.connect_player()

    def get_player(self):
        return self.player


if __name__ == '__main__':
    app = PhaseTenApp()
    app.run()