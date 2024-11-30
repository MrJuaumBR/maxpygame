# Import PyGameEngine
import pygameengine as pyge
import pygameengine.widgets as pw


# Init PyGameEngine
pge = pyge.PyGameEngine()

# Create Screen
S_W,S_H = (640,400)
screen = pge.createScreen(S_W,S_H, pyge.pg.HWSURFACE|pyge.pg.RESIZABLE)
pge.setScreenTitle("Hello, World!")

# Create a font
arial16 = pge.createSysFont('Arial', 16)
arial24 = pge.createSysFont('Arial', 24)

pge.setFPS(60)
pge.enableFPS_unstable()

# Widgets
Widget_List:dict = {}
for i in range(1,10):
    Btn = pw.Button(pge, (35,(35*i)+15),arial24, "Button for: "+str(i), [pge.Colors.DARKGRAY, pge.Colors.WHITE, pge.Colors.LIGHTGRAY], id=f'button{i}', tip=(f'Button ID: {i}', arial16))
    Widget_List[f'{pge.stringToKey(str(i))}'] = Btn

while True:
    pge.draw_text((5,5), f'FPS: {pge.fps}, ScreenSize: {pge.screen_size}', arial24, pge.Colors.WHITE)
    for event in pge.events:
        if event.type == pyge.QUIT:
            pge.exit()
        if event.type == pyge.KEYDOWN:
            if event.key == pyge.K_ESCAPE:
                pge.exit()
            elif event.key in [pyge.K_1, pyge.K_2, pyge.K_3, pyge.K_4, pyge.K_5, pyge.K_6, pyge.K_7, pyge.K_8, pyge.K_9]:
                Button = Widget_List[str(event.key)]
                Button.enable = not Button.enable
                
    pge.update()
    pge.screen.fill((0,0,0))
    pge.draw_widgets()