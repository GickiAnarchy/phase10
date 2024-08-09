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
from kivy.properties import ObjectProperty

from cards import Player, Stack, Deck, Hand, Card, GameApp, Phase, Goal, RunGoal, SetGoal, ColorGoal, SkipCard

"""GLOBAL"""
EMPTY_SLOT_IMAGE = r"images/empty_slot.png"



class PlayerDisplay(BoxLayout):
    def __init__(self, player: Player = None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        if player == None:
            pop = PlayerCreationScreen(Phase10App().getGameApp())
            self.player = pop.open()
        self.player = player
        self.player_label = ObjectProperty(None)
        self.phase_box = PhaseDisplay()
        self. update_display()

    def update_display(self):
        self.player_label.text = self.player.name
        self.phase_box.phase = self.player.get_current_phase()
        self.phase_box.update_display()

class PhaseDisplay(BoxLayout):
    def __init__(self, phase: Phase, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.phase = phase
        self.update_display()
    
    def update_display(self):
        self.clear_widgets()
        self.add_widget(Label(text=f"Current Phase: {phase.name}"))
        for i, goal in enumerate(self.phase.goals):
            goal_display = GoalDisplay(goal)
            self.add_widget(goal_display)

class GoalDisplay(GridLayout):
    def __init__(self, goal:Goal = None, **kwargs):
        super().__init__(**kwargs)
        self.rows = 2
        self.cols = 1
        self.goal = goal
        self.name = Label()
        self.card_box = BoxLayout(orientation = "horizontal")
        self.card_first = Image(source = EMPTY_SLOT_IMAGE)
        self.card_last = Image(source = EMPTY_SLOT_IMAGE)
        self.card_box.add_widget(self.card_first)
        self.card_box.add_widget(self.card_last)
        self.update_display()

    def update_display(self):
        self.clear_widgets()
        self.name.text = self.goal.name
        if self.goal != None:
            self.goal.cards.sortByNumber()
            self.card_first.source = self.goal.cards[0].getImage()
            self.card_last.source = self.goal.cards[-1].getImage()
        self.root.add_widget(self.name)
        self.root.add_widget(self.card_box)

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

class StackDisplay(BoxLayout):
    def __init__(self, stack: Stack = None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.spacing = 10
        self.stack = stack
        self.update_stack()

    def update_stack(self):
        self.clear_widgets()
        for card in self.stack.cards:
            self.add_widget(SelectableCard(card))

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

class ButtonBox(BoxLayout):
    def __init__(self, gameapp = None, hand = None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.gameapp = gameapp
        self.hand = hand
        self.draw_button = Button()
        self.discard_button = Button()
        self.play_button = Button()
        self.draw_button.bind(on_press = self.draw)
        self.discard_button.bind(on_press = self.discard)
        self.play_button.bind(on_press = self.play)
        self.update_display()

    def update_display(self):
        self.draw_button.text = "Draw"
        self.discard_button.text = "Discard"
        self.play_button.text = "Play"
        self.root.add_widget(self.draw_button)
        self.root.add_widget(self.play_button)
        self.root.add_widget(self.discard_button)

    def draw(self, instance):
        if self.gameapp.turn_phase == "Draw":
            self.gameapp.draw()

    def discard(self, instance):
        if self.gameapp.turn_phase == "Discard":
            sel = self.gameapp.getSelectedCards()
            if len(sel.cards) == 1:
                self.gameapp.discard(sel)

    def play(self, sel_cards, instance):
        if isinstance(sel_cards, list): sel_cards = Stack(sel_cards)
        if isinstance(sel_cards, SkipCard):
            sel_pop = SelectPlayerPopup()
            skipping = sel_pop.open()
            skipping.toggle_skip()

#Popups
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
            return self.game_app.create_player(player_name)
        else:
            print("Please enter a player name.")

class SelectPlayerPopup(Popup):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', spacing=10, padding=10, **kwargs)
        self.lbl = Label("Choose a player.")
        self.root.add_widget(self.lbl)
        self.btns = BoxLayout(orientation="horizontal")
        self.game = Phase10App().getGameApp()
        for p in self.game:
            if p.name == self.game.currentPlayer.name:
                continue
            else:
                self.btns.add_widget(Button(text=p.name, on_press=self.chooseMe))
        self.root.add_widget(self.btns)

    def chooseMe(self, instance) -> Player:
        for p in self.game.players:
            if p.name == instance.text:
                return p




class Phase10App(App):
    game = GameApp()
    def build(self):
        self.root = BoxLayout(orientation="vertical")
        self.create_opponent_info()
        self.create_player_info()
        self.create_dk_and_dis_display()
        self.create_hand_display()
        self.create_button_display()
        return self.root

    def create_opponent_info(self):
        self.opp_info_box = OpponentDisplay(self)
        self.root.add_widget(self.opp_info_box)
    def create_dk_and_dis_display(self):
        self.box = BoxLayout(orientation="horizontal")
        self.deck_box = StackDisplay(game.deck)
        self.box.add_widget(self.deck_box)
        self.discard_box = Stack(game.discards)
        self.box.add_widget(self.discard_box)
        self.root.add_widget(self.box)
    def create_hand_display(self):
        self.player_hand_box = SelectableHand(self.player.hand)
        self.root.add_widget(self.player_hand_box)
    def create_player_info(self):
        self.player_info = PlayerDisplay()
        self.root.add_widget(self.player_info)
    def create_button_display(self):
        self.button_box = ButtonBox(Phase10App().getGameApp())

    def getSelectedCards(self) -> Stack:
        return Stack(self.player_hand_box.get_selected_cards())

    def update_game(self, dt):
        self.opp_info_box.update_display()
        self.deck_box.update_display()
        self.discard_box.update_display()
        self.player_info.update_display()
        self.player_hand_box.update_display()
        self.button_box.update_display()

    @classmethod
    def getGameApp(cls):
        return cls.game



if __name__ == "__main__":
    Phase10App().run()