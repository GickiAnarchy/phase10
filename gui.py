import random

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.image import AsyncImage
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.uix.popup import Popup

from cards import Player, Stack, Deck, Hand, Card, GameApp



class PlayerCreationScreen(Popup):
    def __init__(self, game_app, **kwargs):
        super().__init__(orientation='vertical', spacing=10, padding=10, **kwargs)
        self.game_app = game_app

        self.name_label = Label(text='Player Name:')
        self.name_input = TextInput(multiline=False)

        self.create_button = Button(text='Create Player')
        self.create_button.bind(on_press=self.create_player)

        self.add_widget(self.name_label)
        self.add_widget(self.name_input)
        self.add_widget(self.create_button)

    def create_player(self, instance):
        player_name = self.name_input.text
        if player_name:
            self.game_app.create_player(player_name)
            return
        else:
            print("Please enter a player name.")

class OpponentDisplay(BoxLayout):
    def __init__(self, opponent , **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        if opponent == None:
            opponent = Player("Default Opponent")
        self.opponent = opponent
        self.opp_name_label = Label()
        self.opp_hand_info = StackDisplay(self.opponent.hand)
        self.update_display()

    def update_display(self):
        self.opp_name_label.text = self.opponent.name
        self.opp_hand_info.update_display()
        self.add_widget(self.opp_name_label)
        self.add_widget(self.opp_hand_info)

class PhaseDisplay(BoxLayout):
    def __init__(self, player, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.player = player
        self.update_display()
    
    def update_display(self):
        self.clear_widgets()
        current_phase = self.player.get_current_phase()
        if current_phase:
            self.add_widget(Label(text=f"Current Phase: {current_phase.name}"))
            for i, goal in enumerate(current_phase.goals):
                goal_text = f"Goal {i+1}: "
                if isinstance(goal, SetGoal):
                    goal_text += f"Set of {goal.min_cards}"
                elif isinstance(goal, RunGoal):
                    goal_text += f"Run of {goal.min_cards}"
                elif isinstance(goal, ColorGoal):
                    goal_text += f"Color group of {goal.min_cards}"
                goal_text += f" ({'Complete' if goal.complete else 'Incomplete'})"
                self.add_widget(Label(text=goal_text))
        else:
            self.add_widget(Label(text="All phases complete!"))

class SelectableCard(ToggleButton):
    def __init__(self, card, **kwargs):
        super().__init__(**kwargs)
        self.card = card
        self.background_normal = card.getImage()
        self.background_color = (1, 1, 1, 1)  # White background
        self.size_hint = (None, None)
        self.size = (100, 150)  # Adjust size as needed

        # Add a colored border when selected
        with self.canvas.before:
            self.border_color = Color(0, 1, 0, 1)  # Green border
            self.border = Rectangle(pos=self.pos, size=self.size)
        
        self.bind(pos=self.update_border, size=self.update_border,
                  state=self.update_border)

    def update_border(self, *args):
        self.border.pos = self.pos
        self.border.size = self.size
        if self.state == 'down':
            self.border_color.a = 1  # Fully opaque
        else:
            self.border_color.a = 0  # Fully transparent

class SelectableHand(BoxLayout):
    def __init__(self, hand, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.spacing = 10
        self.hand = hand
        self.update_hand()

    def update_hand(self):
        self.clear_widgets()
        for card in self.hand.cards:
            self.add_widget(SelectableCard(card))

    def get_selected_cards(self):
        return [widget.card for widget in self.children if widget.state == 'down']

class PlayerDisplay(BoxLayout):
    def __init__(self, player = None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        if player == None:
            self.player_popup = PlayerCreationScreen()
            try:
                self.payer = self.player_popup.open()
            except:
                print("guess were just gonna crash.")
        self.player = player
        self.left = BoxLayout(orientation = "vertical")
        self.player_label = Label()
        self.current_phase_label = Label()
        self.left.add_widget(self.current_phase_label)
        self.left.add_widget(self.player_label)
        self.right = BoxLayout(orientation = "vertical")
        self.phase_box = PhaseDisplay(self.player)
        self. update_display(self)

    def update_display(self):
        self.player_label.text = self.player.name
        c_phase = self.player.get_current_phase()
        self.current_phase_label.text - c_phase.name
        self.phase_box.update_display()

class StackDisplay(BoxLayout):
    def __init__(self, stack, img = "images/stack_back_small.png", **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.stack = stack
        self.image = Image(source = img)
        self.amount_display = Label()
        self.update_display()

    def update_display(self):
        self.amount_display.text = f"{len(self.stack.cards)}"
        self.root.add_widget(self.image)
        self.root.add_widget(self.amount_display)



class Phase10App(App):
    game = GameApp()
    def build(self):
        self.root = BoxLayout(orientation="vertical")
        self.create_opponent_info()
        self.create_player_info()
        self.create_dk_and_dis_display()
        self.create_phase_display()
        self.create_hand_display()
        self.create_action_buttons()
        return self.root

    def create_opponent_info(self):
        self.opp_info_box = OpponentDisplay(self)
        self.root.add_widget(self.opp_info_box)

    def create_player_info(self):
        self.player_info = PlayerDisplay()
        self.root.add_widget(self.player_info)

    def create_phase_display(self):
        self.phase_display = PhaseDisplay(self.player)

    def create_hand_display(self):
        self.player_hand_box = SelectableHand(self.player.hand)
        self.root.add_widget(self.player_hand_box)

    def create_dk_and_dis_display(self):
        self.box = BoxLayout(orientation="horizontal")
        self.deck_box = StackDisplay(game.deck)
        self.box.add_widget(self.deck_box)
        self.discard_box = Stack(game.discards)
        self.box.add_widget(self.discard_box)
        self.root.add_widget(self.box)

    #
    # TODO BUTTON ROW CLASS??
    def create_action_buttons(self):
        self.button_box = BoxLayout(orientation="horizontal")
        self.draw_button = Button(text="Draw Card", on_press=self.draw_card)
        self.play_button = Button(text="Play Cards", on_press=self.play_cards)
        self.discard_button = Button(
            text="Discard Card", on_press=self.discard_card)
        self.button_box.add_widget(self.draw_button)
        self.button_box.add_widget(self.play_button)
        self.button_box.add_widget(self.discard_button)
        self.root.add_widget(self.button_box)
    def update_button_states(self):
        is_current_player = self.player == self.game.getCurrentPlayer()
        self.draw_button.disabled = not is_current_player
        self.play_button.disabled = not is_current_player
        self.discard_button.disabled = not is_current_player

    def update_game(self, dt):
        self.opp_info_box.update_display()
        self.create_dk_and_discrd_display.deck_box.update_display()
        self.create_dk_and_discrd_display.deck_discard_box.update_display()
        self.phase_display.update_display()
        self.player_info.update_display()
        self.player_hand_box.update_display()




if __name__ == "__main__":
    Phase10App().run()