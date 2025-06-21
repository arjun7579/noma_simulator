# simvis.py

import pygame
import time
import json
import os
from config import WORLD_LIMIT, VISION_RADIUS

# Constants
W, H = WORLD_LIMIT * 2, WORLD_LIMIT * 2
GRID_SPACING = 50

# Init
pygame.init()
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("🛰️ NOMA Drone Simulation (Centered World)")
font = pygame.font.SysFont("Arial", 12)

def transform(x, y):
    """Convert world (x, y) to screen coordinates with (0,0) at bottom-left."""
    return int(x + WORLD_LIMIT), int(H - (y + WORLD_LIMIT))

def draw_grid():
    screen.fill((255, 255, 255))
    for x in range(0, W + 1, GRID_SPACING):
        pygame.draw.line(screen, (220, 220, 220), (x, 0), (x, H))
        label = font.render(str(x - WORLD_LIMIT), True, (120, 120, 120))
        screen.blit(label, (x + 4, H - 18))

    for y in range(0, H + 1, GRID_SPACING):
        pygame.draw.line(screen, (220, 220, 220), (0, y), (W, y))
        label = font.render(str(y - WORLD_LIMIT), True, (120, 120, 120))
        screen.blit(label, (4, H - y - 18))

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            exit()

    draw_grid()

    if os.path.exists("world_state.json"):
        try:
            state = json.load(open("world_state.json"))
        except json.JSONDecodeError:
            continue

        # Obstacles - red
        for ox, oy in state.get("obstacles", []):
            pygame.draw.circle(screen, (255, 0, 0), transform(ox, oy), 5)

        # Users - green
        for ux, uy in state.get("users", []):
            pygame.draw.circle(screen, (0, 180, 0), transform(ux, uy), 4)

        # Drones - blue + radius + label
        for idx, (dx, dy) in enumerate(state.get("drones", [])):
            px, py = transform(dx, dy)
            pygame.draw.circle(screen, (0, 0, 255), (px, py), 7)
            pygame.draw.circle(screen, (255, 0, 0), (px, py), VISION_RADIUS, 1)
            label = font.render(f"D{idx}", True, (0, 0, 0))
            screen.blit(label, (px + 8, py + 6))

    pygame.display.flip()
    time.sleep(0.1)

