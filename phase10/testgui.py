#!/usr/bin/env python

import asyncio

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

from client import send_message, run_client
from common import Client


class TestApp(App):
    def build(self):
        self.loop = asyncio.get_event_loop()
        root = BoxLayout(orientation="vertical")
        lbl1 = Label(text="Test Mesaages")
        btn1 = Button(text="Push to Test")
        self.client = Client()
        btn1.bind(on_press = self.register_button(self.client))
        root.add_widget(lbl1)
        root.add_widget(btn1)
        return root

    def register_button(self, cl):
        run_client(cl)
        message = {
            "type": "register",
            "client_id": self.client.client_id
        }
        self.loop.create_task(self.send_test_message())

    async def send_test_message(self, message = None):
        if message == None:
            message = {"type": "test", "data": "Test message"}
        await send_message(self.client, message)




if __name__=="__main__":
    TestApp().run()
    
    
    
##-------------------------------------

import asyncio
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock

from client import GameClient  # Import your GameClient class


class MyApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')

        self.label = Label(text="Waiting for client to start...")
        self.layout.add_widget(self.label)

        self.start_button = Button(text="Draw Card")
        self.start_button.bind(on_press=self.start_client)
        self.layout.add_widget(self.start_button)

        Clock.schedule_once(self.run_async_tasks, 0)  # Start asyncio tasks when app starts
        return self.layout

    async def start_client(self, instance):
        """Trigger client to send a message and then wait for the server response."""
        await self.client.draw_card(0)  # Send the message (draw a card)

    def run_async_tasks(self, dt):
        """Initialize the GameClient and connect to the server."""
        self.client = GameClient()

        # Schedule the client run method to connect and register with the server
        asyncio.ensure_future(self.client.run())

    def update_label(self, message):
        """Update the label text with a message (for feedback purposes)."""
        self.label.text = message


if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    app = MyApp()

    # Running the Kivy app in an executor so it doesn't block asyncio's event loop
    loop.run_in_executor(None, app.run)

    # Start the asyncio event loop
    loop.run_forever()