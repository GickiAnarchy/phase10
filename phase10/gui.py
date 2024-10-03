#!/usr/bin/env python

import asyncio

from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen, ScreenManager

from client import run_main
from common import Client


class GetPlayerScreen(Screen):
    name_input = ObjectProperty(None)

    def go_button_release(self):
        message = {"type":"get_player", "name":self.name_input.text}



class Loading(Screen):
    pass


class PageMaster(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.loading = Loading(name="loading")
        self.add_widget(self.loading)

    @staticmethod
    def get_client(self):
        return



class PhaseTenApp(App):

    def build(self):
        self.loop = asyncio.get_event_loop()
        self.client = Client()
        run_main()
        return PageMaster()


    @property
    def client(self):
        return self._client

    @client.setter
    def client(self, newclient):
        self._client = newclient


if __name__ == "__main__":
    PhaseTenApp().run()
