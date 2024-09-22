# Import PyGameEngine
import random
import pygameengine as pyge

# Init PyGameEngine
pge = pyge.PyGameEngine()

# Create Screen
S_W,S_H = (300,420)
screen = pge.createScreen(S_W,S_H)
pge.setScreenTitle("Hello, World!")

# Create a font
arial10 = pge.createSysFont('Arial', 10)
arial12 = pge.createSysFont('Arial', 12)

for i in range(pge.widget_limits*3):
    Bt = pyge.Button(pge, (random.randint(0, S_W), random.randint(0, S_H)),arial12, 'Im a Button!', [pge.Colors.DARKGRAY, pge.Colors.WHITE, pge.Colors.LIGHTGRAY], id=f'button{i}', tip=(f'Button ID: {i}', arial10))
    
while True:
    pge.draw_text((0,0), f'FPS: {pge.fps}', arial12, pge.Colors.BLACK)
    for event in pge.getEvents():
        if event.type == pyge.QUIT:
            pge.exit()
            
    pge.update()
    pge.fill(pge.Colors.WHITE)
    pge.draw_widgets()