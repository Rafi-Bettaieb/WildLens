import pygame
from sprite import Sprite, sprites
from input import is_key_pressed

class Player(Sprite):
    def __init__(self, image_path, x, y):
        # We manually initialize to handle the sprite sheet logic
        self.x = x
        self.y = y
        
        # Load and slice the sprite sheet
        self.load_sprites(image_path)
        
        # Animation state
        self.direction = "S" # Default facing South
        self.frame_index = 0
        self.walk_counter = 0
        self.image = self.images["manS0"] # Set initial image
        
        # Add self to the game's sprite list so it gets drawn
        sprites.append(self)

    def load_sprites(self, path):
        # Load the sprite sheet
        sheet = pygame.image.load(path).convert_alpha()
        self.images = {}
        
        # Dimensions from WildLens assets
        orig_w, orig_h = 16, 16
        scale = 2 # Scale to 32x32 to fit the map tiles
        final_w, final_h = orig_w * scale, orig_h * scale
        
        directions = ["N", "E", "S", "W"]
        
        # Slice the sheet
        for row, direction in enumerate(directions):
            for col in range(4):
                # The animation pattern in the sheet is 0, 1, 2. 
                # WildLens logic uses column 1 for the 4th frame (index 3) to create a loop (0, 1, 2, 1)
                sheet_col = 1 if col == 3 else col
                
                rect = pygame.Rect(sheet_col * orig_w, row * orig_h, orig_w, orig_h)
                sub = sheet.subsurface(rect)
                self.images[f"man{direction}{col}"] = pygame.transform.scale(sub, (final_w, final_h))

    def update(self):
        speed = 2
        moving = False
        
        # Handle movement (Supports ZSQD and Arrow Keys)
        if is_key_pressed(pygame.K_z) or is_key_pressed(pygame.K_UP):
            self.y -= speed
            self.direction = "N"
            moving = True
        elif is_key_pressed(pygame.K_s) or is_key_pressed(pygame.K_DOWN):
            self.y += speed
            self.direction = "S"
            moving = True
        
        if is_key_pressed(pygame.K_q) or is_key_pressed(pygame.K_LEFT):
            self.x -= speed
            self.direction = "W"
            moving = True
        elif is_key_pressed(pygame.K_d) or is_key_pressed(pygame.K_RIGHT):
            self.x += speed
            self.direction = "E"
            moving = True
            
        # Handle Animation
        if moving:
            self.walk_counter += 1
            anim_speed = 5 # Change frame every 5 ticks
            
            # Cycle through frames 0-3
            self.frame_index = (self.walk_counter // anim_speed) % 4
            
            # Update the sprite's image
            self.image = self.images[f"man{self.direction}{self.frame_index}"]
        else:
            # Reset to standing frame (frame 0) when stopped
            self.image = self.images[f"man{self.direction}0"]