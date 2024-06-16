from .required import *

# Metadata
class Metadata:
    name = "PyGameEngine"
    author = "MrJuaumBR"
    version = "0.1.3"
    description = "A simple pygame engine"
    

# Time
class TimeSys:
    def __init__(self):
        self.time = pg.time.get_ticks()
        
    def f2s(self , fps:int) -> int:
        return int(self.time / fps) # Return how frames to seconds
    
    def s2f(self , seconds:int) -> int:
        return int(seconds*self.time)

# Color
def hex_to_rgb(hex:str) -> tuple[int,int,int]:
    return tuple(int(hex.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(r:int, g:int, b:int) -> str:
    return f'#{r:02x}{g:02x}{b:02x}'

class RGB:
    r:int
    g:int
    b:int
    brightness:float = 0
    def __init__(self, r:int, g:int, b:int):
        self.r = r
        self.g = g
        self.b = b
        self.validate()
    def validate(self):
        if self.r > 255:
            self.r = 255
        if self.r < 0:
            self.r = 0
        if self.g > 255:
            self.g = 255
        if self.g < 0:
            self.g = 0
        if self.b > 255:
            self.b = 255
        if self.b < 0:
            self.b = 0
            
        self.brightness = round((self.r + self.g + self.b) / 765, 3)
        
    def random(self):
        self.r = random.randint(0, 255)
        self.g = random.randint(0, 255)
        self.b = random.randint(0, 255)
        self.validate()
    
    def hex(self) -> str:
        self.validate()
        return rgb_to_hex(self.r, self.g, self.b)
    
    def rgb(self) -> tuple[int,int,int]:
        self.validate()
        return (self.r, self.g, self.b)

class HEX:
    hex:str
    def __init__(self, hex:str):
        self.hex = hex
    
    def hex(self) -> str:
        return self.hex
    
    def rgb(self) -> tuple[int,int,int]:
        return hex_to_rgb(self.hex)
    
class color():
    rgb:RGB
    hex:HEX
    brightness:float = 0
    def __init__(self, r:int, g:int, b:int,hex:str=None):
        if hex is not None:
            self.rgb = RGB(*hex_to_rgb(hex)) # Convert hex to rgb, and validate color(limit > 0 & < 255)
            self.hex = HEX(self.rgb.hex()) # Convert rgb to hex after validating
        else:
            self.rgb = RGB(r, g, b) # Validate color
            self.hex = HEX(self.rgb.hex()) # Convert rgb to hex after validating
        self.brightness = self.rgb.brightness
        
class spritesheet(object):
    """
    Object for spritesheet
    """
    image:pg.Surface
    image_path:str
    engine:object
    def __init__(self, engine,image_path:str):
        """
        Load an image from a path
        
        Parameters:
            path:str
        Returns:
            pg.SurfaceType
        """
        self.image_path = image_path
        self.engine = engine
        try:
            self.image = self.engine.loadImage(image_path).convert()
        except pg.error as message:
            print('Unable to load spritesheet image:', image_path)
            raise SystemExit(message)
        
    def image_at(self, rect:tuple[int,int,int,int], colorkey=None):
        """
        Get the sprite from the spritesheet
        
        x, y, x+offset, y+offset
        
        Parameters:
            rect:tuple[int,int,int,int]
            colorkey:int
        Returns:
            pg.SurfaceType
        """
        image = pg.Surface(rect.size).convert()
        image.blit(self.sheet, (0,0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pg.RLEACCEL)
        return image
    
    def images_at(self, rects:list[tuple[int,int,int,int]], colorkey=None):
        return [self.image_at(rect, colorkey) for rect in rects]