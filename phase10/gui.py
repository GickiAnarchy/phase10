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


class TestScreen(Screen):

    async def send_five(self):
        message = {"type": "ready", "player": cl.client_id}
        c = loop.create_task(cl.send_message(message))
        

class Loading(Screen):
    pass

class PageMaster(ScreenManager):
    pass


class PhaseTenApp(App):
    # def __init__(self,**kwargs):
#         super().__init__(**kwargs)

    def build(self):
        self.root = PageMaster()
        self.root.add_widget(Loading(name = "loading"))
        self.root.add_widget(TestScreen(name = "testscreen"))
        self.root.current = "testscreen"
        return self.root


    def start_app(self, msg):
        self.other_task = asyncio.ensure_future(self.waste_time_freely())
        async def run_wrapper():
            await self.async_run()

        m_type = ""
        try:
            m_type = msg["type"]
        except:
            print("No 'type' in msg -> start_app")
        async def send_test():
            pass
        
        return asyncio.gather(run_wrapper(), self.other_task)
        
        return asyncio.gather(run_wrapper(), self.other_task)
    
    
    async def waste_time_freely(self):
        try:
            i = 0
            while True:
                if self.root is not None:
                    status = self.root.ids.label.status
                    print('{} on the beach'.format(status))

                    if self.root.ids.btn1.state != 'down' and i >= 2:
                        i = 0
                        print('Yawn, getting tired. Going to sleep')
                        self.root.ids.btn1.trigger_action()

                i += 1
                await asyncio.sleep(2)
        except asyncio.CancelledError as e:
            print('Wasting time was canceled', e)
        finally:
            print('Done wasting time')


cl = GameClient()
#loop = asyncio.new_event_loop()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(AsyncApp().app_func())
    loop.close()



    # async def mainThread():
#         p10 = PhaseTenApp()
#         b = loop.create_task(p10.async_run())
#         a = loop.create_task(cl.run())
#         (done, pending) = await asyncio.wait({a}, return_when='FIRST_COMPLETED')
#     asyncio.run(mainThread())
