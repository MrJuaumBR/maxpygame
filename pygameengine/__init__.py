"""
Main file for PyGameEngine.
"""

from .required import *
from .objects import *
from .widgets import *
from .l_colors import Colors as ccc
from .l_colors import reqColor

class PyGameEngine:
    meta:Metadata = Metadata()
    Colors:ccc
    TimeSys:any
    # PyGame Functions
    screen:pg.SurfaceType=None # Screen
    clock:pg.time.Clock=None # Clock
    
    # Engine Variables
    fps:int=60
    _rfps:float=0
    widgets:list[Widget,] = []
    fonts:list[pg.font.FontType,] = []
    
    def __init__(self,screen:pg.SurfaceType=None):
        pg.init()
        print(f"{self.meta.name} - {self.meta.version}\n\t - {self.meta.author}")
        self.screen = screen
        self.clock = pg.time.Clock()
        self.Colors = ccc()
        self.TimeSys = TimeSys()
    
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
            return reqColor(hex=color).rgb.rgb()
        else:
            try:
                return color.rgb.rgb()
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
            self.screen = pg.display.set_mode((width, height), flags)
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
        return pg.event.get()
    def getKeys(self) -> list[bool]:
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
        pg.quit()
        sys.exit()
        
    def update(self, target:pg.SurfaceType=None):
        """
        Update the screen if there is one, if not try to update the target
        
        Parameters:
            target(Optional):pg.SurfaceType
        Returns:
            None
        """
        if self.hasScreen() and target is None:
            pg.display.update(self.screen)
        elif target:
            pg.display.update(target)
    
    def fpsw(self):
        self.clock.tick(self.fps)
        self._rfps = self.clock.get_fps()
        
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
                fill_color:reqColor = fill_color.rgb.rgb()
            self.screen.fill(fill_color)
    
    def flip(self):
        """
        Flip the screen if there is one
        
        Parameters:
            None
        Returns:
            None
        """
        if self.hasScreen():
            self.screen.flip()
            
    # Font System
    def _findFont(self, font:pg.font.FontType) -> int:
        """
        Find the font in the list of fonts
        
        Parameters:
            font:pg.font.FontType
        Returns:
            int
        """
        if type(font) != int:
            return self.fonts.index(font)
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
        self.widgets.append(widget)
        
    def create_widget(self, widget_type:str, *args, **kwargs) -> Widget:
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
            s = pg.Surface((rect.size[0]-border_width, rect.size[1]-border_width), pg.SRCALPHA if (alpha < 255 or alpha != None) else 0)
            s.fill(color)
            s.set_alpha(alpha)
            
            r = s.get_rect()
            r.topleft = (rect.x+(border_width//2), rect.y+(border_width//2))
            
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

    def draw_text(self, position:tuple[int,int],text:str, font:pg.font.FontType, color:reqColor,screen:pg.SurfaceType=None, bgColor:reqColor=None, alpha:int=255):
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
        if self.hasScreen():
            color = self.getColor(color)
            bgColor = self.getColor(bgColor) if bgColor is not None else None
            
            render = font.render(text, True, color, bgColor)
            render.set_alpha(alpha)
            
            render_rect = render.get_rect()
            render_rect.topleft = position
            
            if screen is None:
                self.screen.blit(render, render_rect)
            else:
                screen.blit(render, render_rect)
            
            return render_rect