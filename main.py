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

# Colors
MENU_BG_COLOR = (50, 50, 50)
BUTTON_COLOR = (200, 200, 200)
TEXT_COLOR = (0, 0, 0)
GREEN_TEXT = (30, 150, 50)

# --- FONTS SETUP ---
# title_font for the big header and buttons
title_font = pygame.font.Font(None, 60) 
# small_font for the story text (Minimized size)
small_font = pygame.font.Font(None, 28) 

# --- GLOBAL TIMER SETTING ---
GLOBAL_TIME_LIMIT = 100 # 100 seconds total for all levels

# --- MUSIC SETUP ---
music_path = os.path.join("sounds", "music.mp3") 

if os.path.exists(music_path):
    try:
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.3)
    except pygame.error as e:
        print(f"Error loading music: {e}")
else:
    print(f"Warning: Music file not found at {music_path}.")

# --- MENU SETUP ---
# I moved these LOWER (y=400 and y=480) so they don't overlap with the text
start_rect = pygame.Rect(screen_width // 2 - 150, 400, 300, 50)
quit_rect = pygame.Rect(screen_width // 2 - 150, 480, 300, 50)

def draw_text_centered(text, rect, surf, font_to_use):
    text_surf = font_to_use.render(text, True, TEXT_COLOR)
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
                    # --- LANCER LE NIVEAU 1 ---
                    level1.run(screen, GLOBAL_TIME_LIMIT)
                    # Reset screen when level finishes
                    pygame.display.set_mode((screen_width, screen_height))
                    
                elif quit_rect.collidepoint(event.pos):
                    running = False

    # 2. DESSIN DU MENU
    screen.fill(MENU_BG_COLOR)
    
    # --- A. Draw the Main Title (Big Font) ---
    title_surface = title_font.render("Welcome To The Game : WILDLENS", True, GREEN_TEXT)
    screen.blit(title_surface, (screen_width//2 - title_surface.get_width()//2, 50))

    # --- B. Draw the Story Text (Small Font) ---
    story_lines = [
        "Agent, listen closely.",
        "A corrupt corporation has replaced nature with a perfect lie.",
        "Use your WildLens to strip away the camouflage",
        "and expose the truth hidden underneath.",
        "",
        "Good luck."
    ]

    current_y = 130 
    spacing = 35  # Tighter spacing for smaller font

    for line in story_lines:
        # Use small_font here
        text_surface = small_font.render(line, True, GREEN_TEXT)
        # Center the text
        text_x = screen_width // 2 - text_surface.get_width() // 2
        screen.blit(text_surface, (text_x, current_y))
        
        current_y += spacing

    # --- C. Draw Buttons ---
    pygame.draw.rect(screen, BUTTON_COLOR, start_rect)
    pygame.draw.rect(screen, BUTTON_COLOR, quit_rect)
    
    # Use title_font for buttons so they are easy to read
    draw_text_centered("START", start_rect, screen, title_font)
    draw_text_centered("QUITTER", quit_rect, screen, title_font)
        
    pygame.display.flip()

pygame.quit()