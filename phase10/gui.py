#!/usr/bin/env python

import asyncio
import asynckivy as ak

from kivy.app import App, async_runTouchApp
from kivy.base import runTouchApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen, ScreenManager

from phase10.client import GameClient


class GetPlayerScreen(Screen):

    async def send_five(self):
        message = {"type": "ready", "player": cl.client_id}
        c = loop.create_task(cl.send_message(message))
        

class Loading(Screen):
    pass

class PageMaster(ScreenManager):
    pass


class PhaseTenApp(App):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)


    def build(self):
        self.root = PageMaster()
        self.root.add_widget(Loading(name = "loading"))
        self.root.add_widget(GetPlayerScreen(name = "getplayer"))
        self.root.current = "getplayer"
        return self.root





cl = GameClient()
loop = asyncio.new_event_loop()

if __name__ == '__main__':
    async def mainThread():
        p10 = PhaseTenApp()
        b = loop.create_task(p10.async_run())
        a = loop.create_task(cl.run())
        (done, pending) = await asyncio.wait({a}, return_when='FIRST_COMPLETED')


    asyncio.run(mainThread())
