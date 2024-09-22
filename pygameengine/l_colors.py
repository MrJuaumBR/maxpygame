from .widgets import *
from .objects import color as reqColor
import requests, json
import random

Git_Colors_JS = 'https://mrjuaumbr.github.io/database/data/colors.json'

# Colors
class Colors:
    aliases:list[str,] = []
    only_native_colors:bool = False
    def __init__(self):
        """
        Some named colors from:
        https://encycolorpedia.com/named
        """
        self.colors_add()
        self.add_colors_from_json()
        print(f'\t - [!] Built in: {self.number_of_colors()} colors')
    
    def get(self, color_name:str) -> reqColor:
        return getattr(self, color_name)
    
    def add_colors_from_json(self):
        if not self.only_native_colors:
            colors = requests.get(Git_Colors_JS)
            succ = self.load_colors_from_json(colors)
            if not succ:
                print('\t\t - [!] Some colors cannot be loaded from online json.')
            # if colors:
            #     colors = colors.json()
            #     for color in colors.keys():
            #         setattr(self, color.upper(), reqColor(*colors[color])) # Default
            # else:
            #     print('\t - [!] Some colors cannot be loaded from online json.')
                
        self.add_aliases()
        
    def load_colors_from_json(self, json_file:dict):
        if type(json_file) == requests.Response:
            try:
                json_file = json_file.json()
            except:
                print('\t - [!] colors cannot be loaded from the provided json.')
                return False
        try:
            colors = json_file
            if colors:
                for color in colors.keys():
                    setattr(self, color.upper(), reqColor(*colors[color])) # Default
                return True # Success
            else:
                print('\t - [!] colors cannot be loaded from the provided json.')
                return False # Error
        except: 
            print('\t - [!] colors cannot be loaded from the provided json.')
            return False # Error
            
    def add_aliases(self):
        colors = self.__dict__.copy()
        for color in colors.keys():
            if type(self.__dict__[color]) == reqColor:
                setattr(self, color.capitalize(), self.__dict__[color])
                setattr(self, color.lower(), self.__dict__[color])
                
                self.aliases.append(color.capitalize())
                self.aliases.append(color.lower())
    
    def colors_add(self):
        # Basic Colors
        self.WHITE = reqColor(255, 255, 255)
        self.BLACK = reqColor(0, 0, 0)
        self.GRAY = reqColor(128, 128, 128)
        self.DARKGRAY = reqColor(64, 64, 64)
        self.LIGHTGRAY = reqColor(192, 192, 192)
        self.BLACK = reqColor(0, 0, 0)
        

        # Red Based Colors
        self.RED = reqColor(255, 0, 0)
        self.LIGHTRED = reqColor(255, 128, 128)
        self.DARKRED = reqColor(128, 0, 0)
        self.BLOODRED = reqColor(0, 0, 0, hex='660000')
        self.BLOOD = reqColor(0, 0, 0, hex='8a0303')
        self.FIREBRICK = reqColor(178, 34, 34)
        

        # Green Based Colors
        self.GREEN = reqColor(0, 255, 0)
        self.LIGHTGREEN = reqColor(128, 255, 128)
        self.DARKGREEN = reqColor(0, 128, 0)
        self.DARKSEAGREEN = reqColor(0,0,0, hex='#8FBC8B')

        # Blue Based Colors
        self.BLUE = reqColor(0, 0, 255)
        self.LIGHTBLUE = reqColor(128, 128, 255)
        self.DARKBLUE = reqColor(0, 0, 128)
        self.METALBLUE = reqColor(64, 64, 192)
        self.SKYBLUE = reqColor(0, 255, 255)
        self.MEDIUMAQUAMARINE = reqColor(0,0,0, hex='#66CDAA')
        self.DODGERBLUE = reqColor(0, 0, 0, hex='#1E90FF')

        # Yellow Based Colors
        self.YELLOW = reqColor(255, 255, 0)
        self.LIGHTYELLOW = reqColor(255, 255, 128)
        self.DARKYELLOW = reqColor(128, 128, 0)

        # Purple Based Colors
        self.PURPLE = reqColor(255, 0, 255)
        self.LIGHTPURPLE = reqColor(255, 128, 255)
        self.DARKPURPLE = reqColor(128, 0, 128)

        # Pink Based Colors
        self.PINK = reqColor(255, 0, 128)
        self.LIGHTPINK = reqColor(255, 128, 255)
        self.DARKPINK = reqColor(128, 0, 255)
        self.HOTPINK = reqColor(0,0,0,hex="FF69B4")
        self.MEDIUMVIOLETRED = reqColor(0, 0, 0, hex="C71585")
        self.PALEVIOLETRED = reqColor(0, 0, 0, hex="DB7093")
        

        # Lime Based Colors
        self.LIME = reqColor(0, 255, 0)
        self.LIGHTLIME = reqColor(128, 255, 128)
        self.DARKLIME = reqColor(0, 128, 0)

        # Brown Based Colors
        self.BROWN = reqColor(128, 64, 0)
        self.LIGHTBROWN = reqColor(192, 128, 64)
        self.DARKBROWN = reqColor(64, 32, 0)

        # Salmon Based Colors
        self.SALMON = reqColor(255, 128, 128)
        self.LIGHTSALMON = reqColor(255, 192, 192)
        self.DARKSALMON = reqColor(192, 64, 64)

        # Orange Based Colors
        self.ORANGE = reqColor(255, 128, 0)
        self.LIGHTORANGE = reqColor(255, 192, 128)
        self.DARKORANGE = reqColor(192, 64, 0)

        # Misc Colors
        self.PEAR = reqColor(128, 255, 128)
        self.ABSOLUTEZERO = reqColor(0, 0, 0,hex='0048ba')
        self.ALUMINUM = reqColor(0,0,0,hex='#d6d6d6')
        self.ALUMINUMFOIL = reqColor(0,0,0,hex='#d2d9db')
        self.ALMOND = reqColor(0,0,0, hex='efdecd')
        self.ANTIFLASH = reqColor(0,0,0, hex='f2f3f4')
        self.BABYPOWDER = reqColor(0,0,0, hex='#fefefa')
        self.BAYSIDE = reqColor(0,0,0, hex='#5fc9bf')
        self.SANDYBROWN = reqColor(0,0,0, hex='#f4a460')
        
    
    def random(self) -> reqColor:
        keys = [key for key in self.__dict__.keys() if type(self.__dict__[key]) == reqColor]
        x = random.choice(keys)
        x = self.__dict__[x]
        return x

    def number_of_colors(self) -> int:
        x = 0
        for color in self.__dict__.keys():
            if color not in self.aliases and type(self.__dict__[color]) == reqColor:
                x += 1
        return x