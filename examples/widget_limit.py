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

pge.SetErrorLimitWidget(False)

pge.setFPS(1000)

for i in range(pge.widget_limits*3):
    Type = random.randint(1, 3)
    if Type == 1:
        Bt = pyge.Button(pge, (random.randint(0, S_W), random.randint(20, S_H)),arial12, 'Im a Button!', [pge.Colors.DARKGRAY, pge.Colors.WHITE, pge.Colors.LIGHTGRAY], id=f'button{i}', tip=(f'Button ID: {i}', arial10))
    elif Type == 2:
        Ck = pyge.Checkbox(pge, (random.randint(0, S_W), random.randint(20, S_H)), arial12, 'Im a Checkbox!', [pge.Colors.WHITE, pge.Colors.GREEN, pge.Colors.RED, pge.Colors.DARKGRAY], id=f'checkbox{i}', value=False, tip=(f'Checkbox ID: {i}', arial10))
    elif Type == 3:
        Sld = pyge.Slider(pge, (random.randint(0, S_W), random.randint(20, S_H)), (100, 20), [pge.Colors.WHITE, pge.Colors.DARKGRAY, pge.Colors.LIGHTGRAY, pge.Colors.DARKPINK], value=.5, id=f'slider{i}')
    
while True:
    pge.draw_text((0,0), f'FPS: {int(pge.getFPS())}, Avg FPS: {int(pge.getAvgFPS())}', arial12, pge.Colors.BLACK)
    for event in pge.getEvents():
        if event.type == pyge.QUIT:
            pge.exit()
    
    pge.draw_widgets()
            
    pge.update()
    pge.fill(pge.Colors.WHITE)
    pge.fpsw()
    