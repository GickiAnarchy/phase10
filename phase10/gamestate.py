#!/usr/bin/env python

from game import Game


class GameEngine:
    def __init__(self, game):
        self.game = game

    # Turn Actions
    def player_passes(self, player_id):
        player = self.game.get_player_by_id(player_id)

    def player_discards(self, player_id, card_id):
        player = self.game.get_player_by_id(player_id)
        card = self.game.get_card_by_id(card_id)
        try:
            self.game.discards(player.cards.pop(card))
            return True
        except ValueError as e:
            print(f"Card must not be present\n{e}")
            return False

    def player_draws(self, player, target):
        player = self.game.get_player_by_id(player_id)
        if self.game.active_player != player.name:
            return False
        if isinstance(target, Discards):
            if isinstance(self.game.discards.get_top_card(), Skip):
                return False
            player.add_card(self.game.discards.take_top_card())
        elif isinstance(target, Deck):
            player.add_card(self.game.deck.draw_card())
        return True

    def player_plays(self, player, card_ids, goal_id):
        player = self.game.get_player_by_id(player_id)
        card = self.game.get_card_by_id(card_ids)
        goal = self.game.get_goal_by_id(goal_id)
        if not goal.check_cards(cards):
            return False
        goal.add_cards(cards)
        player.check_phase_condition()
        return True

    def player_uses_skip(self, player_id, card_id, target_id):
        player = self.game.get_player_by_id(player_id)
        target = self.game.get_player_by_id(target_id)
        card = self.game.get_card_by_id(card_id)
        if not target.is_skipped:
            target.toggle_skipped()
        self.game.discards.add_card(player.cards.pop(card))
        return True

    # Serialization
    def save_all(self):
        print(self.game.to_json())


if __name__ == "__main__":
    g = Game()
    ge = GameEngine(g)
    ge.game.add_player(Player("Corey"))
    ge.game.add_player(Player("Korey"))
    ge.game.ready()
    ge.save_all()
