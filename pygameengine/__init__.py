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
    A **PyGame** Engine.<br>
    Will make create games easier.
    """
    meta:Metadata = Metadata()
    Colors:ccc
    TimeSys:TTimeSys = None
    # PyGame Functions
    screen:pg.SurfaceType=None # Screen
    clock:pg.time.Clock=None # Clock
    
    # Engine Variables
    fps:int=60
    _rfps:float=0
    widgets:list[Widget,] = []
    fonts:list[pg.font.FontType,] = []
    icon:Icon = None
    events:list[pg.event.Event,] = []
    is_running:bool = False
    started_time:datetime = 0
    
    mouse:Mouse = None
    
    widget_limits:int = 30
    limit_error_active:bool = True
    
    def __init__(self,screen:pg.SurfaceType=None):
        """
        Initializes **PyGame** and the **Engine** itself.
        """
        pg.init()
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
        self.clock = pg.time.Clock()
        self.Colors = ccc()
        self.TimeSys = TTimeSys(self)
        self.mouse = Mouse(self)
        self.started_time:datetime = datetime.now()
    
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
    def delta_time(self) -> float:
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
            except: print(f'The {color} is a type that cannot be converted to a rgb color.')
    
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
    
    def createScreen(self, width:int, height:int, flags:int=SCALED) -> pg.SurfaceType:
        """
        Create a screen if there is not one
        
        Parameters:
            width:int
            height:int
            flags(Optional):int
        Returns:
            pg.SurfaceType
        """
        if not self.hasScreen(): # If there is no screen
            if flags == FULLSCREEN: # If fullscreen
                flags = FULLSCREEN|SCALED
            self.screen = pg.display.set_mode((width, height), flags=flags)
            if self.icon is None:
                self.loadIcon()
                self.setScreenIcon(self.icon.surf)
            else: self.setScreenIcon(self.icon)
            self.is_running = True
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
                else:
                    self.mouse.scroll_slow_down()
        return events
    def getKeys(self) -> pg.key.ScancodeWrapper:
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
        
    def update(self, target:pg.SurfaceType=None):
        """
        Update the screen if there is one, if not try to update the target
        
        Parameters:
            target(Optional):pg.SurfaceType
        Returns:
            None
        """
        self.is_running = True
        if self.hasScreen() and target is None:
            self._triesUpdate()
        elif self.hasScreen() and target:
            self._triesUpdate(target)
        self.events = self.getEvents()
        self.mouse.update()
        
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
    
    def enableFPS_unstable(self, state:bool = True):
        """
        Adds a support for low perfomance PCs
        
        using a system that will no longer delay too much clicks(Widgets problem)
        """
        self.TimeSys.unstable_fps = state
    
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
     
    def fill(self, fill_color:reqColor):
        """
        Fill the screen if there is one
        
        Parameters:
            fill_color:reqColor
        Returns:
            None
        """
        if self.hasScreen():
            if not (type(color) in [tuple, list]):
                clr = self.getColor(fill_color)
            else: clr = fill_color
            self.screen.fill(clr)
    
    def createSurface(self, width:int, height:int, flags:int=0) -> pg.SurfaceType:
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
        if len(self.widgets) >= self.widget_limits:
            print('\t - [!] You are using a high amount of widgets, try to reduce it.')
            if len(self.widgets) >= self.widget_limits*2:
                if self.limit_error_active:
                    raise(WidgetPassedError(widget,len(self.widgets)))
        elif len(self.widgets) >= self.widget_limits*0.8:
            print(f'\t - [!] You used {int((len(self.widgets)/self.widget_limits)*100)}% of max recommended widgets. Consider reducing it.')
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
        return pg.image.load(path)
    
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
    def draw_widgets(self, widgets:list[Widget,]=None):
        """
        Draw a list of widgets
        
        Parameters:
            widgets:list[Widget,]
        Returns:
            None
        """
        if widgets is None or len(widgets) <= 0:
            widgets = self.widgets
            
        for widget in widgets:
            widget.draw()
    def draw_rect(self, pos:tuple[int,int],size:tuple[int,int], color:reqColor,border_width:int=0,border_color:reqColor=None, screen:pg.SurfaceType=None, alpha:int=255) -> pg.Rect:
        """
        Draw a rect on the screen
        
        Parameters:
            rect:pg.Rect
            color:reqColor
            border_width(Optional):int
            screen(Optional):pg.SurfaceType
            alpha(Optional):int
        Returns:
            Rect
        """
        if self.hasScreen():
            rect = pg.Rect(*pos, *size)
            
            color = self.getColor(color)
            
            if screen is None:
                screen = self.getScreen()
            if border_width > 0 and border_color is not None:
                b_color = self.getColor(border_color)
                pg.draw.rect(screen, b_color, rect, border_width)
            s = pg.Surface((rect.size[0]+border_width, rect.size[1]+border_width), pg.SRCALPHA if (alpha < 255 or alpha != None) else 0)
            s.fill(color)
            s.set_alpha(alpha)
            
            r = s.get_rect()
            r.topleft = (rect.left-border_width/2, rect.top-border_width/2)
            
            screen.blit(s, r)
            
            return r

    def draw_circle(self, pos:tuple[int,int], radius:int, color:reqColor, screen:pg.SurfaceType=None, alpha:int=255) -> pg.Rect:
        """
        Draw a circle on the screen
        
        Parameters:
            rect:pg.Rect
            color:reqColor
            screen(Optional):pg.SurfaceType
            alpha(Optional):int
        Returns:
            Rect
        """
        if self.hasScreen():
            rect = pg.Rect(*pos, radius*2, radius*2)
            
            color = self.getColor(color)
            
            if screen is None:
                screen = self.getScreen()
            ss = pg.Surface((radius*2, radius*2), pg.SRCALPHA)
            ss.set_alpha(alpha)
            
            rr = pg.draw.ellipse(ss, color, Rect(0, 0, *rect.size))
            rr.topleft = rect.topleft
            
            screen.blit(ss, rr)
            
            return rr
        return None

    def draw_text(self, position:tuple[int,int],text:str, font:pg.font.FontType, color:reqColor,screen:pg.SurfaceType=None, bgColor:reqColor=None,border_width:int=0,border_color:reqColor=None, alpha:int=255):
        """
        Draw text on the screen
        
        Parameters:
            text:str
            font:pg.font.FontType
            position:tuple[int,int]
            color:reqColor
            screen(Optional):pg.SurfaceType
            bgColor(Optional):reqColor
            alpha(Optional):int
        Returns:
            Rect
        """
        HasBorder = border_width > 0 and border_color is not None
        if self.hasScreen():
            color = self.getColor(color)
            bgColor = self.getColor(bgColor) if bgColor is not None else None
            
            render = font.render(text, True, color, None if HasBorder else bgColor)
            render.set_alpha(alpha)
            
            render_rect = render.get_rect()
            render_rect.topleft = position
            
            if HasBorder:
                b_color = self.getColor(border_color)
                self.draw_rect(render_rect.topleft, render_rect.size, bgColor, border_width, border_color, screen, alpha)
            
            if screen is None:
                self.screen.blit(render, render_rect)
            else:
                screen.blit(render, render_rect)
            
            return render_rect
        return None
    
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
            total_memory = float(self.getRam().replace(' Gb', ''))
            free_memory = float(subprocess.check_output("wmic OS get FreePhysicalMemory", shell=True).decode().split('\n')[1].strip()) # In KBytes
            free_memory /= 1024**2 # In GBytes
            free_memory = round(free_memory,2) # Rounded
            return round((total_memory - free_memory) / total_memory,2)
        else:
            mem_info = subprocess.check_output(['free']).decode('utf-8').split('\n')[1].split()
            total_memory = float(mem_info[1])
            used_memory = float(mem_info[2])
            return round(used_memory / total_memory,2)
# God bless me for continue making this project
# Cu'z i'm getting crazy