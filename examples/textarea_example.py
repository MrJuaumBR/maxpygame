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

pge.input_query_enable = True

# Create a font
arial16 = pge.createSysFont('Arial', 16)

# Text
# Get python arg
text:str = 'A Thing'
if len(sys.argv) > 1:
    text = ''
    this_file, path = sys.argv
    with open(path, 'rb') as f:
        text:bytes = f.read()
    text = text.decode()
    
Textarea:pyge.Textarea = pge.create_widget(pyge.Textarea, (10, 15), [pge.Colors.LIGHTBLUE, pge.Colors.DARKGRAY,pge.Colors.WHITE, pge.Colors.LIGHTGRAY], arial16, text,placeholder='Textarea Placeholder', id='textbox1')

# You can now disable textarea edit:
Textarea.editable = True

while True:
    Textarea.position = Textarea.position[0], Textarea.position[1]+pge.mouse.scroll*5
    
    for ev in pge.events:
        if ev.type == pyge.QUIT:
            pge.exit()
    
    if pge.input_query.HasKey(pyge.K_F1):
        pge.input_query.RemoveFromQueryByKey(pyge.K_F1)
        print('Textarea text:', Textarea.text)
            
    pge.update()
    pge.fpsw()
    
    pge.fill(pge.Colors.BLACK)
    pge.draw_widgets()