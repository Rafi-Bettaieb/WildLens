import pygame
import sys
import os
import random
import math

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

# [MODIFICATION] Import du Niveau 3 pour la transition
import levels.level3 as level3

# --- CLASSE FLEUR ---
class Flower:
    def __init__(self, x, y, is_target=False):
        self.width = 20
        self.height = 20
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.is_target = is_target
        self.pulse = 0

    def update(self, map_obj):
        # Animation simple de pulsation pour la cible
        if self.is_target:
            self.pulse = (self.pulse + 0.1) % (2 * math.pi)

    def draw(self, surface, camera, current_filter):
        screen_pos = (self.rect.x - camera.x, self.rect.y - camera.y)
        center = (screen_pos[0] + 10, screen_pos[1] + 10)
        
        # --- LOGIQUE VISUELLE ---
        if current_filter == "bee":
            # VISION ABEILLE (UV)
            if self.is_target:
                # 1. Halo extérieur (Bleu électrique qui pulse)
                radius_halo = 12 + math.sin(self.pulse * 5) * 3
                pygame.draw.circle(surface, (0, 0, 255), center, int(radius_halo)) 
                
                # 2. Pétales (Bleu Ciel Lumineux)
                pygame.draw.circle(surface, (50, 150, 255), center, 8) 
                
                # 3. Coeur (Blanc pur pour contraste max)
                pygame.draw.circle(surface, (255, 255, 255), center, 4) 
                
            else:
                # Les fausses fleurs (Jaune -> devient verdâtre avec filtre)
                pygame.draw.circle(surface, (255, 255, 0), center, 8) 
                pygame.draw.circle(surface, (100, 100, 0), center, 4)
        else:
            # VISION NORMALE
            pygame.draw.circle(surface, (255, 255, 0), center, 8)
            pygame.draw.circle(surface, (255, 150, 0), center, 3)

# --- FONCTION PRINCIPALE ---
def run(screen, remaining_time):
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    
    # Nettoyer les sprites
    sprites.clear()

    # Chargement Map
    tile_kinds = [
        TileKind("dirt", "images/dirt.png", False),
        TileKind("grass", "images/grass.png", False),
        TileKind("water", "images/water.png", True), 
        TileKind("wood", "images/wood.png", False)
    ]
    game_map = Map("maps/start.map", tile_kinds, 32)
    
    # Joueur
    player = Player("images/Man.png", 32*5, 32*5)
    
    # --- CREATION DES OBSTACLES (ARBRES) ---
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
    Sprite("images/tree.png", 27 * 32, 5 * 32)
    Sprite("images/tree.png", 10 * 32, 21 * 32)
    
    # --- GENERATION DES FLEURS ---
    flowers = []
    
    def is_pos_valid(x, y, w, h):
        rect = pygame.Rect(x, y, w, h)
        if game_map.is_blocked(x, y, w, h): return False
        for s in sprites:
            if rect.colliderect(s.rect): return False
        return True

    total_flowers = 30
    created = 0

    
    failsafe = 0 
    
    while created < total_flowers and failsafe < 2000:
        rx = random.randint(50, 800)
        ry = random.randint(50, 600)
        
        # --- NEW: Distance Check ---
        too_close = False
        for f in flowers:
            # Check distance (Euclidean) between new position and existing flowers
            dist = math.hypot(rx - f.rect.x, ry - f.rect.y)
            if dist < 60:  # Minimum 60 pixels apart
                too_close = True
                break
        
        if not too_close:
            is_target = (created == total_flowers - 1)
            
            if is_pos_valid(rx, ry, 20, 20):
                flowers.append(Flower(rx, ry, is_target=is_target))
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
                
                # [MODIFICATION] Transition vers le Niveau 3
                if game_state == "WON":
                    if event.key == pygame.K_RETURN:
                        level3.run(screen, remaining_time)
                        return # Quitter le niveau 2

                # Filtres
                if event.key == pygame.K_0: current_filter = None
                if event.key == pygame.K_1: current_filter = "dog"
                if event.key == pygame.K_2: current_filter = "bee"
                if event.key == pygame.K_3: current_filter = "eagle"
                if event.key == pygame.K_4: current_filter = "bat"
                if event.key == pygame.K_5: current_filter = "fish"
                if event.key == pygame.K_6: current_filter = "snake"
                
                # Action
                if event.key == pygame.K_SPACE and game_state == "PLAYING":
                    picked_flower = None
                    for f in flowers:
                        if player.rect.colliderect(f.rect):
                            picked_flower = f
                            break
                    
                    if picked_flower:
                        if picked_flower.is_target:
                            game_state = "WON"
                            message = "BRAVO ! Nectar trouve."
                        else:
                            game_state = "LOST"
                            message = "ECHEC ! Mauvaise fleur."

            elif event.type == pygame.KEYUP:
                if event.key in keys_down:
                    keys_down.remove(event.key)

        # --- UPDATE ---
        if game_state == "PLAYING":
            player.update(game_map)
            for f in flowers:
                f.update(game_map)
                
            camera.center = player.rect.center
            camera.x = max(0, min(camera.x, game_map.pixel_width - camera.width))
            camera.y = max(0, min(camera.y, game_map.pixel_height - camera.height))

        # --- DESSIN ---
        screen.fill((30, 150, 50))
        game_map.draw(screen, camera)
        
        for s in sprites: s.draw(screen, camera)

        for f in flowers:
            f.draw(screen, camera, current_filter)
            
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
            lbl = font.render("MISSION : Nectare", True, col)
            screen.blit(lbl, (20, 20))
            
            # --- DISPLAY TIMER ---
            timer_col = (255, 255, 255) if remaining_time > 30 else (255, 0, 0)
            timer_txt = font.render(f"TEMPS: {int(remaining_time)}", True, timer_col)
            screen.blit(timer_txt, (screen.get_width() // 2 - timer_txt.get_width() // 2, 20))

            hint = font.render("La nature cache des pistes d'atterrissage", True, (200, 200, 200))
            screen.blit(hint, (20, 40))
    
            hint = font.render("Trouvez la fleur elue par le soleil.", True, (200, 200, 200))
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
            # Fin de partie
            overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0,0))
            
            c_res = (0, 255, 0)
            txt_res = font.render(message, True, c_res)
            
            # [MODIFICATION] Message de suite
            if game_state == "WON":
                col = (0, 255, 0)
                txt_quit = font.render("Appuyez sur ENTREE pour le Niveau 3", True, col)
            else:
                col = (255, 50, 50)
                txt_quit = font.render("Appuyez sur ECHAP pour quitter", True, col)
                
            center_x = screen.get_width() // 2
            center_y = screen.get_height() // 2
            
            screen.blit(txt_res, (center_x - txt_res.get_width()//2, center_y - 30))
            screen.blit(txt_quit, (center_x - txt_quit.get_width()//2, center_y + 30))

        pygame.display.flip()
        clock.tick(60)