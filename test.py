# Import PyGameEngine
import pygameengine as pyge


# Init PyGameEngine
pge = pyge.PyGameEngine()

# Create Screen
screen = pge.createScreen(800, 600)
pge.setScreenTitle("Hello, World!")

# Create a font
arial24 = pge.createSysFont('Arial', 24)

# Create widgets
Button = pge.create_widget(pyge.Button, (15, 400), arial24, 'Im a Button!', [pge.Colors.DARKGRAY, pge.Colors.WHITE, pge.Colors.LIGHTGRAY], id='button1')
Check = pge.create_widget('Checkbox', (190,400), arial24, 'Im a Checkbox!', [pge.Colors.WHITE, pge.Colors.RED, pge.Colors.GREEN, pge.Colors.DARKGRAY], id='checkbox1')
Slider = pge.create_widget('Slider', (15, 450), (300, 20), [pge.Colors.WHITE, pge.Colors.DARKGRAY, pge.Colors.LIGHTGRAY], id='slider1', value=0)

# Game Loop
while True:
    # Draw a common rect
    pge.draw_rect((0,0),(256,256), pge.Colors.RED)
    
    # Draw a rect with a border
    pge.draw_rect((10,10),(600,175), pge.Colors.GREEN, 5, pge.Colors.BLUE)
    
    # Draw a text
    if Button.value:
        pge.draw_text('Button Pressed', arial24, (15, 15), pge.Colors.WHITE)
    if Check.value:
        pge.draw_text('Checkbox Checked', arial24, (15, 36), pge.Colors.WHITE)
        
    pge.draw_text(f'Slider: {Slider.value*100}', arial24, (15, 60), pge.Colors.WHITE)
    
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
    pge.update()
    pge.fpsw()
    # Clear the screen
    pge.fill(pge.Colors.BLACK)
    pge.draw_widgets()