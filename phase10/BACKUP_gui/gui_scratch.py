"""This is a collection of Kivy GUI classes that isn't implemented yet, or has been discarded"""
from kivy.core.image import Image
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton

from phase10.game.classes.deck import Deck
from phase10.game.classes.discards import Discards


class SelectableCard(ToggleButton):
    """Card displays as a button"""
    def __init__(self, card, **kwargs):
        super().__init__(**kwargs)
        self.card = card
        self.source = card.get_image()
        self.background_color = (1, 1, 1, 1)
        self.size_hint = (None, None)
        self.size = (73, 150)
        with self.canvas.before:
            self.border_color = Color(1, 0, 0, 1)  # Red border
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
    """ A players hand as a collection
        of SelectableCards """
    def __init__(self, hand:list, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.spacing = 10
        self.hand = hand
        self.update_hand()

    def update_hand(self):
        self.clear_widgets()
        for card in self.hand:
            self.add_widget(SelectableCard(card))

    def get_selected_cards(self) -> list:
        return [widget.card for widget in self.children if widget.state == 'down']

    def isPressed(self) -> bool:
        return len(self.get_selected_cards()) > 0


class SelectableDeck(ToggleButton):
    def __init__(self, deck: Deck, **kwargs):
        super().__init__(**kwargs)
        self.deck = deck
        self.background_normal = Image(source = "images/CardBack.png")
        self.background_color = (1, 1, 1, 1)  # White background
        self.size_hint = (None, None)
        self.size = (73, 150)
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

    def isPressed(self) -> bool:
        if self.state == "down":
            return True
        else:
            return False

class SelectableDiscards(ToggleButton):
    def __init__(self, discards: Discards, **kwargs):
        super().__init__(**kwargs)
        self.discards = discards
        self.background_normal = Image(source = "images/CardBack.png")
        self.background_color = (1, 1, 1, 1)  # White background
        self.size_hint = (None, None)
        self.size = (73, 150)
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

    def isPressed(self) -> bool:
        if self.state == "down":
            return True
        else:
            return False


from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.properties import ListProperty, OptionProperty, StringProperty
from kivy.uix.behaviors import ToggleButtonBehavior


class ImageToggleButton(ToggleButtonBehavior, Image):
    """Image toggle button widget for kivy"""
    # toggle_type : what does change when state changes (color, source or both)
    toggle_type = OptionProperty('color', options=['color', 'source', 'both'])
    # color_down : color when state is down
    color_down = ListProperty([0.22, 0.79, 1, 1])
    # color_normal : color when state is normal
    color_normal = ListProperty([0.05, 0.175, 0.225, 1])
    # source_down : image source when state is down
    source_down = StringProperty('')
    # source_normal : image source when state is normal
    source_normal = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # force setting according to normal state
        self.on_state(None, 'normal')

    def on_state(self, instance, state):
        if state == 'down':
            if self.toggle_type == 'color' or self.toggle_type == 'both':
                self.color = self.color_down
            if self.toggle_type == 'source' or self.toggle_type == 'both':
                self.source = self.source_down
        else:  # state=='normal'
            if self.toggle_type == 'source' or self.toggle_type == 'both':
                self.source = self.source_normal
            if self.toggle_type == 'color' or self.toggle_type == 'both':
                self.color = self.color_normal

    def on_source_down(self, instance, src):
        if self.state == 'down' and (self.toggle_type == 'source' or self.toggle_type == 'both'):
            self.source = self.source_down

    def on_source_normal(self, instance, src):
        if self.state == 'normal' and (self.toggle_type == 'source' or self.toggle_type == 'both'):
            self.source = self.source_normal

    def on_color_down(self, instance, clr):
        if self.state == 'down' and (self.toggle_type == 'color' or self.toggle_type == 'both'):
            self.color = self.color_down

    def on_color_normal(self, instance, clr):
        if self.state == 'normal' and (self.toggle_type == 'color' or self.toggle_type == 'both'):
            self.color = self.color_normal

    def on_toggle_type(self, instance, tp):
        if tp == 'source':
            # set color to white when toggle_type = 'source'
            self.color = [1, 1, 1, 1]


# example to demonstrate imagetogglebutton widget capabilities
if __name__ == '__main__':
    from kivy.app import App
    from kivy.clock import Clock
    from kivy.lang.builder import Builder
    from kivy.uix.boxlayout import BoxLayout

    kvstr = """
BoxLayout:
    orientation: 'vertical'
    padding: 20
    Label:
        text: 'shapes'
    BoxLayout:
        orientation: 'horizontal'
        spacing: 20
        padding: 30
        ImageToggleButton:
            id: imgtggl_basicdisc
            source: 'shapes/basic_disc.png'
        ImageToggleButton:
            id: imgtggl_basicsquare
            source: 'shapes/basic_square.png'
        ImageToggleButton:
            id: imgtggl_basicsquarerounded
            source: 'shapes/basic_squarerounded.png'
        ImageToggleButton:
            id: imgtggl_contourdisc
            source: 'shapes/contour_disc.png'
        ImageToggleButton:
            id: imgtggl_contoursquare
            source: 'shapes/contour_square.png'
        ImageToggleButton:
            id: imgtggl_contoursquarerounded
            source: 'shapes/contour_squarerounded.png'
    Label:
        text: 'features'
    BoxLayout:
        orientation: 'horizontal'
        BoxLayout:
            orientation: 'vertical'
            Label:
                text: 'toggle_type=color (default)'
            ImageToggleButton:
                id: imgtggl_typecolor
                source: 'shapes/basic_disc.png'
                color_normal: [1,0,0,1]
                color_down: [0,1,0,1]
        BoxLayout:
            orientation: 'vertical'
            Label:
                text: 'toggle_type=source'
            ImageToggleButton:
                id: led_typesource
                toggle_type: 'source'
                source_down: 'media/yes.png'
                source_normal: 'media/no.png'
        BoxLayout:
            orientation: 'vertical'
            Label:
                text: 'toggle_type=both'
            ImageToggleButton:
                id: imgtggl_typeboth
                toggle_type: 'both'
                source_down: 'shapes/basic_disc.png'
                source_normal: 'shapes/basic_square.png'
                color_normal: [1,0,0,1]
                color_down: [0,1,0,1]
        BoxLayout:
            orientation: 'vertical'
            Label:
                text: 'with animated image'
            ImageToggleButton:
                id: imgtggl_animated
                toggle_type: 'both'
                source_down: 'media/fan.zip'
                source_normal: 'media/fan.png'"""


    class ImgToggleApp(App):
        def build(self):
            w = Builder.load_string(kvstr)
            return w



class SelectableCard3(ToggleButton):
    # card_image : Image widget in button
    card_image = ObjectProperty(Image)
    # color_down : color when state is down
    color_down = ListProperty([1,0,0,0])
    # color_normal : color when state is normal
    color_normal = ListProperty([1,0,0,1])
    #img = Card image string for the button
    img = StringProperty("assets/images/empty_slot.png")
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.card = None
        self.card_image.source = self.img
        with self.canvas.before:
            self.border_color = self.color_normal
            self.border = 0,1,0,1
        #self.bind(state=self.update_border)

    def add_card(self, newcard):
        if not isinstance(newcard, Card):
            print("ERROR: add_card() needs arg type Card")
            return
        else:
            self.card = newcard
            self.img = self.card.get_image()
            self.background_normal = self.img
            print(self.card.get_description())

    def update_border(self, *args):
        print(f"Texture size: {self.card_image.texture_size}")
        self.size = self.card_image.texture_size
        if self.state == 'down':
            self.border_color = self.color_down
        else:
            self.border_color = self.color_normal


class SelectableCard2(ToggleButtonBehavior, Image):
    """Selectable Card Widget for Phase 10"""
    # color_down : color when state is down
    color_down = ListProperty([0.22, 0.79, 1, 1])
    # color_normal : color when state is normal
    color_normal = ListProperty([0.05, 0.175, 0.225, 1])
    # source_down : image source when state is down
    source_down = StringProperty('')
    # source_normal : image source when state is normal
    source_normal = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.on_state(None, 'normal')
        self.source = "assets/images/empty_slot.png"
        self.color = self.color_normal
        self.card = None
        with self.canvas.before:
            self.border_color = self.color_normal
            self.border = Rectangle(pos=self.pos, size=self.size)

    def on_color_down(self, instance, clr):
        if self.state == 'down' and (self.toggle_type == 'color' or self.toggle_type == 'both'):
            self.color = self.color_down

    def on_color_normal(self, instance, clr):
        if self.state == 'normal' and (self.toggle_type == 'color' or self.toggle_type == 'both'):
            self.color = self.color_normal

    def on_state(self, instance, state):
        if state == 'down':
            if self.toggle_type == 'color' or self.toggle_type == 'both':
                self.color = self.color_down
            if self.toggle_type == 'source' or self.toggle_type == 'both':
                self.source = self.source_down
        else:  # state=='normal'
            if self.toggle_type == 'source' or self.toggle_type == 'both':
                self.source = self.source_normal
            if self.toggle_type == 'color' or self.toggle_type == 'both':
                self.color = self.color_normal

    def add_card(self, card):
        print(self.texture)
        if isinstance(card, Card):
            self.source = card.get_image()
        else:
            self.source = "assets/images/empty_slot.png"

    def on_state(self, instance, state):
        if state == 'down':
            self.border_color = self.color_down
        else:
            self.border_color = self.color_normal



#####################################
from kivy.graphics import Rectangle, Color, BorderImage
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.properties import ListProperty, OptionProperty, StringProperty, ObjectProperty, ColorProperty
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.uix.togglebutton import ToggleButton
from kivy.graphics import Line, Color

from phase10.game.classes.card import Card


class SelectableCard(ToggleButtonBehavior, Image):
    card = ObjectProperty(None)
    selected_color = ColorProperty([1, 0, 0, 1])  # Red color for selected border
    normal_color = ColorProperty([1, 1, 1, 1])  # White color for normal border

    def __init__(self, card=None, **kwargs):
        super().__init__(**kwargs)
        self.card = card
        self.selected_color = ([1,0,0,1])
        #Clock.schedule_once(self._update_border, 0)

        # Instruction to draw the border
        with self.canvas:
            self.border_color = Color(*self.selected_color)  # Unpack color tuple
            self.border = Line(rectangle=(self.x, self.y, self.width, self.height), width=3)

    def add_card(self, new_card: Card):
        self.card = new_card
        self.source = self.card.get_image()

    def on_card(self, *args):
        print(f"Card has been changed to {self.card.get_description()}")

    '''def _update_border(self, *args):
        self.border.size = self.size
        self.border.pos = self.pos'''

    def on_press(self):
        self._toggle_border()

    def _toggle_border(self):
        # Method to toggle the border color
        if self.state == "down":
            self.border_color.rgb = self.selected_color
        else:
            self.border_color.rgb = (1, 1, 1)  # Default color (white)

