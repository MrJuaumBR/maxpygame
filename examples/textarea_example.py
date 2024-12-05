"""
Run with a command arg

example:

python .\textarea_example.py ./LICENSE
python .\textarea_example.py ./test.py
"""

# Import PyGameEngine
import pygameengine as pyge
import sys


# Init PyGameEngine
pge = pyge.PyGameEngine()

# Create Screen
screen = pge.createScreen(1024, 720)
pge.setScreenTitle("Hello, World!")

# Create a font
arial16 = pge.createSysFont('Arial', 16)

# Text
# Get python arg
text:str = ''
if len(sys.argv) > 1:
    this_file, path = sys.argv
    with open(path, 'rb') as f:
        text:bytes = f.read()
    text = text.decode()
    
Textarea:pyge.Textarea = pge.create_widget(pyge.Textarea, (10, 15), [pge.Colors.DARKGRAY, pge.Colors.LIGHTBLUE,pge.Colors.WHITE, pge.Colors.LIGHTGRAY], arial16, text, id='textbox1')

# You can now disable textarea edit:
Textarea.editable = False

while True:
    Textarea.position = Textarea.position[0], Textarea.position[1]+pge.mouse.scroll*5
    
    for ev in pge.events:
        if ev.type == pyge.QUIT:
            pge.exit()
        elif ev.type == pyge.KEYDOWN:
            if ev.key == pyge.K_F1:
                print(Textarea.text)
            
    pge.update()
    pge.fpsw()
    
    pge.fill(pge.Colors.BLACK)
    pge.draw_widgets()