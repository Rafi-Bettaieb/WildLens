import pygame
import sys
import os
# Import your level
import levels.level1 as level1

# --- CONFIGURATION ---
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 675
FPS = 60

# --- COLOR PALETTE (Tech / Nature Theme) ---
COLOR_BG = (20, 24, 28)           # Dark Slate (Background)
COLOR_ACCENT = (0, 255, 128)      # Neon Green (Tech Nature)
COLOR_TEXT_MAIN = (240, 240, 240) # Off-White (Readable text)
COLOR_TEXT_DIM = (160, 170, 180)  # Grey (Subtitles)
COLOR_BTN_NORMAL = (40, 50, 60)   # Dark Button
COLOR_BTN_HOVER = (60, 80, 100)   # Lighter Button
COLOR_SHADOW = (10, 10, 10)       # Drop shadow

# --- SETUP ---
pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("WildLens - Adventure")
clock = pygame.time.Clock()

# --- ASSET MANAGER ---
def get_font(name, size, bold=False):
    """Returns a system font to avoid 'None' default font look."""
    # Tries to find specific fonts, falls back to default if not found
    font_name = pygame.font.match_font(name)
    if not font_name:
        font_name = pygame.font.get_default_font()
    return pygame.font.Font(font_name, size)

# Fonts
font_title = get_font('impact', 70)       # Bold Title
font_subtitle = get_font('arial', 22)     # Clean story text
font_button = get_font('arial', 30, bold=True)

# --- SOUND MANAGER ---
def play_music():
    music_path = os.path.join("sounds", "music.mp3")
    if os.path.exists(music_path):
        try:
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.3)
        except pygame.error as e:
            print(f"Audio Error: {e}")
    else:
        print("Music file not found, skipping.")

play_music()

# --- UI CLASSES ---
class Button:
    def __init__(self, text, x, y, width, height, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.is_hovered = False

    def draw(self, surface):
        # Determine color based on hover state
        color = COLOR_BTN_HOVER if self.is_hovered else COLOR_BTN_NORMAL
        border_color = COLOR_ACCENT if self.is_hovered else (80, 90, 100)

        # Draw Shadow
        shadow_rect = self.rect.copy()
        shadow_rect.move_ip(4, 4)
        pygame.draw.rect(surface, COLOR_SHADOW, shadow_rect, border_radius=12)

        # Draw Main Button Body (Rounded)
        pygame.draw.rect(surface, color, self.rect, border_radius=12)
        
        # Draw Border
        pygame.draw.rect(surface, border_color, self.rect, 2, border_radius=12)

        # Draw Text
        text_surf = font_button.render(self.text, True, COLOR_TEXT_MAIN)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def update(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def check_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered and self.action:
                self.action()

# --- HELPER FUNCTIONS ---
def draw_background_grid(surface):
    """Draws a subtle tech grid in the background."""
    surface.fill(COLOR_BG)
    grid_color = (30, 35, 40)
    gap = 40
    for x in range(0, SCREEN_WIDTH, gap):
        pygame.draw.line(surface, grid_color, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, gap):
        pygame.draw.line(surface, grid_color, (0, y), (SCREEN_WIDTH, y))

def draw_title_centered(text, y_pos):
    # Shadow
    shadow_surf = font_title.render(text, True, COLOR_SHADOW)
    screen.blit(shadow_surf, (SCREEN_WIDTH//2 - shadow_surf.get_width()//2 + 4, y_pos + 4))
    # Main Text
    text_surf = font_title.render(text, True, COLOR_ACCENT)
    screen.blit(text_surf, (SCREEN_WIDTH//2 - text_surf.get_width()//2, y_pos))

def draw_story_block(lines, start_y):
    current_y = start_y
    spacing = 28
    
    for line in lines:
        text_surf = font_subtitle.render(line, True, COLOR_TEXT_DIM)
        # Add a subtle background box for readability if needed, but clean text is nice
        text_rect = text_surf.get_rect(center=(SCREEN_WIDTH // 2, current_y))
        screen.blit(text_surf, text_rect)
        current_y += spacing

# --- ACTIONS ---
def start_game():
    global_time_limit = 180
    level1.run(screen, global_time_limit)
    # Re-setup display after level returns (just in case level changed it)
    pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("WildLens - Menu")

def quit_game():
    pygame.quit()
    sys.exit()

# --- MAIN EXECUTION ---

# Create Buttons
btn_start = Button("START MISSION", SCREEN_WIDTH//2 - 125, 480, 250, 60, start_game)
btn_quit = Button("QUIT", SCREEN_WIDTH//2 - 125, 560, 250, 60, quit_game)
buttons = [btn_start, btn_quit]

story_lines = [
    "Agent, écoutez attentivement.",
    "Une corporation corrompue a remplacé la nature par un mensonge parfait.",
    "Utilisez votre WildLens pour retirer le camouflage",
    "et révéler la vérité cachée en dessous.",
    "", # Empty line for spacing
    "Pour progresser, sélectionnez la vision adaptée à chaque situation",
    "en utilisant les indices.",
    "", # Empty line for spacing
    "Bonne chance."
]

running = True

while running:
    # 1. Event Handling
    mouse_pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        for btn in buttons:
            btn.check_click(event)

    # 2. Update State
    for btn in buttons:
        btn.update(mouse_pos)

    # 3. Drawing
    draw_background_grid(screen)
    
    # Draw Logo/Title
    draw_title_centered("WILDLENS", 50)
    
    # Draw Story
    draw_story_block(story_lines, 160)
    
    # Draw Buttons
    for btn in buttons:
        btn.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()