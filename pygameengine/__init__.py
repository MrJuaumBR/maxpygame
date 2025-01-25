"""
Main file for PyGameEngine.
"""

from .required import *
from .objects import *
from .widgets import *
from .l_colors import Colors as ccc
from .l_colors import reqColor
from .excptions import *

class PyGameEngine:
    """
    A *PyGame* Engine.
    Will make create games easier.
    """
    meta:Metadata = Metadata()
    Colors:ccc
    TimeSys:TTimeSys = None
    # PyGame Functions
    screen:pg.SurfaceType=None # Screen
    screen_center:tuple[int,int] = (0,0)
    clock:pg.time.Clock=None # Clock
    
    # Engine Variables
    fps:int=60
    _rfps:float=0
    LastFPSCount:tuple[float,float] = None
    LastAvgFPSCount:tuple[float,float] = None
    widgets:list[Widget,] = []
    fonts:list[pg.font.FontType,] = []
    icon:Icon = None
    events:list[pg.event.Event,] = []
    is_running:bool = False
    started_time:datetime = 0
    _screen_size:tuple[int,int] = (0,0)
    
    # Input Query
    input_query_enable:bool = False
    input_query:InputQuery = None
    
    # Mouse Handler
    mouse:Mouse = None
    
    # Joystick Handler
    joystick:Joystick = None
    joystick_mouse_emulate:bool = False
    
    
    widget_limits:int = 30
    limit_error_active:bool = True
    
    cfgtips = cfgtips()
    
    backgroundFunctions:list[tuple[tuple,object]] = []
    run_background_thread:bool = False
    BackgroundThread:threading.Thread

    
    text_cache:dict
    
    MonitorInfo:VideoInfo = None
    def __init__(self,screen:pg.SurfaceType=None):
        """
        Initializes **PyGame** and the **Engine** itself.
        """
        pg.init()
        self.MonitorInfo = pg.display.Info()
        pg.joystick.init()
        self.input_query=InputQuery(self)
        print(f"{self.meta.name} - {self.meta.version}\n\t - By {self.meta.author}")
        try:
            print(f'\t - [!] Any issues, please go to: {self.meta.github}')
            data_online = requests.get('https://raw.githubusercontent.com/MrJuaumBR/maxpygame/main/data.json').json()
            if 'version' in data_online.keys():
                # Check if metadata version can be converted to int
                try:
                    int(self.meta.splitver())
                    ver = self.meta.splitver2int()
                    if data_online['version'] > ver:
                        print(f'\t - [!] New version available, please go to: {self.meta.github}')
                    elif data_online['version'] < ver:
                        print(f'\t - [!] You are using an unknown version, please go to: {self.meta.github}')
                    else:
                        print(f'\t - Updated version.')
                except: # Cant convert to int
                    if 'fix' in self.meta.version:
                        ver = int(self.meta.splitver().replace('fix',''))
                        if data_online['version'] > ver:
                            print(f'\t - [!] New version available, please go to: {self.meta.github}')
                        elif data_online['version'] < ver:
                            print(f'\t - [!] You are using an unknown version, please go to: {self.meta.github}')
                        else:
                            print(f'\t - Updated version.')
        except: pass
        self.screen = screen
        if self.screen:
            self.screen_center = (self.screen_size[0]//2, self.screen_size[1]//2)
        self.clock = pg.time.Clock()
        self.Colors = ccc()
        self.TimeSys = TTimeSys(self)
        self.mouse = Mouse(self)
        self.joystick = Joystick(self)
        self.started_time:datetime = datetime.now()
    
        self.text_cache:dict = {}
        self.cache_cleanup_time:float = 0.7
    
    def _getElapsedTime(self) -> dict:
        """
        Get the elapsed time of the engine
        
        Parameters:
            None
        Returns:
            dict
        """
        x = humanize_seconds((datetime.now() - self.started_time).seconds)
        return x
    
    def getElapsedTime(self) -> str:
        """
        Get the elapsed time of the engine
        
        Parameters:
            None
        Returns:
            str
        """
        x = self._getElapsedTime()
        s_ = []
        s = ''
        for key in x.keys():
            if x[key] > 0:
                s_.append(f'{x[key]} {key}')
        
        for index,item in enumerate(s_):
            if index == len(s_)-1:
                s += item
            else:
                s += f'{item}, '
        return s
    
    @property
    def delta_time(self) -> timedelta:
        """
        Get the delta time of the engine
        
        Parameters:
            None
        Returns:
            float
        """
        return (datetime.now() - self.started_time)
    
    @delta_time.setter
    def delta_time(self, value:float):
        print("Delta time can't get be changed.")
    
    def getMonitorSize(self) -> tuple[int,int]:
        """
        Get the monitor size
        
        Parameters:
            None
        Returns:
            tuple[int,int]
        """
        return (self.MonitorInfo.current_w, self.MonitorInfo.current_h)
    
    def loadIcon(self):
        """
        Use this when you want to load the engine icon
        """
        self.icon=Icon(self)
    
    # Color System
    def getColor(self, color:reqColor or tuple) -> tuple[int,int,int]: # type: ignore
        """
        Get the color based on type, if is a reqColor convert to rgb, if is a tuple convert to rgb
        
        Parameters:
            color: reqColor or tuple
        Returns:
            tuple[int,int,int]
        """
        if type(color) in [tuple, list]:
            return color
        elif type(color) == str:
            return reqColor(hex=color).rgb
        else:
            try:
                return color.rgb
            except: print(f'The {color} (type: {type(color)}) is a type that cannot be converted to a rgb color.')
    
    # Screen System
    def hasScreen(self) -> bool:
        """
        Check if there is a screen
        
        Parameters:
            None
        Returns:
            bool
        """
        return self.getScreen() is not None
    
    def getScreen(self) -> pg.SurfaceType:
        """
        Get the screen if there is one
        
        Parameters:
            None
        Returns:
            pg.SurfaceType
        """
        if self.screen is None:
            return pg.display.get_surface()
        return self.screen
    
    @property
    def screen_size(self) -> tuple[int,int]:
        """
        Get the size of the screen if there is one
        
        """
        return self._screen_size
    
    @screen_size.setter
    def screen_size(self, value:tuple[int,int]):
        self._screen_size = value
        self.screen_center = (self.screen_size[0]//2, self.screen_size[1]//2)
    
    def setMouseEmulation(self, state:bool = True):
        self.joystick_mouse_emulate = state
        
    
    def createScreen(self, width:int, height:int, flags:int=SCALED,VSync:bool=False) -> pg.SurfaceType:
        """
        Create a screen if there is not one
        
        Parameters:
            width:int
            height:int
            flags(Optional):int
            VSync(Optional):bool
        Returns:
            pg.SurfaceType
        """
        if not self.hasScreen(): # If there is no screen
            if flags == FULLSCREEN: # If fullscreen
                flags = FULLSCREEN|SCALED
            self.screen = pg.display.set_mode((width, height), flags=flags,vsync=VSync)
            if self.icon is None:
                self.loadIcon()
                self.setScreenIcon(self.icon.surf)
            else: self.setScreenIcon(self.icon)
            self.is_running = True
            self.screen_size = (width, height)
            self.screen_center = (self.screen_size[0]//2, self.screen_size[1]//2)
            return self.screen
    
    def setScreenTitle(self, title:str):
        """
        Set the title of the screen if there is one
        
        Parameters:
            title:str
        Returns:
            None
        """
        if self.hasScreen():
            pg.display.set_caption(title)
            
    
    def setScreenIcon(self, icon:pg.SurfaceType):
        """
        Set the icon of the screen if there is one
        
        Parameters:
            icon:pg.SurfaceType
        Returns:
            None
        """
        if self.hasScreen():
            pg.display.set_icon(icon)
    
    # Event System
    
    def getEvents(self) -> list[pg.event.Event,]:
        """
        Get all the events of PyGame
        
        Parameters:
            None
        Returns:
            list[pg.event.Event,]
        """
        events = pg.event.get()
        if len(events) == 0: # If there are no events
            self.mouse.scroll_slow_down()
        else:
            for event in events:
                if event.type == MOUSEWHEEL:
                    self.mouse.scroll_detector(event)
                elif event.type == VIDEORESIZE:
                    self.screen_size = self.screen.get_size()
                else:
                    self.mouse.scroll_slow_down()
        return events
    def getKeys(self) -> pg.key.ScancodeWrapper:
        """
        Get all Keys pressed
        
        Parameters:
            None
        Returns:
            ScancodeWrapper
        """
        
        return pg.key.get_pressed()
        
    def hasKeyPressed(self, key:int) -> bool:
        """
        Check if a key is pressed
        
        Parameters:
            key:int
        Returns:
            bool
        """
        return self.getKeys()[key]
    
    def keyToString(self, key:int) -> str:
        """
        Convert a key to a string
        
        Parameters:
            key:int
        Returns:
            str
        """
        return pg.key.name(key)
    
    def stringToKey(self, name:str) -> int:
        """
        Convert a string to a key
        
        Parameters:
            name:str
        Returns:
            int
        """
        return pg.key.key_code(name)
    
    def exit(self):
        """
        Exit PyGameEngine
        
        Parameters:
            None
        Returns:
            None
        """
        self.is_running = False
        pg.quit()
        sys.exit()
        
    def _triesUpdate(self, target:pg.SurfaceType=None):
        """
        Update the screen if there is one, if not try to update the target
        
        ! This function is for trying to catch a error !
        
        Parameters:
            target(Optional):pg.SurfaceType
        """
        try:
            if target is None:
                pg.display.update(self.screen)
            else:
                pg.display.update(target)
        except Exception as ex:
            try:
                # Tries Flip
                pg.display.flip()
            except Exception as ex:
                raise ex    
    
    def background_thread(self):
        """
        Background thread for the engine
        
        Parameters:
            None
        Returns:
            None
        """
        print("\t - [!] Background thread started.")
        with self.threadLock:
            while self.run_background_thread and self.is_running:
                if self.BgFnCanRun:
                    for index, func_data in enumerate(self.backgroundFunctions):
                        func = func_data[0]
                        args = func_data[1]
                        try:
                            if func:
                                if callable(func):
                                    func(*args)
                        except Exception as ex:
                            print(f'\t - [!] Error in background thread: {ex}')
                        self.backgroundFunctions.pop(index)
                    self.BgFnCanRun = False
                self.fpsw()

    def setRunBackgroundThread(self, state:bool = True):
        """
        Enable or disable the background thread
        
        Parameters:
            state:bool
        Returns:
            None
        """
        self.run_background_thread = state
        if state:
            print(f'\t - [!] Background thread enabled.')
            
            self.BackgroundThread = threading.Thread(target=self.background_thread,name='BackgroundThread',daemon=True)
            self.BackgroundThread.start()
            print("After")
        else:
            print(f'\t - [!] Background thread disabled.')
            self.BackgroundThread = None
            self.backgroundFunctions.clear()
            
    def addFunction(self, func:object, args:tuple):
        """
        Add a function to the background thread
        
        Parameters:
            func:object
            args:tuple
        Returns:
            None
        """
        if self.run_background_thread:
            self.backgroundFunctions.append((func,args))
        else:
            print(f'\t - [!] Background thread is disabled.')
    
    def _update(self, target:pg.SurfaceType=None):
        """
        Update the screen if there is one, if not try to update the target
        
        Parameters:
            target(Optional):pg.SurfaceType
        Returns:
            None
        """
        self.is_running = True
        if self.hasScreen():
            self._triesUpdate(target)
        self.events = self.getEvents()
        self.mouse.update()

        current_joysticks = pg.joystick.get_count()
        if current_joysticks != self.joystick.number_of_joysticks:
            self.joystick.checkJoysticks()

        if current_joysticks > 0 and self.joystick_mouse_emulate:
            self.joystick.main.mouse_emulate = self.joystick_mouse_emulate
            self.joystick.update()

        if self.input_query_enable:
            self.events = [event for event in self.events if event.type != pg.KEYUP]
            for event in self.events:
                if event.type == pg.KEYDOWN:
                    self.input_query.insert_query(event)
            self.input_query.update(self.delta_time)
            
    def update(self, target:pg.SurfaceType=None,runBackground:bool=False):
        """
        Update the screen if there is one, if not try to update the target
        
        *If run_background_thread is True, this function will be called in a background thread*
        
        Parameters:
            target(Optional):pg.SurfaceType
        Returns:
            None
        """
        if self.run_background_thread and runBackground:
            self.backgroundFunctions.append((self._update,(target,)))
        else:
            self._update(target)
            self.BgFnCanRun:bool = True
        
                    
        
    def flip(self):
        """
        Flip the screen if there is one
        
        ! Make sure that you don't use update function !
        
        Parameters:
            None
        Returns:
            None
        """
        self.is_running = True
        if self.hasScreen():
            pg.display.flip()
            
        self.events = self.getEvents()
        self.mouse.update()
    
    def fpsw(self):
        """
        Wait fps(Frames Per Second)
        
        Defines the FPS to wait using → setFPS()
        """
        self.clock.tick(self.fps)
        self._rfps = self.clock.get_fps()
        current_time = time.time()
        if self.LastFPSCount and current_time - self.LastFPSCount[0] >= 1:
            self.LastFPSCount = (current_time, self._rfps)
        elif not self.LastFPSCount:
            self.LastFPSCount = (current_time, self._rfps)
    def enableFPS_unstable(self, state:bool = True):
        """
        Adds a support for low perfomance PCs
        
        using a system that will no longer delay too much clicks(Widgets problem)
        """
        self.TimeSys.unstable_fps = state
    
    def getAvgFPS(self) -> float:
        """
        Get the average FPS of the screen if there is one
        
        Parameters:
            None
        Returns:
            float
        """
        current_time = time.time()
        
        if self.LastAvgFPSCount is None:
            self.LastAvgFPSCount = (current_time, self._rfps)
            return self._rfps
        
        if self.LastFPSCount and current_time - self.LastFPSCount[0] >= 0.9:
            avg_fps = (self.LastAvgFPSCount[1] * 2 + self._rfps + self.LastFPSCount[1]) / 4
            self.LastAvgFPSCount = (current_time, avg_fps)
            return avg_fps
        
        return self.LastAvgFPSCount[1]
    
    def getFPS(self) -> float:
        """
        Get the FPS of the screen if there is one
        
        Parameters:
            None
        Returns:
            float
        """
        return self._rfps
    
    def setFPS(self, fps:int):
        """
        Set the FPS of the screen if there is one
        
        Parameters:
            fps:int
        Returns:
            None
        """
        if self.hasScreen():
            self.fps = fps
            self.TimeSys.time = pg.time.get_ticks() # Updates.
     
    def fill(self, fill_color:reqColor) -> bool:
        """
        Fill the screen if there is one
        and draw the mouse trail if it's enabled
        
        Parameters:
            fill_color:reqColor
        Returns:
            None or bool
        """
        if not self.hasScreen(): return None # No screen then no,no
        self.screen.fill(fill_color if type(fill_color) in [tuple, list] else self.getColor(fill_color))
        self.mouse_draw_trail()
        return True
    
    def mouse_draw_trail(self):
        """
        Draw the mouse trail if it's enabled
        
        Parameters:
            None
        Returns:
            None
        """
        if self.mouse.mouse_trail_enabled:
            self.mouse.draw_trail()
            return True
        else:
            return None
    
    def createSurface(self, width:int, height:int, flags:int=0) -> pg.SurfaceType:
        """
        Creates a Surface
        
        Parameters:
            width:int
            height:int
            flags:int (Optional)
        Returns:
            pg.SurfaceType
        """
        return pg.Surface((width, height), flags)
    
    # Font System
    def _findFont(self, font:pg.font.FontType) -> pg.font.FontType:
        """
        Find the font in the list of fonts
        
        Parameters:
            font:pg.font.FontType
        Returns:
            pg.font.FontType
        """
        if type(font) != int:
            return self.fonts[self.fonts.index(font)]
        else:
            return self.fonts[font]
    
    def createSysFont(self,font_name:str, font_size:int, bold:bool=False, italic:bool=False) -> pg.font.FontType:
        """
        Create a font from the system
        
        Parameters:
            font_name:str
            font_size:int
            bold(Optional):bool
            italic(Optional):bool
        Returns:
            pg.font.FontType
        """
        font = pg.font.SysFont(font_name, font_size, bold, italic)
        if font not in self.fonts:
            self.fonts.append(font)
        else:
            font = self.fonts[self._findFont(font)]
        return font
    
    def createFont(self, font_file:str, font_size:int) -> pg.font.FontType:
        """
        Create a font from a file
        
        Parameters:
            font_file:str
            font_size:int
        Returns:
            pg.font.FontType
        """
        font = pg.font.Font(font_file, font_size)
        if font not in self.fonts:
            self.fonts.append(font)
        else:
            font = self.fonts[self._findFont(font)]
        return font

    # Mouse System
    def getMousePos(self) -> tuple[int,int]:
        """
        Get the mouse position
        
        Parameters:
            None
        Returns:
            tuple[int,int]
        """
        return pg.mouse.get_pos()
    
    def getMousePressed(self,num:int=3) -> list[bool,]:
        """
        Check if the mouse is pressed
        
        Parameters:
            None
        Returns:
            bool
        """
        return pg.mouse.get_pressed(num)

    # Widget System
    def addWidget(self, widget:Widget):
        """
        Add a widget to the list of widgets
        
        Parameters:
            widget:Widget
        Returns:
            None
        """
        widget_count = len(self.widgets)
        if widget_count >= self.widget_limits:
            print('\t - [!] You are using a high amount of widgets, try to reduce it.')
            if widget_count >= self.widget_limits * 2 and self.limit_error_active:
                raise WidgetPassedError(widget, widget_count)
        elif widget_count >= self.widget_limits * 0.8:
            print(f'\t - [!] You used {int((widget_count / self.widget_limits) * 100)}% of max recommended widgets. Consider reducing it.')
        
        self.widgets.append(widget)
    
    def create_tip(self, text:str, font:pg.font.FontType) -> Tip:
        """
        Create a tip from a text and a font
        
        Parameters:
            text:str
            font:pg.font.FontType
        Returns:
            Tip
        """
        return Tip(self, text, font)
    
    def create_widget(self, widget_type:str, *args, **kwargs) -> Widget:
        """
        Create a widget from a type
        
        Parameters:
            widget_type:str or WidgetClass
            *args
            **kwargs
        Returns:
            Widget
        """
        # Get the widget
        if type(widget_type) != str:
            if inspect.isclass(widget_type):
                widget = widget_type
            else:
                raise(CreateWidgetTypeError(str(widget_type)))
        else:
            widget = getattr(sys.modules[__name__], str(widget_type).capitalize())
        if widget:
            aargs = args
            return widget(self, *aargs, **kwargs)
        return None
    
    def SetLimitWidget(self, limit:int=30):
        """
        Set the widget limit number
        
        Parameters:
            limit:int
        Returns:
            None
        """
        self.widget_limits = limit
        
    def SetErrorLimitWidget(self, state:bool=True):
        """
        Enable or disable the widget limit error
        
        Parameters:
            state:bool
        Returns:
            None
        """
        self.limit_error_active = state
        
    def findWidgetById(self, id:str) -> Widget:
        """
        Find a widget by its id and then return it
        
        Parameters:
            id:str
        Returns:
            Widget
        """
        if type(id) in [str,int]:
            id = str(id)
            for widget in self.widgets:
                if str(widget._id) == id:
                    return self.widgets[self.widgets.index(widget)]
        
        return None

    def DeleteWidget(self, widget:Widget):
        """
        Delete a widget from the list of widgets and from any group that is in.
        """
        self.findWidgetById(widget).delete()
        
    def _DeleteWidget(self, widget_id:str):
        """
        Delete a widget from the list of widgets and from any group that is in.
        """
        w = self.widgets.index(self.findWidgetById(widget_id))
        self.widgets.pop(w)

    # Image System
    def loadImage(self, path:str) -> pg.SurfaceType:
        """
        Load an image from a path
        
        Parameters:
            path:str
        Returns:
            pg.SurfaceType
        """
        return pg.image.load(path).convert_alpha()
    
    def flip_surface(self, surface:pg.SurfaceType, x_axis:bool=False, y_axis:bool=False) -> pg.SurfaceType:
        """
        Flips a surface on the x &/or y axis
        
        Parameters:
            surface:pg.SurfaceType
            x_axis:bool
            y_axis:bool
        Returns:
            pg.SurfaceType
        """
        x = pg.transform.flip(surface, x_axis, y_axis)
        return x
    
    def rotate(self, surface:pg.SurfaceType, rect:pg.Rect, angle:int) -> tuple[pg.SurfaceType, pg.Rect]:
        """
        Rotate a surface
        
        Parameters:
            surface:pg.SurfaceType
            rect:pg.Rect
            angle:int = Degrees
        Returns:
            tuple[pg.SurfaceType, pg.Rect]
        """
        new_image = pg.transform.rotate(surface, angle)
        new_rect = new_image.get_rect(center=rect.center)
        return new_image, new_rect
        
    
    def createSpritesheet(self, image_path:str) -> spritesheet:
        """
        Create a spritesheet from an image
        
        Parameters:
            image_path:str
        Returns:
            spritesheet
        """
        return spritesheet(self, image_path)

    # Draw System
    def draw_widgets(self, widgets:list[Widget]=None):
        """
        Draw a list of widgets
        
        Parameters:
            widgets:list[Widget]
        Returns:
            None
        """
        for widget in widgets or self.widgets:
            if widget.enable:
                widget.draw()
                
    def draw_rect(self, pos:tuple[int,int], size:tuple[int,int], color:reqColor, border_width:int=0, border_color:reqColor=None, surface:pg.SurfaceType=None, alpha:int=255,align:Literal['center', 'topleft', 'topright', 'bottomleft', 'bottomright'] = 'topleft') -> pg.Rect:
        """
        Draw a rect on the surface
        
        Parameters:
            Position:tuple[int,int]
            Size:tuple[int,int]
            color:reqColor
            border_width(Optional):int
            surface(Optional):pg.SurfaceType
            alpha(Optional):int
        Returns:
            Rect
        """
        if not self.hasScreen():
            return None
        
        rect = pg.Rect(*pos, *size)
        if align == 'center':
            rect.center = pos
        elif align == 'topleft':
            rect.topleft = pos
        elif align == 'topright':
            rect.topright = pos
        elif align == 'bottomleft':
            rect.bottomleft = pos
        elif align == 'bottomright':
            rect.bottomright = pos
        else:
            raise(InvalidAlignParameter(align))
            
        color = self.getColor(color)
        
        if surface is None:
            surface = self.getScreen()
        
        if border_width > 0 and border_color is not None:
            b_color = self.getColor(border_color)
            pg.draw.rect(surface, b_color, rect, border_width)
        
        s = pg.Surface(rect.size, pg.SRCALPHA)
        s.fill(color)
        s.set_alpha(alpha)
        surface.blit(s, rect.topleft)
        
        return rect

    def draw_circle(self, pos:tuple[int,int], radius:int, color:reqColor, surface:pg.SurfaceType=None, alpha:int=255) -> pg.Rect:
        """
        Draw a circle on the surface
        
        Parameters:
            rect:pg.Rect
            color:reqColor
            surface(Optional):pg.SurfaceType
            alpha(Optional):int
        Returns:
            Rect
        """
        if self.hasScreen():
            rect = pg.Rect(*pos, radius*2, radius*2)
            
            color = self.getColor(color)
            
            if surface is None:
                surface = self.getScreen()
            
            pg.draw.ellipse(surface, color, rect, radius)
            
            return rect
        return None

    def draw_text(self, position: tuple[int, int], text: str, font: pg.font.FontType, color: reqColor, surface: pg.SurfaceType = None, bgColor: reqColor = None, border_width: int = 0, border_color: reqColor = None, alpha: int = 255, align:Literal['center','topleft','topright','bottomleft','bottomright'] = 'topleft') -> pg.Rect:
        """
        Draw text on the surface

        Parameters:
            text: str
            font: pg.font.FontType
            position: tuple[int, int]
            color: reqColor
            surface (Optional): pg.SurfaceType
            bgColor (Optional): reqColor
            alpha (Optional): int
            align (Optional): 'center','topleft','topright','bottomleft','bottomright'
        Returns:
            Rect
        """
        font = self._findFont(font)
        color = self.getColor(color)
        bgColor = self.getColor(bgColor) if bgColor is not None else None

        text_id = hash((text, color, bgColor, border_width, border_color, alpha, align))
        if text_id in self.text_cache:
            text_surface = self.text_cache[text_id][0]
        else:
            text_surface = pg.Surface((font.size(text)[0] + border_width * 2, font.size(text)[1] + border_width * 2), pg.SRCALPHA)
            render = font.render(text, True, color, bgColor)
            render.set_alpha(alpha)
            text_surface.blit(render, (border_width, border_width))
            self.text_cache[text_id] = (text_surface, time.time())

        rect:pg.rect.RectType = Rect(0,0,*text_surface.get_size())
        align = str(align).lower()
        
        if align == 'center':
            rect.center = position
        elif align == 'topleft':
            rect.top = position[1]
            rect.left = position[0]
        elif align == 'topright':
            rect.top = position[1]
            rect.right = position[0]
        elif align == 'bottomleft':
            rect.bottomleft = position
        elif align == 'bottomright':
            rect.bottomright = position
        else:
            raise(InvalidAlignParameter(align))
            
        if surface is None:
            surface = self.getScreen()
        surface.blit(text_surface, rect.topleft)

        self._clean_text_cache()
        
        return rect

    def clear_cache(self):
        self.text_cache.clear()

    def _clean_text_cache(self):
        current_time = time.time()
        for Text_Id, (surf, timestamp) in list(self.text_cache.items()):
            if current_time - timestamp > self.cache_cleanup_time:
                del self.text_cache[Text_Id]
    
    def getSystemDict(self) -> dict:
        info = {
            "System": platform.system(),
            "Node Name": platform.node(),
            "Release": platform.release(),
            "Version": platform.version(),
            "Machine": platform.machine(),
        }
        
        cpu_cmd = ''
        gpu_cmd = ''
        if info["System"].lower() == "windows":
            cpu_cmd = 'wmic cpu get name'
            gpu_cmd = 'wmic path Win32_VideoController get name'
        elif info["System"].lower() == "linux":
            cpu_cmd = 'lscpu'
            gpu_cmd = 'lspci'
        
        cpu = subprocess.run(cpu_cmd, shell=True, stdout=subprocess.PIPE).stdout.strip().decode("utf-8").replace("\r",'').replace("\n",'').replace("    ", "")
        gpu = subprocess.run(gpu_cmd, shell=True, stdout=subprocess.PIPE).stdout.strip().decode("utf-8").replace("\r",'').replace("\n",'').replace("    ", "")
        
        info["CPU"] = cpu
        info["GPU"] = gpu
        info["RAM"] = self.getRam()
        
        return info
    
    def getRam(self):
        if platform.system().lower() == "windows":
            total_memory = float(os.popen("wmic ComputerSystem get TotalPhysicalMemory").read().strip().split()[-1])
        else:
            mem_info = subprocess.check_output(['free', '-b']).decode('utf-8').split('\n')[1].split()
            total_memory = float(mem_info[1])
            
        return f'{round(total_memory / (1024**3), 2)} Gb'
            

    def printSystemInfo(self):
        info = self.getSystemDict()
        for key in info.keys():
            print(f'{key}: {info[key]}')
            
            
    def getInUseCPU(self) -> float:
        """
        ! This function uses CMD, so is totally unstable and the FPS will drop if in the game loop. !
        Get the percentage(%) of CPU in use
        """
        if platform.system().lower() == "windows":
            return float(os.popen("wmic cpu get loadpercentage").read().strip().split()[-1])
        else:
            return float(os.popen("top -bn1 | grep 'Cpu(s)' | sed 's/.*, *\([0-9.]*\)%* id.*/\\1/' | awk '{print 100 - $1}'").read().strip())
        
    def getInUseRam(self) -> float:
        """
        ! This function uses CMD, so is totally unstable and the FPS will drop if in the game loop. !
        Get the percentage(%) of RAM in use
        """
        if platform.system().lower() == "windows":
            mem_info = subprocess.check_output(['wmic', 'OS', 'get', 'FreePhysicalMemory']).decode('utf-8').split()
            free_memory = float(mem_info[1]) # In KBytes
            total_memory = float(subprocess.check_output(['wmic', 'ComputerSystem', 'get', 'TotalPhysicalMemory']).decode('utf-8').split()[1])
            free_memory /= 1024**2 # In GBytes
            total_memory /= 1024**2 # In GBytes
            return round((total_memory - free_memory) / total_memory,2)
        else:
            mem_info = subprocess.check_output(['free']).decode('utf-8').split('\n')[1].split()
            total_memory = float(mem_info[1])
            used_memory = float(mem_info[2])
            return round(used_memory / total_memory,2)
# God bless me for continue making this project
# Cu'z i'm getting crazy