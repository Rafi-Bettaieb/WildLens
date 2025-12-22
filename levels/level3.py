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

from player import Player
from sprite import Sprite, sprites
from input import keys_down 
from filters import apply_bat_vision

# --- 1. CARTE FANTOME ---
class DummyMap:
    def __init__(self, width, height):
        self.pixel_width = width
        self.pixel_height = height
    
    def is_blocked(self, x, y, w, h):
        return False

# --- 2. CONFIGURATION DU LABYRINTHE ---
BLOCK_SIZE = 32
MAZE_LAYOUT = [
    "1111111111110E01111111111111", # Exit (Top Center)
    "1000001000000000001000001001",
    "1011101011111111101111101011",
    "1010001000000010100000101001",
    "1010111111111010111110101101",
    "1000100000001000000010100001",
    "1110101111101111111010111111", 
    "1000101000100000001010000001",
    "1110101010111111101011111101", 
    "1000100010000000101000000101",
    "1111111010111110101111110101",
    "1000001010000010100000010101",
    "1011101011111010111111010101",
    "1010001000001000000001010001", 
    "1010111111101111111101011101",
    "1010000000101000000101000101",
    "1011111110101011110101110101",
    "1000000010100010010100010101",
    "1111110010111010010111010101",
    "100000S000000010000000010001", # Start (Bottom Left)
    "1111111111111111111111111111"
]

LEVEL_WIDTH = len(MAZE_LAYOUT[0]) * BLOCK_SIZE
LEVEL_HEIGHT = len(MAZE_LAYOUT) * BLOCK_SIZE

# --- 3. CLASSE CIBLE (PAPILLON) ---
class Moth:
    def __init__(self, x, y):
        self.width = 16
        self.height = 16
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.start_x = x
        self.start_y = y
        self.timer = 0

    def update(self):
        self.timer += 0.1
        self.rect.x = self.start_x + math.sin(self.timer) * 5
        self.rect.y = self.start_y + math.cos(self.timer) * 5

    def draw(self, surface, camera):
        screen_pos = (self.rect.x - camera.x, self.rect.y - camera.y)
        p1 = (screen_pos[0] + 8, screen_pos[1])
        p2 = (screen_pos[0], screen_pos[1] + 16)
        p3 = (screen_pos[0] + 16, screen_pos[1] + 16)
        pygame.draw.polygon(surface, (255, 255, 255), [p1, p2, p3])

# --- 4. FONCTION PRINCIPALE ---
def run(screen, remaining_time):
    clock = pygame.time.Clock()
    
    font = pygame.font.Font(None, 36)
    font_large = pygame.font.Font(None, 74) 
    font_btn = pygame.font.Font(None, 50)   
    
    exit_button_rect = pygame.Rect(screen.get_width()//2 - 100, screen.get_height()//2 + 60, 200, 60)
    
    sprites.clear()
    dummy_map = DummyMap(LEVEL_WIDTH, LEVEL_HEIGHT)
    
    player = None
    moth = None
    
    for row_idx, row_str in enumerate(MAZE_LAYOUT):
        for col_idx, char in enumerate(row_str):
            x = col_idx * BLOCK_SIZE
            y = row_idx * BLOCK_SIZE
            
            if char == "1": Sprite("images/wood.png", x, y)
            elif char == "S": player = Player("images/Man.png", x, y)
            elif char == "E": moth = Moth(x, y)
    
    if player is None: player = Player("images/man.png", 100, 100)
    if moth is None: moth = Moth(100, 50)

    camera = pygame.Rect(0, 0, screen.get_width(), screen.get_height())
    current_filter = None
    game_state = "PLAYING"

    running = True
    while running:
        dt = clock.get_time() / 1000.0
        
        # --- TIMER LOGIC ---
        if game_state == "PLAYING":
            remaining_time -= dt
            if remaining_time <= 0:
                remaining_time = 0
                game_state = "LOST"

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            
            if game_state == "WON" or game_state == "LOST":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if exit_button_rect.collidepoint(event.pos): return 
            
            if event.type == pygame.KEYDOWN:
                keys_down.add(event.key)
                if event.key == pygame.K_ESCAPE: return
                
                if game_state == "PLAYING":
                    # [MODIFICATION] Toutes les touches de vision fonctionnent
                    # Filtres
                    if event.key == pygame.K_0: current_filter = None
                    if event.key == pygame.K_1: current_filter = "dog"
                    if event.key == pygame.K_2: current_filter = "bee"
                    if event.key == pygame.K_3: current_filter = "eagle"
                    if event.key == pygame.K_4: current_filter = "bat"
                    if event.key == pygame.K_5: current_filter = "fish"
                    if event.key == pygame.K_6: current_filter = "snake"
                    
            elif event.type == pygame.KEYUP:
                if event.key in keys_down:
                    keys_down.remove(event.key)

        # --- UPDATE ---
        if game_state == "PLAYING":
            player.update(dummy_map)
            moth.update()
            
            if player.rect.colliderect(moth.rect):
                game_state = "WON"
                pygame.mouse.set_visible(True)

            camera.center = player.rect.center
            camera.x = max(0, min(camera.x, LEVEL_WIDTH - camera.width))
            camera.y = max(0, min(camera.y, LEVEL_HEIGHT - camera.height))

        # --- DESSIN ---
        screen.fill((0, 0, 0)) # Fond Noir de base
        
        # On dessine le jeu (mais il ne sera visible que si le filtre le permet)
        for s in sprites: s.draw(screen, camera)
        moth.draw(screen, camera)
        player.draw(screen, camera)

        # [MODIFICATION] Gestion de la visibilité selon le filtre
        if current_filter == "bat":
            # Seul le sonar révèle les murs (contours)
            bat_view = apply_bat_vision(screen)
            screen.blit(bat_view, (0, 0))
        else:
            # Pour TOUS les autres filtres (ou aucun), c'est noir.
            # (Les autres animaux ne voient pas dans le noir total)
            screen.fill((0, 0, 0))

        # --- HUD ---
        if game_state == "PLAYING":
            col = (255, 255, 255)
            
            # Affichage du nom de la vision active
            vision_name = "Humaine (Aveugle)"
            if current_filter == "snake": vision_name = "Serpent (Aveugle)"
            elif current_filter == "bee": vision_name = "Abeille (Aveugle)"
            elif current_filter == "bat": vision_name = "Chauve-Souris (Sonar Actif)"
            elif current_filter == "eagle": vision_name = "Aigle (Aveugle)"
            elif current_filter == "dog": vision_name = "Chien (Aveugle)"
            elif current_filter == "fish": vision_name = "Poisson (Aveugle)"

            # Couleur du texte : Vert si Bat, Gris sinon
            text_col = (255, 255, 255)
            
            screen.blit(font.render(f"NIVEAU 3 : ECHOLOCALISATION", True, text_col), (20, 20))
            screen.blit(font.render("Il fait noir complet.Criez pour voir les murs", True, (200, 200, 200)), (20, 60))
            
            # --- DISPLAY TIMER ---
            timer_col = (255, 255, 255) if remaining_time > 30 else (255, 0, 0)
            timer_txt = font.render(f"TEMPS: {int(remaining_time)}", True, timer_col)
            screen.blit(timer_txt, (screen.get_width() // 2 - timer_txt.get_width() // 2, 20))

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
        
        elif game_state == "WON":
            overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            screen.blit(overlay, (0,0))
            
            txt_won = font_large.render("GAME OVER - YOU WON", True, (0, 255, 0))
            rect_won = txt_won.get_rect(center=(screen.get_width()//2, screen.get_height()//2 - 50))
            screen.blit(txt_won, rect_won)
            
            pygame.draw.rect(screen, (200, 200, 200), exit_button_rect) 
            pygame.draw.rect(screen, (255, 255, 255), exit_button_rect, 3) 
            
            txt_btn = font_btn.render("QUITTER", True, (0, 0, 0))
            rect_btn = txt_btn.get_rect(center=exit_button_rect.center)
            screen.blit(txt_btn, rect_btn)
            
        elif game_state == "LOST":
            overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            screen.blit(overlay, (0,0))
            
            txt_lost = font_large.render("TEMPS ÉCOULÉ - PERDU", True, (255, 0, 0))
            rect_lost = txt_lost.get_rect(center=(screen.get_width()//2, screen.get_height()//2 - 50))
            screen.blit(txt_lost, rect_lost)
            
            pygame.draw.rect(screen, (200, 200, 200), exit_button_rect) 
            pygame.draw.rect(screen, (255, 255, 255), exit_button_rect, 3) 
            
            txt_btn = font_btn.render("QUITTER", True, (0, 0, 0))
            rect_btn = txt_btn.get_rect(center=exit_button_rect.center)
            screen.blit(txt_btn, rect_btn)

        pygame.display.flip()
        clock.tick(60)