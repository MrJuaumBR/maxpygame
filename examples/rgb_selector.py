# Import PyGameEngine
import pygameengine as pyge

# Init PyGameEngine
pge = pyge.PyGameEngine()

# Create Screen
S_W,S_H = (640,400)
screen = pge.createScreen(S_W,S_H,0)
pge.setScreenTitle("Hello, World!")

# Create a font
arial14 = pge.createSysFont('Arial', 14)
arial18 = pge.createSysFont('Arial', 18)

pge.setFPS(60)
pge.enableFPS_unstable()

RedSlider = pyge.Slider(pge, (305, 65), (300, 20), [pge.Colors.RED, pge.Colors.DARKGRAY, pge.Colors.LIGHTGRAY, pge.Colors.DARKRED], value=.5, id='redslider')
GreenSlider = pyge.Slider(pge, (305, 100), (300, 20), [pge.Colors.GREEN, pge.Colors.DARKGRAY, pge.Colors.LIGHTGRAY, pge.Colors.DARKGREEN], value=.5, id='greenslider')
BlueSlider = pyge.Slider(pge, (305, 135), (300, 20), [pge.Colors.BLUE, pge.Colors.DARKGRAY, pge.Colors.LIGHTGRAY, pge.Colors.DARKBLUE], value=.5, id='blueslider')

Color = pyge.reqColor(0,0,0)
Brightness = Color.brightness

while True:
    pge.draw_text((0,0), f'FPS: {pge.fps}', arial14, pge.Colors.BLACK)
    pge.draw_text((0,20), f'Color: ({round(RedSlider.value*255,2)},{round(GreenSlider.value*255,2)},{round(BlueSlider.value*255,2)})', arial18, pge.Colors.BLACK)
    pge.draw_text((0,40), f'Color - Float: ({RedSlider.value},{GreenSlider.value},{BlueSlider.value})', arial14, pge.Colors.BLACK)
    pge.draw_text((0,200), f'Brightness: {Brightness}, HEX: {Color.hex}, HSV: {[round(x,3) for x in Color.hsv]}', arial18, pge.Colors.BLACK)
    pge.draw_rect((10,65), (128,128), Color)
    
    
    Color.rgb = (round(RedSlider.value*255), round(GreenSlider.value*255), round(BlueSlider.value*255))
    Brightness = Color.brightness
    
    for ev in pge.events:
        if ev.type == pyge.QUIT:
            pge.exit()
        if ev.type == pyge.KEYDOWN:
            if ev.key == pyge.K_ESCAPE:
                pge.exit()
    pge.flip()
    pge.fill(pge.Colors.WHITE)
    pge.draw_widgets()