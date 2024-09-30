# Import PyGameEngine
import pygameengine as pyge
from pygameengine import pg


# Init PyGameEngine
pge = pyge.PyGameEngine()

# Create Screen
screen = pge.createScreen(1024, 720)
pge.setScreenTitle("Hello, World!")

image = pg.Surface((320, 200), pg.SRCALPHA)
pg.draw.polygon(image, pge.Colors.BLUE.rgb, ((0, 0), (320, 100), (0, 200)))



flip_x = False
flip_y = False

while True:
    for event in pge.events:
        if event.type == pg.QUIT:
            exit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                exit()
            elif event.key == pg.K_a:
                flip_x = not flip_x
                image = pge.flip(image, flip_x, flip_y)
            elif event.key == pg.K_d:
                flip_y = not flip_y
                image = pge.flip(image, flip_x, flip_y)
                
    pge.screen.fill(pge.Colors.GRAY.rgb)
    pge.screen.blit(image, (520,240))
    pge.update()
    pge.fpsw()