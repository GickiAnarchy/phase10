class Phase10App(App):
    def build(self):
        # ... your existing build method ...

        self.game = GameApp()  # Create a GameApp instance
        self.game.startGame()  # Start the game

        Clock.schedule_interval(self.update_game, 1/60)
        return root_widget

    def update_game(self, dt):
        # Check if it's the current player's turn
        if self.game.current_player == self.player:
            # Handle player's turn
            self.game.turn()
            # Update UI based on game state
            # ...

        # Update other game elements (e.g., discard pile, deck)
        # ...

    def on_draw_button_press(self, instance):
        self.game.draw_card(self.player)
        # Update UI

    def on_play_button_press(self, instance):
        # Handle card selection and playing logic
        # Call self.game.play_cards(self.player, selected_cards)
        # Update UI

    def on_discard_button_press(self, instance):
        self.game.discard_card(self.player)
        # Update UI
