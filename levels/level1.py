import pygame
import sys
import os
import random

# --- IMPORTATION DES MODULES ---
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from map import Map, TileKind
from player import Player
from sprite import Sprite, sprites 
from input import keys_down 
from filters import (
    apply_snake_vision, 
    apply_bee_vision, 
    apply_bat_vision, 
    apply_eagle_vision, 
    apply_dog_vision, 
    apply_deepsea_vision
)

# [CORRECTION] Import du niveau 2 pour la transition
import levels.level2 as level2

# --- CLASSE MOUTON ---
class Sheep:
    def __init__(self, x, y, is_robot=False):
        self.width = 30
        self.height = 30
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.is_robot = is_robot
        self.move_timer = 0
        self.dx = 0
        self.dy = 0
        
        # Création de l'image (Carré blanc avec tête)
        self.image_normal = pygame.Surface((self.width, self.height))
        self.image_normal.fill((250, 250, 250)) # Blanc laine
        pygame.draw.rect(self.image_normal, (255, 200, 200), (20, 5, 8, 20)) # Tête rose
        pygame.draw.circle(self.image_normal, (0,0,0), (24, 10), 2) # Oeil

    # [MODIFICATION] Added 'other_sheeps' parameter for collision check
    def update(self, map_obj, other_sheeps):
        # Mouvement aléatoire
        self.move_timer += 1
        if self.move_timer > 50: 
            self.dx = random.choice([-2, 0, 2])
            self.dy = random.choice([-2, 0, 2])
            self.move_timer = 0
            
        new_x = self.rect.x + self.dx
        new_y = self.rect.y + self.dy
        
        # 1. Limites de l'écran
        if new_x < 0: new_x = 0
        if new_y < 0: new_y = 0
        if new_x > map_obj.pixel_width - self.width: new_x = map_obj.pixel_width - self.width
        if new_y > map_obj.pixel_height - self.height: new_y = map_obj.pixel_height - self.height
        
        # Collisions
        future_rect = pygame.Rect(new_x, new_y, self.width, self.height)
        
        # A. Map Obstacles
        if map_obj.is_blocked(new_x, new_y, self.width, self.height): return 
        
        # B. Sprites (Trees, etc.)
        for s in sprites:
            if future_rect.colliderect(s.rect): return 

        # C. [NEW] Other Sheeps
        for s in other_sheeps:
            if s is not self: # Don't check collision with yourself
                if future_rect.colliderect(s.rect):
                    return # Stop moving if hitting another sheep

        self.rect.x = new_x
        self.rect.y = new_y

    def draw(self, surface, camera, current_filter):
        screen_pos = (self.rect.x - camera.x, self.rect.y - camera.y)
        
        if current_filter == "snake":
            if self.is_robot:
                pygame.draw.rect(surface, (0, 0, 0), (*screen_pos, self.width, self.height))
            else:
                pygame.draw.rect(surface, (255, 255, 255), (*screen_pos, self.width, self.height))
        else:
            surface.blit(self.image_normal, screen_pos)

# --- FONCTION PRINCIPALE ---
def run(screen, remaining_time):
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    
    # Nettoyer les sprites précédents
    sprites.clear()

    # Chargement Map
    tile_kinds = [
        TileKind("dirt", "images/dirt.png", False),
        TileKind("grass", "images/grass.png", False),
        TileKind("water", "images/water.png", True), 
        TileKind("wood", "images/wood.png", False)
    ]
    game_map = Map("maps/start.map", tile_kinds, 32)
    
    # Joueur au centre
    player = Player("images/Man.png", 32*5, 32*5)
    
    # Création des Arbres (Obstacles)
    Sprite("images/tree.png", 0 * 32, 0 * 32)
    Sprite("images/tree.png", 7 * 32, 2 * 32)
    Sprite("images/tree.png", 12* 32, -1* 32)
    Sprite("images/tree.png", 14* 32, 9 * 32)
    Sprite("images/tree.png", 12* 32, -1* 32)
    Sprite("images/tree.png", 13* 32, 12* 32)
    Sprite("images/tree.png", 20* 32, 9 * 32)
    Sprite("images/tree.png", 22* 32, -1* 32)
    Sprite("images/tree.png", 24* 32, 12* 32)
    Sprite("images/tree.png", 2 * 32, 8 * 32)
    Sprite("images/tree.png", 15* 32, 15* 32)
    Sprite("images/tree.png", 17 * 32, 1 * 32)
    Sprite("images/tree.png", 1 * 32, 15 * 32)
    Sprite("images/tree.png", 27 * 32, 5 * 32)
    Sprite("images/tree.png", 10 * 32, 21 * 32)
    
    # Génération des moutons 
    sheeps = []
    def is_pos_valid(x, y, w, h):
        rect = pygame.Rect(x, y, w, h)
        if game_map.is_blocked(x, y, w, h): return False
        for s in sprites:
            if rect.colliderect(s.rect): return False
        
        # [MODIFICATION] Check against already created sheeps during generation
        for s in sheeps:
            if rect.colliderect(s.rect): return False
            
        return True

    total_sheep = 15
    created = 0
    # Add a failsafe loop counter to prevent infinite loops if map is full
    failsafe = 0
    while created < total_sheep and failsafe < 2000:
        rx = random.randint(100, 800)
        ry = random.randint(100, 600)
        is_robot = (created == total_sheep - 1)
        if is_pos_valid(rx, ry, 30, 30):
            sheeps.append(Sheep(rx, ry, is_robot=is_robot))
            created += 1
        failsafe += 1
    
    camera = pygame.Rect(0, 0, screen.get_width(), screen.get_height())
    current_filter = None
    game_state = "PLAYING"
    message = ""

    running = True
    while running:
        dt = clock.get_time() / 1000.0
        
        # --- TIMER LOGIC ---
        if game_state == "PLAYING":
            remaining_time -= dt
            if remaining_time <= 0:
                remaining_time = 0
                game_state = "LOST"
                message = "TEMPS ECOULE ! GAME OVER"
        
        # --- EVENEMENTS ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            
            if event.type == pygame.KEYDOWN:
                keys_down.add(event.key)
                if event.key == pygame.K_ESCAPE: return
                
                # [CORRECTION] Gestion de la transition vers Niveau 2
                if game_state == "WON":
                    if event.key == pygame.K_RETURN: # Touche Entrée
                        level2.run(screen, remaining_time)
                        return # Quitter le niveau 1
                
                # Filtres & Jeu
                if game_state == "PLAYING":
                    if event.key == pygame.K_0: current_filter = None
                    if event.key == pygame.K_1: current_filter = "dog"
                    if event.key == pygame.K_2: current_filter = "bee"
                    if event.key == pygame.K_3: current_filter = "eagle"
                    if event.key == pygame.K_4: current_filter = "bat"
                    if event.key == pygame.K_5: current_filter = "fish"
                    if event.key == pygame.K_6: current_filter = "snake"
                    
                    # Action capture
                    if event.key == pygame.K_SPACE:
                        hit_sheep = None
                        for s in sheeps:
                            if player.rect.colliderect(s.rect):
                                hit_sheep = s
                                break
                        if hit_sheep:
                            if hit_sheep.is_robot:
                                game_state = "WON"
                                message = "BRAVO ! Robot neutralise."
                            else:
                                game_state = "LOST"
                                message = "ECHEC ! C'etait un vrai animal."

            elif event.type == pygame.KEYUP:
                if event.key in keys_down:
                    keys_down.remove(event.key)

        # --- UPDATE ---
        if game_state == "PLAYING":
            player.update(game_map)
            for s in sheeps:
                # [MODIFICATION] Pass the full list of sheeps to update
                s.update(game_map, sheeps)
                
            camera.center = player.rect.center
            camera.x = max(0, min(camera.x, game_map.pixel_width - camera.width))
            camera.y = max(0, min(camera.y, game_map.pixel_height - camera.height))

        # --- DESSIN ---
        screen.fill((30, 150, 50))
        game_map.draw(screen, camera)
        
        for s in sprites:
            s.draw(screen, camera)
        for s in sheeps:
            s.draw(screen, camera, current_filter)
            
        if current_filter == "snake": screen.blit(apply_snake_vision(screen), (0,0))
        elif current_filter == "bee": screen.blit(apply_bee_vision(screen), (0,0))
        elif current_filter == "bat": screen.blit(apply_bat_vision(screen), (0,0))
        elif current_filter == "eagle":
            pos = (player.rect.centerx - camera.x, player.rect.centery - camera.y)
            screen.blit(apply_eagle_vision(screen, pos), (0,0))
        elif current_filter == "dog": screen.blit(apply_dog_vision(screen), (0,0))
        elif current_filter == "fish": screen.blit(apply_deepsea_vision(screen), (0,0))

        # HUD
        if game_state == "PLAYING":
            col = (255, 255, 255)
            if current_filter == "snake": col = (200, 200, 255) 
            
            lbl = font.render("MISSION : SANG-FROID", True, col)
            screen.blit(lbl, (20, 20))
            
            # --- DISPLAY TIMER ---
            timer_col = (255, 255, 255) if remaining_time > 30 else (255, 0, 0)
            timer_txt = font.render(f"TEMPS: {int(remaining_time)}", True, timer_col)
            screen.blit(timer_txt, (screen.get_width() // 2 - timer_txt.get_width() // 2, 20))
        
            hint = font.render("Au milieu de la vie, un coeur de pierre ne bat pas.", True, (200, 200, 200))
            screen.blit(hint, (20, 40))
            hint = font.render("Cherchez celui qui ne degage aucune chaleur.", True, (200, 200, 200))
            screen.blit(hint, (20, 60))
            visions = [
                "1 - dog",
                "2 - bee",
                "3 - eagle",
                "4 - bat",
                "5 - fish",
                "6 - snake"
            ]
            
            for i, line in enumerate(visions):
                txt_surf = font.render(line, True, (255, 255, 255))
                # Position: Right aligned with 20px padding
                screen.blit(txt_surf, (screen.get_width() - txt_surf.get_width() - 20, 20 + i * 30))
        
        else:
            # Ecran Fin
            overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0,0))
            
            center_x = screen.get_width() // 2
            center_y = screen.get_height() // 2

            if game_state == "WON":
                col = (0, 255, 0)
                txt = font.render(message, True, col)
                txt2 = font.render("Appuyez sur ENTREE pour le Niveau 2", True, (255, 255, 255))
                
            else:
                col = (255, 50, 50)
                txt = font.render(message, True, col)
                txt2 = font.render("Appuyez sur ECHAP pour quitter", True, (255, 255, 255))
            screen.blit(txt, (center_x - txt.get_width()//2, center_y - 30))
            screen.blit(txt2, (center_x - txt2.get_width()//2, center_y + 30))

        pygame.display.flip()
        clock.tick(60)