from kivy.graphics import Rectangle, Line
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.uix.image import Image
from kivy.uix.togglebutton import ToggleButton
from kivy.properties import ObjectProperty, StringProperty, ListProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView 
from kivy.uix.button import Button
from kivy.lang import Builder

from phase10.game.classes.deck import Deck

Builder.load_file("selectable.kv")

class SelectableCard(ToggleButton):
    card = ObjectProperty(None)
    image_source = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #self.size_hint = (None,None)
        self.background_color = ([0,0,0,0])


    def on_card(self, instance, value):
        if self.card:
            self.image_source = self.card.get_image()


    def add_card(self, newcard):
        self.card = newcard


class SelectableHand(ScrollView):
    cards = ListProperty([])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.hand_layout = BoxLayout(orientation='horizontal', spacing=-50, size_hint_y=None)
        self.hand_layout.bind(minimum_width=self.hand_layout.setter('width'))
        self.add_widget(self.hand_layout)

    def update_hand(self, new_cards):
        """Repopulate the hand with a new set of cards."""
        self.cards = new_cards
        self.hand_layout.clear_widgets()
        for card in self.cards:
            selectable_card = SelectableCard(card=card)
            selectable_card.bind(state=self.on_card_selected)
            self.hand_layout.add_widget(selectable_card)

    def on_card_selected(self, instance, state):
        """Update selected cards based on the toggle state of each card."""
        if state == 'down' and instance.card not in self.cards:
            self.cards.append(instance.card)
        elif state == 'normal' and instance.card in self.cards:
            self.cards.remove(instance.card)

    def get_selected_cards(self):
        """Return a list of selected cards."""
        return [card for card in self.cards if card.selected]


class SelectableDeck(Button):
    selectable = BooleanProperty(False)
    deck = ObjectProperty(Deck)

    def create_and_shuffle(self):
        self.deck.create_deck()
        self.deck.shuffle()

    def on_selectable(self, ins, value):
        if value == True:
            self.deck.is_disabled = False
        elif value == False:
            self.deck.is_disabled = True


class SelectableDiscards(Button):
    selectable = BooleanProperty(False)
    discards = ObjectProperty(None)
    image_source = StringProperty("assets/images/empty_slot.png")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(discards=self.on_discards)

    def on_discards(self, instance, discards):
        # Bind to discards' top_card_image property to update image dynamically
        if self.discards:
            self.image_source = self.discards.top_card_image
            self.discards.bind(top_card_image=self.update_image_source)

    def update_image_source(self, instance, value):
        # Called whenever top_card_image changes
        self.image_source = value

    def on_selectable(self, ins, value):
        if value and self.discards and self.discards.can_take_card():
            self.disabled = False
        else:
            self.disabled = True