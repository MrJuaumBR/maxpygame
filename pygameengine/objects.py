from .required import *

# Metadata
class Metadata:
    name = "PyGameEngine"
    author = "MrJuaumBR"
    version = "0.2.7"
    description = "A simple pygame engine"
    github = "https://github.com/MrJuaumBR/maxpygame"
    testpypi = "https://test.pypi.org/project/maxpygame/"
    def splitver(self) -> str:
        x = ''
        for number in self.version.split("."): x += str(number)
        return x
    def splitver2int(self) -> int:
        x = self.splitver()
        return int(x)

class Icon:
    """
    The engine icon when not initialized.
    """
    surf:pg.Surface
    size:tuple[int,int]
    default_size = (128,128)
    ratio:float = 1
    engine:any
    def __init__(self,engine, size:tuple[int,int]=(128,128)):
        """
        The engine icon initialized and drawned, ready for be used.
        """
        self.size = size
        self.ratio = (self.size[0]/self.default_size[0] + self.size[1]/self.default_size[1])/2
        self.surf = pg.Surface(size)
        self.engine = engine
        
        self.surf.fill(self.engine.Colors.WHITE.rgb)
        
        green_color = color(1, 248, 107)
        yellow_color = color(247, 249, 0)
        blue_color = color(0, 122, 204)
        
        # Draw Background w/ Border
        self.engine.draw_rect((0,0), [size[0]-int(5*self.ratio),size[1]-int(5*self.ratio)], self.engine.Colors.WHITE,
                              border_width=int(5*self.ratio), border_color=self.engine.Colors.BROWN, screen=self.surf)
        
            # Console Bg
        self.engine.draw_rect((int(20*self.ratio), int(20*self.ratio)), (int(88*self.ratio), int(88*self.ratio)), self.engine.Colors.DARKGRAY,
                              border_width=int(3*self.ratio), border_color=self.engine.Colors.GRAY, screen=self.surf)
            # Console Topbar
        self.engine.draw_rect((int(17*self.ratio),int(19*self.ratio)), (int(94*self.ratio),int(20*self.ratio)), blue_color,
                              screen=self.surf)
        
        
        # Draw Green Part
        self.engine.draw_rect((int(25*self.ratio), int(45*self.ratio)), (int(70*self.ratio),int(10*self.ratio)), green_color,
                              screen=self.surf)
        
        self.engine.draw_rect((int(45*self.ratio), int(69*self.ratio)), (int(40*self.ratio),int(10*self.ratio)), green_color,
                              screen=self.surf)
        
        # Draw Yellow Part
        self.engine.draw_rect((int(25*self.ratio), int(57*self.ratio)), (int(60*self.ratio),int(10*self.ratio)), yellow_color,
                              screen=self.surf)
        
        self.engine.draw_rect((int(25*self.ratio), int(81*self.ratio)), (int(70*self.ratio),int(10*self.ratio)), yellow_color,
                              screen=self.surf)
        
        for x in range(3):
            i = x + 1
            c = green_color if x%2 == 0 else yellow_color
            self.engine.draw_rect((int((25*i)*self.ratio), int(93*self.ratio)), (int(19*self.ratio),int(10*self.ratio)), c,
                              screen=self.surf)
# Mouse Object
class Mouse:
    _x:int = 0
    _y:int = 0
    pos:tuple[int,int] = (_x, _y)
    scroll:float = 0
    
    left:bool = False
    middle:bool = False
    right:bool = False
    
    # 5 buttons
    button_4:bool = False
    button_5:bool = False
    
    # Scroll Smooth
    smooth_scroll:bool = True
    smooth_scroll_delay:int = 0 # frames to wait
    non_smooth_delay:int = 0.16 # seconds
    loss_speed:int = 80
    
    engine:object
    def __init__(self, engine):
        self.engine = engine
    
    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, value):
        self._x = value
        self.pos = (self._x, self._y)
        
    @property
    def y(self):
        return self._y
    
    @y.setter
    def y(self, value):
        self._y = value
        self.pos = (self._x, self._y)
    
    def scroll_detector(self, scroll_event:pg.event.EventType):
        self.scroll = scroll_event.y
    
    def scroll_slow_down(self):
        if (self.scroll < 0 or self.scroll > 0) and self.smooth_scroll:
            self.scroll *= self.loss_speed/100 # xx% Loss Speed
            self.scroll = round(self.scroll, 4)
            if abs(self.scroll) < 0.085:
                self.scroll = 0
        elif not self.smooth_scroll:
            if self.smooth_scroll_delay <= 0:
                self.scroll = 0
                self.smooth_scroll_delay = self.engine.TimeSys.s2f(self.non_smooth_delay)
    
    def update(self):
        if self.smooth_scroll_delay > 0:
            self.smooth_scroll_delay -= 1
        
        self.x, self.y = self.engine.getMousePos()
        buttons:list[bool,] = self.engine.getMousePressed(5)
        self.left, self.middle, self.right = buttons[0], buttons[1], buttons[2]
        if len(buttons) > 3:
            self.button_4 = buttons[3]
            self.button_5 = buttons[4]
        else:
            self.button_4 = False
            self.button_5 = False

# Time
class TTimeSys:
    unstable_fps:bool = False
    def __init__(self, engine):
        self.engine = engine
        self.fps = engine.fps
    
    def s2f(self , seconds:int) -> int:
        """
        How frames will run in a second
        
        Transform Seconds to Frames
        
        * Now Supports unstable_fps
        """
        if self.unstable_fps:
            x = round(self.engine._rfps / self.fps,2)
            return int((x*self.fps)*seconds)
        else: return int(seconds*self.fps)
        
    def f2s(self, frames:int) -> int:
        """
        How seconds will run in a frame
        
        Transform Frames to Seconds
        
        * Now Supports unstable_fps
        """
        if self.unstable_fps:
            x = round(self.engine._rfps / self.fps,2)
            return int(frames * x)
        else: return int(frames / self.fps)

# Color
def hex_to_rgb(hex:str) -> tuple[int,int,int]:
    return tuple(int(hex.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(r:int, g:int, b:int) -> str:
    return f'#{r:02x}{g:02x}{b:02x}'

# Input Query
class InputQuery:
    """
    InputQuery System
    """
    engine:object
    _query:list[int,] = [] #Each value inside of the query is a int that represents the key
    last_change:float = 0.0 # Represents the delta time that the query was last changed
    query_limit:int = 12 # The limit of keys into the query
    def __init__(self,engine):
        self.engine = engine
    
    def insert_query(self, key:int):
        """
        This function will insert a key into the query
        
        Parameters:
            key (int): The key to insert
        
        Returns:
            None
        """
        self._query.append(key)
        self.last_change = self.engine.delta_time.total_seconds()
    
    def GetQuery(self) -> list[(int,int),]:
        """
        This function will return a list of tuples
        The first value is the index of the key
        The second value is the key
        
        Parameters:
            None
        
        Returns:
            list[(int,int),]: A list of tuples
        """
        q = []
        for index, key in enumerate(self._query):
            q.append((index,key))
        return q
    
    def update(self, delta_time:timedelta):
        """
        This function will update the query
        
        Parameters:
            delta_time (timedelta): The delta time
        
        Returns:
            None
        """
        dt = delta_time.total_seconds()
        if dt-self.last_change > 1 and len(self._query) > 0:
            self._query.pop(0)
            self.last_change = dt-0.875
        else:
            if len(self._query) > self.query_limit:
                self._query.pop(0) # Removes the older key

def humanize_seconds(seconds:int) -> dict:
    """
    This command will humanize seconds
    Like: Days, Hours, Minutes, Seconds
    """
    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return {'days':days, 'hours':hours, 'minutes':minutes, 'seconds':seconds}

class RGB:
    _r:int = 0
    _g:int = 0
    _b:int = 0
    brightness:float = 0
    def __init__(self, r:int, g:int, b:int):
        self.r = r
        self.g = g
        self.b = b
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

    @property
    def r(self):
        return self._r
    
    @r.setter
    def r(self, r:int):
        self._r = r
        self.validate()
    
    @property
    def g(self):
        return self._g
    
    @g.setter
    def g(self, g:int):
        self._g = g
        self.validate()
    
    @property
    def b(self):
        return self._b
    
    @b.setter
    def b(self, b:int):
        self._b = b
        self.validate()
    
    def random(self):
        self.r = random.randint(0, 255)
        self.g = random.randint(0, 255)
        self.b = random.randint(0, 255)
    
    def hex(self) -> str:
        self.validate()
        return rgb_to_hex(self.r, self.g, self.b)
    
    def rgb(self) -> tuple[int,int,int]:
        self.validate()
        return (self.r, self.g, self.b)
    
    def setRGB(self, rgb:tuple[int,int,int]):
        self.r = rgb[0]
        self.g = rgb[1]
        self.b = rgb[2]

class HEX:
    _hex:str
    def __init__(self, hex:str):
        self.hex = hex
    
    @property
    def hex(self) -> str:
        return self._hex
    
    @hex.setter
    def hex(self, hex:str):
        self._hex = hex
    
    def ghex(self) -> str:
        return self.hex
    
    def rgb(self) -> tuple[int,int,int]:
        return hex_to_rgb(self.hex)
    
class color():
    _rgb:RGB
    _hex:HEX
    brightness:float = 0
    def __init__(self, r:int, g:int, b:int,hex:str=None):
        if hex is not None:
            self._rgb = RGB(*hex_to_rgb(hex)) # Convert hex to rgb, and validate color(limit > 0 & < 255)
            self._hex = HEX(self._rgb.hex()) # Convert rgb to hex after validating
        else:
            self._rgb = RGB(r, g, b) # Validate color
            self._hex = HEX(self._rgb.hex()) # Convert rgb to hex after validating
        self.brightness = self._rgb.brightness
    
    @property
    def rgb(self) -> RGB:
        return self._rgb
    
    @rgb.setter
    def rgb(self, rgb:tuple[int,int,int]):
        r,g,b = rgb
        self._rgb = RGB(r, g, b) # Validate color
        self._hex = HEX(self._rgb.hex()) # Convert rgb to hex after validating
        self.brightness = self._rgb.brightness
        
    @rgb.getter
    def rgb(self) -> tuple[int,int,int]:
        return self._rgb.rgb()
    
    @property
    def hex(self) -> HEX:
        return self._hex
    
    @hex.setter
    def hex(self, hex:str):
        self._rgb = RGB(*hex_to_rgb(hex)) # Convert hex to rgb, and validate color(limit > 0 & < 255)
        self._hex = HEX(self._rgb.hex()) # Convert rgb to hex after validating
        self.brightness = self._rgb.brightness
        
    @hex.getter
    def hex(self) -> str:
        return self._hex.ghex()
        
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
        image.blit(self.image, (0,0), rect)
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pg.RLEACCEL)
        return image
    
    def images_at(self, rects:list[tuple[int,int,int,int]], colorkey=None):
        return [self.image_at(rect, colorkey) for rect in rects]
    
class cfgtimes:
    """
    settings the delay time for the engine
    """
    
    # Widgets
    WD_BTN_CLICK_TIME = 0.1 # Default -> 0.1s
    WD_CKBX_CLICK_TIME = 0.35 # Default -> 0.35s
    WD_SLCT_CLICK_TIME = 0.45 # Default -> 0.45s
    WD_TXBX_DEL_TIME = 0.2 # Default -> 0.2s
    WD_TXBX_KEYP_TIME = 0.075 # Default -> 0.075s
    WD_TXBX_CLICK_TIME = 0.15 # Default -> 0.15s
    WD_DPDW_UPDATE_TIME = 0.07 # Default -> 0.07s
    WD_DPDW_CLICK_TIME = 0.45 # Default -> 0.45s
    
class cfgtips:
    """
    settings for the tips
    """
    
    mouse_distance:tuple[int,int] = (10,10)
    
    background_color:color = color(255,192,128)
    border_color:color = color(192, 128, 64)
    text_color:color = color(0,0,0)
    border_width:int = 2
    alpha:int = 200
    refresh_time = 0.05 # Default -> 0.05s