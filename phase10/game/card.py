
import random

from kivy.parser import color_error


class Card:
    count = 0
    def __init__(self, number = None, color = None, is_skip = False, is_wild = False):
        self.number = number
        self.color = color
        self.is_skip = is_skip
        self.is_wild = is_wild
        self.image = self.get_image()
        Card.count += 1
        print(f"{self.get_description()}\n{Card.count} cards created")

    def get_description(self):
        if self.is_wild:
            return "Wild Card"
        elif self.is_skip:
            return "Skip Card"
        else:
            return f"{self.color} {self.number} Card"

    def get_image(self):
        img_path = "assets/images"
        if self.is_wild:
            return f"{img_path}/Wild.png"
        elif self.is_skip:
            return f"{img_path}/Skip.png"
        else:
            return f"{img_path}/{self.color}_{self.number}.png"

    @classmethod
    def get_count(cls):
        return cls.count

    def __eq__(self, other):
        if isinstance(other, int):
            return self.number == other
        if isinstance(other, str):
            return self.color == other
        else:
            return self == other
    def __lt__(self, other):
        if isinstance(other, int):
            return self.number < other
    def __gt__(self, other):
        if isinstance(other, int):
            return self.number > other

class Wild(Card):
    def __init__(self,number = 0, color = "Wild", is_wild = True):
        super().__init__(number,color,False,is_wild)

    def __eq__(self, other):
        if isinstance(other, int):
            return True
        if isinstance(other, str):
            return True
        else:
            return self == other
    def __lt__(self, other):
        if isinstance(other, int):
            return True
    def __gt__(self, other):
        if isinstance(other, int):
            return True

class Skip(Card):
    def __init__(self,number = 0, color = "Skip", is_skip = True):
        super().__init__(number,color,is_skip,False)

    def __eq__(self, other):
        return False
    def __gt__(self, other):
        return False
    def __lt__(self, other):
        return False