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