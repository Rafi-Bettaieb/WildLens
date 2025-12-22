import pygame
from sprite import Sprite, sprites
from input import is_key_pressed

class Player(Sprite):
    def __init__(self, image_path, x, y):
        self.x = x
        self.y = y
        
        # --- NEW: Store starting position for respawn ---
        self.start_x = x
        self.start_y = y
        # ------------------------------------------------
        
        # Load and slice the sprite sheet
        self.load_sprites(image_path)
        
        # Animation state
        self.direction = "S" 
        self.frame_index = 0
        self.walk_counter = 0
        self.image = self.images["manS0"]
        
        # Player dimensions (32x32)
        self.width = 32
        self.height = 32
        self.rect = pygame.Rect(x, y, self.width, self.height)
        
        sprites.append(self)

    def load_sprites(self, path):
        sheet = pygame.image.load(path).convert_alpha()
        self.images = {}
        orig_w, orig_h = 16, 16
        scale = 2
        final_w, final_h = orig_w * scale, orig_h * scale
        directions = ["N", "E", "S", "W"]
        for row, direction in enumerate(directions):
            for col in range(4):
                sheet_col = 1 if col == 3 else col
                rect = pygame.Rect(sheet_col * orig_w, row * orig_h, orig_w, orig_h)
                sub = sheet.subsurface(rect)
                self.images[f"man{direction}{col}"] = pygame.transform.scale(sub, (final_w, final_h))

    def update(self, map_obj):
        speed = 2
        dx = 0
        dy = 0
        moving = False
        
        if is_key_pressed(pygame.K_z) or is_key_pressed(pygame.K_UP):
            dy = -speed
            self.direction = "N"
            moving = True
        elif is_key_pressed(pygame.K_s) or is_key_pressed(pygame.K_DOWN):
            dy = speed
            self.direction = "S"
            moving = True
        
        if is_key_pressed(pygame.K_q) or is_key_pressed(pygame.K_LEFT):
            dx = -speed
            self.direction = "W"
            moving = True
        elif is_key_pressed(pygame.K_d) or is_key_pressed(pygame.K_RIGHT):
            dx = speed
            self.direction = "E"
            moving = True
            
        # Move X axis and check collision
        if dx != 0:
            new_x = self.x + dx
            if not self.check_collision(new_x, self.y, map_obj):
                self.x = new_x

        # Move Y axis and check collision
        if dy != 0:
            new_y = self.y + dy
            if not self.check_collision(self.x, new_y, map_obj):
                self.y = new_y
        
        # --- CHANGED: Boundaries Constraint (Clamp) ---
        # Prevent the player from crossing the map edges
        self.x = max(0, min(self.x, map_obj.pixel_width - self.width))
        self.y = max(0, min(self.y, map_obj.pixel_height - self.height))
        # ----------------------------------------------

        # Sync rect with new position
        self.rect.topleft = (self.x, self.y)

        # Handle Animation
        if moving:
            self.walk_counter += 1
            anim_speed = 5
            self.frame_index = (self.walk_counter // anim_speed) % 4
            self.image = self.images[f"man{self.direction}{self.frame_index}"]
        else:
            self.image = self.images[f"man{self.direction}0"]

    def check_collision(self, x, y, map_obj):
        # 1. Check Map (Tiles)
        if map_obj.is_blocked(x, y, self.width, self.height):
            return True
            
        # 2. Check Sprites (Trees)
        future_rect = pygame.Rect(x, y, self.width, self.height)
        for s in sprites:
            if s == self: continue # Don't collide with yourself
            if s.rect.colliderect(future_rect):
                return True
        return False