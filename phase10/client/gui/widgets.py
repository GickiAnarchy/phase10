from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, StringProperty, NumericProperty, BooleanProperty
from kivy.lang import Builder

from phase10.game.classes.player import Player


Builder.load_file("widgets.kv")


class InfoWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_player(self, *args):
        pass


class NameInfoWidget(InfoWidget):
    player = ObjectProperty(None)  # the player instance

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_player(self, *args):
        self.ids.name_label.text = self.player.name


class PhaseTenInfoWidget(InfoWidget):
    player_name = StringProperty("")        #players name
    player_score = NumericProperty(0)       #players score
    current_phase = NumericProperty(0)      #players current phase
    is_active = BooleanProperty(False)      #players current turn status


    def on_player(self, *args):
        """Updates displayed information based on the Player instance."""
        print("in PlayerInfoWidget.on_player()")
        if isinstance(self.player, Player):
            self.player_name = self.player.name
            self.player_score = self.player.score
            self.current_phase = self.player.current_phase.number
            self.is_active = self.player.is_active
            print("\t-Player updated")

    def update_info(self, *args):
        """Updates displayed information based on the Player instance."""
        if isinstance(self.player, Player):
            self.player_name = self.player.name
            self.player_score = self.player.score
            self.current_phase = self.player.phase_desc() if self.player.phase_desc() else 0
            self.is_active = self.player.is_active if self.player.is_active else "False"


class RPSInfoWidget(InfoWidget):
    player_name = StringProperty("")
    player_score = NumericProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_player(self, *args):
        self.player_name = self.player.name
        self.player_score = self.player.score
