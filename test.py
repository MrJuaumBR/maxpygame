# Import PyGameEngine
import pygameengine as pyge


# Init PyGameEngine
pge = pyge.PyGameEngine()

# Create Screen
screen = pge.createScreen(1024, 720)
pge.setScreenTitle("Hello, World!")

# Create a font
arial24 = pge.createSysFont('Arial', 24)
arial16 = pge.createSysFont('Arial', 16)
arial36 = pge.createSysFont('Arial', 36)

# Create widgets
Button = pge.create_widget(pyge.Button, (15, 100), arial24, 'Im a Button!', [pge.Colors.DARKGRAY, pge.Colors.WHITE, pge.Colors.LIGHTGRAY], id='button1')
Check = pge.create_widget('Checkbox', (190,100), arial24, 'Im a Checkbox!', [pge.Colors.WHITE, pge.Colors.RED, pge.Colors.GREEN, pge.Colors.DARKGRAY], id='checkbox1')
Slider = pge.create_widget('Slider', (15, 170), (300, 20), [pge.Colors.WHITE, pge.Colors.DARKGRAY, pge.Colors.LIGHTGRAY, pge.Colors.DARKPINK], value=0, id='slider1')
Select = pge.create_widget('Select', (25, 250), arial24, [pge.Colors.HOTPING, pge.Colors.DARKGRAY, pge.Colors.LIGHTGRAY], items=['Item 1', 'Item 2', 'Item 3'],textBg=True)

longtexttest = """This is a long text made for test the LongText widget\ndo you liked this text? and so... about the widget? and about the engine? is currently useful or no? we will be accepting any suggestions, please add it to our github page! we will read and try it on the engine! do you know a fun fact about this widget? it haves a mode that autosizes the text and auto breaks lines, can be useful for make dialogs box"""

LongText = pge.create_widget(pyge.LongText, (10,300), arial24, longtexttest, [pge.Colors.WHITE, pge.Colors.DARKGRAY, pge.Colors.LIGHTGRAY], id='longtext1')

# Game Loop
while True:
    # Draw a text
    if Button.value:
        pge.draw_text((15, 15),'Button Pressed', arial24, pge.Colors.WHITE)
    if Check.value:
        pge.draw_text( (15, 36), 'Checkbox Checked', arial24, pge.Colors.WHITE)
        
    pge.draw_text((15, 60),f'Slider: {Slider.value*100}', arial24, pge.Colors.WHITE)
    
    # Detect events
    for ev in pge.getEvents():
        # Quit if the user closes the window
        if ev.type == pyge.QUIT:
            pge.exit()
        elif ev.type == pyge.KEYDOWN:
            if ev.key == pyge.K_ESCAPE:
                pge.exit()
            elif ev.key == pyge.K_b:
                print(f'{pge.widgets}')
            
    # Update the screen
    pge.draw_widgets()
    pge.update()
    pge.fpsw()
    # Clear the screen
    pge.fill(pge.Colors.BLACK)