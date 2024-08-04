import random

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import AsyncImage
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock

# Import your game logic classes from cards.py
from cards import Player, Deck, Hand, Card, GameApp



class Phase10App(App):
    def build(self):
        self.game = GameApp()                                       #Main Game app from card.py

        self.game.createPlayer("Sam")
        self.player = self.game.getPlayer("Sam")
            # Need to create a create player screen

        self.game.createPlayer("George")                            # For testing purposes

        self.cycler = self.game.getNextPlayer(self.game.players)    # Player Turn cycler

        self.deck = self.game.deck                                  # Phase 10 Deck
        Clock.schedule_interval(self.update_game, 1/60)             # update clock =
        self.game.startGame()

        
    def update_game(self, dt):

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
        discard_pile = BoxLayout(orientation="horizontal", size_hint_x = .5, size_hint_y = .5)
        discard_label = Label(text=f"Discard Pile: {len(self.game.discards.cards)} cards")
        discard_pile.add_widget(discard_label)
        # Add button or image for discard pile
        root_widget.add_widget(discard_pile)

        # Deck section (placeholder)
        deck_box = BoxLayout(orientation="horizontal")
        deck_label = Label(text=f"Deck: {len(self.deck.cards)} cards")
        deck_box.add_widget(deck_label)
        deck_image = AsyncImage(source="images/CardBack.png")  # Replace with deck back image
        deck_box.add_widget(deck_image)
        root_widget.add_widget(deck_box)

        # Action buttons (placeholder)
        button_box = BoxLayout(orientation="horizontal")
        draw_button = Button(text="Draw Card")
        play_button = Button(text="Play Cards")
        discard_button = Button(text="Discard Card")
        button_box.add_widget(draw_button)
        button_box.add_widget(play_button)
        button_box.add_widget(discard_button)
        root_widget.add_widget(button_box)

        # Bind button actions (to be implemented)
        draw_button.bind(on_press=self.draw_card)
        play_button.bind(on_press=self.play_cards)
        discard_button.bind(on_press=self.discard_card)

        if self.player != self.game.getCurrentPlayer():
            draw_button.disabled = True
            play_button.disabled = True
            discard_button.disabled = True
        if self.player == self.game.getCurrentPlayer():
            draw_button.disabled = False
            play_button.disabled = False
            discard_button.disabled = False

        return root_widget

    # Implement button actions here (functions to call corresponding methods from cards.py)
    def draw_card(self, instance, player):
        # Call player.recieveCard(self.deck.drawCard()) and update UI
        player.recieveCard(self.deck.drawCard())

    def play_cards(self, instance, player, cards):
        # Call player related methods to handle playing cards and update UI
        for g in player.getCurrentPhase().goal:
            if player.lay_cards(cards, cards, g):
                return True
            return False

    def discard_card(self, instance, selected_card = None):
        # Call player related methods to handle discarding cards and update UI
        if selected_card == None:
            selected_card = random.choice(self.player.hand.cards)
            selected_card = [selected_card]
        if isinstance(selected_card, list):
            selected_card = selected_card[0]
        #if player.discardCard(player.hand.cards.index(selected_card)):
        if self.player.discardCard(selected_card):
            self.discards.addToStack(selected_card)
        self.currentPlayer = next(self.cycler)

    def turn(self):
        pass



if __name__ == "__main__":
    Phase10App().run()
