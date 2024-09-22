"""
A File designed to work in Widgets for the engine.

- Button;
- Switch;
- Checkbox;
- Slider;
- Textbox;
- Dropdown;
- ProgressBar;
- Image;
- Tip;
"""

from .required import pg
from .l_colors import reqColor
from .objects import cfgtimes,cfgtips, Mouse


"""
Tip System
"""
class Tip():
    """
    Is Basically a tip, that will trigger when you hover over the element that this is setted
    """
    _type:str="tip"
    
    
    engine:any
    rect:pg.Rect = None
    _text:str = None
    
    font:pg.font.FontType = None
    text_lines:list[str,] = []
    total_size:tuple[int,int] = (0,0)
    
    refresh_time_counter = 0
    
    surface:pg.Surface = None
    
    text_changed:bool = False
    def __init__(self, engine,text:str, font:pg.font.FontType):
        self.engine = engine
        self.text = text
        self.font = self.engine._findFont(font)
        
    @property
    def text(self):
        """
        The property that is the text of the tip
        """
        return self._text
    
    @text.setter
    def text(self, text:str):
        self._text = text
        self.text_changed = True
        
    def build_rect(self):
        """
        Will build the base rect for the tip
        """
        if self.rect is None:
            self.rect = pg.Rect(0,0,0,0)
        
        self.rect.width = self.total_size[0] + cfgtips.border_width
        self.rect.height = self.total_size[1] + cfgtips.border_width
        m_pos:tuple[int,int] = self.engine.mouse.pos
        
        m_pos = (m_pos[0] + cfgtips.mouse_distance[0], m_pos[1] + cfgtips.mouse_distance[1])
        
        if self.rect.width + m_pos[0] > self.engine.screen.get_width():
            self.rect.left = m_pos[0] - self.rect.width
        else:
            self.rect.left = m_pos[0]
            
        if self.rect.height + m_pos[1] > self.engine.screen.get_height():
            self.rect.top = m_pos[1] - self.rect.height
        else:
            self.rect.top = m_pos[1]
            
        return self.rect
    
    def strip_text(self):
        """
        This function will make 3 things:
        
        1. Split the text in lines when haves '\n'
        2. Break line when passes max_x
        3. Calculate the total_size(
            width: will get the bigger line width using font,
            height: will get total size of the height of all lines using font too
        )
        """
        mouse_pos: tuple[int, int] = self.engine.getMousePos()
        screen_size: tuple[int, int] = self.engine.screen.get_size()
        
        max_x, max_y = screen_size[0] - (mouse_pos[0]+cfgtips.mouse_distance[0]), screen_size[1] - (mouse_pos[1]+cfgtips.mouse_distance[1])
        
        # Split when haves '\n'
        self.text_lines = self.text.split('\n')
        
        # Break line when passes max_x
        lines_copy = []
        for line in self.text_lines:
            words = line.split(' ')
            current_line = ''
            for x,word in enumerate(words):
                if self.font.size(current_line + ' ' + word)[0] >= max_x:
                    lines_copy.append(current_line)
                    current_line = word
                else:
                    current_line += (' ' if x > 0 else '') + word
            lines_copy.append(current_line)
            
        # Calculate the total size
        self.total_size = (0, 0)
        for line in lines_copy:
            width, height = self.font.size(line)
            self.total_size = (max(self.total_size[0], width) + 3, self.total_size[1] + height + 3)
        
        [(lines_copy.pop(x) if text in ['\n',''] else None) for x,text in enumerate(lines_copy)]
        
        self.text_lines = lines_copy
    
    def update(self):
        """
        Updates the tip. If the refresh time counter is bigger than 0, 
        it will decrement by 1. If the text changed or the refresh time counter
        is equal or less than 0, it will build the rect and strip the text, and
        reset the text changed to False and refresh time counter to the refresh time
        in seconds.
        """
        if self.refresh_time_counter > 0:
            self.refresh_time_counter -= 1
        
        if self.text_changed or self.refresh_time_counter <= 0:
            self.build_rect()
            self.strip_text()
            self.text_changed = False
            self.refresh_time_counter = self.engine.TimeSys.s2f(cfgtips.refresh_time)
            
    def draw(self):
        self.update()
        
        self.surface = pg.Surface(self.total_size, pg.SRCALPHA)
        
        self.engine.draw_rect((0,0), self.total_size, cfgtips.background_color, border_width=cfgtips.border_width, border_color=cfgtips.border_color, screen=self.surface, alpha=cfgtips.alpha)
        position:list = [0,0]
        for line in self.text_lines:
            self.engine.draw_text(position, line, self.font, cfgtips.text_color, screen=self.surface)
            position[1] += self.font.size(line)[1] + 1
            
        self.engine.screen.blit(self.surface, self.rect)
        
"""
Widgets
"""

class Widget(pg.sprite.Sprite):
    """
    Base Widget Class
    
    Used for pre-setup widgets
    """
    _id:str
    _type:str='widget'
    engine:any
    
    position:pg.Vector2 = pg.Vector2(0, 0)
    size:pg.Vector2 = pg.Vector2(0, 0)
    rect:pg.Rect = pg.Rect(0, 0, 0, 0)
    image:pg.Surface = None
    colors:list[reqColor,]
    text:str = ''
    
    alpha:int=255
    
    value:any
    
    tip:Tip = None
    
    _UpdateWhenDraw:bool = True
    def __init__(self, engine,id:str=None, tip:Tip=None):
        """
        Initializes the widget.
        
        Args:
            engine (any): The engine that the widget is in
            id (str, optional): The id of the widget. Defaults to None.
        """
        super().__init__()
        self.engine = engine
        self.engine.addWidget(self)
        
        if id in [' ','',None,'None']:
            self._id = f'{self._type}{len(self.engine.widgets)}'
        else:
            self._id = id
            
        if tip is not None:
            if type(tip) in [list, tuple]:
                self.tip = self.engine.create_tip(*tip)
    
    def build_widget_display(self):
        pass
    
    def cooldown_refresh(self):
        pass
    
    def hovered(self):
        m_pos = self.engine.mouse.pos
        if self.rect.collidepoint(m_pos):
            if self.tip is not None:
                self.tip.draw()
    
    def draw(self):
        self.hovered()
        if self.image is None:
            self.build_widget_display() # First run of the draw, then create the draw object
        if self._UpdateWhenDraw: self.update()
    
    def delete(self):
        self.engine._DeleteWidget(self._id)
        self.kill()
    
    def update(self):
        self.cooldown_refresh()
    
class Button(Widget):
    """
    Button Widget.
    
    For collect valor use: Button.value
    will return a bool value(True/False)
    """
    _type:str = 'button'
    
    
    click_time:int = cfgtimes.WD_BTN_CLICK_TIME
    click_time_counter:int = 0
    
    value:bool = False
    def __init__(self,engine, position:pg.Vector2, font:int or pg.font.FontType, text:str, colors:list[reqColor,reqColor,],id:str=None,alpha:int=255, tip:Tip=None): # type: ignore
        """
        Button Widget, can be very useful
        
        Args:
            engine (any): The engine that the widget is in
            position (pg.Vector2): The position of the button
            font (int or pg.font.FontType): The font of the button
            text (str): The text of the button
            colors (list[reqColor,reqColor,]): The colors of the button
            id (str, optional): The id of the widget. Defaults to None.
            alpha (int, optional): The alpha of the button. Defaults to 255.
        """
        super().__init__(engine,id,tip)
        self.position = position
        self.font:pg.font.FontType = self.engine._findFont(font)
        self.text = text
        self.colors = colors
        self.alpha = alpha
        
    def build_widget_display(self):
        # First get the size of the text
        font:pg.font.FontType = self.engine._findFont(self.font)
        self.size = pg.math.Vector2(*font.size(self.text))
        
        self.image = pg.Surface(self.size, (pg.SRCALPHA if (self.alpha < 255 or self.alpha != None) else 0))
        if len(self.colors) < 3: # Has only 2 colors
            self.engine.draw_rect((0,0), self.size, self.colors[1], screen=self.image, alpha=self.alpha)
        elif len(self.colors) == 3: # Has 3 colors
            self.engine.draw_rect((0,0), self.size, self.colors[1], border_width=3, border_color=self.colors[2], screen=self.image, alpha=self.alpha)
            
        self.engine.draw_text((0,0),self.text, self.font, self.colors[0], screen=self.image, alpha=self.alpha)
        self.rect = pg.Rect(*self.position,*self.size)
        
    def update(self):
        if self.rect.collidepoint(self.engine.mouse.pos):
            if self.engine.mouse.left:
                if self.click_time_counter <= 0:
                    self.click_time_counter = self.engine.TimeSys.s2f(self.click_time) # Reset Timer
                    self.value = True
                else:
                    self.value = False
            else:
                self.value = False
        else:
            self.value = False
        
        return super().update()
        
    def cooldown_refresh(self):
        if self.click_time_counter > 0:
            self.click_time_counter -= 1
            
    def draw(self):
        if self.image and self.rect:
            self.engine.screen.blit(self.image, self.rect)
        
        return super().draw()
    
class Checkbox(Widget):
    """
    Checkbox Widget.
    
    For collect valor use: Checkbox.value
    will return a bool value(True/False)
    
    Click, True, Click, False, Click, True
    Checkbox!
    """
    _type:str = 'checkbox'
    
    click_time:int = cfgtimes.WD_CKBX_CLICK_TIME
    click_time_counter:int = 0
    
    box_size:int # Default -> 1/4 of wid
    
    value:bool = False
    def __init__(self,engine, position:pg.Vector2, font:int or pg.font.FontType, text:str, colors:list[reqColor,reqColor,reqColor,],id:str=None,alpha:int=255, tip:Tip=None): # type: ignore
        """
        Checkbox Widget, can be very useful
        
        Args:
            engine (any): The engine that the widget is in
            position (pg.Vector2): The position of the checkbox
            font (int or pg.font.FontType): The font of the checkbox
            text (str): The text of the checkbox
            colors (list[reqColor,reqColor,reqColor,]): The colors of the checkbox
            id (str, optional): The id of the widget. Defaults to None.
            alpha (int, optional): The alpha of the checkbox. Defaults to 255.
        """
        super().__init__(engine,id,tip)
        self.position = position
        self.font:pg.font.FontType = self.engine._findFont(font)
        self.text = text
        self.colors = colors
        self.alpha = alpha
        
    def build_widget_display(self):
        # Colors: 0(Font),1(Disable), 2(Enable), 3(Background),4(Border)
        self.size = pg.math.Vector2(*self.font.size(self.text))
        
        # Add Box Size
        self.box_size = int(self.size.x / 4)
        self.size.x += int(self.box_size * 1.15)
        
        # Create Image
        self.image = pg.Surface(self.size, pg.SRCALPHA)
        
        # Insert Text
        self.engine.draw_text((int(self.box_size * 1.15),0),self.text, self.font, self.colors[0], screen=self.image, alpha=self.alpha)
        
        # Defines
        self.rect = pg.Rect(*self.position,*self.size)
        
    
    def update(self):
        if self.rect.collidepoint(self.engine.mouse.pos):
            if self.engine.mouse.left:
                if self.click_time_counter <= 0:
                    self.value = not self.value
                    self.click_time_counter = self.engine.TimeSys.s2f(self.click_time) # Reset Timer
        return super().update()
    
    def cooldown_refresh(self):
        if self.click_time_counter > 0:
            self.click_time_counter -= 1
            
    def draw(self):
        if self.image and self.rect:
            self.engine.screen.blit(self.image, self.rect)

            # Draw box
            c = self.colors[1] if not self.value else self.colors[2]
            self.engine.draw_rect(self.rect.topleft, (self.box_size, self.size.y), c,border_width=(3 if len(self.colors) > 3 else 0),border_color= (self.colors[3] if len(self.colors) > 3 else (0,0,0)), alpha=self.alpha)
        
        return super().draw()
    
class Slider(Widget):
    """
    Slider Widget.
    
    Value beetween 0 and 1
    collect from _value or value - Float
    """
    _type:str = 'slider'
    
    circle:pg.Rect = None
    ball_size:int = 10
    
    fill_passed:bool = True
    
    _value:float = None
    value:float = 0
    def __init__(self,engine, position:[int,int], size:tuple[int,int],colors:list[reqColor,reqColor,],value:float=None,fill_passed:bool=True,id:str=None,alpha:int=255, tip:Tip=None): # type: ignore
        """
        Slider Widget, is very useful
        
        Args:
            engine (any): The engine that the widget is in
            position (pg.Vector2): The position of the slider
            size (tuple[int,int]): The size of the slider
            colors (list[reqColor,reqColor,]): The colors of the slider
            value (float, optional): The value of the slider. Defaults to None.
            fill_passed (bool, optional): If the slider should fill the passed area. Defaults to True.
            id (str, optional): The id of the widget. Defaults to None.
            alpha (int, optional): The alpha of the slider. Defaults to 255.
        """
        super().__init__(engine,id,tip)
        self.position = position
        self.size = size
        self.colors = colors
        self.alpha = alpha
        if value is not None:
            self._value = value
        
        self.fill_passed = fill_passed
        
    def build_widget_display(self):
        
        self.ball_size = self.size[1]//2 + 5
        self.image = pg.Surface(self.size, pg.SRCALPHA)
        
        self.engine.draw_rect((0,0),self.size,self.colors[1], screen=self.image, alpha=self.alpha, border_width=(3 if len(self.colors) >= 3 else 0),border_color= (self.colors[2] if len(self.colors) >= 3 else (0,0,0)))
        
        self.rect = pg.Rect(*self.position,*self.size)
        
        if self._value is not None:
            # Value is between 0 and 1
            # make the cur position beetween min pos and max pos using the value as percentage
            # Value only will interact with the X vector
            self.currentPosition = [self.rect.x + self._value * (self.rect.width - self.ball_size), self.rect.y - self.ball_size//4] # Fixed.
        else:
            self.currentPosition = [self.rect.x + self.ball_size//2, self.rect.y - self.ball_size//4]
    
    def update(self):
        if self.circle:
            if self.circle.collidepoint(self.engine.mouse.pos):
                if self.engine.mouse.left:
                    self.currentPosition[0] = self.engine.mouse.x - self.circle.width/2
                    # Limit X Right
                    if self.currentPosition[0] > self.rect.x + self.rect.width - self.ball_size/2:
                        self.currentPosition[0] = self.rect.x + self.rect.width - self.ball_size/2
                    elif self.currentPosition[0] < self.rect.x - self.ball_size/2:# Limit X Left
                        self.currentPosition[0] = self.rect.x - self.ball_size/2
                    
        # Calculate the value (float beetween 0 and 1)
        
        # Get the value beetween 0 and max size
        a = self.rect.width - self.rect.x # Min 0, Max Width
        b = self.currentPosition[0] - self.rect.x
        v = b / a
        if v < 0: v = 0
        elif v > 1: v = 1
        self.value = round(v,2)
                        
                    
        return super().update()
    
    def draw(self):
        
        if self.image and self.rect:
            self.engine.screen.blit(self.image, self.rect)
            
            # Fill passed
            
            if self.fill_passed:
                w = self.currentPosition[0]-self.rect.x
                self.engine.draw_rect((self.rect.x, self.rect.y), (0 if w < 0 else w+self.ball_size/2, self.rect.height), self.colors[0] if len(self.colors) < 4 else self.colors[3], alpha=self.alpha)
            
            self.circle = self.engine.draw_circle(self.currentPosition,self.ball_size, self.colors[0], alpha=self.alpha)
        
        return super().draw()

class Select(Widget):
    """
    Select Widget.
    
    It's like choose a item, Left or Right.
    """
    _type:str = 'select'
    
    leftButton:Button = None
    rightButton:Button = None
    button_click_time = cfgtimes.WD_SLCT_CLICK_TIME
    
    items:list=[]
    value:int=0
    textBg:bool = False
    
    def __init__(self, engine, position: [int, int], font: int or pg.font.FontType,colors: list[reqColor, reqColor,], items: list ,value:int=0, textBg:bool = False,id: str = None, alpha: int = 255, tip:Tip=None): # type: ignore
        """
        Select Widget.
        
        It's like choose a item, Left or Right.
        
        Args:
            engine (any): The engine that the widget is in
            position (pg.Vector2): The position of the select
            font (int or pg.font.FontType): The font of the select
            colors (list[reqColor,reqColor,]): The colors of the select
            items (list): The items of the select
            value (int, optional): The value of the select. Defaults to 0.
            textBg (bool, optional): If the text background is enabled. Defaults to False.
            id (str, optional): The id of the widget. Defaults to None.
            alpha (int, optional): The alpha of the select. Defaults to 255.
        """
        super().__init__(engine, id,tip)
        self.position = position
        self.font:pg.font.FontType = self.engine._findFont(font)
        self.colors = colors
        self.items = items
        self.value = value
        self.alpha = alpha
        self.textBg = textBg
        
    def build_widget_display(self):
        self.size = self.font.size(self.items[self.value])
        
        self.leftButton = Button(self.engine, (self.position[0],self.position[1]), self.font, '<', self.colors, alpha=self.alpha, id=f'{self._id}_left')
        self.rightButton = Button(self.engine, (self.position[0],self.position[1]), self.font, '>', self.colors, alpha=self.alpha, id=f'{self._id}_right')
        
        self.leftButton.click_time = self.button_click_time
        self.rightButton.click_time = self.button_click_time
        
        self.rect = pg.Rect(*self.position,*self.size)
        
        self.image = pg.Surface(self.size, pg.SRCALPHA)
        
    
    def update(self):
        if self.leftButton and self.rightButton:
            if self.leftButton.value:
                self.value -= 1
                if self.value < 0:
                    self.value = len(self.items) - 1
                
            if self.rightButton.value:
                self.value += 1
                if self.value >= len(self.items):
                    self.value = 0
                
            
            self.size = self.font.size(str(self.items[self.value]))
            self.rect = pg.Rect(*self.position,*self.size)
        return super().update()
    
    def draw(self):
        
        if self.leftButton and self.rightButton:
            self.leftButton.rect.right = self.rect.left - 5
            self.rightButton.rect.left = self.rect.right + 5
            
            self.engine.draw_text((self.rect.left,self.rect.top),str(self.items[self.value]), self.font, self.colors[0],bgColor=self.colors[1],border_width=3,border_color=self.colors[2], alpha=self.alpha)
            # Draw buttons independant of list widgets // Fix
            self.leftButton.draw()
            self.rightButton.draw()        
        return super().draw()
    
class Longtext(Widget):
    """
    LongText Widget.
    
    It's like a textarea.
    """
    _type:str = 'longtext'
    
    lines:list[str,] = []
    auto_size:bool = False
    
    def __init__(self, engine, position: [int,int], font: int or pg.font.FontType,text:str,colors: list[reqColor,],size: [int, int] = None,id: str = None, alpha: int = 255, tip:Tip=None): # type: ignore
        """
        It's like a textarea but you can't type.
        
        Args:
            engine (any): The engine that the widget is in
            position (tuple[int,int]): The position of the textarea
            font (int or pg.font.FontType): The font of the textarea
            text (str): The text of the textarea
            colors (list[reqColor,]): The colors of the textarea
            size (list[int, int], optional): The size of the textarea. Defaults to None.
            id (str, optional): The id of the widget. Defaults to None.
            alpha (int, optional): The alpha of the textarea. Defaults to 255.
        """
        super().__init__(engine, id, tip)
        self.position = position
        self.font:pg.font.FontType = self.engine._findFont(font)
        self.colors = colors
        if size == None:
            self.auto_size = True
            self.size = (0,0)
        else:
            self.size = size
        self.text = text
        self.alpha = alpha
    
    def get_lines(self) -> dict:
        """
        - Get the lines of the text;
        - Break the lines when it's too long;
        """
        lines = {}
        current_line = ''
        self.text = self.text.replace('\n',' ')
        for word in self.text.split(' '):
            if pg.font.Font.size(self.font, current_line + word)[0] > self.engine.screen.get_size()[0] - self.position[0]:
                lines[len(lines) + 1] = current_line
                current_line = word + ' '
            else:
                current_line += word + ' '
        lines[len(lines) + 1] = current_line.strip()
        return lines

    
    def build_widget_display(self):
        """
        Basically this will limit the text to only show to the border of screen, and if this is too long, it will break to the next line, and will get the line with the biggest width as self.size[0]
        and the total height of lines as self.size[1]
        
        but only if self.auto_size is True
        else it will get the size of the text and bypass the screen size
        """
        if self.auto_size:
            lines = self.get_lines()
            
            max_size = 0
            for line in lines.values():
                if pg.font.Font.size(self.font, line)[0] > max_size:
                    max_size = pg.font.Font.size(self.font, line)[0]
            
            self.text = [line for line in lines.values()]
            self.size = (max_size, (len(self.text) * pg.font.Font.size(self.font, 'W')[1])+5)
            
        self.image = pg.Surface(self.size, pg.SRCALPHA)
        self.rect = pg.Rect(*self.position,*self.size)
        if len(self.colors) > 1:
            self.engine.draw_rect((0,0), self.size, self.colors[1], border_width=3 if len(self.colors) > 2 else 0, border_color=self.colors[2] if len(self.colors) > 2 else None,alpha=self.alpha, screen=self.image)
        for i, line in enumerate(self.text):
            self.engine.draw_text((0,(i*pg.font.Font.size(self.font, 'W')[1])),line, self.font, self.colors[0],alpha=self.alpha, screen=self.image)
            
    def draw(self):
        if self.image and self.rect:
            self.engine.screen.blit(self.image, self.rect)
        return super().draw()
    
class Progressbar(Widget):
    _type:str = 'progressbar'
    
    colors:list[reqColor,reqColor,reqColor,] = []
    text:str = None
    font:pg.font.FontType = None
    
    value:float = 0
    def __init__(self, engine,position:tuple[int,int],size:tuple[int,int],colors:list[reqColor,reqColor,reqColor,],value:float=0,text:str=None,font:pg.font.FontType=None, id: str = None, tip:Tip=None):
        """
        A Progress bar, can be used for make a loading bar or life bars
        
        Args:
            engine (any): The engine that the widget is in
            position (pg.Vector2): The position of the widget
            size (tuple[int,int]): The size of the widget
            colors (list[reqColor,reqColor,reqColor,]): The colors of the widget
            value (float, optional): The value of the widget. Defaults to 0.
            text (str, optional): The text of the widget. Defaults to None.
            id (str, optional): The id of the widget. Defaults to None.
        """
        super().__init__(engine, id, tip)
        self.position = position
        self.size = size
        self.colors = colors
        self.text = text
        self.value = value
        self.font = font
        
    def build_widget_display(self):
        self.rect = pg.Rect(*self.position,*self.size)
        self.image = pg.Surface(self.size, pg.SRCALPHA)
        
    def draw(self):
        if self.image and self.rect:
            if self.value < 0:
                self.value = 0
            elif self.value > 1:
                self.value = 1
            # Background with border
            self.engine.draw_rect(self.rect.topleft, self.rect.size, self.colors[1], border_width=3, border_color=self.colors[2])
            
            # Fill bar
            self.engine.draw_rect(self.rect.topleft, (self.rect.width * self.value, self.rect.height), self.colors[0])
            
            if self.text and (self.font and len(self.colors) > 3):
                self.engine.draw_text((self.rect.left+1, self.rect.top+1),str(self.text), self.font, self.colors[3])
        return super().draw()
    
class Textbox(Widget):
    _type:str = 'textbox'
    
    colors:list[reqColor,reqColor,reqColor,] = []
    text:str = None
    font:pg.font.FontType = None
    height:int = 0
    max_width:int = 0
    active = False
    
    del_press_time:int = cfgtimes.WD_TXBX_DEL_TIME
    del_press_counter:int = 0
    
    key_press_time:int = cfgtimes.WD_TXBX_KEYP_TIME
    key_press_counter:int = 0
    
    click_time:int = cfgtimes.WD_TXBX_CLICK_TIME
    click_counter:int = 0
    
    blacklist = [
        pg.K_BACKSPACE,
        pg.K_DELETE,
        pg.K_LEFT,
        pg.K_RIGHT,
        pg.K_UP,
        pg.K_DOWN,
        pg.K_LCTRL, pg.K_RCTRL,
        pg.K_LALT, pg.K_RALT,
    ]
    def __init__(self, engine,position:tuple[int,int],height:int,colors:list[reqColor,reqColor,reqColor,],font:pg.font.FontType,text:str=None,alpha:int=255, id: str = None, tip:Tip=None):
        """
        A Textbox, you can write in it.
        
        Args:
            engine (any): The engine that the widget is in
            position (pg.Vector2): The position of the widget
            height (int): The height of the widget
            colors (list[reqColor,reqColor,reqColor,]): The colors of the widget (Background Unactive, Background Active, Text, Border)
            font (pg.font.FontType): The font of the widget. Defaults to None.
            text (str, optional): The text of the widget. Defaults to None.
            alpha (int, optional): The alpha of the widget. Defaults to 255.
            id (str, optional): The id of the widget. Defaults to None.
        """
        super().__init__(engine, id, tip)
        self.position:tuple[int,int] = position
        self.height:int = height
        self.colors:list[reqColor,reqColor,] = colors
        self.text:str = text
        self.font:pg.font.FontType = self.engine._findFont(font)
        self.alpha:int = alpha
        
    def build_widget_display(self):
        self.max_width = self.engine.screen.get_width() - self.position[0]
        self.image = pg.Surface((0,0))
        self.rect = pg.Rect(*self.position,self.max_width,self.height)
        
    def update(self):
        # Update Size
        size = self.font.size(self.text)
        w,h = size[0]+5,size[1]
        if h > self.height:
            self.height = h+2
        self.rect.size = (self.font.size('WW')[0] if w < self.font.size('WW')[0] else w,h+2)
        
        # Update Value
        self.value = self.text
        
        # Get mouse and update if is active or no
        if self.engine.mouse.left:
            if self.click_counter <= 0:
                if self.rect.collidepoint(self.engine.mouse.pos):
                    if not self.active:
                        self.click_counter = self.engine.TimeSys.s2f(self.click_time) # Reset Timer
                        self.active = True
                else:
                    self.active = False
        
        if self.active:
            if self.key_press_counter <= 0 or self.del_press_counter <= 0:    
                keys:pg.key.ScancodeWrapper = self.engine.getKeys() # Get Keys pressed
                if keys[pg.K_BACKSPACE] and self.del_press_counter <= 0:
                    self.text = self.text[:-1] # Remove last character
                    self.del_press_counter = self.engine.TimeSys.s2f(self.del_press_time)
                elif keys[pg.K_RETURN] and self.key_press_counter <= 0:
                    self.active = False
                    self.key_press_counter = self.engine.TimeSys.s2f(self.key_press_time)
                elif self.key_press_counter <= 0:
                    for ev in self.engine.events:
                        if ev.type == pg.KEYDOWN:
                            if not (ev.key in self.blacklist):
                                self.text += ev.unicode
                            self.key_press_counter = self.engine.TimeSys.s2f(self.key_press_time)
                            
        
        
        return super().update()
    
    def cooldown_refresh(self):
        if self.key_press_counter > 0:
            self.key_press_counter -= 1
        if self.click_counter > 0:
            self.click_counter -= 1
        if self.del_press_counter > 0:
            self.del_press_counter -= 1
        return super().cooldown_refresh()
    
    def draw(self):
        if self.image:
            self.engine.draw_rect(self.rect.topleft, self.rect.size, self.colors[0] if not self.active else self.colors[1], border_width=3 if len(self.colors) > 3 else 0, border_color=self.colors[2] if len(self.colors) > 3 else None,alpha=self.alpha)
            self.engine.draw_text((self.rect.left+2.5, self.rect.top+1),self.text, self.font, self.colors[2],alpha=self.alpha)
        return super().draw()
    
class Dropdown(Widget):
    _type:str = 'dropdown'
    
    colors:list[reqColor,reqColor,reqColor,] = []
    texts:list[str,] = []
    current_text:int = 0
    font:pg.font.FontType = None
    position:tuple[int,int] = (0,0)
    
    texts_rects:list[tuple[pg.rect.RectType, int]] = [] # The Rect of text, Index of text
    
    rect:pg.Rect = None
    
    active:bool = False
    
    update_delay_count:int = 0
    Click_Time_counter:int = 0
    def __init__(self, engine, position:tuple[int,int], colors:list[reqColor,reqColor,reqColor,], texts:list[str,], font:pg.font.FontType, alpha:int=255, current_text:int=0,id:str=None, tip:Tip=None):
        """
        Dropdown widget, is a dropdown when you click you can choose one of the items listed.
        
        Args:
            position:tuple[int,int]
            colors:list[reqColor,reqColor,reqColor,]
            texts:list[str,]
            font:pg.font.FontType
            alpha:int
            current_text:int
            id:str
            tip:Tip
        """
        super().__init__(engine, id, tip)
        
        self.position:tuple = position
        self.colors:list = colors
        self.texts:list = texts
        self.font:pg.font.FontType = font
        self.alpha:int = alpha
        self.current_text:int = current_text
        
        self.build_widget_display()
        
    def build_widget_display(self):
        # Set the rect for the new one
        self.rect = pg.Rect(*self.position, self.font.size(self.texts[self.current_text])[0]+4, self.font.size(self.texts[self.current_text])[1]+2)
        
        width,height = self.rect.size
        
        # Set width to be the width of the longest text
        for text in self.texts:
            if self.font.size(text)[0]+4 > width:
                width = self.font.size(text)[0]+4
        
        self.surface = pg.Surface((width,height), pg.SRCALPHA)
        
        if self.active:
            self.texts_rects.clear()
            height += (self.font.size(self.texts[self.current_text])[1]*((len(self.texts)-1) if len(self.texts) > 1 else 1))+2
            
            self.surface = pg.Surface((width,height), pg.SRCALPHA)
            
            self.engine.draw_rect((0,self.rect.height), (width,height-self.rect.height), self.colors[1], border_width=3 if len(self.colors) > 2 else 0, border_color=self.colors[2] if len(self.colors) > 2 else (0,0,0), alpha=self.alpha if self.alpha < 255 else 200, screen=self.surface)
            pos = [2,self.rect.height+2]
            for x,line in enumerate(self.texts):
                if x != self.current_text:
                    r = self.engine.draw_text((pos[0], pos[1]), str(line), self.font, self.colors[0], screen=self.surface, alpha=self.alpha)
                    r.topleft = (pos[0]+self.position[0],pos[1]+self.position[1])
                    self.texts_rects.append((r,x))
                    pos[1] += self.font.size(line)[1]
        
        self.surface.set_alpha(self.alpha)
        
        self.engine.draw_rect((0,0), self.rect.size, self.colors[1], border_width=3 if len(self.colors) > 2 else 0, border_color=self.colors[2] if len(self.colors) > 2 else (0,0,0), alpha=self.alpha, screen=self.surface)
        self.engine.draw_text((2, 1),self.texts[self.current_text], self.font, self.colors[0], screen=self.surface, alpha=self.alpha)
        
        # self.rect.size = (width,height)
    
    def update_wd(self):
        self.build_widget_display()
    
    def hovered(self):
        if self.engine.mouse.left and self.Click_Time_counter <= 0:
            if self.rect.collidepoint(self.engine.mouse.pos):
                self.active = not self.active
                self.update_wd()
            else:
                if self.active:
                    passed:bool = False
                    for rect, index in self.texts_rects:
                        if rect.collidepoint(self.engine.mouse.pos):
                            self.current_text = index
                            passed = True
                            
                    if not passed:
                        self.active = False
                else:
                    self.active = False
            self.Click_Time_counter = self.engine.TimeSys.s2f(cfgtimes.WD_DPDW_CLICK_TIME)
        return super().hovered()
        
    def update(self):
        if self.Click_Time_counter > 0:
            self.Click_Time_counter -= 1
        
        super().update()
    
    def draw(self):
        self.engine.screen.blit(self.surface, self.rect.topleft)
        return super().draw()
    
class Textarea(Widget):
    _type:str = 'textarea'
    
    colors:list[reqColor,reqColor,reqColor,] = []
    text:str = None
    shown_text:list[str,] = []
    font:pg.font.FontType = None
    active = False
    
    del_press_time:int = cfgtimes.WD_TXBX_DEL_TIME
    del_press_counter:int = 0
    
    key_press_time:int = cfgtimes.WD_TXBX_KEYP_TIME
    key_press_counter:int = 0
    
    click_time:int = cfgtimes.WD_TXBX_CLICK_TIME
    click_counter:int = 0
    total_size:tuple[int,int] = (0,0)
    
    blacklist = [
        pg.K_BACKSPACE,
        pg.K_DELETE,
        pg.K_LEFT,
        pg.K_RIGHT,
        pg.K_UP,
        pg.K_DOWN,
        pg.K_LCTRL, pg.K_RCTRL,
        pg.K_LALT, pg.K_RALT,
    ]
    def __init__(self, engine,position:tuple[int,int],colors:list[reqColor,reqColor,reqColor,],font:pg.font.FontType,text:str=None,alpha:int=255, id: str = None, tip:Tip=None):
        """
        A Textarea, is basically a **textbox**, but will break when have a "\n" or pass the screen size.
        
        Args:
            engine:Engine
            position:tuple[int,int]
            height:int
            colors:list[reqColor,reqColor,reqColor,]
            font:pg.font.FontType
            text:str
            alpha:int
            id:str
            tip:Tip
        """
        super().__init__(engine,id,tip)
        self.position:tuple[int,int] = position
        self.colors:list[reqColor,reqColor,] = colors
        self.text:str = text
        self.font:pg.font.FontType = self.engine._findFont(font)
        self.alpha:int = alpha
        
        self.strip_text()
    
    def strip_text(self):
        """
        This function will make 3 things:
        
        1. Split the text in lines when haves '\n'
        2. Break line when passes max_x
        3. Calculate the total_size(
            width: will get the bigger line width using font,
            height: will get total size of the height of all lines using font too
        )
        """
        screen_size: tuple[int, int] = self.engine.screen.get_size()
        
        max_x, max_y = screen_size[0] - self.position[0], screen_size[1] - self.position[1]
        
        # Split when haves '\n'
        self.shown_text = self.text.replace('\r','').split('\n')
        
        # Break line when passes max_x
        lines_copy = []
        for line in self.shown_text:
            words = line.split(' ')
            current_line = ''
            for x,word in enumerate(words):
                if self.font.size(current_line + ' ' + word)[0] >= max_x:
                    lines_copy.append(current_line)
                    current_line = word
                    self.build_widget_display()
                else:
                    current_line += (' ' if x > 0 else '') + word
            lines_copy.append(current_line)
            
        # Calculate the total size
        self.total_size = (0, 0)
        for line in lines_copy:
            width, height = self.font.size(line)
            self.total_size = (max(self.total_size[0], width) + 3, self.total_size[1] + height + 3)
        
        [(lines_copy.pop(x) if text in ['\n','\r',''] else None) for x,text in enumerate(lines_copy)]
        
        self.shown_text = lines_copy
        
    def update(self):
        # Update Value
        self.value = self.text
        
        # Get mouse and update if is active or no
        if self.engine.mouse.left:
            if self.click_counter <= 0:
                if self.rect.collidepoint(self.engine.mouse.pos):
                    if not self.active:
                        self.click_counter = self.engine.TimeSys.s2f(self.click_time) # Reset Timer
                        self.active = True
                else:
                    self.active = False
        
        if self.active:
            if self.key_press_counter <= 0 or self.del_press_counter <= 0:    
                changed = False
                keys:pg.key.ScancodeWrapper = self.engine.getKeys() # Get Keys pressed
                if keys[pg.K_BACKSPACE] and self.del_press_counter <= 0:
                    self.text = self.text[:-1] # Remove last character
                    self.del_press_counter = self.engine.TimeSys.s2f(self.del_press_time)
                    changed = True
                elif keys[pg.K_RETURN] and self.key_press_counter <= 0:
                    self.active = False
                    self.key_press_counter = self.engine.TimeSys.s2f(self.key_press_time)
                    changed = True
                elif self.key_press_counter <= 0:
                    for ev in self.engine.events:
                        if ev.type == pg.KEYDOWN:
                            if not (ev.key in self.blacklist):
                                self.text += ev.unicode
                            self.key_press_counter = self.engine.TimeSys.s2f(self.key_press_time)
                            changed = True
                            
                if changed:
                    self.strip_text()
        
        return super().update()
    
    def cooldown_refresh(self):
        if self.key_press_counter > 0:
            self.key_press_counter -= 1
        if self.click_counter > 0:
            self.click_counter -= 1
        if self.del_press_counter > 0:
            self.del_press_counter -= 1
        return super().cooldown_refresh()
    
    def draw(self):
        self.rect = pg.Rect(*self.position,*self.total_size)
        self.engine.draw_rect(self.rect.topleft, self.rect.size, self.colors[0] if not self.active else self.colors[1], border_width=3 if len(self.colors) > 3 else 0, border_color=self.colors[2] if len(self.colors) > 3 else None,alpha=self.alpha)
        for ind,line in enumerate(self.shown_text):
            self.engine.draw_text((self.rect.left+1.5, self.rect.top+1+(ind*self.font.get_height())),line, self.font, self.colors[2],alpha=self.alpha)
        return super().draw()