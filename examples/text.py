# Import PyGameEngine
import pygameengine as pyge
import random

# Init PyGameEngine
pge = pyge.PyGameEngine()

# Create Screen
S_W,S_H = (1024,768)
screen = pge.createScreen(S_W,S_H)
pge.setScreenTitle("Hello, World!")

# Create a font
arial12 = pge.createSysFont('Arial', 12)

pge.setFPS(1000)
pge.extra_process = False

Texts = []
for i in range(random.randint(150, 300)):
    Texts.append(
        [
            random.randint(0, S_W),
            random.randint(0, S_H),
            f'Text {i}: {random.randint(0, 1000)}',
        ]
    )

while True:
    for Text in Texts:
        pge.draw_text((Text[0], Text[1]), Text[2], arial12, pge.Colors.WHITE)
    for event in pge.events:
        if event.type == pyge.pg.QUIT:
            pge.exit()
        elif event.type == pyge.pg.KEYDOWN:
            if event.key == pyge.pg.K_ESCAPE:
                pge.exit()
                
    pge.update()
    pge.fill(pge.Colors.BLACK)
    pge.fpsw()
    pge.draw_text((10, 10), f'FPS: {int(pge.getFPS())}, Avg FPS: {int(pge.getAvgFPS())}', arial12, pge.Colors.GREEN)