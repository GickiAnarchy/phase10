import random
import copy
import os

"""
from .cards import Card, Deck
from .cards import Phase, PhaseGoal
from .cards import Player, Game
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty

# Import the game logic script
import .cards as logic


class PlayerHand(BoxLayout):
    player_name = ObjectProperty(None)
    hand_text = ObjectProperty(None)

    def __init__(self, player_name, **kwargs):
        super(PlayerHand, self).__init__(**kwargs)
        self.player_name.text = player_name
        self.hand_text.text = ""

class PhaseGoalDisplay(BoxLayout):
    phase_name = ObjectProperty(None)
    goal_text = ObjectProperty(None)

    def __init__(self, phase_name, goal_text, **kwargs):
        super(PhaseGoalDisplay, self).__init__(**kwargs)
        self.phase_name.text = phase_name
        self.goal_text.text = goal_text

class Phase10App(App):
    game = None
    current_player = None
    current_phase = None
    player_hands = []
    phase_goal_displays = []

    def build(self):
        # Initialize the game logic
        self.game = logic.GameCLI([logic.Player("Player 1"), logic.Player("Player 2")])
        self.game.deck.deal(self.game.players)
        self.current_player = self.game.players[0]
        self.current_phase = self.current_player.checkCurrentPhase()

        # Create the main layout
        main_layout = BoxLayout(orientation="vertical")

        # Display current player information
        player_info_box = BoxLayout(orientation="horizontal")
        player_info_box.add_widget(Label(text="Current Player: "))
        player_info_box.add_widget(Label(text=self.current_player.name))
        main_layout.add_widget(player_info_box)

        # Display current phase information
        phase_info_box = BoxLayout(orientation="horizontal")
        phase_info_box.add_widget(Label(text="Current Phase: "))
        phase_info_box.add_widget(Label(text=self.current_phase.name))
        main_layout.add_widget(phase_info_box)

        # Display player hands
        for player in self.game.players:
            player_hand = PlayerHand(player.name)
            player_hand.hand_text.text = player.hand.showHand(player.name)
            self.player_hands.append(player_hand)
            main_layout.add_widget(player_hand)

        # Display phase goals
        for goal in self.current_phase.goal:
            goal_display = PhaseGoalDisplay(self.current_phase.name, str(goal))
            self.phase_goal_displays.append(goal_display)
            main_layout.add_widget(goal_display)

        # Draw card button
        draw_card_button = Button(text="Draw Card")
        draw_card_button.bind(on_press=self.draw_card_button_clicked)
        main_layout.add_widget(draw_card_button)

        # Discard card button
        discard_card_button = Button(text="Discard Card")
        discard_card_button.bind(on_press=self.discard_card_button_clicked)
        main_layout.add_widget(discard_card_button)

        # Play cards button (not yet implemented)
        play_cards_button = Button(text="Play Cards")
        play_cards_button.bind(on_press=self.play_cards_button_clicked)
        play_cards_button.disabled = True  # Disable until implemented
        main_layout.add_widget(play_cards_button)

        return main_layout

    def draw_card_button_clicked(self, instance):
        # Draw a card from the deck and update the UI
        card = self.game.deck.drawCard()
        self.current_player.recieveCard(card)
        
