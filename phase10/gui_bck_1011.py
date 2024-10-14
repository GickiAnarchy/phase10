#!/usr/bin/env python

import asyncio
from asyncio import get_event_loop, new_event_loop

import asynckivy as ak

from kivy.app import App, async_runTouchApp
from kivy.base import runTouchApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen, ScreenManager

from phase10.client import GameClient


class TestScreen(Screen):
    btn5 = ObjectProperty(None)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.btn5.bind(on_release = self.send_5)

    def send_five(self):
        app = App.get_running_app()


    async def send_5(self, *args):
        print(*args)
        message = {"type": "ready", "player": PhaseTenApp.cl.client_id}
        await PhaseTenApp.cl.send_message(message)


class Loading(Screen):
    pass

class PageMaster(ScreenManager):
    pass


class PhaseTenApp(App):
    cl = GameClient()

    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    def build(self):
        self.root = PageMaster()
        self.root.add_widget(Loading(name = "loading"))
        self.root.add_widget(TestScreen(name ="getplayer"))
        self.root.current = "getplayer"
        return self.root

    def on_start(self):
        self.loop = get_event_loop()
        self.a_task = self.loop.create_task(PhaseTenApp.cl.run())
        #asyncio.ensure_future(PhaseTenApp.cl.run())



p10 = PhaseTenApp()
loop = asyncio.new_event_loop()

if __name__ == '__main__':
    asyncio.run(p10.async_run())

'''
    async def mainThread():
        #a = loop.create_task(p10.async_run())
        a = loop.create_task(cl.run())
        (done, pending) = await asyncio.wait({a}, return_when='FIRST_COMPLETED')

    asyncio.run(mainThread())
'''
