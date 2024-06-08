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
        super().__init__()
        self.engine = engine
        self.engine.addWidget(self)
        
        if id == None:
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
    _type:str = 'button'
    
    
    click_time:int = 0.15 # Default -> 0.15s
    click_time_counter:int = 0
    
    value:bool = False
    def __init__(self,engine, position:pg.Vector2, font:int or pg.font.FontType, text:str, colors:list[reqColor,reqColor,],id:str=None,alpha:int=255): # type: ignore
        super().__init__(engine,id)
        self.position = position
        self.font = font
        self.text = text
        self.colors = colors
        self.alpha = alpha
        
    def build_widget_display(self):
        # First get the size of the text
        font:pg.font.FontType = self.engine.fonts[self.engine._findFont(self.font)]
        self.size = pg.math.Vector2(*font.size(self.text))
        
        self.image = pg.Surface(self.size, (pg.SRCALPHA if (self.alpha < 255 or self.alpha != None) else 0))
        if len(self.colors) < 3: # Has only 2 colors
            self.engine.draw_rect((0,0), self.size, self.colors[0], screen=self.image, alpha=self.alpha)
        elif len(self.colors) == 3: # Has 3 colors
            self.engine.draw_rect((0,0), self.size, self.colors[0], border_width=3, border_color=self.colors[2], screen=self.image, alpha=self.alpha)
            
        self.engine.draw_text(self.text, self.font, (0,0), self.colors[1], screen=self.image, alpha=self.alpha)
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
    _type:str = 'switch'
    
    click_time:int =0.5 # Default -> 0.5s
    click_time_counter:int = 0
    
    box_size:int # Default -> 1/4 of wid
    
    value:bool = False
    def __init__(self,engine, position:pg.Vector2, font:int or pg.font.FontType, text:str, colors:list[reqColor,reqColor,reqColor,],id:str=None,alpha:int=255): # type: ignore
        super().__init__(engine,id)
        self.position = position
        self.font = font
        self.text = text
        self.colors = colors
        self.alpha = alpha
        
    def build_widget_display(self):
        # Colors: 0(Font),1(Disable), 2(Enable), 3(Background),4(Border)
        font:pg.font.FontType = self.engine.fonts[self.engine._findFont(self.font)]
        self.size = pg.math.Vector2(*font.size(self.text))
        
        # Add Box Size
        self.box_size = int(self.size.x / 4)
        self.size.x += int(self.box_size * 1.15)
        
        # Create Image
        self.image = pg.Surface(self.size, pg.SRCALPHA)
        
        # Insert Text
        self.engine.draw_text(self.text, font, (int(self.box_size * 1.15),0), self.colors[0], screen=self.image, alpha=self.alpha)
        
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
    _type:str = 'slider'
    
    circle:pg.Rect = None
    ball_size:int = 10
    
    _value:float = None
    value:float = 0
    def __init__(self,engine, position:[int,int], size:tuple[int,int],colors:list[reqColor,reqColor,],value:float=None,id:str=None,alpha:int=255): # type: ignore
        super().__init__(engine,id)
        self.position = position
        self.size = size
        self.colors = colors
        self.alpha = alpha
        if value is not None:
            self._value = value
        
    def build_widget_display(self):
        
        self.ball_size = self.size[1]//2 + 5
        self.image = pg.Surface(self.size, pg.SRCALPHA)
        
        self.engine.draw_rect((0,0),self.size,self.colors[1], screen=self.image, alpha=self.alpha, border_width=(3 if len(self.colors) >= 3 else 0),border_color= (self.colors[2] if len(self.colors) >= 3 else (0,0,0)))
        
        self.rect = pg.Rect(*self.position,*self.size)
        
        if self._value is not None:
            # Value is between 0 and 1
            # make the cur position beetween min pos and max pos using the value as percentage
            # Value only will interact with the X vector
            self.currentPosition = [(self.rect.x + self.ball_size//2) * self.value, self.rect.y - self.ball_size//4]
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
            
            self.circle = self.engine.draw_circle(self.currentPosition,self.ball_size, self.colors[0], alpha=self.alpha)
        
        return super().draw()