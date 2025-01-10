# # Buttons
#             

import pygameengine as pyge


# Init PyGameEngine
pge = pyge.PyGameEngine()

# Create Screen
screen = pge.createScreen(1024, 728)
pge.setScreenTitle("Hello, World!")

# Turn on Controller
pge.setMouseEmulation(True)

# Create a font
arial12 = pge.createSysFont('Arial', 12)
arial16 = pge.createSysFont('Arial', 16)
arial32 = pge.createSysFont('Arial', 32)
arial72 = pge.createSysFont('Arial', 72)

testButton = pyge.Button(pge, (10, 600), arial32, 'Test Button', [pge.Colors.DARKGRAY, pge.Colors.WHITE, pge.Colors.LIGHTGRAY], id='button1', tip=(f'This is a test Button, use {str(pge.joystick.joystick_trigger_mouse_button).capitalize()} to trigger!', arial12))
dropdownTest = pyge.Dropdown(pge, (10, 500), [pge.Colors.WHITE, pge.Colors.GRAY, pge.Colors.DARKGRAY], ['Dropdown Option 0', 'Dropdown Option 1', 'Dropdown Option 2','Small Option 1', "Tiny Opt"], arial16, id='dropdown1')

while True:
    
    for event in pge.events:
        if event.type == pyge.QUIT:
            pge.exit()
    
    if pge.joystick.mainController is None:
        pge.draw_text((10, 10), 'No joystick connected.', arial72, pge.Colors.RED)
    else:
        pge.draw_text((10, 10), f'Joystick: {pge.joystick.mainController.get_name()}', arial32, pge.Colors.YELLOW)
        # Buttons
        Buttons = pge.joystick.mainController.allButtons()
        for index, button_name in enumerate(Buttons.keys()):
            button_state = Buttons[button_name]
            pge.draw_text((10, 140+index*20), f'Button {button_name}: {button_state}', arial12, pge.Colors.GREEN)
            
        # Hats/Dpad
        pge.draw_text((150,140), f'DPad: {pge.joystick.mainController.getDPad()}', arial12, pge.Colors.GREEN)
            
        # Axes
        pge.draw_text((150, 180), f'Axes: {pge.joystick.mainController.getAxisByString("left")}, {pge.joystick.mainController.getAxisByString("right")}', arial12, pge.Colors.GREEN)
        
        for index in range(pge.joystick.mainController.joystick.get_numbuttons()):
            pge.draw_text((150, 220+index*20), f'Button {index}: {pge.joystick.mainController.get_button(index)}', arial12, pge.Colors.GREEN)
    
    if testButton.value:
        print("You clicked the button!")
    
    pge.update()
    pge.fill(pge.Colors.BLACK)
    pge.draw_widgets()
    pge.fpsw()