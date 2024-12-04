from kivy.uix.togglebutton import ToggleButton
from kivy.properties import ObjectProperty, StringProperty, ListProperty, BooleanProperty
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.lang import Builder

from phase10.server.classes.deck import Deck

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
            self.image_source = "../" + self.card.get_image()


    def add_card(self, newcard):
        self.card = newcard


class SelectableHand(ScrollView):
    cards = ListProperty([])            # All cards in the hand
    selected_cards = ListProperty([])    # Currently selected cards
    hand_layout = ObjectProperty(None)      #The root layout(BoxLayout)

    #def __init__(self, **kwargs):
        #super().__init__(**kwargs)

    def update_hand(self, new_cards):
        """Updates the hand display with a new set of cards."""
        # Clear both the displayed widgets and internal tracking lists
        self.cards = new_cards
        self.selected_cards.clear()
        self.hand_layout.clear_widgets()
        # Add each card as a SelectableCard instance to the layout
        selectable_card = None
        for card in self.cards:
            selectable_card = SelectableCard(card=card)
            selectable_card.bind(state=self.on_card_selected)  # Track selection state
            self.hand_layout.add_widget(selectable_card)
        #self.hand_layout.height = selectable_card.height + 50

    def on_card_selected(self, instance, state):
        """Updates the selected cards list based on the card's toggle state."""
        if state == 'down' and instance.card not in self.selected_cards:
            self.selected_cards.append(instance.card)
        elif state == 'normal' and instance.card in self.selected_cards:
            self.selected_cards.remove(instance.card)

    def get_selected_cards(self):
        """Returns the list of currently selected cards."""
        return self.selected_cards


class SelectableDeck(Button):
    selectable = BooleanProperty(False)
    deck = ObjectProperty(Deck)

    def create_and_shuffle(self):
        self.deck.create_deck()
        self.deck.shuffle()

    def on_selectable(self, ins, value):
        if value:
            self.deck.is_disabled = False
        elif not value:
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