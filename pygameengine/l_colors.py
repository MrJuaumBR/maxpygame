from .widgets import *
from .objects import color as reqColor
import random

# Colors
class Colors:
    def __init__(self):
        self.colors_add()
        print(f'Built in: {self.number_of_colors()} colors')
    
    def colors_add(self):
        self.WHITE = reqColor(255, 255, 255)
        self.BLACK = reqColor(0, 0, 0)
        self.GRAY = reqColor(128, 128, 128)
        self.DARKGRAY = reqColor(64, 64, 64)
        self.LIGHTGRAY = reqColor(192, 192, 192)
        self.BLACK = reqColor(0, 0, 0)

        self.RED = reqColor(255, 0, 0)
        self.LIGHTRED = reqColor(255, 128, 128)
        self.DARKRED = reqColor(128, 0, 0)

        self.GREEN = reqColor(0, 255, 0)
        self.LIGHTGREEN = reqColor(128, 255, 128)
        self.DARKGREEN = reqColor(0, 128, 0)

        self.BLUE = reqColor(0, 0, 255)
        self.LIGHTBLUE = reqColor(128, 128, 255)
        self.DARKBLUE = reqColor(0, 0, 128)
        self.METALBLUE = reqColor(64, 64, 192)
        self.SKYBLUE = reqColor(0, 255, 255)

        self.YELLOW = reqColor(255, 255, 0)
        self.LIGHTYELLOW = reqColor(255, 255, 128)
        self.DARKYELLOW = reqColor(128, 128, 0)

        self.PURPLE = reqColor(255, 0, 255)
        self.LIGHTPURPLE = reqColor(255, 128, 255)
        self.DARKPURPLE = reqColor(128, 0, 128)

        self.PINK = reqColor(255, 0, 128)
        self.LIGHTPINK = reqColor(255, 128, 255)
        self.DARKPINK = reqColor(128, 0, 255)

        self.LIME = reqColor(0, 255, 0)
        self.LIGHTLIME = reqColor(128, 255, 128)
        self.DARKLIME = reqColor(0, 128, 0)

        self.BROWN = reqColor(128, 64, 0)
        self.LIGHTBROWN = reqColor(192, 128, 64)
        self.DARKBROWN = reqColor(64, 32, 0)

        self.SALMON = reqColor(255, 128, 128)
        self.LIGHTSALMON = reqColor(255, 192, 192)
        self.DARKSALMON = reqColor(192, 64, 64)

        self.ORANGE = reqColor(255, 128, 0)
        self.LIGHTORANGE = reqColor(255, 192, 128)
        self.DARKORANGE = reqColor(192, 64, 0)

        self.PEAR = reqColor(128, 255, 128)
    
    def random(self) -> reqColor:
        x = random.choice(self.__dict__.keys())
        x = self.__dict__[x]
        return x

    def number_of_colors(self) -> int:
        return len(self.__dict__.keys())