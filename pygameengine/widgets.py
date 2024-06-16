"""
A File designed to work in Widgets for the engine.

- Button;
- Switch;
- Checkbox;
- Slider;
- Textbox;
- Dropdown;
- Image;
"""

from .required import pg
from .l_colors import reqColor

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
    
    _UpdateWhenDraw:bool = True
    def __init__(self, engine,id:str=None):
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
    
    def build_widget_display(self):
        pass
    
    def cooldown_refresh(self):
        pass
    
    def draw(self):
        if self.image is None:
            self.build_widget_display() # First run of the draw, then create the draw object
        if self._UpdateWhenDraw: self.update()
    
    def update(self):
        self.cooldown_refresh()
    
class Button(Widget):
    """
    Button Widget.
    
    For collect valor use: Button.value
    will return a bool value(True/False)
    """
    _type:str = 'button'
    
    
    click_time:int = 0.15 # Default -> 0.15s
    click_time_counter:int = 0
    
    value:bool = False
    def __init__(self,engine, position:pg.Vector2, font:int or pg.font.FontType, text:str, colors:list[reqColor,reqColor,],id:str=None,alpha:int=255): # type: ignore
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
        super().__init__(engine,id)
        self.position = position
        self.font:pg.font.FontType = self.engine.fonts[self.engine._findFont(font)]
        self.text = text
        self.colors = colors
        self.alpha = alpha
        
    def build_widget_display(self):
        # First get the size of the text
        font:pg.font.FontType = self.engine.fonts[self.engine._findFont(self.font)]
        self.size = pg.math.Vector2(*font.size(self.text))
        
        self.image = pg.Surface(self.size, (pg.SRCALPHA if (self.alpha < 255 or self.alpha != None) else 0))
        if len(self.colors) < 3: # Has only 2 colors
            self.engine.draw_rect((0,0), self.size, self.colors[1], screen=self.image, alpha=self.alpha)
        elif len(self.colors) == 3: # Has 3 colors
            self.engine.draw_rect((0,0), self.size, self.colors[1], border_width=3, border_color=self.colors[2], screen=self.image, alpha=self.alpha)
            
        self.engine.draw_text((0,0),self.text, self.font, self.colors[0], screen=self.image, alpha=self.alpha)
        self.rect = pg.Rect(*self.position,*self.size)
        
    def update(self):
        m_pos = self.engine.getMousePos()
        if self.rect.collidepoint(m_pos):
            m_press = self.engine.getMousePressed()
            if m_press[0]:
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
    
    click_time:int =0.5 # Default -> 0.5s
    click_time_counter:int = 0
    
    box_size:int # Default -> 1/4 of wid
    
    value:bool = False
    def __init__(self,engine, position:pg.Vector2, font:int or pg.font.FontType, text:str, colors:list[reqColor,reqColor,reqColor,],id:str=None,alpha:int=255): # type: ignore
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
        super().__init__(engine,id)
        self.position = position
        self.font:pg.font.FontType = self.engine.fonts[self.engine._findFont(font)]
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
        m_pos = self.engine.getMousePos()
        if self.rect.collidepoint(m_pos):
            m_press = self.engine.getMousePressed()
            if m_press[0]:
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
    def __init__(self,engine, position:[int,int], size:tuple[int,int],colors:list[reqColor,reqColor,],value:float=None,fill_passed:bool=True,id:str=None,alpha:int=255): # type: ignore
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
        super().__init__(engine,id)
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
            m_pos = self.engine.getMousePos()
            if self.circle.collidepoint(m_pos):
                m_press = self.engine.getMousePressed()
                if m_press[0]:
                    self.currentPosition[0] = m_pos[0] - self.circle.width/2
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
                self.engine.draw_rect((self.rect.x, self.rect.y), ((self.rect.width * self.value)+5, self.rect.height), self.colors[0] if len(self.colors) < 4 else self.colors[3], alpha=self.alpha)
            
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
    
    items:list=[]
    value:int=0
    textBg:bool = False
    
    def __init__(self, engine, position: [int, int], font: int or pg.font.FontType,colors: list[reqColor, reqColor,], items: list ,value:int=0, textBg:bool = False,id: str = None, alpha: int = 255,): # type: ignore
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
        super().__init__(engine, id)
        self.position = position
        self.font:pg.font.FontType = self.engine.fonts[self.engine._findFont(font)]
        self.colors = colors
        self.items = items
        self.value = value
        self.alpha = alpha
        self.textBg = textBg
        
    def build_widget_display(self):
        self.size = self.font.size(self.items[self.value])
        
        self.leftButton = Button(self.engine, (self.position[0],self.position[1]), self.font, '<', self.colors, alpha=self.alpha, id=f'{self._id}_left')
        self.rightButton = Button(self.engine, (self.position[0],self.position[1]), self.font, '>', self.colors, alpha=self.alpha, id=f'{self._id}_right')
        
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
            self.leftButton.rect.right = self.rect.left * .85
            self.rightButton.rect.left = self.rect.right * 1.05
            
            self.engine.draw_text((self.rect.left,self.rect.top),str(self.items[self.value]), self.font, self.colors[0],bgColor=self.colors[1], alpha=self.alpha)
            # Draw buttons independant of list widgets // Fix
            self.leftButton.draw()
            self.rightButton.draw()        
        return super().draw()
    
class LongText(Widget):
    """
    LongText Widget.
    
    It's like a textarea.
    """
    _type:str = 'longtext'
    
    lines:list[str,] = []
    auto_size:bool = False
    
    def __init__(self, engine, position: [int,int], font: int or pg.font.FontType,text:str,colors: list[reqColor,],size: [int, int] = None,id: str = None, alpha: int = 255): # type: ignore
        super().__init__(engine, id)
        self.position = position
        self.font:pg.font.FontType = self.engine.fonts[self.engine._findFont(font)]
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
            print('Draw Backgroun with border')
        for i, line in enumerate(self.text):
            self.engine.draw_text((0,(i*pg.font.Font.size(self.font, 'W')[1])),line, self.font, self.colors[0],alpha=self.alpha, screen=self.image)
            
    def draw(self):
        if self.image and self.rect:
            self.engine.screen.blit(self.image, self.rect)
        return super().draw()