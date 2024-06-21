import pygame, colorsys, cv2, numpy as np
from pygame import image, transform, surface, font, draw
from tkinter.filedialog import askopenfilename

default_text_font = font.SysFont("Arial", 24)

def create_multiline_text(text: str, size: tuple[int, int] = None, font_size: int = None, font_family: str = None) -> surface.Surface:
    _font_size = font_size or 24
    _font_family = font_family or "Arial"

    _font = font.SysFont(
        _font_family, _font_size) if font_size or font_family else default_text_font

    lines = text.splitlines()
    line_count = len(lines)

    surfaces: list[surface.Surface] = []

    width = 0
    height = line_count * (_font_size + 5) - 5

    for line in lines:
        line_surface = _font.render(line, True, (255, 255, 255))
        _width = line_surface.get_width()
        if _width > width:
            width = _width

        surfaces.append(line_surface)

    _surface = surface.Surface((width + 10, height + 10), pygame.SRCALPHA)

    draw.rect(_surface, (0, 0, 0, 100), _surface.get_rect(), border_radius=5)

    for i, line in enumerate(surfaces):
        _surface.blit(line, (5, i * (_font_size + 5)))

    if size:
        _surface = transform.scale(_surface, size)

    draw.rect(_surface, (0, 0, 0), _surface.get_rect(), 2, border_radius=5)

    return _surface

def surface_to_grid(surface:pygame.Surface):
    w, h = surface.get_size()
    grid = []
    
    for rr in range(h):
        row = []
        
        for cc in range(w):
            r, g, b, a = surface.get_at((cc, rr))
            h, s, v = colorsys.rgb_to_hsv(r, g, b)
            
            if s < 20 and v < 70: # make sure black-dark gray pixels are 1
                row.append(1)
            else:
                row.append(0)
                
        grid.append(row)
        
    return grid

def find_points(image_path):
    image = cv2.imread(image_path)

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    lower_blue = np.array([90, 50, 50])
    upper_blue = np.array([130, 255, 255])
    lower_red1 = np.array([0, 70, 50])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 70, 50])
    upper_red2 = np.array([180, 255, 255])

    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)

    mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask_red = cv2.bitwise_or(mask_red1, mask_red2)

    blue_coords = np.column_stack(np.where(mask_blue > 0))
    red_coords = np.column_stack(np.where(mask_red > 0))

    if blue_coords.size == 0 or red_coords.size == 0:
        return None, None

    blue_pos = tuple(np.mean(blue_coords, axis=0).astype(int))
    red_pos = tuple(np.mean(red_coords, axis=0).astype(int))

    print(f"Blue position: {blue_pos}, Red position: {red_pos}")
    return blue_pos, red_pos


def import_map():
    file = askopenfilename(filetypes=[(
        "Pygame Supported Image Files", ".bmp .jpeg .jpg .pcx .png .pnm .tiff .webp .xpm")])
       
    blue, red = find_points(file)
    
    _surface = image.load(file).convert()

    return _surface, blue, red

