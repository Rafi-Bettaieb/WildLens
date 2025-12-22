import pygame
from input import keys_down
# Import sprites list to add player to drawing loop
from sprite import sprites 

class Player:
    def __init__(self, image_path, x, y):
        # --- Dimensions du hitbox (zone de collision) ---
        self.width = 30 
        self.height = 30
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.speed = 3

        # --- GESTION DES ANIMATIONS ---
        self.animations = {}
        # Start standing (frame index 4 is the 5th column)
        self.frame_index = 4 
        self.animation_speed = 5 
        self.animation_timer = 0
        self.direction = 'down' 
        
        # Chargement et découpage du spritesheet
        self.load_spritesheet(image_path)
        
        # Safety check
        if self.direction not in self.animations:
            self.direction = list(self.animations.keys())[0]
            
        self.image = self.animations[self.direction][self.frame_index]
        
        # Offset pour centrer le sprite
        self.sprite_offset_x = (self.frame_width - self.width) // 2
        self.sprite_offset_y = (self.frame_height - self.height) 

        # Add self to sprites list so level1.py draws it
        sprites.append(self)

    def load_spritesheet(self, path):
        sheet = pygame.image.load(path).convert_alpha()
        sheet_w, sheet_h = sheet.get_size()
        
        # 5 Columns (0-3: Walk, 4: Stand) and 8 Rows (Directions)
        cols = 5
        rows = 8
        
        self.frame_width = sheet_w // cols
        self.frame_height = sheet_h // rows
        
        # Mapping based on your request
        dir_map = {
            0: 'up', 
            1: 'down', 
            2: 'down_right', 
            3: 'right',
            4: 'up_right', 
            5: 'down_left', 
            6: 'left', 
            7: 'up_left'
        }

        for row_idx, direction in dir_map.items():
            self.animations[direction] = []
            for col_idx in range(cols):
                rect = pygame.Rect(col_idx * self.frame_width, row_idx * self.frame_height, self.frame_width, self.frame_height)
                frame = sheet.subsurface(rect)
                self.animations[direction].append(frame)

    def update(self, map_obj):
        vx = 0
        vy = 0
        
        # 1. Gestion des touches
        if pygame.K_LEFT in keys_down or pygame.K_q in keys_down:
            vx = -self.speed
        if pygame.K_RIGHT in keys_down or pygame.K_d in keys_down:
            vx = self.speed
        if pygame.K_UP in keys_down or pygame.K_z in keys_down:
            vy = -self.speed
        if pygame.K_DOWN in keys_down or pygame.K_s in keys_down:
            vy = self.speed
            
        # 2. Normalisation (Diagonal speed fix)
        if vx != 0 and vy != 0:
            vx *= 0.7071
            vy *= 0.7071

        # 3. Direction determination
        if vy > 0:
            if vx > 0: self.direction = 'down_right'
            elif vx < 0: self.direction = 'down_left'
            else: self.direction = 'down'
        elif vy < 0:
            if vx > 0: self.direction = 'up_right'
            elif vx < 0: self.direction = 'up_left'
            else: self.direction = 'up'
        else:
            if vx > 0: self.direction = 'right'
            elif vx < 0: self.direction = 'left'
            # If idle, keep previous direction

        # 4. Animation Logic
        is_moving = vx != 0 or vy != 0
        
        if is_moving:
            # If we were standing (index 4), reset to walking cycle (0) immediately
            if self.frame_index == 4:
                self.frame_index = 0
                
            self.animation_timer += 1
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0
                # Loop through first 4 frames ONLY (0, 1, 2, 3)
                self.frame_index = (self.frame_index + 1) % 4
        else:
            # Not moving? Use the last column (index 4) for Standing
            self.frame_index = 4
            self.animation_timer = 0
            
        self.image = self.animations[self.direction][self.frame_index]

        # 5. Mouvement & Collisions
        # Axe X
        new_x = self.rect.x + vx
        if not self.check_collision(new_x, self.rect.y, map_obj):
            self.rect.x = new_x
            
        # Axe Y
        new_y = self.rect.y + vy
        if not self.check_collision(self.rect.x, new_y, map_obj):
            self.rect.y = new_y

        # Limites écran
        self.rect.x = max(0, min(self.rect.x, map_obj.pixel_width - self.width))
        self.rect.y = max(0, min(self.rect.y, map_obj.pixel_height - self.height))

    def check_collision(self, x, y, map_obj):
        # 1. Map Tiles
        if map_obj.is_blocked(x, y, self.width, self.height):
            return True
        
        # 2. Other Sprites (Trees)
        future_rect = pygame.Rect(x, y, self.width, self.height)
        for s in sprites:
            if s is self: continue # Skip self
            if s.rect.colliderect(future_rect):
                return True
        return False

    def draw(self, surface, camera):
        draw_x = self.rect.x - camera.x - self.sprite_offset_x
        draw_y = self.rect.y - camera.y - self.sprite_offset_y
        surface.blit(self.image, (draw_x, draw_y))