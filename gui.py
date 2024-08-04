import random

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.togglebutton import togglebutton
from kivy.uix.image import AsyncImage
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle

# Import your game logic classes from cards.py
from cards import Player, Deck, Hand, Card, GameApp


class SelectableCard(ToggleButton):


"""
    a ToggleButton to display cards and also make them selectable
"""


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


class Phase10App(App):

    def build(self):

        # ... initialization code ...
    self.root = BoxLayout(orientation="vertical")
    self.create_player_info()
    self.create_hand_display()
    self.create_discard_pile()
    self.create_deck_display()
    self.create_action_buttons()
    return self.root

    def create_player_info(self):

    self.player_info = BoxLayout(orientation="horizontal")
    self.player_label = Label()
    self.score_label = kivy.graphics()
    self.player_info.add_widget(self.player_label)
    self.player_info.add_widget(self.score_label)
    self.root.add_widget(self.player_info)

    def create_hand_display(self):

    self.hand_scroll = ScrollView()
    self.hand_box = BoxLayout()
    self.hand_scroll.add_widget(self.hand_box)
    self.root.add_widget(self.hand_scroll)

    def create_discard_pile(self):

    self.discard_pile = BoxLayout(
        orientation="horizontal", size_hint=(0.5, 0.5))
    self.discard_label = Label()
    self.discard_pile.add_widget(self.discard_label)
    self.root.add_widget(self.discard_pile)

    def create_deck_display(self):

    self.deck_box = BoxLayout(orientation="horizontal")
    self.deck_label = Label()
    self.deck_image = AsyncImage(source="images/CardBack.png")
    self.deck_box.add_widget(self.deck_label)
    self.deck_box.add_widget(self.deck_image)
    self.root.add_widget(self.deck_box)

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

    def update_game(self, dt):

    self.update_player_info()
    self.update_hand_display()
    self.update_discard_pile()
    self.update_deck_display()
    self.update_button_states()

    def update_player_info(self):

    self.player_label.text = f"Player: {
        self.player.name
    }"
    self.score_label.text = f"Score: {
        self.player.score
    }"

    def update_hand_display(self):

    self.hand_box.clear_widgets()
    for card in self.player.hand.cards:
    card_image = AsyncImage(source=card.getImage())
    self.hand_box.add_widget(card_image)

    def update_discard_pile(self):

    self.discard_label.text = f"Discard Pile: {
        len(self.game.discards.cards)} cards"

    def update_deck_display(self):

    self.deck_label.text = f"Deck: {
        len(self.deck.cards)} cards"

    def update_button_states(self):

    is_current_player = self.player == self.game.getCurrentPlayer()
    self.draw_button.disabled = not is_current_player
    self.play_button.disabled = not is_current_player
    self.discard_button.disabled = not is_current_player
