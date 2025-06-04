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

    
    text_cache:dict
    extra_process:bool = True
    extra_process_query:list[object, ] = []
    
    # Particles
    particles:set[Particle,] = set()
    
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
        print(f'\t - [!] Any issues, please go to: {self.meta.github}')
        self.detect_version()
        self.screen = screen
        if self.screen:
            self.screen_center = (self.screen_size[0]//2, self.screen_size[1]//2)
        self.clock = pg.time.Clock()
        self.Colors = ccc()
        self.TimeSys = TTimeSys(self)
        self.mouse = Mouse(self)
        self.joystick = Joystick(self)
        self.started_time:datetime = datetime.now()
        
        self.is_running = True
    
        self.text_cache:dict = {}
        self.cache_cleanup_time:float = 0.7
        
        if self.extra_process:
            threading.Thread(target=self.extra_process_do_query).start()
    
    def detect_version(self) -> bool:
        with urllib.request.urlopen('https://raw.githubusercontent.com/MrJuaumBR/maxpygame/main/data.json') as resp:
            data = resp.read().decode()
            
        data_online = json.loads(data)
        if 'version' in data_online.keys():
                # Check if metadata version can be converted to int
        #         try:
        #             int(self.meta.splitver())
            ver = self.meta.splitver2int()
            if data_online['version'] > ver:
                print(f'\t - [!] New version available, please go to: {self.meta.github}')
            elif data_online['version'] < ver:
                print(f'\t - [!] You are using an unknown version ({ver}), please go to: {self.meta.github}')
            else:
                print(f'\t - Updated version.')
                return True
        
        
        return False
    def extra_process_do_query(self):
        if self.extra_process:
            while self.is_running:
                if len(self.extra_process_query) > 0:
                    for query, args in self.extra_process_query:
                        try:
                            query(*args)
                        except Exception as e:
                            print(f'Error in extra process: {e}')
                self.clock.tick(self.fps*0.95)
    
    
    def _getElapsedTime(self) -> dict:
        """
        Get the elapsed time of the engine
        
        Parameters:
            None
        Returns:
            dict
        """
        return humanize_seconds(self.delta_time.total_seconds())
    
    def getElapsedTime(self) -> str:
        """
        Get the elapsed time of the engine
        
        Parameters:
            None
        Returns:
            str
        """
        x = self._getElapsedTime()
        return ', '.join(f'{x[key]} {key}' for key in x if x[key] > 0)
    
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
        raise AttributeError("delta_time is a read-only property")
    
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
            except AttributeError: print(f'The {color} (type: {type(color)}) is a type that cannot be converted to a rgb color.')
    
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
        return pg.display.get_surface() if self.screen is None else self.screen
    
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
    
    def getEvents(self) -> list[pg.event.EventType]:
        """
        Get all the events of PyGame
        
        Parameters:
            None
        Returns:
            list[pg.event.EventType]
        """
        events = pg.event.get()
        has_events = bool(events)
        
        if not has_events:
            self.mouse.scroll_slow_down()
        else:
            if resize_event := next((e for e in events if e.type == pg.VIDEORESIZE), None):
                self.screen_size = self.screen.get_size()
            for event in events:
                if event.type == MOUSEWHEEL:
                    self.mouse.scroll_detector(event)

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
    quit = exit
        
    def _triesUpdate(self, target:pg.SurfaceType=None):
        """
        Update the screen if there is one, if not try to update the target
        
        ! This function is for trying to catch a error !
        
        Parameters:
            target(Optional):pg.SurfaceType
        """
        try:
            if target is None:
                pg.display.flip()
            else:
                pg.display.update(target)
        except Exception as e:
            raise(e)
            print(f'Error trying to update the screen: {e}')
    
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

        if self.extra_process:
            if self.input_query_enable:
                self.extra_process_query.append((self.input_query_process, ()))
            if len(self.particles) > 0:
                self.extra_process_query.append((self.particles_process, ()))
        else:
            if self.input_query_enable:
                self.input_query_process()
            if len(self.particles) > 0:
                self.particles_process()
            
    def input_query_process(self):
        self.events = [event for event in self.events if event.type != pg.KEYUP]
        for event in self.events:
            if event.type == pg.KEYDOWN:
                self.input_query.insert_query(event)
        self.input_query.update(self.delta_time)
    
    def particles_process(self):
        """
        This function processes particles by updating their properties and removing them if they have
        exceeded their lifetime.
        """
        for particle in self.particles.copy():
            if not particle.anchored:
                if (self.delta_time-particle.start_time).total_seconds() > particle.lifetime:
                    self.particles.remove(particle)
                    continue
            particle.update()
            
            
    def particles_render(self):
        for particle in self.particles.copy():
            particle.render()
            
    def update(self, target:pg.SurfaceType=None):
        """
        Update the screen if there is one, if not try to update the target
        
        Parameters:
            target(Optional):pg.SurfaceType
        Returns:
            None
        """
        self._update(target)
            
        
                    
        
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
        current_time = self.delta_time.total_seconds()
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
        current_time = self.delta_time.total_seconds()
        if self.LastAvgFPSCount is None or current_time < 1.1:
            r = self._rfps if self._rfps <= 0 else self.fps
            self.LastAvgFPSCount = (current_time, r)
            return r
        elif (self.LastFPSCount and current_time - self.LastFPSCount[0] >= 1):
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
        self.particles_render()
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
        if type(widget_type) == str:
            widget = getattr(sys.modules[__name__], widget_type.capitalize())
        elif inspect.isclass(widget_type):
            widget = widget_type
        else:
            raise(CreateWidgetTypeError(widget_type))
        if widget:
            args = args
            return widget(self, *args, **kwargs)
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
        
    def findWidgetById(self, widget_id:str) -> Widget:
        """
        Find a widget by its id and then return it
        
        Parameters:
            id:str
        Returns:
            Widget
        """
        widget_id = str(widget_id)
        return next((widget for widget in self.widgets if widget._id == widget_id), None)

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

    def CreateParticle(self, position:tuple, lifetime:float, colors:list[reqColor,], nodes:int, size:float, speed:float, direction:Literal['all', 'up', 'down', 'left', 'right']='all', anchored:bool=False, respawn_threshold:float=1, continuity:bool=False, fade_out:bool=True) -> Particle:
        """
        Create a Particle of a type
        
        Parameters:
            position:tuple
            lifetime:float
            colors:list[reqColor,]
            nodes:int
            size:float
            speed:float
            direction:Literal['all', 'up', 'down', 'left', 'right']
            anchored:bool
            respawn_threshold:float
            continuity:bool
            fade_out:bool
        Returns:
            Particle
        """
        
        p = Particle(engine=self, position=position, lifetime=lifetime, colors=colors, quantity=nodes, size=size, speed=speed, direction=direction, anchored=anchored, respawn_threshold=respawn_threshold, continuity=continuity, fade_out=fade_out)
        self.particles.add(p)
        return p

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
        return pg.transform.flip(surface, x_axis, y_axis)
    
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
                
    def draw_rect(self, pos:tuple[int,int], size:tuple[int,int], color:reqColor, border_width:int=0, border_color:reqColor=None, surface:pg.SurfaceType=None, alpha:int=255,root_point:Literal['center', 'topleft', 'topright', 'bottomleft', 'bottomright'] = 'topleft') -> pg.Rect:
        """
        Draw a rect on the surface
        
        Parameters:
            Position:tuple[int,int]
            Size:tuple[int,int]
            color:reqColor
            border_width(Optional):int
            surface(Optional):pg.SurfaceType
            alpha(Optional):int
            root_point(Optional):'center', 'topleft', 'topright', 'bottomleft', 'bottomright'
        Returns:
            Rect
        """
        if not self.hasScreen():
            return None
        
        root_point = str(root_point).lower()
        rect = pg.Rect(*pos, *size)
        if root_point == 'bottomleft':
            rect.bottomleft = pos
        elif root_point == 'bottomright':
            rect.bottomright = pos
        elif root_point == 'center':
            rect.center = pos
        elif root_point == 'topleft':
            rect.topleft = pos
        elif root_point == 'topright':
            rect.topright = pos
        
        else:
            raise(InvalidAlignParameter(root_point))
            
        if surface is None:
            surface = self.getScreen()
        
        if border_width > 0 and border_color is not None:
            b_color = self.getColor(border_color)
            pg.draw.rect(surface, b_color, rect, border_width)
        
        s = pg.Surface(rect.size, pg.SRCALPHA)
        if color:
            color = self.getColor(color)
            s.fill(color)
        s.set_alpha(alpha)
        surface.blit(s, rect.topleft)
        
        return rect

    def draw_circle(self, pos:tuple[int,int], radius:int, color:reqColor, surface:pg.SurfaceType=None, width:int=0, alpha:int=255) -> pg.Rect:
        """
        Draw a circle on the surface
        
        Parameters:
            rect:pg.Rect
            color:reqColor
            surface(Optional):pg.SurfaceType
            width(Optional):int
            alpha(Optional):int
        Returns:
            Rect
        """
        if self.hasScreen():
            rect = pg.Rect(*pos, radius*2, radius*2)
            
            color = self.getColor(color)
            
            if surface is None:
                surface = self.getScreen()
            
            # Create a surface with alpha channel
            s = pg.Surface((radius*2, radius*2), pg.SRCALPHA)
            pg.draw.circle(s, color, (radius, radius), radius, width)
            s.set_alpha(alpha)
            
            # Blit the surface onto the target surface
            surface.blit(s, pos)
            
            return rect
        return None

    def draw_text(self, position: tuple[int, int], text: str, font: pg.font.FontType, color: reqColor, surface: pg.SurfaceType = None, bgColor: reqColor = None, border_width: int = 0, border_color: reqColor = None, alpha: int = 255, root_point:Literal['center','topleft','topright','bottomleft','bottomright'] = 'topleft') -> pg.Rect:
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
            root_point (Optional): 'center','topleft','topright','bottomleft','bottomright'
        Returns:
            Rect
        """
        font = self._findFont(font)
        color = self.getColor(color)
        bgColor = self.getColor(bgColor) if bgColor is not None else None

        text_id = hash((text, color, bgColor, border_width, border_color, alpha, root_point))
        if text_id in self.text_cache:
            text_surface = self.text_cache[text_id][0]
        else:
            text_surface = pg.Surface((font.size(text)[0] + border_width * 2, font.size(text)[1] + border_width * 2), pg.SRCALPHA)
            render = font.render(text, True, color, bgColor)
            render.set_alpha(alpha)
            text_surface.blit(render, (border_width, border_width))
            
        self.text_cache[text_id] = (text_surface, self.delta_time.total_seconds())

        rect:pg.rect.RectType = Rect(0,0,*text_surface.get_size())
        root_point = str(root_point).lower()
        
        if root_point == 'center':
            rect.center = position
        elif root_point == 'topleft':
            rect.top = position[1]
            rect.left = position[0]
        elif root_point == 'topright':
            rect.top = position[1]
            rect.right = position[0]
        elif root_point == 'bottomleft':
            rect.bottomleft = position
        elif root_point == 'bottomright':
            rect.bottomright = position
        else:
            raise(InvalidAlignParameter(root_point))
            
        if surface is None:
            surface = self.getScreen()
        surface.blit(text_surface, rect.topleft)

        self.clean_text_cache()
        
        return rect

    def clear_cache(self):
        self.text_cache.clear()
    def clean_text_cache(self):
        if self.extra_process:
            self.extra_process_query.append((self._clean_text_cache, ()))
        else:
            self._clean_text_cache()
    def _clean_text_cache(self):
        current_time = self.delta_time.total_seconds()
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