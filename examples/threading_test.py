# Import PyGameEngine
import pygameengine as pyge
import threading

# Init PyGameEngine
pge = pyge.PyGameEngine()

# Create Screen
screen = pge.createScreen(1024, 720)
pge.setScreenTitle("Hello, World!")

def second_thread():
    while pge.is_running:
        pge.draw_rect((0,0),(50,50),pge.Colors.BLACK)


def main_loop():
    pge.setFPS(30)
    threading.Thread(target=second_thread).start()
    while True:
        pge.draw_rect((100, 100), (50,50), pge.Colors.RED)
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