from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen

# Import the game logic script
import .cards as CARDS


class PlayerHand(BoxLayout):
    player_name = ObjectProperty(None)
    hand_image_grid = ObjectProperty(None)  # Replace with ImageGrid

    def __init__(self, player_name, **kwargs):
        super(PlayerHand, self).__init__(**kwargs)
        self.player_name.text = player_name
        self.hand_image_grid.cols = 10  # Adjust number of columns as needed

    def update_hand_display(self, player):
        self.hand_image_grid.clear_widgets()
        for card in player.hand.cards:
            card_image = Image(source=f"card_images/{card.name.lower()}_{card.color.lower()}.png")
            self.hand_image_grid.add_widget(card_image)

class PhaseGoalDisplay(BoxLayout):
    phase_name = ObjectProperty(None)
    goal_text = ObjectProperty(None)

    def __init__(self, phase_name, goal_text, **kwargs):
        super(PhaseGoalDisplay, self).__init__(**kwargs)
        self.phase_name.text = phase_name
        self.goal_text.text = str(goal_text)

class PlayerCreationScreen(Screen):
    player_name_input = ObjectProperty(None)

    def __init__(self, game_app, **kwargs):
        super(PlayerCreationScreen, self).__init__(**kwargs)
        self.game_app = game_app

    def create_player(self):
        player_name = self.player_name_input.text
        if player_name:
            self.game_app.create_player(player_name)
        else:
            # Handle empty player name
            pass

class GameScreen(Screen):
    def __init__(self, game_app, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        self.game_app = game_app

        # Build the game UI here, similar to your previous code
        # ...

    def draw_card_button_clicked(self, instance):
        # ...

    # Other button handlers and game CARDS

class Phase10App(App):
    def build(self):
        self.game = CARDS.GameApp()
        self.screen_manager = ScreenManager()

        player_creation_screen = PlayerCreationScreen(self.game)
        self.screen_manager.add_widget(player_creation_screen)

        game_screen = GameScreen(self.game)
        self.screen_manager.add_widget(game_screen)

        self.screen_manager.current = 'player_creation'

        return self.screen_manager

    def create_player(self, player_name):
        self.game.create_player(player_name)
        # Handle adding player to game logic and UI
        # ...

