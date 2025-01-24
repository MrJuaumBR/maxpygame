from .required import *

# Metadata
_version = "0.3.4"
class Metadata:
    name = "PyGameEngine"
    author = "MrJuaumBR"
    version = _version
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
                              border_width=int(5*self.ratio), border_color=self.engine.Colors.BROWN, surface=self.surf)
        
            # Console Bg
        self.engine.draw_rect((int(20*self.ratio), int(20*self.ratio)), (int(88*self.ratio), int(88*self.ratio)), self.engine.Colors.DARKGRAY,
                              border_width=int(3*self.ratio), border_color=self.engine.Colors.GRAY, surface=self.surf)
            # Console Topbar
        self.engine.draw_rect((int(17*self.ratio),int(19*self.ratio)), (int(94*self.ratio),int(20*self.ratio)), blue_color,
                              surface=self.surf)
        
        
        # Draw Green Part
        self.engine.draw_rect((int(25*self.ratio), int(45*self.ratio)), (int(70*self.ratio),int(10*self.ratio)), green_color,
                              surface=self.surf)
        
        self.engine.draw_rect((int(45*self.ratio), int(69*self.ratio)), (int(40*self.ratio),int(10*self.ratio)), green_color,
                              surface=self.surf)
        
        # Draw Yellow Part
        self.engine.draw_rect((int(25*self.ratio), int(57*self.ratio)), (int(60*self.ratio),int(10*self.ratio)), yellow_color,
                              surface=self.surf)
        
        self.engine.draw_rect((int(25*self.ratio), int(81*self.ratio)), (int(70*self.ratio),int(10*self.ratio)), yellow_color,
                              surface=self.surf)
        
        for x in range(3):
            i = x + 1
            c = green_color if x%2 == 0 else yellow_color
            self.engine.draw_rect((int((25*i)*self.ratio), int(93*self.ratio)), (int(19*self.ratio),int(10*self.ratio)), c,
                              surface=self.surf)
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
    
    def insert_query(self, event:pg.event.EventType):
        """
        This function will insert a key into the query
        
        Parameters:
            key (int): The key to insert
        
        Returns:
            None
        """
        self._query.append((event, event.key))
        self.last_change = self.engine.delta_time.total_seconds()
    
    def HasKey(self, key:int) -> bool:
        """
        This function will check if a key is in the query
        
        Parameters:
            key (int): The key to check
        
        Returns:
            bool: True if the key is in the query, False if not
        """
        for value in self._query:
            if value[1] == key:
                return True
        return False
    
    def HasKeyIndex(self, key:int) -> int:
        """
        This function will return the index of a key in the query
        
        Parameters:
            key (int): The key to check
        
        Returns:
            int: The index of the key in the query
        """
        for index, value in enumerate(self._query):
            if value[1] == key:
                return index
        return None
    
    def GetQuery(self) -> list[(int,int, pg.event.EventType),]:
        """
        This function will return a list of tuples\n
        * The first value is the index of the key\n
        * The second value is the key\n
        * The third value is the event\n
        
        Parameters:
            None
        
        Returns:
            list[(int,int),]: A list of tuples
        """
        q = []
        for index, value in enumerate(self._query):
            event, key = value
            q.append((index,key,event))
        return q
    
    def RemoveFromQueryByKey(self, key:int):
        """
        This function will remove the first time a key appears in the query
        
        Parameters:
            key (int): The key to remove
        
        Returns:
            None
        """
        if self.HasKey(key):
            index = self.HasKeyIndex(key)
            self.RemoveFromQuery(index)
        else:
            print(f'Key {self.engine.keyToString(key)}({key}) not found in query')

    
    def RemoveFromQuery(self, index:int):
        """
        This function will remove a key from the query
        
        Parameters:
            index (int): The index of the key to remove
        
        Returns:
            None
        """
        try:
            self._query.pop(index)
        except Exception as ex:
            print(f'Index {index} not found in query')
    
    def update(self, delta_time:timedelta):
        """
        This function will update the query
        
        Parameters:
            delta_time (timedelta): The delta time
        
        Returns:
            None
        """
        dt = delta_time.total_seconds()
        if self._query and (dt - self.last_change > 1 or len(self._query) > self.query_limit):
            self._query.pop(0)
            self.last_change = dt - 0.875

class VideoInfo:
    """
    Just a way to connect things to:
    pygame.display._VidInfo
    """
    hw: int
    wm: int
    video_mem: int
    bitsize: int
    bytesize: int
    masks: tuple[int,int,int,int]
    shifts: tuple[int,int,int,int]
    losses: tuple[int,int,int,int]
    blit_hw: int
    blit_hw_CC: int
    blit_hw_A: int
    blit_sw: int
    blit_sw_CC: int
    blit_sw_A: int
    current_h: int
    current_w: int

def humanize_seconds(seconds:int) -> dict:
    """
    This command will humanize seconds
    Like: Days, Hours, Minutes, Seconds
    """
    s, ms = divmod(seconds, 1000)
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    return {'days':d, 'hours':h, 'minutes':m, 'seconds':s}

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
        return self.rgb()
    
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
    
    def random(self) -> RGB:
        """
        Generate a random color based on RGB Values
        
        Parameters:
            None
        Returns:
            RGB
        """
        
        x = RGB(0,0,0)
        x.random()
        self._rgb = x # Validate color
        self._hex = HEX(self._rgb.hex()) # Convert rgb to hex after validating
        self.brightness = self._rgb.brightness
        return self._rgb.rgb()
    
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
            self.image = pg.image.load(image_path).convert_alpha()
        except pg.error as message:
            print('Unable to load spritesheet image:', image_path)
            raise SystemExit(str(message))
        
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
        image = pg.Surface(rect.size, pg.SRCALPHA)
        image.blit(self.image, (0,0), rect)
        if colorkey is not None:
            image.set_colorkey(colorkey, pg.RLEACCEL)
        return image
    
    def images_at(self, rects:list[tuple[int,int,int,int]], colorkey=None):
        return [self.image_at(rect, colorkey) for rect in rects]

# Controller Object Identification

JOYSTICK_A_BUTTON = 0
JOYSTICK_B_BUTTON = 1
JOYSTICK_X_BUTTON = 2
JOYSTICK_Y_BUTTON = 3
JOYSTICK_LEFT_BUTTON = 4
JOYSTICK_RIGHT_BUTTON = 5
JOYSTICK_BACK_BUTTON = 6
JOYSTICK_START_BUTTON = 7
JOYSTICK_HOME = 10

JOYSTICK_LEFT_AXIS_X = 0
JOYSTICK_LEFT_AXIS_Y = 1
JOYSTICK_RIGHT_AXIS_X = 2
JOYSTICK_RIGHT_AXIS_Y = 3


JOYSTICK_LEFT_AXIS_PRESS = 8
JOYSTICK_RIGHT_AXIS_PRESS = 9

JOYSTICK_LEFT_TRIGGER = 4
JOYSTICK_RIGHT_TRIGGER = 5
# Aliases
JOYSTICK_LB = JOYSTICK_LEFT_BUTTON
JOYSTICK_RB = JOYSTICK_RIGHT_BUTTON
JOYSTICK_SHARE_BUTTON = JOYSTICK_BACK_BUTTON
JOYSTICK_OPTIONS_BUTTON = JOYSTICK_START_BUTTON
JOYSTICK_LT = JOYSTICK_LEFT_TRIGGER
JOYSTICK_RT = JOYSTICK_RIGHT_TRIGGER

class Controller():
    joystick:pg.joystick.JoystickType
    engine:object
    mouse_emulate:bool = False
    
    # Loaded from Handler
    joystick_mouse_speed:float
    joystick_mouse_axis:str
    joystick_trigger_mouse_button:str
    joystick_mouse_wheel_button:str
    joystick_mouse_axis_slower_button:str
    def __init__(self,id:int, Handler:object) -> pg.joystick.JoystickType:
        self.id = id
        self.engine = Handler.engine
        
        # Load Config from Handler
        self.joystick_mouse_speed = Handler.joystick_mouse_speed
        self.joystick_mouse_axis = Handler.joystick_mouse_axis
        self.joystick_trigger_mouse_button = Handler.joystick_trigger_mouse_button
        self.joystick_mouse_wheel_button = Handler.joystick_mouse_wheel_button
        self.joystick_mouse_axis_slower_button = Handler.joystick_mouse_axis_slower_button
        
        self.loadJoystickFromPygame()
        
    def loadJoystickFromPygame(self):
        """
        This function gonna get all function from pygame.joystick.Joystick
        and put them in this object
        
        You can still access the original object by using <this object>.joystick
        """
        self.joystick:pg.joystick.JoystickType = pg.joystick.Joystick(self.id)
        
        for name, __ in inspect.getmembers(self.joystick):
            if callable(getattr(self.joystick, name)) and not name.startswith('_'):
                setattr(self, name, getattr(self.joystick, name))
                
    
    def allButtons(self) -> dict:
        """
        Get All Buttons(Based on Xbox Controller)
        """
        buttons_name = [
            'a','b','x','y','lb','rb','back','start','rt','lt','dpad',
            'left_press','right_press'
        ]
        
        buttons = {}
        for button in buttons_name:
            buttons[button] = self.getButtonByString(button)
            
        return buttons
    
    def getButtonByString(self, name:str) -> bool:
        """
        Get Any Button of Controller By Using the name of button
        
        Parameters:
            name:str
        Returns:
            bool
        """
        name = str(name).lower()
        
        

        if name in ['cross','a']:
            return self.getButtonById(JOYSTICK_A_BUTTON)
        elif name in ['circle','b']:
            return self.getButtonById(JOYSTICK_B_BUTTON)
        elif name in ['square','x']:
            return self.getButtonById(JOYSTICK_X_BUTTON)
        elif name in ['triangle','y']:
            return self.getButtonById(JOYSTICK_Y_BUTTON)
        elif name in ['left','lb']:
            return self.getButtonById(JOYSTICK_LEFT_BUTTON)
        elif name in ['right','rb']:
            return self.getButtonById(JOYSTICK_RIGHT_BUTTON)
        elif name in ['back','share']:
            return self.getButtonById(JOYSTICK_BACK_BUTTON)
        elif name in ['start','options']:
            return self.getButtonById(JOYSTICK_START_BUTTON)
        elif name in ['left_trigger','lt']:
            return True if self.get_axis(JOYSTICK_LEFT_TRIGGER) > 0 else False
        elif name in ['right_trigger','rt']:
            return True if self.get_axis(JOYSTICK_RIGHT_TRIGGER) > 0 else False
        elif name in ['dpad','directions']:
            return self.dpad_as_buttons(dual=True)
        elif name in ['left_press','left_axis_press']:
            return self.getButtonById(JOYSTICK_LEFT_AXIS_PRESS)
        elif name in ['right_press','right_axis_press']:
            return self.getButtonById(JOYSTICK_RIGHT_AXIS_PRESS)
        else:
            return False
    
    def dpad_as_buttons(self, dual:bool=True) -> str or tuple[str,str]: # type: ignore
        """
        Return Dpad as buttons
        
        If Dual False then this will return just one axis, if Dual True then this will return two axis
        
        Parameters:
            dual:bool(Optional)
        Returns:
            str if Dual = False
            tuple[str,str] if Dual = True
        """
        dpad = self.getDPad()
        
        if dual:
            x = 'right' if dpad[0] > 0 else 'left' if dpad[0] < 0 else ''
            y = 'up' if dpad[1] > 0 else 'down' if dpad[1] < 0 else ''
            return (x,y)
        else:
            return {
                (-1, 0): 'left',
                (1, 0): 'right',
                (0, -1): 'down',
                (0, 1): 'up'
            }.get(dpad, '')
    
    def getDPad(self) -> tuple[int,int]:
        """
        Returns DPad Info
        
        X Axis
        -1 = Left
        0 = Center
        1 = Right
        
        Y Axis
        -1 = Up
        0 = Center
        1 = Down
        
        Parameters:
            None
        Returns:
            tuple[int,int] both beetween -1 and 1 when 0 = center
        """
        dpad = self.get_hat(0)
        return dpad
        
    def _emulate_mouse(self):
        """
        Emulate Mouse with Controller/Joystick
        
        * Mouse Movement
        * Mouse Click (Left)
        * Mouse Scroll
        
        Parameters:
            None
        Returns:
            None
        """
        axis = self.getAxisByString(self.joystick_mouse_axis)
        if self.mouse_emulate:
            if self.getButtonByString(self.joystick_trigger_mouse_button):
                self.engine.mouse.left = True
            if self.getButtonByString(self.joystick_mouse_wheel_button):
                self.engine.mouse.scroll = round(axis[1],4)
            else:
                x,y = self.engine.mouse.pos
                x += round(axis[0],4) * (self.joystick_mouse_speed * (0.5 if self.getButtonByString(self.joystick_mouse_axis_slower_button) else 1))
                y += round(axis[1],4) * (self.joystick_mouse_speed * (0.5 if self.getButtonByString(self.joystick_mouse_axis_slower_button) else 1))
                pg.mouse.set_pos((x,y))
        
    def getButtonById(self, id:int) -> bool:
        return self.joystick.get_button(id)
    
    def getAxisByString(self, name:str) -> tuple[float,float]:
        name = str(name).lower()
        
        if name in ['left','lxy']:
            return (self.getAxisById(JOYSTICK_LEFT_AXIS_X), self.getAxisById(JOYSTICK_LEFT_AXIS_Y))
        elif name in ['right','rxy']:
            return (self.getAxisById(JOYSTICK_RIGHT_AXIS_X), self.getAxisById(JOYSTICK_RIGHT_AXIS_Y))
        else:
            return (0,0)
        
    def getAxisById(self, id:int) -> float:
        return self.joystick.get_axis(id)
    
    def update(self):
        self._emulate_mouse()
    
    # def get_id(self) -> int:
    #     return self.joystick.get_id()
    
    # def get_name(self) -> str:
    #     return self.joystick.get_name()
    
    

class Joystick:
    """
    Joystick Object
    
    Paramaters:
        engine:object
    Returns:
        Joystick
    """
    engine:object
    number_of_joysticks:int = 0
    joysticks:list[Controller,] = []
    
    
    # Config
    joystick_mouse_speed:float = 10.0
    joystick_mouse_axis:str = 'right'
    joystick_trigger_mouse_button:str = 'rt'
    joystick_mouse_wheel_button:str = 'lt'
    joystick_mouse_axis_slower_button:str = 'right_press'
    
    def __init__(self,engine:object):
        self.engine = engine
        self.number_of_joysticks = pg.joystick.get_count()
        self.joysticks = [Controller(i,self) for i in range(self.number_of_joysticks)]
        
        self.main = self.getJoystickById(0) # Main Joystick == Id 0 or Player 1

    @property
    def mainController(self) -> Controller:
        return self.main

    @mainController.setter
    def mainController(self, joystick:Controller):
        print("This is a read-only property")
        
    @mainController.getter
    def mainController(self) -> Controller:
        return self.main
    
    mainJoystick = mainController # Aliases
    
    def getControllerById(self, id:int) -> Controller:
        for joystick in self.joysticks: 
            if joystick.joystick.get_id() == id: return joystick 
            else: pass
        return None
    
    getJoystickById = getControllerById # Aliases
    
    def checkJoysticks(self):
        self.number_of_joysticks = pg.joystick.get_count()
        self.joysticks = [Controller(i,self) for i in range(self.number_of_joysticks)]
        
        if self.number_of_joysticks == 0:
            self.main = None
        else:
            # Updates main controller too
            self.main = self.getJoystickById(0) # Main Joystick == Id 0 or Player 1
            
    def update(self):
        if self.main:
            self.main.update()
    
# Mouse Object
class TrailNode:
    """
    The "TrailNode" for mouse Trail System
    
    Paramaters:
        engine:object
        position:pg.Vector2
        size:tuple[int,int]
        node_color:color/tuple[int,int]
        
    Returns:
        TrailNode
    """
    engine:object
    
    position:pg.Vector2
    node_color:color
    size:tuple
    
    start_time:timedelta
    alpha:int = 255
    alpha_minus:float
    
    surface:pg.SurfaceType
    def __init__(self,engine:object, position:pg.Vector2,size:tuple[int,int],node_color:color):
        """
        The "TrailNode" for mouse Trail System
        
        Paramaters:
            engine:object
            position:pg.Vector2
            size:tuple[int,int]
            node_color:color/tuple[int,int]
            
        Returns:
            TrailNode
        """
        self.position = position
        self.node_color = node_color
        self.size = size
        self.engine = engine
        self.start_time = self.engine.delta_time
        self.surface = pg.Surface(size, SRCALPHA)
        self.surface.fill((node_color if type(node_color) in [list, tuple] else node_color.rgb))
        self.alpha = 255
        
        
    def draw(self, surface:pg.surface.SurfaceType=None):
        """
        Draw "TrailNode"
        
        Paramaters:
            surface:pg.SurfaceType (Optional)
        Returns:
            None
        """
        time_alive = (self.engine.delta_time - self.start_time).total_seconds()
        self.alpha = max(0, self.alpha - int(255 * time_alive / self.engine.mouse.trail_duration))
        if surface is None:
            surface = self.engine.screen
        
        self.surface.set_alpha(self.alpha)
        surface.blit(self.surface, self.position)


class Mouse:
    """
    Mouse Handler Object
    
    This class has the functions to:
    * Get Mouse Position
    * Handle Scroll of the mouse
    * Handle all the Buttons of the mouse
    * Mouse Trail
    
    Paramaters:
        engine:object
    Returns:
        Mouse
    """
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
    
    # Trail
    trail_nodes:list[TrailNode,] = []
    mouse_trail_enabled:bool = False
    trail_duration:int = 1/2 # In Seconds
    trail_node_size:tuple[int,int] = (3,3)
    trail_node_color:color = color(200,200,200)
    trail_node_random_color:bool = False
    
    engine:object
    def __init__(self, engine):
        """
        Mouse Handler Object
        
        This class has the functions to:
        * Get Mouse Position
        * Handle Scroll of the mouse
        * Handle all the Buttons of the mouse
        * Mouse Trail
        
        Paramaters:
            engine:object
        Returns:
            Mouse
        """
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
        """
        Scroll Detection Event
        
        Paramaters:
            Scroll_Event:pg.event.EventType
        Returns:
            None
        """
        self.scroll = scroll_event.y
    
    def collidePoint(self, rect:pg.rect.RectType) -> bool:
        """
        Collide Point
        
        Paramaters:
            rect:pg.rect.RectType
        Returns:
            bool
        """
        if type(rect) in [list, tuple]:
            r = pg.rect.Rect(0,0,0,0)
            r.center = rect
        else: r = rect
            
        return r.collidepoint(self.pos)
        
    def scroll_slow_down(self):
        """
        Scroll Slow Down, Makes a Smooth Scroll that will use accelration for slowly slow down the scrolling
        
        Parameters:
            None
        Returns:
            None
        """
        if (self.scroll < 0 or self.scroll > 0) and self.smooth_scroll:
            self.scroll *= self.loss_speed/100 # xx% Loss Speed
            self.scroll = round(self.scroll, 4)
            if abs(self.scroll) < 0.085:
                self.scroll = 0
        elif not self.smooth_scroll:
            if self.smooth_scroll_delay <= 0:
                self.scroll = 0
                self.smooth_scroll_delay = self.engine.TimeSys.s2f(self.non_smooth_delay)
    
    def draw_trail(self):
        """
        Draw Trail
        Will draw the mouse trail at the screen
        
        Parameters:
            None
        Returns:
            None
        """
        current_time = self.engine.delta_time
        self.trail_nodes = [
            trail for trail in self.trail_nodes 
            if (current_time - trail.start_time).total_seconds() < self.trail_duration
        ]
        
        for trail in self.trail_nodes:
            trail.draw(self.engine.screen)
    
    def update(self):
        """
        Updates the mouse
        * Trail Creation
        * Smooth Scroll
        * Position Update
        * Buttons Update
        
        Parameters:
            None
        Returns:
            None
        """
        if self.mouse_trail_enabled:
            self.trail_nodes.append(TrailNode(
                self.engine, pg.Vector2(self.pos), self.trail_node_size,
                self.trail_node_color if not self.trail_node_random_color else color(0, 0, 0).random()
            ))
        
        self.smooth_scroll_delay = max(0, self.smooth_scroll_delay - 1)
        
        self.x,self.y = pg.mouse.get_pos()
        buttons = pg.mouse.get_pressed(5)
        self.left, self.middle, self.right = buttons[:3]
        self.button_4, self.button_5 = (buttons[3], buttons[4]) if len(buttons) > 3 else (False, False)
        
        # self.draw_trail()
            


    
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