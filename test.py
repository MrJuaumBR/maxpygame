# Import PyGameEngine
print("Import")
import pygameengine as pyge


# Init PyGameEngine
pge = pyge.PyGameEngine()

# Create Screen
screen = pge.createScreen(1024, 720)
pge.setScreenTitle("Hello, World!")

# pge.setRunBackgroundThread(True)


# Create a font
arial24 = pge.createSysFont('Arial', 24)
arial16 = pge.createSysFont('Arial', 16)
arial36 = pge.createSysFont('Arial', 36)
arial14 = pge.createSysFont('Arial', 14)
arial12 = pge.createSysFont('Arial', 12)

# Create widgets
Button:pyge.Button = pge.create_widget(pyge.Button, (15, 100), arial24, 'Im a Button!', [pge.Colors.DARKGRAY, pge.Colors.WHITE, pge.Colors.LIGHTGRAY], id='button1',tip=('This is a test tip, without manual break.', arial16))
Check:pyge.Checkbox = pge.create_widget('Checkbox', (190,100), arial24, 'Im a Checkbox!', [pge.Colors.WHITE, pge.Colors.GREEN, pge.Colors.RED, pge.Colors.DARKGRAY], id='checkbox1',value=False, tip=('This is a test tip\nwith manual break.\nEnable this to enable mouse emulate with controller', arial16))
Slider:pyge.Slider = pge.create_widget('Slider', (15, 170), (300, 20), [pge.Colors.WHITE, pge.Colors.DARKGRAY, pge.Colors.LIGHTGRAY, pge.Colors.DARKPINK], value=.5, id='slider1', on_change=lambda obj: print(f"Slider change: {obj.value}"))
Select:pyge.Select = pge.create_widget('Select', (25, 250), arial24, [pge.Colors.HOTPING, pge.Colors.DARKGRAY, pge.Colors.LIGHTGRAY], items=['480x360', '640x480', '800x600', '1024x768', '1280x720', '1366x768', '1440x900', '1600x900', '1680x1050', '1920x1200','1920x1080'],textBg=True)
ProgressBar:pyge.Progressbar = pge.create_widget('ProgressBar', (15, 450), (300, 20), [pge.Colors.RED, pge.Colors.BROWN, pge.Colors.BROWN, pge.Colors.WHITE],text='?/?', font=arial16, value=.5)
TextBox = pyge.Textbox(pge, (10, 600), 20, [pge.Colors.DARKGRAY, pge.Colors.LIGHTBLUE,pge.Colors.WHITE, pge.Colors.LIGHTGRAY], arial16, 'Im a textbox!',placeholder="Enter a text...", id='textbox1')
Dropdown = pyge.Dropdown(pge, (10, 500), [pge.Colors.WHITE, pge.Colors.GRAY, pge.Colors.DARKGRAY], ['Dropdown Option 0', 'Dropdown Option 1', 'Dropdown Option 2','Small Option 1', "Tiny Opt"], arial16, id='dropdown1')

# FPS Variability
pge.enableFPS_unstable()
pge.setFPS(1000)

# Load Engine Icon
pge.loadIcon()

# Example Tip
ExampleTip = pyge.Tip(pge, 'This is a example tip :)', arial16)

pge.input_query_enable = True

# pge.mouse.mouse_trail_enabled = True
# pge.mouse.trail_node_random_color = True

def Dropdown_Change(obj:pyge.Dropdown):
    print(f"""
          Changed Dropdown:
          {obj.value} - {obj.texts[obj.value]}
          """)

def Select_Change(obj:pyge.Select):
    print(f"""
          Changed Select:
          {obj.value} - {obj.items[obj.value]}
          """)

def Checkbox_Change(obj:pyge.Checkbox):
    print(f"Checkbox change: {obj.value}")
    print(f"{'Enable' if obj.value else 'Disable'} mouse emulate with controller")
    pge.setMouseEmulation(obj.value)

Dropdown.on_change = Dropdown_Change
Select.on_change = Select_Change
Check.on_change = Checkbox_Change

# Game Loop
while True:
    # Draw a text
    if Button.value:
        pge.draw_text((15, 15),f'Button Pressed, Delay Counter(Frames): {Button.click_time_counter}', arial24, pge.Colors.WHITE)
    if Check.value:
        pge.draw_text( (15, 36), 'Checkbox Checked', arial24, pge.Colors.WHITE)
    
    pge.draw_text((15, 60),f'Slider: {round(Slider.value*100,3)}%', arial24, pge.Colors.WHITE)
    
    ProgressBar.text = f'{int(ProgressBar.value*100)}/100'
    
    if pge.hasKeyPressed(pyge.K_LCTRL) or pge.hasKeyPressed(pyge.K_RCTRL):
        ExampleTip.draw()
    
    # Input Query
    inputQueryVlue = ''
    for index,key,_ in pge.input_query.GetQuery():
        inputQueryVlue += pge.keyToString(key) + f"{'' if index == len(pge.input_query.GetQuery())-1 else ', '}"
    
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
            elif ev.key == pyge.K_F1:
                print(pge.getElapsedTime())
                
                print(f'Ram in use: {pge.getInUseRam()*100}% ')
            elif ev.key == pyge.K_F2:
                pge.input_query_enable = not pge.input_query_enable
            
    # Update the screen
    pge.draw_text((0,0), f'FPS: {int(pge.getFPS())}, Avg FPS: {int(pge.getAvgFPS())}, Cached Text: {len(pge.text_cache.keys())}, Delta Time: {pge.delta_time}', arial16, pge.Colors.WHITE)
    pge.draw_widgets()
    pge.screen.blit(pge.icon.surf, (896, 592))
    if pge.hasKeyPressed(pyge.K_LSHIFT) or pge.hasKeyPressed(pyge.K_RSHIFT):
        pge.draw_text((pge.mouse.x+10, pge.mouse.y), str(pge.mouse.pos), arial14, pge.Colors.WHITE)
        pge.draw_text((pge.mouse.x+10, pge.mouse.y+20), f'Left: {pge.mouse.left}, Right: {pge.mouse.right}, Middle: {pge.mouse.middle}', arial12, pge.Colors.WHITE)
        pge.draw_text((pge.mouse.x+10, pge.mouse.y+40), f'Btn 4: {pge.mouse.button_4}, Btn 5: {pge.mouse.button_5}', arial12, pge.Colors.WHITE)
        pge.draw_text((pge.mouse.x+10, pge.mouse.y+60), f'Wheel: {pge.mouse.scroll}', arial12, pge.Colors.WHITE)
        pge.draw_text((pge.mouse.x+10, pge.mouse.y+80), f'Monitor Size: {pge.getMonitorSize()}, Screen Size: {pge.screen_size}', arial12, pge.Colors.WHITE)
        if pge.joystick.mainController:
            pge.draw_text((pge.mouse.x+10, pge.mouse.y+100), f'Joystick (Id): {pge.joystick.mainController.get_id()}, Name: {pge.joystick.mainController.get_name()}', arial12, pge.Colors.YELLOW)
            # Joystick axis
            pge.draw_text((pge.mouse.x+10, pge.mouse.y+120), f'Left X,Y: {round(pge.joystick.mainController.get_axis(0),3)}, {round(pge.joystick.mainController.get_axis(1),3)},            Right X,Y: {round(pge.joystick.mainController.get_axis(2),3)}, {round(pge.joystick.mainController.get_axis(3),3)}', arial12, pge.Colors.YELLOW)
            
    pge.update()
    pge.fpsw()
    # Clear the screen
    pge.fill(pge.Colors.BLACK)