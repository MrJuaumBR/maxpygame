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

orig_image = image
image_rect = image.get_rect(center=(320, 240))

angle:int = 0

while True:
    for event in pge.events:
        if event.type == pg.QUIT:
            exit()

    angle += 1
    image, image_rect = pge.rotate(orig_image, image_rect, angle)

    pge.screen.fill(pge.Colors.GRAY.rgb)
    pge.screen.blit(image, image_rect)
    pge.update()
    pge.fpsw()