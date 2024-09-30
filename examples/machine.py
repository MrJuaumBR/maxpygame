# Import PyGameEngine
import pygameengine as pyge


# Init PyGameEngine
pge = pyge.PyGameEngine()

# Create Screen
screen = pge.createScreen(620, 420)
pge.setScreenTitle("Hello, World!")

# Create a font
arial24 = pge.createSysFont('Arial', 24)
arial16 = pge.createSysFont('Arial', 16)
arial36 = pge.createSysFont('Arial', 36)
arial14 = pge.createSysFont('Arial', 14)
arial12 = pge.createSysFont('Arial', 12)

sysinfo = pge.getSystemDict()
while True:
    pge.draw_text((0,0), f'FPS: {pge.fps}', arial12, pge.Colors.BLACK)
    
    # System Info
    pge.draw_text((10, 10), 'System Info', arial24, pge.Colors.BLACK)
    pos = [15, 34]
    for info in sysinfo.keys():
        pge.draw_text(pos, f'{info}: {sysinfo[info]}', arial14, pge.Colors.BLACK)
        pos[1] += 20
    
    for event in pge.events:
        if event.type == pyge.QUIT:
            pge.exit()
            
    pge.update()
    pge.fill(pge.Colors.WHITE)
    pge.draw_widgets()