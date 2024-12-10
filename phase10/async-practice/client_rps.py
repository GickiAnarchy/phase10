import asyncio
import random

from kivy.app import App
from kivy.base import EventLoop
from kivy.properties import ObjectProperty, ListProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager


class RPSApp(App):
    def build(self):
        pass