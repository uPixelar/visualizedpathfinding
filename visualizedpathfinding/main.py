import pygame
from pygame import image, transform, time as ptime, surface, font, event, display, draw
from tkinter import Tk

# Initialization

tk_app = Tk()
tk_app.withdraw() # hide default window


WIDTH = 1280
HEIGHT = 720

pygame.init()
screen = display.set_mode((WIDTH, HEIGHT))

# Main

from algorithm import Algorithm, BFS, GBFS, AStar, Node
from utils import surface_to_grid, import_map, create_multiline_text

# Constant Variables
FPS = 60

# Variables
running = True
simulating = False
simulatable = False
dt = 0
speed = 10
algorithm: Algorithm = None
is_help_open = True

# Game Objects
clock = ptime.Clock()
default_font = font.SysFont("Arial", 30)

# Surfaces
pause_button = transform.scale(image.load("assets/pause.jpg").convert(), (50, 50))
play_button = transform.scale(image.load("assets/play.jpg").convert(), (50, 50))
map_original = surface.Surface((1, 1))
map_surface = map_original.copy()
map_display = map_surface.copy()
non_simulatable = default_font.render("Non simulatable", True, (255, 0, 0), (0, 0, 0, 100))
algorithm_text = default_font.render("NO ALGORITHM", True, (0, 200, 30))
help_surface = create_multiline_text("""\
Keymap: 
[H]: Toggle Help
[J]: Import Map
[K]: Toggle Simulation

Algorithms
[1]: BFS
[2]: GBFS
[3]: A*
"""
)

# Custom functions

def draw_path(map_surface:surface.Surface, node:Node):
    surf = map_surface.copy()
    
    while node:
        r, c = node.state
        surf.set_at((c, r), (0, 255, 0))
        node = node.parent
    
    return surf

# Maze
grid = blue = red = None
       
while running:
    for e in event.get():
        if e.type == pygame.QUIT:
            running = False
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                running = False
            elif e.key == pygame.K_h:
                is_help_open = not is_help_open
            elif e.key == pygame.K_j:
                map_original, blue, red = import_map()
                map_surface = map_original.copy()
                map_display = transform.scale(map_surface, (WIDTH, HEIGHT))
                simulatable = blue and red
                if simulatable:
                    grid = surface_to_grid(map_surface)
                    algorithm = BFS(grid, blue, red)
                    algorithm_text = default_font.render("[1]: BFS", True, (0, 200, 30))
                
            elif e.key == pygame.K_k and simulatable:
                simulating = not simulating
            elif e.key == pygame.K_1 and simulatable:
                map_surface = map_original.copy()
                map_display = transform.scale(map_surface.copy(), (WIDTH, HEIGHT))
                algorithm = BFS(grid, blue, red)
                algorithm_text = default_font.render("[1]: BFS", True, (0, 200, 30))
                simulating = False
            elif e.key == pygame.K_2 and simulatable:
                map_surface = map_original.copy()
                map_display = transform.scale(map_surface.copy(), (WIDTH, HEIGHT))
                algorithm = GBFS(grid, blue, red)
                algorithm_text = default_font.render("[2]: GBFS", True, (0, 200, 30))
                simulating = False
            elif e.key == pygame.K_3 and simulatable:
                map_surface = map_original.copy()
                map_display = transform.scale(map_surface.copy(), (WIDTH, HEIGHT))
                algorithm = AStar(grid, blue, red)
                algorithm_text = default_font.render("[3]: A*", True, (0, 200, 30))
                simulating = False

    screen.fill("white")
    
    if simulating and not algorithm.finished:
        for i in range(speed):
            current_node = algorithm.solve()
            r, c = current_node.state
            map_surface.set_at((c, r), (200, 200, 0, 100))
            pathed = draw_path(map_surface, current_node)
            map_display = transform.scale(pathed, (WIDTH, HEIGHT))
            
            if algorithm.found:
                
                simulating = False
            
    
    screen.blit(map_display, (0, 0))
    
    # OVERLAYS
    screen.blit(play_button if simulating else pause_button, (WIDTH - 55, 5, 50, 50))
    
    if simulatable:
        screen.blit(algorithm_text, algorithm_text.get_rect(bottomleft=(0, HEIGHT)))
    else:
        screen.blit(non_simulatable, non_simulatable.get_rect(midbottom=(WIDTH / 2, HEIGHT - 10)))

    if algorithm and algorithm.finished:
        cost_surf = default_font.render(f"Cost: {algorithm.cost} Length: {len(algorithm.solution)}", True, (0, 0, 0))
        screen.blit(cost_surf, cost_surf.get_rect(bottomright=(WIDTH, HEIGHT)))

    if is_help_open: 
        screen.blit(help_surface, (0, 0))

    display.flip()
    dt = clock.tick(FPS)

pygame.quit()  # quit pygame
tk_app.destroy()  # quit tkinter