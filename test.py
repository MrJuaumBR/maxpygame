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
arial14 = pge.createSysFont('Arial', 14)
arial12 = pge.createSysFont('Arial', 12)

# System Info
pge.getSystemInfo()

# Create widgets
Button:pyge.Button = pge.create_widget(pyge.Button, (15, 100), arial24, 'Im a Button!', [pge.Colors.DARKGRAY, pge.Colors.WHITE, pge.Colors.LIGHTGRAY], id='button1',tip=('This is a test tip, without manual break.', arial16))
Check = pge.create_widget('Checkbox', (190,100), arial24, 'Im a Checkbox!', [pge.Colors.WHITE, pge.Colors.RED, pge.Colors.GREEN, pge.Colors.DARKGRAY], id='checkbox1', tip=('This is a test tip\nwith manual break.', arial16))
Slider = pge.create_widget('Slider', (15, 170), (300, 20), [pge.Colors.WHITE, pge.Colors.DARKGRAY, pge.Colors.LIGHTGRAY, pge.Colors.DARKPINK], value=.5, id='slider1')
Select = pge.create_widget('Select', (25, 250), arial24, [pge.Colors.HOTPING, pge.Colors.DARKGRAY, pge.Colors.LIGHTGRAY], items=['480x360', '640x480', '800x600', '1024x768', '1280x720', '1366x768', '1440x900', '1600x900', '1680x1050', '1920x1200','1920x1080'],textBg=True)
ProgressBar = pge.create_widget('ProgressBar', (15, 450), (300, 20), [pge.Colors.RED, pge.Colors.BROWN, pge.Colors.BROWN, pge.Colors.WHITE],text='?/?', font=arial16, value=.5)
TextBox = pyge.Textbox(pge, (10, 600), 20, [pge.Colors.DARKGRAY, pge.Colors.LIGHTBLUE,pge.Colors.WHITE, pge.Colors.LIGHTGRAY], arial16, 'Im a textbox!', id='textbox1')
Dropdown = pyge.Dropdown(pge, (10, 500), [pge.Colors.WHITE, pge.Colors.GRAY, pge.Colors.DARKGRAY], ['Dropdown Option 0', 'Dropdown Option 1', 'Dropdown Option 2','Small Option 1', "Tiny Opt"], arial16, id='dropdown1')

longtexttest = """This is a long text made for test the LongText widget\ndo you liked this text? and so... about the widget? and about the engine? is currently useful or no? we will be accepting any suggestions, please add it to our github page! we will read and try it on the engine! do you know a fun fact about this widget? it haves a mode that autosizes the text and auto breaks lines, can be useful for make dialogs box"""

LongText = pge.create_widget(pyge.Longtext, (10,300), arial24, longtexttest, [pge.Colors.WHITE, pge.Colors.DARKGRAY, pge.Colors.LIGHTGRAY], id='longtext1')

# FPS Variability
pge.enableFPS_unstable()

# Load Engine Icon
pge.loadIcon()

# Example Tip
ExampleTip = pyge.Tip(pge, 'This is a example tip :)', arial16)

# Game Loop
while True:
    # Draw a text
    if Button.value:
        pge.draw_text((15, 15),f'Button Pressed, Delay Counter(Frames): {Button.click_time_counter}', arial24, pge.Colors.WHITE)
    if Check.value:
        pge.draw_text( (15, 36), 'Checkbox Checked', arial24, pge.Colors.WHITE)
    
    pge.draw_text((15, 60),f'Slider: {Slider.value*100}', arial24, pge.Colors.WHITE)
    
    ProgressBar.text = f'{int(ProgressBar.value*100)}/100'
    
    if pge.hasKeyPressed(pyge.K_LCTRL) or pge.hasKeyPressed(pyge.K_RCTRL):
        ExampleTip.draw()
    
    # Detect events
    for ev in pge.events:
        # Quit if the user closes the window
        if ev.type == pyge.QUIT:
            pge.exit()
        elif ev.type == pyge.KEYDOWN:
            if ev.key == pyge.K_ESCAPE:
                pge.exit()
            elif ev.key == pyge.K_b:
                print(f'{pge.widgets}')
            elif ev.key == pyge.K_KP_PLUS:
                ProgressBar.value += 0.05
            elif ev.key == pyge.K_KP_MINUS:
                ProgressBar.value -= 0.05
            
    # Update the screen
    pge.draw_text((0,0), f'FPS: {int(pge.getFPS())}', arial16, pge.Colors.WHITE)
    pge.draw_widgets()
    pge.screen.blit(pge.icon.surf, (896, 592))
    if pge.hasKeyPressed(pyge.K_LSHIFT) or pge.hasKeyPressed(pyge.K_RSHIFT):
        pge.draw_text((pge.mouse.x+10, pge.mouse.y), str(pge.mouse.pos), arial14, pge.Colors.WHITE)
        pge.draw_text((pge.mouse.x+10, pge.mouse.y+20), f'Left: {pge.mouse.left}, Right: {pge.mouse.right}, Middle: {pge.mouse.middle}', arial12, pge.Colors.WHITE)
        pge.draw_text((pge.mouse.x+10, pge.mouse.y+40), f'Btn 4: {pge.mouse.button_4}, Btn 5: {pge.mouse.button_5}', arial12, pge.Colors.WHITE)
        pge.draw_text((pge.mouse.x+10, pge.mouse.y+60), f'Wheel: {pge.mouse.scroll}', arial12, pge.Colors.WHITE)
    pge.update()
    pge.fpsw()
    # Clear the screen
    pge.fill(pge.Colors.BLACK)