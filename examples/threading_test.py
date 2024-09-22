# Import PyGameEngine
import pygameengine as pyge
import threading, math

# Init PyGameEngine
pge = pyge.PyGameEngine()

# Create Screen
screen = pge.createScreen(1024, 720)
pge.setScreenTitle("Hello, World!")

def second_thread():
    x,y = 0,0
    
    color = pyge.reqColor(0,0,0)
    
    while pge.is_running:
        pge.draw_rect((x,y),(50,50),color)
        color = pge.Colors.random()

def main_loop():
    pge.setFPS(30)
    x,y = 500,500
    threading.Thread(target=second_thread).start()
    
    color = pyge.reqColor(0,0,0)
    
    speed = 5
    directionx, directiony = 1, 1
    while True:
        pge.draw_rect((x, y), (50,50), color)
        
        if x > 1024-50:
            directionx = -1
            color = pge.Colors.random()
        elif x < 0:
            directionx = 1
            color = pge.Colors.random()
        if y > 720-50:
            directiony = -1
            color = pge.Colors.random()
        elif y < 0:
            directiony = 1
            color = pge.Colors.random()
        
        x += directionx * speed
        y += directiony * speed
        
        
        for ev in pge.events:
            if ev.type == pyge.QUIT:
                pge.exit()
            elif ev.type == pyge.KEYDOWN:
                if ev.key == pyge.K_ESCAPE:
                    pge.exit()
                    
        pge.update()
        pge.fill(pge.Colors.WHITE)
        pge.fpsw()

main_loop()