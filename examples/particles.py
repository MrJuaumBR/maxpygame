# Import PyGameEngine
print("Import")
import pygameengine as pyge


# Init PyGameEngine
pge = pyge.PyGameEngine()

# Create Screen
screen = pge.createScreen(1024, 720)
pge.setScreenTitle("Hello, World!")

# Fonts
arial16 = pge.createSysFont('Arial', 16)
arial12 = pge.createSysFont('Arial', 12)

# Type Dropdown
ParticleType = pyge.Dropdown(pge, (10, 35), [pge.Colors.WHITE, pge.Colors.GRAY, pge.Colors.DARKGRAY], ['Fire','Rainbow','Purple','Green','Water','Smoke'], arial16, id='dropdown1')

pge.enableFPS_unstable()
pge.setFPS(500)


pge.CreateParticle((360, 250), 2, pyge.PARTICLES_PRESETS['smoke'], 25, 10,5, 'all', respawn_threshold=0.5 , anchored=True, continuity=True)
pge.CreateParticle((650, 250), 2, pyge.PARTICLES_PRESETS['fire'], 25, 10,5, 'up', respawn_threshold=0.2 , anchored=True, continuity=True)
pge.CreateParticle((75, 250), 2, pyge.PARTICLES_PRESETS['water'], 25, 10,5, 'down', respawn_threshold=0.5, anchored=True, continuity=True)
while True:
    # Draw avg fps
    pge.draw_text((0,0), f"FPS: {int(pge.getFPS())}, Avg: {int(pge.getAvgFPS())}, Particles: {len(pge.particles)}", arial12, pge.Colors.WHITE,bgColor=pge.Colors.DARKGRAY, surface=screen)
    for ev in pge.events:
        if ev.type == pyge.QUIT:
            pge.exit()
        elif ev.type == pyge.MOUSEBUTTONDOWN:
            if ev.button == 1:
                pge.CreateParticle(pge.mouse.pos, 2, pyge.PARTICLES_PRESETS[str(ParticleType.text).lower()], 25, 10,10, 'all')
    
    pge.draw_widgets()
    pge.update()
    pge.fpsw()
    # Clear the screen
    pge.fill(pge.Colors.BLACK)