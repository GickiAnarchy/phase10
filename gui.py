from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import AsyncImage
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

# Import your game logic classes from cards.py
from cards import Player, Deck, Hand, Card

class Phase10App(App):
    def build(self):
        # Initialize game objects
        self.deck = Deck()
        self.player = Player("Player 1")
        self.deck.deal(self.player)  # Deal cards to player

        # Create the main layout
        root_widget = BoxLayout(orientation="vertical")

        # Player information section
        player_info = BoxLayout(orientation="horizontal")
        player_label = Label(text=f"Player: {self.player.name}")
        score_label = Label(text=f"Score: {self.player.score}")
        player_info.add_widget(player_label)
        player_info.add_widget(score_label)
        root_widget.add_widget(player_info)

        # Hand display section
        hand_scroll = ScrollView()
        hand_box = BoxLayout()
        for card in self.player.hand.cards:
            card_image = AsyncImage(source=card.getImage())
            hand_box.add_widget(card_image)
        hand_scroll.add_widget(hand_box)
        root_widget.add_widget(hand_scroll)

        # Discard pile section (placeholder)
        discard_pile = BoxLayout(orientation="horizontal")
        discard_label = Label(text="Discard Pile:")
        discard_pile.add_widget(discard_label)
        # Add button or image for discard pile
        root_widget.add_widget(discard_pile)

        # Deck section (placeholder)
        deck_box = BoxLayout(orientation="horizontal")
        deck_label = Label(text="Deck:")
        deck_image = AsyncImage(source="images/CardBack.png")  # Replace with deck back image
        deck_box.add_widget(deck_label)
        deck_box.add_widget(deck_image)
        root_widget.add_widget(deck_box)

        # Action buttons (placeholder)
        button_box = BoxLayout(orientation="horizontal")
        draw_button = Button(text="Draw Card")
        play_button = Button(text="Play Cards")
        discard_button = Button(text="Discard Card")
        button_box.add_widget(draw_button)
        button_box.add_widget(play_button)
        button_button.add_widget(discard_button)
        root_widget.add_widget(button_box)

        # Bind button actions (to be implemented)
        # draw_button.bind(on_press=self.draw_card)
        # play_button.bind(on_press=self.play_cards)
        # discard_button.bind(on_press=self.discard_card)

        return root_widget

    # Implement button actions here (functions to call corresponding methods from cards.py)
    def draw_card(self, instance):
        # Call player.recieveCard(self.deck.drawCard()) and update UI
        pass

    def play_cards(self, instance):
        # Call player related methods to handle playing cards and update UI
        pass

    def discard_card(self, instance):
        # Call player related methods to handle discarding cards and update UI
        pass

if __name__ == "__main__":
    Phase10App().run()
