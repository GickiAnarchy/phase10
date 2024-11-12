#!/usr/bin/env python


class Card:
    count = 0

    def __init__(self, number=None, color=None, is_skip=False, is_wild=False):
        Card.count += 1
        self.id = Card.count
        self.number = number
        self.color = color
        self.is_skip = is_skip
        self.is_wild = is_wild
        self.image = self.get_image()
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
        try:
            if self.is_wild:
                return f"{img_path}/Wild.png"
            elif self.is_skip:
                return f"{img_path}/Skip.png"
            else:
                return f"{img_path}/{str(self.color).lower()}_{self.number}.png"
        except Exception as e:
            print(e)
            return None

    def point_value(self):
        if self.is_wild or self.is_skip:
            return 25
        if self.number <= 9:
            return 5
        if self.number >= 10:
            return 10

    @classmethod
    def get_count(cls):
        return cls.count

    @property
    def points(self):
        if self.is_wild or self.is_wild:
            return 25
        if self.number >= 10:
            return 10
        if self.number <= 9:
            return 5

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

    def to_dict(self):
        return {"id": self.id,
               "number": self.number,
               "color": self.is_skip,
               "is_skip": self.color,
               "is_wild": self.is_wild,
               "image": self.image}

    @classmethod
    def from_dict(cls, data):
        obj = cls(
            number=data.get("number"),
            color=data.get("color"),
            is_skip=data.get("is_skip"),
            is_wild=data.get("is_wild"),
        )
        obj.id = data.get("id", Card.count)
        return obj


class Wild(Card):
    def __init__(self, number=0, color="Wild", is_wild=True):
        super().__init__(number, color, is_skip=False, is_wild = is_wild)

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
    def __init__(self, number=0, color="Skip", is_skip=True):
        super().__init__(number, color, is_skip, False)

    def __eq__(self, other):
        return False

    def __gt__(self, other):
        return False

    def __lt__(self, other):
        return False

