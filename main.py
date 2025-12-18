import pygame
import sys
# Import du dossier levels
import levels.level1 as level1

pygame.init()

pygame.display.set_caption("WildLens - Adventure")
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Colors & Font for Menu
MENU_BG_COLOR = (50, 50, 50)
BUTTON_COLOR = (200, 200, 200)
TEXT_COLOR = (0, 0, 0)
font = pygame.font.Font(None, 50)

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
                    # --- LANCER LE NIVEAU 1 (2D) ---
                    level1.run(screen)
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