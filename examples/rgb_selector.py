# Import PyGameEngine
import pygameengine as pyge

# Init PyGameEngine
pge = pyge.PyGameEngine()

# Create Screen
S_W,S_H = (800,600)
screen = pge.createScreen(S_W,S_H)
pge.setScreenTitle("Hello, World!")

# Create a font
arial14 = pge.createSysFont('Arial', 14)
arial18 = pge.createSysFont('Arial', 18)

pge.setFPS(60)
pge.enableFPS_unstable()

RedSlider = pyge.Slider(pge, (350, 120), (300, 20), [pge.Colors.RED, pge.Colors.DARKGRAY, pge.Colors.LIGHTGRAY, pge.Colors.DARKRED], value=.5, id='redslider')
GreenSlider = pyge.Slider(pge, (350, 150), (300, 20), [pge.Colors.GREEN, pge.Colors.DARKGRAY, pge.Colors.LIGHTGRAY, pge.Colors.DARKGREEN], value=.5, id='greenslider')
BlueSlider = pyge.Slider(pge, (350, 180), (300, 20), [pge.Colors.BLUE, pge.Colors.DARKGRAY, pge.Colors.LIGHTGRAY, pge.Colors.DARKBLUE], value=.5, id='blueslider')

while True:
    pge.draw_text((0,0), f'FPS: {pge.fps}', arial14, pge.Colors.BLACK)
    pge.draw_text((0,20), f'Color: ({round(RedSlider.value*255,2)},{round(GreenSlider.value*255,2)},{round(BlueSlider.value*255,2)})', arial18, pge.Colors.BLACK)
    pge.draw_text((0,40), f'Color - Float: ({RedSlider.value},{GreenSlider.value},{BlueSlider.value})', arial14, pge.Colors.BLACK)
    pge.draw_rect((10,65), (256,256), (RedSlider.value*255,GreenSlider.value*255,BlueSlider.value*255))
    for ev in pge.events:
        if ev.type == pyge.QUIT:
            pge.exit()
        if ev.type == pyge.KEYDOWN:
            if ev.key == pyge.K_ESCAPE:
                pge.exit()
    pge.update()
    pge.fill(pge.Colors.WHITE)
    pge.draw_widgets()