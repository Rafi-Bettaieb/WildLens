import pygame
import sys
import os
# Import du dossier levels
import levels.level1 as level1

pygame.init()
pygame.mixer.init() # Initialize the mixer module for sound

pygame.display.set_caption("WildLens - Adventure")
screen_width = 900
screen_height = 675
screen = pygame.display.set_mode((screen_width, screen_height))

# Colors & Font for Menu
MENU_BG_COLOR = (50, 50, 50)
BUTTON_COLOR = (200, 200, 200)
TEXT_COLOR = (0, 0, 0)
font = pygame.font.Font(None, 50)

# --- GLOBAL TIMER SETTING ---
GLOBAL_TIME_LIMIT = 100 # 100 secondes total for all levels

# --- MUSIC SETUP ---
# Path to your music file 
music_path = os.path.join("sounds", "music.mp3") 

# Check if file exists to prevent crashing if missing
if os.path.exists(music_path):
    try:
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play(-1) # -1 means loop indefinitely
        pygame.mixer.music.set_volume(0.3) # Set volume (0.0 to 1.0)
    except pygame.error as e:
        print(f"Error loading music: {e}")
else:
    print(f"Warning: Music file not found at {music_path}. Please add 'music.mp3' to a 'sounds' folder.")

# --- MENU SETUP ---
start_rect = pygame.Rect(screen_width // 2 - 150, screen_height // 2 - 60, 300, 50)
quit_rect = pygame.Rect(screen_width // 2 - 150, screen_height // 2 + 20, 300, 50)

def draw_text_centered(text, rect, surf):
    text_surf = font.render(text, True, TEXT_COLOR)
    text_rect = text_surf.get_rect(center=rect.center)
    surf.blit(text_surf, text_rect)

running = True

while running:
    # 1. GESTION DU MENU
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Clic gauche
                if start_rect.collidepoint(event.pos):
                    # --- LANCER LE NIVEAU 1 AVEC LE CHRONO GLOBAL ---
                    level1.run(screen, GLOBAL_TIME_LIMIT)
                    
                    # Quand le niveau est fini (return), on remet la config écran menu
                    pygame.display.set_mode((screen_width, screen_height))
                    
                elif quit_rect.collidepoint(event.pos):
                    running = False

    # 2. DESSIN DU MENU
    screen.fill(MENU_BG_COLOR)
    
    # Titre
    title = font.render("WILDLENS", True, (30, 150, 50))
    screen.blit(title, (screen_width//2 - title.get_width()//2, 100))
    
    # Boutons
    pygame.draw.rect(screen, BUTTON_COLOR, start_rect)
    pygame.draw.rect(screen, BUTTON_COLOR, quit_rect)
    
    draw_text_centered("START", start_rect, screen)
    draw_text_centered("QUITTER", quit_rect, screen)
        
    pygame.display.flip()

pygame.quit()