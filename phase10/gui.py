import asyncio

from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.clock import Clock

from phase10 import Player
from phase10.client import GameClient


class TestScreen(Screen):
    name_input = ObjectProperty(None)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name_input.disabled = True


    def send_five(self):
        pass  # Your logic here

    def player_info_box(self):
        try:
            the_player = App.get_running_app().root.client.player
        except Exception as e:
            print(f"Error. Maybe there is not player?\n{e}")
            return
        the_player = Player(the_player)
        App.get_running_app().app_root.current = "player_info"

class Loading(Screen):
    pass

class NameScreen(Screen):
    pass

class PlayerInfoScreen(Screen):
    pl = ObjectProperty(None)
    p_info = ObjectProperty(None)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pl = self.update_info)
    
    def update_info(self, instance, value):
        self.p_info.player_name_lbl.text = value.name
        self.p_info.player_score_lbl.text = value.score
        self.p_info.player_phase_lbl.text = value.current_phase.name
        if value.is_active:
            self.player_active_lbl.text = "☆☆☆"
        else:
            self.player_active_lbl.text = "-"
        
class PlayerInfo(GridLayout):
    player_name_lbl = ObjectProperty()
    player_score_lbl = ObjectProperty()
    player_phase_lbl = ObjectProperty()
    player_active_lbl = ObjectProperty()

    def __init__(self, player = None, **kwargs):
        super().__init__(**kwargs)
        self.player = player
        if player:
            self.player_name_lbl = player.name
            self.player_score_lbl = str(player.score)
            self.player_phase_lbl = player.current_phase.name
            self.player_active_lbl = "False"
        else:
            self.player_name_lbl = "--"
            self.player_score_lbl = "--"
            self.player_phase_lbl = "--"
            self.player_active_lbl = "--"

    def update(self):
        self.clear_widgets()
        self.player_name_lbl = player.name
        self.player_score_lbl = str(player.score)
        self.player_phase_lbl = player.current_phase.name
        self.player_active_lbl = "False"
        
class PageMaster(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Loading(name="loading"))
        self.add_widget(TestScreen(name="testscreen"))
        self.add_widget(NameScreen(name="namescreen"))
        self.add_widget(PlayerInfoScreen(name = "player_info"))

class

#   #   #   #   #   #   #   #   #   #
class PhaseTenApp(App):
    game = ObjectProperty(None)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.client = GameClient(self)
        self.client.make_client_id()
        self.loop = asyncio.new_event_loop()

    def build(self):
        self.app_root = PageMaster()
        self.app_root.current = "namescreen"
        self.bind(game = self.update_game)
        return self.app_root
 
    def update_game(self, instance, value):
        
    
    def start_async_loop(self, dt = None):
        if self.client.has_player():
            in_cl = asyncio.ensure_future(self.init_client())  # Start the client asynchronously
            print("\tin start_async_loop()\nRunning init_client()")
            self.loop.run_until_complete(in_cl)
        else:
            print("No player attached to the client!")

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

    def connect_player(self, name, instance = None):
        """Trigger the client to bind the client_id to this player, adding them to the game"""
        asyncio.set_event_loop(self.loop)
        self.client.player = Player(name)
        print(f"Player {name} attatched to client {self.client.client_id}")
        print("running start_async_loop()...")
        #Clock.schedule_once(self.start_async_loop, 0)
        self.start_async_loop()

        msg = {
            "type": "connect_player",
            "client_id": self.client.client_id,
            "name": name,
            "instance": instance
        }
        con_pl = asyncio.ensure_future(self.client.send_message(msg))
        self.loop.run_until_complete(con_pl)

    


if __name__ == '__main__':
    app = PhaseTenApp()
    app.run()