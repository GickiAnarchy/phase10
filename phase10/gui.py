import asyncio
from threading import Thread

from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.clock import Clock

from phase10.client import GameClient


class TestScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def send_five(self):
        pass  # Your logic here


class Loading(Screen):
    pass


class PageMaster(ScreenManager):
    pass


class PhaseTenApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.client = GameClient()

    def build(self):
        self.root = PageMaster()
        self.root.add_widget(Loading(name="loading"))
        self.root.add_widget(TestScreen(name="testscreen"))
        self.root.current = "testscreen"

        # Start the async loop in the same thread as Kivy
        Clock.schedule_once(self.start_async_loop, 0)

        return self.root

    def start_async_loop(self, dt):
        """Start the asyncio loop in the same thread as Kivy."""
        self.loop = asyncio.new_event_loop()  # Create a new event loop
        asyncio.set_event_loop(self.loop)
        self.in_cl = asyncio.ensure_future(self.init_client())  # Start the client asynchronously
        self.loop.run_until_complete(self.in_cl)


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


if __name__ == '__main__':
    app = PhaseTenApp()
    app.run()