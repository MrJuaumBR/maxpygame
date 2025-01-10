# Import PyGameEngine
import pygameengine as pyge

# Init PyGameEngine
pge = pyge.PyGameEngine()

# Create Screen
S_W,S_H = (400,420)
screen = pge.createScreen(S_W,S_H, pyge.pg.HWSURFACE)
pge.setScreenTitle("Hello, World!")

# Create a font
arial16= pge.createSysFont('Arial', 16)
arial12= pge.createSysFont('Arial', 12)

Text = """O que é Lorem Ipsum?\nLorem Ipsum é simplesmente uma simulação de texto da indústria tipográfica e de impressos, e vem sendo utilizado desde o século XVI, quando um impressor desconhecido pegou uma bandeja de tipos e os embaralhou para fazer um livro de modelos de tipos. Lorem Ipsum sobreviveu não só a cinco séculos, como também ao salto para a editoração eletrônica, permanecendo essencialmente inalterado. Se popularizou na década de 60, quando a Letraset lançou decalques contendo passagens de Lorem Ipsum, e mais recentemente quando passou a ser integrado a softwares de editoração eletrônica como Aldus PageMaker.\nPorque nós o usamos?\nÉ um fato conhecido de todos que um leitor se distrairá com o conteúdo de texto legível de uma página quando estiver examinando sua diagramação. A vantagem de usar Lorem Ipsum é que ele tem uma distribuição normal de letras, ao contrário de "Conteúdo aqui, conteúdo aqui", fazendo com que ele tenha uma aparência similar a de um texto legível. Muitos softwares de publicação e editores de páginas na internet agora usam Lorem Ipsum como texto-modelo padrão, e uma rápida busca por 'lorem ipsum' mostra vários websites ainda em sua fase de construção. Várias versões novas surgiram ao longo dos anos, eventualmente por acidente, e às vezes de propósito (injetando humor, e coisas do gênero)."""

# Create a surface
TextBox_Widget = pyge.Longtext(pge, (2,30), arial16, Text, [pge.Colors.BLACK, pge.Colors.GRAY, pge.Colors.WHITE, pge.Colors.WHITE])

print('\n\n',TextBox_Widget.get_lines(),'\n\n')

y_shift = 0

# Enable/Disable controller emulation
pge.setMouseEmulation(True)

while True:
    pge.draw_text((0,0), f"Mouse Scroll: {pge.mouse.scroll}, Smooth Scroll: {"On" if pge.mouse.smooth_scroll else "Off"}", arial12, pge.Colors.WHITE,bgColor=pge.Colors.DARKGRAY, surface=screen)
    for ev in pge.events:
        if ev.type == pyge.QUIT:
            pge.exit()
        if ev.type == pyge.KEYDOWN:
            if ev.key == pyge.K_ESCAPE:
                pge.exit()
            elif ev.key == pyge.K_m:
                pge.mouse.smooth_scroll = not pge.mouse.smooth_scroll
    
    if abs(pge.mouse.scroll) > 0:
        y_shift += pge.mouse.scroll * 5
    if abs(y_shift) > 0:
        TextBox_Widget.rect.y += y_shift
        y_shift = 0
    
    pge.update()
    pge.fpsw()
    pge.fill(pge.Colors.WHITE)
    pge.draw_widgets()