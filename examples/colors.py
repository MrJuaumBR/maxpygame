# Import PyGameEngine
import pygameengine as pyge

# Init PyGameEngine
pge = pyge.PyGameEngine()

# Create Screen
S_W,S_H = (1024,768)
screen = pge.createScreen(S_W,S_H)
pge.setScreenTitle("Hello, World!")

# Create a font
arial12 = pge.createSysFont('Arial', 12)

# pge.setFPS(60)
# pge.enableFPS_unstable()

# Create a surface
X_SHIFT = 0
Y_SHIFT = 0
size_add = 50

per_line = 16
max_x = 600

zoom = 0.5

pge.setFPS(1000)

pge.setMouseEmulation(True)

while True:
    # Add colors_surf
    x,y = 0,0
    ii = 0
    ind = 0
    for color in pge.Colors.__dict__.keys():
        if not (color in pge.Colors.aliases) and type(pge.Colors.__dict__[color]) == pyge.reqColor:
            ind += 1
            text_c = pge.Colors.get(color)
            if text_c.brightness > 0.4: text_c = pge.Colors.BLACK
            else: text_c = pge.Colors.WHITE
            
            text_size = arial12.size(str(color))
            rect_size = [size_add if text_size[0]-5 < size_add else text_size[0]+10,size_add]
            
            # Draw Rect
            color_rect = pge.draw_rect(((x+zoom)+X_SHIFT,(y+zoom)+Y_SHIFT),(rect_size[0]*zoom,rect_size[1]*zoom), pge.Colors.get(color), border_color=text_c, border_width=int(2*zoom))
            # Draw Text
            pge.draw_text((color_rect.x+3, color_rect.y+3),str(color) + f' {ind}',arial12, text_c, surface=screen)
            
            x += color_rect.width
            ii += 1
            if ii >= per_line or x >= max_x:
                x = 0
                ii = 0
                y += color_rect.height
    pge.draw_text((S_W-300,S_H-20), f'X: {X_SHIFT}, Y: {Y_SHIFT}, Zoom: {round(zoom,4)}, Colors: {pge.Colors.number_of_colors()}, Aliases: {len(pge.Colors.aliases)}, FPS: {int(pge.getFPS())}', arial12, pge.Colors.WHITE, surface=screen)
    
    if pge.joystick.mainController:
        x,y = pge.joystick.mainController.getAxisByString('left')
        Y_SHIFT += y * -(5*zoom)
        X_SHIFT += x * -(5*zoom)
    keys = pge.getKeys()
    if keys[pyge.K_w] or keys[pyge.K_UP]:
        Y_SHIFT += 10
    if keys[pyge.K_s] or keys[pyge.K_DOWN]:
        Y_SHIFT -= 10
    if keys[pyge.K_a] or keys[pyge.K_LEFT]:
        X_SHIFT += 10
    if keys[pyge.K_d] or keys[pyge.K_RIGHT]:
        X_SHIFT -= 10
        
    if keys[pyge.K_q]:
        zoom += 0.025
    if keys[pyge.K_e]:
        zoom -= 0.025
    if abs(pge.mouse.scroll) > 0:
        zoom += pge.mouse.scroll*0.05
    if zoom < 0.1:
        zoom = 0.1
    elif zoom > 1.5:
        zoom = 1.5
    
    # Detect events
    for ev in pge.events:
        # Quit if the user closes the window
        if ev.type == pyge.QUIT:
            pge.exit()
        elif ev.type == pyge.KEYDOWN:
            if ev.key == pyge.K_ESCAPE:
                pge.exit()
            elif ev.key == pyge.K_1:
                pge.mouse.smooth_scroll = not pge.mouse.smooth_scroll
                print(f'Mouse Smooth Scroll: {"On" if pge.mouse.smooth_scroll else "Off"}')
                
    
    # Update the screen
    pge.update()
    pge.fpsw()
    # Clear the screen
    pge.fill(pge.Colors.BLACK)
    
    