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
from .objects import cfgtimes,cfgtips, Mouse, InputQuery


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
        
        lines = [line for line in self.text.split('\n') if line]
        self.text_lines = []
        current_line = ''
        for word in ' '.join(lines).split(' '):
            if self.font.size(current_line + ' ' + word)[0] <= max_x:
                current_line += ' ' + word
            else:
                self.text_lines.append(current_line)
                current_line = word
        if current_line:
            self.text_lines.append(current_line)
        
        self.total_size = (max(self.font.size(line)[0] for line in self.text_lines) + 3, sum(self.font.size(line)[1] for line in self.text_lines) + 3)
    
    def update(self):
        """
        Updates the tip. If the refresh time counter is bigger than 0, 
        it will decrement by 1. If the text changed or the refresh time counter
        is equal or less than 0, it will build the rect and strip the text, and
        reset the text changed to False and refresh time counter to the refresh time
        in seconds.
        """
        if self.refresh_time_counter <= 0:
            self.strip_text()
            self.build_rect()
            self.refresh_time_counter = self.engine.TimeSys.s2f(cfgtips.refresh_time)
        else:
            self.refresh_time_counter -= 1
            
    def draw(self):
        self.update()

        if not self.surface or self.text_changed:
            self.surface = pg.Surface(self.total_size, pg.SRCALPHA)

            self.engine.draw_rect(
                (0, 0), self.total_size,
                self.engine.cfgtips.background_color,
                border_width=self.engine.cfgtips.border_width,
                border_color=self.engine.cfgtips.border_color,
                surface=self.surface, alpha=self.engine.cfgtips.alpha
            )

            text_height = self.font.get_linesize()
            for idx, line in enumerate(self.text_lines):
                self.engine.draw_text(
                    (0, idx * text_height), line, self.font,
                    self.engine.cfgtips.text_color, surface=self.surface
                )

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
    enable:bool = True
    
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
        if self.enable:
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
    # Button
    
    Button Widget, can be very useful
    
    Parameters:
        engine (any): The engine that the widget is in
        position (pg.Vector2): The position of the button
        font (int or pg.font.FontType): The font of the button
        text (str): The text of the button
        colors (list[reqColor,reqColor,]): The colors of the button -> **[Text, Background, Border(Optional)]**
        id (str, optional): The id of the widget. Defaults to None.
        alpha (int, optional): The alpha of the button. Defaults to 255.
    """
    _type:str = 'button'
    
    
    click_time:int = cfgtimes.WD_BTN_CLICK_TIME
    click_time_counter:int = 0
    
    value:bool = False
    def __init__(self,engine, position:pg.Vector2, font:int or pg.font.FontType, text:str, colors:list[reqColor,reqColor,],id:str=None,alpha:int=255, tip:Tip=None): # type: ignore
        """
        # Button
        
        Button Widget, can be very useful
        
        Parameters:
            engine (any): The engine that the widget is in
            position (pg.Vector2): The position of the button
            font (int or pg.font.FontType): The font of the button
            text (str): The text of the button
            colors (list[reqColor,reqColor,]): The colors of the button -> **[Text, Background, Border(Optional)]**
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
        font = self.engine._findFont(self.font)
        self.size = pg.Vector2(font.size(self.text))

        self.image = pg.Surface(self.size, pg.SRCALPHA if self.alpha < 255 else 0)
        draw_params = {
            'surface': self.image,
            'alpha': self.alpha,
            'border_width': 0
        }

        if len(self.colors) == 3:
            draw_params.update({'border_width': 3, 'border_color': self.colors[2]})

        self.engine.draw_rect((0, 0), self.size, self.colors[1], **draw_params)
        self.engine.draw_text((0, 0), self.text, font, self.colors[0], surface=self.image, alpha=self.alpha)
        self.rect = pg.Rect(*self.position, *self.size)
        
    def update(self):
        if self.engine.mouse.collidePoint(self.rect) and self.engine.mouse.left and self.click_time_counter <= 0:
            self.click_time_counter = self.engine.TimeSys.s2f(self.click_time) # Reset Timer
            self.value = True
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
    # Checkbox
    
    Checkbox Widget, can be very useful
    
    *Clicky, True, Clicky, False, Clicky, True*
    
    Parameters:
        engine (any): The engine that the widget is in
        position (pg.Vector2): The position of the checkbox
        font (int or pg.font.FontType): The font of the checkbox
        text (str): The text of the checkbox
        colors (list[reqColor,reqColor,reqColor,]): The colors of the checkbox -> **[Text, Active, Unactive, Border(Optional)]**
        id (str, optional): The id of the widget. Defaults to None.
        value (bool, optional): The value of the checkbox. Defaults to False.
        alpha (int, optional): The alpha of the checkbox. Defaults to 255.
    """
    _type:str = 'checkbox'
    
    click_time:int = cfgtimes.WD_CKBX_CLICK_TIME
    click_time_counter:int = 0
    
    box_size:int # Default -> 1/3 of wid limited to 10 > x < 20
    
    on_change:object = None
    
    value:bool = False
    def __init__(self,engine, position:pg.Vector2, font:int or pg.font.FontType, text:str, colors:list[reqColor,reqColor,reqColor,],id:str=None,alpha:int=255, value:bool=False,tip:Tip=None): # type: ignore
        """
        # Checkbox
        
        Checkbox Widget, can be very useful
        
        *Clicky, True, Clicky, False, Clicky, True*
        
        Parameters:
            engine (any): The engine that the widget is in
            position (pg.Vector2): The position of the checkbox
            font (int or pg.font.FontType): The font of the checkbox
            text (str): The text of the checkbox
            colors (list[reqColor,reqColor,reqColor,]): The colors of the checkbox -> **[Text, Active, Unactive, Border(Optional)]**
            id (str, optional): The id of the widget. Defaults to None.
            value (bool, optional): The value of the checkbox. Defaults to False.
            alpha (int, optional): The alpha of the checkbox. Defaults to 255.
        """
        super().__init__(engine,id,tip)
        self.position = position
        self.font:pg.font.FontType = self.engine._findFont(font)
        self.text = text
        self.colors = colors
        self.alpha = alpha
        self.value = value
        
    def build_widget_display(self):
        # Colors: 0(Font),1(Disable), 2(Enable), 3(Background),4(Border)
        font = self.engine._findFont(self.font)
        text_size = font.size(self.text)
        self.box_size = min(20, max(10, int(text_size[0] / 3)))
        self.size = pg.math.Vector2(text_size[0] + self.box_size + 5, text_size[1])
        self.image = pg.Surface(self.size, pg.SRCALPHA)
        self.engine.draw_text((self.box_size + 5,0), self.text, font, self.colors[0], self.image, self.alpha)
        self.rect = pg.Rect(*self.position,*self.size)
        
    def __on_change(self):
        """
        Function that will trigger the custom On_Change Event of the user
        
        Parameters:
            None
        Returns:
            None
        """
        if self.on_change:
            if callable(self.on_change):
                self.on_change(self)
    
    def update(self):
        if self.rect.collidepoint(self.engine.mouse.pos) and self.engine.mouse.left and self.click_time_counter <= 0:
            self.value = not self.value
            self.__on_change()
            self.click_time_counter = self.engine.TimeSys.s2f(self.click_time)
        return super().update() if self.click_time_counter > 0 else self
    
    def cooldown_refresh(self):
        if self.click_time_counter > 0:
            self.click_time_counter -= 1
            
    def draw(self):
        if not (self.image and self.rect):
            return super().draw()
        
        self.engine.screen.blit(self.image, self.rect)

        # Draw box
        color = self.colors[1 if self.value else 2]
        border_width, border_color = (3, self.colors[3]) if len(self.colors) > 3 else (0, (0, 0, 0))
        self.engine.draw_rect(self.rect.topleft, (self.box_size, self.size.y), color, border_width=border_width, border_color=border_color, alpha=self.alpha)
        
        return super().draw()
    
class Slider(Widget):
    """
    # Slider
    
    Slider Widget, is very useful
    
    Parameters:
        engine (any): The engine that the widget is in
        position (pg.Vector2): The position of the slider
        size (tuple[int,int]): The size of the slider
        colors (list[reqColor,reqColor,]): The colors of the slider -> **[Fill & Circle, Background, Border(Optional)]**
        value (float, optional): The value of the slider. Defaults to None.
        fill_passed (bool, optional): If the slider should fill the passed area. Defaults to True.
        id (str, optional): The id of the widget. Defaults to None.
        alpha (int, optional): The alpha of the slider. Defaults to 255.
        on_change (object, optional): The on_change event of the slider. Defaults to None. Needs to be callable and will get the slider as a parameter.
    """
    _type:str = 'slider'
    
    circle:pg.Rect = None
    ball_size:int = 10
    
    fill_passed:bool = True
    
    change_on_scroll:bool = True
    
    _on_change:object = None
    
    _value:float = None
    value:float = 0
    def __init__(self,engine, position:[int,int], size:tuple[int,int],colors:list[reqColor,reqColor,],value:float=None,fill_passed:bool=True,id:str=None,alpha:int=255, tip:Tip=None,on_change:object=None): # type: ignore
        """
        # Slider
        
        Slider Widget, is very useful
        
        Parameters:
            engine (any): The engine that the widget is in
            position (pg.Vector2): The position of the slider
            size (tuple[int,int]): The size of the slider
            colors (list[reqColor,reqColor,]): The colors of the slider -> **[Fill & Circle, Background, Border(Optional)]**
            value (float, optional): The value of the slider. Defaults to None.
            fill_passed (bool, optional): If the slider should fill the passed area. Defaults to True.
            id (str, optional): The id of the widget. Defaults to None.
            alpha (int, optional): The alpha of the slider. Defaults to 255.
            on_change (object, optional): The on_change event of the slider. Defaults to None. Needs to be callable and will get the slider as a parameter.
        """
        super().__init__(engine,id,tip)
        self.position = position
        self.size = size
        self.colors = colors
        self.alpha = alpha
        self._on_change = on_change
        if value is not None:
            self._value = value
        
        self.fill_passed = fill_passed
        
    def build_widget_display(self):
        self.ball_size = (self.size[1] + 10) // 2
        self.image = pg.Surface(self.size, pg.SRCALPHA)
        border_width = 3 if len(self.colors) == 3 else 0
        border_color = self.colors[2] if len(self.colors) == 3 else (0, 0, 0)
        self.engine.draw_rect((0, 0), self.size, self.colors[1], surface=self.image, alpha=self.alpha, border_width=border_width, border_color=border_color)
        self.rect = self.image.get_rect(topleft=self.position)
        self.currentPosition = [self.rect.x + ((self._value or 0) * (self.rect.width - self.ball_size)), self.rect.y - self.ball_size // 4]
        self.circle = pg.Rect(self.currentPosition[0] - self.ball_size / 2, self.currentPosition[1] - self.ball_size / 2, self.ball_size, self.ball_size)
    
    def on_change(self):
        if self._on_change:
            if callable(self._on_change):
                self._on_change(self)
    
    def update(self):
        mouse_pos = self.engine.mouse.pos
        if self.change_on_scroll and (self.engine.mouse.collidePoint(self.rect) or self.engine.mouse.collidePoint(self.circle)):
            scroll = self.engine.mouse.scroll
            if scroll:
                self.currentPosition[0] = max(
                    self.rect.x + self.circle.width // 2,
                    min(self.currentPosition[0] + scroll * 5, self.rect.right - self.circle.width // 2),
                )

        if self.engine.mouse.left and self.rect.collidepoint(mouse_pos):
            self.currentPosition[0] = mouse_pos[0]
            self.currentPosition[0] = max(
                self.rect.x + self.circle.width // 2,
                min(self.currentPosition[0], self.rect.right - self.circle.width // 2),
            )

        # Calculate and clamp the value between 0 and 1
        new_value = round(
            max(
                0, 
                min(
                    (self.currentPosition[0] - self.rect.x - self.circle.width // 2) / (self.rect.width - self.circle.width), 
                    1
                )
            ),
            2
        )

        if new_value != self.value:
            self.value = new_value
            self.on_change()
    
    def draw(self):
        if self.image and self.rect:
            self.engine.screen.blit(self.image, self.rect)
            if self.fill_passed:
                w = self.currentPosition[0]-self.rect.x
                self.engine.draw_rect((self.rect.x, self.rect.y), (0 if w < 0 else w+self.ball_size/2, self.rect.height), self.colors[0], alpha=self.alpha, surface=self.engine.screen)
            self.engine.draw_circle(self.currentPosition,self.ball_size, self.colors[0], alpha=self.alpha, surface=self.engine.screen)
        return super().draw()

class Select(Widget):
    """
    # Select
    
    It's like choose a item, Left or Right.
    
    Parameters:
        engine (any): The engine that the widget is in
        position (pg.Vector2): The position of the select
        font (int or pg.font.FontType): The font of the select
        colors (list[reqColor,reqColor,]): The colors of the select -> **[Text, Background, Border(Optional)]**
        items (list): The items of the select
        value (int, optional): The value of the select. Defaults to 0.
        textBg (bool, optional): If the text background is enabled. Defaults to False.
        id (str, optional): The id of the widget. Defaults to None.
        alpha (int, optional): The alpha of the select. Defaults to 255.
    """
    _type:str = 'select'
    
    leftButton:Button = None
    rightButton:Button = None
    button_click_time = cfgtimes.WD_SLCT_CLICK_TIME
    
    
    items:list=[]
    value:int=0
    textBg:bool = False
    
    change_on_scroll:bool = True
    scroll_change_counter = 0
    
    on_change:object = None
    def __init__(self, engine, position: [int, int], font: int or pg.font.FontType,colors: list[reqColor, reqColor,], items: list ,value:int=0, textBg:bool = False,id: str = None, alpha: int = 255, tip:Tip=None): # type: ignore
        """
        # Select
        
        It's like choose a item, Left or Right.
        
        Parameters:
            engine (any): The engine that the widget is in
            position (pg.Vector2): The position of the select
            font (int or pg.font.FontType): The font of the select
            colors (list[reqColor,reqColor,]): The colors of the select -> **[Text, Background, Border(Optional)]**
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
        self.image = pg.Surface(self.size, pg.SRCALPHA)
        self.rect = pg.Rect(*self.position,*self.size)
        self.leftButton = Button(self.engine, (self.position[0],self.position[1]), self.font, '<', self.colors, alpha=self.alpha, id=f'{self._id}_left')
        self.rightButton = Button(self.engine, (self.position[0],self.position[1]), self.font, '>', self.colors, alpha=self.alpha, id=f'{self._id}_right')
        self.leftButton.click_time = self.button_click_time
        self.rightButton.click_time = self.button_click_time
    
    def __on_change(self):
        """
        Function that will trigger the custom On_Change Event of the user
        
        Parameters:
            None
        Returns:
            None
        """    
        if self.on_change:
            if callable(self.on_change):
                self.on_change(self)
    
    def fix_list(self):
        self.value %= len(self.items)
    
    def update(self):
        if self.change_on_scroll and self.engine.mouse.collidePoint(self.rect):
            scroll = self.engine.mouse.scroll
            if abs(scroll) != 0 and self.scroll_change_counter <= 0:
                self.value += 1 if scroll > 0 else -1
                self.fix_list()
                self.__on_change()
                self.scroll_change_counter = self.engine.TimeSys.s2f(0.3)
        if self.leftButton and self.rightButton:
            if self.leftButton.value:
                self.value -= 1
                self.fix_list()
                self.__on_change()
            if self.rightButton.value:
                self.value += 1
                self.fix_list()
                self.__on_change()
            self.size = self.font.size(str(self.items[self.value]))
            self.rect = pg.Rect(*self.position,*self.size)
        return super().update()
    
    def cooldown_refresh(self):
        if self.scroll_change_counter > 0: self.scroll_change_counter -= 1
        return super().cooldown_refresh()
    
    def draw(self):
        if self.leftButton and self.rightButton:
            offset = 10
            self.leftButton.rect.right = self.rect.left - int(offset*0.45)
            self.rightButton.rect.left = self.rect.right + offset

            # Draw text and buttons
            draw_params = {
                'position': (self.rect.left, self.position[1]-2.5),
                'text': str(self.items[self.value]),
                'font': self.font,
                'color': self.colors[0],
                'bgColor': self.colors[1],
                'border_width': 3,
                'border_color': self.colors[2],
                'alpha': self.alpha
            }
            self.engine.draw_text(**draw_params)
            self.leftButton.draw()
            self.rightButton.draw()
        
        return super().draw()
    
class Longtext(Widget):
    """
    # LongText
    It's like a textarea/textbox but you can't type.
    
    Parameters:
        engine (any): The engine that the widget is in
        position (tuple[int,int]): The position of the Longtext
        font (int or pg.font.FontType): The font of the Longtext
        text (str): The text of the Longtext
        colors (list[reqColor,]): The colors of the Longtext -> **[Text, Background(Optional), Border(Optional)]**
        size (list[int, int], optional): The size of the Longtext. Defaults to None.
        id (str, optional): The id of the widget. Defaults to None.
        alpha (int, optional): The alpha of the Longtext. Defaults to 255.
    """
    _type:str = 'longtext'
    
    lines:list[str,] = []
    auto_size:bool = False
    __font_size_cache:dict[str,tuple[int,int]] = {}
    
    def __init__(self, engine, position: [int,int], font: int or pg.font.FontType,text:str,colors: list[reqColor,],size: [int, int] = None,id: str = None, alpha: int = 255, tip:Tip=None): # type: ignore
        super().__init__(engine, id, tip)
        self.position = position
        self.font:pg.font.FontType = self.engine._findFont(font)
        self.colors = colors
        self.auto_size = size is None
        self.size = (0, 0) if self.auto_size else size
        self.text = text
        self.alpha = alpha
        self.lines = self.__generate_lines()
        
    def __generate_lines(self) -> list[str]:
        lines = []
        current_line = ''
        for word in self.text.split():
            test_line = f'{current_line} {word}'.strip()
            if self.__get_font_size(test_line)[0] <= self.engine.screen.get_size()[0] - (self.position[0]+1):
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
        return lines
    
    get_lines = __generate_lines
    
    def __get_font_size(self, text:str) -> tuple[int,int]:
        if text not in self.__font_size_cache:
            self.__font_size_cache[text] = pg.font.Font.size(self.font, text)
        return self.__font_size_cache[text]
    
    def build_widget_display(self):
        if self.auto_size:
            try:
                max_width = max(pg.font.Font.size(self.font, line)[0] for line in self.lines)
                self.size = (max_width, len(self.lines) * pg.font.Font.size(self.font, 'W')[1] + 5)
            except: pass
        else:
            max_width = self.size[0]

        self.image = pg.Surface(self.size, pg.SRCALPHA)
        self.rect = pg.Rect(*self.position, *self.size)
        if len(self.colors) > 1:
            self.engine.draw_rect((0,0), self.size, self.colors[1], border_width=3 if len(self.colors) > 2 else 0, border_color=self.colors[2] if len(self.colors) > 2 else None, alpha=self.alpha, surface=self.image)

        y = 0
        for line in self.lines:
            rect = self.font.size(line)
            if rect[0] > max_width:
                words = line.split()
                line = ''
                for word in words:
                    if pg.font.Font.size(self.font, f'{line} {word}')[0] > max_width:
                        self.engine.draw_text((0, y), line, self.font, self.colors[0], alpha=self.alpha, surface=self.image)
                        line = word
                        y += rect[1]
                    else:
                        line += f' {word}'
                self.engine.draw_text((0, y), line, self.font, self.colors[0], alpha=self.alpha, surface=self.image)
                y += rect[1]
            else:
                self.engine.draw_text((0, y), line, self.font, self.colors[0], alpha=self.alpha, surface=self.image)
                y += rect[1]
            
    def draw(self):
        if self.image and self.rect:
            self.engine.screen.blit(self.image, self.rect)
        return super().draw()
    
class Progressbar(Widget):
    """
    # Progress bar
    
    A Progress bar, can be used for make a loading bar or life bars
    
    Parameters:
        engine (any): The engine that the widget is in
        position (pg.Vector2): The position of the widget
        size (tuple[int,int]): The size of the widget
        colors (list[reqColor,reqColor,reqColor,]): The colors of the widget -> **[Fill Color, Background, Border, Text(Optional)]**
        value (float, optional): The value of the widget. Defaults to 0.
        text (str, optional): The text of the widget. Defaults to None.
        id (str, optional): The id of the widget. Defaults to None.
    """
    _type:str = 'progressbar'
    
    colors:list[reqColor,reqColor,reqColor,] = []
    text:str = None
    font:pg.font.FontType = None
    
    value:float = 0
    def __init__(self, engine,position:tuple[int,int],size:tuple[int,int],colors:list[reqColor,reqColor,reqColor,],value:float=0,text:str=None,font:pg.font.FontType=None, id: str = None, tip:Tip=None):
        """
        # Progress bar
        
        A Progress bar, can be used for make a loading bar or life bars
        
        Parameters:
            engine (any): The engine that the widget is in
            position (pg.Vector2): The position of the widget
            size (tuple[int,int]): The size of the widget
            colors (list[reqColor,reqColor,reqColor,]): The colors of the widget -> **[Fill Color, Background, Border, Text(Optional)]**
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
            
            if self.text and (self.font):
                self.engine.draw_text((self.rect.left+1, self.rect.top+1),str(self.text), self.font, (self.colors[3] if len(self.colors) >= 3 else self.colors[1]))
        return super().draw()
    
class Textbox(Widget):
    """
    # Textbox
    
    A Textbox, you can write in it.
    
    Parameters:
        engine (any): The engine that the widget is in
        position (pg.Vector2): The position of the widget
        height (int): The height of the widget
        colors (list[reqColor,reqColor,reqColor,]): The colors of the widget -> **[Background Unactive, Background Active, Text, Border(Optional)]**
        font (pg.font.FontType): The font of the widget. Defaults to None.
        text (str, optional): The text of the widget. Defaults to None.
        alpha (int, optional): The alpha of the widget. Defaults to 255.
        placeholder (str, optional): The placeholder of the widget. Defaults to None.
        id (str, optional): The id of the widget. Defaults to None.
        on_change (object, optional): The on_change event of the widget. Defaults to None. Needs to be callable and will get the widget as a parameter.
    """
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
    
    placeholder_text:str = None
    editable:bool = True
    
    _on_change:object = None
    
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
    def __init__(self, engine,position:tuple[int,int],height:int,colors:list[reqColor,reqColor,reqColor,],font:pg.font.FontType,text:str=None,alpha:int=255,placeholder:str=None, id: str = None, tip:Tip=None,on_change:object=None):
        """
        # Textbox
        
        A Textbox, you can write in it.
        
        Parameters:
            engine (any): The engine that the widget is in
            position (pg.Vector2): The position of the widget
            height (int): The height of the widget
            colors (list[reqColor,reqColor,reqColor,]): The colors of the widget -> **[Background Unactive, Background Active, Text, Border(Optional)]**
            font (pg.font.FontType): The font of the widget. Defaults to None.
            text (str, optional): The text of the widget. Defaults to None.
            alpha (int, optional): The alpha of the widget. Defaults to 255.
            placeholder (str, optional): The placeholder of the widget. Defaults to None.
            id (str, optional): The id of the widget. Defaults to None.
            on_change (object, optional): The on_change event of the widget. Defaults to None. Needs to be callable and will get the widget as a parameter.
        """
        super().__init__(engine, id, tip)
        self.position:tuple[int,int] = position
        self.height:int = height
        self.colors:list[reqColor,reqColor,] = colors
        self.text:str = text
        self.font:pg.font.FontType = self.engine._findFont(font)
        self.alpha:int = alpha
        
        self.placeholder_text:str = placeholder
        
        self._on_change = on_change
        
    def build_widget_display(self):
        self.max_width = self.engine.screen.get_width() - self.position[0]
        self.image = pg.Surface((0,0))
        self.rect = pg.Rect(*self.position,self.max_width,self.height)
        
    def update(self):
        if self.editable:
            # Update Size
            size = self.font.size(self.text)
            w,h = size[0]+5,size[1]
            if h > self.height:
                self.height = h+2
            if len(str(self.placeholder_text)) <= 2 or not self.placeholder_text:
                self.rect.size = ((self.font.size('WW')[0]*1.15) if w < self.font.size('WW')[0] else w,h+2)
            else:
                self.rect.size = (int(self.font.size(self.placeholder_text)[0]*1.15) if w < self.font.size(self.placeholder_text)[0] else w,h+2)
            
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
                        if not self.engine.input_query_enable:
                            for ev in self.engine.events:
                                if ev.type == pg.KEYDOWN:
                                    if not (ev.key in self.blacklist):
                                        self.text += ev.unicode
                                    self.key_press_counter = self.engine.TimeSys.s2f(self.key_press_time)                   
                        else:
                            ipq:InputQuery = self.engine.input_query
                            for index, key, event in ipq.GetQuery():
                                index:int
                                key:int
                                event:pg.event.EventType
                                if not (key in self.blacklist):
                                    self.text += event.unicode
                                ipq.RemoveFromQuery(index) # Prevents Dupe
                                self.key_press_counter = self.engine.TimeSys.s2f(self.key_press_time)                   
            
                    if self.text != self.value:
                        self.on_change()
                        
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
            if self.active:
                color = self.colors[1]
            else:
                color = self.colors[0]
            self.engine.draw_rect(self.rect.topleft, self.rect.size, color, border_width=3 if len(self.colors) > 3 else 0, border_color=self.colors[2] if len(self.colors) > 3 else None,alpha=self.alpha)
            self.engine.draw_text((self.rect.x+2.5, self.rect.y+1),self.text, self.font, self.colors[2],alpha=self.alpha)
            
            if self.placeholder_text and (len(str(self.text)) == 0 or not self.text):
                r1 = pg.Rect(0, 0, *self.font.size(self.placeholder_text))
                r1.center = self.rect.topleft
                r1.left += 5
                self.engine.draw_text(r1.center, self.placeholder_text, self.font, self.colors[2], alpha=150)
        return super().draw()
    
    def on_change(self):
        if self._on_change:
            if callable(self._on_change):
                self._on_change(self)
    
class Dropdown(Widget):
    """
    # Dropdown
    
    Dropdown widget, is a dropdown when you click you can choose one of the items listed.
    
    Parameters:
        position:tuple[int,int]
        colors:list[reqColor,reqColor,reqColor,] -> **[Text Color, Background Color, Border Color(Optional)]**
        texts:list[str,]
        font:pg.font.FontType
        alpha:int
        current_text:int
        id:str
        tip:Tip
    """
    _type:str = 'dropdown'
    
    colors:list[reqColor,reqColor,reqColor,] = []
    texts:list[str,] = []
    text:str = ''
    current_text:int = 0
    font:pg.font.FontType = None
    position:tuple[int,int] = (0,0)
    
    texts_rects:list[tuple[pg.rect.RectType, int]] = [] # The Rect of text, Index of text
    
    rect:pg.Rect = None
    
    active:bool = False
    change_on_scroll:bool = True
    on_change:object = None
    
    update_delay_count:int = 0
    Click_Time_counter:int = 0
    def __init__(self, engine, position:tuple[int,int], colors:list[reqColor,reqColor,reqColor,], texts:list[str,], font:pg.font.FontType, alpha:int=255, current_text:int=0,id:str=None, tip:Tip=None):
        """
        # Dropdown
        
        Dropdown widget, is a dropdown when you click you can choose one of the items listed.
        
        Parameters:
            position:tuple[int,int]
            colors:list[reqColor,reqColor,reqColor,] -> **[Text Color, Background Color, Border Color(Optional)]**
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
        self.text = self.texts[self.current_text]
        self.build_widget_display()
    
    def __on_change(self):
        """
        Function that will trigger the custom On_Change Event of the user
        
        Parameters:
            None
        Returns:
            None
        """  
        self.value = self.current_text
        self.text = self.texts[self.current_text]
        if self.on_change:
            if callable(self.on_change):
                self.on_change(self)
    
    def build_widget_display(self):
        width,height = max(self.font.size(text) for text in self.texts)
        
        # Set the rect for the new one
        self.rect = pg.Rect(*self.position, width, height)
        
        self.surface = pg.Surface((width,height), pg.SRCALPHA)
        
        if self.active:
            self.texts_rects.clear()
            height += (self.font.size(self.texts[self.current_text])[1]*((len(self.texts)-1) if len(self.texts) > 1 else 1))+2
            
            self.surface = pg.Surface((width,height), pg.SRCALPHA)
            
            self.engine.draw_rect((0,self.rect.height), (width,height-self.rect.height), self.colors[1], border_width=3 if len(self.colors) > 2 else 0, border_color=self.colors[2] if len(self.colors) > 2 else (0,0,0), alpha=self.alpha if self.alpha < 255 else 200, surface=self.surface)
            pos = [2,self.rect.height+2]
            for x,line in enumerate(self.texts):
                if x != self.current_text:
                    r = self.engine.draw_text((pos[0], pos[1]), str(line), self.font, self.colors[0], surface=self.surface, alpha=self.alpha)
                    r.topleft = (pos[0]+self.position[0],pos[1]+self.position[1])
                    self.texts_rects.append((r,x))
                    pos[1] += self.font.size(line)[1]
        
        self.surface.set_alpha(self.alpha)
        
        self.engine.draw_rect((0,0), self.rect.size, self.colors[1], border_width=3 if len(self.colors) > 2 else 0, border_color=self.colors[2] if len(self.colors) > 2 else (0,0,0), alpha=self.alpha, surface=self.surface)
        self.engine.draw_text((2, 1),self.texts[self.current_text], self.font, self.colors[0], surface=self.surface, alpha=self.alpha)
        
        # self.rect.size = (width,height)
    
    def update_wd(self):
        self.build_widget_display()
    
    def hovered(self):
        if (self.change_on_scroll and self.Click_Time_counter <= 0 and self.rect.collidepoint(self.engine.mouse.pos)): # Check if the mouse is in the rect, change on scroll True and click time counter <= 0
            if self.engine.mouse.scroll != 0: # Check if the mouse is scrolling
                self.Click_Time_counter = self.engine.TimeSys.s2f(cfgtimes.WD_DPDW_CLICK_TIME)
                change = self.engine.mouse.scroll * -1
                change = 1 if change > 0 else -1
                self.current_text += change
                if self.current_text < 0:
                    self.current_text = len(self.texts)-1
                elif self.current_text >= len(self.texts):
                    self.current_text = 0
                self.__on_change()    
        if (self.engine.mouse.left) and self.Click_Time_counter <= 0:
            if self.rect.collidepoint(self.engine.mouse.pos):
                self.active = not self.active
                self.update_wd()
            else:
                if self.active:
                    passed:bool = False
                    for rect, index in self.texts_rects:
                        if rect.collidepoint(self.engine.mouse.pos):
                            self.current_text = index
                            self.__on_change()
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
    """
    # Textarea Widget
    A Textarea, is basically a **textbox**, but will break when have a "\\n" or pass the screen size.
    
    Parameters:
        engine:Engine
        position:tuple[int,int]
        height:int
        colors:list[reqColor,reqColor,reqColor,] -> **[Active Color, Inactive Color, Text Color & Border Color]**
        font:pg.font.FontType
        text:str
        alpha:int (Optional)
        placeholder:str (Optional)
        id:str (Optional)
        tip:Tip (Optional)
    """
    _type:str = 'textarea'
    
    colors:list[reqColor,reqColor,reqColor,] = []
    text:str = None
    shown_text:list[str,] = []
    font:pg.font.FontType = None
    active:bool = False
    editable:bool = True
    
    del_press_time:int = cfgtimes.WD_TXBX_DEL_TIME
    del_press_counter:int = 0
    
    key_press_time:int = cfgtimes.WD_TXBX_KEYP_TIME
    key_press_counter:int = 0
    
    click_time:int = cfgtimes.WD_TXBX_CLICK_TIME
    click_counter:int = 0
    total_size:tuple[int,int] = (0,0)
    
    surface:pg.Surface = None
    
    placeholder_text:str = None
    
    min_size = (0,0)
    
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
    def __init__(self, engine,position:tuple[int,int],colors:list[reqColor,reqColor,reqColor,],font:pg.font.FontType,text:str=None,alpha:int=255,placeholder:str=None, id: str = None, tip:Tip=None):
        """
        # Textarea Widget
        A Textarea, is basically a **textbox**, but will break when have a "\\n" or pass the screen size.
        
        Parameters:
            engine:Engine
            position:tuple[int,int]
            height:int
            colors:list[reqColor,reqColor,reqColor,] -> **[Active Color, Inactive Color, Text Color & Border Color]**
            font:pg.font.FontType
            text:str
            alpha:int (Optional)
            placeholder:str (Optional)
            id:str (Optional)
            tip:Tip (Optional)
        """
        super().__init__(engine,id,tip)
        self.position:tuple[int,int] = position
        self.colors:list[reqColor,reqColor,] = colors
        self.text:str = text
        self.font:pg.font.FontType = self.engine._findFont(font)
        self.alpha:int = alpha
        self.placeholder_text:str = placeholder
        
        self.min_size = self.font.size('WWWWWW')
        
        self.strip_text()
    
    def strip_text(self):
        """
        This function will make 3 things:
        
        1. Split the text in lines when haves '\\n'
        2. Break line when passes max_x
        3. Calculate the total_size(
            width: will get the bigger line width using font,
            height: will get total size of the height of all lines using font too
        )
        """
        screen_size: tuple[int, int] = self.engine.screen.get_size()
        
        max_x, _ = screen_size[0] - self.position[0], screen_size[1] - self.position[1]
        
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
    
    def remove_blacklist_fromQuery(self):
        if self.engine.input_query_enable:
            for key in self.blacklist:
                if self.engine.input_query.HasKey(key):
                    self.engine.input_query.RemoveFromQueryByKey(key)
    
    def update(self):
        # Update Value
        self.value = self.text
        
        # Get mouse and update if is active or no
        if self.editable:
            if self.engine.mouse.left: # Left Mouse Click Active ?
                if self.click_counter <= 0: # Isn't in Click Cooldown
                    if self.engine.mouse.collidePoint(self.rect): # Mouse on Widget ?
                        if not self.active: # Isn't Active
                            self.click_counter = self.engine.TimeSys.s2f(self.click_time) # Reset Timer
                            self.active = True # Set Active
                            self.text_changed = True
                    else: # Mouse not on Widget
                        self.active = False # Set Inactive
                        self.text_changed = True
            
            if self.active and self.editable: # Is Active & Editable
                self.remove_blacklist_fromQuery()
                if self.key_press_counter <= 0 or self.del_press_counter <= 0: # Isn't in Key Press Cooldown//Del Press Cooldown
                    keys:pg.key.ScancodeWrapper = self.engine.getKeys() # Get Keys pressed
                    self.text_changed = False
                    if keys[pg.K_BACKSPACE] and self.del_press_counter <= 0: # Backspace
                        self.text = self.text[:-1] # Remove last character
                        self.del_press_counter = self.engine.TimeSys.s2f(self.del_press_time) # Reset Timer
                        self.text_changed = True
                    elif keys[pg.K_RETURN] and self.key_press_counter <= 0: # Enter
                        self.active = False # Set Inactive
                        self.key_press_counter = self.engine.TimeSys.s2f(self.key_press_time) # Reset Timer
                        self.text_changed = True
                    elif self.key_press_counter <= 0: # Isn't in Key Press Cooldown
                        if not self.engine.input_query_enable: # No Input Query Enable (Old System)
                            for ev in self.engine.events: # Get Events
                                if ev.type == pg.KEYDOWN: # Key Down
                                    if not (ev.key in self.blacklist):
                                        self.text += ev.unicode
                                        self.text_changed = True
                                    self.key_press_counter = self.engine.TimeSys.s2f(self.key_press_time)                   
                        else:
                            ipq:InputQuery = self.engine.input_query
                            if len(ipq.GetQuery()) > 0:
                                for index, key, event in ipq.GetQuery():
                                    index:int
                                    key:int
                                    event:pg.event.EventType
                                    if not (key in self.blacklist):
                                        self.text += event.unicode
                                        self.text_changed = True
                                    ipq.RemoveFromQuery(index) # Prevents Dupe
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
        if self.surface is None or self.text_changed:
            self.strip_text()
            if self.placeholder_text and (len(str(self.text)) == 0 or not self.text):
                self.total_size = [int(i*1.15) for i in self.font.size(self.placeholder_text)]
            elif (self.total_size[0] < self.min_size[0] or self.total_size[1] < self.min_size[1]):
                self.total_size = self.min_size
                
            # Update Rect
            self.rect.topleft = self.position
            self.rect.size = self.total_size
                
            self.surface = pg.Surface(self.total_size, pg.SRCALPHA)
            
            self.engine.draw_rect((0,0), self.total_size, self.colors[0] if self.active else self.colors[1], border_width=3 if len(self.colors) > 3 else 0, border_color=self.colors[2] if len(self.colors) > 3 else None, alpha=self.alpha, surface=self.surface)
            for ind,line in enumerate(self.shown_text):
                self.engine.draw_text((1.5, 1+(ind*self.font.get_height())),line, self.font, self.colors[2], alpha=self.alpha, surface=self.surface)
            
            # Draw placeholder text at center of the widget with alpha
            if self.placeholder_text and (len(str(self.text)) == 0 or not self.text):
                r1 = pg.Rect(0, 0, *self.font.size(self.placeholder_text))
                r1.center = self.surface.get_rect().topleft
                r1.left += 5
                self.engine.draw_text(r1.center, self.placeholder_text, self.font, self.colors[2], alpha=150, surface=self.surface)    
                
            self.text_changed = False
            
        self.engine.screen.blit(self.surface, self.position)
        return super().draw()    
    