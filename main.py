import pygame
from sprite import sprites, Sprite
from player import Player
from input import keys_down
from map import Map, TileKind


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

# Game Loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            keys_down.add(event.key)
        elif event.type == pygame.KEYUP:
            keys_down.remove(event.key)

    # Update Code
    player.update(map)

    # --- Update Camera ---
    # 1. Center the camera on the player
    camera.center = player.rect.center
    
    # 2. Clamp the camera so it doesn't show outside the map
    # Prevent left/top overflow
    if camera.left < 0: 
        camera.left = 0
    if camera.top < 0:
        camera.top = 0
        
    # Prevent right/bottom overflow
    if camera.right > map.pixel_width:
        camera.right = map.pixel_width
    if camera.bottom > map.pixel_height:
        camera.bottom = map.pixel_height
    # ---------------------

    # Draw Code
    screen.fill(clear_color)
    
    # Pass camera to draw functions
    map.draw(screen, camera)
    for s in sprites:
        s.draw(screen, camera)
        
    pygame.display.flip()

    # Cap the frames
    pygame.time.delay(17)


# Break down Pygame
pygame.quit()