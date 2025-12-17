import pygame
import numpy as np
from sprite import sprites, Sprite
from player import Player
from input import keys_down
from map import Map, TileKind

# Import the filters
from filters import (
    apply_snake_vision, 
    apply_bee_vision, 
    apply_bat_vision, 
    apply_eagle_vision, 
    apply_dog_vision, 
    apply_deepsea_vision
)

# Set up 
pygame.init()

pygame.display.set_caption("Adventure Game")
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

clear_color = (30, 150, 50)
running = True

tile_kinds = [
    TileKind("dirt", "images/dirt.png", False),
    TileKind("grass", "images/grass.png", False),
    TileKind("water", "images/water.png", True), 
    TileKind("wood", "images/wood.png", False)
]

player = Player("images/man.png", 32*11, 32*7)
map = Map("maps/start.map", tile_kinds, 32)

Sprite("images/tree.png", 0 * 32, 0 * 32)
Sprite("images/tree.png", 7 * 32, 2 * 32)
Sprite("images/tree.png", 1 * 32, 10* 32)
Sprite("images/tree.png", 12* 32, -1* 32)
Sprite("images/tree.png", 14* 32, 9 * 32)
Sprite("images/tree.png", 12* 32, -1* 32)
Sprite("images/tree.png", 13* 32, 12* 32)
Sprite("images/tree.png", 20* 32, 9 * 32)
Sprite("images/tree.png", 22* 32, -1* 32)
Sprite("images/tree.png", 24* 32, 12* 32)
Sprite("images/tree.png", 2 * 32, 8 * 32)
Sprite("images/tree.png", 15* 32, 15* 32)
Sprite("images/tree.png", 17 * 32,1 * 32)
Sprite("images/tree.png", 1 * 32, 15 * 32)

# Camera definition
camera = pygame.Rect(0, 0, screen_width, screen_height)

# Current active filter
current_filter = None

# Game Loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            keys_down.add(event.key)
            
            if event.key == pygame.K_0: current_filter = None
            if event.key == pygame.K_1: current_filter = "snake"
            if event.key == pygame.K_2: current_filter = "bee"
            if event.key == pygame.K_3: current_filter = "bat"
            if event.key == pygame.K_4: current_filter = "eagle"
            if event.key == pygame.K_5: current_filter = "dog"
            if event.key == pygame.K_6: current_filter = "fish"

        elif event.type == pygame.KEYUP:
            keys_down.remove(event.key)

    # Update Code
    player.update(map)

    # Update Camera
    camera.center = player.rect.center
    if camera.left < 0: camera.left = 0
    if camera.top < 0: camera.top = 0
    if camera.right > map.pixel_width: camera.right = map.pixel_width
    if camera.bottom > map.pixel_height: camera.bottom = map.pixel_height

    # Draw Code
    screen.fill(clear_color)
    
    map.draw(screen, camera)
    for s in sprites:
        s.draw(screen, camera)
        
    # --- Apply Active Filter ---
    if current_filter == "snake":
        filtered_surf = apply_snake_vision(screen)
        screen.blit(filtered_surf, (0, 0))
    elif current_filter == "bee":
        filtered_surf = apply_bee_vision(screen)
        screen.blit(filtered_surf, (0, 0))
    elif current_filter == "bat":
        filtered_surf = apply_bat_vision(screen)
        screen.blit(filtered_surf, (0, 0))
        
    elif current_filter == "eagle":
        # --- NEW: Calculate player's screen position ---
        player_screen_pos = (player.rect.centerx - camera.x, player.rect.centery - camera.y)
        # Pass it to the filter
        filtered_surf = apply_eagle_vision(screen, player_pos=player_screen_pos)
        screen.blit(filtered_surf, (0, 0))
        # -----------------------------------------------
        
    elif current_filter == "dog":
        filtered_surf = apply_dog_vision(screen)
        screen.blit(filtered_surf, (0, 0))
    elif current_filter == "fish":
        filtered_surf = apply_deepsea_vision(screen)
        screen.blit(filtered_surf, (0, 0))

    pygame.display.flip()
    pygame.time.delay(17)

pygame.quit()