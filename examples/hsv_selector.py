# Import PyGameEngine
import pygameengine as pyge

# Init PyGameEngine
pge = pyge.PyGameEngine()

# Create Screen
S_W,S_H = (640,400)
screen = pge.createScreen(S_W,S_H,0)
pge.setScreenTitle("Hello, World!")

# Create a font
arial12 = pge.createSysFont('Arial', 12)

pge.setFPS(60)
pge.enableFPS_unstable()

HueSlider = pyge.Slider(pge, (305, 65), (300, 20), [pge.Colors.BLOOD, pge.Colors.DARKGRAY, pge.Colors.LIGHTGRAY, pge.Colors.DARKRED], value=.5, id='hueslider' ,tip=('Hue (0-360)', arial12))
SaturationSlider = pyge.Slider(pge, (305, 100), (300, 20), [pge.Colors.BLOOD, pge.Colors.DARKGRAY, pge.Colors.LIGHTGRAY, pge.Colors.DARKGREEN], value=.5, id='satslider' ,tip=('Saturation (0-100)', arial12))
ValueSlider = pyge.Slider(pge, (305, 135), (300, 20), [pge.Colors.BLOOD, pge.Colors.DARKGRAY, pge.Colors.LIGHTGRAY, pge.Colors.DARKBLUE], value=.5, id='valueslider' ,tip=('Value (0-100)', arial12))

Color = pyge.reqColor(0,0,0)

while True:
    Color.hsv_to_rgb(HueSlider.value*360, SaturationSlider.value*100, ValueSlider.value*100)
    for ev in pge.events:
        if ev.type == pyge.QUIT:
            pge.exit()
        if ev.type == pyge.KEYDOWN:
            if ev.key == pyge.K_ESCAPE:
                pge.exit()
    
    pge.update()
    pge.fill(pge.Colors.WHITE)
    pge.draw_widgets()
    pge.draw_text((0,0), f'FPS: {pge.fps}', arial12, pge.Colors.BLACK)
    pge.draw_text((0,20), f'RGB: {Color.rgb}, HSV: {Color.hsv}, HEX: {Color.hex}', arial12, pge.Colors.BLACK)
    pge.draw_rect((10,65), (128,128), Color)